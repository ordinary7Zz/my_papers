#!/usr/bin/env python3
"""Generate Nature-style LaTeX supplementary tables for per-center performance.

Reference style: TRACE Nature paper Supplementary Tables.
  - Values: point estimate (CI lower, CI upper)
  - Best per row (per metric) bolded
  - booktabs rules, cmidrule for grouping
  - sidewaystable for wide tables
"""

import csv
import re
from pathlib import Path
from collections import defaultdict

CSV_PATH = Path(__file__).parent / "data" / "per_by_center_ci.csv"
OUT_PATH = Path(__file__).parent / "per_center_tables.tex"

# ── Model display names ──
MODEL_NAMES = {
    "dinov3_unet": r"ThyroidXAgent",
    "medsam2": r"MedSAM2",
    "medsegx": r"MedSegX",
    "transunet": r"TransUNet",
    "ultrafedfm": r"UltraFedFM",
    "biomedclip": r"BiomedCLIP",
    "medsiglip": r"MedSigLIP",
    "dinov3_unet_multitask": r"ThyroidXAgent",
    "autogluon": r"AutoGluon",
}

# Model order per task (ThyroidXAgent first)
SEG_MODELS = ["dinov3_unet", "medsam2", "medsegx", "transunet", "ultrafedfm"]
CLS_MODELS = ["dinov3_unet_multitask", "biomedclip", "medsiglip", "ultrafedfm"]

# Center code → province (from md report)
CENTER_REGIONS = {
    "ZJ24": "Zhejiang", "EN04": "Inner Mongolia", "BJ01": "Beijing",
    "SH01": "Shanghai", "ZJ05": "Zhejiang", "SH05": "Shanghai",
    "NX01": "Ningxia", "ZJ06": "Zhejiang", "QX07": "Qinghai",
    "AN01": "Anhui", "CQ03": "Chongqing", "GZ02": "Guizhou",
    "JX06": "Jiangxi", "JS02": "Jiangsu", "YN05": "Yunnan",
    "EN02": "Inner Mongolia", "AH04": "Anhui", "GS03": "Gansu",
    "FJ03": "Fujian", "SD12": "Shandong", "JS01": "Jiangsu",
    "NM02": "Inner Mongolia", "JL04": "Jilin", "SH06": "Shanghai",
    "SX04": "Shaanxi", "BJ09": "Beijing", "SC06": "Sichuan",
    "XJ01": "Xinjiang", "YN01": "Yunnan", "SD13": "Shandong",
    "GX01": "Guangxi", "ZJ29": "Zhejiang", "HB07": "Hubei",
    "SD14": "Shandong", "FJ01": "Fujian",
}


def parse_ci(s):
    """Parse '0.8064 [0.7984,0.8140]' → (0.8064, 0.7984, 0.8140)."""
    s = s.strip()
    if not s:
        return None
    m = re.match(r"([\d.]+)\s*\[([\d.]+),\s*([\d.]+)\]", s)
    if m:
        return float(m.group(1)), float(m.group(2)), float(m.group(3))
    # Try plain number
    try:
        v = float(s)
        return v, None, None
    except ValueError:
        return None


def fmt_val(parsed, decimals=3, percent=False, adaptive=False):
    """Format parsed CI as '80.64\\textsubscript{(79.84, 81.40)}'.

    percent=True: multiply values by 100 (for Dice).
    adaptive=True: use 1 fewer decimal for |value| >= 100 (for HD95).
    CI shown as subscript in small font at bottom-right.
    """
    if parsed is None:
        return r"--"
    val, lo, hi = parsed
    scale = 100 if percent else 1
    val_s = val * scale
    d = decimals - 1 if (adaptive and abs(val_s) >= 100) else decimals
    if lo is not None and hi is not None:
        lo_s = lo * scale
        hi_s = hi * scale
        ci = f"{lo_s:.{d}f}, {hi_s:.{d}f}"
        return f"{val_s:.{d}f}" + r"\textsubscript{(" + ci + r")}"
    return f"{val_s:.{d}f}"


def fmt_val_bold(parsed, decimals=3, percent=False, adaptive=False):
    """Bold only the point estimate; CI as subscript."""
    if parsed is None:
        return r"--"
    val, lo, hi = parsed
    scale = 100 if percent else 1
    val_s = val * scale
    d = decimals - 1 if (adaptive and abs(val_s) >= 100) else decimals
    if lo is not None and hi is not None:
        lo_s = lo * scale
        hi_s = hi * scale
        ci = f"{lo_s:.{d}f}, {hi_s:.{d}f}"
        return r"\textbf{" + f"{val_s:.{d}f}" + r"}" + r"\textsubscript{(" + ci + r")}"
    return r"\textbf{" + f"{val_s:.{d}f}" + r"}"


