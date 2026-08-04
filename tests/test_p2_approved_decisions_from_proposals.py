from __future__ import annotations

import pytest

from scripts.build_p2_approved_decisions_from_proposals import grouped_decisions, table_rows


def test_markdown_code_ticks_are_not_part_of_a_referenced_unit_id(tmp_path) -> None:
    proposal = tmp_path / "proposal.md"
    proposal.write_text(
        "| # | card | decision | role | component / join | track | refers_to | reason |\n"
        "|---:|---|---|---|---|---|---|---|\n"
        "| 1 | `card.one` | approve | post_outcome | concurrence / not_applicable | "
        "base | `traffic_special_act` | approved reason |\n",
        encoding="utf-8",
    )

    row = table_rows([proposal])[1]

    assert row["refers_to_unit"] == "traffic_special_act"


def test_compact_decision_groups_expand_without_review_markdown() -> None:
    rows = grouped_decisions({"decision_groups": [{
        "card_numbers": [1, 3],
        "decision": "approve",
        "role": "component",
        "component_id": "conduct",
        "component_join": "alternative_any",
        "track_id": "base",
        "refers_to_unit": None,
        "rationale": "delegated legal normalization",
    }]})

    assert sorted(rows) == [1, 3]
    assert rows[1] == rows[3]
    assert rows[1] is not rows[3]


def test_compact_decision_groups_reject_duplicate_card_numbers() -> None:
    with pytest.raises(ValueError, match="duplicate grouped decision"):
        grouped_decisions({"decision_groups": [
            {"card_numbers": [1], "decision": "approve"},
            {"card_numbers": [1], "decision": "context_only"},
        ]})
