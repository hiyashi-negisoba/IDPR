from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest
import yaml

from idpr.v2.evaluate import FALSE, TRUE, UNKNOWN
from idpr.v2.registry import DefinitionRegistry, load_definitions
from idpr.v2.runtime.concurrence import (
    ABSORPTION,
    ACTOR_ANY,
    ACTOR_SAME,
    APPROVED,
    IMAGINATIVE_CONCURRENCE,
    ConcurrenceRule,
    load_concurrence_rules,
    plan_concurrence_candidates,
    plan_specialty_candidates,
    resolve_concurrence,
)
from idpr.v2.runtime.identity import OffenseInstanceKey


def _instance(offense: str, occurrence: str) -> OffenseInstanceKey:
    return OffenseInstanceKey("case", "甲", offense, occurrence)


def test_planner_requires_same_episode_and_exact_offense_refs() -> None:
    injury = _instance("offense.injury", "binding:001")
    homicide = _instance("offense.homicide", "binding:002")
    unrelated = _instance("offense.property_damage", "binding:003")
    rule = ConcurrenceRule(
        "rule.injury_absorbed",
        ABSORPTION,
        "offense.injury",
        "offense.homicide",
        "card.injury_absorbed",
    )

    candidates = plan_concurrence_candidates(
        (injury, homicide, unrelated),
        episode_by_instance={
            injury: "episode:1",
            homicide: "episode:1",
            unrelated: "episode:1",
        },
        rules=(rule,),
    )
    assert [(value.first, value.second) for value in candidates] == [
        (injury, homicide)
    ]

    assert (
        plan_concurrence_candidates(
            (injury, homicide),
            episode_by_instance={injury: "episode:1", homicide: "episode:2"},
            rules=(rule,),
        )
        == ()
    )


def test_unknown_condition_never_removes_an_offense() -> None:
    injury = _instance("offense.injury", "binding:001")
    homicide = _instance("offense.homicide", "binding:002")
    rule = ConcurrenceRule(
        "rule.injury_absorbed",
        ABSORPTION,
        "offense.injury",
        "offense.homicide",
        "card.injury_absorbed",
    )
    candidate = plan_concurrence_candidates(
        (injury, homicide),
        episode_by_instance={injury: "episode:1", homicide: "episode:1"},
        rules=(rule,),
    )[0]

    result = resolve_concurrence(
        (injury, homicide),
        (candidate,),
        condition_truths={(rule.rule_id, injury, homicide): UNKNOWN},
    )
    assert result.retained_instances == {injury, homicide}
    assert result.absorbed_instances == set()
    assert result.unresolved_candidates == (candidate,)


def test_true_absorption_removes_only_the_exact_child_occurrence() -> None:
    injury = _instance("offense.injury", "binding:001")
    another_injury = _instance("offense.injury", "binding:009")
    homicide = _instance("offense.homicide", "binding:002")
    rule = ConcurrenceRule(
        "rule.injury_absorbed",
        ABSORPTION,
        "offense.injury",
        "offense.homicide",
        "card.injury_absorbed",
    )
    candidate = plan_concurrence_candidates(
        (injury, another_injury, homicide),
        episode_by_instance={
            injury: "episode:1",
            another_injury: "episode:2",
            homicide: "episode:1",
        },
        rules=(rule,),
    )[0]
    result = resolve_concurrence(
        (injury, another_injury, homicide),
        (candidate,),
        condition_truths={(rule.rule_id, injury, homicide): TRUE},
    )
    assert result.absorbed_instances == {injury}
    assert result.retained_instances == {another_injury, homicide}


def test_false_and_imaginative_conditions_have_distinct_effects() -> None:
    arson = _instance("offense.arson_of_occupied_structure", "binding:001")
    homicide = _instance("offense.homicide", "binding:002")
    rule = ConcurrenceRule(
        "rule.arson_homicide",
        IMAGINATIVE_CONCURRENCE,
        "offense.arson_of_occupied_structure",
        "offense.homicide",
        "card.arson_homicide",
    )
    candidate = plan_concurrence_candidates(
        (arson, homicide),
        episode_by_instance={arson: "episode:1", homicide: "episode:1"},
        rules=(rule,),
    )[0]
    false_result = resolve_concurrence(
        (arson, homicide),
        (candidate,),
        condition_truths={(rule.rule_id, arson, homicide): FALSE},
    )
    assert false_result.imaginative_pairs == ()

    true_result = resolve_concurrence(
        (arson, homicide),
        (candidate,),
        condition_truths={(rule.rule_id, arson, homicide): TRUE},
    )
    assert true_result.imaginative_pairs == ((arson, homicide),)
    assert true_result.retained_instances == {arson, homicide}


