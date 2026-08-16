#!/bin/bash
#SBATCH --job-name=phase3_judge_pn_retry
#SBATCH --output=logs/phase3_judge_pn_dbsfix_retry_%j.out
#SBATCH --error=logs/phase3_judge_pn_dbsfix_retry_%j.err
#SBATCH --partition=gpu
#SBATCH --time=2:00:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=16G

set -euo pipefail
cd /data5/jaehoonjeong/IDPR

.venv/bin/python scripts/run_phase3_llm_judge.py \
    --model anthropic/claude-sonnet-4-6 \
    --backend sonnet \
    --sealed-inventory data/inventory/kcl_criminal_v1_draft.jsonl \
    --expected-cases 61 \
    --case-id-file .cache/phase3_substantive_law_case_lists/curated_26.txt \
    --method-id v2_idpr_p_defeated_by_state_fix_26 \
    --method-id v2_idpr_n_defeated_by_state_fix_26 \
    --paired-target-method-id v2_idpr_p_defeated_by_state_fix_26 \
    --concurrency 2 \
    --timeout-seconds 300 \
    --max-tokens 16384 \
    --reasoning-effort low \
    --contract-attempts 6 \
    --api-retries 2 \
    --out experiments/results/phase3_judge_sonnet_pn_defeated_by_state_fix/judgments.jsonl \
    --summary experiments/results/phase3_judge_sonnet_pn_defeated_by_state_fix/summary.json \
    --manifest experiments/results/phase3_judge_sonnet_pn_defeated_by_state_fix/manifest.json \
    --cache-dir .cache/phase3_judge_sonnet_pn_defeated_by_state_fix
