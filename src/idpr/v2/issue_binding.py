"""Full-case-text Call 1.5 case-time issue binding contract."""

from __future__ import annotations

import re
from collections.abc import Iterable, Mapping, Sequence
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

import yaml

from idpr.v2.registry import DefinitionRegistry

MAX_BINDINGS_PER_CASE = 64
_RESPONSIBILITY_ACTOR = re.compile(r"[甲乙丙丁戊己庚辛壬癸]")


class IssueBindingContractError(ValueError):
    def __init__(self, errors: Sequence[str]) -> None:
        self.errors = tuple(errors)
        super().__init__("; ".join(self.errors))


@dataclass(frozen=True)
class BindingSeedCue:
    seed_index: int
    offense_ref: str
    display_name: str
    statutory_refs: tuple[str, ...]
    minimal_conduct_description: str
    linked_offender_role: str | None = None
    """Which seeds may bind a `linked_offender`, read from the offense definition.

    Whether an offense presupposes another person's crime is a legal property of the offense, so
    the host answers it from the authored definition and tells Call 1.5.  Asking the model to
    decide it would put a legal classification back inside the factual binding step.
    """

    def as_dict(self) -> dict[str, Any]:
        payload = {
            "seed_index": self.seed_index,
            "offense_ref": self.offense_ref,
            "display_name": self.display_name,
            "statutory_refs": list(self.statutory_refs),
            "minimal_conduct_description": self.minimal_conduct_description,
        }
        if self.linked_offender_role is not None:
            payload["requires_linked_offender"] = self.linked_offender_role
        return payload


@dataclass(frozen=True)
class BindingFragment:
    fragment_id: str
    fragment_kind: Literal["episode_source", "factual_action", "context"]
    source_quote: str
    source_start: int
    source_end: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "fragment_id": self.fragment_id,
            "fragment_kind": self.fragment_kind,
            "source_quote": self.source_quote,
            "source_span": {"start": self.source_start, "end": self.source_end},
        }


@dataclass(frozen=True)
class FactualAction:
    """One time-local factual act, transfer, result, or status proposition.

    The source actor is the person syntactically/factually performing the action.
    It intentionally does not have to be the person whose liability is later
    assessed: a transfer by 乙 can be the focal receipt event for 丙.
    """

    factual_action_id: str
    factual_episode_id: str
    source_actor_id: str
    participant_ids: tuple[str, ...]
    source_fragments: tuple[BindingFragment, ...]
    sequence_index: int

    @property
    def evidence_text(self) -> str:
        return "\n".join(value.source_quote for value in self.source_fragments)

    def as_dict(self) -> dict[str, Any]:
        return {
            "factual_action_id": self.factual_action_id,
            "factual_episode_id": self.factual_episode_id,
            "source_actor_id": self.source_actor_id,
            "participant_ids": list(self.participant_ids),
            "source_fragments": [value.as_dict() for value in self.source_fragments],
            "sequence_index": self.sequence_index,
        }


