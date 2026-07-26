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

**진짜 남은 핵심 4가지**: (1) 평가 지표 집계·통계 층(A1) — **코드 골격 완료(2026-07-21):
`src/idpr/eval/` 집계기+McNemar+bootstrap CI. 남은 건 code→지표 매핑의 법률 검토와 A3에 물린
평가셋 스윕**, (2) KCL 61 커버 rulegen 확장(A3=L3), (3) 절차 레이어 whole-IRAC 배선(A4),
(4) 결론 구조화(A5).

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

### 집계·통계 층 (실제 A1 작업)

`idpr_research_draft.md` §8의 지표를 **사건 집합 × 시스템** 위에서 자동 집계하는 층.

1. **§8.2 rate 집계 — 구축됨(2026-07-21).** `src/idpr/eval/__init__.py`에 매트릭스 리포트
   로더(`load_matrix_reports`)·집계기(`summarize`)·마크다운 표(`render_markdown`) 구현. per-run
   `answer_validation_violations`(+m6 `violations_after`)를 argument-conclusion consistency,
   contradiction, unsupported rule, fact hallucination, conclusion flip 5개 rate로 **여러 사건에
   걸쳐** 묶는다. 재채점이 아니라 이미 도는 채점기 산출을 집합 수준으로 집계·명명하는 일이었다.
   **위반 code→§8.2 지표 매핑은 법률-의미 판단이라 `METRIC_CODE_MAP` 단일 상수로 격리했다 —
   사용자 검토 필요**(각 code가 어느 rate에 계상되는지가 논문 headline 숫자를 정함).
2. **통계층 — 구축됨(2026-07-21).** 같은 모듈에 paired 정확 McNemar 검정(`mcnemar_exact`,
   stdlib exact binomial)과 percentile bootstrap CI(`bootstrap_rate_ci`, numpy, seed 고정)를
   구현. `summarize`가 reference(IDPR/M5) vs baseline을 지표별로 대응 검정한다. scipy 미선언이라
   stdlib+numpy만 사용. 검증: `tests/test_eval_aggregation.py` 14건 + 전체 138 passed(miniconda).
3. **§8.1 legal quality — 잔여(단 rubric 데이터는 이미 있음, 2026-07-21 정정).** "rubric 데이터가
   repo에 없어 확보가 선행"은 틀린 기술이었다. **전체 채점 rubric이 원본 parquet에 있다**:
   `lbox_kcl_essay` `test.parquet`(169행)의 `rubrics`(문항당 이진 체크포인트 배열, 61문항 합
   1166항목)·`score`(배점)·`supporting_precedents`(gold 판례 원문). inventory에는 요약 5개
   (`rubric_summary`)와 개수(`rubric_count`)만 저장돼 있으나 전량은 parquet에서 인출 가능.
   rubric 항목 유형이 쟁점(issue spotting)·판례 인용 설명(rule statement)·사안 적용(application)·
   결론(conclusion)으로 나뉘어 §8.1 하위지표에 직접 대응한다. **judge 하니스 순수 코어
   구축됨(2026-07-21)**: `src/idpr/eval/rubric.py`에 sp_qwen `src/eval/kcl/{judge,gold}.py`
   (사용자 확정 2026-06-21)를 포팅 — rubric 로더(inventory↔parquet 조인)·유형분류·안전장치
   (인용 실재검증·조문게이트)·채점(satisfied/total, 유형별 recall). 검증: `tests/test_rubric_grading.py`
   12건 + 전체 150 passed. **남은 건 실제 judge 호출**(답안×rubric→O/X): 프롬프트+API라 승인
   게이트이고, 지금은 `DeferredJudge`가 실행을 거부해 자기채점 사고를 막는다. 결정 2건 대기 —
   ① 활성 judge 프롬프트 승인, ② judge 모델(백본 Gemma 자기채점 vs 독립모델, §12.5 순환성).
   순환성 통제(§12.5): rubric은 채점에만 쓰고 prompt·RAG·rulegen에 노출하지 않는다. IDPR은
   구조화 JSON 출력(`complete_json`)이라 sp_qwen 자유서술 파싱 대신 verdict JSON 스키마로 포팅.
4. **전 평가셋 스윕 러너 — 잔여(집계층의 실물 입력).** 현재 매트릭스는 사건 1건씩 돈다. 평가셋
   (A3) 전체 × 시스템을 쓸어 사건별 `fraud_irac_matrix_report.json`을 뽑는 스윕이 있어야
   `summarize`가 n>1 표를 낸다. **스윕 = vLLM 호출이라 승인 게이트·A3 확정에 게이팅됨.**
   집계 CLI는 준비됨: `scripts/aggregate_eval_matrix.py <리포트들/디렉터리>`가 스윕 산출을 바로 조준.
