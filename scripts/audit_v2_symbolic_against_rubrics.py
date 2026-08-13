#!/usr/bin/env python3
"""Compare KCL-26 CaseTruths/Scallop output with reviewed rubric issue refs."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--call2-artifact", type=Path, required=True)
    parser.add_argument("--scallop-artifact", type=Path, required=True)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--definition-gold", type=Path, required=True)
    parser.add_argument("--json-out", type=Path, required=True)
    parser.add_argument("--markdown-out", type=Path, required=True)
    args = parser.parse_args()
    call2 = {value["sub_question_id"]: value for value in _jsonl(args.call2_artifact)}
    scallop = {value["sub_question_id"]: value for value in _jsonl(args.scallop_artifact)}
    inventory = {value["sub_question_id"]: value for value in _jsonl(args.inventory)}
    raw_gold = json.loads(args.definition_gold.read_text(encoding="utf-8"))
    gold = {value["case_id"]: value for value in raw_gold["cases"]}
    case_ids = tuple(call2)
    if not (tuple(scallop) == case_ids and all(value in inventory and value in gold for value in case_ids)):
        raise ValueError("artifact case universes differ")

    reports = []
    aggregate_truths: Counter[str] = Counter()
    total_established = total_outside = 0
    skipped_rejected = 0
    for case_id in case_ids:
        truth_counts = Counter(value["truth"] for value in call2[case_id]["case_truths"])
        aggregate_truths.update(truth_counts)
        established = [
            value["instance_key"]
            for value in scallop[case_id]["liability_results"]
            if value["result"].get("liability_result") is not None
        ]
        rubric_refs = set(gold[case_id]["gold_definition_refs"])
        execution_status = scallop[case_id].get("execution_status", "SUCCEEDED")
        if execution_status == "SKIPPED_REJECTED_PARTICIPATION":
            skipped_rejected += 1
        outside = [value for value in established if value["offense_ref"] not in rubric_refs]
        total_established += len(established)
        total_outside += len(outside)
        outside_counts = Counter(value["offense_ref"] for value in outside)
        inside_counts = Counter(
            value["offense_ref"] for value in established if value["offense_ref"] in rubric_refs
        )
        reports.append({
            "sub_question_id": case_id,
            "execution_status": execution_status,
            "rubric_count": int(inventory[case_id].get("rubric_count", 0)),
            "rubric_summary": list(inventory[case_id].get("rubric_summary", [])),
            "rubric_candidate_refs": sorted(rubric_refs),
            "truth_counts": dict(truth_counts),
            "established_instance_count": len(established),
            "established_within_rubric_candidate_counts": dict(inside_counts),
            "established_outside_rubric_candidate_counts": dict(outside_counts),
            "proxy_verdict": "FAIL_OVERGENERATION" if outside else "NO_OUTSIDE_REF_DETECTED",
            "scope_note": (
                "Rubric DefinitionRef gold includes issues to examine, including rejected theories; "
                "outside-ref establishment is strong false-positive evidence, while in-set establishment "
                "is not by itself proof of rubric correctness."
            ),
        })
    aggregate = {
        "case_count": len(case_ids),
        "truth_counts": dict(aggregate_truths),
        "established_instance_count": total_established,
        "established_outside_rubric_candidate_count": total_outside,
        "outside_rate": total_outside / total_established if total_established else 0.0,
        "cases_with_outside_establishment": sum(
            bool(value["established_outside_rubric_candidate_counts"]) for value in reports
        ),
        "skipped_rejected_participation_case_count": skipped_rejected,
    }
    payload = {"aggregate": aggregate, "cases": reports}
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# KCL-26 symbolic rubric proxy audit",
        "",
        (
            "This is an indirect structural comparison, not a final rubric score. Reviewed "
            "DefinitionRef gold contains both positive and ultimately rejected legal theories."
        ),
        "",
        f"- Cases: {aggregate['case_count']}",
        (
            f"- CaseTruths: {sum(aggregate_truths.values())} "
            f"(TRUE {aggregate_truths['TRUE']}, FALSE {aggregate_truths['FALSE']}, "
            f"UNKNOWN {aggregate_truths['UNKNOWN']})"
        ),
        f"- Established instances: {total_established}",
        f"- Skipped rejected-participation cases: {skipped_rejected}",
        (
            f"- Established outside rubric candidate scope: {total_outside} "
            f"({aggregate['outside_rate']:.1%})"
        ),
        (
            f"- Cases with outside-scope establishment: "
            f"{aggregate['cases_with_outside_establishment']}/26"
        ),
        "",
        "| case | execution | truths T/F/U | established | within rubric candidates | outside rubric candidates | proxy |",
        "|---|---|---:|---:|---|---|---|",
    ]
    for value in reports:
        truth = value["truth_counts"]
        inside = ", ".join(
            f"{key}×{count}" for key, count in value["established_within_rubric_candidate_counts"].items()
        ) or "—"
        outside = ", ".join(
            f"{key}×{count}" for key, count in value["established_outside_rubric_candidate_counts"].items()
        ) or "—"
        lines.append(
            f"| `{value['sub_question_id']}` | {value['execution_status']} | "
            f"{truth.get('TRUE', 0)}/{truth.get('FALSE', 0)}/"
            f"{truth.get('UNKNOWN', 0)} | {value['established_instance_count']} | {inside} | "
            f"{outside} | {value['proxy_verdict']} |"
        )
    args.markdown_out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(aggregate, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
