#!/bin/bash
# IDPR 자체 산출물 하나(IDPR_JUDGE_METHOD_ID)를 anthropic/claude-sonnet-4-6 +
# 새 judge 프롬프트로 채점한다. baseline 7개는 run_phase3_llm_judge_sonnet.sh
# 가 따로 처리하므로, 같은 --out 파일에 동시에 쓰지 않도록 이 잡은 별도 출력
# 경로를 쓴다.
#
# 2026-08-07 사용자 결정: 61개 전체가 아니라 26개만 기본으로 채점한다(API
# 비용 절감, docs/handoff/CURRENT.md "방법론 결함 발견·정정"). 61개 전체(또는
# 다른 서브셋)가 필요하면 IDPR_JUDGE_CASE_LIST로 다른 case-id 목록 파일을
# 넘길 것 — 그 경우 --out 등 출력 경로도 다르게 지정할 것.
#
# 제출 예 (method id는 매 세션 새 IDPR 산출물마다 바뀌므로 반드시 지정):
#   IDPR_JUDGE_METHOD_ID=idpr_nsn_lean_61_routing_fix \
#     sbatch scripts/slurm/run_phase3_llm_judge_sonnet_idpr.sh
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

JUDGE_METHOD_ID="${IDPR_JUDGE_METHOD_ID:?set IDPR_JUDGE_METHOD_ID to the registered method id in data/eval/phase3_method_outputs.json}"
JUDGE_CASE_LIST="${IDPR_JUDGE_CASE_LIST:-$PROJECT_ROOT/.cache/phase3_substantive_law_case_lists/curated_26.txt}"
OUT_DIR="${IDPR_JUDGE_OUT_DIR:-experiments/results/phase3_judge_sonnet_idpr_${JUDGE_METHOD_ID}}"

echo "=== Phase-3 Sonnet judge start (method=$JUDGE_METHOD_ID, case-list=$JUDGE_CASE_LIST): $(date) ==="
echo "job=${SLURM_JOB_ID:-NA} host=$(hostname) cpus=${SLURM_CPUS_PER_TASK:-NA} mem=16G gpu=none walltime=4h"
echo "commit=$(git rev-parse HEAD)"

"$JUDGE_PYTHON" scripts/run_phase3_llm_judge.py \
    --model anthropic/claude-sonnet-4-6 \
    --backend sonnet \
    --sealed-inventory data/inventory/kcl_criminal_v1_draft.jsonl \
    --expected-cases 61 \
    --case-id-file "$JUDGE_CASE_LIST" \
    --method-id "$JUDGE_METHOD_ID" \
    --concurrency 3 \
    --timeout-seconds 300 \
    --max-tokens 16384 \
    --reasoning-effort low \
    --contract-attempts 3 \
    --api-retries 2 \
    --out "$OUT_DIR/judgments.jsonl" \
    --summary "$OUT_DIR/summary.json" \
    --manifest "$OUT_DIR/manifest.json" \
    --cache-dir ".cache/phase3_judge_sonnet_idpr_${JUDGE_METHOD_ID}" \
    --overwrite

echo "=== Phase-3 Sonnet judge end: $(date) ==="
