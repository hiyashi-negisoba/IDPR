# RuleIR-native 비재산죄 확장 준비도 조사

## 결론

비재산죄는 재산죄 registry/runtime 계약으로 확장할 수 있다. 그러나 P2·총칙·절차법 중
현재 바로 registry에 등록할 수 있는 단위는 없다. P2에 남아 있는 것은 검토된 카드 묶음이고,
죄명별 RuleIR candidate와 compiled SCL은 아니다. 따라서 M1/M2에서 이 영역은 계속
`predicate_ir_missing`이어야 한다.

첫 후보는 **현주건조물등방화 (`art164`, unit `arson`)**다. P2 9개 죄명군 중 유일한
단일 조문 unit이고 47장이라, 107~229장인 나머지 unit보다 역할·variant·runtime 계약을
작게 검증할 수 있다. 다만 이것은 우선순위일 뿐 지원 선언은 아니다.

## 실제 자산 대조

| 영역 | 현재 자산 | RuleIR-native에 부족한 필수 자산 | 판정 |
|---|---|---|---|
| P2 | 9개 죄명군, 1,280 core 카드, level map | unit별 predicate/rule/argument schema, compiled SCL, golden facts·결론 | 미지원 |
| P2 `arson` | 단일 조문 `art164`, 47카드 | 위 3개와 역할 계약 | 첫 pilot 후보 |
| 형법총칙 | 독립 commentary corpus/카드 unit 없음 | 독립 source scope와 각칙 조합 규칙 | 미지원 |
| 절차법 | `cp308_2`, `cp342` RuleIR 요청 6개, topic scope | 실제 norm card set, RuleIR candidate, compiled SCL | 미지원 |

`data/rulegen/p2/p2_full.scl`은 재사용 불가다. 여섯 일반 input
(`actor`, `victim`, `action_committed`, `unlawful_intent`, `causation_established`,
`result_occurred`)로 여섯 죄명군 결론을 내는 데모이며, 다음이 없다.

- `norm_card_id → predicate` 연결과 전량 assessment 계약
- 죄명별 역할 tuple
- `not_established`, `undetermined`, `conflict` 결론 relation
- 실제 golden scenario (파일 상태는 `labels_pending`, scenarios 0개)

## P2 unit의 상대적 크기

| Unit | 조문 수 | 카드 수 | review_required | precedent_position |
|---|---:|---:|---:|---:|
| arson | 1 | 47 | 40 | 6 |
| justice_crimes | 2 | 93 | 58 | 38 |
| dwelling_intrusion | 2 | 107 | 75 | 39 |
| bribery | 3 | 119 | 76 | 60 |
| sexual_crimes | 5 | 150 | 94 | 31 |
| document_crimes | 5 | 171 | 110 | 48 |
| official_duty | 4 | 180 | 135 | 100 |
| bodily_injury | 6 | 184 | 132 | 77 |
| homicide | 3 | 229 | 180 | 120 |

카드 수가 적다고 법리 위험이 사라지는 것은 아니다. `arson`도 40/47장이 사실관계 평가를
필요로 하고, 객체·현주/현존·점화/독립연소·미수·결과적 가중 등 variant가 섞여 있다.
그러므로 첫 pilot의 성공 기준은 ‘방화 전부 지원’이 아니라, 명시한 sub-track의 모든 카드와
unknown/충돌을 빠짐없이 흐르게 하는 것이다.

## 권장 확장 순서

1. `arson` 카드 묶음에서 **한 RuleIR candidate**를 결정론적으로 조립한다. source scope,
   card scope, 모든 commentary predicate, rule, query relation을 property/fraud와 같은
   JSON 계약에 기록한다.
2. 카드 내용에서 필요한 entity/role을 먼저 열거해 `arson_case_roles`를 정의한다. 이 단계 전에는
   actor/victim 같은 P2 데모 tuple을 재사용하지 않는다.
3. `arson_{elements_satisfied,established,not_established,undetermined,conflict}`를 명시하고
   compiled SCL을 만든다. predicate assessment 수는 47과 정확히 같아야 한다.
4. 정상·미완결·unknown·상충·명시적 배제 사례를 사람이 작성해 실제 `scli`로 golden을 실행한다.
5. registry audit와 golden이 모두 통과한 뒤에만 `arson`을 registry enum에 추가한다.

그 다음 후보는 `dwelling_intrusion` 또는 `justice_crimes`가 아니라, arson pilot에서 검증된
역할 schema가 실제로 어느 unit과 공유되는지를 보고 정한다. 넓은 9개 죄명군을 한 번에
등록하는 것은 금지한다.

## 총칙과 절차법의 별도 경계

총칙은 각칙의 `established` 뒤에 덧붙이는 generic fallback이 아니다. 미수·공범·위법성
조각 등은 독립 source scope와 조합 relation을 가진 shared RuleIR module로 만들어야 한다.
P2 카드 안에 산재한 정당방위나 공범 관련 문장을 총칙 module으로 승격시키지 않는다.

절차법도 결론 형태가 유무죄와 다르다. 예를 들어 증거/절차 unit은 `admissible`,
`excluded`, `undetermined`, `conflict`처럼 해당 쟁점에 맞는 query contract를 별도로 정해야
한다. 현재는 요청 파일과 bootstrap `hearsay.scl` 초안만 있으므로, 이를 native runtime의
입력으로 연결하지 않는다.
