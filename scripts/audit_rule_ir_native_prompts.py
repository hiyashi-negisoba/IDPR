"""Offline audit for the lean three-stage RuleIR-native prompt chain."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.prompts import INPUT_PLACEHOLDER, load_prompt, prompt_path  # noqa: E402
from idpr.rulegen.native_host import (  # noqa: E402
    closed_issue_selection_schema,
    predicate_assessment_schema,
)
from idpr.rulegen.registry import build_registry  # noqa: E402


STAGES = {
    "issue_select": {
        "system": "rule_ir_native_issue_select",
        "user": "rule_ir_native_issue_select_user",
        "required": (
            "allowed_units",
            "unsupported",
            "의미검색",
            "depends_on_issue_ids",
            "source_quote",
            "결론",
            "rubric",
        ),
    },
    "predicate_assess": {
        "system": "rule_ir_native_predicate_assess",
        "user": "rule_ir_native_predicate_assess_user",
        "required": (
            "case_text",
            "전체",
            "생략",
            "top-k",
            "satisfied",
            "not_satisfied",
            "unknown",
            "source_quotes",
            "Scallop",
            "rubric",
        ),
    },
    "section_write": {
        "system": "rule_ir_native_write",
        "user": "rule_ir_native_write_user",
        "required": (
            "하나의 쟁점",
            "### 법리",
            "### 사안의 적용",
            "결론",
            "JSON",
            "rubric",
        ),
    },
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit() -> dict[str, Any]:
    errors: list[str] = []
    prompt_rows = []
    all_prompt_text = ""
    for stage, spec in STAGES.items():
        system = load_prompt(spec["system"])
        user = load_prompt(spec["user"])
        all_prompt_text += system + "\n" + user
        missing = [token for token in spec["required"] if token not in system]
        if missing:
            errors.append(f"{stage}: required contract language absent: {missing}")
        if INPUT_PLACEHOLDER in system:
            errors.append(f"{stage}: system prompt contains runtime placeholder")
        if user.count(INPUT_PLACEHOLDER) != 1:
            errors.append(f"{stage}: user prompt must contain one runtime placeholder")
        prompt_rows.append(
            {
                "stage": stage,
                "system": spec["system"],
                "system_sha256": _sha256(prompt_path(spec["system"])),
                "user": spec["user"],
                "user_sha256": _sha256(prompt_path(spec["user"])),
                "required_contract_terms_present": not missing,
            }
        )

    forbidden_contracts = {
        "FactGraph": "generic FactGraph must not exist in the active prompt chain",
        "model_only_general_part_experiment": (
            "unsupported law must not receive a model-only pseudo-symbolic conclusion"
        ),
        "symbolic_sections": "whole-answer JSON writer must not be active",
        "general_part_sections": "whole-answer JSON writer must not be active",
    }
    for token, detail in forbidden_contracts.items():
        if token in all_prompt_text:
            errors.append(f"forbidden prompt contract {token!r}: {detail}")

    registry = build_registry()
    selection_schema = closed_issue_selection_schema(case_id="audit-case")
    enum = selection_schema["properties"]["issues"]["items"]["properties"][
        "unit_id"
    ]["enum"]
    if enum != sorted(registry) + ["unsupported"]:
        errors.append("closed selection enum differs from the audited registry")

    sample_entry = next(iter(registry.values()))
    assessment_schema = predicate_assessment_schema(
        case_id="audit-case", issue_id="audit-issue", entry=sample_entry
    )
    required_predicates = assessment_schema["properties"]["assessments"]["required"]
    expected_predicates = [item["id"] for item in sample_entry.commentary_inputs]
    if required_predicates != expected_predicates:
        errors.append("assessment schema does not preserve complete predicate order")
    required_roles = assessment_schema["properties"]["role_values"]["required"]
    expected_roles = [
        item["name"] for item in sample_entry.role_predicate["arguments"]
    ]
    if required_roles != expected_roles:
        errors.append("assessment schema does not preserve the complete role contract")

    return {
        "version": "2.0.0",
        "status": "pass" if not errors else "fail",
        "scope": "offline three-stage prompt/schema audit; no model calls",
        "api_calls": 0,
        "prompts": prompt_rows,
        "schemas": {
            "registered_unit_enum": len(registry),
            "unsupported_sentinel": "unsupported",
            "sample_unit": sample_entry.unit_id,
            "sample_required_predicates": len(required_predicates),
            "sample_required_roles": len(required_roles),
            "writer_format": "one_plain_markdown_section",
            "writer_conclusion_field": False,
        },
        "errors": errors,
        "warnings": [
            "The audit proves contracts, not model compliance or legal correctness."
        ],
    }


def render_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        "# Lean RuleIR-native KCL 프롬프트 감사",
        "",
        f"- 상태: **{report['status']}**",
        "- 모델/API 호출: 0",
        "- 신경망 단계: closed issue selection → full predicate assessment → section prose",
        "",
        "## 프롬프트 고정값",
        "",
        "| stage | system SHA-256 | user SHA-256 | 계약 문구 |",
        "|---|---|---|---|",
    ]
    for item in report["prompts"]:
        lines.append(
            f"| `{item['stage']}` | `{item['system_sha256']}` | "
            f"`{item['user_sha256']}` | "
            f"{'pass' if item['required_contract_terms_present'] else 'fail'} |"
        )
    lines.extend(
        [
            "",
            "## 불변식",
            "",
            "- 초기 검색과 generic FactGraph가 없다.",
            f"- 선택 enum은 등록 RuleIR {report['schemas']['registered_unit_enum']}개와 "
            "`unsupported`뿐이다.",
            "- 선택 unit의 모든 predicate와 역할이 schema required field다.",
            "- 미지원 쟁점은 `predicate_ir_missing`이며 모델 결론을 받지 않는다.",
            "- writer는 section별 Markdown만 쓰고 결론은 호스트가 붙인다.",
        ]
    )
    if report["errors"]:
        lines.extend(["", "## 오류", "", *[f"- {item}" for item in report["errors"]]])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json-out",
        type=Path,
        default=ROOT / "data/e2e/rule_ir_native/prompt_audit.json",
    )
    parser.add_argument(
        "--markdown-out",
        type=Path,
        default=ROOT / "docs/audits/rule_ir_native_prompts.md",
    )
    args = parser.parse_args()
    report = audit()
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.markdown_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    args.markdown_out.write_text(render_markdown(report), encoding="utf-8")
    print(f"{report['status']}: {len(report['prompts'])} stages, {len(report['errors'])} errors")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