@dataclass(frozen=True)
class FactualEpisode:
    factual_episode_id: str
    source_fragments: tuple[BindingFragment, ...]
    participants: tuple[str, ...]
    factual_actions: tuple[FactualAction, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {
            "factual_episode_id": self.factual_episode_id,
            "source_fragments": [value.as_dict() for value in self.source_fragments],
            "participants": list(self.participants),
            "factual_actions": [value.as_dict() for value in self.factual_actions],
        }


@dataclass(frozen=True)
class IssueBinding:
    """A seed's factual candidate, deliberately distinct from a realization.

    ``binding_id`` only identifies the Call 1.5 candidate.  It must never be
    used as a Call 2/Scallop occurrence identity.  The focal and supporting
    action references are materialized into a legal realization by the planner.
    """

    binding_id: str
    factual_episode_id: str
    seed_index: int
    offense_ref: str
    actor_id: str
    focal_action_id: str
    supporting_action_ids: tuple[str, ...]
    factual_targets: tuple[str, ...]

    directed_action_target: str | None = None
    """The person the source text explicitly says the conduct was aimed at.

    Deliberately narrower than `factual_targets`, which carries counterparts, recipients and any
    directly involved participant.  This is one person or nothing, and only when the source itself
    names the direction ("乙인 줄 알고", "…를 겨누어").  Together with `actual_result_bearer` it is
    the only factual basis for `relation.intended_object_divergence`; neither field asserts that a
    mistake occurred.
    """

    actual_result_bearer: str | None = None
    """The person the source text says actually bore the result of that conduct."""

    linked_offender: str | None = None
    """The other person whose own crime this offense presupposes (Article 151's object).

    Only bindable on a seed the host marked, from the offense's authored linked-offender
    dependency.  It names a person, never that person's liability.
    """

    def as_dict(self) -> dict[str, Any]:
        return {
            "binding_id": self.binding_id,
            "factual_episode_id": self.factual_episode_id,
            "seed_index": self.seed_index,
            "offense_ref": self.offense_ref,
            "actor_id": self.actor_id,
            "focal_action_id": self.focal_action_id,
            "supporting_action_ids": list(self.supporting_action_ids),
            "factual_targets": list(self.factual_targets),
            "directed_action_target": self.directed_action_target,
            "actual_result_bearer": self.actual_result_bearer,
            "linked_offender": self.linked_offender,
        }


@dataclass(frozen=True)
class SeedBindingResult:
    seed_index: int
    offense_ref: str
    bindings: tuple[IssueBinding, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "seed_index": self.seed_index,
            "offense_ref": self.offense_ref,
            "bindings": [value.as_dict() for value in self.bindings],
        }


@dataclass(frozen=True)
class IssueBindingResult:
    factual_episodes: tuple[FactualEpisode, ...]
    seed_results: tuple[SeedBindingResult, ...]

    @property
    def bindings(self) -> tuple[IssueBinding, ...]:
        return tuple(
            binding for result in self.seed_results for binding in result.bindings
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "factual_episodes": [value.as_dict() for value in self.factual_episodes],
            "seed_results": [value.as_dict() for value in self.seed_results],
        }


def question_actor_ids(question_prompt: str) -> tuple[str, ...]:
    """Return the source labels whose liability the question explicitly requests."""
    values = tuple(dict.fromkeys(_RESPONSIBILITY_ACTOR.findall(question_prompt)))
    if not values:
        raise IssueBindingContractError(
            ["question_prompt contains no supported responsibility actor label"]
        )
    return values


def _identity(registry: DefinitionRegistry, ref: str) -> tuple[str, tuple[str, ...]]:
    entry = registry.get(ref)
    if entry is None:
        raise IssueBindingContractError([f"unknown binding seed: {ref!r}"])
    identity = entry.payload.get("identity")
    if isinstance(identity, Mapping):
        name = identity.get("name")
        statutory = identity.get("statutory_refs")
        return (
            name if isinstance(name, str) else ref,
            tuple(value for value in (statutory or ()) if isinstance(value, str)),
        )
    derivation = entry.payload.get("derivation")
    source_refs: list[str] = []
    if isinstance(derivation, Mapping):
        if derivation.get("kind") == "qualify" and isinstance(derivation.get("base"), str):
            source_refs.append(derivation["base"])
        for component in derivation.get("components") or ():
            if isinstance(component, Mapping) and component.get("kind") == "offense":
                source_refs.append(str(component.get("ref")))
    statutes: list[str] = []
    for source in source_refs:
        _, values = _identity(registry, source)
        statutes.extend(values)
    return ref, tuple(dict.fromkeys(statutes))


def linked_offender_role(registry: DefinitionRegistry, offense_ref: str) -> str | None:
    """The authored linked-offender role for a seed, or None.

    Read from the definition so no code names an offense id.  Both offense kinds are consulted:
    a presupposing offense could later be authored as a derived offense.
    """
    entry = registry.get(offense_ref)
    if entry is None or entry.kind not in {"offense", "derived_offense"}:
        return None
    dependency = entry.payload.get("linked_offender_dependency")
    if not isinstance(dependency, Mapping):
        return None
    role = dependency.get("role")
    return role if isinstance(role, str) else None


def linked_offender_seed_refs(
    registry: DefinitionRegistry, seeds: Iterable[str]
) -> tuple[str, ...]:
    """The subset of seeds the host will accept a `linked_offender` on."""
    return tuple(
        dict.fromkeys(ref for ref in seeds if linked_offender_role(registry, ref) is not None)
    )


UNAUTHORED_CUE_KEY = "unauthored_cue_offense_refs"
"""cue가 아직 저작되지 않은 죄의 명시적 목록.

Call 1이 라우팅한 죄에 cue가 없으면 Call 1.5가 그 사건에서 예외로 죽는다. 그 구멍을 조용히
두지 않으려면 어딘가에 적혀 있어야 하고, 그 자리가 카탈로그 자신이다 -- 별도 문서에 적으면
카탈로그를 고치는 사람이 그 문서를 보지 않는다.
"""


def load_unauthored_cue_refs(path: Path) -> tuple[str, ...]:
    """저작되지 않았다고 명시된 죄. 목록에 없으면서 cue도 없는 죄는 계약 위반이다."""
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    values = raw.get(UNAUTHORED_CUE_KEY) if isinstance(raw, Mapping) else None
    if values is None:
        return ()
    if not isinstance(values, list) or not all(isinstance(value, str) for value in values):
        raise IssueBindingContractError([f"{path}: {UNAUTHORED_CUE_KEY} must be a ref list"])
    return tuple(values)


def load_binding_seed_cue_catalog(path: Path) -> dict[str, tuple[str, str]]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, Mapping) or not raw:
        raise IssueBindingContractError([f"{path}: cue catalog must be a nonempty mapping"])
    output: dict[str, tuple[str, str]] = {}
    for ref, value in raw.items():
        if ref == UNAUTHORED_CUE_KEY:
            continue
        if (
            not isinstance(ref, str)
            or not isinstance(value, Mapping)
            or set(value) != {"display_name", "minimal_conduct_description"}
            or not all(isinstance(item, str) and item.strip() for item in value.values())
        ):
            raise IssueBindingContractError([f"{path}: malformed cue for {ref!r}"])
        output[ref] = (value["display_name"], value["minimal_conduct_description"])
    return output


def binding_seed_cues(
    registry: DefinitionRegistry,
    seeds: Iterable[str],
    *,
    cue_catalog: Mapping[str, tuple[str, str]],
) -> tuple[BindingSeedCue, ...]:
    output = []
    for index, ref in enumerate(seeds):
        _, statutes = _identity(registry, ref)
        authored = cue_catalog.get(ref)
        if authored is None:
            raise IssueBindingContractError([f"binding seed lacks authored cue: {ref!r}"])
        name, description = authored
        output.append(
            BindingSeedCue(
                index,
                ref,
                name,
                statutes,
                description,
                linked_offender_role(registry, ref),
            )
        )
    return tuple(output)


