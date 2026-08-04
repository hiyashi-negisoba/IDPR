from __future__ import annotations

from pathlib import Path

import pytest

from idpr.neural.core_contract import (
    core_issue_selection_schema,
    core_unit_analysis_schema,
    needed_predicate_ids,
    selected_track_closure,
    validate_core_issue_selection,
    validate_core_unit_analysis,
)
from idpr.rulegen.core_profile import load_core_profiles
from idpr.rulegen.core_runtime import execute_core_unit
from idpr.rulegen.native_host import DEFAULT_SCLI


def _profiles() -> dict:
    return load_core_profiles()["units"]


def test_selection_contract_contains_only_issue_identity_and_conduct() -> None:
    schema = core_issue_selection_schema(
        case_id="case-1", unit_ids=["fraud", "theft"]
    )
    item = schema["properties"]["issues"]["items"]
    assert set(item["required"]) == {"unit_id", "issue_label", "subject", "conduct"}
    assert "facts" not in schema["properties"]
    payload = {
        "case_id": "case-1",
        "issues": [{
            "unit_id": "theft", "issue_label": "절도",
            "subject": "甲", "conduct": "C의 수표를 가져갔다",
        }],
    }
    validate_core_issue_selection(
        payload, case_id="case-1", unit_ids=["fraud", "theft"]
    )


def test_analysis_contract_combines_tracks_roles_and_all_predicates() -> None:
    fraud = _profiles()["fraud"]
    schema = core_unit_analysis_schema(
        case_id="case-1", issue_id="issue-01", profile=fraud
    )
    assert set(schema["required"]) == {
        "case_id", "issue_id", "selected_tracks", "role_values", "assessments"
    }
    predicate_ids = [item["predicate_id"] for item in fraud["model_input_predicates"]]
    assert schema["properties"]["assessments"]["required"] == predicate_ids
    roles = {
        item["name"]: item["name"]
        for item in fraud["role_contract"]["arguments"]
        if item["name"] != "case_id"
    }
    payload = {
        "case_id": "case-1",
        "issue_id": "issue-01",
        "selected_tracks": ["base"],
        "role_values": roles,
        "assessments": {
            predicate_id: {"status": "satisfied", "reason": "사실상 인정된다"}
            for predicate_id in predicate_ids
        },
    }
    validate_core_unit_analysis(
        payload, case_id="case-1", issue_id="issue-01", profile=fraud
    )


def test_every_profile_builds_one_lean_analysis_schema() -> None:
    for unit_id, profile in _profiles().items():
        schema = core_unit_analysis_schema(
            case_id="case-1", issue_id="issue-01", profile=profile
        )
        assert schema["properties"]["selected_tracks"]["minItems"] == 1, unit_id
        assert schema["properties"]["assessments"]["required"], unit_id


def test_track_closure_and_needed_predicates_are_deterministic() -> None:
    homicide = _profiles()["homicide"]
    selected = [homicide["tracks"][-1]["track_id"]]
    closure = selected_track_closure(homicide, selected)
    needed = needed_predicate_ids(homicide, selected)
    assert closure
    assert needed
    assert len(needed) == len(set(needed))


@pytest.mark.skipif(not DEFAULT_SCLI.is_file(), reason="pinned scli is not installed")
def test_core_projection_reaches_a_real_scallop_derivation(tmp_path: Path) -> None:
    theft = _profiles()["theft"]
    assessments = {
        item["predicate_id"]: {"status": "satisfied"}
        for item in theft["model_input_predicates"]
    }
    roles = {
        "case_id": "case-1", "defendant_id": "d", "owner_id": "o",
        "possessor_id": "p",
    }
    result = execute_core_unit(
        profile=theft, case_id="case-1", role_values=roles,
        selected_tracks=["base"], assessments=assessments, work_dir=tmp_path,
    )
    assert result["runtime"] == "scallop_scli_core_projection"
    assert result["track_outcomes"]["base"]["symbolic_conclusion"] == "established"

    first = next(iter(assessments))
    assessments[first] = {"status": "not_satisfied"}
    negative = execute_core_unit(
        profile=theft, case_id="case-1", role_values=roles,
        selected_tracks=["base"], assessments=assessments,
        work_dir=tmp_path / "negative",
    )
    assert negative["track_outcomes"]["base"]["symbolic_conclusion"] == "not_established"

    assessments[first] = {"status": "unknown"}
    unknown = execute_core_unit(
        profile=theft, case_id="case-1", role_values=roles,
        selected_tracks=["base"], assessments=assessments,
        work_dir=tmp_path / "unknown",
    )
    assert unknown["track_outcomes"]["base"]["symbolic_conclusion"] == "undetermined"
