# 상해 RuleIR 제안 02 — 고의·인과관계·위법성 (29–52번)

track 어휘는 제안 01을 따른다.

## 초안

| # | decision | role | component / join | track | refers_to | 이유 |
|---:|---|---|---|---|---|---|
| 29 | rewrite | component | intent / alternative_any | base | - | 추측 어미 제거. 결과 발생을 감수·용인하고 폭행에 나아간 미필적 고의 경로 |
| 30 | approve | component | attempt_result / mandatory_all | attempt | - | 상해 고의로 폭행 결과에 그친 경우 상해미수 |
| 31 | approve | component | intent / mandatory_all | base | - | 생리적 기능을 해한다는 인식·인용. 미필적 고의로 충분 |
| 32 | approve | component | intent / mandatory_all | base | - | 주관적 구성요건으로서 상해 고의. #31과 같은 요건의 provenance |
| 33 | approve | boundary | intent / not_applicable | base | assault_resulting_injury | 상해 고의 없이 폭행 고의만 있으면 폭행치상으로 경계 이동 |
| 34 | approve | bar | intent / not_applicable | base | - | 객체·방법의 착오는 고의를 조각하지 않는다는 차단규칙 |
| 35 | approve | bar | intent / not_applicable | base | - | 목적한 사람이 아니어도 고의가 인정된다는 차단규칙. #34와 같은 규칙 |
| 36 | approve | component | causation / mandatory_all | base | - | 합법칙적 조건관계와 객관적 귀속 |
| 37 | approve | component | causation / mandatory_all | base | - | 고의행위로 인한 인과관계 있는 상해 결과 |
| 38 | rewrite | bar | causation / not_applicable | base | - | 메타 래퍼 제거. 힘의 차이로 보아 특별한 사정 없으면 인과관계 부정 |
| 39 | approve | bar | justification / not_applicable | base | - | 새로운 적극적 공격이 아닌 방어적 유형력은 위법성 조각 |
| 40 | context_only | context_only | - | base | - | 징계가 상해에 이르면 조각되지 않는다는 한계. 아래 미결 논점 참조 |
| 41 | context_only | context_only | - | base | - | 부정확·불충분한 설명에 기한 승낙은 무효라는 한계 |
| 42 | context_only | context_only | - | base | - | 훈육권·징계권 범위를 넘은 감금·구타는 위법하다는 한계 |
| 43 | approve | bar | justification / not_applicable | base | - | 군 질서 유지 목적의 경미한 유형력은 사회상규에 위배되지 않음 |
| 44 | context_only | context_only | - | base | - | 권한 없는 얼차려 지시는 정당행위가 아니라는 한계 |
| 45 | context_only | context_only | - | base | - | 싸움에 의한 상호 상해는 조각되지 않는다는 한계 |
| 46 | approve | bar | justification / not_applicable | base | - | 방법·정도가 사회상규에 벗어나지 않는 체벌은 정당행위 |
| 47 | context_only | context_only | - | base | - | 체벌이 상해에 이르면 위법하다는 한계 |
| 48 | approve | bar | justification / not_applicable | base | - | 친권자 체벌이 불가피하고 극히 제한된 범위인 경우 |
| 49 | approve | bar | justification / not_applicable | base | - | 운전 위험을 감수한 동승은 과실상해에 대한 승낙 |
| 50 | context_only | context_only | - | base | - | 교육상 불가피성과 객관적 타당성을 모두 갖춘 경우에만 허용된다는 한계 |
| 51 | approve | bar | object_scope / not_applicable | base | - | 자상은 구성요건에 해당하지 않으므로 방조·교사도 불벌 |
| 52 | approve | bar | justification / not_applicable | base | - | 규칙을 지킨 운동경기에 수반된 상해는 승낙에 의한 조각 |

## 결정 — 한계 카드 7장은 `context_only`로 확정 (2026-08-03 승인)

역할 어휘를 늘리지 않고 손실을 감수하기로 했다. 아래는 그 결정의 근거 기록이다.

위법성 카드 14장은 성격이 두 가지로 갈린다.

- **조각 사유** (#39·#43·#46·#48·#49·#52): 충족되면 성립을 배제한다. `bar`로 깔끔하게 들어간다.
- **조각의 한계** (#40·#41·#42·#44·#45·#47·#50): "이 경우에는 조각되지 않는다"는 규칙이다.
  성립을 막지도 않고 요건을 충족시키지도 않는다. **다른 카드의 평가를 한정할 뿐이다.**

현재 역할 어휘 `component / bar / boundary / waiver / post_outcome / context_only`에는 이
자리가 없다. 초안은 손실을 감수하고 7장을 `context_only`로 두었지만, 그러면 "징계로 상해에
이르면 조각 안 된다" 같은 실체 법리가 RuleIR 밖으로 나간다. 좋은 결과가 아니다.

`qualifier` 역할을 추가하는 안도 검토했으나 채택하지 않았다. 역할 어휘가 늘어날수록 조립기와
검수 계약이 함께 복잡해지고, 이 트랙이 벗어나려는 오버엔지니어링으로 되돌아간다. 7장은
`context_only`로 두되 카드 자체는 폐기하지 않으므로, 나중에 필요하면 같은 자리에서 복구할 수 있다.

다만 손실은 명확히 기록한다: 징계·승낙·정당행위의 **한계**를 정하는 법리가 RuleIR 밖에 있으므로,
이 unit의 위법성 판단은 조각 사유 인정에만 근거하고 그 한계는 심볼릭 계층이 검사하지 않는다.

## Human decision H-B02 — 전부 승인 (2026-08-03)

- [x] 29–52번 초안 승인
- [x] 한계 카드 7장(#40·#41·#42·#44·#45·#47·#50)은 `context_only`로 확정. `qualifier` 역할 추가는 기각
- [x] #33의 폭행치상 경계는 보존하되 `predicate_ir_missing`으로 보고
- [x] 위법성 조각은 `bar`. `waiver`는 인적 처벌조각에 남긴다
