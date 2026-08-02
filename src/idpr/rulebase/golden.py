"""Golden scenarios for the compiled rulebase: one per reasoning path.

The previous asset's golden files cannot be reused. ``p2_scallop_golden_cases.json`` and
``property_scallop_golden_cases.json`` hold zero scenarios, while the archived pilot
golden cases assert on offence-specific relations that the generic rulebase deliberately
replaced. Their *coverage* is
carried over here (established, blocked, refuted, conflict, unknown) and extended to the
paths that are new: defeater, exception, absorption, imaginative concurrence, and the
decision that an unaddressed element does not block.

Cards are selected by ``(article, role, polarity)`` rather than named by id, so a scenario
states the reasoning path it exercises instead of pinning today's corpus. Selection is
deterministic (lowest id wins) and a missing combination fails the scenario rather than
silently skipping it -- if the corpus stops containing a defeater card for 제319조, the
defeater path stops being tested, and that must be loud.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

from idpr.rulebase.cards import CardCorpus, card_corpus
from idpr.rulebase.doctrine import UNCONDITIONAL
from idpr.rulebase.roles import CardRole, resolve_card_roles

#: Every relation a scenario may assert on.
ASSERTED_RELATIONS: tuple[str, ...] = (
    "element_supported",
    "element_refuted",
    "element_excluded",
    "element_unaddressed",
    "offense_defeated",
    "offense_established",
    "offense_undetermined",
    "is_absorbed",
    "final_offense",
    "concurrent_offenses",
    "contradiction",
)


class GoldenSelectionError(LookupError):
    """Raised when the corpus holds no card for a slot a scenario needs."""


@dataclass(frozen=True)
class CardSlot:
    """A card a scenario needs, described by what it must be rather than by id."""

    article: str
    role: str
    polarity: str
    status: str


@dataclass(frozen=True)
class Scenario:
    """One reasoning path, with the offences expected in each outcome relation."""

    scenario_id: str
    describes: str
    cards: tuple[CardSlot, ...]
    established: frozenset[str] = frozenset()
    undetermined: frozenset[str] = frozenset()
    defeated: frozenset[str] = frozenset()
    final: frozenset[str] = frozenset()
    absorbed: frozenset[str] = frozenset()
    concurrent: tuple[tuple[str, str], ...] = ()
    attempt_flagged: frozenset[str] = frozenset()
    #: When set, the first card is asserted both satisfied and not_satisfied, which is the
    #: only way to reach the contradiction guard: :func:`select_cards` never returns the
    #: same card twice.
    conflicting: bool = False
    #: Doctrine tables the scenario isolates. ``None`` keeps the reviewed table from disk;
    #: an explicit value (including an empty tuple) replaces it, so a scenario can test one
    #: concurrence rule without the rest of the corpus's doctrine firing alongside it.
    absorbed_by: tuple[tuple[str, str, str], ...] | None = ()
    imaginative_concurrence: tuple[tuple[str, str, str], ...] | None = ()
    attempt_punishable: tuple[str, ...] | None = ()
    preparation_punishable: tuple[str, ...] | None = ()
    #: Set when the scenario's point is that some element slot went unargued.
    expects_unaddressed_elements: bool = False


#: 제319조 주거침입 and 제297조 강간 are used throughout: both carry core, presumed,
#: negative, exception and defeater cards, so every path can be exercised on real doctrine.
_INTRUSION = "art319"
_RAPE = "art297"

#: Placeholder for "the card this scenario's last slot resolves to". A conditional
#: concurrence rule names a real card id, which :func:`select_cards` only knows at run
#: time, so the scenario states the *role* the condition plays and the substitution is
#: made once the cards are picked.
_CONDITION = "$condition"

SCENARIOS: tuple[Scenario, ...] = (
    Scenario(
        scenario_id="established_on_one_core_element",
        describes=(
            "core positive 카드 하나가 충족되고 막는 것이 없으면 죄가 성립한다. "
            "다른 요건 슬롯이 논증되지 않았어도 막지 않는다 — 이것이 게이트 설계의 핵심이다."
        ),
        cards=(CardSlot(_INTRUSION, "core", "positive", "satisfied"),),
        established=frozenset({_INTRUSION}),
        final=frozenset({_INTRUSION}),
        expects_unaddressed_elements=True,
    ),
    Scenario(
        scenario_id="presumed_element_also_supports",
        describes="presumed 카드 충족도 지지다. 주체·객체가 자명한 사안이 여기 해당한다.",
        cards=(CardSlot(_INTRUSION, "presumed", "positive", "satisfied"),),
        established=frozenset({_INTRUSION}),
        final=frozenset({_INTRUSION}),
        expects_unaddressed_elements=True,
    ),
    Scenario(
        scenario_id="unknown_neither_supports_nor_blocks",
        describes=(
            "unknown은 지지도 반증도 아니다. 죄는 성립하지도, 미정으로 남지도 않는다 — "
            "논의된 적 없는 죄명과 같은 상태다."
        ),
        cards=(CardSlot(_INTRUSION, "core", "positive", "unknown"),),
    ),
    Scenario(
        scenario_id="refuted_core_element_makes_undetermined",
        describes=(
            "core positive 카드가 명시적으로 반증되면 성립이 막히고 미정으로 남는다. "
            "삭제하지 않는다 — 콜 3이 그대로 논증한다."
        ),
        cards=(
            CardSlot(_INTRUSION, "core", "positive", "satisfied"),
            CardSlot(_INTRUSION, "core", "positive", "not_satisfied"),
        ),
        undetermined=frozenset({_INTRUSION}),
    ),
    Scenario(
        scenario_id="negative_card_satisfied_refutes",
        describes=(
            "negative polarity 카드는 '이런 경우에는 아니다'를 말한다. 충족은 반증이다."
        ),
        cards=(
            CardSlot(_INTRUSION, "core", "positive", "satisfied"),
            CardSlot(_INTRUSION, "core", "negative", "satisfied"),
        ),
        undetermined=frozenset({_INTRUSION}),
    ),
    Scenario(
        scenario_id="exception_card_excludes_the_element",
        describes="exception 카드가 충족되면 그 요건이 조각되어 성립이 막힌다.",
        cards=(
            CardSlot(_INTRUSION, "core", "positive", "satisfied"),
            CardSlot(_INTRUSION, "core", "exception", "satisfied"),
        ),
        undetermined=frozenset({_INTRUSION}),
    ),
    Scenario(
        scenario_id="defeater_blocks_a_supported_offense",
        describes=(
            "위법성·책임 조각사유가 충족되면 요건이 충족되어도 죄가 성립하지 않는다. "
            "심볼릭 레이어가 실제로 결정하는 것 중 하나다."
        ),
        cards=(
            CardSlot(_INTRUSION, "core", "positive", "satisfied"),
            CardSlot(_INTRUSION, "defeater", "positive", "satisfied"),
        ),
        defeated=frozenset({_INTRUSION}),
        undetermined=frozenset({_INTRUSION}),
    ),
    Scenario(
        scenario_id="context_card_cannot_establish_anything",
        describes=(
            "context 역할 카드는 충족되어도 지지가 되지 않는다. 의의·판례 예시가 "
            "죄를 성립시키면 안 된다."
        ),
        cards=(CardSlot(_INTRUSION, "context", "positive", "satisfied"),),
    ),
    Scenario(
        scenario_id="stage_card_cannot_establish_anything",
        describes="기수시기 카드도 성립 게이트에 들어가지 않는다.",
        cards=(CardSlot(_INTRUSION, "stage", "positive", "satisfied"),),
    ),
    Scenario(
        scenario_id="two_offenses_established_independently",
        describes="죄수 정의가 없으면 두 죄가 각각 성립하고 둘 다 최종 죄명이 된다.",
        cards=(
            CardSlot(_INTRUSION, "core", "positive", "satisfied"),
            CardSlot(_RAPE, "core", "positive", "satisfied"),
        ),
        established=frozenset({_INTRUSION, _RAPE}),
        final=frozenset({_INTRUSION, _RAPE}),
        expects_unaddressed_elements=True,
    ),
    Scenario(
        scenario_id="unconditional_absorption_drops_the_child_from_final",
        describes=(
            "조건 없는 흡수관계에서는 흡수되는 죄가 성립하되 최종 죄명에서 빠진다. "
            "`is_absorbed`는 질의 대상이므로 콜 3이 '흡수되어 별도로 성립하지 않는다'를 "
            "서술할 수 있다 — rubric이 점수를 주는 것은 그 서술이다."
        ),
        cards=(
            CardSlot(_INTRUSION, "core", "positive", "satisfied"),
            CardSlot(_RAPE, "core", "positive", "satisfied"),
        ),
        absorbed_by=((_INTRUSION, _RAPE, UNCONDITIONAL),),
        established=frozenset({_INTRUSION, _RAPE}),
        absorbed=frozenset({_INTRUSION}),
        final=frozenset({_RAPE}),
        expects_unaddressed_elements=True,
    ),
    Scenario(
        scenario_id="conditional_absorption_fires_when_the_condition_card_holds",
        describes=(
            "조건부 흡수는 조건 카드가 satisfied일 때 발화한다. 조건이 카드에 남아 "
            "있으므로 조문 쌍이 조건절을 삼키지 않는다."
        ),
        cards=(
            CardSlot(_INTRUSION, "core", "positive", "satisfied"),
            CardSlot(_RAPE, "core", "positive", "satisfied"),
            CardSlot(_INTRUSION, "concurrence", "positive", "satisfied"),
        ),
        absorbed_by=((_INTRUSION, _RAPE, _CONDITION),),
        established=frozenset({_INTRUSION, _RAPE}),
        absorbed=frozenset({_INTRUSION}),
        final=frozenset({_RAPE}),
        expects_unaddressed_elements=True,
    ),
    Scenario(
        scenario_id="conditional_absorption_stays_silent_when_the_condition_fails",
        describes=(
            "조건 카드가 not_satisfied면 흡수가 발화하지 않고 두 죄가 다 최종 죄명이 "
            "된다. 2항 표였다면 조건과 무관하게 죄명이 지워졌을 자리다."
        ),
        cards=(
            CardSlot(_INTRUSION, "core", "positive", "satisfied"),
            CardSlot(_RAPE, "core", "positive", "satisfied"),
            CardSlot(_INTRUSION, "concurrence", "positive", "not_satisfied"),
        ),
        absorbed_by=((_INTRUSION, _RAPE, _CONDITION),),
        established=frozenset({_INTRUSION, _RAPE}),
        final=frozenset({_INTRUSION, _RAPE}),
        expects_unaddressed_elements=True,
    ),
    Scenario(
        scenario_id="imaginative_concurrence_is_reported",
        describes="상상적 경합은 죄를 지우지 않고 관계로 보고된다.",
        cards=(
            CardSlot(_INTRUSION, "core", "positive", "satisfied"),
            CardSlot(_RAPE, "core", "positive", "satisfied"),
        ),
        imaginative_concurrence=((_INTRUSION, _RAPE, UNCONDITIONAL),),
        established=frozenset({_INTRUSION, _RAPE}),
        final=frozenset({_INTRUSION, _RAPE}),
        concurrent=((_INTRUSION, _RAPE),),
        expects_unaddressed_elements=True,
    ),
    Scenario(
        scenario_id="blocked_offense_with_an_attempt_provision_flags_the_attempt",
        describes=(
            "기수가 막힌 죄명에 미수 처벌 규정이 있으면 미수 검토가 결정론적으로 뜬다. "
            "스모크 케이스의 중지미수 논점이 이 경로다 — 강간 기수는 막혔고 제300조가 "
            "강간죄의 미수를 처벌한다."
        ),
        cards=(
            CardSlot(_RAPE, "core", "positive", "satisfied"),
            CardSlot(_RAPE, "core", "positive", "not_satisfied"),
        ),
        undetermined=frozenset({_RAPE}),
        attempt_flagged=frozenset({_RAPE}),
        attempt_punishable=(_RAPE,),
    ),
    Scenario(
        scenario_id="blocked_offense_without_an_attempt_provision_flags_nothing",
        describes=(
            "미수 처벌 규정이 없는 죄명은 기수가 막혀도 미수 검토가 뜨지 않는다. "
            "주거침입죄의 미수는 제322조 소관이고 코퓨스 밖이다."
        ),
        cards=(
            CardSlot(_INTRUSION, "core", "positive", "satisfied"),
            CardSlot(_INTRUSION, "core", "positive", "not_satisfied"),
        ),
        undetermined=frozenset({_INTRUSION}),
        attempt_punishable=(),
    ),
    Scenario(
        scenario_id="conflicting_status_for_one_card_is_detected",
        describes=(
            "한 카드에 두 상태가 오면 모순으로 검출된다. JSON 스키마가 막지만 "
            "값싼 방어다."
        ),
        cards=(CardSlot(_INTRUSION, "core", "positive", "satisfied"),),
        conflicting=True,
        undetermined=frozenset({_INTRUSION}),
    ),
)


def select_cards(
    scenario: Scenario,
    corpus: CardCorpus | None = None,
    roles: Sequence[CardRole] | None = None,
) -> tuple[tuple[str, str], ...]:
    """Resolve a scenario's card slots to ``(card_id, status)`` pairs.

    Distinct slots resolve to distinct cards, so a scenario asking for one satisfied and
    one refuted core card gets two different cards rather than the same card twice -- the
    latter would test the contradiction path by accident.
    """
    corpus = corpus or card_corpus()
    roles = roles or resolve_card_roles(corpus)
    role_by_card = {role.card_id: role.role for role in roles}

    used: set[str] = set()
    resolved: list[tuple[str, str]] = []
    for slot in scenario.cards:
        candidates = sorted(
            card.id
            for card in corpus.cards
            if card.article == slot.article
            and card.polarity == slot.polarity
            and role_by_card[card.id] == slot.role
            and card.id not in used
        )
        if not candidates:
            raise GoldenSelectionError(
                f"{scenario.scenario_id}: no unused card for "
                f"{slot.article}/{slot.role}/{slot.polarity}"
            )
        used.add(candidates[0])
        resolved.append((candidates[0], slot.status))
    return tuple(resolved)


def resolve_conditions(
    scenario: Scenario, selected: Sequence[tuple[str, str]]
) -> tuple[
    tuple[tuple[str, str, str], ...] | None, tuple[tuple[str, str, str], ...] | None
]:
    """Substitute the ``$condition`` placeholder with the card the last slot resolved to.

    Returns the scenario's two concurrence tables ready to compile. ``None`` is passed
    through so a scenario can still say "use the reviewed table from disk".
    """
    condition_card = selected[-1][0] if selected else UNCONDITIONAL

    def substitute(
        table: Sequence[tuple[str, str, str]] | None,
    ) -> tuple[tuple[str, str, str], ...] | None:
        if table is None:
            return None
        return tuple(
            (first, second, condition_card if cond == _CONDITION else cond)
            for first, second, cond in table
        )

    return substitute(scenario.absorbed_by), substitute(scenario.imaginative_concurrence)


def expected_relations(scenario: Scenario) -> Mapping[str, frozenset[tuple[str, ...]]]:
    """The tuples a scenario expects, keyed by relation.

    ``element_*`` and ``element_unaddressed`` are checked only for emptiness or
    non-emptiness, because their slot argument is corpus detail rather than doctrine.
    """
    return {
        "offense_established": frozenset((off,) for off in scenario.established),
        "offense_undetermined": frozenset((off,) for off in scenario.undetermined),
        "offense_defeated": frozenset((off,) for off in scenario.defeated),
        "final_offense": frozenset((off,) for off in scenario.final),
        "is_absorbed": frozenset((off,) for off in scenario.absorbed),
        "concurrent_offenses": frozenset(scenario.concurrent),
        "attempt_to_consider": frozenset((off,) for off in scenario.attempt_flagged),
    }
