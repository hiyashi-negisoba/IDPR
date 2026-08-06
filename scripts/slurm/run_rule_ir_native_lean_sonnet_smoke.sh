#!/bin/bash
# r10/r14 + 4개 사례 소규모 재실행: 술어평가 4-state + 신뢰 상태 수정이 실제로
# 결론을 바꾸는지 Claude Sonnet(anthropic/claude-sonnet-4-6, SKI-ML 게이트웨이 경유)로
# 확인한다. 원격 API 전용 잡이므로 기존 phase3_llm_judge.sh 선례와 동일한 CPU-only
# 자원(gpu partition, GPU 미할당)을 쓴다.
#
#SBATCH --job-name=ruleir_native_sonnet_smoke
#SBATCH --output=logs/ruleir_native_sonnet_smoke_%j.out
#SBATCH --error=logs/ruleir_native_sonnet_smoke_%j.err
#SBATCH --partition=gpu
#SBATCH --time=02:00:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=16G
# (의도적으로 --gres=gpu 없음: 원격 Anthropic API를 SKI-ML 게이트웨이로 호출한다)

set -euo pipefail

source "${IDPR_PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}/scripts/slurm/_env.sh"
cd "$PROJECT_ROOT"
mkdir -p logs

set -a
[ -f "$PROJECT_ROOT/.env" ] && source "$PROJECT_ROOT/.env"
set +a

RUN_PYTHON="${IDPR_JUDGE_PYTHON:-$PROJECT_ROOT/.venv/bin/python}"
if [ ! -x "$RUN_PYTHON" ]; then
    echo "run Python is not executable: $RUN_PYTHON" >&2
    exit 2
fi

CASE_LIST="${IDPR_CASE_LIST:?set IDPR_CASE_LIST to a file of inventory sub_question_ids, one per line}"
RUN_DIR="${IDPR_RUN_DIR:-$PROJECT_ROOT/experiments/results/rule_ir_native_sonnet_smoke_${SLURM_JOB_ID}}"
MODEL="${IDPR_SONNET_MODEL:-anthropic/claude-sonnet-4-6}"

if [ ! -s "$CASE_LIST" ]; then
    echo "case list is empty or missing: $CASE_LIST" >&2
    exit 1
fi

TOTAL=$(grep -c '[^[:space:]]' "$CASE_LIST")
echo "=== RuleIR-native Sonnet smoke start: $(date) ==="
echo "job=${SLURM_JOB_ID:-NA} host=$(hostname) cases=$TOTAL model=$MODEL"
echo "commit=$(git rev-parse HEAD)"

INDEX=0
FAILED=0
STATUS_LOG="$RUN_DIR/batch_status.tsv"
mkdir -p "$RUN_DIR"
: > "$STATUS_LOG"
while read -r CASE_ID; do
    [ -n "$CASE_ID" ] || continue
    INDEX=$((INDEX + 1))
    echo "--- [$INDEX/$TOTAL] $CASE_ID : $(date +%H:%M:%S) ---"
    if "$RUN_PYTHON" scripts/run_rule_ir_native_lean_sonnet.py \
        --model "$MODEL" \
        --case-id "$CASE_ID" \
        --out-dir "$RUN_DIR"; then
        printf '%s\tok\n' "$CASE_ID" >> "$STATUS_LOG"
    else
        printf '%s\tfailed\n' "$CASE_ID" >> "$STATUS_LOG"
        FAILED=$((FAILED + 1))
        echo "case failed: $CASE_ID" >&2
    fi
done < "$CASE_LIST"

echo "=== RuleIR-native Sonnet smoke end: $(date) ==="
echo "cases=$TOTAL failed=$FAILED status=$STATUS_LOG run_dir=$RUN_DIR"
[ "$FAILED" -eq 0 ]
