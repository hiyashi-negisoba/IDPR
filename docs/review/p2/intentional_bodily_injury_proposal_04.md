# 상해 RuleIR 제안 04 — 상해치사·동시범 특례·계승 카드 (71–104번)

track 어휘는 제안 01을 따른다. 101–104번은 결정 C에서 이미 선택된 `doctrine_overlay` 카드로,
학설 선택은 재질문하지 않고 이 unit에서의 role·join·track만 판단한다.

## 초안 — 상해치사 (71–84번)

| # | decision | role | component / join | track | refers_to | 이유 |
|---:|---|---|---|---|---|---|
| 71 | approve | component | death_result / mandatory_all | aggravated_result | - | 상해하여 사망에 이르게 한 기본 구성요건 |
| 72 | approve | component | result_foreseeability / mandatory_all | aggravated_result | - | 인과관계와 사망 결과에 대한 예견가능성 |
| 73 | approve | boundary | death_intent / not_applicable | aggravated_result | homicide | 사망에 고의가 있으면 상해치사가 아니라 살인죄 |
| 74 | approve | boundary | injury_intent / not_applicable | aggravated_result | assault_resulting_death | 폭행 고의뿐이면 폭행치사, 고의 없으면 과실치사로 경계 이동 |
| 75 | approve | component | death_result / mandatory_all | aggravated_result | - | 상해에 고의, 사망에 고의 없는 결과적 가중범 구조 |
| 76 | rewrite | component | result_causation / alternative_any | aggravated_result | - | 메타 래퍼 제거. 도주 중 교통사고, 수술 지연이 공동원인인 경우 |
| 77 | approve | component | result_causation / alternative_any | aggravated_result | - | 간접 원인이 결합한 경우의 인과관계 |
| 78 | approve | component | result_causation / alternative_any | aggravated_result | - | 통상 예견 가능한 개입행위 또는 직접적·유력한 원인 |
| 79 | approve | component | result_causation / alternative_any | aggravated_result | - | 지병·합병증·불충분한 치료가 개입한 경우 |
| 80 | approve | bar | result_causation / not_applicable | aggravated_result | - | 상해 종료 후 피해자 부주의가 원인이면 상당인과관계 부정 |
| 81 | rewrite | component | result_foreseeability / alternative_any | aggravated_result | - | 메타 래퍼 제거. 중요 부위에 대한 강한 타격의 예견가능성 |
| 82 | approve | boundary | death_intent / not_applicable | aggravated_result | homicide | 공동정범 중 1인의 살인 고의는 나머지에게 귀속되지 않음 |
| 83 | approve | post_outcome | offense_count / not_applicable | aggravated_result | - | 상해치사죄와 상해죄의 경합범 |
| 84 | approve | boundary | death_result / not_applicable | aggravated_result | robbery | 강도 중 상해로 사망 시 강도치사죄만 성립 |

## 초안 — 동시범 특례 (85–100번)

| # | decision | role | component / join | track | refers_to | 이유 |
|---:|---|---|---|---|---|---|
| 85 | approve | bar | special_provision_scope / not_applicable | concurrent_offenders | - | 강간치상·강도치상·체포감금치상·방화치상·낙태치상에는 특례 적용 불가 |
| 86 | approve | bar | unidentified_cause / not_applicable | concurrent_offenders | - | 원인행위가 판명되거나 특정인의 폭행이 아님이 증명되면 적용 없음 |
| 87 | approve | bar | unidentified_cause / not_applicable | concurrent_offenders | - | 개별 인과관계 부존재 입증으로 책임에서 벗어남 |
| 88 | context_only | context_only | - | concurrent_offenders | - | 특례가 수정하는 개인책임 원칙의 배경 서술 |
| 89 | approve | component | simultaneous_offenders / mandatory_all | concurrent_offenders | - | 의사연락 없이 동일 객체에 개별적·동시에 범한 동시범 |
| 90 | approve | component | unidentified_cause / mandatory_all | concurrent_offenders | - | 상해 원인행위가 판명되지 않아야 한다는 요건 |
| 91 | approve | component | special_effect / mandatory_all | concurrent_offenders | - | 미수범이 아니라 공동정범의 예로 처벌하는 특례 효과 |
| 92 | approve | bar | simultaneous_offenders / not_applicable | concurrent_offenders | - | 의사연락이 있어 공동정범이면 적용 문제 자체가 없음 |
| 93 | approve | component | simultaneous_offenders / mandatory_all | concurrent_offenders | - | 독립행위의 경합 |
| 94 | approve | bar | simultaneous_offenders / not_applicable | concurrent_offenders | - | 가해행위 사실 자체가 불분명하면 적용 없음 |
| 95 | rewrite | component | simultaneous_offenders / alternative_any | concurrent_offenders | - | 메타 래퍼 제거. 이시의 독립행위 경합에도 적용 |
| 96 | rewrite | component | simultaneous_offenders / alternative_any | concurrent_offenders | - | 메타 래퍼 제거. #95와 같은 규칙의 provenance |
| 97 | approve | component | injury_result_required / mandatory_all | concurrent_offenders | - | 상해 결과 발생 필요. 폭행에 그치면 적용 없음 |
| 98 | approve | post_outcome | resulting_offense / not_applicable | concurrent_offenders | - | 폭행 고의와 상해 고의가 섞이면 각각 폭행치상·상해기수 |
| 99 | rewrite | bar | special_provision_scope / not_applicable | concurrent_offenders | - | 메타 래퍼 제거. 과실치사에는 특례 적용 부정 |
| 100 | approve | post_outcome | resulting_offense / not_applicable | concurrent_offenders | - | 경합행위가 상해면 상해기수, 폭행이면 폭행치상 |

