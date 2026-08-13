#!/usr/bin/env python3
"""Run occurrence-scoped Call 2 shards and emit exact-key CaseTruths rows."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.eval.input_formatter import assert_no_leaked_fields
from idpr.neural.vllm_client import VLLMClient
from idpr.prompts import load_prompt
from idpr.v2.gold_factual_identity import (
    GoldOccurrence,
    load_gold_article263_pairs,
    load_gold_factual_participants,
    load_gold_occurrences,
)
from idpr.v2.question_assumptions import load_question_assumptions
from idpr.v2.registry import load_definitions
from idpr.v2.relations import RelationInstanceKey
from idpr.v2.runtime.article263_grounding import (
    Article263OccurrencePair,
    add_article263_truths,
    article263_request_payload,
    article263_schema,
    plan_article263_occurrence_pairs,
    validate_article263_output,
)
from idpr.v2.runtime.grounding import (
    AssessmentTarget,
    call2_request_payload,
    call2_schema,
    case_truths_from_assessments,
    expand_ground_fact_assessments,
    grounding_request_targets,
    predicate_definitions,
    shard_assessment_targets_by_occurrence,
    validate_call2_output,
)
from idpr.v2.runtime.identity import (
    FactualActionKey,
    FactualParticipantKey,
    OffenseInstanceKey,
    RuntimeRelationKey,
)
from idpr.v2.runtime.indirect_principal_grounding import (
    FactualUtilizationTarget,
    compile_indirect_principal_dependencies,
    factual_utilization_request_payload,
    factual_utilization_schema,
    validate_factual_utilization_output,
)
from idpr.v2.runtime.participation_grounding import (
    ParticipationGroundingError,
    ParticipationLocalTarget,
    compile_participation_bindings,
    participation_request_payload,
    participation_schema,
    validate_participation_output,
)
from idpr.v2.runtime.relation_grounding import (
    RelationAssessmentTarget,
    add_relation_assessments,
    relation_definitions,
    relation_request_payload,
    relation_schema,
    shard_relation_targets_by_occurrence,
    validate_relation_output,
)
from idpr.v2.runtime.utilized_participant_outcome import (
    UtilizedParticipantOutcomeTarget,
    UtilizedParticipantPredicateTarget,
    produce_utilized_participant_outcomes,
    utilized_participant_request_payload,
    utilized_participant_schema,
    validate_utilized_participant_output,
)

DEFAULT_DEFINITIONS = ROOT / "data/v2/definitions"
DEFAULT_INVENTORY = ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl"
DEFAULT_QUESTION_ASSUMPTIONS = ROOT / "data/v2/question_assumptions.jsonl"
DEFAULT_FACTUAL_PARTICIPANTS = ROOT / "data/v2/gold_factual_participants.jsonl"
PROMPTS = ("v2_call2_grounding", "v2_call2_grounding_user")
ARTICLE263_PROMPTS = ("v2_call2_article263", "v2_call2_article263_user")
RELATION_PROMPTS = ("v2_call2_relation", "v2_call2_relation_user")
PARTICIPATION_PROMPTS = ("v2_call2_participation", "v2_call2_participation_user")
UTILIZATION_PROMPTS = ("v2_call2_utilization", "v2_call2_utilization_user")
UTILIZED_OUTCOME_PROMPTS = (
    "v2_call2_utilized_participant_outcome",
    "v2_call2_utilized_participant_outcome_user",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    values = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
    if not all(isinstance(value, dict) for value in values):
        raise ValueError(f"{path}: every row must be an object")
    return values


def _index(rows: Iterable[Mapping[str, Any]], label: str) -> dict[str, Mapping[str, Any]]:
    values = tuple(rows)
    result = {str(value.get("sub_question_id")): value for value in values}
    if len(result) != len(values):
        raise ValueError(f"{label}: duplicate sub_question_id")
    return result


def _occurrences(row: Mapping[str, Any]) -> tuple[GoldOccurrence, ...]:
    return tuple(
        GoldOccurrence(
            str(value["occurrence_id"]),
            str(value["actor_id"]),
            str(value["source_text"]),
            int(value["source_span"]["start"]),
            int(value["source_span"]["end"]),
        )
        for value in row["occurrences"]
    )


def _instances(row: Mapping[str, Any]) -> tuple[OffenseInstanceKey, ...]:
    return tuple(
        OffenseInstanceKey(
            str(value["case_id"]),
            str(value["actor_id"]),
            str(value["offense_ref"]),
            str(value["occurrence_id"]),
        )
        for value in row["assessment_instances"]
    )


def _article263_pair_candidates(
    row: Mapping[str, Any],
) -> tuple[Article263OccurrencePair, ...]:
    def instance(value: Mapping[str, Any]) -> OffenseInstanceKey:
        return OffenseInstanceKey(
            str(value["case_id"]),
            str(value["actor_id"]),
            str(value["offense_ref"]),
            str(value["occurrence_id"]),
        )

    output = []
    for value in row.get("article263_pair_candidates", []):
        evidence = value["relation_evidence"]
        span = evidence["source_span"]
        output.append(
            Article263OccurrencePair(
                str(value["pair_id"]),
                instance(value["left_instance_key"]),
                instance(value["right_instance_key"]),
                str(evidence["source_text"]),
                int(span["start"]),
                int(span["end"]),
            )
        )
    return tuple(output)


def _targets(row: Mapping[str, Any]) -> tuple[AssessmentTarget, ...]:
    values = []
    for value in row["assessment_targets"]:
        key = value["instance_key"]
        values.append(
            AssessmentTarget(
                OffenseInstanceKey(
                    str(key["case_id"]),
                    str(key["actor_id"]),
                    str(key["offense_ref"]),
                    str(key["occurrence_id"]),
                ),
                str(value["predicate_ref"]),
            )
        )
    return tuple(values)


def _relation_targets(row: Mapping[str, Any]) -> tuple[RelationAssessmentTarget, ...]:
    output = []
    for value in row["relation_assessment_targets"]:
        raw_instance = value["instance_key"]
        raw_relation = value["relation_key"]
        endpoints = value["endpoints"]
        instance = OffenseInstanceKey(
            str(raw_instance["case_id"]),
            str(raw_instance["actor_id"]),
            str(raw_instance["offense_ref"]),
            str(raw_instance["occurrence_id"]),
        )
        definition = RelationInstanceKey(
            tuple(str(item) for item in raw_relation["occurrence_path"]),
            str(raw_relation["relation_ref"]),
            str(raw_relation["left_local_key"]),
            str(raw_relation["right_local_key"]),
        )
        output.append(
            RelationAssessmentTarget(
                RuntimeRelationKey(instance, definition),
                str(endpoints["left_ref"]),
                str(endpoints["right_ref"]),
                str(endpoints["left_view"]),
                str(endpoints["right_view"]),
            )
        )
    return tuple(output)


def _participation_targets(
    row: Mapping[str, Any],
) -> tuple[ParticipationLocalTarget, ...]:
    def parse(value: Mapping[str, Any]) -> OffenseInstanceKey:
        return OffenseInstanceKey(
            str(value["case_id"]),
            str(value["actor_id"]),
            str(value["offense_ref"]),
            str(value["occurrence_id"]),
        )

    return tuple(
        ParticipationLocalTarget(
            str(value["relation_kind"]),
            tuple(parse(item) for item in value["member_instances"]),
        )
        for value in row["participation_local_targets"]
    )


def _utilization_targets(
    row: Mapping[str, Any],
) -> tuple[FactualUtilizationTarget, ...]:
    return tuple(
        FactualUtilizationTarget(
            FactualActionKey(
                str(value["utilizer_action"]["case_id"]),
                str(value["utilizer_action"]["actor_id"]),
                str(value["utilizer_action"]["occurrence_id"]),
            ),
            FactualParticipantKey(
                str(value["utilized_participant"]["case_id"]),
                str(value["utilized_participant"]["participant_id"]),
            ),
        )
        for value in row.get("factual_utilization_targets", [])
    )


def _utilized_outcome_targets(
    row: Mapping[str, Any],
) -> tuple[
    tuple[UtilizedParticipantOutcomeTarget, tuple[UtilizedParticipantPredicateTarget, ...]],
    ...,
]:
    output = []
    for value in row.get("utilized_participant_outcome_targets", []):
        raw_participant = value["participant"]
        target = UtilizedParticipantOutcomeTarget(
            FactualParticipantKey(
                str(raw_participant["case_id"]),
                str(raw_participant["participant_id"]),
            ),
            str(value["offense_ref"]),
        )
        output.append(
            (
                target,
                tuple(
                    UtilizedParticipantPredicateTarget(target, str(ref))
                    for ref in value["predicate_refs"]
                ),
            )
        )
    return tuple(output)


def _top_level_instances(row: Mapping[str, Any]) -> tuple[OffenseInstanceKey, ...]:
    return tuple(
        OffenseInstanceKey(
            str(value["case_id"]),
            str(value["actor_id"]),
            str(value["offense_ref"]),
            str(value["occurrence_id"]),
        )
        for value in row["top_level_instances"]
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--api-key", default="local-idpr")
    parser.add_argument("--call1-artifact", type=Path, required=True)
    parser.add_argument("--gold-occurrences", type=Path, required=True)
    parser.add_argument("--gold-article263-pairs", type=Path, required=True)
    parser.add_argument(
        "--gold-factual-participants",
        type=Path,
        default=DEFAULT_FACTUAL_PARTICIPANTS,
    )
    parser.add_argument("--plan-artifact", type=Path, required=True)
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument(
        "--question-assumptions",
        type=Path,
        default=DEFAULT_QUESTION_ASSUMPTIONS,
    )
    parser.add_argument("--definitions", type=Path, default=DEFAULT_DEFINITIONS)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--case-id", action="append", default=[])
    parser.add_argument("--max-targets-per-request", type=int, default=24)
    parser.add_argument(
        "--smoke-target-limit",
        type=int,
        help="explicit partial smoke only; manifest is never marked full SUCCEEDED",
    )
    parser.add_argument("--max-tokens", type=int, default=4096)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument(
        "--planner-occurrence-evidence",
        action="store_true",
        help=(
            "use factual occurrences serialized by the binding-scoped planner; "
            "do not load offline gold occurrences, factual participants, or Article 263 pairs"
        ),
    )
    parser.add_argument(
        "--diagnostic-continue-participation-errors",
        action="store_true",
        help=(
            "record rejected participation cases and continue; never produces an "
            "acceptance artifact"
        ),
    )
    parser.add_argument("--prompt-approved", action="store_true")
    args = parser.parse_args()
    if not args.prompt_approved:
        parser.error("--prompt-approved is required before a Call 2 model run")

    call1 = _index(_read_jsonl(args.call1_artifact), "Call 1")
    plans = _index(_read_jsonl(args.plan_artifact), "planner")
    inventory = _index(_read_jsonl(args.inventory), "inventory")
    question_assumptions = load_question_assumptions(
        args.question_assumptions,
        question_prompt_by_id={
            key: str(value["question_prompt"]) for key, value in inventory.items()
        },
    )
    if args.planner_occurrence_evidence:
        gold_by_case = {}
        participants_by_case = {}
        pair_bindings = ()
    else:
        gold_by_case = load_gold_occurrences(
            args.gold_occurrences,
            case_text_by_id={
                key: str(value["question_text"]) for key, value in inventory.items()
            },
            required_case_ids=plans,
        )
        participants_by_case = load_gold_factual_participants(
            args.gold_factual_participants,
            case_text_by_id={
                key: str(value["question_text"]) for key, value in inventory.items()
            },
        )
        pair_bindings = load_gold_article263_pairs(
            args.gold_article263_pairs,
            occurrences_by_id=gold_by_case,
            case_text_by_id={
                key: str(value["question_text"]) for key, value in inventory.items()
            },
        )
    selected = tuple(args.case_id) if args.case_id else tuple(plans)
    missing = [
        value
        for value in selected
        if value not in call1
        or (not args.planner_occurrence_evidence and value not in gold_by_case)
        or value not in plans
        or value not in inventory
    ]
    if missing:
        raise ValueError(f"missing selected cases: {missing}")

    registry = load_definitions(args.definitions)
    client = VLLMClient(args.base_url, args.model, args.api_key)
    system_prompt, user_prompt = (load_prompt(value) for value in PROMPTS)
    article263_system, article263_user = (
        load_prompt(value) for value in ARTICLE263_PROMPTS
    )
    relation_system, relation_user = (load_prompt(value) for value in RELATION_PROMPTS)
    participation_system, participation_user = (
        load_prompt(value) for value in PARTICIPATION_PROMPTS
    )
    utilization_system, utilization_user = (
        load_prompt(value) for value in UTILIZATION_PROMPTS
    )
    utilized_outcome_system, utilized_outcome_user = (
        load_prompt(value) for value in UTILIZED_OUTCOME_PROMPTS
    )
    output: list[dict[str, Any]] = []
    aggregate_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    physical_requests = 0
    rejected_participation_case_count = 0
    for case_index, case_id in enumerate(selected, start=1):
        plan_row = plans[case_id]
        planned_occurrences = _occurrences(plan_row)
        if args.planner_occurrence_evidence:
            occurrences = planned_occurrences
        else:
            occurrences = gold_by_case[case_id].occurrences
            planned_identity = tuple(
                (value.occurrence_id, value.actor_id) for value in planned_occurrences
            )
            gold_identity = tuple(
                (value.occurrence_id, value.actor_id) for value in occurrences
            )
            if planned_identity != gold_identity:
                raise ValueError(f"{case_id}: planner/gold occurrence identity mismatch")
        instances = _instances(plan_row)
        refs = tuple(str(value) for value in plan_row["selected_predicate_refs"])
        predicates = predicate_definitions(registry, refs)
        planned_targets = _targets(plan_row)
        if any(target.instance_key not in set(instances) for target in planned_targets):
            raise ValueError(f"{case_id}: target instance is outside assessment universe")
        targets = (
            planned_targets[: args.smoke_target_limit]
            if args.smoke_target_limit is not None
            else planned_targets
        )
        if args.smoke_target_limit is not None and args.smoke_target_limit <= 0:
            raise ValueError("--smoke-target-limit must be positive")
        request_targets = grounding_request_targets(registry, targets)
        shards = shard_assessment_targets_by_occurrence(
            request_targets, max_targets=args.max_targets_per_request
        )
        request_assessments = []
        shard_records = []
        occurrence_by_id = {value.occurrence_id: value for value in occurrences}
        predicate_by_ref = {value.predicate_ref: value for value in predicates}
        for shard_index, shard in enumerate(shards, start=1):
            shard_occurrence_ids = tuple(
                dict.fromkeys(value.instance_key.occurrence_id for value in shard)
            )
            if len(shard_occurrence_ids) != 1:
                raise AssertionError("physical Call 2 shard crossed an occurrence boundary")
            evidence_occurrence = occurrence_by_id[shard_occurrence_ids[0]]
            shard_predicate_refs = tuple(
                dict.fromkeys(value.predicate_ref for value in shard)
            )
            payload = call2_request_payload(
                evidence_occurrence=evidence_occurrence,
                question_assumptions=question_assumptions.get(case_id, ()),
                predicates=tuple(predicate_by_ref[value] for value in shard_predicate_refs),
                targets=shard,
            )
            assert_no_leaked_fields(payload)
            raw, metadata = client.complete_json(
                system_prompt=system_prompt,
                payload=payload,
                schema_name="v2_occurrence_scoped_call2",
                schema=call2_schema(shard),
                max_tokens=args.max_tokens,
                temperature=args.temperature,
                user_template=user_prompt,
            )
            validated = validate_call2_output(raw, targets=shard)
            request_assessments.extend(validated)
            usage = metadata.get("usage", {})
            for key in aggregate_usage:
                aggregate_usage[key] += int(usage.get(key, 0) or 0)
            physical_requests += 1
            shard_records.append({
                "shard_kind": "predicate",
                "shard_index": shard_index,
                "target_count": len(shard),
                "evidence_occurrence_id": evidence_occurrence.occurrence_id,
                "predicate_definition_count": len(shard_predicate_refs),
                "usage": usage,
                "model_response": {
                    "id": metadata.get("id"),
                    "finish_reason": metadata.get("finish_reason"),
                },
            })
        assessments = expand_ground_fact_assessments(
            registry, request_assessments, expected_targets=targets
        )
        truths = case_truths_from_assessments(assessments, expected_targets=targets)
        planned_relation_targets = _relation_targets(plan_row)
        relation_targets = (
            planned_relation_targets[: args.smoke_target_limit]
            if args.smoke_target_limit is not None
            else planned_relation_targets
        )
        relation_assessments = []
        relation_shards = shard_relation_targets_by_occurrence(
            relation_targets, max_targets=args.max_targets_per_request
        )
        for relation_shard_index, relation_shard in enumerate(relation_shards, start=1):
            occurrence_ids = {
                value.key.instance.occurrence_id for value in relation_shard
            }
            if len(occurrence_ids) != 1:
                raise AssertionError("relation shard crossed an occurrence boundary")
            evidence_occurrence = occurrence_by_id[next(iter(occurrence_ids))]
            refs = tuple(
                dict.fromkeys(
                    value.key.definition_key.relation_ref for value in relation_shard
                )
            )
            payload = relation_request_payload(
                evidence_occurrence=evidence_occurrence,
                definitions=relation_definitions(registry, refs),
                targets=relation_shard,
            )
            assert_no_leaked_fields(payload)
            raw, metadata = client.complete_json(
                system_prompt=relation_system,
                payload=payload,
                schema_name="v2_occurrence_scoped_relation_call2",
                schema=relation_schema(relation_shard),
                max_tokens=args.max_tokens,
                temperature=args.temperature,
                user_template=relation_user,
            )
            relation_assessments.extend(
                validate_relation_output(raw, targets=relation_shard)
            )
            usage = metadata.get("usage", {})
            for key in aggregate_usage:
                aggregate_usage[key] += int(usage.get(key, 0) or 0)
            physical_requests += 1
            shard_records.append(
                {
                    "shard_kind": "relation",
                    "shard_index": relation_shard_index,
                    "target_count": len(relation_shard),
                    "evidence_occurrence_id": evidence_occurrence.occurrence_id,
                    "usage": usage,
                    "model_response": {
                        "id": metadata.get("id"),
                        "finish_reason": metadata.get("finish_reason"),
                    },
                }
            )
        truths = add_relation_assessments(truths, relation_assessments)
        planned_participation_targets = _participation_targets(plan_row)
        participation_targets = (
            planned_participation_targets[: args.smoke_target_limit]
            if args.smoke_target_limit is not None
            else planned_participation_targets
        )
        participation_assessments = []
        for participation_shard_index, participation_target in enumerate(
            participation_targets, start=1
        ):
            occurrence_ids = {
                member.occurrence_id for member in participation_target.members
            }
            evidence = tuple(occurrence_by_id[value] for value in sorted(occurrence_ids))
            payload = participation_request_payload(
                registry=registry,
                occurrences=evidence,
                targets=(participation_target,),
            )
            assert_no_leaked_fields(payload)
            raw, metadata = client.complete_json(
                system_prompt=participation_system,
                payload=payload,
                schema_name="v2_local_participation_relation_call2",
                schema=participation_schema((participation_target,)),
                max_tokens=args.max_tokens,
                temperature=args.temperature,
                user_template=participation_user,
            )
            try:
                participation_assessments.append(
                    validate_participation_output(raw, targets=(participation_target,))
                )
            except ParticipationGroundingError as exc:
                raise ParticipationGroundingError(
                    [
                        f"target={participation_target.as_dict()!r}",
                        f"raw={raw!r}",
                        *exc.errors,
                    ]
                ) from exc
            usage = metadata.get("usage", {})
            for key in aggregate_usage:
                aggregate_usage[key] += int(usage.get(key, 0) or 0)
            physical_requests += 1
            shard_records.append(
                {
                    "shard_kind": "participation",
                    "shard_index": participation_shard_index,
                    "target_count": 1,
                    "group_key": {
                        "case_id": participation_target.case_id,
                        "offense_ref": participation_target.offense_ref,
                    },
                    "relation_kind": participation_target.kind,
                    "evidence_occurrence_ids": sorted(occurrence_ids),
                    "usage": usage,
                    "model_response": {
                        "id": metadata.get("id"),
                        "finish_reason": metadata.get("finish_reason"),
                    },
                }
            )
        participation_compile_status = "SUCCEEDED"
        participation_compile_errors: list[str] = []
        try:
            compile_participation_bindings(
                participation_assessments,
                expected_targets=participation_targets,
            )
        except ParticipationGroundingError as exc:
            truth_counts = {
                truth: sum(value.truth == truth for value in participation_assessments)
                for truth in ("TRUE", "FALSE", "UNKNOWN")
            }
            diagnostic_errors = [
                f"case_id={case_id}",
                f"truth_counts={truth_counts!r}",
                "positive_local_assessments="
                + repr(
                    [
                        value.as_dict()
                        for value in participation_assessments
                        if value.truth == "TRUE"
                    ]
                ),
                *exc.errors,
            ]
            if not args.diagnostic_continue_participation_errors:
                raise ParticipationGroundingError(diagnostic_errors) from exc
            participation_compile_status = "REJECTED"
            participation_compile_errors = list(exc.errors)
            rejected_participation_case_count += 1
        planned_utilization_targets = _utilization_targets(plan_row)
        utilization_targets = (
            planned_utilization_targets[: args.smoke_target_limit]
            if args.smoke_target_limit is not None
            else planned_utilization_targets
        )
        factual_participants = (
            participants_by_case[case_id].participants
            if case_id in participants_by_case
            else ()
        )
        utilization_assessments = []
        for utilization_index, utilization_target in enumerate(
            utilization_targets, start=1
        ):
            payload = factual_utilization_request_payload(
                occurrences=occurrences,
                participants=factual_participants,
                targets=(utilization_target,),
            )
            assert_no_leaked_fields(payload)
            raw, metadata = client.complete_json(
                system_prompt=utilization_system,
                payload=payload,
                schema_name="v2_factual_utilization_relation_call2",
                schema=factual_utilization_schema(utilization_target),
                max_tokens=args.max_tokens,
                temperature=args.temperature,
                user_template=utilization_user,
            )
            utilization_assessments.append(
                validate_factual_utilization_output(raw, target=utilization_target)
            )
            usage = metadata.get("usage", {})
            for key in aggregate_usage:
                aggregate_usage[key] += int(usage.get(key, 0) or 0)
            physical_requests += 1
            shard_records.append(
                {
                    "shard_kind": "factual_utilization",
                    "shard_index": utilization_index,
                    "target_count": 1,
                    "utilizer_occurrence_id": (
                        utilization_target.utilizer_action.occurrence_id
                    ),
                    "utilized_participant_id": (
                        utilization_target.utilized_participant.participant_id
                    ),
                    "usage": usage,
                    "model_response": {
                        "id": metadata.get("id"),
                        "finish_reason": metadata.get("finish_reason"),
                    },
                }
            )
        planned_outcome_bundles = _utilized_outcome_targets(plan_row)
        outcome_bundles = (
            planned_outcome_bundles[: args.smoke_target_limit]
            if args.smoke_target_limit is not None
            else planned_outcome_bundles
        )
        participant_by_id = {
            value.participant_id: value for value in factual_participants
        }
        outcome_targets = []
        participant_predicate_assessments = []
        for outcome_index, (outcome_target, predicate_targets) in enumerate(
            outcome_bundles, start=1
        ):
            participant = participant_by_id.get(outcome_target.participant.participant_id)
            if participant is None:
                raise ValueError(
                    f"{case_id}: utilized outcome participant evidence is missing"
                )
            payload = utilized_participant_request_payload(
                registry,
                participant=participant,
                outcome_target=outcome_target,
                predicate_targets=predicate_targets,
            )
            assert_no_leaked_fields(payload)
            raw, metadata = client.complete_json(
                system_prompt=utilized_outcome_system,
                payload=payload,
                schema_name="v2_utilized_participant_predicate_call2",
                schema=utilized_participant_schema(predicate_targets),
                max_tokens=args.max_tokens,
                temperature=args.temperature,
                user_template=utilized_outcome_user,
            )
            outcome_targets.append(outcome_target)
            participant_predicate_assessments.extend(
                validate_utilized_participant_output(
                    raw, predicate_targets=predicate_targets
                )
            )
            usage = metadata.get("usage", {})
            for key in aggregate_usage:
                aggregate_usage[key] += int(usage.get(key, 0) or 0)
            physical_requests += 1
            shard_records.append(
                {
                    "shard_kind": "utilized_participant_predicates",
                    "shard_index": outcome_index,
                    "target_count": len(predicate_targets),
                    "utilized_participant_id": outcome_target.participant.participant_id,
                    "offense_ref": outcome_target.offense_ref,
                    "usage": usage,
                    "model_response": {
                        "id": metadata.get("id"),
                        "finish_reason": metadata.get("finish_reason"),
                    },
                }
            )
        utilized_outcomes = produce_utilized_participant_outcomes(
            registry,
            outcome_targets,
            participant_predicate_assessments,
        )
        indirect_dependencies = ()
        if args.smoke_target_limit is None:
            indirect_dependencies = compile_indirect_principal_dependencies(
                registry,
                _top_level_instances(plan_row),
                factual_participants,
                tuple(utilization_assessments),
                utilized_outcomes,
            )
        if args.planner_occurrence_evidence:
            article263_pairs = _article263_pair_candidates(plan_row)
        else:
            bindings = tuple(
                value for value in pair_bindings if value.sub_question_id == case_id
            )
            article263_pairs = plan_article263_occurrence_pairs(bindings, instances)
        article263_records = []
        article263_assessments = ()
        if article263_pairs:
            article263_payload = article263_request_payload(
                occurrences=tuple(
                    occurrence
                    for occurrence in occurrences
                    if occurrence.occurrence_id
                    in {
                        instance.occurrence_id
                        for pair in article263_pairs
                        for instance in (pair.left, pair.right)
                    }
                ),
                pairs=article263_pairs,
            )
            assert_no_leaked_fields(article263_payload)
            article263_raw, article263_metadata = client.complete_json(
                system_prompt=article263_system,
                payload=article263_payload,
                schema_name="v2_article263_call2",
                schema=article263_schema(article263_pairs),
                max_tokens=args.max_tokens,
                temperature=args.temperature,
                user_template=article263_user,
            )
            article263_assessments = validate_article263_output(
                article263_raw, pairs=article263_pairs
            )
            truths = add_article263_truths(truths, article263_assessments)
            usage = article263_metadata.get("usage", {})
            for key in aggregate_usage:
                aggregate_usage[key] += int(usage.get(key, 0) or 0)
            physical_requests += 1
            article263_records = [
                {
                    "pair": value.pair.as_dict(),
                    "statutory_truths": [
                        {
                            "predicate_ref": ref,
                            "truth": truth,
                        }
                        for ref, truth in value.truths
                    ],
                    "shared_result_truths": [
                        {
                            "predicate_ref": ref,
                            "truth": truth,
                        }
                        for ref, truth in value.shared_result_truths
                    ],
                }
                for value in article263_assessments
            ]
        projected_truths = [
            {
                "instance_key": {
                    "case_id": instance.case_id,
                    "actor_id": instance.actor_id,
                    "offense_ref": instance.offense_ref,
                    "occurrence_id": instance.occurrence_id,
                },
                "predicate_ref": ref,
                "truth": truth,
            }
            for (instance, ref), truth in truths.predicate.items()
        ]
        projected_relation_truths = [
            {
                **value.target.as_dict(),
                "truth": value.truth,
            }
            for value in relation_assessments
        ]
        output.append({
            "sub_question_id": case_id,
            "logical_stage": "Call 2",
            "physical_request_count": (
                len(shards)
                + len(relation_shards)
                + len(participation_targets)
                + len(utilization_targets)
                + len(outcome_bundles)
                + int(bool(article263_pairs))
            ),
            "assessment_target_count": len(targets),
            "neural_predicate_request_target_count": len(request_targets),
            "relation_assessment_target_count": len(relation_assessments),
            "planned_relation_assessment_target_count": len(planned_relation_targets),
            "participation_local_target_count": len(participation_assessments),
            "planned_participation_local_target_count": len(
                planned_participation_targets
            ),
            "factual_utilization_target_count": len(utilization_assessments),
            "planned_factual_utilization_target_count": len(
                planned_utilization_targets
            ),
            "utilized_participant_outcome_target_count": len(utilized_outcomes),
            "planned_utilized_participant_outcome_target_count": len(
                planned_outcome_bundles
            ),
            "utilized_participant_predicate_target_count": len(
                participant_predicate_assessments
            ),
            "planned_assessment_target_count": len(planned_targets),
            "assessments": [value.as_dict() for value in assessments],
            "case_truths": projected_truths,
            "case_relation_truths": projected_relation_truths,
            "participation_local_assessments": [
                value.as_dict() for value in participation_assessments
            ],
            "planned_participation_local_targets": [
                value.as_dict() for value in planned_participation_targets
            ],
            "factual_utilization_assessments": [
                value.as_dict() for value in utilization_assessments
            ],
            "utilized_participant_predicate_assessments": [
                value.as_dict() for value in participant_predicate_assessments
            ],
            "utilized_participant_outcomes": [
                {
                    "participant": {
                        "case_id": value.participant.case_id,
                        "participant_id": value.participant.participant_id,
                    },
                    "offense_ref": value.offense_ref,
                    "status": value.status,
                }
                for value in utilized_outcomes
            ],
            "indirect_principal_dependencies": [
                value.as_dict() for value in indirect_dependencies
            ],
            "participation_compile_status": participation_compile_status,
            "participation_compile_errors": participation_compile_errors,
            "top_level_instances": list(plan_row["top_level_instances"]),
            "assessment_instances": list(plan_row["assessment_instances"]),
            "candidate_doctrine_refs": list(plan_row["candidate_doctrine_refs"]),
            "question_assumption_count": len(question_assumptions.get(case_id, ())),
            "article263_assessments": article263_records,
            "shards": shard_records,
        })
        print(
            f"[{case_index}/{len(selected)}] {case_id}: targets={len(targets)} "
            f"general_shards={len(shards)} relation_targets={len(relation_assessments)} "
            f"participation_local_targets={len(participation_assessments)} "
            f"factual_utilization_targets={len(utilization_assessments)} "
            f"utilized_outcomes={len(utilized_outcomes)} "
            f"article263={int(bool(article263_pairs))}"
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(json.dumps(value, ensure_ascii=False) + "\n" for value in output),
        encoding="utf-8",
    )
    if args.smoke_target_limit is not None:
        run_status = "SMOKE_PARTIAL"
    elif args.diagnostic_continue_participation_errors:
        run_status = "DEGRADED_DIAGNOSTIC"
    else:
        run_status = "SUCCEEDED"
    manifest = {
        "step": "v2_occurrence_scoped_call2",
        "status": run_status,
        "logical_stage_count": len(selected),
        "physical_request_count": physical_requests,
        "assessment_target_count": sum(value["assessment_target_count"] for value in output),
        "neural_predicate_request_target_count": sum(
            value["neural_predicate_request_target_count"] for value in output
        ),
        "relation_assessment_target_count": sum(
            value["relation_assessment_target_count"] for value in output
        ),
        "participation_local_target_count": sum(
            value["participation_local_target_count"] for value in output
        ),
        "factual_utilization_target_count": sum(
            value["factual_utilization_target_count"] for value in output
        ),
        "utilized_participant_outcome_target_count": sum(
            value["utilized_participant_outcome_target_count"] for value in output
        ),
        "utilized_participant_predicate_target_count": sum(
            value["utilized_participant_predicate_target_count"] for value in output
        ),
        "participation_rejected_case_count": rejected_participation_case_count,
        "diagnostic_continue_participation_errors": (
            args.diagnostic_continue_participation_errors
        ),
        "usage": aggregate_usage,
        "max_targets_per_request": args.max_targets_per_request,
        "smoke_target_limit": args.smoke_target_limit,
        "call1_artifact_sha256": _sha256(args.call1_artifact),
        "evidence_mode": (
            "binding_scoped_planner_occurrences"
            if args.planner_occurrence_evidence
            else "legacy_gold_occurrences"
        ),
        "gold_occurrences_sha256": (
            None if args.planner_occurrence_evidence else _sha256(args.gold_occurrences)
        ),
        "gold_article263_pairs_sha256": (
            None if args.planner_occurrence_evidence else _sha256(args.gold_article263_pairs)
        ),
        "gold_factual_participants_sha256": (
            None
            if args.planner_occurrence_evidence
            else _sha256(args.gold_factual_participants)
        ),
        "question_assumptions_sha256": _sha256(args.question_assumptions),
        "plan_artifact_sha256": _sha256(args.plan_artifact),
        "inventory_sha256": _sha256(args.inventory),
        "case_ids": list(selected),
    }
    manifest_path = args.out.with_suffix(".manifest.json")
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.out}")
    print(f"wrote {manifest_path}")


if __name__ == "__main__":
    main()
