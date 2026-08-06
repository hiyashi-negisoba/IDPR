# Current handoff

기준: 2026-08-06 · 브랜치 `antigravity-0804`

## 지금 최우선 — 평가(judge)와 라우팅 구조 문제

**사용자 결정: 장물죄 원장 적재 작업은 잠시 보류. 이 문제부터 해결하고 원래 궤도로
복귀한다.** 26문항 Gemini 채점(아래)을 사용자가 직접 검토한 뒤 "말이 안 된다"고 판단,
FOL 답안 하나를 반례로 지목했다. 다음 세션은 여기서 시작할 것.

**다음 세션 시작점 (2026-08-06 갱신, 2번째)**: 4단계(라우팅 출력 확장)와 라우팅
정확도 진단 필드(진단 완료)까지 끝난 뒤, "base unit이 실제로 부합하는데도 참여형태
불확실성 등을 이유로 `unsupported`를 고르는 패턴"을 프롬프트로 막는 시도를 **2회
했으나 둘 다 무효로 확인돼 롤백했다** — 상세는 아래 "decision 단계 프롬프트 수정
시도 — 2회 실패, 롤백" 절 참고. **이 문제는 미해결 상태로 남겨두고 다음은 5단계
(rule-base 범위 보완)로 이동한다(사용자 지시).**

**5단계 후보 — 출처 등급을 나눠서 볼 것 (아래 "sealed-59 오염 정책" 절 참고)**:
- **A등급(정당, 바로 착수 가능): 살인교사·공모관계.** `declared_not_compiled`로
  2026-08-04자 `docs/review/2026-08-04_homicide_legal_gate_01.md` 등에 이번 세션 전에
  이미 문서화된 공백 — sealed case를 읽어서 발견한 게 아니다.
- **B등급(공백 자체는 정당, 우선순위 근거만 오염): 강도상해·강도치상 결합범.**
  `data/rulegen/property/rule_ir_units/robbery.json`에 art337/338 norm card가 이미
  추출돼 있고, `data/rulegen/rule_ir_registry_manifest.json`의 `robbery` unit
  `query_relations`엔 `robbery_established/not_established/...`만 있고 상해·사망
  결과 트랙이 없다 — 이 자체는 사례 내용과 무관하게 레지스트리 vs 코퍼스 대조만으로
  확인되는 진짜 구조적 공백. 다만 **이번 세션에 이걸 1순위로 콕 집은 계기는
  sealed-59 소속 `kcl_criminal_r11_p1_q1`의 답안을 읽다가 실패를 본 것** — 착수할 때
  카드는 r11의 구체적 사실관계가 아니라 art337/338 코퍼스와 판례만 참고해서 짤 것.

**주의(5단계 착수 전에 반드시 읽을 것)**: 5단계는 라우팅 정확도 문제(라우터가
이미 있는 unit을 회피하는 결함)의 해법이 **아니다** — 서로 다른 결함 범주다.
5단계는 레지스트리에 아예 없는 unit을 새로 만드는 작업이고, 롤백한 시도는 레지스트리에
"이미 있는" unit을 라우터가 스스로 정확히 짚어놓고도 거부하는 결정 단계 문제였다.
5단계로 새 unit을 추가해도 이 회피 휴리스틱이 그 새 unit에 대해서도 똑같이 나타날
위험이 있다 — 두 문제를 하나로 섞어 "5단계가 끝나면 라우팅 정확도도 좋아졌겠지"라고
가정하지 말 것.

### sealed-59 오염 정책 (2026-08-06, 사용자 결정)

