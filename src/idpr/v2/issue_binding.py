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

    def as_dict(self) -> dict[str, Any]:
        return {
            "seed_index": self.seed_index,
            "offense_ref": self.offense_ref,
            "display_name": self.display_name,
            "statutory_refs": list(self.statutory_refs),
            "minimal_conduct_description": self.minimal_conduct_description,
        }


@dataclass(frozen=True)
class BindingFragment:
    fragment_id: str
    fragment_kind: Literal["episode_source", "actor_action", "context"]
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
class FactualEpisode:
    factual_episode_id: str
    source_fragments: tuple[BindingFragment, ...]
    participants: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "factual_episode_id": self.factual_episode_id,
            "source_fragments": [value.as_dict() for value in self.source_fragments],
            "participants": list(self.participants),
        }


@dataclass(frozen=True)
class IssueBinding:
    """One candidate factual episode, not an established legal realization."""

    binding_id: str
    factual_episode_id: str
    seed_index: int
    offense_ref: str
    actor_id: str
    actor_action_fragments: tuple[BindingFragment, ...]
    context_fragments: tuple[BindingFragment, ...]
    factual_targets: tuple[str, ...]

    @property
    def evidence_text(self) -> str:
        return "\n".join(
            value.source_quote
            for value in (*self.actor_action_fragments, *self.context_fragments)
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "binding_id": self.binding_id,
            "factual_episode_id": self.factual_episode_id,
            "seed_index": self.seed_index,
            "offense_ref": self.offense_ref,
            "actor_id": self.actor_id,
            "actor_action_fragments": [value.as_dict() for value in self.actor_action_fragments],
            "context_fragments": [value.as_dict() for value in self.context_fragments],
            "factual_targets": list(self.factual_targets),
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


def load_binding_seed_cue_catalog(path: Path) -> dict[str, tuple[str, str]]:
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, Mapping) or not raw:
        raise IssueBindingContractError([f"{path}: cue catalog must be a nonempty mapping"])
    output: dict[str, tuple[str, str]] = {}
    for ref, value in raw.items():
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
            )
        )
    return tuple(output)


