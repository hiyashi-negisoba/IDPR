#!/bin/bash
# 26문항(실체법 전용 curated 서브셋, legal_area=="substantive")에 대해 7개
# baseline 산출물을 anthropic/claude-sonnet-4-6로 재채점한다 — Consistency
# 순환논증 방지 규칙과 Coverage partially_met(0.5)를 반영한 새 judge
# 프롬프트로. idpr_nsn(IDPR 자체)은 여기 없다.
#
# 2026-08-07 사용자 결정: 61개 전체가 아니라 26개만 기본으로 채점한다(API
# 비용 절감 — 절차법 33개는 IDPR이 원래 다루지 않는 스코프라 채점할 이유가
# 없다, docs/handoff/CURRENT.md "방법론 결함 발견·정정"). 61개 전체(또는 다른
# 서브셋)가 필요하면 IDPR_JUDGE_CASE_LIST로 다른 case-id 목록 파일을 넘길 것 —
# 그 경우 --out 등 출력 경로도 다르게 지정해 기존 26개 전용 산출물을 덮어쓰지
# 않도록 할 것. 기존 run_phase3_llm_judge.sh(Gemini)와 동일한 CPU-only 원격
# API 자원.
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

JUDGE_CASE_LIST="${IDPR_JUDGE_CASE_LIST:-$PROJECT_ROOT/.cache/phase3_substantive_law_case_lists/curated_26.txt}"

echo "=== Phase-3 Sonnet judge start (case-list=$JUDGE_CASE_LIST, baselines only): $(date) ==="
echo "job=${SLURM_JOB_ID:-NA} host=$(hostname) cpus=${SLURM_CPUS_PER_TASK:-NA} mem=16G gpu=none walltime=12h"
echo "commit=$(git rev-parse HEAD)"

"$JUDGE_PYTHON" scripts/run_phase3_llm_judge.py \
    --model anthropic/claude-sonnet-4-6 \
    --backend sonnet \
    --sealed-inventory data/inventory/kcl_criminal_v1_draft.jsonl \
    --expected-cases 61 \
    --case-id-file "$JUDGE_CASE_LIST" \
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
    --out experiments/results/phase3_judge_sonnet_26/judgments.jsonl \
    --summary experiments/results/phase3_judge_sonnet_26/summary.json \
    --manifest experiments/results/phase3_judge_sonnet_26/manifest.json \
    --cache-dir .cache/phase3_judge_sonnet_26 \
    --overwrite

echo "=== Phase-3 Sonnet judge end: $(date) ==="
