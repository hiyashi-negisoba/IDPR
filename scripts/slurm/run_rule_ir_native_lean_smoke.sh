#!/bin/bash
#SBATCH --job-name=ruleir_native_lean
#SBATCH --output=logs/ruleir_native_lean_%j.out
#SBATCH --error=logs/ruleir_native_lean_%j.err
#SBATCH --time=02:00:00
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:PRO6000:1
#SBATCH --mem=32G

set -euo pipefail

SUBMIT_ROOT="${IDPR_PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-}}"
if [ -z "$SUBMIT_ROOT" ]; then
    echo "set IDPR_PROJECT_ROOT or submit from the repository root" >&2
    exit 2
fi
# shellcheck source=scripts/slurm/_env.sh
source "$SUBMIT_ROOT/scripts/slurm/_env.sh"

CASE_ID="${IDPR_CASE_ID:?set IDPR_CASE_ID to one inventory sub_question_id}"
RUN_DIR="${IDPR_RUN_DIR:-$PROJECT_ROOT/experiments/results/rule_ir_native_lean_smoke_${SLURM_JOB_ID}}"
SERVER_DIR="${IDPR_SERVER_DIR:-$PROJECT_ROOT/.cache/rule_ir_native_lean_server/${SLURM_JOB_ID}}"
SCLI_PATH="${IDPR_SCLI:-$PROJECT_ROOT/tools/scallop/scli-0.2.4-linux-x86_64}"

export TOKENIZERS_PARALLELISM=false
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export VLLM_USE_FLASHINFER_SAMPLER=0
export JE_ARROW_MALLOC_CONF="${JE_ARROW_MALLOC_CONF:-background_thread:false}"
export TORCH_CUDA_ARCH_LIST="${TORCH_CUDA_ARCH_LIST:-12.0}"
export PYTHONPATH="$PROJECT_ROOT/src${PYTHONPATH:+:$PYTHONPATH}"

cd "$PROJECT_ROOT"
mkdir -p "$SERVER_DIR" "$RUN_DIR" logs

PORT=$(
    "$CLIENT_PYTHON" -c \
        'import socket; s=socket.socket(); s.bind(("127.0.0.1", 0)); print(s.getsockname()[1]); s.close()'
)
VLLM_PID=""
cleanup() {
    if [ -n "$VLLM_PID" ]; then
        kill "$VLLM_PID" 2>/dev/null || true
        wait "$VLLM_PID" 2>/dev/null || true
        VLLM_PID=""
    fi
}
trap cleanup EXIT

echo "=== RuleIR-native lean smoke start: $(date) ==="
echo "job=$SLURM_JOB_ID host=$(hostname) case=$CASE_ID model=$MODEL_SNAPSHOT"
echo "commit=$(git rev-parse HEAD)"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader

VLLM_LOG="$SERVER_DIR/vllm.log"
"$VLLM_BIN" serve "$MODEL_SNAPSHOT" \
    --served-model-name "$SERVED_MODEL" \
    --host 127.0.0.1 \
    --port "$PORT" \
    --api-key "$LOCAL_API_KEY" \
    --tensor-parallel-size 1 \
    --max-model-len 65536 \
    --max-num-seqs 1 \
    --gpu-memory-utilization 0.90 \
    --generation-config vllm \
    --reasoning-parser gemma4 \
    --structured-outputs-config '{"backend":"guidance","disable_any_whitespace":true}' \
    > "$VLLM_LOG" 2>&1 &
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
        echo "vLLM exited before readiness" >&2
        tail -n 100 "$VLLM_LOG" >&2
        exit 1
    fi
    sleep 10
done
if [ "$READY" != 1 ]; then
    echo "vLLM did not become ready within 30 minutes" >&2
    exit 1
fi

"$CLIENT_PYTHON" scripts/run_rule_ir_native_lean.py \
    --base-url "http://127.0.0.1:${PORT}" \
    --model "$SERVED_MODEL" \
    --case-id "$CASE_ID" \
    --out-dir "$RUN_DIR" \
    --scli "$SCLI_PATH"

cleanup
echo "answer=$RUN_DIR/$CASE_ID/05_answer.md"
echo "=== RuleIR-native lean smoke end: $(date) ==="
