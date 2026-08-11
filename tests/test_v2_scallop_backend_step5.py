"""Step 5 generic liability-chain parity and route-boundary tests."""

from pathlib import Path

import pytest

from idpr.v2 import compile as compilemod
from idpr.v2 import participation as participation_mod
from idpr.v2.registry import DefinitionEntry, load_definitions
from idpr.v2.runtime import completion, participation, pipeline
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.scallop_backend import (
    ScallopBackendContractError,
    run_article_263_liability_parity_program,
    run_liability_chain_parity_program,
)
from idpr.v2.runtime.stages import StatutoryDeemingObligation
from idpr.v2.runtime.statutory import resolve_article_263_deemed_liability
from idpr.v2.runtime.truths import CaseTruths

_DEFINITIONS = Path(__file__).resolve().parents[1] / "data/v2/definitions"


def _compiled(registry, ref: str):
    value = compilemod.compile_offense(registry, ref)
    assert isinstance(value, compilemod.CompiledOffense)
    return value


def _instance(ref: str, actor: str) -> OffenseInstanceKey:
    return OffenseInstanceKey("C-step5", actor, ref, "o1")


def test_direct_completion_chain_reconstructs_python_trace(tmp_path: Path) -> None:
    registry = load_definitions(_DEFINITIONS)
    compiled = _compiled(registry, "offense.embezzlement")
    instance = _instance(compiled.id, "direct")
    truths = CaseTruths()

    actual = run_liability_chain_parity_program(
        registry, [compiled], [instance], truths, work_dir=tmp_path,
        completion_targets=[instance],
    )
    expected_completion = completion.resolve_completion(None, compiled, instance, truths)
    expected = pipeline.resolve_liability(
        registry, compiled, instance, expected_completion, frozenset(), truths
    )

    assert actual == {instance: expected}


def test_derivative_dag_uses_prior_principal_evaluation(tmp_path: Path) -> None:
    registry = load_definitions(_DEFINITIONS)
    principal_compiled = _compiled(registry, "offense.robbery")
    accessory_compiled = _compiled(registry, "offense.obstruction_of_right_exercise")
    principal = _instance(principal_compiled.id, "principal")
    accessory = _instance(accessory_compiled.id, "accessory")
    truths = CaseTruths()

    actual = run_liability_chain_parity_program(
        registry,
        [principal_compiled, accessory_compiled],
        [principal, accessory],
        truths,
        work_dir=tmp_path,
        completion_targets=[principal],
        derivative_links=[(accessory, principal, "aider")],
    )
    expected_principal = pipeline.resolve_liability(
        registry, principal_compiled, principal,
        completion.resolve_completion(
            completion.completion_policy_for(registry, principal_compiled.id),
            principal_compiled, principal, truths,
        ),
        frozenset(), truths,
    )
    policy = participation_mod.participation_policy_for(registry)
    assert policy is not None
    expected_accessory = participation.resolve_derivative_liability(
        registry, policy, "aider", expected_principal, accessory, frozenset(), truths,
    )

    assert actual == {principal: expected_principal, accessory: expected_accessory}


def test_co_principal_attribute_precedes_completion_and_preserves_input(tmp_path: Path) -> None:
    registry = load_definitions(_DEFINITIONS)
    compiled = _compiled(registry, "offense.obstruction_of_right_exercise")
    target = _instance(compiled.id, "target")
    source = _instance(compiled.id, "source")
    taking = "legal_element.taking_of_own_property_conduct"
    status = "legal_element.own_property_object"
    truths = CaseTruths(predicate={
        (target, taking): "FALSE", (source, taking): "TRUE",
        (target, status): "FALSE", (source, status): "TRUE",
    })

    actual = run_liability_chain_parity_program(
        registry, [compiled], [target, source], truths, work_dir=tmp_path,
        completion_targets=[target], co_principal_sources=[(target, source)],
    )
    attributed = participation.apply_attribution(
        registry, compiled, compiled.id, target, [source], truths
    )
    expected = participation.resolve_co_principal_liability(
        registry, compiled, compiled.id, target, [source],
        completion.resolve_completion(None, compiled, target, attributed),
        frozenset(), truths,
    )

    assert actual == {target: expected}
    assert truths.predicate[(target, taking)] == "FALSE"


