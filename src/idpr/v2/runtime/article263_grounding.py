"""Dedicated Article 263 Call 2 route over general factual occurrences."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from idpr.v2.evaluate import TruthValue
from idpr.v2.gold_factual_identity import GoldArticle263PairBinding, GoldOccurrence
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.truths import CaseTruths

ARTICLE263_PREDICATE_REFS = (
    "legal_element.concurrent_independent_acts",
    "legal_element.same_object_of_result",
    "legal_element.causal_origin_unascertained",
)
_TRUTHS = frozenset({"TRUE", "FALSE", "UNKNOWN"})


class Article263GroundingError(ValueError):
    pass


@dataclass(frozen=True)
class Article263OccurrencePair:
    pair_id: str
    left: OffenseInstanceKey
    right: OffenseInstanceKey

    def as_dict(self) -> dict[str, Any]:
        def key(value: OffenseInstanceKey) -> dict[str, str]:
            return {
                "case_id": value.case_id,
                "actor_id": value.actor_id,
                "offense_ref": value.offense_ref,
                "occurrence_id": value.occurrence_id,
            }

        return {
            "pair_id": self.pair_id,
            "left_instance_key": key(self.left),
            "right_instance_key": key(self.right),
        }


@dataclass(frozen=True)
class Article263PairAssessment:
    pair: Article263OccurrencePair
    truths: tuple[tuple[str, TruthValue], ...]


def plan_article263_occurrence_pairs(
    bindings: Iterable[GoldArticle263PairBinding],
    instances: Iterable[OffenseInstanceKey],
) -> tuple[Article263OccurrencePair, ...]:
    """Bind only manually selected occurrence pairs to injury instances.

    This is a candidate route only.  Concurrency, independence, same legal
    object, and causal uncertainty remain the three model/symbolic predicates.
    """
    instance_values = tuple(instances)
    values: list[Article263OccurrencePair] = []
    for binding in bindings:
        left_matches = tuple(
            value for value in instance_values
            if value.case_id == binding.sub_question_id
            and value.occurrence_id == binding.left_occurrence_id
            and value.offense_ref == "offense.injury"
        )
        right_matches = tuple(
            value for value in instance_values
            if value.case_id == binding.sub_question_id
            and value.occurrence_id == binding.right_occurrence_id
            and value.offense_ref == "offense.injury"
        )
        if len(left_matches) != 1 or len(right_matches) != 1:
            raise Article263GroundingError(
                f"{binding.sub_question_id}: binding must resolve to two injury instances"
            )
        values.append(
            Article263OccurrencePair(
                pair_id=f"article263-pair:{len(values) + 1:04d}",
                left=left_matches[0],
                right=right_matches[0],
            )
        )
    return tuple(values)


def article263_request_payload(
    *, occurrences: Iterable[GoldOccurrence], pairs: Iterable[Article263OccurrencePair]
) -> dict[str, Any]:
    pair_values = tuple(pairs)
    if not pair_values:
        raise Article263GroundingError("empty Article 263 pair set is a host no-op")
    occurrence_values = tuple(occurrences)
    occurrence_by_id = {value.occurrence_id: value for value in occurrence_values}
    if len(occurrence_by_id) != len(occurrence_values):
        raise Article263GroundingError("duplicate Article 263 evidence occurrence")
    required_ids = {
        instance.occurrence_id
        for pair in pair_values
        for instance in (pair.left, pair.right)
    }
    if set(occurrence_by_id) != required_ids:
        raise Article263GroundingError(
            "Article 263 request must contain exactly the bound occurrence evidence"
        )
    return {
        "occurrence_evidence": [occurrence_by_id[value].as_dict() for value in sorted(required_ids)],
        "article263_pairs": [value.as_dict() for value in pair_values],
        "predicate_refs": list(ARTICLE263_PREDICATE_REFS),
    }


def article263_schema(pairs: Iterable[Article263OccurrencePair]) -> dict[str, Any]:
    pair_values = tuple(pairs)
    if not pair_values:
        raise Article263GroundingError("empty Article 263 pair set has no schema")
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["pair_assessments"],
        "properties": {
            "pair_assessments": {
                "type": "array",
                "minItems": len(pair_values),
                "maxItems": len(pair_values),
                "prefixItems": [
                    {
                        "type": "object",
                        "additionalProperties": False,
                        "required": ["pair_id", "truths"],
                        "properties": {
                            "pair_id": {"const": pair.pair_id},
                            "truths": {
                                "type": "array",
                                "minItems": 3,
                                "maxItems": 3,
                                "prefixItems": [
                                    {
                                        "type": "object",
                                        "additionalProperties": False,
                                        "required": ["predicate_ref", "truth"],
                                        "properties": {
                                            "predicate_ref": {"const": ref},
                                            "truth": {"type": "string", "enum": sorted(_TRUTHS)},
                                        },
                                    }
                                    for ref in ARTICLE263_PREDICATE_REFS
                                ],
                                "items": False,
                            },
                        },
                    }
                    for pair in pair_values
                ],
                "items": False,
            }
        },
    }


def validate_article263_output(
    payload: Any, *, pairs: Iterable[Article263OccurrencePair]
) -> tuple[Article263PairAssessment, ...]:
    expected = tuple(pairs)
    if not isinstance(payload, Mapping) or set(payload) != {"pair_assessments"}:
        raise Article263GroundingError("response must contain exactly pair_assessments")
    raw_values = payload["pair_assessments"]
    if not isinstance(raw_values, list) or len(raw_values) != len(expected):
        raise Article263GroundingError("pair_assessments cardinality mismatch")
    output: list[Article263PairAssessment] = []
    for index, (raw, pair) in enumerate(zip(raw_values, expected, strict=True)):
        if not isinstance(raw, Mapping) or set(raw) != {"pair_id", "truths"}:
            raise Article263GroundingError(f"pair_assessments[{index}] shape mismatch")
        if raw["pair_id"] != pair.pair_id or not isinstance(raw["truths"], list):
            raise Article263GroundingError(f"pair_assessments[{index}] target mismatch")
        truths = []
        for position, ref in enumerate(ARTICLE263_PREDICATE_REFS):
            if position >= len(raw["truths"]):
                raise Article263GroundingError(f"pair_assessments[{index}] missing truth")
            value = raw["truths"][position]
            if (
                not isinstance(value, Mapping)
                or set(value) != {"predicate_ref", "truth"}
                or value["predicate_ref"] != ref
                or value["truth"] not in _TRUTHS
            ):
                raise Article263GroundingError(f"pair_assessments[{index}] truth mismatch")
            truths.append((ref, value["truth"]))
        if len(raw["truths"]) != len(ARTICLE263_PREDICATE_REFS):
            raise Article263GroundingError(f"pair_assessments[{index}] extra truth")
        output.append(Article263PairAssessment(pair, tuple(truths)))
    return tuple(output)


def add_article263_truths(
    base: CaseTruths, assessments: Sequence[Article263PairAssessment]
) -> CaseTruths:
    """Attach pair results to both existing injury instances; never attribute conduct."""
    predicate = dict(base.predicate)
    for assessment in assessments:
        for instance in (assessment.pair.left, assessment.pair.right):
            for ref, truth in assessment.truths:
                key = (instance, ref)
                if key in predicate and predicate[key] != truth:
                    raise Article263GroundingError(f"conflicting Article 263 truth for {key!r}")
                predicate[key] = truth
    return CaseTruths(predicate=predicate, relation=base.relation)


__all__ = [
    "ARTICLE263_PREDICATE_REFS",
    "Article263GroundingError",
    "Article263OccurrencePair",
    "Article263PairAssessment",
    "add_article263_truths",
    "article263_request_payload",
    "article263_schema",
    "plan_article263_occurrence_pairs",
    "validate_article263_output",
]
