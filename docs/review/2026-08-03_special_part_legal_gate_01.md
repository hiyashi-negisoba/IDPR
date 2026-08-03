# 형법각칙 RuleIR-native 법률 검수 게이트 01

상태: `approved`

이 문서는 모델 실행 승인이 아니라 **범위·법령시점·RuleIR 실행 단위**를 확정하기 위한
법률전문가 검수 패킷이다. 승인 전에는 P2 asset을 registry에 등록하지 않는다.

## D1. “완전한 형각”의 범위

현재 저장소가 실제로 가진 것은 다음 세 층이다.

| 층 | 범위 | 현재 상태 |
|---|---|---|
| A | 카드가 있는 51개 조문 | fraud/property RuleIR 일부만 실행 가능 |
| B | A + 루브릭이 요구하지만 카드가 없는 12개 조문 | 원천 주석은 있으나 카드 미생성 |
| C | 형법각칙 주석서 파싱 원천 251개 조문 | inventory·현행성·카드 상태 전수 감사 전 |

과거 `KCL_1730_RULEBASE_SPECIFICATION.md`는 1,730개 **카드**를 1,730개 RuleIR로 표현했지만,
현재 실제 candidate RuleIR/SCL 자산과 일치하지 않는다. 51개 조문을 닫는 것만으로 대한민국
형법각칙 전체가 되지는 않는다.

### 사용자 결정 (2026-08-03)

이번 “완전한 형각”의 범위는 **현재 카드 자산을 보유한 51개 조문(P1+P2)** 으로 확정한다.
원천 주석만 있고 카드가 없는 추가 12개 조문과 251개 조문 전체 확장은 이번 완료 조건에서
제외한다. 다만 조문별 상태는
`covered / card_missing / rule_ir_missing / legal_review_pending / executable`로 계속 공개한다.

- [x] D1 승인 — 보유 카드 기준 51개 조문
- [ ] D1 수정: ____________________

## D2. 법령 시점

2026-08-03 현재 국가법령정보센터에는 형법 법률 제21450호의 2026-03-12 시행본이 현행이고,
2026-09-13 시행 예정 시점도 표시된다. 서로 다른 시행본을 한 SCL에 섞지 않는다.

제안:

1. 첫 snapshot은 `effective_on=2026-08-03`, 적용 법령은 2026-03-12 시행본으로 고정한다.
2. 2026-09-13 시행본은 별도 future snapshot으로 사전 구축하되 현재 사건에 적용하지 않는다.
3. 모든 RuleIR registry unit에 `law_snapshot_id`를 의무화한다.

- [x] D2 승인 — 2026-08-03 사용자 승인
- [ ] D2 수정: ____________________

## D3. 실행 단위 원칙

재산죄에서 승인된 원칙을 형각 전체에 일반화한다.

1. RuleIR unit은 주석 수집용 죄명군이나 조문번호가 아니라 **독립적으로 성립 여부를 질의할
   수 있는 죄명**이다.
2. 기본범과 그 가중형·미수·예비는 기본 요건을 공유할 때 같은 unit의 subtype/단계 relation으로
   둔다.
3. 행위주체와 역할 tuple이 달라지는 별도 죄명은 분리한다.
4. 준용·인적 처벌조각·소추조건은 공유 module로 두고 offense outcome bridge를 입력받는다.
5. 각 unit은 자체 `established / not_established / undetermined / conflict` 의미 mapping을
   registry manifest에 선언한다.

- [x] D3 승인 — 재산죄와 같은 죄명 unit/가중 stratum/shared module 원칙
- [ ] D3 수정: ____________________

## D4. 현재 P2 31개 조문의 실행 단위 분해안

현재 9개 죄명군은 카드 보관 단위로만 유지하고, runtime unit은 아래처럼 분리한다.

| 제안 unit | 조문 | 처리 |
|---|---|---|
| dereliction_of_duty | 122 | 독립 죄명 |
| official_secret_disclosure | 127 | 독립 죄명 |
| bribe_receipt | 129 | 수뢰·사전수뢰 subtype 포함 |
| third_party_bribery | 130 | 제3자 역할 때문에 수뢰와 분리 |
| bribe_giving | 133 | 공여자 역할 때문에 수뢰와 분리 |
| obstruction_of_official_duty | 136 | 독립 죄명 |
| deceptive_obstruction_of_official_duty | 137 | 실행행위가 달라 제136조와 분리 |
| harboring_offender | 151 | 친족 불처벌은 후단 modifier로 보존 |
| perjury | 152 | 모해위증 subtype 포함 |
| arson_of_occupied_structure | 164 | 기본·미수·치사상 subtype 분리 출력 |
| public_document_forgery | 225 | 독립 죄명 |
| false_public_document | 227 | 작성권한 있는 공무원 역할 때문에 제225조와 분리 |
| private_document_forgery | 231 | 독립 죄명 |
| use_of_forged_private_document | 234 | 선행 위조와 별도 성립 가능하므로 분리 |
| seal_forgery_or_misuse | 239 | 독립 죄명 |
| homicide | 250, 254, 255 | 기본·존속·미수·예비/음모 subtype |
| intentional_bodily_injury | 257, 258-2, 259, 263 | 특수·치사·동시범 relation 포함 |
| negligent_bodily_harm | 267, 268 | 과실·업무상/중과실 subtype |
| rape | 297 | 독립 기본범 |
| indecent_assault | 298 | 독립 기본범 |
| quasi_sexual_offense | 299 | 준강간/준강제추행 subtype은 별도 출력 |
| sexual_offense_attempt | 300 | 세 기본범 outcome을 받는 공유 단계 module |
| sexual_offense_injury_or_death | 301 | 세 기본범 outcome과 결과·인과를 받는 공유 결과적 가중 module |
| dwelling_intrusion | 319 | 침입·퇴거불응 subtype |
| relative_property_crime_exception | 328, 344 및 준용조문 | 재산죄 공유 후단 module로 귀속 |

