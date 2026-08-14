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


def test_unstated_voluntary_cessation_no_longer_blocks_ordinary_attempt() -> None:
    """장애미수 must not require proof that 중지미수 did not happen.

    "자의로 중지하지 않았다" is never an affirmative case fact, so requiring its negation
    left every attempt permanently unresolved -- the defect that made `attempted` fire zero
    times across all 26 questions.
    """
    result = _resolve(
        "offense.homicide",
        {
            "legal_element.commencement_of_execution": TRUE,
            "ground_fact.death_of_victim": FALSE,
            "ground_fact.means_or_object_defect": FALSE,
            # 자의적 중지는 사실관계에 언급되지 않아 UNKNOWN으로 남는다.
        },
    )

    assert result.state == "attempted"
    assert result.punishable


def test_confirmed_voluntary_cessation_still_yields_abandoned_attempt() -> None:
    """The exception must remain exact: when it is TRUE the general state steps aside."""
    result = _resolve(
        "offense.homicide",
        {
            "legal_element.commencement_of_execution": TRUE,
            "ground_fact.death_of_victim": FALSE,
            "ground_fact.means_or_object_defect": FALSE,
            "legal_element.voluntary_cessation_or_prevention": TRUE,
        },
    )

    assert result.state == "abandoned_attempt"


def test_yielding_never_reads_unknown_as_a_negation() -> None:
    """A state only yields to a sibling that is independently TRUE.

    With the 기수 element unknown, neither state is confirmed and the policy stays unresolved
    rather than defaulting into the general attempt.
    """
    result = _resolve(
        "offense.homicide",
        {
            "legal_element.commencement_of_execution": TRUE,
            "ground_fact.means_or_object_defect": FALSE,
        },
    )

    assert result.state == "unresolved"


def test_unstated_means_defect_no_longer_blocks_ordinary_attempt() -> None:
    """제25조 장애미수 must not require proof that 제27조's defect did not occur.

    "수단·대상에 흠결이 없었다" is not written into a case, so demanding its negation left
    19 of the 30 unresolved completions structurally underivable.
    """
    result = _resolve(
        "offense.theft",
        {
            "legal_element.commencement_of_execution": TRUE,
            "ground_fact.taking_conduct": FALSE,
            # 수단·대상 흠결은 서술되지 않아 UNKNOWN으로 남는다.
        },
    )

    assert result.state == "attempted"


def test_confirmed_means_defect_blocks_the_ordinary_attempt() -> None:
    """A blocker excludes on confirmation, so a 불능미수 fact is never labelled 장애미수."""
    result = _resolve(
        "offense.theft",
        {
            "legal_element.commencement_of_execution": TRUE,
            "ground_fact.taking_conduct": FALSE,
            "ground_fact.means_or_object_defect": TRUE,
            # 위험성이 아직 미확정이므로 불능미수도 확정되지 않는다.
        },
    )

    assert result.state == "unresolved"


def test_confirmed_defect_with_danger_reaches_impossible_attempt() -> None:
    result = _resolve(
        "offense.theft",
        {
            "legal_element.commencement_of_execution": TRUE,
            "ground_fact.taking_conduct": FALSE,
            "ground_fact.means_or_object_defect": TRUE,
            "legal_element.dangerousness": TRUE,
        },
    )

    assert result.state == "impossible_attempt"
