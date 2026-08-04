# obstruction_of_official_duty RuleIR 승인 원장 감사

- status: `ready_for_rule_ir`
- approval: `data/rulegen/p2/native_review/obstruction_of_official_duty_approved_decisions.json`
- approval SHA-256: `c7f38b1ea88e010de8fb8e5685609a4b329c841656a0be01f7b5be2de3cf9018`
- law snapshot: `kr_criminal_act_effective_2026-08-03`
- queue cards: 54
- components: 13
- context_only 제외: 2
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
| `base` | `violence_or_threat` | bar, component | alternative_any | 19 | - |
| `official_coercion` | `absorption` | post_outcome |  | 1 | assault_or_threat |
| `official_coercion` | `coercion_definition` | component | mandatory_all | 1 | - |
| `official_coercion` | `coercive_conduct` | component | alternative_any | 2 | - |
| `official_coercion` | `official_act_scope` | bar, component | mandatory_all | 2 | coercion |
| `official_coercion` | `official_object` | component | mandatory_all | 1 | - |
| `official_coercion` | `specific_purpose` | component | mandatory_all | 1 | - |

## RuleIR에서 제외된 카드

- `art136_sec2_2.subject.unrestricted`: 주체 무제한 일반설명
- `art136_sec3_2.subject_unrestricted`: 주체 무제한 일반설명
