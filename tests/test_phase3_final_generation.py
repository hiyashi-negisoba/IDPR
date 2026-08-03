import json

from scripts.build_phase3_final_eval_inventory import DEVELOPMENT_CASES, build_rows
from idpr.eval.issue_recall import INVENTORY_PATH


def test_final_generation_inventory_is_exactly_the_sealed_59_and_rubric_free():
    rows = build_rows(INVENTORY_PATH)
    assert len(rows) == 59
    assert DEVELOPMENT_CASES.isdisjoint({row["sub_question_id"] for row in rows})
    assert all(set(row) == {"sub_question_id", "question_text", "question_prompt"} for row in rows)
    assert "rubric" not in json.dumps(rows, ensure_ascii=False).lower()


def test_final_generation_job_runs_every_pipeline_stage_and_writes_manifest():
    script = (INVENTORY_PATH.parents[2] / "scripts/slurm/run_phase3_final_59.sh").read_text(
        encoding="utf-8"
    )
    for command in (
        "run_call1_fact_graphs.py",
        "run_article_select.py",
        "run_l0_candidates.py",
        "run_issue_pipeline_batch.py",
        "write_phase3_generation_manifest.py",
    ):
        assert command in script
    assert "--top-k-articles 10" in script


def test_final_generation_resume_reuses_the_frozen_submission_wrapper():
    root = INVENTORY_PATH.parents[2]
    submission = (root / "scripts/slurm/run_phase3_final_59.sh").read_text(
        encoding="utf-8"
    )
    resume_body = (root / "scripts/slurm/run_phase3_final_59_resume.sh").read_text(
        encoding="utf-8"
    )
    assert 'IDPR_FINAL59_RESUME:-0' in submission
    assert 'exec /bin/bash "$PROJECT_ROOT/scripts/slurm/run_phase3_final_59_resume.sh"' in submission
    assert "#SBATCH" not in resume_body
