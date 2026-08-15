"""KCL-26 manual factual identity, deliberately free of legal labels.

이 파일이 싣는 것은 **사람이 손으로 적은** 사실 식별자다. 파이프라인이 산출한 것이 아니므로
성능 주장의 근거로 쓸 수 없고, 실행 경로에서는 증거 텍스트와 span의 출처로만 쓴다.
"""

from __future__ import annotations

import json
from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class GoldFactualIdentityError(ValueError):
    pass


_OCCURRENCE_ROW_FIELDS = frozenset({"sub_question_id", "occurrences"})
_OCCURRENCE_FIELDS = frozenset({"occurrence_id", "actor_id", "source_text"})
_PAIR_ROW_FIELDS = frozenset(
    {"sub_question_id", "left_occurrence_id", "right_occurrence_id", "relation_source_text"}
)
_PARTICIPANT_ROW_FIELDS = frozenset({"sub_question_id", "participants"})
_PARTICIPANT_FIELDS = frozenset({"participant_id", "participant_label", "source_text"})


@dataclass(frozen=True)
class GoldOccurrence:
    occurrence_id: str
    actor_id: str
    source_text: str
    source_start: int
    source_end: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "occurrence_id": self.occurrence_id,
            "actor_id": self.actor_id,
            "source_text": self.source_text,
            "source_span": {"start": self.source_start, "end": self.source_end},
        }


@dataclass(frozen=True)
class GoldOccurrenceSet:
    sub_question_id: str
    occurrences: tuple[GoldOccurrence, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "sub_question_id": self.sub_question_id,
            "occurrences": [value.as_dict() for value in self.occurrences],
        }


@dataclass(frozen=True)
class GoldFactualParticipant:
    """One source-local person identity with no legal or participation label."""

    participant_id: str
    participant_label: str
    source_text: str
    source_start: int
    source_end: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "participant_id": self.participant_id,
            "participant_label": self.participant_label,
            "source_text": self.source_text,
            "source_span": {"start": self.source_start, "end": self.source_end},
        }


@dataclass(frozen=True)
class GoldFactualParticipantSet:
    sub_question_id: str
    participants: tuple[GoldFactualParticipant, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "sub_question_id": self.sub_question_id,
            "participants": [value.as_dict() for value in self.participants],
        }


@dataclass(frozen=True)
class GoldArticle263PairBinding:
    sub_question_id: str
    left_occurrence_id: str
    right_occurrence_id: str
    relation_source_text: str
    relation_source_start: int
    relation_source_end: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "sub_question_id": self.sub_question_id,
            "left_occurrence_id": self.left_occurrence_id,
            "right_occurrence_id": self.right_occurrence_id,
            "relation_source_text": self.relation_source_text,
            "relation_source_span": {
                "start": self.relation_source_start,
                "end": self.relation_source_end,
            },
        }


