#!/bin/bash

# Run only as a CPU job step inside an existing vLLM service allocation:
#   IDPR_STEP8_SERVICE_JOB_ID=<job> srun --jobid=<job> --ntasks=1 --cpus-per-task=1 /bin/bash \
#     /data5/jaehoonjeong/IDPR/scripts/slurm/run_v2_call3.sh --execution-approved
#
# This script never starts vLLM or requests a GPU. The service is loopback-only,
# so it must run on the node assigned to that service allocation.

set -euo pipefail

if [ "${1:-}" != "--execution-approved" ] || [ "$#" -ne 1 ]; then
    echo "usage: $0 --execution-approved" >&2
    exit 2
fi

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CLIENT_PYTHON="${IDPR_STEP8_CLIENT_PYTHON:-/data5/jaehoonjeong/miniconda3/bin/python}"
SERVICE_JOB_ID="${IDPR_STEP8_SERVICE_JOB_ID:-222907}"
SERVICE_ROOT="${IDPR_STEP8_V0_SERVICE_ROOT:-/data5/jaehoonjeong/IDPR-step8-v0-host/experiments/v2_call1_v0_service_${SERVICE_JOB_ID}}"
SERVED_MODEL="idpr-gemma-4-26b-a4b"
PLANS="${IDPR_ANSWER_PLANS:-$PROJECT_ROOT/experiments/v2_call15_directscope_26_causal/answer_plan_v1/answer_plans.jsonl}"
RUN_ROOT="${IDPR_CALL3_RUN_ROOT:-$PROJECT_ROOT/experiments/v2_call15_directscope_26_causal/call3_dev_v1}"
CASE_ID_FILE="${IDPR_CALL3_CASE_ID_FILE:-}"

test -x "$CLIENT_PYTHON"
test -s "$PLANS"

PORT="$("$CLIENT_PYTHON" -c "
import json,sys
s=json.load(open('$SERVICE_ROOT/state.json'))
assert s.get('status')=='READY', s.get('status')
assert s.get('job_id')=='$SERVICE_JOB_ID', s.get('job_id')
assert s.get('served_model')=='$SERVED_MODEL', s.get('served_model')
print(int(s['port']))
")"

STATE_HOST="$($CLIENT_PYTHON -c "import json; print(json.load(open('$SERVICE_ROOT/state.json'))['host'])")"
if [ "$(hostname -s)" != "$STATE_HOST" ]; then
    echo "call3 client must run on service host $STATE_HOST; got $(hostname -s)" >&2
    exit 2
fi

mkdir -p "$RUN_ROOT"
export PYTHONPATH="$PROJECT_ROOT/src${PYTHONPATH:+:$PYTHONPATH}"

echo "=== Call 3 IRAC answers via existing service ${SERVICE_JOB_ID} ==="
echo "host=$(hostname -s) port=$PORT out=$RUN_ROOT"

ARGS=(--answer-plans "$PLANS" --out "$RUN_ROOT" \
      --base-url "http://127.0.0.1:${PORT}" --model "$SERVED_MODEL")
if [ -n "$CASE_ID_FILE" ]; then
    ARGS+=(--case-id-file "$CASE_ID_FILE")
fi

"$CLIENT_PYTHON" "$PROJECT_ROOT/scripts/run_v2_call3.py" "${ARGS[@]}"
