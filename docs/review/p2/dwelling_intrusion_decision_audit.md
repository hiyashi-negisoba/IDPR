# dwelling_intrusion RuleIR 승인 원장 감사

- status: `ready_for_rule_ir`
- approval: `data/rulegen/p2/native_review/dwelling_intrusion_approved_decisions.json`
- approval SHA-256: `27e47478ad35041dddc304a6e36374e8bb2dd00339314bd6a9b64e3e81fd2aef`
- law snapshot: `kr_criminal_act_effective_2026-08-03`
- queue cards: 104
- components: 14
- context_only 제외: 9
- 미해결 unit 참조: 0

승인된 판정만 RuleIR 입력이 된다. 미해결 참조는 추측하지 않고 `predicate_ir_missing`으로 보고한다.

## 계약 위반

없음.

## 미해결 unit 참조

없음.

## component 구성

| track | component | role | join | 카드 수 | 참조 |
|---|---|---|---|---:|---|
| `attempt` | `dangerous_commencement` | bar, component | alternative_any | 5 | - |
| `intrusion` | `bodily_entry` | component | mandatory_all | 1 | - |
| `intrusion` | `continuation_and_count` | post_outcome |  | 7 | - |
| `intrusion` | `entry_authority` | component | mandatory_all | 1 | - |
| `intrusion` | `intent` | component | alternative_any | 3 | - |
| `intrusion` | `intrusive_entry` | bar, component | alternative_any | 29 | - |
| `intrusion` | `justification` | waiver |  | 9 | - |
| `intrusion` | `property_offense_concurrence` | post_outcome |  | 5 | theft |
| `intrusion` | `protected_place_and_peace` | bar, component | alternative_any | 21 | - |
| `refusal_to_leave` | `ability_to_leave` | bar, component | mandatory_all | 3 | - |
| `refusal_to_leave` | `justified_demand` | bar, component | alternative_any | 4 | - |
| `refusal_to_leave` | `lawful_initial_presence_and_place` | component | alternative_any | 3 | - |
| `refusal_to_leave` | `refusal_intent` | component | mandatory_all | 1 | - |
| `refusal_to_leave` | `unjustified_noncompliance` | component | alternative_any | 3 | - |

## RuleIR에서 제외된 카드

- `art319_sec3_1.consent_and_coerced_consent`: 복합 승낙·점유분쟁·정당행위 부정 사례 또는 동기 설명으로 독립 단위사실에서 제외
- `art319_sec3_1.possession_dispute_and_owner_tenant`: 복합 승낙·점유분쟁·정당행위 부정 사례 또는 동기 설명으로 독립 단위사실에서 제외
- `art319_sec5_2.labor_dispute_exclusive_occupation`: 복합 승낙·점유분쟁·정당행위 부정 사례 또는 동기 설명으로 독립 단위사실에서 제외
- `art319_sec5_2.labor_dispute_explicit_denial_entry`: 복합 승낙·점유분쟁·정당행위 부정 사례 또는 동기 설명으로 독립 단위사실에서 제외
- `art319_sec5_2.labor_dispute_plant_occupation`: 복합 승낙·점유분쟁·정당행위 부정 사례 또는 동기 설명으로 독립 단위사실에서 제외
- `art319_sec5_2.right_holder_entry_without_procedure`: 복합 승낙·점유분쟁·정당행위 부정 사례 또는 동기 설명으로 독립 단위사실에서 제외
- `art319_sec5_3.rightless_possessor.peace`: 복합 승낙·점유분쟁·정당행위 부정 사례 또는 동기 설명으로 독립 단위사실에서 제외
- `art319_sec5_3.self_help.right_holder_negative`: 복합 승낙·점유분쟁·정당행위 부정 사례 또는 동기 설명으로 독립 단위사실에서 제외
- `art319_sec7_3.debt_dispute_motive`: 복합 승낙·점유분쟁·정당행위 부정 사례 또는 동기 설명으로 독립 단위사실에서 제외
