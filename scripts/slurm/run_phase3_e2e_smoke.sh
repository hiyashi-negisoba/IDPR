#!/bin/bash
#SBATCH --job-name=phase3_e2e_freeze
#SBATCH --output=logs/phase3_e2e_freeze_%j.out
#SBATCH --error=logs/phase3_e2e_freeze_%j.err
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:PRO6000:1
#SBATCH --mem=32G

# Phase-3 freeze gate over exactly the dedicated two-case smoke inventory.
#
# The GPU phases are serialized: Call 1/1.5 use vLLM, retrieval takes the released GPU,
# then Call 2/3 start a fresh long-context vLLM.  No prior model artifact is accepted as
# fallback and the downstream runner is forced to overwrite every case.

set -euo pipefail

source "${IDPR_PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}/scripts/slurm/_env.sh"

INVENTORY="$PROJECT_ROOT/data/smoke/phase3_e2e_inventory.jsonl"
RUBRIC="$PROJECT_ROOT/data/smoke/phase3_e2e_rubrics.json"
RUN_ROOT="${IDPR_FREEZE_ROOT:-$PROJECT_ROOT/experiments/results/phase3_e2e_freeze_v1}"
FACT_GRAPHS="$RUN_ROOT/fact_graphs.jsonl"
SELECTION="$RUN_ROOT/article_selection.jsonl"
CANDIDATES="$RUN_ROOT/l0_candidates.jsonl"
L0_REPORT="$RUN_ROOT/l0_report.json"
CASES="$RUN_ROOT/cases"
OUTPUT="$RUN_ROOT/idpr_nsn_outputs.jsonl"
SERVER_DIR="$RUN_ROOT/server"

CALL1_MAX_TOKENS="${IDPR_CALL1_MAX_TOKENS:-8192}"
CALL15_MAX_TOKENS="${IDPR_CALL15_MAX_TOKENS:-2048}"
TOP_K_ARTICLES="${IDPR_TOP_K_ARTICLES:-18}"
CALL2_MAX_TOKENS="${IDPR_CALL2_MAX_TOKENS:-12288}"
CALL3_MAX_TOKENS="${IDPR_CALL3_MAX_TOKENS:-16384}"

export TOKENIZERS_PARALLELISM=false
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export VLLM_USE_FLASHINFER_SAMPLER=0
export JE_ARROW_MALLOC_CONF="${JE_ARROW_MALLOC_CONF:-background_thread:false}"
export TORCH_CUDA_ARCH_LIST="${TORCH_CUDA_ARCH_LIST:-12.0}"

cd "$PROJECT_ROOT"
mkdir -p logs
if [ -e "$RUN_ROOT" ]; then
    echo "freeze output already exists; use a new IDPR_FREEZE_ROOT: $RUN_ROOT" >&2
    exit 1
fi
mkdir -p "$RUN_ROOT" "$CASES" "$SERVER_DIR"

echo "=== Phase-3 two-case E2E start: $(date) ==="
echo "job=$SLURM_JOB_ID host=$(hostname) model=$MODEL_SNAPSHOT"
echo "inventory=$INVENTORY"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
"$CLIENT_PYTHON" -c "import torch; print('torch/cuda', torch.__version__, torch.version.cuda)"
export PYTHONPATH="$PROJECT_ROOT/src${PYTHONPATH:+:$PYTHONPATH}"

VLLM_PID=""
PORT=""
cleanup() {
    if [ -n "$VLLM_PID" ]; then
        echo "[cleanup] stopping vLLM pid=$VLLM_PID"
        kill "$VLLM_PID" 2>/dev/null || true
        wait "$VLLM_PID" 2>/dev/null || true
        VLLM_PID=""
    fi
}
trap cleanup EXIT

start_vllm() {
    local max_model_len="$1"
    local phase="$2"
    PORT=$("$CLIENT_PYTHON" -c \
        'import socket; s=socket.socket(); s.bind(("127.0.0.1", 0)); print(s.getsockname()[1]); s.close()')
    unset CUDA_HOME CUDA_PATH FLASHINFER_CUDA_ARCH_LIST FLASHINFER_WORKSPACE_BASE
    local ready=0
    local attempt
    for attempt in 1 2 3; do
        local log="$SERVER_DIR/${phase}_attempt_${attempt}.log"
        echo "starting vLLM phase=$phase attempt=$attempt max_model_len=$max_model_len"
        "$VLLM_BIN" serve "$MODEL_SNAPSHOT" \
            --served-model-name "$SERVED_MODEL" \
            --host 127.0.0.1 \
            --port "$PORT" \
            --api-key "$LOCAL_API_KEY" \
            --tensor-parallel-size 1 \
            --max-model-len "$max_model_len" \
            --max-num-seqs 1 \
            --gpu-memory-utilization 0.90 \
            --reasoning-parser gemma4 \
            --structured-outputs-config '{"backend":"guidance","disable_any_whitespace":true}' \
            > "$log" 2>&1 &
        VLLM_PID=$!
        for _ in $(seq 1 180); do
            if "$CLIENT_PYTHON" -c \
                "import json,urllib.request; r=urllib.request.Request('http://127.0.0.1:${PORT}/v1/models',headers={'Authorization':'Bearer ${LOCAL_API_KEY}'}); d=json.load(urllib.request.urlopen(r,timeout=5)); assert any(m['id']=='${SERVED_MODEL}' for m in d['data'])" \
                2>/dev/null; then
                ready=1
                break
            fi
            if ! kill -0 "$VLLM_PID" 2>/dev/null; then
                echo "vLLM exited before readiness" >&2
                wait "$VLLM_PID" 2>/dev/null || true
                VLLM_PID=""
                tail -n 100 "$log" >&2
                break
            fi
            sleep 10
        done
        [ "$ready" = 1 ] && return 0
        cleanup
    done
    echo "vLLM failed to become ready after three attempts" >&2
    return 1
}

