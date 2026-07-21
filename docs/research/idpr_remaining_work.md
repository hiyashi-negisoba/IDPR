# IDPR 잔여 작업 목록

작성일: 2026-07-19 (프롬프트-계약 정합 세션 종료 시점 기준)
갱신일: 2026-07-21 (8/11 논문 데드라인 기준 재정렬)

## 이 문서의 기준

**단기 목표는 2026-08-11 NLLP @ EMNLP 2026 (non-archival long paper) 제출이다.**
preprint는 비공개 옵션으로 내고 이후 ACL 2027에 제출한다. 아래 우선순위는 전부 이
데드라인을 기준으로 매긴다. 수사지원 산출물은 이 논문의 실험이 아니라 장기 확장이며
문서 하단 "장기 트랙"으로 내렸다(`idpr_research_draft.md` §1 "장기 IDPR").

### 논문이 주장하는 것

neuro-symbolic을 법률 도메인에 접목해 (a) long-form 생성의 **논증-결론 정합성**과
(b) 어려운 법률 판단의 **높은 이해**를 보인다. 슬로건: "결론은 논리가 계산하고, 문장은
모델이 쓴다"(`project_init.md`). 결론을 생성 전 Scallop에서 확정하고 모델은 언어화만
하므로 논증-결론 불일치가 구조적으로 불가능해진다는 것이 핵심 기여다.

### 마일스톤 대비 현재 위치 (냉정하게)

`project_init.md` §8 역산 일정과 실제:

| 주차 | 계획 DoD | 실제 (2026-07-21) |
|---|---|---|
| W1 (7/14–20) | 인벤토리·스키마·rulegen·사기죄 rule verified | 대체로 달성 |
| W2 (7/21–27) | S1–S4 E2E가 사기 5개 설문 동작 · 절차 레이어 · inadmissible_use 데모 | **M5 E2E 사기 5건 동작(표준 아키텍처·A6까지 완료). 절차 레이어 초안·검증기 존재, whole-IRAC 배선 미착수** |
| W3 (7/28–8/3) | 커버 설문 전체 본 실험 + 베이스라인 4종 + ablation · 커버리지 figure | **6방법 러너·측정 primitive 있음. 본실험·집계 미착수** |
| W4 (8/4–11) | 집필 · 리뷰 반영 · 제출 | — |

**오늘이 W2 첫날이고 W3 본실험까지 일주일이다.** M5 표준 아키텍처는 사기 5건에서 작동하고
(A6까지 완료), 측정 primitive와 6방법 비교 러너도 이미 있다(A1·A2). 남은 병목은 그 산출물을
**사건집합 × 시스템으로 집계·통계 내는 층**(A1)과 **평가셋 확정**(A3)이다. "측정 수단이 아예
없다"는 앞선 진단은 부정확했다(2026-07-21 정정).

사용자 판단(2026-07-21): 최대 병목은 평가 하니스의 **집계층**이다. 이것이 없으면 베이스라인을
돌려도 논문 표로 묶을 수 없어 전체가 게이팅된다.

---

## 이미 구축된 자산 (2026-07-21 코드베이스 전수 감사)

이 문서는 이미 완료된 작업을 반복적으로 "미구현/미착수"로 적어왔다(사용자 지적, 2회). 아래는
코드베이스 전수 감사로 확인한 실제 완료 자산이며, **잔여 작업은 전부 이 위에 얹는 것**이다.
개별 항목의 "이미 있는 것/없는 것"은 각 A·B·L 절에서 이 목록을 기준으로 다시 적었다.

- **M5 표준 파이프라인** — 2-call neuro-symbolic 전 구간 작동(`neural/__init__.py`,
  `run_fraud_irac_matrix.py`). 사기 5 paraphrase 100% 통과, 정적 위반 0, A6 극성수정 완료.
- **평가 primitive** — 논증-결론 정합성 채점(`assess_irac_answer_alignment`), ClaimGraph
  back-parse, 답안 계약 위반 집계, **M1~M6 6방법 비교 러너**까지 가동(A1·A2).
- **M6 검증 경로** — ClaimGraph 추출 + 구획 재작성(`run_claim_verification`, 프롬프트 2종)이
  구현돼 matrix에서 실행 중(m6_claim_verified). 남은 건 whole-IRAC 이관뿐(B3).
