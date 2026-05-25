from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


HEADING_KEYWORDS = {
    "abstract",
    "introduction",
    "background",
    "related work",
    "methods",
    "method",
    "materials and methods",
    "experiments",
    "results",
    "discussion",
    "conclusion",
    "conclusions",
    "limitations",
    "references",
    "acknowledgments",
    "acknowledgements",
    "appendix",
}

PAGE_NUMBER_RE = re.compile(r"^(page\s+)?\d+\s*$", re.IGNORECASE)
NUMBERED_HEADING_RE = re.compile(r"^(\d+(?:\.\d+)*)[\.)]?\s+(.+)$")
ABSTRACT_PREFIX_RE = re.compile(r"^abstract\s*[:\-—.]?\s*(.*)$", re.IGNORECASE)
KEYWORDS_PREFIX_RE = re.compile(r"^(keywords?|index terms)\s*[:\-—.]\s*(.*)$", re.IGNORECASE)


@dataclass
class Segment:
    index: int
    page_number: int
    page_height: float
    y0: float
    y1: float
    text: str
    word_count: int
    line_count: int
    avg_size: float
    max_size: float
    bold_ratio: float


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def merge_line_texts(lines: Sequence[str]) -> str:
    merged = ""
    for raw_line in lines:
        line = normalize_text(raw_line)
        if not line:
            continue
        if not merged:
            merged = line
            continue
        if merged.endswith("-") and line[:1].islower():
            merged = merged[:-1] + line
        elif merged.endswith(("(", "[", "/")) or line.startswith((".", ",", ";", ":", ")", "]")):
            merged += line
        else:
            merged += " " + line
    return merged.strip()


def import_fitz():
    try:
        import fitz
    except ImportError as exc:
        raise SystemExit(
            "PyMuPDF is required. Install it with: pip install pymupdf"
        ) from exc
    return fitz


def extract_segments(pdf_path: Path) -> List[Segment]:
    fitz = import_fitz()
    document = fitz.open(pdf_path)
    segments: List[Segment] = []
    index = 0

    for page_idx, page in enumerate(document, start=1):
        page_height = float(page.rect.height)
        text_dict = page.get_text("dict", sort=True)

        for block in text_dict.get("blocks", []):
            if block.get("type") != 0:
                continue

            line_texts: List[str] = []
            weighted_sizes = 0.0
            total_chars = 0
            bold_chars = 0
            max_size = 0.0
            y0 = None
            y1 = None

            for line in block.get("lines", []):
                spans = [span for span in line.get("spans", []) if normalize_text(span.get("text", ""))]
                if not spans:
                    continue

                text = "".join(span.get("text", "") for span in spans)
                text = normalize_text(text)
                if not text:
                    continue

                line_texts.append(text)
                bbox = line.get("bbox", [0, 0, 0, 0])
                y0 = bbox[1] if y0 is None else min(y0, bbox[1])
                y1 = bbox[3] if y1 is None else max(y1, bbox[3])

                for span in spans:
                    span_text = span.get("text", "")
                    char_count = max(len(span_text.strip()), 1)
                    size = float(span.get("size", 0.0))
                    font_name = str(span.get("font", "")).lower()
                    weighted_sizes += size * char_count
                    total_chars += char_count
                    max_size = max(max_size, size)
                    if "bold" in font_name:
                        bold_chars += char_count

            if not line_texts or total_chars == 0 or y0 is None or y1 is None:
                continue

            text = merge_line_texts(line_texts)
            if not text:
                continue

            segments.append(
                Segment(
                    index=index,
                    page_number=page_idx,
                    page_height=page_height,
                    y0=float(y0),
                    y1=float(y1),
                    text=text,
                    word_count=len(text.split()),
                    line_count=len(line_texts),
                    avg_size=weighted_sizes / total_chars,
                    max_size=max_size,
                    bold_ratio=bold_chars / total_chars,
                )
            )
            index += 1

    document.close()
    return segments


def body_font_size(segments: Sequence[Segment]) -> float:
    counts: Counter = Counter()
    for segment in segments:
        if 8 <= segment.word_count <= 120:
            rounded = round(segment.avg_size, 1)
            counts[rounded] += segment.word_count
    if counts:
        return float(counts.most_common(1)[0][0])
    if not segments:
        return 10.0
    return round(sum(segment.avg_size for segment in segments) / len(segments), 1)


def is_margin_candidate(segment: Segment) -> bool:
    if segment.word_count > 12:
        return False
    return segment.y0 < segment.page_height * 0.08 or segment.y1 > segment.page_height * 0.92


def filter_repeated_margins(segments: Sequence[Segment]) -> List[Segment]:
    repeated: Counter = Counter()
    for segment in segments:
        if is_margin_candidate(segment):
            repeated[segment.text] += 1

    repeated_texts = {text for text, count in repeated.items() if count >= 2}

    filtered: List[Segment] = []
    for segment in segments:
        if PAGE_NUMBER_RE.match(segment.text):
            continue
        if segment.text in repeated_texts and is_margin_candidate(segment):
            continue
        filtered.append(segment)
    return filtered


def detect_title(segments: Sequence[Segment]) -> Tuple[Optional[str], set]:
    first_page = [
        segment
        for segment in segments
        if segment.page_number == 1
        and segment.y0 < segment.page_height * 0.40
        and 2 <= segment.word_count <= 30
    ]
    if not first_page:
        return None, set()

    anchor = max(first_page, key=lambda segment: (segment.max_size, -segment.y0))
    selected = [anchor]

    for segment in sorted(first_page, key=lambda item: item.y0):
        if segment.index == anchor.index:
            continue
        same_size = abs(segment.max_size - anchor.max_size) <= 0.5
        close_to_title = 0 <= segment.y0 - selected[-1].y1 <= 28
        if same_size and close_to_title:
            selected.append(segment)

    selected.sort(key=lambda item: item.y0)
    title = normalize_text(" ".join(segment.text for segment in selected))
    return title or None, {segment.index for segment in selected}


