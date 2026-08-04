# 살인 RuleIR 제안 05 — 공범 (Ⅰ.19, 24장)

## 이 track은 선언하되 이번 회차에 컴파일하지 않는다

공동정범·교사·방조는 **2인 이상의 관계**를 전제한다. 제안 01의 역할 tuple
`homicide_case_roles(case_id, defendant_id, victim_id)`로는 "누가 누구를 교사했는가"를
표현할 수 없다. 어제 상해의 제263조 동시범 특례에서 같은 벽에 부딪혔고, 그때와 같이
서명을 데이터로 선언하고 `declared_not_compiled`로 둔다.

```text
homicide_complicity_case_roles(case_id, defendant_id, victim_id, accomplice_id)
```

카드 판정은 아래에 전부 남기므로, 공범 module을 만들 때 그대로 컴파일된다. 공범은 총칙
제30~34조이고 모든 죄명이 공유하므로, 제263조와 함께 공유 module 후보다.

## 초안 — 공동정범 (7장)

| # | decision | role | component / join | track | 이유 |
|---:|---|---|---|---|---|
| 115 | approve | component | joint_principal / mandatory_all | complicity | 공동가공의 의사와 기능적 행위지배라는 주관적·객관적 요건 |
| 106 | approve | component | conspiracy / mandatory_all | complicity | 2인 이상의 공동가공 의사 결합. 순차적·암묵적 결합도 포함 |
| 108 | approve | component | conspiracy / mandatory_all | complicity | 공모자는 실행에 관여하지 않아도 공동정범 책임을 진다 |
| 107 | approve | component | functional_control / mandatory_all | complicity | 본질적 기여를 통한 기능적 행위지배로 공모공동정범 인정 |
| 116 | approve | bar | joint_principal / not_applicable | complicity | 인식·용인만으로는 공동가공의 의사가 되지 않는다 |
| 119 | approve | component | shared_intent / mandatory_all | complicity | 강도살인 공동정범은 살인 부분의 고의 공동을 요한다 |
| 121 | approve | bar | shared_intent / not_applicable | complicity | 예기치 못한 1인의 살인은 나머지에게 귀속되지 않는다 |

## 초안 — 공모관계 이탈 (3장)

| # | decision | role | component / join | track | 이유 |
|---:|---|---|---|---|---|
| 122 | approve | bar | withdrawal / not_applicable | complicity | 실행 착수 전 이탈하면 이후 행위에 책임이 없다. 명시적일 필요 없음 |
| 123 | context_only | context_only | - | - | 총을 버리고 도망간 것만으로는 부족 — 이탈 인정의 한계 |
| 124 | context_only | context_only | - | - | 주도자는 영향력을 제거해야 이탈 — 이탈 인정의 한계 |

## 초안 — 방조 (5장)

| # | decision | role | component / join | track | 이유 |
|---:|---|---|---|---|---|
| 103 | approve | component | aiding / mandatory_all | complicity | 정범의 살인을 알면서 실행행위를 용이하게 한 자는 방조범 |
| 102 | approve | component | aiding_conduct / alternative_any | complicity | 물질적 방조, 정신적 방조, 착수 전 방조 |
| 118 | approve | component | aiding_conduct / alternative_any | complicity | 보호·양육의무자가 구타를 제지하지 않은 부작위 방조 |
| 104 | approve | component | aiding_intent / alternative_any | complicity | 방조 고의와 정범 고의의 이중 고의 |
| 105 | approve | component | aiding_intent / alternative_any | complicity | 정범 고의는 미필적 인식·예견으로 충분 |

#104는 요건, #105는 그 요건 중 정범 고의 부분의 완화다. 필수와 택일이 섞이면 조립이
막히므로 둘 다 `alternative_any`로 통일했다. 상해의 `intent`에서 쓴 처리와 같다.

## 초안 — 교사 (5장)

| # | decision | role | component / join | track | 이유 |
|---:|---|---|---|---|---|
| 111 | approve | component | instigation / mandatory_all | complicity | 살의 없던 자를 교사하여 결의하게 하고 피교사자가 살인을 범한 경우 |
| 112 | approve | post_outcome | instigation_outcome / not_applicable | complicity | 승낙하지 않거나 착수하지 않으면 예비·음모에 준하여 처벌 |
| 109 | approve | post_outcome | instigation_outcome / not_applicable | complicity | 상해만 실행하면 상해교사와 교사미수의 상상적 경합 |
| 232 | approve | post_outcome | instigation_outcome / not_applicable | complicity | 결정 C 선택. 초과 실행 시 교사자는 상해치사 책임까지 |
| 113 | context_only | context_only | - | - | 교사 사실은 엄격한 증명을 요한다 — 증거법 영역 |

## 초안 — 증거·절차 (4장)

| # | decision | role | 이유 |
|---:|---|---|---|
| 110 | context_only | context_only | 교사사실을 간접사실로 증명하는 방법 — 증거법 |
| 114 | context_only | context_only | 공소장 변경 없이 방조 인정 — 형사소송법 영역 |
| 117 | context_only | context_only | 군 폭행 사건의 고의·공동정범 파기환송 사례. 사실인정 판단 |
| 120 | context_only | context_only | 인천 초등생 사건의 공모 증거 부족 판단. 증거법 |

#117과 #120은 법리가 아니라 **그 사건에서 증거가 부족했다**는 판단이다. #121이 같은
법리(예기치 못한 살인의 불귀속)를 규칙 문장으로 이미 담고 있으므로 손실이 없다.

## Human decision H-H05

1. 위 24장 초안을 일괄 승인하는가?
2. `complicity` track을 `declared_not_compiled`로 두고 공유 module 이관 대상으로
   표시하는 데 동의하는가? 컴파일하면 24장이 들어오지만 단독 피고인 tuple로는
   "누가 누구를 교사했는가"가 표현되지 않는다.
3. #104·#105를 둘 다 `alternative_any`로 통일하는 데 동의하는가?
