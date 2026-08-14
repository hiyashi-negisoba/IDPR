#!/bin/bash
#SBATCH --job-name=idpr_v2_card_rs
#SBATCH --output=logs/idpr_v2_card_rs_%j.out
#SBATCH --error=logs/idpr_v2_card_rs_%j.err
#SBATCH --time=02:00:00
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:1
#SBATCH --mem=48G

# ANSWERPLAN_SPEC 5.5 card retrieval for the P condition.  Reads the frozen N artifacts
# and writes a rule-statement artifact; no answer plan and no answer is produced here.
#
#   IDPR_HF_HOME=/data5/jaehoonjeong/.cache/huggingface \
#   sbatch scripts/slurm/run_v2_card_rule_statements.sh

set -euo pipefail

source "${IDPR_PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}/scripts/slurm/_env.sh"

CLIENT_PYTHON="${IDPR_PYTHON:-/data5/jaehoonjeong/miniconda3/bin/python}"
RUN_ROOT="$PROJECT_ROOT/experiments/v2_call15_directscope_26_causal"
OUT="${IDPR_CARD_RS_OUT:-$RUN_ROOT/card_rule_statements_v1/rule_statements.jsonl}"

export TOKENIZERS_PARALLELISM=false
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export PYTHONPATH="$PROJECT_ROOT/src"

cd "$PROJECT_ROOT"
mkdir -p logs "$(dirname "$OUT")"
echo "=== v2 card rule statements start: $(date) ==="
echo "job=${SLURM_JOB_ID:-none} host=$(hostname -s) out=$OUT"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader || true

"$CLIENT_PYTHON" scripts/build_v2_card_rule_statements.py \
    --e2e-results "$RUN_ROOT/final_responsibility_v13_gf_rebase/results.jsonl" \
    --call2-artifact "$RUN_ROOT/call2_v10_ground_fact_rebase/grounding_output_rebased.jsonl" \
    --issue-bindings "$RUN_ROOT/issue_bindings.jsonl" \
    --plan-artifact "$RUN_ROOT/participation_plan_v7_necessary_gate/evaluation_instance_plan.jsonl" \
    --out "$OUT"

echo "=== v2 card rule statements end: $(date) ==="
