# private_document_forgery RuleIR 승인 원장 감사

- status: `ready_for_rule_ir`
- approval: `data/rulegen/p2/native_review/private_document_forgery_approved_decisions.json`
- approval SHA-256: `685b110cf99b1576730a4c40e16761777c3ce9c31ab23f74b8a8cf6476ad493f`
- law snapshot: `kr_criminal_act_effective_2026-08-03`
- queue cards: 44
- components: 7
- context_only 제외: 0
- 미해결 unit 참조: 1

승인된 판정만 RuleIR 입력이 된다. 미해결 참조는 추측하지 않고 `predicate_ir_missing`으로 보고한다.

## 계약 위반

없음.

## 미해결 unit 참조

- `art231_sec6.own_document_altered_in_anothers_possession` → `document_damage` (predicate_ir_missing)

## component 구성

| track | component | role | join | 카드 수 | 참조 |
|---|---|---|---|---:|---|
| `alteration` | `document_damage` | post_outcome |  | 1 | document_damage |
| `alteration` | `identity_preserving_change` | bar, component | alternative_any | 14 | - |
| `attempt` | `punishable_attempt` | component | alternative_any | 2 | - |
| `common` | `intent_and_use_purpose` | component | alternative_any | 5 | - |
| `common` | `protected_document` | bar, component | alternative_any | 8 | - |
| `forgery` | `seal_absorption` | post_outcome |  | 1 | seal_forgery_or_misuse |
| `forgery` | `unauthorized_creation` | bar, component | alternative_any | 13 | fraud |

## RuleIR에서 제외된 카드

없음.
