"""Axis 8 (checks/completion.py) -- completion policy well-formedness.

The gate that matters: a state which suspends anything must dispose of EVERY relation instance of
its offense. No affectedness inference is attempted, so the tests below pin both directions --
coverage is demanded when suspensions exist, and demanded of nobody when they do not.
"""

from __future__ import annotations

from idpr.v2.checks.completion import check_completion
from idpr.v2.registry import DefinitionEntry, DefinitionRegistry, load_definitions

_ROBBERY_HOMICIDE = "derived_offense.robbery_homicide"
_INJURY = "offense.injury"

_RETAIN_OCCASION = {
    "relation": "relation.occasion_identity",
    "left": "robbery_part",
    "right": "homicide_part",
    "disposition": "retain",
}


def _codes(registry: DefinitionRegistry) -> list[str]:
    return [finding.code for finding in check_completion(registry)]


def _with_policy(policy_id: str, offense: str, states: dict) -> DefinitionRegistry:
    """Replace (or add) one completion policy, leaving the rest of the real corpus intact."""
    registry = load_definitions()
    replacement = DefinitionEntry(
        id=policy_id,
        kind="completion_policy",
        payload={"id": policy_id, "offense": offense, "states": states},
        source_file="<synthetic>",
    )
    policies = tuple(e for e in registry.by_kind["completion_policy"] if e.id != policy_id)
    by_kind = {**registry.by_kind, "completion_policy": policies + (replacement,)}
    return DefinitionRegistry(
        by_id={**registry.by_id, policy_id: replacement}, by_kind=by_kind
    )


def _homicide_policy(attempted: dict) -> DefinitionRegistry:
    return _with_policy(
        "completion_policy.robbery_homicide",
        _ROBBERY_HOMICIDE,
        {
            "completed": {
                "when": {"op": "ref", "ref": "ground_fact.death_of_victim"},
                "punishable": True,
            },
            "attempted": attempted,
        },
    )


def test_real_corpus_is_axis_8_clean() -> None:
    assert check_completion(load_definitions()) == []


# --------------------------------------------------------------------------------------------
# relation disposition coverage -- the core gate
# --------------------------------------------------------------------------------------------


def test_state_with_suspends_requires_a_disposition_for_every_relation() -> None:
    """Silence is not consent. Leaving a relation undisposed is refused, not defaulted to retain.

    Defaulting either way would be the checker making a legal judgement (does 기회의 동일성 survive
    the attempt?) that only the author can make.
    """
    registry = _homicide_policy({
        "when": {"op": "ref", "ref": "ground_fact.attempt_commencement"},
        "punishable": True,
        "suspends": ["result", "causation"],
    })

    assert "completion_relation_disposition_missing" in _codes(registry)


def test_state_without_suspends_needs_no_disposition() -> None:
    """A state that removes no obligation retains every relation, so nothing needs authoring."""
    registry = _homicide_policy({
        "when": {"op": "ref", "ref": "ground_fact.attempt_commencement"},
        "punishable": True,
    })

    assert _codes(registry) == []


def test_full_coverage_passes_whichever_disposition_was_chosen() -> None:
    """`retain` and `suspend` are equally acceptable -- the check is that a human chose one."""
    for disposition in ("retain", "suspend"):
        registry = _homicide_policy({
            "when": {"op": "ref", "ref": "ground_fact.attempt_commencement"},
            "punishable": True,
            "suspends": ["result", "causation"],
            "relations": [{**_RETAIN_OCCASION, "disposition": disposition}],
        })

        assert _codes(registry) == [], disposition


def test_disposition_that_matches_no_relation_instance_is_reported() -> None:
    registry = _homicide_policy({
        "when": {"op": "ref", "ref": "ground_fact.attempt_commencement"},
        "punishable": True,
        "suspends": ["result", "causation"],
        "relations": [{**_RETAIN_OCCASION, "left": "nonexistent_part"}],
    })
    codes = _codes(registry)

    assert "completion_relation_disposition_unresolved" in codes
    # and the real instance is still reported as undisposed -- a wrong entry does not cover it
    assert "completion_relation_disposition_missing" in codes


def test_duplicate_disposition_for_one_relation_is_reported() -> None:
    registry = _homicide_policy({
        "when": {"op": "ref", "ref": "ground_fact.attempt_commencement"},
        "punishable": True,
        "suspends": ["result", "causation"],
        "relations": [_RETAIN_OCCASION, {**_RETAIN_OCCASION, "disposition": "suspend"}],
    })

    assert "completion_relation_disposition_duplicate" in _codes(registry)


