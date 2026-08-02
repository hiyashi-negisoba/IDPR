#!/bin/bash
#SBATCH --job-name=idpr_irac_matrix
#SBATCH --output=logs/idpr_irac_matrix_%j.out
#SBATCH --error=logs/idpr_irac_matrix_%j.err
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:PRO6000:1
#SBATCH --mem=32G

set -euo pipefail

source "${IDPR_PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}/scripts/slurm/_env.sh"
RUN_DIR="${IDPR_RUN_DIR:-$PROJECT_ROOT/.cache/e2e/fraud_irac_matrix/${SLURM_JOB_ID}}"
REPORT_PATH="${IDPR_REPORT_PATH:-$PROJECT_ROOT/data/e2e/fraud/irac_matrix/fraud_irac_matrix_report.json}"
CASE_PATH="${IDPR_CASE_PATH:-$PROJECT_ROOT/data/e2e/fraud/kcl_r14_p1_q2_case.json}"
CASE_ARGS=(--case-path "$CASE_PATH")
if [ -n "${IDPR_CASE_ID:-}" ]; then
    CASE_ARGS+=(--case-id "$IDPR_CASE_ID")
fi
METHOD_ARGS=()
if [ -n "${IDPR_METHODS:-}" ]; then
    read -r -a SELECTED_METHODS <<< "$IDPR_METHODS"
    METHOD_ARGS=(--methods "${SELECTED_METHODS[@]}")
fi
SAMPLING_ARGS=()
if [ -n "${IDPR_TEMPERATURE:-}" ]; then
    SAMPLING_ARGS+=(--temperature "$IDPR_TEMPERATURE")
fi
if [ -n "${IDPR_TOP_P:-}" ]; then
    SAMPLING_ARGS+=(--top-p "$IDPR_TOP_P")
fi
if [ -n "${IDPR_TOP_K:-}" ]; then
    SAMPLING_ARGS+=(--top-k "$IDPR_TOP_K")
fi

export TOKENIZERS_PARALLELISM=false
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export VLLM_USE_FLASHINFER_SAMPLER=0
export JE_ARROW_MALLOC_CONF="${JE_ARROW_MALLOC_CONF:-background_thread:false}"
export TORCH_CUDA_ARCH_LIST="12.0"

cd "$PROJECT_ROOT"
mkdir -p "$RUN_DIR" logs data/e2e/fraud/irac_matrix

echo "=== IDPR IRAC matrix start: $(date) ==="
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
        --no-enable-prefix-caching \
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

run_case() {
    local case_run_dir="$1"
    local case_report_path="$2"
    shift 2
    "$CLIENT_PYTHON" scripts/run_fraud_irac_matrix.py \
        --base-url "http://127.0.0.1:${PORT}" \
        --model "$SERVED_MODEL" \
        --api-key "$LOCAL_API_KEY" \
        "$@" \
        --run-dir "$case_run_dir" \
        --report-path "$case_report_path" \
        "${METHOD_ARGS[@]}" \
        "${SAMPLING_ARGS[@]}"
}

if [ -n "${IDPR_CASE_IDS:-}" ]; then
    IFS=':' read -r -a SELECTED_CASE_IDS <<< "$IDPR_CASE_IDS"
    REPORT_ROOT="${IDPR_REPORT_ROOT:-$PROJECT_ROOT/data/e2e/fraud/case_batch/${SLURM_JOB_ID}}"
    for SELECTED_CASE_ID in "${SELECTED_CASE_IDS[@]}"; do
        if [ -z "$SELECTED_CASE_ID" ]; then
            echo "IDPR_CASE_IDS contains an empty case ID" >&2
            exit 1
        fi
        echo "=== case start: $SELECTED_CASE_ID ==="
        run_case \
            "$RUN_DIR/$SELECTED_CASE_ID" \
            "$REPORT_ROOT/$SELECTED_CASE_ID/report.json" \
            --case-path "$CASE_PATH" \
            --case-id "$SELECTED_CASE_ID"
        echo "=== case end: $SELECTED_CASE_ID ==="
    done
    echo "reports=$REPORT_ROOT"
else
    run_case "$RUN_DIR" "$REPORT_PATH" "${CASE_ARGS[@]}"
    echo "report=$REPORT_PATH"
fi

echo "artifacts=$RUN_DIR"
echo "=== IDPR IRAC matrix end: $(date) ==="
