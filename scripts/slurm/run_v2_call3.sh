#!/bin/bash

# Run only as a CPU job step inside an existing vLLM service allocation.  The answer-plan
# and output paths are intentionally required so an action-realization run cannot silently
# regenerate answers from the frozen binding/episode plan:
#   IDPR_ANSWER_PLANS=... IDPR_CALL3_RUN_ROOT=... IDPR_STEP8_SERVICE_JOB_ID=<job> \
#   srun --jobid=<job> --ntasks=1 --cpus-per-task=1 /bin/bash \
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
PLANS="${IDPR_ANSWER_PLANS:?IDPR_ANSWER_PLANS is required (fresh action-realization answer plans)}"
RUN_ROOT="${IDPR_CALL3_RUN_ROOT:?IDPR_CALL3_RUN_ROOT is required (fresh N or P Call 3 output directory)}"
CASE_ID_FILE="${IDPR_CALL3_CASE_ID_FILE:-}"
# Decoding is a condition variable, not a fixed property of the pipeline: a comparison
# across arms wants it identical and reproducible.  Left unset, run_v2_call3.py keeps its
# own defaults.
TEMPERATURE="${IDPR_CALL3_TEMPERATURE:-}"
MAX_TOKENS="${IDPR_CALL3_MAX_TOKENS:-}"

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
if [ -n "$TEMPERATURE" ]; then
    ARGS+=(--temperature "$TEMPERATURE")
fi
if [ -n "$MAX_TOKENS" ]; then
    ARGS+=(--max-tokens "$MAX_TOKENS")
fi

"$CLIENT_PYTHON" "$PROJECT_ROOT/scripts/run_v2_call3.py" "${ARGS[@]}"
