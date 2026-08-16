#!/bin/bash

# ANSWERPLAN_SPEC §5.5 근거 회수. 카드 코퍼스에서 `(offense instance, predicate)` 쌍마다
# 판시 법리 문장을 회수해 AnswerPlan의 `rule_statements[]`에만 싣는다 -- truth는 건드리지
# 않는다(SPEC 4-10). 이 산출물이 있으면 P 조건, 없으면 N 조건이다.
#
# 임베딩·재정렬 모델을 올리므로 GPU를 요청한다. IDPR_HF_HOME을 반드시 넘긴다.
#
#   IDPR_HF_HOME=/data5/jaehoonjeong/.cache/huggingface \
#   IDPR_CARD_RUN_ROOT=$PWD/experiments/v2_unknown_reduction_26 \
#     sbatch scripts/slurm/run_v2_card_rule_statements.sh

#SBATCH --job-name=v2_card_rule_statements
#SBATCH --output=logs/v2_card_rule_statements_%j.out
#SBATCH --error=logs/v2_card_rule_statements_%j.err
#SBATCH --time=02:00:00
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:1
#SBATCH --mem=48G

set -euo pipefail
source "${IDPR_PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}/scripts/slurm/_env.sh"

RUN_ROOT="${IDPR_CARD_RUN_ROOT:?set the axis run root that already holds scallop/ and call2/}"
CALL15="${IDPR_CALL15_ARTIFACT:-$PROJECT_ROOT/experiments/v2_rulebase_regen_26/call15/issue_binding.jsonl}"
OUT_DIR="${IDPR_CARD_OUT:-$RUN_ROOT/card_rule_statements}"

export PYTHONPATH="$PROJECT_ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
unset HF_HUB_OFFLINE TRANSFORMERS_OFFLINE

cd "$PROJECT_ROOT"
mkdir -p logs "$OUT_DIR"
"$CLIENT_PYTHON" scripts/build_v2_card_rule_statements.py \
    --e2e-results "$RUN_ROOT/scallop/results.jsonl" \
    --call2-artifact "$RUN_ROOT/call2/grounding_output_with_article151.jsonl" \
    --issue-bindings "$CALL15" \
    --plan-artifact "$RUN_ROOT/plan_doctrine/evaluation_instance_plan.jsonl" \
    --out "$OUT_DIR/rule_statements.jsonl"

echo "out=$OUT_DIR/rule_statements.jsonl"
