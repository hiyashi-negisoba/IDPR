#!/bin/bash
#SBATCH --job-name=idpr_l0_union
#SBATCH --output=logs/idpr_l0_union_%j.out
#SBATCH --error=logs/idpr_l0_union_%j.err
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:PRO6000:1
#SBATCH --mem=32G

# L0 end to end: article selection (call 1.5) then retrieval, unioned into the candidate
# set call 2 consumes.
#
# Two GPU phases in one job because one card cannot hold gemma-4-26B and the retrieval
# models at once. Each phase writes its artifact, so either half can be re-run alone --
# SKIP_SELECT=1 reuses an existing article_selection.jsonl.
#
# NO_RETRIEVAL=1 runs the model-selection-only fallback. It is the answer if the union
# turns out too slow to keep: selection alone measured 0.727 recall against the union's
# 0.927, at 8.1k call-2 tokens against 62.0k.
#
# Resource values are copied verbatim from run_retrieval_l0.sh by standing rule.

set -euo pipefail

source "${IDPR_PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}/scripts/slurm/_env.sh"
RUN_DIR="$PROJECT_ROOT/.cache/l0_union/${SLURM_JOB_ID}"
SELECTION="${IDPR_ARTICLE_SELECTION:-$PROJECT_ROOT/data/eval/article_selection.jsonl}"
CANDIDATES="${IDPR_L0_CANDIDATES:-$PROJECT_ROOT/data/eval/l0_candidates.jsonl}"
REPORT="${IDPR_L0_UNION_REPORT:-$PROJECT_ROOT/data/eval/l0_union_report.json}"

export TOKENIZERS_PARALLELISM=false
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export VLLM_USE_FLASHINFER_SAMPLER=0
export JE_ARROW_MALLOC_CONF="${JE_ARROW_MALLOC_CONF:-background_thread:false}"
export TORCH_CUDA_ARCH_LIST="12.0"

cd "$PROJECT_ROOT"
mkdir -p \
    "$RUN_DIR" \
    logs \
    "$(dirname "$SELECTION")" \
    "$(dirname "$CANDIDATES")" \
    "$(dirname "$REPORT")"

echo "=== IDPR L0 union start: $(date) ==="
echo "job=$SLURM_JOB_ID host=$(hostname)"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader

# ---------------------------------------------------------------------------
# Phase A -- call 1.5 (article selection). vLLM only.
# ---------------------------------------------------------------------------
if [ "${SKIP_SELECT:-0}" = "1" ]; then
    echo "=== phase A skipped: reusing $SELECTION ==="
    test -s "$SELECTION" || { echo "no selection to reuse" >&2; exit 1; }
else
echo "--- phase A start: $(date +%T) ---"
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

export PYTHONPATH="$PROJECT_ROOT/src"
STAGED_SELECTION="$RUN_DIR/article_selection.jsonl"
"$CLIENT_PYTHON" scripts/run_article_select.py \
    --base-url "http://127.0.0.1:${PORT}" \
    --model "$SERVED_MODEL" \
    --api-key "$LOCAL_API_KEY" \
    --out "$STAGED_SELECTION"
mv "$STAGED_SELECTION" "$SELECTION"

cleanup
echo "--- phase A end: $(date +%T) ---"
sleep 15
fi

# ---------------------------------------------------------------------------
# Phase B -- legacy retrieval union. Encoder + reranker only.
#
# This entry point is retained for reproducibility of Phase-2 measurements. The current
# pipeline retrieves before Call 1.5 and assembles ``reviewed_selection`` scope afterwards.
#
# HF_HUB_OFFLINE stays unset here on purpose: transformers 4.57.3 calls model_info()
# from _patch_mistral_regex unconditionally and dies offline even with a warm cache.
# ---------------------------------------------------------------------------
unset HF_HUB_OFFLINE TRANSFORMERS_OFFLINE
export PYTHONPATH="$PROJECT_ROOT/src"
echo "--- phase B start: $(date +%T) ---"
EXTRA_ARGS=(--routing-policy "${IDPR_ROUTING_POLICY:-legacy_union}")
if [ "${NO_RETRIEVAL:-0}" = "1" ]; then
    EXTRA_ARGS+=(--no-retrieval)
fi
if [ -n "${IDPR_RETRIEVAL_CANDIDATES:-}" ]; then
    EXTRA_ARGS+=(--retrieval-candidates "$IDPR_RETRIEVAL_CANDIDATES")
fi
STAGED_CANDIDATES="$RUN_DIR/l0_candidates.jsonl"
STAGED_REPORT="$RUN_DIR/l0_union_report.json"
"$CLIENT_PYTHON" scripts/run_l0_candidates.py \
    --selection "$SELECTION" \
    --out "$STAGED_CANDIDATES" \
    --report "$STAGED_REPORT" \
    --checks data/eval/diagnostic_checks.json \
    "${EXTRA_ARGS[@]}"
mv "$STAGED_CANDIDATES" "$CANDIDATES"
mv "$STAGED_REPORT" "$REPORT"
echo "--- phase B end: $(date +%T) ---"

echo "candidates=$CANDIDATES"
echo "report=$REPORT"
echo "=== IDPR L0 union end: $(date) ==="
