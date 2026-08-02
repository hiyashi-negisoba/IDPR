from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INVENTORY = PROJECT_ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl"
REVIEW = PROJECT_ROOT / "data/inventory/kcl_criminal_v1_review.md"
TAG_COUNTS = PROJECT_ROOT / "data/inventory/kcl_criminal_v1_tag_counts.md"


def test_kcl_criminal_inventory_review_artifacts_exist() -> None:
    assert INVENTORY.exists()
    assert REVIEW.exists()


def test_kcl_criminal_inventory_has_all_criminal_essay_subquestions() -> None:
    rows = [json.loads(line) for line in INVENTORY.read_text(encoding="utf-8").splitlines()]

    assert len(rows) == 61
    assert len({row["sub_question_id"] for row in rows}) == 61
    assert all(row["subject"] == "형사법" for row in rows)
    assert all(row["review_status"] == "reviewed" for row in rows)
    assert all(row["coverage_review_status"] == "needs_review" for row in rows)
    assert all(row["question_text"] for row in rows)
    assert all(row["question_prompt"] for row in rows)
    assert all(row["issue_tags"] for row in rows)
    assert not any("unknown_issue" in row["issue_tags"] for row in rows)


def test_inventory_prompt_preserves_a_separate_fact_scope_qualifier() -> None:
    rows = {
        row["sub_question_id"]: row
        for row in (
            json.loads(line) for line in INVENTORY.read_text(encoding="utf-8").splitlines()
        )
    }

    assert rows["kcl_criminal_r10_p1_q1_ga"]["question_prompt"] == (
        "사실관계 (1)과 관련하여, 甲의 죄책을 논하시오."
    )
    assert rows["kcl_criminal_r10_p1_q3_ga"]["question_prompt"] == (
        "사실관계 (3)과 관련하여, 甲, 丙, 丁의 죄책을 논하시오."
    )


def test_kcl_criminal_inventory_marks_bootstrap_candidates_without_claiming_coverage() -> None:
    rows = [json.loads(line) for line in INVENTORY.read_text(encoding="utf-8").splitlines()]

    assert not any(row["covered"] for row in rows)
    assert any("fraud" in row["issue_tags"] for row in rows)
    assert any(row["coverage_candidate"] == "procedure_gating_candidate" for row in rows)
    assert any(row["coverage_candidate"] == "property_crime_candidate" for row in rows)


def test_kcl_criminal_inventory_review_shows_coverage_for_every_row() -> None:
    review = REVIEW.read_text(encoding="utf-8")

    assert "| content review | coverage review | covered |" in review
    assert review.count("| false |") == 61
    assert review.count("| reviewed | needs_review | false |") == 61


def test_kcl_criminal_inventory_reports_unique_tag_counts() -> None:
    report = TAG_COUNTS.read_text(encoding="utf-8")

    assert "- Unique tags: 165" in report
    assert "- Total tag assignments: 207" in report
    assert "| `joint_principal` | 4 | yes |" in report
