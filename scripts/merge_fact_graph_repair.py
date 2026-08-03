"""Merge repaired Call-1 rows into a base fact-graph artifact, preserving row order.

Only rows that the repair actually admitted replace the base row.  A repair row that still
has no admitted ``fact_graph`` leaves the base row untouched, so a failed repair can never
look like a success.  ``--require-complete`` makes the merge fail loudly when any case is
still missing, which is what stops a doomed downstream generation run from starting.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def admitted(row: dict[str, Any]) -> bool:
    return isinstance(row.get("fact_graph"), dict)


def merge(
    base_rows: list[dict[str, Any]],
    repair_rows: list[dict[str, Any]],
    *,
    repair_note: dict[str, Any] | None = None,
) -> tuple[list[dict[str, Any]], list[str], list[str]]:
    repaired = {
        str(row["sub_question_id"]): row for row in repair_rows if admitted(row)
    }
    merged: list[dict[str, Any]] = []
    replaced: list[str] = []
    for row in base_rows:
        case_id = str(row["sub_question_id"])
        if case_id in repaired and not admitted(row):
            fresh = dict(repaired[case_id])
            if repair_note is not None:
                fresh["repair"] = repair_note
            merged.append(fresh)
            replaced.append(case_id)
        else:
            merged.append(row)
    still_missing = [
        str(row["sub_question_id"]) for row in merged if not admitted(row)
    ]
    return merged, replaced, still_missing


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--repair", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--repair-note", default="")
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()

    base_rows = read_jsonl(args.base)
    repair_rows = read_jsonl(args.repair)
    note = {"kind": "call1_repair", "detail": args.repair_note} if args.repair_note else None
    merged, replaced, still_missing = merge(base_rows, repair_rows, repair_note=note)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in merged),
        encoding="utf-8",
    )
    print(json.dumps({
        "rows": len(merged),
        "replaced": replaced,
        "still_missing": still_missing,
        "out": str(args.out),
    }, ensure_ascii=False))
    if args.require_complete and still_missing:
        raise SystemExit(
            f"fact graphs still missing for {len(still_missing)} case(s): {still_missing}"
        )


if __name__ == "__main__":
    main()
