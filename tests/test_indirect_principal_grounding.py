from __future__ import annotations

from pathlib import Path

import pytest

from idpr.v2.compile import CompiledOffense, compile_offense
from idpr.v2.gold_factual_identity import GoldFactualParticipant, GoldOccurrence
from idpr.v2.registry import load_definitions
from idpr.v2.relations import iter_relation_instances
from idpr.v2.runtime.identity import FactualParticipantKey, OffenseInstanceKey
from idpr.v2.runtime.indirect_principal_grounding import (
    FactualUtilizationAssessment,
    IndirectPrincipalGroundingError,
    compile_indirect_principal_dependencies,
    factual_utilization_request_payload,
    factual_utilization_targets,
    validate_factual_utilization_output,
)
from idpr.v2.runtime.participation import resolve_indirect_principal_liability
from idpr.v2.runtime.scallop_backend import (
    compile_indirect_principal_dependency_program,
    render_indirect_principal_dependency_edb,
    run_indirect_principal_liability_parity_program,
)
from idpr.v2.runtime.stages import UtilizedParticipantOutcome
from idpr.v2.runtime.truths import CaseTruths
from idpr.v2.runtime.utilized_participant_outcome import (
    UtilizedParticipantOutcomeError,
    UtilizedParticipantPredicateAssessment,
    produce_utilized_participant_outcomes,
    utilized_participant_outcome_targets,
    utilized_participant_predicate_targets,
    utilized_participant_request_payload,
    validate_utilized_participant_output,
)

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = load_definitions(ROOT / "data/v2/definitions")


def _occurrence() -> GoldOccurrence:
    return GoldOccurrence("gocc:001", "甲", "甲이 A에게 행동을 시켰다.", 0, 15)


def _participant() -> GoldFactualParticipant:
    return GoldFactualParticipant("fpart:001", "A", "A가 행동하였다.", 16, 24)


def test_capability_only_gates_offense_free_factual_targets() -> None:
    instances = (
        OffenseInstanceKey("case", "甲", "offense.forcible_indecency", "gocc:001"),
        OffenseInstanceKey("case", "甲", "offense.rape", "gocc:001"),
    )
    targets = factual_utilization_targets(REGISTRY, instances, (_participant(),))
    assert len(targets) == 1
    rendered = targets[0].as_dict()
    assert rendered["relation_kind"] == "factual_action_direction"
    assert "offense_ref" not in str(rendered)


def test_request_is_action_direction_only_and_has_no_legal_activation_fields() -> None:
    target = factual_utilization_targets(
        REGISTRY,
        (OffenseInstanceKey("case", "甲", "offense.forcible_indecency", "gocc:001"),),
        (_participant(),),
    )[0]
    payload = factual_utilization_request_payload(
        occurrences=(_occurrence(),), participants=(_participant(),), targets=(target,)
    )
    assert payload["relation_contract"]["direction"] == (
        "utilizer_action_to_utilized_participant_action"
    )
    assert payload["relation_contract"]["legal_effect"] == "none"
    forbidden = {"offense_ref", "mode", "role", "liability", "rubric", "card"}

    def keys(value):
        if isinstance(value, dict):
            return set(value) | set().union(*(keys(item) for item in value.values()))
        if isinstance(value, list):
            return set().union(*(keys(item) for item in value))
        return set()

    assert not (forbidden & keys(payload))


def test_output_validator_preserves_unknown_and_rejects_extra_legal_labels() -> None:
    target = factual_utilization_targets(
        REGISTRY,
        (OffenseInstanceKey("case", "甲", "offense.forcible_indecency", "gocc:001"),),
        (_participant(),),
    )[0]
    assessment = validate_factual_utilization_output(
        {
            "relation_assessment": {
                "relation_kind": "factual_action_direction",
                "truth": "UNKNOWN",
            }
        },
        target=target,
    )
    assert assessment.truth == "UNKNOWN"
    with pytest.raises(IndirectPrincipalGroundingError):
        validate_factual_utilization_output(
            {
                "relation_assessment": {
                    "relation_kind": "factual_action_direction",
                    "truth": "TRUE",
                    "role": "indirect_principal",
                }
            },
            target=target,
        )


