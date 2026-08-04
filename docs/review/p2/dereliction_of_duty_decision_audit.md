# dereliction_of_duty RuleIR 승인 원장 감사

- status: `ready_for_rule_ir`
- approval: `data/rulegen/p2/native_review/dereliction_of_duty_approved_decisions.json`
- approval SHA-256: `46fda05f934e9fc5551db1e0828f46442a8a3f75aca7ae6f72cc09459b9e09af`
- law snapshot: `kr_criminal_act_effective_2026-08-03`
- queue cards: 49
- components: 11
- context_only 제외: 1
- 미해결 unit 참조: 10

승인된 판정만 RuleIR 입력이 된다. 미해결 참조는 추측하지 않고 `predicate_ir_missing`으로 보고한다.

## 계약 위반

없음.

## 미해결 unit 참조

- `art122_sec2_5.instigation_per_public_official` → `complicity` (predicate_ir_missing)
- `art122_sec3_3.evidence_destruction_absorption` → `evidence_destruction` (predicate_ir_missing)
- `art122_sec3_3.office_abuse_prosecutorial_choice` → `abuse_of_authority` (predicate_ir_missing)
- `art122_sec3_3.office_abuse_two_modes_absorption` → `abuse_of_authority` (predicate_ir_missing)
- `art122_sec3_5.building_instigation_excludes_dereliction` → `special_dereliction_offense` (predicate_ir_missing)
- `art122_sec3_5.dereliction_and_instigation_concurrent_offenses` → `complicity` (predicate_ir_missing)
- `art122_sec3_5.human_rights_order_and_dereliction_imaginary_concurrence` → `special_dereliction_offense` (predicate_ir_missing)
- `art122_sec4.military_dereliction_requirements` → `special_dereliction_offense` (predicate_ir_missing)
- `art122_sec4.military_inadequate_performance_not_sufficient` → `special_dereliction_offense` (predicate_ir_missing)
- `art122_sec4.specific_crimes_act_recognition_threshold` → `special_dereliction_offense` (predicate_ir_missing)

## component 구성

| track | component | role | join | 카드 수 | 참조 |
|---|---|---|---|---:|---|
| `base` | `absorption` | post_outcome |  | 3 | deceptive_obstruction_of_official_duty, evidence_destruction, harboring_offender |
| `base` | `conscious_abandonment` | bar, component | alternative_any | 22 | - |
| `base` | `false_document_concurrence` | post_outcome |  | 2 | false_public_document |
| `base` | `instigation` | post_outcome |  | 2 | complicity |
| `base` | `intent` | component | mandatory_all | 1 | - |
| `base` | `offense_count` | post_outcome |  | 1 | - |
| `base` | `office_abuse` | post_outcome |  | 2 | abuse_of_authority |
| `base` | `public_official_status` | bar, component | alternative_any | 5 | - |
| `base` | `special_statute` | post_outcome |  | 5 | special_dereliction_offense |
| `base` | `specific_original_duty` | bar, component | alternative_any | 4 | - |
| `base` | `substantial_wrongfulness` | component | mandatory_all | 1 | - |

## RuleIR에서 제외된 카드

- `art122_sec3_3.indictment_scope_overlapping_offenses`: 공소범위와 현실적 심판대상에 관한 절차법 문맥
