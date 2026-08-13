#!/bin/bash

# Run only as a CPU job step inside an existing vLLM service allocation:
#   IDPR_STEP8_SERVICE_JOB_ID=<job> srun --jobid=<job> --ntasks=1 --cpus-per-task=1 /bin/bash \
#     /data5/jaehoonjeong/IDPR/scripts/slurm/run_v2_call15d_doctrine_cues.sh \
#     --execution-approved
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
CALL15_ARTIFACT="${IDPR_CALL15_ARTIFACT:-$PROJECT_ROOT/experiments/v2_call15_directscope_26_causal/issue_bindings.jsonl}"
CUES="${IDPR_DOCTRINE_CUES:-$PROJECT_ROOT/data/v2/doctrine_raising_cues.yaml}"
SERVED_MODEL="idpr-gemma-4-26b-a4b"
RUN_ROOT="${IDPR_CALL15D_RUN_ROOT:-$PROJECT_ROOT/experiments/v2_call15_directscope_26_causal/call15d_v1}"
ARTIFACT="$RUN_ROOT/doctrine_cues.jsonl"

test -x "$CLIENT_PYTHON"
test -s "$CALL15_ARTIFACT"
test -s "$CUES"

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
try:
    port = int(state.get("port"))
except (TypeError, ValueError) as error:
    raise SystemExit(f"invalid service port: {state.get('port')!r}") from error
if not 1 <= port <= 65535:
    raise SystemExit(f"invalid service port: {port!r}")
print(port)
PY
)"

STATE_HOST="$($CLIENT_PYTHON -c "import json; print(json.load(open('$SERVICE_ROOT/state.json'))['host'])")"
if [ "$(hostname -s)" != "$STATE_HOST" ]; then
    echo "Call 1.5-D client must run on service host $STATE_HOST; got $(hostname -s)" >&2
    exit 2
fi

mkdir -p "$RUN_ROOT"
export PYTHONPATH="$PROJECT_ROOT/src${PYTHONPATH:+:$PYTHONPATH}"

echo "=== Call 1.5-D via existing service ${SERVICE_JOB_ID} ==="
echo "host=$(hostname -s) port=$PORT artifact=$ARTIFACT"

"$CLIENT_PYTHON" "$PROJECT_ROOT/scripts/run_v2_call15_doctrine_cues.py" \
    --base-url "http://127.0.0.1:${PORT}" \
    --model "$SERVED_MODEL" \
    --api-key "${IDPR_STEP8_API_KEY:-local-idpr}" \
    --call15-artifact "$CALL15_ARTIFACT" \
    --cues "$CUES" \
    --out "$ARTIFACT" \
    --prompt-approved

echo "artifact=$ARTIFACT"
echo "manifest=${ARTIFACT%.jsonl}.manifest.json"
