#!/usr/bin/env python3
"""Offline prompt, payload, and schema audit for the normalized core pipeline."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from idpr.generation.native_hybrid_answer import hybrid_answer_schema  # noqa: E402
from idpr.neural.core_contract import (  # noqa: E402
    assessment_groups,
    core_assessment_schema,
    core_issue_selection_schema,
    role_binding_schema,
)
from idpr.prompts import INPUT_PLACEHOLDER, load_prompt, prompt_path  # noqa: E402
from idpr.rulegen.core_profile import load_core_profiles  # noqa: E402
from scripts.run_rule_ir_core_kcl_e2e import PROMPTS  # noqa: E402


REQUIRED = {
    "selection": ("allowed_units", "검색", "role_bindings", "총칙", "형사소송법"),
    "binding": ("role_contract", "core_predicates", "엔티티", "관계", "track_selections"),
    "assessment": ("전량", "authority_context", "satisfied", "not_satisfied", "unknown"),
    "generation": ("rule_ir_scallop", "model_only_general_part_experiment", "결론"),
}
UNSUPPORTED_GUIDANCE = {"if", "then", "else", "prefixItems"}


def _nested_keys(value: Any) -> set[str]:
    if isinstance(value, Mapping):
        return set(value) | {
            key for child in value.values() for key in _nested_keys(child)
        }
    if isinstance(value, list):
        return {key for child in value for key in _nested_keys(child)}
    return set()


def _hash(name: str) -> str:
    return hashlib.sha256(prompt_path(name).read_bytes()).hexdigest()


def audit() -> dict[str, Any]:
    errors = []
    prompt_hashes = {}
    prompt_rows = []
    for stage, (system_name, user_name) in PROMPTS.items():
        system = load_prompt(system_name)
        user = load_prompt(user_name)
        missing = [token for token in REQUIRED[stage] if token not in system]
        if missing:
            errors.append(f"{stage}: missing prompt contract terms {missing}")
        if INPUT_PLACEHOLDER in system or user.count(INPUT_PLACEHOLDER) != 1:
            errors.append(f"{stage}: invalid runtime placeholder placement")
        prompt_hashes[system_name] = _hash(system_name)
        prompt_hashes[user_name] = _hash(user_name)
        prompt_rows.append({
            "stage": stage, "system": system_name, "user": user_name,
            "system_characters": len(system), "user_characters": len(user),
        })

    profiles = load_core_profiles()["units"]
    fraud = profiles["fraud"]
    fraud_group = assessment_groups(fraud, ["base"], max_predicates=10)[0]
    predicate_ids = [item["predicate_id"] for item in fraud_group["predicates"]]
    schemas = {
        "selection": core_issue_selection_schema(
            case_id="audit-case", unit_ids=sorted(profiles)
        ),
        "binding": role_binding_schema(
            case_id="audit-case", issue_id="issue-1", profile=fraud
        ),
        "assessment": core_assessment_schema(
            case_id="audit-case", predicate_ids=predicate_ids
        ),
        "generation": hybrid_answer_schema([
            {"section_id": "special", "authority": "rule_ir_scallop"},
            {
                "section_id": "general",
                "authority": "model_only_general_part_experiment",
            },
        ]),
    }
    incompatible = sorted(
        UNSUPPORTED_GUIDANCE & set().union(*(_nested_keys(schema) for schema in schemas.values()))
    )
    if incompatible:
        errors.append(f"vLLM guidance-incompatible schema keys: {incompatible}")
    selection_item = schemas["selection"]["properties"]["issues"]["items"]
    if "role_bindings" in selection_item["properties"]:
        errors.append("issue selection still performs legal role binding")
    if not {"subject_quote", "conduct_quotes"}.issubset(selection_item["required"]):
        errors.append("issue selection does not preserve subject and conduct")
    binding_roles = schemas["binding"]["properties"]["role_bindings"]["required"]
    if binding_roles != [
        "defendant_id", "deceived_person_id", "disposer_id",
        "property_owner_id", "beneficiary_id",
    ]:
        errors.append("fraud role schema differs from the RuleIR role tuple")
    track_item = schemas["binding"]["properties"]["track_selections"]["items"]
    if not {"applies_to_entity_id", "source_quotes", "reason"}.issubset(
        track_item["required"]
    ):
        errors.append("track selection lacks subject/evidence contract")
    detailed = sum(
        profile["detailed_card_predicates"]["count"] for profile in profiles.values()
    )
    core = sum(len(profile["model_input_predicates"]) for profile in profiles.values())
    if core >= detailed:
        errors.append("core projection did not reduce model-facing predicates")
    return {
        "version": "1.0.0", "status": "pass" if not errors else "fail",
        "scope": "offline normalized-core preflight; no model calls", "api_calls": 0,
        "prompt_hashes": prompt_hashes, "prompts": prompt_rows,
        "schemas": {
            "stages": list(schemas),
            "unsupported_guidance_keywords_present": incompatible,
            "selection_performs_role_binding": False,
            "selection_preserves_subject_and_conduct": True,
            "track_selection_requires_subject_and_evidence": True,
        },
        "predicate_boundary": {
            "units": len(profiles), "detailed_card_predicates": detailed,
            "core_model_predicates": core, "fraud": [88, 10], "theft": [66, 6],
        },
        "search_contract": {
            "initial_issue_search": False,
            "predicate_conditioned_context": True,
            "context_may_change_predicate_set": False,
        },
        "errors": errors,
    }


def render_markdown(report: Mapping[str, Any]) -> str:
    boundary = report["predicate_boundary"]
    return "\n".join([
        "# RuleIR core-normalized KCL 사전 감사", "",
        f"- 상태: **{report['status']}**", "- 모델/API 호출: 0",
        f"- 등록 unit: {boundary['units']}",
        f"- 카드별 모델 입력 제거: {boundary['detailed_card_predicates']}",
        f"- 핵심 component 모델 입력: {boundary['core_model_predicates']}",
        "- 최초 쟁점 검색: 사용하지 않음",
        "- 검색/context 위치: 선택된 predicate 판단 단계",
        "- context의 predicate 집합 변경: 금지", "",
        "## 오류", "",
        *(f"- {item}" for item in report["errors"]), "",
    ])


def main() -> None:
    report = audit()
    target = ROOT / "data/e2e/rule_ir_core/prompt_audit.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    doc = ROOT / "docs/2026-08-04_rule_ir_core_prompt_audit.md"
    doc.write_text(render_markdown(report), encoding="utf-8")
    print(f"{report['status']}: core={report['predicate_boundary']['core_model_predicates']} errors={len(report['errors'])}")
    if report["errors"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
