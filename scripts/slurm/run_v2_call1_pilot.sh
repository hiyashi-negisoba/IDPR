#!/bin/bash
#SBATCH --job-name=idpr_v2_call1_pilot
#SBATCH --output=logs/idpr_v2_call1_pilot_%j.out
#SBATCH --error=logs/idpr_v2_call1_pilot_%j.err
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:PRO6000:1
#SBATCH --mem=32G

# Step 8 Call 1 only: the model selects ordered closed offense seeds, then the
# host validates them and runs Step 7 structural closure.  It intentionally does
# not run Call 2/3.  The runner records every case failure; this script always
# writes the calibration report before returning a failing job status.

set -euo pipefail

source "${IDPR_PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}/scripts/slurm/_env.sh"

CLIENT_PYTHON="${IDPR_STEP8_CLIENT_PYTHON:-/data5/jaehoonjeong/miniconda3/bin/python}"
VLLM_BIN="${IDPR_STEP8_VLLM_BIN:-/data5/jaehoonjeong/miniconda3/envs/inv_ass_env/bin/vllm}"
MODEL_SNAPSHOT="${IDPR_STEP8_MODEL_SNAPSHOT:-/data5/jaehoonjeong/.cache/huggingface/hub/models--google--gemma-4-26B-A4B-it/snapshots/01e5b3ee840d3a9e0b0b493c593e85398a30ef75}"
SERVED_MODEL="${IDPR_STEP8_SERVED_MODEL:-idpr-gemma-4-26b-a4b}"
LOCAL_API_KEY="${IDPR_STEP8_API_KEY:-local-idpr}"
GOLD_PARQUET="${IDPR_STEP8_GOLD_PARQUET:-/home/jaehoonjeong/data/sp_qwen/warehouse/lbox_kcl/kcl_essay/test.parquet}"
CASE_LIST="${IDPR_STEP8_CASE_LIST:-$PROJECT_ROOT/data/eval/kcl_substantive_case_ids.txt}"
INVENTORY="${IDPR_STEP8_INVENTORY:-$PROJECT_ROOT/data/inventory/kcl_criminal_v1_draft.jsonl}"
RUN_ROOT="${IDPR_STEP8_RUN_ROOT:-$PROJECT_ROOT/experiments/v2_call1_pilot_${SLURM_JOB_ID}}"
SERVER_DIR="$RUN_ROOT/server"
ARTIFACT="$RUN_ROOT/router_output.jsonl"
REPORT="$RUN_ROOT/router_output.report.json"

export TOKENIZERS_PARALLELISM=false
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export VLLM_USE_FLASHINFER_SAMPLER=0
export JE_ARROW_MALLOC_CONF="${JE_ARROW_MALLOC_CONF:-background_thread:false}"
export TORCH_CUDA_ARCH_LIST="${TORCH_CUDA_ARCH_LIST:-12.0}"
export PYTHONPATH="$PROJECT_ROOT/src${PYTHONPATH:+:$PYTHONPATH}"

cd "$PROJECT_ROOT"
mkdir -p logs "$RUN_ROOT" "$SERVER_DIR"
test -x "$CLIENT_PYTHON"
test -x "$VLLM_BIN"
test -d "$MODEL_SNAPSHOT"
test -s "$CASE_LIST"
test -s "$INVENTORY"
test -s "$GOLD_PARQUET"

TOTAL=$(grep -c '[^[:space:]]' "$CASE_LIST")
test "$TOTAL" -eq 26
MODEL_REVISION=$(basename "$MODEL_SNAPSHOT")
PORT=$("$CLIENT_PYTHON" -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1", 0)); print(s.getsockname()[1]); s.close()')
VLLM_PID=""

cleanup() {
    if [ -n "$VLLM_PID" ]; then
        kill "$VLLM_PID" 2>/dev/null || true
        wait "$VLLM_PID" 2>/dev/null || true
        VLLM_PID=""
    fi
}
trap cleanup EXIT

echo "=== Step 8 Call 1 pilot start: $(date) ==="
echo "job=$SLURM_JOB_ID host=$(hostname) cases=$TOTAL model=$MODEL_SNAPSHOT"
echo "commit=$(git rev-parse HEAD 2>/dev/null || echo unavailable)"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader

unset CUDA_HOME CUDA_PATH FLASHINFER_CUDA_ARCH_LIST FLASHINFER_WORKSPACE_BASE
VLLM_LOG="$SERVER_DIR/vllm.log"
"$VLLM_BIN" serve "$MODEL_SNAPSHOT" \
    --served-model-name "$SERVED_MODEL" \
    --host 127.0.0.1 \
    --port "$PORT" \
    --api-key "$LOCAL_API_KEY" \
    --tensor-parallel-size 1 \
    --max-model-len 32768 \
    --max-num-seqs 1 \
    --gpu-memory-utilization 0.90 \
    --reasoning-parser gemma4 \
    --structured-outputs-config '{"backend":"guidance","disable_any_whitespace":true}' \
    > "$VLLM_LOG" 2>&1 &
VLLM_PID=$!

READY=0
for _ in $(seq 1 180); do
    if "$CLIENT_PYTHON" -c \
        "import json,urllib.request; r=urllib.request.Request('http://127.0.0.1:${PORT}/v1/models',headers={'Authorization':'Bearer ${LOCAL_API_KEY}'}); d=json.load(urllib.request.urlopen(r,timeout=5)); assert any(m['id']=='${SERVED_MODEL}' for m in d['data'])" \
        2>/dev/null; then
        READY=1
        break
    fi
    if ! kill -0 "$VLLM_PID"; then
        echo "vLLM exited before readiness" >&2
        tail -n 120 "$VLLM_LOG" >&2
        exit 1
    fi
    sleep 10
done
if [ "$READY" != 1 ]; then
    echo "vLLM did not become ready within 30 minutes" >&2
    exit 1
fi

"$CLIENT_PYTHON" scripts/run_v2_call1_pilot.py \
    --base-url "http://127.0.0.1:${PORT}" \
    --model "$SERVED_MODEL" \
    --api-key "$LOCAL_API_KEY" \
    --inventory "$INVENTORY" \
    --case-list "$CASE_LIST" \
    --out "$ARTIFACT" \
    --gold-parquet "$GOLD_PARQUET" \
    --model-snapshot "$MODEL_SNAPSHOT" \
    --model-revision "$MODEL_REVISION" \
    --vllm-max-model-len 32768 \
    --vllm-max-num-seqs 1 \
    --vllm-gpu-memory-utilization 0.90 \
    --vllm-reasoning-parser gemma4 \
    --vllm-structured-outputs-config '{"backend":"guidance","disable_any_whitespace":true}' \
    --prompt-approved

cleanup

"$CLIENT_PYTHON" scripts/report_v2_call1_pilot.py \
    --artifact "$ARTIFACT" \
    --out "$REPORT" \
    --inventory "$INVENTORY" \
    --parquet "$GOLD_PARQUET"

echo "artifact=$ARTIFACT"
echo "manifest=${ARTIFACT%.jsonl}.manifest.json"
echo "report=$REPORT"
if ! "$CLIENT_PYTHON" -c \
    "import json,sys; report=json.load(open('$REPORT', encoding='utf-8')); print('run_status=' + report['run_status']); sys.exit(0 if report['calibration_valid'] else 1)"; then
    echo "pilot artifacts are complete but calibration is invalid" >&2
    exit 1
fi
echo "=== Step 8 Call 1 pilot end: $(date) ==="