def issue_binding_request_payload(
    *,
    question_prompt: str,
    case_text: str,
    factual_scope_text: str,
    seed_cues: Iterable[BindingSeedCue],
    verified_candidate_hints: Iterable[Mapping[str, Any]] = (),
) -> dict[str, Any]:
    cues = tuple(seed_cues)
    if (
        not question_prompt.strip()
        or not case_text.strip()
        or not factual_scope_text.strip()
        or not cues
    ):
        raise IssueBindingContractError(
            [
                (
                    "question_prompt, full case_text, source-derived factual_scope_text, "
                    "and seed cues must be non-empty and consistent"
                )
            ]
        )
    payload: dict[str, Any] = {
        "question_prompt": question_prompt,
        "candidate_actor_ids": list(question_actor_ids(question_prompt)),
        "case_text": case_text,
        "factual_scope_text": factual_scope_text,
        "seeds": [value.as_dict() for value in cues],
    }
    hints = tuple(dict(value) for value in verified_candidate_hints)
    if hints:
        payload["verified_factual_candidate_hints"] = list(hints)
    return payload


def issue_binding_schema(*, seed_count: int) -> dict[str, Any]:
    if seed_count <= 0:
        raise IssueBindingContractError(["seed_count must be positive"])
    quote_array = {
        "type": "array",
        "uniqueItems": True,
        "items": {"type": "string", "minLength": 1},
    }
    _nullable_participant = {"type": ["string", "null"], "minLength": 1}
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["factual_episodes", "seed_results"],
        "properties": {
            "factual_episodes": {
                "type": "array",
                "maxItems": MAX_BINDINGS_PER_CASE,
                "uniqueItems": True,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": [
                        "episode_index",
                        "source_quotes",
                        "participants",
                        "actions",
                    ],
                    "properties": {
                        "episode_index": {"type": "integer", "minimum": 0},
                        "source_quotes": {**quote_array, "minItems": 1},
                        "participants": {
                            "type": "array",
                            "minItems": 1,
                            "uniqueItems": True,
                            "items": {"type": "string", "minLength": 1},
                        },
                        "actions": {
                            "type": "array",
                            "minItems": 1,
                            "maxItems": MAX_BINDINGS_PER_CASE,
                            "items": {
                                "type": "object",
                                "additionalProperties": False,
                                "required": [
                                    "action_index",
                                    "source_actor_id",
                                    "participant_ids",
                                    "action_quotes",
                                ],
                                "properties": {
                                    "action_index": {"type": "integer", "minimum": 0},
                                    "source_actor_id": {
                                        "type": "string",
                                        "minLength": 1,
                                    },
                                    "participant_ids": {
                                        "type": "array",
                                        "minItems": 1,
                                        "uniqueItems": True,
                                        "items": {"type": "string", "minLength": 1},
                                    },
                                    "action_quotes": {**quote_array, "minItems": 1},
                                },
                            },
                        },
                    },
                },
            },
            "seed_results": {
                "type": "array",
                "minItems": seed_count,
                "maxItems": seed_count,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["seed_index", "bindings"],
                    "properties": {
                        "seed_index": {
                            "type": "integer",
                            "minimum": 0,
                            "maximum": seed_count - 1,
                        },
                        "bindings": {
                            "type": "array",
                            "maxItems": MAX_BINDINGS_PER_CASE,
                            "uniqueItems": True,
                            "items": {
                                "type": "object",
                                "additionalProperties": False,
                                "required": [
                                    "episode_index",
                                    "actor_id",
                                    "focal_action_index",
                                    "supporting_action_indexes",
                                    "factual_targets",
                                    # Required but nullable: an absent identity must be stated,
                                    # never left out, or a silent omission and a considered "the
                                    # source does not say" become the same wire value.
                                    "directed_action_target",
                                    "actual_result_bearer",
                                    "linked_offender",
                                ],
                                "properties": {
                                    "episode_index": {"type": "integer", "minimum": 0},
                                    "actor_id": {"type": "string", "minLength": 1},
                                    "focal_action_index": {
                                        "type": "integer",
                                        "minimum": 0,
                                    },
                                    "supporting_action_indexes": {
                                        "type": "array",
                                        "uniqueItems": True,
                                        "items": {"type": "integer", "minimum": 0},
                                    },
                                    "factual_targets": {
                                        "type": "array",
                                        "uniqueItems": True,
                                        "items": {"type": "string", "minLength": 1},
                                    },
                                    "directed_action_target": _nullable_participant,
                                    "actual_result_bearer": _nullable_participant,
                                    "linked_offender": _nullable_participant,
                                },
                            },
                        },
                    },
                },
            }
        },
    }


def _fragments(
    *,
    binding_id: str,
    kind: Literal["episode_source", "factual_action", "context"],
    quotes: Any,
    case_text: str,
    errors: list[str],
    where: str,
) -> tuple[BindingFragment, ...]:
    if (
        not isinstance(quotes, list)
        or (kind in {"episode_source", "factual_action"} and not quotes)
        or not all(isinstance(value, str) and value.strip() for value in quotes)
        or len(quotes) != len(set(quotes))
    ):
        errors.append(f"{where} must be a stable unique quote array")
        return ()
    output = []
    for index, quote in enumerate(quotes, 1):
        start = case_text.find(quote)
        if start < 0 or case_text.find(quote, start + 1) >= 0:
            errors.append(f"{where}[{index - 1}] must occur exactly once in case_text")
            continue
        output.append(
            BindingFragment(
                f"{binding_id}:{kind}:{index:03d}",
                kind,
                quote,
                start,
                start + len(quote),
            )
        )
    return tuple(output)


