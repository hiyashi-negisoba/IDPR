"""Experimental KCL writer for symbolic special-part and model-only general-part units."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from jsonschema import Draft202012Validator


class NativeHybridAnswerError(ValueError):
    pass


def hybrid_answer_schema(sections: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    symbolic_ids = [
        str(section["section_id"])
        for section in sections
        if section["authority"] == "rule_ir_scallop"
    ]
    general_ids = [
        str(section["section_id"])
        for section in sections
        if section["authority"] == "model_only_general_part_experiment"
    ]

    def section_array(ids: list[str], *, general: bool) -> dict[str, Any]:
        properties: dict[str, Any] = {
            "section_id": {"enum": ids} if ids else {"type": "string"},
            "rule": {"type": "string", "minLength": 1, "maxLength": 8000},
            "application": {"type": "string", "minLength": 1, "maxLength": 8000},
        }
        required = ["section_id", "rule", "application"]
        if general:
            properties["provisional_conclusion"] = {
                "type": "string", "minLength": 1, "maxLength": 2000
            }
            required.append("provisional_conclusion")
        return {
            "type": "array",
            "minItems": len(ids),
            "maxItems": len(ids),
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": required,
                "properties": properties,
            },
        }

    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["version", "symbolic_sections", "general_part_sections"],
        "properties": {
            "version": {"const": "1.0.0"},
            "symbolic_sections": section_array(symbolic_ids, general=False),
            "general_part_sections": section_array(general_ids, general=True),
        },
    }


def finalize_hybrid_answer(
    *, request: Mapping[str, Any], model_payload: Mapping[str, Any]
) -> dict[str, Any]:
    sections = request.get("sections", [])
    errors = [
        f"{'.'.join(str(part) for part in error.absolute_path) or '$'}: {error.message}"
        for error in Draft202012Validator(hybrid_answer_schema(sections)).iter_errors(
            model_payload
        )
    ]
    if errors:
        raise NativeHybridAnswerError("; ".join(errors))
    planned_symbolic = [
        str(section["section_id"])
        for section in sections
        if section["authority"] == "rule_ir_scallop"
    ]
    planned_general = [
        str(section["section_id"])
        for section in sections
        if section["authority"] == "model_only_general_part_experiment"
    ]
    for field, expected in (
        ("symbolic_sections", planned_symbolic),
        ("general_part_sections", planned_general),
    ):
        actual = [str(item["section_id"]) for item in model_payload[field]]
        if actual != expected:
            errors.append(f"{field}: expected ordered section ids {expected}, got {actual}")
    if errors:
        raise NativeHybridAnswerError("; ".join(errors))
    labels = {
        "established": "성립",
        "not_established": "불성립",
        "undetermined": "현재 사실만으로 성립 여부 미확정",
        "conflict": "predicate 평가 충돌로 결론 유보",
        "no_derived_outcome": "RuleIR에서 결론 미도출",
    }
    finalized = []
    prose_by_id = {
        str(prose["section_id"]): prose
        for field in ("symbolic_sections", "general_part_sections")
        for prose in model_payload[field]
    }
    for planned in sections:
        prose = prose_by_id[str(planned["section_id"])]
        if planned["authority"] == "rule_ir_scallop":
            status = str(planned["symbolic_directive"])
            finalized.append({
                **dict(prose),
                "heading": planned["heading"],
                "authority": "rule_ir_scallop",
                "symbolic_conclusion": status,
                "conclusion": labels[status],
                "established_relations": list(planned["established_relations"]),
            })
        else:
            finalized.append({
                **dict(prose),
                "heading": planned["heading"],
                "authority": "model_only_general_part_experiment",
                "conclusion": prose["provisional_conclusion"],
            })
    return {
        "version": "1.0.0",
        "case_id": request["case_id"],
        "sections": finalized,
        "conclusion_policy": {
            "supported_special_part": "host_injected_from_scallop",
            "unsupported_general_part": "model_only_experimental_not_symbolic",
        },
    }


def render_hybrid_markdown(answer: Mapping[str, Any]) -> str:
    lines = ["# 형법 사례 답안", ""]
    for index, section in enumerate(answer["sections"], 1):
        lines.extend([
            f"## {index}. {section['heading']}",
            "",
        ])
        if section["authority"] == "model_only_general_part_experiment":
            lines.extend([
                "> 실험상 비기호 총칙 분석 — 현재 RuleIR/Scallop 결론이 아닙니다.",
                "",
            ])
        lines.extend([
            "### 법리",
            "",
            str(section["rule"]),
            "",
            "### 사안의 적용",
            "",
            str(section["application"]),
            "",
            "### 결론",
            "",
            str(section["conclusion"]),
            "",
        ])
    return "\n".join(lines).rstrip() + "\n"
