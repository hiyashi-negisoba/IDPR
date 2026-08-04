# intentional_bodily_injury RuleIR 승인 원장 감사

- status: `ready_for_rule_ir`
- approval: `data/rulegen/p2/native_review/intentional_bodily_injury_approved_decisions.json`
- approval SHA-256: `6cab21f92cf2fb97f375998ab9c602401a5997c774104b26360baa3e53a4c30f`
- law snapshot: `kr_criminal_act_effective_2026-08-03`
- queue cards: 104
- components: 27
- context_only 제외: 15
- 미해결 unit 참조: 2

승인된 판정만 RuleIR 입력이 된다. 미해결 참조는 추측하지 않고 `predicate_ir_missing`으로 보고한다.

## 계약 위반

없음.

## 미해결 unit 참조

- `art257_sec1_4.intent_only_violence_result` → `assault_resulting_injury` (predicate_ir_missing)
- `art259_sec1.no_injury_intent_classification` → `assault_resulting_death` (predicate_ir_missing)

## component 구성

| track | component | role | join | 카드 수 | 참조 |
|---|---|---|---|---:|---|
| `aggravated_result` | `death_intent` | boundary |  | 2 | homicide |
| `aggravated_result` | `death_result` | boundary, component | mandatory_all | 3 | robbery |
| `aggravated_result` | `injury_intent` | boundary |  | 1 | assault_resulting_death |
| `aggravated_result` | `offense_count` | post_outcome |  | 2 | - |
| `aggravated_result` | `result_causation` | bar, component | alternative_any | 5 | - |
| `aggravated_result` | `result_foreseeability` | component | alternative_any | 2 | - |
| `ancestral` | `ancestral_relation` | bar, component | mandatory_all | 3 | - |
| `attempt` | `attempt_punishability` | component | mandatory_all | 2 | - |
| `attempt` | `attempt_result` | component | mandatory_all | 1 | - |
| `base` | `causation` | bar, component | mandatory_all | 3 | - |
| `base` | `concurrence` | post_outcome |  | 3 | homicide |
| `base` | `injury_concept` | bar, component | mandatory_all | 9 | - |
| `base` | `injury_conduct` | component | alternative_any | 5 | - |
| `base` | `injury_indicia` | component | alternative_any | 7 | - |
| `base` | `intent` | bar, boundary, component | alternative_any | 6 | assault_resulting_injury |
| `base` | `justification` | bar |  | 6 | - |
| `base` | `object_scope` | bar, component | mandatory_all | 8 | - |
| `base` | `offense_count` | post_outcome |  | 2 | - |
| `base` | `offense_count_standard` | post_outcome |  | 1 | - |
| `base` | `offense_definition` | component | mandatory_all | 1 | - |
| `concurrent_offenders` | `injury_result_required` | component | mandatory_all | 1 | - |
| `concurrent_offenders` | `resulting_offense` | post_outcome |  | 2 | - |
| `concurrent_offenders` | `simultaneous_offenders` | bar, component | mandatory_all | 6 | - |
| `concurrent_offenders` | `special_effect` | component | mandatory_all | 1 | - |
| `concurrent_offenders` | `special_provision_scope` | bar |  | 2 | - |
| `concurrent_offenders` | `unidentified_cause` | bar, component | mandatory_all | 3 | - |
| `special` | `special_means` | component | alternative_any | 2 | - |

## RuleIR에서 제외된 카드

- `art257.diagnosis_evidentiary_value`: 상해진단서의 증명력은 증거법 영역이며 구성요건 요소가 아니다
- `art257.subjective_pain_diagnosis_assessment`: 상해진단서의 증명력 판단 기준이며 증거법 영역이다
- `art257_sec1_6.disciplinary_injury`: 징계가 상해에 이르면 조각되지 않는다는 조각의 한계이며, 현재 역할 어휘에 자리가 없다
- `art257_sec1_6.insufficient_medical_explanation`: 부정확·불충분한 설명에 기한 승낙은 무효라는 조각의 한계
- `art257_sec1_6.military_detention_beating`: 훈육권·징계권의 범위를 넘은 감금·구타는 위법하다는 조각의 한계
- `art257_sec1_6.military_unauthorized_punishment_order`: 권한 없는 얼차려 지시는 정당행위가 아니라는 조각의 한계
- `art257_sec1_6.mutual_fight_no_self_defense`: 싸움에 의한 상호 상해는 정당방위로 조각되지 않는다는 조각의 한계
- `art257_sec1_6.old_education_law_injurious_corporal_punishment`: 체벌이 상해에 이르면 위법하다는 조각의 한계
- `art257_sec1_6.pre_amendment_teacher_guidance`: 교육상 불가피성과 객관적 타당성을 모두 갖춘 경우에만 허용된다는 조각의 한계
- `art2582_2_sec2.favorable_law_change`: 형법 제1조 제2항 경과규정의 적용 문제이며 총칙 영역이다
- `art2582_2_sec2.no_abolition_dangerous_object_injury`: 같은 경과규정의 적용 결과이며 총칙 영역이다
- `art2582_2_sec3.habitual_offender_aggravation`: 상습범 가중은 제264조이며 현재 51조문 범위 밖이다
- `art2582_2_sec3.qualification_suspension`: 자격정지 병과는 양형 사항이며 성립 결론을 바꾸지 않는다
- `art2582_2_sec3.recidivist_aggravation`: 폭력행위 등 처벌에 관한 법률의 누범 가중이며 특별법 영역이다
- `art263.individual_liability_principle`: 특례가 수정하는 개인책임 원칙의 배경 서술이다
