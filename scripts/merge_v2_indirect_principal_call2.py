#!/usr/bin/env python3
"""Merge isolated indirect-principal dependencies into a frozen Call 2 artifact."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-call2", type=Path, required=True)
    parser.add_argument("--indirect-call2", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    indirect_rows = _rows(args.indirect_call2)
    indirect = {row["sub_question_id"]: row for row in indirect_rows}
    if len(indirect) != len(indirect_rows):
        raise ValueError("duplicate indirect-principal case")
    output = _rows(args.base_call2)
    base_ids = {row["sub_question_id"] for row in output}
    if set(indirect) - base_ids:
        raise ValueError("indirect-principal case is outside base Call 2")
    for row in output:
        case = indirect.get(row["sub_question_id"])
        row["indirect_principal_dependencies"] = (
            list(case["indirect_principal_dependencies"]) if case else []
        )
        row["indirect_principal_dependency_count"] = len(row["indirect_principal_dependencies"])
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in output))
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
