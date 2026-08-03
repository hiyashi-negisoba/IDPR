# 살인 RuleIR 제안 04 — 위법성과 책임 (Ⅰ.16~Ⅰ.18, 29장)

track 어휘는 제안 01·03을 따른다.

## 제안 01의 "책임능력 11장 전량 제외"를 철회한다

제안 01에서 Ⅰ.18을 총칙 영역으로 보아 통째로 빼자고 적었다. 11장을 다시 읽고 생각을
바꿨다. **책임능력은 구성요건·위법성과 나란한 범죄성립요건이고, 심신상실은 성립을
배제한다.** 감경 사유인 심신미약과 성립 배제인 심신상실을 뭉뚱그려 총칙이라고 버리면
"심신상실이면 살인죄가 성립하지 않는다"는 결론이 RuleIR 밖으로 나간다.

그래서 4장은 자리를 주고 7장만 `context_only`로 둔다. 아래 표에 근거를 적었다.

## 초안 — 위법성 조각 (Ⅰ.16, 12장)

| # | decision | role | component / join | track | refers_to | 이유 |
|---:|---|---|---|---|---|---|
| 83 | approve | bar | justification / not_applicable | base | - | 법익의 종류·정도, 침해 방법·완급을 참작한 사회적 상당성 |
| 76 | approve | bar | justification / not_applicable | base | - | 반격방어도 방어행위에 포함되나 상당한 이유를 요함 |
| 80 | rewrite | bar | justification / not_applicable | base | - | 메타 래퍼 제거. 격투 중 예상 범위를 넘는 흉기 사용은 부당한 침해 |
| 85 | approve | boundary | justification / not_applicable | base | consent_homicide | 피해자 승낙은 위법성을 조각하지 않고 제252조로 경계가 이동 |
| 78 | approve | post_outcome | excessive_defense / not_applicable | base | - | 연속된 전후행위를 하나로 보아 과잉방위가 될 수 있음. 감면 사항 |
| 74 | context_only | context_only | - | - | - | 위급하지 않고 비치명적 수단이 있었으면 과잉방위 부정 — 조각의 한계 |
| 75 | context_only | context_only | - | - | - | 침해 종료 후 제압된 침입자에 대한 폭행 — 조각의 한계 |
| 77 | context_only | context_only | - | - | - | 지속적 가정폭력이 있어도 회피 가능하면 부정 — 조각의 한계 |
| 79 | context_only | context_only | - | - | - | 싸움은 방위·공격 양면이므로 정당방위 불가 — 조각의 한계 |
| 81 | context_only | context_only | - | - | - | 살인죄에 긴급피난이 적용되지 않는다는 한계 |
| 82 | context_only | context_only | - | - | - | 계획된 심장 자상은 상당성 부정 — 조각의 한계 |
| 84 | context_only | context_only | - | - | - | 폭행·협박을 받았어도 칼로 자상하면 한도 초과 — 조각의 한계 |

## 초안 — 안락사와 연명의료 중단 (Ⅰ.17, 6장)

| # | decision | role | component / join | track | 이유 |
|---:|---|---|---|---|---|
| 89 | approve | bar | justification / not_applicable | base | 연명의료결정법의 요건·절차를 지킨 중단은 제20조 법령에 의한 행위 |
| 87 | approve | bar | justification / not_applicable | base | 회복불가능한 사망 단계에서 자기결정권 행사가 인정되면 중단 허용 |
| 86 | approve | bar | justification / not_applicable | base | 사전의료지시가 있고 의사 변경의 특별사정이 없는 경우 |
| 88 | approve | bar | justification / not_applicable | base | 사전의료지시가 없어도 추정적 의사가 인정되는 경우 |
| 90 | context_only | context_only | - | - | 1957년 판결의 결론 인용에 그치고 적용 요건이 없음 |
| 231 | context_only | context_only | - | - | 결정 C 선택(적극적 안락사 부정설). 조각의 한계이므로 자리가 없음 |

#86·#87·#88은 같은 조각 사유의 세 인정 경로다. `bar`는 join을 쓰지 않으므로 셋 다 두어도
충돌하지 않고, 어느 하나가 충족되면 성립이 저지된다 — 법리와 일치한다.

## 초안 — 책임능력 (Ⅰ.18, 11장)

| # | decision | role | component / join | track | 이유 |
|---:|---|---|---|---|---|
| 99 | approve | component | responsibility_capacity / mandatory_all | base | 범행 당시를 기준으로 책임능력이 있어야 살인죄가 성립 |
| 97 | approve | bar | mental_incapacity / not_applicable | base | 생물학적 요소와 심리학적 요소를 모두 갖춘 심신장애 |
| 101 | approve | bar | mental_incapacity / not_applicable | base | 정신병자와 동등하다고 평가할 만큼 심각한 성격적 결함 |
| 92 | approve | bar | expectability / not_applicable | base | 적법행위의 기대가능성이 없으면 책임을 물을 수 없음 |
| 93 | context_only | context_only | - | - | 성격적 결함은 원칙적으로 심신장애가 아니라는 한계 |
| 96 | context_only | context_only | - | - | 정상적 능력이 있으면 심신장애가 아니라는 한계 |
| 98 | context_only | context_only | - | - | 병적/성격적 결함의 구분 기준이며 #97·#101과 중복 |
| 91 | context_only | context_only | - | - | 원인에 있어서 자유로운 행위. 감경 배제이므로 성립 결론과 무관 |
| 100 | context_only | context_only | - | - | 필로폰 자의 투약 사안. #91과 같은 규칙 |
| 94 | context_only | context_only | - | - | 정신감정 없이 배척하면 위법. 심리 절차 영역 |
| 95 | context_only | context_only | - | - | 감정 의견에 기속되지 않는다는 판단 방법. 심리 영역 |

`mental_incapacity`는 심신**상실**만을 겨냥한다. 심신미약은 감경 사유이므로 성립을 막지
않고, 이 unit은 형을 다루지 않으므로 표현하지 않는다. #97·#101이 `bar`로 충족되는 경우는
심신상실 수준일 때뿐이라는 것을 평가 단계에서 구분해야 한다 — 이 구분은 카드 문언에
없으므로 아래 H-H04 제3문에서 확인을 구한다.

## 손실 기록 — 이 문서에서만 15장이 `context_only`다

정당방위 7장, 안락사 2장, 책임능력 6장이 RuleIR 밖으로 나간다. 전부 "이 경우에는 조각되지
않는다" 또는 "이 경우에는 심신장애가 아니다"라는 **조각의 한계** 규칙이고, 현재 역할 어휘
`component / bar / boundary / waiver / post_outcome / context_only`에 자리가 없다.

상해에서 같은 문제로 7장을 버렸고, 그때 `qualifier` 역할 추가는 기각되었다. 여기서는
손실이 15장으로 두 배가 넘는다. 다시 묻지는 않되 규모가 커졌다는 사실만 적어 둔다.

## Human decision H-H04

1. 위 29장 초안을 일괄 승인하는가?
2. 제안 01의 "책임능력 11장 전량 제외"를 철회하고 4장(#99·#97·#101·#92)에 자리를 주는
   위 방식에 동의하는가?
3. `mental_incapacity` bar가 **심신상실에 한정**된다는 것을 평가 단계 지침으로 두는 데
   동의하는가? 카드 문언은 심신상실과 심신미약을 구분하지 않는다.
4. #85(피해자 승낙)를 제252조 촉탁·승낙살인으로의 `boundary`로 두는 데 동의하는가?
   해당 unit RuleIR이 없으므로 `predicate_ir_missing`으로 보고된다.
