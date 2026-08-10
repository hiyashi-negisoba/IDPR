"""Focused Phase 5.1 regressions over the production Definition Layer."""

from __future__ import annotations

from pathlib import Path

import pytest

from idpr.v2 import compile as compilemod
from idpr.v2.checks import run_type_checks
from idpr.v2.evaluate import FALSE, TRUE, UNKNOWN
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.completion import CompletionResult
from idpr.v2.runtime.completion import component_instance_for, completion_policy_for, resolve_completion
from idpr.v2.runtime.identity import OffenseInstanceKey, RuntimeRelationKey
from idpr.v2.runtime.participation import (
    resolve_co_principal_liability,
    resolve_indirect_principal_liability,
)
from idpr.v2.runtime.pipeline import resolve_liability
from idpr.v2.runtime.stages import (
    Article151OffenderStatusObligation,
    CoPrincipalConstitutiveStatusObligation,
    IndirectPrincipalDependencyObligation,
    LiabilityEvaluation,
    OffenseRealization,
    StageResult,
    StatutoryDeemingObligation,
    not_reached,
)
from idpr.v2.runtime.statutory import (
    Article151QualifyingLink,
    resolve_article_151_liability,
    resolve_article_263_deemed_liability,
)
from idpr.v2.runtime.truths import CaseTruths
from idpr.v2.relations import iter_relation_instances

_PRODUCTION = Path(__file__).resolve().parents[1] / "data/v2/definitions"


def _registry():
    registry = load_definitions(_PRODUCTION)
    assert run_type_checks(registry) == []
    return registry


def _compiled(registry, ref: str):
    compiled = compilemod.compile_offense(registry, ref)
    assert isinstance(compiled, compilemod.CompiledOffense), compiled
    return compiled


def _completed() -> CompletionResult:
    return CompletionResult(state="completed", punishable=True)


def _failed_utilised(instance: OffenseInstanceKey, stage: str) -> LiabilityEvaluation:
    satisfied = StageResult(evaluation_state="evaluated", legal_state="satisfied", gate_state="passes")
    failed_elements = StageResult(evaluation_state="evaluated", legal_state="failed", gate_state="fails")
    failed_unlawfulness = StageResult(
        evaluation_state="evaluated", legal_state="defeated", gate_state="fails"
    )
    failed_culpability = StageResult(
        evaluation_state="evaluated", legal_state="defeated", gate_state="fails"
    )
    if stage == "elements":
        return LiabilityEvaluation(
            instance=instance, completion=_completed(), elements=failed_elements,
            unlawfulness=not_reached(), culpability=not_reached(), punishability=not_reached(),
        )
    if stage == "unlawfulness":
        return LiabilityEvaluation(
            instance=instance, completion=_completed(), elements=satisfied,
            unlawfulness=failed_unlawfulness, culpability=not_reached(), punishability=not_reached(),
        )
    realization = OffenseRealization(instance=instance, elements=satisfied, unlawfulness=satisfied)
    return LiabilityEvaluation(
        instance=instance, completion=_completed(), elements=satisfied, unlawfulness=satisfied,
        culpability=failed_culpability, punishability=not_reached(), realization=realization,
    )


def test_c33a_status_is_an_elements_source_not_a_case_truth_merge():
    registry = _registry()
    ref = "offense.obstruction_of_right_exercise"
    target = OffenseInstanceKey("C1", "non_owner", ref, "o1")
    owner = OffenseInstanceKey("C1", "owner", ref, "o1")
    truths = CaseTruths(predicate={
        (target, "legal_element.own_property_object"): FALSE,
        (owner, "legal_element.own_property_object"): TRUE,
        (target, "legal_element.third_party_possession_or_right_object"): TRUE,
        (target, "legal_element.obstruction_of_right_exercise"): TRUE,
        (target, "legal_element.taking_of_own_property_conduct"): FALSE,
        (owner, "legal_element.taking_of_own_property_conduct"): TRUE,
    })

    evaluation = resolve_co_principal_liability(
        registry, _compiled(registry, ref), ref, target, [owner], _completed(), frozenset(), truths
    )

    assert truths.predicate[(target, "legal_element.own_property_object")] == FALSE
    assert evaluation.liability_result is not None
    status_outcomes = [
        outcome for outcome in evaluation.elements.provenance
        if isinstance(outcome.obligation, CoPrincipalConstitutiveStatusObligation)
    ]
    assert len(status_outcomes) == 1 and status_outcomes[0].truth == TRUE
    assert status_outcomes[0].obligation.satisfying_instances == (owner,)