def _is_single_edit(left: str, right: str) -> bool:
    """Return whether two strings differ by exactly one edit."""
    if abs(len(left) - len(right)) > 1 or left == right:
        return False
    if len(left) == len(right):
        return sum(a != b for a, b in zip(left, right, strict=True)) == 1
    shorter, longer = (left, right) if len(left) < len(right) else (right, left)
    mismatch = 0
    for index, value in enumerate(shorter):
        if value != longer[index + mismatch]:
            mismatch += 1
            if mismatch > 1 or value != longer[index + mismatch]:
                return False
    return True


def _unique_single_edit_quote(quote: str, source_text: str) -> str | None:
    if len(quote) < 8 or quote in source_text:
        return None
    candidates: list[tuple[int, str]] = []
    for width in range(max(1, len(quote) - 1), len(quote) + 2):
        for start in range(len(source_text) - width + 1):
            candidate = source_text[start : start + width]
            if (
                candidate[0] == quote[0]
                and candidate[-1] == quote[-1]
                and _is_single_edit(quote, candidate)
            ):
                candidates.append((start, candidate))
                if len(candidates) > 1:
                    return None
    return candidates[0][1] if len(candidates) == 1 else None


def _unique_elided_quote_split(
    quote: str, episode_quotes: Sequence[str]
) -> tuple[str, str] | None:
    """Split an invalid concatenation only when one source gap is unambiguous."""
    if len(quote) < 24:
        return None
    candidates: list[tuple[str, str]] = []
    for episode_quote in episode_quotes:
        for split_at in range(12, len(quote) - 11):
            left, right = quote[:split_at], quote[split_at:]
            left_start = episode_quote.find(left)
            right_start = episode_quote.find(right)
            if (
                left_start >= 0
                and right_start > left_start + len(left)
                and right[0].isalnum()
                and episode_quote.find(left, left_start + 1) < 0
                and episode_quote.find(right, right_start + 1) < 0
            ):
                candidates.append((left, right))
    return candidates[0] if len(candidates) == 1 else None


def normalize_issue_binding_output(
    payload: Mapping[str, Any],
    *,
    case_text: str,
    factual_scope_text: str | None = None,
) -> tuple[dict[str, Any], tuple[dict[str, Any], ...]]:
    """Apply only deterministic source-copy repairs to action-atomic output.

    The host may repair a single source-copy typo or enlarge an episode's quoted
    envelope with an already-authored action quote.  It never invents an action,
    changes an action's temporal boundary, or rewrites a binding reference.
    """
    normalized = deepcopy(dict(payload))
    changes: list[dict[str, Any]] = []
    source = factual_scope_text if factual_scope_text is not None else case_text
    episodes = normalized.get("factual_episodes")
    if not isinstance(episodes, list):
        return normalized, tuple(changes)

    quote_arrays: list[tuple[str, Any]] = []
    for episode_index, episode in enumerate(episodes):
        if not isinstance(episode, dict):
            continue
        quote_arrays.append(
            (f"factual_episodes[{episode_index}].source_quotes", episode.get("source_quotes"))
        )
        actions = episode.get("actions")
        if isinstance(actions, list):
            for action_index, action in enumerate(actions):
                if isinstance(action, dict):
                    quote_arrays.append(
                        (
                            f"factual_episodes[{episode_index}].actions[{action_index}].action_quotes",
                            action.get("action_quotes"),
                        )
                    )
    for location, quotes in quote_arrays:
        if not isinstance(quotes, list):
            continue
        for quote_index, quote in enumerate(quotes):
            if not isinstance(quote, str) or case_text.count(quote) == 1:
                continue
            replacement = _unique_single_edit_quote(quote, source)
            if replacement is None or case_text.count(replacement) != 1:
                continue
            quotes[quote_index] = replacement
            changes.append(
                {
                    "location": f"{location}[{quote_index}]",
                    "reason": "unique_single_edit_source_quote",
                    "original_quote": quote,
                    "normalized_quote": replacement,
                }
            )
    for episode_index, episode in enumerate(episodes):
        if not isinstance(episode, dict):
            continue
        source_quotes = episode.get("source_quotes")
        actions = episode.get("actions")
        if not isinstance(source_quotes, list) or not isinstance(actions, list):
            continue
        action_quotes = [
            quote
            for action in actions
            if isinstance(action, dict)
            for quote in (action.get("action_quotes") or [])
            if isinstance(quote, str) and case_text.count(quote) == 1 and quote in source
        ]
        valid_quotes = [
            quote
            for quote in source_quotes
            if isinstance(quote, str) and case_text.count(quote) == 1 and quote in source
        ]
        if len(valid_quotes) != len(source_quotes) and action_quotes:
            episode["source_quotes"] = list(dict.fromkeys((*valid_quotes, *action_quotes)))
            changes.append(
                {
                    "location": f"factual_episodes[{episode_index}].source_quotes",
                    "reason": "invalid_episode_source_replaced_by_action_quotes",
                }
            )
            source_quotes = episode["source_quotes"]
        for quote in action_quotes:
            if any(quote in str(existing) for existing in source_quotes):
                continue
            source_quotes.append(quote)
            changes.append(
                {
                    "location": f"factual_episodes[{episode_index}].source_quotes",
                    "reason": "action_quote_added_to_declared_episode_scope",
                    "added_quote": quote,
                }
            )
        # An action may name an incidental case actor the model forgot to declare
        # as an episode participant (a rescue crew, a bystander).  The label is
        # already in the case text and the action is already authored, so this
        # only registers a name the model itself used.  It cannot widen the
        # responsibility actors: those are gated separately by candidate scope.
        participants = episode.get("participants")
        if not isinstance(participants, list):
            continue
        for action_index, action in enumerate(actions):
            if not isinstance(action, dict):
                continue
            source_actor_id = action.get("source_actor_id")
            if not isinstance(source_actor_id, str) or source_actor_id not in case_text:
                continue
            if source_actor_id not in participants:
                participants.append(source_actor_id)
                changes.append(
                    {
                        "location": f"factual_episodes[{episode_index}].participants",
                        "reason": "action_source_actor_added_to_episode_participants",
                        "added_participant": source_actor_id,
                    }
                )
            action_participants = action.get("participant_ids")
            if isinstance(action_participants, list) and source_actor_id not in action_participants:
                action_participants.append(source_actor_id)
                changes.append(
                    {
                        "location": (
                            f"factual_episodes[{episode_index}]"
                            f".actions[{action_index}].participant_ids"
                        ),
                        "reason": "action_source_actor_added_to_action_participants",
                        "added_participant": source_actor_id,
                    }
                )
    return normalized, tuple(changes)


