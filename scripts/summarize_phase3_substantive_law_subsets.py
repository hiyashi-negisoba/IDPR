#!/usr/bin/env python3
"""Recompute Phase-3 judge macro/micro metrics over several case-id subsets.

The full 61-case sealed set mixes substantive-law and procedure-law
questions; IDPR's routing prompt explicitly refuses to raise procedure-law
issues, so scoring it against the full 61 unfairly penalizes coverage
(docs/handoff/CURRENT.md "방법론 결함 발견·정정"). This recomputes the same
``aggregate_records`` macro/micro summary the judge itself uses, but over
arbitrary case-id subsets, from the already-produced judgments.jsonl — no
new judge calls.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.eval.phase3_judge import aggregate_records  # noqa: E402


DEVELOPMENT_CASES = {"kcl_criminal_r10_p1_q1_ga", "kcl_criminal_r14_p1_q2"}

# The inventory carries an exact categorical ``legal_area`` field
# (substantive/procedure/mixed) — verified this session: legal_area==
# "substantive" reproduces the prior session's 26-case curated set exactly
# (byte-for-byte set equality against the case ids cached from job 219779),
# and substantive+mixed == 28, matching the documented "28개" figure. This
# replaces an earlier regex-density reconstruction attempt in this script
# that turned out not to discriminate at all (every case scored under 4%
# density regardless of topic) — the categorical field was already there
# and exact, no reconstruction needed.
def load_legal_areas(inventory_path: Path) -> dict[str, str]:
    areas: dict[str, str] = {}
    with inventory_path.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            case_id = str(record.get("sub_question_id", ""))
            areas[case_id] = str(record.get("legal_area", ""))
    return areas


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--judgments", type=Path, required=True)
    parser.add_argument("--method-id", required=True)
    parser.add_argument(
        "--sealed-inventory",
        type=Path,
        default=ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl",
    )
    args = parser.parse_args()

    records = []
    with args.judgments.open(encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            if record.get("method_id") == args.method_id:
                records.append(record)

    all_ids = sorted({str(record["sub_question_id"]) for record in records})
    sealed_59_ids = sorted(set(all_ids) - DEVELOPMENT_CASES)

    legal_areas = load_legal_areas(args.sealed_inventory)
    substantive_26_ids = sorted(
        case_id for case_id in all_ids if legal_areas.get(case_id) == "substantive"
    )
    substantive_or_mixed_28_ids = sorted(
        case_id
        for case_id in all_ids
        if legal_areas.get(case_id) in ("substantive", "mixed")
    )

    subsets: dict[str, list[str]] = {
        "61_all": all_ids,
        "59_sealed_only": sealed_59_ids,
        f"{len(substantive_or_mixed_28_ids)}_substantive_or_mixed": substantive_or_mixed_28_ids,
        f"{len(substantive_26_ids)}_substantive_only": substantive_26_ids,
    }

    report: dict[str, Any] = {}
    for name, case_ids in subsets.items():
        subset_records = [
            record for record in records if str(record["sub_question_id"]) in case_ids
        ]
        summary = aggregate_records(subset_records, expected_case_ids=case_ids)
        report[name] = summary["methods"].get(args.method_id, {})

    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