라우팅 정확도 회귀 배치(job 220070/220071/220074)가 쓴 6사례 중 4개
(`kcl_criminal_r11_p1_q1`, `r12_p1_q1`, `r13_p1_q1`, `r14_p1_q1`)는 승인된 dev
case 2개(`r10_p1_q1_ga`, `r14_p1_q2`, `scripts/build_phase3_final_eval_inventory.py`의
`DEVELOPMENT_CASES`)에 안 들고 **sealed-59 최종 평가셋 소속**이다. 디버깅 목적으로
이 4개의 답안·이슈선택 결과를 반복해서 읽은 것 자체가 이미 노출이고, 그 중 하나
(강도상해 결합범 공백)는 실제로 5단계 우선순위 판단에 영향을 줬다(위 "B등급" 참고).

**사용자 결정: 지금부터는 (a) — 라우팅/decision 단계 디버깅용 스모크는 승인된 dev
case 2개로만 제한한다.** sealed-59 소속 사례를 채점(최종 평가) 목적이 아니라
규칙·프롬프트 튜닝 디버깅 목적으로 다시 열어보지 않는다. 이미 노출된 두 사례
(r11_p1_q1 강도상해, r14_p1_q1 살인교사)는 소급해서 되돌릴 수 없으므로, 그 공백을
고치는 작업 자체는 위 A/B 등급 구분대로 진행하되(코퍼스 기반으로만 작성), 앞으로
새로운 디버깅 배치를 짤 때 sealed-59 case_id를 케이스 리스트에 넣지 않도록 주의.
필요하면 dev case를 승인 절차를 거쳐 추가하는 것을 고려(현재는 2개뿐).

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

### 이번 세션 완료 — predassess 스모크 검증 통과 (job 219900 재제출부터 시작해 완결)

**job 219900은 실패했다 (코드 문제 아님).** vLLM 엔진 초기화 중 `IDPR_HF_HOME`을
안 넘긴 채 제출해 `HF_HOME`이 홈 디렉터리 기본 경로(비어있음/불완전)로 새고,
거기서 실시간 재다운로드를 시도하다 `RuntimeError: Internal error: Internal
Writer Error: Background writer channel closed`로 끊겨 죽었다. 진짜 캐시는
`/data5/jaehoonjeong/.cache/huggingface`(49G, 완전함, `~/.bashrc`의 `HF_HOME`이
가리키는 곳)에 있었다 — `scripts/slurm/_env.sh`는 `IDPR_HF_HOME`이 명시적으로
안 오면 기본 폴백 없이 그냥 넘어가므로, 이후 이 모델을 쓰는 모든 sbatch 제출은
`IDPR_HF_HOME=/data5/jaehoonjeong/.cache/huggingface`를 반드시 명시해야 한다.

