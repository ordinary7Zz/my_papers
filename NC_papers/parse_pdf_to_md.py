from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path


PAGE_NUMBER_RE = re.compile(r"^(?:page\s+)?\d+(?:\s*/\s*\d+)?$", re.IGNORECASE)
BULLET_RE = re.compile(r"^(?:[-*•]|\d+[.)]|[A-Za-z][.)])\s+")
NUMBERED_HEADING_RE = re.compile(
    r"^(?P<prefix>(?:\d+(?:\.\d+)*\.?|[IVXLCM]+\.?|[A-Z]\.))\s+(?P<title>.+)$",
    re.IGNORECASE,
)
INLINE_HEADING_RE = re.compile(r"^(?P<name>[A-Za-z][A-Za-z\s]+?)\s*[:—-]\s*(?P<rest>.+)$")
CAPTION_RE = re.compile(r"^(Figure|Fig\.?|Table)\s+\d+[A-Za-z]?(?:[.:\-]|\s)(?P<rest>.*)$", re.IGNORECASE)
REFERENCE_START_RE = re.compile(r"^(?:\[(?P<bracket>\d+)\]|\((?P<paren>\d+)\)|(?P<plain>\d+)[.)])\s+")

SECTION_NAME_MAP = {
    "abstract": "Abstract",
    "summary": "Summary",
    "introduction": "Introduction",
    "background": "Background",
    "related work": "Related Work",
    "materials and methods": "Materials and Methods",
    "methods": "Methods",
    "methodology": "Methodology",
    "experimental setup": "Experimental Setup",
    "experiments": "Experiments",
    "results": "Results",
    "discussion": "Discussion",
    "conclusion": "Conclusion",
    "conclusions": "Conclusions",
    "future work": "Future Work",
    "limitations": "Limitations",
    "appendix": "Appendix",
    "appendices": "Appendices",
    "acknowledgments": "Acknowledgments",
    "acknowledgements": "Acknowledgments",
    "references": "References",
    "bibliography": "References",
    "works cited": "References",
    "keywords": "Keywords",
    "index terms": "Keywords",
}

AFFILIATION_KEYWORDS = {
    "university",
    "institute",
    "department",
    "school",
    "college",
    "laboratory",
    "lab",
    "hospital",
    "center",
    "centre",
    "faculty",
    "academy",
    "research",
    "company",
    "inc",
    "ltd",
    "corp",
    "corporation",
    "clinic",
}

