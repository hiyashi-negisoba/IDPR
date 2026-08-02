#!/bin/bash
#SBATCH --job-name=idpr_issue_retrieval
#SBATCH --output=logs/idpr_issue_retrieval_%j.out
#SBATCH --error=logs/idpr_issue_retrieval_%j.err
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:PRO6000:1
#SBATCH --mem=32G

set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/_env.sh"
FACT_GRAPHS="$PROJECT_ROOT/data/eval/fact_graphs.jsonl"
SELECTION="$PROJECT_ROOT/data/eval/article_selection.jsonl"
REPORT="$PROJECT_ROOT/data/eval/issue_retrieval_l0_report.json"

export TOKENIZERS_PARALLELISM=false
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
export PYTHONPATH="$PROJECT_ROOT/src"
unset HF_HUB_OFFLINE TRANSFORMERS_OFFLINE

cd "$PROJECT_ROOT"
mkdir -p logs data/eval
echo "=== issue-first L0 retrieval start: $(date) ==="
echo "job=$SLURM_JOB_ID host=$(hostname)"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader

"$CLIENT_PYTHON" scripts/run_issue_retrieval_l0_report.py --fact-graphs "$FACT_GRAPHS" --selection "$SELECTION" --out "$REPORT"

echo "report=$REPORT"
echo "=== issue-first L0 retrieval end: $(date) ==="