재제출(219978) 이후 실제 API 실행으로만 드러나는 버그를 2개 발견·수정했다
(둘 다 지난 세션의 1~3단계 구현이 "스키마/유닛 테스트만 통과, 실제 API로는
미실행"이라고 남겨뒀던 그 구멍):

1. **스키마 `if`/`then`은 vLLM guidance backend가 미지원** (job 219978, 6/6
   전부 `Grammar error: Unimplemented keys: ["if","then"]`로 즉시 실패) —
   `inference_rationale` 조건부 필수화를 JSON Schema `if`/`then`으로 구현한
   게 생성 요청 자체를 막았다. `native_host.py`의 `predicate_assessment_schema()`
   에서 `if`/`then` 제거, `inference_rationale`을 무조건 `required`로(단
   `minLength` 없이, 빈 문자열 허용) 바꿔 grammar가 키 존재는 강제하되 내용은
   강제하지 않게 하고, "`inferentially_supported`면 비어있으면 안 된다"는
   조건은 `validate_predicate_assessment()`의 Python 쪽 상태별 체크로 옮겼다.
2. **`genuinely_unresolved`의 `missing_facts` 누락이 쟁점 전체를 폐기** (job
   219989 재제출 직후, r14_p1_q2 사기 88개 술어 중 44개가 `missing_facts`를
   비운 채 `genuinely_unresolved`로만 남아 쟁점 전체가 `predicate_assessment_invalid`
   로 강등). 비운 술어 대부분이 이 사건과 무관한 경계/예외 법리(광고 기망,
   공익목적 예외, 삼각사기 판례 등) — 판정 자체는 맞고 `missing_facts` 생성
   계약만 깨진 사례(사용자 분류상 B 유형)로 확인. `prompts/rule_ir_native_predicate_assess.md`
   에 "이 predicate가 사건과 무관해 보이더라도 `missing_facts`를 비우지 말고
   어떤 사실이 추가로 확인돼야 하는지 적으라"는 한 줄만 추가. 단독 재실행
   (job 219993, `r14_p1_q2` 1건)으로 검증: 44개 전부 `missing_facts` 채워짐,
   `issue_1`(사기)이 더 이상 강등되지 않고 `not_established`+`verified`로
   정상 실행. 구조적 완화(`assessment_validity` 필드 분리)는 이 한 줄로
   불필요해졌다 — 도입 안 함.

6-case 배치(job 219992, gemma 백본)는 최종 **6/6 성공**. 종료조건 확인:
**추론 가능한 술어는 `inferentially_supported`로 판정되고, 실제 불확정
술어는 쟁점을 폐기하지 않은 채 provisional/verified 경로로 정상 전달된다.**
(**목표를 `established`+`verified`로 두지 않았다** — 사용자 지시: 그렇게
튜닝하면 과다추론으로 precision을 깎는다. `r14_p1_q2` 사기의 최종 결론은
여전히 `not_established`이고, 그 결론 자체가 골드와 맞는지는 이번 스모크
범위 밖.)

**사고 기록 — RUN_DIR 재사용 함정**: 같은 `IDPR_RUN_DIR`로 여러 job을 연달아
제출하면 실패한 이전 job이 남긴 `01_rejected_issues.json` 등이 안 지워진 채
남아 최신 성공 결과와 섞여 보인다. 이번 세션에서 `r10_p2_q1`의 사기 쟁점이
실제로는(fresh `03_native_report.json` 기준) 정상 실행됐는데, 이전 job의
잔존 `01_rejected_issues.json`(mtime이 새 job 시작 시각보다 이전) 때문에
한 번 강등된 것으로 오판할 뻔했다. 다음에 이 디렉터리를 다시 볼 때 파일
mtime을 job 시작 시각과 대조할 것.

**사용자 결정: 26문항 전체 재실행은 생략(필수 아님).** 원래 계획된 4번
(전체 재실행·219779 비교)은 건너뛰고 바로 아래 4~6단계로 진행한다.

**다음 세션 시작점: 4단계 — 라우팅 출력 확장.** 이 문서 맨 위 "다음 세션 작업
순서" 목록의 2번(`required_subissues`/`conclusion_sensitive_facts`/
`unresolved_branch_points`/`alternative_legal_routes`/`required_conclusions`
반환) 참고. 1~3단계(술어평가 4-state, trust_status, 강제지시 분기)는 API
실행까지 검증 완료됐으니 여기서부터.

### 4단계 구현 완료 (이번 세션) — 라우팅 출력 확장, API 스모크는 GPU 대기 중

`closed_issue_selection_schema()`(`src/idpr/rulegen/native_host.py`)에 `issues`
외 다섯 개 배열을 전부 **무조건 필수**로 추가했다: `required_subissues`,
`conclusion_sensitive_facts`, `unresolved_branch_points`,
`alternative_legal_routes`, `required_issue_labels`(원래 이름
`required_conclusions`였으나 검수에서 지적받아 개명 — 아래 참고). 값은 매번
빈 배열이라도 키 자체는 항상 나와야 한다 — `inference_rationale`에 썼던 것과
같은 "무조건 필수 키 + 내용은 Python 쪽에서 조건부 검사" 패턴이다.

**1차 구현 후 사용자 검수에서 세 가지 지적을 받아 설치 전에 수정**:

