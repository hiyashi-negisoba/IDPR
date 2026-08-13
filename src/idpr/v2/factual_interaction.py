"""Offense-free Call 1.5-P factual interaction binding contract."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from typing import Any, Literal

from idpr.v2.issue_binding import FactualEpisode

InteractionType = Literal[
    "request_or_instruction",
    "means_information_or_assistance",
    "agreement_or_coordinated_conduct",
]

INTERACTION_TYPES: tuple[InteractionType, ...] = (
    "request_or_instruction",
    "means_information_or_assistance",
    "agreement_or_coordinated_conduct",
)
MAX_INTERACTIONS_PER_EPISODE = 16


class FactualInteractionContractError(ValueError):
    def __init__(self, errors: Sequence[str]) -> None:
        self.errors = tuple(errors)
        super().__init__("; ".join(self.errors))


@dataclass(frozen=True)
class InteractionEvidence:
    evidence_id: str
    source_quote: str
    source_start: int
    source_end: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "source_quote": self.source_quote,
            "source_span": {"start": self.source_start, "end": self.source_end},
        }


@dataclass(frozen=True)
class FactualInteraction:
    interaction_id: str
    factual_episode_id: str
    interaction_type: InteractionType
    source_actor_id: str
    target_actor_ids: tuple[str, ...]
    evidence: tuple[InteractionEvidence, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "interaction_id": self.interaction_id,
            "factual_episode_id": self.factual_episode_id,
            "interaction_type": self.interaction_type,
            "source_actor_id": self.source_actor_id,
            "target_actor_ids": list(self.target_actor_ids),
            "evidence": [value.as_dict() for value in self.evidence],
        }


def factual_interaction_request_payload(
    *,
    case_id: str,
    question_prompt: str,
    responsibility_actor_ids: Sequence[str],
    episode: FactualEpisode,
) -> dict[str, Any]:
    if not case_id or not question_prompt.strip() or not responsibility_actor_ids:
        raise FactualInteractionContractError(
            ["case, question prompt, and responsibility actor universe must be non-empty"]
        )
    participants = episode.participants
    if not participants or len(participants) != len(set(participants)):
        raise FactualInteractionContractError(["episode participant universe is invalid"])
    source_quotes = tuple(value.source_quote for value in episode.source_fragments)
    if not source_quotes:
        raise FactualInteractionContractError(["episode has no source quotes"])
    return {
        "case_id": case_id,
        "question_prompt": question_prompt,
        "responsibility_actor_ids": list(dict.fromkeys(responsibility_actor_ids)),
        "factual_episode_id": episode.factual_episode_id,
        "episode_participant_ids": list(participants),
        "episode_source_quotes": list(source_quotes),
    }


def factual_interaction_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["interactions"],
        "properties": {
            "interactions": {
                "type": "array",
                "maxItems": MAX_INTERACTIONS_PER_EPISODE,
                "uniqueItems": True,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "interaction_type",
                        "source_actor_id",
                        "target_actor_ids",
                        "evidence_quotes",
                    ],
                    "properties": {
                        "interaction_type": {
                            "type": "string",
                            "enum": list(INTERACTION_TYPES),
                        },
                        "source_actor_id": {"type": "string", "minLength": 1},
                        "target_actor_ids": {
                            "type": "array",
                            "minItems": 1,
                            "uniqueItems": True,
                            "items": {"type": "string", "minLength": 1},
                        },
                        "evidence_quotes": {
                            "type": "array",
                            "minItems": 1,
                            "uniqueItems": True,
                            "items": {"type": "string", "minLength": 1},
                        },
                    },
                },
            }
        },
    }


def validate_factual_interaction_output(
    payload: Any,
    *,
    case_text: str,
    episode: FactualEpisode,
) -> tuple[FactualInteraction, ...]:
    errors: list[str] = []
    if not isinstance(payload, Mapping) or set(payload) != {"interactions"}:
        raise FactualInteractionContractError(
            ["output must contain exactly one interactions array"]
        )
    raw = payload.get("interactions")
    if not isinstance(raw, list):
        raise FactualInteractionContractError(["interactions must be an array"])
    if len(raw) > MAX_INTERACTIONS_PER_EPISODE:
        errors.append(
            f"interactions exceeds {MAX_INTERACTIONS_PER_EPISODE} per episode"
        )
    participants = frozenset(episode.participants)
    source_scopes = tuple(value.source_quote for value in episode.source_fragments)
    output: list[FactualInteraction] = []
    semantic_keys: set[tuple[str, str, tuple[str, ...], tuple[str, ...]]] = set()
    episode_suffix = episode.factual_episode_id.rsplit(":", 1)[-1]
    for index, value in enumerate(raw, 1):
        where = f"interactions[{index - 1}]"
        if not isinstance(value, Mapping) or set(value) != {
            "interaction_type",
            "source_actor_id",
            "target_actor_ids",
            "evidence_quotes",
        }:
            errors.append(f"{where} has invalid fields")
            continue
        kind = value.get("interaction_type")
        source = value.get("source_actor_id")
        targets = value.get("target_actor_ids")
        quotes = value.get("evidence_quotes")
        if kind not in INTERACTION_TYPES:
            errors.append(f"{where}.interaction_type is invalid")
        if not isinstance(source, str) or source not in participants:
            errors.append(f"{where}.source_actor_id is outside episode participants")
        if (
            not isinstance(targets, list)
            or not targets
            or not all(isinstance(item, str) and item in participants for item in targets)
            or len(targets) != len(set(targets))
        ):
            errors.append(f"{where}.target_actor_ids is invalid")
            targets = []
        if isinstance(source, str) and source in targets:
            errors.append(f"{where} contains a factual self-link")
        if (
            not isinstance(quotes, list)
            or not quotes
            or not all(isinstance(item, str) and item.strip() for item in quotes)
            or len(quotes) != len(set(quotes))
        ):
            errors.append(f"{where}.evidence_quotes is invalid")
            quotes = []
        interaction_id = f"finteraction:{episode_suffix}:{index:03d}"
        evidence: list[InteractionEvidence] = []
        for quote_index, quote in enumerate(quotes, 1):
            start = case_text.find(quote)
            if start < 0 or case_text.find(quote, start + 1) >= 0:
                errors.append(
                    f"{where}.evidence_quotes[{quote_index - 1}] must occur exactly once in case_text"
                )
                continue
            if not any(quote in scope for scope in source_scopes):
                errors.append(
                    f"{where}.evidence_quotes[{quote_index - 1}] is outside the factual episode"
                )
                continue
            evidence.append(
                InteractionEvidence(
                    f"{interaction_id}:evidence:{quote_index:03d}",
                    quote,
                    start,
                    start + len(quote),
                )
            )
        if (
            kind in INTERACTION_TYPES
            and isinstance(source, str)
            and source in participants
            and targets
            and len(evidence) == len(quotes)
        ):
            key = (kind, source, tuple(targets), tuple(quotes))
            if key in semantic_keys:
                errors.append(f"{where} duplicates an earlier interaction")
            semantic_keys.add(key)
            output.append(
                FactualInteraction(
                    interaction_id,
                    episode.factual_episode_id,
                    kind,
                    source,
                    tuple(targets),
                    tuple(evidence),
                )
            )
    if errors:
        raise FactualInteractionContractError(errors)
    return tuple(output)


def parse_factual_interactions(
    values: Iterable[Mapping[str, Any]],
    *,
    case_text: str,
    episodes: Iterable[FactualEpisode],
) -> tuple[FactualInteraction, ...]:
    """Revalidate host-enriched persisted Call 1.5-P interactions."""
    episode_values = tuple(episodes)
    episode_by_id = {value.factual_episode_id: value for value in episode_values}
    if len(episode_by_id) != len(episode_values):
        raise FactualInteractionContractError(["duplicate factual episode identity"])
    grouped: dict[str, list[Mapping[str, Any]]] = {}
    for value in values:
        if not isinstance(value, Mapping):
            raise FactualInteractionContractError(
                ["persisted factual interaction must be an object"]
            )
        episode_id = value.get("factual_episode_id")
        if not isinstance(episode_id, str) or episode_id not in episode_by_id:
            raise FactualInteractionContractError(
                ["persisted factual interaction has dangling episode identity"]
            )
        grouped.setdefault(episode_id, []).append(value)
    output: list[FactualInteraction] = []
    for episode_id, episode_values in grouped.items():
        raw = {"interactions": []}
        for value in episode_values:
            evidence = value.get("evidence")
            raw["interactions"].append(
                {
                    "interaction_type": value.get("interaction_type"),
                    "source_actor_id": value.get("source_actor_id"),
                    "target_actor_ids": value.get("target_actor_ids"),
                    "evidence_quotes": [
                        item.get("source_quote")
                        for item in evidence
                        if isinstance(item, Mapping)
                    ]
                    if isinstance(evidence, list)
                    else None,
                }
            )
        parsed = validate_factual_interaction_output(
            raw, case_text=case_text, episode=episode_by_id[episode_id]
        )
        if [value.as_dict() for value in parsed] != list(episode_values):
            raise FactualInteractionContractError(
                [f"{episode_id}: persisted factual interaction lineage is noncanonical"]
            )
        output.extend(parsed)
    return tuple(output)


__all__ = [
    "FactualInteraction",
    "FactualInteractionContractError",
    "InteractionEvidence",
    "InteractionType",
    "factual_interaction_request_payload",
    "factual_interaction_schema",
    "parse_factual_interactions",
    "validate_factual_interaction_output",
]
