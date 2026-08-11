from __future__ import annotations

from pathlib import Path

import pytest

from idpr.v2.compile import CompiledOffense, compile_offense
from idpr.v2.gold_factual_identity import GoldOccurrence
from idpr.v2.participation import effective_attributable_slots, participation_policy_for
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.participation import apply_attribution
from idpr.v2.runtime.participation_grounding import (
    ParticipationGroundingError,
    ParticipationRouteAssessment,
    participation_bindings_from_assessments,
    participation_request_payload,
    participation_route_targets,
    validate_participation_output,
)
from idpr.v2.runtime.truths import CaseTruths

ROOT = Path(__file__).resolve().parents[1]


def test_standard_co_principal_policy_attributes_conduct() -> None:
    registry = load_definitions(ROOT / "data/v2/definitions")
    policy = participation_policy_for(registry)
    offense = registry.get("offense.theft")
    assert policy is not None and offense is not None
    assert effective_attributable_slots(policy, offense) == frozenset({"conduct"})


def test_co_principal_source_conduct_reaches_target_without_mutating_input() -> None:
    registry = load_definitions(ROOT / "data/v2/definitions")
    compiled = compile_offense(registry, "offense.theft")
    assert isinstance(compiled, CompiledOffense)
    target = OffenseInstanceKey("case", "甲", "offense.theft", "gocc:001")
    source = OffenseInstanceKey("case", "乙", "offense.theft", "gocc:002")
    ref = "ground_fact.taking_conduct"
    truths = CaseTruths(predicate={(target, ref): "FALSE", (source, ref): "TRUE"})
    attributed = apply_attribution(
        registry, compiled, "offense.theft", target, (source,), truths
    )
    assert truths.predicate[(target, ref)] == "FALSE"
    assert attributed.predicate[(target, ref)] == "TRUE"


def test_participation_planner_enumerates_one_exclusive_choice_per_participant() -> None:
    registry = load_definitions(ROOT / "data/v2/definitions")
    left = OffenseInstanceKey("case", "甲", "offense.theft", "gocc:001")
    right = OffenseInstanceKey("case", "乙", "offense.theft", "gocc:002")
    targets = participation_route_targets(registry, (left, right))
    assert len(targets) == 2
    assert tuple(option.option_id for option in targets[0].options) == (
        "none",
        "unknown",
        "co_principal:0001",
        "instigator:0001",
        "aider:0001",
    )
    assert all(
        source.actor_id != target.participant.actor_id
        for target in targets
        for option in target.options
        for source in option.sources
    )


def test_participation_request_has_only_exact_endpoint_evidence_and_compact_truths() -> None:
    registry = load_definitions(ROOT / "data/v2/definitions")
    left = OffenseInstanceKey("case", "甲", "offense.theft", "gocc:001")
    right = OffenseInstanceKey("case", "乙", "offense.theft", "gocc:002")
    target = participation_route_targets(registry, (left, right))[0]
    sources = ("甲이 망을 보았다.", "乙이 물건을 가져갔다.")
    occurrences = tuple(
        GoldOccurrence(f"gocc:{index:03d}", actor, source, 0, len(source))
        for index, (actor, source) in enumerate(zip(("甲", "乙"), sources, strict=True), 1)
    )
    payload = participation_request_payload(
        registry=registry, occurrences=occurrences, targets=(target,)
    )
    assert set(payload) == {
        "occurrence_evidence",
        "offense_definition",
        "route_target",
        "mode_contract",
    }
    assert "case_text" not in payload
    values = validate_participation_output(
        {"option_id": "co_principal:0001"},
        targets=(target,),
    )
    assert values == (
        ParticipationRouteAssessment(target, "co_principal:0001"),
    )
    with pytest.raises(ParticipationGroundingError):
        validate_participation_output(
            {"option_id": "not-an-option"},
            targets=(target,),
        )


def test_participation_binding_cannot_select_two_derivative_modes() -> None:
    accessory = OffenseInstanceKey("case", "甲", "offense.theft", "gocc:001")
    principal = OffenseInstanceKey("case", "乙", "offense.theft", "gocc:002")
    target = participation_route_targets(
        load_definitions(ROOT / "data/v2/definitions"), (accessory, principal)
    )[0]
    assessments = (ParticipationRouteAssessment(target, "instigator:0001"),)
    bindings = participation_bindings_from_assessments(assessments)
    assert bindings.derivative_links == ((accessory, principal, "instigator"),)
    with pytest.raises(ParticipationGroundingError):
        participation_bindings_from_assessments((*assessments, *assessments))
