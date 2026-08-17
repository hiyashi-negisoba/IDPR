#!/bin/bash
#SBATCH --job-name=idpr_v2_external
#SBATCH --output=logs/idpr_v2_external_%j.out
#SBATCH --error=logs/idpr_v2_external_%j.err
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:PRO6000:1
#SBATCH --mem=32G

set -euo pipefail

source "${IDPR_PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}/scripts/slurm/_env.sh"

CLIENT_PYTHON="${IDPR_EXTERNAL_CLIENT_PYTHON:-${IDPR_STEP8_CLIENT_PYTHON:-/data5/jaehoonjeong/miniconda3/bin/python}}"
VLLM_BIN="${IDPR_EXTERNAL_VLLM_BIN:-${IDPR_STEP8_VLLM_BIN:-/data5/jaehoonjeong/miniconda3/envs/inv_ass_env/bin/vllm}}"
MODEL_SNAPSHOT="${IDPR_EXTERNAL_MODEL_SNAPSHOT:?set IDPR_EXTERNAL_MODEL_SNAPSHOT}"
SERVED_MODEL="${IDPR_EXTERNAL_SERVED_MODEL:-idpr-external-model}"
LOCAL_API_KEY="${IDPR_EXTERNAL_API_KEY:-local-idpr}"
BENCHMARK="${IDPR_EXTERNAL_BENCHMARK:-all}"
BINARY_MODE="${IDPR_EXTERNAL_BINARY_MODE:-0}"
RUN_ROOT="${IDPR_EXTERNAL_RUN_ROOT:-$PROJECT_ROOT/experiments/external/runs/${SLURM_JOB_ID}}"
MATERIALIZED="$RUN_ROOT/materialized"
SERVER_DIR="$RUN_ROOT/server"
MAX_MODEL_LEN="${IDPR_EXTERNAL_MAX_MODEL_LEN:-32768}"
MAX_NUM_SEQS="${IDPR_EXTERNAL_MAX_NUM_SEQS:-1}"
GPU_MEMORY_UTILIZATION="${IDPR_EXTERNAL_GPU_MEMORY_UTILIZATION:-0.90}"

case "$BENCHMARK" in
    all|lbox_call1|kbl_call2) ;;
    *) echo "invalid IDPR_EXTERNAL_BENCHMARK=$BENCHMARK" >&2; exit 2 ;;
esac

test -x "$CLIENT_PYTHON"
test -x "$VLLM_BIN"
test -d "$MODEL_SNAPSHOT"

export TOKENIZERS_PARALLELISM=false
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export VLLM_USE_FLASHINFER_SAMPLER=0
export JE_ARROW_MALLOC_CONF="${JE_ARROW_MALLOC_CONF:-background_thread:false}"
export PYTHONPATH="$PROJECT_ROOT/src${PYTHONPATH:+:$PYTHONPATH}"

cd "$PROJECT_ROOT"
mkdir -p "$RUN_ROOT" "$MATERIALIZED" "$SERVER_DIR"

if [ "${IDPR_EXTERNAL_SKIP_TESTS:-0}" != "1" ]; then
    "$CLIENT_PYTHON" -m pytest -q tests/test_v2_external_benchmarks.py
fi

LBOX_SOURCE_ARGS=()
if [ -n "${IDPR_EXTERNAL_LBOX_SOURCE_DIR:-}" ]; then
    LBOX_SOURCE_ARGS=(--lbox-source-dir "$IDPR_EXTERNAL_LBOX_SOURCE_DIR")
fi
KBL_SOURCE_ARGS=()
if [ -n "${IDPR_EXTERNAL_KBL_SOURCE:-}" ]; then
    KBL_SOURCE_ARGS=(--kbl-source "$IDPR_EXTERNAL_KBL_SOURCE")
fi

"$CLIENT_PYTHON" scripts/prepare_v2_external_benchmarks.py \
    --benchmark "$BENCHMARK" \
    --out-root "$MATERIALIZED" \
    "${LBOX_SOURCE_ARGS[@]}" \
    "${KBL_SOURCE_ARGS[@]}"

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

VLLM_ARGS=(
    serve "$MODEL_SNAPSHOT"
    --served-model-name "$SERVED_MODEL"
    --host 127.0.0.1
    --port "$PORT"
    --api-key "$LOCAL_API_KEY"
    --tensor-parallel-size 1
    --max-model-len "$MAX_MODEL_LEN"
    --max-num-seqs "$MAX_NUM_SEQS"
    --gpu-memory-utilization "$GPU_MEMORY_UTILIZATION"
    --structured-outputs-config '{"backend":"guidance","disable_any_whitespace":true}'
)
if [ -n "${IDPR_EXTERNAL_REASONING_PARSER:-}" ]; then
    VLLM_ARGS+=(--reasoning-parser "$IDPR_EXTERNAL_REASONING_PARSER")
fi

unset CUDA_HOME CUDA_PATH FLASHINFER_CUDA_ARCH_LIST FLASHINFER_WORKSPACE_BASE
"$VLLM_BIN" "${VLLM_ARGS[@]}" > "$SERVER_DIR/vllm.log" 2>&1 &
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
        tail -n 120 "$SERVER_DIR/vllm.log" >&2
        exit 1
    fi
    sleep 10
done
if [ "$READY" != 1 ]; then
    echo "vLLM did not become ready" >&2
    exit 1
fi

run_benchmark() {
    local benchmark="$1"
    local input_dir="$MATERIALIZED/$benchmark"
    local out="$RUN_ROOT/$benchmark/predictions.jsonl"
    mkdir -p "$(dirname "$out")"
    local cmd=(
        "$CLIENT_PYTHON" scripts/run_v2_external_benchmark.py
        --benchmark "$benchmark"
        --input-dir "$input_dir"
        --out "$out"
        --base-url "http://127.0.0.1:${PORT}"
        --model "$SERVED_MODEL"
        --api-key "$LOCAL_API_KEY"
        --prompt-approved
    )
    if [ "$benchmark" = "kbl_call2" ] && [ "$BINARY_MODE" = "1" ]; then
        cmd+=(--binary-mode)
    fi
    "${cmd[@]}"
}

if [ "$BENCHMARK" = "all" ] || [ "$BENCHMARK" = "lbox_call1" ]; then
    run_benchmark lbox_call1
fi
if [ "$BENCHMARK" = "all" ] || [ "$BENCHMARK" = "kbl_call2" ]; then
    run_benchmark kbl_call2
fi

cleanup

echo "run_root=$RUN_ROOT"
if [ "$BENCHMARK" = "all" ] || [ "$BENCHMARK" = "lbox_call1" ]; then
    echo "$CLIENT_PYTHON scripts/evaluate_v2_external_benchmark.py --benchmark lbox_call1 --input-dir $MATERIALIZED/lbox_call1 --predictions $RUN_ROOT/lbox_call1/predictions.jsonl --out $RUN_ROOT/lbox_call1/scores.json"
fi
if [ "$BENCHMARK" = "all" ] || [ "$BENCHMARK" = "kbl_call2" ]; then
    echo "$CLIENT_PYTHON scripts/evaluate_v2_external_benchmark.py --benchmark kbl_call2 --input-dir $MATERIALIZED/kbl_call2 --predictions $RUN_ROOT/kbl_call2/predictions.jsonl --out $RUN_ROOT/kbl_call2/scores.json"
fi
