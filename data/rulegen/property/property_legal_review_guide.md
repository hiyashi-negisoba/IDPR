# KCL 커버 재산죄 NormCard 벌크 검토 가이드

생성: 로컬 전용(`api_calls: 0`) · 대상: KCL 61문항이 커버하는 재산죄 17조문 · 라우팅 근거: 사용자 지시 3.1~3.5 (세션 a9e15d21, 2026-07-21)

## 이 검토가 무엇인가

KCL 61문항이 커버하는 재산죄 17조문에서 NormCard **1112장**과 critic 지적 **472건**이 나왔다. 지시하신 3.1~3.5 라우팅으로 **자동 187건 / 에이전트 수정 180건**을 걷어내고, **사람이 볼 것 452건**만 남겼다.

> 주의: 큐는 카드 목록이 아니라 **결정점 목록**이다. 지적이 없는 카드도 실행 core면 `property_core_card_review.json`에 전수 노출된다(원칙 14).

## 자동 처리분 (사용자 확인 불요, 원장에 기록)

| 항목 | 건수 | 근거 |
|---|---:|---|
| 3.2 authority 라벨 정규화 | 97 | 이번 배치 포렌식: `rules/`·`rule_ir.schema` 0 hit → 결론 무관 |
| **소계** | **187** | `property_auto_decisions_ledger.json` |

## 사용자가 볼 것 (우선순위 순)

| 유형 | 건수 | 무엇을 하나 |
|---|---:|---|
| `3.3_overgeneralization` 출처 범위 초과 판정 | 38 | 지시: "이건 사람검토 필요" |
| `3.1_variant_finding` 학설대립 지적 | 51 | 판례 방향 확인 후 실무규칙 확정 |
| `3.1_variant_group` 경쟁견해 그룹 | 67 | 판시사항 보고 그룹당 1회 선택 → 그룹 카드 일괄 정리 |
| `3.2_authority_upgrade` 판례 인덱스 대조 | 21 | 출처가 실제 판례 인용 → 자동 상향 금지, 사람 대조 |
| `3.4_negative_query` 긍정형 질의문 승인 | 190 | 초안 190건 작성완료 → confirm/수정만. 47건은 질의 불요 |
| **합계** | **452** | |

#### 3.1 경쟁견해 202건 — 판례증거 tier (이 순서로 보면 빠름)

| tier | 건수 | 의미 |
|---|---:|---|
| `판례후보_조문일치_비공유` | 0 | 참조조문이 해당 조문 + 경쟁카드와 비공유 → 방향 특정 가능성 최상 |
| `판례후보_조문일치_공유` | 0 | 참조조문 일치하나 경쟁카드가 같은 판례를 공유 → 판시사항으로 가려야 함 |
| `판례후보_조문불일치` | 0 | 인용은 있으나 참조조문이 다름 → 약한 근거 |
| `판례없음_context_only_강등후보` | 0 | 대법원 판례 근거 없음 → 강등 검토 |

각 항목에 `precedent_evidence`로 **참조조문·판시사항**을 붙여 두었다. 판시사항이 그 명제를 지지하면 실무규칙 확정, 아니면 `context_only` 강등이다. 판례가 그 명제를 지지하는지는 법률 판단이라 자동 확정하지 않았다.

### 전문가 동작

각 항목은 `human_review.{decision, notes}` 슬롯을 가진다. **confirm / override + notes**가 기본 동작이고 백지 검토가 아니다. `3.4`는 `approved_query`에 긍정형 질의문을 확정한다.

- 이중부정 카드 **41장**을 먼저 본다(문장구조 난이도 최상, A6 실측).

#### 3.4 질의문 초안 상태

`property_negative_query_drafts.json`에 **에이전트가 직접 작성한 초안 190건**이 들어 있다. 규칙기반 변환은 비문을 만들어 폐기했다. 부정이 조건절에 있는지 귀결절에 있는지에 따라 `card_status_when_query_satisfied`가 갈리므로(반전 129 / 동행 61) 이 값도 함께 확인해야 한다.

237장 중 47장은 질의 대상이 아니다 — 요건불요형 7(요건 제외 **규칙**), 판례소개형 40(규범 주장이 아닌 **보고문**, `context_only` 재분류 검토).

## 에이전트가 처리할 것 (사용자 시간 대상 아님)

| 유형 | 건수 |
|---|---:|
| entailment_구조성 | 2 |
| formalization_기타 | 15 |
| missing_norm | 101 |
| other | 41 |
| 구조성_source_scope | 8 |
| 구조성_variant | 13 |
| **소계** | **180** |

법률-의미 결정점이 아니라 구조·형식화·출처대조 문제다. 원칙 11에 따라 **API를 쓰지 않고** 로컬로 수정한 뒤 spot-check을 받는다.

## 3.5 golden-case 결론 라벨 (front-load 대상, 아직 차단)

데이터에 gold 결론이 없어 **사용자가 유일한 정답 원천**이다. 다만 시나리오는 RuleIR 확정 후에야 만들 수 있어 현재는 `property_scallop_golden_cases.json`에 빈 슬롯으로 예약해 두었다.

## 산출 파일

- `data/rulegen/property/property_norm_card_review_queue.json` — 사람 큐 (위 5유형)
- `data/rulegen/property/property_core_card_review.json` — 실행 core 전수 노출 (원칙 14)
- `data/rulegen/property/property_auto_decisions_ledger.json` — 자동 확정·정규화 원장
- `data/rulegen/property/property_agent_remediation_queue.json` — 에이전트 수정 대상
- `data/rulegen/property/property_negative_query_drafts.json` — 3.4 긍정형 질의문 초안 (에이전트 작성 190건 + 질의 불요 47건)
- `data/rulegen/property/property_scallop_golden_cases.json` — 3.5 라벨 슬롯 (예약)
- `data/rulegen/property/property_review_summary.json` — 집계
