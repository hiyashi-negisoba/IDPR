# official_secret_disclosure RuleIR 승인 원장 감사

- status: `ready_for_rule_ir`
- approval: `data/rulegen/p2/native_review/official_secret_disclosure_approved_decisions.json`
- approval SHA-256: `f598ff5f7dca5a2f4c8e3bdf7cd2e4cc7df75ad7741b420480d1da889b7c5865`
- law snapshot: `kr_criminal_act_effective_2026-08-03`
- queue cards: 27
- components: 8
- context_only 제외: 0
- 미해결 unit 참조: 2

승인된 판정만 RuleIR 입력이 된다. 미해결 참조는 추측하지 않고 `predicate_ir_missing`으로 보고한다.

## 계약 위반

없음.

## 미해결 unit 참조

- `art127_sec7.special_law_priority` → `special_secret_disclosure` (predicate_ir_missing)
- `art127_sec7.special_offense_absorption` → `special_secret_disclosure` (predicate_ir_missing)

## component 구성

| track | component | role | join | 카드 수 | 참조 |
|---|---|---|---|---:|---|
| `base` | `acquired_in_official_duties` | bar, component | alternative_any | 4 | - |
| `base` | `bribery_concurrence` | post_outcome |  | 1 | bribe_receipt |
| `base` | `disclosure` | bar, component | alternative_any | 4 | - |
| `base` | `lawful_disclosure` | waiver |  | 1 | - |
| `base` | `official_status` | component | mandatory_all | 1 | - |
| `base` | `protectable_secret` | bar, component | alternative_any | 13 | - |
| `base` | `special_statute` | post_outcome |  | 2 | special_secret_disclosure |
| `base` | `specificity` | component | mandatory_all | 1 | - |

## RuleIR에서 제외된 카드

없음.
