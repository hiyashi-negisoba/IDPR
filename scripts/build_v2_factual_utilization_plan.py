#!/usr/bin/env python3
"""Augment a binding plan with sparse production indirect-principal probes."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.v2.factual_interaction import parse_factual_interactions
from idpr.v2.issue_binding import parse_issue_binding_result
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.factual_utilization import (
    materialize_factual_utilization_candidates,
)


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
    registry = load_definitions(args.definitions)
    output = []
    for case_id, source_plan in plans.items():
        binding_row = bindings[case_id]
        binding_result = parse_issue_binding_result(
            {
                "factual_episodes": binding_row["factual_episodes"],
                "seed_results": binding_row["seed_results"],
            },
            seeds=binding_row["seeds"],
            case_text=str(inventory[case_id]["question_text"]),
            candidate_actor_ids=tuple(interactions[case_id]["responsibility_actor_ids"]),
        )
        interaction_values = parse_factual_interactions(
            interactions[case_id]["interactions"],
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
        row = copy.deepcopy(source_plan)
        row["factual_participants"] = [value.as_dict() for value in compiled.participants]
        row["factual_utilization_targets"] = [value.as_dict() for value in compiled.targets]
        row["factual_utilization_target_count"] = len(compiled.targets)
        row["utilized_participant_outcome_targets"] = [
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
        "call15_artifact_sha256": _sha256(args.call15_artifact),
        "interaction_artifact_sha256": _sha256(args.interaction_artifact),
    }
    args.out.with_suffix(".manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(manifest, ensure_ascii=False))


if __name__ == "__main__":
    main()
