#!/bin/bash
# P/N judge for the citation-mandate + conclusion-alignment pass revision
# (v2_idpr_p_v2_aligned_26 / v2_idpr_n_v2_aligned_26). Same underlying
# scripts/run_phase3_llm_judge.py invocation as the earlier defeated_by_state_fix run.
#
#SBATCH --job-name=phase3_judge_pn_v2_aligned
#SBATCH --output=logs/phase3_judge_pn_v2_aligned_%j.out
#SBATCH --error=logs/phase3_judge_pn_v2_aligned_%j.err
#SBATCH --partition=gpu
#SBATCH --time=4:00:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=16G

set -euo pipefail
cd /data5/jaehoonjeong/IDPR
mkdir -p logs

.venv/bin/python scripts/run_phase3_llm_judge.py \
    --model anthropic/claude-sonnet-4-6 \
    --backend sonnet \
    --sealed-inventory data/inventory/kcl_criminal_v1_draft.jsonl \
    --expected-cases 61 \
    --case-id-file .cache/phase3_substantive_law_case_lists/curated_26.txt \
    --method-id v2_idpr_p_v2_aligned_26 \
    --method-id v2_idpr_n_v2_aligned_26 \
    --paired-target-method-id v2_idpr_p_v2_aligned_26 \
    --concurrency 3 \
    --timeout-seconds 300 \
    --max-tokens 16384 \
    --reasoning-effort low \
    --contract-attempts 6 \
    --api-retries 2 \
    --out experiments/results/phase3_judge_sonnet_pn_v2_aligned/judgments.jsonl \
    --summary experiments/results/phase3_judge_sonnet_pn_v2_aligned/summary.json \
    --manifest experiments/results/phase3_judge_sonnet_pn_v2_aligned/manifest.json \
    --cache-dir .cache/phase3_judge_sonnet_pn_v2_aligned \
    --overwrite

echo "=== Phase-3 Sonnet P/N v2-aligned judge end: $(date) ==="
