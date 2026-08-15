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
from pathlib import Path

import yaml

from idpr.v2.evaluate import FALSE, TRUE, UNKNOWN, TruthValue
from idpr.v2.registry import DefinitionRegistry
from idpr.v2.runtime.identity import OffenseInstanceKey

ABSORPTION = "absorption"
IMAGINATIVE_CONCURRENCE = "imaginative_concurrence"
SPECIALTY = "specialty"
"""법조경합 특별관계 -- a qualified derived offense displacing the base it was built from.

Unlike the other two kinds this one carries no assessable condition. It is not a reading of the
case text but an application of the DSL's own authored `derivation.kind == "qualify"` relation:
if 특수절도 is established for this actor on the very theft binding that materialized it, plain
절도 is not separately realized. The host therefore never decides anything here -- see
:func:`plan_specialty_candidates` for the three joins that must all hold.
"""

DEFINITIONAL_RESOLUTION = "definitional_resolution"
"""An authored displacement that needs no case condition.

Two offences can be alternative readings of one and the same realized conduct -- 제337조 writes
"상해하거나 상해에 이르게 한 때" in a single article, and 살인 and 상해치사 divide the same death by
whether the intent is established.  The fact that separates them (상해·살인의 고의) is already an
element of the intentional offence, so asking it again as a concurrence condition would put one
proposition in two places and let the two answers disagree.  Establishment of the displacing
offence is therefore the whole ground: no condition is looked up, exactly as for SPECIALTY.

`resolution_type` records which doctrine the pair belongs to.  It is metadata for the writer and
the audit trail; the runtime behaviour of both types is identical.
"""

ALTERNATIVE_SUBTYPE = "alternative_subtype"
"""Two branches of one article (제337조 강도상해/치상, 제301조 강간상해/치상)."""

INTENT_DISPLACEMENT = "intent_displacement"
"""Separate articles where a confirmed intent governs the same result (살인 over 상해치사)."""

RESOLUTION_TYPES = frozenset({ALTERNATIVE_SUBTYPE, INTENT_DISPLACEMENT})

SAME_EPISODE = "same_episode"

SAME_REALIZATION = "same_realization"
"""Both instances must rest on the same realized conduct, not merely the same episode.

One episode can carry the same actor injuring one victim and killing another.  Displacing an
offence on nothing more than a shared episode would then delete a conviction earned by different
conduct, so a definitional rule joins on the focal action the two instances were built from.
"""

ACTOR_SAME = "same"
ACTOR_ANY = "any"
"""Whether a rule may join two instances belonging to different actors.

Authored per rule rather than enforced host-globally.  Absorption as authored today expresses a
relation between two offenses of *one* actor, and joining 甲's document forgery to 乙's seal
forgery on nothing but a shared episode is an identity defect -- but that is a property of the
rule, not of concurrence as such, so a future rule that genuinely relates two actors must be able
to say so in its own text instead of fighting a host invariant.  The in-code default is
:data:`ACTOR_SAME` because that is the safe reading; :func:`load_concurrence_rules` nonetheless
requires authored rules to state it explicitly, so the choice is never silent.
"""

_DEFINITIONAL_CONDITION = "derivation.qualify"
"""Placeholder condition ref for SPECIALTY rules; never looked up in `condition_truths`."""


@dataclass(frozen=True, slots=True)
class ConcurrenceRule:
    rule_id: str
    kind: str
    first_offense_ref: str
    second_offense_ref: str
    condition_ref: str
    occurrence_constraint: str = SAME_EPISODE
    actor_constraint: str = ACTOR_SAME
    source_card_ids: tuple[str, ...] = ()
    condition_statement: str = ""
    legal_standard: str = ""
    resolution_type: str = ""

    def __post_init__(self) -> None:
        if self.kind not in {
            ABSORPTION,
            IMAGINATIVE_CONCURRENCE,
            SPECIALTY,
            DEFINITIONAL_RESOLUTION,
        }:
            raise ValueError(f"unsupported concurrence kind: {self.kind!r}")
        if self.kind == DEFINITIONAL_RESOLUTION:
            if self.resolution_type not in RESOLUTION_TYPES:
                raise ValueError(
                    f"{self.rule_id}: definitional resolution must state a known resolution_type"
                )
            if self.condition_statement:
                raise ValueError(
                    f"{self.rule_id}: a definitional resolution has no assessable condition -- "
                    "put the doctrine in legal_standard instead of condition_statement"
                )
            if self.occurrence_constraint != SAME_REALIZATION:
                raise ValueError(
                    f"{self.rule_id}: definitional resolution must join on same_realization; a "
                    "shared episode can hold separate conduct against different victims"
                )
        elif self.resolution_type:
            raise ValueError(
                f"{self.rule_id}: resolution_type belongs to definitional resolutions only"
            )
        if self.occurrence_constraint not in {SAME_EPISODE, SAME_REALIZATION}:
            raise ValueError(
                f"unsupported occurrence_constraint: {self.occurrence_constraint!r}"
            )
        if self.actor_constraint not in {ACTOR_SAME, ACTOR_ANY}:
            raise ValueError(f"unsupported actor_constraint: {self.actor_constraint!r}")
        if self.first_offense_ref == self.second_offense_ref:
            raise ValueError("same-offense multiplicity needs a separately authored rule")
        if not self.rule_id or not self.condition_ref:
            raise ValueError("concurrence rule requires rule_id and condition_ref")


