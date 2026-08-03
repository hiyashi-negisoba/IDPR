#!/bin/bash
#SBATCH --job-name=phase3_v5_e2e
#SBATCH --output=logs/phase3_v5_e2e_%j.out
#SBATCH --error=logs/phase3_v5_e2e_%j.err
#SBATCH --time=06:00:00
#SBATCH --cpus-per-task=2
#SBATCH --gres=gpu:PRO6000:1
#SBATCH --mem=32G

# Full two-smoke regeneration for v5.  Runtime paths match the successful Phase-3
# jobs exactly.  The source hashes pin the uncommitted v5 patch because compute nodes
# do not expose git and a queued job must not silently consume later workspace edits.

set -euo pipefail

MAIN_ROOT="/data5/jaehoonjeong/IDPR"
PYTHON_BIN="/data5/jaehoonjeong/miniconda3/envs/inv_ass_env/bin/python"
VLLM_BIN="/data5/jaehoonjeong/miniconda3/envs/inv_ass_env/bin/vllm"
MODEL_SNAPSHOT="/data5/jaehoonjeong/.cache/huggingface/hub/models--google--gemma-4-26B-A4B-it/snapshots/01e5b3ee840d3a9e0b0b493c593e85398a30ef75"
SERVED_MODEL="idpr-gemma-4-26b-a4b"
SOURCE_FINGERPRINT="e5a10440bfb19c7ddd89f820b36d4437e27c8ce376e9ed221c1b20de186a5e13"

verify_hash() {
    local expected="$1"
    local relative_path="$2"
    test "$(sha256sum "$MAIN_ROOT/$relative_path" | cut -d' ' -f1)" = "$expected"
}

cd "$MAIN_ROOT"
verify_hash 0bb67b79fd8b899a7f534c86d7ba94b18496a108ff82dea8cb433313493ec6e6 data/smoke/phase3_e2e_inventory.jsonl
verify_hash af0d50a3a79df83e2f66d860fea6988105fe18dfd5890ef4bc209503b64f5207 data/smoke/phase3_e2e_rubrics.json
verify_hash d84a91690ab30b7b60a236c1383f8da6a2fe7fc6d273d784686c2c4a6369579b src/idpr/candidates.py
verify_hash 56f1ad743dc869df048c0d7996502ae647238a28cc63bf9c0911b549c0c454f8 src/idpr/neural/article_select.py
verify_hash ab76eac3041b43902bfc10bcea7c9db5ef435aad127d5bd048a8ef2ab628d9ce src/idpr/neural/fact_graph.py
verify_hash 0570e703ee7f64e2c9dc2cd3656fe844bb42db924edfa90f9cca987b31d4d307 src/idpr/issue_pipeline.py
verify_hash 638caae8d52c5aab364c2144634f073546c1d9db2ceb02c05cd799a2adc4b3a4 src/idpr/generation/issue_answer.py
verify_hash 60eb78fcbd988499ef1b1b48260336a786dd520951cfaf5a2c6f8a8a2039a065 scripts/run_l0_candidates.py
verify_hash 4c61c1afb7c3b20356ddbabdd9539341ca716376835808d61589beae331ee1ff prompts/issue_long_form_generate.md
verify_hash 47de7db1218844e104b05a6ccae854f9e4e1c29c4cab35da1d7da4cf1d367d62 scripts/report_phase3_candidate_lifecycle.py
verify_hash f69e68a75e0e11a098160ca2825b6fbe9e82bfb09346e165ae89cb7b0f8427bb scripts/verify_phase3_v5_e2e.py
verify_hash eb5f2e166baff7064b41fd59688cbccd95eae54e1a8ea0834af7e03dc9b4799d scripts/slurm/run_phase3_e2e_smoke.sh
test -x "$PYTHON_BIN"
test -x "$VLLM_BIN"
test -d "$MODEL_SNAPSHOT"

export IDPR_PROJECT_ROOT="$MAIN_ROOT"
export IDPR_PYTHON="$PYTHON_BIN"
export IDPR_VLLM_BIN="$VLLM_BIN"
export IDPR_MODEL_SOURCE="$MODEL_SNAPSHOT"
export IDPR_SERVED_MODEL="$SERVED_MODEL"
export IDPR_API_KEY=local-idpr
export IDPR_HF_HOME="/data5/jaehoonjeong/.cache/huggingface"
export IDPR_TESTED_CODE_COMMIT="73133164655548f3f5636d6a96f4cea969063936+v5-${SOURCE_FINGERPRINT}"
export IDPR_FREEZE_ROOT="$MAIN_ROOT/experiments/results/phase3_v5_e2e_${SLURM_JOB_ID}"
export IDPR_TOP_K_ARTICLES=10
export IDPR_PIPELINE_VERSION=v5_p0_p1

bash scripts/slurm/run_phase3_e2e_smoke.sh
"$CLIENT_PYTHON" scripts/report_phase3_candidate_lifecycle.py \
    --run-root "$IDPR_FREEZE_ROOT" \
    --out "$IDPR_FREEZE_ROOT/candidate_lifecycle_report.json"
"$CLIENT_PYTHON" scripts/verify_phase3_v5_e2e.py \
    --run-root "$IDPR_FREEZE_ROOT" \
    --out "$IDPR_FREEZE_ROOT/v5_acceptance.json"

echo "run_root=$IDPR_FREEZE_ROOT"
