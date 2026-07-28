"""
test_schema_registry.py
Unit tests for Schema Registry and Draft 7 JSON Schema generation.
"""

from __future__ import annotations

import pytest
from idpr.pipeline.schema_registry import PREDICATE_SCHEMA_REGISTRY, get_fact_graph_json_schema

def test_schema_registry_has_32_predicates():
    """Verifies that the schema registry contains exactly 32 canonical predicates."""
    preds = PREDICATE_SCHEMA_REGISTRY["predicates"]
    assert len(preds) == 32

def test_json_schema_draft_7_structure():
    """Verifies generated JSON Schema has valid Draft 7 structure for vLLM structured output."""
    schema = get_fact_graph_json_schema()
    assert schema["type"] == "object"
    assert "case_id" in schema["properties"]
    assert "actors" in schema["properties"]
    assert "facts" in schema["properties"]
    
    enum_preds = schema["properties"]["facts"]["items"]["properties"]["predicate"]["enum"]
    assert len(enum_preds) == 32
    assert "dwelling_intrusion_committed" in enum_preds
    assert "arson_act" in enum_preds
    assert "unlawful_taking" in enum_preds