- 정리하면 A1의 코드 골격(1·2)은 완료돼 "스윕이 나오면 바로 조준 가능"한 상태다. 남은 건
  매핑의 법률 검토(1)와 §8.1 rubric(3)·평가셋 스윕(4)이며, 4는 A3에 물려 있다.

## A2. 베이스라인 러너 (에이전트)

상태: **6방법 러너 이미 가동.** `run_fraud_irac_matrix.py`가 M1~M6을 돌린다. 이 중
m1_direct·m2_rag·m5_irac_plan·m6_claim_verified가 §7.1 9종의 Direct IRAC·RAG-only·IDPR
generate·IDPR verify에 해당하고, m3/m4는 중간 ablation이다.

- 미착수는 나머지 5종: Few-shot IRAC, Plan-then-write, Self-Refine, Best-of-N + LLM judge,
  Doctrinal critique(DCDE). 동일 모델·temperature·budget·prompt hash cache로 공정 비교(§7.3).
- 단일 사건 러너를 평가셋(A3) 스윕으로 감싸고 A1 집계층으로 채점되면 논문 표가 된다.

## A3. 평가셋 확정 (사용자 + 에이전트)

상태: **KCL 커버 재산죄 벌크 HITL 완료 · core 카드셋 조립 완료 · 질의문 잔여분 승인 대기(2026-07-25).**
최종 universe는 KCL 61문항 커버. 사기 5건 수동 paraphrase는 정합성 검증용 smoke다.

**2026-07-25 진척 (API 0회):**
- **재산죄 core 확정 427장.** 결정 A/A2·B·C/C2를 카드에 일괄 반영하고(v3~v5), 카드결함 감사와
  절 계층(ancestry) 감사로 추가 강등(v6), 파서가 놓친 사용자 취지 1건을 정정해 확정(v7).
  452 → **427장**(standard_input 326 / deterministic_rule 101, 이중매매 21장은 별도 트랙).
  학설선택 승격 43장 포함. 원장 `core_finalize_ledger.json`·`결정C_승격원장.json`.
- **사기 core도 같은 축으로 전수감사** — 88 → **84장**(판단지침형 1·증명법 1 강등, 중복 2 병합,
  메타 래퍼 2 재작성). RuleIR은 강등 카드 단독근거 규칙 15개·술어 8개를 제거해 재빌드
  (`fraud_full_rule_ir_rebuilt.json`). `fraud_core_rule_selection_audit.json`의
  `method: ..._no_api`는 "API 없이"라는 뜻이고 전수 인간검토가 아니다 — 두 세트의 검토 수준이
  다르다고 읽은 것은 오독이었다(정정).
- **core → NormCardSet 조립 완료** (`scripts/build_property_core_norm_card_sets.py`,
  산출 `data/rulegen/property/core_norm_card_sets/art*.json` 16개). v7은 감사 원장이라 카드 원본
  필드가 없어 RuleIR 입력이 못 된다. merge 산출 카드에 v7 판정을 되돌려 반영하고
  (`final_role`→`formalization`, 재작성 명제 47장, `review_required` 해제 277장,
  `disputed`→확정 43장) **전 조문이 `idpr/NormCardSet` 계약 통과**.
  - **인용 축자성 복원 17건**: 주석서 OCR이 낱말 중간에 넣은 공백을 모델이 정리한 것 11건은 원문
    구간으로 되돌리고, 문장을 압축한 6건은 정렬 구간의 원문 문언으로 복원했다. 이걸 고치기 전에는
    제355조·제328조가 계약 위반이었다(quote가 commentary의 정확한 부분문자열이 아님).
  - merge 단계 계약까지 건 엄격검증 지적 **47장/427**: 대부분(32장) 후보 polarity=negative를
    카드가 exception으로 재분류한 것이고 이는 정상 승격이다. 나머지는 추적성 드리프트
    (인용 출처가 연결 후보 밖 10·norm_kind 혼합병합 8·후보 id 미존재 6 등) → 원장
    `core_norm_card_set_ledger.json:strict_findings`.
- **결정 B-2 발행(승인 대기)**: 결정B 큐가 `polarity=='negative'`만 담았고 merge가 부정형 명제
  일부를 `exception`으로 재분류한 탓에, core의 negative/exception 127장 중 **44장이 질의문 심사를
  건너뛰었다**. standard_input 32장 질의문 초안 + deterministic_rule 12장 면제로 정리했다
  (`결정B2_예외형질의문승인.md`, `scripts/draft_exception_queries.py`). 부정형 명제가 모델에
  도달하지 않게 하는 장치라 **배선 전 승인 필요**.

**2026-07-23 진척 (상세: `rulegen_sweep_cost_estimate.md` §8·§9):**
- **장물 다운스트림 파일럿** — 죄명-불문 드라이버 `scripts/run_rulegen_downstream.py`(merge+normcard
  critic) 신설·실측. RuleIR은 **죄명별 인간 게이트**(reviewed core set + 10항목 preflight)라
  자동 스윕 불가 → 캠페인은 (추출+merge+critic 자동) → **벌크 HITL** → (RuleIR 자동) 3단이다.
