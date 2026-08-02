#!/bin/bash
#SBATCH --job-name=phase3_reconcile
#SBATCH --output=logs/phase3_reconcile_%j.out
#SBATCH --error=logs/phase3_reconcile_%j.err
#SBATCH --time=02:00:00
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:PRO6000:1
#SBATCH --mem=32G

# Runs two generic upstream admission policies against the frozen two-smoke candidates.
# It does not run Call 2 or modify the frozen output tree.

set -euo pipefail
source "${IDPR_PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}/scripts/slurm/_env.sh"

FREEZE_ROOT="${IDPR_FREEZE_ROOT:-$PROJECT_ROOT/experiments/results/phase3_e2e_freeze_v1}"
RUN_ROOT="${IDPR_RECONCILE_ROOT:-$PROJECT_ROOT/experiments/results/phase3_article_reconcile_${SLURM_JOB_ID}}"
export IDPR_RECONCILE_ACTUAL_ROOT="$RUN_ROOT"
INVENTORY="$PROJECT_ROOT/data/smoke/phase3_e2e_inventory.jsonl"
SELECTION="$FREEZE_ROOT/article_selection.jsonl"
CANDIDATES="$FREEZE_ROOT/l0_candidates.jsonl"
SERVER_LOG="$RUN_ROOT/vllm.log"

export TOKENIZERS_PARALLELISM=false
export VLLM_USE_FLASHINFER_SAMPLER=0
export JE_ARROW_MALLOC_CONF="${JE_ARROW_MALLOC_CONF:-background_thread:false}"
export TORCH_CUDA_ARCH_LIST="${TORCH_CUDA_ARCH_LIST:-12.0}"
export PYTHONPATH="$PROJECT_ROOT/src${PYTHONPATH:+:$PYTHONPATH}"

cd "$PROJECT_ROOT"
mkdir -p logs "$RUN_ROOT"
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
    --max-model-len 32768 \
    --max-num-seqs 1 \
    --gpu-memory-utilization 0.90 \
    --reasoning-parser gemma4 \
    --structured-outputs-config '{"backend":"guidance","disable_any_whitespace":true}' \
    > "$SERVER_LOG" 2>&1 &
VLLM_PID=$!

for _ in $(seq 1 180); do
    if "$CLIENT_PYTHON" -c \
        "import json,urllib.request; r=urllib.request.Request('http://127.0.0.1:${PORT}/v1/models',headers={'Authorization':'Bearer ${LOCAL_API_KEY}'}); d=json.load(urllib.request.urlopen(r,timeout=5)); assert any(m['id']=='${SERVED_MODEL}' for m in d['data'])" \
        2>/dev/null; then
        break
    fi
    if ! kill -0 "$VLLM_PID" 2>/dev/null; then
        tail -n 120 "$SERVER_LOG" >&2
        exit 1
    fi
    sleep 10
done

for POLICY in article_reconcile article_reconcile_precision; do
    mkdir -p "$RUN_ROOT/$POLICY"
    "$CLIENT_PYTHON" scripts/run_article_reconcile.py \
        --base-url "http://127.0.0.1:${PORT}" \
        --model "$SERVED_MODEL" \
        --api-key "$LOCAL_API_KEY" \
        --inventory "$INVENTORY" \
        --selection "$SELECTION" \
        --candidates "$CANDIDATES" \
        --system-prompt "$POLICY" \
        --out "$RUN_ROOT/$POLICY/reconciliation.jsonl" \
        --l0-out "$RUN_ROOT/$POLICY/l0_candidates.jsonl"
done

"$CLIENT_PYTHON" - <<'PY'
import hashlib, json, os
from pathlib import Path
root = Path(os.environ["IDPR_RECONCILE_ACTUAL_ROOT"])
files = sorted(path for path in root.rglob("*") if path.is_file())
payload = {
    "slurm_job_id": os.environ["SLURM_JOB_ID"],
    "git_sha": os.popen("git rev-parse HEAD").read().strip(),
    "model": os.environ.get("IDPR_SERVED_MODEL", "google/gemma-4-26B-A4B-it"),
    "files": {
        str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in files if path.name != "manifest.json"
    },
}
(root / "manifest.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
PY

echo "run_root=$RUN_ROOT"