def test_dependency_compiler_accepts_an_explicit_sparse_target_universe() -> None:
    participants = (
        _participant(),
        GoldFactualParticipant("fpart:002", "B", "B가 행동하였다.", 25, 33),
    )
    instance = OffenseInstanceKey(
        "case", "甲", "offense.forcible_indecency", "gocc:001"
    )
    cartesian = factual_utilization_targets(REGISTRY, (instance,), participants)
    sparse = cartesian[:1]
    outcome = UtilizedParticipantOutcome(
        sparse[0].utilized_participant,
        instance.offense_ref,
        "culpability_defeat",
    )
    dependencies = compile_indirect_principal_dependencies(
        REGISTRY,
        (instance,),
        participants,
        (FactualUtilizationAssessment(sparse[0], "TRUE"),),
        (outcome,),
        expected_targets=sparse,
    )
    assert len(dependencies) == 1
    assert dependencies[0].truth == "TRUE"


def _participant_outcome_frontier(offense_ref: str):
    instances = (OffenseInstanceKey("case", "甲", offense_ref, "gocc:001"),)
    outcome_target = utilized_participant_outcome_targets(
        REGISTRY, instances, (_participant(),)
    )[0]
    predicate_targets = utilized_participant_predicate_targets(
        REGISTRY, (outcome_target,)
    )
    return outcome_target, predicate_targets


def test_participant_predicate_request_is_exact_and_has_no_liability_output() -> None:
    outcome_target, predicate_targets = _participant_outcome_frontier(
        "offense.private_document_forgery"
    )
    payload = utilized_participant_request_payload(
        REGISTRY,
        participant=_participant(),
        outcome_target=outcome_target,
        predicate_targets=predicate_targets,
    )
    assert payload["exact_offense_ref"] == "offense.private_document_forgery"
    assert {value["predicate_ref"] for value in payload["assessment_targets"]} == {
        "legal_element.alteration_of_genuine_document",
        "legal_element.forgery_without_authority",
        "legal_element.private_document_object",
        "legal_element.purpose_to_use_as_genuine",
    }
    assert "liability" not in str(payload).lower()
    raw = {
        "assessments": [
            {"predicate_ref": target.predicate_ref, "truth": "TRUE"}
            for target in reversed(predicate_targets)
        ]
    }
    assessments = validate_utilized_participant_output(
        raw, predicate_targets=predicate_targets
    )
    assert tuple(value.target for value in assessments) == predicate_targets
    with pytest.raises(UtilizedParticipantOutcomeError):
        validate_utilized_participant_output(
            {
                "assessments": [
                    {
                        "predicate_ref": predicate_targets[0].predicate_ref,
                        "truth": "TRUE",
                        "role": "indirect_tool",
                    }
                ]
            },
            predicate_targets=predicate_targets,
        )


def test_participant_outcome_folds_predicates_without_ordinary_actor_instance() -> None:
    outcome_target, predicate_targets = _participant_outcome_frontier(
        "offense.private_document_forgery"
    )

    def produce(overrides=None):
        overrides = overrides or {}
        assessments = tuple(
            UtilizedParticipantPredicateAssessment(
                target, overrides.get(target.predicate_ref, "TRUE")
            )
            for target in predicate_targets
        )
        return produce_utilized_participant_outcomes(
            REGISTRY, (outcome_target,), assessments
        )[0]

    liable = produce()
    assert liable.participant == FactualParticipantKey("case", "fpart:001")
    assert liable.status == "liable_exact_offense"
    assert not hasattr(liable, "instance")
    assert produce(
        {
            "legal_element.alteration_of_genuine_document": "FALSE",
            "legal_element.forgery_without_authority": "FALSE",
        }
    ).status == "elements_failure"
    assert produce(
        {
            "legal_element.alteration_of_genuine_document": "FALSE",
            "legal_element.forgery_without_authority": "UNKNOWN",
        }
    ).status == "unresolved"


