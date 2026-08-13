#!/usr/bin/env python3
"""Augment the canonical binding plan with evidence-scoped participation probes."""

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

from idpr.v2.factual_interaction import (
    FactualInteractionContractError,
    parse_factual_interactions,
)
from idpr.v2.issue_binding import (
    IssueBindingContractError,
    parse_issue_binding_result,
    question_actor_ids,
)
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.factual_participation import (
    FactualParticipationError,
    materialize_factual_participation_candidates,
)

DEFAULT_INVENTORY = ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl"
DEFAULT_CASE_LIST = ROOT / "data/eval/kcl_substantive_case_ids.txt"
DEFAULT_DEFINITIONS = ROOT / "data/v2/definitions"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _jsonl(path: Path) -> list[dict[str, Any]]:
    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]
    if not all(isinstance(row, dict) for row in rows):
        raise ValueError(f"{path}: every row must be an object")
    return rows


def _index(path: Path, label: str) -> dict[str, dict[str, Any]]:
    rows = _jsonl(path)
    output = {str(row.get("sub_question_id")): row for row in rows}
    if len(output) != len(rows):
        raise ValueError(f"{label}: duplicate sub_question_id")
    return output


def _case_ids(path: Path) -> tuple[str, ...]:
    values = tuple(
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    )
    if not values or len(values) != len(set(values)):
        raise ValueError(f"{path}: case ids must be nonempty and unique")
    return values


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan-artifact", type=Path, required=True)
    parser.add_argument("--call15-artifact", type=Path, required=True)
    parser.add_argument("--interaction-artifact", type=Path, required=True)
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--case-list", type=Path, default=DEFAULT_CASE_LIST)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--definitions", type=Path, default=DEFAULT_DEFINITIONS)
    args = parser.parse_args()

    case_ids = _case_ids(args.case_list)
    plans = _index(args.plan_artifact, "planner")
    bindings = _index(args.call15_artifact, "Call 1.5")
    interactions = _index(args.interaction_artifact, "Call 1.5-P")
    inventory = _index(args.inventory, "inventory")
    registry = load_definitions(args.definitions)
    for label, values in (
        ("planner", plans),
        ("Call 1.5", bindings),
        ("Call 1.5-P", interactions),
    ):
        missing = sorted(set(case_ids) - set(values))
        extra = sorted(set(values) - set(case_ids))
        if missing or extra:
            raise ValueError(
                f"{label}: case-list mismatch missing={missing}, extra={extra}"
            )
    missing_inventory = sorted(set(case_ids) - set(inventory))
    if missing_inventory:
        raise ValueError(f"inventory: missing selected cases {missing_inventory}")

    output: list[dict[str, Any]] = []
    for case_id in case_ids:
        source = inventory[case_id]
        binding_row = bindings[case_id]
        interaction_row = interactions[case_id]
        if interaction_row.get("error") not in {None, ""}:
            raise ValueError(f"{case_id}: unsuccessful Call 1.5-P row")
        seeds = binding_row.get("seeds")
        if not isinstance(seeds, list) or not seeds:
            raise ValueError(f"{case_id}: missing Call 1.5 seed lineage")
        responsibility = question_actor_ids(str(source["question_prompt"]))
        try:
            binding_result = parse_issue_binding_result(
                {
                    "factual_episodes": binding_row.get("factual_episodes"),
                    "seed_results": binding_row.get("seed_results"),
                },
                seeds=seeds,
                case_text=str(source["question_text"]),
                candidate_actor_ids=responsibility,
            )
            factual_interactions = parse_factual_interactions(
                interaction_row.get("interactions", []),
                case_text=str(source["question_text"]),
                episodes=binding_result.factual_episodes,
            )
            compiled = materialize_factual_participation_candidates(
                case_id=case_id,
                plan_row=plans[case_id],
                binding_result=binding_result,
                interactions=factual_interactions,
                responsibility_actor_ids=responsibility,
                registry=registry,
            )
        except (
            IssueBindingContractError,
            FactualInteractionContractError,
            FactualParticipationError,
        ) as exc:
            raise ValueError(f"{case_id}: {exc}") from exc

        row = copy.deepcopy(plans[case_id])
        row["occurrences"].extend(
            value.as_dict() for value in compiled.evidence_occurrences
        )
        row["participation_local_targets"] = [
            value.as_dict() for value in compiled.targets
        ]
        row["participation_local_target_count"] = len(compiled.targets)
        row["factual_interaction_count"] = len(factual_interactions)
        row["factual_interaction_candidate_count"] = len(
            {
                value.interaction_id
                for value in factual_interactions
                if value.interaction_id not in compiled.skipped_interaction_ids
            }
        )
        row["skipped_factual_interaction_ids"] = list(
            compiled.skipped_interaction_ids
        )
        row["participation_evidence_occurrence_count"] = len(
            compiled.evidence_occurrences
        )
        occurrence_ids = {
            value["occurrence_id"] for value in row["occurrences"]
        }
        if len(occurrence_ids) != len(row["occurrences"]):
            raise ValueError(f"{case_id}: duplicate occurrence after augmentation")
        for target in row["participation_local_targets"]:
            if any(
                value["occurrence_id"] not in occurrence_ids
                for value in target["member_instances"]
            ):
                raise ValueError(f"{case_id}: dangling participation evidence")
        output.append(row)
        print(
            f"{case_id}: interactions={len(factual_interactions)} "
            f"targets={len(compiled.targets)} "
            f"new_evidence={len(compiled.evidence_occurrences)}",
            flush=True,
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in output),
        encoding="utf-8",
    )
    manifest = {
        "step": "v2_factual_participation_plan",
        "status": "SUCCEEDED",
        "case_count": len(output),
        "factual_interaction_count": sum(
            row["factual_interaction_count"] for row in output
        ),
        "factual_interaction_candidate_count": sum(
            row["factual_interaction_candidate_count"] for row in output
        ),
        "participation_local_target_count": sum(
            row["participation_local_target_count"] for row in output
        ),
        "participation_evidence_occurrence_count": sum(
            row["participation_evidence_occurrence_count"] for row in output
        ),
        "plan_artifact": str(args.plan_artifact),
        "plan_artifact_sha256": _sha256(args.plan_artifact),
        "call15_artifact": str(args.call15_artifact),
        "call15_artifact_sha256": _sha256(args.call15_artifact),
        "interaction_artifact": str(args.interaction_artifact),
        "interaction_artifact_sha256": _sha256(args.interaction_artifact),
        "inventory_sha256": _sha256(args.inventory),
        "case_list_sha256": _sha256(args.case_list),
    }
    args.out.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