### 명시적 데이터 정정 후보

현 `p2_rule_ir_unit_manifest.json`은 제344조를 `dwelling_intrusion`에 넣었다. 제344조 카드는
P2 주거침입 predicate로 컴파일하지 않고 재산죄의 `relative_property_crime_exception` module로
이관하는 안을 제시한다.

- [x] D4 전체 승인 — 2026-08-03 사용자 승인
- [ ] D4 일부 수정: ____________________

## D5. 재산죄·비재산죄 연결 계약

unit별 역할 tuple은 그대로 보존하되, 모든 실행 결과를 다음 의미 필드로 정규화한다.

```text
case_id
issue_id
unit_id
defendant_id
outcome = established | not_established | undetermined | conflict
subtypes[]
active_rule_ids[]
active_norm_card_ids[]
```

이는 Python의 죄명별 분기가 아니라 registry manifest가 unit별 query relation과 canonical outcome의
대응을 선언하는 offline asset이다. cross-offense module은 이 bridge만 입력받고, 원래 derivation을
잃지 않는다.

- [x] D5 승인 — 2026-08-03 사용자 승인
- [ ] D5 수정: ____________________

## D6. 방화 unit 첫 컴파일 범위

[predicate 계약 감사](../2026-08-03_ruleir_predicate_contract_risk.md)에서 재산죄 as-built에
단계 결론과 outcome bridge가 모두 없다는 것이 확인되었다.

- [x] D6 승인 — 2026-08-03. 첫 컴파일은 `base / attempt / completed` 세 track까지만 한다.
      `aggravated_result`와 post_outcome 12장은 outcome bridge 및 `homicide` unit RuleIR이
      생긴 뒤로 미루고, 그때까지 `predicate_ir_missing`으로 보고한다.
- [ ] D6 수정: ____________________

## D7. 방화 role tuple

방화는 공공위험범이므로 재산죄의 owner/possessor 어휘를 재사용하지 않는다.

- [x] D7 승인 — 2026-08-03. 현존자와 치사상 피해자는 다대다 구조로 서로 다를 수 있으므로
      track별로 별도 role tuple을 둔다. base/attempt/completed는 건조물과 현존자를 받고,
      치사상 track은 피해자를 별도로 받는 tuple을 쓴다.
- [ ] D7 수정: ____________________

## D8. 가중 track의 요건 상속 (2026-08-04)

방화의 track은 서로 배타적인 단계였으나, 상해의 `ancestral`·`special`·`aggravated_result`는
기본 구성요건을 그대로 요구하고 자기 요건만 더한다. 조립기가 track을 독립적으로만 다루면
가중 track이 기본 요건 없이 성립할 수 있다.

- [x] D8 승인 — 2026-08-03(H-B03 제2문). 승인 원장의 track 어휘에 `inherits_from`을 선언하면
      조립기가 `<track>_elements_satisfied ← <parent>_elements_satisfied ∧ <track> component`로
      낸다. 원장 검증기가 미선언 track 참조와 순환을 막는다.
- 런타임 확인: `ancestral.unknown_blocks`는 base의 필수 카드 하나를 unknown으로 돌렸을 때
      `ancestral_elements_satisfied`가 비는 것을 실제 Scallop 실행으로 확인한다.

## 검수 회신 형식

다음처럼 짧게 답해도 된다.

```text
D1 승인/수정
D2 승인/수정
D3 승인/수정
D4 승인, 단 ...
D5 승인/수정
```

승인 뒤에는 각 unit별로 카드 proposition·source quote·predicate argument·AND/OR/배제 구조를
10~20장 단위 검수 패킷으로 올린다. 사용자가 `approve / rewrite / context_only / split / reject` 중
하나를 판정하면 그 결정이 원장 JSON에 기록되고, 승인된 결정만 RuleIR과 SCL로 컴파일된다.
