# KCL 61 커버 rulegen sweep — 생성 캠페인 견적 (승인용 초안)

작성일: 2026-07-21 · 상태: **승인 대기 (API 미실행, 계측만)**

이 문서는 "사기 rulegen 파이프라인으로 KCL 61문항 전체를 커버"하는 캠페인의
**실측 기반 견적**이다. 숫자는 사기 캠페인의 캐시된 토큰 로그(`​.cache/llm/runs`)와
주석서 pool(`data/commentary/kcl_criminal_v1_commentary_pool.json`)에서 직접 집계했다.
**terra/sol는 아직 호출하지 않았다.** 견적은 예산 게이트·승인 게이트 통과용이다.

---

## 1. 사기 캠페인 실측 앵커 (1개 조문 = 제347조, 127 chunks)

`.cache/llm/runs` 28개 run.json의 usage 집계:

| 구분 | 토큰 |
|---|---:|
| **Gross (전 반복 포함: critic 4버전·merge 2회·correction 8회·pilot 8회)** | **2,939,742** |
| **Lean (스테이지별 1-pass만)** | **1,525,268** |

Lean 1-pass 스테이지 분해:

| 스테이지 | 역할 | 토큰 |
|---|---|---:|
| candidate_extraction (terra) | 배치→NormCandidate | 205,527 |
| candidate_critic (sol) | 후보 비평 | 225,325 |
| normcard_merge (terra) | 후보→NormCard | 316,184 |
| normcard_critic (sol) | 카드 법률비평 | 399,052 |
| ruleir_gen+patch (terra) | NormCard→RuleIR | 309,104 |
| ruleir_critic (sol) | RuleIR 비평 | 70,076 |
| **합계 (fraud=1 campaign)** | | **1,525,268** |

- Gross/Lean = 1.9×. 파이프라인이 성숙했으므로 신규 죄명은 **lean 기준**으로 잡는다
  (critic 4버전·merge 재실행은 사기 exemplar 개발 과정의 일회성 반복이었다).
- 파생 단가: **12,010 토큰/chunk** (사기 밀도 기준 = 보수적 상한. 사기는 주석서 최대
  분량·최다 학설 대립 죄명이라 다른 죄명은 이보다 옅다).

## 2. 커버 대상 분량 (주석서 pool 실측)

101개 non-fraud target, 중복 제거 후 **3,108 chunks**. 조문(target)당 chunk_count =
해당 조문 주석서 전량. 상위: 제355조 횡령·배임 352, 제106조 압수 150, 제250조 살인 143.

## 3. 단계별 견적 (우선순위 = 실체 먼저, target 중복은 앞 단계에 귀속)

| Phase | 문항 | target (각칙/형소) | chunks | ~토큰(lean) | fraud 배수 |
|---|---:|---|---:|---:|---:|
| **P1 재산범** | 11 | 31 (30/1) | 1,281 | ~15.4M | **10.1×** |
| **P2 OOS 실체 비재산** | 16 | 21 (19/2) | 527 | ~6.3M | **4.1×** |
| P3 절차 증거능력 gate | 17 | 23 (0/23) | 610 | ~7.3M | 4.8× |
| P4 OOS 절차(규칙친화+학설) | 16+1 | 27 (0/27) | 690 | ~8.3M | 5.4× |
| **FULL SWEEP** | 61 | 101 | 3,108 | **~37.3M** | **24.5×** |
| 실체만 (P1+P2, 각칙) | 27 | 49 | 1,717 | ~20.6M | 13.5× |

**핵심 신호: full-depth 61 = 사기 캠페인의 ~24배.** $100 예산(사기에 이미 일부 소모)에서
전량 full-depth는 불가하다. 실체법만 해도 13.5배다. → **단계적 커버 + tier 정직 보고**가
불가피하다(§12.2 coverage tier 원칙과 정합).

## 4. 견적을 낮추는 레버 (권고 적용 순)

1. **per-issue 스코핑 (최대 레버).** 위 chunk_count는 조문 주석서 *전량*이다. 사기 127은
   exemplar라 제347조 전 doctrine을 넣은 값이다. 커버용은 **KCL 문항이 실제 테스트하는
   issue_tag의 section_path만** 배치로 묶으면 된다(파이프라인이 이미 `section_path` 보존
   12,000자 배치 지원). 제355조 352 전량이 아니라 문항이 건드리는 쟁점 절만 → 대폭 감소.
