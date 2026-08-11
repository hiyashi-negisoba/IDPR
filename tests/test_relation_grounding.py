from __future__ import annotations

from pathlib import Path

import pytest

from idpr.v2.gold_factual_identity import GoldOccurrence
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.identity import OffenseInstanceKey
from idpr.v2.runtime.relation_grounding import (
    RelationGroundingError,
    relation_assessment_targets,
    relation_definitions,
    relation_request_payload,
    validate_relation_output,
)

ROOT = Path(__file__).resolve().parents[1]


def _fixture():
    registry = load_definitions(ROOT / "data/v2/definitions")
    instance = OffenseInstanceKey(
        "case", "甲", "derived_offense.rape_causing_intentional_injury", "gocc:001"
    )
    targets = relation_assessment_targets(registry, (instance,))
    source = "강간 과정에서 피해자가 넘어져 다쳤다."
    occurrence = GoldOccurrence("gocc:001", "甲", source, 0, len(source))
    definitions = relation_definitions(
        registry, (target.key.definition_key.relation_ref for target in targets)
    )
    return occurrence, definitions, targets


def test_relation_target_carries_fixed_endpoint_identity() -> None:
    occurrence, definitions, targets = _fixture()
    payload = relation_request_payload(
        evidence_occurrence=occurrence, definitions=definitions, targets=targets
    )
    endpoints = payload["relation_targets"][0]["endpoints"]
    assert endpoints == {
        "left_ref": "offense.rape",
        "right_ref": "offense.injury",
        "left_view": "event",
        "right_view": "event",
    }
    assert "case_text" not in payload


def test_relation_compact_array_has_exact_order_and_cardinality() -> None:
    _, _, targets = _fixture()
    values = validate_relation_output({"truths": ["TRUE", "UNKNOWN"]}, targets=targets)
    assert tuple(value.target for value in values) == targets
    with pytest.raises(RelationGroundingError):
        validate_relation_output({"truths": ["TRUE"]}, targets=targets)
    with pytest.raises(RelationGroundingError):
        validate_relation_output({"truths": ["TRUE", "TRUE"], "extra": []}, targets=targets)
