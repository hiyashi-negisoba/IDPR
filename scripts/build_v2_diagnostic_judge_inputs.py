#!/usr/bin/env python3
"""Build sealed judge inputs for a diagnostic subset of V2 Call 3 answers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--call3-artifact", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()

    inventory_rows = _jsonl(args.inventory)
    inventory = {str(row["sub_question_id"]): row for row in inventory_rows}
    answers = _jsonl(args.call3_artifact)
    case_ids = [str(row["sub_question_id"]) for row in answers]
    if len(case_ids) != len(set(case_ids)) or any(case_id not in inventory for case_id in case_ids):
        raise ValueError("Call 3 diagnostic case universe is invalid")
    if any(not isinstance(row.get("answer"), str) or not row["answer"].strip() for row in answers):
        raise ValueError("Call 3 diagnostic artifact must contain nonempty current `answer` fields")

    sealed = [
        {
            "sub_question_id": case_id,
            "question_text": str(inventory[case_id]["question_text"]),
            "question_prompt": str(inventory[case_id].get("question_prompt", "")),
        }
        for case_id in case_ids
    ]
    method = [
        {
            "sub_question_id": str(row["sub_question_id"]),
            "generated_response": str(row["answer"]),
        }
        for row in answers
    ]
    args.out_dir.mkdir(parents=True, exist_ok=True)
    sealed_path = args.out_dir / "sealed_inventory.jsonl"
    method_path = args.out_dir / "method_answers.jsonl"
    methods_path = args.out_dir / "methods.json"
    _write_jsonl(sealed_path, sealed)
    _write_jsonl(method_path, method)
    methods_path.write_text(
        json.dumps(
            {
                "version": "1.0.0",
                "methods": {"idpr_v2_diagnostic": str(method_path.resolve())},
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"wrote {len(case_ids)} diagnostic judge inputs to {args.out_dir}")


if __name__ == "__main__":
    main()
