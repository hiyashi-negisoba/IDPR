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

1. **결함 위치를 로그로 구분** — ✅ **완료 (이번 세션)**, 상세는 아래
   "1단계 결과: r10/r14 결함 위치 특정" 절 참고. 4가지 범주 모두 실제 사례로 확인됐고,
   지시에 없던 **5번째 범주(술어평가 오류)**가 가장 파급력 큰 결함으로 드러났다.
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

### 1단계 결과: r10/r14 결함 위치 특정 (이번 세션, job 219779 산출물 대조)

`experiments/results/rule_ir_native_lean_batch_219779/{kcl_criminal_r10_p1_q1_ga,
kcl_criminal_r14_p1_q2}/`의 `01_issue_selection.json` / `01_rejected_issues.json` /
`02_assessment_*.json` / `03_native_report.json` / `04_write_prompt.md` / `05_answer.md`를
골드 rubric(`data/inventory/kcl_criminal_v1_draft.jsonl`)과 대조. 두 사례 모두 4가지
범주가 각각 실제로 발생했고, 지시에 없던 5번째 범주가 새로 드러났다.

**r10_p1_q1_ga (성범죄 사례, 甲의 죄책):**

| 쟁점 | 범주 | 내용 |
|---|---|---|
| issue_1 (강제추행 간접정범) | **라우팅 오류** | `indecent_assault`가 활성 레지스트리에 있는데도 router가 `extortion`(공갈)을 골라 role 계약 위반으로 `contract_degraded`. 골드 rubric 36개 중 결론 항목(#11, #36)에 들어가는 죄명이 답안에서 통째로 사라지고, 대신 rubric에 없는 "성폭력처벌법상 촬영물등이용협박"을 답안이 즉석 창작. |
| issue_3 (강도로 오분류) | **라우팅 오류(중복)** | 강간을 위한 폭행·감금 사실을 `robbery` 유닛에 태워 art333~343 술어 ~100개를 돌렸으나 전부 근거 없이 `not_satisfied`라 계약 위반으로 폐기 — 18k 토큰 낭비, 원래 필요한 인과관계 분석에 갈 자원을 소모. |
| issue_6 (중지미수) | **규칙베이스 범위 오류** | 형법 제25·26조 장애미수/중지미수/불능미수라는 총론 법리가 어떤 유닛에도 술어로 존재하지 않음. router가 "unsupported"라고 한 것 자체는 맞다 — 정말 없다. |
| issue_2 (주거침입) | **술어평가 오류 (신규 범주)** | 술어 ~90개가 거의 전부 "unknown". "아파트 공용현관·엘리베이터에 따라 들어간 것 자체가 판례상 기수"라는, 사실관계에 그대로 적힌 카드(`apartment_common_areas`)조차 "확인되지 않음" 처리 → `dwelling_intrusion_undetermined`. |
| issue_4→issue_5 (강간치상) | **상징/구조 오류** | `sexual_offense_attempt`가 `shared_module_missing_dependency`로 강등(의존하는 shared module이 별도 이슈로 라우팅되지 않아 미공급) → issue_5가 `prerequisite_not_established`로 연쇄 붕괴. 사건에서 두 번째로 중요한 결론(강간치상)이 통째로 상징 근거 없이 생성됨. |
| 종합 | **생성 단계** | 상징 결과가 사실상 전무하니 writer가 헤지형 자유 서술로 전체를 메움("성립 가능성이 높으나…"). rubric 필수 죄명 3개 중 2개(강제추행 간접정범, 체포죄)가 최종 답안에서 빠짐. |

**r14_p1_q2 (사기·뇌물·횡령 사례, 乙·丙의 죄책):**

| 쟁점 | 범주 | 내용 |
|---|---|---|
| issue_2, issue_3 (증뢰물전달죄) | **라우팅 오류** | `third_party_bribery`가 router에게 주어진 것과 동일한 closed enum 안에 활성 상태로 존재하는데도 router가 두 쟁점 다 `unit_id: "unsupported"`로 출력. 乙·丙 각각의 핵심 결론(제3자뇌물교부죄/취득죄, rubric #6~14)이 통째로 즉석 창작으로 대체("일반 뇌물공여죄 공동정범"— 오답). |
| issue_1 (사기) | **술어평가 오류** | `fraud_intent_no_disposition_inducement_intent` 등 고의 관련 술어가 전부 "unknown". 대차 용도를 구체적으로 속인 사실 자체가 고의를 강하게 추단시키는 전형적 사안인데도, 평가 모델이 "명시적 진술이 없으면 unknown" 식으로 처리 → `symbolic_conclusion: not_established` (골드 결론과 정반대). |
| issue_1 답안 반영 | **생성 단계 (가장 심각)** | `04_write_prompt.md`가 "확정 결론: 불성립 … 이 결론은 검증된 규칙 추론의 산물이므로 반드시 그대로 따른다"고 강제. 결과 `05_answer.md`는 자체 논증으로 "사기죄의 구성요건을 충족한다고 봄이 타당하다"고 쓴 바로 다음 문장에서 "확정 판정에 따라 사기죄 불성립"으로 뒤집는 **자기모순 답안**을 그대로 출력. |
| issue_4 (횡령) | **규칙베이스 범위 오류 (조용한 오답)** | `embezzlement` 유닛에 불법원인급여물 항변(대법원 판례, 뇌물 자금처럼 불법 목적 급여물은 위탁물 보호대상이 아니라 횡령죄 객체가 아니라는 법리) 카드가 없음 → `symbolic_conclusion: established`(골드는 불성립). 답안도 아무 모순 없이 확신을 갖고 "횡령죄 성립"이라 서술 — r14 사기 사례처럼 표면에 흠이 드러나지 않아 rubric 대조 없이는 못 잡아낸다. |

**교차 사례 종합 — 5번째 범주가 최우선 레버리지 지점**

지시받은 4범주(라우팅/규칙베이스/상징규칙/생성)가 전부 실제로, 그것도 사례 하나당
여러 번 겹쳐서 확인됐다. 그런데 그 위에 **범주 5: 술어평가(predicate assessment)
오류**가 새로 드러났다 — 고의·인과관계·예견가능성처럼 사실관계에서 **추론**해야
하는 요건을 평가 모델이 "명시적 문장으로 서술돼 있지 않으면 unknown" 식으로
과도하게 문자적으로 처리한다. 변호사시험 사실관계는 애초에 내심의 의사를 직접
서술하지 않고 행위로만 암시하는 서술 관행이므로, 이 결함은 이 두 사례에 국한되지
않고 **레지스트리 전역에서 "established" 판정을 광범위하게 억누르고 있을 가능성이
높다** — 라우팅과 규칙베이스를 아무리 고쳐도 평가 단계가 이 모양이면 상징 결론은
계속 `undetermined`/`not_established`로 새고, 결과적으로 4번(생성 단계)의
"반드시 그대로 따른다" 강제 지시가 잘못된 결론을 확신에 찬 답안으로 그대로
찍어낸다. 즉 **평가 단계(범주 5) → 생성 단계 강제 지시(범주 4)**의 조합이 지금
가장 위험한 경로로 보인다: 잘못된 결론이 (a) 자기모순으로 드러나거나(사기 사례,
그나마 육안 검출 가능) (b) 아무 흔적 없이 확신에 찬 오답으로 나간다(횡령 사례,
rubric 없이는 검출 불가).

**다음 결정 필요**: 2~4단계(라우팅/symbolic 출력 확장, judge 재설계)로 바로
넘어가기 전에, 이 술어평가 문제와 "반드시 그대로 따른다" 강제 지시부터 먼저
겨냥할지 사용자 판단 필요 — 활성 프롬프트 변경은 승인 게이트 대상.

**사용자 결정 (같은 세션): 술어평가 오류(범주 5) + 생성 강제 지시(범주 4)부터
먼저 고친다.** 이유: 라우팅 오류는 coverage를 깎지만, 술어평가 오류는 카드를
정확히 골랐어도 결론 자체를 뒤집는다. 사용자가 제시한 순서: 1) predicate
assessment 4-state화 2) symbolic outcome에 신뢰 상태(verified/provisional/
unsupported/invalid) 부여 3) 생성 강제 지시와 충돌 처리 4) 라우팅/하위쟁점 확장
5) rule-base 범위 보완 6) judge 재설계 7) 전체 재실험. 1~3단계를 이번 세션에
구현 완료 — 아래 절 참고. 4~7단계는 미착수.