- **KCL 커버 재산죄 17조문 벌크 완주**(sbatch job 212240, 1h07m, **$34.26**): 1,671 후보 →
  **NormCard 1,112장**. 오케스트레이터 `scripts/run_property_campaign.py`(추출·다운스트림 idempotent).
  범위 표현 주의: "재산죄 각론 전반"이 아니라 **KCL 61문항이 커버하는 재산죄**다(주요조문 47 중 19).
- **벌크 검토자료 생성 완료**(`data/rulegen/property/`, API 0회) — 사용자 지시 3.1~3.5를 라우팅
  규칙으로 구현. 자동 97 / 에이전트수정 244 / **사용자 검토 570**. 3.4 긍정형 질의문 초안 190건은
  에이전트가 직접 작성(규칙기반 변환은 비문이라 폐기). 진입점 `property_legal_review_guide.md`.
- **core scope 감사 완료 (2026-07-23, API 0회)** — merge가 올린 core 896장 중 **444장을 강등**해
  **최종 core 452장(50.4%)**. 1차는 사기 정답 646장으로 검증한 표지 자동강등 298장(강등 정밀도
  97.8%/재현율 48%), 2차는 잔존 598장 **전수 판독** 146장(구체사안 66·죄수경합 16·메타서술 15·
  타법률 15·중복 12·절차증거 9·총칙 7 등). 산출 `property_core_set_final.json`,
  스크립트 `audit_core_scope.py` → `build_final_core_set.py`.
  - **총량을 사기와 직접 비교하면 안 된다**: 사기 646장은 죄명 하나였고 core 88장이다. 재산죄는
    조문 17개(죄명 약 12개)이므로 죄명당 ~38장으로 사기보다 오히려 얇다. 감사 목표치를 "사기 환산
    150장"으로 잡으면 과잉 강등이 된다.
- **결정 B 재발행** — 구판 190건은 감사 **전** 모수라 폐기(그중 103건이 context_only로 강등).
  최종 core 기준 **99건**(구판유지 87 + 신규 12, 이중부정 26). 신규 12건은 remediation 이후 늘어난
  negative core가 구판 초안에 반영되지 않아 누락돼 있던 것이다. `결정B_질의문승인_v2.md`,
  스크립트 `rebuild_decision_b.py`.
- **누적 예산 $61.2 / $100, 잔여 ~$38.8.** P2 OOS 비재산 30조문은 ~$43.6로 잔여 초과 → 부분 커버 결정 필요.

**결정 B-2 검토 완료 (2026-07-25) + RuleIR 단위 확정:**
- 1부 32건 중 코멘트 11건, 2부 면제 12건 전부 승인. 반영: **강등 5장**(사후 반환의사·범행 전
  상계정산·수분양권 위임(22와 중복)·법인 운영권 청탁(지엽) + 다른 원인 교부(11과 중복병합)),
  질의문 수정 3건, 질의 면제 이동 1장(행정절차상 불법 — 항변 차단 규칙이라 물을 사실 없음).
  core **427 → 422장**(standard_input 320 / deterministic_rule 102). 질의문 26 + 면제 13.
  원장 `결정B2_반영원장.json`, 최종 `property_exception_query_final.json`.
  - 코멘트 2건은 확인만 하고 초안대로 뒀다. 제350조 준강도-강도 경계 카드의 극성 방향은 맞고
    (혼동은 "예외형 카드가 강도죄 성립을 긍정한다"는 표기에서 왔다), 배임증재 대칭은 이미
    `art357_sec4.giver_view_justification`(결정B 승인분)이 증재자 관점을 담당해 확보돼 있다.
- **RuleIR 단위 = 죄명 9 + 공유 모듈 2** (사용자 결정, 설계 `rulegen_rule_ir_units.md`).
  `scripts/build_rule_ir_units.py` → `data/rulegen/property/rule_ir_units/*.json` 11개,
  **전 단위 계약 통과(422장)**. 제355조는 `comment_id`의 항 표시로 기계 분할(1항 60/2항 33, 혼합 0),
  제356조는 절 구조로 분할(Ⅲ.1 횡령·Ⅲ.2 배임·나머지 10장은 업무자 신분 공유 모듈).
  가중유형은 기본죄와 한 단위(특수절도→절도, 강도류→강도)에 두어 기본 요건 카드를 복제하지 않는다.
  친족상도례는 성립이 아니라 처벌·소추 층이므로 독립 규칙집합 + 브리지 술어
  `property_crime_established`로 받는다.
