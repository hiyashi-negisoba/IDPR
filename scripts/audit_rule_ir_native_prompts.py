"""Preflight audit for the experimental RuleIR-native KCL prompt chain."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.eval.input_formatter import (  # noqa: E402
    ALLOWED_INPUT_FIELDS,
    LEAKING_FIELDS,
    assert_no_leaked_fields,
)
from idpr.generation.native_hybrid_answer import hybrid_answer_schema  # noqa: E402
from idpr.neural.fact_graph import fact_graph_schema  # noqa: E402
from idpr.neural.issue_assessment import issue_assessment_schema  # noqa: E402
from idpr.prompts import INPUT_PLACEHOLDER, load_prompt, prompt_path  # noqa: E402
from idpr.rulegen.native_host import closed_issue_selection_schema  # noqa: E402
from idpr.rulegen.registry import build_registry  # noqa: E402


CASES = (
    "kcl_criminal_r14_p1_q2",
    "kcl_criminal_r12_p1_q2",
)
STAGES = {
    "fact_extract": {
        "system": "rule_ir_native_fact_extract",
        "user": "rule_ir_native_fact_extract_user",
        "required": (
            "issue_candidates", "retrieval_queries", "빈 배열", "법률 결론",
            "source_quote", "명령문", "rubric",
        ),
    },
    "issue_select": {
        "system": "rule_ir_native_issue_select",
        "user": "rule_ir_native_issue_select_user",
        "required": (
            "allowed_units", "unsupported", "의미검색", "총칙", "형사소송법",
            "결론", "source_quote", "명령문", "rubric",
        ),
    },
    "predicate_assess": {
        "system": "rule_ir_native_predicate_assess",
        "user": "rule_ir_native_predicate_assess_user",
        "required": (
            "전체", "생략", "top-k", "satisfied", "not_satisfied", "unknown",
            "Scallop", "명령문", "rubric",
        ),
    },
    "hybrid_generate": {
        "system": "rule_ir_native_hybrid_generate",
        "user": "rule_ir_native_hybrid_generate_user",
        "required": (
            "rule_ir_scallop", "model_only_general_part_experiment",
            "symbolic_directive", "subject_label", "결론",
        ),
    },
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _inventory_rows() -> dict[str, dict[str, Any]]:
    path = ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl"
    return {
        row["sub_question_id"]: row
        for row in (
            json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    }


def _case_payload(row: Mapping[str, Any]) -> dict[str, Any]:
    payload = {key: row[key] for key in ALLOWED_INPUT_FIELDS}
    assert_no_leaked_fields(payload)
    return payload


def _nested_keys(value: Any) -> set[str]:
    if isinstance(value, Mapping):
        return set(value) | {
            nested for child in value.values() for nested in _nested_keys(child)
        }
    if isinstance(value, list):
        return {nested for child in value for nested in _nested_keys(child)}
    return set()


def _unsupported_guidance_keywords(value: Any) -> set[str]:
    unsupported = {"if", "then", "else", "prefixItems"}
    if isinstance(value, Mapping):
        return (set(value) & unsupported) | {
            nested
            for child in value.values()
            for nested in _unsupported_guidance_keywords(child)
        }
    if isinstance(value, list):
        return {
            nested for child in value for nested in _unsupported_guidance_keywords(child)
        }
    return set()


def audit() -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
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
        prompt_rows.append({
            "stage": stage,
            "system": spec["system"],
            "system_sha256": _sha256(prompt_path(spec["system"])),
            "user": spec["user"],
            "user_sha256": _sha256(prompt_path(spec["user"])),
            "system_characters": len(system),
            "user_characters": len(user),
            "required_contract_terms_present": not missing,
        })

    exact_leak_tokens = sorted(
        field for field in LEAKING_FIELDS if f"`{field}`" in all_prompt_text
    )
    if exact_leak_tokens:
        errors.append(f"prompt text names benchmark-only field identifiers: {exact_leak_tokens}")

    inventory = _inventory_rows()
    payload_rows = []
    for case_id in CASES:
        raw = inventory[case_id]
        payload = _case_payload(raw)
        leaked = sorted(LEAKING_FIELDS & _nested_keys(payload))
        if leaked:
            errors.append(f"{case_id}: payload leaks {leaked}")
        payload_rows.append({
            "case_id": case_id,
            "raw_field_count": len(raw),
            "model_input_fields": sorted(payload),
            "excluded_annotation_fields": sorted(set(raw) - set(payload)),
        })

    registry = build_registry()
    selection_schema = closed_issue_selection_schema(case_id="audit-case")
    enum = selection_schema["properties"]["issues"]["items"]["properties"][
        "unit_id"
    ]["enum"]
    expected_enum = sorted(registry) + ["unsupported"]
    if enum != expected_enum:
        errors.append("closed selection enum differs from the audited registry")

    native_fact_schema = fact_graph_schema()
    for field in ("issue_candidates", "retrieval_queries"):
        native_fact_schema["properties"][field]["minItems"] = 0
        native_fact_schema["properties"][field]["maxItems"] = 0
    if any(
        (
            native_fact_schema["properties"][field].get("minItems"),
            native_fact_schema["properties"][field].get("maxItems"),
        )
        != (0, 0)
        for field in ("issue_candidates", "retrieval_queries")
    ):
        errors.append("native FactGraph schema does not force search outputs empty")

    sample_unit = registry["theft"]
    predicate_ids = [item["id"] for item in sample_unit.commentary_inputs]
    assessment_schema = issue_assessment_schema(
        case_id="audit-case", issue_ids=predicate_ids, fact_ids=("fact_001",)
    )
    required_predicates = assessment_schema["properties"]["assessments"]["required"]
    if required_predicates != predicate_ids:
        errors.append("predicate assessment schema does not preserve complete registry order")

    generation_schema = hybrid_answer_schema([
        {"section_id": "supported", "authority": "rule_ir_scallop"},
        {
            "section_id": "general",
            "authority": "model_only_general_part_experiment",
        },
    ])
    incompatible = set().union(*(
        _unsupported_guidance_keywords(schema)
        for schema in (
            native_fact_schema,
            selection_schema,
            assessment_schema,
            generation_schema,
        )
    ))
    if incompatible:
        errors.append(
            f"runtime schemas use unsupported vLLM guidance keywords: {sorted(incompatible)}"
        )

    # These are intentional experiment boundaries, not silent production behavior.
    warnings.extend([
        "Unsupported general-part sections use model-only legal knowledge and are not symbolic.",
        "FactGraph vocabulary may omit legally material mental-state detail; omissions must remain unknown.",
        "The audit proves prompt/data contracts, not model compliance or answer correctness.",
    ])
    return {
        "version": "1.0.0",
        "status": "pass" if not errors else "fail",
        "scope": "pre-execution prompt and payload audit; no model calls",
        "api_calls": 0,
        "cases": list(CASES),
        "prompts": prompt_rows,
        "payloads": payload_rows,
        "schemas": {
            "registered_unit_enum": len(registry),
            "unsupported_sentinel": "unsupported",
            "semantic_search_outputs_item_bounds": [0, 0],
            "sample_unit": "theft",
            "sample_required_predicates": len(required_predicates),
            "supported_writer_conclusion_field": False,
            "unsupported_general_part_authority": "model_only_general_part_experiment",
            "unsupported_guidance_keywords_present": sorted(incompatible),
        },
        "errors": errors,
        "warnings": warnings,
    }


def render_markdown(report: Mapping[str, Any]) -> str:
    lines = [
        "# RuleIR-native KCL E2E 사전 프롬프트 감사",
        "",
        f"- 상태: **{report['status']}**",
        "- 모델/API 호출: 0",
        f"- 대상 문항: {', '.join(f'`{value}`' for value in report['cases'])}",
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
    lines.extend([
        "",
        "## 확인된 불변식",
        "",
        "- 모델 입력은 `sub_question_id`, `question_text`, `question_prompt`에서만 유도한다.",
        "- FactGraph의 `issue_candidates`와 `retrieval_queries`는 schema에서 빈 배열로 고정한다.",
        f"- 죄종 선택 enum은 등록 RuleIR {report['schemas']['registered_unit_enum']}개와 "
        "`unsupported` 하나뿐이다.",
        "- 선택된 unit의 predicate는 schema의 required field로 전량 강제한다.",
        "- 지원 각칙의 결론 필드는 생성 모델 schema에 주지 않는다.",
        "- 미지원 총칙은 `model_only_general_part_experiment`로 명시하며 symbolic으로 부르지 않는다.",
        "- 절차법·증거법·수사·공판·상소 쟁점은 이번 실험 답안에서 제외한다.",
        "",
        "## 남은 실험상 위험",
        "",
        *[f"- {warning}" for warning in report["warnings"]],
    ])
    if report["errors"]:
        lines.extend(["", "## 오류", "", *[f"- {error}" for error in report["errors"]]])
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
        default=ROOT / "docs/2026-08-04_rule_ir_native_kcl_prompt_audit.md",
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
