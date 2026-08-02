#!/bin/bash
# P2(비재산) rulegen 다운스트림(merge → normcard critic) — 단일 SLURM job.
# P1(run_property_campaign.sh)과 동일한 오케스트레이터 패턴: 조문 하나씩 순차 처리,
# idempotent(완료분 skip), 러닝 예산 상한에서 자동 중단. candidate 추출은 이미
# launch_rulegen_campaign.sh --confirm으로 완료돼 있어 이 job은 다운스트림만 수행.
#
#SBATCH --job-name=idpr_p2_downstream
#SBATCH --output=logs/idpr_p2_downstream_%j.out
#SBATCH --error=logs/idpr_p2_downstream_%j.err
#SBATCH --partition=gpu
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=32G
# (의도적으로 --gres=gpu 없음: API 벌크는 로컬 GPU를 쓰지 않는다)

set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/_env.sh"
cd "$PROJECT_ROOT"
mkdir -p logs

MAX_USD="${IDPR_P2_MAX_USD:-40}"
CONCURRENCY="${IDPR_P2_CONCURRENCY:-3}"

echo "=== IDPR P2 downstream campaign start: $(date) ==="
echo "job=${SLURM_JOB_ID:-NA} host=$(hostname) cpus=${SLURM_CPUS_PER_TASK:-NA} gpu=none cap=\$${MAX_USD}"

"$CLIENT_PYTHON" scripts/run_p2_downstream_campaign.py \
    --execute --concurrency "$CONCURRENCY" --max-usd "$MAX_USD"

echo "=== IDPR P2 downstream campaign end: $(date) ==="
