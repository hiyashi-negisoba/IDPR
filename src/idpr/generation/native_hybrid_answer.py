"""Experimental KCL writer for symbolic special-part and model-only general-part units."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from jsonschema import Draft202012Validator


class NativeHybridAnswerError(ValueError):
    pass


def hybrid_answer_schema(sections: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    section_ids = [str(section["section_id"]) for section in sections]
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["version", "sections"],
        "properties": {
            "version": {"const": "1.0.0"},
            "sections": {
                "type": "array",
                "minItems": len(section_ids),
                "maxItems": len(section_ids),
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["section_id", "rule", "application"],
                    "properties": {
                        "section_id": {"enum": section_ids},
                        "rule": {"type": "string", "minLength": 1, "maxLength": 8000},
                        "application": {
                            "type": "string", "minLength": 1, "maxLength": 8000
                        },
                        "provisional_conclusion": {
                            "type": "string", "minLength": 1, "maxLength": 2000
                        },
                    },
                },
            },
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
    for index, (planned, prose) in enumerate(
        zip(sections, model_payload["sections"], strict=True)
    ):
        if prose["section_id"] != planned["section_id"]:
            errors.append(
                f"sections.{index}.section_id: expected {planned['section_id']!r}"
            )
        is_general = planned["authority"] == "model_only_general_part_experiment"
        has_provisional = "provisional_conclusion" in prose
        if is_general and not has_provisional:
            errors.append(
                f"sections.{index}: model-only general part requires provisional_conclusion"
            )
        if not is_general and has_provisional:
            errors.append(
                f"sections.{index}: symbolic section cannot provide provisional_conclusion"
            )
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
    for planned, prose in zip(sections, model_payload["sections"], strict=True):
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
