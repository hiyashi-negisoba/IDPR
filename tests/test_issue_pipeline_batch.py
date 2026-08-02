from __future__ import annotations

from pathlib import Path

import pytest

from scripts.run_issue_pipeline_batch import _index_unique, _selected_case_ids, case_commands
from scripts.refresh_l0_issue_catalog import refreshed_row


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_case_commands_use_persisted_scope_without_article_literals(tmp_path: Path):
    assessment, answer = case_commands(
        python="python",
        base_url="http://127.0.0.1:9000",
        model="model-under-test",
        api_key="key",
        case_id="case-1",
        inventory=Path("inventory.jsonl"),
        fact_graphs=Path("facts.jsonl"),
        candidates=Path("candidates.jsonl"),
        case_dir=tmp_path / "case-1",
        call2_max_tokens=100,
        call3_max_tokens=200,
        timeout_seconds=30,
        no_cache=False,
    )
    assert assessment[1] == "scripts/run_issue_assessment.py"
    assert answer[1] == "scripts/run_issue_answer.py"
    assert "--articles" not in assessment
    assert "art297" not in assessment + answer
    assert assessment[assessment.index("--case-id") + 1] == "case-1"


def test_slurm_runner_resolves_repository_from_submission_directory():
    script = (PROJECT_ROOT / "scripts/slurm/run_issue_pipeline_batch.sh").read_text(
        encoding="utf-8"
    )
    shared = (PROJECT_ROOT / "scripts/slurm/_env.sh").read_text(encoding="utf-8")
    assert "SLURM_SUBMIT_DIR" in script
    assert "SLURM_SUBMIT_DIR" in shared


def test_all_shared_slurm_entrypoints_find_env_outside_the_spool_copy():
    expected = (
        'source "${IDPR_PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}/'
        'scripts/slurm/_env.sh"'
    )
    scripts = [
        path
        for path in (PROJECT_ROOT / "scripts/slurm").rglob("*.sh")
        if path.name != "_env.sh" and "source" in path.read_text(encoding="utf-8")
    ]

    assert scripts
    assert not [
        str(path.relative_to(PROJECT_ROOT))
        for path in scripts
        if expected not in path.read_text(encoding="utf-8")
    ]


def test_batch_inventory_rejects_duplicate_case_ids():
    rows = [{"sub_question_id": "case-1"}, {"sub_question_id": "case-1"}]
    with pytest.raises(ValueError, match="duplicate case"):
        _index_unique(rows, source="fixture")


def test_batch_selection_preserves_inventory_order_and_validates_ids():
    rows = [
        {"sub_question_id": "case-2"},
        {"sub_question_id": "case-1"},
        {"sub_question_id": "case-3"},
    ]
    assert _selected_case_ids(rows, requested=["case-1", "case-2"], limit=None) == [
        "case-2",
        "case-1",
    ]
    with pytest.raises(ValueError, match="unknown --case-id"):
        _selected_case_ids(rows, requested=["missing"], limit=None)


def test_refresh_l0_row_rebuilds_derived_issue_fields_without_changing_articles():
    row = {
        "sub_question_id": "case-1",
        "articles": ["art329", "art342"],
        "from_model": ["art329"],
        "from_retrieval": [],
        "from_attempt_expansion": [],
        "issues": 0,
        "issue_ids": [],
    }
    refreshed = refreshed_row(row)
    assert refreshed["articles"] == ["art329", "art342"]
    assert refreshed["initial_issues"] > 0
    assert refreshed["issue_ids"]
