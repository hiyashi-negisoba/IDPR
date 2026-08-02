#!/bin/bash
# rulegen 파일럿 (terra/sol = 원격 SKIML API). 로컬 GPU 불필요 → CPU-only.
# 자원: cpu=2, mem=32G, GPU 미할당, walltime 48h 고정 (사용자 확정 2026-07-21).
#
# 안전장치: 기본은 DRY-RUN(무지출). 실제 API 지출은 IDPR_PILOT_EXECUTE=1 을
# 명시할 때만 일어난다. dry-run은 배치 수·계획 토큰·env 해석만 출력하고 끝난다.
# 프롬프트는 기존 승인본(prompts/rulegen_extract_norm_candidates.md·rulegen_critic.md)
# 재사용. secrets는 .env(dotenv)에서 로드하므로 이 스크립트에 키를 넣지 않는다.
#
#SBATCH --job-name=idpr_rulegen_pilot
#SBATCH --output=logs/idpr_rulegen_pilot_%j.out
#SBATCH --error=logs/idpr_rulegen_pilot_%j.err
#SBATCH --partition=gpu
#SBATCH --time=48:00:00
#SBATCH --cpus-per-task=2
#SBATCH --mem=32G
# (의도적으로 --gres=gpu 없음: API 파일럿은 로컬 GPU를 쓰지 않는다)

set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/_env.sh"

cd "$PROJECT_ROOT"
mkdir -p logs

# --- 파라미터 (env 오버라이드 가능) ---
# 기본 대상 = 장물(제362조) 파일럿. 다른 죄명은 REQUESTS/RUN_ROOT만 바꾸면 됨.
PILOT_REQUESTS="${IDPR_PILOT_REQUESTS:-data/rulegen/stolen_property/stolen_property_rulegen_requests.jsonl}"
PILOT_RUN_ROOT="${IDPR_PILOT_RUN_ROOT:-.cache/llm/runs/stolen_property_rulegen}"
PILOT_LIMIT="${IDPR_PILOT_LIMIT:-1}"          # 돌릴 배치 수 (파일럿은 소수)
PILOT_START="${IDPR_PILOT_START:-1}"          # 1-based 시작 배치
PILOT_RUN_ID="${IDPR_PILOT_RUN_ID:-pilot_${SLURM_JOB_ID:-manual}}"
PILOT_CONCURRENCY="${IDPR_PILOT_CONCURRENCY:-1}"
# terra=gpt-5.6는 추론 모델 → 6k 기본은 reasoning이 전부 소진(finish_reason=length).
# reasoning_effort=low + 넉넉한 출력 한도로 교정.
PILOT_TERRA_EFFORT="${IDPR_PILOT_TERRA_EFFORT:-low}"
PILOT_TERRA_MAX="${IDPR_PILOT_TERRA_MAX:-16000}"

CMD=("$CLIENT_PYTHON" scripts/run_fraud_rulegen_pilot.py
     --requests "$PILOT_REQUESTS"
     --run-root "$PILOT_RUN_ROOT"
     --start "$PILOT_START"
     --limit "$PILOT_LIMIT"
     --concurrency "$PILOT_CONCURRENCY"
     --run-id "$PILOT_RUN_ID"
     --terra-max-tokens "$PILOT_TERRA_MAX"
     --terra-reasoning-effort "$PILOT_TERRA_EFFORT"
     --with-critic)

# 실지출은 명시 플래그로만. 미설정 시 dry-run(요약만 출력, API 호출 0).
if [ "${IDPR_PILOT_EXECUTE:-0}" = "1" ]; then
    CMD+=(--execute)
    echo "[MODE] EXECUTE — 실제 terra/sol API 호출 (예산 소모)"
else
    echo "[MODE] DRY-RUN — API 호출 없음. 실행하려면 IDPR_PILOT_EXECUTE=1"
fi

echo "=== IDPR rulegen pilot start: $(date) ==="
echo "job=${SLURM_JOB_ID:-NA} host=$(hostname) cpus=${SLURM_CPUS_PER_TASK:-NA} mem=32G gpu=none walltime=48h"
echo "cmd: ${CMD[*]}"

"${CMD[@]}"

echo "=== IDPR rulegen pilot end: $(date) ==="
