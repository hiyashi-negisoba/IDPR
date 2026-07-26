# KCL 실체법 rulegen 캠페인 — 실행준비 상태 + 런치 절차

작성일: 2026-07-22 · 갱신: 2026-07-27 · 상태: **재산죄(P1) 완료 반영, P2만 남음, 실행 대기(예산 게이트).** terra/sol 미실행.

장물 파일럿(§ 파일럿 결과)으로 파이프라인·비용·config를 검증한 뒤, 실체 P1(재산범)+
P2(OOS 비재산) 형법각칙 47개 조문의 캠페인을 **생성만** 해 둔 상태였다. **2026-07-27
재스코핑: P1 재산죄 16개 조문(art323·328·329·331·334·335·337·338·342·343·350·355·356·
357·360·366)은 이 캠페인이 아니라 주석서 직접 판독 + 결정B/B2/B3 검토로 이미 끝났다**
(재산죄 RuleIR 10단위, `WORK_REPORT.md` 2026-07-26 항목). `scripts/build_rulegen_campaign.py`
의 `DONE_TARGETS`에 편입해 매니페스트를 재생성했다 — **이제 대상은 P2 31개 조문뿐**
(제344조 친족간의 범행은 P1이 아니라 A4 준용 보강 대상이라 남아 있다). 실제 API 실행은
잔여 예산 확인 후 명시 승인으로만 한다.

## 준비된 자산

| 자산 | 내용 |
|---|---|
| `data/rulegen/campaign/kcl_substantive_campaign_manifest.json` | **31개 조문**(P2만) 대상·chunk·배치·파일럿보정 비용 |
| `data/rulegen/campaign/art*_rulegen_requests.jsonl` | 조문별 requests (총 93 배치, P1분 16개 파일 삭제됨) |
| `scripts/build_rulegen_campaign.py` | 매니페스트+requests 재생성 (결정론, API 아님) |
| `scripts/slurm/run_rulegen_pilot.sh` | 조문 1개 실행 sbatch (CPU-only, GPU 미할당, 48h) |
| `scripts/slurm/launch_rulegen_campaign.sh` | 전 조문 per-crime sbatch 런처 (기본 dry-list) |

## 규모·비용 (파일럿 보정, 2026-07-27 재스코핑 — P2 31 조문만)

- **31 조문 / 858 chunks / 93 배치** (P1 재산죄 16개 조문 제외 후).
- **추출+후보비평 스테이지 = $20.37** (장물 실측 $0.094 terra + $0.125 sol critic/배치).
- 밀도 = 사기의 ~0.5× (장물 25 cand/배치 vs 사기 ~51) → 다운스트림도 그만큼 가벼움.
- **다운스트림(merge·normcard critic·RuleIR·RuleIR critic)은 P2 기준 미파일럿** — 47조문
  전체 기준으로는 다운스트림이 원가를 ~2.8배 키웠다($35.5→~$100). 같은 비율을 P2에 적용하면
  **전체 ≈ $57 내외**. 2026-07-23에 독립적으로 잡아둔 "P2 잔여 30조문 ~$43.6" 추정과는
  ±$14 차이가 나므로, 이 범위(**$44~57**)로 보고 실행 전 P2 표본으로 다운스트림을 한 번 더
  파일럿하면 좁혀진다(재산죄 때처럼).

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

1. **예산 확인** — 랩 대시보드가 지금 최신 지출을 안 보여주므로, 확인되는 즉시 아래 §범위 결정을
   다시 계산할 것.
2. **다운스트림 파일럿 — 완료(2026-07-22, 사기·장물 기준).** P2 31개 조문 표본으로는 아직
   안 돌렸다 — §규모·비용의 $44~57 범위를 좁히려면 P2에서도 한 번 더 파일럿 권장.
3. **검토는 벌크로** — 생성 후 HITL은 `docs/research/hitl_bulk_review_spec.md`대로 유형별 1회.

## 범위 결정 (2026-07-27 갱신 — P1 완료 반영)

**옵션 A(P1 재산범 우선)는 소멸했다** — 이미 완료됐다(WORK_REPORT 2026-07-26). 남은 선택은 P2
31개 조문뿐이고, 전체(candidate+critic+다운스트림) 견적은 **~$44~57**이다:
- **B. 31조문 전량** — 견적 범위 안에서 예산이 확인되면 그대로 착수.
- **C. 31조문 candidate+merge+critic만(~$20.4 + 다운스트림 일부), RuleIR은 벌크 HITL 후 별도** —
  RuleIR은 어차피 죄명별 인간 게이트라 지연해도 손해가 없다.
- **D. 모듈크기 상한 그룹핑으로 다운스트림 절감** — merge 콜수↓ 시도(재산죄 때는 안 씀, 미검증).

**절차법(P3 증거능력 gate 17 + P4 OOS 절차 16)은 이 캠페인에 없다** — A4 별도 트랙이며 저작 방식이
다르다(rulegen 병합 파이프라인 아님). 위 견적·범위는 전부 **실체법**만이다.

## 파일럿 결과 (장물 제362조, 2026-07-22)

- job 211617(6k 기본)=실패: terra=gpt-5.6는 **추론 모델**, 6k를 reasoning이 전부 소진(finish_reason=length).
- job 211619(16k/low)=추출 성공, 경로버그로 중단. job 211635=경로수정 후 batch1 완주.
- **수정**: terra `reasoning_effort=low` + `--terra-max-tokens 16000` (reasoning 6000→326/31 토큰).
- **밀도**: 25 cand/배치(사기 ~51의 0.5×). critic verdict=revise, 5 findings/31 cand.
- **norm_kind 이슈**: 모델이 부정형 규범에서 `norm_kind='negative'`(polarity 값을 kind에 오배치) →
  extract 프롬프트 규칙 3 보강으로 교정(norm_kind vs polarity 독립 명시). A6 계열.
- 누적 지출 ~$0.5.

관련: `rulegen_sweep_cost_estimate.md` · `hitl_bulk_review_spec.md` · `idpr_remaining_work.md` A3
