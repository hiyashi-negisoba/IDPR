#!/bin/bash
#SBATCH --job-name=idpr_fraud_e2e
#SBATCH --output=logs/idpr_fraud_e2e_%j.out
#SBATCH --error=logs/idpr_fraud_e2e_%j.err
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:PRO6000:1
#SBATCH --mem=32G

set -euo pipefail

source "${IDPR_PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}/scripts/slurm/_env.sh"
RUN_DIR="$PROJECT_ROOT/.cache/e2e/fraud/${SLURM_JOB_ID}"
REPORT_PATH="$PROJECT_ROOT/data/e2e/fraud/fraud_neural_e2e_vllm_report.json"

export TOKENIZERS_PARALLELISM=false
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export VLLM_USE_FLASHINFER_SAMPLER=0
export JE_ARROW_MALLOC_CONF="${JE_ARROW_MALLOC_CONF:-background_thread:false}"
export TORCH_CUDA_ARCH_LIST="12.0"

cd "$PROJECT_ROOT"
mkdir -p "$RUN_DIR" logs data/e2e/fraud

echo "=== IDPR fraud neural E2E start: $(date) ==="
echo "job=$SLURM_JOB_ID host=$(hostname)"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
"$CLIENT_PYTHON" -c \
    "import torch; print('torch/cuda', torch.__version__, torch.version.cuda)"
test -x "$VLLM_BIN"
echo "vllm=$VLLM_BIN"

if [ -d "$MODEL_SNAPSHOT" ]; then
    "$CLIENT_PYTHON" scripts/check_gemma4_cache.py \
        --snapshot "$MODEL_SNAPSHOT" \
        --json-out "$RUN_DIR/model_cache_audit.json"
fi

PORT=$("$CLIENT_PYTHON" -c \
    'import socket; s=socket.socket(); s.bind(("127.0.0.1", 0)); print(s.getsockname()[1]); s.close()')
unset CUDA_HOME CUDA_PATH FLASHINFER_CUDA_ARCH_LIST FLASHINFER_WORKSPACE_BASE
VLLM_PID=""

cleanup() {
    if [ -n "$VLLM_PID" ]; then
        echo "[cleanup] stopping vLLM pid=$VLLM_PID"
        kill "$VLLM_PID" 2>/dev/null || true
        wait "$VLLM_PID" 2>/dev/null || true
    fi
}
trap cleanup EXIT

READY=0
for ATTEMPT in 1 2 3; do
    VLLM_LOG="$RUN_DIR/vllm_attempt_${ATTEMPT}.log"
    echo "starting vLLM attempt=$ATTEMPT log=$VLLM_LOG"
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
    for _ in $(seq 1 180); do
        if "$CLIENT_PYTHON" -c \
            "import json,urllib.request; r=urllib.request.Request('http://127.0.0.1:${PORT}/v1/models',headers={'Authorization':'Bearer ${LOCAL_API_KEY}'}); d=json.load(urllib.request.urlopen(r,timeout=5)); assert any(m['id']=='${SERVED_MODEL}' for m in d['data'])" \
            2>/dev/null; then
            READY=1
            break
        fi
        if ! kill -0 "$VLLM_PID" 2>/dev/null; then
            echo "vLLM attempt=$ATTEMPT exited before readiness" >&2
            wait "$VLLM_PID" 2>/dev/null || true
            VLLM_PID=""
            tail -n 80 "$VLLM_LOG" >&2
            break
        fi
        sleep 10
    done
    if [ "$READY" = 1 ]; then
        break
    fi
    if [ -n "$VLLM_PID" ]; then
        kill "$VLLM_PID" 2>/dev/null || true
        wait "$VLLM_PID" 2>/dev/null || true
        VLLM_PID=""
    fi
    sleep 10
done
if [ "$READY" != 1 ]; then
    echo "vLLM failed to become ready after three attempts" >&2
    exit 1
fi

# Gemma 4 model-card sampling, thinking disabled by decision: greedy
# baseline plus the recommended temperature=1.0, top_p=0.95, top_k=64.
# Thinking arms were dropped: greedy+thinking loops without terminating and
# thinking adds transcription risk without demonstrated benefit.
for CASE_NAME in "case_a" "case_c"; do
    case "$CASE_NAME" in
        "case_a") TEMP="0.0"; TOPP=""; TOPK=""; THINK="" ;;
        "case_c") TEMP="1.0"; TOPP="0.95"; TOPK="64"; THINK="" ;;
    esac

    CASE_RUN_DIR="$RUN_DIR/$CASE_NAME"
    CASE_REPORT="$PROJECT_ROOT/data/e2e/fraud/fraud_neural_e2e_vllm_report_${CASE_NAME}.json"
    mkdir -p "$CASE_RUN_DIR"

    echo "Running $CASE_NAME with temp=$TEMP top_p=${TOPP:-default} top_k=${TOPK:-default} $THINK"
    CMD=("$CLIENT_PYTHON" scripts/run_fraud_neural_e2e.py \
        --mode vllm \
        --base-url "http://127.0.0.1:${PORT}" \
        --model "$SERVED_MODEL" \
        --api-key "$LOCAL_API_KEY" \
        --run-dir "$CASE_RUN_DIR" \
        --report-path "$CASE_REPORT" \
        --temperature "$TEMP")

    if [ -n "$TOPP" ]; then
        CMD+=(--top-p "$TOPP" --top-k "$TOPK")
    fi
    if [ -n "$THINK" ]; then
        CMD+=("$THINK")
    fi

    "${CMD[@]}" || echo "[WARN] $CASE_NAME failed (exit $?), continuing..."
done

echo "report=$REPORT_PATH"
echo "artifacts=$RUN_DIR"
echo "=== IDPR fraud neural E2E end: $(date) ==="
