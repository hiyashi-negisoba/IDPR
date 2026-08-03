# arson_of_occupied_structure RuleIR 승인 원장 감사

- status: `ready_for_rule_ir`
- approval: `data/rulegen/p2/native_review/arson_of_occupied_structure_approved_decisions.json`
- approval SHA-256: `99aca927fc6c2e3429815a240f74d6f38700f4f7dd82a62018ef49a4575f966f`
- law snapshot: `kr_criminal_act_effective_2026-08-03`
- queue cards: 52
- components: 28
- context_only 제외: 4
- 미해결 unit 참조: 5

승인된 판정만 RuleIR 입력이 된다. 미해결 참조는 추측하지 않고 `predicate_ir_missing`으로 보고한다.

## 계약 위반

없음.

## 미해결 unit 참조

- `art164_sec2_1.accomplices_residence_general_building` → `general_structure_arson` (predicate_ir_missing)
- `art164_sec2_1.derelict_building_not_building_precedent` → `object_arson` (predicate_ir_missing)
- `art164_sec2_1.no_attempt_before_ignition#preparation_referral` → `arson_preparation` (predicate_ir_missing)
- `art164_sec2_1.residence_factual_use` → `general_structure_arson` (predicate_ir_missing)
- `art164_sec2_1.sole_offender_home_general_building` → `general_structure_arson` (predicate_ir_missing)

## component 구성

| track | component | role | join | 카드 수 | 참조 |
|---|---|---|---|---:|---|
| `aggravated_result` | `aggravated_result_basis` | component | mandatory_all | 1 | - |
| `aggravated_result` | `aggravated_result_subject` | component | alternative_any | 1 | - |
| `aggravated_result` | `concurrence` | post_outcome |  | 1 | - |
| `aggravated_result` | `concurrence_with_homicide` | post_outcome |  | 5 | homicide, robbery |
| `aggravated_result` | `person_scope` | component | mandatory_all | 1 | - |
| `aggravated_result` | `result_causation` | component | alternative_any | 1 | - |
| `aggravated_result` | `result_foreseeability` | bar, component | mandatory_all | 2 | - |
| `aggravated_result` | `result_foreseeability_per_participant` | component | mandatory_all | 2 | - |
| `attempt` | `attempt_commencement` | bar, component | alternative_any | 5 | dwelling_intrusion |
| `base` | `arson_conduct` | component | alternative_any | 2 | - |
| `base` | `object_identity` | component | alternative_any | 1 | - |
| `base` | `person_scope` | boundary, component | mandatory_all | 2 | general_structure_arson |
| `base` | `presence` | component | mandatory_all | 1 | - |
| `base` | `protected_object` | boundary |  | 2 | general_structure_arson, object_arson |
| `base` | `protected_object_building` | component | mandatory_all | 1 | - |
| `base` | `protected_object_class` | component | alternative_any | 1 | - |
| `base` | `residence_or_presence` | bar, component | alternative_any | 3 | - |
| `base` | `residence_use` | bar, boundary, component | mandatory_all | 3 | general_structure_arson |
| `base` | `residence_use_indicia` | component | alternative_any | 2 | - |
| `completed` | `act_unity` | post_outcome |  | 1 | - |
| `completed` | `burning_definition` | component | mandatory_all | 1 | - |
| `completed` | `combustion_mode` | component | alternative_any | 1 | - |
| `completed` | `concurrence` | post_outcome |  | 1 | property_damage |
| `completed` | `concurrence_with_homicide` | post_outcome |  | 1 | homicide |
| `completed` | `independent_combustion` | component | mandatory_all | 3 | - |
| `completed` | `offense_count` | post_outcome |  | 3 | - |
| `completed` | `offense_count_standard` | post_outcome |  | 1 | - |
| `preparation` | `preparation_referral` | boundary |  | 1 | arson_preparation |

## RuleIR에서 제외된 카드

- `art164.fire_insurance_claim_concurrence`: 보험사기방지특별법은 현재 51조문 RuleIR 범위 밖
- `art164.pre_claim_insurance_fraud_no_attempt`: 보험사기 실행착수 판단은 현재 범위 밖
- `art164_sec2_1.independent_combustion_ceiling_case`: 개별 사체·천정 사례이며 현재 quote만으로 일반 RuleIR 경로를 추가할 필요 없음
- `art164_sec2_2.mental_weakness_serial_arson_case`: 형법 제10조 제2항 심신미약은 총칙 영역이고 현재 51조문 밖. unit outcome을 바꾸지 않음