def build_heading_size_map(segments: Sequence[Segment], body_size: float, title_indexes: set) -> Dict[float, int]:
    candidate_sizes = set()
    for segment in segments:
        if segment.index in title_indexes:
            continue
        short = segment.word_count <= 18 and len(segment.text) <= 140
        larger = segment.max_size >= body_size + 0.8
        if short and larger:
            candidate_sizes.add(round(segment.max_size, 1))

    ordered = sorted(candidate_sizes, reverse=True)
    return {size: min(2 + idx, 4) for idx, size in enumerate(ordered)}


def normalize_heading_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().rstrip("-–—")


def classify_heading(segment: Segment, body_size: float, size_map: Dict[float, int]) -> Optional[int]:
    text = normalize_heading_text(segment.text)
    lower = text.lower()

    if lower in HEADING_KEYWORDS:
        return 2

    numbered = NUMBERED_HEADING_RE.match(text)
    if numbered:
        depth = numbered.group(1).count(".") + 1
        return min(depth + 1, 4)

    if segment.word_count > 18 or len(text) > 140:
        return None

    ends_like_sentence = text.endswith((".", "?", "!", ";", ":"))
    rounded_size = round(segment.max_size, 1)

    if segment.max_size >= body_size + 0.8 and not ends_like_sentence:
        return size_map.get(rounded_size, 2)

    if segment.bold_ratio >= 0.6 and segment.max_size >= body_size + 0.2 and not ends_like_sentence:
        return size_map.get(rounded_size, 3)

    return None


def append_paragraph(markdown_lines: List[str], paragraph: str) -> None:
    paragraph = normalize_text(paragraph)
    if paragraph:
        markdown_lines.append(paragraph)
        markdown_lines.append("")


def segment_to_markdown(
    segment: Segment,
    body_size: float,
    size_map: Dict[float, int],
) -> List[str]:
    text = normalize_text(segment.text)
    if not text:
        return []

    abstract_match = ABSTRACT_PREFIX_RE.match(text)
    if abstract_match:
        lines = ["## Abstract", ""]
        remainder = normalize_text(abstract_match.group(1))
        if remainder:
            lines.append(remainder)
            lines.append("")
        return lines

    keywords_match = KEYWORDS_PREFIX_RE.match(text)
    if keywords_match:
        keyword_body = normalize_text(keywords_match.group(2))
        if keyword_body:
            return ["**Keywords:** " + keyword_body, ""]
        return []

    heading_level = classify_heading(segment, body_size, size_map)
    if heading_level is not None:
        return ["#" * heading_level + " " + normalize_heading_text(text), ""]

    return [text, ""]


def convert_pdf(pdf_path: Path) -> str:
    segments = filter_repeated_margins(extract_segments(pdf_path))
    if not segments:
        return ""

    title, title_indexes = detect_title(segments)
    body_size = body_font_size(segments)
    size_map = build_heading_size_map(segments, body_size, title_indexes)

    markdown_lines: List[str] = []
    if title:
        markdown_lines.append("# " + title)
        markdown_lines.append("")

    for segment in segments:
        if segment.index in title_indexes:
            continue
        markdown_lines.extend(segment_to_markdown(segment, body_size, size_map))

    while markdown_lines and not markdown_lines[-1].strip():
        markdown_lines.pop()
    return "\n".join(markdown_lines) + "\n"


def resolve_pdf_paths(inputs: Sequence[str], input_dir: Path) -> List[Path]:
    if inputs:
        pdf_paths = [Path(item).expanduser().resolve() for item in inputs]
    else:
        pdf_paths = sorted(input_dir.glob("*.pdf"))

    missing = [str(path) for path in pdf_paths if not path.exists()]
    if missing:
        raise SystemExit("PDF not found: " + ", ".join(missing))

    if not pdf_paths:
        raise SystemExit("No PDF files found.")

    return pdf_paths


def write_markdown(pdf_path: Path, output_dir: Path, markdown: str, overwrite: bool) -> Path:
    output_path = output_dir / (pdf_path.stem + ".md")
    if output_path.exists() and not overwrite:
        raise SystemExit(
            "Output already exists: {0}. Use --overwrite to replace it.".format(output_path)
        )
    output_path.write_text(markdown, encoding="utf-8")
    return output_path


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    default_dir = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(description="Convert academic PDFs to Markdown.")
    parser.add_argument("inputs", nargs="*", help="PDF files to convert. Defaults to all PDFs in --input-dir.")
    parser.add_argument(
        "--input-dir",
        default=str(default_dir),
        help="Directory to scan when no PDF path is given.",
    )
    parser.add_argument(
        "--output-dir",
        default=None,
        help="Directory for generated Markdown files. Defaults to the input directory.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing Markdown files.",
    )
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    input_dir = Path(args.input_dir).expanduser().resolve()
    output_dir = Path(args.output_dir).expanduser().resolve() if args.output_dir else input_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    pdf_paths = resolve_pdf_paths(args.inputs, input_dir)

    for pdf_path in pdf_paths:
        markdown = convert_pdf(pdf_path)
        output_path = write_markdown(pdf_path, output_dir, markdown, args.overwrite)
        print("Converted {0} -> {1}".format(pdf_path.name, output_path.name))

    return 0


if __name__ == "__main__":
    sys.exit(main())
