from __future__ import annotations

import pytest

from idpr.eval.input_formatter import InputLeakageError, assert_no_leaked_fields
from scripts.audit_rule_ir_native_prompts import audit, render_markdown


def test_native_prompt_preflight_passes_without_model_calls() -> None:
    report = audit()
    assert report["status"] == "pass"
    assert report["api_calls"] == 0
    assert not report["errors"]
    assert len(report["prompts"]) == 4
    assert report["schemas"]["registered_unit_enum"] == 36
    assert report["schemas"]["semantic_search_outputs_item_bounds"] == [0, 0]
    assert report["schemas"]["supported_writer_conclusion_field"] is False
    assert render_markdown(report).startswith(
        "# RuleIR-native KCL E2E 사전 프롬프트 감사\n"
    )


def test_leakage_gate_rejects_nested_benchmark_annotations() -> None:
    with pytest.raises(InputLeakageError, match="rubric_summary"):
        assert_no_leaked_fields({"request": {"rubric_summary": ["answer key"]}})
