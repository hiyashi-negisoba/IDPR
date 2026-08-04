# false_public_document RuleIR 승인 원장 감사

- status: `ready_for_rule_ir`
- approval: `data/rulegen/p2/native_review/false_public_document_approved_decisions.json`
- approval SHA-256: `ba7470084e10ebe00c34bb35398697468fa1bb181e267db6ea1692cd26aa1376`
- law snapshot: `kr_criminal_act_effective_2026-08-03`
- queue cards: 44
- components: 6
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
| `base` | `bribery_concurrence` | post_outcome |  | 1 | bribe_receipt |
| `base` | `dereliction_concurrence` | post_outcome |  | 1 | dereliction_of_duty |
| `base` | `false_creation_or_change` | bar, component | alternative_any | 24 | - |
| `base` | `intent_and_use_purpose` | bar, component | alternative_any | 4 | - |
| `base` | `official_authority` | bar, component | alternative_any | 12 | public_document_forgery |
| `base` | `official_document` | component | alternative_any | 2 | - |

## RuleIR에서 제외된 카드

없음.