APPROVED = "approved"
"""The only `status` a rule file entry may carry to reach the runtime.

Authoring and approval are separated on purpose. A rule that is written down but not yet reviewed
must be visible to the next reader -- deleting it loses the analysis -- and must not fire. Anything
other than `approved` is loaded, counted, and then left out of the returned rules.
"""


def load_concurrence_rules(
    path: Path, *, include_unapproved: bool = False
) -> tuple[ConcurrenceRule, ...]:
    """Read authored concurrence rules, keeping only approved ones unless asked otherwise.

    `include_unapproved` exists for audits and review documents, never for the runtime path.
    """
    document = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    output: list[ConcurrenceRule] = []
    for entry in document.get("rules") or ():
        status = entry.get("status")
        if status != APPROVED and not include_unapproved:
            continue
        rule_id = str(entry["rule_id"])
        # Authored rules must state these; the in-code defaults exist for rules the host builds
        # itself (specialty), not as a place for an authoring omission to hide.
        if "actor_constraint" not in entry:
            raise ValueError(f"{rule_id}: authored rules must state actor_constraint")
        # `legal_standard` is always required; `condition_statement` only where a condition is
        # actually assessed.  A definitional resolution has nothing to ask, and filling the field
        # anyway would invite the next reader to wire it to a neural condition.
        required = ("legal_standard",)
        if str(entry.get("kind")) != DEFINITIONAL_RESOLUTION:
            required = ("condition_statement", "legal_standard")
        for field in required:
            if not str(entry.get(field) or "").strip():
                raise ValueError(
                    f"{rule_id}: {field} must be authored -- the assessment payload carries it "
                    "so the model reads the condition's meaning from the rule, not from a ref name"
                )
        output.append(
            ConcurrenceRule(
                rule_id=rule_id,
                kind=str(entry["kind"]),
                first_offense_ref=str(entry["first_offense_ref"]),
                second_offense_ref=str(entry["second_offense_ref"]),
                condition_ref=str(entry["condition_ref"]),
                occurrence_constraint=str(entry.get("occurrence_constraint", SAME_EPISODE)),
                actor_constraint=str(entry["actor_constraint"]),
                source_card_ids=tuple(str(value) for value in entry.get("source_card_ids") or ()),
                condition_statement=str(entry.get("condition_statement") or "").strip(),
                legal_standard=str(entry["legal_standard"]).strip(),
                resolution_type=str(entry.get("resolution_type") or "").strip(),
            )
        )
    return tuple(output)


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
    absorbed_into: tuple[tuple[OffenseInstanceKey, OffenseInstanceKey], ...] = ()
    """`(밀려난 죄, 밀어낸 죄)`. 가담자 쪽으로 같은 결정을 옮기려면 상대가 누구인지가 필요하다."""


def plan_concurrence_candidates(
    established_instances: Iterable[OffenseInstanceKey],
    *,
    episode_by_instance: Mapping[OffenseInstanceKey, str],
    rules: Iterable[ConcurrenceRule],
    focal_action_by_instance: Mapping[OffenseInstanceKey, str] | None = None,
) -> tuple[ConcurrenceCandidate, ...]:
    """Join exact authored offense pairs only inside one factual episode.

    A rule whose `actor_constraint` is `same` additionally requires both instances to belong to
    one actor.  Without it a single episode carrying 甲's document forgery and 乙's seal forgery
    would open a candidate across the two, and a TRUE condition would then delete 乙's offense on
    the strength of what 甲 did.
    """
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
                    if (
                        rule.actor_constraint == ACTOR_SAME
                        and first.actor_id != second.actor_id
                    ):
                        continue
                    if rule.occurrence_constraint == SAME_REALIZATION:
                        focal = focal_action_by_instance or {}
                        first_focal = focal.get(first)
                        second_focal = focal.get(second)
                        if (
                            first_focal is None
                            or second_focal is None
                            or first_focal != second_focal
                        ):
                            continue
                    output.append(
                        ConcurrenceCandidate(rule, first, second, first_episode)
                    )
    return tuple(output)