- **법리 카드 코퍼스** — NormCard **646장**(8개 도메인) + retrieval **558장**. 활성
  core+profile은 이 중 선별분(카드 슬롯 25).
- **rulegen 파이프라인** — 인벤토리→commentary bundle→후보 카드→critic→adjudication→RuleIR
  →Scallop까지 스크립트 전 단계가 사기 기준으로 구축(29개 러너). 죄명 확장 = 이 파이프라인 재실행.
- **KCL 61 인벤토리 + 주석서 선별** — 61문항 전수 태깅(실체 26/절차 33/mixed 2), issue_tag
  165개 → commentary target 102개 매핑 완료(`kcl_criminal_v1_commentary_pool.json`). 절차
  문항용 CP_* 매핑도 포함.
- **절차 레이어 초안** — evidence gating Scallop 초안(`gates.scl`, `hearsay.scl`), 후보
  게이트(`procedural_gate_v1_candidate.scl`), `inadmissible_use` 검증기(`verify_claims`),
  절차 commentary 선별까지 존재. whole-IRAC 배선 + 절차 rulegen만 미착수(A4).
- **RAG 검색** — 558 retrieval 카드 위 결정론 BM25 인출(`build_fraud_rag_packet`)이 구현돼
  m2/m3에서 실행 중. L2는 이 검색의 *용도*를 수사 착안사항으로 재정의하는 작업(검색 신규 아님).

**진짜 남은 핵심 4가지**: (1) 평가 지표를 사건집합×시스템으로 집계·통계 내는 층(A1), (2) KCL
61 커버 rulegen 확장(A3=L3), (3) 절차 레이어 whole-IRAC 배선(A4), (4) 결론 구조화(A5).

---

# A. 논문 트랙 (8/11 데드라인, 우선순위 순)

## A1. 평가 하니스 (에이전트, 최우선 병목)

상태: **측정 primitive는 이미 구현·가동 중이다. 없는 것은 그 위에 얹는 집계·통계·rubric
층뿐이다.** `src/idpr/eval/__init__.py`가 빈 모듈이라는 사실만 보고 "하니스 미구현"으로
적었던 것은 부정확했다(2026-07-21 사용자 지적으로 정정). 하니스의 채점 로직은 `eval/`이
아니라 `generation/`·`neural/`·런너에 흩어져 이미 돌고 있다.

### 이미 있는 것 (재사용, 신규 개발 아님)

- **논증-결론 정합성 채점** — `generation/__init__.py`의 `assess_irac_answer_alignment`가
  구획↔plan 불일치, 필수 카드/사실 메타데이터 누락, 구획 결론 불일치, 전체 결론 불일치를
  위반으로 검출한다. `run_fraud_irac_matrix.py`의 `answer_contract_violations`가 답안 계약
  위반을 함께 센다. 이것이 §8.2의 핵심 채점기다.
- **ClaimGraph back-parse** — `validate_claim_graph`, `normalize_claim_graph`(스키마+grounding).
- **inadmissible_use gating** — `verification/__init__.py`의 `verify_claims`(score+violations).
  단 구 `Derivation` 기반이라 현행 whole-IRAC 계약과는 아직 미연결(A4에서 배선).
- **방법 간 비교 러너** — `run_fraud_irac_matrix.py`가 M1~M6 6방법을 한 사건에 돌려 방법별
  위반 건수·구조화 결론·레이턴시를 `fraud_irac_matrix_report.json`으로 뽑는다. 이미
  A2 베이스라인 비교의 뼈대다(아래 A2 참조).
- **런별 지표 산출물** — `revalidation_after_validator_fix.json`, `neural_query_resolution.json`,
  각 experiment의 `report.json`/`summary.json`. A6 극성수정의 비교표(잘못된 not_established,
  부호 뒤집힘, 카드 판정 불일치, 계약 위반, 안전망 발화)가 전부 이 산출물에서 손으로 집계됐다.

### 없는 것 (집계·통계 층 — 실제 A1 작업)

`idpr_research_draft.md` §8의 지표를 **사건 집합 × 시스템** 위에서 자동 집계하는 층이 없다.

