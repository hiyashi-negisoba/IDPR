# relative_property_crime_exception RuleIR 승인 원장 감사

- status: `ready_for_rule_ir`
- approval: `data/rulegen/p2/native_review/relative_property_crime_exception_approved_decisions.json`
- approval SHA-256: `cf24f44f357f5388c05b92f74cfdc5a57155760fb9ac45ec928b9a1040875d06`
- law snapshot: `kr_criminal_act_effective_2026-08-03`
- queue cards: 5
- components: 2
- context_only 제외: 1
- 미해결 unit 참조: 0

승인된 판정만 RuleIR 입력이 된다. 미해결 참조는 추측하지 않고 `predicate_ir_missing`으로 보고한다.

## 계약 위반

없음.

## 미해결 unit 참조

없음.

## component 구성

| track | component | role | join | 카드 수 | 참조 |
|---|---|---|---|---:|---|
| `exception` | `eligible_property_offense` | bar, component | mandatory_all | 2 | robbery, theft |
| `exception` | `kinship_with_owner_and_possessor` | bar, component | mandatory_all | 2 | - |

## RuleIR에서 제외된 카드

- `art344_x_raw_pdf.reported_kinship_classifications`: 개별 촌수 사례 소개로서 친족관계 FactGraph 산정 문맥
