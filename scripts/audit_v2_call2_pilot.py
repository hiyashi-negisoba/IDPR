#!/usr/bin/env python3
"""Offline exact-key/cardinality audit for gold-scoped Call 2 output."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{path}: expected object")
    return value


def _jsonl(path: Path) -> list[dict[str, Any]]:
    values = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
    if not all(isinstance(value, dict) for value in values):
        raise ValueError(f"{path}: expected object rows")
    return values


def _target_key(value: dict[str, Any]) -> tuple[str, str, str, str, str]:
    key = value["instance_key"]
    return (
        str(key["case_id"]), str(key["actor_id"]), str(key["offense_ref"]),
        str(key["occurrence_id"]), str(value["predicate_ref"]),
    )


def _relation_key(value: dict[str, Any]) -> tuple[Any, ...]:
    instance = value["instance_key"]
    relation = value["relation_key"]
    endpoints = value["endpoints"]
    return (
        str(instance["case_id"]),
        str(instance["actor_id"]),
        str(instance["offense_ref"]),
        str(instance["occurrence_id"]),
        tuple(str(item) for item in relation["occurrence_path"]),
        str(relation["relation_ref"]),
        str(relation["left_local_key"]),
        str(relation["right_local_key"]),
        str(endpoints["left_ref"]),
        str(endpoints["right_ref"]),
        str(endpoints["left_view"]),
        str(endpoints["right_view"]),
    )


def _participation_key(value: dict[str, Any]) -> tuple[Any, ...]:
    participant = value["participant_instance"]
    options = tuple(
        (
            str(option["option_id"]),
            str(option["mode"]),
            tuple(
                (
                    str(source["case_id"]),
                    str(source["actor_id"]),
                    str(source["offense_ref"]),
                    str(source["occurrence_id"]),
                )
                for source in option["source_instances"]
            ),
        )
        for option in value["route_options"]
    )
    return (
        str(participant["case_id"]),
        str(participant["actor_id"]),
        str(participant["offense_ref"]),
        str(participant["occurrence_id"]),
        options,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--plan-artifact", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    output = args.out or args.artifact.with_suffix(".audit.json")
    rows = _jsonl(args.artifact)
    plans = {value["sub_question_id"]: value for value in _jsonl(args.plan_artifact)}
    manifest = _json(args.manifest)
    smoke_limit = manifest.get("smoke_target_limit")
    if smoke_limit is not None and (not isinstance(smoke_limit, int) or smoke_limit <= 0):
        raise ValueError("manifest smoke_target_limit must be positive or null")
    errors: list[str] = []
    row_ids = [str(value.get("sub_question_id")) for value in rows]
    if row_ids != manifest.get("case_ids"):
        errors.append("artifact order differs from manifest case_ids")
    if manifest.get("plan_artifact_sha256") != _sha256(args.plan_artifact):
        errors.append("plan artifact hash mismatch")
    physical = general_targets = relation_targets = participation_targets = truth_count = article263_pairs = 0
    for row in rows:
        case_id = str(row.get("sub_question_id"))
        plan = plans.get(case_id)
        if plan is None:
            errors.append(f"{case_id}: missing planner row")
            continue
        expected_values = plan["assessment_targets"]
        if smoke_limit is not None:
            expected_values = expected_values[:smoke_limit]
        expected = tuple(_target_key(value) for value in expected_values)
        actual = tuple(_target_key(value) for value in row.get("assessments", []))
        if actual != expected:
            errors.append(f"{case_id}: general assessments do not exactly equal planner targets")
        if len(actual) != len(set(actual)):
            errors.append(f"{case_id}: duplicate general assessment key")
        truths = tuple(_target_key(value) for value in row.get("case_truths", []))
        if len(truths) != len(set(truths)):
            errors.append(f"{case_id}: duplicate CaseTruths key")
        if not set(actual).issubset(truths):
            errors.append(f"{case_id}: general assessment missing from CaseTruths")
        expected_relation_values = plan.get("relation_assessment_targets", [])
        if smoke_limit is not None:
            expected_relation_values = expected_relation_values[:smoke_limit]
        expected_relations = tuple(_relation_key(value) for value in expected_relation_values)
        actual_relations = tuple(
            _relation_key(value) for value in row.get("case_relation_truths", [])
        )
        if actual_relations != expected_relations:
            errors.append(f"{case_id}: relation truths do not exactly equal planner targets")
        if len(actual_relations) != len(set(actual_relations)):
            errors.append(f"{case_id}: duplicate relation truth key")
        expected_participation_values = plan.get("participation_route_targets", [])
        if smoke_limit is not None:
            expected_participation_values = expected_participation_values[:smoke_limit]
        expected_participation = tuple(
            _participation_key(value) for value in expected_participation_values
        )
        actual_participation = tuple(
            _participation_key(value)
            for value in row.get("participation_route_assessments", [])
        )
        if actual_participation != expected_participation:
            errors.append(
                f"{case_id}: participation assessments do not exactly equal planner targets"
            )
        if len(actual_participation) != len(set(actual_participation)):
            errors.append(f"{case_id}: duplicate participation assessment key")
        dedicated = row.get("article263_assessments", [])
        if not isinstance(dedicated, list):
            errors.append(f"{case_id}: invalid Article263 assessment container")
            dedicated = []
        expected_truth_count = len(actual) + 6 * len(dedicated)
        if len(truths) != expected_truth_count:
            errors.append(
                f"{case_id}: CaseTruths count {len(truths)} != {expected_truth_count}"
            )
        physical += int(row.get("physical_request_count", 0))
        general_targets += len(actual)
        relation_targets += len(actual_relations)
        participation_targets += len(actual_participation)
        truth_count += len(truths)
        article263_pairs += len(dedicated)
    if physical != manifest.get("physical_request_count"):
        errors.append("physical request aggregate mismatch")
    if general_targets != manifest.get("assessment_target_count"):
        errors.append("general target aggregate mismatch")
    if relation_targets != manifest.get("relation_assessment_target_count"):
        errors.append("relation target aggregate mismatch")
    if participation_targets != manifest.get("participation_route_target_count"):
        errors.append("participation target aggregate mismatch")
    report = {
        "step": "v2_gold_occurrence_call2_audit",
        "run_status": "SUCCEEDED" if not errors else "FAILED",
        "case_count": len(rows),
        "general_assessment_target_count": general_targets,
        "relation_assessment_target_count": relation_targets,
        "participation_route_target_count": participation_targets,
        "case_truth_count": truth_count,
        "article263_pair_count": article263_pairs,
        "physical_request_count": physical,
        "errors": errors,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {output}")
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
