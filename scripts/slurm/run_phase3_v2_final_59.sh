#!/bin/bash
# Reproduce the Phase-3 v2 pipeline at the exact answer-visibility commit over the
# sealed 59-case inventory.  Source, model snapshot, Python/vLLM environment, and
# output root are intentionally pinned to the previously successful job 218274 setup.
#SBATCH --job-name=phase3_v2_final_59
#SBATCH --output=logs/phase3_v2_final_59_%j.out
#SBATCH --error=logs/phase3_v2_final_59_%j.err
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:PRO6000:1
#SBATCH --mem=32G

set -euo pipefail

MAIN_ROOT="/data5/jaehoonjeong/IDPR"
V2_ROOT="$MAIN_ROOT/.worktrees/phase3_v2_4d48b2e"
V2_COMMIT="4d48b2e289f0e27c1212ef18af1bf5bbb12b9a03"
RUN_ROOT="$MAIN_ROOT/experiments/results/phase3_v2_final_59"
INVENTORY="$MAIN_ROOT/experiments/results/phase3_final_59/final_59_inventory.jsonl"
EXPECTED_INVENTORY_SHA="01e286646fdc0298a553af26cffa7dc324d050bcdef773d28026966dfdf5af28"
PYTHON_BIN="/data5/jaehoonjeong/miniconda3/envs/inv_ass_env/bin/python"
VLLM_BIN="/data5/jaehoonjeong/miniconda3/envs/inv_ass_env/bin/vllm"
MODEL_SNAPSHOT="/data5/jaehoonjeong/.cache/huggingface/hub/models--google--gemma-4-26B-A4B-it/snapshots/01e5b3ee840d3a9e0b0b493c593e85398a30ef75"
SERVED_MODEL="idpr-gemma-4-26b-a4b"
LOCAL_API_KEY="local-idpr"

FACT_GRAPHS="$RUN_ROOT/fact_graphs.jsonl"
SELECTION="$RUN_ROOT/article_selection.jsonl"
CANDIDATES="$RUN_ROOT/l0_candidates.jsonl"
CASES="$RUN_ROOT/cases"
OUTPUT="$RUN_ROOT/idpr_nsn_outputs.jsonl"
SERVER_DIR="$RUN_ROOT/server"

cd "$MAIN_ROOT"
mkdir -p logs
# Compute nodes do not expose git.  Verify the pinned worktree through immutable
# source hashes captured from V2_COMMIT on the submit node.
test "$(sha256sum "$V2_ROOT/scripts/run_call1_fact_graphs.py" | cut -d' ' -f1)" = \
    "06e61f45857588c57ee869f13591d97e59643d553094b51846e41827da37f92e"
test "$(sha256sum "$V2_ROOT/scripts/run_article_select.py" | cut -d' ' -f1)" = \
    "8ca0730a8915555d8b89741cd52bd1a16fe4572e602517bcc081cabcb5f8b0a4"
test "$(sha256sum "$V2_ROOT/scripts/run_l0_candidates.py" | cut -d' ' -f1)" = \
    "4e24ea84429eca0b49034c4395a17ff11cad7c09d3c6dec331b9a09f05d5c6c2"
test "$(sha256sum "$V2_ROOT/scripts/run_issue_pipeline_batch.py" | cut -d' ' -f1)" = \
    "5b02657a5f61d654be1626c32fba8a6e6366a03d80a8ed30e85bdc1be1876e6d"
test "$(sha256sum "$INVENTORY" | cut -d' ' -f1)" = "$EXPECTED_INVENTORY_SHA"
test -x "$PYTHON_BIN"
test -x "$VLLM_BIN"
test -d "$MODEL_SNAPSHOT"
if [ -e "$RUN_ROOT" ]; then
    echo "output already exists: $RUN_ROOT" >&2
    exit 1
fi
mkdir -p "$RUN_ROOT" "$CASES" "$SERVER_DIR"

export TOKENIZERS_PARALLELISM=false
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export VLLM_USE_FLASHINFER_SAMPLER=0
export JE_ARROW_MALLOC_CONF="${JE_ARROW_MALLOC_CONF:-background_thread:false}"
export TORCH_CUDA_ARCH_LIST="${TORCH_CUDA_ARCH_LIST:-12.0}"
export HF_HOME="/data5/jaehoonjeong/.cache/huggingface"
export PYTHONPATH="$V2_ROOT/src"

VLLM_PID=""
PORT=""
cleanup() {
    if [ -n "$VLLM_PID" ]; then
        kill "$VLLM_PID" 2>/dev/null || true
        wait "$VLLM_PID" 2>/dev/null || true
        VLLM_PID=""
    fi
}
trap cleanup EXIT