def same_realization_keys(
    *,
    focal_action_by_instance: Mapping[OffenseInstanceKey, str],
    source_realizations_by_instance: Mapping[OffenseInstanceKey, Iterable[str]],
    focal_action_by_occurrence: Mapping[str, str],
) -> dict[OffenseInstanceKey, str]:
    """`same_realization` 비교에 쓸 실현 식별자. 초점행위가 없는 파생실현까지 포함한다.

    host가 두 개 이상의 source realization에서 조립한 파생죄에는 초점행위가 없다. 강도치상은
    강도와 상해 두 실현에 걸쳐 있어 어느 하나를 초점으로 고를 수 없기 때문이고, 그 결정 자체는
    옳다 -- 증거 폭을 하나의 행위로 좁히면 안 되는 죄다.

    그런데 `same_realization`을 초점행위 동일성으로만 보면, 결과적 가중범(파생, 초점 없음)과
    고의범(직접 결박, 초점 있음)을 짝지으라고 저작된 규칙이 후보조차 열지 못한다. 실제로
    `r14_p2_q1`의 강도치상 대 강도상해가 그렇게 막혀 있었다.

    그래서 파생실현의 실현 식별자는 그 source realization들이 **한 초점행위에 모일 때** 그
    행위로 읽는다. 사건 원문을 다시 해석하는 것이 아니라 host 자신의 조립 기록을 되읽는 것이고,
    source들이 서로 다른 초점을 가지면 모호하므로 식별자를 만들지 않는다.
    """
    output: dict[OffenseInstanceKey, str] = {}
    for instance, focal in focal_action_by_instance.items():
        if focal:
            output[instance] = focal
    for instance, source_ids in source_realizations_by_instance.items():
        if output.get(instance):
            continue
        focals = {
            focal_action_by_occurrence[source_id]
            for source_id in source_ids
            if focal_action_by_occurrence.get(source_id)
        }
        if len(focals) == 1:
            output[instance] = focals.pop()
    return output


def plan_specialty_candidates(
    established_instances: Iterable[OffenseInstanceKey],
    *,
    registry: DefinitionRegistry,
    episode_by_instance: Mapping[OffenseInstanceKey, str],
    source_bindings_by_instance: Mapping[OffenseInstanceKey, Iterable[str]],
) -> tuple[ConcurrenceCandidate, ...]:
    """Open 특별관계 candidates from the authored qualify-derivation, not from case text.

    Three joins must all hold, and each is load-bearing:

    * the derived offense's `derivation.kind` is `qualify` and names this base ref;
    * both instances belong to the same actor -- one factual episode can carry 甲, 乙 and 丙 each
      committing theft, and 甲's 특수절도 must not swallow 乙's 절도;
    * the base instance's occurrence is one the planner actually recorded as a
      source realization when it materialized the derived candidate.  (The
      parameter name remains for historical callers.)

    The third is what keeps this deterministic: the absorption link is read back out of the
    host's own materialization record, never re-derived from the text.
    """
    established = tuple(dict.fromkeys(established_instances))
    missing = set(established) - set(episode_by_instance)
    if missing:
        raise ValueError(
            f"established instances lack factual episode ids: {sorted(missing, key=repr)}"
        )
    by_actor_ref: dict[tuple[str, str, str], list[OffenseInstanceKey]] = {}
    for instance in established:
        key = (instance.case_id, instance.actor_id, instance.offense_ref)
        by_actor_ref.setdefault(key, []).append(instance)

    output: list[ConcurrenceCandidate] = []
    for derived in established:
        entry = registry.get(derived.offense_ref)
        if entry is None or entry.kind != "derived_offense":
            continue
        derivation = entry.payload.get("derivation") or {}
        if derivation.get("kind") != "qualify":
            continue
        base_ref = derivation.get("base")
        if not base_ref:
            continue
        sources = frozenset(source_bindings_by_instance.get(derived, ()))
        if not sources:
            continue
        rule = ConcurrenceRule(
            rule_id=f"specialty:{base_ref}<-{derived.offense_ref}",
            kind=SPECIALTY,
            first_offense_ref=base_ref,
            second_offense_ref=derived.offense_ref,
            condition_ref=_DEFINITIONAL_CONDITION,
        )
        bases = by_actor_ref.get((derived.case_id, derived.actor_id, base_ref), ())
        for base in bases:
            if base.occurrence_id not in sources:
                continue
            episode = episode_by_instance[derived]
            if episode != episode_by_instance[base]:
                continue
            output.append(ConcurrenceCandidate(rule, base, derived, episode))
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
        if candidate.rule.kind in (SPECIALTY, DEFINITIONAL_RESOLUTION):
            # Definitional: the qualify-derivation itself is the ground, so there is no condition
            # to look up. It still folds through the same conflict handling below, which is the
            # point -- two parents claiming one child stay unresolved here as anywhere else.
            true_absorptions.append(candidate)
            continue
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
        absorbed_into=tuple(
            (candidate.first, candidate.second) for candidate in applied
        ),
    )