def test_conflicting_true_absorptions_are_unresolved_not_repaired() -> None:
    child = _instance("offense.injury", "binding:001")
    first_parent = _instance("offense.homicide", "binding:002")
    second_parent = _instance("offense.robbery", "binding:003")
    rules = (
        ConcurrenceRule(
            "rule.parent1",
            ABSORPTION,
            "offense.injury",
            "offense.homicide",
            "card.parent1",
        ),
        ConcurrenceRule(
            "rule.parent2",
            ABSORPTION,
            "offense.injury",
            "offense.robbery",
            "card.parent2",
        ),
    )
    episodes = {value: "episode:1" for value in (child, first_parent, second_parent)}
    candidates = plan_concurrence_candidates(
        (child, first_parent, second_parent),
        episode_by_instance=episodes,
        rules=rules,
    )
    truths = {
        (value.rule.rule_id, value.first, value.second): TRUE for value in candidates
    }
    result = resolve_concurrence(
        (child, first_parent, second_parent),
        candidates,
        condition_truths=truths,
    )
    assert result.absorbed_instances == set()
    assert result.retained_instances == {child, first_parent, second_parent}
    assert set(result.rejected_conflicts) == set(candidates)


def test_authored_absorption_does_not_cross_actors() -> None:
    """甲's document forgery must not swallow 乙's seal forgery on a shared episode alone."""
    seal_eul = OffenseInstanceKey("case", "乙", "offense.seal", "binding:001")
    document_gap = OffenseInstanceKey("case", "甲", "offense.document", "binding:002")
    seal_gap = OffenseInstanceKey("case", "甲", "offense.seal", "binding:003")
    rule = ConcurrenceRule(
        "rule.seal_absorbed",
        ABSORPTION,
        "offense.seal",
        "offense.document",
        "condition.seal_absorbed",
        actor_constraint=ACTOR_SAME,
    )
    episodes = dict.fromkeys((seal_eul, document_gap, seal_gap), "episode:1")

    candidates = plan_concurrence_candidates(
        (seal_eul, document_gap, seal_gap),
        episode_by_instance=episodes,
        rules=(rule,),
    )
    assert [candidate.first for candidate in candidates] == [seal_gap]

    crossing = plan_concurrence_candidates(
        (seal_eul, document_gap, seal_gap),
        episode_by_instance=episodes,
        rules=(replace(rule, actor_constraint=ACTOR_ANY),),
    )
    assert {candidate.first for candidate in crossing} == {seal_eul, seal_gap}


def test_authored_rules_must_state_the_actor_constraint_and_condition_meaning() -> None:
    """Loader-level, not dataclass-level: an authoring omission must not take a safe default."""
    entry = {
        "rule_id": "rule.draft",
        "status": APPROVED,
        "kind": ABSORPTION,
        "first_offense_ref": "offense.seal",
        "second_offense_ref": "offense.document",
        "condition_ref": "condition.seal_absorbed",
        "actor_constraint": ACTOR_SAME,
        "condition_statement": "그 인영이 그 문서의 구성부분을 이루는가.",
        "legal_standard": "그 인영이 바로 그 문서에 찍혀 기명·날인 부분을 이루는지를 본다.",
    }

    def _write(payload: dict[str, object], tmp: Path) -> Path:
        tmp.write_text(
            yaml.safe_dump({"version": 1, "rules": [payload]}, allow_unicode=True),
            encoding="utf-8",
        )
        return tmp

    with TemporaryDirectory() as directory:
        root = Path(directory)
        assert load_concurrence_rules(_write(entry, root / "ok.yaml"))
        for missing in ("actor_constraint", "condition_statement", "legal_standard"):
            payload = {key: value for key, value in entry.items() if key != missing}
            with pytest.raises(ValueError, match=missing):
                load_concurrence_rules(_write(payload, root / f"{missing}.yaml"))


def test_the_authored_absorption_condition_asks_only_the_pair_relation() -> None:
    """The condition carries one atomic proposition: is that impression part of that document?

    Two things it must *not* carry.  It must not split 위조 from 부정사용 --
    `offense.seal_forgery_or_misuse` holds both subtypes in one definition, so a condition reaching
    only forged impressions would silently drop Article 239 misuse out of the rule.  And it must not
    re-ask whether the impression was unauthorized: that is the absorbed instance's own element, and
    at resolution time its establishment already guarantees it.  A pair target that judged authority
    again would let one question be answered differently in two places.
    """
    rules = load_concurrence_rules(Path("data/v2/concurrence_rules.yaml"))
    rule = next(
        value
        for value in rules
        if value.rule_id == "absorption.seal_forgery_by_private_document_forgery"
    )
    assert rule.actor_constraint == ACTOR_SAME
    assert "구성부분" in rule.condition_statement
    for element_word in ("위조", "부정사용", "권한"):
        assert element_word not in rule.condition_statement
    assert "권한이 있었는지는 여기서 판단하지 않는다" in rule.legal_standard


