#!/bin/bash
#SBATCH --job-name=phase3_sp_light
#SBATCH --output=logs/phase3_sp_light_%j.out
#SBATCH --error=logs/phase3_sp_light_%j.err
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:PRO6000:1
#SBATCH --mem=32G

set -euo pipefail

MAIN_ROOT="/data5/jaehoonjeong/IDPR"
PROJECT_ROOT="$MAIN_ROOT/.worktrees/phase3_special_part_light"
UPSTREAM_ROOT="$MAIN_ROOT/experiments/results/phase3_v2_final_59"
INVENTORY="$MAIN_ROOT/experiments/results/phase3_final_59/final_59_inventory.jsonl"
FACT_GRAPHS="$UPSTREAM_ROOT/fact_graphs.jsonl"
BROAD_CANDIDATES="$UPSTREAM_ROOT/l0_candidates.jsonl"
PYTHON_BIN="/data5/jaehoonjeong/miniconda3/envs/inv_ass_env/bin/python"
VLLM_BIN="/data5/jaehoonjeong/miniconda3/envs/inv_ass_env/bin/vllm"
MODEL_SNAPSHOT="/data5/jaehoonjeong/.cache/huggingface/hub/models--google--gemma-4-26B-A4B-it/snapshots/01e5b3ee840d3a9e0b0b493c593e85398a30ef75"
SERVED_MODEL="idpr-gemma-4-26b-a4b"
LOCAL_API_KEY="local-idpr"

if [ "${IDPR_FULL:-0}" = 1 ]; then
    RUN_ROOT="$MAIN_ROOT/experiments/results/phase3_special_part_light_59"
    CASE_ARGS=()
else
    RUN_ROOT="$MAIN_ROOT/experiments/results/phase3_special_part_light_smoke"
    CASE_ARGS=(--case-id kcl_criminal_r10_p1_q1_na --case-id kcl_criminal_r10_p1_q2)
fi
PLANNED_CANDIDATES="$RUN_ROOT/special_part_candidates.jsonl"
CASES="$RUN_ROOT/cases"
OUTPUT="$RUN_ROOT/idpr_special_part_light_outputs.jsonl"
SERVER_DIR="$RUN_ROOT/server"

test -x "$PYTHON_BIN"
test -x "$VLLM_BIN"
test -d "$MODEL_SNAPSHOT"
test -s "$INVENTORY"
test -s "$FACT_GRAPHS"
test -s "$BROAD_CANDIDATES"

export TOKENIZERS_PARALLELISM=false
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export VLLM_USE_FLASHINFER_SAMPLER=0
export JE_ARROW_MALLOC_CONF="${JE_ARROW_MALLOC_CONF:-background_thread:false}"
export TORCH_CUDA_ARCH_LIST="${TORCH_CUDA_ARCH_LIST:-12.0}"
export HF_HOME="/data5/jaehoonjeong/.cache/huggingface"
export PYTHONPATH="$PROJECT_ROOT/src"

cd "$PROJECT_ROOT"
mkdir -p "$RUN_ROOT" "$CASES" "$SERVER_DIR" logs

PORT=$("$PYTHON_BIN" -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1",0)); print(s.getsockname()[1]); s.close()')
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
VLLM_LOG="$SERVER_DIR/vllm_${SLURM_JOB_ID}.log"
"$VLLM_BIN" serve "$MODEL_SNAPSHOT" \
    --served-model-name "$SERVED_MODEL" \
    --host 127.0.0.1 --port "$PORT" --api-key "$LOCAL_API_KEY" \
    --tensor-parallel-size 1 --max-model-len 65536 --max-num-seqs 1 \
    --gpu-memory-utilization 0.90 --reasoning-parser gemma4 \
    --structured-outputs-config '{"backend":"guidance","disable_any_whitespace":true}' \
    > "$VLLM_LOG" 2>&1 &
VLLM_PID=$!

for _ in $(seq 1 180); do
    if "$PYTHON_BIN" -c "import json,urllib.request; r=urllib.request.Request('http://127.0.0.1:${PORT}/v1/models',headers={'Authorization':'Bearer ${LOCAL_API_KEY}'}); d=json.load(urllib.request.urlopen(r,timeout=5)); assert any(m['id']=='${SERVED_MODEL}' for m in d['data'])" 2>/dev/null; then
        READY=1
        break
    fi
    kill -0 "$VLLM_PID" 2>/dev/null || { tail -n 120 "$VLLM_LOG" >&2; exit 1; }
    sleep 10
done
test "${READY:-0}" = 1

echo "=== special-part light start: $(date) ==="
echo "job=$SLURM_JOB_ID branch=experiment/phase3-special-part-light-20260803 full=${IDPR_FULL:-0}"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader

"$PYTHON_BIN" scripts/run_special_part_plan.py \
    --base-url "http://127.0.0.1:${PORT}" --model "$SERVED_MODEL" \
    --api-key "$LOCAL_API_KEY" --inventory "$INVENTORY" \
    --broad-candidates "$BROAD_CANDIDATES" --out "$PLANNED_CANDIDATES" \
    --work-dir "$RUN_ROOT/planner_cases" \
    --max-tokens 4096 --timeout-seconds 7200 \
    "${CASE_ARGS[@]}"

"$PYTHON_BIN" scripts/run_issue_pipeline_batch.py \
    --base-url "http://127.0.0.1:${PORT}" --model "$SERVED_MODEL" \
    --api-key "$LOCAL_API_KEY" --inventory "$INVENTORY" \
    --fact-graphs "$FACT_GRAPHS" --candidates "$PLANNED_CANDIDATES" \
    --run-dir "$CASES" --out "$OUTPUT" --special-part-light \
    --call2-max-tokens 12288 --call3-max-tokens 16384 --no-cache \
    "${CASE_ARGS[@]}"

"$PYTHON_BIN" -c 'import json,sys; from pathlib import Path; p=Path(sys.argv[1]); rows=[json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]; assert rows and all(r.get("generated_response", "").strip() for r in rows); print({"answers":len(rows),"routes":{r.get("route","article_local") for r in rows}})' "$OUTPUT"

cleanup
echo "output=$OUTPUT"
echo "=== special-part light end: $(date) ==="
