# sexual_offense_injury_or_death RuleIR 승인 원장 감사

- status: `ready_for_rule_ir`
- approval: `data/rulegen/p2/native_review/sexual_offense_injury_or_death_approved_decisions.json`
- approval SHA-256: `3e41085aaad48a770a823af4a950bbb02f68684e46e40a5a8d0a0b5530740b37`
- law snapshot: `kr_criminal_act_effective_2026-08-03`
- queue cards: 34
- components: 11
- context_only 제외: 3
- 미해결 unit 참조: 3

승인된 판정만 RuleIR 입력이 된다. 미해결 참조는 추측하지 않고 `predicate_ir_missing`으로 보고한다.

## 계약 위반

없음.

## 미해결 unit 참조

- `art301_sec6.intentional_injury_conspirator_intent` → `complicity` (predicate_ir_missing)
- `art301_sec6.pre_execution_withdrawal` → `complicity` (predicate_ir_missing)
- `art301_sec7.special_rape_injury_completed` → `special_sexual_offense_injury` (predicate_ir_missing)

## component 구성

| track | component | role | join | 카드 수 | 참조 |
|---|---|---|---|---:|---|
| `common` | `attempt_scope` | post_outcome |  | 1 | sexual_offense_attempt |
| `common` | `complicity` | post_outcome |  | 2 | complicity |
| `common` | `concurrence` | post_outcome |  | 2 | - |
| `common` | `injury` | bar, component | alternative_any | 9 | - |
| `common` | `injury_nexus` | bar, component | alternative_any | 7 | - |
| `common` | `object_scope` | component | mandatory_all | 1 | - |
| `common` | `predicate_offense` | component | alternative_any | 2 | - |
| `common` | `special_statute` | post_outcome |  | 1 | special_sexual_offense_injury |
| `death` | `death_result` | component | mandatory_all | 1 | - |
| `intentional_injury` | `injury_intent` | component | mandatory_all | 1 | - |
| `result_aggravated_injury` | `result_responsibility` | component | alternative_any | 4 | - |

## RuleIR에서 제외된 카드

- `art301_sec4_2.delayed_diagnosis_case`: 파기환송 사례, 진단서 증명력 또는 미성년 피해자 경향은 독립 단위사실이 아닌 증거평가 문맥
- `art301_sec4_2.injury_diagnosis_evidence`: 파기환송 사례, 진단서 증명력 또는 미성년 피해자 경향은 독립 단위사실이 아닌 증거평가 문맥
- `art301_sec4_4.minor_broader_injury`: 파기환송 사례, 진단서 증명력 또는 미성년 피해자 경향은 독립 단위사실이 아닌 증거평가 문맥
