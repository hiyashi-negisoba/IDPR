"""Materialize the sealed 59-case final-generation inventory without rubric fields."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from idpr.eval.issue_recall import INVENTORY_PATH


# The first case is the KCL development smoke. The second is the original KCL case whose
# bribery/fraud/entrustment doctrine family is represented by the user-authored replacement
# smoke. Both are excluded explicitly so the final pool is the sealed 59 described in the
# Phase-3 scope documents.
DEVELOPMENT_CASES = frozenset(
    {"kcl_criminal_r10_p1_q1_ga", "kcl_criminal_r14_p1_q2"}
)
MODEL_FIELDS = ("sub_question_id", "question_text", "question_prompt")


def build_rows(source: Path) -> list[dict[str, str]]:
    rows = [
        json.loads(line)
        for line in source.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    selected = [row for row in rows if row.get("sub_question_id") not in DEVELOPMENT_CASES]
    if len(rows) != 61 or len(selected) != 59:
        raise ValueError(
            f"expected 61 source and 59 final cases, got {len(rows)} and {len(selected)}"
        )
    if DEVELOPMENT_CASES - {str(row.get("sub_question_id")) for row in rows}:
        raise ValueError("a reviewed development-case exclusion is absent from the source")
    return [
        {field: str(row.get(field, "")) for field in MODEL_FIELDS}
        for row in selected
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=INVENTORY_PATH)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    rows = build_rows(args.source)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )
    print(f"wrote {len(rows)} sealed final-evaluation inputs to {args.out}")


if __name__ == "__main__":
    main()