def propagate_absorption_to_accessories(
    resolution: ConcurrenceResolution,
    *,
    derivative_links: Iterable[tuple[OffenseInstanceKey, OffenseInstanceKey, str]],
) -> ConcurrenceResolution:
    """정범의 죄가 밀려나면 그 정범을 향한 가담자의 죄도 같이 밀려난다.

    가담자 후보는 정범 realization 하나마다 따로 만들어지므로, 甲의 절도가 특수절도에 밀려도
    乙의 절도방조는 그대로 남는다. 그러면 乙에게 절도방조와 특수절도방조가 함께 선다.

    여기서 새로 판단하는 것은 없다. 정범 단계에서 이미 내려진 결정을 그 정범을 향한 가담
    관계로 옮길 뿐이고, **대체가 실제로 존재할 때만** 옮긴다 -- 乙이 밀어낸 죄 쪽 정범에게도
    같은 mode로 연결되어 있어야 한다. 대체 없이 밀어내면 책임을 지우는 것이 되고, 그것은
    경합이 하는 일이 아니다.
    """
    links = tuple(derivative_links)
    if not resolution.absorbed_into or not links:
        return resolution
    principal_of = {
        (accessory, mode): principal for accessory, principal, mode in links
    }
    accessories_of: dict[tuple[OffenseInstanceKey, str], list[OffenseInstanceKey]] = {}
    for accessory, principal, mode in links:
        accessories_of.setdefault((principal, mode), []).append(accessory)
    extra: dict[OffenseInstanceKey, OffenseInstanceKey] = {}
    for child, parent in resolution.absorbed_into:
        for (accessory, mode), principal in principal_of.items():
            if principal != child or accessory not in resolution.retained_instances:
                continue
            replacement = next(
                (
                    value
                    for value in accessories_of.get((parent, mode), ())
                    if value.actor_id == accessory.actor_id
                    and value in resolution.retained_instances
                ),
                None,
            )
            if replacement is not None:
                extra[accessory] = replacement
    if not extra:
        return resolution
    absorbed = resolution.absorbed_instances | frozenset(extra)
    return ConcurrenceResolution(
        retained_instances=resolution.retained_instances - frozenset(extra),
        absorbed_instances=absorbed,
        imaginative_pairs=resolution.imaginative_pairs,
        unresolved_candidates=resolution.unresolved_candidates,
        rejected_conflicts=resolution.rejected_conflicts,
        absorbed_into=(*resolution.absorbed_into, *sorted(
            extra.items(),
            key=lambda value: (*_instance_fields(value[0]), *_instance_fields(value[1])),
        )),
    )


def _instance_fields(value: OffenseInstanceKey) -> tuple[str, str, str, str]:
    return (value.case_id, value.actor_id, value.offense_ref, value.occurrence_id)


REAL_CONCURRENCE_CANDIDATE = "real_concurrence_candidate"
"""실체적 경합 **후보**. 확정이 아니다.

형법 제40조의 "한 개의 행위"는 사회관념상 하나의 행위로 평가되는지를 묻는 규범적 판단이고,
초점행위가 다르다는 구조적 사실이 곧 제37조 전단의 경합범이라는 결론은 아니다. 그래서 이
값은 저작이나 별도의 typed 판단이 확정해 줄 자리를 열어 둘 뿐이고, 그 자체로 답안의 최종
죄수관계가 되지 않는다 -- 상상적 경합 규칙에 걸리지 않았다는 사실을 실체적 경합의 적극적
근거로 쓰지 않는다는 원칙이 여기에도 그대로 적용된다.
"""