### 1~3단계 구현 완료 (이번 세션) — 술어평가 4-state + 신뢰 상태 + 충돌 검출

**변경 범위**: `src/idpr/rulegen/native_host.py`, `scripts/run_rule_ir_native_lean.py`,
`prompts/rule_ir_native_predicate_assess.md`, `prompts/rule_ir_native_write.md`,
`scripts/audit_rule_ir_native_prompts.py`, 관련 테스트. **아직 실제 API로 실행한
적 없음 — 스키마/유닛 테스트만 통과 확인.** 1차 구현 후 사용자가 3가지 구멍을
지적해 같은 세션에서 수정 완료(아래 "1차 검수 반영" 참고). 전체 스위트:
**637 passed**(신규 테스트 5건), 실패 11건은 전부 이전부터 문서화된 기존 결함
(재산죄 golden `card_conflict_blocks` 10건 + `test_section_writer_cannot_supply_host_conclusion`)
그대로 — 이번 변경이 만든 회귀 없음. `python scripts/audit_rule_ir_native_prompts.py`
도 pass.

1. **predicate assessment 4-state화** (`native_host.py`
   `ASSESSMENT_STATUSES`/`normalize_assessment_status`) — 스키마 enum을
   `satisfied/not_satisfied/unknown`에서
   `explicitly_supported/inferentially_supported/contradicted/genuinely_unresolved`로
   교체(구조화 출력 자체를 이 네 값으로 강제, validator도 이 네 값 기준으로
   재작성). Scallop 실행 직전 `normalize_assessment_status()`로 `explicitly_supported`·
   `inferentially_supported`→`satisfied`, `contradicted`→`not_satisfied`,
   `genuinely_unresolved`→`unknown`으로 정규화 — symbolic 실행 로직 자체는
   무변경. `inferentially_supported`에는 `inference_rationale`(추론 근거 1~2문장)을
   JSON Schema `if/then`으로 조건부 필수화 — 명시적 사실 없이 결론을 낸 이유를
   사후 검수할 수 있게. `prompts/rule_ir_native_predicate_assess.md`에 "내심적·
   규범적 요건의 추론" 절을 신설해 사기 고의 예시를 넣고, "문장으로 서술돼 있지
   않다"는 사실 자체는 `genuinely_unresolved`의 근거가 아니라고 명시.
