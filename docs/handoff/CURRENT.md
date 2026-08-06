# Current handoff

기준: 2026-08-06 · 브랜치 `antigravity-0804`

## 지금 최우선 — 평가(judge)와 라우팅 구조 문제

**사용자 결정: 장물죄 원장 적재 작업은 잠시 보류. 이 문제부터 해결하고 원래 궤도로
복귀한다.** 26문항 Gemini 채점(아래)을 사용자가 직접 검토한 뒤 "말이 안 된다"고 판단,
FOL 답안 하나를 반례로 지목했다. 다음 세션은 여기서 시작할 것.

### 26문항 채점 결과 (job 219790, `gemini/gemini-2.5-flash`)

`/data5/jaehoonjeong/IDPR/.cache/phase3_judge_219779/summary.json` (method
`idpr_nsn_native_lean_219779`, 26/26 완료):

| 지표 | 값 |
|---|---|
| coverage_macro | 0.246 |
| consistency_macro | 0.692 |
| precision_macro | 0.838 / precision_micro 0.821 |
| hallucination_free_rate | 0.346 (hallucination_score_macro -3.27) |

**주의**: 이 26문항 안에 phase3 sealed-59에서 의도적으로 제외한 dev case 2개
(`kcl_criminal_r10_p1_q1_ga`, `kcl_criminal_r14_p1_q2`, `scripts/build_phase3_final_eval_inventory.py`의
`DEVELOPMENT_CASES`)가 섞여 있다. 다른 방법(baseline)들의 기존 결과는 61문항 대상이라
이 26문항 숫자와 그대로 비교하면 안 된다 — 재정리 필요.

사용자가 특히 의심한 비교: FOL Autoformalizer+Solver의 consistency 85.96 > IDPR
69.23. `experiments/results/fol_autoformalizer_solver_outputs.jsonl`의 `kcl_criminal_r10_p1_q1_ga`
답안을 열어 보면 Z3 코드에 `s.add(Guilty(甲, Death))`로 **결론을 사실로 먼저 주입한 뒤**
같은 결론을 satisfiability 결과로 재출력하는 패턴이 보인다 — 이건 검증이 아니라 반복이다.
그런데도 이 답안이 높은 consistency 점수를 받았다면, 현재 judge가 코드/symbolic trace의
의미를 읽지 않고 **자연어 결론이 처음부터 끝까지 반복되는지**만 보고 있을 가능성이 높다.

### 사용자 진단: judge 문제

- 현재 Outcome Consistency judge가 실제로 측정하는 것은 "중간 서술과 최종 결론의
  표면적 반복 일관성"이지, 원하는 "중간 쟁점 판단 — 적용 법리 — 상징 결과 — 최종 죄책"
  간의 정합성이 아니다.
- FOL 답안은 결론을 여러 형식(FOL facts / Z3 output / legal conclusion / summary)으로
  반복하므로 전제가 틀려도 형식적 일관성 점수를 얻기 쉽다.