def load_data():
    """Load CSV, return dict[task][model][center] = {metric: (val, lo, hi), n: int}."""
    data = defaultdict(lambda: defaultdict(dict))
    with open(CSV_PATH, encoding="utf-8") as f:
        # Skip header lines like "=== 分割任务 ==="
        lines = f.readlines()

    # Find CSV sections and parse
    csv_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("===") or stripped == "":
            if csv_lines:
                _parse_csv_block(csv_lines, data)
                csv_lines = []
            continue
        csv_lines.append(line)
    if csv_lines:
        _parse_csv_block(csv_lines, data)
    return data


def _parse_csv_block(csv_lines, data):
    reader = csv.DictReader(csv_lines)
    for row in reader:
        task = row["task"]
        model = row["model"]
        center = row["center"]
        n = int(row["n"])
        entry = {"n": n}
        for col in row:
            if col in ("task", "model", "center", "n"):
                continue
            # col like "Dice [CI95]" or "AUROC [CI95]"
            metric = col.split("[")[0].strip()
            entry[metric] = parse_ci(row[col])
        data[task][model][center] = entry


def clean_center_name(center):
    """Return full center code with underscores escaped for LaTeX."""
    return center.replace("_", r"\_")


def get_centers_sorted(task_data, models):
    """Get centers sorted by total n (descending), excluding '全局'."""
    center_n = {}
    for model in models:
        for center, entry in task_data[model].items():
            if center == "全局":
                continue
            center_n[center] = entry["n"]
    # Sort by n descending, then by center name
    return sorted(center_n.keys(), key=lambda c: (-center_n[c], c))


def find_best_per_metric(task_data, models, centers, metric):
    """For each center, find the model with best metric value."""
    best = {}
    for center in centers:
        best_val = None
        best_model = None
        for model in models:
            entry = task_data[model].get(center)
            if entry is None or entry.get(metric) is None:
                continue
            val = entry[metric][0]
            if best_val is None or val > best_val:
                best_val = val
                best_model = model
        best[center] = best_model
    return best


def gen_seg_table(data, task, task_label, models, metric, metric_label,
                  decimals, lower_better, caption, label, percent=False, adaptive=False):
    """Generate table for a single segmentation metric."""
    task_data = data[task]
    centers = get_centers_sorted(task_data, models)

    # Find best per center
    best = {}
    for center in centers:
        best_val = None
        best_model = None
        for model in models:
            entry = task_data[model].get(center)
            if entry is None or entry.get(metric) is None:
                continue
            val = entry[metric][0]
            if best_val is None:
                best_val = val
                best_model = model
            elif (lower_better and val < best_val) or (not lower_better and val > best_val):
                best_val = val
                best_model = model
        best[center] = best_model

    lines = []
    lines.append(r"\begin{table}[p]")
    lines.append(r"\centering")
    lines.append(r"\caption{" + caption + r"}")
    lines.append(r"\label{" + label + r"}")
    lines.append(r"\footnotesize")
    lines.append(r"\setlength{\tabcolsep}{4pt}")
    lines.append(r"\begin{tabular}{ll" + "r" * len(models) + r"}")
    lines.append(r"\toprule")

    # Header
    hdr = r"\multirow{2}{*}{Center} & \multirow{2}{*}{$N$} & "
    for model in models:
        hdr += r"\multicolumn{1}{c}{" + MODEL_NAMES[model] + r"} & "
    hdr = hdr.rstrip(" & ") + r" \\"
    lines.append(hdr)

    # cmidrules
    cmid = ""
    col = 3
    for model in models:
        cmid += r"\cmidrule(lr){" + str(col) + "-" + str(col) + r"} "
        col += 1
    cmid = cmid.rstrip()
    lines.append(cmid)

    # Sub-header: metric name
    sub = r" & & "
    for _ in models:
        sub += metric_label + r" & "
    sub = sub.rstrip(" & ") + r" \\"
    lines.append(sub)
    lines.append(r"\midrule")

    # Overall row
    overall = task_data[models[0]].get("全局")
    if overall:
        row = r"\textit{Overall} & " + f"{overall['n']:,} & "
        for model in models:
            entry = task_data[model].get("全局", {})
            val = entry.get(metric)
            row += fmt_val(val, decimals, percent, adaptive) + r" & "
        row = row.rstrip(" & ") + r" \\"
        lines.append(row)
        lines.append(r"\midrule")

    # Data rows
    for center in centers:
        n_val = None
        for model in models:
            entry = task_data[model].get(center)
            if entry:
                n_val = entry["n"]
                break
        row = f"{clean_center_name(center)} & {n_val:,} & "
        for model in models:
            entry = task_data[model].get(center)
            if entry is None:
                row += r"-- & "
                continue
            val = entry.get(metric)
            if val is None:
                row += r"-- & "
            elif best.get(center) == model:
                row += fmt_val_bold(val, decimals, percent, adaptive) + r" & "
            else:
                row += fmt_val(val, decimals, percent, adaptive) + r" & "
        row = row.rstrip(" & ") + r" \\"
        lines.append(row)

    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append(r"\end{table}")
    lines.append(r"\clearpage")
    return "\n".join(lines)


