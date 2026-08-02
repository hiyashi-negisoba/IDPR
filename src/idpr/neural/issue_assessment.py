"""Issue-first Call-2 contract.

One output corresponds to one constituent issue.  General-rule cards are context inside
the issue; subordinate standards and case patterns are not silently turned into separate
mandatory questions.
"""

from __future__ import annotations

import re
from typing import Any, Iterable, Mapping, Sequence

from jsonschema import Draft202012Validator

from idpr.eval.input_formatter import assert_no_leaked_fields, scoped_question_text
from idpr.neural.fact_graph import assessment_facts

SCHEMA_VERSION = "2.0.0"
STATUSES = ("satisfied", "not_satisfied", "unknown")
_CASE_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_.-]*$")


class IssueAssessmentError(ValueError):
    def __init__(self, errors: Sequence[str]) -> None:
        self.errors = list(errors)
        super().__init__("; ".join(self.errors))


def _unique(values: Iterable[str], *, name: str) -> tuple[str, ...]:
    result = tuple(values)
    if not result:
        raise IssueAssessmentError([f"{name} must not be empty"])
    if any(not isinstance(value, str) or not value for value in result):
        raise IssueAssessmentError([f"{name} must contain non-empty strings"])
    duplicates = sorted(value for value in set(result) if result.count(value) > 1)
    if duplicates:
        raise IssueAssessmentError([f"duplicate {name}: {duplicates}"])
    return result


def _assessment_schema(fact_ids: Sequence[str]) -> dict[str, Any]:
    evidence = {
        "type": "array",
        "maxItems": 16,
        "uniqueItems": True,
        "items": {"type": "string", "enum": list(fact_ids)},
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["status", "basis_fact_ids", "counter_fact_ids", "missing_facts"],
        "properties": {
            "status": {"type": "string", "enum": list(STATUSES)},
            "basis_fact_ids": evidence,
            "counter_fact_ids": evidence,
            "missing_facts": {
                "type": "array",
                "maxItems": 8,
                "uniqueItems": True,
                "items": {"type": "string", "minLength": 1, "maxLength": 300},
            },
        },
        # The status constants are disjoint, so ``anyOf`` has one matching branch.  The
        # guidance backend implements anyOf directly; oneOf would require coercion.
        "anyOf": [
            {
                "properties": {
                    "status": {"const": "satisfied"},
                    "basis_fact_ids": {"minItems": 1},
                }
            },
            {
                "properties": {
                    "status": {"const": "not_satisfied"},
                    "counter_fact_ids": {"minItems": 1},
                }
            },
            {
                "properties": {
                    "status": {"const": "unknown"},
                    "missing_facts": {"minItems": 1},
                }
            },
        ],
    }


def issue_assessment_schema(
    *, case_id: str, issue_ids: Sequence[str], fact_ids: Sequence[str]
) -> dict[str, Any]:
    if not _CASE_ID_RE.fullmatch(case_id):
        raise IssueAssessmentError([f"case_id must be a safe identifier, got {case_id!r}"])
    issues = _unique(issue_ids, name="issue_ids")
    facts = _unique(fact_ids, name="fact_ids")
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "idpr/IssueAssessmentBundle",
        "$defs": {"assessment": _assessment_schema(facts)},
        "type": "object",
        "additionalProperties": False,
        "required": ["version", "case_id", "assessments"],
        "properties": {
            "version": {"const": SCHEMA_VERSION},
            "case_id": {"const": case_id},
            "assessments": {
                "type": "object",
                "additionalProperties": False,
                "required": list(issues),
                "properties": {
                    issue_id: {"$ref": "#/$defs/assessment"} for issue_id in issues
                },
            },
        },
    }