1. **관계는 `unit_id`가 아니라 `issue_id`로만 참조한다.** 1차안은
   `subissue_unit_id`/`branch_unit_ids`/`alternative_unit_id`처럼 unit_id로
   연결했는데, 같은 unit_id가 서로 다른 행위자·행위에 여러 번 등장할 수 있고
   `unit_id=unsupported`인 issue도 한 사건에 여러 개 있을 수 있어 unit_id로는
   어느 issue를 가리키는지 특정할 수 없다는 지적. `subissue_issue_id`/
   `alternative_issue_id`로 개명하고, 호스트가 참조된 issue의 `unit_id`를
   조회하는 방식으로 바꿨다.
2. **`unresolved_branch_points`는 서로 다른 unit 두 개를 요구하면 안 된다.**
   같은 unit(예: 특수강도치사) 안에서도 사실 판단(예: 의료과실이 통상적
   과실인지 독립적 중대 과오인지)에 따라 결론이 갈릴 수 있기 때문. 구조를
   `branch_unit_ids`(unit 2개 이상)에서 `affects_issue_ids` + `branch_conditions`
   (갈릴 수 있는 사실 판단을 서술한 문장, 2개 이상)로 교체 — 새 unit을
   요구하지 않고 이미 라우팅된 같은 issue의 조건부 분기를 서술한다.
3. **`required_conclusions`라는 이름이 "라우팅 단계는 결론을 내리지 않는다"는
   앞부분 규칙과 충돌한다.** 실제 의미는 결론이 아니라 정확한 법적 명칭 보존이므로
   `required_issue_labels`로 개명.

호스트에 `assess_routing_completeness()`(신규 함수)를 추가해 이 다섯 배열이
실제로 `issues`에 반영됐는지 대조한다 — 라우터가 하위쟁점/대안을 "이름만
적고" `issues`에 별도 항목으로 안 넣으면 `gap_type`이 붙은 기록으로 남는다
(`required_subissue_missing`/`alternative_route_missing`/
`dangling_issue_reference`). 케이스를 실패시키거나 자동으로 채워 넣지 않는다
— 기존 `01_rejected_issues.json`과 같은 "강등·기록만, 조용히 패치하지 않는다"
원칙. `scripts/run_rule_ir_native_lean.py`가 이 결과를 `01b_routing_completeness.json`
으로 저장하고, `required_issue_labels`는 writer에게 넘기는 죄명 라벨을
정확한 명칭으로 덮어쓰며(`특수강도`가 `강도`로 뭉개지는 것 방지), 나머지
네 배열은 새 "하위쟁점/분기/대안/정확한 죄명" 체크리스트 절로 렌더링돼
`04_write_prompt.md`에 추가된다. **두 번째 라우팅 호출은 없다** — M5 3콜
아키텍처([[m5-standard-architecture]] 참고)를 유지하기 위해 분기의 양쪽
unit 모두 같은 라우팅 호출 한 번 안에서 `issues`에 등재돼야 한다는 전제다.

프롬프트 승인 게이트에 따라 스키마·코드를 먼저 구현하고 전문을 채팅으로
제시해 위 세 가지 수정 지시를 받은 뒤에만 `prompts/rule_ir_native_issue_select.md`
에 새 절("하위 쟁점·분기·대안·정확한 죄명")을 설치했다. `scripts/audit_rule_ir_native_prompts.py`
에 다섯 필드가 schema의 `required`와 `properties`에 모두 있는지 검사하는
로직과 새 계약 문구(다섯 필드명 + precision guard 문구 "적용되는 법리나")를
추가 — 감사 통과 확인(`pass: 3 stages, 0 errors`). 신규 유닛테스트 5건
(`tests/test_rule_ir_native_host.py`) 통과, 기존 두 파일 타깃 재실행에서
회귀 없음 확인. **아직 실제 API/vLLM 실행으로는 검증 못함** — job 220007
(r10_p1_q1_ga + r14_p1_q2, `scripts/slurm/run_rule_ir_native_lean_batch.sh`,
로컬 vLLM gemma, `IDPR_HF_HOME` 명시)을 제출했으나 GPU 자원 부족으로
`PD (Resources)` 대기 중 — 완료되면 다섯 필드가 실제 guided-decoding 출력에서
스키마대로 채워지는지, `assess_routing_completeness`가 실제 gap을 잡아내는지
확인 필요. 전체 pytest 스위트도 이번 리네임 반영 후 재실행 중(직전 확인 시점
기준 642 passed / 11 failed, 전부 문서화된 기존 결함 — 리네임 이후 재확인은
다음 세션 또는 잡 완료 후 결과 참고).

