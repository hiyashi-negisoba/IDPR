from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

import pytest

from idpr.rulegen.native_host import DEFAULT_SCLI
from idpr.rulegen.registry import build_registry
from scripts.run_p2_native_scallop_golden import UnitScenarios
from scripts.run_rule_ir_native_lean import ROOT, run_case


CASE_TEXT = "피고인이 피해자에게 행위하였다."


def _assessment(unit_id: str, scenario: dict[str, Any]) -> dict[str, Any]:
    entry = build_registry()[unit_id]
    status_by_card = {
        item["card_id"]: item["status"] for item in scenario["assessments"]
    }
    assessments = {}
    for predicate in entry.commentary_inputs:
        status = status_by_card.get(predicate["norm_card_ids"][0], "unknown")
        assessments[predicate["id"]] = {
            "status": status,
            "source_quotes": [CASE_TEXT] if status != "unknown" else [],
            "missing_facts": ["판단에 필요한 구체적 사실"] if status == "unknown" else [],
        }
    roles = {
        argument["name"]: scenario[argument["name"]]
        for argument in entry.role_predicate["arguments"]
    }
    roles["case_id"] = "case-1"
    return {
        "version": "1.0.0",
        "case_id": "case-1",
        "issue_id": "issue-1",
        "unit_id": unit_id,
        "role_values": roles,
        "distinct_entities": scenario.get("distinct_entities", []),
        "assessments": assessments,
    }


class FakeClient:
    def __init__(self, assessment: dict[str, Any]) -> None:
        self.assessment = assessment
        self.json_calls: list[str] = []
        self.text_calls = 0

    def complete_json(self, **kwargs: Any) -> tuple[dict[str, Any], dict[str, Any]]:
        schema_name = str(kwargs["schema_name"])
        self.json_calls.append(schema_name)
        if schema_name == "rule_ir_native_issue_selection":
            return (
                {
                    "version": "1.0.0",
                    "case_id": "case-1",
                    "issues": [
                        {
                            "issue_id": "issue-1",
                            "unit_id": self.assessment["unit_id"],
                            "reported_label": "검증 대상 죄명",
                            "source_quote": CASE_TEXT,
                            "role_candidates": {
                                key: value
                                for key, value in self.assessment["role_values"].items()
                                if key != "case_id"
                            },
                            "depends_on_issue_ids": [],
                        }
                    ],
                },
                {"usage": {"prompt_tokens": 1, "completion_tokens": 1}},
            )
        return self.assessment, {
            "usage": {"prompt_tokens": 1, "completion_tokens": 1}
        }

    def complete_text(self, **kwargs: Any) -> str:
        self.text_calls += 1
        return "### 법리\n\n법리 설명\n\n### 사안의 적용\n\n사실 적용"


@pytest.mark.skipif(not DEFAULT_SCLI.is_file(), reason="pinned scli is not installed")
def test_lean_runner_reaches_committed_scallop_and_host_answer(tmp_path: Path) -> None:
    unit_id = "rape"
    scenario = UnitScenarios(unit_id).build()[0]
    client = FakeClient(_assessment(unit_id, scenario))
    result = run_case(
        client=client,
        raw_case={
            "sub_question_id": "case-1",
            "question_text": CASE_TEXT,
            "question_prompt": "죄책을 검토하라.",
            "rubric_summary": ["모델에 전달되면 안 되는 정답 정보"],
        },
        out_dir=tmp_path,
    )

    assert client.json_calls == [
        "rule_ir_native_issue_selection",
        "rule_ir_native_predicate_assessment",
    ]
    assert client.text_calls == 1
    assert result["manifest"]["semantic_search_used"] is False
    assert result["manifest"]["fact_graph_used"] is False
    assert result["manifest"]["core_projection_used"] is False
    runtime = result["native_report"]["unit_results"]["issue-1"]
    assert runtime["runtime"] == "scallop_scli_committed_rule_ir"
    assert runtime["symbolic_conclusion"] == "established"
    assert result["answer"]["sections"][0]["conclusion"] == "성립"
    assert (tmp_path / "05_answer.md").is_file()


def test_active_runner_imports_no_retrieval_fact_graph_or_core_runtime() -> None:
    path = ROOT / "scripts/run_rule_ir_native_lean.py"
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imports = {
        node.module
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module
    }
    forbidden = {
        "idpr.neural.fact_graph",
        "idpr.neural.issue_assessment",
        "idpr.rulegen.core_profile",
        "idpr.rulegen.core_runtime",
        "idpr.retrieval",
    }
    assert not (imports & forbidden)
