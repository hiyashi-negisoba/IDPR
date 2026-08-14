"""Firing conditions for the authored definitional resolutions.

Removing `not(injury_intent)` / `not(homicide_intent)` from the result-aggravated offences let
them be evaluated on their own elements, which is correct but leaves the intentional sibling
standing beside them.  These rules are what keeps that from becoming double liability, and they
are definitional: establishment of the displacing offence is the whole ground, so nothing here
asks the case text a second time about an intent the sibling's elements already decided.

The gate that matters most is `same_realization`.  One episode can hold the same actor injuring
one victim and killing another, and joining on the episode alone would delete a conviction earned
by different conduct.
"""

from __future__ import annotations

from pathlib import Path

from idpr.v2.runtime.concurrence import (
    ALTERNATIVE_SUBTYPE,
    DEFINITIONAL_RESOLUTION,
    INTENT_DISPLACEMENT,
    load_concurrence_rules,
    plan_concurrence_candidates,
    resolve_concurrence,
)
from idpr.v2.runtime.identity import OffenseInstanceKey

ROOT = Path(__file__).resolve().parents[1]
RULES = load_concurrence_rules(ROOT / "data/v2/concurrence_rules.yaml")
DEFINITIONAL = tuple(rule for rule in RULES if rule.kind == DEFINITIONAL_RESOLUTION)

CASE = "case"
EPISODE = "factual_episode:001"
FOCAL = "factual_action:001:002"
OTHER_FOCAL = "factual_action:001:005"

AGGRAVATED = "derived_offense.robbery_causing_injury_by_aggravated_result"
INTENTIONAL = "derived_offense.robbery_causing_intentional_injury"


def _instance(offense_ref: str, actor: str = "甲", occurrence: str = "realization:001"):
    return OffenseInstanceKey(CASE, actor, offense_ref, occurrence)


def _resolve(instances, focal_by_instance):
    candidates = plan_concurrence_candidates(
        instances,
        episode_by_instance={instance: EPISODE for instance in instances},
        rules=DEFINITIONAL,
        focal_action_by_instance=focal_by_instance,
    )
    return candidates, resolve_concurrence(instances, candidates, condition_truths={})


def test_both_doctrinal_types_are_authored_and_approved() -> None:
    types = {rule.resolution_type for rule in DEFINITIONAL}
    assert types == {ALTERNATIVE_SUBTYPE, INTENT_DISPLACEMENT}
    assert all(not rule.condition_statement for rule in DEFINITIONAL)


def test_intentional_subtype_displaces_the_result_aggravated_one() -> None:
    aggravated = _instance(AGGRAVATED)
    intentional = _instance(INTENTIONAL, occurrence="realization:002")
    instances = (aggravated, intentional)

    candidates, resolution = _resolve(
        instances, {aggravated: FOCAL, intentional: FOCAL}
    )

    assert len(candidates) == 1
    assert resolution.absorbed_instances == frozenset({aggravated})
    assert intentional in resolution.retained_instances
    assert not resolution.unresolved_candidates


def test_confirmed_homicide_displaces_injury_causing_death() -> None:
    aggravated = _instance("derived_offense.injury_causing_death")
    homicide = _instance("offense.homicide", occurrence="realization:002")
    instances = (aggravated, homicide)

    _candidates, resolution = _resolve(instances, {aggravated: FOCAL, homicide: FOCAL})

    assert resolution.absorbed_instances == frozenset({aggravated})


def test_separate_conduct_in_one_episode_is_not_displaced() -> None:
    """The same_realization gate: different focal actions are different conduct."""
    aggravated = _instance(AGGRAVATED)
    intentional = _instance(INTENTIONAL, occurrence="realization:002")
    instances = (aggravated, intentional)

    candidates, resolution = _resolve(
        instances, {aggravated: FOCAL, intentional: OTHER_FOCAL}
    )

    assert not candidates
    assert not resolution.absorbed_instances


def test_another_actors_intentional_offense_never_displaces_this_one() -> None:
    aggravated = _instance(AGGRAVATED, actor="甲")
    intentional = _instance(INTENTIONAL, actor="乙", occurrence="realization:002")
    instances = (aggravated, intentional)

    candidates, resolution = _resolve(
        instances, {aggravated: FOCAL, intentional: FOCAL}
    )

    assert not candidates
    assert not resolution.absorbed_instances


def test_result_aggravated_offense_stands_alone_when_no_intentional_sibling_is_established() -> None:
    """The point of removing the negative gate: it must survive an unproven intent."""
    aggravated = _instance(AGGRAVATED)

    candidates, resolution = _resolve((aggravated,), {aggravated: FOCAL})

    assert not candidates
    assert resolution.retained_instances == frozenset({aggravated})
