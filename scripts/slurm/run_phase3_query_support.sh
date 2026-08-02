#!/bin/bash
#SBATCH --job-name=phase3_query_support
#SBATCH --output=logs/phase3_query_support_%j.out
#SBATCH --error=logs/phase3_query_support_%j.err
#SBATCH --time=02:00:00
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:PRO6000:1
#SBATCH --mem=32G

set -euo pipefail
source "${IDPR_PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}/scripts/slurm/_env.sh"

FREEZE_ROOT="${IDPR_FREEZE_ROOT:-$PROJECT_ROOT/experiments/results/phase3_e2e_freeze_v1}"
RUN_ROOT="${IDPR_QUERY_SUPPORT_ROOT:-$PROJECT_ROOT/experiments/results/phase3_query_support_${SLURM_JOB_ID}}"
export IDPR_QUERY_SUPPORT_ACTUAL_ROOT="$RUN_ROOT"
export PYTHONPATH="$PROJECT_ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
unset HF_HUB_OFFLINE TRANSFORMERS_OFFLINE

cd "$PROJECT_ROOT"
mkdir -p logs "$RUN_ROOT"
"$CLIENT_PYTHON" scripts/diagnostics/run_phase3_query_support.py \
    --fact-graphs "$FREEZE_ROOT/fact_graphs.jsonl" \
    --out "$RUN_ROOT/query_support.jsonl"

"$CLIENT_PYTHON" - <<'PY'
import hashlib, json, os, subprocess
from pathlib import Path
root = Path(os.environ["IDPR_QUERY_SUPPORT_ACTUAL_ROOT"])
path = root / "query_support.jsonl"
payload = {
    "slurm_job_id": os.environ["SLURM_JOB_ID"],
    "git_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], text=True).strip(),
    "dense_model": os.environ.get("IDPR_DENSE_MODEL", "google/embeddinggemma-300m"),
    "reranker_model": os.environ.get("IDPR_RERANKER_MODEL", "BAAI/bge-reranker-v2-m3"),
    "query_support_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
}
(root / "manifest.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
PY

echo "run_root=$RUN_ROOT"
