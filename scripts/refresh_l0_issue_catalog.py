"""Refresh issue hierarchy fields in an L0 artifact without rerunning retrieval.

Article provenance is immutable input here.  The command rebuilds only fields derived
from the current rule/issue catalog and refuses to write if the current expansion would
change the persisted article boundary.
"""

from __future__ import annotations

import argparse
import json
import statistics as st
from pathlib import Path

from idpr.candidates import candidate_issues
from idpr.eval.issue_recall import PROJECT_ROOT
from idpr.issue_pipeline import issue_candidate_row


DEFAULT_CANDIDATES = PROJECT_ROOT / "data/eval/l0_candidates.jsonl"
DEFAULT_REPORT = PROJECT_ROOT / "data/eval/l0_union_report.json"


def refreshed_row(row: dict) -> dict:
    scope = candidate_issues(
        selected=tuple(row.get("from_model", ())),
        retrieved=tuple(row.get("from_retrieval", ())),
    )
    persisted_articles = tuple(row.get("articles", ()))
    if scope.articles != persisted_articles:
        raise ValueError(
            f"{row.get('sub_question_id')}: article boundary changed; rerun L0 retrieval"
        )
    return issue_candidate_row(
        str(row["sub_question_id"]),
        scope,
        retrieved_issue_ids=tuple(row.get("retrieved_issue_ids", ())),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--out", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()

    rows = [
        json.loads(line)
        for line in args.input.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    refreshed = [refreshed_row(row) for row in rows]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.out.with_suffix(args.out.suffix + ".tmp")
    temporary.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in refreshed),
        encoding="utf-8",
    )
    temporary.replace(args.out)

    if args.report.is_file():
        report = json.loads(args.report.read_text(encoding="utf-8"))
        issue_counts = [row["initial_issues"] for row in refreshed]
        anchor_counts = [
            sum(
                len(issue.anchor_card_ids) + len(issue.reviewed_anchor_rules)
                for issue in candidate_issues(
                    selected=tuple(row.get("from_model", ())),
                    retrieved=tuple(row.get("from_retrieval", ())),
                ).initial_issues
            )
            for row in rows
        ]
        report["initial_issues_per_question"] = {
            "median": int(st.median(issue_counts)),
            "max": max(issue_counts),
        }
        report["anchor_rules_per_question"] = {
            "median": int(st.median(anchor_counts)),
            "max": max(anchor_counts),
        }
        args.report.write_text(
            json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    print(f"refreshed {len(refreshed)} rows in {args.out}")


if __name__ == "__main__":
    main()
