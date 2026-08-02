#!/bin/bash
# 재산죄 RuleIR 생성 + sol 비평 — 죄명 단위 10개(친족상도례는 A4로 이월).
# preflight 10항목 사용자 승인(2026-07-26) 후 실행. 러너가 승인 게이트를 다시 확인하고,
# 이미 만들어진 후보는 skip하므로 재제출해도 이중 지출이 없다.
# terra/sol = 원격 SKIML API라 로컬 GPU 불필요 → CPU-only (gpu 파티션, --gres 없음).
#
#SBATCH --job-name=idpr_prop_rule_ir
#SBATCH --output=logs/idpr_prop_rule_ir_%j.out
#SBATCH --error=logs/idpr_prop_rule_ir_%j.err
#SBATCH --partition=gpu
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=32G
# (의도적으로 --gres=gpu 없음: API 생성은 로컬 GPU를 쓰지 않는다)

set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/_env.sh"
cd "$PROJECT_ROOT"
mkdir -p logs

RUN_ID="${IDPR_RULE_IR_RUN_ID:-property_v1}"
MAX_USD="${IDPR_RULE_IR_MAX_USD:-6}"
STAGE="${IDPR_RULE_IR_STAGE:-all}"

echo "=== IDPR property RuleIR start: $(date) ==="
echo "job=${SLURM_JOB_ID:-NA} host=$(hostname) cpus=${SLURM_CPUS_PER_TASK:-NA} gpu=none"
echo "run_id=${RUN_ID} stage=${STAGE} cap=\$${MAX_USD}"

"$CLIENT_PYTHON" scripts/run_rulegen_rule_ir.py \
    --execute --run-id "$RUN_ID" --stage "$STAGE" --max-usd "$MAX_USD"

echo "=== IDPR property RuleIR end: $(date) ==="