IMAGINATIVE_CONCURRENCE_CANDIDATE = "imaginative_concurrence_candidate"
"""초점행위가 같아 상상적 경합이 의심되는 짝. 저작이 확정한 것이 아니므로 후보다."""


def classify_concurrence_relations(
    retained_instances: Iterable[OffenseInstanceKey],
    *,
    realization_by_instance: Mapping[OffenseInstanceKey, str],
    imaginative_pairs: Iterable[tuple[OffenseInstanceKey, OffenseInstanceKey]] = (),
) -> tuple[tuple[OffenseInstanceKey, OffenseInstanceKey, str], ...]:
    """한 행위자에게 남은 죄들 사이의 죄수관계를 타입으로 산출한다.

    실체적 경합을 "흡수도 상상적 경합도 아닌 나머지"로 찍지 않는다. 그렇게 하면 규칙베이스가
    모든 죄수관계를 빠짐없이 열거했다는 보장 위에 서게 되고, 부존재를 적극적 사실로 쓰는 일이
    된다. 대신 두 갈래 모두 **실현 행위의 동일성**이라는 같은 근거에서 적극적으로 읽는다 --
    행위가 하나면 상상적 경합(제40조), 행위가 여럿이면 실체적 경합(제37조 전단)이다.

    법조경합(흡수·특별관계)은 이 단계 이전에 이미 제거되어 있다. 여기 남은 것은 모두 실제로
    병존하는 죄다.

    두 갈래의 지위가 다르다. 저작된 `imaginative_concurrence` 규칙이 확정한 상상적 경합만
    확정이고, 초점행위가 다르다는 사실에서 읽은 실체적 경합은 **후보**다. 형법 제40조의
    "한 개의 행위"는 사회관념상 하나의 행위로 평가되는지를 묻는 규범적 판단이므로, 초점행위가
    다르다는 구조적 사실이 곧 제37조 전단의 경합범이라는 결론이 되지 않는다. 초점행위가 같아
    상상적 경합이 의심되는 경우도 저작이 확정하지 않았으면 후보로만 남긴다.

    실현 식별자를 모르는 instance는 짝을 만들지 않는다 -- 모르면 말하지 않는다.
    """
    retained = tuple(dict.fromkeys(retained_instances))
    authored = {
        frozenset(pair) for pair in imaginative_pairs
    }
    output: list[tuple[OffenseInstanceKey, OffenseInstanceKey, str]] = []
    for index, left in enumerate(sorted(retained, key=_instance_fields)):
        for right in sorted(retained, key=_instance_fields)[index + 1 :]:
            if left.actor_id != right.actor_id or left.case_id != right.case_id:
                continue
            if frozenset((left, right)) in authored:
                output.append((left, right, IMAGINATIVE_CONCURRENCE))
                continue
            left_key = realization_by_instance.get(left)
            right_key = realization_by_instance.get(right)
            if not left_key or not right_key:
                continue
            output.append(
                (
                    left,
                    right,
                    IMAGINATIVE_CONCURRENCE_CANDIDATE
                    if left_key == right_key
                    else REAL_CONCURRENCE_CANDIDATE,
                )
            )
    return tuple(output)


__all__ = [
    "ABSORPTION",
    "ACTOR_ANY",
    "ACTOR_SAME",
    "ALTERNATIVE_SUBTYPE",
    "APPROVED",
    "DEFINITIONAL_RESOLUTION",
    "IMAGINATIVE_CONCURRENCE",
    "INTENT_DISPLACEMENT",
    "RESOLUTION_TYPES",
    "SAME_EPISODE",
    "SAME_REALIZATION",
    "SPECIALTY",
    "ConcurrenceCandidate",
    "ConcurrenceResolution",
    "ConcurrenceRule",
    "load_concurrence_rules",
    "plan_concurrence_candidates",
    "plan_specialty_candidates",
    "IMAGINATIVE_CONCURRENCE_CANDIDATE",
    "REAL_CONCURRENCE_CANDIDATE",
    "classify_concurrence_relations",
    "propagate_absorption_to_accessories",
    "resolve_concurrence",
    "same_realization_keys",
]