**다음 세션(또는 잡 220007 완료 시) 할 일**: (1) job 220007 결과로 다섯 배열이
실제로 채워지는지, precision guard(모든 불확실성이 아니라 결론이 갈리는
지점만)가 지켜지는지, `01b_routing_completeness.json`의 `gaps`가 r10/r14에서
실제로 뭘 잡아내는지 확인. (2) 문제없으면 5단계(rule-base 범위 보완)로 진행.

### job 220007 스모크 결과 (같은 세션, GPU 대기 후 완료) — 구조는 작동, 정확도는 별개 문제

2건 모두 성공(`cases=2 failed=0`). 확인된 것:

- **precision guard가 실제로 지켜졌다.** 두 사례 모두 다섯 배열을 과다하게
  채우지 않았다(r10: `conclusion_sensitive_facts` 1건 + `alternative_legal_routes`
  1건만, 나머지 0건; r14: 다섯 배열 전부 0건). 우려했던 "모든 불확실성을
  분기"하는 과다분기는 관찰되지 않았다.
- **`unresolved_branch_points`/`unsupported` role_candidates 규칙은 정상
  준수**됐다 — r10의 `unit_id=unsupported` issue(`issue_6`, "강도치상")가
  `role_candidates: {}`, `depends_on_issue_ids: []`로 정확히 비어 있다.
- **`assess_routing_completeness`가 실제 gap을 잡아냈다.** r10에서
  `conclusion_sensitive_facts`가 `affects_issue_ids: ["issue_4"]`를 참조했는데,
  issue_4(강간미수)는 `source_quote`가 원문에 없어(`quote_not_grounded`)
  per-issue 강등으로 이미 `issues`에서 빠진 상태였다. 라우터가 참조를
  갱신하지 않아 생긴 진짜 dangling reference를 정확히 잡아 `01b_routing_completeness.json`
  의 `gaps`에 기록했다 — 설계 의도대로 동작.
- **`alternative_legal_routes`가 실제 법리 신호를 실어 날랐다.** r10에서
  "강도(issue_3) 폭행과 상해의 인과관계가 단절되면 강도치상이 아니라 강도+상해
  경합범"이라는 대안을 issue_5(상해)로 정확히 연결했고, writer가 이걸 받아
  최종 답안에서 "재물 탈취 의사가 없었으므로 강도치상 불성립 → 강간치상 검토"로
  실제로 활용해 이전 세션 진단(자기모순·헤지형 서술)보다 더 정확한 결론에
  도달했다(`05_answer.md`).
- **라우팅 정확도 자체는 이번 단계로 고쳐지지 않는다 — 예상된 결과.** r14에서
  `third_party_bribery`(증뢰물전달죄)가 활성 레지스트리에 있는데도 issue_2/
  issue_3이 여전히 `unit_id: unsupported`로 나왔다(문서화된 기존 결함 재현).
  다섯 배열 중 어느 것도 이 결함을 스스로 감지하거나 우회하지 못했다 —
  `required_subissues`/`alternative_legal_routes`는 라우터가 최소한 issue_id로
  "이게 필요하다"는 걸 알고 있을 때만 신호를 만든다. 애초에 유닛을 잘못
  판단(활성 유닛을 unsupported로 오분류)하는 문제는 구조 확장이 아니라
  라우터 자체의 유닛 판별 정확도 문제이므로 별도로 다뤄야 한다. writer는
  기존과 같이 "뇌물공여의 전달자"라는 개념을 즉석 창작했다.

