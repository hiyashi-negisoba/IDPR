#!/bin/bash
# P vs N judge for the defeated_by_state-fix evaluation baseline (commit 13232a5,
# agent/v2-semantic-integrity-fix).  Same underlying scripts/run_phase3_llm_judge.py
# invocation as run_phase3_llm_judge_sonnet_idpr.sh; this wrapper only differs in
# scoring two --method-id values (P, N) in one job so their paired bootstrap delta
# comes out of a single run.
#
#SBATCH --job-name=phase3_llm_judge_pn_dbsfix
#SBATCH --output=logs/phase3_llm_judge_pn_dbsfix_%j.out
#SBATCH --error=logs/phase3_llm_judge_pn_dbsfix_%j.err
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

JUDGE_CASE_LIST="${IDPR_JUDGE_CASE_LIST:-$PROJECT_ROOT/.cache/phase3_substantive_law_case_lists/curated_26.txt}"
OUT_DIR="${IDPR_JUDGE_OUT_DIR:-experiments/results/phase3_judge_sonnet_pn_defeated_by_state_fix}"

echo "=== Phase-3 Sonnet P/N judge start (case-list=$JUDGE_CASE_LIST): $(date) ==="
echo "job=${SLURM_JOB_ID:-NA} host=$(hostname) cpus=${SLURM_CPUS_PER_TASK:-NA} mem=16G gpu=none walltime=4h"
echo "commit=$(git rev-parse HEAD)"

"$JUDGE_PYTHON" scripts/run_phase3_llm_judge.py \
    --model anthropic/claude-sonnet-4-6 \
    --backend sonnet \
    --sealed-inventory data/inventory/kcl_criminal_v1_draft.jsonl \
    --expected-cases 61 \
    --case-id-file "$JUDGE_CASE_LIST" \
    --method-id v2_idpr_p_defeated_by_state_fix_26 \
    --method-id v2_idpr_n_defeated_by_state_fix_26 \
    --paired-target-method-id v2_idpr_p_defeated_by_state_fix_26 \
    --concurrency 3 \
    --timeout-seconds 300 \
    --max-tokens 16384 \
    --reasoning-effort low \
    --contract-attempts 3 \
    --api-retries 2 \
    --out "$OUT_DIR/judgments.jsonl" \
    --summary "$OUT_DIR/summary.json" \
    --manifest "$OUT_DIR/manifest.json" \
    --cache-dir ".cache/phase3_judge_sonnet_pn_defeated_by_state_fix" \
    --overwrite

echo "=== Phase-3 Sonnet P/N judge end: $(date) ==="