JOB_START=$(date +%s)
start_vllm 32768 call1

CALL1_START=$(date +%s)
"$CLIENT_PYTHON" scripts/run_call1_fact_graphs.py \
    --base-url "http://127.0.0.1:${PORT}" \
    --model "$SERVED_MODEL" \
    --api-key "$LOCAL_API_KEY" \
    --inventory "$INVENTORY" \
    --out "$FACT_GRAPHS" \
    --max-tokens "$CALL1_MAX_TOKENS"
CALL1_SECONDS=$(( $(date +%s) - CALL1_START ))

CALL15_START=$(date +%s)
"$CLIENT_PYTHON" scripts/run_article_select.py \
    --base-url "http://127.0.0.1:${PORT}" \
    --model "$SERVED_MODEL" \
    --api-key "$LOCAL_API_KEY" \
    --inventory "$INVENTORY" \
    --out "$SELECTION" \
    --max-tokens "$CALL15_MAX_TOKENS"
CALL15_SECONDS=$(( $(date +%s) - CALL15_START ))

cleanup
sleep 15

unset HF_HUB_OFFLINE TRANSFORMERS_OFFLINE
L0_START=$(date +%s)
"$CLIENT_PYTHON" scripts/run_l0_candidates.py \
    --inventory "$INVENTORY" \
    --fact-graphs "$FACT_GRAPHS" \
    --selection "$SELECTION" \
    --out "$CANDIDATES" \
    --report "$L0_REPORT" \
    --top-k-articles "$TOP_K_ARTICLES"
L0_SECONDS=$(( $(date +%s) - L0_START ))

sleep 15
start_vllm 65536 call2_call3
CALL23_START=$(date +%s)
"$CLIENT_PYTHON" scripts/run_issue_pipeline_batch.py \
    --base-url "http://127.0.0.1:${PORT}" \
    --model "$SERVED_MODEL" \
    --api-key "$LOCAL_API_KEY" \
    --inventory "$INVENTORY" \
    --fact-graphs "$FACT_GRAPHS" \
    --candidates "$CANDIDATES" \
    --run-dir "$CASES" \
    --out "$OUTPUT" \
    --call2-max-tokens "$CALL2_MAX_TOKENS" \
    --call3-max-tokens "$CALL3_MAX_TOKENS" \
    --overwrite \
    --no-cache
CALL23_SECONDS=$(( $(date +%s) - CALL23_START ))
cleanup

TOTAL_SECONDS=$(( $(date +%s) - JOB_START ))
"$CLIENT_PYTHON" scripts/verify_phase3_e2e_contract.py \
    --run-root "$RUN_ROOT" \
    --inventory "$INVENTORY" \
    --rubric "$RUBRIC" \
    --model "$SERVED_MODEL" \
    --slurm-job-id "$SLURM_JOB_ID" \
    --parameter "call1_max_tokens=$CALL1_MAX_TOKENS" \
    --parameter "call1_5_max_tokens=$CALL15_MAX_TOKENS" \
    --parameter "retrieval_top_k_articles=$TOP_K_ARTICLES" \
    --parameter "call2_max_tokens=$CALL2_MAX_TOKENS" \
    --parameter "call3_max_tokens=$CALL3_MAX_TOKENS" \
    --parameter "temperature=0.0" \
    --stage-seconds "call1=$CALL1_SECONDS" \
    --stage-seconds "call1_5=$CALL15_SECONDS" \
    --stage-seconds "l0=$L0_SECONDS" \
    --stage-seconds "call2_call3=$CALL23_SECONDS" \
    --stage-seconds "total=$TOTAL_SECONDS"

echo "manifest=$RUN_ROOT/freeze_manifest.json"
echo "=== Phase-3 two-case E2E passed: $(date) ==="
