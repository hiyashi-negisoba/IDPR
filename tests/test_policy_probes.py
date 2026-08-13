"""The generic probe compiler. Its job is to make "authored but never asked" impossible."""

from pathlib import Path

import pytest

from idpr.v2 import policy_probes
from idpr.v2.policy_probes import (
    OFFENSE_INSTANCE,
    PARTICIPATION_CANDIDATE,
    PolicyProbeError,
    neural_target_refs,
    probe_requirements,
    unsatisfied_requirements,
    validate_probe_refs,
)
from idpr.v2.registry import load_definitions


@pytest.fixture(scope="module")
def registry():
    return load_definitions(Path("data/v2/definitions"))


def test_every_probe_ref_resolves_to_the_kind_its_supply_implies(registry) -> None:
    assert validate_probe_refs(registry) == ()


def test_all_three_policies_declare_requirements(registry) -> None:
    owners = {requirement.policy_id for requirement in probe_requirements(registry)}
    assert owners == {
        "mistake_policy.korean_law_concrete_fact",
        "excess_policy.korean_law_standard",
        "offense.ancestral_homicide",
    }


def test_requirements_split_by_the_object_they_attach_to(registry) -> None:
    instance_owners = {
        requirement.policy_id
        for requirement in probe_requirements(registry, applies_to=OFFENSE_INSTANCE)
    }
    candidate_owners = {
        requirement.policy_id
        for requirement in probe_requirements(registry, applies_to=PARTICIPATION_CANDIDATE)
    }
    assert instance_owners == {"mistake_policy.korean_law_concrete_fact"}
    assert candidate_owners == {
        "excess_policy.korean_law_standard",
        "offense.ancestral_homicide",
    }


def test_only_neural_requirements_become_call_2_targets(registry) -> None:
    """Declaring a policy must not widen neural load by itself: structural relations are read off
    bindings and provenance is carried from upstream."""
    targets = neural_target_refs(registry)
    assert "legal_element.object_misidentification" in targets
    assert "legal_element.lineal_ascendant_of_self_or_spouse_status" in targets
    assert "relation.intended_object_divergence" not in targets
    assert not any(ref.startswith("provenance.") for ref in targets)


def test_a_missing_input_is_reported_as_a_gap_with_the_authored_marker(registry) -> None:
    """This is the doctrine dead loop, made visible instead of silent."""
    gaps = unsatisfied_requirements(registry, available_refs=(), applies_to=OFFENSE_INSTANCE)
    markers = {gap.unresolved_marker for gap in gaps}
    assert markers == {"UNRESOLVED_MISTAKE_BINDING"}
    assert {gap.ref for gap in gaps} == {
        "relation.intended_object_divergence",
        "legal_element.object_misidentification",
        "legal_element.intent",
    }


def test_supplying_everything_leaves_no_gap(registry) -> None:
    every_ref = {requirement.ref for requirement in probe_requirements(registry)}
    assert unsatisfied_requirements(registry, available_refs=every_ref) == ()


def test_an_optional_requirement_is_not_a_gap(registry) -> None:
    """결과적 가중범 분기에서만 필요한 예견가능성이 없다고 초과 판정 전체가 막히면 안 된다."""
    supplied = {
        requirement.ref
        for requirement in probe_requirements(registry)
        if not requirement.optional
    }
    gaps = unsatisfied_requirements(registry, available_refs=supplied)
    assert gaps == ()
    assert any(
        requirement.optional
        and requirement.ref
        == "legal_element.foreseeability_of_aggravated_result_by_participant"
        for requirement in probe_requirements(registry)
    )


def test_an_unknown_target_kind_is_rejected(registry) -> None:
    with pytest.raises(PolicyProbeError, match="unknown probe target kind"):
        probe_requirements(registry, applies_to="whatever")


def test_a_dangling_probe_ref_is_reported(registry) -> None:
    entry = registry.get("mistake_policy.korean_law_concrete_fact")
    broken = type(entry)(
        id=entry.id,
        kind=entry.kind,
        payload={
            **entry.payload,
            "probe": {
                **entry.payload["probe"],
                "requires": [{"ref": "legal_element.nonexistent", "supply": "neural_predicate"}],
            },
        },
        source_file=entry.source_file,
    )
    patched = type(registry)(
        by_id={**registry.by_id, broken.id: broken},
        by_kind={**registry.by_kind, "mistake_policy": (broken,)},
    )
    errors = validate_probe_refs(patched)
    assert any("does not exist" in message for message in errors)


def test_a_structural_supply_pointing_at_a_predicate_is_rejected(registry) -> None:
    """supply와 kind가 어긋나면 host가 읽어야 할 값을 모델에게 묻거나 그 반대가 된다."""
    entry = registry.get("mistake_policy.korean_law_concrete_fact")
    broken = type(entry)(
        id=entry.id,
        kind=entry.kind,
        payload={
            **entry.payload,
            "probe": {
                **entry.payload["probe"],
                "requires": [
                    {"ref": "legal_element.intent", "supply": policy_probes.STRUCTURAL_RELATION}
                ],
            },
        },
        source_file=entry.source_file,
    )
    patched = type(registry)(
        by_id={**registry.by_id, broken.id: broken},
        by_kind={**registry.by_kind, "mistake_policy": (broken,)},
    )
    errors = validate_probe_refs(patched)
    assert any("expected one of ['relation']" in message for message in errors)
