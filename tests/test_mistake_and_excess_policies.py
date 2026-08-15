"""The 2026-08-13 legal review settled four things that are easy to regress silently.

Each of them is a decision about what the host is *not* allowed to conclude, so none of them
shows up as a failing assertion elsewhere -- a regression just quietly produces more answers.
"""

from pathlib import Path

import pytest

from idpr.v2.checks.references import check_references
from idpr.v2.registry import DefinitionEntry, RegistryError, load_definitions
from idpr.v2.schema import schema_errors

DEFINITIONS = Path("data/v2/definitions")


@pytest.fixture(scope="module")
def registry():
    return load_definitions(DEFINITIONS)


def test_definitions_load_and_every_reference_resolves(registry) -> None:
    assert check_references(registry) == []
    assert len(registry.by_kind["mistake_policy"]) == 1
    assert len(registry.by_kind["excess_policy"]) == 1


def test_korean_law_profile_fixes_statutory_conformity(registry) -> None:
    """검수 ①-a: symbolic result is not left unresolved for same-offense divergence."""
    policy = registry.get("mistake_policy.korean_law_concrete_fact")
    assert policy.payload["profile"] == "korean_law"
    assert policy.payload["scope"] == "same_statutory_offense"
    effects = policy.payload["effects"]
    assert effects["object_misidentification"] == "intent_preserved"
    assert effects["method_divergence"] == "intent_preserved"


def test_mistaken_justifying_circumstance_sits_on_culpability(registry) -> None:
    """검수 ①-c: 판례형 정당한 이유 법리이므로 책임 단계다. Elements로 옮기면 고의 조각이 된다."""
    doctrine = registry.get("doctrine.mistaken_justifying_circumstance")
    assert doctrine.payload["stage"] == "culpability"
    assert doctrine.payload["effect"] == {"effect": "DEFEAT", "stage": "culpability"}


def test_article_33_proviso_names_the_aggravated_offense_and_keeps_co_principal(registry) -> None:
    """검수 ②-a/②-b: the accessory's own realization is the aggravated offense, and 제33조는
    제30조부터 제32조까지를 대상으로 하므로 co_principal이 빠지면 안 된다."""
    offense = registry.get("offense.ancestral_homicide")
    proviso = offense.payload["participation_constraints"]["aggravating_status_participation"]
    assert proviso["base_offense_ref"] == "offense.homicide"
    assert proviso["status_ref"] == "legal_element.lineal_ascendant_of_self_or_spouse_status"
    assert set(proviso["applies_to_modes"]) == {"instigator", "aider", "co_principal"}
    # The status leaf must be one this offense already uses, not a new one invented for 제33조.
    assert offense.payload["elements"]["object"]["ref"] == proviso["status_ref"]


def test_absent_derivation_is_unresolved_rather_than_qualitative_excess(registry) -> None:
    """검수 ③-a, the load-bearing one. 저작되지 않은 구조관계를 '무관하다'로 읽으면 안 된다."""
    policy = registry.get("excess_policy.korean_law_standard")
    assert policy.payload["unresolved_marker"] == "UNRESOLVED_EXCESS_RELATION"
    assert (
        policy.payload["qualitative"]["condition"] == "authored_incompatible_relation_present"
    )
    authored_pairs = {
        (pair["instigated_offense_ref"], pair["realized_offense_ref"])
        for pair in policy.payload["incompatible_offense_pairs"]
    }
    assert ("offense.theft", "offense.injury") in authored_pairs
    # 2026-08-15: 폭행치상이 저작되어 甲 갈래의 pair가 들어왔다. 지키는 것은 그대로다 --
    # pair는 **명시적으로 저작된 조합**에서만 나오고, derivation이 없다는 사실 자체가 질적
    # 초과의 근거가 되지는 않는다.
    assert ("offense.theft", "derived_offense.assault_causing_injury") in authored_pairs
    assert all(
        instigated == "offense.theft" for instigated, _realized in authored_pairs
    ), authored_pairs


def test_result_aggravated_excess_branches_on_the_participants_own_foreseeability(registry) -> None:
    """검수 ③-b: 양적 초과에 instigated scope를 일률 적용하지 않는다."""
    aggravated = registry.get("excess_policy.korean_law_standard").payload["quantitative"][
        "result_aggravated"
    ]
    assert aggravated["foreseeability_ref"] == (
        "legal_element.foreseeability_of_aggravated_result_by_participant"
    )
    assert aggravated["on_true"] == "liable_for_aggravated_result"
    assert aggravated["on_false"] == "liable_for_instigated_scope"
    assert aggravated["on_unknown"] == "unresolved"


def test_qualitative_excess_cannot_be_authored_as_derivation_absence() -> None:
    """The schema, not just the fixture, is what forbids the rejected rule."""
    errors = schema_errors(
        "excess_policy",
        {
            "id": "excess_policy.bad",
            "profile": "korean_law",
            "quantitative": {
                "condition": "realized_offense_derives_from_instigated_offense",
                "ordinary_qualification_effect": "liable_for_instigated_scope",
                "result_aggravated": {
                    "foreseeability_ref": "legal_element.x",
                    "on_true": "liable_for_aggravated_result",
                    "on_false": "liable_for_instigated_scope",
                    "on_unknown": "unresolved",
                },
            },
            "qualitative": {
                "condition": "no_derivation_between_offenses",
                "effect": "no_liability_for_excess",
            },
            "unresolved_marker": "UNRESOLVED_EXCESS_RELATION",
        },
    )
    assert any("qualitative.condition" in message for message in errors)


def test_a_mistake_policy_must_cover_both_divergence_kinds() -> None:
    """Authoring only one branch would let the other kind of 착오 pass in silence, which is not
    the same thing as concluding the intent is absent."""
    errors = schema_errors(
        "mistake_policy",
        {
            "id": "mistake_policy.half",
            "profile": "korean_law",
            "scope": "same_statutory_offense",
            "divergence_relation": "relation.intended_object_divergence",
            "divergence_kind_ref": "legal_element.object_misidentification",
            "effects": {"object_misidentification": "intent_preserved"},
            "authority_refs": [{"authority_basis": "statute_text", "citation": "형법 제13조"}],
        },
    )
    assert any("method_divergence" in message for message in errors)
