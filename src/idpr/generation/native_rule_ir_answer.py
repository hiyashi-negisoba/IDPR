"""Section-at-a-time writer boundary for committed RuleIR conclusions."""

from __future__ import annotations

from typing import Any, Mapping, Sequence


class NativeGenerationError(ValueError):
    pass


CONCLUSION_TEXT = {
    "established": "성립",
    "not_established": "불성립",
    "undetermined": "성립 여부 미확정",
    "conflict": "상충하는 predicate 평가로 결론 유보",
    "no_derived_outcome": "도출된 결론 없음",
}


def build_native_section_requests(
    *,
    case: Mapping[str, Any],
    selection: Mapping[str, Any],
    native_report: Mapping[str, Any],
) -> list[dict[str, Any]]:
    """Create one small prose request for every executed symbolic issue."""

    contract = native_report.get("generation_contract", {})
    if contract.get("source") != "committed_rule_ir_scallop_only":
        raise NativeGenerationError(
            "native report is not backed by committed RuleIR Scallop directives"
        )
    issue_by_id = {
        str(issue["issue_id"]): issue for issue in selection.get("issues", [])
    }
    requests = []
    for directive in contract.get("conclusion_directives", []):
        issue_id = str(directive["issue_id"])
        if issue_id not in issue_by_id:
            raise NativeGenerationError(
                f"symbolic directive has no selected issue: {issue_id}"
            )
        issue = issue_by_id[issue_id]
        requests.append(
            {
                "version": "1.0.0",
                "case_id": native_report.get("case_id"),
                "issue_id": issue_id,
                "unit_id": directive["unit_id"],
                "heading": issue["reported_label"],
                "question_text": str(case.get("question_text", "")),
                "question_prompt": str(case.get("question_prompt", "")),
                "instructions": (
                    "법리와 사안의 적용만 Markdown으로 작성한다. 제목과 최종 결론은 "
                    "호스트가 부착하므로 작성하지 않는다."
                ),
                "symbolic_directive": directive["symbolic_conclusion"],
                "established_relations": list(directive["established_relations"]),
                "predicate_evidence": dict(directive["evidence"]),
                "compiled_scl_path": directive["compiled_scl_path"],
                "compiled_scl_sha256": directive["compiled_scl_sha256"],
            }
        )
    return requests


def validate_native_section_prose(text: str) -> None:
    """Reject empty or JSON responses while accepting flexible IRAC essays."""

    stripped = text.strip()
    errors = []
    if not stripped:
        errors.append("section prose is empty")
    if len(stripped) > 50_000:
        errors.append("section prose exceeds 50,000 characters")
    if stripped.startswith("{") or stripped.startswith("["):
        errors.append("section writer returned JSON instead of Markdown")
    if errors:
        raise NativeGenerationError("; ".join(errors))


def finalize_native_answer(
    *,
    section_requests: Sequence[Mapping[str, Any]],
    prose_by_issue: Mapping[str, str],
    unsupported_issues: Sequence[Mapping[str, Any]] = (),
    case_id: str | None = None,
) -> dict[str, Any]:
    """Attach every heading and conclusion exclusively from host-owned state."""

    expected = [str(request["issue_id"]) for request in section_requests]
    if set(prose_by_issue) != set(expected):
        raise NativeGenerationError(
            "writer output issue set mismatch: "
            f"missing={sorted(set(expected) - set(prose_by_issue))}, "
            f"extra={sorted(set(prose_by_issue) - set(expected))}"
        )
    sections = []
    for request in section_requests:
        issue_id = str(request["issue_id"])
        prose = prose_by_issue[issue_id].strip()
        validate_native_section_prose(prose)
        status = str(request["symbolic_directive"])
        if status not in CONCLUSION_TEXT:
            raise NativeGenerationError(f"unknown symbolic directive: {status}")
        sections.append(
            {
                "issue_id": issue_id,
                "unit_id": request["unit_id"],
                "heading": request["heading"],
                "prose": prose,
                "symbolic_conclusion": status,
                "conclusion": CONCLUSION_TEXT[status],
                "established_relations": list(request["established_relations"]),
                "compiled_scl_path": request["compiled_scl_path"],
                "compiled_scl_sha256": request["compiled_scl_sha256"],
            }
        )
    fallback_case_id = (
        case_id
        or (section_requests[0]["case_id"] if section_requests else None)
        or (unsupported_issues[0].get("case_id") if unsupported_issues and isinstance(unsupported_issues[0], dict) else None)
    )
    return {
        "version": "1.0.0",
        "case_id": fallback_case_id,
        "sections": sections,
        "unsupported_issues": [dict(issue) for issue in unsupported_issues],
        "conclusion_source": "committed_rule_ir_scallop_only",
    }


def render_native_answer(answer: Mapping[str, Any]) -> str:
    """Render host-owned answer structure around model-written section prose."""

    lines = ["# 형법 사례 답안", ""]
    for index, section in enumerate(answer["sections"], 1):
        lines.extend(
            [
                f"## {index}. {section['heading']}",
                "",
                str(section["prose"]),
                "",
                "### 결론",
                "",
                str(section["conclusion"]),
                "",
            ]
        )
    unsupported = answer.get("unsupported_issues", [])
    if unsupported:
        lines.extend(["## 지원되지 않는 쟁점", ""])
        for item in unsupported:
            lines.append(
                f"- {item['reported_label']}: `predicate_ir_missing`"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
