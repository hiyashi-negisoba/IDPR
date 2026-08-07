# obstruction_of_official_duty RuleIR 승인 원장 감사

- status: `ready_for_rule_ir`
- approval: `data/rulegen/p2/native_review/obstruction_of_official_duty_approved_decisions.json`
- approval SHA-256: `0d19f43eac61487f2875bc88103270e8e00a6e560b67875a0cedbd522d65538a`
- law snapshot: `kr_criminal_act_effective_2026-08-03`
- queue cards: 54
- components: 13
- context_only 제외: 3
- 미해결 unit 참조: 6

승인된 판정만 RuleIR 입력이 된다. 미해결 참조는 추측하지 않고 `predicate_ir_missing`으로 보고한다.

## 계약 위반

없음.

## 미해결 unit 참조

- `art136_sec1.special_offense_displacement` → `special_official_duty_obstruction` (predicate_ir_missing)
- `art136_sec2_6.illegal_duty_act.other_offenses` → `assault_or_threat` (predicate_ir_missing)
- `art136_sec2_7.military_criminal_act_special_relation` → `special_official_duty_obstruction` (predicate_ir_missing)
- `art136_sec2_7.special_public_duty_provisions` → `special_official_duty_obstruction` (predicate_ir_missing)
- `art136_sec3_4.nonofficial_act_coercion` → `coercion` (predicate_ir_missing)
- `art136_sec3_6.assault_threat_absorption` → `assault_or_threat` (predicate_ir_missing)

## component 구성

| track | component | role | join | 카드 수 | 참조 |
|---|---|---|---|---:|---|
| `base` | `concurrence` | post_outcome |  | 4 | intentional_bodily_injury |
| `base` | `intent` | component | alternative_any | 3 | - |
| `base` | `lawful_duty_execution` | bar, component | alternative_any | 13 | - |
| `base` | `public_official_object` | component | mandatory_all | 1 | - |
| `base` | `special_statute` | post_outcome |  | 3 | special_official_duty_obstruction |
| `base` | `unlawful_duty_response` | post_outcome |  | 1 | assault_or_threat |
| `base` | `violence_or_threat` | bar, component | alternative_any | 18 | - |
| `official_coercion` | `absorption` | post_outcome |  | 1 | assault_or_threat |
| `official_coercion` | `coercion_definition` | component | mandatory_all | 1 | - |
| `official_coercion` | `coercive_conduct` | component | alternative_any | 2 | - |
| `official_coercion` | `official_act_scope` | bar, component | mandatory_all | 2 | coercion |
| `official_coercion` | `official_object` | component | mandatory_all | 1 | - |
| `official_coercion` | `specific_purpose` | component | mandatory_all | 1 | - |

## RuleIR에서 제외된 카드

- `art136_sec2_2.subject.unrestricted`: 주체 무제한 일반설명
- `art136_sec2_4.active_conduct_requirement`: 일반 원칙(적극적 행위 요건) 재진술 — 같은 component에 이미 사실관계별 bar 카드 5장(passive_resistance_not_assault/preplaced_obstacles_not_assault/self_harm_not_assault_or_threat/vehicle_departure_not_assault/assault_not_against_officer_exception)이 이 원칙을 각각 구체적 사실유형으로 정확히 구현하고 있어 이 카드가 별도 bar일 필요가 없음. 이 카드는 satisfied=적극적 행위가 '있었다'는 뜻인데 bar로 배선되면 폭행이 실제로 인정될수록 오히려 불성립으로 뒤집히는 극성 역전 버그였다(2026-08-07 발견, docs/handoff/CURRENT.md).
- `art136_sec3_2.subject_unrestricted`: 주체 무제한 일반설명
