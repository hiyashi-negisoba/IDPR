"""Step 4 Scallop parity: participation adapters and active doctrine effects."""

from __future__ import annotations

from pathlib import Path

import pytest

from idpr.v2 import compile as compilemod
from idpr.v2 import evaluate
from idpr.v2.registry import DefinitionEntry, DefinitionRegistry, load_definitions
from idpr.v2.runtime import effects, participation
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.scallop_backend import (
    ScallopBackendContractError,
    compile_participation_stage_program,
    render_participation_stage_edb,
    run_participation_stage_parity_program,
)
from idpr.v2.runtime.truths import CaseTruths


_DEFINITIONS = Path(__file__).resolve().parents[1] / "data/v2/definitions"


def _registry() -> DefinitionRegistry:
    return load_definitions(_DEFINITIONS)


def _compiled(registry: DefinitionRegistry, ref: str) -> compilemod.CompiledOffense:
    value = compilemod.compile_offense(registry, ref)
    assert isinstance(value, compilemod.CompiledOffense)
    return value


def _instance(ref: str, actor: str) -> OffenseInstanceKey:
    return OffenseInstanceKey("C1", actor, ref, "o1")


def test_co_principal_sparse_override_and_constitutive_provenance_match_python(tmp_path: Path) -> None:
    registry = _registry()
    compiled = _compiled(registry, "offense.obstruction_of_right_exercise")
    target = _instance(compiled.id, "target")
    source = _instance(compiled.id, "source")
    taking = "legal_element.taking_of_own_property_conduct"
    status = "legal_element.own_property_object"
    truths = CaseTruths(predicate={
        (target, taking): evaluate.FALSE,
        (source, taking): evaluate.TRUE,
        (target, status): evaluate.FALSE,
        (source, status): evaluate.TRUE,
    })

    actual = run_participation_stage_parity_program(
        registry,
        [compiled],
        [target, source],
        truths,
        work_dir=tmp_path,
        participation_targets=[target],
        co_principal_sources=[(target, source)],
    )
    expected_view = participation.apply_attribution(
        registry, compiled, compiled.id, target, [source], truths
    )

    assert actual.attributed_predicates[(target, taking)] == expected_view.predicate[(target, taking)]
    assert actual.constitutive_statuses[(target, status)] == evaluate.TRUE
    assert actual.constitutive_true_members == frozenset({(target, status, source)})


def test_derivative_requirement_and_aggregate_preserve_two_obligations(tmp_path: Path) -> None:
    registry = _registry()
    accessory_compiled = _compiled(registry, "offense.obstruction_of_right_exercise")
    principal_compiled = _compiled(registry, "offense.robbery")
    accessory = _instance(accessory_compiled.id, "accessory")
    principal = _instance(principal_compiled.id, "principal")
    link = (accessory, principal, "aider")
    truths = CaseTruths(predicate={(accessory, "legal_element.aiding_intent"): evaluate.TRUE})

    actual = run_participation_stage_parity_program(
        registry,
        [accessory_compiled, principal_compiled],
        [accessory, principal],
        truths,
        work_dir=tmp_path,
        derivative_links=[link],
        principal_realization_truths={principal: evaluate.UNKNOWN},
    )

    assert actual.derivative_requirements[link] == evaluate.TRUE
    assert actual.derivative_elements[link] == evaluate.UNKNOWN


def test_stage_effect_fold_matches_python_and_reads_co_principal_override(tmp_path: Path) -> None:
    registry = _with_attributed_doctrine(_registry())
    compiled = _compiled(registry, "offense.obstruction_of_right_exercise")
    target = _instance(compiled.id, "target")
    source = _instance(compiled.id, "source")
    taking = "legal_element.taking_of_own_property_conduct"
    doctrine_ref = "doctrine.synthetic_attributed_step4"
    truths = CaseTruths(predicate={(target, taking): evaluate.FALSE, (source, taking): evaluate.TRUE})

    actual = run_participation_stage_parity_program(
        registry,
        [compiled],
        [target, source],
        truths,
        work_dir=tmp_path,
        participation_targets=[target],
        co_principal_sources=[(target, source)],
        active_doctrines=[(target, doctrine_ref)],
        stage_effect_targets=[(target, "unlawfulness"), (target, "culpability")],
    )
    attributed = participation.apply_attribution(registry, compiled, compiled.id, target, [source], truths)
    expected_unlawfulness = effects.resolve_stage(
        "unlawfulness", frozenset({doctrine_ref}), registry, target, attributed
    )
    expected_culpability = effects.resolve_stage("culpability", frozenset(), registry, target, attributed)

    assert actual.stage_effects[(target, doctrine_ref)] == ("DEFEAT", evaluate.TRUE)
    assert actual.stage_results[(target, "unlawfulness")] == (
        expected_unlawfulness.legal_state,
        expected_unlawfulness.gate_state,
    )
    assert actual.stage_results[(target, "culpability")] == (
        expected_culpability.legal_state,
        expected_culpability.gate_state,
    )