def _specialty_registry() -> DefinitionRegistry:
    return load_definitions(Path("data/v2/definitions"))


def test_specialty_absorbs_only_the_same_actor_base_binding() -> None:
    """KCL r13_p1_q1 shape: 甲, 乙 and 丙 each steal in one episode and each gets 특수절도."""
    registry = _specialty_registry()
    episode = "factual_episode:001"
    theft_gap = OffenseInstanceKey("case", "甲", "offense.theft", "binding:001")
    theft_eul = OffenseInstanceKey("case", "乙", "offense.theft", "binding:003")
    special_gap = OffenseInstanceKey(
        "case", "甲", "derived_offense.special_theft", "derived_binding:002"
    )
    established = (theft_gap, theft_eul, special_gap)

    candidates = plan_specialty_candidates(
        established,
        registry=registry,
        episode_by_instance=dict.fromkeys(established, episode),
        # The planner materialized 甲's 특수절도 out of every actor's theft binding.
        source_bindings_by_instance={special_gap: ("binding:001", "binding:003")},
    )

    assert [candidate.first for candidate in candidates] == [theft_gap]

    resolution = resolve_concurrence(established, candidates, condition_truths={})
    assert resolution.absorbed_instances == frozenset({theft_gap})
    assert theft_eul in resolution.retained_instances


def test_specialty_needs_the_recorded_materialization_link() -> None:
    registry = _specialty_registry()
    theft = OffenseInstanceKey("case", "甲", "offense.theft", "binding:009")
    special = OffenseInstanceKey(
        "case", "甲", "derived_offense.special_theft", "derived_binding:002"
    )
    established = (theft, special)

    candidates = plan_specialty_candidates(
        established,
        registry=registry,
        episode_by_instance=dict.fromkeys(established, "factual_episode:001"),
        source_bindings_by_instance={special: ("binding:001",)},
    )

    assert candidates == ()


def test_specialty_does_not_fire_when_the_derived_offense_is_not_established() -> None:
    registry = _specialty_registry()
    theft = OffenseInstanceKey("case", "甲", "offense.theft", "binding:001")

    candidates = plan_specialty_candidates(
        (theft,),
        registry=registry,
        episode_by_instance={theft: "factual_episode:001"},
        source_bindings_by_instance={},
    )

    assert candidates == ()


def test_ordered_cross_episode_opens_a_candidate_the_episode_boundary_would_hide() -> None:
    """불가벌적 사후행위의 전형은 "먼저 성립 → 시간 경과 → 나중 영득"이다.

    episode 경계는 법적 요건이 아니라 Call 1.5가 서사를 나눈 결과다. 그것을 규칙의 요건으로
    쓰면 아는 false negative를 규칙에 저작하게 된다.
    """
    from idpr.v2.runtime.concurrence import (
        ORDERED_CROSS_EPISODE,
        ConcurrenceRule,
        plan_concurrence_candidates,
    )
    from idpr.v2.runtime.identity import OffenseInstanceKey

    custody = OffenseInstanceKey("case", "甲", "offense.stolen_property_custody", "r1")
    embezzlement = OffenseInstanceKey("case", "甲", "offense.embezzlement", "r2")
    rule = ConcurrenceRule(
        "absorption.test",
        "absorption",
        "offense.embezzlement",
        "offense.stolen_property_custody",
        "condition.test",
        occurrence_constraint=ORDERED_CROSS_EPISODE,
    )
    episodes = {custody: "factual_episode:001", embezzlement: "factual_episode:002"}
    order = ("factual_episode:001", "factual_episode:002")

    candidates = plan_concurrence_candidates(
        (custody, embezzlement),
        episode_by_instance=episodes,
        rules=(rule,),
        factual_episode_order=order,
    )
    assert len(candidates) == 1

    # 같은 입력이라도 `same_episode`로는 후보가 열리지 않는다.
    same_episode_rule = ConcurrenceRule(
        "absorption.test",
        "absorption",
        "offense.embezzlement",
        "offense.stolen_property_custody",
        "condition.test",
    )
    assert (
        plan_concurrence_candidates(
            (custody, embezzlement),
            episode_by_instance=episodes,
            rules=(same_episode_rule,),
            factual_episode_order=order,
        )
        == ()
    )


