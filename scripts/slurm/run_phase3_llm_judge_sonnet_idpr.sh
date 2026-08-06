#!/bin/bash
# IDPR 자체(idpr_nsn_lean_61 — 4단계 라우팅 확장까지 반영한 현재 코드로
# 61개 전체 재생성한 답안)를 anthropic/claude-sonnet-4-6 + 새 judge
# 프롬프트로 채점한다. baseline 7개는 run_phase3_llm_judge_sonnet.sh(job
# 220075/220077, 재시도 220223)가 이미/따로 처리 중이므로, 같은 --out
# 파일에 동시에 쓰지 않도록 이 잡은 별도 출력 경로를 쓴다.
#
# 제출 예:
#   sbatch scripts/slurm/run_phase3_llm_judge_sonnet_idpr.sh
#
#SBATCH --job-name=phase3_llm_judge_sonnet_idpr
#SBATCH --output=logs/phase3_llm_judge_sonnet_idpr_%j.out
#SBATCH --error=logs/phase3_llm_judge_sonnet_idpr_%j.err
#SBATCH --partition=gpu
#SBATCH --time=4:00:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=16G
# (의도적으로 --gres=gpu 없음: judge는 원격 Sonnet API를 SKI-ML 게이트웨이로 쓴다)

set -euo pipefail

source "${IDPR_PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}/scripts/slurm/_env.sh"
cd "$PROJECT_ROOT"
mkdir -p logs

JUDGE_PYTHON="${IDPR_JUDGE_PYTHON:-$PROJECT_ROOT/.venv/bin/python}"
if [ ! -x "$JUDGE_PYTHON" ]; then
    echo "judge Python is not executable: $JUDGE_PYTHON" >&2
    exit 2
fi

echo "=== Phase-3 Sonnet judge start (61-case, idpr_nsn_lean_61 only): $(date) ==="
echo "job=${SLURM_JOB_ID:-NA} host=$(hostname) cpus=${SLURM_CPUS_PER_TASK:-NA} mem=16G gpu=none walltime=4h"
echo "commit=$(git rev-parse HEAD)"

"$JUDGE_PYTHON" scripts/run_phase3_llm_judge.py \
    --model anthropic/claude-sonnet-4-6 \
    --backend sonnet \
    --sealed-inventory data/inventory/kcl_criminal_v1_draft.jsonl \
    --expected-cases 61 \
    --method-id idpr_nsn_lean_61 \
    --concurrency 3 \
    --timeout-seconds 300 \
    --max-tokens 16384 \
    --reasoning-effort low \
    --contract-attempts 3 \
    --api-retries 2 \
    --out experiments/results/phase3_judge_sonnet_idpr/judgments.jsonl \
    --summary experiments/results/phase3_judge_sonnet_idpr/summary.json \
    --manifest experiments/results/phase3_judge_sonnet_idpr/manifest.json \
    --cache-dir .cache/phase3_judge_sonnet_idpr \
    --overwrite

echo "=== Phase-3 Sonnet judge end: $(date) ==="
