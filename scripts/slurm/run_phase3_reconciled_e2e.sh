#!/bin/bash
#SBATCH --job-name=phase3_reconciled_e2e
#SBATCH --output=logs/phase3_reconciled_e2e_%j.out
#SBATCH --error=logs/phase3_reconciled_e2e_%j.err
#SBATCH --time=03:00:00
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:PRO6000:1
#SBATCH --mem=32G

# Downstream-only E2E for one approved experimental L0 artifact. Frozen Call 1 and 1.5
# are copied byte-for-byte; Call 2, Scallop, and Call 3 are regenerated without cache.

set -euo pipefail
source "${IDPR_PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}/scripts/slurm/_env.sh"

: "${IDPR_RECONCILED_L0:?set IDPR_RECONCILED_L0 to the experimental l0_candidates.jsonl}"
FREEZE_ROOT="${IDPR_FREEZE_ROOT:-$PROJECT_ROOT/experiments/results/phase3_e2e_freeze_v1}"
RUN_ROOT="${IDPR_RECONCILED_E2E_ROOT:-$PROJECT_ROOT/experiments/results/phase3_reconciled_e2e_${SLURM_JOB_ID}}"
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
mkdir -p "$RUN_ROOT" "$CASES"
cp "$FREEZE_ROOT/fact_graphs.jsonl" "$RUN_ROOT/fact_graphs.jsonl"
cp "$FREEZE_ROOT/article_selection.jsonl" "$RUN_ROOT/article_selection.jsonl"
cp "$IDPR_RECONCILED_L0" "$RUN_ROOT/l0_candidates.jsonl"
if [ -n "${IDPR_RECONCILE_AUDIT:-}" ]; then
    cp "$IDPR_RECONCILE_AUDIT" "$RUN_ROOT/reconciliation.jsonl"
fi

PORT=$("$CLIENT_PYTHON" -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1",0)); print(s.getsockname()[1]); s.close()')
VLLM_PID=""
cleanup() {
    if [ -n "$VLLM_PID" ]; then
        kill "$VLLM_PID" 2>/dev/null || true
        wait "$VLLM_PID" 2>/dev/null || true
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
    --call2-max-tokens 12288 \
    --call3-max-tokens 16384 \
    --overwrite \
    --no-cache
SECONDS_USED=$(( $(date +%s) - START ))
cleanup
VLLM_PID=""

"$CLIENT_PYTHON" scripts/verify_phase3_e2e_contract.py \
    --run-root "$RUN_ROOT" \
    --inventory "$INVENTORY" \
    --rubric "$RUBRIC" \
    --model "$SERVED_MODEL" \
    --slurm-job-id "$SLURM_JOB_ID" \
    --tested-code-commit "$(git rev-parse HEAD)" \
    --parameter "candidate_policy=${IDPR_CANDIDATE_POLICY:-reconciled}" \
    --parameter "frozen_upstream=phase3-e2e-freeze-v1" \
    --parameter "call2_max_tokens=12288" \
    --parameter "call3_max_tokens=16384" \
    --parameter "temperature=0.0" \
    --stage-seconds "call2_call3=$SECONDS_USED" \
    --out "$RUN_ROOT/e2e_manifest.json"

echo "run_root=$RUN_ROOT"