def _validate_action_atomic_issue_binding_output(
    payload: Mapping[str, Any],
    *,
    seeds: Iterable[str],
    case_text: str,
    factual_scope_text: str | None = None,
    candidate_actor_ids: Iterable[str] | None = None,
    linked_offender_seed_refs: Iterable[str] = (),
) -> IssueBindingResult:
    """Validate the v2 action-atomic Call 1.5 contract.

    A factual episode is broad narrative context; an action is the only source
    unit a later legal realization may focalize.  This deliberately rejects the
    former binding-only wire format: there is no sound host-side migration from a
    mixed sentence into its temporal factual actions.
    """
    seed_values = tuple(seeds)
    actor_scope = frozenset(candidate_actor_ids or ())
    linked_offender_seeds = frozenset(linked_offender_seed_refs)
    errors: list[str] = []
    if set(payload) != {"factual_episodes", "seed_results"}:
        errors.append("output must contain exactly factual_episodes and seed_results")
    raw_episodes = payload.get("factual_episodes")
    raw_seed_results = payload.get("seed_results")
    if not isinstance(raw_episodes, list) or not isinstance(raw_seed_results, list):
        raise IssueBindingContractError(
            [*errors, "factual_episodes and seed_results must be arrays"]
        )
    if len(raw_episodes) > MAX_BINDINGS_PER_CASE:
        errors.append(f"factual_episodes exceeds {MAX_BINDINGS_PER_CASE}")

    episode_fields = {"episode_index", "source_quotes", "participants", "actions"}
    action_fields = {
        "action_index",
        "source_actor_id",
        "participant_ids",
        "action_quotes",
    }
    episodes: list[FactualEpisode] = []
    episode_by_index: dict[int, FactualEpisode] = {}
    action_by_episode_index: dict[int, dict[int, FactualAction]] = {}
    for episode_index, raw_episode in enumerate(raw_episodes):
        where = f"factual_episodes[{episode_index}]"
        if (
            not isinstance(raw_episode, Mapping)
            or set(raw_episode) != episode_fields
            or raw_episode.get("episode_index") != episode_index
        ):
            errors.append(f"{where} must have canonical episode_index={episode_index}")
            continue
        episode_id = f"factual_episode:{episode_index + 1:03d}"
        fragments = _fragments(
            binding_id=episode_id,
            kind="episode_source",
            quotes=raw_episode.get("source_quotes"),
            case_text=case_text,
            errors=errors,
            where=f"{where}.source_quotes",
        )
        participants = raw_episode.get("participants")
        if (
            not isinstance(participants, list)
            or not participants
            or not all(isinstance(value, str) and value in case_text for value in participants)
            or len(participants) != len(set(participants))
        ):
            errors.append(f"{where}.participants must be unique case participant labels")
            participants = []
        participant_values = tuple(participants)
        if factual_scope_text is not None and any(
            fragment.source_quote not in factual_scope_text for fragment in fragments
        ):
            errors.append(f"{where} source quote is outside the factual scope")
        episode_spans = tuple(
            (value.source_start, value.source_end) for value in fragments
        )
        raw_actions = raw_episode.get("actions")
        if not isinstance(raw_actions, list) or not raw_actions:
            errors.append(f"{where}.actions must be a nonempty array")
            raw_actions = []
        if len(raw_actions) > MAX_BINDINGS_PER_CASE:
            errors.append(f"{where}.actions exceeds {MAX_BINDINGS_PER_CASE}")
        actions: list[FactualAction] = []
        action_by_index: dict[int, FactualAction] = {}
        for action_index, raw_action in enumerate(raw_actions):
            action_where = f"{where}.actions[{action_index}]"
            if (
                not isinstance(raw_action, Mapping)
                or set(raw_action) != action_fields
                or raw_action.get("action_index") != action_index
            ):
                errors.append(
                    f"{action_where} must have canonical action_index={action_index}"
                )
                continue
            source_actor_id = raw_action.get("source_actor_id")
            action_participants = raw_action.get("participant_ids")
            if (
                not isinstance(source_actor_id, str)
                or source_actor_id not in participant_values
            ):
                errors.append(f"{action_where}.source_actor_id must belong to the episode")
                continue
            if (
                not isinstance(action_participants, list)
                or not action_participants
                or not all(value in participant_values for value in action_participants)
                or len(action_participants) != len(set(action_participants))
                or source_actor_id not in action_participants
            ):
                errors.append(
                    f"{action_where}.participant_ids must be unique episode participants "
                    "and include source_actor_id"
                )
                continue
            action_id = f"factual_action:{episode_index + 1:03d}:{action_index + 1:03d}"
            action_fragments = _fragments(
                binding_id=action_id,
                kind="factual_action",
                quotes=raw_action.get("action_quotes"),
                case_text=case_text,
                errors=errors,
                where=f"{action_where}.action_quotes",
            )
            if tuple(value.source_start for value in action_fragments) != tuple(
                sorted(value.source_start for value in action_fragments)
            ):
                errors.append(f"{action_where}.action_quotes must preserve source order")
            for fragment in action_fragments:
                if factual_scope_text is not None and fragment.source_quote not in factual_scope_text:
                    errors.append(f"{action_where} quote is outside the factual scope")
                if not any(
                    start <= fragment.source_start and fragment.source_end <= end
                    for start, end in episode_spans
                ):
                    errors.append(f"{action_where} quote lies outside the referenced episode")
            action = FactualAction(
                action_id,
                episode_id,
                source_actor_id,
                tuple(action_participants),
                action_fragments,
                action_index,
            )
            actions.append(action)
            action_by_index[action_index] = action
        # Action indexes are temporal source order, not arbitrary labels.  Reusing a
        # broad sentence for two actions (or embedding one action's quote inside
        # another's) would put the old mixed-evidence defect back into the wire
        # contract, so reject it before a planner can materialize a realization.
        prior_start: int | None = None
        prior_end: int | None = None
        for action in actions:
            spans = tuple(
                sorted(
                    (fragment.source_start, fragment.source_end)
                    for fragment in action.source_fragments
                )
            )
            if not spans:
                continue
            if any(
                next_start < current_end
                for (_, current_end), (next_start, _) in zip(spans, spans[1:])
            ):
                errors.append(
                    f"{where}.actions[{action.sequence_index}].action_quotes overlap"
                )
            start, end = spans[0][0], spans[-1][1]
            if prior_start is not None and start <= prior_start:
                errors.append(f"{where}.actions must be in source order")
            if prior_end is not None and start < prior_end:
                errors.append(f"{where}.actions must not overlap")
            prior_start, prior_end = start, end
        episode = FactualEpisode(
            episode_id, fragments, participant_values, tuple(actions)
        )
        episodes.append(episode)
        episode_by_index[episode_index] = episode
        action_by_episode_index[episode_index] = action_by_index

    if len(raw_seed_results) != len(seed_values):
        errors.append("seed_results must account for every explicit seed exactly once")
    expected_seed_indexes = list(range(len(seed_values)))
    actual_seed_indexes = [
        value.get("seed_index") if isinstance(value, Mapping) else None
        for value in raw_seed_results
    ]
    if actual_seed_indexes != expected_seed_indexes:
        errors.append("seed_results must be ordered by every canonical seed_index")
    binding_fields = {
        "episode_index",
        "actor_id",
        "focal_action_index",
        "supporting_action_indexes",
        "factual_targets",
        "directed_action_target",
        "actual_result_bearer",
        "linked_offender",
    }
    seen: set[tuple[int, int, str, int, tuple[int, ...]]] = set()
    seed_results: list[SeedBindingResult] = []
    binding_number = 0
    for result_index, raw_result in enumerate(raw_seed_results):
        result_where = f"seed_results[{result_index}]"
        if (
            not isinstance(raw_result, Mapping)
            or set(raw_result) != {"seed_index", "bindings"}
        ):
            errors.append(f"{result_where} must contain exactly seed_index and bindings")
            continue
        seed_index = raw_result.get("seed_index")
        if (
            not isinstance(seed_index, int)
            or isinstance(seed_index, bool)
            or not 0 <= seed_index < len(seed_values)
        ):
            errors.append(f"{result_where}.seed_index is outside the frozen seed list")
            continue
        raw_bindings = raw_result.get("bindings")
        if not isinstance(raw_bindings, list):
            errors.append(f"{result_where}.bindings must be an array")
            continue
        bindings: list[IssueBinding] = []
        for local_index, raw_binding in enumerate(raw_bindings):
            where = f"{result_where}.bindings[{local_index}]"
            if not isinstance(raw_binding, Mapping) or set(raw_binding) != binding_fields:
                errors.append(f"{where} must contain exactly {sorted(binding_fields)}")
                continue
            episode_index = raw_binding.get("episode_index")
            episode = episode_by_index.get(episode_index)
            actions = action_by_episode_index.get(episode_index, {})
            if episode is None:
                errors.append(f"{where}.episode_index does not resolve uniquely")
                continue
            actor_id = raw_binding.get("actor_id")
            if not isinstance(actor_id, str) or actor_id not in episode.participants:
                errors.append(f"{where}.actor_id must belong to the referenced episode")
                continue
            if actor_scope and actor_id not in actor_scope:
                errors.append(f"{where}.actor_id is outside the requested responsibility actors")
                continue
            focal_index = raw_binding.get("focal_action_index")
            focal_action = actions.get(focal_index)
            if focal_action is None:
                errors.append(f"{where}.focal_action_index does not resolve uniquely")
                continue
            supports = raw_binding.get("supporting_action_indexes")
            if (
                not isinstance(supports, list)
                or not all(isinstance(value, int) and not isinstance(value, bool) for value in supports)
                or len(supports) != len(set(supports))
                or supports != sorted(supports)
                or focal_index in supports
                or any(value not in actions for value in supports)
            ):
                errors.append(
                    f"{where}.supporting_action_indexes must be unique same-episode "
                    "actions distinct from focal_action_index"
                )
                continue
            # The responsibility actor need not perform the focal action.  A
            # participant, an accessory, or an instigator is bound to the
            # principal's execution action while its own contribution sits in the
            # supporting actions.  Requiring focal participation would make every
            # such binding unrepresentable, so the actor only has to appear
            # somewhere in the evidence this realization actually carries.
            carried_participants = set(focal_action.participant_ids)
            for value in supports:
                carried_participants.update(actions[value].participant_ids)
            if actor_id not in carried_participants:
                errors.append(
                    f"{where}.actor_id must participate in its focal or supporting factual actions"
                )
                continue
            targets = raw_binding.get("factual_targets")
            if (
                not isinstance(targets, list)
                or not all(isinstance(value, str) for value in targets)
                or len(targets) != len(set(targets))
                or any(value not in episode.participants for value in targets)
            ):
                errors.append(f"{where}.factual_targets must be episode participants")
                continue
            # The narrow identities are scoped to the evidence this binding actually carries, not
            # to the episode.  An episode is broad narrative context, so an episode-wide check
            # would let a person from an unrelated part of the story be named as the target this
            # very action was aimed at.
            identity_errors: list[str] = []
            narrow_identities: dict[str, str | None] = {}
            for field in ("directed_action_target", "actual_result_bearer", "linked_offender"):
                value = raw_binding.get(field)
                if value is None:
                    narrow_identities[field] = None
                    continue
                if not isinstance(value, str) or value not in carried_participants:
                    identity_errors.append(
                        f"{where}.{field} must be a participant of its focal or supporting "
                        "factual actions, or null"
                    )
                    continue
                narrow_identities[field] = value
            if (
                narrow_identities.get("linked_offender") is not None
                and seed_values[seed_index] not in linked_offender_seeds
            ):
                identity_errors.append(
                    f"{where}.linked_offender is set on a seed the host did not mark as "
                    "presupposing another person's offense"
                )
            if identity_errors:
                errors.extend(identity_errors)
                continue
            identity = (seed_index, episode_index, actor_id, focal_index, tuple(supports))
            if identity in seen:
                errors.append(f"{where} duplicates an earlier binding")
                continue
            seen.add(identity)
            binding_number += 1
            bindings.append(
                IssueBinding(
                    f"binding:{binding_number:03d}",
                    episode.factual_episode_id,
                    seed_index,
                    seed_values[seed_index],
                    actor_id,
                    focal_action.factual_action_id,
                    tuple(actions[value].factual_action_id for value in supports),
                    tuple(targets),
                    narrow_identities["directed_action_target"],
                    narrow_identities["actual_result_bearer"],
                    narrow_identities["linked_offender"],
                )
            )
        seed_results.append(
            SeedBindingResult(seed_index, seed_values[seed_index], tuple(bindings))
        )
    if errors:
        raise IssueBindingContractError(errors)
    return IssueBindingResult(tuple(episodes), tuple(seed_results))