start_vllm() {
    local max_len="$1"
    local phase="$2"
    PORT=$("$PYTHON_BIN" -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1",0)); print(s.getsockname()[1]); s.close()')
    unset CUDA_HOME CUDA_PATH FLASHINFER_CUDA_ARCH_LIST FLASHINFER_WORKSPACE_BASE
    "$VLLM_BIN" serve "$MODEL_SNAPSHOT" \
        --served-model-name "$SERVED_MODEL" \
        --host 127.0.0.1 --port "$PORT" --api-key "$LOCAL_API_KEY" \
        --tensor-parallel-size 1 --max-model-len "$max_len" --max-num-seqs 1 \
        --gpu-memory-utilization 0.90 --reasoning-parser gemma4 \
        --structured-outputs-config '{"backend":"guidance","disable_any_whitespace":true}' \
        > "$SERVER_DIR/${phase}.log" 2>&1 &
    VLLM_PID=$!
    for _ in $(seq 1 180); do
        if "$PYTHON_BIN" -c "import json,urllib.request; r=urllib.request.Request('http://127.0.0.1:${PORT}/v1/models',headers={'Authorization':'Bearer ${LOCAL_API_KEY}'}); d=json.load(urllib.request.urlopen(r,timeout=5)); assert any(m['id']=='${SERVED_MODEL}' for m in d['data'])" 2>/dev/null; then
            return 0
        fi
        kill -0 "$VLLM_PID" 2>/dev/null || { tail -n 120 "$SERVER_DIR/${phase}.log" >&2; return 1; }
        sleep 10
    done
    echo "vLLM did not become ready for $phase" >&2
    return 1
}

echo "=== Phase-3 v2 59 generation start: $(date) ==="
echo "job=$SLURM_JOB_ID source_commit=$V2_COMMIT model=$MODEL_SNAPSHOT"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader

JOB_START=$(date +%s)
start_vllm 32768 call1
CALL1_START=$(date +%s)
cd "$V2_ROOT"
"$PYTHON_BIN" scripts/run_call1_fact_graphs.py \
    --base-url "http://127.0.0.1:${PORT}" --model "$SERVED_MODEL" \
    --api-key "$LOCAL_API_KEY" --inventory "$INVENTORY" \
    --out "$FACT_GRAPHS" --max-tokens 8192
"$PYTHON_BIN" scripts/run_article_select.py \
    --base-url "http://127.0.0.1:${PORT}" --model "$SERVED_MODEL" \
    --api-key "$LOCAL_API_KEY" --inventory "$INVENTORY" \
    --out "$SELECTION" --max-tokens 2048
CALL1_SECONDS=$(( $(date +%s) - CALL1_START ))
cleanup
sleep 15

L0_START=$(date +%s)
unset HF_HUB_OFFLINE TRANSFORMERS_OFFLINE
"$PYTHON_BIN" scripts/run_l0_candidates.py \
    --inventory "$INVENTORY" --fact-graphs "$FACT_GRAPHS" \
    --selection "$SELECTION" --out "$CANDIDATES" \
    --report "$RUN_ROOT/l0_report.json" --top-k-articles 10
L0_SECONDS=$(( $(date +%s) - L0_START ))
sleep 15

start_vllm 65536 call2_call3
CALL23_START=$(date +%s)
"$PYTHON_BIN" scripts/run_issue_pipeline_batch.py \
    --base-url "http://127.0.0.1:${PORT}" --model "$SERVED_MODEL" \
    --api-key "$LOCAL_API_KEY" --inventory "$INVENTORY" \
    --fact-graphs "$FACT_GRAPHS" --candidates "$CANDIDATES" \
    --run-dir "$CASES" --out "$OUTPUT" \
    --call2-max-tokens 12288 --call3-max-tokens 16384 \
    --overwrite --no-cache
CALL23_SECONDS=$(( $(date +%s) - CALL23_START ))
cleanup
TOTAL_SECONDS=$(( $(date +%s) - JOB_START ))

"$PYTHON_BIN" "$MAIN_ROOT/scripts/write_phase3_v2_generation_manifest.py" \
    --run-root "$RUN_ROOT" --inventory "$INVENTORY" --output "$OUTPUT" \
    --model "$SERVED_MODEL" --model-snapshot "$MODEL_SNAPSHOT" \
    --source-root "$V2_ROOT" --source-commit "$V2_COMMIT" \
    --slurm-job-id "$SLURM_JOB_ID" \
    --stage-seconds "call1_call1_5=$CALL1_SECONDS" \
    --stage-seconds "l0=$L0_SECONDS" \
    --stage-seconds "call2_call3=$CALL23_SECONDS" \
    --stage-seconds "total=$TOTAL_SECONDS"

echo "output=$OUTPUT"
echo "=== Phase-3 v2 59 generation end: $(date) ==="