def test_c151_linked_qualifying_result_supplies_its_leaf_and_absence_is_unresolved():
    registry = _registry()
    offender = OffenseInstanceKey("C1", "offender", "offense.injury", "o1")
    offender_truths = CaseTruths(predicate={
        (offender, "legal_element.natural_person_victim_status"): TRUE,
        (offender, "ground_fact.injury_conduct"): TRUE,
        (offender, "legal_element.injury_result"): TRUE,
        (offender, "legal_element.intent"): TRUE,
    })
    offender_evaluation = resolve_liability(
        registry, _compiled(registry, offender.offense_ref), offender, _completed(), frozenset(), offender_truths
    )
    assert offender_evaluation.liability_result is not None

    instance = OffenseInstanceKey("C1", "helper", "offense.harboring_or_escape", "o1")
    truths = CaseTruths(predicate={
        (instance, "legal_element.act_directed_at_another_offender"): TRUE,
        (instance, "legal_element.omission_requires_guarantor_status"): TRUE,
        (instance, "legal_element.for_the_offenders_benefit"): TRUE,
        (instance, "ground_fact.concealment_or_escape_conduct"): TRUE,
        (instance, "legal_element.intent"): TRUE,
    })
    compiled = _compiled(registry, instance.offense_ref)

    unresolved = resolve_article_151_liability(
        registry, compiled, instance, _completed(), frozenset(), truths, None
    )
    linked = resolve_article_151_liability(
        registry,
        compiled,
        instance,
        _completed(),
        frozenset(),
        truths,
        Article151QualifyingLink(offender_evaluation, "caller: fine-or-greater confirmed"),
    )

    assert unresolved.elements.gate_state == "unresolved"
    assert linked.liability_result is not None
    outcome = next(
        outcome for outcome in linked.elements.provenance
        if isinstance(outcome.obligation, Article151OffenderStatusObligation)
    )
    assert outcome.truth == TRUE
    assert outcome.obligation.linked_instance == offender
    assert outcome.obligation.qualification_provenance == "caller: fine-or-greater confirmed"


def test_c263_deems_liability_for_the_underlying_injury_identity_without_attribution():
    registry = _registry()
    instance = OffenseInstanceKey("C1", "actor", "offense.injury", "o1")
    truths = CaseTruths(predicate={
        (instance, "legal_element.natural_person_victim_status"): TRUE,
        (instance, "ground_fact.injury_conduct"): TRUE,
        (instance, "legal_element.injury_result"): TRUE,
        (instance, "legal_element.intent"): TRUE,
        (instance, "legal_element.concurrent_independent_acts"): TRUE,
        (instance, "legal_element.same_object_of_result"): TRUE,
        (instance, "legal_element.causal_origin_unascertained"): TRUE,
    })

    evaluation = resolve_article_263_deemed_liability(
        registry, _compiled(registry, instance.offense_ref), instance, _completed(), frozenset(), truths
    )

    assert evaluation.liability_result is not None
    assert evaluation.instance.offense_ref == "offense.injury"
    outcome = next(
        outcome for outcome in evaluation.elements.provenance
        if isinstance(outcome.obligation, StatutoryDeemingObligation)
    )
    assert outcome.truth == TRUE and outcome.obligation.underlying_instance == instance


def test_c34_runtime_path_distinguishes_each_proven_unpunished_outcome():
    registry = _registry()
    policy = registry.get("participation_policy.standard")
    user = OffenseInstanceKey("C1", "user", "offense.injury", "o1")
    agent = OffenseInstanceKey("C1", "agent", "offense.injury", "o1")
    truths = CaseTruths(predicate={(user, "legal_element.instigator_intent"): TRUE})

    expected = {
        "elements": "target_elements_failure",
        "unlawfulness": "unlawfulness_defeat",
        "culpability": "culpability_defeat_after_realization",
    }
    for stage, reason in expected.items():
        evaluation = resolve_indirect_principal_liability(
            registry, policy, "instigator", _failed_utilised(agent, stage), user, frozenset(), truths
        )
        dependency = next(
            outcome for outcome in evaluation.elements.provenance
            if isinstance(outcome.obligation, IndirectPrincipalDependencyObligation)
        )
        assert dependency.truth == TRUE and dependency.obligation.reason == reason
        assert evaluation.liability_result is not None

    negligence = OffenseInstanceKey("C1", "agent", "offense.negligent_homicide", "o1")
    negligence_truths = CaseTruths(predicate={
        (user, "legal_element.instigator_intent"): TRUE,
        (negligence, "ground_fact.death_of_victim"): TRUE,
        (negligence, "legal_element.result_causation"): TRUE,
        (negligence, "legal_element.duty_of_care"): TRUE,
        (negligence, "legal_element.foreseeability"): TRUE,
        (negligence, "legal_element.avoidability"): TRUE,
        (negligence, "legal_element.breach_of_duty"): TRUE,
    })
    negligence_evaluation = resolve_liability(
        registry, _compiled(registry, negligence.offense_ref), negligence, _completed(), frozenset(), negligence_truths
    )
    evaluation = resolve_indirect_principal_liability(
        registry,
        policy,
        "instigator",
        _failed_utilised(agent, "elements"),
        user,
        frozenset(),
        negligence_truths,
        negligence_evaluation=negligence_evaluation,
    )
    dependency = next(
        outcome for outcome in evaluation.elements.provenance
        if isinstance(outcome.obligation, IndirectPrincipalDependencyObligation)
    )
    assert negligence_evaluation.liability_result is not None
    assert dependency.truth == TRUE and dependency.obligation.reason == "different_negligence_offense"
    assert evaluation.liability_result is not None


