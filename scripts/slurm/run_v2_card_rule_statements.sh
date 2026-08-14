#!/bin/bash
#SBATCH --job-name=idpr_v2_card_rs
#SBATCH --output=logs/idpr_v2_card_rs_%j.out
#SBATCH --error=logs/idpr_v2_card_rs_%j.err
#SBATCH --time=02:00:00
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:1
#SBATCH --mem=48G

# ANSWERPLAN_SPEC 5.5 card retrieval for the P condition.  Reads one completed
# action-realization E2E run and writes a rule-statement artifact; no answer plan and no
# answer is produced here.  The four input artifacts are deliberately required: this
# launcher must never silently fall back to the frozen binding/episode run.
#
#   IDPR_E2E_RESULTS=... IDPR_CALL2_ARTIFACT=... IDPR_ISSUE_BINDINGS=... \
#   IDPR_PLAN_ARTIFACT=... IDPR_HF_HOME=/data5/jaehoonjeong/.cache/huggingface \
#   sbatch scripts/slurm/run_v2_card_rule_statements.sh

set -euo pipefail

source "${IDPR_PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}/scripts/slurm/_env.sh"

CLIENT_PYTHON="${IDPR_PYTHON:-/data5/jaehoonjeong/miniconda3/bin/python}"
RUN_ROOT="${IDPR_RUN_ROOT:-$PROJECT_ROOT/experiments/v2_action_realization_26_e2e}"
E2E_RESULTS="${IDPR_E2E_RESULTS:?IDPR_E2E_RESULTS is required (new action-realization Scallop results)}"
CALL2_ARTIFACT="${IDPR_CALL2_ARTIFACT:?IDPR_CALL2_ARTIFACT is required (new action-realization Call 2 output)}"
ISSUE_BINDINGS="${IDPR_ISSUE_BINDINGS:?IDPR_ISSUE_BINDINGS is required (new action-atomic Call 1.5 output)}"
PLAN_ARTIFACT="${IDPR_PLAN_ARTIFACT:?IDPR_PLAN_ARTIFACT is required (new action-realization planner output)}"
OUT="${IDPR_CARD_RS_OUT:-$RUN_ROOT/card_rule_statements/rule_statements.jsonl}"

export TOKENIZERS_PARALLELISM=false
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export PYTHONPATH="$PROJECT_ROOT/src"

cd "$PROJECT_ROOT"
mkdir -p logs "$(dirname "$OUT")"
test -s "$E2E_RESULTS"
test -s "$CALL2_ARTIFACT"
test -s "$ISSUE_BINDINGS"
test -s "$PLAN_ARTIFACT"
echo "=== v2 card rule statements start: $(date) ==="
echo "job=${SLURM_JOB_ID:-none} host=$(hostname -s) run_root=$RUN_ROOT out=$OUT"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || true

"$CLIENT_PYTHON" scripts/build_v2_card_rule_statements.py \
    --e2e-results "$E2E_RESULTS" \
    --call2-artifact "$CALL2_ARTIFACT" \
    --issue-bindings "$ISSUE_BINDINGS" \
    --plan-artifact "$PLAN_ARTIFACT" \
    --out "$OUT"

echo "=== v2 card rule statements end: $(date) ==="
