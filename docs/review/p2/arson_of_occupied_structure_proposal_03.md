# 현주건조물등방화 RuleIR 제안 03

대상 source packet:
`docs/review/p2/arson_of_occupied_structure_cards_03.md` (31–45번)

아래는 패킷의 proposition과 bounded quote만 직접 대조한 초안이다. 주석 전체나 판례 원문을
전수 검토했다는 뜻이 아니며, human approval 전에는 RuleIR에 반영하지 않는다.

track 어휘는 제안 02에서 제시한 `base / attempt / completed / aggravated_result / preparation`을 따른다.

## 초안

| # | decision | role | component / join | track | refers_to | 이유 |
|---:|---|---|---|---|---|---|
| 31 | approve | post_outcome | offense_count / not_applicable | completed | - | 1개 방화행위로 수개 현주건조물을 태우면 1죄 |
| 32 | approve | post_outcome | offense_count / not_applicable | completed | - | 수개 방화행위·수개 목적물은 원칙적 경합범. 예외는 이 카드 범위 밖 |
| 33 | approve | post_outcome | offense_count / not_applicable | completed | - | 같은 구역·동일 기회 순차 방화는 1죄 |
| 34 | approve | post_outcome | act_unity / not_applicable | completed | - | 동일 목적물 순차 점화의 행위 단일성 판단. #31·#33의 입력이 됨 |
| 35 | approve | post_outcome | offense_count_standard / mandatory_all | completed | - | 죄수 기준 자체(행위 단일성 + 공공의 안전, 피해물건 수는 부수적) |
| 36 | approve | component | aggravated_result_basis / mandatory_all | aggravated_result | - | 제164조 제1항 방화 + 상해·사망 결과라는 기본 구성요건 |
| 37 | approve | component | result_foreseeability / mandatory_all | aggravated_result | - | 거주자 사상에 대한 예견가능성 요건 |
| 38 | context_only | context_only | - | aggravated_result | homicide | 살인죄와의 상상적 경합을 부정하는 판례 입장. 결정 C #5에서 긍정설(#51)이 이미 선택되어 반대 입장으로 보존 |
| 39 | approve | component | result_causation / alternative_any | aggravated_result | - | 소사·질식·압사·추락·쇼크사 등 인과관계 인정 경로 |
| 40 | approve | component | person_scope / mandatory_all | aggravated_result | - | 치사상 객체 '사람'에서 범인·공범 제외. #20과 같은 요건 한정을 치사상 track에 적용 |
| 41 | approve | bar | result_foreseeability / not_applicable | aggravated_result | - | 전혀 예상할 수 없고 일반인에게 이례적인 진화 중 화상은 예견가능한 결과가 아님 |
| 42 | approve | post_outcome | concurrence / not_applicable | aggravated_result | - | 1행위 수인 사상 시 각 치사·치상죄의 상상적 경합 |
| 43 | approve | post_outcome | concurrence / not_applicable | completed | homicide | 살해 고의로 방화했으나 사망하지 않은 경우 방화죄와 살인미수의 상상적 경합 |
| 44 | approve | component | result_foreseeability_per_participant / mandatory_all | aggravated_result | - | 집단원별 예견가능성. 일부의 고의 살상만으로 다른 집단원 책임을 자동 확정하지 않음 |
| 45 | approve | component | result_foreseeability_per_participant / mandatory_all | aggravated_result | - | 교사·방조범도 기본범죄 관여 외에 중한 결과 예견가능성 필요 |

## 확인된 충돌

#38(판례: 방화치사죄만 의율)은 결정 C #5에서 선택된 #51(긍정설: 살인죄와 상상적 경합)과
정면으로 어긋난다. 학설 선택을 다시 묻는 것이 아니라, **이미 선택된 학설이 이 판례 카드보다
우선하는지**만 확정하면 된다. 초안은 선택값 우선을 전제로 #38을 `context_only`로 두었다.

## Human decision H-A03

1. 위 31–45번 초안을 일괄 승인하는가? 수정 번호만 적어도 된다.
2. #38을 `context_only`로 보존하고 결정 C #5의 긍정설(#51)을 unit 결론으로 삼는 것을 확정하는가?
   반대로 판례를 우선하려면 결정 C #5를 개정해야 하므로 그 뜻을 밝혀주면 원장부터 고친다.
3. #44·#45는 공범·교사·방조라는 총칙 법리다. art164 카드로 존재하므로 일단 unit 안에 두었는데,
   장차 총칙 공범 module로 이관할 대상으로 표시해둘까?
4. #34를 죄수 결론이 아니라 행위 단일성 판단으로 따로 두는 구조(`act_unity`)를 승인하는가?
