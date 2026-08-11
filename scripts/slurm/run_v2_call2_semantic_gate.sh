#!/bin/bash

# Execute the mandatory real-model Call 2 semantic gate inside vLLM job 221593.

set -euo pipefail

if [ "${1:-}" != "--execution-approved" ] || [ "$#" -ne 1 ]; then
    echo "usage: $0 --execution-approved" >&2
    exit 2
fi

PROJECT_ROOT="/home/jaehoonjeong/data/IDPR"
SERVICE_ROOT="/data5/jaehoonjeong/IDPR-step8-v0-host/experiments/v2_call1_v0_service_221593"
STATE="$SERVICE_ROOT/state.json"
PYTHON="$PROJECT_ROOT/.venv/bin/python"
SERVED_MODEL="idpr-gemma-4-26b-a4b"
REPORT_ROOT="$PROJECT_ROOT/experiments/v2_restart_rebuild"

if [ "$(hostname -s)" != "n05" ]; then
    echo "semantic gate must run inside job 221593 on n05" >&2
    exit 2
fi

PORT="$($PYTHON -c 'import json,sys; print(json.load(open(sys.argv[1]))["port"])' "$STATE")"
mkdir -p "$REPORT_ROOT"

export IDPR_VLLM_BASE_URL="http://127.0.0.1:$PORT"
export IDPR_VLLM_MODEL="$SERVED_MODEL"
export PYTHONPATH="$PROJECT_ROOT/src"

cd "$PROJECT_ROOT"
"$PYTHON" -m pytest -q tests/live \
    --junitxml="$REPORT_ROOT/gemma_call2_semantic_gate.xml"
