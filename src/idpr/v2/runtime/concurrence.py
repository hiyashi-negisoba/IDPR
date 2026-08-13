"""Occurrence-aware concurrence and absorption boundary for v2.

The legacy rulebase keys concurrence by case and Criminal Act article.  V2 cannot reuse
that identity: one article can contain multiple offenses, and one actor can realize the
same offense more than once.  This module therefore accepts only authored rules over
exact DefinitionRefs and joins them to :class:`OffenseInstanceKey` values.

Planning and resolution are separate.  A rule plus two established instances opens a
candidate; only a separately assessed TRUE condition applies its effect.  FALSE leaves
both offenses untouched and UNKNOWN is preserved as unresolved.  The host never repairs
or guesses the condition from card text.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Mapping
from dataclasses import dataclass

from idpr.v2.evaluate import FALSE, TRUE, UNKNOWN, TruthValue
from idpr.v2.runtime.identity import OffenseInstanceKey

ABSORPTION = "absorption"
IMAGINATIVE_CONCURRENCE = "imaginative_concurrence"
SAME_EPISODE = "same_episode"


@dataclass(frozen=True, slots=True)
class ConcurrenceRule:
    rule_id: str
    kind: str
    first_offense_ref: str
    second_offense_ref: str
    condition_ref: str
    occurrence_constraint: str = SAME_EPISODE
    source_card_ids: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.kind not in {ABSORPTION, IMAGINATIVE_CONCURRENCE}:
            raise ValueError(f"unsupported concurrence kind: {self.kind!r}")
        if self.occurrence_constraint != SAME_EPISODE:
            raise ValueError(
                "v2 concurrence currently requires occurrence_constraint=same_episode"
            )
        if self.first_offense_ref == self.second_offense_ref:
            raise ValueError("same-offense multiplicity needs a separately authored rule")
        if not self.rule_id or not self.condition_ref:
            raise ValueError("concurrence rule requires rule_id and condition_ref")


@dataclass(frozen=True, slots=True)
class ConcurrenceCandidate:
    rule: ConcurrenceRule
    first: OffenseInstanceKey
    second: OffenseInstanceKey
    factual_episode_id: str


@dataclass(frozen=True, slots=True)
class ConcurrenceResolution:
    retained_instances: frozenset[OffenseInstanceKey]
    absorbed_instances: frozenset[OffenseInstanceKey]
    imaginative_pairs: tuple[tuple[OffenseInstanceKey, OffenseInstanceKey], ...]
    unresolved_candidates: tuple[ConcurrenceCandidate, ...]
    rejected_conflicts: tuple[ConcurrenceCandidate, ...]


def plan_concurrence_candidates(
    established_instances: Iterable[OffenseInstanceKey],
    *,
    episode_by_instance: Mapping[OffenseInstanceKey, str],
    rules: Iterable[ConcurrenceRule],
) -> tuple[ConcurrenceCandidate, ...]:
    """Join exact authored offense pairs only inside one factual episode."""
    established = tuple(dict.fromkeys(established_instances))
    missing = set(established) - set(episode_by_instance)
    if missing:
        raise ValueError(f"established instances lack factual episode ids: {sorted(missing, key=repr)}")
    by_case_ref: dict[tuple[str, str], list[OffenseInstanceKey]] = {}
    for instance in established:
        by_case_ref.setdefault((instance.case_id, instance.offense_ref), []).append(instance)

    output: list[ConcurrenceCandidate] = []
    for rule in rules:
        case_ids = {
            case_id
            for case_id, ref in by_case_ref
            if ref in {rule.first_offense_ref, rule.second_offense_ref}
        }
        for case_id in sorted(case_ids):
            first_values = by_case_ref.get((case_id, rule.first_offense_ref), ())
            second_values = by_case_ref.get((case_id, rule.second_offense_ref), ())
            for first in first_values:
                for second in second_values:
                    first_episode = episode_by_instance[first]
                    if first_episode != episode_by_instance[second]:
                        continue
                    output.append(
                        ConcurrenceCandidate(rule, first, second, first_episode)
                    )
    return tuple(output)


def resolve_concurrence(
    established_instances: Iterable[OffenseInstanceKey],
    candidates: Iterable[ConcurrenceCandidate],
    *,
    condition_truths: Mapping[tuple[str, OffenseInstanceKey, OffenseInstanceKey], TruthValue],
) -> ConcurrenceResolution:
    """Apply only unconflicted TRUE effects; preserve UNKNOWN and conflicts."""
    established = frozenset(established_instances)
    candidate_values = tuple(candidates)
    unresolved: list[ConcurrenceCandidate] = []
    true_absorptions: list[ConcurrenceCandidate] = []
    imaginative: list[tuple[OffenseInstanceKey, OffenseInstanceKey]] = []
    for candidate in candidate_values:
        if candidate.first not in established or candidate.second not in established:
            raise ValueError("concurrence candidate refers to a non-established instance")
        key = (candidate.rule.rule_id, candidate.first, candidate.second)
        truth = condition_truths.get(key, UNKNOWN)
        if truth == UNKNOWN:
            unresolved.append(candidate)
        elif truth == FALSE:
            continue
        elif truth == TRUE and candidate.rule.kind == ABSORPTION:
            true_absorptions.append(candidate)
        elif truth == TRUE:
            imaginative.append((candidate.first, candidate.second))
        else:
            raise ValueError(f"unsupported concurrence condition truth: {truth!r}")

    # In an absorption rule the first instance is the child.  Multiple TRUE parents or a
    # cycle are not repaired by priority; every involved candidate remains unresolved.
    parent_counts = Counter(candidate.first for candidate in true_absorptions)
    child_to_parent = {
        candidate.first: candidate.second for candidate in true_absorptions
    }
    conflicted_instances = {
        child for child, count in parent_counts.items() if count > 1
    }
    for child, parent in child_to_parent.items():
        if child_to_parent.get(parent) == child:
            conflicted_instances.update((child, parent))
    rejected = tuple(
        candidate
        for candidate in true_absorptions
        if candidate.first in conflicted_instances
        or candidate.second in conflicted_instances
    )
    rejected_set = set(rejected)
    applied = tuple(
        candidate for candidate in true_absorptions if candidate not in rejected_set
    )
    absorbed = frozenset(candidate.first for candidate in applied)
    return ConcurrenceResolution(
        retained_instances=established - absorbed,
        absorbed_instances=absorbed,
        imaginative_pairs=tuple(dict.fromkeys(imaginative)),
        unresolved_candidates=(*unresolved, *rejected),
        rejected_conflicts=rejected,
    )


__all__ = [
    "ABSORPTION",
    "IMAGINATIVE_CONCURRENCE",
    "SAME_EPISODE",
    "ConcurrenceCandidate",
    "ConcurrenceResolution",
    "ConcurrenceRule",
    "plan_concurrence_candidates",
    "resolve_concurrence",
]
