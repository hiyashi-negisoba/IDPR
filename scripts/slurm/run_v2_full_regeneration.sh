#!/bin/bash

# 2026-08-15 rulebase 개정 이후의 전체 재생성 상류 -- Call 1 → Call 1.5 → planner.
#
# 이 단계들이 기존 축 체인(run_v2_axis_closure_e2e.sh)에 없는 이유는, 그 체인이 Call 1과
# Call 1.5를 **고정 입력으로 받도록** 설계되었기 때문이다. 이번에는 그 둘이 바뀌었다.
#
#   * Call 1: offense 6개가 늘어 routing universe가 달라졌다. 옛 manifest는 lineage 검증에서
#     실패하고, 그것이 의도된 동작이다.
#   * Call 1.5: binding 계약에 사실 3개(directed_action_target / actual_result_bearer /
#     linked_offender)가 늘었다.
#
# 기존 vLLM service allocation 안에서 CPU job step으로만 돌린다. GPU를 요청하지 않는다.
#
#   IDPR_STEP8_SERVICE_JOB_ID=223815 srun --jobid=223815 --ntasks=1 --cpus-per-task=8 \
#     /bin/bash scripts/slurm/run_v2_full_regeneration.sh --execution-approved
#
# 단계 이름: call1 call15 plan

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
SKIP="${IDPR_REGEN_SKIP:-}"

RUN_ROOT="${IDPR_REGEN_RUN_ROOT:-$PROJECT_ROOT/experiments/v2_rulebase_regen_26}"
GOLD_PARQUET="${IDPR_GOLD_PARQUET:-/home/jaehoonjeong/data/sp_qwen/warehouse/lbox_kcl/kcl_essay/test.parquet}"

test -x "$CLIENT_PYTHON"
test -s "$GOLD_PARQUET"

STATE="$SERVICE_ROOT/state.json"
PORT="$("$CLIENT_PYTHON" - "$STATE" "$SERVED_MODEL" "$SERVICE_JOB_ID" <<'PY'
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
print(int(state.get("port")))
PY
)"
MODEL_SNAPSHOT="$("$CLIENT_PYTHON" -c "import json;print(json.load(open('$STATE'))['model_snapshot'])")"
STATE_HOST="$("$CLIENT_PYTHON" -c "import json;print(json.load(open('$STATE'))['host'])")"
if [ "$(hostname -s)" != "$STATE_HOST" ]; then
    echo "must run on service host $STATE_HOST; got $(hostname -s)" >&2
    exit 2
fi

BASE_URL="http://127.0.0.1:${PORT}"
export PYTHONPATH="$PROJECT_ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
mkdir -p "$RUN_ROOT/call1" "$RUN_ROOT/call15" "$RUN_ROOT/plan"

skipped() { case " $SKIP " in *" $1 "*) return 0 ;; *) return 1 ;; esac; }
step() {
    local name="$1"
    shift
    if skipped "$name"; then echo "=== [$name] skipped ==="; return 0; fi
    echo "=== [$name] $(date -u +%H:%M:%S) ==="
    "$@"
    echo "=== [$name] done $(date -u +%H:%M:%S) ==="
}

cd "$PROJECT_ROOT"

# 1. Call 1 -- routing universe가 바뀌었으므로 필수다. 건너뛰면 존재하지 않던 죄로 라우팅된
#    seed 위에 새 rulebase를 얹게 된다.
CALL1="$RUN_ROOT/call1/router_output.jsonl"
step call1 "$CLIENT_PYTHON" "$PROJECT_ROOT/scripts/run_v2_call1_pilot.py" \
    --base-url "$BASE_URL" --model "$SERVED_MODEL" --api-key "$API_KEY" \
    --inventory "$PROJECT_ROOT/data/inventory/kcl_criminal_v1_draft.jsonl" \
    --case-list "$PROJECT_ROOT/data/eval/kcl_substantive_case_ids.txt" \
    --out "$CALL1" \
    --gold-parquet "$GOLD_PARQUET" \
    --model-snapshot "$MODEL_SNAPSHOT" \
    --model-revision "$(basename "$MODEL_SNAPSHOT")" \
    --prompt-approved

# 2. Call 1.5 -- binding 계약에 사실 3개가 늘었다. `--occurrences`는 lineage 참조일 뿐
#    production binding universe를 제한하지 않는다.
CALL15="$RUN_ROOT/call15/issue_binding.jsonl"
step call15 "$CLIENT_PYTHON" "$PROJECT_ROOT/scripts/run_v2_call15_issue_binding.py" \
    --base-url "$BASE_URL" --model "$SERVED_MODEL" --api-key "$API_KEY" \
    --call1-artifact "$CALL1" \
    --occurrences "$PROJECT_ROOT/data/v2/gold_occurrences.jsonl" \
    --out "$CALL15" \
    --max-tokens "${IDPR_CALL15_MAX_TOKENS:-4096}" \
    --prompt-approved

# 3. planner -- 결정론적. 여기서 linked_offender_dependencies와 intended_object_divergences가
#    plan에 실린다.
PLAN="$RUN_ROOT/plan/evaluation_instance_plan.jsonl"
step plan "$CLIENT_PYTHON" "$PROJECT_ROOT/scripts/run_v2_evaluation_instance_planner.py" \
    --call1-artifact "$CALL1" \
    --call1-manifest "$RUN_ROOT/call1/router_output.manifest.json" \
    --call15-artifact "$CALL15" \
    --out "$PLAN" \
    --manifest-out "$RUN_ROOT/plan/evaluation_instance_plan.manifest.json"

echo "=== upstream done ==="
echo "CALL1=$CALL1"
echo "CALL15=$CALL15"
echo "PLAN=$PLAN"
