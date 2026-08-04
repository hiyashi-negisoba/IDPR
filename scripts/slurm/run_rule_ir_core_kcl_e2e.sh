#!/bin/bash
#SBATCH --job-name=ruleir_core_e2e
#SBATCH --output=logs/ruleir_core_e2e_%j.out
#SBATCH --error=logs/ruleir_core_e2e_%j.err
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=4
#SBATCH --gres=gpu:PRO6000:1
#SBATCH --mem=48G

set -euo pipefail

source "${IDPR_PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}/scripts/slurm/_env.sh"

RUN_ROOT="${IDPR_CORE_E2E_ROOT:-$PROJECT_ROOT/experiments/results/rule_ir_core_kcl_e2e_${SLURM_JOB_ID}}"
SERVER_DIR="$RUN_ROOT/server"
mkdir -p "$PROJECT_ROOT/logs" "$RUN_ROOT" "$SERVER_DIR"
cd "$PROJECT_ROOT"

export TOKENIZERS_PARALLELISM=false
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export VLLM_USE_FLASHINFER_SAMPLER=0
export JE_ARROW_MALLOC_CONF="${JE_ARROW_MALLOC_CONF:-background_thread:false}"
export TORCH_CUDA_ARCH_LIST="${TORCH_CUDA_ARCH_LIST:-12.0}"
export PYTHONPATH="$PROJECT_ROOT/src${PYTHONPATH:+:$PYTHONPATH}"

echo "=== RuleIR core-normalized KCL E2E start: $(date) ==="
echo "job=$SLURM_JOB_ID commit=$(git rev-parse HEAD) model=$MODEL_SNAPSHOT"
echo "run_root=$RUN_ROOT"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader

"$CLIENT_PYTHON" scripts/audit_rule_ir_core_prompts.py

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

VLLM_LOG="$SERVER_DIR/vllm.log"
"$VLLM_BIN" serve "$MODEL_SNAPSHOT" \
    --served-model-name "$SERVED_MODEL" \
    --host 127.0.0.1 --port "$PORT" --api-key "$LOCAL_API_KEY" \
    --tensor-parallel-size 1 --max-model-len 65536 --max-num-seqs 1 \
    --gpu-memory-utilization 0.90 --reasoning-parser gemma4 \
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
        tail -n 120 "$VLLM_LOG" >&2
        exit 1
    fi
    sleep 10
done
if [ "$READY" != 1 ]; then
    echo "vLLM did not become ready" >&2
    exit 1
fi

CASE_ARGS=()
if [ -n "${IDPR_CORE_E2E_CASES:-}" ]; then
    IFS=',' read -ra CASE_IDS <<< "$IDPR_CORE_E2E_CASES"
    for case_id in "${CASE_IDS[@]}"; do CASE_ARGS+=(--case-id "$case_id"); done
fi

"$CLIENT_PYTHON" scripts/run_rule_ir_core_kcl_e2e.py \
    --base-url "http://127.0.0.1:${PORT}" --model "$SERVED_MODEL" \
    --api-key "$LOCAL_API_KEY" --out-dir "$RUN_ROOT" "${CASE_ARGS[@]}"

cleanup
echo "report=$RUN_ROOT/report.json"
echo "=== RuleIR core-normalized KCL E2E end: $(date) ==="
