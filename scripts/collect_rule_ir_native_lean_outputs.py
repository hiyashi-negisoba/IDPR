#!/usr/bin/env python3
"""Collect a rule_ir_native_lean batch run_dir into a phase3-judge outputs.jsonl.

``run_rule_ir_native_lean_batch.sh`` writes one subdirectory per case with a
``05_answer.md`` (the graded, VERDICT_MANIFEST-stripped answer). The Phase-3
judge consumes a single flat JSONL of ``{"sub_question_id", "generated_response"}``
records (data/eval/phase3_method_outputs.json's schema) — this is the missing
link between the two, done ad hoc in a prior session and not saved then.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--case-list", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    case_ids = [
        line.strip()
        for line in args.case_list.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    records = []
    missing = []
    for case_id in case_ids:
        answer_path = args.run_dir / case_id / "05_answer.md"
        if not answer_path.is_file():
            missing.append(case_id)
            continue
        records.append(
            {
                "sub_question_id": case_id,
                "generated_response": answer_path.read_text(encoding="utf-8"),
            }
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"collected {len(records)}/{len(case_ids)} cases -> {args.out}")
    if missing:
        print(f"missing 05_answer.md for {len(missing)} cases: {missing}", file=sys.stderr)
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
