from __future__ import annotations

import ast
import copy
import json
from pathlib import Path
from typing import Any

import pytest

from idpr.rulegen.native_host import DEFAULT_SCLI
from idpr.rulegen.registry import build_registry
from scripts.run_p2_native_scallop_golden import UnitScenarios
from scripts.run_rule_ir_native_lean import ROOT, run_case


CASE_TEXT = "피고인이 피해자에게 행위하였다."

# The five routing-extension arrays are unconditionally required by the
# schema (docs/handoff/CURRENT.md "라우팅 출력 확장"); these fakes have
# nothing to declare.
_EMPTY_ROUTING_EXTENSIONS: dict[str, Any] = {
    "required_subissues": [],
    "conclusion_sensitive_facts": [],
    "unresolved_branch_points": [],
    "alternative_legal_routes": [],
    "required_issue_labels": [],
}

# Golden scenarios speak the legacy 3-state Scallop vocabulary; the live
# predicate_assessment schema speaks the 4-state evidentiary-basis grammar
# (see native_host.ASSESSMENT_STATUSES). Translated here, at the test boundary.
_LEGACY_TO_ASSESSMENT_STATUS = {
    "satisfied": "explicitly_supported",
    "not_satisfied": "contradicted",
    "unknown": "genuinely_unresolved",
}


def _assessment(unit_id: str, scenario: dict[str, Any]) -> dict[str, Any]:
    entry = build_registry()[unit_id]
    status_by_card = {
        item["card_id"]: item["status"] for item in scenario["assessments"]
    }
    assessments = {}
    for predicate in entry.commentary_inputs:
        legacy_status = status_by_card.get(predicate["norm_card_ids"][0], "unknown")
        status = _LEGACY_TO_ASSESSMENT_STATUS[legacy_status]
        assessments[predicate["id"]] = {
            "status": status,
            "source_quotes": [CASE_TEXT] if legacy_status != "unknown" else [],
            "missing_facts": ["판단에 필요한 구체적 사실"] if legacy_status == "unknown" else [],
            "inference_rationale": "",
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
                            "closest_allowed_unit_ids": [],
                            "unsupported_reason": "",
                        }
                    ],
                    **_EMPTY_ROUTING_EXTENSIONS,
                },
                {"usage": {"prompt_tokens": 1, "completion_tokens": 1}},
            )
        return self.assessment, {
            "usage": {"prompt_tokens": 1, "completion_tokens": 1}
        }

    def complete_text(self, **kwargs: Any) -> str:
        self.text_calls += 1
        return (
            "### 법리\n\n법리 설명\n\n### 사안의 적용\n\n사실 적용"
            "\n\n<!--VERDICT_MANIFEST\nissue-1: established\n-->"
        )


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
    assert runtime["proof_dag"], "proof lineage must reach the native report"
    assert (tmp_path / "05_answer.md").is_file()

    # The writer receives a Korean brief, never the engine's own vocabulary.
    write_prompt = (tmp_path / "04_write_prompt.md").read_text(encoding="utf-8")
    assert "확정 결론: 성립 (구성요건 충족)" in write_prompt
    assert "Scallop" not in write_prompt
    assert "symbolic_conclusion" not in write_prompt

    # The writer's machine trailer is stripped before the graded answer is
    # written, and a verdict matching the verified directive is not a
    # contradiction.
    answer = (tmp_path / "05_answer.md").read_text(encoding="utf-8")
    assert "VERDICT_MANIFEST" not in answer
    assert result["verdict_contradictions"] == []
    assert not (tmp_path / "06_verdict_consistency.json").exists()


class TwoIssueFakeClient:
    """Selects two issues of the same unit, one good assessment and one bad."""

    def __init__(self, good: dict[str, Any], bad: dict[str, Any]) -> None:
        self.good = good
        self.bad = bad
        self.json_calls: list[str] = []

    def _issue_entry(self, issue_id: str, assessment: dict[str, Any]) -> dict[str, Any]:
        return {
            "issue_id": issue_id,
            "unit_id": assessment["unit_id"],
            "reported_label": f"쟁점 {issue_id}",
            "source_quote": CASE_TEXT,
            "role_candidates": {
                key: value
                for key, value in assessment["role_values"].items()
                if key != "case_id"
            },
            "depends_on_issue_ids": [],
            "closest_allowed_unit_ids": [],
            "unsupported_reason": "",
        }

    def complete_json(self, **kwargs: Any) -> tuple[dict[str, Any], dict[str, Any]]:
        schema_name = str(kwargs["schema_name"])
        self.json_calls.append(schema_name)
        usage = {"usage": {"prompt_tokens": 1, "completion_tokens": 1}}
        if schema_name == "rule_ir_native_issue_selection":
            return (
                {
                    "version": "1.0.0",
                    "case_id": "case-1",
                    "issues": [
                        self._issue_entry("issue-1", self.good),
                        self._issue_entry("issue-2", self.bad),
                    ],
                    **_EMPTY_ROUTING_EXTENSIONS,
                },
                usage,
            )
        issue_id = kwargs["payload"]["issue"]["issue_id"]
        assessment = self.good if issue_id == "issue-1" else self.bad
        return assessment, usage

    def complete_text(self, **kwargs: Any) -> str:
        return (
            "### 법리\n\n법리 설명\n\n### 사안의 적용\n\n사실 적용"
            "\n\n<!--VERDICT_MANIFEST\nissue-1: established\n-->"
        )


@pytest.mark.skipif(not DEFAULT_SCLI.is_file(), reason="pinned scli is not installed")
def test_lean_runner_degrades_single_bad_predicate_assessment_not_whole_case(
    tmp_path: Path,
) -> None:
    """One issue's contract-violating assessment must not discard the case.

    219740 lost cases like this: a single predicate assessment declaring
    ``contradicted`` with no source quote raised out of the per-issue loop
    and killed every other issue the case had selected, including well-formed
    ones. The fix demotes only the offending issue, the same way a bad issue
    *selection* was already demoted.
    """

    unit_id = "rape"
    scenario = UnitScenarios(unit_id).build()[0]
    good = _assessment(unit_id, scenario)
    good["issue_id"] = "issue-1"
    bad = copy.deepcopy(good)
    bad["issue_id"] = "issue-2"
    predicate_id = next(iter(bad["assessments"]))
    bad["assessments"][predicate_id] = {
        "status": "contradicted",
        "source_quotes": [],
        "missing_facts": [],
    }

    client = TwoIssueFakeClient(good, bad)
    result = run_case(
        client=client,
        raw_case={
            "sub_question_id": "case-1",
            "question_text": CASE_TEXT,
            "question_prompt": "죄책을 검토하라.",
        },
        out_dir=tmp_path,
    )

    unit_results = result["native_report"]["unit_results"]
    assert unit_results["issue-1"]["symbolic_conclusion"] == "established"
    assert "issue-2" not in unit_results

    rejected = json.loads(
        (tmp_path / "01_rejected_issues.json").read_text(encoding="utf-8")
    )["rejected"]
    assert [item["issue_id"] for item in rejected] == ["issue-2"]
    assert rejected[0]["degraded_reason"] == ["predicate_assessment_invalid"]
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