def test_participant_outcome_preserves_missing_relation_as_unknown() -> None:
    outcome_target, predicate_targets = _participant_outcome_frontier(
        "derived_offense.fraud"
    )
    assessments = tuple(
        UtilizedParticipantPredicateAssessment(target, "TRUE")
        for target in predicate_targets
    )
    assert produce_utilized_participant_outcomes(
        REGISTRY, (outcome_target,), assessments
    )[0].status == "unresolved"
    compiled = compile_offense(REGISTRY, outcome_target.offense_ref)
    assert isinstance(compiled, CompiledOffense)
    relation_key = next(iter(iter_relation_instances(compiled)))[0]
    assert produce_utilized_participant_outcomes(
        REGISTRY,
        (outcome_target,),
        assessments,
        relation_truths={(outcome_target, relation_key): "TRUE"},
    )[0].status == "liable_exact_offense"


def test_participant_outcome_uses_explicit_active_doctrine_predicates() -> None:
    outcome_target, _ = _participant_outcome_frontier(
        "offense.private_document_forgery"
    )
    active = {outcome_target: frozenset({"doctrine.juvenile_defeat"})}
    predicate_targets = utilized_participant_predicate_targets(
        REGISTRY,
        (outcome_target,),
        active_doctrines_by_target=active,
    )
    assessments = tuple(
        UtilizedParticipantPredicateAssessment(target, "TRUE")
        for target in predicate_targets
    )
    outcome = produce_utilized_participant_outcomes(
        REGISTRY,
        (outcome_target,),
        assessments,
        active_doctrines_by_target=active,
    )[0]
    assert outcome.status == "culpability_defeat"


def test_unaware_public_document_signer_fails_explicit_intent_element() -> None:
    outcome_target, predicate_targets = _participant_outcome_frontier(
        "offense.false_public_document_creation"
    )
    assert "legal_element.intent" in {
        value.predicate_ref for value in predicate_targets
    }
    assessments = tuple(
        UtilizedParticipantPredicateAssessment(
            target,
            "FALSE" if target.predicate_ref == "legal_element.intent" else "TRUE",
        )
        for target in predicate_targets
    )
    assert produce_utilized_participant_outcomes(
        REGISTRY, (outcome_target,), assessments
    )[0].status == "elements_failure"


def test_outcome_producer_requires_exact_predicate_correspondence() -> None:
    outcome_target, predicate_targets = _participant_outcome_frontier(
        "offense.private_document_forgery"
    )
    with pytest.raises(UtilizedParticipantOutcomeError, match="exactly equal"):
        produce_utilized_participant_outcomes(
            REGISTRY,
            (outcome_target,),
            tuple(
                UtilizedParticipantPredicateAssessment(target, "TRUE")
                for target in predicate_targets[:-1]
            ),
        )


def test_produced_internal_outcome_feeds_dependency_without_actor_conversion() -> None:
    instance = OffenseInstanceKey(
        "case", "甲", "offense.private_document_forgery", "gocc:001"
    )
    participant = _participant()
    outcome_target = utilized_participant_outcome_targets(
        REGISTRY, (instance,), (participant,)
    )[0]
    predicate_targets = utilized_participant_predicate_targets(
        REGISTRY, (outcome_target,)
    )
    assessments = tuple(
        UtilizedParticipantPredicateAssessment(
            target,
            (
                "FALSE"
                if target.predicate_ref
                in {
                    "legal_element.alteration_of_genuine_document",
                    "legal_element.forgery_without_authority",
                }
                else "TRUE"
            ),
        )
        for target in predicate_targets
    )
    outcome = produce_utilized_participant_outcomes(
        REGISTRY, (outcome_target,), assessments
    )[0]
    utilization_target = factual_utilization_targets(
        REGISTRY, (instance,), (participant,)
    )[0]
    dependency = compile_indirect_principal_dependencies(
        REGISTRY,
        (instance,),
        (participant,),
        (FactualUtilizationAssessment(utilization_target, "TRUE"),),
        (outcome,),
    )[0]
    assert outcome.status == "elements_failure"
    assert dependency.truth == "TRUE"
    assert dependency.utilized_participant == outcome.participant


def test_host_compiler_requires_relation_and_exact_offense_outcome() -> None:
    instances = (
        OffenseInstanceKey("case", "甲", "offense.forcible_indecency", "gocc:001"),
    )
    participant = _participant()
    target = factual_utilization_targets(REGISTRY, instances, (participant,))[0]
    outcome = UtilizedParticipantOutcome(
        FactualParticipantKey("case", "fpart:001"),
        "offense.forcible_indecency",
        "culpability_defeat",
    )
    dependencies = compile_indirect_principal_dependencies(
        REGISTRY,
        instances,
        (participant,),
        (FactualUtilizationAssessment(target, "TRUE"),),
        (outcome,),
    )
    assert len(dependencies) == 1
    assert dependencies[0].truth == "TRUE"
    assert dependencies[0].reason == "culpability_defeat"


