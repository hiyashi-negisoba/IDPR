#!/bin/bash

# 네 축(completion·evidence carrier·elements·participation·doctrine·concurrence)을 닫은 뒤의
# 첫 전체 관통. 목적은 "더 고칠 것 찾기"가 아니라 하나다 --
#
#   닫았다고 판단한 구조가 production chain 끝까지 실제로 연결되는가.
#
# 그래서 여기서 보는 것은 경로 단절뿐이다. 개별 UNKNOWN이나 모델 오판은 이 실행의 판단
# 대상이 아니다.
#
# 기존 vLLM service allocation 안에서 CPU job step으로만 돌린다. GPU를 요청하지 않는다.
#
#   IDPR_STEP8_SERVICE_JOB_ID=<job> srun --jobid=<job> --ntasks=1 --cpus-per-task=8 /bin/bash \
#     /data5/jaehoonjeong/IDPR/scripts/slurm/run_v2_axis_closure_e2e.sh --execution-approved
#
# 단계를 건너뛰려면 IDPR_AXIS_SKIP에 이름을 공백으로 나열한다. 이미 만든 산출물이 있으면
# 그 단계만 빼고 이어서 돌릴 수 있다.
#
#   IDPR_AXIS_SKIP="call15p call15d" ... --execution-approved
#
# 단계 이름: call15p call15d plan_participation plan_doctrine dependency_route call2
#            linked_offender_call2 absorption symbolic answer_plan call3

set -euo pipefail

if [ "${1:-}" != "--execution-approved" ] || [ "$#" -ne 1 ]; then
    echo "usage: $0 --execution-approved" >&2
    exit 2
fi

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CLIENT_PYTHON="${IDPR_STEP8_CLIENT_PYTHON:-/data5/jaehoonjeong/miniconda3/bin/python}"
SERVICE_JOB_ID="${IDPR_STEP8_SERVICE_JOB_ID:?set the vLLM service job id}"
SERVICE_ROOT="${IDPR_STEP8_V0_SERVICE_ROOT:-/data5/jaehoonjeong/IDPR-step8-v0-host/experiments/v2_call1_v0_service_${SERVICE_JOB_ID}}"
SERVED_MODEL="${IDPR_SERVED_MODEL:-idpr-gemma-4-26b-a4b}"
API_KEY="${IDPR_STEP8_API_KEY:-local-idpr}"
SKIP="${IDPR_AXIS_SKIP:-}"

RUN_ROOT="${IDPR_AXIS_RUN_ROOT:-$PROJECT_ROOT/experiments/v2_axis_closure_26_e2e}"
CALL1="${IDPR_CALL1_ARTIFACT:-$PROJECT_ROOT/experiments/v2_restart_rebuild/call1/router_output.jsonl}"
CALL15="${IDPR_CALL15_ARTIFACT:-$PROJECT_ROOT/experiments/v2_action_realization_26_e2e/call15_action_bindings_26.jsonl}"
BASE_PLAN="${IDPR_BASE_PLAN:-$PROJECT_ROOT/experiments/v2_action_realization_26_e2e/plan_ckpt/evaluation_instance_plan.jsonl}"

test -x "$CLIENT_PYTHON"
test -s "$CALL1"
test -s "$CALL15"
test -s "$BASE_PLAN"

PORT="$("$CLIENT_PYTHON" - "$SERVICE_ROOT/state.json" "$SERVED_MODEL" "$SERVICE_JOB_ID" <<'PY'
import json
import sys
from pathlib import Path

state = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
if state.get("status") != "READY":
    raise SystemExit(f"service is not READY: {state.get('status')!r}")
if state.get("job_id") != sys.argv[3]:
    raise SystemExit(f"expected service job {sys.argv[3]}, got {state.get('job_id')!r}")
if state.get("served_model") != sys.argv[2]:
    raise SystemExit(f"served-model mismatch: {state.get('served_model')!r}")
port = int(state.get("port"))
if not 1 <= port <= 65535:
    raise SystemExit(f"invalid service port: {port!r}")
print(port)
PY
)"

STATE_HOST="$("$CLIENT_PYTHON" -c "import json;print(json.load(open('$SERVICE_ROOT/state.json'))['host'])")"
if [ "$(hostname -s)" != "$STATE_HOST" ]; then
    echo "must run on service host $STATE_HOST; got $(hostname -s)" >&2
    exit 2
