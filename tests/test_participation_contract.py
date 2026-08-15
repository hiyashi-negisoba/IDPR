from __future__ import annotations

from pathlib import Path

import pytest

from idpr.v2.compile import CompiledOffense, compile_offense
from idpr.v2.gold_factual_identity import GoldOccurrence
from idpr.v2.participation import (
    co_principal_established_predicate_refs,
    effective_attributable_slots,
    participation_policy_for,
)
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.identity import (
    PARTICIPATION_OCCURRENCE_PREFIX,
    OffenseInstanceKey,
)
from idpr.v2.runtime.participation import apply_attribution
from idpr.v2.runtime.participation_grounding import (
    ParticipationGroundingError,
    ParticipationLocalAssessment,
    ParticipationLocalTarget,
    add_co_principal_established_truths,
    compile_participation_bindings,
    participation_local_targets,
    participation_request_payload,
    validate_participation_output,
)
from idpr.v2.runtime.truths import CaseTruths

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = load_definitions(ROOT / "data/v2/definitions")


def _instance(actor: str, number: int) -> OffenseInstanceKey:
    return OffenseInstanceKey("case", actor, "offense.theft", f"gocc:{number:03d}")


def _assessments(
    instances: tuple[OffenseInstanceKey, ...],
    true_targets: tuple[ParticipationLocalTarget, ...] = (),
    unknown_targets: tuple[ParticipationLocalTarget, ...] = (),
) -> tuple[ParticipationLocalAssessment, ...]:
    targets = participation_local_targets(REGISTRY, instances)
    return tuple(
        ParticipationLocalAssessment(
            target,
            "TRUE" if target in true_targets else "UNKNOWN" if target in unknown_targets else "FALSE",
        )
        for target in targets
    )


def _target(
    targets: tuple[ParticipationLocalTarget, ...],
    kind: str,
    members: tuple[OffenseInstanceKey, ...],
) -> ParticipationLocalTarget:
    return next(value for value in targets if value.kind == kind and value.members == members)


def test_standard_co_principal_policy_attributes_conduct() -> None:
    policy = participation_policy_for(REGISTRY)
    offense = REGISTRY.get("offense.theft")
    assert policy is not None and offense is not None
    assert effective_attributable_slots(policy, offense) == frozenset({"conduct"})
    assert co_principal_established_predicate_refs(policy) == frozenset(
        {"legal_element.joint_commission_by_two_or_more"}
    )


def test_co_principal_source_conduct_reaches_target_without_mutating_input() -> None:
    compiled = compile_offense(REGISTRY, "offense.theft")
    assert isinstance(compiled, CompiledOffense)
    target = _instance("甲", 1)
    source = _instance("乙", 2)
    ref = "ground_fact.taking_conduct"
    truths = CaseTruths(predicate={(target, ref): "FALSE", (source, ref): "TRUE"})
    attributed = apply_attribution(
        REGISTRY, compiled, "offense.theft", target, (source,), truths
    )
    assert truths.predicate[(target, ref)] == "FALSE"
    assert attributed.predicate[(target, ref)] == "TRUE"


def test_true_co_group_symbolically_establishes_joint_commission_predicate() -> None:
    left, right = _instance("甲", 1), _instance("乙", 2)
    target = ParticipationLocalTarget("co_principal_group", (left, right))
    bindings = compile_participation_bindings(
        (ParticipationLocalAssessment(target, "TRUE"),),
        expected_targets=(target,),
    )
    original = CaseTruths(
        predicate={(left, "legal_element.joint_commission_by_two_or_more"): "UNKNOWN"}
    )
    projected, audit = add_co_principal_established_truths(
        REGISTRY, original, bindings
    )
    ref = "legal_element.joint_commission_by_two_or_more"
    assert original.predicate[(left, ref)] == "UNKNOWN"
    assert projected.predicate[(left, ref)] == "TRUE"
    assert projected.predicate[(right, ref)] == "TRUE"
    assert len(audit) == 2


def test_model_request_contains_exactly_one_lightweight_local_relation() -> None:
    instances = (_instance("甲", 1), _instance("乙", 2))
    target = _target(
        participation_local_targets(REGISTRY, instances),
        "instigation",
        instances,
    )
    texts = ("甲이 乙을 설득하였다.", "乙이 실행하였다.")
    occurrences = tuple(
        GoldOccurrence(f"gocc:{index:03d}", actor, text, 0, len(text))
        for index, (actor, text) in enumerate(zip(("甲", "乙"), texts, strict=True), 1)
    )
    payload = participation_request_payload(
        registry=REGISTRY, occurrences=occurrences, targets=(target,)
    )
    assert set(payload) == {
        "occurrence_evidence",
        "offense_definition",
        "local_relation_target",
        "relation_contract",
    }
    assessment = validate_participation_output({"truth": "TRUE"}, targets=(target,))
    assert assessment == ParticipationLocalAssessment(target, "TRUE")
    with pytest.raises(ParticipationGroundingError):
        participation_request_payload(
            registry=REGISTRY, occurrences=occurrences, targets=(target, target)
        )


