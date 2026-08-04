# seal_forgery_or_misuse RuleIR 승인 원장 감사

- status: `ready_for_rule_ir`
- approval: `data/rulegen/p2/native_review/seal_forgery_or_misuse_approved_decisions.json`
- approval SHA-256: `2af0f07bea6c6d98ade0a3b3ddcaa28a625bf04c487bc89e80d25ae0483c0e91`
- law snapshot: `kr_criminal_act_effective_2026-08-03`
- queue cards: 19
- components: 5
- context_only 제외: 0
- 미해결 unit 참조: 1

승인된 판정만 RuleIR 입력이 된다. 미해결 참조는 추측하지 않고 `predicate_ir_missing`으로 보고한다.

## 계약 위반

없음.

## 미해결 unit 참조

- `art239_sec1_5.foreign_national_overseas_jurisdiction` → `criminal_procedure` (predicate_ir_missing)

## component 구성

| track | component | role | join | 카드 수 | 참조 |
|---|---|---|---|---:|---|
| `creation_or_misuse` | `false_manifestation` | bar, component | alternative_any | 8 | - |
| `creation_or_misuse` | `intent_and_use_purpose` | bar, component | alternative_any | 5 | - |
| `creation_or_misuse` | `private_person_mark` | component | mandatory_all | 1 | - |
| `creation_or_misuse` | `territorial_jurisdiction` | post_outcome |  | 1 | criminal_procedure |
| `use` | `exposure_or_use` | bar, component | alternative_any | 4 | - |

## RuleIR에서 제외된 카드

없음.