- **강도 기본조문 누락은 자산 부재가 아니었다(정정).** 처음에 "주석서 코퍼스 부재 → uncovered"로
  적었으나 오독이다. 원천 파싱본(`sp_qwen/.../commentary_chunks/docs.parquet`, 형법 4,011 chunks /
  251 조문)에 제333조 [강도] **51 chunks가 절 구조까지** 있고 원본 PDF도 있다
  (`sp/commentary_criminal.zip`, casenote PDF 373개). IDPR 번들(3,108/96)이 KCL 태그 매핑에서
  빠뜨린 것이다. 기존 카드가 전제하는 조문만 보강 대상으로 추렸다 —
  제333조 51 + 제332조 상습범 15 + 제330조 야간주거침입절도 5 = **71 chunks / $3.61**.
  `scripts/extend_commentary_bundle.py`로 보강 번들·요청 JSONL 생성 완료(정본 번들은 미변경).
- **친족상도례는 A4 절차 레이어로 이월**(사용자 결정). 형 면제(1항)·친고죄(2항)는 성립이 아니라
  처벌·소추 층이고 절차 레이어가 다루는 층과 같다. 재산죄 트랙에서는 카드를 독립 모듈로 떼어
  두는 데까지만 하고(25장, 계약 통과), 브리지 술어 `property_crime_established`를 preflight에
  넣어 두고 받는 쪽 규칙은 A4에서 쓴다. 친족 준용 조문(제344·354·361·365조) 보강도 그때 함께.

**보강 추출 완주 (2026-07-25, job 213426, 9분 17초, 실지출 $4.87):** 제330·332·333조 71 chunks →
후보 145 → **NormCard 145장**(42 모듈). 견적 $3.61을 35% 초과했는데, 다운스트림 비용이 chunk가
아니라 **모듈 수에 붙는 고정비**(스키마+gold exemplar 프롬프트)에 지배되기 때문이다(제330조
$0.102/chunk vs 제333조 $0.0525/chunk). 소규모 조문 견적은 모듈 수 기준으로 잡는다. 누적 $62.4/$100.

**보강분 전수 판독 완료 (API 0회, `scripts/audit_supplement_core.py`):** 145장 → **core 49장**
(art330 4 · art332 9 · art333 36). 강등 68장(죄수 28 · 공범총칙 12 · 구체사안 13 · 타법률 7 ·
판단지침형 3 · 증명소송법 3 · 근사중복 1 · merge판정 1). 제332조는 '상습범'이 총칙 표지에 걸리지만
조문 자체가 가중유형을 정하므로 구성요건으로 남겼고, 제333조 Ⅹ·Ⅸ절 33장은 축대로 내리되 KCL이
묻는 쟁점 5건은 확인 항목으로 올렸다. **학설선택 23장 + 확인 5건이 사용자 검토 대기**
(`data/rulegen/property/보강3조문_검토요청.md`).

**보강분 검토 반영 완료 (2026-07-25):** 학설선택 10그룹 중 8건 제안대로, **2건 사용자 정정** —
제333조 선행상태 이용은 판례가 인과관계 부정설(`unconsciousness_prior_force_no_causation`)이고,
권리행사는 대법원이 소극설(`right_exercise_robbery_negative`)이다. 후자는 내가 근거로 든 공갈죄
카드와의 정합성이 실은 반대 결론을 가리킨 경우다. 승격 10 / 학설강등 13 / 확인 5건은 무응답이라
감사 판정 유지(되돌리려면 `apply_supplement_review.py`의 `USER_CHECK_DECISION` 한 줄).
**core 481장**(v8 422 + 보강 59), 조문별 카드셋 19개·죄명 단위 11개 전부 계약 통과.
`robbery` 56 → **99장**(강도 기본 구성요건 채워짐), `theft` 50 → **66장**.

**결정 B-3 발행(승인 대기):** core 481장 중 부정형·예외형이면서 승인 질의문이 없는 19장 →
질의문 13 + 면제 6(`결정B3_보강조문_질의문승인.md`). B-2 지적 반영으로 **발동 시 결론**을 항목마다
적었고, 이중부정이 되는 4건은 있는 쪽 사실을 묻고 방향을 뒤집었다(`not_satisfied`).

**결정 B-3 검토 반영 완료 (2026-07-25):** 지적 4건 중 3건이 내 오독이었다.
① 제332조 동종성 — "절도·강도·사기"는 죄종을 번갈아 한 것이 아니라 각 죄종이 상습 가중조항을 가져
포괄 서술한 것이다. 카드가 담는 규칙은 **동종성 판단의 범위**이므로 명제·질의문을 다시 쓰고 발동
결론을 "그 경력을 상습성 근거에서 제외"로 정확히 했다. ② 강도·공갈 경계 — 정도의 상한이 질의문에
없었다("반항할 수 있는 상태"로 긍정형 추가). ③ 부동산 재물성 — 원문이 "재물 아님 + 권리는 재산상
이익" 두 문장 한 세트라 쪼개면 규칙이 반쪽만 발동한다 → **카드 병합**(조립기에
`absorb_source_refs_from` 추가, 흡수 카드의 인용·후보를 함께 근거로 삼는다).
**core 480장**, 조문별 19개·단위 11개 계약 통과(`robbery` 98 · `theft` 66). 질의문 13 + 면제 6 확정
(`supplement_query_final.json`, 수정 3건은 재확인 대상으로 표시).

