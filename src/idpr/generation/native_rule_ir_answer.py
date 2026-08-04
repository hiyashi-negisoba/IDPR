"""Writer boundary for RuleIR-native Scallop results."""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from jsonschema import Draft202012Validator


class NativeGenerationError(ValueError):
    pass


def build_native_generation_request(
    *, case: Mapping[str, Any], native_report: Mapping[str, Any]
) -> dict[str, Any]:
    """Expose evidence and immutable symbolic directives, never raw runtime noise."""

    contract = native_report.get("generation_contract", {})
    if contract.get("source") != "scallop_derivation_only":
        raise NativeGenerationError("native report is not backed by Scallop directives")
    directives = contract.get("conclusion_directives", [])
    return {
        "case_id": native_report.get("case_id"),
        "question_text": str(case.get("question_text", "")),
        "question_prompt": str(case.get("question_prompt", "")),
        "instructions": (
            "각 unit의 법리와 사실 적용만 작성한다. 죄명과 결론은 호스트가 "
            "symbolic_directive에서 고정하므로 새로 만들거나 변경하지 않는다."
        ),
        "units": [
            {
                "unit_id": item["unit_id"],
                "symbolic_directive": item["symbolic_conclusion"],
                "established_relations": list(item["established_relations"]),
                "predicate_evidence": dict(item["evidence"]),
            }
            for item in directives
        ],
    }


def native_answer_schema(unit_ids: Sequence[str]) -> dict[str, Any]:
    """The model writes analysis only; conclusion fields do not exist in its grammar."""

    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["version", "sections"],
        "properties": {
            "version": {"const": "1.0.0"},
            "sections": {
                "type": "array",
                "minItems": len(unit_ids),
                "maxItems": len(unit_ids),
                "prefixItems": [
                    {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["unit_id", "rule", "application"],
                        "properties": {
                            "unit_id": {"const": unit_id},
                            "rule": {"type": "string", "minLength": 1},
                            "application": {"type": "string", "minLength": 1},
                        },
                    }
                    for unit_id in unit_ids
                ],
                "items": False,
            },
        },
    }


def finalize_native_answer(
    *, request: Mapping[str, Any], model_payload: Mapping[str, Any]
) -> dict[str, Any]:
    """Validate prose and attach the conclusion exclusively from Scallop."""

    units = request.get("units", [])
    unit_ids = [str(item["unit_id"]) for item in units]
    errors = [
        f"{'.'.join(str(part) for part in error.absolute_path) or '$'}: {error.message}"
        for error in Draft202012Validator(native_answer_schema(unit_ids)).iter_errors(
            model_payload
        )
    ]
    if errors:
        raise NativeGenerationError("; ".join(errors))
    conclusion_text = {
        "established": "성립",
        "not_established": "불성립",
        "undetermined": "성립 여부 미확정",
        "conflict": "상충하는 predicate 평가로 결론 유보",
        "no_derived_outcome": "도출된 결론 없음",
    }
    sections = []
    for prose, directive in zip(model_payload["sections"], units, strict=True):
        status = str(directive["symbolic_directive"])
        sections.append({
            **dict(prose),
            "symbolic_conclusion": status,
            "conclusion": conclusion_text[status],
            "established_relations": list(directive["established_relations"]),
        })
    return {
        "version": "1.0.0",
        "case_id": request.get("case_id"),
        "sections": sections,
        "overall_conclusion": "; ".join(
            f"{item['unit_id']}: {item['conclusion']}" for item in sections
        ),
        "conclusion_source": "scallop_derivation_only",
    }