def gen_cls_table(data, task, task_label, models, metrics, metric_labels, caption, label):
    """Generate table for classification."""
    task_data = data[task]
    centers = get_centers_sorted(task_data, models)

    # Find best per center per metric
    best = {}
    for metric in metrics:
        best[metric] = {}
        for center in centers:
            best_val = None
            best_model = None
            for model in models:
                entry = task_data[model].get(center)
                if entry is None or entry.get(metric) is None:
                    continue
                val = entry[metric][0]
                if best_val is None or val > best_val:
                    best_val = val
                    best_model = model
            best[metric][center] = best_model

    lines = []
    lines.append(r"\begin{table}[p]")
    lines.append(r"\centering")
    lines.append(r"\caption{" + caption + r"}")
    lines.append(r"\label{" + label + r"}")
    lines.append(r"\footnotesize")
    lines.append(r"\setlength{\tabcolsep}{4pt}")
    lines.append(r"\begin{tabular}{ll" + "r" * (len(models) * len(metrics)) + r"}")
    lines.append(r"\toprule")

    # Header row 1: Center/N (multirow) + model names
    hdr1 = r"\multirow{2}{*}{Center} & \multirow{2}{*}{$N$} & "
    for model in models:
        if len(metrics) == 1:
            hdr1 += r"\multicolumn{1}{c}{" + MODEL_NAMES[model] + r"} & "
        else:
            hdr1 += r"\multicolumn{" + str(len(metrics)) + r"}{c}{" + MODEL_NAMES[model] + r"} & "
    hdr1 = hdr1.rstrip(" & ") + r" \\"
    lines.append(hdr1)

    # cmidrules
    cmid = ""
    col = 3
    for model in models:
        cmid += r"\cmidrule(lr){" + str(col) + "-" + str(col + len(metrics) - 1) + r"} "
        col += len(metrics)
    cmid = cmid.rstrip()
    lines.append(cmid)

    # Header row 2: metric labels (single metric → same label under each model)
    hdr2 = r" & & "
    for model in models:
        for ml in metric_labels:
            hdr2 += ml + r" & "
    hdr2 = hdr2.rstrip(" & ") + r" \\"
    lines.append(hdr2)
    lines.append(r"\midrule")

    # Overall row
    overall = task_data[models[0]].get("全局")
    if overall:
        row = r"\textit{Overall} & " + f"{overall['n']:,} & "
        for model in models:
            entry = task_data[model].get("全局", {})
            for metric in metrics:
                val = entry.get(metric)
                row += fmt_val(val) + r" & "
        row = row.rstrip(" & ") + r" \\"
        lines.append(row)
        lines.append(r"\midrule")

    # Data rows
    for center in centers:
        n_val = None
        for model in models:
            entry = task_data[model].get(center)
            if entry:
                n_val = entry["n"]
                break
        if n_val is None or n_val == 0:
            row = f"{clean_center_name(center)} & 0 & "
            for model in models:
                for _ in metrics:
                    row += r"-- & "
            row = row.rstrip(" & ") + r" \\"
            lines.append(row)
            continue

        row = f"{clean_center_name(center)} & {n_val:,} & "
        for model in models:
            entry = task_data[model].get(center)
            if entry is None:
                for _ in metrics:
                    row += r"-- & "
                continue
            for metric in metrics:
                val = entry.get(metric)
                if val is None:
                    row += r"-- & "
                elif best.get(metric, {}).get(center) == model:
                    row += fmt_val_bold(val) + r" & "
                else:
                    row += fmt_val(val) + r" & "
        row = row.rstrip(" & ") + r" \\"
        lines.append(row)

    lines.append(r"\bottomrule")
    lines.append(r"\end{tabular}")
    lines.append(r"\end{table}")
    lines.append(r"\clearpage")
    return "\n".join(lines)