def validate_issue_binding_output(
    payload: Mapping[str, Any],
    *,
    seeds: Iterable[str],
    case_text: str,
    factual_scope_text: str | None = None,
    candidate_actor_ids: Iterable[str] | None = None,
    linked_offender_seed_refs: Iterable[str] = (),
) -> IssueBindingResult:
    return _validate_action_atomic_issue_binding_output(
        payload,
        seeds=seeds,
        case_text=case_text,
        factual_scope_text=factual_scope_text,
        candidate_actor_ids=candidate_actor_ids,
        linked_offender_seed_refs=linked_offender_seed_refs,
    )


def _parse_action_atomic_issue_binding_result(
    payload: Mapping[str, Any],
    *,
    seeds: Iterable[str],
    case_text: str,
    candidate_actor_ids: Iterable[str] | None = None,
    linked_offender_seed_refs: Iterable[str] | None = None,
) -> IssueBindingResult:
    if set(payload) != {"factual_episodes", "seed_results"}:
        raise IssueBindingContractError(["persisted result has unexpected fields"])
    raw_episodes_value = payload.get("factual_episodes")
    raw_results_value = payload.get("seed_results")
    if not isinstance(raw_episodes_value, list) or not isinstance(raw_results_value, list):
        raise IssueBindingContractError(["persisted result must contain episode/result arrays"])
    raw_episodes: list[dict[str, Any]] = []
    action_index_by_id: dict[str, tuple[int, int]] = {}
    episode_index_by_id: dict[str, int] = {}
    for episode_index, episode in enumerate(raw_episodes_value):
        if not isinstance(episode, Mapping):
            raise IssueBindingContractError([f"factual_episodes[{episode_index}] is malformed"])
        episode_id = f"factual_episode:{episode_index + 1:03d}"
        if episode.get("factual_episode_id") != episode_id:
            raise IssueBindingContractError(["persisted episode has noncanonical identity"])
        raw_actions = episode.get("factual_actions")
        if not isinstance(raw_actions, list):
            raise IssueBindingContractError(
                [
                    "persisted result predates action-atomic Call 1.5; "
                    "re-run Call 1.5 instead of migrating mixed bindings"
                ]
            )
        actions: list[dict[str, Any]] = []
        for action_index, action in enumerate(raw_actions):
            if not isinstance(action, Mapping):
                raise IssueBindingContractError(["persisted factual action is malformed"])
            action_id = f"factual_action:{episode_index + 1:03d}:{action_index + 1:03d}"
            if (
                action.get("factual_action_id") != action_id
                or action.get("factual_episode_id") != episode_id
                or action.get("sequence_index") != action_index
            ):
                raise IssueBindingContractError(["persisted factual action has broken lineage"])
            action_index_by_id[action_id] = (episode_index, action_index)
            actions.append(
                {
                    "action_index": action_index,
                    "source_actor_id": action.get("source_actor_id"),
                    "participant_ids": action.get("participant_ids"),
                    "action_quotes": [
                        item.get("source_quote")
                        for item in action.get("source_fragments", [])
                        if isinstance(item, Mapping)
                    ],
                }
            )
        episode_index_by_id[episode_id] = episode_index
        raw_episodes.append(
            {
                "episode_index": episode_index,
                "source_quotes": [
                    item.get("source_quote")
                    for item in episode.get("source_fragments", [])
                    if isinstance(item, Mapping)
                ],
                "participants": episode.get("participants"),
                "actions": actions,
            }
        )
    seed_values = tuple(seeds)
    raw_results: list[dict[str, Any]] = []
    binding_number = 0
    for seed_index, result in enumerate(raw_results_value):
        if not isinstance(result, Mapping):
            raise IssueBindingContractError([f"seed_results[{seed_index}] is malformed"])
        if (
            seed_index >= len(seed_values)
            or result.get("seed_index") != seed_index
            or result.get("offense_ref") != seed_values[seed_index]
        ):
            raise IssueBindingContractError([f"seed_results[{seed_index}] has broken lineage"])
        bindings: list[dict[str, Any]] = []
        raw_bindings = result.get("bindings")
        if not isinstance(raw_bindings, list):
            raise IssueBindingContractError([f"seed_results[{seed_index}].bindings is malformed"])
        for binding in raw_bindings:
            if not isinstance(binding, Mapping):
                raise IssueBindingContractError(["persisted binding is malformed"])
            binding_number += 1
            if binding.get("binding_id") != f"binding:{binding_number:03d}":
                raise IssueBindingContractError(["persisted binding has noncanonical identity"])
            episode_id = binding.get("factual_episode_id")
            episode_index = episode_index_by_id.get(str(episode_id))
            focal_id = binding.get("focal_action_id")
            focal = action_index_by_id.get(str(focal_id))
            supports = binding.get("supporting_action_ids")
            if (
                episode_index is None
                or focal is None
                or focal[0] != episode_index
                or not isinstance(supports, list)
            ):
                raise IssueBindingContractError(["binding has dangling factual action identity"])
            support_indexes: list[int] = []
            for action_id in supports:
                action = action_index_by_id.get(str(action_id))
                if action is None or action[0] != episode_index:
                    raise IssueBindingContractError(
                        ["binding support has dangling factual action identity"]
                    )
                support_indexes.append(action[1])
            bindings.append(
                {
                    "episode_index": episode_index,
                    "actor_id": binding.get("actor_id"),
                    "focal_action_index": focal[1],
                    "supporting_action_indexes": support_indexes,
                    "factual_targets": binding.get("factual_targets"),
                    "directed_action_target": binding.get("directed_action_target"),
                    "actual_result_bearer": binding.get("actual_result_bearer"),
                    "linked_offender": binding.get("linked_offender"),
                }
            )
        raw_results.append({"seed_index": seed_index, "bindings": bindings})
    if len(raw_results) != len(seed_values):
        raise IssueBindingContractError(["persisted seed results do not match frozen seeds"])
    return _validate_action_atomic_issue_binding_output(
        {"factual_episodes": raw_episodes, "seed_results": raw_results},
        seeds=seed_values,
        case_text=case_text,
        candidate_actor_ids=candidate_actor_ids,
        linked_offender_seed_refs=(
            seed_values if linked_offender_seed_refs is None else linked_offender_seed_refs
        ),
    )


