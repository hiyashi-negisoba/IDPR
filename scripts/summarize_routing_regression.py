#!/usr/bin/env python3
"""Aggregate routing-accuracy diagnostics across a batch of lean-runner cases.

Scope note: this computes what the per-case diagnostic fields
(``closest_allowed_unit_ids``/``unsupported_reason``, ``01b_routing_completeness.json``)
can measure without a hand-labeled gold set — unsupported false-positive rate,
unsupported precision, and dangling-reference count. A true ``unit_id`` recall
metric needs a gold mapping of case -> expected unit_id per issue, which does not
exist yet; ``--known-target`` lets one or two manually-confirmed cases (e.g. the
bribe_giving miss in kcl_criminal_r14_p1_q2, docs/handoff/CURRENT.md "라우팅 정확도")
be checked as a spot recall check instead of a full metric.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def _load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def summarize(run_dir: Path, known_targets: list[tuple[str, str]]) -> dict[str, Any]:
    case_dirs = sorted(p for p in run_dir.iterdir() if p.is_dir())
    cases: list[dict[str, Any]] = []
    total_unsupported = 0
    total_routing_miss = 0
    total_dangling = 0

    for case_dir in case_dirs:
        selection = _load_json(case_dir / "01_issue_selection.json")
        completeness = _load_json(case_dir / "01b_routing_completeness.json")
        diagnostics = _load_json(case_dir / "01c_unsupported_diagnostics.json")
        unsupported_items = diagnostics.get("unsupported_issues", [])
        gaps = completeness.get("gaps", [])
        routed_unit_ids = {
            str(item.get("unit_id", ""))
            for item in selection.get("issues", [])
            if isinstance(item, dict)
        }

        miss_count = sum(1 for item in unsupported_items if item.get("likely_routing_miss"))
        total_unsupported += len(unsupported_items)
        total_routing_miss += miss_count
        total_dangling += len(gaps)

        cases.append(
            {
                "case_id": case_dir.name,
                "issue_count": len(selection.get("issues", [])),
                "unsupported_count": len(unsupported_items),
                "unsupported_routing_miss_count": miss_count,
                "dangling_reference_count": len(gaps),
                "unsupported_issues": unsupported_items,
                "routed_unit_ids": sorted(routed_unit_ids),
            }
        )

    known_target_results = []
    by_case = {case["case_id"]: case for case in cases}
    for case_id, expected_unit_id in known_targets:
        case = by_case.get(case_id)
        found = expected_unit_id in case["routed_unit_ids"] if case else False
        known_target_results.append(
            {
                "case_id": case_id,
                "expected_unit_id": expected_unit_id,
                "found": found,
            }
        )

    unsupported_fp_rate = (
        total_routing_miss / total_unsupported if total_unsupported else None
    )
    unsupported_precision = (
        1 - unsupported_fp_rate if unsupported_fp_rate is not None else None
    )

    return {
        "run_dir": str(run_dir),
        "case_count": len(cases),
        "total_unsupported_issues": total_unsupported,
        "unsupported_false_positive_rate": unsupported_fp_rate,
        "unsupported_precision": unsupported_precision,
        "dangling_reference_count": total_dangling,
        "known_target_recall": known_target_results,
        "cases": cases,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument(
        "--known-target",
        action="append",
        default=[],
        metavar="CASE_ID=UNIT_ID",
        help="Manually confirmed case_id=unit_id pair to spot-check for recall.",
    )
    parser.add_argument("--json-out", type=Path, default=None)
    args = parser.parse_args()

    known_targets = []
    for raw in args.known_target:
        case_id, _, unit_id = raw.partition("=")
        known_targets.append((case_id, unit_id))

    report = summarize(args.run_dir, known_targets)
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
