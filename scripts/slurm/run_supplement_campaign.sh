#!/bin/bash
# 누락 조문 보강 rulegen (제333조 강도 · 제332조 상습범 · 제330조 야간주거침입절도).
# RuleIR 단위 설계에서 robbery 단위에 강도 기본 구성요건이 없다는 것이 드러났고, 원천 파싱본에
# 제333조가 절 구조까지 있음을 확인해 보강한다. 71 chunks / 추정 $3.61.
#
# terra/sol = 원격 SKIML API라 로컬 GPU 불필요 → CPU-only (gpu 파티션, --gres 없음).
# 오케스트레이터는 재산죄 벌크와 같은 경로(run_property_campaign.py)를 매니페스트만 바꿔 쓴다.
# 추출/다운스트림 모두 idempotent(완료분 skip)이므로 재제출해도 이중 지출이 없다.
#
#SBATCH --job-name=idpr_suppl_campaign
#SBATCH --output=logs/idpr_suppl_campaign_%j.out
#SBATCH --error=logs/idpr_suppl_campaign_%j.err
#SBATCH --partition=gpu
#SBATCH --time=12:00:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=32G
# (의도적으로 --gres=gpu 없음: API 벌크는 로컬 GPU를 쓰지 않는다)

set -euo pipefail
PROJECT_ROOT="/data5/jaehoonjeong/IDPR"
CLIENT_PYTHON="/data5/jaehoonjeong/miniconda3/bin/python"
cd "$PROJECT_ROOT"
mkdir -p logs

MANIFEST="data/rulegen/campaign/kcl_supplement_manifest.json"
ARTICLES="${IDPR_SUPPL_ARTICLES:-330,332,333}"
MAX_USD="${IDPR_SUPPL_MAX_USD:-6}"
CONCURRENCY="${IDPR_SUPPL_CONCURRENCY:-3}"

echo "=== IDPR supplement campaign start: $(date) ==="
echo "job=${SLURM_JOB_ID:-NA} host=$(hostname) cpus=${SLURM_CPUS_PER_TASK:-NA} gpu=none cap=\$${MAX_USD}"
echo "articles=${ARTICLES} manifest=${MANIFEST}"

"$CLIENT_PYTHON" scripts/run_property_campaign.py \
    --manifest "$MANIFEST" \
    --articles "$ARTICLES" \
    --summary data/rulegen/campaign/supplement_campaign_run_summary.json \
    --execute --concurrency "$CONCURRENCY" --max-usd "$MAX_USD"

echo "=== IDPR supplement campaign end: $(date) ==="
