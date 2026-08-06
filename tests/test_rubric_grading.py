from __future__ import annotations

import json
from pathlib import Path

import pytest

from idpr.eval.rubric import (
    DeferredJudge,
    RubricSet,
    Verdict,
    apply_safeguards,
    classify_rubric_item,
    load_rubric_sets,
    normalize_case_no,
    parse_free_text_verdicts,
    quote_in_answer,
    resolve_rubric_set,
    score_answer,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INVENTORY = PROJECT_ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl"


def _parquet_available() -> bool:
    if not INVENTORY.exists():
        return False
    first = json.loads(INVENTORY.read_text(encoding="utf-8").splitlines()[0])
    return Path(first["source"]["parquet_path"]).exists()


# --------------------------------------------------------------------------- #
# Loading (needs source parquet).
# --------------------------------------------------------------------------- #
@pytest.mark.skipif(not _parquet_available(), reason="source KCL parquet unavailable")
def test_load_rubric_sets_joins_full_rubric():
    sets = load_rubric_sets(INVENTORY)
    assert len(sets) == 61
    rs = sets["kcl_criminal_r14_p1_q2"]
    assert len(rs) == 30  # inventory rubric_count for row 154
    assert len(rs.item_types) == len(rs.rubrics)
    assert rs.score is not None
    assert all(t in {"issue", "rule", "application", "conclusion", "other"} for t in rs.item_types)


@pytest.mark.skipif(not _parquet_available(), reason="source KCL parquet unavailable")
def test_resolve_rubric_set_from_matrix_case():
    sets = load_rubric_sets(INVENTORY)
    case = {"source_sub_question_id": "kcl_criminal_r14_p1_q2"}
    rs = resolve_rubric_set(case, sets)
    assert rs is not None and rs.sub_question_id == "kcl_criminal_r14_p1_q2"
    assert resolve_rubric_set({"source_sub_question_id": "nope"}, sets) is None


# --------------------------------------------------------------------------- #
# Item typing.
# --------------------------------------------------------------------------- #
def test_classify_rubric_item():
    assert classify_rubric_item("쟁점 강제추행죄의 간접정범의 성부를 논하는지") == "issue"
    assert classify_rubric_item(
        "강제추행죄의 폭행은 항거를 곤란하게 할 정도면 족함을 판례를 인용하여 설명하는지"
    ) == "rule"
    assert classify_rubric_item("甲의 협박이 강제추행죄의 협박에 해당한다고 사안에서 적용하는지") == "application"
    assert classify_rubric_item("따라서 주거침입강간치상죄가 성립한다") == "conclusion"


# --------------------------------------------------------------------------- #
# Case-number normalization (gold precedents).
# --------------------------------------------------------------------------- #
def test_normalize_case_no():
    assert normalize_case_no("[대법원 2006도5979]") == "2006도5979"
    assert normalize_case_no("대법원 2015도1234(전합)") == "2015도1234"


# --------------------------------------------------------------------------- #
# Verdict safeguards.
# --------------------------------------------------------------------------- #
def test_quote_in_answer():
    answer = "甲은 A를 기망하여 재물을 편취하였다. 따라서 사기죄가 성립한다."
    norm = "".join(ch for ch in answer if ch.isalnum())
    assert quote_in_answer("甲은 A를 기망하여 재물을 편취하였다", norm)
    assert not quote_in_answer("존재하지 않는 완전히 다른 문장이다", norm)
    assert not quote_in_answer("짧다", norm)  # below min_chars


def test_apply_safeguards_hallucinated_o_downgraded():
    rubrics = ["기망행위를 논하는지", "편취 고의를 논하는지"]
    answer = "甲은 A를 기망하여 재물을 편취하였다."
    verdicts = [
        Verdict(1, "O", "甲은 A를 기망하여 재물을 편취하였다."),  # real quote -> 1
        Verdict(2, "O", "답안에 없는 지어낸 근거 문장이다."),  # fake quote -> 0
    ]
    assert apply_safeguards(verdicts, answer=answer, rubrics=rubrics) == [1, 0]


def test_apply_safeguards_article_gate():
    # rubric demands citing 제347조 specifically; answer never cites it -> O voided.
    rubrics = ["사기죄의 제347조를 명시하여 적시하는지"]
    answer_no_art = "甲은 A를 기망하여 재물을 편취하였으므로 사기죄가 성립한다."
    v = [Verdict(1, "O", "甲은 A를 기망하여 재물을 편취하였으므로 사기죄가 성립한다.")]
    assert apply_safeguards(v, answer=answer_no_art, rubrics=rubrics) == [0]
    answer_with_art = "형법 제347조에 따라 甲은 A를 기망하여 재물을 편취하였으므로 사기죄가 성립한다."
    v2 = [Verdict(1, "O", "형법 제347조에 따라 甲은 A를 기망하여 재물을 편취하였으므로 사기죄가 성립한다.")]
    assert apply_safeguards(v2, answer=answer_with_art, rubrics=rubrics) == [1]


def test_apply_safeguards_missing_verdict_defaults_zero():
    rubrics = ["a를 논하는지", "b를 논하는지", "c를 논하는지"]
    answer = "무관한 답안."
    assert apply_safeguards([], answer=answer, rubrics=rubrics) == [0, 0, 0]


def test_apply_safeguards_partial_credit_weight_and_hallucination_downgrade():
    rubrics = ["기망행위를 논하는지", "편취 고의를 논하는지"]
    answer = "甲은 A를 기망하여 재물을 편취하였다."
    verdicts = [
        Verdict(1, "P", "甲은 A를 기망하여 재물을 편취하였다."),  # real quote -> 0.5
        Verdict(2, "P", "답안에 없는 지어낸 근거 문장이다."),  # fake quote -> 0
    ]
    assert apply_safeguards(verdicts, answer=answer, rubrics=rubrics) == [0.5, 0]


def test_apply_safeguards_partial_credit_article_gate():
    rubrics = ["사기죄의 제347조를 명시하여 적시하는지"]
    answer_no_art = "甲은 A를 기망하여 재물을 편취하였으므로 사기죄가 성립한다."
    v = [Verdict(1, "P", "甲은 A를 기망하여 재물을 편취하였으므로 사기죄가 성립한다.")]
    assert apply_safeguards(v, answer=answer_no_art, rubrics=rubrics) == [0]


def test_parse_free_text_verdicts():
    out = "1 | O | 근거: 어떤 문장\n2 | X | 근거: 없음\n3 | o | 다른 문장"
    parsed = parse_free_text_verdicts(out)
    assert [(v.index, v.verdict) for v in parsed] == [(1, "O"), (2, "X"), (3, "O")]


# --------------------------------------------------------------------------- #
# Scoring.
# --------------------------------------------------------------------------- #
def test_score_answer_recall_by_type():
    binary = [1, 0, 1, 1]
    types = ["issue", "issue", "rule", "conclusion"]
    out = score_answer(binary, types)
    assert out["satisfied"] == 3
    assert out["total"] == 4
    assert out["rubric_score"] == 0.75
    assert out["issue_spotting_recall"] == 0.5  # 1 of 2 issue items
    assert out["recall_by_type"]["rule"] == 1.0
    assert out["recall_by_type"]["conclusion"] == 1.0


def test_score_answer_empty_rubric():
    out = score_answer([], [])
    assert out["total"] == 0 and out["rubric_score"] is None


def test_score_answer_partial_credit_weights_recall():
    binary = [1, 0.5, 1, 0.5]
    types = ["issue", "issue", "rule", "conclusion"]
    out = score_answer(binary, types)
    assert out["satisfied"] == 3.0
    assert out["rubric_score"] == 0.75
    assert out["issue_spotting_recall"] == 0.75  # (1 + 0.5) of 2 issue items
    assert out["recall_by_type"]["conclusion"] == 0.5


# --------------------------------------------------------------------------- #
# Deferred judge refuses to run.
# --------------------------------------------------------------------------- #
def test_deferred_judge_refuses():
    with pytest.raises(NotImplementedError):
        DeferredJudge().score_rubrics("q", "a", ["r"])