- IDPR 답안의 정상적인 법률 논증 어투("...성립 가능성이 매우 높다", "...인정된다면
  최종적으로 성립한다" 같은 조건부 서술 후 단정적 결론)를 judge가 충돌로 오인할 수 있다.
- 다음 세션 작업: judge 프롬프트가 코드/symbolic trace를 실제로 평가 입력에 포함하는지부터
  확인. 그 다음 평가기준을 다시 설계하고 **judge 백본을 `anthropic/claude-sonnet-4-6`로
  교체**해 전체 재평가. IDPR을 제외한 나머지 baseline들은 새 judge로 미리 돌려둘 수 있다.

### 사용자 진단: 파이프라인(라우팅) 자체의 구조적 결함

judge 문제와는 별개로, 실제 두 사례(kcl_criminal_r10_p1_q1_ga, r14_p1_q2)를 검토한 결과
라우팅이 죄명 수준에서 멈추고 시험이 요구하는 법리 단위까지 못 내려가는 것으로 보인다.

1. **핵심 하위 법리 카드가 라우팅 안 됨** — 예: 제263조(동시범 특례)와 제19조(독립행위
   경합)의 관계, 특수강도(흉기휴대)와 단순강도의 구별이 답안에서 사라짐. 대표 죄명
   (강도치사, 인과관계)만 잡히고 그 아래 단위(비유형적 인과관계, 개입원인, 객관적 귀속,
   위험창출/위험실현, 규범의 보호목적, 기본범죄 기수/미수와 결과적 가중범의 관계)가
   안 잡힌다.
2. **상위 카드가 선택돼도 필수 하위 쟁점이 자동 확장되지 않는다** — 카드를 독립적으로
   검색하는 구조에 가까워서, 상위 죄명은 나오는데 그 아래 요구되는 법리가 누락된다.
3. **불확정 사실이 대안 법리를 호출하지 못한다** — `unresolved`가 새 분기를 여는 대신
   사실상 `not_satisfied`처럼 처리돼, 인과관계 불명 → 상해치사 불성립 → 상해죄 성립으로
   바로 가버린다. 원래는 인과관계 불명 → 독립행위 경합 검토 → 263조 적용 가능성 → 19조
   적용 여부까지 이어져야 한다.
4. **symbolic 결과가 결론만 주고 논증 의무는 안 준다** — 생성 단계에 결론(성립/불성립,
   인과관계 인정/부정)만 전달되고, 반드시 다뤄야 할 학설·요건(조건설/상당인과관계설/
   합법칙적 조건설, 위험창출/실현, 규범의 보호목적 등)이 체크리스트로 전달되지 않는다.
5. **정확한 죄명/유형이 생성 과정에서 단순화된다** — 특수강도로 라우팅/평가됐어도
   답안에는 그냥 "강도"로 나오는 사례. 어느 단계(라우팅 미선택 / predicate 미충족 /
   생성 단순화 / 표시명·법적명 미분리)에서 없어졌는지 로그 확인 필요.
6. **생성 모델이 라우팅 안 된 쟁점을 임의로 추가한다** — 예: 살인 고의를 불필요하게
   검토하면서 정작 필요한 특수강도·결과적 가중범 미수는 빠뜨림.
7. **불확정 사실을 조건부 분기로 유지하지 못한다** — 의료과실 정도가 불명확하면 통상
   과실/중대한 과오 두 경우로 나눠 각각의 객관적 귀속 결론을 내야 하는데, 지금은 생성
   모델이 하나로 임의 확정해버린다.

**핵심 진단(사용자 문구)**: "IDPR은 죄명 수준의 결론을 계산하지만 장문 답안에서 필요한
법리 수준의 쟁점 구조를 충분히 계산하지 못한다." "Judge를 고쳐도 이 구조적 누락은
그대로 남는다" — 즉 이건 judge 교체로 해결되는 문제가 아니라 라우팅/상징 출력 설계
자체를 손봐야 하는 문제.

### 다음 세션 작업 순서 (사용자 지시)

1. **결함 위치를 로그로 구분**: 카드가 있는데 미선택 = 라우팅 오류 / 하위쟁점 카드
   자체가 룰베이스에 없음 = 규칙베이스 범위 오류 / 카드 선택됐지만 분기 미실행 = 상징
   규칙 오류 / 분기 결과는 있었지만 답안에서 빠짐 = 생성 단계 오류. r10/r14 두 사례부터
   시작해서 각 결함이 정확히 어느 단계인지 특정.
2. **라우팅 출력 확장**: `selected_issues` 외에 `required_subissues`,
   `conclusion_sensitive_facts`, `unresolved_branch_points`, `alternative_legal_routes`,
   `required_conclusions` 반환. 단, 모든 불확실성을 분기하면 precision이 떨어지므로
   **사실 판단에 따라 적용 법리나 최종 죄책이 달라지는 지점만** 분기.
3. **symbolic 출력 확장**: 결론뿐 아니라 `activated_rules`, `required_issues`,
   `required_doctrines`, `alternative_branches`도 반환해 생성 단계로 넘김.
   `required_issues`는 문장 순서를 통제하지 않고 최종 생성에서 반드시 다뤄야 할
   체크리스트로만 쓴다 — 자유 장문 생성이라는 현재 설계는 유지.
4. **judge 재설계 + 백본 교체**: 위 judge 절 참고. 코드/trace가 실제로 평가 입력에
   들어가는지 확인 → 프롬프트/기준 재설계 → `anthropic/claude-sonnet-4-6`로 전량
   재평가. 우리 파이프라인 외 baseline들은 새 judge로 미리 돌려둘 수 있다.
5. 이 네 가지가 끝나면 **원래 궤도(장물죄 146장 원장 적재)로 복귀**.

---

## 이 세션에 반영된 것 (커밋 대상, 미완료 항목은 아래 "장물죄" 절 참고)

### 쟁점 단위 강등 — 단일 결함이 사건 전체를 폐기하던 4곳 수정

이전에는 계약 위반 하나가 케이스 전체를 크래시시켰다. 전부 "그 쟁점만
`contract_degraded`/`symbolic_execution_failed`로 강등하고 나머지는 계속 실행"으로
바꿨다 (`src/idpr/rulegen/native_host.py`, `scripts/run_rule_ir_native_lean.py`):

1. 쟁점 선택 후 재검증(`selected_predicate_requests`)이 전량 기각된 케이스에서
   기본 `min_items=1`로 재검증해 크래시 — `min_items` 파라미터화.
2. predicate assessment 계약(인용문/누락사실) 위반 — try/except로 감싸
   `01_rejected_issues.json`에 `degraded_reason: predicate_assessment_invalid`로 기록.
3. Scallop scenario fact 검증 실패(`ScallopFactValidationError`, 예: `distinct_entities`가
   행위자 튜플 밖의 엔티티를 참조) — `symbolic_execution_failed` 상태로 강등.
4. `shared_module` 역할 유닛이 의존성 없이 선택된 경우 `raise NativeHostError` —
   `shared_module_missing_dependency` 상태로 강등.

각각 회귀 테스트 추가(`tests/test_rule_ir_native_host.py`,
`tests/test_rule_ir_native_lean_runner.py`). sbatch 219774(25/26) → 219779(26/26) 두 번의
전량 재실행으로 검증.

### track-coverage gate — 빈 track이 공유 요건만으로 성립 판정 나던 결함 선제 차단

`scripts/build_property_rule_ir.py`: track별 positive component가 하나도 없는 track이
공유 컴포넌트만으로 `established`를 도출할 수 있던 건전성 구멍. 이제 그런 track은
`core.outcome.track.{name}` / `elements_satisfied.{name}` 규칙 자체를 안 만들어
`track_pred`를 도달 불가능하게 하고, `coverage_gaps`에
`track_positive_path_missing: {name}`을 기록한다. 로버리 4개 track으로 회귀 테스트 작성
(`tests/test_property_rule_ir.py::test_track_without_positive_components_never_derives_established`).

### 검수 004 J-06 반영 — LEVEL과 role의 L6 결합 제거

기존에는 "역할 등록이 필요한가"를 `LEVEL == BAR_LEVEL("L6")`로 판단해서, LEVEL(요건
단계)과 role(카드 기능)이 부적절하게 묶여 있었다. `build_property_rule_ir.py`의
`negative_kind()`를 role 조회가 레벨과 무관하게 이뤄지도록 재작성 — 카드가
`card_roles.json`에 어떤 값으로든 있으면 그 역할을 쓰고, negative/exception 극성 카드가
등록 없이 들어오면 `SystemExit`. `build_rule_ir_card_roles.py`도 `LEVEL==L6` 필터 대신
"negative/exception 극성 전량"을 필수 등록 대상으로 바꿨다. `evidentiary_standard`,
`procedural_outcome` 역할 신설, `outcome_subtype` 정합성 검증(`POST_OUTCOME_SUBTYPES`
7종 대조) 추가.

정합성 검증: 로버리 재조립 후 `robbery_rule_ir_candidate.json` / `property_robbery_v1_candidate.scl`
해시가 이전과 바이트 단위로 동일 — 이번 리팩터가 기존 산출물을 바꾸지 않았음을 확인.

**사고 기록**: `build_rule_ir_card_roles.py` 실행이 그 스크립트의 불완전한 스키마로
`card_roles.json` 전체를 재생성하면서, 우발적으로 로버리 카드 하나의 `outcome_subtype`
필드를 지울 뻔했다 (테스트 `KeyError`로 검출, 원인 규명 후 `OUTCOME_SUBTYPES` 딕셔너리로
재생성 가능한 방식으로 복구, 해시 대조로 무결성 확인). 앞으로 데이터 재생성 스크립트를
돌리기 전에 그 스크립트의 소스 스키마가 현재 파일의 모든 필드를 커버하는지 먼저 확인할 것.

전체 스위트: **632 passed, 11 failed** — 실패 11건은 전부 기존 문서화된 결함(재산죄
golden `card_conflict_blocks` 10건 + `test_section_writer_cannot_supply_host_conclusion`).
이번 변경이 만든 회귀 없음.

## 장물죄 146장 적재 — 검수 004 접수 완료, 반영은 판단 문제 해결 후 재개

`docs/reviews/review_batch_004_stolen_property_level_design.md`에 사용자가 J-01~J-06
판정을 직접 기입 완료:

| 항목 | 판정 |
|---|---|
| J-01 (빈 track + coverage gap 감사) | O |
| J-02 (shared 레벨 분해) | X — 재분해 필요 (주체 component, 장물성/출처 분리, intent/timing AND 아닌 OR로 잘못 묶임 등) |
| J-03 (분리 원칙) | 수정 후 O — `acquisition.knowledge_at_delivery`, `custody.knowledge` 둘 다 3장으로 분리 |
| J-04 (`transport.consent_and_delivery`) | X — 3장 분리 필수 (부분 컴파일 방식 불승인) |
| J-05 (LEVEL 코드) | X — `L0a` 류 단순 코드 대신 `SP_` 네임스페이스 시맨틱 코드 |
| J-06 (LEVEL/role 결합) | 구조 수정 필요 — **이 세션에서 반영 완료** (위 절 참고) |

지시된 작업 순서: 1. LEVEL-role L6 결합 제거 → 2. component-scoped bar/variant 상태 기능
확인 → 3. 카드 분리 → 4. coverage gap 등록 → 5. namespaced LEVEL 확정 → 6. 원장 적재 →
7. SCL 생성 → 8. track별 golden test.

**진행 상황**: 1, 2 완료(위 절). 3~8은 미착수 — 지금 판단할 문제(judge/라우팅)를 먼저
정리한 뒤 재개.

카드 분리 대상 최종 13장 (기존 배치 002의 11장 + 배치 004가 추가한 2장):
```
sec3_2.foreign_offense, sec3_3.transport.knowledge_midway, sec3_3.custody.knowledge,
good_faith_acquisition, accession_processing, breach_of_trust_bribe,
resale_fraud_nonabsorption, acquisition.food_consumption,
transfer.knowledge_and_subsequent_transfer, brokering.completion_doctrines,
acquisition_brokering_relationship,
acquisition.knowledge_at_delivery (신규, J-03),
transport.consent_and_delivery (신규, J-04)
```

신규 coverage gap 3종 (배치 004가 추가 지적, 기존 카드로 못 채움):
```
missing_card_slot: 일반 주체 eligibility component (instigator_aider_subject 단독으로는 부족/부적절)
missing_card_slot: 운반 track 고의시점 component (acquisition/custody와 분리 필요)
missing_card_slot: "장물임을 실제로 인식했다"는 사실 component (intent_and_knowledge의 추상적 고의범 서술과 별개)
```

146장 역할 재분류 대조 결과(검수 002 E절 대조, 이번 세션에 수행): 이름으로 명시 판정된
건 124장, E-04 일괄방침("학설군 일괄 미채택")으로 커버되는 건 19장(개별 재검토 불요),
어디에도 안 걸리는 진짜 미검토 카드는 2장 — `sec3_2.copied_media`,
`sec3_2.victim_consent_gift_inheritance` (둘 다 polarity=exception, exception-polarity
게이트로 자동 격리되므로 잠정 배정해도 결론엔 영향 없음, 다만 최종 역할은 사용자 확인
필요).

데이터 이슈 발견(미해결): 카드 ID `stolen_property_sec3_2.stolen_property_used_to_defraud`에
`stolen_property_` 접두사가 중복 포함돼 있다(146장 중 유일 사례, 추출 파이프라인
아티팩트로 추정). 원장 적재 시 이 ID를 그대로 쓸지 정정할지 결정 필요 — 임의로
바꾸지 않고 다음 세션에서 확인.

## 이전부터 열려 있는 결함 (미착수)

- **F-01 shared module `post_offense_absorption`** — 장물보관 후 임의처분 불가벌적
  사후행위. 배치 002 F-01에 bridge relation 8종·출력 4종 확정. 호스트가 쟁점별 유닛을
  독립 실행하고 유닛 간 사실을 안 주고받는 구조라 bridge 경로 신설 필요.
- **사기 룰베이스 재작업(검수 003 G절, 판정 완료·미반영)** — `BAR_CARD_IDS` 23장 중
  미수/기수 혼동 3장, boundary 재분류 3장, `assessment_standard` 재작성 등.
- **`polarity=exception` 88장 극성 복구(검수 003 I)** — 현재 `enforce: false` + quarantine.
  처리 순서: 실발화 카드 → bar → boundary → P2 waiver → 도달가능 미발화 → 비활성.
- **Stage 1/2 역할 결박 대조 없음(P0)** — `role_candidates`/`role_values`가 서로 비교되지
  않아 Stage 2가 Stage 1의 행위자·객체 선택을 조용히 바꿀 수 있음.
- **재산죄 golden 10건 실패** — `card_conflict_blocks`, 커밋 `2c4e75e`가 무장 해제.
- **`test_section_writer_cannot_supply_host_conclusion`** — 죽은 경로를 지키는 가드,
  경로를 지울지 가드를 옮길지 결정 필요.
- **25개 P2 RuleIR이 `status=draft`** — 레지스트리 활성화가 승인 원장/해시에 안 묶임.
- **back-parse 검증 없음** — 답안과 derivation 모순 대조 단계 없음.
- **`post_outcome` 191장 `outcome_subtype` 미지정** — coverage gap으로만 노출 중.

## 실행 환경

- 추론 환경: `inv_ass_env`. **sbatch 설정은 건드리지 말고 전례대로만.**
- 원격 API(judge 등) 작업도 **항상 sbatch** — raw 백그라운드 프로세스 금지. 스크래치
  파일은 compute node가 못 보는 세션 `/tmp/...`가 아니라 `/data5/jaehoonjeong/IDPR/.cache/...`
  같은 공유 스토리지에 둘 것 (job 219789가 이 실수로 실패, 219790으로 정정).
- 셸에 conda가 활성화돼 있지 않으면 `IDPR_PYTHON` / `IDPR_VLLM_BIN` / `IDPR_MODEL_SOURCE`를
  명시해 제출해야 한다.
- GPU를 만지는 작업은 길이와 무관하게 항상 sbatch. `nohup` 금지.
- 고정 심볼릭 런타임: `tools/scallop/scli-0.2.4-linux-x86_64`
- 레지스트리 매니페스트: `data/rulegen/rule_ir_registry_manifest.json` (36 유닛)
- 테스트: `python -m pytest` — miniconda **base** 환경 (레포 `.venv`는 빈 껍데기,
  `inv_ass_env`도 아님).

## 검수 문서

| 배치 | 내용 | 상태 |
|---|---|---|
| [001](../reviews/review_batch_001_roles_and_stolen_property.md) | 역할 배치 36건 + 장물죄 4건 | 답변 완료·반영 완료 |
| [002](../reviews/review_batch_002_assessment_standard_and_stolen_property.md) | `assessment_standard` 설계 + 장물죄 146장 | 답변 완료·C/D절 반영, E/F절 미반영 |
| [003](../reviews/review_batch_003_fraud_bars_and_sweep_findings.md) | 사기 BAR 23장 + 26문항 실행 발견 | 답변 완료·H-03/I 반영, G/H-01 미반영 |
| [004](../reviews/review_batch_004_stolen_property_level_design.md) | 장물죄 track/LEVEL/role 설계 6건 | 답변 완료·1~2단계 반영, 3~8단계 미반영(위 절 참고) |

검수는 카드 단위로 판정하며, **검수 문서는 그 자리에서 답할 수 있어야** 한다 —
재료만 나열하면 안 된다.

이어서 읽을 것: [`DESIGN.md`](DESIGN.md), [`RECOVERY.md`](RECOVERY.md),
[`../../project_init.md`](../../project_init.md). RuleIR 시그니처나 법률적 구성을
바꿀 때는 [`RULEIR_RISKS.md`](RULEIR_RISKS.md).