# --------------------------------------------------------------------------------------------
# suspends sanity
# --------------------------------------------------------------------------------------------


def test_suspending_a_slot_the_offense_does_not_author_is_reported() -> None:
    """A no-op suspension is almost always the wrong slot name or the wrong offense."""
    registry = _with_policy(
        "completion_policy.injury",
        _INJURY,
        {
            "completed": {
                "when": {"op": "ref", "ref": "ground_fact.injury_occurred"},
                "punishable": True,
            },
            "attempted": {
                "when": {"op": "ref", "ref": "ground_fact.attempt_commencement"},
                "punishable": True,
                "suspends": ["causation"],  # offense.injury authors no causation obligation
            },
        },
    )

    assert "completion_suspends_unauthored_slot" in _codes(registry)


def test_completed_state_may_not_suspend_anything() -> None:
    registry = _homicide_policy({
        "when": {"op": "ref", "ref": "ground_fact.attempt_commencement"},
        "punishable": True,
    })
    policy = registry.by_id["completion_policy.robbery_homicide"]
    policy.payload["states"]["completed"]["suspends"] = ["result"]

    assert "completion_completed_state_suspends" in _codes(registry)


def test_suspending_a_slot_several_components_contribute_to_is_refused() -> None:
    """강도강간미수 shape: `conduct` carries both offences' contributions in one flattened slot.

    Occurrence-scoped suspension is not implemented, so "suspend the rape part's conduct" cannot be
    expressed -- suspending `conduct` would silently drop the robbery conduct too. The checker
    refuses rather than running a program the author could not have meant.
    """
    registry = _with_policy(
        "completion_policy.robbery_rape",
        "derived_offense.robbery_rape",
        {
            "completed": {
                "when": {"op": "ref", "ref": "ground_fact.forcible_intercourse"},
                "punishable": True,
            },
            "attempted": {
                "when": {"op": "ref", "ref": "ground_fact.attempt_commencement"},
                "punishable": True,
                "suspends": ["conduct"],
                "relations": [{
                    "relation": "relation.occasion_identity",
                    "left": "robbery_part",
                    "right": "rape_part",
                    "disposition": "retain",
                }],
            },
        },
    )

    assert "completion_unsupported_slot_suspension" in _codes(registry)


# --------------------------------------------------------------------------------------------
# state declaration
# --------------------------------------------------------------------------------------------


def test_missing_completed_state_is_reported() -> None:
    """`completed` as "whatever is left over" would be a default ordering -- the one section 14 bans."""
    registry = _with_policy(
        "completion_policy.injury",
        _INJURY,
        {
            "attempted": {
                "when": {"op": "ref", "ref": "ground_fact.attempt_commencement"},
                "punishable": True,
            }
        },
    )

    assert "completion_completed_state_missing" in _codes(registry)


def test_two_states_with_identical_conditions_are_reported() -> None:
    """The one statically decidable overlap: indistinguishable states can only yield `unresolved`."""
    registry = _with_policy(
        "completion_policy.injury",
        _INJURY,
        {
            "completed": {
                "when": {"op": "ref", "ref": "ground_fact.injury_occurred"},
                "punishable": True,
            },
            "attempted": {
                "when": {"op": "ref", "ref": "ground_fact.injury_occurred"},
                "punishable": True,
            },
        },
    )

    assert "completion_duplicate_state_condition" in _codes(registry)


def test_two_policies_may_not_govern_one_offense() -> None:
    registry = load_definitions()
    duplicate = DefinitionEntry(
        id="completion_policy.injury_second",
        kind="completion_policy",
        payload={
            "id": "completion_policy.injury_second",
            "offense": _INJURY,
            "states": {
                "completed": {
                    "when": {"op": "ref", "ref": "ground_fact.injury_occurred"},
                    "punishable": True,
                }
            },
        },
        source_file="<synthetic>",
    )
    by_kind = dict(registry.by_kind)
    by_kind["completion_policy"] = by_kind["completion_policy"] + (duplicate,)
    extended = DefinitionRegistry(
        by_id={**registry.by_id, duplicate.id: duplicate}, by_kind=by_kind
    )

    assert "completion_policy_offense_already_governed" in _codes(extended)