def main():
    data = load_data()

    output = []
    output.append(r"% Auto-generated per-center performance tables")
    output.append(r"% Required packages (add to document preamble):")
    output.append(r"%   \usepackage{booktabs}")
    output.append(r"%   \usepackage{multirow}")
    output.append("")

    # ── S1: Gland Dice ──
    output.append(r"% ============================================================")
    output.append(r"% Supplementary Table S1: Gland segmentation — Dice")
    output.append(r"% ============================================================")
    output.append("")
    output.append(gen_seg_table(
        data, "gland", "Gland segmentation", SEG_MODELS,
        "Dice", r"Dice (\%) $\uparrow$", 2, False,
        r"Per-centre Dice similarity coefficient (\%) for "
        r"thyroid gland segmentation on the NHC-MISD-TUS external test set. Values are reported "
        r"as point estimates with 95\% confidence intervals. Bold indicates the best result in each row.",
        "tab:gland_dice", percent=True
    ))
    output.append("")

    # ── S2: Gland HD95 ──
    output.append(r"% ============================================================")
    output.append(r"% Supplementary Table S2: Gland segmentation — HD95")
    output.append(r"% ============================================================")
    output.append("")
    output.append(gen_seg_table(
        data, "gland", "Gland segmentation", SEG_MODELS,
        "HD95", r"HD95 (mm) $\downarrow$", 2, True,
        r"Per-centre 95\% Hausdorff distance (HD95, mm) for "
        r"thyroid gland segmentation on the NHC-MISD-TUS external test set. Values are reported "
        r"as point estimates with 95\% confidence intervals. Bold indicates the best result in each row.",
        "tab:gland_hd95", adaptive=True
    ))
    output.append("")

    # ── S3: Nodule Dice ──
    output.append(r"% ============================================================")
    output.append(r"% Supplementary Table S3: Nodule segmentation — Dice")
    output.append(r"% ============================================================")
    output.append("")
    output.append(gen_seg_table(
        data, "nodule", "Nodule segmentation", SEG_MODELS,
        "Dice", r"Dice (\%) $\uparrow$", 2, False,
        r"Per-centre Dice similarity coefficient (\%) for "
        r"thyroid nodule segmentation on the NHC-MISD-TUS external test set. Values are reported "
        r"as point estimates with 95\% confidence intervals. Bold indicates the best result in each row.",
        "tab:nodule_dice", percent=True
    ))
    output.append("")

    # ── S4: Nodule HD95 ──
    output.append(r"% ============================================================")
    output.append(r"% Supplementary Table S4: Nodule segmentation — HD95")
    output.append(r"% ============================================================")
    output.append("")
    output.append(gen_seg_table(
        data, "nodule", "Nodule segmentation", SEG_MODELS,
        "HD95", r"HD95 (mm) $\downarrow$", 2, True,
        r"Per-centre 95\% Hausdorff distance (HD95, mm) for "
        r"thyroid nodule segmentation on the NHC-MISD-TUS external test set. Values are reported "
        r"as point estimates with 95\% confidence intervals. Bold indicates the best result in each row.",
        "tab:nodule_hd95", adaptive=True
    ))
    output.append("")

    # ── S5: Binary AUROC ──
    output.append(r"% ============================================================")
    output.append(r"% Supplementary Table S5: Binary classification — AUROC")
    output.append(r"% ============================================================")
    output.append("")
    output.append(gen_cls_table(
        data, "binary", "Binary classification", CLS_MODELS,
        ["AUROC"], [r"AUROC $\uparrow$"],
        r"Per-centre AUROC for benign versus malignant thyroid "
        r"nodule classification on the NHC-MISD-TUS external test set. Values are reported as "
        r"point estimates with 95\% confidence intervals. Bold indicates the best result in each row.",
        "tab:binary_auroc"
    ))
    output.append("")

    # ── S6: Binary AUPRC ──
    output.append(r"% ============================================================")
    output.append(r"% Supplementary Table S6: Binary classification — AUPRC")
    output.append(r"% ============================================================")
    output.append("")
    output.append(gen_cls_table(
        data, "binary", "Binary classification", CLS_MODELS,
        ["AUPRC"], [r"AUPRC $\uparrow$"],
        r"Per-centre AUPRC for benign versus malignant thyroid "
        r"nodule classification on the NHC-MISD-TUS external test set. Values are reported as "
        r"point estimates with 95\% confidence intervals. Bold indicates the best result in each row.",
        "tab:binary_auprc"
    ))
    output.append("")

    OUT_PATH.write_text("\n".join(output), encoding="utf-8")
    print(f"Written to {OUT_PATH}")
    print(f"Total lines: {len(output)}")


if __name__ == "__main__":
    main()
