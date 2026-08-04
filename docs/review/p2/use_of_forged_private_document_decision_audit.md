# use_of_forged_private_document RuleIR 승인 원장 감사

- status: `ready_for_rule_ir`
- approval: `data/rulegen/p2/native_review/use_of_forged_private_document_approved_decisions.json`
- approval SHA-256: `50e55ae4bff6cf9297067b5a843906601b2e1d84478b81eaa255fa9dcd06b08a`
- law snapshot: `kr_criminal_act_effective_2026-08-03`
- queue cards: 22
- components: 6
- context_only 제외: 3
- 미해결 unit 참조: 0

승인된 판정만 RuleIR 입력이 된다. 미해결 참조는 추측하지 않고 `predicate_ir_missing`으로 보고한다.

## 계약 위반

없음.

## 미해결 unit 참조

없음.

## component 구성

| track | component | role | join | 카드 수 | 참조 |
|---|---|---|---|---:|---|
| `base` | `attempt` | post_outcome |  | 1 | - |
| `base` | `concurrence` | post_outcome |  | 3 | private_document_forgery |
| `base` | `covered_forged_instrument` | component | alternative_any | 2 | private_document_forgery |
| `base` | `exercise` | bar, component | alternative_any | 10 | - |
| `base` | `intent` | component | mandatory_all | 1 | - |
| `base` | `unaware_interested_counterparty` | bar, component | mandatory_all | 2 | - |

## RuleIR에서 제외된 카드

- `art234_sec2_1.no_actual_harm_required`: 실해 불요 또는 주체 무제한의 일반 설명
- `art234_sec2_1.no_actual_recognition_or_harm_risk_required`: 실해 불요 또는 주체 무제한의 일반 설명
- `art234_sec2_1.unrestricted_principal`: 실해 불요 또는 주체 무제한의 일반 설명