def test_step5_rejects_route_overlap_and_derivative_cycle(tmp_path: Path) -> None:
    registry = load_definitions(_DEFINITIONS)
    compiled = _compiled(registry, "offense.obstruction_of_right_exercise")
    left = _instance(compiled.id, "left")
    right = _instance(compiled.id, "right")

    with pytest.raises(ScallopBackendContractError, match="both completion and derivative"):
        run_liability_chain_parity_program(
            registry, [compiled], [left, right], CaseTruths(), work_dir=tmp_path,
            completion_targets=[left], derivative_links=[(left, right, "aider")],
        )
    with pytest.raises(ScallopBackendContractError, match="acyclic DAG"):
        run_liability_chain_parity_program(
            registry, [compiled], [left, right], CaseTruths(), work_dir=tmp_path,
            completion_targets=[],
            derivative_links=[(left, right, "aider"), (right, left, "aider")],
        )


def test_step5_does_not_use_python_liability_or_derivative_resolvers(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Reachability and derivative Elements must come from Scallop rows, not the oracle."""
    registry = load_definitions(_DEFINITIONS)
    principal_compiled = _compiled(registry, "offense.robbery")
    accessory_compiled = _compiled(registry, "offense.obstruction_of_right_exercise")
    principal = _instance(principal_compiled.id, "principal")
    accessory = _instance(accessory_compiled.id, "accessory")

    def forbidden(*_args, **_kwargs):
        raise AssertionError("Step 5 must not call the Python full-chain oracle")

    monkeypatch.setattr(pipeline, "resolve_liability", forbidden)
    monkeypatch.setattr(participation, "resolve_derivative_liability", forbidden)
    actual = run_liability_chain_parity_program(
        registry,
        [principal_compiled, accessory_compiled],
        [principal, accessory],
        CaseTruths(),
        work_dir=tmp_path,
        completion_targets=[principal],
        derivative_links=[(accessory, principal, "aider")],
    )

    assert set(actual) == {principal, accessory}


@pytest.mark.parametrize(
    ("statutory_truth", "expected_gate"),
    (("TRUE", "passes"), ("FALSE", "fails"), ("UNKNOWN", "unresolved")),
)
def test_article_263_backend_matches_dedicated_runtime(
    tmp_path: Path, statutory_truth: str, expected_gate: str
) -> None:
    registry = load_definitions(_DEFINITIONS)
    compiled = _compiled(registry, "offense.injury")
    instance = _instance(compiled.id, f"article-263-{statutory_truth.lower()}")
    truths_by_ref = {
        "legal_element.natural_person_victim_status": "TRUE",
        "ground_fact.injury_conduct": "TRUE",
        "legal_element.injury_result": "TRUE",
        "legal_element.intent": "TRUE",
        "legal_element.concurrent_independent_acts": statutory_truth,
        "legal_element.same_object_of_result": "TRUE",
        "legal_element.causal_origin_unascertained": "TRUE",
    }
    truths = CaseTruths(predicate={
        (instance, ref): truth
        for ref, truth in truths_by_ref.items()
        if truth != "UNKNOWN"
    })

    actual = run_article_263_liability_parity_program(
        registry, compiled, instance, truths, work_dir=tmp_path
    )
    expected = resolve_article_263_deemed_liability(
        registry,
        compiled,
        instance,
        completion.resolve_completion(None, compiled, instance, truths),
        frozenset(),
        truths,
    )

    assert actual == expected
    obligation = next(
        outcome for outcome in actual.elements.provenance
        if isinstance(outcome.obligation, StatutoryDeemingObligation)
    )
    assert obligation.truth == statutory_truth
    assert actual.elements.gate_state == expected_gate


def test_article_263_backend_does_not_call_python_statutory_or_pipeline_resolver(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    registry = load_definitions(_DEFINITIONS)
    compiled = _compiled(registry, "offense.injury")
    instance = _instance(compiled.id, "article-263-native")
    truths = CaseTruths(predicate={
        (instance, "legal_element.natural_person_victim_status"): "TRUE",
        (instance, "ground_fact.injury_conduct"): "TRUE",
        (instance, "legal_element.injury_result"): "TRUE",
        (instance, "legal_element.intent"): "TRUE",
        (instance, "legal_element.concurrent_independent_acts"): "TRUE",
        (instance, "legal_element.same_object_of_result"): "TRUE",
        (instance, "legal_element.causal_origin_unascertained"): "TRUE",
    })

    def forbidden(*_args, **_kwargs):
        raise AssertionError("Article 263 backend must not call a Python semantic resolver")

    monkeypatch.setattr(pipeline, "resolve_liability", forbidden)
    monkeypatch.setattr("idpr.v2.runtime.statutory.resolve_article_263_deemed_liability", forbidden)
    actual = run_article_263_liability_parity_program(
        registry, compiled, instance, truths, work_dir=tmp_path
    )

    assert actual.liability_result is not None


def test_article_263_completion_stop_keeps_elements_and_statutory_provenance_unreached(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    registry = load_definitions(_DEFINITIONS)
    compiled = _compiled(registry, "offense.injury")
    instance = _instance(compiled.id, "article-263-completion-stop")
    original_policy_for = completion.completion_policy_for
    synthetic_policy = DefinitionEntry(
        id="completion_policy.test_article_263_stop",
        kind="completion_policy",
        payload={
            "states": {
                "completed": {
                    "when": {"op": "ref", "ref": "legal_element.commencement_of_execution"},
                    "punishable": True,
                },
            },
        },
        source_file="test",
    )

    def policy_for(_registry, offense_ref):
        if offense_ref == compiled.id:
            return synthetic_policy
        return original_policy_for(_registry, offense_ref)

    monkeypatch.setattr(completion, "completion_policy_for", policy_for)
    truths = CaseTruths(predicate={
        (instance, "legal_element.natural_person_victim_status"): "TRUE",
        (instance, "ground_fact.injury_conduct"): "TRUE",
        (instance, "legal_element.injury_result"): "TRUE",
        (instance, "legal_element.intent"): "TRUE",
        (instance, "legal_element.concurrent_independent_acts"): "TRUE",
        (instance, "legal_element.same_object_of_result"): "TRUE",
        (instance, "legal_element.causal_origin_unascertained"): "TRUE",
    })

    actual = run_article_263_liability_parity_program(
        registry, compiled, instance, truths, work_dir=tmp_path
    )
    expected_completion = completion.resolve_completion(synthetic_policy, compiled, instance, truths)
    expected = resolve_article_263_deemed_liability(
        registry, compiled, instance, expected_completion, frozenset(), truths
    )

    assert expected_completion.state == "unresolved"
    assert actual == expected
    assert actual.elements.evaluation_state == "not_reached"
    assert actual.unlawfulness.evaluation_state == "not_reached"
    assert not any(
        isinstance(outcome.obligation, StatutoryDeemingObligation)
        for outcome in actual.elements.provenance
    )


@pytest.mark.parametrize(
    ("doctrine", "extra_truths", "closed_stage"),
    (
        (
            "doctrine.self_defense",
            {
                "legal_element.infringement_situation": "TRUE",
                "legal_element.defensive_act": "TRUE",
                "legal_element.reasonable_grounds": "TRUE",
            },
            "unlawfulness",
        ),
        (
            "doctrine.juvenile_defeat",
            {"ground_fact.actor_age_under_14_at_act_time": "TRUE"},
            "culpability",
        ),
    ),
)
def test_article_263_active_doctrine_closes_only_the_reached_stage_tail(
    tmp_path: Path,
    doctrine: str,
    extra_truths: dict[str, str],
    closed_stage: str,
) -> None:
    registry = load_definitions(_DEFINITIONS)
    compiled = _compiled(registry, "offense.injury")
    instance = _instance(compiled.id, f"article-263-{closed_stage}-defeat")
    truths_by_ref = {
        "legal_element.natural_person_victim_status": "TRUE",
        "ground_fact.injury_conduct": "TRUE",
        "legal_element.injury_result": "TRUE",
        "legal_element.intent": "TRUE",
        "legal_element.concurrent_independent_acts": "TRUE",
        "legal_element.same_object_of_result": "TRUE",
        "legal_element.causal_origin_unascertained": "TRUE",
        **extra_truths,
    }
    truths = CaseTruths(predicate={(instance, ref): truth for ref, truth in truths_by_ref.items()})
    active = frozenset({doctrine})

    actual = run_article_263_liability_parity_program(
        registry,
        compiled,
        instance,
        truths,
        work_dir=tmp_path,
        active_doctrines=[(instance, doctrine)],
    )
    expected = resolve_article_263_deemed_liability(
        registry,
        compiled,
        instance,
        completion.resolve_completion(None, compiled, instance, truths),
        active,
        truths,
    )

    assert actual == expected
    assert getattr(actual, closed_stage).gate_state == "fails"
    if closed_stage == "unlawfulness":
        assert actual.culpability.evaluation_state == "not_reached"
    else:
        assert actual.punishability.evaluation_state == "not_reached"
