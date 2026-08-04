# deceptive_obstruction_of_official_duty RuleIR 승인 원장 감사

- status: `ready_for_rule_ir`
- approval: `data/rulegen/p2/native_review/deceptive_obstruction_of_official_duty_approved_decisions.json`
- approval SHA-256: `447abec147ed400c85fd436dd43c3c182253cfbb85d57e257e6bd7ebd741628b`
- law snapshot: `kr_criminal_act_effective_2026-08-03`
- queue cards: 50
- components: 6
- context_only 제외: 1
- 미해결 unit 참조: 1

승인된 판정만 RuleIR 입력이 된다. 미해결 참조는 추측하지 않고 `predicate_ir_missing`으로 보고한다.

## 계약 위반

없음.

## 미해결 unit 참조

- `art137_sec6.false_report_absorption` → `false_report` (predicate_ir_missing)

## component 구성

| track | component | role | join | 카드 수 | 참조 |
|---|---|---|---|---:|---|
| `base` | `absorption` | post_outcome |  | 2 | dereliction_of_duty, false_report |
| `base` | `actual_obstruction` | bar, component | alternative_any | 16 | - |
| `base` | `deception` | bar, component | alternative_any | 24 | - |
| `base` | `intent` | bar |  | 1 | - |
| `base` | `offender_harboring` | post_outcome |  | 1 | harboring_offender |
| `base` | `official_duty` | bar, component | alternative_any | 5 | - |

## RuleIR에서 제외된 카드

- `art137_sec2.unrestricted_subject`: 주체 무제한 일반설명
