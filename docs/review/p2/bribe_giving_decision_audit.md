# bribe_giving RuleIR 승인 원장 감사

- status: `ready_for_rule_ir`
- approval: `data/rulegen/p2/native_review/bribe_giving_approved_decisions.json`
- approval SHA-256: `a2de8fef99ca7ccb45ab3ee5b2fc9bceb9230782234674c22f8b2393daf09746`
- law snapshot: `kr_criminal_act_effective_2026-08-03`
- queue cards: 26
- components: 8
- context_only 제외: 4
- 미해결 unit 참조: 0

승인된 판정만 RuleIR 입력이 된다. 미해결 참조는 추측하지 않고 `predicate_ir_missing`으로 보고한다.

## 계약 위반

없음.

## 미해결 unit 참조

없음.

## component 구성

| track | component | role | join | 카드 수 | 참조 |
|---|---|---|---|---:|---|
| `common` | `benefit_and_duty_relation` | component | alternative_any | 3 | - |
| `common` | `independent_third_party` | bar, component | mandatory_all | 2 | - |
| `delivery_giver` | `delivery_by_giver` | component | mandatory_all | 1 | - |
| `delivery_recipient` | `absorption` | post_outcome |  | 1 | - |
| `delivery_recipient` | `delivery_intent` | component | mandatory_all | 1 | - |
| `delivery_recipient` | `delivery_receipt` | bar, component | alternative_any | 4 | - |
| `offering` | `offering_conduct` | bar, component | alternative_any | 9 | - |
| `offering` | `offering_intent` | component | mandatory_all | 1 | - |

## RuleIR에서 제외된 카드

- `art133_sec1_2.receiver_bribery_not_required`: 상대방 수뢰죄 독립성, 공소사실 특정, 처분권 또는 주체 일반설명
- `art133_sec1_2.specific_duty_authority_allegation`: 상대방 수뢰죄 독립성, 공소사실 특정, 처분권 또는 주체 일반설명
- `art133_sec1_2.substantive_use_disposal_authority`: 상대방 수뢰죄 독립성, 공소사실 특정, 처분권 또는 주체 일반설명
- `art133_sec1_2.unrestricted_offender`: 상대방 수뢰죄 독립성, 공소사실 특정, 처분권 또는 주체 일반설명
