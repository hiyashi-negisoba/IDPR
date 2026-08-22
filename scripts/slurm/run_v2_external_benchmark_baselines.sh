#!/bin/bash
#SBATCH --job-name=idpr_v2_external_baselines
#SBATCH --output=logs/idpr_v2_external_baselines_%j.out
#SBATCH --error=logs/idpr_v2_external_baselines_%j.err
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:PRO6000:1
#SBATCH --mem=32G

# Runs the official, unmodified `run_baselines_experiment.py` (vanilla_zero_shot /
# chain_of_thought) against an already-materialized LBOX/KBL benchmark directory, then
# scores the free-text output with the new deterministic keyword-match scorer
# (`score_v2_external_benchmark_baseline.py`). Production Call1/Call2 harness and
# baseline classes are untouched -- this script only adapts and orchestrates.
#
#   IDPR_EXTERNAL_MODEL_SNAPSHOT=/path/to/model \
#   IDPR_EXTERNAL_MATERIALIZED=<existing materialized dir, e.g. experiments/external/runs/full/materialized> \
#   sbatch --export=ALL scripts/slurm/run_v2_external_benchmark_baselines.sh

set -euo pipefail

source "${IDPR_PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}/scripts/slurm/_env.sh"

# Baseline classes (ACAL/leprec/standard_rag/...) need heavier deps (langchain_chroma etc.)
# than base python carries -- unlike the production Call1/Call2 harness, this defaults to
# inv_ass_env, not base.
CLIENT_PYTHON="${IDPR_EXTERNAL_CLIENT_PYTHON:-${IDPR_STEP8_CLIENT_PYTHON:-/data5/jaehoonjeong/miniconda3/envs/inv_ass_env/bin/python}}"
VLLM_BIN="${IDPR_EXTERNAL_VLLM_BIN:-${IDPR_STEP8_VLLM_BIN:-/data5/jaehoonjeong/miniconda3/envs/inv_ass_env/bin/vllm}}"
MODEL_SNAPSHOT="${IDPR_EXTERNAL_MODEL_SNAPSHOT:?set IDPR_EXTERNAL_MODEL_SNAPSHOT}"
SERVED_MODEL="${IDPR_EXTERNAL_SERVED_MODEL:-idpr-external-model}"
LOCAL_API_KEY="${IDPR_EXTERNAL_API_KEY:-local-idpr}"
BASELINES="${IDPR_EXTERNAL_BASELINES:-vanilla_zero_shot,chain_of_thought}"
MATERIALIZED="${IDPR_EXTERNAL_MATERIALIZED:?set IDPR_EXTERNAL_MATERIALIZED to an existing materialized dir}"
RUN_ROOT="${IDPR_EXTERNAL_BASELINE_RUN_ROOT:-$PROJECT_ROOT/experiments/external/runs/baselines/${SLURM_JOB_ID}}"
MAX_MODEL_LEN="${IDPR_EXTERNAL_MAX_MODEL_LEN:-32768}"
MAX_NUM_SEQS="${IDPR_EXTERNAL_MAX_NUM_SEQS:-1}"
GPU_MEMORY_UTILIZATION="${IDPR_EXTERNAL_GPU_MEMORY_UTILIZATION:-0.90}"

test -x "$CLIENT_PYTHON"
test -x "$VLLM_BIN"
test -d "$MODEL_SNAPSHOT"
test -d "$MATERIALIZED/lbox_call1"
test -d "$MATERIALIZED/kbl_call2"

export TOKENIZERS_PARALLELISM=false
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export VLLM_USE_FLASHINFER_SAMPLER=0
export JE_ARROW_MALLOC_CONF="${JE_ARROW_MALLOC_CONF:-background_thread:false}"
export PYTHONPATH="$PROJECT_ROOT/src${PYTHONPATH:+:$PYTHONPATH}"

cd "$PROJECT_ROOT"
mkdir -p "$RUN_ROOT/datasets" "$RUN_ROOT/outputs" "$RUN_ROOT/scores"

"$CLIENT_PYTHON" scripts/build_v2_external_baseline_dataset.py \
    --benchmark lbox_call1 --input-dir "$MATERIALIZED/lbox_call1" \
    --out "$RUN_ROOT/datasets/lbox_call1.jsonl"
"$CLIENT_PYTHON" scripts/build_v2_external_baseline_dataset.py \
    --benchmark kbl_call2 --input-dir "$MATERIALIZED/kbl_call2" \
    --out "$RUN_ROOT/datasets/kbl_call2.jsonl"

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
)
if [ -n "${IDPR_EXTERNAL_REASONING_PARSER:-}" ]; then
    VLLM_ARGS+=(--reasoning-parser "$IDPR_EXTERNAL_REASONING_PARSER")
fi

unset CUDA_HOME CUDA_PATH FLASHINFER_CUDA_ARCH_LIST FLASHINFER_WORKSPACE_BASE
"$VLLM_BIN" "${VLLM_ARGS[@]}" > "$RUN_ROOT/vllm.log" 2>&1 &
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
        tail -n 120 "$RUN_ROOT/vllm.log" >&2
        exit 1
    fi
    sleep 10
done
if [ "$READY" != 1 ]; then
    echo "vLLM did not become ready" >&2
    exit 1
fi

for benchmark in lbox_call1 kbl_call2; do
    "$CLIENT_PYTHON" scripts/run_baselines_experiment.py \
        --baseline "$BASELINES" \
        --dataset "$RUN_ROOT/datasets/${benchmark}.jsonl" \
        --outdir "$RUN_ROOT/outputs/${benchmark}" \
        --vllm-url "http://127.0.0.1:${PORT}" \
        --vllm-model "$SERVED_MODEL"
done

cleanup

echo "run_root=$RUN_ROOT"
IFS=',' read -ra BASELINE_LIST <<< "$BASELINES"
for benchmark in lbox_call1 kbl_call2; do
    for baseline_id in "${BASELINE_LIST[@]}"; do
        "$CLIENT_PYTHON" scripts/score_v2_external_benchmark_baseline.py \
            --benchmark "$benchmark" \
            --input-dir "$MATERIALIZED/$benchmark" \
            --predictions "$RUN_ROOT/outputs/${benchmark}/${baseline_id}_outputs.jsonl" \
            --baseline-id "$baseline_id" \
            --out "$RUN_ROOT/scores/${benchmark}_${baseline_id}.json"
    done
done
