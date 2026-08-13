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
