from __future__ import annotations

import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from idpr.eval.phase3_judge import (
    JudgeContractError,
    aggregate_records,
    evidence_in_answer,
    load_method_answers,
    reduce_judge_output,
)
from idpr.eval.rubric import RubricSet
from scripts.run_phase3_llm_judge import _git_revision


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = json.loads(
    (PROJECT_ROOT / "data/eval/phase3_judge_protocol.json").read_text(encoding="utf-8")
)


def _rubric_set() -> RubricSet:
    return RubricSet(
        sub_question_id="case_1",
        question="甲의 죄책을 논하시오.",
        rubrics=(
            "형법 제347조를 인용하여 사기죄 성립을 결론 내리는지",
            "절도죄 불성립을 결론 내리는지",
        ),
        item_types=("conclusion", "conclusion"),
    )


def _judge_output() -> dict:
    return {
        "rubric_assessments": [
            {
                "index": 1,
                "status": "met",
                "answer_quote": "형법 제347조에 따라 기망과 처분행위가 인정되므로 사기죄가 성립한다.",
                "rationale": "조문과 결론이 있다.",
            },
            {
                "index": 2,
                "status": "met",
                "answer_quote": "답안에 존재하지 않는 절도죄 불성립 문장이다.",
                "rationale": "가짜 근거다.",
            },
        ],
        "claims": [
            {
                "claim_id": 1,
                "answer_quote": "형법 제347조에 따라 기망과 처분행위가 인정되므로 사기죄가 성립한다.",
                "classification": "gold_aligned_correct",
                "rubric_indices": [1],
                "rationale": "gold 결론이다.",
            },
            {
                "claim_id": 2,
                "answer_quote": "절도죄도 성립한다.",
                "classification": "incorrect",
                "rubric_indices": [2],
                "rationale": "gold와 반대다.",
            },
        ],
        "hallucinations": [
            {
                "answer_quote": "절도죄도 성립한다.",
                "kind": "doctrinal_error",
                "severity": "major",
                "explanation": "절도죄 결론이 틀렸다.",
            },
            {
                "answer_quote": "답안에 없는 오류다.",
                "kind": "other",
                "severity": "critical",
                "explanation": "가짜 근거다.",
            },
        ],
        "consistency": {
            "score": 2,
            "violations": [
                {
                    "answer_quotes": [
                        "사기죄가 성립한다.",
                        "종합하면 사기죄는 성립하지 않는다.",
                    ],
                    "explanation": "개별 결론과 종합 결론이 충돌한다.",
                }
            ],
            "rationale": "결론이 충돌한다.",
        },
    }


def test_phase3_schema_is_valid() -> None:
    schema = json.loads(
        (PROJECT_ROOT / "docs/contracts/phase3_llm_judge.schema.json").read_text(
            encoding="utf-8"
        )
    )
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(_judge_output())


def test_judge_revision_uses_pinned_value_without_git(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("IDPR_TESTED_CODE_COMMIT", "pinned-test-revision")
    monkeypatch.setattr("scripts.run_phase3_llm_judge.shutil.which", lambda _: None)
    assert _git_revision() == "pinned-test-revision"


def test_evidence_in_answer_normalizes_markdown_and_spacing() -> None:
    answer = "**사기죄**가 성립한다."
    assert evidence_in_answer("사기죄가 성립한다", answer, minimum=4)
    assert not evidence_in_answer("횡령죄가 성립한다", answer, minimum=4)


def test_reduce_judge_output_applies_all_safeguards() -> None:
    answer = (
        "형법 제347조에 따라 기망과 처분행위가 인정되므로 사기죄가 성립한다. "
        "절도죄도 성립한다. 그러나 종합하면 사기죄는 성립하지 않는다."
    )
    reduced = reduce_judge_output(
        output=_judge_output(),
        answer=answer,
        rubric_set=_rubric_set(),
        protocol=PROTOCOL,
    )
    assert reduced["coverage"]["binary"] == [1, 0]
    assert reduced["coverage"]["rubric_score"] == 0.5
    assert reduced["precision"]["numerator"] == 1
    assert reduced["precision"]["total_claims"] == 2
    assert reduced["precision"]["score"] == 0.5
    assert reduced["hallucination"]["score"] == -2
    assert reduced["hallucination"]["incident_count"] == 1
    assert reduced["consistency"]["score"] == 2
    assert reduced["safeguards"] == {
        "rubric_met_downgrades": 1,
        "dropped_hallucinations": 1,
        "dropped_consistency_violations": 0,
    }


def test_reduce_rejects_claim_quote_absent_from_answer() -> None:
    output = _judge_output()
    output["claims"][0]["answer_quote"] = "실제 답안에는 없는 명제"
    with pytest.raises(JudgeContractError, match="cites text absent"):
        reduce_judge_output(
            output=output,
            answer="사기죄가 성립한다.",
            rubric_set=_rubric_set(),
            protocol=PROTOCOL,
        )


def test_invalid_consistency_evidence_cannot_lower_score() -> None:
    output = _judge_output()
    output["consistency"]["violations"][0]["answer_quotes"] = ["답안에 없는 문장"]
    reduced = reduce_judge_output(
        output=output,
        answer=(
            "형법 제347조에 따라 기망과 처분행위가 인정되므로 사기죄가 성립한다. "
            "절도죄도 성립한다."
        ),
        rubric_set=_rubric_set(),
        protocol=PROTOCOL,
    )
    assert reduced["consistency"]["score"] == 4
    assert reduced["safeguards"]["dropped_consistency_violations"] == 1


def test_load_method_answers_strictly_joins_expected_ids(tmp_path: Path) -> None:
    output = tmp_path / "method.jsonl"
    output.write_text(
        "".join(
            json.dumps(
                {"sub_question_id": case_id, "generated_response": f"answer {case_id}"}
            )
            + "\n"
            for case_id in ("case_1", "case_2", "development_case")
        ),
        encoding="utf-8",
    )
    manifest = tmp_path / "methods.json"
    manifest.write_text(
        json.dumps({"methods": {"method_a": str(output)}}), encoding="utf-8"
    )
    answers, paths = load_method_answers(
        project_root=tmp_path,
        methods_manifest_path=manifest,
        expected_case_ids=("case_1", "case_2"),
    )
    assert list(answers["method_a"]) == ["case_1", "case_2"]
    assert paths["method_a"] == output


def test_aggregate_records_reports_missing_and_micro_precision() -> None:
    def record(case_id: str, *, coverage: float, numerator: int, total: int) -> dict:
        return {
            "status": "ok",
            "method_id": "method_a",
            "sub_question_id": case_id,
            "metrics": {
                "coverage": {"rubric_score": coverage},
                "precision": {
                    "score": numerator / total,
                    "numerator": numerator,
                    "total_claims": total,
                },
                "hallucination": {"score": 0},
                "consistency": {"normalized_score": 1},
            },
        }

    summary = aggregate_records(
        [record("case_1", coverage=0.5, numerator=1, total=2)],
        expected_case_ids=("case_1", "case_2"),
    )["methods"]["method_a"]
    assert summary["completed_cases"] == 1
    assert summary["missing_cases"] == ["case_2"]
    assert summary["coverage_macro"] == 0.5
    assert summary["precision_micro"] == 0.5
