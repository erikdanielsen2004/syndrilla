#!/usr/bin/env python3
import argparse
from pathlib import Path
import re
import csv
import yaml
import matplotlib.pyplot as plt


def to_float(x):
    if x is None:
        return None
    if isinstance(x, (int, float)):
        return float(x)
    if isinstance(x, str):
        s = x.strip().strip("'").strip('"')
        try:
            return float(s)
        except ValueError:
            return None
    return None


def load_yaml(p: Path) -> dict:
    with p.open("r") as f:
        return yaml.safe_load(f) or {}


def infer_metadata_from_path(path: Path) -> dict:
    """
    Optional: extract metadata from folder names.
    Example patterns you might have:
      .../quant_34/...  -> i=3, f=4
      .../h200/...      -> h=200
      .../hx_...        -> hx/hz
    Adjust patterns to match your naming scheme.
    """
    s = str(path)

    meta = {}
    m = re.search(r"quant_(\d)(\d)", s)
    if m:
        meta["quant_i"] = int(m.group(1))
        meta["quant_f"] = int(m.group(2))

    m = re.search(r"h(\d+)", s)
    if m:
        meta["h"] = int(m.group(1))

    if "hx" in s:
        meta["basis"] = "hx"
    elif "hz" in s:
        meta["basis"] = "hz"

    return meta


def extract_record(doc: dict, file_path: Path) -> dict:
    d0 = doc.get("decoder_0", {}) or {}
    df = doc.get("decoder_full", {}) or {}

    rec = {
        "file": str(file_path),
        "folder": str(file_path.parent),
        "algorithm": d0.get("algorithm") or df.get("algorithm"),
        "p": to_float(df.get("physical error rate")),
        "ler": to_float(d0.get("logical error rate") or df.get("logical error rate")),
        "dfer": to_float(d0.get("data frame error rate")),
        "fail_rate": to_float(d0.get("converge failure rate")),
        "avg_iter": to_float(d0.get("average iteration")),
        "time_s": to_float(d0.get("total time (s)") or df.get("total time (s)")),
        "batch_size": to_float(df.get("batch size")),
        "target_error": to_float(df.get("target error")),
        "target_error_reached": to_float(df.get("target error reached")),
    }

    rec.update(infer_metadata_from_path(file_path))
    return rec


def write_csv(records, out_csv: Path):
    if not records:
        return
    cols = [
        "algorithm", "p", "ler", "dfer", "fail_rate", "avg_iter", "time_s",
        "batch_size", "target_error", "target_error_reached",
        "quant_i", "quant_f", "h", "basis",
        "folder", "file",
    ]
    # include any extra discovered keys
    extra = sorted({k for r in records for k in r.keys()} - set(cols))
    cols = cols + extra

    with out_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in records:
            w.writerow(r)


def scatter_by_algorithm(records, xkey, ykey, out_png: Path, title: str, xlabel: str, ylabel: str):
    by_alg = {}
    for r in records:
        x = r.get(xkey)
        y = r.get(ykey)
        if x is None or y is None:
            continue
        by_alg.setdefault(r.get("algorithm", "unknown"), []).append((x, y))

    if not by_alg:
        print(f"Skipping {title}: no usable ({xkey}, {ykey}) points found.")
        return

    plt.figure()
    for alg, pts in by_alg.items():
        xs = [a for a, _ in pts]
        ys = [b for _, b in pts]
        plt.scatter(xs, ys, label=alg)

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.grid(True, linestyle="--", linewidth=0.5)
    plt.tight_layout()
    plt.savefig(out_png, dpi=200)
    plt.close()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="Top-level sweep folder (e.g., bp_relay_sweeping)")
    ap.add_argument("--pattern", default="result*.yaml", help="Result filename pattern (default: result*.yaml)")
    ap.add_argument("--outdir", default="plots", help="Output folder for CSV + images")
    args = ap.parse_args()

    root = Path(args.root).expanduser().resolve()
    outdir = Path(args.outdir).expanduser().resolve()
    outdir.mkdir(parents=True, exist_ok=True)

    result_files = sorted(root.rglob(args.pattern))
    if not result_files:
        raise SystemExit(f"No result YAML files found in {root} matching {args.pattern}")

    records = []
    for fp in result_files:
        try:
            doc = load_yaml(fp)
            records.append(extract_record(doc, fp))
        except Exception as e:
            print(f"Skipping {fp}: {e}")

    out_csv = outdir / "summary.csv"
    write_csv(records, out_csv)
    print(f"Wrote {out_csv} ({len(records)} records)")

    scatter_by_algorithm(
        records, "p", "ler",
        outdir / "ler_vs_p.png",
        "Logical error rate vs physical error rate",
        "physical error rate (p)",
        "logical error rate (LER)",
    )
    scatter_by_algorithm(
        records, "p", "time_s",
        outdir / "time_vs_p.png",
        "Runtime vs physical error rate",
        "physical error rate (p)",
        "total time (s)",
    )
    scatter_by_algorithm(
        records, "p", "fail_rate",
        outdir / "failrate_vs_p.png",
        "Convergence failure rate vs physical error rate",
        "physical error rate (p)",
        "converge failure rate",
    )

    print(f"Wrote plots to {outdir}/")


if __name__ == "__main__":
    main()