def test_host_compiler_preserves_unknown_and_rejects_missing_outcome() -> None:
    instances = (
        OffenseInstanceKey("case", "甲", "offense.forcible_indecency", "gocc:001"),
    )
    participant = _participant()
    target = factual_utilization_targets(REGISTRY, instances, (participant,))[0]
    with pytest.raises(IndirectPrincipalGroundingError, match="missing utilized outcome"):
        compile_indirect_principal_dependencies(
            REGISTRY,
            instances,
            (participant,),
            (FactualUtilizationAssessment(target, "UNKNOWN"),),
            (),
        )
    dependency = compile_indirect_principal_dependencies(
        REGISTRY,
        instances,
        (participant,),
        (FactualUtilizationAssessment(target, "UNKNOWN"),),
        (
            UtilizedParticipantOutcome(
                FactualParticipantKey("case", "fpart:001"),
                "offense.forcible_indecency",
                "liable_exact_offense",
            ),
        ),
    )[0]
    assert dependency.truth == "UNKNOWN"
    assert dependency.reason == "factual_utilization_unresolved"


def test_false_relation_creates_no_dependency_and_needs_no_outcome() -> None:
    instances = (
        OffenseInstanceKey("case", "甲", "offense.forcible_indecency", "gocc:001"),
    )
    participant = _participant()
    target = factual_utilization_targets(REGISTRY, instances, (participant,))[0]
    assert compile_indirect_principal_dependencies(
        REGISTRY,
        instances,
        (participant,),
        (FactualUtilizationAssessment(target, "FALSE"),),
        (),
    ) == ()


def test_indirect_runtime_consumes_compiled_dependency_not_accessory_mode() -> None:
    instance = OffenseInstanceKey(
        "case", "甲", "offense.forcible_indecency", "gocc:001"
    )
    participant = _participant()
    target = factual_utilization_targets(REGISTRY, (instance,), (participant,))[0]
    dependency = compile_indirect_principal_dependencies(
        REGISTRY,
        (instance,),
        (participant,),
        (FactualUtilizationAssessment(target, "TRUE"),),
        (
            UtilizedParticipantOutcome(
                FactualParticipantKey("case", "fpart:001"),
                "offense.forcible_indecency",
                "culpability_defeat",
            ),
        ),
    )[0]
    evaluation = resolve_indirect_principal_liability(
        REGISTRY, dependency, frozenset(), CaseTruths()
    )
    assert evaluation.instance == instance
    assert evaluation.elements.gate_state == "passes"
    assert evaluation.completion is None
    assert evaluation.liability_result is not None


def test_scallop_lowering_is_dedicated_and_matches_host_runtime(tmp_path: Path) -> None:
    instance = OffenseInstanceKey(
        "case", "甲", "offense.forcible_indecency", "gocc:001"
    )
    participant = _participant()
    target = factual_utilization_targets(REGISTRY, (instance,), (participant,))[0]
    dependency = compile_indirect_principal_dependencies(
        REGISTRY,
        (instance,),
        (participant,),
        (FactualUtilizationAssessment(target, "TRUE"),),
        (
            UtilizedParticipantOutcome(
                FactualParticipantKey("case", "fpart:001"),
                "offense.forcible_indecency",
                "culpability_defeat",
            ),
        ),
    )[0]
    program = compile_indirect_principal_dependency_program()
    edb = render_indirect_principal_dependency_edb(REGISTRY, (dependency,))
    assert "v2_indirect_principal_dependency_input" in program + edb
    assert "v2_derivative_link" not in program + edb
    scallop = run_indirect_principal_liability_parity_program(
        REGISTRY, dependency, CaseTruths(), work_dir=tmp_path
    )
    host = resolve_indirect_principal_liability(
        REGISTRY, dependency, frozenset(), CaseTruths()
    )
    assert scallop == host