TITLE_STOP_HEADINGS = {
    "abstract",
    "summary",
    "keywords",
    "index terms",
    "introduction",
    "background",
    "references",
    "bibliography",
    "works cited",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract text from a PDF and write a paper-style Markdown file.")
    parser.add_argument(
        "input_pdf",
        nargs="?",
        default="NC_papers/26-Report.pdf",
        help="Path to the source PDF file.",
    )
    parser.add_argument(
        "output_md",
        nargs="?",
        default=None,
        help="Path to the output Markdown file. Defaults to the PDF name with .md suffix.",
    )
    return parser.parse_args()


def load_reader(pdf_path: Path):
    try:
        from pypdf import PdfReader
    except ModuleNotFoundError as exc:
        raise SystemExit(
            "Missing dependency: pypdf\n"
            "Install it with: python -m pip install pypdf"
        ) from exc

    return PdfReader(str(pdf_path))


def extract_page_text(page) -> str:
    try:
        text = page.extract_text(extraction_mode="layout")
    except TypeError:
        text = page.extract_text()
    return text or ""


def normalize_lines(text: str) -> list[str]:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    return [re.sub(r"\s+", " ", line).strip() for line in text.split("\n")]


def repeated_edge_lines(pages: list[list[str]]) -> set[str]:
    candidates: list[str] = []
    for lines in pages:
        non_empty = [line for line in lines if line]
        if not non_empty:
            continue
        for line in non_empty[:3]:
            candidates.append(line)
        for line in non_empty[-3:]:
            candidates.append(line)

    counts = Counter(candidates)
    min_repeats = max(2, len(pages) // 2)
    return {
        line
        for line, count in counts.items()
        if count >= min_repeats and not PAGE_NUMBER_RE.match(line)
    }


def should_keep_line(line: str, repeated_lines: set[str]) -> bool:
    if not line:
        return False
    if line in repeated_lines:
        return False
    if PAGE_NUMBER_RE.match(line):
        return False
    return True


def prettify_text(text: str) -> str:
    if not text:
        return text
    if not text.isupper():
        return text

    words: list[str] = []
    for word in text.split():
        plain = re.sub(r"[^A-Za-z]", "", word)
        if plain.isupper() and 1 < len(plain) <= 5:
            words.append(word)
            continue
        words.append(word[:1] + word[1:].lower())
    return " ".join(words)


def canonical_section_name(name: str) -> str | None:
    normalized = re.sub(r"\s+", " ", name.strip().lower())
    normalized = normalized.rstrip(".:;")
    return SECTION_NAME_MAP.get(normalized)


def inline_heading(line: str) -> tuple[str, str] | None:
    match = INLINE_HEADING_RE.match(line)
    if not match:
        canonical = canonical_section_name(line)
        if canonical:
            return canonical, ""
        return None

    canonical = canonical_section_name(match.group("name"))
    if not canonical:
        return None
    return canonical, match.group("rest").strip()


def heading_depth(prefix: str) -> int:
    prefix = prefix.rstrip(".")
    if prefix and prefix[0].isdigit():
        return prefix.count(".") + 1
    return 1


def is_heading_text(text: str) -> bool:
    text = text.strip()
    if not text or len(text) > 120:
        return False
    if "@" in text:
        return False
    if text.endswith((".", "?", "!")):
        return False
    words = text.split()
    if not 1 <= len(words) <= 14:
        return False
    lower = text.lower()
    if any(keyword in lower for keyword in AFFILIATION_KEYWORDS):
        return False
    return True


def classify_heading(line: str) -> tuple[str, str, str] | None:
    matched_inline = inline_heading(line)
    if matched_inline:
        canonical, remainder = matched_inline
        return canonical.lower(), f"## {canonical}", remainder

    match = NUMBERED_HEADING_RE.match(line)
    if match:
        title = match.group("title").strip()
        if is_heading_text(title):
            level = min(4, heading_depth(match.group("prefix")) + 1)
            canonical = canonical_section_name(title) or prettify_text(title)
            return canonical.lower(), f"{'#' * level} {canonical}", ""

    canonical = canonical_section_name(line)
    if canonical and is_heading_text(line):
        return canonical.lower(), f"## {canonical}", ""

    if (
        is_heading_text(line)
        and len(line.split()) <= 10
        and (line.isupper() or all(word[:1].isupper() for word in line.split() if word[:1].isalpha()))
    ):
        return prettify_text(line).lower(), f"## {prettify_text(line)}", ""

    return None


def looks_like_name_token(token: str) -> bool:
    token = token.strip(" ,;*†‡1234567890")
    plain = re.sub(r"[^A-Za-z.-]", "", token)
    if not plain:
        return False
    if len(plain) == 1 and plain.isalpha():
        return True
    if plain.isupper() and len(plain) <= 4:
        return True
    return plain[0].isupper() and (plain[1:].islower() or "." in plain or "-" in plain)


def is_probable_author_line(line: str) -> bool:
    lower = line.lower()
    if "@" in line:
        return True
    if any(keyword in lower for keyword in AFFILIATION_KEYWORDS):
        return True
    if any(char.isdigit() for char in line) and not line.strip().startswith("20"):
        return True
    pieces = [piece for piece in re.split(r"(?:,|\band\b)", line) if piece.strip()]
    if 1 < len(pieces) <= 8:
        name_like = 0
        token_count = 0
        for piece in pieces:
            tokens = [token for token in piece.split() if token]
            token_count += len(tokens)
            if tokens and all(looks_like_name_token(token) for token in tokens[:4]):
                name_like += 1
        if name_like == len(pieces) and token_count <= 20:
            return True
    return False


def is_title_like(line: str) -> bool:
    if not line or len(line) > 180:
        return False
    if line.endswith((".", "?", "!")):
        return False
    if "@" in line:
        return False
    if canonical_section_name(line) and canonical_section_name(line).lower() in TITLE_STOP_HEADINGS:
        return False
    words = line.split()
    if not 2 <= len(words) <= 24:
        return False
    lower = line.lower()
    if any(keyword in lower for keyword in AFFILIATION_KEYWORDS):
        return False
    letters = sum(char.isalpha() for char in line)
    return letters >= max(6, len(line) // 3)


def detect_front_matter(first_page_lines: list[str], repeated_lines: set[str], fallback_title: str) -> tuple[str, list[str], int]:
    meaningful = [
        (index, line.strip())
        for index, line in enumerate(first_page_lines)
        if should_keep_line(line.strip(), repeated_lines)
    ]
    if not meaningful:
        return fallback_title, [], -1

    front: list[tuple[int, str]] = []
    for index, line in meaningful[:20]:
        heading = classify_heading(line)
        if front and heading and heading[0] in TITLE_STOP_HEADINGS:
            break
        front.append((index, line))

    if not front:
        return fallback_title, [], -1

    title_lines: list[str] = []
    author_lines: list[str] = []
    switched_to_authors = False

    for _, line in front:
        if not switched_to_authors and is_title_like(line) and not is_probable_author_line(line):
            if len(title_lines) < 3:
                title_lines.append(line)
                continue
        switched_to_authors = True
        author_lines.append(line)

    if not title_lines:
        title_lines = [front[0][1]]
        author_lines = [line for _, line in front[1:]]

    title = prettify_text(" ".join(title_lines))
    front_end_index = front[-1][0]
    return title or fallback_title, author_lines, front_end_index


def join_wrapped_lines(lines: list[str]) -> str:
    if not lines:
        return ""

    paragraph = lines[0]
    for line in lines[1:]:
        if paragraph.endswith("-") and not paragraph.endswith(" -"):
            paragraph = paragraph[:-1] + line
        else:
            paragraph += " " + line
    return paragraph.strip()


def format_keywords(line: str) -> str:
    matched = inline_heading(line)
    if matched and matched[0] == "Keywords":
        return f"**Keywords:** {matched[1]}" if matched[1] else "**Keywords:**"
    if ":" in line:
        label, rest = line.split(":", 1)
        return f"**{prettify_text(label.strip())}:** {rest.strip()}"
    return f"**Keywords:** {line}"


def is_caption(line: str) -> bool:
    return CAPTION_RE.match(line) is not None


def is_reference_start(line: str) -> bool:
    return REFERENCE_START_RE.match(line) is not None


def build_markdown(pdf_path: Path) -> str:
    reader = load_reader(pdf_path)
    pages = [normalize_lines(extract_page_text(page)) for page in reader.pages]
    repeated_lines = repeated_edge_lines(pages)

    title, author_lines, front_end_index = detect_front_matter(pages[0] if pages else [], repeated_lines, pdf_path.stem)

    content: list[str] = [f"# {title}"]
    clean_authors = [line for line in author_lines if line and not canonical_section_name(line)]
    if clean_authors:
        content.extend(f"> {line}" for line in clean_authors)

    paragraph_lines: list[str] = []
    reference_lines: list[str] = []
    in_references = False

    def flush_paragraph() -> None:
        nonlocal paragraph_lines
        paragraph = join_wrapped_lines(paragraph_lines)
        if paragraph:
            content.append(paragraph)
        paragraph_lines = []

    def flush_reference() -> None:
        nonlocal reference_lines
        reference = join_wrapped_lines(reference_lines)
        if reference:
            content.append(f"- {reference}")
        reference_lines = []

    for page_index, page_lines in enumerate(pages):
        for raw_index, raw_line in enumerate(page_lines):
            if page_index == 0 and raw_index <= front_end_index:
                continue

            line = raw_line.strip()
            if not should_keep_line(line, repeated_lines):
                continue

            heading = classify_heading(line)
            if heading:
                kind, markdown_heading, remainder = heading
                flush_paragraph()
                if in_references and kind != "references":
                    flush_reference()
                    in_references = False

                if kind == "keywords":
                    content.append(format_keywords(line))
                    continue

                content.append(markdown_heading)
                if kind == "references":
                    flush_reference()
                    in_references = True
                if remainder:
                    if kind == "references":
                        reference_lines.append(remainder)
                    else:
                        paragraph_lines.append(remainder)
                continue

            if is_caption(line):
                flush_paragraph()
                if in_references:
                    flush_reference()
                    in_references = False
                content.append(f"*{line}*")
                continue

            if in_references:
                if is_reference_start(line):
                    flush_reference()
                    reference_lines.append(line)
                else:
                    reference_lines.append(line)
                continue

            if BULLET_RE.match(line):
                flush_paragraph()
                bullet = BULLET_RE.sub("", line, count=1)
                content.append(f"- {bullet}")
                continue

            paragraph_lines.append(line)

    flush_paragraph()
    flush_reference()

    normalized_content: list[str] = []
    previous = None
    for block in content:
        block = block.strip()
        if not block:
            continue
        if block == previous and block.startswith("## "):
            continue
        normalized_content.append(block)
        previous = block

    return "\n\n".join(normalized_content).strip() + "\n"


def main() -> int:
    args = parse_args()
    input_pdf = Path(args.input_pdf)
    output_md = Path(args.output_md) if args.output_md else input_pdf.with_suffix(".md")

    if not input_pdf.exists():
        print(f"Input PDF not found: {input_pdf}", file=sys.stderr)
        return 1

    markdown = build_markdown(input_pdf)
    output_md.write_text(markdown, encoding="utf-8")
    print(f"Wrote Markdown to {output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
