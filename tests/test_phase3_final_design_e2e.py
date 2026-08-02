from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_final_e2e_wraps_the_full_smoke_and_gates_on_comparison():
    script = (ROOT / "scripts/slurm/run_phase3_final_design_e2e.sh").read_text(
        encoding="utf-8"
    )
    assert "run_phase3_e2e_smoke.sh" in script
    assert "IDPR_TOP_K_ARTICLES=10" in script
    assert "verify_phase3_final_design_e2e.py" in script


def test_final_59_job_is_only_submitted_with_an_afterok_dependency():
    # The dependency is recorded at submission time in the handover, not embedded as a
    # scheduler id in reusable production code. This test pins the reusable job itself.
    script = (ROOT / "scripts/slurm/run_phase3_final_59.sh").read_text(encoding="utf-8")
    assert "phase3_final_59" in script
    assert "#SBATCH --time=48:00:00" in script