1. **§8.2 rate 집계** — 위 per-run 위반 리스트를 argument-conclusion consistency rate,
   contradiction rate, unsupported rule rate, fact hallucination rate, conclusion flip rate로
   **여러 사건에 걸쳐** 묶는 집계기. primitive는 있으니 신규 코드는 집계·명명뿐이다.
2. **통계층** — paired test·bootstrap CI가 **전무하다**(전 소스 grep 확인). 논문 표에 필요.
3. **§8.1 legal quality** — KCL rubric score, issue spotting recall. rubric 데이터가 repo에
   없어 확보가 선행. LLM judge + 사람 검수 표본 병행. 순환성 통제(§12.5): rubric은 채점에만
   쓰고 prompt·RAG·rulegen에 노출하지 않는다.
4. **전 평가셋 스윕 러너** — 현재 매트릭스는 사건 1건씩 돈다. 평가셋(A3) 전체 × 시스템을
   쓸어 위 rate를 내는 러너로 감싸야 한다.
- 정리하면 A1은 "채점기를 새로 만드는 일"이 아니라 **이미 도는 채점기를 집합 수준으로
  집계하고 통계를 붙이는 일**이다. 이것이 A2·A3의 채점 대상이 된다.

## A2. 베이스라인 러너 (에이전트)

상태: **6방법 러너 이미 가동.** `run_fraud_irac_matrix.py`가 M1~M6을 돌린다. 이 중
m1_direct·m2_rag·m5_irac_plan·m6_claim_verified가 §7.1 9종의 Direct IRAC·RAG-only·IDPR
generate·IDPR verify에 해당하고, m3/m4는 중간 ablation이다.

- 미착수는 나머지 5종: Few-shot IRAC, Plan-then-write, Self-Refine, Best-of-N + LLM judge,
  Doctrinal critique(DCDE). 동일 모델·temperature·budget·prompt hash cache로 공정 비교(§7.3).
- 단일 사건 러너를 평가셋(A3) 스윕으로 감싸고 A1 집계층으로 채점되면 논문 표가 된다.

## A3. 평가셋 확정 (사용자 + 에이전트)

상태: **방향 확정(2026-07-21).** 현 단계는 사기죄만으로 전체 파이프라인 정합성을 검증하는
단계이고, **최종 universe는 KCL 61문항 커버**다. 사기 5건 수동 paraphrase는 그 정합성
검증용 smoke다.

- **확장 경로**: 이미 정해둔 주석서 자료를 기반으로 KCL 61을 커버하도록 card·RuleIR 등
  Scallop 엔진용 재료를 API로 생성한다. **방식은 지난번 사기 rulegen과 동일하며 사람 검토를
  포함한다.** 곧 L3(사기 외 죄명 확장)이 이 경로의 실체이며, 논문 평가셋과 직결되므로 장기
  트랙이 아니라 A3의 실행 항목이다. 8/11 안에 61 중 어디까지 커버하느냐가 본실험 규모를 정한다.
- 오염 축(§12.5): KCL 기출은 학습 컷오프(2025-01)와 겹칠 수 있다. coverage tier(§12.2)로
  full-61과 rule 보유 covered-tier를 함께 보고하고 사후 제외하지 않는다. paraphrase 5건은
  오염 통제 대조군으로 병행 유지한다.
- 현재 진행: 파이프라인 정합성 + **최종 평가 방식(A2)** 결정을 함께 보고 있다.

## A4. 절차 레이어 + evidence gating (에이전트 + 사용자)

상태: **미결(2026-07-21).** 현재 실체법 중 사기죄만 보고 있어 절차 레이어는 보류다. 단
**초안 자산은 이미 있다**(위 "이미 구축된 자산" 참조): gating Scallop 초안(`gates.scl`,
`hearsay.scl`)·후보 게이트(`procedural_gate_v1_candidate.scl`)·`inadmissible_use` 검증기·절차
commentary 선별(CP_*). "데모도 없다"가 아니라 **whole-IRAC M5 배선 + 절차 norm card/RuleIR
rulegen이 미착수**다.

