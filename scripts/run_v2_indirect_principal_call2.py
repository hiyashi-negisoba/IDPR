#!/usr/bin/env python3
"""Run only sparse factual-utilization and utilized-participant Call 2 probes."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.eval.input_formatter import assert_no_leaked_fields
from idpr.neural.vllm_client import VLLMClient
from idpr.prompts import load_prompt
from idpr.v2.gold_factual_identity import GoldFactualParticipant, GoldOccurrence
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.identity import FactualActionKey, FactualParticipantKey, OffenseInstanceKey
from idpr.v2.runtime.indirect_principal_grounding import (
    FactualUtilizationTarget,
    compile_indirect_principal_dependencies,
    factual_utilization_request_payload,
    factual_utilization_schema,
    validate_factual_utilization_output,
)
from idpr.v2.runtime.utilized_participant_outcome import (
    UtilizedParticipantOutcomeTarget,
    UtilizedParticipantPredicateTarget,
    produce_utilized_participant_outcomes,
    utilized_participant_request_payload,
    utilized_participant_schema,
    validate_utilized_participant_output,
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line]


def _instance(value: Mapping[str, Any]) -> OffenseInstanceKey:
    return OffenseInstanceKey(str(value["case_id"]), str(value["actor_id"]), str(value["offense_ref"]), str(value["occurrence_id"]))


def _occurrence(value: Mapping[str, Any]) -> GoldOccurrence:
    span = value["source_span"]
    return GoldOccurrence(str(value["occurrence_id"]), str(value["actor_id"]), str(value["source_text"]), int(span["start"]), int(span["end"]))


def _participant(value: Mapping[str, Any]) -> GoldFactualParticipant:
    span = value["source_span"]
    return GoldFactualParticipant(str(value["participant_id"]), str(value["participant_label"]), str(value["source_text"]), int(span["start"]), int(span["end"]))


def _target(value: Mapping[str, Any]) -> FactualUtilizationTarget:
    action = value["utilizer_action"]
    participant = value["utilized_participant"]
    return FactualUtilizationTarget(
        FactualActionKey(str(action["case_id"]), str(action["actor_id"]), str(action["occurrence_id"])),
        FactualParticipantKey(str(participant["case_id"]), str(participant["participant_id"])),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--api-key", default="local-idpr")
    parser.add_argument("--plan-artifact", type=Path, required=True)
    parser.add_argument("--definitions", type=Path, default=ROOT / "data/v2/definitions")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-tokens", type=int, default=4096)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--prompt-approved", action="store_true")
    args = parser.parse_args()
    if not args.prompt_approved:
        parser.error("--prompt-approved is required before a Call 2 model run")

    registry = load_definitions(args.definitions)
    client = VLLMClient(args.base_url, args.model, args.api_key)
    utilization_system = load_prompt("v2_call2_utilization")
    utilization_user = load_prompt("v2_call2_utilization_user")
    outcome_system = load_prompt("v2_call2_utilized_participant_outcome")
    outcome_user = load_prompt("v2_call2_utilized_participant_outcome_user")
    output = []
    usage_total = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    requests = 0
    for row in _rows(args.plan_artifact):
        case_id = str(row["sub_question_id"])
        targets = tuple(_target(value) for value in row.get("factual_utilization_targets", []))
        if not targets:
            continue
        occurrences = tuple(_occurrence(value) for value in row["occurrences"])
        participants = tuple(_participant(value) for value in row["factual_participants"])
        top_level = tuple(_instance(value) for value in row["top_level_instances"])
        utilization_assessments = []
        records = []
        for target in targets:
            payload = factual_utilization_request_payload(occurrences=occurrences, participants=participants, targets=(target,))
            assert_no_leaked_fields(payload)
            raw, metadata = client.complete_json(
                system_prompt=utilization_system,
                payload=payload,
                schema_name="v2_factual_utilization_relation_call2",
                schema=factual_utilization_schema(target),
                max_tokens=args.max_tokens,
                temperature=args.temperature,
                user_template=utilization_user,
            )
            assessment = validate_factual_utilization_output(raw, target=target)
            utilization_assessments.append(assessment)
            requests += 1
            for key in usage_total:
                usage_total[key] += int((metadata.get("usage") or {}).get(key, 0) or 0)
            records.append({"kind": "factual_utilization", "assessment": assessment.as_dict()})

        outcome_targets = []
        predicate_assessments = []
        participant_by_id = {value.participant_id: value for value in participants}
        for value in row["utilized_participant_outcome_targets"]:
            participant_raw = value["participant"]
            outcome = UtilizedParticipantOutcomeTarget(
                FactualParticipantKey(str(participant_raw["case_id"]), str(participant_raw["participant_id"])),
                str(value["offense_ref"]),
            )
            predicates = tuple(UtilizedParticipantPredicateTarget(outcome, str(ref)) for ref in value["predicate_refs"])
            participant = participant_by_id[outcome.participant.participant_id]
            payload = utilized_participant_request_payload(registry, participant=participant, outcome_target=outcome, predicate_targets=predicates)
            assert_no_leaked_fields(payload)
            raw, metadata = client.complete_json(
                system_prompt=outcome_system,
                payload=payload,
                schema_name="v2_utilized_participant_predicate_call2",
                schema=utilized_participant_schema(predicates),
                max_tokens=args.max_tokens,
                temperature=args.temperature,
                user_template=outcome_user,
            )
            assessed = validate_utilized_participant_output(raw, predicate_targets=predicates)
            outcome_targets.append(outcome)
            predicate_assessments.extend(assessed)
            requests += 1
            for key in usage_total:
                usage_total[key] += int((metadata.get("usage") or {}).get(key, 0) or 0)
            records.append({"kind": "utilized_participant_predicates", "target": outcome.as_dict(), "assessments": [item.as_dict() for item in assessed]})
        outcomes = produce_utilized_participant_outcomes(registry, outcome_targets, predicate_assessments)
        dependencies = compile_indirect_principal_dependencies(
            registry,
            top_level,
            participants,
            utilization_assessments,
            outcomes,
            expected_targets=targets,
        )
        output.append({
            "sub_question_id": case_id,
            "factual_utilization_assessments": [value.as_dict() for value in utilization_assessments],
            "utilized_participant_outcomes": [
                {
                    "participant": {
                        "case_id": value.participant.case_id,
                        "participant_id": value.participant.participant_id,
                    },
                    "offense_ref": value.offense_ref,
                    "status": value.status,
                }
                for value in outcomes
            ],
            "indirect_principal_dependencies": [value.as_dict() for value in dependencies],
            "records": records,
        })

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in output))
    manifest = {
        "step": "v2_indirect_principal_call2",
        "status": "SUCCEEDED",
        "case_count": len(output),
        "physical_request_count": requests,
        "dependency_count": sum(len(row["indirect_principal_dependencies"]) for row in output),
        "usage": usage_total,
        "plan_artifact_sha256": _sha256(args.plan_artifact),
    }
    args.out.with_suffix(".manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
