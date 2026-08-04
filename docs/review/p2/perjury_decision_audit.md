# perjury RuleIR 승인 원장 감사

- status: `ready_for_rule_ir`
- approval: `data/rulegen/p2/native_review/perjury_approved_decisions.json`
- approval SHA-256: `ed745a533c8229f655743b002acd273f2d763edb635679f6baaf005bb80d9ee6`
- law snapshot: `kr_criminal_act_effective_2026-08-03`
- queue cards: 36
- components: 13
- context_only 제외: 0
- 미해결 unit 참조: 8

승인된 판정만 RuleIR 입력이 된다. 미해결 참조는 추측하지 않고 `predicate_ir_missing`으로 보고한다.

## 계약 위반

없음.

## 미해결 unit 참조

- `art152_sec1_1.instigation_or_aiding` → `complicity` (predicate_ir_missing)
- `art152_sec1_4.instigation_and_aiding_possible` → `complicity` (predicate_ir_missing)
- `art152_sec1_5.separate_instigation_multiple_persons` → `complicity` (predicate_ir_missing)
- `art152_sec1_6.false_accusation_perjury_concurrence` → `false_accusation` (predicate_ir_missing)
- `art152_sec1_6.malicious_perjury_after_false_accusation` → `false_accusation` (predicate_ir_missing)
- `art152_sec1_6.oath_incompetent_false_testimony_not_evidence_fabrication` → `evidence_destruction` (predicate_ir_missing)
- `art152_sec2_7.special_statute_malicious_perjury_exclusion` → `special_malicious_perjury` (predicate_ir_missing)
- `art152_sec1_6.perjury_evidence_destruction_special_relation` → `evidence_destruction` (predicate_ir_missing)

## component 구성

| track | component | role | join | 카드 수 | 참조 |
|---|---|---|---|---:|---|
| `base` | `completion` | bar, component | alternative_any | 5 | - |
| `base` | `complicity` | post_outcome |  | 3 | complicity |
| `base` | `evidence_destruction` | post_outcome |  | 2 | evidence_destruction |
| `base` | `false_accusation_concurrence` | post_outcome |  | 2 | false_accusation |
| `base` | `false_factual_statement` | component | alternative_any | 2 | - |
| `base` | `intent` | component | mandatory_all | 1 | - |
| `base` | `lawful_oath` | bar, component | alternative_any | 7 | - |
| `base` | `offense_count` | post_outcome |  | 4 | - |
| `base` | `timely_correction` | waiver |  | 2 | - |
| `base` | `witness_status` | component | alternative_any | 2 | - |
| `malicious` | `malicious_purpose` | component | alternative_any | 3 | - |
| `malicious` | `pending_criminal_or_disciplinary_proceeding` | bar, component | mandatory_all | 2 | - |
| `malicious` | `special_statute` | post_outcome |  | 1 | special_malicious_perjury |

## RuleIR에서 제외된 카드

없음.
