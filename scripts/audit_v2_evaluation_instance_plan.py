#!/usr/bin/env python3
"""Offline reproducibility audit for a Step 8 evaluation-instance plan."""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from run_v2_evaluation_instance_planner import (
    FROZEN_CLOSURE_SHA256,
    _case_ids,
    _read_json,
    _read_jsonl,
    _registry_sha256,
    _sha256,
    build_plan_rows,
)

from idpr.v2.registry import load_definitions

DEFAULT_DEFINITIONS = ROOT / "data/v2/definitions"
DEFAULT_INVENTORY = ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl"
DEFAULT_CASE_LIST = ROOT / "data/eval/kcl_substantive_case_ids.txt"


def _error(errors: list[str], detail: str) -> None:
    errors.append(detail)


def _verify_manifest(
    manifest: Mapping[str, Any], *, definitions: Path, inventory: Path, case_list: Path, errors: list[str]
) -> None:
    # The planner used to serialize a Call 1.5 binding directly as the legal
    # occurrence.  Action/realization plans deliberately do not: a binding is
    # provenance and the host assigns the occurrence id after it has selected a
    # focal action (and optional supporting actions).  Keep the historical
    # contract readable for old artifacts, but validate a newly produced plan
    # against the contract it actually declares rather than falsely rejecting it.
    action_realization_contract = manifest.get("occurrence_rule") == (
        "OffenseInstanceKey.occurrence_id is legal realization identity, never binding_id"
    )
    if action_realization_contract:
        identity_expectations = {
            "binding_rule": (
                "validated binding candidates reference atomic factual actions; host groups them "
                "into legal realizations and applies only registry-authored derived candidates"
            ),
            "factual_identity_rule": (
                "binding_id is provenance only; occurrence_id is a host-authored legal realization "
                "over focal/supporting factual actions"
            ),
            "occurrence_rule": (
                "OffenseInstanceKey.occurrence_id is legal realization identity, never binding_id"
            ),
        }
    else:
        identity_expectations = {
            "binding_rule": (
                "one validated direct binding plus registry-authored evidence-gated derived "
                "candidates requiring at least two same-episode same-actor bindings"
            ),
            "factual_identity_rule": (
                "Call 1.5 binding_id and source fragments only; offline gold occurrence and "
                "participant annotations are not production inputs"
            ),
            "occurrence_rule": (
                "binding_id is case-time candidate identity; source fragments remain auditable"
            ),
        }
    expected = {
        "step": "v2_evaluation_instance_planner",
        "status": "SUCCEEDED",
        "registry_sha256": _registry_sha256(definitions),
        "inventory_sha256": _sha256(inventory),
        "case_list_sha256": _sha256(case_list),
        **identity_expectations,
    }
    for field, value in expected.items():
        if manifest.get(field) != value:
            _error(errors, f"manifest {field!r} mismatch: expected {value!r}, got {manifest.get(field)!r}")
    if _sha256(ROOT / "src/idpr/v2/closure.py") != FROZEN_CLOSURE_SHA256:
        _error(errors, "current frozen closure source hash differs from approved hash")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--definitions", type=Path, default=DEFAULT_DEFINITIONS)
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--case-list", type=Path, default=DEFAULT_CASE_LIST)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    output = args.out or args.artifact.with_suffix(".audit.json")
    errors: list[str] = []
    manifest = _read_json(args.manifest)
    case_ids = _case_ids(args.case_list)
    _verify_manifest(manifest, definitions=args.definitions, inventory=args.inventory, case_list=args.case_list, errors=errors)
    if manifest.get("case_ids") != list(case_ids):
        _error(errors, "manifest case ids differ from frozen case list")

    call1_path = Path(str(manifest.get("call1_artifact", "")))
    call15_path = Path(str(manifest.get("call15_artifact", "")))
    if not call1_path.is_file():
        _error(errors, "Call 1 artifact is unavailable")
        expected_rows: list[dict[str, Any]] = []
    elif manifest.get("call1_artifact_sha256") != _sha256(call1_path):
        _error(errors, "Call 1 artifact hash mismatch")
        expected_rows = []
    elif not call15_path.is_file():
        _error(errors, "Call 1.5 artifact is unavailable")
        expected_rows = []
    elif manifest.get("call15_artifact_sha256") != _sha256(call15_path):
        _error(errors, "Call 1.5 artifact hash mismatch")
        expected_rows = []
    else:
        try:
            inventory_rows = _read_jsonl(args.inventory)
            expected_rows = build_plan_rows(
                registry=load_definitions(args.definitions),
                call1_rows=_read_jsonl(call1_path),
                call15_rows=_read_jsonl(call15_path),
                inventory_rows=inventory_rows,
                case_ids=case_ids,
            )
        except (ValueError, KeyError) as exc:
            _error(errors, f"could not recompute plan: {exc}")
            expected_rows = []

    actual_rows = _read_jsonl(args.artifact)
    actual_ids = [str(row.get("sub_question_id")) for row in actual_rows]
    if actual_ids != list(case_ids):
        _error(errors, "artifact case order does not equal frozen case list")
    if expected_rows and actual_rows != expected_rows:
        _error(errors, "artifact rows do not exactly reproduce frozen planner output")
    expected_counts = {
        key: sum(int(row[key]) for row in expected_rows)
        for key in (
            "top_level_instance_count",
            "predicate_scope_instance_count",
            "assessment_instance_count",
            "final_assessment_target_count",
            "neural_predicate_request_target_count",
            "relation_assessment_target_count",
            "participation_local_target_count",
            "factual_utilization_target_count",
            "utilized_participant_outcome_target_count",
            "utilized_participant_predicate_target_count",
            "derived_binding_candidate_count",
            "unbound_seed_count",
            "article263_pair_candidate_count",
            "context_only_binding_count",
        )
    }
    if expected_rows and manifest.get("aggregate_counts") != expected_counts:
        _error(errors, "manifest aggregate counts do not equal recomputed rows")

    collision_count = 0
    for row in actual_rows:
        keys = [
            (
                value.get("case_id"), value.get("actor_id"),
                value.get("offense_ref"), value.get("occurrence_id"),
            )
            for value in row.get("top_level_instances", [])
        ]
        collision_count += len(keys) - len(set(keys))
    if collision_count:
        _error(errors, f"top-level OffenseInstanceKey collisions: {collision_count}")

    report = {
        "step": "v2_evaluation_instance_planner_audit",
        "artifact": str(args.artifact),
        "artifact_sha256": _sha256(args.artifact),
        "manifest": str(args.manifest),
        "manifest_sha256": _sha256(args.manifest),
        "run_status": "SUCCEEDED" if not errors else "FAILED",
        "case_count": len(actual_rows),
        "recomputed_aggregate_counts": expected_counts,
        "top_level_instance_key_collision_count": collision_count,
        "errors": errors,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {output}")
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
