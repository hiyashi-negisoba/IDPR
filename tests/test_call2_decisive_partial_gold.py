from __future__ import annotations

import json
from pathlib import Path

from idpr.v2.registry import load_definitions

ROOT = Path(__file__).resolve().parents[1]


def test_forgery_authority_standard_separates_authenticity_from_false_content() -> None:
    registry = load_definitions(ROOT / "data/v2/definitions")
    entry = registry.get("legal_element.forgery_without_authority")
    assert entry is not None
    standard = entry.payload["legal_standard"]
    assert "명의자가 직접 작성" in standard
    assert "내용의 허위만으로는 명의모용이 되지 않는다" in standard


def test_partial_gold_is_sparse_reviewed_and_evidence_backed() -> None:
    path = ROOT / "data/eval/v2_call2_decisive_predicate_partial_gold.jsonl"
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]
    assert rows
    assert len({row["annotation_id"] for row in rows}) == len(rows)
    assert {row["review_status"] for row in rows} == {"reviewed_explicit"}
    assert all(row["evidence_text"] and row["rubric_support"] and row["rationale"] for row in rows)
    assert {row["evidence_carrier"] for row in rows} <= {
        "LOCAL_OCCURRENCE",
        "QUESTION_ASSUMPTION",
        "MULTI_OCCURRENCE_RELATION",
    }
    assert {row["expected_truth"] for row in rows} <= {"TRUE", "FALSE", "UNKNOWN"}


def test_local_partial_gold_evidence_is_in_the_actual_occurrence_carrier() -> None:
    annotations = [
        json.loads(line)
        for line in (
            ROOT / "data/eval/v2_call2_decisive_predicate_partial_gold.jsonl"
        ).read_text(encoding="utf-8").splitlines()
        if line
    ]
    gold = {
        row["sub_question_id"]: row
        for row in (
            json.loads(line)
            for line in (ROOT / "data/v2/gold_occurrences.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
            if line
        )
    }
    for annotation in annotations:
        if annotation["evidence_carrier"] != "LOCAL_OCCURRENCE":
            continue
        instance = annotation["instance_key"]
        occurrence = next(
            value
            for value in gold[annotation["sub_question_id"]]["occurrences"]
            if value["occurrence_id"] == instance["occurrence_id"]
        )
        assert annotation["evidence_text"] in occurrence["source_text"], annotation[
            "annotation_id"
        ]


def test_question_assumption_partial_gold_uses_the_typed_carrier_exactly() -> None:
    annotations = [
        json.loads(line)
        for line in (
            ROOT / "data/eval/v2_call2_decisive_predicate_partial_gold.jsonl"
        ).read_text(encoding="utf-8").splitlines()
        if line
    ]
    assumptions = {
        row["sub_question_id"]: {
            value["source_text"] for value in row["assumptions"]
        }
        for row in (
            json.loads(line)
            for line in (ROOT / "data/v2/question_assumptions.jsonl")
            .read_text(encoding="utf-8")
            .splitlines()
            if line
        )
    }
    for annotation in annotations:
        if annotation["evidence_carrier"] == "QUESTION_ASSUMPTION":
            assert annotation["evidence_text"] in assumptions[annotation["sub_question_id"]]
