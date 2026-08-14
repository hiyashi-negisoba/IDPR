#!/usr/bin/env python3
"""Whole-corpus and whole-plan invariant audit for the v2 quality-repair lineage."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.v2.checks import run_type_checks
from idpr.v2.registry import load_definitions

SCOPES = {
    "exact_actor_action",
    "same_actor_episode",
    "offense_realization",
    "typed_relation",
}


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _instance_key(value: dict[str, Any]) -> tuple[str, str, str, str]:
    return tuple(
        str(value[name])
        for name in ("case_id", "actor_id", "offense_ref", "occurrence_id")
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--issue-bindings", type=Path, required=True)
    parser.add_argument("--participation", type=Path, required=True)
    parser.add_argument("--call2", type=Path)
    parser.add_argument(
        "--inventory", type=Path,
        default=ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl",
    )
    parser.add_argument(
        "--definitions", type=Path, default=ROOT / "data/v2/definitions"
    )
    parser.add_argument(
        "--dispute-registry", type=Path,
        default=ROOT / "data/v2/dispute_registry.json",
    )
    parser.add_argument(
        "--explicit-miss-gold", type=Path,
        default=ROOT / "data/eval/v2_call15_explicit_miss_gold.jsonl",
    )
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    registry = load_definitions(args.definitions)
    inventory = _jsonl(args.inventory)
    plans = _jsonl(args.plan)
    issues = {row["sub_question_id"]: row for row in _jsonl(args.issue_bindings)}
    participation = {
        row["sub_question_id"]: row for row in _jsonl(args.participation)
    }
    call2 = (
        {row["sub_question_id"]: row for row in _jsonl(args.call2)}
        if args.call2 else {}
    )
    errors: list[str] = []
    warnings: list[str] = []

    type_findings = run_type_checks(registry)
    errors.extend(
        f"definition:{value.axis}:{value.code}:{value.definition_id}:{value.field_path}"
        for value in type_findings
    )

    inventory_ids = {str(row["sub_question_id"]) for row in inventory}
    substantive_ids = {
        str(row["sub_question_id"])
        for row in inventory if row.get("legal_area") == "substantive"
    }
    plan_ids = {str(row["sub_question_id"]) for row in plans}
    if plan_ids != substantive_ids:
        errors.append(
            "plan case universe differs from all substantive inventory rows: "
            f"missing={sorted(substantive_ids-plan_ids)}, extra={sorted(plan_ids-substantive_ids)}"
        )
    unsupported_ids = inventory_ids - substantive_ids

    predicate_scope_counts: Counter[str] = Counter()
    predicates_with_exclusions = 0
    for kind in ("ground_fact", "legal_element"):
        for entry in registry.by_kind.get(kind, ()):
            scope = str(entry.payload.get("evidence_scope", "exact_actor_action"))
            predicate_scope_counts[f"{kind}/{scope}"] += 1
            if scope not in SCOPES:
                errors.append(f"{entry.id}: invalid evidence_scope {scope!r}")
            exclusions = entry.payload.get("semantic_exclusions", ())
            if exclusions:
                predicates_with_exclusions += 1
                if not all(isinstance(value, str) and value.strip() for value in exclusions):
                    errors.append(f"{entry.id}: malformed semantic_exclusions")

    plan_counts = Counter()
    scheduled_scope_counts: Counter[str] = Counter()
    plan_by_case = {str(row["sub_question_id"]): row for row in plans}
    for row in plans:
        case_id = str(row["sub_question_id"])
        if case_id not in issues or case_id not in participation:
            errors.append(f"{case_id}: missing issue or participation artifact")
            continue
        occurrence_ids = {
            str(value["occurrence_id"]) for value in row.get("occurrences", ())
        }
        direct_bindings = {
            str(binding["binding_id"]): binding
            for seed in issues[case_id].get("seed_results", ())
            for binding in seed.get("bindings", ())
        }
        for candidate in row.get("derived_binding_candidates", ()):
            for source_id in candidate.get("source_binding_ids", ()):
                if str(source_id) not in direct_bindings:
                    errors.append(
                        f"{case_id}/{candidate['binding_id']}: dangling source binding {source_id}"
                    )
        seen_targets = set()
        for target in row.get("assessment_targets", ()):
            raw_instance = target["instance_key"]
            key = (*_instance_key(raw_instance), str(target["predicate_ref"]))
            if key in seen_targets:
                errors.append(f"{case_id}: duplicate assessment target {key}")
            seen_targets.add(key)
            if key[3] not in occurrence_ids:
                errors.append(f"{case_id}: assessment target has unknown occurrence {key}")
            entry = registry.get(key[4])
            if entry is None or entry.kind not in {"ground_fact", "legal_element"}:
                errors.append(f"{case_id}: invalid predicate target {key[4]}")
            else:
                scope = str(entry.payload.get("evidence_scope", "exact_actor_action"))
                scheduled_scope_counts[f"{entry.kind}/{scope}"] += 1
        for target in row.get("participation_local_targets", ()):
            group = target["group_key"]
            members = target["member_instances"]
            if len(members) < 2:
                errors.append(f"{case_id}: participation target has fewer than two members")
            for member in members:
                if str(member["case_id"]) != case_id:
                    errors.append(f"{case_id}: cross-case participation member")
                if str(member["offense_ref"]) != str(group["offense_ref"]):
                    errors.append(f"{case_id}: cross-offense member without authored route")
                if str(member["occurrence_id"]) not in occurrence_ids:
                    errors.append(f"{case_id}: participation member lacks evidence occurrence")
        part_row = participation[case_id]
        if part_row.get("participation_compile_status") != "SUCCEEDED":
            errors.append(f"{case_id}: participation compile did not succeed")
        if part_row.get("participation_compile_errors"):
            errors.append(f"{case_id}: participation compile errors are nonempty")
        if int(part_row.get("participation_local_target_count", -1)) != len(
            row.get("participation_local_targets", ())
        ):
            errors.append(f"{case_id}: participation target count mismatch")
        plan_counts.update({
            "cases": 1,
            "assessment_targets": len(row.get("assessment_targets", ())),
            "participation_targets": len(row.get("participation_local_targets", ())),
            "unbound_seeds": len(row.get("unbound_seeds", ())),
            "derived_bindings": len(row.get("derived_binding_candidates", ())),
        })

    call2_truths = Counter()
    call2_unknown_by_scope = Counter()
    for case_id, row in call2.items():
        if case_id not in plan_ids:
            errors.append(f"{case_id}: Call 2 row outside plan universe")
        for value in row.get("assessments", ()):
            truth = str(value["truth"])
            call2_truths[truth] += 1
            entry = registry.get(str(value["predicate_ref"]))
            if truth == "UNKNOWN" and entry is not None:
                scope = str(entry.payload.get("evidence_scope", "exact_actor_action"))
                call2_unknown_by_scope[f"{entry.kind}/{scope}"] += 1

    disputes = json.loads(args.dispute_registry.read_text())
    if int(disputes.get("dispute_count", -1)) != len(disputes.get("disputes", ())):
        errors.append("dispute registry count mismatch")
    dispute_ids = []
    dispute_routes = []
    for dispute in disputes.get("disputes", ()):
        dispute_ids.append(dispute.get("dispute_id"))
        dispute_routes.append(
            (dispute.get("variant_group"), dispute.get("trigger_card_id"))
        )
        predicate_ref = dispute.get("predicate_ref")
        if predicate_ref and registry.get(str(predicate_ref)) is None:
            warnings.append(f"dispute predicate outside definition registry: {predicate_ref}")
    if len(dispute_ids) != len(set(dispute_ids)):
        errors.append("duplicate dispute registry id")
    if len(dispute_routes) != len(set(dispute_routes)):
        errors.append("duplicate dispute registry route")

    explicit_seed_recall = []
    for gold in _jsonl(args.explicit_miss_gold):
        case_id = str(gold["sub_question_id"])
        offense_ref = str(gold["offense_ref"])
        plan = plan_by_case.get(case_id)
        if plan is None:
            status = "OUTSIDE_PLAN_UNIVERSE"
        else:
            top_level = {
                str(value["offense_ref"])
                for value in plan.get("top_level_instances", ())
            }
            assessment = {
                str(value["offense_ref"])
                for value in plan.get("assessment_instances", ())
            }
            derived = {
                str(value.get("offense_ref"))
                for value in plan.get("derived_binding_candidates", ())
            }
            if offense_ref in top_level:
                status = "TOP_LEVEL_BOUND"
            elif offense_ref in assessment:
                status = "ASSESSMENT_REACHABLE"
            elif offense_ref in derived:
                status = "DERIVED_BOUND"
            else:
                status = "MISSING_FROM_PLAN"
        explicit_seed_recall.append({
            "sub_question_id": case_id,
            "offense_ref": offense_ref,
            "status": status,
        })

    report = {
        "step": "v2_structural_invariant_audit",
        "status": "SUCCEEDED" if not errors else "FAILED",
        "inputs": {
            "plan": str(args.plan), "plan_sha256": _sha(args.plan),
            "issue_bindings": str(args.issue_bindings),
            "participation": str(args.participation),
            "call2": str(args.call2) if args.call2 else None,
        },
        "whole_inventory_boundary": {
            "all_rows": len(inventory),
            "substantive_rows_in_plan": len(substantive_ids),
            "unsupported_procedure_or_mixed_rows": len(unsupported_ids),
            "unsupported_ids": sorted(unsupported_ids),
        },
        "definition_layer": {
            "definition_count": len(registry.by_id),
            "type_finding_count": len(type_findings),
            "predicate_scope_counts": dict(predicate_scope_counts),
            "predicates_with_semantic_exclusions": predicates_with_exclusions,
            "dispute_routes": len(disputes.get("disputes", ())),
        },
        "plan": dict(plan_counts),
        "offline_explicit_seed_recall": {
            "warning": "evaluation-only gold; never a production selector",
            "status_counts": dict(Counter(
                value["status"] for value in explicit_seed_recall
            )),
            "records": explicit_seed_recall,
        },
        "scheduled_predicate_scope_counts": dict(scheduled_scope_counts),
        "call2": {
            "truth_counts": dict(call2_truths),
            "unknown_by_authored_scope": dict(call2_unknown_by_scope),
        },
        "errors": errors,
        "warnings": warnings,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "status": report["status"],
        "whole_inventory_boundary": report["whole_inventory_boundary"],
        "definition_layer": report["definition_layer"],
        "plan": report["plan"],
        "call2": report["call2"],
        "error_count": len(errors),
        "warning_count": len(warnings),
    }, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
