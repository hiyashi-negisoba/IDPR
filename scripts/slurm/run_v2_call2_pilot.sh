#!/bin/bash

# Run only as a CPU job step inside existing vLLM allocation 221593:
#   srun --jobid=221593 --ntasks=1 --cpus-per-task=1 /bin/bash \
#     /home/jaehoonjeong/data/IDPR/scripts/slurm/run_v2_call2_pilot.sh \
#     --execution-approved
#
# This script never starts vLLM or requests a GPU.  The service is loopback-only
# on n05, so it must not be invoked from a login node or a fresh Slurm allocation.

set -euo pipefail

if [ "${1:-}" != "--execution-approved" ] || [ "$#" -ne 1 ]; then
    echo "usage: $0 --execution-approved" >&2
    exit 2
fi

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CLIENT_PYTHON="${IDPR_STEP8_CLIENT_PYTHON:-/data5/jaehoonjeong/miniconda3/bin/python}"
SERVICE_ROOT="${IDPR_STEP8_V0_SERVICE_ROOT:-/data5/jaehoonjeong/IDPR-step8-v0-host/experiments/v2_call1_v0_service_221593}"
CALL1_ARTIFACT="${IDPR_STEP8_CALL1_ARTIFACT:-$PROJECT_ROOT/experiments/v2_restart_rebuild/call1/router_output.jsonl}"
GOLD_OCCURRENCES="$PROJECT_ROOT/data/v2/gold_occurrences.jsonl"
GOLD_ARTICLE263_PAIRS="$PROJECT_ROOT/data/v2/gold_article263_pairs.jsonl"
PLAN_ARTIFACT="$PROJECT_ROOT/experiments/v2_restart_rebuild/evaluation_instance_plan.jsonl"
SERVED_MODEL="idpr-gemma-4-26b-a4b"
RUN_ROOT="${IDPR_STEP8_CALL2_RUN_ROOT:-$PROJECT_ROOT/experiments/v2_restart_rebuild/call2_full}"
ARTIFACT="$RUN_ROOT/grounding_output.jsonl"
AUDIT="$RUN_ROOT/grounding_output.audit.json"

test -x "$CLIENT_PYTHON"
test -s "$CALL1_ARTIFACT"
test -s "$GOLD_OCCURRENCES"
test -s "$GOLD_ARTICLE263_PAIRS"
test -s "$PLAN_ARTIFACT"

PORT="$("$CLIENT_PYTHON" - "$SERVICE_ROOT/state.json" "$SERVED_MODEL" <<'PY'
import json
import sys
from pathlib import Path

state = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
if state.get("status") != "READY":
    raise SystemExit(f"service is not READY: {state.get('status')!r}")
if state.get("job_id") != "221593":
    raise SystemExit(f"expected service job 221593, got {state.get('job_id')!r}")
if state.get("host") != "n05":
    raise SystemExit(f"expected service host n05, got {state.get('host')!r}")
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

if [ "$(hostname -s)" != "n05" ]; then
    echo "Call 2 client must run inside service allocation on n05; got $(hostname -s)" >&2
    exit 2
fi

mkdir -p "$RUN_ROOT"
export PYTHONPATH="$PROJECT_ROOT/src${PYTHONPATH:+:$PYTHONPATH}"

echo "=== Step 8 Call 2 via existing service 221593 ==="
echo "host=$(hostname -s) port=$PORT artifact=$ARTIFACT"

SMOKE_ARGS=()
if [ -n "${IDPR_STEP8_SMOKE_TARGET_LIMIT:-}" ]; then
    SMOKE_ARGS=(--smoke-target-limit "$IDPR_STEP8_SMOKE_TARGET_LIMIT")
fi

"$CLIENT_PYTHON" "$PROJECT_ROOT/scripts/run_v2_call2_pilot.py" \
    --base-url "http://127.0.0.1:${PORT}" \
    --model "$SERVED_MODEL" \
    --api-key "${IDPR_STEP8_API_KEY:-local-idpr}" \
    --call1-artifact "$CALL1_ARTIFACT" \
    --gold-occurrences "$GOLD_OCCURRENCES" \
    --gold-article263-pairs "$GOLD_ARTICLE263_PAIRS" \
    --plan-artifact "$PLAN_ARTIFACT" \
    --out "$ARTIFACT" \
    "${SMOKE_ARGS[@]}" \
    --prompt-approved

"$CLIENT_PYTHON" "$PROJECT_ROOT/scripts/audit_v2_call2_pilot.py" \
    --artifact "$ARTIFACT" \
    --manifest "${ARTIFACT%.jsonl}.manifest.json" \
    --plan-artifact "$PLAN_ARTIFACT" \
    --out "$AUDIT"

echo "artifact=$ARTIFACT"
echo "manifest=${ARTIFACT%.jsonl}.manifest.json"
echo "audit=$AUDIT"
