# 현주건조물등방화 RuleIR 제안 01

대상 source packet:
`docs/review/p2/arson_of_occupied_structure_cards_01.md`

아래는 패킷의 proposition과 bounded quote만 직접 대조한 초안이다. 주석 전체나 판례 원문을
전수 검토했다는 뜻이 아니며, human approval 전에는 RuleIR에 반영하지 않는다.

| # | decision | role | component / join | track | refers_to | 이유 |
|---:|---|---|---|---|---|---|
| 1 | approve | post_outcome | concurrence / not_applicable | completed | property_damage | 방화 성립 뒤 손괴 흡수를 정하는 법조경합 규칙 |
| 2 | context_only | context_only | - | - | - | 보험사기방지특별법은 현재 51조문 RuleIR 범위 밖 |
| 3 | context_only | context_only | - | - | - | 보험사기 실행착수 판단은 현재 범위 밖 |
| 4 | approve | boundary | protected_object / not_applicable | base | general_structure_arson | 비범인 현주·현존이 없는 경우 제164조를 배제하고 일반건조물방화로 경계 이동 |
| 5 | approve | component | arson_conduct / mandatory_all | base | - | 화력으로 목적물 연소에 원인력을 부여하는 실행행위 |
| 6 | approve | component | attempt_commencement / alternative_any | attempt | - | 직접 점화 또는 매개물 도화라는 착수 경로 |
| 7 | approve | component | protected_object_building / mandatory_all | base | - | 건조물 객체의 구조·사용가능성 요건 |
| 8 | approve | component | object_identity / alternative_any | base | - | 복수 외관 건물의 물리적·기능적 일체성 판단 경로 |
| 9 | split | component | burning_and_completion / not_applicable | completed | - | 불태움의 의미와 기수 결론이 한 카드에 결합되어 있고 #15의 기수 기준과 중복 |
| 10 | approve | component | independent_combustion / alternative_any | completed | - | 불꽃 없는 고온 산화·열전달도 독립연소가 되는 판단 경로 |
| 11 | rewrite | boundary | protected_object / not_applicable | base | object_arson | 메타 래퍼를 제거하고 폐가의 구체적 상태가 제164조 건조물에서 배제된다는 규칙으로 한정 |
| 12 | approve | bar | attempt_commencement / not_applicable | attempt | dwelling_intrusion | 방화 목적의 주거침입만으로 방화 착수는 아니며 별도 주거침입 가능 |
| 13 | approve | component | attempt_commencement / alternative_any | attempt | - | 연소 가능한 매개물 점화 후 목적물에 옮겨붙지 않은 미수 경로 |
| 14 | context_only | context_only | - | completed | - | 개별 사체·천정 사례이며 현재 quote만으로 일반 RuleIR 경로를 추가할 필요 없음 |
| 15 | approve_inherited_policy | component | independent_combustion / mandatory_all | completed | - | `결정C_학설선택.md` #3에서 독립연소설을 이미 선택했으므로 completed track의 필수 요건으로 계승 |

## Human decision H-A01

1. 위 1–14번 초안을 일괄 승인하는가? 수정 번호만 적어도 된다.
2. 15번은 기존 결정 C의 독립연소설 선택을 재질문 없이 계승한다. 카드 중복·문언은 RuleIR 편입 시 감사한다.
3. 4번의 `general_structure_arson`과 11번의 `object_arson`은 현재 카드 범위 밖이므로
   boundary를 보존하되 `predicate_ir_missing`으로 보고하는 안을 승인하는가?
