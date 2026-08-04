# indecent_assault RuleIR 승인 원장 감사

- status: `ready_for_rule_ir`
- approval: `data/rulegen/p2/native_review/indecent_assault_approved_decisions.json`
- approval SHA-256: `d03536ca88029c0f3ed7981598529496875561fd26f648b6f0a2cb50147faeb0`
- law snapshot: `kr_criminal_act_effective_2026-08-03`
- queue cards: 33
- components: 10
- context_only 제외: 4
- 미해결 unit 참조: 2

승인된 판정만 RuleIR 입력이 된다. 미해결 참조는 추측하지 않고 `predicate_ir_missing`으로 보고한다.

## 계약 위반

없음.

## 미해결 unit 참조

- `art298_sec8.forced_undressing_camera_concurrence` → `illegal_filming` (predicate_ir_missing)
- `art298_sec8.special_forcible_indecency` → `special_indecent_assault` (predicate_ir_missing)

## component 구성

| track | component | role | join | 카드 수 | 참조 |
|---|---|---|---|---:|---|
| `base` | `absorption` | post_outcome |  | 1 | rape |
| `base` | `attempt` | post_outcome |  | 3 | sexual_offense_attempt |
| `base` | `coercive_means` | component | alternative_any | 3 | - |
| `base` | `concurrence` | post_outcome |  | 1 | illegal_filming |
| `base` | `conduct` | component | alternative_any | 4 | - |
| `base` | `indecent_act` | bar, component | alternative_any | 12 | - |
| `base` | `intent` | component | mandatory_all | 1 | - |
| `base` | `object_scope` | component | mandatory_all | 1 | - |
| `base` | `offense_count` | post_outcome |  | 2 | - |
| `base` | `special_offense` | post_outcome |  | 1 | special_indecent_assault |

## RuleIR에서 제외된 카드

- `art298.spousal_victim.precedent_position`: 배우자·주체 일반설명 또는 고의의 증거평가 기준으로서 독립 단위사실 predicate로 실행하지 않음
- `art298.subject.unrestricted`: 배우자·주체 일반설명 또는 고의의 증거평가 기준으로서 독립 단위사실 predicate로 실행하지 않음
- `art298_sec4.disability_intent_assessment`: 배우자·주체 일반설명 또는 고의의 증거평가 기준으로서 독립 단위사실 predicate로 실행하지 않음
- `art298_sec4.intent_inference`: 배우자·주체 일반설명 또는 고의의 증거평가 기준으로서 독립 단위사실 predicate로 실행하지 않음
