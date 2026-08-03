#!/bin/bash
# Gemini responseJsonSchema 및 의미 계약 수리 경로를 실제 원격 API에서 검증한다.
# API는 Slurm compute node에서만 호출한다.
#SBATCH --job-name=p3_judge_schema_smoke
#SBATCH --output=logs/phase3_judge_schema_smoke_%j.out
#SBATCH --error=logs/phase3_judge_schema_smoke_%j.err
#SBATCH --partition=gpu
#SBATCH --time=01:00:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=32G
# (의도적으로 --gres=gpu 없음: judge는 원격 Gemini API를 사용한다)

set -euo pipefail

source "${IDPR_PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}/scripts/slurm/_env.sh"
cd "$PROJECT_ROOT"
mkdir -p logs experiments/results/phase3_judge/schema_smoke

JUDGE_PYTHON="${IDPR_JUDGE_PYTHON:-$PROJECT_ROOT/.venv/bin/python}"
if [ ! -x "$JUDGE_PYTHON" ]; then
    echo "judge Python is not executable: $JUDGE_PYTHON" >&2
    exit 2
fi

COMMON_ARGS=(
    --model gemini/gemini-2.5-flash
    --concurrency 1
    --timeout-seconds 300
    --max-tokens 16384
    --reasoning-effort low
    --contract-attempts 6
    --api-retries 0
    --gemini-safety-threshold OFF
)

echo "=== Phase-3 schema smoke start: $(date) ==="
echo "job=${SLURM_JOB_ID:-NA} host=$(hostname) cpus=${SLURM_CPUS_PER_TASK:-NA} mem=32G gpu=none"

"$JUDGE_PYTHON" scripts/run_phase3_llm_judge.py \
    "${COMMON_ARGS[@]}" \
    --method-id acal \
    --case-id kcl_criminal_r12_p1_q3 \
    --out experiments/results/phase3_judge/schema_smoke/enum.jsonl \
    --summary experiments/results/phase3_judge/schema_smoke/enum_summary.json \
    --manifest experiments/results/phase3_judge/schema_smoke/enum_manifest.json \
    --cache-dir .cache/phase3_judge_schema_smoke/enum \
    --overwrite

"$JUDGE_PYTHON" scripts/run_phase3_llm_judge.py \
    "${COMMON_ARGS[@]}" \
    --method-id fol_autoformalizer_solver \
    --case-id kcl_criminal_r12_p1_q1 \
    --out experiments/results/phase3_judge/schema_smoke/quote.jsonl \
    --summary experiments/results/phase3_judge/schema_smoke/quote_summary.json \
    --manifest experiments/results/phase3_judge/schema_smoke/quote_manifest.json \
    --cache-dir .cache/phase3_judge_schema_smoke/quote \
    --overwrite

"$JUDGE_PYTHON" -c 'import json,sys; paths=sys.argv[1:]; bad=[p for p in paths if json.load(open(p, encoding="utf-8"))["status"] != "complete"]; print("smoke_manifests=" + ",".join(paths)); raise SystemExit(bool(bad))' \
    experiments/results/phase3_judge/schema_smoke/enum_manifest.json \
    experiments/results/phase3_judge/schema_smoke/quote_manifest.json

echo "=== Phase-3 schema smoke end: $(date) ==="
