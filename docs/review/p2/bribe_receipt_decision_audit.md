# bribe_receipt RuleIR 승인 원장 감사

- status: `ready_for_rule_ir`
- approval: `data/rulegen/p2/native_review/bribe_receipt_approved_decisions.json`
- approval SHA-256: `48196ad0fb00ddff6aa58ec2b6c1cf9efbbdb1fa018ca8f721ea2a23cc67757c`
- law snapshot: `kr_criminal_act_effective_2026-08-03`
- queue cards: 55
- components: 13
- context_only 제외: 6
- 미해결 unit 참조: 0

승인된 판정만 RuleIR 입력이 된다. 미해결 참조는 추측하지 않고 `predicate_ir_missing`으로 보고한다.

## 계약 위반

없음.

## 미해결 unit 참조

없음.

## component 구성

| track | component | role | join | 카드 수 | 참조 |
|---|---|---|---|---:|---|
| `current_common` | `bribe_and_duty_relation` | bar, component | alternative_any | 8 | - |
| `current_common` | `current_status` | component | alternative_any | 3 | - |
| `current_common` | `intent` | component | mandatory_all | 1 | - |
| `demand` | `active_demand` | bar, component | alternative_any | 3 | - |
| `prior` | `prior_intent` | component | mandatory_all | 1 | - |
| `prior` | `prior_offense_definition` | bar, component | mandatory_all | 5 | fraud |
| `prior` | `prior_request` | component | mandatory_all | 1 | - |
| `prior` | `prospective_status` | component | mandatory_all | 1 | - |
| `promise` | `definite_agreement` | component | alternative_any | 3 | - |
| `receipt` | `absorption` | post_outcome |  | 1 | - |
| `receipt` | `appropriation_intent` | bar, component | alternative_any | 8 | - |
| `receipt` | `offense_count` | post_outcome |  | 3 | - |
| `receipt` | `receipt` | bar, component | alternative_any | 11 | - |

## RuleIR에서 제외된 카드

- `art129.bribery_giving_despite_coercion`: 증뢰·공갈·횡령 구별 또는 구체성 낮은 증거·사례 문맥
- `art129.coercion_independent_bribery_decision`: 증뢰·공갈·횡령 구별 또는 구체성 낮은 증거·사례 문맥
- `art129.contract_payment_bribery_or_embezzlement`: 증뢰·공갈·횡령 구별 또는 구체성 낮은 증거·사례 문맥
- `art129.extortion_provider_not_bribe_giver`: 증뢰·공갈·횡령 구별 또는 구체성 낮은 증거·사례 문맥
- `art129.political_funds_definition`: 증뢰·공갈·횡령 구별 또는 구체성 낮은 증거·사례 문맥
- `art129.voluntary_special_fund_gift`: 증뢰·공갈·횡령 구별 또는 구체성 낮은 증거·사례 문맥