**가중유형 on/off 설계(사용자 요청)**: 출력 술어를 3층으로 — `<crime>_established`(기본범) /
`<crime>_aggravation(kind)`(가중 플래그 열거) / `charge(label)`(죄명 확정). 기본 요건 카드를 복제하지
않고, 플래그가 꺼지면 자동으로 기본범이 되며, 결과적 가중범은 폭행 고의 카드를 전제조건으로 요구한다.
상세 `rulegen_rule_ir_units.md` §3.1 — preflight 정식 항목.

**preflight 10항목 발행 (2026-07-26, 승인 대기):** `data/rulegen/property/RuleIR_preflight_10항목.md`
— scope / unit_granularity / outputs / **aggravation** / actor_roles / **bridge_predicate** /
neural_state / evidence_gate / fewshot / api_ceiling. 사기와 달라지는 것은 단위 11개별 출력 술어,
가중유형 플래그 분리, 공유 모듈 브리지(친족은 배출하는 쪽까지만). 부정형 카드 질의문 보유를 게이트에서
확인 — 승인 116 / 면제 26 / **미보유 0**.

**레벨(페이즈) 구조 확정 (2026-07-26):** `rulegen_rule_ir_phases.md`, 기계 판독본
`rule_ir_phase_map.json`. core 480장을 L0 적격·객체 123 / L1 실행행위 120 / L2 인과 3 / L3 주관 70 /
L4 단계 30 / L5 가중 99 / L6 위법성 10 / L7 처벌·소추 25로 배정했다. 레벨 순서가 계약과 맞물린다 —
부정이 최종 스트라텀에서만 허용되므로 `elements_met`(L0~L4) → `established`(`not justified`) →
`aggravation`(L5) → `charge` 순서가 강제된다. 조문 19개는 기본범 8 + 가중/특별유형 8 + 공유
수정요소 2 + 미수 처벌근거 1로 정리됐다.
**빈 레벨 = coverage 보고 항목**: L2가 3장뿐(재산죄 주석서는 인과관계를 독립 절로 두지 않고 일반론은
형법총칙 주석서 필요 — `causation`·`objective_attribution` uncovered와 정합), 점유이탈물횡령 L3,
권리행사방해 L4, 공갈 L5(특수공갈 미커버).

**RuleIR 생성 2회 실패 → 경로 정정 필요 (2026-07-26, 상세: WORK_REPORT):** preflight 승인 후 두 번
제출했고 둘 다 10단위 전부 계약 검증에서 막혔다($0.14 + $0.17 = **$0.31**).
1. 검증기가 사기 전용이었다(`fraud_established`·`fraud_case_roles`·`fraud.core.outcome.established`
   하드코딩) → `RuleIRGenerationProfile`로 파라미터화, 사기 기본값 보존, 테스트 150 passed.
   사기 artifact 게이트가 "검토 후 변경"을 정확히 잡아 사유 기록 후 재해시.
   내 레벨 설계도 계약 위반이었다 — `not justified`를 직접 쓰면 안 되고 L6 카드는 `has_negative`로
   흘러야 한다(부정을 쓰는 규칙은 최종 하나뿐).
2. **전제 자체가 틀렸다.** 사기 RuleIR은 terra 1콜 산출이 아니다 — terra 산출물은 **규칙 4개·술어
   6개**의 부분 초안이고(`fraud_full_rule_ir_terra_partial_output.json`), 최종 349 규칙은
   `build_fraud_full_rule_ir_candidate.py`(2,377줄)가 **결정론적으로 조립**한 것이다.
   completion 4,606토큰으로 349 규칙이 나올 수 없다는 점을 견적 때 알아챘어야 했다.
   → **preflight 2항목(단위당 1콜)·10항목($4.52)은 무효.** RuleIR은 LLM 생성이 아니라 검토완료
   카드에서의 **결정론적 컴파일**이고, LLM은 비평에만 쓴다(API ~0).

