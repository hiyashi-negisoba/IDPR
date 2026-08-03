#!/bin/bash
# Resume only Call 2/3 for the pinned V2 59-case run after job 218654 completed
# Call 1, article selection, and L0.  Existing valid per-case answers are retained.
#SBATCH --job-name=phase3_v2_resume23
#SBATCH --output=logs/phase3_v2_resume23_%j.out
#SBATCH --error=logs/phase3_v2_resume23_%j.err
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
PYTHON_BIN="/data5/jaehoonjeong/miniconda3/envs/inv_ass_env/bin/python"
VLLM_BIN="/data5/jaehoonjeong/miniconda3/envs/inv_ass_env/bin/vllm"
MODEL_SNAPSHOT="/data5/jaehoonjeong/.cache/huggingface/hub/models--google--gemma-4-26B-A4B-it/snapshots/01e5b3ee840d3a9e0b0b493c593e85398a30ef75"
SERVED_MODEL="idpr-gemma-4-26b-a4b"
LOCAL_API_KEY="local-idpr"
MAIN_SCLI="$MAIN_ROOT/tools/scallop/scli-0.2.4-linux-x86_64"
V2_SCLI="$V2_ROOT/tools/scallop/scli-0.2.4-linux-x86_64"

FACT_GRAPHS="$RUN_ROOT/fact_graphs.jsonl"
CANDIDATES="$RUN_ROOT/l0_candidates.jsonl"
CASES="$RUN_ROOT/cases"
OUTPUT="$RUN_ROOT/idpr_nsn_outputs.jsonl"
SERVER_DIR="$RUN_ROOT/server"

verify_hash() {
    local expected="$1"
    local path="$2"
    test "$(sha256sum "$path" | cut -d' ' -f1)" = "$expected"
}

cd "$MAIN_ROOT"
mkdir -p logs "$CASES" "$SERVER_DIR"
verify_hash 01e286646fdc0298a553af26cffa7dc324d050bcdef773d28026966dfdf5af28 "$INVENTORY"
verify_hash 7b91d1d82403b5a2e100e649931420ee8b1cc540dc0a72b6d6207fc19ec3d1fe "$FACT_GRAPHS"
verify_hash e6d0667399469e4e6f680a6f2fe538eea9fbf9a6fa7b64ef6b932a859f66060e "$RUN_ROOT/article_selection.jsonl"
verify_hash c33b7a859348764151459f870c669e427207f7c6b6939ca75019ffd24c2f318f "$CANDIDATES"
verify_hash 056a8d5f2482feca25a3542bf4cf3c99fba965e9b8eb1d3f80ccb97d8f5380b6 "$RUN_ROOT/l0_report.json"
verify_hash 5b02657a5f61d654be1626c32fba8a6e6366a03d80a8ed30e85bdc1be1876e6d "$V2_ROOT/scripts/run_issue_pipeline_batch.py"
verify_hash 8c5ec86fcdb0dbd55698eff7570ac7396d0b0878e601207f868d61f9d6482b9a "$MAIN_SCLI"
test -x "$PYTHON_BIN"
test -x "$VLLM_BIN"
test -d "$MODEL_SNAPSHOT"

# The native runtime is intentionally not tracked by git, so the historical worktree
# contains its README but not the executable.  Link the byte-identical pinned binary
# from the main deployment and verify it again at the path V2 resolves by default.
if [ ! -e "$V2_SCLI" ]; then
    ln -s "$MAIN_SCLI" "$V2_SCLI"
fi
verify_hash 8c5ec86fcdb0dbd55698eff7570ac7396d0b0878e601207f868d61f9d6482b9a "$V2_SCLI"
test -x "$V2_SCLI"

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
    PORT=$("$PYTHON_BIN" -c 'import socket; s=socket.socket(); s.bind(("127.0.0.1",0)); print(s.getsockname()[1]); s.close()')
    unset CUDA_HOME CUDA_PATH FLASHINFER_CUDA_ARCH_LIST FLASHINFER_WORKSPACE_BASE
    local log="$SERVER_DIR/call2_call3_resume_${SLURM_JOB_ID}.log"
    "$VLLM_BIN" serve "$MODEL_SNAPSHOT" \
        --served-model-name "$SERVED_MODEL" \
        --host 127.0.0.1 --port "$PORT" --api-key "$LOCAL_API_KEY" \
        --tensor-parallel-size 1 --max-model-len 65536 --max-num-seqs 1 \
        --gpu-memory-utilization 0.90 --reasoning-parser gemma4 \
        --structured-outputs-config '{"backend":"guidance","disable_any_whitespace":true}' \
        > "$log" 2>&1 &
    VLLM_PID=$!
    for _ in $(seq 1 180); do
        if "$PYTHON_BIN" -c "import json,urllib.request; r=urllib.request.Request('http://127.0.0.1:${PORT}/v1/models',headers={'Authorization':'Bearer ${LOCAL_API_KEY}'}); d=json.load(urllib.request.urlopen(r,timeout=5)); assert any(m['id']=='${SERVED_MODEL}' for m in d['data'])" 2>/dev/null; then
            return 0
        fi
        kill -0 "$VLLM_PID" 2>/dev/null || { tail -n 120 "$log" >&2; return 1; }
        sleep 10
    done
    echo "vLLM did not become ready" >&2
    return 1
}

echo "=== Phase-3 v2 Call 2/3 resume start: $(date) ==="
echo "job=$SLURM_JOB_ID parent_job=218654 source_commit=$V2_COMMIT"
echo "preserved=fact_graphs,article_selection,l0_candidates"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader

TOTAL_START=$(date +%s)
start_vllm
CALL23_START=$(date +%s)
cd "$V2_ROOT"
"$PYTHON_BIN" scripts/run_issue_pipeline_batch.py \
    --base-url "http://127.0.0.1:${PORT}" --model "$SERVED_MODEL" \
    --api-key "$LOCAL_API_KEY" --inventory "$INVENTORY" \
    --fact-graphs "$FACT_GRAPHS" --candidates "$CANDIDATES" \
    --run-dir "$CASES" --out "$OUTPUT" \
    --call2-max-tokens 12288 --call3-max-tokens 16384 \
    --no-cache
CALL23_SECONDS=$(( $(date +%s) - CALL23_START ))
cleanup
TOTAL_SECONDS=$(( $(date +%s) - TOTAL_START ))

"$PYTHON_BIN" "$MAIN_ROOT/scripts/write_phase3_v2_generation_manifest.py" \
    --run-root "$RUN_ROOT" --inventory "$INVENTORY" --output "$OUTPUT" \
    --model "$SERVED_MODEL" --model-snapshot "$MODEL_SNAPSHOT" \
    --source-root "$V2_ROOT" --source-commit "$V2_COMMIT" \
    --slurm-job-id "$SLURM_JOB_ID" \
    --stage-seconds "upstream_job_218654_elapsed=1518" \
    --stage-seconds "call2_call3_resume=$CALL23_SECONDS" \
    --stage-seconds "resume_total=$TOTAL_SECONDS"

echo "output=$OUTPUT"
echo "=== Phase-3 v2 Call 2/3 resume end: $(date) ==="
