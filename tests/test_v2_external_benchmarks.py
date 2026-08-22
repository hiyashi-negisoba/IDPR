from __future__ import annotations

from pathlib import Path

import pytest

from idpr.v2.benchmarks.external import evaluate_call1, evaluate_call2
from idpr.v2.benchmarks.external_data import (
    KBL_CAUSATION_REF,
    KBL_EXTERNAL_OFFENSE,
    prepare_kbl_rows,
    prepare_lbox_rows,
    resolve_lbox_statute,
)
from idpr.v2.registry import DefinitionEntry, DefinitionRegistry, load_definitions

ROOT = Path(__file__).resolve().parents[1]


def _offense(ref: str, name: str, statute: str) -> DefinitionEntry:
    return DefinitionEntry(
        id=ref,
        kind="offense",
        payload={
            "id": ref,
            "identity": {"name": name, "statutory_refs": [statute]},
            "elements": {},
        },
        source_file="test",
    )


def _lbox_registry() -> DefinitionRegistry:
    entries = (
        _offense("offense.acquire", "장물취득죄", "형법 제362조 제1항"),
        _offense("offense.custody", "장물보관죄", "형법 제362조 제1항"),
        _offense("offense.theft", "절도죄", "형법 제329조"),
    )
    return DefinitionRegistry(
        by_id={entry.id: entry for entry in entries},
        by_kind={"offense": entries, "derived_offense": ()},
    )


def test_lbox_shared_statute_requires_unique_casename_resolution() -> None:
    registry = _lbox_registry()
    resolved, status = resolve_lbox_statute(
        registry,
        statute="형법   제362조 제1항",
        casename="장물취득",
    )
    assert resolved == "offense.acquire"
    assert status == "resolved_by_casename"

    unresolved, status = resolve_lbox_statute(
        registry,
        statute="형법 제362조 제1항",
        casename="기타",
    )
    assert unresolved is None
    assert status == "ambiguous_statute_mapping"


def test_lbox_materialization_filters_before_model_input_and_hides_gold() -> None:
    registry = _lbox_registry()
    rows = {
        "test": [
            {
                "id": 1,
                "casetype": "criminal",
                "casename": "절도",
                "statutes": ["형법 제329조"],
                "facts": "피고인은 타인의 물건을 가져갔다.",
            },
            {
                "id": 2,
                "casetype": "criminal",
                "casename": "기타",
                "statutes": ["형법 제362조 제1항"],
                "facts": "사실관계",
            },
        ]
    }
    prepared = prepare_lbox_rows(registry, rows)
    assert prepared["summary"]["source_N"] == 2
    assert prepared["summary"]["fully_covered_N"] == 1
    assert prepared["summary"]["excluded_N"] == 1
    assert prepared["gold_rows"][0]["gold_definition_refs"] == ["offense.theft"]
    payload = prepared["model_inputs"][0]["payload"]
    assert "casename" not in payload
    assert "statutes" not in payload
    assert set(payload) == {"question_prompt", "case_text", "offense_catalog"}


def _kbl_row(doc_id: int, *, label: str, a: str, b: str) -> dict[str, object]:
    return {
        "doc-id": doc_id,
        "question": "질문",
        "facts_charged": "피고인의 행위로 피해자가 사망하였다고 기소되었다.",
        "defendant_claim": "피고인은 인과관계를 다툰다.",
        "facts_accepted": "법원이 채택한 사실과 증거가 제시되어 있다.",
        "cause": "피고인의 행위",
        "effect": "피해자의 사망",
        "label": label,
        "A": a,
        "B": b,
        "meta": {"raw-data-doc-ids": "사건"},
    }


def test_kbl_label_is_derived_from_option_semantics_not_letter_position() -> None:
    registry = load_definitions(ROOT / "data/v2/definitions")
    prepared = prepare_kbl_rows(
        registry,
        (
            _kbl_row(1, label="B", a="인과관계없음", b="인과관계있음"),
            _kbl_row(2, label="B", a="인과관계있음", b="인과관계없음"),
        ),
    )
    assert prepared["summary"]["fully_covered_N"] == 2
    assert [row["label"] for row in prepared["gold_rows"]] == ["TRUE", "FALSE"]
    model_input = prepared["model_inputs"][0]
    assert model_input["target"]["predicate_ref"] == KBL_CAUSATION_REF
    assert model_input["target"]["instance_key"]["offense_ref"] == KBL_EXTERNAL_OFFENSE
    assert "label" not in model_input["payload"]
    assert "[판단대상 원인]" in model_input["payload"]["evidence_occurrence"]["source_text"]


def test_call1_scores_raw_and_closure_recovery_separately() -> None:
    gold = [
        {"id": "a", "gold_definition_refs": ["offense.a"]},
        {"id": "b", "gold_definition_refs": ["offense.b"]},
    ]
    predictions = [
        {
            "id": "a",
            "seeds": ["offense.a"],
            "candidate_offense_refs": ["offense.a"],
        },
        {
            "id": "b",
            "seeds": ["offense.base"],
            "candidate_offense_refs": ["offense.base", "offense.b"],
        },
    ]
    result = evaluate_call1(gold, predictions)["summary"]
    assert result["raw_successes"] == 1
    assert result["closure_successes"] == 2
    assert result["closure_recoveries"] == 1
    assert result["raw_survival_rate"] == 0.5
    assert result["closure_survival_rate"] == 1.0


def test_call2_reports_three_way_unknown_and_selective_metrics() -> None:
    gold = [
        {"id": "a", "label": "TRUE"},
        {"id": "b", "label": "FALSE"},
    ]
    predictions = [
        {"id": "a", "label": "TRUE"},
        {"id": "b", "label": "UNKNOWN"},
    ]
    result = evaluate_call2(gold, predictions)["summary"]
    assert result["accuracy"] == 0.5
    assert result["coverage"] == 0.5
    assert result["selective_accuracy"] == 1.0
    assert result["unknown_rate"] == 0.5
    assert result["confusion_matrix"]["FALSE"]["UNKNOWN"] == 1


def test_kbl_primary_macro_f1_uses_observed_gold_labels() -> None:
    gold = [
        {"id": "a", "label": "TRUE"},
        {"id": "b", "label": "FALSE"},
    ]
    predictions = [
        {"id": "a", "label": "TRUE"},
        {"id": "b", "label": "FALSE"},
    ]
    result = evaluate_call2(gold, predictions)["summary"]
    assert result["macro_f1_observed_gold"] == 1.0
    assert result["macro_f1_fixed_3way"] == pytest.approx(2 / 3)


def test_external_scorers_require_exact_id_alignment() -> None:
    with pytest.raises(ValueError, match="id mismatch"):
        evaluate_call2(
            [{"id": "gold", "label": "TRUE"}],
            [{"id": "pred", "label": "TRUE"}],
        )
