"""Step 7 caller routes must remain source-derived and cross-offense safe."""

from __future__ import annotations

from pathlib import Path

import pytest

from idpr.v2.closure import compile_candidate_offenses, compile_closure
from idpr.v2.evaluate import TRUE
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.completion import CompletionResult
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.orchestration import (
    OrchestrationError,
    resolve_article_263_from_participation_probe,
    resolve_cross_offense_derivative_route,
)
from idpr.v2.runtime.pipeline import resolve_liability
from idpr.v2.runtime.truths import CaseTruths

_PRODUCTION = Path(__file__).resolve().parents[1] / "data/v2/definitions"


def _completed() -> CompletionResult:
    return CompletionResult(state="completed", punishable=True)


def test_c33b_route_preserves_caller_selected_cross_offense_target() -> None:
    registry = load_definitions(_PRODUCTION)
    closure = compile_closure(registry, {"offense.homicide", "offense.ancestral_homicide"})
    compiled = compile_candidate_offenses(registry, closure)
    principal = OffenseInstanceKey("C1", "mother", "offense.homicide", "o1")
    target = OffenseInstanceKey("C1", "child", "offense.ancestral_homicide", "o1")
    truths = CaseTruths(predicate={
        (principal, "legal_element.natural_person_victim_status"): TRUE,
        (principal, "ground_fact.killing_conduct"): TRUE,
        (principal, "ground_fact.death_of_victim"): TRUE,
        (principal, "legal_element.result_causation"): TRUE,
        (principal, "legal_element.intent"): TRUE,
        (target, "legal_element.instigator_intent"): TRUE,
    })
    principal_evaluation = resolve_liability(
        registry, compiled[principal.offense_ref], principal, _completed(), frozenset(), truths
    )

    evaluation = resolve_cross_offense_derivative_route(
        registry, closure, compiled, "instigator", principal_evaluation, target, frozenset(), truths
    )

    assert principal_evaluation.realization is not None
    assert evaluation.instance == target
    assert evaluation.instance.offense_ref == "offense.ancestral_homicide"
    assert evaluation.liability_result is not None


def test_c33b_route_rejects_a_target_that_is_not_active_or_a_surviving_candidate() -> None:
    registry = load_definitions(_PRODUCTION)
    closure = compile_closure(registry, {"offense.homicide"})
    compiled = compile_candidate_offenses(registry, closure)
    principal = OffenseInstanceKey("C1", "mother", "offense.homicide", "o1")
    target = OffenseInstanceKey("C1", "child", "offense.ancestral_homicide", "o1")
    evaluation = resolve_liability(
        registry,
        compiled[principal.offense_ref],
        principal,
        _completed(),
        frozenset(),
        CaseTruths(),
    )

    with pytest.raises(OrchestrationError, match="target offense"):
        resolve_cross_offense_derivative_route(
            registry, closure, compiled, "instigator", evaluation, target, frozenset(), CaseTruths()
        )


def test_discovered_probe_candidate_requires_explicit_conditional_activation() -> None:
    registry = load_definitions(_PRODUCTION)
    closure = compile_closure(registry, {"offense.homicide"})
    compiled = compile_candidate_offenses(registry, closure)
    candidate_ref = "derived_offense.robbery_causing_intentional_homicide"
    assert candidate_ref in closure.candidate_offense_refs
    assert candidate_ref not in closure.mandatory_offense_refs

    principal = OffenseInstanceKey("C1", "mother", "offense.homicide", "o1")
    target = OffenseInstanceKey("C1", "child", candidate_ref, "o1")
    truths = CaseTruths(predicate={
        (principal, "legal_element.natural_person_victim_status"): TRUE,
        (principal, "ground_fact.killing_conduct"): TRUE,
        (principal, "ground_fact.death_of_victim"): TRUE,
        (principal, "legal_element.result_causation"): TRUE,
        (principal, "legal_element.intent"): TRUE,
        (target, "legal_element.instigator_intent"): TRUE,
    })
    principal_evaluation = resolve_liability(
        registry, compiled[principal.offense_ref], principal, _completed(), frozenset(), truths
    )

    with pytest.raises(OrchestrationError, match="target offense"):
        resolve_cross_offense_derivative_route(
            registry, closure, compiled, "instigator", principal_evaluation, target, frozenset(), truths
        )

    evaluation = resolve_cross_offense_derivative_route(
        registry,
        closure,
        compiled,
        "instigator",
        principal_evaluation,
        target,
        frozenset(),
        truths,
        conditionally_active_offense_refs={candidate_ref},
    )
    assert evaluation.instance == target


def test_article_263_probe_calls_only_the_dedicated_runtime_after_true_survival() -> None:
    registry = load_definitions(_PRODUCTION)
    closure = compile_closure(registry, {"offense.injury"})
    compiled = compile_candidate_offenses(registry, closure)
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

    evaluation = resolve_article_263_from_participation_probe(
        registry, closure, compiled, instance, _completed(), frozenset(), truths
    )

    assert evaluation is not None
    assert evaluation.instance.offense_ref == "offense.injury"
    assert evaluation.liability_result is not None


def test_article_263_probe_does_not_fall_back_to_attribution_when_not_true() -> None:
    registry = load_definitions(_PRODUCTION)
    closure = compile_closure(registry, {"offense.injury"})
    compiled = compile_candidate_offenses(registry, closure)
    instance = OffenseInstanceKey("C1", "actor", "offense.injury", "o1")

    assert resolve_article_263_from_participation_probe(
        registry, closure, compiled, instance, _completed(), frozenset(), CaseTruths()
    ) is None