**RuleIR 조립 완료 (2026-07-26, API 0회)** — `scripts/build_property_rule_ir.py`가 사기 조립 규격을
죄명-파라미터화한다. **10단위 / 카드 455 / 술어 1,069 / 규칙 2,143 전부 계약 통과**,
Scallop 컴파일 18,771줄(`rules/generated/property_*_v1_candidate.scl`).
사기가 손으로 쓴 `COMPONENT_SOURCES` 자리에 **레벨 맵**을 넣어 480장을 손으로 매핑하지 않았다.
- 걸린 것 3개: `standard_input` 입력 술어는 `kind="standard"` 필수 / 배임수증재는 `defendant_id`
  슬롯이 없어 브리지 head가 unsafe → 첫 역할을 피고인으로 / 업무자 신분(공유 모듈)은 L5가 가중이
  아니라 자기 요건이므로 L0으로 읽고 브리지 미배출.
- **Scallop 런타임 골든 54/54 통과**(`scripts/run_property_scallop_golden.py`, scli 0.2.4 체크섬 고정):
  ordinary_established / incomplete_case_blocked / negative_bar_blocks / card_conflict_blocks /
  unknown_blocks / aggravation_flag_on. 런타임 모듈의 사기 전용 `ACTOR_FIELDS`·`fraud_case_roles`도
  RuleIR에서 역할 계약을 되짚도록 고쳤다(사기 기본값 유지).
- 회귀 테스트 `tests/test_property_rule_ir.py` **31건**(조립 결정론·계약·컴파일 일치·런타임·리포트).
- 레벨 문서 §1 정정: `not justified`는 계약 위반이고 L6 카드는 `has_negative`로 흐른다.

**`human_rule_ir_review` 완료 (2026-07-26, API 0회) — 재산죄 RuleIR 법리 검토 마무리.**
walkthrough(`rulegen_symbolic_layer_theft_walkthrough.md`)에서 "component 내부가 OR이라 소유·점유
같은 결합적(AND) 요건이 하나로 뭉개진다"는 결함을 발견해 10단위 전수를 카드 단위로 재검토·수정했다
(절도·배임·횡령·권리행사방해 객체/주관 분리, 강도는 재물강취/이득강취를 대안트랙(OR)+동시충족
conflict로 재모델링하는 `UNIT_TRACKS` 메커니즘 신설, 오배정 카드 5장 재배치). 사용자 지적으로 카드
역할 2건 추가 정정(bar→boundary), 반대로 위험한 제안 2건(aggravation-scope 카드·기수/미수 미배선
카드를 bar로 바꾸자는 것)은 근거를 확인해 반려했다 — 상세 WORK_REPORT 2026-07-26 항목.
최종 골든 55/55·pytest 31/31. 산출 `RuleIR_죄종별_조건식.md`(죄종별 조건식, 사용자 최종검토 완료).
**재산죄 RuleIR 트랙 완주.** 남은 것은 sol 비평(선택) — 계약·런타임·법리 검토가 전부 자동/사람
게이트를 닫았으므로 필수 게이트는 아니다. 누적 $62.7/$100(이번 세션 API 0회).

**파일럿·캠페인 진척(2026-07-22, 상세: `rulegen_campaign_launch.md`·`rulegen_sweep_cost_estimate.md`):**
- 사용자 결정: 61 **전체 커버**, 검토는 **한 번에 벌크**(죄명별 왕복 아님). 파일럿 죄명=장물(제362조).
- **파일럿 성과**: (1) terra/sol=gpt-5.6 **추론 모델** 확정 — 추출은 `reasoning_effort=low`+`max_tokens≥16000`
  필수(기본 6000은 reasoning이 전부 소진해 실패). (2) 밀도 = **사기의 0.5×**(장물 25 cand/배치 vs 사기 51)
  → 견적 하향 근거. (3) `norm_kind='negative'` 오배치(부정형 규범) → extract 프롬프트 규칙3 보강(승인).
- **캠페인 준비**: 실체 P1(재산범11)+P2(OOS비재산16) 형법각칙 **47조문/1,531 chunks/162 배치** requests 생성
  (`data/rulegen/campaign/`), 매니페스트·per-crime 런처(`launch_rulegen_campaign.sh`, 기본 dry-list) 완비.
  추출+critic ≈ **$35.5**(단가 terra $2.5/$15·sol $5/$30 per 1M). 절차(P3/P4)는 A4 별도 트랙.
- **남은 게이트**: ① 잔여 예산 확인 후 `--confirm` 착수(예산 게이트), ② 다운스트림(merge·RuleIR) 실단가를
  장물로 한 번 더 파일럿해 확정 권장, ③ 벌크 HITL(`hitl_bulk_review_spec.md`)로 유형별 1회 검토.
- **매니페스트 재스코핑 필요(2026-07-26 발견, 미반영)**: `kcl_substantive_campaign_manifest.json`의
  47개 대상에 재산죄 조문(art323·328·329·331·334·335·337·338·342·343·350·355·356·357·360·366)이
  여전히 포함돼 있다. 이 조문들은 위 재산죄 카드·RuleIR 트랙에서 **이미 다른 경로(주석서 직접 판독 +
  결정B/B2/B3)로 끝났다** — `excludes`에는 CC_347(사기)·CC_362(장물)만 있고 재산죄가 안 빠져 있다.
  이대로 `--confirm` 실행하면 끝난 조문을 중복 추출해 예산을 낭비한다. **실행 전 반드시 재산죄
  조문을 targets에서 제외하고 남은 P2(비재산) 조문만으로 비용 재견적** — `scripts/build_rulegen_campaign.py`
  손질 필요.

