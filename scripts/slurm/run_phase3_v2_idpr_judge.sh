#!/bin/bash
# Score only the pinned v2 IDPR answers.  Baselines and current IDPR are not rerun.
#SBATCH --job-name=phase3_v2_idpr_judge
#SBATCH --output=logs/phase3_v2_idpr_judge_%j.out
#SBATCH --error=logs/phase3_v2_idpr_judge_%j.err
#SBATCH --partition=gpu
#SBATCH --time=24:00:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=32G

set -euo pipefail

PROJECT_ROOT="/data5/jaehoonjeong/IDPR"
JUDGE_PYTHON="$PROJECT_ROOT/.venv/bin/python"
cd "$PROJECT_ROOT"
mkdir -p logs
test -x "$JUDGE_PYTHON"
test -s "$PROJECT_ROOT/.env"
test -s "$PROJECT_ROOT/experiments/results/phase3_v2_final_59/idpr_nsn_outputs.jsonl"
test -s "$PROJECT_ROOT/experiments/results/phase3_v2_final_59/generation_manifest.json"
test "$(sha256sum scripts/run_phase3_llm_judge.py | cut -d' ' -f1)" = \
    "40eaf4b7ad92b1ec7e52ec27e21fdc40af515e5fdfbc6f63a35ab376bfea29ac"
"$JUDGE_PYTHON" -c 'from dotenv import dotenv_values; values=dotenv_values(".env"); assert str(values.get("SKIML_API_KEY", "")).strip(), "SKIML_API_KEY missing"'
"$JUDGE_PYTHON" -c 'import json; from pathlib import Path; rows=[json.loads(x) for x in Path("experiments/results/phase3_v2_final_59/idpr_nsn_outputs.jsonl").read_text(encoding="utf-8").splitlines() if x.strip()]; manifest=json.loads(Path("experiments/results/phase3_v2_final_59/generation_manifest.json").read_text(encoding="utf-8")); assert len(rows)==59; assert manifest.get("status")=="complete"; print("judge preflight: 59 answers, complete manifest")'
export IDPR_TESTED_CODE_COMMIT="73133164655548f3f5636d6a96f4cea969063936+gemini-judge-40eaf4b7ad92"

echo "=== Phase-3 v2 IDPR-only Gemini judge start: $(date) ==="
echo "job=$SLURM_JOB_ID dependency=${SLURM_JOB_DEPENDENCY:-missing} excluded_case=kcl_criminal_r11_p1_q4"

"$JUDGE_PYTHON" scripts/run_phase3_llm_judge.py \
    --model gemini/gemini-2.5-flash \
    --methods-manifest data/eval/phase3_method_outputs_v2_idpr.json \
    --method-id idpr_nsn_v2 \
    --exclude-case-id kcl_criminal_r11_p1_q4 \
    --concurrency 1 \
    --timeout-seconds 300 \
    --max-tokens 16384 \
    --reasoning-effort low \
    --contract-attempts 6 \
    --api-retries 0 \
    --gemini-safety-threshold OFF \
    --cache-dir .cache/phase3_v2_idpr_judge \
    --out experiments/results/phase3_v2_idpr_judge/judgments.jsonl \
    --summary experiments/results/phase3_v2_idpr_judge/summary.json \
    --manifest experiments/results/phase3_v2_idpr_judge/manifest.json

echo "=== Phase-3 v2 IDPR-only Gemini judge end: $(date) ==="