def parse_issue_binding_result(
    payload: Mapping[str, Any],
    *,
    seeds: Iterable[str],
    case_text: str,
    candidate_actor_ids: Iterable[str] | None = None,
    linked_offender_seed_refs: Iterable[str] | None = None,
) -> IssueBindingResult:
    """Revalidate a host-enriched persisted Call 1.5 artifact.

    `linked_offender_seed_refs=None` means "trust the gate that ran when this artifact was
    created".  That gate belongs at the wire boundary, where a model answer is first accepted;
    re-deriving it here would make every downstream reader carry a registry just to re-decide a
    question already decided.  A caller that does hold a registry may pass the refs to enforce it
    again, and the planner does exactly that.
    """
    seed_values = tuple(seeds)
    return _parse_action_atomic_issue_binding_result(
        payload,
        seeds=seed_values,
        case_text=case_text,
        candidate_actor_ids=candidate_actor_ids,
        linked_offender_seed_refs=(
            seed_values if linked_offender_seed_refs is None else linked_offender_seed_refs
        ),
    )


__all__ = [
    "MAX_BINDINGS_PER_CASE",
    "BindingFragment",
    "BindingSeedCue",
    "FactualAction",
    "FactualEpisode",
    "IssueBinding",
    "IssueBindingContractError",
    "IssueBindingResult",
    "SeedBindingResult",
    "binding_seed_cues",
    "issue_binding_request_payload",
    "linked_offender_role",
    "linked_offender_seed_refs",
    "issue_binding_schema",
    "UNAUTHORED_CUE_KEY",
    "load_binding_seed_cue_catalog",
    "load_unauthored_cue_refs",
    "normalize_issue_binding_output",
    "parse_issue_binding_result",
    "question_actor_ids",
    "validate_issue_binding_output",
]
