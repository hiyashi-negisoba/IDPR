#!/bin/bash
# 형소법 rulegen 밀도 파일럿 — 두 절차 축에서 각 1조문씩 실단가를 실측한다.
#   제308조의2 위법수집증거의 배제 (40ch) = 증거능력 축
#   제342조   일부상소             (30ch) = 재판절차 규칙친화 축
# 형법각칙 재산죄 실측치($0.0508/chunk)를 형소법에 그대로 적용할 수 없다는
# 판단(사용자 2026-07-23: "형소법은 카드밀도가 다를 것 같다")에 따른 검증이다.
# terra/sol = 원격 API → CPU-only.
#
#SBATCH --job-name=idpr_proc_pilot
#SBATCH --output=logs/idpr_proc_pilot_%j.out
#SBATCH --error=logs/idpr_proc_pilot_%j.err
#SBATCH --partition=gpu
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=32G
# (의도적으로 --gres=gpu 없음)

set -euo pipefail
source "${IDPR_PROJECT_ROOT:-${SLURM_SUBMIT_DIR:-$PWD}}/scripts/slurm/_env.sh"
PY="$CLIENT_PYTHON"
cd "$PROJECT_ROOT"
mkdir -p logs

echo "=== procedure density pilot start: $(date) ==="

run_one () {
    local SLUG="$1" ART="$2" BATCHES="$3"
    local REQ="data/rulegen/procedure/${SLUG}_rulegen_requests.jsonl"
    local EXTRACT_ROOT=".cache/llm/runs/procedure_pilot"

    echo "--- [$SLUG] $ART : extraction ($BATCHES batches)"
    "$PY" scripts/run_fraud_rulegen_pilot.py \
        --requests "$REQ" \
        --run-root "$EXTRACT_ROOT" --run-id "$SLUG" \
        --start 1 --limit "$BATCHES" --concurrency 2 \
        --terra-max-tokens 16000 --terra-reasoning-effort low \
        --with-critic --execute || echo "   (extract rc=$? — rc=2는 검증플래그, 정상)"

    echo "--- [$SLUG] $ART : downstream (merge + normcard critic)"
    "$PY" scripts/run_rulegen_downstream.py \
        --crime-slug "$SLUG" --article-slug "$SLUG" --article "$ART" \
        --law-id 001671 \
        --requests "$REQ" \
        --candidates-dir "$EXTRACT_ROOT/$SLUG/terra" \
        --run-id "$SLUG" --stage all --concurrency 2 \
        --execute || echo "   (downstream rc=$? — rc=2는 일부 검증실패, 정상)"
}

run_one cp342   "제342조"    2
run_one cp308_2 "제308조의2" 4

echo "=== procedure density pilot end: $(date) ==="
