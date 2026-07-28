#!/bin/bash
#SBATCH --job-name=kcl1730_e2e_vllm
#SBATCH --partition=gpu
#SBATCH --gres=gpu:PRO6000:1
#SBATCH --cpus-per-task=2
#SBATCH --mem=32G
#SBATCH --time=48:00:00
#SBATCH --output=/home/jaehoonjeong/data/IDPR/logs/kcl1730_e2e_vllm_%j.log
#SBATCH --error=/home/jaehoonjeong/data/IDPR/logs/kcl1730_e2e_vllm_%j.err

set -eo pipefail

echo "=================================================================="
echo "🚀 Starting KCL 1,730 E2E Neuro-Symbolic Pipeline Slurm Job"
echo "Date: $(date -u)"
echo "Host: $(hostname)"
echo "CUDA_VISIBLE_DEVICES: ${CUDA_VISIBLE_DEVICES:-N/A}"
echo "=================================================================="

PROJECT_ROOT="/home/jaehoonjeong/data/IDPR"
cd "${PROJECT_ROOT}"

mkdir -p logs data/e2e/output

export PYTHONPATH="${PROJECT_ROOT}/src:${PYTHONPATH:-}"

PORT=8000
MODEL_NAME="google/gemma-4-26B-A4B-it"

echo "[1/3] Starting job-local vLLM Server (${MODEL_NAME}) on port ${PORT}..."
vllm serve "${MODEL_NAME}" \
    --port "${PORT}" \
    --max-model-len 32768 \
    --gpu-memory-utilization 0.90 \
    --trust-remote-code > "${PROJECT_ROOT}/logs/vllm_server_${SLURM_JOB_ID}.log" 2>&1 &

VLLM_PID=$!
echo "vLLM Server launched with PID: ${VLLM_PID}"

cleanup() {
    echo "Cleaning up vLLM server PID: ${VLLM_PID}..."
    kill -9 "${VLLM_PID}" || true
}
trap cleanup EXIT

echo "Waiting for vLLM server to become ready at http://localhost:${PORT}/v1/models..."
for i in $(seq 1 120); do
    if curl -s "http://localhost:${PORT}/v1/models" | grep -q "${MODEL_NAME}"; then
        echo "✅ vLLM Server is READY!"
        break
    fi
    echo "Waiting for vLLM initialization (${i}/120)..."
    sleep 5
done

echo "[2/3] Executing Real Neural-Symbolic E2E Pipeline on Live Gemma 4 Model..."
python3 "${PROJECT_ROOT}/scripts/run_kcl_1730_e2e_pipeline.py" \
    --mode vllm \
    --base-url "http://localhost:${PORT}" \
    --model "${MODEL_NAME}" \
    --out-dir "${PROJECT_ROOT}/data/e2e/output"

echo "[3/3] KCL 1,730 Live Neural-Symbolic E2E Pipeline Completed Successfully!"
