from __future__ import annotations

import pytest

from idpr.eval.input_formatter import InputLeakageError, assert_no_leaked_fields
from scripts.audit_rule_ir_native_prompts import audit, render_markdown


def test_native_prompt_preflight_passes_without_model_calls() -> None:
    report = audit()
    assert report["status"] == "pass"
    assert report["api_calls"] == 0
    assert not report["errors"]
    assert len(report["prompts"]) == 3
    assert report["schemas"]["registered_unit_enum"] == 36
    assert report["schemas"]["writer_format"] == "one_plain_markdown_section"
    assert report["schemas"]["writer_conclusion_field"] is False
    assert render_markdown(report).startswith(
        "# Lean RuleIR-native KCL 프롬프트 감사\n"
    )


def test_leakage_gate_rejects_nested_benchmark_annotations() -> None:
    with pytest.raises(InputLeakageError, match="rubric_summary"):
        assert_no_leaked_fields({"request": {"rubric_summary": ["answer key"]}})
