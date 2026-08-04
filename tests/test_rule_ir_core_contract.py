from __future__ import annotations

from pathlib import Path

import pytest

from idpr.neural.core_contract import (
    CoreContractError,
    assessment_groups,
    context_packet,
    role_binding_schema,
    validate_role_binding,
)
from idpr.rulegen.core_profile import load_core_profiles
from idpr.rulegen.core_runtime import execute_core_unit
from idpr.rulegen.native_host import DEFAULT_SCLI


def _profiles() -> dict:
    return load_core_profiles()["units"]


def test_role_binding_is_conditioned_on_the_selected_unit_contract() -> None:
    fraud = _profiles()["fraud"]
    schema = role_binding_schema(case_id="case-1", issue_id="issue-1", profile=fraud)
    required = schema["properties"]["role_bindings"]["required"]
    assert required == [
        "defendant_id", "deceived_person_id", "disposer_id",
        "property_owner_id", "beneficiary_id",
    ]
    assert schema["properties"]["selected_tracks"]["items"]["enum"] == ["base"]


def test_role_binding_rejects_ungrounded_or_unknown_entities() -> None:
    fraud = _profiles()["fraud"]
    text = "乙은 B에게 거짓말하여 B가 乙에게 돈을 주었다."
    payload = {
        "version": "1.0.0", "case_id": "case-1", "issue_id": "issue-1",
        "unit_id": "fraud", "selected_tracks": ["base"],
        "entities": [
            {"entity_id": "eul", "label": "乙", "source_quotes": ["乙"]},
            {"entity_id": "b", "label": "B", "source_quotes": ["B"]},
        ],
        "role_bindings": {
            "defendant_id": {"entity_id": "eul", "source_quotes": ["乙은"], "reason": "행위자"},
            "deceived_person_id": {"entity_id": "b", "source_quotes": ["B에게"], "reason": "기망 상대방"},
            "disposer_id": {"entity_id": "b", "source_quotes": ["B가 乙에게 돈을 주었다"], "reason": "교부자"},
            "property_owner_id": {"entity_id": "b", "source_quotes": ["B가 乙에게 돈을 주었다"], "reason": "재산권자"},
            "beneficiary_id": {"entity_id": "eul", "source_quotes": ["乙에게 돈을 주었다"], "reason": "수익자"},
        },
        "relations": [{
            "relation_id": "r1", "subject_id": "b", "relation": "금전교부",
            "object_id": "eul", "source_quote": "B가 乙에게 돈을 주었다",
        }],
    }
    validate_role_binding(
        payload, case_text=text, case_id="case-1", issue_id="issue-1", profile=fraud
    )
    payload["role_bindings"]["disposer_id"]["entity_id"] = "ghost"
    with pytest.raises(CoreContractError, match="unknown entity"):
        validate_role_binding(
            payload, case_text=text, case_id="case-1", issue_id="issue-1", profile=fraud
        )


def test_assessment_is_grouped_and_context_cannot_change_predicates() -> None:
    homicide = _profiles()["homicide"]
    groups = assessment_groups(homicide, ["base"], max_predicates=8)
    ids = [item["predicate_id"] for group in groups for item in group["predicates"]]
    assert len(groups) == 2
    assert len(ids) == 14
    assert len(ids) == len(set(ids))
    packet = context_packet(homicide, ids[:2])
    assert packet["predicate_set_mutable"] is False
    assert packet["external_search_used"] is False
    assert set(packet["items"]) == set(ids[:2])


@pytest.mark.skipif(not DEFAULT_SCLI.is_file(), reason="pinned scli is not installed")
def test_core_projection_reaches_a_real_scallop_derivation(tmp_path: Path) -> None:
    theft = _profiles()["theft"]
    assessments = {
        item["predicate_id"]: {"status": "satisfied"}
        for item in theft["model_input_predicates"]
    }
    result = execute_core_unit(
        profile=theft,
        case_id="case-1",
        role_values={
            "case_id": "case-1", "defendant_id": "d", "owner_id": "o",
            "possessor_id": "p",
        },
        selected_tracks=["base"],
        assessments=assessments,
        work_dir=tmp_path,
    )
    assert result["runtime"] == "scallop_scli_core_projection"
    assert result["track_outcomes"]["base"]["symbolic_conclusion"] == "established"
    assert result["query_results"]["theft_established"] is True

    first = next(iter(assessments))
    assessments[first] = {"status": "not_satisfied"}
    negative = execute_core_unit(
        profile=theft,
        case_id="case-1",
        role_values={
            "case_id": "case-1", "defendant_id": "d", "owner_id": "o",
            "possessor_id": "p",
        },
        selected_tracks=["base"], assessments=assessments,
        work_dir=tmp_path / "negative",
    )
    assert negative["track_outcomes"]["base"]["symbolic_conclusion"] == "not_established"

    assessments[first] = {"status": "unknown"}
    unknown = execute_core_unit(
        profile=theft,
        case_id="case-1",
        role_values={
            "case_id": "case-1", "defendant_id": "d", "owner_id": "o",
            "possessor_id": "p",
        },
        selected_tracks=["base"], assessments=assessments,
        work_dir=tmp_path / "unknown",
    )
    assert unknown["track_outcomes"]["base"]["symbolic_conclusion"] == "undetermined"