2. **symbolic outcome 신뢰 상태** (`native_host.py` `classify_symbolic_trust`) —
   `execute_native_case`가 만드는 `conclusion_directives`/`skipped_directives`
   각 항목에 `trust_status` 필드 부여:
   - `verified`: 실행 완료 + established/not_established **그리고** 그 결론이
     실제로 발화(fire)한 Scallop 증명 경로(`proof_dag.proof_tree`를
     `_collect_critical_predicates()`로 추적)에 포함된 술어 중
     `genuinely_unresolved`가 하나도 없음. `inferentially_supported`가
     섞여 있다는 사실 자체는 verified를 막지 않는다 — 정규화하면 explicit과
     동등하기 때문. 이 조건이 1차 구현에서 빠져 있었다: unit 하나에 보통
     수십~백여 개 술어가 있고 그중 사실관계와 무관해 정당하게
     `genuinely_unresolved`로 남는 것이 항상 있는데, "unit 전체에 unresolved가
     하나라도 있으면 provisional"로 잡으면 verified가 사실상 한 번도 안 뜨고,
     반대로 아무 검사도 안 하면 특정 카드가 "반증되지 않으면 인정"식으로
     설계돼 있을 때 unresolved 술어가 조용히 통과해 established로 확정되는
     반대 방향 오류가 생긴다 — 증명 경로 추적으로 이 둘을 다 피한다.
   - `provisional`: 실행 완료했지만 undetermined/conflict/no_derived_outcome,
     또는 established/not_established가 떴어도 위 조건을 못 만족(발화 경로에
     unresolved 술어 포함, 또는 증명 경로 자체를 못 찾음 — 후자는 방어적으로
     "확인 불가 = provisional" 처리)
   - `unsupported`: 해당 unit의 RuleIR 자체가 없음(`predicate_ir_missing`)
   - `invalid`: contract_degraded/shared_module_missing_dependency/
     prerequisite_not_established/symbolic_execution_failed — 시스템 내부 실패,
     법리적 신호 없음