**결론**: 4단계 구조(스키마·검증·writer 배선)는 설계대로 작동하고 실제로
답안 품질에 기여하는 사례(r10)를 만들어냈다. 다만 이 구조는 "라우터가 이미
알고 있는 관계"를 명시화하는 것이지 "라우터가 애초에 틀리게 고른 유닛"을
고치지 못한다 — r14의 유닛 누락은 5단계(rule-base 범위 보완)가 아니라 라우팅
정확도 자체의 문제로, 별도 이슈로 남겨둔다. **정정(같은 세션 후속 조사)**: 아래
절에서 밝혀지듯 실제 누락 대상은 `third_party_bribery`가 아니라 `bribe_giving`
이었다 — 사용자 지시로 다시 판 결과 확인.

### 라우팅 정확도 — third_party_bribery 오진단 정정 + 진단 필드 도입 + 회귀 배치 (같은 세션, 사용자 지시)

**사용자 결정: rule-base 범위 보완(5단계)보다 라우팅 정확도(활성 unit을
`unsupported`로 잘못 보내는 문제)를 먼저 고친다.** 이유: 카드를 더 추가해도
라우터가 그 카드를 고르지 않으면 그 사례는 계속 실행되지 않는다 — "진짜
미지원"과 "지원되는데 라우터가 놓침"을 섞으면 논문에서 서로 다른 실패
유형을 하나로 잘못 계상하게 된다.

**오진단 발견**: job 220007에서 `third_party_bribery`가 라우팅 정확도 문제의
사례로 지목됐으나, 등록 카드(`assess_art130_*`)를 직접 열어보니 전부 "공무원이
직무에 관하여 제3자에게 뇌물을 공여하게 하는" 제130조 제3자뇌물제공죄만
다룬다 — 사인(乙)이 사인(丙)에게 공무원(P1)에게 전달할 돈을 맡긴 r14의
사실관계와는 아예 다른 범죄다. 실제로 정확히 맞는 유닛은 `bribe_giving`
(제133조) — `assess_art133_sec1_2_*` 카드 세트가 증뢰물전달죄(제133조 제2항)
요건(교부·인식·독립된 제3자·완성시점 등)을 전부 담고 있고, role_predicate에
`intermediary_id`(전달자 역할)까지 이미 있다. 라우터가 이 유닛도 놓쳤다 — 즉
진짜 라우팅 누락은 있었지만 대상이 바뀐다.

**진단 필드 추가** (`native_host.py`): 각 issue에 `closest_allowed_unit_ids`
(최종 선택 전 비교한 후보, 최대 3개, `unsupported`가 아닐 때는 반드시 빈 배열)
`unsupported_reason`(선택 이유, `unsupported`일 때만 채움) 두 필드를
스키마에 무조건 필수로 추가하고, `validate_closed_issue_selection`이 양방향
계약(unsupported면 이유 필수, 아니면 두 필드 다 비어 있어야 함)을 강제한다.
호스트의 symbolic execution·writer 입력·평가에는 이 두 필드를 전혀 쓰지
않는다 — 순수 진단 trace. `diagnose_unsupported_issues()`가 이 trace로
"라우터가 실제 후보를 이름 붙이고도 거부함(`likely_routing_miss`)" 여부를
계산해 `01c_unsupported_diagnostics.json`으로 남긴다.