def issue_assessment_request(
    *,
    case: Mapping[str, Any],
    fact_graph: Mapping[str, Any],
    issues: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    case_id = str(case.get("sub_question_id", ""))
    if fact_graph.get("case_id") != case_id:
        raise IssueAssessmentError(["fact graph case_id does not match the case"])

    model_issues: list[dict[str, Any]] = []
    errors: list[str] = []
    for index, issue in enumerate(issues):
        issue_id = str(issue.get("issue_id", ""))
        question = str(issue.get("question", ""))
        rules = [str(rule) for rule in issue.get("rules", [])]
        raw_details = issue.get("details", [])
        details: list[dict[str, str]] = []
        if not isinstance(raw_details, Sequence) or isinstance(raw_details, (str, bytes)):
            errors.append(f"issues[{index}].details must be an array")
            raw_details = []
        for detail_index, detail in enumerate(raw_details):
            if not isinstance(detail, Mapping):
                errors.append(
                    f"issues[{index}].details[{detail_index}] must be an object"
                )
                continue
            card_id = str(detail.get("id", ""))
            proposition = str(detail.get("proposition", ""))
            if not card_id or not proposition:
                errors.append(
                    f"issues[{index}].details[{detail_index}] requires id and proposition"
                )
            details.append({"id": card_id, "proposition": proposition})
        if len({detail["id"] for detail in details}) != len(details):
            errors.append(f"issues[{index}].details contains duplicate ids")
        if not issue_id or not question or not rules or any(not rule for rule in rules):
            errors.append(f"issues[{index}] requires issue_id, question, and non-empty rules")
        model_issue: dict[str, Any] = {
            "issue_id": issue_id,
            "question": question,
            "rules": rules,
        }
        if details:
            model_issue["details"] = details
        model_issues.append(model_issue)
    if len({issue["issue_id"] for issue in model_issues}) != len(model_issues):
        errors.append("issue ids must be unique")
    if not model_issues:
        errors.append("issues must not be empty")
    if errors:
        raise IssueAssessmentError(errors)

    question_prompt = str(case.get("question_prompt", ""))
    request = {
        "case_id": case_id,
        "question_text": scoped_question_text(
            str(case.get("question_text", "")), question_prompt
        ),
        "question_prompt": question_prompt,
        "entities": [dict(entity) for entity in fact_graph.get("entities", [])],
        "facts": assessment_facts(fact_graph),
        "issues": model_issues,
    }
    assert_no_leaked_fields(request)
    return request


def validate_issue_assessments(
    payload: Mapping[str, Any],
    *,
    case_id: str,
    issue_ids: Sequence[str],
    fact_ids: Sequence[str],
) -> None:
    schema = issue_assessment_schema(
        case_id=case_id, issue_ids=issue_ids, fact_ids=fact_ids
    )
    errors = [
        f"{'.'.join(str(part) for part in error.absolute_path) or '$'}: {error.message}"
        for error in sorted(
            Draft202012Validator(schema).iter_errors(payload),
            key=lambda item: tuple(str(part) for part in item.path),
        )
    ]
    assessments = payload.get("assessments", {})
    if isinstance(assessments, Mapping):
        for issue_id in issue_ids:
            assessment = assessments.get(issue_id)
            if not isinstance(assessment, Mapping):
                continue
            status = assessment.get("status")
            if status == "satisfied" and not assessment.get("basis_fact_ids"):
                errors.append(f"{issue_id}: satisfied requires basis facts")
            if status == "not_satisfied" and not assessment.get("counter_fact_ids"):
                errors.append(f"{issue_id}: not_satisfied requires counter facts")
            if status == "unknown" and not assessment.get("missing_facts"):
                errors.append(f"{issue_id}: unknown requires concrete missing facts")
    if errors:
        raise IssueAssessmentError(errors)


def issue_status_rows(payload: Mapping[str, Any]) -> tuple[tuple[str, str], ...]:
    """Return validated issue ids and statuses for the symbolic input boundary."""
    assessments = payload.get("assessments", {})
    if not isinstance(assessments, Mapping):
        raise IssueAssessmentError(["assessments must be an object"])
    return tuple(
        (str(issue_id), str(assessment["status"]))
        for issue_id, assessment in assessments.items()
        if isinstance(assessment, Mapping)
    )
