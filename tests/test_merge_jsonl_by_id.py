from __future__ import annotations

import pytest

from scripts.merge_jsonl_by_id import merge_rows


def test_merge_rows_replaces_only_named_rows_and_preserves_order() -> None:
    base = [
        {"sub_question_id": "a", "fact_graph": {"old": 1}},
        {"sub_question_id": "b", "error": "failed"},
        {"sub_question_id": "c", "fact_graph": {"old": 3}},
    ]
    replacement = [{"sub_question_id": "b", "fact_graph": {"new": 2}}]
    merged = merge_rows(
        base,
        replacement,
        id_field="sub_question_id",
        required_fields=("fact_graph",),
        rejected_fields=("error",),
    )
    assert [row["sub_question_id"] for row in merged] == ["a", "b", "c"]
    assert merged[0] == base[0]
    assert merged[1] == replacement[0]
    assert merged[2] == base[2]


def test_merge_rows_rejects_invalid_replacement() -> None:
    with pytest.raises(ValueError, match="field gates"):
        merge_rows(
            [{"sub_question_id": "a", "fact_graph": {}}],
            [{"sub_question_id": "a", "error": "still failed"}],
            id_field="sub_question_id",
            required_fields=("fact_graph",),
            rejected_fields=("error",),
        )