**catalog에 `legal_labels` 추가**: `closed_unit_catalog()`가 각 unit의
`role_definition`(예: `bribe_giving`="증뢰자 또는 전달자, 이익, 상대 공무원,
전달 제3자의 역할 tuple")이 죄명 자체(증뢰물전달죄)를 전혀 언급하지 않는다는
사실을 확인 — 이게 라우터가 이름으로 매칭 못 하는 근본 원인 중 하나로
보인다. 확인된 두 유닛(`bribe_giving`, `third_party_bribery`)에만 검증된
법률명을 채워 넣었다 — 36개 유닛 전체를 추측으로 채우지 않는다.

**프롬프트 개정**: `rule_ir_native_issue_select.md`에 "unsupported 판단
절차와 진단 근거" 절 신설 — (1) `allowed_units` 전부를 `role_definition`·
`legal_labels`와 사실관계 대조 (2) 죄명이 문자 그대로 안 적혀 있어도 행위·
대상·상대방 구조가 부합하면 선택 (3) 대조를 마친 뒤에도 안 맞으면
`unsupported` — 라는 3단계 절차와 위 두 진단 필드의 채움 규칙을 명시. 감사
스크립트(`audit_rule_ir_native_prompts.py`)에 계약 문구 검사와 5개 확장
배열의 schema `required`/`properties` 존재 검사를 추가, 통과 확인. 전체
스위트 재확인: **645 passed, 11 failed**(전부 기존 문서화된 결함, 회귀 없음).

**회귀 배치 결과 (job 220070, 6사례: r10_p1_q1_ga·r11_p1_q1·r12_p1_q1·
r13_p1_q1·r14_p1_q1·r14_p1_q2, `scripts/summarize_routing_regression.py`)**:

- **자동 지표(`unsupported_false_positive_rate` 등)는 신뢰할 수 없다.** 새
  프롬프트가 "unsupported를 고르면 후보를 반드시 적으라"고 지시하므로 모델이
  거의 항상 후보를 채운다 — `closest_allowed_unit_ids` 비어있지 않음 = 실제
  라우팅 누락이 아니다. 강도치상/강도상해(결합범 unit 자체가 없음), 살인교사·
  공모관계(레지스트리에 `declared_not_compiled`로 이미 문서화된 진짜 공백)도
  전부 후보를 채운 채 정당하게 `unsupported`로 남았다. 12건 중 9건을
  `likely_routing_miss=True`로 잘못 표시했다 — 이 숫자 자체를 논문 지표로 쓰면
  안 된다.
- **손으로 읽었을 때는 지표보다 훨씬 값진 것이 나왔다.** 두 건이 진짜 라우팅
  누락으로 확인됐고, **둘 다 같은 실패 모양**을 보였다: 모델이
  `closest_allowed_unit_ids`에 정확히 맞는 unit을 스스로 짚어내고도, 참여형태·
  분류 문제를 이유로 그 unit을 통째로 버렸다.
  - r12_p1_q1 "사문서위조": 후보 `['private_document_forgery']`(정확히 맞음,
    art231/232), 이유 "명확히 매칭되지 않음"(근거 없는 회피).
  - r14_p1_q2 issue_2(뇌물공여): 후보에 `bribe_giving`이 **이번에 처음
    등장**(legal_labels 추가가 recall 자체는 실제로 개선시켰다는 증거) — 그런데도
    "乙의 행위가 丙을 도구로 한 간접정범인지... 구체적 죄명 분류를 위해
    unsupported로 처리함"이라며 회피. `known_target_recall`에서 여전히
    `bribe_giving`이 `issues`에 없음(found: false) — 최종 선택 단계는 아직
    못 고쳤다.
- **결론**: 이번 세션 수정은 recall 단계(후보를 찾아내는 것)는 개선했지만
  decision 단계(찾은 후보를 실제로 쓰는 것)는 아직이다. 다음 수정은 더
  구체적이어야 한다 — "참여형태·가담정도(간접정범/공동정범 등)가 불확실하다는
  이유로 이미 부합하는 base unit 선택을 보류하지 마라. base unit은 선택하고
  그 불확실성은 `required_subissues`나 writer 체크리스트로 넘겨라"는 지시를
  추가해야 할 것으로 보인다. **미착수 — 다음 세션 시작점.**
- 산출물: `experiments/results/rule_ir_native_lean_routing_regression/`(6사례
  전체), `.cache/routing_expansion_smoke/regression_summary.json`(위 지표·
  사례별 원본 trace).

### decision 단계 프롬프트 수정 시도 — 2회 실패, 롤백 (다음 세션, 사용자 지시)

위 절 마지막에 미착수로 남겨둔 "참여형태 불확실성을 이유로 이미 부합하는 base unit
선택을 보류하지 마라"는 수정을 시도했으나, **두 번 다 실패해 롤백했다.**

1. **1차 시도(negative carve-out, commit `7b7656f`)**: "참여형태(직접정범/간접정범/
   공동정범 등)의 확정 여부는 unsupported 사유가 아니다"라는 4번째 절차를 추가.
   job 220071(같은 6사례 재실행, `rule_ir_native_lean_routing_regression_v2`)로 검증:
   `bribe_giving`/`private_document_forgery` 둘 다 여전히 `found: false`(전혀 무변화,
   unsupported 총계도 12→13으로 사실상 동일). `unsupported_reason` 원문 대조 결과, 모델이
   금지된 표현("간접정범인지... 구체적 죄명 분류를 위해")만 피하고 **똑같은 결론을 다른
   말("행위 유형을 가장 정확히 특정할 수 있는 단독 unit이 부족함")로 재포장**했다.
