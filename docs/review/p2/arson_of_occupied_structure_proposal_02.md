# 현주건조물등방화 RuleIR 제안 02

대상 source packet:
`docs/review/p2/arson_of_occupied_structure_cards_02.md` (16–30번)

아래는 패킷의 proposition과 bounded quote만 직접 대조한 초안이다. 주석 전체나 판례 원문을
전수 검토했다는 뜻이 아니며, human approval 전에는 RuleIR에 반영하지 않는다.

## track 어휘 제안

제안 01은 `base / attempt / completed` 세 track만 사용했다. 16–52번에는 제164조 제2항
치사상과 예비가 포함되므로 아래 track을 추가한다.

| track | 의미 |
|---|---|
| `base` | 제164조 제1항 기본 구성요건 |
| `attempt` | 실행 착수·미수 |
| `completed` | 기수 및 죄수 |
| `aggravated_result` | 제164조 제2항 치사상 결과적 가중 |
| `preparation` | 예비. 제175조는 현재 51조문 범위 밖이므로 `predicate_ir_missing`으로 보고만 한다 |

## 초안

| # | decision | role | component / join | track | refers_to | 이유 |
|---:|---|---|---|---|---|---|
| 16 | approve | component | residence_or_presence / alternative_any | base | - | 일체를 이루는 건물의 일부 주거·일부 현존을 전체로 확장하는 판단 경로 |
| 17 | approve | component | attempt_commencement / alternative_any | attempt | - | 매개물 연소 지속 가능 상태를 착수로 보는 규칙. #13과 같은 component에 provenance만 추가 |
| 18 | split | bar + boundary | attempt_commencement / not_applicable | attempt → preparation | - | 앞부분은 점화 전 착수 부정(bar), 뒷부분은 제175조 예비로의 경계 이동(boundary) |
| 19 | approve | component | arson_conduct / alternative_any | base | - | 기발 화력 방치라는 부작위 실행행위 경로 |
| 20 | approve | component | person_scope / mandatory_all | base | - | 주거·현존의 '사람'에서 범인과 공범을 제외하는 요건 한정 |
| 21 | approve | component | presence / mandatory_all | base | - | 방화 당시 범인 외의 자가 내부에 사실상 존재. 권원·이유 불문 |
| 22 | rewrite | component | protected_object_class / alternative_any | base | - | 열거 객체 선택지만 남기고 주거·현존 요건은 #29 component로 위임해 중복 제거 |
| 23 | approve | component | residence_use / mandatory_all | base | - | 주거 사용 = 범인 외의 사람의 일상생활 장소 |
| 24 | approve | boundary | residence_use / not_applicable | base | general_structure_arson | 사용 포기 폐가·영업중단 호텔은 주거용 건조물이 아니므로 제164조 배제 |
| 25 | approve | bar | residence_use / not_applicable | base | - | 지속 현존·주거목적 건축·동일인 거주·주민등록의 부존재만으로 주거성을 부정할 수 없다는 차단규칙 |
| 26 | approve | component | residence_use / alternative_any | base | - | 장기부재 가옥·별장·산장·객실도 사용 가능 상태면 주거 사용 경로 |
| 27 | approve | bar | residence_or_presence / not_applicable | base | - | 주거형 객체에서 방화 당시 현존 부존재를 이유로 배제할 수 없다는 차단규칙 |
| 28 | approve | boundary | person_scope / not_applicable | base | general_structure_arson | 범인 단독거주 가옥은 제164조가 아니라 일반건조물방화. #4의 공범 사안과 같은 경계 |
| 29 | approve | component | residence_or_presence / alternative_any | base | - | 행위 당시 주거 사용 또는 현존이라는 상위 택일 요건. #21·#23·#26이 그 하위 경로 |
| 30 | context_only | context_only | - | - | - | 형법 제10조 제2항 심신미약은 총칙 영역이고 현재 51조문 밖. unit outcome을 바꾸지 않음 |

## 중복 카드 처리 방침

같은 법리를 담은 카드가 여러 장인 경우 카드를 버리지 않고 **동일 `component_id`에 묶어
provenance를 복수로 유지**한다. 지금 확인된 묶음은 두 개다.

- `attempt_commencement`: #13, #17
- `residence_use`: #23(정의), #26(확장), #25(차단)

## Human decision H-A02

1. 위 16–29번 초안을 일괄 승인하는가? 수정 번호만 적어도 된다.
2. `aggravated_result`와 `preparation` track 추가를 승인하는가?
3. #18을 bar(착수 부정)와 boundary(예비 이관)로 쪼개고, 예비는 제175조 자산이 없으므로
   `predicate_ir_missing`으로 보고만 하는 안을 승인하는가?
4. #22를 객체 열거 전용 component로 축소하고 주거·현존 요건을 #29로 위임하는 안을 승인하는가?
5. #30 심신미약 판례를 `context_only`로 두는 것에 동의하는가? 총칙 unit이 생기면 그때 이관한다.
6. 중복 카드를 삭제하지 않고 같은 `component_id`의 복수 provenance로 유지하는 방침을 승인하는가?
