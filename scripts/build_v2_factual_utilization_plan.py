#!/usr/bin/env python3
"""Augment a binding plan with sparse production indirect-principal probes."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.v2.factual_interaction import (
    FactualInteractionContractError,
    parse_factual_interactions,
)
from idpr.v2.issue_binding import IssueBindingContractError, parse_issue_binding_result
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.factual_utilization import (
    FactualUtilizationPlanError,
    materialize_factual_utilization_candidates,
)


PARTICIPATION_PLAN_STEP = "v2_factual_participation_plan"


def _json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected an object")
    return value


def _rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line]


def _index(path: Path) -> dict[str, dict[str, Any]]:
    values = _rows(path)
    result = {str(value["sub_question_id"]): value for value in values}
    if len(result) != len(values):
        raise ValueError(f"{path}: duplicate sub_question_id")
    return result


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _validate_compiled_endpoints(
    case_id: str,
    row: Mapping[str, Any],
    *,
    participant_ids: set[str],
    target_values: list[dict[str, Any]],
    outcome_values: list[dict[str, Any]],
) -> None:
    """Make the logical relation endpoints and physical action carriers total."""

    occurrence_actor_by_id: dict[str, str] = {}
    raw_occurrences = row.get("occurrences")
    if not isinstance(raw_occurrences, list):
        raise ValueError(f"{case_id}: plan occurrences are malformed")
    for occurrence in raw_occurrences:
        if not isinstance(occurrence, Mapping):
            raise ValueError(f"{case_id}: plan occurrence is malformed")
        occurrence_id = occurrence.get("occurrence_id")
        actor_id = occurrence.get("actor_id")
        if not isinstance(occurrence_id, str) or not isinstance(actor_id, str):
            raise ValueError(f"{case_id}: plan occurrence lacks identity")
        if occurrence_id in occurrence_actor_by_id:
            raise ValueError(f"{case_id}: duplicate plan occurrence identity")
        occurrence_actor_by_id[occurrence_id] = actor_id

    target_participants: set[str] = set()
    for target in target_values:
        action = target.get("utilizer_action")
        participant = target.get("utilized_participant")
        evidence_id = target.get("utilizer_action_evidence_id")
        if not isinstance(action, Mapping) or not isinstance(participant, Mapping):
            raise ValueError(f"{case_id}: utilization target is malformed")
        actor_id = action.get("actor_id")
        participant_id = participant.get("participant_id")
        if not isinstance(evidence_id, str) or not evidence_id:
            raise ValueError(
                f"{case_id}: utilization target lacks explicit action evidence id"
            )
        if occurrence_actor_by_id.get(evidence_id) != actor_id:
            raise ValueError(
                f"{case_id}: utilization carrier does not match its utilizer actor"
            )
        if not isinstance(participant_id, str) or participant_id not in participant_ids:
            raise ValueError(
                f"{case_id}: utilization target has no source-local participant evidence"
            )
        target_participants.add(participant_id)
    outcome_participants = {
        str(value["participant"]["participant_id"])
        for value in outcome_values
        if isinstance(value.get("participant"), Mapping)
    }
    if target_participants != participant_ids or outcome_participants != participant_ids:
        raise ValueError(
            f"{case_id}: utilization participant endpoint universe is not exact"
        )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan-artifact", type=Path, required=True)
    parser.add_argument("--call15-artifact", type=Path, required=True)
    parser.add_argument("--interaction-artifact", type=Path, required=True)
    parser.add_argument("--inventory", type=Path, default=ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl")
    parser.add_argument("--definitions", type=Path, default=ROOT / "data/v2/definitions")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    plans = _index(args.plan_artifact)
    bindings = _index(args.call15_artifact)
    interactions = _index(args.interaction_artifact)
    inventory = _index(args.inventory)
    if not (set(plans) == set(bindings) == set(interactions)):
        raise ValueError("planner/Call1.5/Call1.5-P case universes differ")
    missing_inventory = sorted(set(plans) - set(inventory))
    if missing_inventory:
        raise ValueError(f"inventory is missing planned cases: {missing_inventory}")
    parent_manifest_path = args.plan_artifact.with_suffix(".manifest.json")
    if not parent_manifest_path.is_file():
        raise ValueError(
            "canonical factual utilization requires a manifest-backed participation plan"
        )
    parent_manifest = _json(parent_manifest_path)
    if parent_manifest.get("step") != PARTICIPATION_PLAN_STEP:
        raise ValueError(
            "canonical factual utilization requires a participation-augmented parent plan"
        )
    registry = load_definitions(args.definitions)
    output = []
    for case_id, source_plan in plans.items():
        binding_row = bindings[case_id]
        interaction_row = interactions[case_id]
        if interaction_row.get("error") not in {None, ""}:
            raise ValueError(f"{case_id}: unsuccessful Call 1.5-P row")
        responsibility = interaction_row.get("responsibility_actor_ids")
        if (
            not isinstance(responsibility, list)
            or not responsibility
            or not all(isinstance(value, str) and value for value in responsibility)
            or len(responsibility) != len(set(responsibility))
        ):
            raise ValueError(f"{case_id}: invalid Call 1.5-P responsibility actors")
        try:
            binding_result = parse_issue_binding_result(
                {
                    "factual_episodes": binding_row["factual_episodes"],
                    "seed_results": binding_row["seed_results"],
                },
                seeds=binding_row["seeds"],
                case_text=str(inventory[case_id]["question_text"]),
                candidate_actor_ids=tuple(responsibility),
            )
            interaction_values = parse_factual_interactions(
                interaction_row["interactions"],
                case_text=str(inventory[case_id]["question_text"]),
                episodes=binding_result.factual_episodes,
            )
            compiled = materialize_factual_utilization_candidates(
                case_id=case_id,
                plan_row=source_plan,
                binding_result=binding_result,
                interactions=interaction_values,
                registry=registry,
            )
        except (
            FactualInteractionContractError,
            FactualUtilizationPlanError,
            IssueBindingContractError,
            KeyError,
        ) as exc:
            raise ValueError(f"{case_id}: {exc}") from exc
        row = copy.deepcopy(source_plan)
        factual_participants = [value.as_dict() for value in compiled.participants]
        factual_utilization_targets = [value.as_dict() for value in compiled.targets]
        utilized_outcomes = [
            {
                **value.as_dict(),
                "predicate_refs": [
                    predicate.predicate_ref
                    for predicate in compiled.predicate_targets
                    if predicate.outcome_target == value
                ],
            }
            for value in compiled.outcome_targets
        ]
        _validate_compiled_endpoints(
            case_id,
            row,
            participant_ids={value["participant_id"] for value in factual_participants},
            target_values=factual_utilization_targets,
            outcome_values=utilized_outcomes,
        )
        row["factual_participants"] = factual_participants
        row["factual_utilization_targets"] = factual_utilization_targets
        row["factual_utilization_target_count"] = len(compiled.targets)
        row["utilized_participant_outcome_targets"] = utilized_outcomes
        row["utilized_participant_outcome_target_count"] = len(compiled.outcome_targets)
        row["utilized_participant_predicate_target_count"] = len(compiled.predicate_targets)
        row["factual_utilization_interaction_ids"] = list(compiled.used_interaction_ids)
        output.append(row)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in output))
    manifest = {
        "step": "v2_factual_utilization_plan",
        "status": "SUCCEEDED",
        "case_count": len(output),
        "factual_participant_count": sum(len(row["factual_participants"]) for row in output),
        "factual_utilization_target_count": sum(row["factual_utilization_target_count"] for row in output),
        "utilized_participant_outcome_target_count": sum(row["utilized_participant_outcome_target_count"] for row in output),
        "utilized_participant_predicate_target_count": sum(row["utilized_participant_predicate_target_count"] for row in output),
        "plan_artifact": str(args.plan_artifact),
        "plan_artifact_sha256": _sha256(args.plan_artifact),
        "parent_plan_step": parent_manifest["step"],
        "parent_plan_manifest": str(parent_manifest_path),
        "parent_plan_manifest_sha256": _sha256(parent_manifest_path),
        "call15_artifact_sha256": _sha256(args.call15_artifact),
        "interaction_artifact_sha256": _sha256(args.interaction_artifact),
    }
    args.out.with_suffix(".manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
