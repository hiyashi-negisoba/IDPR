#!/bin/bash
# P1 재산범 rulegen 벌크 (candidate → merge → normcard critic) — SLURM 제출용.
# terra/sol = 원격 SKIML API라 로컬 GPU 불필요 → CPU-only (gpu 파티션, --gres 없음).
# 오케스트레이터(run_property_campaign.py)가 재산범 17조문을 싼 것부터 순차 처리하며,
# 추출/다운스트림 모두 idempotent(완료분 skip)이라 재제출해도 안전하다.
# RuleIR은 죄명별 인간 게이트(벌크 HITL)라 제외. 러닝 예산 상한 $55에서 자동 중단.
#
#SBATCH --job-name=idpr_prop_campaign
#SBATCH --output=logs/idpr_prop_campaign_%j.out
#SBATCH --error=logs/idpr_prop_campaign_%j.err
#SBATCH --partition=gpu
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=32G
# (의도적으로 --gres=gpu 없음: API 벌크는 로컬 GPU를 쓰지 않는다)

set -euo pipefail
source "${IDPR_PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}/scripts/slurm/_env.sh"
cd "$PROJECT_ROOT"
mkdir -p logs

MAX_USD="${IDPR_PROP_MAX_USD:-55}"
CONCURRENCY="${IDPR_PROP_CONCURRENCY:-3}"

echo "=== IDPR property campaign start: $(date) ==="
echo "job=${SLURM_JOB_ID:-NA} host=$(hostname) cpus=${SLURM_CPUS_PER_TASK:-NA} gpu=none cap=\$${MAX_USD}"

"$CLIENT_PYTHON" scripts/run_property_campaign.py \
    --execute --concurrency "$CONCURRENCY" --max-usd "$MAX_USD"

echo "=== IDPR property campaign end: $(date) ==="
