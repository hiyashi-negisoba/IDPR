#!/usr/bin/env python3
"""Offline audit for the lean core RuleIR pipeline."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from idpr.neural.core_contract import (  # noqa: E402
    core_issue_selection_schema,
    core_unit_analysis_schema,
)
from idpr.prompts import INPUT_PLACEHOLDER, load_prompt, prompt_path  # noqa: E402
from idpr.rulegen.core_profile import load_core_profiles  # noqa: E402
from scripts.run_rule_ir_core_kcl_e2e import (  # noqa: E402
    JSON_PROMPTS,
    WRITE_PROMPT,
)


REQUIRED = {
    "selection": ("allowed_units", "unsupported", "대상자", "행위"),
    "analysis": ("role", "track", "predicate", "Scallop"),
    "writing": ("호스트가 고정한 결론", "법리", "포섭", "Markdown"),
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
    errors: list[str] = []
    prompt_hashes: dict[str, str] = {}
    prompt_rows = []
    prompt_specs = {
        **JSON_PROMPTS,
        "writing": WRITE_PROMPT,
    }
    for stage, (system_name, user_name) in prompt_specs.items():
        system = load_prompt(system_name)
        user = load_prompt(user_name)
        missing = [token for token in REQUIRED[stage] if token not in system]
        if missing:
            errors.append(f"{stage}: missing prompt terms {missing}")
        if INPUT_PLACEHOLDER in system or user.count(INPUT_PLACEHOLDER) != 1:
            errors.append(f"{stage}: invalid runtime placeholder placement")
        if len(system) > 1000 or len(user) > 400:
            errors.append(f"{stage}: prompt exceeds lean size bound")
        prompt_hashes[system_name] = _hash(system_name)
        prompt_hashes[user_name] = _hash(user_name)
        prompt_rows.append({
            "stage": stage,
            "system": system_name,
            "user": user_name,
            "system_characters": len(system),
            "user_characters": len(user),
            "output_mode": "plain_text" if stage == "writing" else "json_schema",
        })

    profiles = load_core_profiles()["units"]
    fraud = profiles["fraud"]
    schemas = {
        "selection": core_issue_selection_schema(
            case_id="audit-case", unit_ids=sorted(profiles)
        ),
        "analysis": core_unit_analysis_schema(
            case_id="audit-case", issue_id="issue-01", profile=fraud
        ),
    }
    incompatible = sorted(
        UNSUPPORTED_GUIDANCE
        & set().union(*(_nested_keys(schema) for schema in schemas.values()))
    )
    if incompatible:
        errors.append(f"vLLM guidance-incompatible schema keys: {incompatible}")
    analysis_required = set(schemas["analysis"]["required"])
    if analysis_required != {
        "case_id", "issue_id", "selected_tracks", "role_values", "assessments"
    }:
        errors.append("analysis contract contains unexpected layers")
    core = sum(len(profile["model_input_predicates"]) for profile in profiles.values())
    detailed = sum(
        profile["detailed_card_predicates"]["count"] for profile in profiles.values()
    )
    return {
        "version": "2.0.0",
        "status": "pass" if not errors else "fail",
        "scope": "offline lean-core preflight; no model calls",
        "api_calls": 0,
        "prompt_hashes": prompt_hashes,
        "prompts": prompt_rows,
        "pipeline": {
            "model_stages": ["closed_issue_selection", "unit_analysis", "section_prose"],
            "fact_inventory_stage": False,
            "separate_role_binding_stage": False,
            "whole_answer_json_stage": False,
            "writer_output": "plain_text_per_section",
            "initial_semantic_search": False,
            "runtime": "scallop_scli_core_projection",
        },
        "predicate_boundary": {
            "units": len(profiles),
            "detailed_card_predicates": detailed,
            "core_model_predicates": core,
        },
        "schemas": {
            "json_stages": list(schemas),
            "unsupported_guidance_keywords_present": incompatible,
        },
        "errors": errors,
    }


def render_markdown(report: Mapping[str, Any]) -> str:
    pipeline = report["pipeline"]
    boundary = report["predicate_boundary"]
    return "\n".join([
        "# RuleIR lean-core 사전 감사", "",
        f"- 상태: **{report['status']}**",
        "- 모델/API 호출: 0",
        f"- 모델 단계: {' → '.join(pipeline['model_stages'])}",
        f"- 전체 답안 JSON 생성: {pipeline['whole_answer_json_stage']}",
        f"- section writer: {pipeline['writer_output']}",
        f"- 등록 unit: {boundary['units']}",
        f"- core predicate: {boundary['core_model_predicates']}", "",
        "## 오류", "",
        *(f"- {item}" for item in report["errors"]), "",
    ])


def main() -> None:
    report = audit()
    target = ROOT / "data/e2e/rule_ir_core/prompt_audit.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    doc = ROOT / "docs/2026-08-04_rule_ir_core_prompt_audit.md"
    doc.write_text(render_markdown(report), encoding="utf-8")
    print(
        f"{report['status']}: stages=3 core={report['predicate_boundary']['core_model_predicates']} "
        f"errors={len(report['errors'])}"
    )
    if report["errors"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
