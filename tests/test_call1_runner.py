from __future__ import annotations

import pytest

from scripts.run_call1_fact_graphs import restore_previous_graph, select_records_for_run


def test_failed_regeneration_can_reuse_a_previous_admitted_graph() -> None:
    failed = {
        "sub_question_id": "case-1",
        "error": "FactGraphError: insufficient grounding",
        "errors": ["only 2 of 5 acts are grounded"],
        "rejected_payload": {"acts": []},
    }
    previous = {
        "sub_question_id": "case-1",
        "fact_graph": {"case_id": "case-1", "acts": []},
        "admission": {"dropped_total": 0},
        "usage": {"total_tokens": 100},
    }

    restored = restore_previous_graph(failed, previous_row=previous)

    assert restored["fact_graph"] == previous["fact_graph"]
    assert restored["fallback"]["kind"] == "previous_valid_fact_graph"
    assert "insufficient grounding" in restored["fallback"]["regeneration_error"]
    assert "error" not in restored


def test_failed_regeneration_stays_failed_without_a_valid_previous_graph() -> None:
    failed = {"sub_question_id": "case-1", "error": "boom"}

    assert restore_previous_graph(failed, previous_row=None) is failed
    assert restore_previous_graph(failed, previous_row={"error": "old"}) is failed


def test_retry_selection_runs_only_failed_prior_rows() -> None:
    records = [
        {"sub_question_id": "a"},
        {"sub_question_id": "b"},
        {"sub_question_id": "c"},
    ]
    retry_rows = [
        {"sub_question_id": "a", "fact_graph": {}},
        {"sub_question_id": "b", "error": "failed"},
        {"sub_question_id": "c", "fact_graph": {}},
    ]
    selected, retry_index = select_records_for_run(
        records, requested_case_ids=[], retry_rows=retry_rows, limit=0
    )
    assert selected == [{"sub_question_id": "b"}]
    assert retry_index["b"]["error"] == "failed"


def test_retry_selection_rejects_ambiguous_scope() -> None:
    with pytest.raises(ValueError, match="mutually exclusive"):
        select_records_for_run(
            [{"sub_question_id": "a"}],
            requested_case_ids=["a"],
            retry_rows=[{"sub_question_id": "a", "error": "failed"}],
            limit=0,
        )