def _read_jsonl(path: Path) -> tuple[Mapping[str, Any], ...]:
    values: list[Mapping[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            value = json.loads(line)
        except json.JSONDecodeError as exc:
            raise GoldFactualIdentityError(f"{path}:{line_number}: invalid JSON") from exc
        if not isinstance(value, Mapping):
            raise GoldFactualIdentityError(f"{path}:{line_number}: row must be an object")
        values.append(value)
    return tuple(values)


def load_gold_occurrences(
    path: Path,
    *,
    case_text_by_id: Mapping[str, str],
    required_case_ids: Iterable[str],
) -> dict[str, GoldOccurrenceSet]:
    """Load an exact 26-row factual-only oracle and derive source offsets."""
    required = tuple(required_case_ids)
    if not required or len(required) != len(set(required)):
        raise GoldFactualIdentityError("required case ids must be nonempty and unique")
    output: dict[str, GoldOccurrenceSet] = {}
    for row_number, row in enumerate(_read_jsonl(path), 1):
        if set(row) != _OCCURRENCE_ROW_FIELDS:
            raise GoldFactualIdentityError(
                f"row {row_number}: allowed fields are {sorted(_OCCURRENCE_ROW_FIELDS)}"
            )
        case_id = row["sub_question_id"]
        raw_occurrences = row["occurrences"]
        if not isinstance(case_id, str) or case_id not in case_text_by_id:
            raise GoldFactualIdentityError(f"row {row_number}: unknown sub_question_id")
        if case_id in output:
            raise GoldFactualIdentityError(f"row {row_number}: duplicate {case_id}")
        if not isinstance(raw_occurrences, list) or not raw_occurrences:
            raise GoldFactualIdentityError(f"{case_id}: occurrences must be a nonempty array")
        case_text = case_text_by_id[case_id]
        occurrences: list[GoldOccurrence] = []
        seen_identity: set[tuple[str, str]] = set()
        for index, raw in enumerate(raw_occurrences, 1):
            if not isinstance(raw, Mapping) or set(raw) != _OCCURRENCE_FIELDS:
                raise GoldFactualIdentityError(
                    f"{case_id}: occurrence {index} allowed fields are "
                    f"{sorted(_OCCURRENCE_FIELDS)}"
                )
            occurrence_id = raw["occurrence_id"]
            actor_id = raw["actor_id"]
            source_text = raw["source_text"]
            expected_id = f"gocc:{index:03d}"
            if occurrence_id != expected_id:
                raise GoldFactualIdentityError(
                    f"{case_id}: expected occurrence_id {expected_id!r}"
                )
            if not isinstance(actor_id, str) or not actor_id.strip():
                raise GoldFactualIdentityError(f"{case_id}/{occurrence_id}: invalid actor_id")
            if not isinstance(source_text, str) or not source_text.strip():
                raise GoldFactualIdentityError(f"{case_id}/{occurrence_id}: empty source_text")
            start = case_text.find(source_text)
            if start < 0 or case_text.find(source_text, start + 1) >= 0:
                raise GoldFactualIdentityError(
                    f"{case_id}/{occurrence_id}: source_text must occur exactly once"
                )
            identity = (actor_id, source_text)
            if identity in seen_identity:
                raise GoldFactualIdentityError(
                    f"{case_id}/{occurrence_id}: duplicate actor/source collision"
                )
            seen_identity.add(identity)
            occurrences.append(
                GoldOccurrence(
                    occurrence_id,
                    actor_id,
                    source_text,
                    start,
                    start + len(source_text),
                )
            )
        output[case_id] = GoldOccurrenceSet(case_id, tuple(occurrences))
    missing = [value for value in required if value not in output]
    extra = sorted(set(output) - set(required))
    if missing or extra:
        raise GoldFactualIdentityError(
            f"gold occurrence case-list mismatch: missing={missing}, extra={extra}"
        )
    return output


def load_gold_article263_pairs(
    path: Path,
    *,
    occurrences_by_id: Mapping[str, GoldOccurrenceSet],
    case_text_by_id: Mapping[str, str],
) -> tuple[GoldArticle263PairBinding, ...]:
    """Load caller bindings only; an empty file is valid."""
    output: list[GoldArticle263PairBinding] = []
    seen: set[tuple[str, str, str]] = set()
    for row_number, row in enumerate(_read_jsonl(path), 1):
        if set(row) != _PAIR_ROW_FIELDS:
            raise GoldFactualIdentityError(
                f"pair row {row_number}: allowed fields are {sorted(_PAIR_ROW_FIELDS)}"
            )
        case_id = row["sub_question_id"]
        left = row["left_occurrence_id"]
        right = row["right_occurrence_id"]
        relation_source_text = row["relation_source_text"]
        if not all(
            isinstance(value, str) and value
            for value in (case_id, left, right, relation_source_text)
        ):
            raise GoldFactualIdentityError(f"pair row {row_number}: fields must be strings")
        occurrence_set = occurrences_by_id.get(case_id)
        if occurrence_set is None:
            raise GoldFactualIdentityError(f"pair row {row_number}: unknown case")
        known = {value.occurrence_id for value in occurrence_set.occurrences}
        if left == right or left not in known or right not in known:
            raise GoldFactualIdentityError(f"pair row {row_number}: invalid occurrence binding")
        case_text = case_text_by_id.get(case_id, "")
        source_start = case_text.find(relation_source_text)
        if source_start < 0 or case_text.find(relation_source_text, source_start + 1) >= 0:
            raise GoldFactualIdentityError(
                f"pair row {row_number}: relation_source_text must occur exactly once"
            )
        key = (case_id, left, right)
        reverse = (case_id, right, left)
        if key in seen or reverse in seen:
            raise GoldFactualIdentityError(f"pair row {row_number}: duplicate pair")
        seen.add(key)
        output.append(
            GoldArticle263PairBinding(
                case_id,
                left,
                right,
                relation_source_text,
                source_start,
                source_start + len(relation_source_text),
            )
        )
    return tuple(output)


def load_gold_factual_participants(
    path: Path, *, case_text_by_id: Mapping[str, str]
) -> dict[str, GoldFactualParticipantSet]:
    """Load a sparse, factual-only participant namespace from exact source spans.

    Sparse is intentional: these rows supplement the liable-actor occurrence universe; they do
    not expand it.  A participant label may coincide with a GOLD occurrence actor, but identity
    remains the explicit ``fpart:*`` key and is never merged by matching the display label.
    """
    output: dict[str, GoldFactualParticipantSet] = {}
    for row_number, row in enumerate(_read_jsonl(path), 1):
        if set(row) != _PARTICIPANT_ROW_FIELDS:
            raise GoldFactualIdentityError(
                f"participant row {row_number}: allowed fields are "
                f"{sorted(_PARTICIPANT_ROW_FIELDS)}"
            )
        case_id = row["sub_question_id"]
        raw_values = row["participants"]
        if not isinstance(case_id, str) or case_id not in case_text_by_id:
            raise GoldFactualIdentityError(f"participant row {row_number}: unknown case")
        if case_id in output:
            raise GoldFactualIdentityError(f"participant row {row_number}: duplicate case")
        if not isinstance(raw_values, list) or not raw_values:
            raise GoldFactualIdentityError(f"{case_id}: participants must be nonempty")
        case_text = case_text_by_id[case_id]
        participants: list[GoldFactualParticipant] = []
        seen_labels: set[str] = set()
        for index, raw in enumerate(raw_values, 1):
            if not isinstance(raw, Mapping) or set(raw) != _PARTICIPANT_FIELDS:
                raise GoldFactualIdentityError(
                    f"{case_id}: participant {index} allowed fields are "
                    f"{sorted(_PARTICIPANT_FIELDS)}"
                )
            participant_id = raw["participant_id"]
            participant_label = raw["participant_label"]
            source_text = raw["source_text"]
            expected_id = f"fpart:{index:03d}"
            if participant_id != expected_id:
                raise GoldFactualIdentityError(
                    f"{case_id}: expected participant_id {expected_id!r}"
                )
            if not all(
                isinstance(value, str) and value.strip()
                for value in (participant_label, source_text)
            ):
                raise GoldFactualIdentityError(
                    f"{case_id}/{participant_id}: label and source_text must be nonempty"
                )
            if participant_label in seen_labels:
                raise GoldFactualIdentityError(
                    f"{case_id}/{participant_id}: duplicate participant label"
                )
            start = case_text.find(source_text)
            if start < 0 or case_text.find(source_text, start + 1) >= 0:
                raise GoldFactualIdentityError(
                    f"{case_id}/{participant_id}: source_text must occur exactly once"
                )
            if participant_label not in source_text:
                raise GoldFactualIdentityError(
                    f"{case_id}/{participant_id}: source_text must contain participant label"
                )
            seen_labels.add(participant_label)
            participants.append(
                GoldFactualParticipant(
                    participant_id,
                    participant_label,
                    source_text,
                    start,
                    start + len(source_text),
                )
            )
        output[case_id] = GoldFactualParticipantSet(case_id, tuple(participants))
    return output


__all__ = [
    "GoldArticle263PairBinding",
    "GoldFactualIdentityError",
    "GoldFactualParticipant",
    "GoldFactualParticipantSet",
    "GoldOccurrence",
    "GoldOccurrenceSet",
    "load_gold_article263_pairs",
    "load_gold_factual_participants",
    "load_gold_occurrences",
]
