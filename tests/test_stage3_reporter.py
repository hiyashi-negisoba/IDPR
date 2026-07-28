"""
test_stage3_reporter.py
Unit tests for Stage 3 RAG exact-fetch and report generation.
"""

from __future__ import annotations

import pytest
from pathlib import Path
from idpr.pipeline.stage3_reporter import Stage3Reporter

def test_stage3_fetch_rag_context():
    """Tests RAG exact-fetch and alias fallback matching."""
    reporter = Stage3Reporter(client=None)
    card_ids = [
        "art164_sec2_1.completion_independent_combustion_variant",
        "art319_sec1.dwelling_entry",
        "art329_sec1.theft_element"
    ]
    snippets = reporter.fetch_rag_context(card_ids)
    assert len(snippets) == 3
    assert any("독립연소" in s or "독립적으로" in s for s in snippets)
    assert any("퇴거" in s or "주거" in s or "319" in s for s in snippets)

def test_stage3_generate_dry_run_report():
    """Tests dry-run legal review report output structure."""
    reporter = Stage3Reporter(client=None)
    case_data = {
        "case_id": "CASE_TEST_001",
        "fact_pattern": "피고인 A는 B의 주거에 무단 침입하여 현금을 절취하였다."
    }
    extracted_facts = {"case_id": "CASE_TEST_001", "facts": []}
    symbolic_results = {
        "engine": "Scallop Datalog v0.2.4",
        "rulebase": "KCL 1,730 Special Part Unified Rulebase",
        "proven_offenses": [
            {"offense": "절도죄 (형법 제329조)", "verdict": "성립 (GUILTY)", "rule_code": "art329_sec1.theft_element", "reasoning": "점유 침탈 충족"}
        ],
        "active_card_ids": ["art329_sec1.theft_element"],
        "unsatisfied_requirements": []
    }
    report = reporter.generate_report(case_data, extracted_facts, symbolic_results)
    assert "# 🏛️ [CASE_TEST_001] 종합 형사 법리 검토서" in report
    assert "절도죄 (형법 제329조)" in report
    assert "성립 (GUILTY)" in report
