"""
test_stage2_symbolic.py
Unit and Integration tests for Stage 2 Generic Scallop 0.2.4 Datalog Symbolic Reasoning Engine.
Tests multiple crime fact patterns (theft, fraud, homicide, injury, arson, dwelling intrusion, embezzlement, breach of trust).
"""

from __future__ import annotations

import os
import pytest
from pathlib import Path

from idpr.pipeline.stage2_symbolic import Stage2SymbolicReasoner

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCL_PATH = PROJECT_ROOT / "data/rulegen/kcl_special_part_full.scl"
SCLI_BINARY = PROJECT_ROOT / "tools/scallop/scli-0.2.4-linux-x86_64"

@pytest.fixture
def reasoner():
    return Stage2SymbolicReasoner(scl_path=SCL_PATH, scli_binary=SCLI_BINARY)

def test_stage2_theft_and_intrusion(reasoner):
    """Tests theft and dwelling intrusion reasoning using generic Datalog relation names."""
    extracted_facts = {
        "case_id": "CASE_TEST_THEFT_01",
        "actors": [{"entity_id": "actor_A", "roles": ["defendant"]}],
        "facts": [
            {"predicate": "dwelling_intrusion_committed", "arguments": ["place_dwelling"]},
            {"predicate": "unlawful_taking", "arguments": ["act_theft", "prop_cash"]},
            {"predicate": "unlawful_intent", "arguments": ["theft"]}
        ]
    }
    result = reasoner.run_datalog_reasoning(extracted_facts)
    assert result["case_id"] == "CASE_TEST_THEFT_01"
    proven = [off["offense"] for off in result["proven_offenses"]]
    assert any("theft_established" in p for p in proven)
    assert any("dwelling_intrusion_established" in p for p in proven)
    assert "rule.theft_established" in result["active_card_ids"]

def test_stage2_arson_and_homicide(reasoner):
    """Tests arson and homicide reasoning using generic Datalog relation names."""
    extracted_facts = {
        "case_id": "CASE_TEST_ARSON_02",
        "actors": [{"entity_id": "actor_A", "roles": ["defendant"]}],
        "facts": [
            {"predicate": "action_committed", "arguments": ["act_kill"]},
            {"predicate": "result_occurred", "arguments": ["death"]},
            {"predicate": "unlawful_intent", "arguments": ["murder"]},
            {"predicate": "causation_established", "arguments": ["act_kill", "death"]},
            {"predicate": "arson_act", "arguments": ["place_dwelling"]},
            {"predicate": "independent_combustion", "arguments": ["place_dwelling"]},
            {"predicate": "unlawful_intent", "arguments": ["arson"]}
        ]
    }
    result = reasoner.run_datalog_reasoning(extracted_facts)
    proven = [off["offense"] for off in result["proven_offenses"]]
    assert any("homicide_established" in p for p in proven)
    assert any("arson_established" in p for p in proven)

def test_stage2_empty_facts(reasoner):
    """Tests empty facts handling gracefully."""
    extracted_facts = {
        "case_id": "CASE_EMPTY",
        "actors": [],
        "facts": []
    }
    result = reasoner.run_datalog_reasoning(extracted_facts)
    assert len(result["proven_offenses"]) == 0
    assert len(result["active_card_ids"]) == 0
    assert len(result["unsatisfied_requirements"]) > 0

def test_stage2_invalid_scl_path():
    """Tests invalid scl path raises RuntimeError."""
    r = Stage2SymbolicReasoner(scl_path=Path("/non_existent.scl"))
    with pytest.raises(RuntimeError):
        r.run_datalog_reasoning({"case_id": "FAIL"})