2. **2차 시도(affirmative rule + 회피 사유 금지 목록, commit `e913783`)**: "구조 부합
   판정을 내린 후보는 반드시 선택한다"는 단정 규칙으로 교체하고, 그때까지 관찰된 회피
   표현 4종(참여형태 불확실, 단독 unit 아님, 결합 구조 특정 필요, 완전 포괄 못함)을
   명시적으로 금지. job 220074(`rule_ir_native_lean_routing_regression_v3`)로 재검증:
   **역시 무변화** — 두 known-target 다시 `found: false`, `unsupported_reason`이 세
   번째 다른 표현("전달을 부탁한 주체로서의 성격이 강하고... 결합된 구조를 표현할
   적절한 unit이 부족함")으로 또 우회.
3. **사용자 결정: 강하게 강제해도 안 되면 롤백하고 다음 단계로.** `git revert -n
   e913783 7b7656f`로 두 커밋을 되돌려 `prompts/rule_ir_native_issue_select.md`/
   `scripts/audit_rule_ir_native_prompts.py`를 job 220070 시점 상태로 복원(감사·테스트
   재확인 완료, 회귀 없음). 산출물은 보존:
   `experiments/results/rule_ir_native_lean_routing_regression_v2/`,
   `..._v3/`, `.cache/routing_expansion_smoke/regression_summary_v{2,3}.json`.

**결론(중요, 다음 세션에 이 문제를 다시 열 때 참고)**: 이 특정 회피 패턴(구조가
부합한다고 스스로 서술해놓고도 완벽한 사실관계 일치를 요구하며 unsupported로
후퇴)은 **프롬프트 문구 수정만으로는 안 뚫린다** — 세 번(220070/220071/220074)
연속으로 같은 두 사례에서 매번 다른 표현으로 같은 결론을 냈다. 이건 26B 로컬
모델의 특정 문구 회피가 아니라 더 근본적인 결정 휴리스틱으로 보인다. 다음에
다시 시도한다면 프롬프트 문구가 아니라 **구조적 게이트**(예: `closest_allowed_unit_ids`가
비어있지 않은 채 `unit_id=unsupported`가 나오면 그 자체를 계약 위반으로 강등하거나,
1차 host-side 재검증 콜을 추가)를 고려할 것 — M5 3콜 원칙 이탈이므로 별도 승인 필요.

**다음 세션 시작점: 5단계 — rule-base 범위 보완.** job 220070에서 이미 확인된 진짜
공백(강도치상/강도상해 결합범 unit 부재, 살인교사·공모관계 `declared_not_compiled`)이
1순위 후보.

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
