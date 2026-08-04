# rape RuleIR 승인 원장 감사

- status: `ready_for_rule_ir`
- approval: `data/rulegen/p2/native_review/rape_approved_decisions.json`
- approval SHA-256: `8aa38d0d3f1e1bfccf0bc800f6a3c4ce2cc622c118c26e561d630a815cabd10a`
- law snapshot: `kr_criminal_act_effective_2026-08-03`
- queue cards: 56
- components: 21
- context_only 제외: 10
- 미해결 unit 참조: 12

승인된 판정만 RuleIR 입력이 된다. 미해결 참조는 추측하지 않고 `predicate_ir_missing`으로 보고한다.

## 계약 위반

없음.

## 미해결 unit 참조

- `art297.relative_special_act` → `relative_sexual_offense` (predicate_ir_missing)
- `art297.special-protection-statutes` → `protected_victim_sexual_offense` (predicate_ir_missing)
- `art297_sec4_2.non_vaginal_acts_exception` → `quasi_rape` (predicate_ir_missing)
- `art297_sec4_4.successive_co_perpetration_negative` → `complicity` (predicate_ir_missing)
- `art297_sec9.abduction_for_marriage_rape` → `abduction_for_marriage` (predicate_ir_missing)
- `art297_sec9.confinement_rape_attempted_case` → `confinement` (predicate_ir_missing)
- `art297_sec9.continued_confinement_after_rape` → `confinement` (predicate_ir_missing)
- `art297_sec9.means_violence_absorption` → `assault_or_threat` (predicate_ir_missing)
- `art297_sec9.separate_confinement_rape_violence` → `confinement` (predicate_ir_missing)
- `art297_sec9.special_rape` → `special_rape` (predicate_ir_missing)
- `art297_sec9.special_robbery_rape` → `special_robbery_rape` (predicate_ir_missing)
- `art297_sec9.special_theft_rape` → `special_theft_rape` (predicate_ir_missing)

## component 구성

| track | component | role | join | 카드 수 | 참조 |
|---|---|---|---|---:|---|
| `base` | `absence_of_consent` | bar, component | alternative_any | 4 | - |
| `base` | `aggravated_result` | post_outcome |  | 1 | sexual_offense_injury_or_death |
| `base` | `attempt_commencement` | post_outcome |  | 1 | sexual_offense_attempt |
| `base` | `attempt_commencement_standard` | post_outcome |  | 1 | sexual_offense_attempt |
| `base` | `attempt_outcome` | post_outcome |  | 1 | sexual_offense_attempt |
| `base` | `causation` | component | mandatory_all | 1 | - |
| `base` | `coercion_attribution` | boundary |  | 1 | quasi_sexual_offense |
| `base` | `coercion_timing` | component | alternative_any | 2 | - |
| `base` | `coercive_degree` | component | alternative_any | 6 | - |
| `base` | `coercive_means` | component | mandatory_all | 1 | - |
| `base` | `concurrence` | post_outcome |  | 6 | abduction_for_marriage, assault_or_threat, confinement, theft |
| `base` | `intent` | bar, component | mandatory_all | 2 | - |
| `base` | `object_scope` | component | mandatory_all | 1 | - |
| `base` | `offense_count` | post_outcome |  | 3 | - |
| `base` | `offense_definition` | component | alternative_any | 2 | - |
| `base` | `offense_scope` | post_outcome |  | 5 | dwelling_intrusion, robbery, special_rape, special_robbery_rape, special_theft_rape |
| `base` | `participation_form` | post_outcome |  | 2 | complicity, quasi_sexual_offense |
| `base` | `penetration` | bar, component | mandatory_all | 2 | quasi_rape |
| `base` | `sex_classification` | component | mandatory_all | 1 | - |
| `base` | `sex_pair` | component | mandatory_all | 1 | - |
| `base` | `special_statute` | post_outcome |  | 2 | protected_victim_sexual_offense, relative_sexual_offense |

## RuleIR에서 제외된 카드

- `art297.indirect_perpetration`: 간접정범은 intermediary 역할과 총칙 module 없이 단독 피고인 tuple로 실행할 수 없음
- `art297.unrestricted_principal`: 주체 무제한 설명만으로 구체적 강간행위나 간접정범 형태를 증명하지 않음
- `art297_sec10.planned_killing_after_rape_no_self_defense`: 강간 피해자의 사후 계획살인에 관한 살인·정당방위 문맥이지 피고인의 강간 성립요건이 아님
- `art297_sec10.self_defense_against_rape`: 피해자의 방어행위 위법성 조각은 별도 정당방위 문제
- `art297_sec10.tongue_biting_self_defense`: 피해자의 혀 절단 반격에 관한 정당방위 사례
- `art297_sec4_1.gender_sensitive_limit`: 성인지 관점에도 증명력 한계가 있다는 증거평가 문맥
- `art297_sec4_1.gender_sensitive_testimony`: 피해자다움을 요구하지 않는 진술 신빙성 평가기준
- `art297_sec4_1.no_retrospective_inference`: 사후 이탈·불충분한 반항만으로 강제성을 부정하지 말라는 증거평가 한계
- `art297_sec4_1.victim_testimony_reliability`: 유일한 직접증거인 피해자 진술의 증명력 판단기준
- `art297_sec9.nonprosecution_not_false_report_proof`: 불기소·무죄만으로 무고를 증명할 수 없다는 절차·증거 문맥
