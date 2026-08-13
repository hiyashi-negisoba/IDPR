#!/usr/bin/env python3
"""Merge isolated participation assessments into a frozen general Call 2 artifact."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _rows(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]


def _key(value: dict[str, Any]) -> tuple[str, str, str, str]:
    return (
        str(value["case_id"]),
        str(value["actor_id"]),
        str(value["offense_ref"]),
        str(value["occurrence_id"]),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-call2", type=Path, required=True)
    parser.add_argument("--participation-call2", type=Path, required=True)
    parser.add_argument("--participation-plan", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument(
        "--diagnostic-preserve-rejected",
        action="store_true",
        help="preserve rejected participation rows for typed downstream diagnostic skipping",
    )
    args = parser.parse_args()

    base_rows = _rows(args.base_call2)
    participation = {
        row["sub_question_id"]: row for row in _rows(args.participation_call2)
    }
    plans = {row["sub_question_id"]: row for row in _rows(args.participation_plan)}
    if set(participation) != set(plans) or {
        row["sub_question_id"] for row in base_rows
    } != set(plans):
        raise ValueError("Call 2/participation/plan case universes differ")

    projection_count = 0
    rejected_count = 0
    for row in base_rows:
        case_id = row["sub_question_id"]
        p_row = participation[case_id]
        assessments = p_row["participation_local_assessments"]
        planned = p_row["planned_participation_local_targets"]
        if len(assessments) != len(planned):
            raise ValueError(f"{case_id}: participation target correspondence failed")
        if p_row["participation_compile_status"] != "SUCCEEDED":
            if not args.diagnostic_preserve_rejected:
                raise ValueError(f"{case_id}: rejected participation cannot be merged")
            rejected_count += 1
            # Quarantine the entire participation layer for this case.  The base
            # predicate/relation truths remain executable; none of the conflicting
            # assessments is selected or projected.
            row["participation_local_assessments"] = []
            row["planned_participation_local_targets"] = []
            row["participation_local_target_count"] = 0
            row["planned_participation_local_target_count"] = 0
            row["participation_compile_status"] = "UNRESOLVED_CONFLICT"
            row["participation_compile_errors"] = list(
                p_row.get("participation_compile_errors", [])
            )
            row["quarantined_participation_local_assessments"] = assessments
            row["quarantined_planned_participation_local_targets"] = planned
            row["quarantined_participation_local_target_count"] = len(assessments)
            row["factual_participation_requirement_projection_count"] = 0
            continue

        assessment_instances = {
            _key(value): value for value in row["assessment_instances"]
        }
        top_level = {_key(value): value for value in row["top_level_instances"]}
        requirement_truths: dict[tuple[tuple[str, str, str, str], str], str] = {}
        for assessment in assessments:
            members = assessment["member_instances"]
            for member in members:
                assessment_instances.setdefault(_key(member), member)
            kind = assessment["relation_kind"]
            if kind == "co_principal_group":
                for member in members:
                    top_level.setdefault(_key(member), member)
                continue
            predicate_ref = (
                "legal_element.instigator_intent"
                if kind == "instigation"
                else "legal_element.aiding_intent"
            )
            actor = members[0]
            key = (_key(actor), predicate_ref)
            truth = assessment["truth"]
            previous = requirement_truths.get(key)
            if previous is not None and previous != truth:
                raise ValueError(
                    f"{case_id}: conflicting derivative requirement projections"
                )
            requirement_truths[key] = truth

        existing_truths = {
            (_key(value["instance_key"]), value["predicate_ref"]): value["truth"]
            for value in row["case_truths"]
        }
        for (instance_key, predicate_ref), truth in requirement_truths.items():
            existing = existing_truths.get((instance_key, predicate_ref))
            if existing is not None and existing != truth:
                raise ValueError(f"{case_id}: participation projection truth conflict")
            if existing is None:
                instance = assessment_instances[instance_key]
                row["case_truths"].append(
                    {
                        "instance_key": instance,
                        "predicate_ref": predicate_ref,
                        "truth": truth,
                    }
                )
                projection_count += 1

        row["assessment_instances"] = list(assessment_instances.values())
        row["top_level_instances"] = list(top_level.values())
        row["participation_local_assessments"] = assessments
        row["planned_participation_local_targets"] = planned
        row["participation_local_target_count"] = len(assessments)
        row["planned_participation_local_target_count"] = len(planned)
        row["participation_compile_status"] = "SUCCEEDED"
        row["participation_compile_errors"] = []
        row["physical_request_count"] = int(row["physical_request_count"]) + len(
            assessments
        )
        row["factual_participation_requirement_projection_count"] = len(
            requirement_truths
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in base_rows),
        encoding="utf-8",
    )
    manifest = {
        "step": "v2_factual_participation_call2_merge",
        "status": "DEGRADED_DIAGNOSTIC" if rejected_count else "SUCCEEDED",
        "case_count": len(base_rows),
        "participation_local_target_count": sum(
            row["participation_local_target_count"] for row in base_rows
        ),
        "participation_requirement_projection_count": projection_count,
        "rejected_case_count": rejected_count,
        "base_call2": str(args.base_call2),
        "base_call2_sha256": _sha256(args.base_call2),
        "participation_call2": str(args.participation_call2),
        "participation_call2_sha256": _sha256(args.participation_call2),
        "participation_plan": str(args.participation_plan),
        "participation_plan_sha256": _sha256(args.participation_plan),
    }
    args.out.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
