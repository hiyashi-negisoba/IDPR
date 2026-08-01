"""Call 2 contract: assess every candidate card against host-identified facts.

The schema is built for one candidate set. Card ids are object keys and every key is
required, so guided decoding cannot omit a difficult card or add one that the host did not
select. The model reports only the judgment and its evidence links; rationale, confidence,
and authority ids are deliberately absent because none is consumed by the symbolic layer.
"""

from __future__ import annotations

import re
from typing import Any, Iterable, Mapping, Sequence

from jsonschema import Draft202012Validator

from idpr.eval.input_formatter import assert_no_leaked_fields
from idpr.neural.fact_graph import assessment_facts

SCHEMA_VERSION = "1.0.0"
STATUSES = ("satisfied", "not_satisfied", "unknown")

_CASE_ID_RE = re.compile(r"^[a-z0-9][a-z0-9_.-]*$")


class CardAssessmentError(ValueError):
    """Raised with every call-2 contract violation found."""

    def __init__(self, errors: Sequence[str]) -> None:
        self.errors = list(errors)
        super().__init__("; ".join(self.errors))


def _unique(values: Iterable[str], *, name: str) -> tuple[str, ...]:
    result = tuple(values)
    if not result:
        raise CardAssessmentError([f"{name} must not be empty"])
    if any(not isinstance(value, str) or not value for value in result):
        raise CardAssessmentError([f"{name} must contain non-empty strings"])
    duplicates = sorted(value for value in set(result) if result.count(value) > 1)
    if duplicates:
        raise CardAssessmentError([f"duplicate {name}: {duplicates}"])
    return result


def _assessment_item_schema(fact_ids: Sequence[str]) -> dict[str, Any]:
    evidence = {
        "type": "array",
        "maxItems": 24,
        "uniqueItems": True,
        "items": {"type": "string", "enum": list(fact_ids)},
    }
    return {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "status",
            "basis_fact_ids",
            "counter_fact_ids",
            "missing_facts",
        ],
        "properties": {
            "status": {"type": "string", "enum": list(STATUSES)},
            "basis_fact_ids": evidence,
            "counter_fact_ids": evidence,
            "missing_facts": {
                "type": "array",
                "maxItems": 12,
                "uniqueItems": True,
                "items": {"type": "string", "minLength": 1, "maxLength": 500},
            },
        },
    }


def card_assessment_schema(
    *, case_id: str, card_ids: Sequence[str], fact_ids: Sequence[str]
) -> dict[str, Any]:
    """Build a schema in which every host-selected card is a required output field."""
    if not _CASE_ID_RE.fullmatch(case_id):
        raise CardAssessmentError([f"case_id must be a safe identifier, got {case_id!r}"])
    cards = _unique(card_ids, name="card_ids")
    facts = _unique(fact_ids, name="fact_ids")
    properties = {
        card_id: {"$ref": "#/$defs/assessment"} for card_id in cards
    }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "idpr/CardAssessmentBundle",
        "description": "Call 2 output over one host-selected candidate-card set.",
        "$defs": {"assessment": _assessment_item_schema(facts)},
        "type": "object",
        "additionalProperties": False,
        "required": ["version", "case_id", "assessments"],
        "properties": {
            "version": {"const": SCHEMA_VERSION},
            "case_id": {"const": case_id},
            "assessments": {
                "type": "object",
                "additionalProperties": False,
                "required": list(cards),
                "properties": properties,
            },
        },
    }


def assessment_request(
    *,
    case: Mapping[str, Any],
    fact_graph: Mapping[str, Any],
    cards: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """Build the call-2 payload from whitelisted case fields and reviewed card text.

    Benchmark annotations never enter this function. Card provenance stays on the host;
    the model receives exactly ``id`` and ``proposition`` for each candidate card.
    """
    case_id = str(case.get("sub_question_id", ""))
    if fact_graph.get("case_id") != case_id:
        raise CardAssessmentError(["fact graph case_id does not match the case"])
    model_cards = [
        {"id": str(card.get("id", "")), "proposition": str(card.get("proposition", ""))}
        for card in cards
    ]
    errors: list[str] = []
    for index, card in enumerate(model_cards):
        if not card["id"] or not card["proposition"]:
            errors.append(f"cards[{index}] requires id and proposition")
    if len({card["id"] for card in model_cards}) != len(model_cards):
        errors.append("candidate card ids must be unique")
    if not model_cards:
        errors.append("candidate cards must not be empty")
    if errors:
        raise CardAssessmentError(errors)
    request = {
        "case_id": case_id,
        "question_text": str(case.get("question_text", "")),
        "question_prompt": str(case.get("question_prompt", "")),
        "entities": [dict(entity) for entity in fact_graph.get("entities", [])],
        "facts": assessment_facts(fact_graph),
        "cards": model_cards,
    }
    assert_no_leaked_fields(request)
    return request


def validate_card_assessments(
    payload: Mapping[str, Any],
    *,
    case_id: str,
    card_ids: Sequence[str],
    fact_ids: Sequence[str],
) -> None:
    """Validate grammar, exact card coverage, and status/evidence coupling."""
    schema = card_assessment_schema(
        case_id=case_id, card_ids=card_ids, fact_ids=fact_ids
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
        for card_id in card_ids:
            assessment = assessments.get(card_id)
            if not isinstance(assessment, Mapping):
                continue
            status = assessment.get("status")
            if status == "satisfied" and not assessment.get("basis_fact_ids"):
                errors.append(f"{card_id}: satisfied requires at least one basis fact")
            if status == "not_satisfied" and not assessment.get("counter_fact_ids"):
                errors.append(
                    f"{card_id}: not_satisfied requires at least one counter fact"
                )
            if status == "unknown" and not assessment.get("missing_facts"):
                errors.append(f"{card_id}: unknown requires missing_facts")
    if errors:
        raise CardAssessmentError(errors)


def card_status_rows(payload: Mapping[str, Any]) -> tuple[tuple[str, str], ...]:
    """Return validated assessment values in their schema-preserved card order.

    Card polarity is not accepted here. It remains host-owned metadata in the compiled
    rulebase, where positive, negative, and exception cards are interpreted
    deterministically rather than by the model.
    """
    return tuple(
        (card_id, str(assessment["status"]))
        for card_id, assessment in payload["assessments"].items()
    )
