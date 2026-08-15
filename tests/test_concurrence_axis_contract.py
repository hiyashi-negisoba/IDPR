"""Concurrence 축의 종료 증명.

성립한 죄들 사이의 최종 중복·배제만 본다. 어떤 죄가 성립하는지는 앞 축들의 일이다.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from idpr.v2.registry import load_definitions
from idpr.v2.runtime.concurrence import (
    ABSORPTION,
    DEFINITIONAL_RESOLUTION,
    SAME_REALIZATION,
    SPECIALTY,
    ConcurrenceCandidate,
    ConcurrenceResolution,
    ConcurrenceRule,
    load_concurrence_rules,
    plan_concurrence_candidates,
    propagate_absorption_to_accessories,
    resolve_concurrence,
    same_realization_keys,
)
from idpr.v2.runtime.identity import OffenseInstanceKey

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = load_definitions(ROOT / "data/v2/definitions")
RULES = load_concurrence_rules(ROOT / "data/v2/concurrence_rules.yaml")


def _instance(actor: str, ref: str, occurrence: str) -> OffenseInstanceKey:
    return OffenseInstanceKey("case", actor, ref, occurrence)


# --------------------------------------------------------------------------
# 1. 발화 불가능성 — 저작된 규칙이 후보조차 열지 못하는가
# --------------------------------------------------------------------------


@pytest.mark.parametrize("rule", RULES, ids=lambda value: value.rule_id)
def test_both_endpoints_of_every_rule_are_loaded_offences(rule) -> None:
    for ref in (rule.first_offense_ref, rule.second_offense_ref):
        entry = REGISTRY.get(ref)
        assert entry is not None and entry.kind in {"offense", "derived_offense"}, ref


@pytest.mark.parametrize(
    "rule",
    [value for value in RULES if value.occurrence_constraint == SAME_REALIZATION],
    ids=lambda value: value.rule_id,
)
def test_same_realization_rules_open_across_a_host_derived_offence(rule) -> None:
    """결과적 가중범은 host가 조립한 파생실현이라 초점행위가 없다.

    `same_realization`을 초점행위 동일성으로만 보면, 결과적 가중범과 고의범을 짝지으라고
    저작된 규칙이 후보를 하나도 열지 못한다. 감사 시점 `r14_p2_q1`의 강도치상 대 강도상해가
    정확히 그 상태였다 -- 한쪽 focal은 `factual_action:001:007`, 다른 쪽은 None이었다.
    """
    derived = _instance("甲", rule.first_offense_ref, "realization:derived:001")
    direct = _instance("甲", rule.second_offense_ref, "realization:004")
    source = _instance("甲", "offense.theft", "realization:003")
    focal = "factual_action:001:007"

    keys = same_realization_keys(
        focal_action_by_instance={direct: focal, source: focal},
        source_realizations_by_instance={derived: (source.occurrence_id,)},
        focal_action_by_occurrence={source.occurrence_id: focal},
    )
    assert keys[derived] == focal, "파생실현이 실현 식별자를 얻지 못했다"

    candidates = plan_concurrence_candidates(
        (derived, direct),
        episode_by_instance={derived: "ep:001", direct: "ep:001"},
        rules=(rule,),
        focal_action_by_instance=keys,
    )
    assert candidates, f"{rule.rule_id}: 후보가 열리지 않았다"


def test_ambiguous_sources_leave_the_realization_unidentified() -> None:
    """source들이 서로 다른 초점을 가리키면 식별자를 만들지 않는다. 추측하지 않는다."""
    derived = _instance("甲", "derived_offense.special_theft", "realization:derived:001")
    keys = same_realization_keys(
        focal_action_by_instance={},
        source_realizations_by_instance={derived: ("realization:001", "realization:002")},
        focal_action_by_occurrence={
            "realization:001": "factual_action:001:001",
            "realization:002": "factual_action:001:009",
        },
    )
    assert derived not in keys


# --------------------------------------------------------------------------
# 2. 최종 중복 — 정범에서 밀려난 죄가 가담자 쪽에 남지 않는가
# --------------------------------------------------------------------------


def _absorbed(child: OffenseInstanceKey, parent: OffenseInstanceKey, *others):
    return ConcurrenceResolution(
        retained_instances=frozenset({parent, *others}),
        absorbed_instances=frozenset({child}),
        imaginative_pairs=(),
        unresolved_candidates=(),
        rejected_conflicts=(),
        absorbed_into=((child, parent),),
    )


def test_accessory_follows_the_principal_absorption() -> None:
    """甲의 절도가 특수절도에 밀리면 乙의 절도방조도 특수절도방조에 밀린다."""
    base = _instance("甲", "offense.theft", "realization:001")
    qualified = _instance("甲", "derived_offense.special_theft", "realization:002")
    aid_base = _instance("乙", "offense.theft", "participation_realization:a")
    aid_qualified = _instance(
        "乙", "derived_offense.special_theft", "participation_realization:b"
    )
    resolved = propagate_absorption_to_accessories(
        _absorbed(base, qualified, aid_base, aid_qualified),
        derivative_links=(
            (aid_base, base, "aider"),
            (aid_qualified, qualified, "aider"),
        ),
    )
    assert aid_base in resolved.absorbed_instances
    assert aid_qualified in resolved.retained_instances
    assert (aid_base, aid_qualified) in resolved.absorbed_into


def test_accessory_is_not_absorbed_without_a_replacement() -> None:
    """대체가 없으면 밀어내지 않는다. 대체 없는 흡수는 책임을 지우는 일이다."""
    base = _instance("甲", "offense.theft", "realization:001")
    qualified = _instance("甲", "derived_offense.special_theft", "realization:002")
    aid_base = _instance("乙", "offense.theft", "participation_realization:a")
    resolved = propagate_absorption_to_accessories(
        _absorbed(base, qualified, aid_base),
        derivative_links=((aid_base, base, "aider"),),
    )
    assert aid_base in resolved.retained_instances
    assert resolved.absorbed_instances == frozenset({base})


def test_another_actors_accessory_is_untouched() -> None:
    """다른 가담자의 죄를 대체로 세지 않는다."""
    base = _instance("甲", "offense.theft", "realization:001")
    qualified = _instance("甲", "derived_offense.special_theft", "realization:002")
    aid_base = _instance("乙", "offense.theft", "participation_realization:a")
    other = _instance("丙", "derived_offense.special_theft", "participation_realization:c")
    resolved = propagate_absorption_to_accessories(
        _absorbed(base, qualified, aid_base, other),
        derivative_links=((aid_base, base, "aider"), (other, qualified, "aider")),
    )
    assert aid_base in resolved.retained_instances


# --------------------------------------------------------------------------
# 3. 배타·우선관계 — 두 부모가 한 자식을 주장하면 어느 쪽도 이기지 않는다
# --------------------------------------------------------------------------


def test_conflicting_parents_leave_the_child_standing_and_unresolved() -> None:
    child = _instance("甲", "offense.theft", "realization:001")
    left = _instance("甲", "derived_offense.special_theft", "realization:002")
    right = _instance("甲", "derived_offense.nighttime_dwelling_theft", "realization:003")
    rule = lambda ref, second: ConcurrenceRule(  # noqa: E731
        rule_id=ref,
        kind=SPECIALTY,
        first_offense_ref=child.offense_ref,
        second_offense_ref=second.offense_ref,
        condition_ref="derivation.qualify",
    )
    resolution = resolve_concurrence(
        (child, left, right),
        (
            ConcurrenceCandidate(rule("a", left), child, left, "ep:001"),
            ConcurrenceCandidate(rule("b", right), child, right, "ep:001"),
        ),
        condition_truths={},
    )
    assert child in resolution.retained_instances
    assert resolution.rejected_conflicts
    assert not resolution.absorbed_into


def test_authored_rules_are_all_approved_and_of_a_supported_kind() -> None:
    assert RULES, "승인된 경합 규칙이 하나도 없다"
    for rule in RULES:
        assert rule.kind in {ABSORPTION, SPECIALTY, DEFINITIONAL_RESOLUTION}
