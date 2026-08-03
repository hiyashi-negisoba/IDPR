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
| 38 | approve | post_outcome | concurrence_with_homicide / not_applicable | aggravated_result | homicide | 대법원 입장. 보통살인죄의 법정형이 방화치사죄보다 무겁지 않아 법조경합으로 흡수되고 상상적 경합이 아님 |
| 39 | approve | component | result_causation / alternative_any | aggravated_result | - | 소사·질식·압사·추락·쇼크사 등 인과관계 인정 경로 |
| 40 | approve | component | person_scope / mandatory_all | aggravated_result | - | 치사상 객체 '사람'에서 범인·공범 제외. #20과 같은 요건 한정을 치사상 track에 적용 |
| 41 | approve | bar | result_foreseeability / not_applicable | aggravated_result | - | 전혀 예상할 수 없고 일반인에게 이례적인 진화 중 화상은 예견가능한 결과가 아님 |
| 42 | approve | post_outcome | concurrence / not_applicable | aggravated_result | - | 1행위 수인 사상 시 각 치사·치상죄의 상상적 경합 |
| 43 | approve | post_outcome | concurrence / not_applicable | completed | homicide | 살해 고의로 방화했으나 사망하지 않은 경우 방화죄와 살인미수의 상상적 경합 |
| 44 | approve | component | result_foreseeability_per_participant / mandatory_all | aggravated_result | - | 집단원별 예견가능성. 일부의 고의 살상만으로 다른 집단원 책임을 자동 확정하지 않음 |
| 45 | approve | component | result_foreseeability_per_participant / mandatory_all | aggravated_result | - | 교사·방조범도 기본범죄 관여 외에 중한 결과 예견가능성 필요 |

## 초안 01의 오류 정정 (2026-08-03 법률전문가 재정)

이 문서의 최초 초안은 #38을 `context_only`로 강등하고 결정 C #5의 긍정설을 우선시켰다.
법률전문가 재정에서 그 판단이 뒤집혔다.

보통살인죄(사형·무기 또는 5년 이상)의 법정형은 현주건조물방화치사죄(사형·무기 또는 7년 이상)보다
무겁지 않다. 따라서 법조경합이 되어 방화치사죄만 성립하고 살인죄는 흡수된다. #38이 대법원 입장을
정확히 담고 있고, 결정 C #5가 선택했던 긍정설은 학설의 시각이었다.

재정 결과 결정 C #5의 선택은
`art164_sec3_6.intentional_fire_death_murder_concurrence_negative`로 대체되었다.
원래 선택은 삭제하지 않고 [전문가 재정 원장](../../../data/rulegen/p2/결정C_전문가재정.json)과
구조화 원장의 `superseded_card_ids`에 보존된다.

## Human decision H-A03

- [x] #44·#45를 지금은 unit 안에 두되 총칙 공범 module 이관 대상으로 표시 — 2026-08-03 승인

남은 질문:

1. 위 31–45번 초안을 일괄 승인하는가? 수정 번호만 적어도 된다.
2. #34를 죄수 결론이 아니라 행위 단일성 판단으로 따로 두는 구조(`act_unity`)를 승인하는가?