fi

BASE_URL="http://127.0.0.1:${PORT}"
export PYTHONPATH="$PROJECT_ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
mkdir -p "$RUN_ROOT"

skipped() {
    case " $SKIP " in *" $1 "*) return 0 ;; *) return 1 ;; esac
}

step() {
    local name="$1"
    shift
    if skipped "$name"; then
        echo "=== [$name] skipped ==="
        return 0
    fi
    echo "=== [$name] $(date -u +%H:%M:%S) ==="
    "$@"
    echo "=== [$name] done $(date -u +%H:%M:%S) ==="
}

# 1. Call 1.5-P -- 사람 사이의 관계. episode 스코프가 기본이다. 행위 스코프는 두 행위의
#    병렬로만 서술되는 공동행동을 구조적으로 잘라낸다.
INTERACTIONS="$RUN_ROOT/call15_factual_interaction.jsonl"
step call15p "$CLIENT_PYTHON" "$PROJECT_ROOT/scripts/run_v2_call15_factual_interaction.py" \
    --base-url "$BASE_URL" --model "$SERVED_MODEL" --api-key "$API_KEY" \
    --call15-artifact "$CALL15" \
    --interaction-scope episode \
    --out "$INTERACTIONS" \
    --prompt-approved

# 2. Call 1.5-D -- 어느 법리가 이 사건에서 제기되는가. 이것이 없으면 13개 doctrine 전부가
#    leaf target을 얻지 못해 잠든 채로 끝난다.
CUES_OUT="$RUN_ROOT/call15d/doctrine_cues.jsonl"
mkdir -p "$RUN_ROOT/call15d"
step call15d "$CLIENT_PYTHON" "$PROJECT_ROOT/scripts/run_v2_call15_doctrine_cues.py" \
    --base-url "$BASE_URL" --model "$SERVED_MODEL" --api-key "$API_KEY" \
    --call15-artifact "$CALL15" \
    --out "$CUES_OUT" \
    --prompt-approved

# 3. participation plan -- 가담 후보와 그 mode가 요구하는 요건을 target으로 연다.
PLAN_P="$RUN_ROOT/plan_participation/evaluation_instance_plan.jsonl"
step plan_participation "$CLIENT_PYTHON" "$PROJECT_ROOT/scripts/build_v2_factual_participation_plan.py" \
    --plan-artifact "$BASE_PLAN" \
    --call15-artifact "$CALL15" \
    --interaction-artifact "$INTERACTIONS" \
    --out "$PLAN_P"

# 4. doctrine target plan -- 제기된 법리의 leaf를 target으로 연다.
PLAN_D="$RUN_ROOT/plan_doctrine/evaluation_instance_plan.jsonl"
step plan_doctrine "$CLIENT_PYTHON" "$PROJECT_ROOT/scripts/build_v2_doctrine_target_plan.py" \
    --plan-artifact "$PLAN_P" \
    --call15d-artifact "$CUES_OUT" \
    --out "$PLAN_D"

# 4-b. dependency ROUTE -- 질문이 죄책을 묻지 않은 사람에 대한 offense routing.
#      Call 1과 같은 ROUTE operation이고, 다른 것은 누구를 어느 범위로 라우팅하는가뿐이다.
#      plan의 `linked_offender_dependencies`가 비어 있으면 아무것도 하지 않으므로, 이 단계가
#      없어도 나머지 체인은 정상으로 돈다 -- 대신 제151조만 조용히 UNKNOWN으로 남는다.
#
#      산출물의 `predicate_targets`는 5-b에서 소비한다.
DEPENDENCY_ROUTE="$RUN_ROOT/dependency_route/predecessor_candidates.jsonl"
mkdir -p "$RUN_ROOT/dependency_route"
step dependency_route "$CLIENT_PYTHON" "$PROJECT_ROOT/scripts/run_v2_dependency_route.py" \
    --base-url "$BASE_URL" --model "$SERVED_MODEL" --api-key "$API_KEY" \
    --plan "$PLAN_D" \
    --inventory "$PROJECT_ROOT/data/inventory/kcl_criminal_v1_draft.jsonl" \
    --out "$DEPENDENCY_ROUTE"

