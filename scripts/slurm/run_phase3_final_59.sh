#!/bin/bash
#SBATCH --job-name=phase3_final_59
#SBATCH --output=logs/phase3_final_59_%j.out
#SBATCH --error=logs/phase3_final_59_%j.err
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:PRO6000:1
#SBATCH --mem=32G

set -euo pipefail
source "${IDPR_PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}/scripts/slurm/_env.sh"

if [ "${IDPR_FINAL59_RESUME:-0}" = "1" ]; then
    exec /bin/bash "$PROJECT_ROOT/scripts/slurm/run_phase3_final_59_resume.sh"
fi

RUN_ROOT="${IDPR_FINAL59_ROOT:-$PROJECT_ROOT/experiments/results/phase3_final_59}"
INVENTORY="$RUN_ROOT/final_59_inventory.jsonl"
FACT_GRAPHS="$RUN_ROOT/fact_graphs.jsonl"
SELECTION="$RUN_ROOT/article_selection.jsonl"
CANDIDATES="$RUN_ROOT/l0_candidates.jsonl"
CASES="$RUN_ROOT/cases"
OUTPUT="$RUN_ROOT/idpr_nsn_outputs.jsonl"
SERVER_DIR="$RUN_ROOT/server"

export TOKENIZERS_PARALLELISM=false
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export VLLM_USE_FLASHINFER_SAMPLER=0
export JE_ARROW_MALLOC_CONF="${JE_ARROW_MALLOC_CONF:-background_thread:false}"
export TORCH_CUDA_ARCH_LIST="${TORCH_CUDA_ARCH_LIST:-12.0}"
export PYTHONPATH="$PROJECT_ROOT/src${PYTHONPATH:+:$PYTHONPATH}"

cd "$PROJECT_ROOT"
mkdir -p logs
if [ -e "$RUN_ROOT" ]; then
    echo "output already exists: $RUN_ROOT" >&2
    exit 1
fi
mkdir -p "$RUN_ROOT" "$CASES" "$SERVER_DIR"
"$CLIENT_PYTHON" scripts/build_phase3_final_eval_inventory.py --out "$INVENTORY"

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
    PORT=$("$CLIENT_PYTHON" -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1",0)); print(s.getsockname()[1]); s.close()')
    unset CUDA_HOME CUDA_PATH FLASHINFER_CUDA_ARCH_LIST FLASHINFER_WORKSPACE_BASE
    "$VLLM_BIN" serve "$MODEL_SNAPSHOT" --served-model-name "$SERVED_MODEL" \
        --host 127.0.0.1 --port "$PORT" --api-key "$LOCAL_API_KEY" \
        --tensor-parallel-size 1 --max-model-len "$max_len" --max-num-seqs 1 \
        --gpu-memory-utilization 0.90 --reasoning-parser gemma4 \
        --structured-outputs-config '{"backend":"guidance","disable_any_whitespace":true}' \
        > "$SERVER_DIR/${phase}.log" 2>&1 &
    VLLM_PID=$!
    for _ in $(seq 1 180); do
        if "$CLIENT_PYTHON" -c "import json,urllib.request; r=urllib.request.Request('http://127.0.0.1:${PORT}/v1/models',headers={'Authorization':'Bearer ${LOCAL_API_KEY}'}); d=json.load(urllib.request.urlopen(r,timeout=5)); assert any(m['id']=='${SERVED_MODEL}' for m in d['data'])" 2>/dev/null; then
            return 0
        fi
        kill -0 "$VLLM_PID" 2>/dev/null || { tail -n 100 "$SERVER_DIR/${phase}.log" >&2; return 1; }
        sleep 10
    done
    return 1
}

JOB_START=$(date +%s)
start_vllm 32768 call1
CALL1_START=$(date +%s)
"$CLIENT_PYTHON" scripts/run_call1_fact_graphs.py --base-url "http://127.0.0.1:${PORT}" \
    --model "$SERVED_MODEL" --api-key "$LOCAL_API_KEY" --inventory "$INVENTORY" \
    --out "$FACT_GRAPHS" --max-tokens 8192
"$CLIENT_PYTHON" scripts/run_article_select.py --base-url "http://127.0.0.1:${PORT}" \
    --model "$SERVED_MODEL" --api-key "$LOCAL_API_KEY" --inventory "$INVENTORY" \
    --out "$SELECTION" --max-tokens 2048
CALL1_SECONDS=$(( $(date +%s) - CALL1_START ))
cleanup
sleep 15

L0_START=$(date +%s)
unset HF_HUB_OFFLINE TRANSFORMERS_OFFLINE
"$CLIENT_PYTHON" scripts/run_l0_candidates.py --inventory "$INVENTORY" \
    --fact-graphs "$FACT_GRAPHS" --selection "$SELECTION" --out "$CANDIDATES" \
    --report "$RUN_ROOT/l0_report.json" --top-k-articles 10
L0_SECONDS=$(( $(date +%s) - L0_START ))
sleep 15

start_vllm 65536 call2_call3
CALL23_START=$(date +%s)
"$CLIENT_PYTHON" scripts/run_issue_pipeline_batch.py --base-url "http://127.0.0.1:${PORT}" \
    --model "$SERVED_MODEL" --api-key "$LOCAL_API_KEY" --inventory "$INVENTORY" \
    --fact-graphs "$FACT_GRAPHS" --candidates "$CANDIDATES" --run-dir "$CASES" \
    --out "$OUTPUT" --call2-max-tokens 12288 --call3-max-tokens 16384 \
    --overwrite --no-cache
CALL23_SECONDS=$(( $(date +%s) - CALL23_START ))
cleanup
TOTAL_SECONDS=$(( $(date +%s) - JOB_START ))

"$CLIENT_PYTHON" scripts/write_phase3_generation_manifest.py --run-root "$RUN_ROOT" \
    --inventory "$INVENTORY" --output "$OUTPUT" --model "$SERVED_MODEL" \
    --slurm-job-id "$SLURM_JOB_ID" --tested-code-commit "$(git rev-parse HEAD)" \
    --stage-seconds "call1_call1_5=$CALL1_SECONDS" --stage-seconds "l0=$L0_SECONDS" \
    --stage-seconds "call2_call3=$CALL23_SECONDS" --stage-seconds "total=$TOTAL_SECONDS"

echo "output=$OUTPUT"
echo "manifest=$RUN_ROOT/generation_manifest.json"
