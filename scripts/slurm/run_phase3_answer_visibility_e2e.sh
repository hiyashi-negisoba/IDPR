#!/bin/bash
#SBATCH --job-name=phase3_answer_visibility
#SBATCH --output=logs/phase3_answer_visibility_%j.out
#SBATCH --error=logs/phase3_answer_visibility_%j.err
#SBATCH --time=02:00:00
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:PRO6000:1
#SBATCH --mem=32G

# Call-3-only E2E over the two authorized smoke cases.  The persisted top-10 experiment's
# Call 1, Call 1.5, L0, Call 2 and Scallop artifacts are copied byte-for-byte.  Only the
# answer request, real model response, host attachment and final contract are regenerated.

set -euo pipefail
source "${IDPR_PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}/scripts/slurm/_env.sh"

SOURCE_ROOT="$PROJECT_ROOT/experiments/results/phase3_top10_e2e"
RUN_ROOT="${IDPR_ANSWER_VISIBILITY_ROOT:-$PROJECT_ROOT/experiments/results/phase3_answer_visibility_e2e}"
INVENTORY="$PROJECT_ROOT/data/smoke/phase3_e2e_inventory.jsonl"
RUBRIC="$PROJECT_ROOT/data/smoke/phase3_e2e_rubrics.json"
CASES="$RUN_ROOT/cases"
OUTPUT="$RUN_ROOT/idpr_nsn_outputs.jsonl"
SERVER_LOG="$RUN_ROOT/vllm.log"

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
mkdir -p "$CASES/kcl_criminal_r10_p1_q1_ga"
mkdir -p "$CASES/CASE_KCL1730_2026_BRIBERY_FRAUD_002"
cp "$SOURCE_ROOT/fact_graphs.jsonl" "$RUN_ROOT/fact_graphs.jsonl"
cp "$SOURCE_ROOT/article_selection.jsonl" "$RUN_ROOT/article_selection.jsonl"
cp "$SOURCE_ROOT/l0_candidates.jsonl" "$RUN_ROOT/l0_candidates.jsonl"
cp "$SOURCE_ROOT/cases/kcl_criminal_r10_p1_q1_ga/issue_assessment.json" \
    "$CASES/kcl_criminal_r10_p1_q1_ga/issue_assessment.json"
cp "$SOURCE_ROOT/cases/CASE_KCL1730_2026_BRIBERY_FRAUD_002/issue_assessment.json" \
    "$CASES/CASE_KCL1730_2026_BRIBERY_FRAUD_002/issue_assessment.json"

PORT=$("$CLIENT_PYTHON" -c \
    'import socket; s=socket.socket(); s.bind(("127.0.0.1",0)); print(s.getsockname()[1]); s.close()')
VLLM_PID=""
cleanup() {
    if [ -n "$VLLM_PID" ]; then
        kill "$VLLM_PID" 2>/dev/null || true
        wait "$VLLM_PID" 2>/dev/null || true
        VLLM_PID=""
    fi
}
trap cleanup EXIT

unset CUDA_HOME CUDA_PATH FLASHINFER_CUDA_ARCH_LIST FLASHINFER_WORKSPACE_BASE
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
    > "$SERVER_LOG" 2>&1 &
VLLM_PID=$!

READY=0
for _ in $(seq 1 180); do
    if "$CLIENT_PYTHON" -c \
        "import json,urllib.request; r=urllib.request.Request('http://127.0.0.1:${PORT}/v1/models',headers={'Authorization':'Bearer ${LOCAL_API_KEY}'}); d=json.load(urllib.request.urlopen(r,timeout=5)); assert any(m['id']=='${SERVED_MODEL}' for m in d['data'])" \
        2>/dev/null; then
        READY=1
        break
    fi
    if ! kill -0 "$VLLM_PID" 2>/dev/null; then
        tail -n 120 "$SERVER_LOG" >&2
        exit 1
    fi
    sleep 10
done
if [ "$READY" != 1 ]; then
    echo "vLLM did not become ready" >&2
    exit 1
fi

START=$(date +%s)
"$CLIENT_PYTHON" scripts/run_issue_pipeline_batch.py \
    --base-url "http://127.0.0.1:${PORT}" \
    --model "$SERVED_MODEL" \
    --api-key "$LOCAL_API_KEY" \
    --inventory "$INVENTORY" \
    --fact-graphs "$RUN_ROOT/fact_graphs.jsonl" \
    --candidates "$RUN_ROOT/l0_candidates.jsonl" \
    --run-dir "$CASES" \
    --out "$OUTPUT" \
    --call3-max-tokens 16384 \
    --no-cache
SECONDS_USED=$(( $(date +%s) - START ))
cleanup

"$CLIENT_PYTHON" scripts/verify_phase3_e2e_contract.py \
    --run-root "$RUN_ROOT" \
    --inventory "$INVENTORY" \
    --rubric "$RUBRIC" \
    --model "$SERVED_MODEL" \
    --slurm-job-id "$SLURM_JOB_ID" \
    --tested-code-commit "$(git rev-parse HEAD)" \
    --parameter "candidate_policy=union_top10" \
    --parameter "upstream_source=phase3_top10_e2e" \
    --parameter "call2=reused_byte_for_byte" \
    --parameter "call3_max_tokens=16384" \
    --parameter "answer_visibility=full_compact_hidden_v1" \
    --stage-seconds "call3=$SECONDS_USED" \
    --out "$RUN_ROOT/e2e_manifest.json"

echo "run_root=$RUN_ROOT"
