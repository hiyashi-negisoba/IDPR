"""Write an inventory subset containing only the cases whose Call-1 fact graph failed.

The pinned V2 Call-1 runner has no case selection or retry flag, so a targeted repair is
expressed as a smaller inventory rather than as a code change.  Selection is driven by the
artifact itself: a row without an admitted ``fact_graph`` object is a failure.  No case id
is written into this file.
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


def failed_case_ids(rows: list[dict[str, Any]]) -> list[str]:
    return [
        str(row["sub_question_id"])
        for row in rows
        if not isinstance(row.get("fact_graph"), dict)
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fact-graphs", type=Path, required=True)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    graph_rows = read_jsonl(args.fact_graphs)
    inventory = read_jsonl(args.inventory)
    by_id = {str(row["sub_question_id"]): row for row in inventory}
    if len(by_id) != len(inventory):
        raise ValueError("inventory contains duplicate sub_question_id values")

    wanted = failed_case_ids(graph_rows)
    unknown = sorted(set(wanted) - set(by_id))
    if unknown:
        raise ValueError(f"failed cases absent from inventory: {unknown}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(json.dumps(by_id[case_id], ensure_ascii=False) + "\n" for case_id in wanted),
        encoding="utf-8",
    )
    print(json.dumps({
        "fact_graph_rows": len(graph_rows),
        "failed": len(wanted),
        "case_ids": wanted,
        "out": str(args.out),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