def test_ordered_cross_episode_refuses_the_reverse_order_and_unknown_episodes() -> None:
    """순서는 후보를 좁히는 자료다. 모르는 것을 "앞선다"로 읽으면 무제약이 된다."""
    from idpr.v2.runtime.concurrence import (
        ORDERED_CROSS_EPISODE,
        ConcurrenceRule,
        plan_concurrence_candidates,
    )
    from idpr.v2.runtime.identity import OffenseInstanceKey

    custody = OffenseInstanceKey("case", "甲", "offense.stolen_property_custody", "r1")
    embezzlement = OffenseInstanceKey("case", "甲", "offense.embezzlement", "r2")
    rule = ConcurrenceRule(
        "absorption.test",
        "absorption",
        "offense.embezzlement",
        "offense.stolen_property_custody",
        "condition.test",
        occurrence_constraint=ORDERED_CROSS_EPISODE,
    )
    # 횡령이 보관보다 앞선다 -- 사후행위가 아니다.
    reversed_episodes = {custody: "factual_episode:002", embezzlement: "factual_episode:001"}
    order = ("factual_episode:001", "factual_episode:002")
    assert (
        plan_concurrence_candidates(
            (custody, embezzlement),
            episode_by_instance=reversed_episodes,
            rules=(rule,),
            factual_episode_order=order,
        )
        == ()
    )

    # 선언된 순서에 없는 episode는 비교하지 않는다.
    assert (
        plan_concurrence_candidates(
            (custody, embezzlement),
            episode_by_instance={custody: "factual_episode:001", embezzlement: "factual_episode:009"},
            rules=(rule,),
            factual_episode_order=order,
        )
        == ()
    )


def test_the_stolen_property_absorption_rule_is_approved_and_ordered() -> None:
    """설치된 규칙이 실제로 그 제약을 쓰는지 -- 저작만 하고 same_episode로 남으면 무의미하다."""
    from pathlib import Path

    from idpr.v2.runtime.concurrence import ORDERED_CROSS_EPISODE, load_concurrence_rules

    root = Path(__file__).resolve().parents[1]
    rules = {rule.rule_id: rule for rule in load_concurrence_rules(root / "data/v2/concurrence_rules.yaml")}
    rule = rules["absorption.embezzlement_by_stolen_property_custody"]

    assert rule.occurrence_constraint == ORDERED_CROSS_EPISODE
    assert rule.first_offense_ref == "offense.embezzlement"
    assert rule.second_offense_ref == "offense.stolen_property_custody"


def test_three_node_absorption_cycle_is_rejected_as_one_conflict() -> None:
    from idpr.v2.runtime.concurrence import ConcurrenceCandidate

    first = _instance('offense.injury', 'binding:cycle-a')
    second = _instance('offense.homicide', 'binding:cycle-b')
    third = _instance('offense.robbery', 'binding:cycle-c')
    rules = (
        ConcurrenceRule(
            'rule.cycle-a', ABSORPTION, first.offense_ref, second.offense_ref, 'condition.a'
        ),
        ConcurrenceRule(
            'rule.cycle-b', ABSORPTION, second.offense_ref, third.offense_ref, 'condition.b'
        ),
        ConcurrenceRule(
            'rule.cycle-c', ABSORPTION, third.offense_ref, first.offense_ref, 'condition.c'
        ),
    )
    candidates = tuple(
        ConcurrenceCandidate(rule, child, parent, 'episode:1')
        for rule, child, parent in zip(
            rules,
            (first, second, third),
            (second, third, first),
            strict=True,
        )
    )
    truths = {
        (candidate.rule.rule_id, candidate.first, candidate.second): TRUE
        for candidate in candidates
    }

    result = resolve_concurrence(
        (first, second, third), candidates, condition_truths=truths
    )

    assert result.absorbed_instances == frozenset()
    assert result.retained_instances == frozenset({first, second, third})
    assert set(result.rejected_conflicts) == set(candidates)
    assert set(result.unresolved_candidates) == set(candidates)
    assert result.absorbed_into == ()


def test_acyclic_absorption_chain_still_applies_transitively_as_authored_edges() -> None:
    from idpr.v2.runtime.concurrence import ConcurrenceCandidate

    first = _instance('offense.injury', 'binding:chain-a')
    second = _instance('offense.homicide', 'binding:chain-b')
    third = _instance('offense.robbery', 'binding:chain-c')
    rules = (
        ConcurrenceRule(
            'rule.chain-a', ABSORPTION, first.offense_ref, second.offense_ref, 'condition.a'
        ),
        ConcurrenceRule(
            'rule.chain-b', ABSORPTION, second.offense_ref, third.offense_ref, 'condition.b'
        ),
    )
    candidates = (
        ConcurrenceCandidate(rules[0], first, second, 'episode:1'),
        ConcurrenceCandidate(rules[1], second, third, 'episode:1'),
    )
    truths = {
        (candidate.rule.rule_id, candidate.first, candidate.second): TRUE
        for candidate in candidates
    }

    result = resolve_concurrence(
        (first, second, third), candidates, condition_truths=truths
    )

    assert result.absorbed_instances == frozenset({first, second})
    assert result.retained_instances == frozenset({third})
    assert result.rejected_conflicts == ()
    assert result.absorbed_into == ((first, second), (second, third))
