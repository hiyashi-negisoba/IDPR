#!/bin/bash
# BLOCK_NONE에서 8/8 차단된 동일 원문을 Gemini native safety=OFF로 검증한다.
# 기존 원격 API 잡과 동일한 CPU-only 자원을 사용하고 원문 축약은 하지 않는다.
#
#SBATCH --job-name=phase3_judge_off
#SBATCH --output=logs/phase3_judge_off_%j.out
#SBATCH --error=logs/phase3_judge_off_%j.err
#SBATCH --partition=gpu
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=32G
# (의도적으로 --gres=gpu 없음)

set -euo pipefail

source "${IDPR_PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}/scripts/slurm/_env.sh"
cd "$PROJECT_ROOT"
mkdir -p logs

JUDGE_PYTHON="${IDPR_JUDGE_PYTHON:-$PROJECT_ROOT/.venv/bin/python}"
if [ ! -x "$JUDGE_PYTHON" ]; then
    echo "judge Python is not executable: $JUDGE_PYTHON" >&2
    exit 2
fi

"$JUDGE_PYTHON" scripts/run_phase3_llm_judge.py \
    --model gemini/gemini-2.5-flash \
    --method-id vanilla_zero_shot \
    --method-id fol_autoformalizer_solver \
    --method-id idpr_nsn \
    --case-id kcl_criminal_r11_p1_q4 \
    --concurrency 1 \
    --timeout-seconds 300 \
    --max-tokens 16384 \
    --reasoning-effort low \
    --contract-attempts 3 \
    --api-retries 0 \
    --gemini-safety-threshold OFF \
    --out experiments/results/phase3_judge_off_smoke/judgments.jsonl \
    --summary experiments/results/phase3_judge_off_smoke/summary.json \
    --manifest experiments/results/phase3_judge_off_smoke/manifest.json \
    --cache-dir .cache/phase3_judge_off_smoke \
    --overwrite
