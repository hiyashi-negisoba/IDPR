#!/bin/bash
#SBATCH --job-name=phase3_final_e2e
#SBATCH --output=logs/phase3_final_e2e_%j.out
#SBATCH --error=logs/phase3_final_e2e_%j.err
#SBATCH --time=06:00:00
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:PRO6000:1
#SBATCH --mem=32G

set -euo pipefail
source "${IDPR_PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}/scripts/slurm/_env.sh"
export IDPR_FREEZE_ROOT="${IDPR_FINAL_E2E_ROOT:-$PROJECT_ROOT/experiments/results/phase3_final_design_e2e}"
export IDPR_TOP_K_ARTICLES=10

cd "$PROJECT_ROOT"
bash scripts/slurm/run_phase3_e2e_smoke.sh
"$CLIENT_PYTHON" scripts/verify_phase3_final_design_e2e.py \
    --run-root "$IDPR_FREEZE_ROOT" \
    --previous-root "$PROJECT_ROOT/experiments/results/phase3_answer_visibility_e2e_v2" \
    --out "$IDPR_FREEZE_ROOT/final_design_comparison.json"
