"""Aggregate IRAC matrix reports into the §8.2 internal-consistency table (A1).

Reads one or more per-case matrix reports (or directories of them) produced by
``run_fraud_irac_matrix.py`` and emits the paired case-set × method summary with
bootstrap CIs and an exact McNemar test of the reference method (IDPR/M5)
against the baseline.

This consumes existing scoring output only; it does not call the model. Point it
at the matrix reports of an evaluation-set sweep once one exists.

Example:
    python scripts/aggregate_eval_matrix.py \
        data/e2e/fraud/irac_matrix \
        --summary-out data/e2e/fraud/eval/consistency_summary.json \
        --markdown-out data/e2e/fraud/eval/consistency_summary.md
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from idpr.eval import METRIC_ORDER, load_matrix_reports, render_markdown, summarize


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "reports",
        nargs="+",
        type=Path,
        help="matrix report json files and/or directories to scan recursively",
    )
    parser.add_argument("--baseline", default="m1_direct")
    parser.add_argument("--reference", default="m5_irac_plan")
    parser.add_argument("--metrics", nargs="+", default=list(METRIC_ORDER))
    parser.add_argument("--n-boot", type=int, default=10_000)
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--summary-out", type=Path, default=None)
    parser.add_argument("--markdown-out", type=Path, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    records = load_matrix_reports(args.reports)
    if not records:
        raise SystemExit("no run records loaded from the given reports")
    summary = summarize(
        records,
        baseline=args.baseline,
        reference=args.reference,
        metrics=args.metrics,
        n_boot=args.n_boot,
        alpha=args.alpha,
        seed=args.seed,
    )
    markdown = render_markdown(summary)

    if args.summary_out:
        args.summary_out.parent.mkdir(parents=True, exist_ok=True)
        args.summary_out.write_text(
            json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
        )
    if args.markdown_out:
        args.markdown_out.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_out.write_text(markdown, encoding="utf-8")

    print(markdown)
    print(
        f"[aggregate_eval_matrix] paired cases={summary['paired_case_count']} "
        f"methods={len(summary['methods'])} records={len(records)}"
    )


if __name__ == "__main__":
    main()