3. **생성 강제 지시 분기 + 자기모순 검출** (`run_rule_ir_native_lean.py`
   `_render_verdict_brief`/`_render_directive_block`, `prompts/rule_ir_native_write.md`) —
   기존에는 실행된 결론이면 established든 undetermined든 전부 "확정 결론 …
   반드시 그대로 따른다"로 동일하게 강제했다(이게 r14 사기/횡령 사례의 핵심
   원인). 이제 4단으로 분기: `verified`만 "확정 결론"으로 절대 준수, `provisional`은
   "잠정 결론"으로 제시하되 근거가 있으면 대안 논증 허용, `unsupported`/`invalid`는
   각각 "규칙베이스 범위 밖"/"규칙 추론이 완료되지 못한 쟁점"으로 분리해 아무 힌트
   없이 자율 논증(둘 다 자율 논증이지만 이후 결함 분석에서 "커버리지 부족"과
   "파이프라인 버그"를 구분할 수 있게 라벨은 남긴다).
   자기모순 검출: writer가 답안 맨 끝에 `<!--VERDICT_MANIFEST\nissue_id: established
   또는 not_established\n-->` 트레일러를 출력하도록 지시(`native_host.py`
   `parse_verdict_manifest`/`strip_verdict_manifest`). `check_verdict_consistency()`가
   이 트레일러를 `verified` 쟁점의 `symbolic_conclusion`과 대조 — 불일치하면
   `06_verdict_consistency.json`에 **기록만 하고 재생성/중단은 하지 않는다**
   (사용자 확인: 이번 최소 실험은 원 답안 보존·트레일러 대조·불일치 기록·재시도
   없음으로 고정 — repair를 넣으려면 API 호출 횟수·추론 예산·답안 선택 절차·
   baseline 비교 조건이 다 바뀌므로 별도 후처리 단계나 ablation으로 분리할 것).
   트레일러는 `05_answer_raw.md`에만 남고 `05_answer.md`(채점/사람이 읽는 파일)
   에서는 제거된다. `generation_contract.model_may_override_symbolic_conclusion:
   False` 필드는 원래부터 있었지만 아무도 검사하지 않던 죽은 계약이었다 —
   이 체크가 그걸 실제로 강제하는 첫 코드.

### 1차 구현 검수 반영 (같은 세션) — 사용자가 지적한 3가지 구멍

1. **스키마/validator가 실제로 4-state를 강제하는지** — 프롬프트만 바꾸고
   스키마를 안 바꾸면 출력이 자체 validation에서 탈락한다는 지적. 확인 결과
   스키마(`predicate_assessment_schema`의 `ASSESSMENT_STATUSES` enum)는 처음부터
   같이 바꿔뒀었고, 이번에 `inferentially_supported`→`inference_rationale`
   조건부 필수(`if/then`)를 추가로 넣었다.
2. **raw/normalized 상태를 둘 다 보존** — `assessment_evidence`의 필드를
   `raw_status`(원래 4-state 그대로)와 `normalized_status`(Scallop용 3-state)
   두 개로 분리(이전엔 `status`+`assessment_basis`로 이름이 불명확했다).
   재실행 결과가 개선됐을 때 "새 사실 때문"과 "추론 허용 때문"을 구분할 수 있게
   됐다. `_render_verdict_brief`의 인정/부정/미확인 요건 목록도
   `normalized_status` 기준으로 수정.
3. **verified 기준 강화** — 위 2번 "symbolic outcome 신뢰 상태" 절 참고. Scallop
   proof tree를 실제로 역추적해 검증하는 `_collect_critical_predicates`/
   `_is_cleanly_derived`를 추가(경험적으로 rape 골든 시나리오의 proof_tree
   구조를 직접 실행해 확인한 뒤 작성 — established 관계에서 `assess_*` 술어
   리프까지의 경로가 실제로 추적 가능함을 확인).

