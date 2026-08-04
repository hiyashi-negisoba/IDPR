"""Regression test verifying that alternative OR component cards do not trigger false theft_not_established."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from idpr.rulegen.scallop_runtime import run_scenario
from idpr.rulegen.native_host import DEFAULT_SCLI, PROJECT_ROOT
from scripts.build_property_rule_ir import UnitBuilder, read_json, UNITS, PHASE_MAP, UNIT_MANIFEST


def test_property_theft_alternative_or_cards_established(tmp_path: Path) -> None:
    """Card A (anothers_property) satisfied while Card B (vehicle_internal_ownership_agreement) is not_satisfied.
    
    Before fix: Card B being not_satisfied triggered mandatory_negative -> theft_not_established = True.
    After fix: theft_not_established is False because mandatory_negative requires ALL alternative cards to be not_satisfied.
    """
    compiled_scl_path = PROJECT_ROOT / "rules/generated/property_theft_v1_candidate.scl"
    
    if not DEFAULT_SCLI.exists():
        pytest.skip(f"scli binary not found at {DEFAULT_SCLI}")

    manifest = read_json(UNIT_MANIFEST)
    phase_rows = read_json(PHASE_MAP)["rows"]
    card_set = read_json(UNITS / "theft.json")
    
    builder = UnitBuilder("theft", card_set, phase_rows)
    rule_ir = builder.build()
    compiled_scl = compiled_scl_path.read_text(encoding="utf-8")

    # Alternative ownership cards:
    # Card A: art329_sec2.theft_object_anothers_property_in_possession (standard_input)
    # Card B: art329_sec2_1.vehicle_internal_ownership_agreement (standard_input)
    scenario = {
        "scenario_id": "test_alternative_or_case",
        "case_id": "case_001",
        "defendant_id": "def_001",
        "owner_id": "owner_001",
        "possessor_id": "poss_001",
        "selected_card_ids": [
            "art329_sec2.theft_object_anothers_property_in_possession",
            "art329_sec2_1.vehicle_internal_ownership_agreement",
        ],
        "assessments": [
            # Alternative Ownership Card A: SATISFIED
            {
                "assessment_id": "assessment_0001",
                "card_id": "art329_sec2.theft_object_anothers_property_in_possession",
                "status": "satisfied",
                "provable": True,
            },
            # Alternative Ownership Card B: NOT_SATISFIED (should NOT trigger theft_not_established)
            {
                "assessment_id": "assessment_0002",
                "card_id": "art329_sec2_1.vehicle_internal_ownership_agreement",
                "status": "not_satisfied",
                "provable": True,
            },
        ],
        "distinct_entities": [
            ["def_001", "owner_001"],
            ["def_001", "poss_001"],
        ],
        "close_case": True,
    }

    query_relations = [
        "theft_object_ownership_satisfied",
        "theft_not_established",
    ]

    results = run_scenario(
        rule_ir=rule_ir,
        compiled_source=compiled_scl,
        scenario=scenario,
        query_relations=query_relations,
        scli_path=DEFAULT_SCLI,
        work_dir=tmp_path,
    )

    assert results["theft_object_ownership_satisfied"]["nonempty"] is True
    # The critical fix assertion: theft_not_established MUST BE False
    assert results["theft_not_established"]["nonempty"] is False