- 구조: 전문법칙·위수증 gate가 `admissible(E)`를 거짓으로 만들면 그 증거에 의존하는 사실이
  `provable`이 되지 못하고, 그 사실을 실체법 논증에 쓰면 `inadmissible_use` 위반으로 검출된다.
  `idpr_research_draft.md` §8.3(procedure-substance consistency), 잠정 contribution 3번 근거.
- **사용자 방향(2026-07-21)**: 절차-실체 동시판단이 중요한 쟁점으로 확정되면, 지금 보는 사기
  KCL smoke 1문항과 **같은 사실관계에서 나오는 절차법 쟁점 1문항**을 짝 smoke로 빼서 그 둘로
  절차 레이어 동작을 검증한다. **인벤토리에 이미 그런 짝이 있다**(예: r10_p1_q1 실체 죄책 +
  같은 청테이프 사실관계의 증거능력 절차 문항 q1_na/da). 최소 1건 inadmissible_use 데모로 범위를 좁힌다.
- 넣으면 "실체법과 절차법을 gating으로 연결" 기여를 주장하고, 빼면 실체법 정합성으로 한정한다.

## A5. 결론 구조화: 무죄와 미완결의 분리 (에이전트)

상태: **사용자 승인(2026-07-21), 착수 가능.** 논문 트랙에서는 A1 consistency 지표의 입력 정확도에 기여한다.

- `scripts/run_fraud_irac_matrix.py:231`의 우선순위는 conflict > not_established >
  undetermined > established다. 우선순위 자체는 법리적으로 타당하다(증명된 소극요건은
  다른 요건이 미확인이어도 무죄를 확정).
- 문제는 결론이 스칼라 하나라 `not_established`가 나오면 동시에 참인 `fraud_undetermined`가
  라벨에서 사라진다는 점이다. conclusion flip rate·consistency 집계가 이 손실을 오탐할 수
  있으므로, 결론을 (라벨, 미확인 요건 목록, 확정 소극요건 목록) 구조로 바꾼다.
- 이 구조는 장기 트랙(L1 수사지원)의 체크리스트 입력이기도 하다.

## A6. 부정형 카드의 극성 처리 수정 (에이전트)

상태: **완료 (2026-07-20, job `211051`/`211052`).** 전문 기록은 WORK_REPORT.md "부정형 카드
극성 분리" 절, 88장 문장구조 분류는 `fraud_card_linguistic_difficulty.md`.

