from __future__ import annotations

from scripts.build_p2_approved_decisions_from_proposals import table_rows


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