## 초안 — 계승 카드 (101–104번)

| # | decision | role | component / join | track | 결정 C | 이유 |
|---:|---|---|---|---|---|---|
| 101 | approve_inherited_policy | bar | object_scope / not_applicable | base | #21 | 태아 상태 침해는 침해 당시 객체가 사람이 아니므로 상해죄 부정 |
| 102 | approve_inherited_policy | bar | injury_concept / not_applicable | base | #22 | 임신은 생리적 기능 장애가 아니므로 상해 아님 |
| 103 | approve_inherited_policy | component | injury_conduct / alternative_any | base | #23 | 약물 투여는 무형적 방법에 의한 상해 |
| 104 | approve_inherited_policy | post_outcome | offense_count / not_applicable | aggravated_result | #24 | 사망 오인 후 위장 추락까지 포괄하여 단일 상해치사죄 |

## 범위 밖 참조

`homicide`는 P2 25개 unit에 선언되어 있으나 아직 RuleIR이 없다. `robbery`는 재산죄 registry에
등록되어 있으나 강도치사 조문 포함 여부는 미확인이다. `assault_resulting_injury`(폭행치상)와
`assault_resulting_death`(폭행치사)는 제262조로 현재 51조문 밖이다. 넷 다 경계는 보존하되
`predicate_ir_missing`으로 보고한다.

## 동시범 특례의 성격

제263조는 성립 요건이 아니라 **원인행위가 판명되지 않을 때의 귀속 특례**다. 상해죄뿐 아니라
폭행치상에도 걸리므로, 장차 친족상도례처럼 공유 module로 분리하는 것이 구조적으로 맞다.
**2026-08-03 결정: 분리가 맞다.** 다만 지금 분리하면 상해 unit 컴파일이 함께 밀리므로,
이번 회차는 이 unit의 `concurrent_offenders` track으로 두고 `shared_module_candidate`로
표시한다. 공유 module 계층을 만들 때 이 track을 통째로 이관한다.

## Human decision H-B04 — 승인 (2026-08-03)

- [x] 71–104번 초안 승인
- [x] 제263조 특례는 분리가 옳다는 판단. 이번 회차는 track으로 두고 이관 대상으로 표시
- [x] #88은 `context_only`
- [x] 제262조 폭행치사상: 별도 unit을 만들지 않는다. 아래 정정 참조

## 제262조 — 결손이 아니라 설계상 범위 밖 (2026-08-03 정정)

처음 이 항목을 "카드가 없어 만들 수 없는 결손"으로 적었다. 그것은 잘못된 프레이밍이었다.

`data/rulebase/card_catalog_v2.json`은 51개 조문에 1,848장을 담고 있고, KCL 루브릭 gold가
요구하는 43개 조문을 **하나도 빠짐없이** 포함한다(`gold - catalog = 공집합`). 오히려 카드 쪽이
제130·263·267·268·328·332·344·366조를 더 갖고 있다.

즉 rulegen 51조문은 임의로 자른 범위가 아니라 **KCL이 요구하는 실체법 전체를 덮도록 구성된
범위**이며, 이미 덮고 있다. 폭행 계열(제260·261·262·264조)은 카드에도, 주석서 파싱 96개
조문에도, 루브릭 gold에도 없다. 빠진 것이 아니라 이 벤치마크가 묻지 않는 영역이다.

따라서 제262조 unit은 만들지 않는다. #33과 #74의 경계는 그대로 보존하되 이 unit의 결론에는
영향을 주지 않는 범위 밖 참조로 보고한다.