# 5. Call 2 -- 사실 판단. 재실행에는 planner occurrence evidence가 필수다.
CALL2="$RUN_ROOT/call2/grounding_output.jsonl"
mkdir -p "$RUN_ROOT/call2"
# `--planner-occurrence-evidence`가 켜져 있으면 offline gold는 읽지 않는다. 인자 자체는
# 필수라서 경로만 넘기고 값은 쓰이지 않는다.
step call2 "$CLIENT_PYTHON" "$PROJECT_ROOT/scripts/run_v2_call2_pilot.py" \
    --base-url "$BASE_URL" --model "$SERVED_MODEL" --api-key "$API_KEY" \
    --call1-artifact "$CALL1" \
    --gold-occurrences "$PROJECT_ROOT/data/v2/gold_occurrences.jsonl" \
    --gold-article263-pairs "$PROJECT_ROOT/data/v2/gold_article263_pairs.jsonl" \
    --plan-artifact "$PLAN_D" \
    --planner-occurrence-evidence \
    --out "$CALL2" \
    --prompt-approved

# 5-b. linked offender participant Call 2 -- 선행범죄 predicate를 그 사람에게 묻고 신분으로
#      접는다. Call 2 아티팩트를 보강하므로 symbolic은 이 산출물을 읽는다. dependency가 없는
#      사건은 원본 행이 그대로 지나간다.
CALL2_ENRICHED="$RUN_ROOT/call2/grounding_output_with_article151.jsonl"
step linked_offender_call2 "$CLIENT_PYTHON" "$PROJECT_ROOT/scripts/run_v2_linked_offender_call2.py" \
    --base-url "$BASE_URL" --model "$SERVED_MODEL" --api-key "$API_KEY" \
    --dependency-route "$DEPENDENCY_ROUTE" \
    --call2 "$CALL2" \
    --out "$CALL2_ENRICHED"

# 6. 흡수조건 -- 저작된 흡수규칙의 조건을 사건별로 평가한다. 이것이 없으면 조건이 영구
#    UNKNOWN이라 흡수가 한 번도 발화하지 못한다.
CONDITIONS="$RUN_ROOT/absorption/concurrence_condition_assessments.jsonl"
mkdir -p "$RUN_ROOT/absorption"
step absorption "$CLIENT_PYTHON" "$PROJECT_ROOT/scripts/run_v2_absorption_condition_pairs.py" \
    --base-url "$BASE_URL" --model "$SERVED_MODEL" --api-key "$API_KEY" \
    --pair-plan "$PLAN_D" \
    --call15-artifact "$CALL15" \
    --out "$CONDITIONS" \
    --prompt-approved

# 7. symbolic -- 결정론적 단계. 판단은 여기 출력으로 한다.
SYMBOLIC="$RUN_ROOT/scallop/results.jsonl"
mkdir -p "$RUN_ROOT/scallop"
step symbolic "$CLIENT_PYTHON" "$PROJECT_ROOT/scripts/run_v2_scallop_e2e.py" \
    --call2-artifact "$CALL2_ENRICHED" \
    --plan "$PLAN_D" \
    --concurrence-condition-assessments "$CONDITIONS" \
    --work-dir "$RUN_ROOT/scallop/work" \
    --out "$SYMBOLIC"

# 8. AnswerPlan -- 아는 것만 정확한 단위로 넘긴다.
PLANS="$RUN_ROOT/answer_plan"
step answer_plan "$CLIENT_PYTHON" "$PROJECT_ROOT/scripts/build_v2_answer_plan.py" \
    --e2e-results "$SYMBOLIC" \
    --call2-artifact "$CALL2_ENRICHED" \
    --issue-bindings "$CALL15" \
    --plan-artifact "$PLAN_D" \
    --out "$PLANS"

# 9. Call 3 -- 답안.
step call3 "$CLIENT_PYTHON" "$PROJECT_ROOT/scripts/run_v2_call3.py" \
    --answer-plans "$PLANS/answer_plans.jsonl" \
    --base-url "$BASE_URL" --model "$SERVED_MODEL" \
    --out "$RUN_ROOT/call3"

echo
echo "=== chain complete ==="
echo "run_root=$RUN_ROOT"
