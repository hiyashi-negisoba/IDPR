# 현주건조물등방화 RuleIR 제안 04

대상 source packet:
`docs/review/p2/arson_of_occupied_structure_cards_04.md` (46–52번)

46–47번은 unit_core 카드이고, 48–52번은 결정 C에서 이미 선택된 `doctrine_overlay` 카드다.
overlay 카드는 학설 선택을 재질문하지 않으며, 이 unit에서의 role·join·track만 판단한다.

track 어휘는 제안 02의 `base / attempt / completed / aggravated_result / preparation`을 따른다.

## 초안

| # | decision | role | component / join | track | refers_to | 이유 |
|---:|---|---|---|---|---|---|
| 46 | context_only | context_only | - | aggravated_result | homicide | 존속살해와 방화치사의 상상적 경합 학설. 결정 C #15에서 법조경합 판례(#52)가 선택되어 반대 입장으로 보존 |
| 47 | approve | post_outcome | concurrence / not_applicable | aggravated_result | robbery | 강취 후 살해 목적 방화 사안에서 강도살인죄와 방화치사죄의 상상적 경합 |
| 48 | approve_inherited_policy | component | residence_use / alternative_any | base | - | 결정 C #2 선택. 거주자 전원 살해 직후에도 그 가옥의 주거성을 인정하는 경로 |
| 49 | approve_inherited_policy | component | independent_combustion / mandatory_all | completed | - | 결정 C #3 선택인 독립연소설 본문. #15와 같은 component에 provenance로 합류 |
| 50 | approve_inherited_policy | component | aggravated_result_basis / alternative_any | aggravated_result | - | 결정 C #4 선택. 제164조 제1항의 미수범도 치사상죄 주체가 되는 택일 경로 |
| 51 | approve_inherited_policy | post_outcome | concurrence_with_homicide / not_applicable | aggravated_result | homicide | 결정 C #5 선택인 긍정설. 살인죄와 현주건조물방화치사죄의 상상적 경합 |
| 52 | approve_inherited_policy | post_outcome | specialty_absorption / not_applicable | aggravated_result | homicide | 결정 C #15 선택. 존속살해죄는 법조경합으로 흡수되어 별도 성립하지 않음 |

## 남아 있는 긴장

#51과 #52는 둘 다 선택된 카드인데 방향이 반대로 보인다. 다만 적용 국면이 다르다.

- #51은 **보통살인**과의 관계에서 상상적 경합을 인정한다.
- #52는 **존속살해**와의 관계에서 법정형 비교를 근거로 법조경합·흡수를 인정한다.

초안은 이 둘을 충돌이 아니라 `victim_is_lineal_ascendant` 조건으로 갈리는 별개 규칙으로 본다.
이 해석이 선생님의 원래 취지와 다르면 알려주면 된다.

## 범위 밖 참조

#47의 `robbery`는 재산죄 registry의 강도 unit을 가리킨다. 강도살인 조문이 현재 51조문 범위와
compiled SCL에 실제로 들어 있는지 확인되기 전에는 `predicate_ir_missing`으로 보고한다.
#46·#51·#52가 가리키는 `homicide`는 P2 25개 unit에 선언되어 있으나 아직 RuleIR이 없다.

## Human decision H-A04

1. 위 46–52번 초안을 일괄 승인하는가? 수정 번호만 적어도 된다.
2. #51과 #52를 충돌이 아니라 피해자가 직계존속인지에 따라 갈리는 별개 규칙으로 보는 해석을 승인하는가?
3. #46을 `context_only`로 보존하고 결정 C #15의 법조경합 판례(#52)를 결론으로 삼는 것을 확정하는가?
4. #47의 강도살인 연결을 지금 `robbery` unit으로 선언해두고 미해결이면 `predicate_ir_missing`으로
   보고하는 안을 승인하는가?
