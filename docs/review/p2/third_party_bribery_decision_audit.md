# third_party_bribery RuleIR 승인 원장 감사

- status: `ready_for_rule_ir`
- approval: `data/rulegen/p2/native_review/third_party_bribery_approved_decisions.json`
- approval SHA-256: `501f3ff14caa0df2102a50606f57d73d72ec323aee180830170e141cddbaca6c`
- law snapshot: `kr_criminal_act_effective_2026-08-03`
- queue cards: 38
- components: 6
- context_only 제외: 1
- 미해결 unit 참조: 4

승인된 판정만 RuleIR 입력이 된다. 미해결 참조는 추측하지 않고 `predicate_ir_missing`으로 보고한다.

## 계약 위반

없음.

## 미해결 unit 참조

- `art130_sec3-na.joint-bribery-conspiracy` → `complicity` (predicate_ir_missing)
- `art130_sec3-na.joint-bribery-no-specific-amount` → `complicity` (predicate_ir_missing)
- `art130_sec3-na.nonofficial-joint-bribery` → `complicity` (predicate_ir_missing)
- `art130_sec4_2.contract_demand_imaginary_concurrence` → `abuse_of_authority` (predicate_ir_missing)

## component 구성

| track | component | role | join | 카드 수 | 참조 |
|---|---|---|---|---:|---|
| `base` | `complicity` | post_outcome |  | 3 | complicity |
| `base` | `improper_request` | bar, component | alternative_any | 10 | - |
| `base` | `independent_third_party_benefit` | bar, component | alternative_any | 21 | bribe_receipt |
| `base` | `offense_count` | post_outcome |  | 1 | - |
| `base` | `offense_definition` | component | mandatory_all | 1 | - |
| `base` | `office_abuse_concurrence` | post_outcome |  | 1 | abuse_of_authority |

## RuleIR에서 제외된 카드

- `art130_sec2_2.indictment_particularity`: 공소사실 특정 정도에 관한 절차법 문맥
