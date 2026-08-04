# quasi_sexual_offense RuleIR 승인 원장 감사

- status: `ready_for_rule_ir`
- approval: `data/rulegen/p2/native_review/quasi_sexual_offense_approved_decisions.json`
- approval SHA-256: `2a07daf2ddf5f4261a73ee7b6cb3073feda5e1121f527cf75112d2174edf3de1`
- law snapshot: `kr_criminal_act_effective_2026-08-03`
- queue cards: 26
- components: 9
- context_only 제외: 2
- 미해결 unit 참조: 2

승인된 판정만 RuleIR 입력이 된다. 미해결 참조는 추측하지 않고 `predicate_ir_missing`으로 보고한다.

## 계약 위반

없음.

## 미해결 unit 참조

- `art299_sec8.noncomplaint_prosecution` → `criminal_procedure` (predicate_ir_missing)
- `art299_sec8.noncomplaint_retroactivity` → `criminal_procedure` (predicate_ir_missing)

## component 구성

| track | component | role | join | 카드 수 | 참조 |
|---|---|---|---|---:|---|
| `base` | `attempt_stage` | post_outcome |  | 3 | sexual_offense_attempt |
| `base` | `changed_circumstances` | post_outcome |  | 1 | rape |
| `base` | `conduct` | component | alternative_any | 3 | - |
| `base` | `incapacity` | bar, component | alternative_any | 9 | rape |
| `base` | `intent` | bar, component | alternative_any | 3 | - |
| `base` | `object_scope` | component | mandatory_all | 1 | - |
| `base` | `offense_count` | post_outcome |  | 1 | - |
| `base` | `prosecution` | post_outcome |  | 2 | criminal_procedure |
| `base` | `use_of_state` | component | mandatory_all | 1 | - |

## RuleIR에서 제외된 카드

- `art299.principal.unrestricted`: 주체 일반설명 또는 공소장변경·방어권에 관한 증거절차 문맥
- `art299_sec8.quasi_indecent_act_indictment_amendment`: 주체 일반설명 또는 공소장변경·방어권에 관한 증거절차 문맥
