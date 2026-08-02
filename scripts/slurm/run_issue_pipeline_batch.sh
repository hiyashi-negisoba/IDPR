#!/bin/bash
#SBATCH --job-name=idpr_nsn
#SBATCH --output=logs/idpr_nsn_%j.out
#SBATCH --error=logs/idpr_nsn_%j.err
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:PRO6000:1
#SBATCH --mem=32G

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="${IDPR_PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$(cd "$SCRIPT_DIR/../.." && pwd)}}"
CLIENT_PYTHON="${IDPR_PYTHON:-python}"
VLLM_BIN="${IDPR_VLLM_BIN:-vllm}"
MODEL_SOURCE="${IDPR_MODEL_SOURCE:-google/gemma-4-26B-A4B-it}"
SERVED_MODEL="${IDPR_SERVED_MODEL:-google/gemma-4-26B-A4B-it}"
LOCAL_API_KEY="${IDPR_API_KEY:-local-idpr}"
RUN_DIR="${IDPR_RUN_DIR:-$PROJECT_ROOT/experiments/results/idpr_nsn}"
OUTPUT="${IDPR_OUTPUT:-$PROJECT_ROOT/experiments/results/idpr_nsn_outputs.jsonl}"
SERVER_DIR="${IDPR_SERVER_DIR:-$PROJECT_ROOT/.cache/issue_pipeline_server/${SLURM_JOB_ID}}"

export TOKENIZERS_PARALLELISM=false
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export VLLM_USE_FLASHINFER_SAMPLER=0
export JE_ARROW_MALLOC_CONF="${JE_ARROW_MALLOC_CONF:-background_thread:false}"
export TORCH_CUDA_ARCH_LIST="${TORCH_CUDA_ARCH_LIST:-12.0}"
export PYTHONPATH="$PROJECT_ROOT/src${PYTHONPATH:+:$PYTHONPATH}"

cd "$PROJECT_ROOT"
mkdir -p "$SERVER_DIR" "$RUN_DIR" logs

PORT=$(
    "$CLIENT_PYTHON" -c \
        'import socket; s=socket.socket(); s.bind(("127.0.0.1", 0)); print(s.getsockname()[1]); s.close()'
)
VLLM_PID=""
cleanup() {
    if [ -n "$VLLM_PID" ]; then
        kill "$VLLM_PID" 2>/dev/null || true
        wait "$VLLM_PID" 2>/dev/null || true
        VLLM_PID=""
    fi
}
trap cleanup EXIT

echo "=== IDPR NSN batch start: $(date) ==="
echo "job=$SLURM_JOB_ID host=$(hostname) model=$MODEL_SOURCE"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader

VLLM_LOG="$SERVER_DIR/vllm.log"
"$VLLM_BIN" serve "$MODEL_SOURCE" \
    --served-model-name "$SERVED_MODEL" \
    --host 127.0.0.1 \
    --port "$PORT" \
    --api-key "$LOCAL_API_KEY" \
    --tensor-parallel-size 1 \
    --max-model-len 65536 \
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
    if ! kill -0 "$VLLM_PID" 2>/dev/null; then
        echo "vLLM exited before readiness" >&2
        tail -n 100 "$VLLM_LOG" >&2
        exit 1
    fi
    sleep 10
done
if [ "$READY" != 1 ]; then
    echo "vLLM did not become ready within 30 minutes" >&2
    exit 1
fi

EXTRA_ARGS=()
if [ -n "${IDPR_LIMIT:-}" ]; then
    EXTRA_ARGS+=(--limit "$IDPR_LIMIT")
fi
if [ "${IDPR_OVERWRITE:-0}" = 1 ]; then
    EXTRA_ARGS+=(--overwrite)
fi
if [ "${IDPR_NO_CACHE:-0}" = 1 ]; then
    EXTRA_ARGS+=(--no-cache)
fi

"$CLIENT_PYTHON" scripts/run_issue_pipeline_batch.py \
    --base-url "http://127.0.0.1:${PORT}" \
    --model "$SERVED_MODEL" \
    --api-key "$LOCAL_API_KEY" \
    --run-dir "$RUN_DIR" \
    --out "$OUTPUT" \
    --call2-max-tokens "${IDPR_CALL2_MAX_TOKENS:-12288}" \
    --call3-max-tokens "${IDPR_CALL3_MAX_TOKENS:-16384}" \
    "${EXTRA_ARGS[@]}"

cleanup
echo "output=$OUTPUT"
echo "=== IDPR NSN batch end: $(date) ==="