2. **card-stage 실제 sub-linear.** merge/critic/RuleIR은 chunk가 아니라 *카드 수*로 스케일.
   비사기 죄명은 학설 대립이 얕아 카드·지적이 사기보다 훨씬 적다 → 12k/chunk는 상한.
3. **iteration 0.** critic 1-pass, merge 1회. 이미 lean에 반영.
4. **절차(P3+P4)는 별도 트랙.** 증거능력 gate·결정론 절차규칙은 commentary→NormCard
   substantive rulegen과 저작 방식이 다르다(A4). 실체 rulegen 예산에서 분리해 본다.

## 5. $ 환산 (단가 확정 2026-07-21)

단가(per 1M tokens): **terra $2.5 in / $15 out · sol $5 in / $30 out.**
스테이지별 input/output를 모델에 매칭해 산정.

### 사기 캠페인 실제 원가 (기준점)
| 기준 | terra | sol | 합계 |
|---|---:|---:|---:|
| **Gross 실지출**(28 run 전부) | $9.67 | $9.36 | **$19.03** |
| **Lean 1-pass**(스테이지별 최종 1회) | — | — | **$10.25** |

- 파생 단가: **$0.081/chunk** (lean, 사기 밀도 = 보수적 상한).
- 즉 총 $100 예산 중 사기에 **~$19 소모**, 잔액 **~$81** 추정([[idpr-budget-priority]] 잔액
  미확인분과 대조 필요).

### Sweep $ (선형 chunk 스케일 = 보수적 상한)
| 범위 | chunks | fraud 배수 | ~$ (lean) |
|---|---:|---:|---:|
| **FULL 61** | 3,108 | 24.5× | **~$251** |
| 실체만 P1+P2 | 1,717 | 13.5× | ~$139 |
| P1 재산범 | 1,281 | 10.1× | ~$103 |
| P2 OOS 실체 | 527 | 4.1× | ~$43 |
| *worst-case: iteration이 사기처럼 재발 시 FULL 61* | | | *~$466* |

**해석:** full-depth 61 = **~$251**(lean), 최악 ~$466. 단 이는 **상한**이다:
- lean 원가의 **68%가 card-stage**(merge+critic+RuleIR)인데 이건 chunk가 아니라 *카드 수*로
  스케일하고, 비사기 죄명은 학설이 얕아 카드가 사기보다 훨씬 적다 → 실제는 선형 이하.
- per-issue 스코핑(§4-1) 적용 시 chunk 자체가 감소.
- 따라서 **현실 full-61 ≈ $150–250 구간**, 실체만이면 $100 내외로 수렴 가능.

## 6. 권고

- **Phase 1(재산범 11) → Phase 2(OOS 실체 16) 순의 실체 우선**, per-issue 스코핑 적용.
  재산범이 현 사기 rule에 근접해 카드 재사용률이 높다.
- **절차(P3/P4)는 A4 트랙에서 별도 견적** — 짝 데모 최소분만 8/11 내, 나머지 uncovered tier.
- 각 phase 착수 = **개별 승인·예산 확인 게이트**. 파일럿 1죄명(재산범 최소 조문)으로 실단가·
  카드밀도 실측 후 잔여 phase 재견적하는 것이 리스크 최소.

## 7. 파일럿 보정 (2026-07-22, 장물 제362조)

파일럿으로 §4의 두 상한-완화 가정을 **실측 확인**했다(상세: `rulegen_campaign_launch.md`):

- **밀도 = 사기의 ~0.5×** 확정(장물 25 cand/배치 vs 사기 ~51). §4-2 "card-stage sub-linear"가
  실측으로 뒷받침됨 → full-61 상한 $251은 실제 하향.
- **추출+후보비평 실단가(파일럿 보정)**: terra $0.094/배치 + sol critic $0.125/배치. 실체 47조문
  162배치 = **$35.5**(추출+critic만). 다운스트림은 미파일럿(장물로 1회 더 권장).
- **반전 요인 — 추론 모델**: terra/sol이 gpt-5.6 추론 모델이라 콜당 출력 토큰이 사기(비추론)
  시절보다 큼. reasoning_effort=low로 통제하나, lean 토큰 기반 $251은 이만큼 상방 압력.
- **순효과**: 밀도 0.5×(하방) vs 추론 출력(상방)이 상쇄. 실체 47조문 전량 추출~critic은 예산 내
  ($35.5)로 확정적이고, full 파이프라인은 다운스트림 파일럿 후 확정.

관련: [[idpr-budget-priority]] · [[rulegen-campaign-pilot]] · A3(평가셋)·L3(죄명확장) — `idpr_remaining_work.md`
