#!/bin/bash
#SBATCH --job-name=acal_retry_vllm
#SBATCH --output=logs/acal_retry_vllm_%j.log
#SBATCH --error=logs/acal_retry_vllm_%j.err
#SBATCH --time=6:00:00
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:PRO6000:1
#SBATCH --mem=32G

set -euo pipefail

echo "=================================================================="
echo "🚀 Retrying ACAL only (fact_pattern key-mismatch fix)"
echo "Date: $(date -u)"
echo "Host: $(hostname)"
echo "CUDA_VISIBLE_DEVICES: ${CUDA_VISIBLE_DEVICES:-N/A}"
echo "=================================================================="

source "${IDPR_PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}/scripts/slurm/_env.sh"
export TOKENIZERS_PARALLELISM=false
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export VLLM_USE_FLASHINFER_SAMPLER=0
export JE_ARROW_MALLOC_CONF="${JE_ARROW_MALLOC_CONF:-background_thread:false}"
export TORCH_CUDA_ARCH_LIST="12.0"

cd "$PROJECT_ROOT"
mkdir -p logs experiments/results

export PYTHONPATH="${PROJECT_ROOT}/src:${PYTHONPATH:-}"

PORT=$("$CLIENT_PYTHON" -c \
    'import socket; s=socket.socket(); s.bind(("127.0.0.1", 0)); print(s.getsockname()[1]); s.close()')
unset CUDA_HOME CUDA_PATH FLASHINFER_CUDA_ARCH_LIST FLASHINFER_WORKSPACE_BASE
VLLM_PID=""

export VLLM_PORT="${PORT}"

cleanup() {
    if [ -n "$VLLM_PID" ]; then
        echo "[cleanup] stopping vLLM pid=$VLLM_PID"
        kill "$VLLM_PID" 2>/dev/null || true
        wait "$VLLM_PID" 2>/dev/null || true
    fi
}
trap cleanup EXIT

echo "starting job-local vLLM Server on port $PORT..."
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
    > "${PROJECT_ROOT}/logs/vllm_acal_retry_server_${SLURM_JOB_ID}.log" 2>&1 &

VLLM_PID=$!

echo "Waiting for vLLM server to become ready at http://127.0.0.1:${PORT}/v1/models..."
READY=0
for i in $(seq 1 600); do
    if "$CLIENT_PYTHON" -c \
        "import json,urllib.request; r=urllib.request.Request('http://127.0.0.1:${PORT}/v1/models',headers={'Authorization':'Bearer ${LOCAL_API_KEY}'}); d=json.load(urllib.request.urlopen(r,timeout=5)); assert any(m['id']=='${SERVED_MODEL}' for m in d['data'])" \
        2>/dev/null; then
        READY=1
        echo "✅ vLLM Server is READY after $((i*5)) seconds!"
        break
    fi
    sleep 5
done

if [ "$READY" != 1 ]; then
    echo "❌ Error: vLLM Server failed to start."
    exit 1
fi

echo "▶ Running acal (fact_pattern key-mismatch fix)..."
$PYTHON_BIN scripts/run_baselines_experiment.py \
    --baseline acal \
    --vllm-url "http://127.0.0.1:${PORT}" \
    --vllm-model "${SERVED_MODEL}"

echo "ACAL retry completed successfully!"