**미해결/다음 세션 판단 필요**:
- `inferentially_supported` 허용이 precision을 깎을 위험(과다추론) — r10/r14뿐
  아니라 "고의가 명확히 추론되는 사례"와 "고의가 실제로 불명확해 unresolved가
  맞는 사례" 음성 대조까지 최소 4~6건으로 소규모 재실행해 확인. 답안 점수보다
  먼저 볼 것: predicate별 old_status→new_raw_status, new_raw_status→
  normalized_status, symbolic_conclusion 변화, trust_status, 생성 결론,
  VERDICT_MANIFEST 일치 여부.
- 자기모순 발견 시 정책(현재는 기록만) — 이번 최소 실험 범위에서는 이대로 유지,
  repair를 넣을지는 별도 결정.
- 4단계(라우팅/하위쟁점 확장) 이후는 미착수.

### 다음 세션 시작점 — job 219900 결과부터 확인

이번 세션 마지막에 소규모 검증 재실행을 **제출까지만 하고 세션을 마감**한다.
다음 세션은 여기서 시작:

1. **`sacct -j 219900`로 완료 여부 확인.** 성공 시 결과는
   `experiments/results/rule_ir_native_lean_predassess_smoke/{case_id}/` 6개
   (`kcl_criminal_r10_p1_q1_ga`, `r14_p1_q2`, `r10_p2_q1`, `r12_p2_q1_da`,
   `r10_p1_q2`, `r14_p2_q2` — 앞 둘은 job 219779와 동일 사례로 직접 대조 가능,
   나머지 4개는 사기/횡령 계열 고의 대조 2건 + 인과관계 대조 2건). 로그:
   `logs/ruleir_native_batch_219900.{out,err}`.
2. **백본은 원래대로 로컬 vLLM `google/gemma-4-26B-A4B-it`** — job 219779와
   동일 조건이라 직접 비교 가능. (세션 중간에 IDPR 생성 백본 자체를 Sonnet으로
   바꿔 제출했다가 사용자 지적으로 40초 만에 취소한 해프닝 있음 — IDPR 생성
   백본에 API 모델을 쓰는 일은 앞으로도 없어야 한다.)
3. 확인할 것(사용자 지시, 답안 점수보다 먼저): `02_assessment_*.json`의
   `raw_status`/`normalized_status`, `03_native_report.json`의
   `trust_status`, `05_answer_raw.md`의 `VERDICT_MANIFEST`와
   `06_verdict_consistency.json`(있다면) 대조. 특히 r14_p1_q2의 사기 쟁점이
   이번엔 `established`+`verified`로 뜨는지, r10_p1_q1_ga의 주거침입/강간치상이
   `verified`로 뜨는지.
4. 문제없으면 **26문항 전체**를 같은 파이프라인(gemma 백본)으로 재실행해
   원본 job 219779 출력과 비교(사용자 지시). 이것도 아직 새 judge 없이 raw
   출력·trust_status 비교 목적으로 하는 것 — 재채점은 6단계(judge 재설계) 이후.
5. 그다음 4~6단계(라우팅/하위쟁점 확장, 룰베이스 범위 보완, judge 재설계)로.

**이번 세션에 새로 만들었지만 아직 안 쓰는 것**: SKI-ML 게이트웨이 경유 Sonnet
클라이언트(`src/idpr/neural/skiml_litellm_client.py`,
`scripts/run_rule_ir_native_lean_sonnet.py`,
`scripts/slurm/run_rule_ir_native_lean_sonnet_smoke.sh`). 연결은
`anthropic/claude-sonnet-4-6` 모델 문자열로 확인 완료(`custom_llm_provider="openai"`
로 호출해야 인증됨 — litellm이 "anthropic/" 접두어만 보고 자체 판단하면
Anthropic 네이티브 인증 경로로 새서 401). **judge 백본 교체(6단계) 전까지는
쓰지 않는다** — IDPR 생성 파이프라인에는 절대 쓰지 않는다.

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