@pytest.mark.parametrize("kind", ("instigation", "aiding"))
def test_direct_root_with_one_derivative_compiles(kind: str) -> None:
    instances = (_instance("甲", 1), _instance("乙", 2))
    targets = participation_local_targets(REGISTRY, instances)
    relation = _target(targets, kind, instances)
    bindings = compile_participation_bindings(
        _assessments(instances, (relation,)), expected_targets=targets
    )
    mode = "instigator" if kind == "instigation" else "aider"
    assert bindings.derivative_links == ((instances[0], instances[1], mode),)


def test_multi_level_derivative_chain_compiles_to_dag() -> None:
    instances = (_instance("甲", 1), _instance("乙", 2), _instance("丙", 3))
    targets = participation_local_targets(REGISTRY, instances)
    relations = (
        _target(targets, "instigation", (instances[0], instances[1])),
        _target(targets, "aiding", (instances[1], instances[2])),
    )
    bindings = compile_participation_bindings(
        _assessments(instances, relations), expected_targets=targets
    )
    assert bindings.derivative_links == (
        (instances[0], instances[1], "instigator"),
        (instances[1], instances[2], "aider"),
    )


def test_true_co_principal_subset_compiles_to_group_node_attribution() -> None:
    instances = (_instance("甲", 1), _instance("乙", 2), _instance("丙", 3))
    targets = participation_local_targets(REGISTRY, instances)
    group = _target(targets, "co_principal_group", instances[:2])
    bindings = compile_participation_bindings(
        _assessments(instances, (group,)), expected_targets=targets
    )
    assert set(bindings.co_principal_sources) == {
        (instances[0], instances[1]),
        (instances[1], instances[0]),
    }
    assert bindings.derivative_links == ()


def test_self_loop_is_not_an_authorized_local_target() -> None:
    actor = _instance("甲", 1)
    with pytest.raises(ParticipationGroundingError, match="duplicate|repeats"):
        participation_request_payload(
            registry=REGISTRY,
            occurrences=(),
            targets=(ParticipationLocalTarget("instigation", (actor, actor)),),
        )


@pytest.mark.parametrize("size", (2, 3))
def test_derivative_cycle_hard_fails(size: int) -> None:
    instances = tuple(_instance(actor, index) for index, actor in enumerate("甲乙丙"[:size], 1))
    targets = participation_local_targets(REGISTRY, instances)
    cycle = tuple(
        _target(
            targets,
            "instigation",
            (instances[index], instances[(index + 1) % size]),
        )
        for index in range(size)
    )
    with pytest.raises(ParticipationGroundingError, match="cycle"):
        compile_participation_bindings(
            _assessments(instances, cycle), expected_targets=targets
        )


def test_missing_local_target_is_dangling_closed_universe_failure() -> None:
    instances = (_instance("甲", 1), _instance("乙", 2))
    targets = participation_local_targets(REGISTRY, instances)
    assessments = _assessments(instances)
    with pytest.raises(ParticipationGroundingError, match="exactly match"):
        compile_participation_bindings(
            assessments[:-1], expected_targets=targets
        )


def test_duplicate_participant_derivative_roles_hard_fail() -> None:
    instances = (_instance("甲", 1), _instance("乙", 2), _instance("丙", 3))
    targets = participation_local_targets(REGISTRY, instances)
    conflicts = (
        _target(targets, "instigation", (instances[0], instances[1])),
        _target(targets, "aiding", (instances[0], instances[2])),
    )
    with pytest.raises(ParticipationGroundingError, match="multiple derivative"):
        compile_participation_bindings(
            _assessments(instances, conflicts), expected_targets=targets
        )


def test_same_logical_edge_with_instigation_and_aiding_hard_fails() -> None:
    principal = _instance("乙", 3)
    instigator = _instance("甲", 1)
    aider_identity = _instance("甲", 2)
    targets = (
        ParticipationLocalTarget("instigation", (instigator, principal)),
        ParticipationLocalTarget("aiding", (aider_identity, principal)),
    )
    assessments = tuple(
        ParticipationLocalAssessment(target, "TRUE") for target in targets
    )
    with pytest.raises(
        ParticipationGroundingError, match="CONFLICTING_PARTICIPATION_MODE"
    ):
        compile_participation_bindings(assessments, expected_targets=targets)