- **확장 경로**: 이미 정해둔 주석서 자료를 기반으로 KCL 61을 커버하도록 card·RuleIR 등
  Scallop 엔진용 재료를 API로 생성한다. **방식은 지난번 사기 rulegen과 동일하며 사람 검토를
  포함한다.** 곧 L3(사기 외 죄명 확장)이 이 경로의 실체이며, 논문 평가셋과 직결되므로 장기
  트랙이 아니라 A3의 실행 항목이다. 8/11 안에 61 중 어디까지 커버하느냐가 본실험 규모를 정한다.
- 오염 축(§12.5): KCL 기출은 학습 컷오프(2025-01)와 겹칠 수 있다. coverage tier(§12.2)로
  full-61과 rule 보유 covered-tier를 함께 보고하고 사후 제외하지 않는다. paraphrase 5건은
  오염 통제 대조군으로 병행 유지한다.
- 현재 진행: 파이프라인 정합성 + **최종 평가 방식(A2)** 결정을 함께 보고 있다.

### OOS 33건 검토 (coverage_candidate = out_of_current_rule_scope)

상태: **분석 완료(2026-07-21), 처리 방침 미결.** 61 중 현 rule DB로 실행 불가한 33건이며,
성격이 다른 두 하위군으로 갈린다(실체 16 / 절차 16 / mixed 1). 나머지 28건은 property_crime
11(현 사기 rule 근접)·procedure_gating 17(증거능력 gate 대상, A4)이다.

1. **실체법 비재산범 16건** — 뇌물·직무유기·위계공무집행방해·주거침입·중지미수·강제추행·
   상해치사·교통과실(과실·인과관계·객관적귀속)·공동정범·죄수 등. **사기와 동일 rulegen
   파이프라인으로 확장 가능**하며 commentary도 이미 선별돼 있다(예: CC_122 직무유기).
   A3=L3 rulegen 확장의 **실제 대상**이 이 16건이다.
2. **다른 절차 축 16건(+mixed 1)** — 상소(일부상소·상소심/환송 심판범위)·불이익변경금지·
   공소시효·재심·공소기각/형식재판·고소(친고죄)·변호인선임 추완·증거개시 등. **현행 gate가
   모델링하는 축은 증거능력(전문법칙·위수증) 하나뿐**이라(procedure_gating 17이 그 대상) 이
   17건은 현행 `admissible`/`provable` 술어로는 안 잡힌다. **단 신경-기호 접근 밖은 아니다** —
   오히려 불이익변경금지(형 경중 비교)·공소시효(날짜 계산·정지)·상소심 심판범위(확정범위 계산)는
   결정론 규칙으로 61문항 중 **가장 기호화하기 좋은** 축이다. 필요한 건 증거능력 gate와 별개의
   절차 규칙 저작이지, 아키텍처 밖이라는 뜻이 아니다.

처리 방침(결정 필요):
- 1번 실체 16건: 8/11까지 rulegen으로 몇 건 커버할지가 A3 본실험 규모를 정한다. paper
  universe 기여도 순으로 우선순위.
- 2번 절차 17건: 세분해서 본다. (a) **규칙친화**(불이익변경금지·공소시효·상소/환송 심판범위·
   항소이유서 기간)는 증거능력 gate와 별개의 신규 절차 규칙 저작으로 커버 가능하며, 결정론 축이라
   IDPR 논지에 오히려 잘 맞는 데모 후보다. (b) **학설 대립 중심**(상소이익·재심사유·항소심 사실오인
   재평가·불심검문 적법성 등)은 신경 측 부담이 크다. 8/11 내에서는 (a) 소수를 절차-실체 짝 데모(A4)에
   넣고, 나머지는 coverage tier(§12.2) uncovered로 정직하게 보고. 사후 제외가 아니라 tier 명시가 원칙.

