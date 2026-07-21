# KCL 실체법 rulegen 캠페인 — 실행준비 상태 + 런치 절차

작성일: 2026-07-22 · 상태: **준비 완료, 실행 대기(예산 게이트).** terra/sol 미실행.

장물 파일럿(§ 파일럿 결과)으로 파이프라인·비용·config를 검증한 뒤, 실체 P1(재산범)+
P2(OOS 비재산) 형법각칙 47개 조문의 캠페인을 **생성만** 해 둔 상태다. 실제 API 실행은
잔여 예산 확인 후 명시 승인으로만 한다.

## 준비된 자산

| 자산 | 내용 |
|---|---|
| `data/rulegen/campaign/kcl_substantive_campaign_manifest.json` | 47개 조문 대상·chunk·배치·파일럿보정 비용 |
| `data/rulegen/campaign/art*_rulegen_requests.jsonl` | 조문별 requests (총 162 배치) |
| `scripts/build_rulegen_campaign.py` | 매니페스트+requests 재생성 (결정론, API 아님) |
| `scripts/slurm/run_rulegen_pilot.sh` | 조문 1개 실행 sbatch (CPU-only, GPU 미할당, 48h) |
| `scripts/slurm/launch_rulegen_campaign.sh` | 전 조문 per-crime sbatch 런처 (기본 dry-list) |

## 규모·비용 (파일럿 보정)

- 47 조문 / 1,531 chunks / **162 배치**.
- **추출+후보비평 스테이지 = ~$35.5** (장물 실측 $0.094 terra + $0.125 sol critic/배치).
- 밀도 = 사기의 ~0.5× (장물 25 cand/배치 vs 사기 ~51) → 다운스트림도 그만큼 가벼움.
- **다운스트림(merge·normcard critic·RuleIR·RuleIR critic)은 미파일럿** — 조문당 1회씩,
  fraud×0.5 density로 추정. 정밀 값은 장물로 다운스트림까지 한 번 돌려야 확정된다.

## 런치 절차 (실행 = 예산 게이트)

```bash
# 1) 무지출 확인 — 무엇이 제출될지 나열
bash scripts/slurm/launch_rulegen_campaign.sh

# 2) 실제 제출 (예산 소모! 잔여 예산 확인 후에만)
bash scripts/slurm/launch_rulegen_campaign.sh --confirm
```

- 각 조문 = 별도 sbatch(CPU-only, `--gres` 없음). SFT 등 GPU 잡과 경합 없음.
- 산출: `.cache/llm/runs/campaign/<slug>/campaign_<slug>/` 에 terra/sol 출력·run.json.
- 단일 조문만 돌리려면: `IDPR_PILOT_EXECUTE=1 IDPR_PILOT_REQUESTS=<path> IDPR_PILOT_RUN_ROOT=.cache/llm/runs/campaign/<slug> IDPR_PILOT_LIMIT=<batches> IDPR_PILOT_RUN_ID=<slug> sbatch scripts/slurm/run_rulegen_pilot.sh`

## 게이트 (착수 전 필수)

1. **예산 확인** — 총 $100 중 잔액. 파일럿까지 누적 ~$0.5 소모.
2. **다운스트림 파일럿(권장)** — 장물로 merge→RuleIR까지 한 번 돌려 다운스트림 실단가 확정 후 전량 착수.
3. **검토는 벌크로** — 생성 후 HITL은 `docs/research/hitl_bulk_review_spec.md`대로 유형별 1회.

## 파일럿 결과 (장물 제362조, 2026-07-22)

- job 211617(6k 기본)=실패: terra=gpt-5.6는 **추론 모델**, 6k를 reasoning이 전부 소진(finish_reason=length).
- job 211619(16k/low)=추출 성공, 경로버그로 중단. job 211635=경로수정 후 batch1 완주.
- **수정**: terra `reasoning_effort=low` + `--terra-max-tokens 16000` (reasoning 6000→326/31 토큰).
- **밀도**: 25 cand/배치(사기 ~51의 0.5×). critic verdict=revise, 5 findings/31 cand.
- **norm_kind 이슈**: 모델이 부정형 규범에서 `norm_kind='negative'`(polarity 값을 kind에 오배치) →
  extract 프롬프트 규칙 3 보강으로 교정(norm_kind vs polarity 독립 명시). A6 계열.
- 누적 지출 ~$0.5.

관련: `rulegen_sweep_cost_estimate.md` · `hitl_bulk_review_spec.md` · `idpr_remaining_work.md` A3
