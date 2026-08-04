# 현주건조물등방화 RuleIR 제안 04

대상 source packet:
`docs/review/p2/arson_of_occupied_structure_cards_04.md` (46–52번)

46–47번은 unit_core 카드이고, 48–52번은 결정 C에서 이미 선택된 `doctrine_overlay` 카드다.
overlay 카드는 학설 선택을 재질문하지 않으며, 이 unit에서의 role·join·track만 판단한다.

51·52번은 2026-08-03 법률전문가 재정으로 선택이 대체된 카드다. 최초 초안은 결정 C의 원래 선택을
전제로 #38·#46을 `context_only`로 강등했으나, 그 판단이 뒤집혔다.

track 어휘는 제안 02의 `base / attempt / completed / aggravated_result / preparation`을 따른다.

## 초안

| # | decision | role | component / join | track | refers_to | 이유 |
|---:|---|---|---|---|---|---|
| 46 | approve | post_outcome | concurrence_with_homicide / not_applicable | aggravated_result | homicide | 대법원 입장. 존속살해죄는 병과 규정으로 실질적으로 더 중하므로 방화치사죄와 상상적 경합 |
| 47 | approve | post_outcome | concurrence / not_applicable | aggravated_result | robbery | 강취 후 살해 목적 방화 사안에서 강도살인죄와 방화치사죄의 상상적 경합 |
| 48 | approve_inherited_policy | component | residence_use / alternative_any | base | - | 결정 C #2 선택. 거주자 전원 살해 직후에도 그 가옥의 주거성을 인정하는 경로 |
| 49 | approve_inherited_policy | component | independent_combustion / mandatory_all | completed | - | 결정 C #3 선택인 독립연소설 본문. #15와 같은 component에 provenance로 합류 |
| 50 | approve_inherited_policy | component | aggravated_result_basis / alternative_any | aggravated_result | - | 결정 C #4 선택. 제164조 제1항의 미수범도 치사상죄 주체가 되는 택일 경로 |
| 51 | approve_inherited_policy | post_outcome | concurrence_with_homicide / not_applicable | aggravated_result | homicide | 재정 ov_001로 대체된 부정설. 보통살인은 법조경합으로 흡수되어 방화치사죄만 성립. #38과 같은 결론 |
| 52 | approve_inherited_policy | post_outcome | concurrence_with_homicide / not_applicable | aggravated_result | homicide | 재정 ov_002로 대체된 상상적 경합설. 존속살해는 중한 죄로 처단. #46과 같은 결론 |

## 재정 후 정합성

재정 이후 #38·#51과 #46·#52는 서로 충돌하지 않고 하나의 원칙에서 갈라진다.

> 의도한 고의범의 법정형이 발생한 결과적 가중범보다 무겁지 않으면 법조경합이 되어 결과적
> 가중범만 성립하고, 더 무겁거나 병과 등 가중처벌 규정이 있으면 상상적 경합이 되어 중한
> 고의범으로 처단한다.

| 사안 | 고의범 법정형 | 방화치사죄 대비 | 결론 | 카드 |
|---|---|---|---|---|
| 보통살인 목적 방화치사 | 사형·무기 또는 5년 이상 | 무겁지 않음 | 법조경합, 방화치사죄만 | #38, #51 |
| 존속살해 목적 방화치사 | 사형·무기 또는 7년 이상 + 제256조 자격정지 병과 | 실질적으로 중함 | 상상적 경합, 존속살해죄로 처단 | #46, #52 |

이 원칙은 방화 전용이 아니라 결과적 가중범 일반에 적용되므로, art164 unit 안에 가두지 않고
[전문가 재정 원장](../../../data/rulegen/p2/결정C_전문가재정.json)의
`intended_offense_vs_aggravated_result_penalty_comparison`으로 선언해두었다. 다만 법정형 비교를
런타임에서 수행하려면 조문별 법정형 자산이 필요한데 현재 저장소에는 없다. 지금은 사안별 결론
카드로만 컴파일하고, 법정형 테이블 구축은 별도 확장으로 남긴다.

## 범위 밖 참조

#47의 `robbery`는 재산죄 registry의 강도 unit을 가리킨다. 강도살인 조문이 현재 51조문 범위와
compiled SCL에 실제로 들어 있는지 확인되기 전에는 `predicate_ir_missing`으로 보고한다.
#46·#51·#52가 가리키는 `homicide`는 P2 25개 unit에 선언되어 있으나 아직 RuleIR이 없다.

## Human decision H-A04

1. 위 46–52번 초안을 일괄 승인하는가? 수정 번호만 적어도 된다.
2. 법정형 비교 원칙을 결과적 가중범 일반의 공유 module로 선언해두는 것을 승인하는가?
   지금은 사안별 결론 카드로만 컴파일하고 조문별 법정형 자산은 별도 확장으로 남긴다.
3. 재정 두 건은 "대법원 판례"로 기록했으나 사건번호는 아직 확인하지 못했다. 1차 판례 색인에서
   대조할 사건번호를 알려줄 수 있는가? 확인 전까지 원장에는 미확인으로 남긴다.
4. #47의 강도살인 연결을 지금 `robbery` unit으로 선언해두고 미해결이면 `predicate_ir_missing`으로
   보고하는 안을 승인하는가?
