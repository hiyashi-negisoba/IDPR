#!/bin/bash

# Re-run Call 2 for only the cases carrying a canonical GroundFact conflict, under the
# occurrence-level canonicalization of d910532.  The point is not to refresh these cases --
# it is to verify live that each canonical GroundFact is now asked once and projected to
# every consuming offense instance with one truth.
#
# Run only as a CPU job step inside the existing vLLM service allocation:
#   IDPR_STEP8_SERVICE_JOB_ID=222907 srun --jobid=222907 --ntasks=1 --cpus-per-task=1 /bin/bash \
#     scripts/slurm/run_v2_call2_ground_fact_rebase.sh --execution-approved

set -euo pipefail

if [ "${1:-}" != "--execution-approved" ] || [ "$#" -ne 1 ]; then
    echo "usage: $0 --execution-approved" >&2
    exit 2
fi

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CLIENT_PYTHON="${IDPR_STEP8_CLIENT_PYTHON:-/data5/jaehoonjeong/miniconda3/bin/python}"
SERVICE_JOB_ID="${IDPR_STEP8_SERVICE_JOB_ID:-222907}"
SERVICE_ROOT="${IDPR_STEP8_V0_SERVICE_ROOT:-/data5/jaehoonjeong/IDPR-step8-v0-host/experiments/v2_call1_v0_service_${SERVICE_JOB_ID}}"
CALL1_ARTIFACT="$PROJECT_ROOT/experiments/v2_restart_rebuild/call1/router_output.jsonl"
PLAN_ARTIFACT="${IDPR_STEP8_PLAN_ARTIFACT:?plan artifact required}"
SERVED_MODEL="idpr-gemma-4-26b-a4b"
RUN_ROOT="${IDPR_STEP8_CALL2_RUN_ROOT:?run root required}"
ARTIFACT="$RUN_ROOT/grounding_output.jsonl"

test -x "$CLIENT_PYTHON"
test -s "$CALL1_ARTIFACT"
test -s "$PLAN_ARTIFACT"
test -n "${IDPR_STEP8_CASE_IDS:?case ids required}"

PORT="$("$CLIENT_PYTHON" -c "
import json
state=json.load(open('$SERVICE_ROOT/state.json'))
assert state['status']=='READY', state['status']
assert state['job_id']=='$SERVICE_JOB_ID', state['job_id']
assert state['served_model']=='$SERVED_MODEL', state['served_model']
print(int(state['port']))
")"
STATE_HOST="$($CLIENT_PYTHON -c "import json; print(json.load(open('$SERVICE_ROOT/state.json'))['host'])")"
if [ "$(hostname -s)" != "$STATE_HOST" ]; then
    echo "client must run on service host $STATE_HOST; got $(hostname -s)" >&2
    exit 2
fi

mkdir -p "$RUN_ROOT"
export PYTHONPATH="$PROJECT_ROOT/src${PYTHONPATH:+:$PYTHONPATH}"

CASE_ARGS=()
for case_id in $IDPR_STEP8_CASE_IDS; do
    CASE_ARGS+=(--case-id "$case_id")
done

echo "=== Call 2 canonical GroundFact rebase via service ${SERVICE_JOB_ID} ==="
echo "host=$(hostname -s) port=$PORT cases=$IDPR_STEP8_CASE_IDS"

"$CLIENT_PYTHON" "$PROJECT_ROOT/scripts/run_v2_call2_pilot.py" \
    --base-url "http://127.0.0.1:${PORT}" \
    --model "$SERVED_MODEL" \
    --api-key "${IDPR_STEP8_API_KEY:-local-idpr}" \
    --call1-artifact "$CALL1_ARTIFACT" \
    --gold-occurrences "$PROJECT_ROOT/data/v2/gold_occurrences.jsonl" \
    --gold-article263-pairs "$PROJECT_ROOT/data/v2/gold_article263_pairs.jsonl" \
    --plan-artifact "$PLAN_ARTIFACT" \
    --out "$ARTIFACT" \
    "${CASE_ARGS[@]}" \
    --planner-occurrence-evidence \
    --prompt-approved

echo "artifact=$ARTIFACT"
