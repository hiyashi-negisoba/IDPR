from __future__ import annotations

import json
from pathlib import Path

import pytest

from idpr.rulegen import compile_rule_ir, validate_full_rule_ir_generation
from idpr.rulegen.scallop_runtime import (
    ScallopFactValidationError,
    sha256_file,
    validate_scenario,
)
from scripts.build_fraud_full_scallop import (
    APPROVAL_PATH,
    COMMENTARY_PATH,
    MANIFEST_PATH,
    NORM_CARD_PATH,
    OUTPUT_PATH,
    PROJECT_ROOT,
    RULE_IR_PATH,
    build,
    read_json,
    read_jsonl,
)
from scripts.run_fraud_scallop_golden import (
    DEFAULT_SCLI,
    GOLDEN_PATH,
    HUMAN_REPORT_PATH,
    expand_scenarios,
    run_all,
)


def _rule_ir_inputs() -> tuple[dict, dict, dict[str, dict]]:
    rule_ir = read_json(RULE_IR_PATH)
    norm_cards = read_json(NORM_CARD_PATH)
    allowed = set(rule_ir["source_scope"]["comment_ids"])
    commentary = {
        row["comment_id"]: row
        for row in read_jsonl(COMMENTARY_PATH)
        if row["comment_id"] in allowed
    }
    return rule_ir, norm_cards, commentary


def test_approved_full_rule_ir_compiles_deterministically() -> None:
    manifest = build()
    rule_ir, norm_cards, commentary = _rule_ir_inputs()

    validate_full_rule_ir_generation(rule_ir, commentary, norm_cards)
    assert OUTPUT_PATH.read_text(encoding="utf-8") == compile_rule_ir(
        rule_ir, commentary, norm_cards
    )
    assert manifest["status"] == "compiled"
    assert manifest["model_output_executed_directly"] is False
    assert manifest["counts"] == {
        "norm_cards": 88,
        "predicates": 201,
        "rules": 342,
    }
    assert manifest["output"]["sha256"] == sha256_file(OUTPUT_PATH)
    approval_key = str(APPROVAL_PATH.relative_to(PROJECT_ROOT))
    assert manifest["inputs"][approval_key] == sha256_file(APPROVAL_PATH)


def test_completion_gate_rejects_missing_selected_assessment() -> None:
    rule_ir = read_json(RULE_IR_PATH)
    fixture = read_json(GOLDEN_PATH)
    scenario = expand_scenarios(fixture)[0]
    scenario["selected_card_ids"].append("fraud_mistake.triangular_fraud_definition")

    with pytest.raises(
        ScallopFactValidationError, match="case_assessment_complete is forbidden"
    ):
        validate_scenario(rule_ir, scenario)


def test_distinct_entity_rejects_reflexive_pair_before_scallop() -> None:
    rule_ir = read_json(RULE_IR_PATH)
    fixture = read_json(GOLDEN_PATH)
    scenario = expand_scenarios(fixture)[0]
    scenario["distinct_entities"] = [["victim", "victim"]]

    with pytest.raises(ScallopFactValidationError, match="is reflexive"):
        validate_scenario(rule_ir, scenario)


def test_scallop_runtime_executes_all_golden_paths(tmp_path: Path) -> None:
    if not DEFAULT_SCLI.is_file():
        pytest.skip("install the pinned runtime with scripts/install_scallop_runtime.sh")

    report = run_all(
        work_dir=tmp_path / "programs",
        report_path=tmp_path / "report.json",
        human_report_path=tmp_path / "human_report.md",
    )

    assert report["status"] == "pass"
    assert report["scenario_count"] == 9
    assert not report["failures"]
    assert all(scenario["status"] == "pass" for scenario in report["scenarios"])
    assert (tmp_path / "human_report.md").is_file()


def test_tracked_runtime_report_matches_golden_fixture() -> None:
    report_path = GOLDEN_PATH.with_name("fraud_scallop_runtime_report.json")
    report = json.loads(report_path.read_text(encoding="utf-8"))
    fixture = read_json(GOLDEN_PATH)

    assert report["status"] == "pass"
    assert report["scenario_count"] == len(fixture["scenarios"])
    assert report["compiled_sha256"] == sha256_file(OUTPUT_PATH)
    assert json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))["status"] == "compiled"


def test_human_runtime_report_explains_inputs_and_limitations() -> None:
    report = HUMAN_REPORT_PATH.read_text(encoding="utf-8")

    assert "이 문서는 사람이 검토하는 보고서" in report
    assert "이번 입력은 자연어 사실관계가 아니다" in report
    assert "기본 판단 14개" in report
    assert "일반형 사기 성립" in report
    assert "삼각사기 성립" in report
    assert "제3자 취득형 사기 성립" in report
    assert "이 시험이 아직 증명하지 않은 것" in report
