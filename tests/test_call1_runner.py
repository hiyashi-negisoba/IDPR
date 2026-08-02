from __future__ import annotations

from scripts.run_call1_fact_graphs import restore_previous_graph


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
