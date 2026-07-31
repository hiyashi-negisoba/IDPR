#!/bin/bash
#SBATCH --job-name=idpr_retrieval_l0
#SBATCH --output=logs/idpr_retrieval_l0_%j.out
#SBATCH --error=logs/idpr_retrieval_l0_%j.err
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:PRO6000:1
#SBATCH --mem=32G

# Phase 2 gate: call 1 over all 61 questions, then L0 retrieval and issue recall.
#
# Two phases in one job because one GPU cannot hold gemma-4-26B and the retrieval models
# at once. vLLM is served, call 1 is run, vLLM is stopped, and only then are the encoder
# and reranker loaded. The fact graphs are written to disk in between, so the retrieval
# half can be re-run and re-measured without paying for the model again.
#
# Resource values are copied verbatim from run_fraud_neural_e2e.sh by standing rule.

set -euo pipefail

PROJECT_ROOT="/data5/jaehoonjeong/IDPR"
CLIENT_PYTHON="/data5/jaehoonjeong/miniconda3/bin/python"
VLLM_BIN="/data5/jaehoonjeong/miniconda3/envs/inv_ass_env/bin/vllm"
MODEL_SNAPSHOT="/data5/jaehoonjeong/.cache/huggingface/hub/models--google--gemma-4-26B-A4B-it/snapshots/01e5b3ee840d3a9e0b0b493c593e85398a30ef75"
SERVED_MODEL="idpr-gemma-4-26b-a4b"
LOCAL_API_KEY="local-idpr"
RUN_DIR="$PROJECT_ROOT/.cache/l0/${SLURM_JOB_ID}"
FACT_GRAPHS="$PROJECT_ROOT/data/eval/fact_graphs.jsonl"
REPORT="$PROJECT_ROOT/data/eval/retrieval_l0_recall_report.json"

# Phase 1 environment is byte-identical to run_fraud_neural_e2e.sh. The first run of this
# job segfaulted vLLM three times with a zero-byte log; the only deviations from the proven
# template were a missing JE_ARROW_MALLOC_CONF and a PYTHONPATH exported into the vLLM
# process. Both are restored/removed here rather than guessed at one at a time.
export HF_HOME="/data5/jaehoonjeong/.cache/huggingface"
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export TOKENIZERS_PARALLELISM=false
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export VLLM_USE_FLASHINFER_SAMPLER=0
export JE_ARROW_MALLOC_CONF="${JE_ARROW_MALLOC_CONF:-background_thread:false}"
export TORCH_CUDA_ARCH_LIST="12.0"

cd "$PROJECT_ROOT"
mkdir -p "$RUN_DIR" logs data/eval

echo "=== IDPR L0 gate start: $(date) ==="
echo "job=$SLURM_JOB_ID host=$(hostname)"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
# Preflight: a segfault before this line is an environment problem, after it is ours.
"/data5/jaehoonjeong/miniconda3/envs/inv_ass_env/bin/python" -c \
    "import torch,vllm; print('torch/cuda/vllm', torch.__version__, torch.version.cuda, vllm.__version__)"

# ---------------------------------------------------------------------------
# Phase 1 -- call 1 (fact graphs). vLLM only.
#
# SKIP_CALL1=1 reuses an existing data/eval/fact_graphs.jsonl. Use it when only the host
# side changed (admission rules, retrieval, scoring): the model output is already on disk
# and re-generating it would cost a vLLM load for a byte-identical result.
# ---------------------------------------------------------------------------
if [ "${SKIP_CALL1:-0}" = "1" ]; then
    echo "=== call 1 skipped: reusing $FACT_GRAPHS ==="
    test -s "$FACT_GRAPHS" || { echo "no fact graphs to reuse" >&2; exit 1; }
else
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
    [ "$READY" = 1 ] && break
    cleanup
    sleep 10
done
if [ "$READY" != 1 ]; then
    echo "vLLM failed to become ready after three attempts" >&2
    exit 1
fi

echo "=== call 1: fact graphs over the inventory ==="
export PYTHONPATH="$PROJECT_ROOT/src"
"$CLIENT_PYTHON" scripts/run_call1_fact_graphs.py \
    --base-url "http://127.0.0.1:${PORT}" \
    --model "$SERVED_MODEL" \
    --api-key "$LOCAL_API_KEY" \
    --out "$FACT_GRAPHS"

cleanup
echo "vLLM stopped; GPU released for the retrieval models"
sleep 15
fi

# ---------------------------------------------------------------------------
# Phase 2 -- retrieval and issue recall. Encoder + reranker only.
#
# HF_HUB_OFFLINE stays unset here on purpose: transformers 4.57.3 calls model_info()
# from _patch_mistral_regex unconditionally and dies offline even with a warm cache.
# ---------------------------------------------------------------------------
unset HF_HUB_OFFLINE TRANSFORMERS_OFFLINE
# Set here as well as in the call-1 branch: with SKIP_CALL1 that branch never runs.
export PYTHONPATH="$PROJECT_ROOT/src"
echo "=== L0 retrieval + issue recall ==="
"$CLIENT_PYTHON" scripts/run_retrieval_l0_report.py \
    --fact-graphs "$FACT_GRAPHS" \
    --out "$REPORT"

echo "fact_graphs=$FACT_GRAPHS"
echo "report=$REPORT"
echo "=== IDPR L0 gate end: $(date) ==="
