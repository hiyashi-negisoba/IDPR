from __future__ import annotations

from pathlib import Path

from idpr.v2.compile import CompiledOffense, compile_offense
from idpr.v2.evaluate import FALSE, TRUE
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.completion import completion_policy_for, resolve_completion
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.truths import CaseTruths

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = load_definitions(ROOT / "data/v2/definitions")


def _resolve(offense_ref: str, values: dict[str, str]):
    compiled = compile_offense(REGISTRY, offense_ref)
    assert isinstance(compiled, CompiledOffense)
    instance = OffenseInstanceKey("case", "actor", offense_ref, "occurrence")
    truths = CaseTruths(
        predicate={(instance, ref): truth for ref, truth in values.items()}
    )
    return resolve_completion(
        completion_policy_for(REGISTRY, offense_ref), compiled, instance, truths
    )


def test_kcl_completion_slice_is_authored() -> None:
    expected = {
        "offense.homicide",
        "offense.ancestral_homicide",
        "offense.rape",
        "offense.quasi_rape",
        "offense.theft",
        "derived_offense.special_theft",
        "offense.injury",
        "offense.robbery",
        "offense.extortion",
        "derived_offense.quasi_robbery",
    }
    assert all(completion_policy_for(REGISTRY, ref) is not None for ref in expected)


def test_homicide_attempt_is_not_a_completed_fallback() -> None:
    result = _resolve(
        "offense.homicide",
        {
            "ground_fact.death_of_victim": FALSE,
            "legal_element.commencement_of_execution": TRUE,
            "ground_fact.means_or_object_defect": FALSE,
            "legal_element.voluntary_cessation_or_prevention": FALSE,
        },
    )
    assert result.state == "attempted"
    assert result.suspended_slots == frozenset({"result", "causation"})


def test_quasi_rape_actual_status_absence_can_resolve_as_impossible_attempt() -> None:
    result = _resolve(
        "offense.quasi_rape",
        {
            "legal_element.mental_incapacity_or_physical_helplessness_status": FALSE,
            "ground_fact.vaginal_intercourse_conduct": TRUE,
            "legal_element.commencement_of_execution": TRUE,
            "ground_fact.means_or_object_defect": TRUE,
            "legal_element.dangerousness": TRUE,
        },
    )
    assert result.state == "impossible_attempt"
    assert result.suspended_slots == frozenset({"object", "circumstance"})


def test_robbery_preparation_requires_positive_preparation_not_failed_completion() -> None:
    result = _resolve(
        "offense.robbery",
        {
            "ground_fact.taking_conduct": FALSE,
            "legal_element.commencement_of_execution": FALSE,
            "legal_element.preparatory_conduct": TRUE,
            "legal_element.conspiracy_agreement": FALSE,
        },
    )
    assert result.state == "preparation"
    assert result.punishable is True
    assert result.suspended_slots == frozenset({"conduct"})


def test_dangerless_impossible_conduct_is_not_labeled_punishable_attempt() -> None:
    result = _resolve(
        "offense.injury",
        {
            "legal_element.injury_result": FALSE,
            "legal_element.commencement_of_execution": TRUE,
            "ground_fact.means_or_object_defect": TRUE,
            "legal_element.dangerousness": FALSE,
        },
    )
    assert result.state == "not_applicable"
    assert result.punishable is None


def test_extortion_attempt_uses_threat_without_property_disposition() -> None:
    result = _resolve(
        "offense.extortion",
        {
            "legal_element.fear_inducement": TRUE,
            "legal_element.property_disposition": FALSE,
        },
    )
    assert result.state == "attempted"
    assert result.suspended_slots == frozenset({"circumstance"})


def test_quasi_robbery_attempt_follows_failed_taking_plus_robbery_violence() -> None:
    result = _resolve(
        "derived_offense.quasi_robbery",
        {
            "ground_fact.taking_conduct": FALSE,
            "legal_element.robbery_level_violence": TRUE,
        },
    )
    assert result.state == "attempted"
    assert result.suspended_slots == frozenset()
    assert result.component_suspended_slots == {
        "theft_part": frozenset({"conduct"})
    }
