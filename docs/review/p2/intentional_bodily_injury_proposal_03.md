# 상해 RuleIR 제안 03 — 죄수·존속상해·특수상해 (53–70번)

track 어휘는 제안 01을 따른다.

## 초안

| # | decision | role | component / join | track | refers_to | 이유 |
|---:|---|---|---|---|---|---|
| 53 | approve | post_outcome | concurrence / not_applicable | base | - | 상해 고의로 선행한 폭행은 상해죄에 흡수 |
| 54 | approve | post_outcome | offense_count / not_applicable | base | - | 피해자가 다르면 피해자별 별개 상해죄 |
| 55 | approve | post_outcome | concurrence / not_applicable | base | homicide | 상해 후 살인 시 상해는 살인의 수반행위로 법조경합 |
| 56 | approve | post_outcome | offense_count_standard / mandatory_all | base | - | 일신전속적 법익이므로 침해법익 수에 따라 죄가 성립 |
| 57 | approve | post_outcome | offense_count / not_applicable | base | - | 1행위 수인 상해는 상상적 경합 |
| 58 | approve | post_outcome | concurrence / not_applicable | base | - | 동일 시간·장소·피해자에 대한 협박은 상해죄에 흡수 |
| 59 | approve | component | ancestral_relation / mandatory_all | ancestral | - | 자기 또는 배우자의 직계존속이라는 존속상해 요건 |
| 60 | approve | component | ancestral_relation / mandatory_all | ancestral | - | 배우자·직계존속은 법률상 개념. 사실상 관계 불포함 |
| 61 | approve | bar | ancestral_relation / not_applicable | ancestral | - | 등록부 기재만으로는 법률상 친자관계가 생기지 않음 |
| 62 | approve | component | attempt_punishability / mandatory_all | attempt | - | 상해·존속상해는 수단 불문 미수 처벌 |
| 63 | approve | component | special_means / alternative_any | special | - | 위험한 물건 휴대라는 특수상해 수단 |
| 64 | approve | component | special_means / alternative_any | special | - | 단체 또는 다중의 위력이라는 특수상해 수단 |
| 65 | context_only | context_only | - | special | - | 형법 제1조 제2항 경과규정 적용 문제이며 총칙 영역 |
| 66 | context_only | context_only | - | special | - | 같은 경과규정의 적용 결과이며 총칙 영역 |
| 67 | approve | component | attempt_punishability / mandatory_all | attempt | - | 특수상해·특수존속상해 미수 처벌 |
| 68 | context_only | context_only | - | - | - | 상습범 가중은 제264조이며 현재 51조문 밖 |
| 69 | context_only | context_only | - | - | - | 자격정지 병과는 양형 사항이며 성립 결론을 바꾸지 않음 |
| 70 | context_only | context_only | - | - | - | 폭력행위 등 처벌에 관한 법률 누범 가중이며 특별법 영역 |

## 가중 track의 구조

`ancestral`과 `special`은 기본범 위에 얹히는 가중 subtype이다(D3 승인). 두 track 모두 `base`의
component를 그대로 요구하고 각자의 추가 요건만 더한다.

```text
ancestral_established  ← base_elements_satisfied  ∧ ancestral_relation_satisfied
special_established    ← base_elements_satisfied  ∧ special_means_satisfied
```

방화의 track은 서로 배타적인 단계였지만 여기서는 기본 요건을 공유하는 누적 구조다. 조립기가
이 관계를 표현하려면 track이 다른 track의 `elements_satisfied`를 입력으로 받을 수 있어야 한다.
현재 조립기는 track을 독립적으로만 다루므로 확장이 필요하다.

## Human decision H-B03

1. 위 53–64·67번 초안을 일괄 승인하는가?
2. 가중 track이 `base_elements_satisfied`를 상속하는 위 구조를 승인하는가?
3. 제264조 상습범(#68), 자격정지 병과(#69), 폭처법 누범(#70)을 현재 범위 밖으로 두는 데
   동의하는가? 셋 다 성립 여부가 아니라 처단형 문제다.
4. 경과규정 카드 2건(#65·#66)을 총칙 영역으로 보아 제외하는 데 동의하는가?
