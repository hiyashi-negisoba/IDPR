#!/bin/bash

# Re-run all 26 Call 1 routes against the existing job 221593 service.

set -euo pipefail

if [ "${1:-}" != "--execution-approved" ] || [ "$#" -ne 1 ]; then
    echo "usage: $0 --execution-approved" >&2
    exit 2
fi

PROJECT_ROOT="/home/jaehoonjeong/data/IDPR"
SERVICE_ROOT="/data5/jaehoonjeong/IDPR-step8-v0-host/experiments/v2_call1_v0_service_221593"
STATE="$SERVICE_ROOT/state.json"
PYTHON="$PROJECT_ROOT/.venv/bin/python"
MODEL_SNAPSHOT="/data5/jaehoonjeong/.cache/huggingface/hub/models--google--gemma-4-26B-A4B-it/snapshots/01e5b3ee840d3a9e0b0b493c593e85398a30ef75"
SERVED_MODEL="idpr-gemma-4-26b-a4b"
RUN_ROOT="$PROJECT_ROOT/experiments/v2_restart_rebuild/call1"
ARTIFACT="$RUN_ROOT/router_output.jsonl"
GOLD_PARQUET="/home/jaehoonjeong/data/sp_qwen/warehouse/lbox_kcl/kcl_essay/test.parquet"

if [ "$(hostname -s)" != "n05" ]; then
    echo "Call 1 rebuild must run inside job 221593 on n05" >&2
    exit 2
fi
PORT="$($PYTHON -c 'import json,sys; print(json.load(open(sys.argv[1]))["port"])' "$STATE")"
mkdir -p "$RUN_ROOT"
export PYTHONPATH="$PROJECT_ROOT/src"

cd "$PROJECT_ROOT"
"$PYTHON" scripts/run_v2_call1_pilot.py \
    --base-url "http://127.0.0.1:$PORT" \
    --model "$SERVED_MODEL" \
    --inventory data/inventory/kcl_criminal_v1_draft.jsonl \
    --case-list data/eval/kcl_substantive_case_ids.txt \
    --out "$ARTIFACT" \
    --gold-parquet "$GOLD_PARQUET" \
    --model-snapshot "$MODEL_SNAPSHOT" \
    --model-revision "$(basename "$MODEL_SNAPSHOT")" \
    --prompt-approved

"$PYTHON" scripts/report_v2_call1_pilot.py \
    --artifact "$ARTIFACT" \
    --out "$RUN_ROOT/router_output.report.json"
