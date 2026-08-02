#!/bin/bash
#SBATCH --job-name=phase3_element_l0
#SBATCH --output=logs/phase3_element_l0_%j.out
#SBATCH --error=logs/phase3_element_l0_%j.err
#SBATCH --time=02:00:00
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:PRO6000:1
#SBATCH --mem=32G

set -euo pipefail
source "${IDPR_PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}/scripts/slurm/_env.sh"

FREEZE_ROOT="${IDPR_FREEZE_ROOT:-$PROJECT_ROOT/experiments/results/phase3_e2e_freeze_v1}"
RUN_ROOT="${IDPR_ELEMENT_L0_ROOT:-$PROJECT_ROOT/experiments/results/phase3_element_l0_${SLURM_JOB_ID}}"
TOP_K_ARTICLES="${IDPR_TOP_K_ARTICLES:-18}"
RETRIEVAL_ADMISSION="${IDPR_RETRIEVAL_ADMISSION:-elements}"
export PYTHONPATH="$PROJECT_ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
unset HF_HUB_OFFLINE TRANSFORMERS_OFFLINE

cd "$PROJECT_ROOT"
mkdir -p logs "$RUN_ROOT"
"$CLIENT_PYTHON" scripts/run_l0_candidates.py \
    --inventory "$PROJECT_ROOT/data/smoke/phase3_e2e_inventory.jsonl" \
    --fact-graphs "$FREEZE_ROOT/fact_graphs.jsonl" \
    --selection "$FREEZE_ROOT/article_selection.jsonl" \
    --out "$RUN_ROOT/l0_candidates.jsonl" \
    --report "$RUN_ROOT/l0_report.json" \
    --top-k-articles "$TOP_K_ARTICLES" \
    --retrieval-admission "$RETRIEVAL_ADMISSION"

echo "run_root=$RUN_ROOT"
