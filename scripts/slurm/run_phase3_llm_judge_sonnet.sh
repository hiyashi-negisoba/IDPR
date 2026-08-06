#!/bin/bash
# 61문항(sealed-59 + 승인된 dev case 2개) 전체에 대해, 이미 생성돼 있는 7개
# baseline 산출물을 anthropic/claude-sonnet-4-6로 재채점한다 — Consistency
# 순환논증 방지 규칙과 Coverage partially_met(0.5)를 반영한 새 judge
# 프롬프트로. idpr_nsn(IDPR 자체)은 여기 없다 — 기존 산출물이 59개뿐이라
# (dev case 2개 없음) 61개 계약을 못 채운다. 로컬 재생성이 61개로 끝나면
# idpr_nsn만 별도로 채점한다. 기존 run_phase3_llm_judge.sh(Gemini)와 동일한
# CPU-only 원격 API 자원.
#
# 제출 예:
#   sbatch scripts/slurm/run_phase3_llm_judge_sonnet.sh
#
#SBATCH --job-name=phase3_llm_judge_sonnet
#SBATCH --output=logs/phase3_llm_judge_sonnet_%j.out
#SBATCH --error=logs/phase3_llm_judge_sonnet_%j.err
#SBATCH --partition=gpu
#SBATCH --time=12:00:00
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

echo "=== Phase-3 Sonnet judge start (61-case, baselines only): $(date) ==="
echo "job=${SLURM_JOB_ID:-NA} host=$(hostname) cpus=${SLURM_CPUS_PER_TASK:-NA} mem=16G gpu=none walltime=12h"
echo "commit=$(git rev-parse HEAD)"

"$JUDGE_PYTHON" scripts/run_phase3_llm_judge.py \
    --model anthropic/claude-sonnet-4-6 \
    --backend sonnet \
    --sealed-inventory data/inventory/kcl_criminal_v1_draft.jsonl \
    --expected-cases 61 \
    --method-id vanilla_zero_shot \
    --method-id chain_of_thought \
    --method-id standard_rag \
    --method-id fol_autoformalizer_solver \
    --method-id acal \
    --method-id legal_chain_reasoner \
    --method-id leprec \
    --concurrency 3 \
    --timeout-seconds 300 \
    --max-tokens 16384 \
    --reasoning-effort low \
    --contract-attempts 3 \
    --api-retries 2 \
    --out experiments/results/phase3_judge_sonnet/judgments.jsonl \
    --summary experiments/results/phase3_judge_sonnet/summary.json \
    --manifest experiments/results/phase3_judge_sonnet/manifest.json \
    --cache-dir .cache/phase3_judge_sonnet \
    --overwrite

echo "=== Phase-3 Sonnet judge end: $(date) ==="
