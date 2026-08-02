#!/bin/bash
# KCL 실체법 rulegen 캠페인 런처 — 매니페스트의 각 조문을 per-crime sbatch로 제출한다.
# 각 잡 = 그 조문의 전 배치 추출+후보비평(run_rulegen_pilot.sh 재사용, CPU-only).
#
# 안전장치: 기본은 DRY-LIST(제출 안 함). 실제 제출은 첫 인자 --confirm 일 때만.
# 실제 제출은 terra/sol 예산 소모 = 예산 게이트. 반드시 잔여 예산 확인 후 --confirm.
#
# 사용:
#   bash scripts/slurm/launch_rulegen_campaign.sh            # dry-list (무지출)
#   bash scripts/slurm/launch_rulegen_campaign.sh --confirm  # 실제 제출 (예산 게이트!)

set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/_env.sh"
PY="$CLIENT_PYTHON"
MANIFEST="$PROJECT_ROOT/data/rulegen/campaign/kcl_substantive_campaign_manifest.json"
cd "$PROJECT_ROOT"

CONFIRM="${1:-}"
if [ "$CONFIRM" = "--confirm" ]; then
    echo "[MODE] CONFIRM — 실제 sbatch 제출 (terra/sol 예산 소모)"
else
    echo "[MODE] DRY-LIST — 제출 안 함. 실제 제출은 첫 인자 --confirm"
fi

# 매니페스트에서 (slug, requests_path, batches) 추출
"$PY" - "$MANIFEST" <<'PY' | while IFS=$'\t' read -r SLUG REQ BATCHES; do
import json, sys
m = json.load(open(sys.argv[1]))
for t in m["targets"]:
    print(f"{t['issue_tag']}\t{t['requests_path']}\t{t['batches']}")
PY
    RUN_ROOT=".cache/llm/runs/campaign/${SLUG}"
    if [ "$CONFIRM" = "--confirm" ]; then
        IDPR_PILOT_EXECUTE=1 \
        IDPR_PILOT_REQUESTS="$REQ" \
        IDPR_PILOT_RUN_ROOT="$RUN_ROOT" \
        IDPR_PILOT_LIMIT="$BATCHES" \
        IDPR_PILOT_RUN_ID="campaign_${SLUG}" \
        sbatch scripts/slurm/run_rulegen_pilot.sh
    else
        echo "  would submit: $SLUG  ($BATCHES batches)  requests=$REQ  run_root=$RUN_ROOT"
    fi
done

echo "done."
