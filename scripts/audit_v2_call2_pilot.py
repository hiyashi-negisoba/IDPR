#!/usr/bin/env python3
"""Offline exact-key/cardinality audit for gold-scoped Call 2 output."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.v2.registry import load_definitions
from idpr.v2.runtime.grounding import AssessmentTarget, grounding_request_targets
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.participation_grounding import (
    ParticipationGroundingError,
    ParticipationLocalAssessment,
    ParticipationLocalTarget,
    compile_participation_bindings,
)

DEFAULT_DEFINITIONS = ROOT / "data/v2/definitions"


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
    group = value["group_key"]
    return (
        str(value["relation_kind"]),
        str(group["case_id"]),
        str(group["offense_ref"]),
        tuple(
            (
                str(member["case_id"]),
                str(member["actor_id"]),
                str(member["offense_ref"]),
                str(member["occurrence_id"]),
            )
            for member in value["member_instances"]
        ),
    )


def _utilization_key(value: dict[str, Any]) -> tuple[str, ...]:
    action = value["utilizer_action"]
    participant = value["utilized_participant"]
    return (
        str(value["relation_kind"]),
        str(action["case_id"]),
        str(action["actor_id"]),
        str(action["occurrence_id"]),
        str(participant["case_id"]),
        str(participant["participant_id"]),
    )


def _utilized_outcome_key(value: dict[str, Any]) -> tuple[str, str, str]:
    participant = value["participant"]
    return (
        str(participant["case_id"]),
        str(participant["participant_id"]),
        str(value["offense_ref"]),
    )


def _utilized_predicate_key(value: dict[str, Any]) -> tuple[str, str, str, str]:
    return (*_utilized_outcome_key(value), str(value["predicate_ref"]))


def _parse_instance(value: dict[str, Any]) -> OffenseInstanceKey:
    return OffenseInstanceKey(
        str(value["case_id"]),
        str(value["actor_id"]),
        str(value["offense_ref"]),
        str(value["occurrence_id"]),
    )


def _parse_participation_target(value: dict[str, Any]) -> ParticipationLocalTarget:
    return ParticipationLocalTarget(
        str(value["relation_kind"]),
        tuple(_parse_instance(member) for member in value["member_instances"]),
    )


def _parse_participation_assessment(
    value: dict[str, Any],
) -> ParticipationLocalAssessment:
    return ParticipationLocalAssessment(
        _parse_participation_target(value),
        str(value["truth"]),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--plan-artifact", type=Path, required=True)
    parser.add_argument("--definitions", type=Path, default=DEFAULT_DEFINITIONS)
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
    diagnostic_mode = bool(
        manifest.get("diagnostic_continue_participation_errors", False)
    )
    registry = load_definitions(args.definitions)
    physical = general_targets = neural_predicate_targets = relation_targets = participation_targets = 0
    utilization_targets = utilized_outcome_targets = utilized_predicate_targets = 0
    truth_count = article263_pairs = rejected_participation_cases = 0
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
        scheduling = row.get("target_scheduling")
        guard_aware = (
            isinstance(scheduling, dict) and scheduling.get("mode") == "guard_aware"
        )
        if guard_aware:
            planned = scheduling.get("planned_targets")
            asked = scheduling.get("asked_targets")
            skipped = scheduling.get("skipped_targets")
            rounds = scheduling.get("rounds")
            if planned != len(expected):
                errors.append(f"{case_id}: scheduled planned target count mismatch")
            if asked != len(row.get("assessments", [])):
                errors.append(f"{case_id}: scheduled asked target count mismatch")
            if not isinstance(rounds, list) or any(
                not isinstance(value, dict) for value in rounds
            ):
                errors.append(f"{case_id}: malformed target scheduling rounds")
            else:
                if [value.get("round") for value in rounds] != list(
                    range(1, len(rounds) + 1)
                ):
                    errors.append(f"{case_id}: non-contiguous target scheduling rounds")
                if sum(int(value.get("targets", 0)) for value in rounds) != asked:
                    errors.append(f"{case_id}: scheduling round target aggregate mismatch")
            if (
                not isinstance(planned, int)
                or not isinstance(asked, int)
                or not isinstance(skipped, int)
                or planned != asked + skipped
            ):
                errors.append(f"{case_id}: target scheduling cardinality mismatch")
            if row.get("planned_assessment_target_count") != len(expected):
                errors.append(f"{case_id}: planned assessment target count mismatch")
        actual = tuple(_target_key(value) for value in row.get("assessments", []))
        if guard_aware and not set(actual).issubset(set(expected)):
            errors.append(f"{case_id}: scheduled assessment is outside planner targets")
        elif not guard_aware and actual != expected:
            errors.append(f"{case_id}: general assessments do not exactly equal planner targets")
        if len(actual) != len(set(actual)):
            errors.append(f"{case_id}: duplicate general assessment key")
        actual_semantic_targets = tuple(
            AssessmentTarget(
                OffenseInstanceKey(*value[:4]),
                value[4],
            )
            for value in actual
        )
        episode_by_occurrence = {
            str(value["instance_key"]["occurrence_id"]): str(
                value["factual_episode_id"]
            )
            for value in plan.get("instance_provenance", [])
        }
        expected_neural_count = len(
            grounding_request_targets(
                registry,
                actual_semantic_targets,
                episode_by_occurrence=episode_by_occurrence,
            )
        )
        if row.get("neural_predicate_request_target_count") != expected_neural_count:
            errors.append(f"{case_id}: neural predicate request target count mismatch")
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
        expected_participation_values = plan.get("participation_local_targets", [])
        if smoke_limit is not None:
            expected_participation_values = expected_participation_values[:smoke_limit]
        expected_participation = tuple(
            _participation_key(value) for value in expected_participation_values
        )
        participation_assessments = tuple(
            value for value in row.get("participation_local_assessments", [])
        )
        actual_participation = tuple(
            _participation_key(value) for value in participation_assessments
        )
        if actual_participation != expected_participation:
            errors.append(
                f"{case_id}: participation assessments do not exactly equal planner targets"
            )
        if len(actual_participation) != len(set(actual_participation)):
            errors.append(f"{case_id}: duplicate participation local assessment")
        expected_utilization_values = plan.get("factual_utilization_targets", [])
        if smoke_limit is not None:
            expected_utilization_values = expected_utilization_values[:smoke_limit]
        expected_utilization = tuple(
            _utilization_key(value) for value in expected_utilization_values
        )
        actual_utilization = tuple(
            _utilization_key(value)
            for value in row.get("factual_utilization_assessments", [])
        )
        if actual_utilization != expected_utilization:
            errors.append(
                f"{case_id}: factual utilization assessments do not exactly equal planner targets"
            )
        if len(actual_utilization) != len(set(actual_utilization)):
            errors.append(f"{case_id}: duplicate factual utilization assessment")
        expected_outcome_values = plan.get("utilized_participant_outcome_targets", [])
        if smoke_limit is not None:
            expected_outcome_values = expected_outcome_values[:smoke_limit]
        expected_outcomes = tuple(
            _utilized_outcome_key(value) for value in expected_outcome_values
        )
        expected_participant_predicates = tuple(
            (*_utilized_outcome_key(value), str(ref))
            for value in expected_outcome_values
            for ref in value.get("predicate_refs", [])
        )
        actual_participant_predicates = tuple(
            _utilized_predicate_key(value)
            for value in row.get("utilized_participant_predicate_assessments", [])
        )
        if actual_participant_predicates != expected_participant_predicates:
            errors.append(
                f"{case_id}: utilized participant predicates do not exactly equal planner targets"
            )
        if len(actual_participant_predicates) != len(set(actual_participant_predicates)):
            errors.append(f"{case_id}: duplicate utilized participant predicate assessment")
        actual_outcomes = tuple(
            _utilized_outcome_key(value)
            for value in row.get("utilized_participant_outcomes", [])
        )
        if actual_outcomes != expected_outcomes:
            errors.append(
                f"{case_id}: utilized participant outcomes do not exactly equal planner targets"
            )
        if len(actual_outcomes) != len(set(actual_outcomes)):
            errors.append(f"{case_id}: duplicate utilized participant outcome")
        dependency_keys = tuple(
            (
                str(value["utilizer_instance"]["case_id"]),
                str(value["utilizer_instance"]["actor_id"]),
                str(value["utilizer_instance"]["offense_ref"]),
                str(value["utilizer_instance"]["occurrence_id"]),
                str(value["utilized_participant"]["participant_id"]),
            )
            for value in row.get("indirect_principal_dependencies", [])
        )
        if smoke_limit is not None and dependency_keys:
            errors.append(f"{case_id}: partial smoke must not compile indirect dependencies")
        if len(dependency_keys) != len(set(dependency_keys)):
            errors.append(f"{case_id}: duplicate indirect-principal dependency")
        compile_error: ParticipationGroundingError | None = None
        try:
            compile_participation_bindings(
                tuple(
                    _parse_participation_assessment(value)
                    for value in participation_assessments
                ),
                expected_targets=tuple(
                    _parse_participation_target(value)
                    for value in expected_participation_values
                ),
            )
        except ParticipationGroundingError as exc:
            compile_error = exc
        except (KeyError, TypeError) as exc:
            errors.append(f"{case_id}: malformed participation assessment: {exc}")
        recorded_status = row.get("participation_compile_status")
        recorded_errors = row.get("participation_compile_errors")
        if compile_error is None:
            if recorded_status != "SUCCEEDED" or recorded_errors != []:
                errors.append(f"{case_id}: successful participation compile status mismatch")
        elif not diagnostic_mode:
            errors.append(
                f"{case_id}: invalid compiled participation graph: {compile_error}"
            )
        else:
            rejected_participation_cases += 1
            if recorded_status != "REJECTED":
                errors.append(f"{case_id}: rejected participation status is missing")
            if recorded_errors != list(compile_error.errors):
                errors.append(f"{case_id}: rejected participation errors differ from compiler")
        dedicated = row.get("article263_assessments", [])
        if not isinstance(dedicated, list):
            errors.append(f"{case_id}: invalid Article263 assessment container")
            dedicated = []
        expected_truth_keys = set(actual)
        for assessment in dedicated:
            if not isinstance(assessment, dict):
                errors.append(f"{case_id}: malformed Article263 assessment")
                continue
            statutory = assessment.get("statutory_truths", assessment.get("truths", []))
            shared = assessment.get("shared_result_truths", [])
            if not isinstance(statutory, list) or not isinstance(shared, list):
                errors.append(f"{case_id}: malformed Article263 truth arrays")
                continue
            pair = assessment.get("pair", {})
            for endpoint in ("left_instance_key", "right_instance_key"):
                instance = pair.get(endpoint)
                if not isinstance(instance, dict):
                    errors.append(f"{case_id}: malformed Article263 endpoint")
                    continue
                prefix = (
                    str(instance.get("case_id")),
                    str(instance.get("actor_id")),
                    str(instance.get("offense_ref")),
                    str(instance.get("occurrence_id")),
                )
                for value in (*statutory, *shared):
                    if not isinstance(value, dict) or "predicate_ref" not in value:
                        errors.append(f"{case_id}: malformed Article263 truth")
                        continue
                    expected_truth_keys.add((*prefix, str(value["predicate_ref"])))
        if set(truths) != expected_truth_keys:
            errors.append(
                f"{case_id}: CaseTruths keys differ from general + Article263 projections"
            )
        shards = row.get("shards", [])
        if not isinstance(shards, list) or any(
            not isinstance(value, dict) for value in shards
        ):
            errors.append(f"{case_id}: malformed physical request shard ledger")
            shards = []
        recorded_predicate_targets = sum(
            int(value.get("target_count", 0))
            for value in shards
            if value.get("shard_kind") == "predicate"
        )
        if recorded_predicate_targets != expected_neural_count:
            errors.append(f"{case_id}: predicate shard target aggregate mismatch")
        expected_physical_count = len(shards) + int(bool(dedicated))
        if row.get("physical_request_count") != expected_physical_count:
            errors.append(f"{case_id}: physical request count mismatch")
        physical += int(row.get("physical_request_count", 0))
        general_targets += len(actual)
        neural_predicate_targets += expected_neural_count
        relation_targets += len(actual_relations)
        participation_targets += len(actual_participation)
        utilization_targets += len(actual_utilization)
        utilized_outcome_targets += len(actual_outcomes)
        utilized_predicate_targets += len(actual_participant_predicates)
        truth_count += len(truths)
        article263_pairs += len(dedicated)
    if physical != manifest.get("physical_request_count"):
        errors.append("physical request aggregate mismatch")
    if general_targets != manifest.get("assessment_target_count"):
        errors.append("general target aggregate mismatch")
    if neural_predicate_targets != manifest.get("neural_predicate_request_target_count"):
        errors.append("neural predicate request target aggregate mismatch")
    if relation_targets != manifest.get("relation_assessment_target_count"):
        errors.append("relation target aggregate mismatch")
    if participation_targets != manifest.get("participation_local_target_count"):
        errors.append("participation target aggregate mismatch")
    if utilization_targets != manifest.get("factual_utilization_target_count"):
        errors.append("factual utilization target aggregate mismatch")
    if utilized_outcome_targets != manifest.get(
        "utilized_participant_outcome_target_count"
    ):
        errors.append("utilized participant outcome target aggregate mismatch")
    if utilized_predicate_targets != manifest.get(
        "utilized_participant_predicate_target_count"
    ):
        errors.append("utilized participant predicate target aggregate mismatch")
    if rejected_participation_cases != manifest.get(
        "participation_rejected_case_count"
    ):
        errors.append("rejected participation case aggregate mismatch")
    if diagnostic_mode and manifest.get("status") != "DEGRADED_DIAGNOSTIC":
        errors.append("diagnostic manifest status mismatch")
    report = {
        "step": "v2_gold_occurrence_call2_audit",
        "run_status": (
            "DEGRADED_DIAGNOSTIC"
            if diagnostic_mode and not errors
            else "SUCCEEDED"
            if not errors
            else "FAILED"
        ),
        "case_count": len(rows),
        "general_assessment_target_count": general_targets,
        "neural_predicate_request_target_count": neural_predicate_targets,
        "relation_assessment_target_count": relation_targets,
        "participation_local_target_count": participation_targets,
        "factual_utilization_target_count": utilization_targets,
        "utilized_participant_outcome_target_count": utilized_outcome_targets,
        "utilized_participant_predicate_target_count": utilized_predicate_targets,
        "participation_rejected_case_count": rejected_participation_cases,
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