def test_c339_component_instances_drive_when_and_scope_only_the_named_contribution():
    registry = _registry()
    ref = "derived_offense.robbery_rape"
    compiled = _compiled(registry, ref)
    policy = completion_policy_for(registry, ref)
    top = OffenseInstanceKey("C1", "actor", ref, "o1")
    robbery = component_instance_for(compiled, top, "robbery_part", "offense.robbery")
    rape = component_instance_for(compiled, top, "rape_part", "offense.rape")
    relation_key = next(iter_relation_instances(compiled))[0]

    completed_truths = CaseTruths(
        predicate={
            (rape, "legal_element.natural_person_victim_status"): TRUE,
            (rape, "legal_element.coercive_conduct"): TRUE,
            (rape, "ground_fact.vaginal_intercourse_conduct"): TRUE,
            (rape, "legal_element.directness_of_coercion_by_offender"): TRUE,
            (rape, "legal_element.coercion_sufficiency_for_rape"): TRUE,
            (rape, "legal_element.coercion_induced_sexual_act_causation"): TRUE,
            (rape, "legal_element.intent"): TRUE,
        },
        relation={RuntimeRelationKey(top, relation_key): TRUE},
    )
    completed = resolve_completion(policy, compiled, top, completed_truths)
    completed_evaluation = resolve_liability(
        registry, compiled, top, completed, frozenset(), completed_truths
    )
    assert completed.state == "completed"
    assert completed.provenance[0].component_instance == rape
    assert completed.component_suspended_slots == {
        "robbery_part": frozenset({"object", "conduct", "mental"})
    }
    assert completed_evaluation.liability_result is not None

    attempted_truths = CaseTruths(
        predicate={
            (robbery, "legal_element.possession"): TRUE,
            (robbery, "ground_fact.taking_conduct"): TRUE,
            (robbery, "legal_element.robbery_level_violence"): TRUE,
            (robbery, "legal_element.unlawful_appropriation_intent"): TRUE,
            (rape, "legal_element.natural_person_victim_status"): TRUE,
            (rape, "legal_element.directness_of_coercion_by_offender"): TRUE,
            (rape, "legal_element.coercion_sufficiency_for_rape"): TRUE,
            (rape, "legal_element.intent"): TRUE,
            (rape, "legal_element.commencement_of_execution"): TRUE,
            (rape, "ground_fact.vaginal_intercourse_conduct"): FALSE,
        },
        relation={RuntimeRelationKey(top, relation_key): TRUE},
    )
    attempted = resolve_completion(policy, compiled, top, attempted_truths)
    attempted_evaluation = resolve_liability(
        registry, compiled, top, attempted, frozenset(), attempted_truths
    )
    assert attempted.state == "attempted"
    assert attempted.provenance[1].component_instance == rape
    assert attempted.component_suspended_slots == {
        "rape_part": frozenset({"conduct", "causation"})
    }
    assert attempted_evaluation.liability_result is not None


@pytest.mark.parametrize(
    ("ref", "robbery_ref", "robbery_slots"),
    (
        ("derived_offense.robbery_rape", "offense.robbery", frozenset({"object", "conduct", "mental"})),
        (
            "derived_offense.special_robbery_rape",
            "derived_offense.special_robbery",
            frozenset({"object", "conduct", "circumstance", "mental"}),
        ),
        (
            "derived_offense.quasi_robbery_rape",
            "derived_offense.quasi_robbery",
            frozenset({"object", "conduct", "mental"}),
        ),
    ),
)
def test_c339_preserves_each_frozen_robbery_side_candidate(
    ref: str, robbery_ref: str, robbery_slots: frozenset[str]
):
    registry = _registry()
    compiled = _compiled(registry, ref)
    policy = completion_policy_for(registry, ref)
    top = OffenseInstanceKey("C1", "actor", ref, "o1")
    robbery = component_instance_for(compiled, top, "robbery_part", robbery_ref)
    rape = component_instance_for(compiled, top, "rape_part", "offense.rape")

    assert robbery.offense_ref == robbery_ref
    assert rape.offense_ref == "offense.rape"
    completed = resolve_completion(
        policy,
        compiled,
        top,
        CaseTruths(predicate={(rape, "ground_fact.vaginal_intercourse_conduct"): TRUE}),
    )
    assert completed.state == "completed"
    assert completed.component_suspended_slots == {"robbery_part": robbery_slots}
