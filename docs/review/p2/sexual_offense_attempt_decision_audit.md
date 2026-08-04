# sexual_offense_attempt RuleIR 승인 원장 감사

- status: `ready_for_rule_ir`
- approval: `data/rulegen/p2/native_review/sexual_offense_attempt_approved_decisions.json`
- approval SHA-256: `1e515cd03217926beaa4046473ceef02f8a7fad4492036ff8836eb722b45a1a8`
- law snapshot: `kr_criminal_act_effective_2026-08-03`
- queue cards: 5
- components: 3
- context_only 제외: 0
- 미해결 unit 참조: 2

승인된 판정만 RuleIR 입력이 된다. 미해결 참조는 추측하지 않고 `predicate_ir_missing`으로 보고한다.

## 계약 위반

없음.

## 미해결 unit 참조

- `art300_x_raw_pdf.art305_under_sixteen_attempt_interpretation` → `statutory_sexual_offense` (predicate_ir_missing)
- `art300_x_raw_pdf.pre_amendment_art305_under_thirteen_attempt` → `statutory_sexual_offense` (predicate_ir_missing)

## component 구성

| track | component | role | join | 카드 수 | 참조 |
|---|---|---|---|---:|---|
| `attempt` | `child_victim_extension` | post_outcome |  | 2 | statutory_sexual_offense |
| `attempt` | `commencement` | component | mandatory_all | 1 | - |
| `attempt` | `eligible_predicate_offense` | bar, component | mandatory_all | 2 | sexual_offense_injury_or_death |

## RuleIR에서 제외된 카드

없음.
