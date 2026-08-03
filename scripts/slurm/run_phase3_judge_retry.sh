#!/bin/bash
# 기존 성공 410건은 재사용하고, q4를 제외한 실패 건만 Gemini로 재채점한다.
# 제출 예:
#   sbatch --dependency=afterok:<schema-smoke-job> scripts/slurm/run_phase3_judge_retry.sh
#SBATCH --job-name=phase3_judge_retry
#SBATCH --output=logs/phase3_judge_retry_%j.out
#SBATCH --error=logs/phase3_judge_retry_%j.err
#SBATCH --partition=gpu
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=32G
# (의도적으로 --gres=gpu 없음: judge는 원격 Gemini API를 사용한다)

set -euo pipefail

source "${IDPR_PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}/scripts/slurm/_env.sh"
cd "$PROJECT_ROOT"
mkdir -p logs

JUDGE_PYTHON="${IDPR_JUDGE_PYTHON:-$PROJECT_ROOT/.venv/bin/python}"
if [ ! -x "$JUDGE_PYTHON" ]; then
    echo "judge Python is not executable: $JUDGE_PYTHON" >&2
    exit 2
fi

echo "=== Phase-3 Gemini retry start: $(date) ==="
echo "job=${SLURM_JOB_ID:-NA} host=$(hostname) cpus=${SLURM_CPUS_PER_TASK:-NA} mem=32G gpu=none walltime=48h"
echo "upstream=${SLURM_JOB_DEPENDENCY:-schema-smoke-afterok} excluded_case=kcl_criminal_r11_p1_q4"

"$JUDGE_PYTHON" scripts/run_phase3_llm_judge.py \
    --model gemini/gemini-2.5-flash \
    --method-id vanilla_zero_shot \
    --method-id chain_of_thought \
    --method-id standard_rag \
    --method-id fol_autoformalizer_solver \
    --method-id acal \
    --method-id legal_chain_reasoner \
    --method-id leprec \
    --method-id idpr_nsn \
    --exclude-case-id kcl_criminal_r11_p1_q4 \
    --concurrency 1 \
    --timeout-seconds 300 \
    --max-tokens 16384 \
    --reasoning-effort low \
    --contract-attempts 6 \
    --api-retries 0 \
    --gemini-safety-threshold OFF \
    --cache-dir .cache/phase3_judge_retry_schema \
    --summary experiments/results/phase3_judge/retry_summary.json \
    --manifest experiments/results/phase3_judge/retry_manifest.json

echo "=== Phase-3 Gemini retry end: $(date) ==="