def issue_binding_request_payload(
    *,
    question_prompt: str,
    case_text: str,
    factual_scope_text: str,
    seed_cues: Iterable[BindingSeedCue],
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
    return {
        "question_prompt": question_prompt,
        "candidate_actor_ids": list(question_actor_ids(question_prompt)),
        "case_text": case_text,
        "factual_scope_text": factual_scope_text,
        "seeds": [value.as_dict() for value in cues],
    }


def issue_binding_schema(*, seed_count: int) -> dict[str, Any]:
    if seed_count <= 0:
        raise IssueBindingContractError(["seed_count must be positive"])
    quote_array = {
        "type": "array",
        "uniqueItems": True,
        "items": {"type": "string", "minLength": 1},
    }
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
                    "required": ["episode_index", "source_quotes", "participants"],
                    "properties": {
                        "episode_index": {"type": "integer", "minimum": 0},
                        "source_quotes": {**quote_array, "minItems": 1},
                        "participants": {
                            "type": "array",
                            "minItems": 1,
                            "uniqueItems": True,
                            "items": {"type": "string", "minLength": 1},
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
                                    "actor_action_quotes",
                                    "context_quotes",
                                    "factual_targets",
                                ],
                                "properties": {
                                    "episode_index": {"type": "integer", "minimum": 0},
                                    "actor_id": {"type": "string", "minLength": 1},
                                    "actor_action_quotes": {
                                        **quote_array,
                                        "minItems": 1,
                                    },
                                    "context_quotes": quote_array,
                                    "factual_targets": {
                                        "type": "array",
                                        "uniqueItems": True,
                                        "items": {"type": "string", "minLength": 1},
                                    },
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
    kind: Literal["episode_source", "actor_action", "context"],
    quotes: Any,
    case_text: str,
    errors: list[str],
    where: str,
) -> tuple[BindingFragment, ...]:
    if (
        not isinstance(quotes, list)
        or (kind in {"episode_source", "actor_action"} and not quotes)
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
    """Apply only deterministic source-copy and episode-scope repairs.

    Semantic fields, actors, targets, seed assignments, and episode identities are
    never inferred or changed here. Anything outside these bounded rules remains a
    contract failure in ``validate_issue_binding_output``.
    """
    normalized = deepcopy(dict(payload))
    changes: list[dict[str, Any]] = []
    source = factual_scope_text if factual_scope_text is not None else case_text

    quote_arrays: list[tuple[str, Any]] = []
    episodes = normalized.get("factual_episodes")
    if isinstance(episodes, list):
        for episode_index, episode in enumerate(episodes):
            if isinstance(episode, dict):
                quote_arrays.append(
                    (f"factual_episodes[{episode_index}].source_quotes", episode.get("source_quotes"))
                )
    seed_results = normalized.get("seed_results")
    if isinstance(seed_results, list):
        for result_index, result in enumerate(seed_results):
            bindings = result.get("bindings") if isinstance(result, dict) else None
            if not isinstance(bindings, list):
                continue
            for binding_index, binding in enumerate(bindings):
                if not isinstance(binding, dict):
                    continue
                for field in ("actor_action_quotes", "context_quotes"):
                    quote_arrays.append(
                        (
                            f"seed_results[{result_index}].bindings[{binding_index}].{field}",
                            binding.get(field),
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

    if isinstance(episodes, list) and isinstance(seed_results, list):
        binding_quotes_by_episode: dict[int, list[str]] = {}
        for result in seed_results:
            bindings = result.get("bindings") if isinstance(result, dict) else None
            if not isinstance(bindings, list):
                continue
            for binding in bindings:
                if not isinstance(binding, dict):
                    continue
                episode_index = binding.get("episode_index")
                if not isinstance(episode_index, int) or isinstance(episode_index, bool):
                    continue
                values = binding_quotes_by_episode.setdefault(episode_index, [])
                for field in ("actor_action_quotes", "context_quotes"):
                    quotes = binding.get(field)
                    if not isinstance(quotes, list):
                        continue
                    for quote in quotes:
                        if (
                            isinstance(quote, str)
                            and case_text.count(quote) == 1
                            and quote in source
                            and quote not in values
                        ):
                            values.append(quote)

        for episode_index, episode in enumerate(episodes):
            if not isinstance(episode, dict):
                continue
            source_quotes = episode.get("source_quotes")
            if not isinstance(source_quotes, list):
                continue
            invalid = [
                quote
                for quote in source_quotes
                if not isinstance(quote, str)
                or case_text.count(quote) != 1
                or quote not in source
            ]
            replacements = binding_quotes_by_episode.get(episode_index, [])
            if not invalid or not replacements:
                continue
            episode["source_quotes"] = list(
                dict.fromkeys(
                    [
                        quote
                        for quote in source_quotes
                        if isinstance(quote, str)
                        and case_text.count(quote) == 1
                        and quote in source
                    ]
                    + replacements
                )
            )
            changes.append(
                {
                    "location": f"factual_episodes[{episode_index}].source_quotes",
                    "reason": "invalid_episode_source_replaced_by_binding_quotes",
                    "removed_quotes": invalid,
                    "replacement_quotes": replacements,
                }
            )

    if isinstance(episodes, list) and isinstance(seed_results, list):
        for result_index, result in enumerate(seed_results):
            bindings = result.get("bindings") if isinstance(result, dict) else None
            if not isinstance(bindings, list):
                continue
            for binding_index, binding in enumerate(bindings):
                if not isinstance(binding, dict):
                    continue
                episode_index = binding.get("episode_index")
                if (
                    not isinstance(episode_index, int)
                    or isinstance(episode_index, bool)
                    or not 0 <= episode_index < len(episodes)
                    or not isinstance(episodes[episode_index], dict)
                ):
                    continue
                source_quotes = episodes[episode_index].get("source_quotes")
                if not isinstance(source_quotes, list):
                    continue
                context_quotes = binding.get("context_quotes")
                if isinstance(context_quotes, list):
                    for quote_index, quote in tuple(enumerate(context_quotes)):
                        if not isinstance(quote, str) or case_text.count(quote) == 1:
                            continue
                        split = _unique_elided_quote_split(
                            quote,
                            tuple(
                                value for value in source_quotes if isinstance(value, str)
                            ),
                        )
                        if split is None or any(case_text.count(value) != 1 for value in split):
                            continue
                        context_quotes[quote_index : quote_index + 1] = list(split)
                        changes.append(
                            {
                                "location": (
                                    f"seed_results[{result_index}].bindings[{binding_index}]"
                                    f".context_quotes[{quote_index}]"
                                ),
                                "reason": "unique_single_elision_split",
                                "original_quote": quote,
                                "normalized_quotes": list(split),
                            }
                        )
                binding_quotes: list[str] = []
                for field in ("actor_action_quotes", "context_quotes"):
                    quotes = binding.get(field)
                    if isinstance(quotes, list):
                        binding_quotes.extend(
                            quote for quote in quotes if isinstance(quote, str)
                        )
                for quote in binding_quotes:
                    if case_text.count(quote) != 1 or any(
                        quote in episode_quote
                        for episode_quote in source_quotes
                        if isinstance(episode_quote, str)
                    ):
                        continue
                    source_quotes.append(quote)
                    changes.append(
                        {
                            "location": (
                                f"seed_results[{result_index}].bindings[{binding_index}]"
                                ".episode_index"
                            ),
                            "reason": "binding_quote_added_to_declared_episode_scope",
                            "episode_index": episode_index,
                            "added_quote": quote,
                        }
                    )

    return normalized, tuple(changes)


def validate_issue_binding_output(
    payload: Mapping[str, Any],
    *,
    seeds: Iterable[str],
    case_text: str,
    factual_scope_text: str | None = None,
    candidate_actor_ids: Iterable[str] | None = None,
) -> IssueBindingResult:
    seed_values = tuple(seeds)
    actor_scope = frozenset(candidate_actor_ids or ())
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
    episodes: list[FactualEpisode] = []
    episode_by_index: dict[int, FactualEpisode] = {}
    for index, raw_episode in enumerate(raw_episodes):
        where = f"factual_episodes[{index}]"
        if (
            not isinstance(raw_episode, Mapping)
            or set(raw_episode) != {"episode_index", "source_quotes", "participants"}
            or raw_episode.get("episode_index") != index
        ):
            errors.append(f"{where} must have canonical episode_index={index}")
            continue
        episode_id = f"factual_episode:{index + 1:03d}"
        fragments = _fragments(
            binding_id=episode_id,
            kind="episode_source",
            quotes=raw_episode["source_quotes"],
            case_text=case_text,
            errors=errors,
            where=f"{where}.source_quotes",
        )
        participants = raw_episode["participants"]
        if (
            not isinstance(participants, list)
            or not participants
            or not all(isinstance(value, str) and value in case_text for value in participants)
            or len(participants) != len(set(participants))
        ):
            errors.append(f"{where}.participants must be unique case participant labels")
            participants = []
        if factual_scope_text is not None and any(
            fragment.source_quote not in factual_scope_text for fragment in fragments
        ):
            errors.append(f"{where} source quote is outside the factual scope")
        episode = FactualEpisode(episode_id, fragments, tuple(participants))
        episodes.append(episode)
        episode_by_index[index] = episode

    if len(raw_seed_results) != len(seed_values):
        errors.append("seed_results must account for every explicit seed exactly once")
    expected_seed_indexes = list(range(len(seed_values)))
    actual_seed_indexes = [
        value.get("seed_index") if isinstance(value, Mapping) else None
        for value in raw_seed_results
    ]
    if actual_seed_indexes != expected_seed_indexes:
        errors.append("seed_results must be ordered by every canonical seed_index")
    expected_binding = {
        "episode_index",
        "actor_id",
        "actor_action_quotes",
        "context_quotes",
        "factual_targets",
    }
    seen: set[tuple[int, int, str, tuple[str, ...], tuple[str, ...]]] = set()
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
        seed_index = raw_result["seed_index"]
        if (
            not isinstance(seed_index, int)
            or isinstance(seed_index, bool)
            or not 0 <= seed_index < len(seed_values)
        ):
            errors.append(f"{result_where}.seed_index is outside the frozen seed list")
            continue
        raw_bindings = raw_result["bindings"]
        if not isinstance(raw_bindings, list):
            errors.append(f"{result_where}.bindings must be an array")
            continue
        bindings: list[IssueBinding] = []
        for local_index, raw in enumerate(raw_bindings):
            where = f"{result_where}.bindings[{local_index}]"
            if not isinstance(raw, Mapping) or set(raw) != expected_binding:
                errors.append(f"{where} must contain exactly {sorted(expected_binding)}")
                continue
            episode_index = raw["episode_index"]
            episode = episode_by_index.get(episode_index)
            if episode is None:
                errors.append(f"{where}.episode_index does not resolve uniquely")
                continue
            actor_id = raw["actor_id"]
            if not isinstance(actor_id, str) or actor_id not in episode.participants:
                errors.append(f"{where}.actor_id must belong to the referenced episode")
                continue
            if actor_scope and actor_id not in actor_scope:
                errors.append(f"{where}.actor_id is outside the requested responsibility actors")
                continue
            binding_number += 1
            binding_id = f"binding:{binding_number:03d}"
            actions = _fragments(
                binding_id=binding_id,
                kind="actor_action",
                quotes=raw["actor_action_quotes"],
                case_text=case_text,
                errors=errors,
                where=f"{where}.actor_action_quotes",
            )
            contexts = _fragments(
                binding_id=binding_id,
                kind="context",
                quotes=raw["context_quotes"],
                case_text=case_text,
                errors=errors,
                where=f"{where}.context_quotes",
            )
            episode_spans = tuple(
                (value.source_start, value.source_end)
                for value in episode.source_fragments
            )
            for fragment in (*actions, *contexts):
                if factual_scope_text is not None and fragment.source_quote not in factual_scope_text:
                    errors.append(f"{where} quote is outside the factual scope")
                if not any(
                    start <= fragment.source_start and fragment.source_end <= end
                    for start, end in episode_spans
                ):
                    errors.append(f"{where} quote lies outside the referenced episode")
            targets = raw["factual_targets"]
            if (
                not isinstance(targets, list)
                or not all(isinstance(value, str) for value in targets)
                or len(targets) != len(set(targets))
                or any(value not in episode.participants for value in targets)
            ):
                errors.append(f"{where}.factual_targets must be episode participants")
                targets = []
            identity = (
                seed_index,
                episode_index,
                actor_id,
                tuple(value.source_quote for value in actions),
                tuple(value.source_quote for value in contexts),
            )
            if identity in seen:
                errors.append(f"{where} duplicates an earlier binding")
                continue
            seen.add(identity)
            bindings.append(
                IssueBinding(
                    binding_id,
                    episode.factual_episode_id,
                    seed_index,
                    seed_values[seed_index],
                    actor_id,
                    actions,
                    contexts,
                    tuple(targets),
                )
            )
        seed_results.append(
            SeedBindingResult(seed_index, seed_values[seed_index], tuple(bindings))
        )
    if errors:
        raise IssueBindingContractError(errors)
    return IssueBindingResult(tuple(episodes), tuple(seed_results))


def parse_issue_binding_result(
    payload: Mapping[str, Any],
    *,
    seeds: Iterable[str],
    case_text: str,
    candidate_actor_ids: Iterable[str] | None = None,
) -> IssueBindingResult:
    """Revalidate a host-enriched persisted Call 1.5 artifact."""
    if set(payload) != {"factual_episodes", "seed_results"}:
        raise IssueBindingContractError(["persisted result has unexpected fields"])
    seed_values = tuple(seeds)
    raw_episodes = []
    for index, value in enumerate(payload["factual_episodes"]):
        raw_episodes.append(
            {
                "episode_index": index,
                "source_quotes": [
                    item.get("source_quote") for item in value.get("source_fragments", [])
                ],
                "participants": value.get("participants"),
            }
        )
    raw_results = []
    binding_number = 0
    for index, value in enumerate(payload["seed_results"]):
        if value.get("seed_index") != index or value.get("offense_ref") != seed_values[index]:
            raise IssueBindingContractError([f"seed_results[{index}] has broken lineage"])
        bindings = []
        for binding in value.get("bindings", []):
            binding_number += 1
            if binding.get("binding_id") != f"binding:{binding_number:03d}":
                raise IssueBindingContractError(["persisted binding has noncanonical identity"])
            episode_id = binding.get("factual_episode_id")
            try:
                episode_index = next(
                    episode_index
                    for episode_index, episode in enumerate(payload["factual_episodes"])
                    if episode.get("factual_episode_id") == episode_id
                )
            except StopIteration as exc:
                raise IssueBindingContractError(
                    ["binding has dangling episode identity"]
                ) from exc
            bindings.append(
                {
                    "episode_index": episode_index,
                    "actor_id": binding.get("actor_id"),
                    "actor_action_quotes": [
                        item.get("source_quote")
                        for item in binding.get("actor_action_fragments", [])
                    ],
                    "context_quotes": [
                        item.get("source_quote")
                        for item in binding.get("context_fragments", [])
                    ],
                    "factual_targets": binding.get("factual_targets"),
                }
            )
        raw_results.append({"seed_index": index, "bindings": bindings})
    return validate_issue_binding_output(
        {"factual_episodes": raw_episodes, "seed_results": raw_results},
        seeds=seed_values,
        case_text=case_text,
        candidate_actor_ids=candidate_actor_ids,
    )


__all__ = [
    "MAX_BINDINGS_PER_CASE",
    "BindingFragment",
    "BindingSeedCue",
    "FactualEpisode",
    "IssueBinding",
    "IssueBindingContractError",
    "IssueBindingResult",
    "SeedBindingResult",
    "binding_seed_cues",
    "issue_binding_request_payload",
    "issue_binding_schema",
    "load_binding_seed_cue_catalog",
    "normalize_issue_binding_output",
    "parse_issue_binding_result",
    "question_actor_ids",
    "validate_issue_binding_output",
]
