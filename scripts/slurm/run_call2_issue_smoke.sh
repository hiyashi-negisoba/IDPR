#!/bin/bash
#SBATCH --job-name=idpr_call2_issue
#SBATCH --output=logs/idpr_call2_issue_%j.out
#SBATCH --error=logs/idpr_call2_issue_%j.err
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:PRO6000:1
#SBATCH --mem=32G

set -euo pipefail

PROJECT_ROOT="/data5/jaehoonjeong/IDPR"
CLIENT_PYTHON="/data5/jaehoonjeong/miniconda3/bin/python"
VLLM_BIN="/data5/jaehoonjeong/miniconda3/envs/inv_ass_env/bin/vllm"
MODEL_SNAPSHOT="/data5/jaehoonjeong/.cache/huggingface/hub/models--google--gemma-4-26B-A4B-it/snapshots/01e5b3ee840d3a9e0b0b493c593e85398a30ef75"
SERVED_MODEL="idpr-gemma-4-26b-a4b"
LOCAL_API_KEY="local-idpr"
RUN_DIR="$PROJECT_ROOT/.cache/call2_issue_smoke/${SLURM_JOB_ID}"
OUT="$PROJECT_ROOT/data/eval/issue_status_smoke.json"
CALL3_OUT="$PROJECT_ROOT/data/eval/issue_answer_smoke.json"

export HF_HOME="/data5/jaehoonjeong/.cache/huggingface"
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export TOKENIZERS_PARALLELISM=false
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export VLLM_USE_FLASHINFER_SAMPLER=0
export JE_ARROW_MALLOC_CONF="${JE_ARROW_MALLOC_CONF:-background_thread:false}"
export TORCH_CUDA_ARCH_LIST="12.0"
export PYTHONPATH="$PROJECT_ROOT/src"

cd "$PROJECT_ROOT"
mkdir -p "$RUN_DIR" logs data/eval

echo "=== IDPR issue-first call 2 smoke start: $(date) ==="
echo "job=$SLURM_JOB_ID host=$(hostname)"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader

PORT=$("$CLIENT_PYTHON" -c \
    'import socket; s=socket.socket(); s.bind(("127.0.0.1", 0)); print(s.getsockname()[1]); s.close()')
unset CUDA_HOME CUDA_PATH FLASHINFER_CUDA_ARCH_LIST FLASHINFER_WORKSPACE_BASE
VLLM_PID=""

cleanup() {
    if [ -n "$VLLM_PID" ]; then
        echo "[cleanup] stopping vLLM pid=$VLLM_PID"
        kill "$VLLM_PID" 2>/dev/null || true
        wait "$VLLM_PID" 2>/dev/null || true
        VLLM_PID=""
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
        --max-model-len 65536 \
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
    [ "$READY" = 1 ] && break
    cleanup
    sleep 10
done
if [ "$READY" != 1 ]; then
    echo "vLLM failed to become ready after three attempts" >&2
    exit 1
fi

if [ "${CALL3_ONLY:-0}" != 1 ]; then
    "$CLIENT_PYTHON" scripts/run_call2_issue_smoke.py \
        --base-url "http://127.0.0.1:${PORT}" \
        --model "$SERVED_MODEL" \
        --api-key "$LOCAL_API_KEY" \
        --work-dir "$RUN_DIR" \
        --out "$OUT" \
        --no-cache
else
    echo "CALL3_ONLY=1: reusing $OUT"
    test -s "$OUT"
fi

"$CLIENT_PYTHON" scripts/run_call3_issue_smoke.py \
    --base-url "http://127.0.0.1:${PORT}" \
    --model "$SERVED_MODEL" \
    --api-key "$LOCAL_API_KEY" \
    --call2 "$OUT" \
    --work-dir "$RUN_DIR/call3" \
    --out "$CALL3_OUT"

cleanup
echo "result=$OUT"
echo "answer=$CALL3_OUT"
echo "=== IDPR issue-first call 2 smoke end: $(date) ==="
