#!/bin/bash
# Phase-3 59문항의 7개 baseline + IDPR 출력에 대한 원격 Gemini API 채점.
# 기존 원격 API 잡 선례와 동일한 CPU-only 자원: gpu partition, GPU 미할당,
# cpu=2, mem=32G, walltime=48h. 생성 잡 dependency는 sbatch 제출 시 지정한다.
#
# 제출 예:
#   sbatch --dependency=afterok:218467 scripts/slurm/run_phase3_llm_judge.sh
#
# 결과와 API cache는 원자적으로 저장되고 완료 행은 재사용하므로 재제출 가능하다.
#
#SBATCH --job-name=phase3_llm_judge
#SBATCH --output=logs/phase3_llm_judge_%j.out
#SBATCH --error=logs/phase3_llm_judge_%j.err
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

echo "=== Phase-3 Gemini judge start: $(date) ==="
echo "job=${SLURM_JOB_ID:-NA} host=$(hostname) cpus=${SLURM_CPUS_PER_TASK:-NA} mem=32G gpu=none walltime=48h"
echo "upstream_generation_job=218467 dependency=${SLURM_JOB_DEPENDENCY:-afterok:218467}"

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
    --concurrency 1 \
    --timeout-seconds 300 \
    --max-tokens 16384 \
    --reasoning-effort low \
    --contract-attempts 3 \
    --api-retries 0

echo "=== Phase-3 Gemini judge end: $(date) ==="