원인: `fraud_intent.no_disposition_inducement_intent`(부정형, "…의사가 없으면 성립하지
않는다") 한 장에서 모델이 실질 판단과 반대 부호를 기록해 잘못된 `not_established` 3건을
만들었다. 활성 core+profile 카드 슬롯 25개 중 부정형은 이 한 장뿐이라 수정 범위가 작았다.

조치(사용자 승인): (1) **host 극성 분리** — registry에 `neural_query`(긍정 술어)를 두고
모델엔 긍정 질문만 던진 뒤 host가 부호를 되돌려 Scallop에 투입. 카드·규칙·인용 문언은 원문
유지. (2) **구조적 안전망** — 부정형 카드가 `satisfied`인데 근거가 같은 사건 긍정 카드의
근거와 겹치면 `unknown` 강등. 구현: `neural/__init__.py`의 `build_authority_packet`·
`resolve_neural_query_statuses`(역전 시 basis/counter swap)·`apply_negative_card_safety_net`.

| 지표 | 적용 전 | 적용 후 |
|---|---|---|
| 잘못된 `not_established` | 3건 | 0건 |
| 부호 뒤집힘 | 확정 5회 중 3회 | 확정 8회 중 0회 |
| 두 설정 카드 불일치 | 5 / 54 | 1 / 54 |
| 안전망 발화 | — | 0회 |

10런 전부 `undetermined`로 수렴, 두 설정 일치. 테스트 124 passed.

남은 것: (1) `run_fraud_neural_e2e.py:194` 구 경로가 부정형 원문을 아직 모델에 보냄 →
B2에서 정리. (2) 나머지 negative 24장은 배선 시 질의문 초안 승인(이중부정 11장 우선).

## A7. 5건 paraphrase 2강 결과 육안 검토 (사용자)

상태: 검토 자료 생성 완료, 사용자 1차 확인 완료. A3 평가셋 결정의 입력이 된다.

사용자 결정(2026-07-20): gold 라벨링을 선행하지 않고 10건 결과를 직접 육안으로 확인한다.

- 검토 자료: `data/e2e/fraud/manual_paraphrases/fraud_paraphrase_10run_visual_review.md`.
  **1번 수정 후 실행(job `211051`/`211052`) 기준으로 재생성했다.** 수정 전 실행
  (`210499`/`210500`) 기준 자료는 같은 파일의 git 이력에 있다.
  기존 `fraud_manual_card_review.md`의 빈 `사용자 판정` 칸은 채우지 않는다.
- 수정 전에는 두 설정이 공통 판정한 54개 카드 중 49개가 일치하고 갈린 5개 중 4개가
  1번의 부정형 카드 하나였다. 수정 후에는 53개가 일치하고 갈린 카드가 1개다.
- 사실추출 충돌은 실질적으로 없다. fact ID 부여만 다르고(`fact_011` vs `fact_101`) 문장은
  동일하며, 총량은 greedy 34 / sampling 32다. 유일한 실질 차이는 sampling이 차용금
  사건에서 만든 `fact_107`("A가 대여금 채무를 변제할 의사나 능력이 있었는지 여부는
  확인되지 않는다", `epistemic_status: unknown`)인데, 없는 사실의 날조가 아니라 공백을
  명시한 노드다. 사용자 평가대로 사실 분리는 양호하며 sampling이 근소하게 낫다.
- confidence 1.0 편중은 paraphrase 사건에서 해소됐다(0.5~1.0 분산). 별도 조치 없음.
- 사용자 판단(2026-07-20): 결론이 설정별로 달라진 것 자체는 현 단계에서 치명적이지 않다.
- 남은 조정: intent 계열 카드의 객관적 정황 추론 허용 폭. 현재 10런이 모두
  `undetermined`이고 intent 계열이 대부분 `unknown`인데, 성립 방향으로 넓힐 이유가 있는지
  사용자 검토가 필요하다(장기 트랙 L1에서는 그 목록 자체가 산출물이다).

---

# B. 파이프라인 정합성 트랙 (논문에 직접 안 들어가나 품질 유지)

## B1. materiality 경계의 법률 검수 (사용자)

상태: **사용자 결정(2026-07-21): 2번(부정형 카드 배선) 채택.** A6 극성처리 완료로 부정형
카드 불안정 문제가 해소되어 2번의 리스크가 사라졌다. 착수 대기.

- 진동의 원인이 된 긍정 카드: `deception.fraud.standard.loan-purpose-materiality`(출처
  `comm_001692_제347조_Ⅳ.1_12`; 용도를 속여 빌린 경우 진정 용도를 고지했더라면 대여하지
  않았을 관계면 성립). 프로파일 `loan_purpose`의 `irac_deception` 단위에 배선. 이 카드가
  **대여자의 반사실적 의사**("고지했더라면 안 빌려줬을 것")를 요구하므로 사건에 근거가 없으면
  `unknown`이 정직한 출력이고, 그러면 기망 단위가 안 닫혀 전체가 `undetermined`가 된다.
  카드 문언 자체는 주석 원문과 일치하므로 수정하지 않는다.
- 채택된 조치(2번): 짝 부정형 카드 `deception.fraud.causal-link.loan-purpose-not-sole-trigger`
  (용도 진실 여부가 대차의 유일 계기가 아니면 인과관계 부정; 88-card 세트엔 있으나 현재
  미배선)를 `loan_purpose` 프로파일의 인과관계 단위에 부정형으로 배선한다. 용도가 유일 계기가
  아니라는 반대 사실이 확인될 때만 성립을 차단하므로, 긍정 카드가 `unknown`이어도 인과관계 쪽
  판단 근거가 생긴다. 배선 시 A6와 동일한 host 극성 분리(질의문 승인)를 적용한다.
- 우선순위: A3 평가셋이 loan_purpose 프로파일 사건을 포함할 때 실효. 미배선 시 해당 카드의
  `missing_facts`("대여자가 진정 용도를 알았다면 대여하지 않았을 사정")는 L1 수사 확인 항목으로
  남는다(손실 아님).

## B2. 전역 RuleIR 호환 코드 정리 (에이전트)

상태: 사용자 승인 완료(2026-07-20, "레거시는 전부 정리"). **우선순위 낮음 — 언젠간 정리(사용자 2026-07-21).** 착수 대기

- 대상: 88-card RuleIR에 남은 구 `assess_*` 입력 관계. 활성 M5 경로에서는 선택·입력되지
  않으나 다음 파일에 잔존한다.
  - `rules/generated/fraud_article347_full_v1.scl`
  - `data/rulegen/fraud/fraud_full_rule_ir_candidate_unreviewed.json`,
    `fraud_full_rule_ir_sol_request.json`,
    `fraud_full_rule_ir_natural_language_scaffold.md`,
    `fraud_full_rule_ir_natural_language_explanation.md`
  - `scripts/build_fraud_full_rule_ir_candidate.py`, `scripts/run_fraud_full_rule_ir_critic.py`,
    `scripts/run_fraud_irac_matrix.py`, `scripts/run_fraud_neural_e2e.py`
  - `src/idpr/generation/__init__.py`, `tests/test_fraud_irac_matrix.py`
- 정리 시 Scallop 프로그램이 재생성되므로 기존 실험 artifact의 재현 경로가 끊긴다.
  구 artifact는 삭제하지 않고 `pre_assess_removal` 백업으로 옮긴 뒤 진행한다.
- 완료 기준: 전체 테스트 통과, KCL 1건과 paraphrase 5건의 결론이 정리 전후로 동일.
- A6의 남은 divergence(`run_fraud_neural_e2e.py`가 부정형 원문을 모델에 보내는 문제)도
  여기서 함께 처리한다.

## B3. M6 evaluator/fallback 경로 이관 (에이전트)

상태: **보류(2026-07-21, 사용자).** M6 자체는 **이미 구현돼 matrix에서 실행 중**이다
(`run_claim_verification`: ClaimGraph 추출 + 위반 구획 재작성, 프롬프트 2종, m6_claim_verified).
보류 대상은 이것을 **whole-IRAC 4구획 계약으로 이관**하는 작업이다. 논문에서 M6은
상한선/fallback이라 우선순위가 낮다(§7.1: IDPR verify = M5+M6). 아래 설계 제약은 재개 시 참조.

사용자 코멘트(2026-07-20): rewriting 방식과 confidence 기반 트리거는 채택하되,
수정 범위를 한정하고 다중 LLM 호출의 병목을 줄이는 설계가 필요하다.

- M6을 whole-IRAC 4구획 계약으로 재작성하려면 ClaimGraph·section repair 계약을 이관해야
  한다(고정 5단락/15 claim 가정 제거, `idpr_prompt_reset_v2_review.md` §17-5).
- 확정 설계 제약:
  1. **수정 범위 한정**: 재작성 대상은 위반이 검출된 구획 하나로 제한한다. 답안 전체
     재생성이나 결론 문장 변경은 허용하지 않는다.
  2. **트리거 조건**: 카드 confidence와 검증기 위반을 함께 본다. 위반이 없으면 호출하지
     않으므로 정상 경로의 추가 비용은 0이다.
  3. **호출 수 상한**: 사건당 재작성 호출 상한을 두고(초과 시 위반을 남긴 채 종료),
     여러 구획에 위반이 있으면 구획별 순차 호출 대신 한 번의 patch bundle로 묶는다.
     현재 사건당 2회인 모델 호출이 최악의 경우에도 3회를 넘지 않도록 한다.

---

# L. 장기 트랙 (8/11 논문 이후, ACL 2027 방향)

`idpr_research_draft.md` §1 "장기 IDPR"에 해당한다. 논문 데드라인 전에는 착수하지 않되,
논문의 설계 결정이 이쪽과 충돌하지 않도록만 관리한다.

## L1. 수사지원 산출물 (프로젝트 최종 목표)

파이프라인의 최종 출력을 유무죄 판정이 아니라 **수사관이 무엇을 더 확인해야 하는지**로
두는 구상이다. Scallop이 닫지 못한 구성요건과 카드별 미확인 사유로 확인 항목을 만들고,
유사 판례(사실심·법률심 분리 적재)를 붙여 보강 의견을 낸 뒤 체크리스트 → 수사계획 →
피의자신문·참고인조사 질문지 → 영장신청서 별지로 이어진다.

- 현재 파이프라인의 약점이 강점이 된다. 5건 전부 `undetermined`이고 intent 계열이
  대부분 `unknown`인데, 성립 판정 정확도로 보면 나쁘지만 수사지원에서는 그 목록이
  산출물이다. 요건 단위 설명가능성이 순수 LLM 체크리스트와의 차별점이다.
- 이미 산출되는 재료(10런 실측): FactGraph `unresolved_questions`(설정별 7개), 카드
  `missing_facts`(greedy 29 / sampling 26). 후자는 **구성요건 단위에 앵커되어 있다.**
- 선행조건: A5(결론 구조화)의 (라벨, 미확인 요건, 소극요건) 객체가 체크리스트 입력이다.
- 주의: 영장 별지·신문사항은 수사기관 문서이므로 모든 항목이 카드 또는 판례에 앵커되어야
  한다는 더 강한 검증이 필요하다.

## L2. RAG 판례 연결

상태: 목적 확정(2026-07-20). L1의 판례 보강 단계다. **검색 기구 자체는 이미 있다**: 558
retrieval 카드 위 결정론 BM25 인출(`build_fraud_rag_packet`)이 구현돼 m2/m3에서 실행 중이다.
L2는 이 검색의 *용도*를 재정의하는 작업이지 검색을 새로 만드는 게 아니다.

RAG의 용도가 장문 생성 보강이 아니라 **미확인 요건의 수사 착안사항 생성**으로 확정됐다.

- 자원: 사용자 보유 판례 인덱스(사실심·법률심 분리 적재), 수사 착안사항 데이터.
  프로젝트 내 RAG/future-work 카드 558장.
- 붙일 지점: 자유 서술 보강이 아니라 **특정 카드의 `missing_facts`를 질의로 삼아** 유사
  사실심 판례를 인출하는 구조. 사실심은 정황 사실의 목록을, 법률심은 카드 자체의 해석
  기준을 제공한다.
- 핵심 법적 제약: **판례로 사실인정을 하지 않는다.** 판례는 "그 요건이 인정된 사건에서
  법원이 무엇을 근거로 삼았는가"를 제공하고, 그 근거가 **확인해야 할 항목의 목록**으로만
  변환된다.
- 주입량: Gemma 4 26B A4B의 장문맥 회상 한계(MRCR 44.1%)와 vLLM `--max-model-len 32768`을
  고려해 소수 정선 주입을 유지한다.
- 참고: 논문 트랙 A1에도 retrieval 품질 지표(§8.4)가 있으나 그것은 현행 commentary/precedent
  RAG의 인용 정확성 채점이고, L2는 수사 착안사항 생성이라는 별개 용도다.

## L3. 사기 외 죄명 확장

상태: **rulegen 확장 자체는 A3의 실행 항목으로 승격(2026-07-21).** KCL 61 커버가 논문
평가셋이므로 사기 외 죄명 rulegen은 더 이상 순수 장기 트랙이 아니다. inventory 61건 중 사기
외 영역은 rulegen 미착수이며, 확장 방식은 A3 참조(주석서 기반 API 생성 + 사람 검토). 착수 시
형법총칙·특별법 commentary corpus 부재 항목은 unavailable로 유지하는 기존 원칙 준수. 8/11 안에
커버할 범위를 넘는 죄종·절차 쟁점 고도화만 장기 트랙(L4)으로 남는다.

## L4. 논문 확장 (ACL 2027)

상태: NLLP non-archival 제출(8/11) 이후. archival 확장 시 더 많은 죄종·절차 쟁점,
paragraph-level verification 고도화, Natural Innocent 죄명 정렬 LJP subset을 검토한다
(`idpr_research_draft.md` §1, §2.3).

## 종결된 항목

### thinking 레버 (2026-07-20 확정)

thinking은 끄는 것으로 확정한다. greedy+thinking은 비종결 루프, 샘플링+thinking은 인용
전사 오탈자 1자로 차단된 이력이 있고, 재도전에 필요한 인용 오류 재시도 정책은 "host가
모델 출력을 보정하지 않는다"는 원칙과 충돌한다. 재검토하지 않는다.
