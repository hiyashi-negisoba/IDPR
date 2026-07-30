#!/bin/bash
#SBATCH --job-name=baselines_eval_vllm
#SBATCH --output=logs/baselines_eval_vllm_%j.log
#SBATCH --error=logs/baselines_eval_vllm_%j.err
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:PRO6000:1
#SBATCH --mem=32G

set -euo pipefail

echo "=================================================================="
echo "🚀 Starting 7 Baselines Sequential Evaluation Slurm Job"
echo "Date: $(date -u)"
echo "Host: $(hostname)"
echo "CUDA_VISIBLE_DEVICES: ${CUDA_VISIBLE_DEVICES:-N/A}"
echo "=================================================================="

PROJECT_ROOT="/data5/jaehoonjeong/IDPR"
CLIENT_PYTHON="/data5/jaehoonjeong/miniconda3/bin/python"
VLLM_BIN="/data5/jaehoonjeong/miniconda3/envs/inv_ass_env/bin/vllm"
MODEL_SNAPSHOT="/data5/jaehoonjeong/.cache/huggingface/hub/models--google--gemma-4-26B-A4B-it/snapshots/01e5b3ee840d3a9e0b0b493c593e85398a30ef75"
SERVED_MODEL="idpr-gemma-4-26b-a4b"
LOCAL_API_KEY="local-idpr"

export HF_HOME="/data5/jaehoonjeong/.cache/huggingface"
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export TOKENIZERS_PARALLELISM=false
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export VLLM_USE_FLASHINFER_SAMPLER=0
export JE_ARROW_MALLOC_CONF="${JE_ARROW_MALLOC_CONF:-background_thread:false}"
export TORCH_CUDA_ARCH_LIST="12.0"

cd "$PROJECT_ROOT"
mkdir -p logs experiments/results

export PYTHONPATH="${PROJECT_ROOT}/src:${PYTHONPATH:-}"

# 1. Dynamic Port Allocation
PORT=$("$CLIENT_PYTHON" -c \
    'import socket; s=socket.socket(); s.bind(("127.0.0.1", 0)); print(s.getsockname()[1]); s.close()')
unset CUDA_HOME CUDA_PATH FLASHINFER_CUDA_ARCH_LIST FLASHINFER_WORKSPACE_BASE
VLLM_PID=""

# EXPORT VLLM_PORT for python baseline monkey-patches to dynamically connect to the correct port
export VLLM_PORT="${PORT}"

cleanup() {
    if [ -n "$VLLM_PID" ]; then
        echo "[cleanup] stopping vLLM pid=$VLLM_PID"
        kill "$VLLM_PID" 2>/dev/null || true
        wait "$VLLM_PID" 2>/dev/null || true
    fi
}
trap cleanup EXIT

echo "starting job-local vLLM Server on port $PORT..."
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
    > "${PROJECT_ROOT}/logs/vllm_baselines_server_${SLURM_JOB_ID}.log" 2>&1 &

VLLM_PID=$!

echo "Waiting for vLLM server to become ready at http://127.0.0.1:${PORT}/v1/models..."
READY=0
# Deployed on NFS storage where model loading can take up to 25 minutes.
# Increase wait time to 600 loops * 5 seconds = 3000 seconds (50 minutes) to avoid premature timeout.
for i in $(seq 1 600); do
    if "$CLIENT_PYTHON" -c \
        "import json,urllib.request; r=urllib.request.Request('http://127.0.0.1:${PORT}/v1/models',headers={'Authorization':'Bearer ${LOCAL_API_KEY}'}); d=json.load(urllib.request.urlopen(r,timeout=5)); assert any(m['id']=='${SERVED_MODEL}' for m in d['data'])" \
        2>/dev/null; then
        READY=1
        echo "✅ vLLM Server is READY after $((i*5)) seconds!"
        break
    fi
    sleep 5
done

if [ "$READY" != 1 ]; then
    echo "❌ Error: vLLM Server failed to start."
    exit 1
fi

PYTHON_BIN="/data5/jaehoonjeong/miniconda3/envs/inv_ass_env/bin/python"

echo "Executing 7 Baselines sequentially on Live Gemma 4 Model..."

# Baseline 1: Vanilla LLM
echo "▶ Running vanilla_zero_shot..."
$PYTHON_BIN scripts/run_baselines_experiment.py \
    --baseline vanilla_zero_shot \
    --vllm-url "http://127.0.0.1:${PORT}" \
    --vllm-model "${SERVED_MODEL}"

# Baseline 2: Chain-of-Thought
echo "▶ Running chain_of_thought..."
$PYTHON_BIN scripts/run_baselines_experiment.py \
    --baseline chain_of_thought \
    --vllm-url "http://127.0.0.1:${PORT}" \
    --vllm-model "${SERVED_MODEL}"

# Baseline 3: Standard RAG (Precedents BM25)
echo "▶ Running standard_rag..."
$PYTHON_BIN scripts/run_baselines_experiment.py \
    --baseline standard_rag \
    --vllm-url "http://127.0.0.1:${PORT}" \
    --vllm-model "${SERVED_MODEL}"

# Baseline 4: LePREC (Unmodified Original)
echo "▶ Running leprec..."
$PYTHON_BIN scripts/run_baselines_experiment.py \
    --baseline leprec \
    --vllm-url "http://127.0.0.1:${PORT}" \
    --vllm-model "${SERVED_MODEL}"

# Baseline 5: ACAL (Unmodified Original)
echo "▶ Running acal..."
$PYTHON_BIN scripts/run_baselines_experiment.py \
    --baseline acal \
    --vllm-url "http://127.0.0.1:${PORT}" \
    --vllm-model "${SERVED_MODEL}"

# Baseline 6: LegalChainReasoner (Unmodified Original)
echo "▶ Running legal_chain_reasoner..."
$PYTHON_BIN scripts/run_baselines_experiment.py \
    --baseline legal_chain_reasoner \
    --vllm-url "http://127.0.0.1:${PORT}" \
    --vllm-model "${SERVED_MODEL}"

# Baseline 7: FOL Autoformalizer + Solver
echo "▶ Running fol_autoformalizer_solver..."
$PYTHON_BIN scripts/run_baselines_experiment.py \
    --baseline fol_autoformalizer_solver \
    --vllm-url "http://127.0.0.1:${PORT}" \
    --vllm-model "${SERVED_MODEL}"

echo "7 Baselines live evaluation completed successfully!"
