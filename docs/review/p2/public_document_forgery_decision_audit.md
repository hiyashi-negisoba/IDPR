# public_document_forgery RuleIR 승인 원장 감사

- status: `ready_for_rule_ir`
- approval: `data/rulegen/p2/native_review/public_document_forgery_approved_decisions.json`
- approval SHA-256: `db2163aeb3b040ef29f812b2585c261a0ff56df6eacf10c3453cb7cbfe9bdc92`
- law snapshot: `kr_criminal_act_effective_2026-08-03`
- queue cards: 43
- components: 7
- context_only 제외: 0
- 미해결 unit 참조: 0

승인된 판정만 RuleIR 입력이 된다. 미해결 참조는 추측하지 않고 `predicate_ir_missing`으로 보고한다.

## 계약 위반

없음.

## 미해결 unit 참조

없음.

## component 구성

| track | component | role | join | 카드 수 | 참조 |
|---|---|---|---|---:|---|
| `alteration` | `alteration_intent` | component | alternative_any | 2 | - |
| `alteration` | `identity_preserving_change` | bar, component | alternative_any | 11 | public_document_forgery |
| `attempt` | `punishable_attempt` | bar, component | alternative_any | 4 | - |
| `common` | `intent_to_use` | component | alternative_any | 5 | - |
| `forgery` | `forgery_intent` | component | mandatory_all | 1 | - |
| `forgery` | `official_document` | bar, component | alternative_any | 13 | - |
| `forgery` | `unauthorized_creation` | bar, component | alternative_any | 7 | - |

## RuleIR에서 제외된 카드

없음.
