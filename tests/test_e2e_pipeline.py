"""
test_e2e_pipeline.py
Automated E2E Integration tests for the 2 Official Standard Test Cases.
Verifies exact ground truth verdicts according to Korean Criminal Law principles:
Case 2: Bribery Delivery (GUILTY) + Fraud (GUILTY) Concurrence, Embezzlement (NOT GUILTY).
"""

from __future__ import annotations

import pytest
from pathlib import Path
from idpr.pipeline.e2e_runner import KCL1730PipelineRunner
from scripts.run_kcl_1730_e2e_pipeline import TEST_CASE_1, TEST_CASE_2

@pytest.fixture
def runner():
    return KCL1730PipelineRunner(base_url=None, model=None)

def test_e2e_official_case_1_realistic_property_nonproperty(runner):
    """Tests official test case 1 (Realistic Complex Crime Case)."""
    result = runner.run_e2e(TEST_CASE_1)
    assert result["case_id"] == "CASE_KCL1730_2026_REAL_001"
    proven = [off["offense"] for off in result["symbolic_results"]["proven_offenses"]]
    assert len(proven) >= 3
    assert any("dwelling_intrusion_established" in p for p in proven)
    assert any("theft_established" in p for p in proven)
    assert any("arson_established" in p for p in proven)

def test_e2e_official_case_2_user_provided_bribery_fraud(runner):
    """Tests official test case 2 (User-provided Bribery Fraud & Misappropriation Case).
    Ground Truth Verification:
    1. 증뢰물전달죄 (형법 제133조 제2항) ➔ 성립 (GUILTY)
    2. 사기죄 (형법 제347조 제1항) ➔ 성립 (GUILTY)
    3. 횡령죄 (형법 제355조 제1항) ➔ 불성립 (NOT GUILTY)
    """
    result = runner.run_e2e(TEST_CASE_2)
    assert result["case_id"] == "CASE_KCL1730_2026_BRIBERY_FRAUD_002"
    proven = [off["offense"] for off in result["symbolic_results"]["proven_offenses"]]
    
    # 1. Bribery Delivery (증뢰물전달죄) & Fraud (사기죄) MUST be proven
    assert any("bribery_delivery_established" in p for p in proven)
    assert any("fraud_established" in p for p in proven)
    assert any("bribery_fraud_concurrence" in p for p in proven)

    # 2. Embezzlement (횡령죄) MUST NOT be proven (불법원인급여로 인한 타인 재물성 조각)
    assert not any("embezzlement_established" in p for p in proven)
