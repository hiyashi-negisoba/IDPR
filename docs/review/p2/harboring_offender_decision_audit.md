# harboring_offender RuleIR 승인 원장 감사

- status: `ready_for_rule_ir`
- approval: `data/rulegen/p2/native_review/harboring_offender_approved_decisions.json`
- approval SHA-256: `aaecc040bd107ddd89066117cf31e2f42ad09686a11f414f8142563014bd99ee`
- law snapshot: `kr_criminal_act_effective_2026-08-03`
- queue cards: 58
- components: 12
- context_only 제외: 4
- 미해결 unit 참조: 3

승인된 판정만 RuleIR 입력이 된다. 미해결 참조는 추측하지 않고 `predicate_ir_missing`으로 보고한다.

## 계약 위반

없음.

## 미해결 unit 참조

- `art151_sec2_5.self_escape_instigation_abuse_of_defense_precedent` → `complicity` (predicate_ir_missing)
- `art151_sec2_6.military_deserter_harboring_special_law` → `military_deserter_harboring` (predicate_ir_missing)
- `art151_sec3_3.nonrelative_accomplice` → `complicity` (predicate_ir_missing)

## component 구성

| track | component | role | join | 카드 수 | 참조 |
|---|---|---|---|---:|---|
| `base` | `absorption` | post_outcome |  | 1 | dereliction_of_duty |
| `base` | `attempt_stage` | post_outcome |  | 2 | - |
| `base` | `concealment_or_escape_assistance` | bar, component | alternative_any | 24 | - |
| `base` | `cooffender_effect` | post_outcome |  | 1 | complicity |
| `base` | `danger_and_completion` | component | alternative_any | 3 | - |
| `base` | `deceptive_obstruction` | post_outcome |  | 3 | deceptive_obstruction_of_official_duty |
| `base` | `instigation` | post_outcome |  | 1 | complicity |
| `base` | `intent` | bar, component | alternative_any | 5 | - |
| `base` | `lawful_defense_or_family` | waiver |  | 6 | - |
| `base` | `non_offender_subject` | bar, component | mandatory_all | 2 | - |
| `base` | `qualifying_offender` | bar, component | alternative_any | 5 | - |
| `base` | `special_statute` | post_outcome |  | 1 | military_deserter_harboring |

## RuleIR에서 제외된 카드

- `art151_sec3_2.covered_relatives`: 친족 범위와 본인을 위한 형사상 이익의 특례 해석 문맥
- `art151_sec3_2.criminal_benefit_objective_test`: 친족 범위와 본인을 위한 형사상 이익의 특례 해석 문맥
- `art151_sec3_2.for_benefit_of_principal`: 친족 범위와 본인을 위한 형사상 이익의 특례 해석 문맥
- `art151_sec3_2.non_criminal_benefit_exclusion`: 친족 범위와 본인을 위한 형사상 이익의 특례 해석 문맥