@pytest.mark.parametrize(
    ("doctrine_ref", "stage", "predicate_ref", "truth"),
    [
        ("doctrine.juvenile_defeat", "culpability", "ground_fact.actor_age_under_14_at_act_time", evaluate.TRUE),
        ("doctrine.juvenile_defeat", "culpability", "ground_fact.actor_age_under_14_at_act_time", evaluate.UNKNOWN),
        ("doctrine.deaf_mute_mandatory_reduction", "culpability", "legal_element.deaf_mute_status", evaluate.TRUE),
        ("doctrine.deaf_mute_mandatory_reduction", "culpability", "legal_element.deaf_mute_status", evaluate.FALSE),
        ("doctrine.deaf_mute_mandatory_reduction", "culpability", "legal_element.deaf_mute_status", evaluate.UNKNOWN),
        ("doctrine.synthetic_exempt_step4", "punishability", "ground_fact.actor_age_under_14_at_act_time", evaluate.TRUE),
        ("doctrine.synthetic_exempt_step4", "punishability", "ground_fact.actor_age_under_14_at_act_time", evaluate.UNKNOWN),
    ],
)
def test_stage_effect_truth_and_fold_match_python_for_closed_three_value_table(
    tmp_path: Path, doctrine_ref: str, stage: str, predicate_ref: str, truth: str
) -> None:
    registry = _with_exempt_doctrine(_registry())
    compiled = _compiled(registry, "offense.robbery")
    instance = _instance(compiled.id, "actor")
    actual = run_participation_stage_parity_program(
        registry,
        [compiled],
        [instance],
        CaseTruths(predicate={(instance, predicate_ref): truth}),
        work_dir=tmp_path,
        active_doctrines=[(instance, doctrine_ref)],
        stage_effect_targets=[(instance, stage)],
    )
    expected = effects.resolve_stage(stage, frozenset({doctrine_ref}), registry, instance, CaseTruths(predicate={(instance, predicate_ref): truth}))
    doctrine = registry.get(doctrine_ref)
    assert doctrine is not None
    assert actual.stage_effects[(instance, doctrine_ref)] == (doctrine.payload["effect"]["effect"], truth)
    assert actual.stage_results[(instance, stage)] == (expected.legal_state, expected.gate_state)


def test_step4_rejects_unapproved_endpoint_and_incomplete_principal_adapter() -> None:
    registry = _registry()
    compiled = _compiled(registry, "offense.obstruction_of_right_exercise")
    target = _instance(compiled.id, "target")
    source = _instance(compiled.id, "source")
    with pytest.raises(ScallopBackendContractError, match="authorized"):
        render_participation_stage_edb(
            registry,
            [compiled],
            [target],
            CaseTruths(),
            participation_targets=[target],
            co_principal_sources=[(target, source)],
        )
    with pytest.raises(ScallopBackendContractError, match="principal realization rows"):
        render_participation_stage_edb(
            registry,
            [compiled],
            [target],
            CaseTruths(),
            derivative_links=[(target, target, "aider")],
        )


def test_step4_static_emission_is_deterministic() -> None:
    registry = _registry()
    left = _compiled(registry, "offense.obstruction_of_right_exercise")
    right = _compiled(registry, "offense.robbery")
    first = compile_participation_stage_program(registry, [left, right])
    second = compile_participation_stage_program(registry, [right, left])
    assert first.program == second.program
    assert first.doctrine_manifest == second.doctrine_manifest


def _with_attributed_doctrine(registry: DefinitionRegistry) -> DefinitionRegistry:
    return _with_doctrine(
        registry,
        "doctrine.synthetic_attributed_step4",
        "unlawfulness",
        "DEFEAT",
        "legal_element.taking_of_own_property_conduct",
    )


def _with_exempt_doctrine(registry: DefinitionRegistry) -> DefinitionRegistry:
    return _with_doctrine(
        registry,
        "doctrine.synthetic_exempt_step4",
        "punishability",
        "EXEMPT",
        "ground_fact.actor_age_under_14_at_act_time",
    )


def _with_doctrine(
    registry: DefinitionRegistry, doctrine_id: str, stage: str, effect: str, predicate_ref: str
) -> DefinitionRegistry:
    by_kind = {kind: list(entries) for kind, entries in registry.by_kind.items()}
    by_kind.setdefault("doctrine", []).append(
        DefinitionEntry(
            id=doctrine_id,
            kind="doctrine",
            payload={
                "stage": stage,
                "requires": {"op": "ref", "ref": predicate_ref},
                "effect": {"effect": effect, "stage": stage},
            },
            source_file="<synthetic>",
        )
    )
    frozen = {kind: tuple(entries) for kind, entries in by_kind.items()}
    return DefinitionRegistry(
        by_id={entry.id: entry for entries in frozen.values() for entry in entries},
        by_kind=frozen,
    )