**commentary 선별 상태 확정 — 후임자 인계(2026-07-21 감사, 착수 전 필독).** 사용자 질문("절차
17건은 commentary에서 선별 안 된 건가? 형소법 주석서가 있으니 안 됐으면 지금 선별하자")에 대한
코드베이스 확인 결과: **절차 commentary는 이미 선별 완료다. 신규 선별 작업 불필요.**
- **형소법 코퍼스가 이미 ingested** — `data/commentary/kcl_criminal_v1_commentary_pool.json`의
  `primary_source.laws`에 형사소송법(law_id `001671`, 571조 5373행)이 형법각칙과 함께 있다.
  즉 "형소법 주석서도 있다"는 소스는 파이프라인에 이미 들어와 있다.
- **OOS 절차 축까지 형소법 조문에 매핑됨**(`kcl_criminal_v1_tag_commentary_manifest.jsonl`,
  절차 태그 78 mapped / 1 gap / 2 unavailable): 불이익변경금지→제368조, 공소시효→제249조,
  일부상소·상소심범위→제342조, 재심→제420조, 공소장변경→제298조, 증거개시→제266조의3,
  긴급체포→제200조의3, 항소이유서→제361조의3 등 2번 그룹 전부가 `status: mapped`.
- **미매핑은 특별법 2~3 태그뿐** — `police_stop_questioning`(불심검문, `unavailable_reason`=
  경찰관직무집행법 주석서 부재)·`non_retroactivity`·`habitual_offense`. 이들만 coverage tier
  uncovered이며, 해당 특별법/총칙 주석서를 새로 넣지 않는 한 `unavailable` 유지(기존 원칙).
- **따라서 절차의 잔여 작업은 commentary 선별이 아니라 규칙 저작이다.** 후임자 to-do는
  (i) procedure_gating 17의 증거능력 gate 배선(A4), (ii) OOS 규칙친화 축(불이익변경금지·공소시효·
  상소심범위)의 신규 결정론 절차 규칙 저작 — commentary는 준비됨. 선별 파이프라인 재실행은 하지 말 것
  (이미 완료, 재실행은 예산 낭비). 특별법 주석서를 사용자가 추가로 제공할 때만 그 2~3 태그 재선별.

## A4. 절차 레이어 + evidence gating (에이전트 + 사용자)

상태: **수직 확장 범위 확정·절 선택 대기(2026-07-23).** 사용자 방향: 수평(각론 전반) 확장이
아니라 **수직 완결** — KCL 커버 재산죄와 **같은 사실관계를 공유하는** 문항의 절차 쟁점을 함께
닫는다. 같은 사실관계에서 실체+절차가 동시에 나와야 gating(§8.3) 실증이 성립하기 때문이다.

**범위 집계 결과** (`scripts/build_procedure_topic_scope.py`, 산출 `data/rulegen/procedure/procedure_topic_scope.json`):
- 재산죄가 걸린 **사실관계 9개** → 절차·mixed 문항 30개 → **유니크 절차 토픽 78개**
- 형소법 52조문. **per-issue 스코핑 필수**: 전량 1,374ch → 실제 필요 **453ch(33%)**.
  (조문 전량을 세면 5~6배 과대계상. 예: 제106조 압수 150ch 중 전자정보·참여권은 43ch뿐이고
  나머지는 강제채혈·DNA·지문·CCTV·계좌추적 등 문항과 무관. 견적문서 §4-1이 경고한 그 레버다.)
- 비용: 카드생성 **$24.1** + RuleIR $2.2 = **$26.3** (형소법 실측 $0.0533/chunk, 파일럿 cp342·cp308_2).
  축별로 A 증거능력·수사 39토픽/775ch/~$41, B 재판절차 35토픽/316ch/~$17.
- **형소법 밀도는 형법과 거의 같다(1.05×)** — "절차법은 얕을 것"이라는 가정은 파일럿으로 반증됐다.

**착수 전 필요:** ① 재산죄 벌크 검토 완료(선행), ② **절 선택 검토** — 절 제목 키워드 매칭은
휴리스틱이라 법률 검토가 필요하다(빠뜨리면 규칙이 비고 넘치면 비용 증가). 사용자가 벌크 검토
후 절 선택을 함께 주기로 함(2026-07-23). ③ 수동 스코핑 필요 5건 + unavailable 4건
(경찰관직무집행법·형법총칙 주석서 부재)은 coverage tier uncovered.

---

이하 종전 기술(증거능력 gate 자산):

현재 실체법 중 사기죄만 보고 있어 절차 레이어는 보류다. 단
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
- **절차 축은 둘이다 — 후임자 주의: 한 gate로 착각하지 말 것**(2026-07-21 정정 이력). (i) **증거능력**
  (전문·위수증 → 현행 `admissible`/`provable` gate·`inadmissible_use`, procedure_gating 17문항) —
  gate·검증기가 이미 있어 짝 데모에 바로 쓸 수 있다. (ii) **재판절차 규칙친화**(불이익변경금지·
  공소시효·상소심/환송 심판범위 등 OOS(a), A3 "OOS 33건 검토" 참조) — 형 경중 비교·날짜 계산 등
  **별개의 신규 결정론 규칙**이 필요하나 IDPR 논지에 가장 잘 맞는다. `inadmissible_use`로는 안 잡히는
  다른 절차 축이다. 짝 smoke는 (i)로 최소 데모를 먼저 뚫고, (ii)는 여력 시 별도 규칙으로 확장.
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