def test_authored_instigator_mode_subsumes_aider_and_preserves_audit() -> None:
    principal = _instance("乙", 3)
    instigator = _instance("甲", 1)
    aider_identity = _instance("甲", 2)
    targets = (
        ParticipationLocalTarget("instigation", (instigator, principal)),
        ParticipationLocalTarget("aiding", (aider_identity, principal)),
    )
    assessments = tuple(
        ParticipationLocalAssessment(target, "TRUE") for target in targets
    )
    bindings = compile_participation_bindings(
        assessments, expected_targets=targets, registry=REGISTRY
    )
    assert bindings.derivative_links == ((instigator, principal, "instigator"),)
    assert bindings.mode_resolutions == ({
        "case_id": instigator.case_id,
        "offense_ref": instigator.offense_ref,
        "participant_id": "甲",
        "principal_instance": {
            "case_id": principal.case_id,
            "actor_id": "乙",
            "offense_ref": principal.offense_ref,
            "occurrence_id": principal.occurrence_id,
        },
        "dominant_mode": "instigator",
        "subsumed_mode": "aider",
        "raw_dominant_truth": "TRUE",
        "raw_subsumed_truth": "TRUE",
        "resolution_basis": "authored_participation_policy",
    },)


def test_unknown_local_relation_emits_no_positive_binding() -> None:
    instances = (_instance("甲", 1), _instance("乙", 2))
    targets = participation_local_targets(REGISTRY, instances)
    unresolved = _target(targets, "aiding", instances)
    bindings = compile_participation_bindings(
        _assessments(instances, unknown_targets=(unresolved,)),
        expected_targets=targets,
    )
    assert bindings.co_principal_sources == ()
    assert bindings.derivative_links == ()


def test_overlapping_maximal_co_groups_hard_fail() -> None:
    instances = (_instance("甲", 1), _instance("乙", 2), _instance("丙", 3))
    targets = participation_local_targets(REGISTRY, instances)
    groups = (
        _target(targets, "co_principal_group", instances[:2]),
        _target(targets, "co_principal_group", instances[1:]),
    )
    with pytest.raises(ParticipationGroundingError, match="overlapping"):
        compile_participation_bindings(
            _assessments(instances, groups), expected_targets=targets
        )


def test_a_narrower_group_from_another_interaction_collapses_instead_of_conflicting() -> None:
    """정규화가 subset 억제보다 먼저 와야 한다.

    같은 관계가 두 상호작용에서 확인되면 참가 후보의 occurrence가 상호작용마다 다르다.
    그 raw instance로 먼저 subset 억제를 하면 {甲,丙}이 {甲,乙,丙}의 부분집합으로 보이지
    않아 살아남고, 그 뒤 정규화해도 이미 늦어 甲의 실현에서 겹쳐 계약 위반으로 죽는다.
    `r13_p1_q1`이 정확히 그 모양이었다 -- 丙의 후보 occurrence만 달랐고 행위자 구성으로는
    한쪽이 다른 쪽에 포함되어 있었다.
    """
    principal = OffenseInstanceKey("case", "甲", "offense.theft", "realization:001")
    first = OffenseInstanceKey(
        "case", "乙", "offense.theft", f"{PARTICIPATION_OCCURRENCE_PREFIX}001:001:乙:aa"
    )
    third_a = OffenseInstanceKey(
        "case", "丙", "offense.theft", f"{PARTICIPATION_OCCURRENCE_PREFIX}001:001:丙:aa"
    )
    third_b = OffenseInstanceKey(
        "case", "丙", "offense.theft", f"{PARTICIPATION_OCCURRENCE_PREFIX}001:003:丙:bb"
    )
    wide = ParticipationLocalTarget("co_principal_group", (first, principal, third_a))
    narrow = ParticipationLocalTarget("co_principal_group", (third_b, principal))

    bindings = compile_participation_bindings(
        (
            ParticipationLocalAssessment(wide, "TRUE"),
            ParticipationLocalAssessment(narrow, "TRUE"),
        ),
        expected_targets=(wide, narrow),
    )

    actors = {left.actor_id for left, _right in bindings.co_principal_sources}
    assert actors == {"甲", "乙", "丙"}


def test_genuinely_conflicting_groups_still_fail_closed() -> None:
    """접히는 것은 부분집합뿐이다. 행위자 구성이 서로 다투면 여전히 계약 위반이다."""
    principal = OffenseInstanceKey("case", "甲", "offense.theft", "realization:001")
    with_b = OffenseInstanceKey(
        "case", "乙", "offense.theft", f"{PARTICIPATION_OCCURRENCE_PREFIX}001:001:乙:aa"
    )
    with_c = OffenseInstanceKey(
        "case", "丙", "offense.theft", f"{PARTICIPATION_OCCURRENCE_PREFIX}001:002:丙:bb"
    )
    left = ParticipationLocalTarget("co_principal_group", (with_b, principal))
    right = ParticipationLocalTarget("co_principal_group", (with_c, principal))

    with pytest.raises(ParticipationGroundingError, match="overlapping co-principal"):
        compile_participation_bindings(
            (
                ParticipationLocalAssessment(left, "TRUE"),
                ParticipationLocalAssessment(right, "TRUE"),
            ),
            expected_targets=(left, right),
        )
