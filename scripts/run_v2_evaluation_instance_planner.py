#!/usr/bin/env python3
"""Materialize one Call 2 evaluation context per validated Call 1.5 binding."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.eval.input_formatter import target_fact_source_spans
from idpr.v2.closure import compile_closure
from idpr.v2.issue_binding import (
    IssueBindingContractError,
    parse_issue_binding_result,
    question_actor_ids,
)
from idpr.v2.registry import KIND_TO_EXAMPLE_FILE, load_definitions
from idpr.v2.routing import router_catalog, router_catalog_fingerprint
from idpr.v2.runtime.evaluation_instance_planner import (
    EvaluationInstancePlannerError,
    plan_binding_scoped_evaluation_instances,
)

FROZEN_STEP7_COMMIT = "62759879019dbcb894f7e274977b07f41957fd45"
# 2026-08-15 재봉인. `blocked_when` leaf를 dependency traversal의 정식 입력으로 넣으면서
# closure.py가 바뀌었다. 그 변경으로 실제로 늘어난 것은 defeat doctrine 5개의 blocker 전용
# predicate뿐이고(자초한 심신장애 등), completion 쪽 frontier fact 집합과 planner가 읽는
# `candidate_offense_refs`는 변경 전과 동일함을 대조로 확인했다.
FROZEN_CLOSURE_SHA256 = "e19186b8129be2dc94cbee0438c1a1f5a6f975bc3658495e959f96cf7635a256"
DEFAULT_DEFINITIONS = ROOT / "data/v2/definitions"
DEFAULT_INVENTORY = ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl"
DEFAULT_CASE_LIST = ROOT / "data/eval/kcl_substantive_case_ids.txt"
SOURCE_FILES = (
    "src/idpr/v2/closure.py",
    "src/idpr/v2/compile.py",
    "src/idpr/v2/gold_factual_identity.py",
    "src/idpr/v2/issue_binding.py",
    "src/idpr/v2/runtime/evaluation_instance_planner.py",
    "src/idpr/v2/runtime/grounding.py",
    "src/idpr/v2/runtime/participation_grounding.py",
    "src/idpr/v2/runtime/indirect_principal_grounding.py",
    "src/idpr/v2/runtime/utilized_participant_outcome.py",
    "src/idpr/v2/runtime/completion.py",
    "src/idpr/v2/runtime/scallop_backend.py",
    "scripts/run_v2_evaluation_instance_planner.py",
)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _registry_sha256(definitions_dir: Path) -> str:
    digest = hashlib.sha256()
    for filename in sorted(set(KIND_TO_EXAMPLE_FILE.values())):
        digest.update(filename.encode("utf-8"))
        digest.update(b"\0")
        digest.update((definitions_dir / filename).read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _source_fingerprint() -> str:
    digest = hashlib.sha256()
    for relative_path in SOURCE_FILES:
        digest.update(relative_path.encode("utf-8"))
        digest.update(b"\0")
        digest.update((ROOT / relative_path).read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _git_commit() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{path}: expected a JSON object")
    return value


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
    if not all(isinstance(row, dict) for row in rows):
        raise ValueError(f"{path}: every JSONL row must be an object")
    return rows


def _case_ids(path: Path) -> tuple[str, ...]:
    values = tuple(line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
    if not values or len(set(values)) != len(values):
        raise ValueError(f"{path}: expected nonempty unique case ids")
    return values


def _index_exact(
    rows: Iterable[Mapping[str, Any]], case_ids: tuple[str, ...], label: str
) -> dict[str, Mapping[str, Any]]:
    values = tuple(rows)
    indexed = {str(row.get("sub_question_id")): row for row in values}
    if len(indexed) != len(values):
        raise ValueError(f"{label}: duplicate sub_question_id")
    missing = [case_id for case_id in case_ids if case_id not in indexed]
    extra = sorted(set(indexed) - set(case_ids))
    if missing or extra:
        raise ValueError(f"{label}: case-list mismatch: missing={missing}, extra={extra}")
    return indexed


def _verify_lineage(
    call1_manifest: Mapping[str, Any], definitions_dir: Path, inventory: Path, case_list: Path
) -> str:
    registry = load_definitions(definitions_dir)
    catalog = router_catalog(registry)
    current_catalog_sha = router_catalog_fingerprint(catalog)
    expected = {
        "inventory_sha256": _sha256(inventory),
        "case_list_sha256": _sha256(case_list),
    }
    errors = [
        f"Call 1 manifest {field} mismatch: expected {value}, got {call1_manifest.get(field)!r}"
        for field, value in expected.items()
        if call1_manifest.get(field) != value
    ]
    closure_sha = _sha256(ROOT / "src/idpr/v2/closure.py")
    if closure_sha != FROZEN_CLOSURE_SHA256:
        errors.append(
            f"frozen closure hash mismatch: expected {FROZEN_CLOSURE_SHA256}, got {closure_sha}"
        )
    recorded_catalog_sha = call1_manifest.get("router_catalog_sha256")
    if recorded_catalog_sha is not None:
        if recorded_catalog_sha != current_catalog_sha:
            errors.append(
                "Call 1 manifest router_catalog_sha256 mismatch: "
                f"expected {current_catalog_sha}, got {recorded_catalog_sha!r}"
            )
        lineage_mode = "router_catalog_sha256"
    else:
        if call1_manifest.get("catalog_definition_ids") != [
            entry.definition_id for entry in catalog
        ]:
            errors.append("legacy Call 1 catalog_definition_ids differ from current router catalog")
        lineage_mode = "legacy_exact_catalog_definition_ids"
    if errors:
        raise ValueError("; ".join(errors))
    return lineage_mode


def _inventory_index(inventory: Iterable[Mapping[str, Any]], case_ids: tuple[str, ...]) -> dict[str, Mapping[str, Any]]:
    values = tuple(inventory)
    indexed = {str(row.get("sub_question_id")): row for row in values}
    if len(indexed) != len(values):
        raise ValueError("inventory: duplicate sub_question_id")
    missing = [case_id for case_id in case_ids if case_id not in indexed]
    if missing:
        raise ValueError(f"inventory: frozen case ids are missing: {missing}")
    return {case_id: indexed[case_id] for case_id in case_ids}


def build_plan_rows(
    *,
    registry: Any,
    call1_rows: Iterable[Mapping[str, Any]],
    call15_rows: Iterable[Mapping[str, Any]],
    inventory_rows: Iterable[Mapping[str, Any]],
    case_ids: tuple[str, ...],
) -> list[dict[str, Any]]:
    """Build the exact ordered artifact rows; exposed for focused tests/audit."""
    call1_by_id = _index_exact(call1_rows, case_ids, "Call 1 artifact")
    call15_by_id = _index_exact(call15_rows, case_ids, "Call 1.5 artifact")
    inventory_by_id = _inventory_index(inventory_rows, case_ids)
    output: list[dict[str, Any]] = []
    for case_id in case_ids:
        call1_row = call1_by_id[case_id]
        if call1_row.get("error"):
            raise ValueError(f"{case_id}: Call 1 row is unsuccessful")
        call15_row = call15_by_id[case_id]
        if call15_row.get("error"):
            raise ValueError(f"{case_id}: Call 1.5 row is unsuccessful")
        seeds = call1_row.get("normalized_seeds")
        if not isinstance(seeds, list) or not seeds:
            raise ValueError(f"{case_id}: missing normalized Call 1 seeds")
        source = inventory_by_id[case_id]
        if not isinstance(source.get("question_text"), str):
            raise TypeError(f"{case_id}: inventory has no string question_text")
        try:
            binding_result = parse_issue_binding_result(
                {
                    "factual_episodes": call15_row.get("factual_episodes"),
                    "seed_results": call15_row.get("seed_results"),
                },
                seeds=seeds,
                case_text=str(source["question_text"]),
                candidate_actor_ids=question_actor_ids(str(source["question_prompt"])),
            )
            plan = plan_binding_scoped_evaluation_instances(
                registry,
                case_id=case_id,
                bindings=binding_result.bindings,
                factual_episodes=binding_result.factual_episodes,
                allowed_candidate_offense_refs=compile_closure(
                    registry, seeds
                ).candidate_offense_refs,
                unbound_seed_refs=(
                    result.offense_ref
                    for result in binding_result.seed_results
                    if not result.bindings
                ),
                case_text=str(source["question_text"]),
                liability_source_spans=target_fact_source_spans(
                    str(source["question_text"]), str(source["question_prompt"])
                ),
            )
        except (EvaluationInstancePlannerError, IssueBindingContractError) as exc:
            raise ValueError(str(exc)) from exc
        output.append(plan.as_dict())
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--call1-artifact", type=Path, required=True)
    parser.add_argument("--call1-manifest", type=Path, required=True)
    parser.add_argument("--call15-artifact", type=Path, required=True)
    parser.add_argument("--definitions", type=Path, default=DEFAULT_DEFINITIONS)
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--case-list", type=Path, default=DEFAULT_CASE_LIST)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--manifest-out", type=Path)
    args = parser.parse_args()
    manifest_out = args.manifest_out or args.out.with_suffix(".manifest.json")

    call1_manifest = _read_json(args.call1_manifest)
    call1_catalog_lineage = _verify_lineage(
        call1_manifest, args.definitions, args.inventory, args.case_list
    )
    case_ids = _case_ids(args.case_list)
    registry = load_definitions(args.definitions)
    inventory_rows = _read_jsonl(args.inventory)
    rows = build_plan_rows(
        registry=registry,
        call1_rows=_read_jsonl(args.call1_artifact),
        call15_rows=_read_jsonl(args.call15_artifact),
        inventory_rows=inventory_rows,
        case_ids=case_ids,
    )
    counts = {
        key: sum(int(row[key]) for row in rows)
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
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )
    manifest = {
        "step": "v2_evaluation_instance_planner",
        "status": "SUCCEEDED",
        "git_commit": _git_commit(),
        "planner_source_fingerprint": _source_fingerprint(),
        "binding_rule": (
            "validated binding candidates reference atomic factual actions; host groups them "
            "into legal realizations and applies only registry-authored derived candidates"
        ),
        "factual_identity_rule": (
            "binding_id is provenance only; occurrence_id is a host-authored legal realization "
            "over focal/supporting factual actions"
        ),
        "evaluation_actor_rule": "actor_id bound by Call 1.5",
        "candidate_order_rule": (
            "direct legal realizations first, then registry-authored derived realizations "
            "linked by source realization ids"
        ),
        "derived_candidate_semantics": (
            "same factual episode and authored supporting bindings open candidate scope only; "
            "Call 2 decides predicates and relations"
        ),
        "zero_binding_rule": "emit typed UNBOUND_SEED diagnostics; never crash or synthesize a binding",
        "predicate_scope_rule": "scallop_backend._completion_scope_instances parity",
        "occurrence_rule": "OffenseInstanceKey.occurrence_id is legal realization identity, never binding_id",
        "case_ids": list(case_ids),
        "aggregate_counts": counts,
        "call1_artifact": str(args.call1_artifact),
        "call1_artifact_sha256": _sha256(args.call1_artifact),
        "call1_manifest": str(args.call1_manifest),
        "call1_manifest_sha256": _sha256(args.call1_manifest),
        "call15_artifact": str(args.call15_artifact),
        "call15_artifact_sha256": _sha256(args.call15_artifact),
        "registry_sha256": _registry_sha256(args.definitions),
        "call1_catalog_lineage": call1_catalog_lineage,
        "router_catalog_sha256": router_catalog_fingerprint(router_catalog(registry)),
        "inventory_sha256": _sha256(args.inventory),
        "case_list_sha256": _sha256(args.case_list),
    }
    manifest_out.parent.mkdir(parents=True, exist_ok=True)
    manifest_out.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {args.out}")
    print(f"wrote {manifest_out}")


if __name__ == "__main__":
    main()
