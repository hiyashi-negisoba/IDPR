# 제3자뇌물제공 RuleIR 카드 검수 2

- unit: `third_party_bribery`
- articles: art130
- cards: 16–30 / 38
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 16. `art130_sec3-na.joint-bribery-no-specific-amount`

- proposition: 뇌물수수 공동정범 성립에는 공범 사이의 금품·이익 규모 또는 구체적 금액에 관한 사전 의사연락이나 인식이 필요하지 않으며, 성립 후 뇌물이 누구에게 실제 귀속되었는지도 이미 성립한 죄에 영향을 미치지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`precedent_position`, review_required=`False`
- source track: `unit_core`
- prior note: 공동정범 성립이 확인된 뒤에는 구체적 금액 인식 또는 사후 귀속만으로 이를 부정하지 않는 관계로 검토한다.
- bounded sources:

  - `comm_001692_제130조_Ⅲ.나_12` / `Ⅲ.나`: “금품이나 이익의 규모나 정도 등에 대하여 사전에 서로 의사의 연락이 있거나 금품 등의 구체적 금액을 공범이 알아야 공동정범 이 성립하는 것은 아니다. 금품이나 이익 전부에 관하여 뇌물수수죄의 공동정범 이 성립한 이후에 뇌물이 실제로 공동정범인 공무원 또는 비공무원 중 누구에 게 귀속되었는지는 이미 성립한 뇌물수수죄에 영향을 미치지 않는다.”

```text
decision:
role:
component_id:
component_join:
track_id:
refers_to_unit:
rationale:
proposition_rewrite:
```

## 17. `art130_sec3-na.joint-perpetrator-not-third-party`

- proposition: 공무원과 공동정범 관계의 비공무원은 제3자뇌물수수죄의 제3자가 될 수 없고, 그 비공무원이 뇌물을 받으면 공무원과 함께 뇌물수수죄 공동정범이 성립하며 제3자뇌물수수죄는 성립하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`precedent_position`, review_required=`False`
- source track: `unit_core`
- prior note: 공동정범 관계가 확정된 경우 제3자 해당성을 배제하는 관계로 검토한다.
- bounded sources:

  - `comm_001692_제130조_Ⅲ.나_11` / `Ⅲ.나`: “공무원과 공동정범 관계에 있는 비공무원은 제 3자뇌물수수죄에서 말하는 제3자가 될 수 없고, 공무원과 공동정범 관계에 있는 비공무원이 뇌물을 받은 경우에는 공무원과 함께 뇌물수수죄의 공동정범이 성 립하고 제3자뇌물수수죄는 성립하지 않는다.”

```text
decision:
role:
component_id:
component_join:
track_id:
refers_to_unit:
rationale:
proposition_rewrite:
```

## 18. `art130_sec3-na.mountain-club-towel`

- proposition: 산악회 지부가 사업자로부터 행사 수건을 받은 사정만으로, 그 지부 고문인 군수가 이를 받은 것과 동일시하기에는 부족하다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 단체의 수령을 고문인 공무원의 직접 수령과 동일시할 수 있는지는 개별 사실관계 평가가 필요하다.
- bounded sources:

  - `comm_001692_제130조_Ⅲ.나_11` / `Ⅲ.나`: “산악회 지부가 사업자로부터 등반대회 행사용 수건을 교부받은 것을 산악회 지부의 고문으로 있는 군수가 이를 교부받은 것과 동일시하기에는 부족하다.”

```text
decision:
role:
component_id:
component_join:
track_id:
refers_to_unit:
rationale:
proposition_rewrite:
```

## 19. `art130_sec3-na.nonofficial-joint-bribery`

- proposition: 비공무원이 공무원과 공동가공의 의사 및 이를 기초로 한 기능적 행위지배를 통하여 공무원 직무에 관하여 뇌물을 수수한 범죄를 실행하면, 공무원과 비공무원에게 뇌물수수죄 공동정범이 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`False`
- source track: `unit_core`
- prior note: 공동가공의 의사와 기능적 행위지배의 충족 여부는 개별 사실관계에 적용하여 검토한다.
- bounded sources:

  - `comm_001692_제130조_Ⅲ.나_11` / `Ⅲ.나`: “비공무원이 공무원과 공동가공의 의사와 이를 기초로 한 기능적 행위지배를”
  - `comm_001692_제130조_Ⅲ.나_11` / `Ⅲ.나`: “통하여 공무원의 직무에 관하여 뇌물을 수수하는 범죄를 실행하였다면 공무원 이 직접 뇌물을 받은 것과 동일하게 평가할 수 있으므로 공무원과 비공무원에 게 형법 제129조 제1항에서 정한 뇌물수수죄의 공동정범이 성립한다.”

```text
decision:
role:
component_id:
component_join:
track_id:
refers_to_unit:
rationale:
proposition_rewrite:
```

## 20. `art130_sec3-na.shareholder-indirect-benefit`

- proposition: 공무원 또는 공동정범자가 아닌 회사가 후원금을 받은 것을 피고인이 직접 받은 것과 동일하게 평가할 수 없는 이상, 피고인이 그 회사 지분 33%를 보유한 주주로서 간접적 경제적 이익을 얻더라도 그 이익에 관하여 단순수뢰죄가 별도로 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 회사 수령과 공무원의 직접 수령의 동일성 및 주주의 간접 이익은 사실관계별 평가가 필요하다.
- bounded sources:

  - `comm_001692_제130조_Ⅲ.나_11` / `Ⅲ.나`: “회사가 후원금을 받은 것을 피고인들이 직접 받은 것과 동일하게 평가할 수 없 다는 이유로 후원금에 대한 단순수뢰죄가 성립하지 않는다고 보는 이상, C주식 회사가 공무원이나 그 공동정범자 이외의 제3자 지위에서 후원금을 공여받음으 로써 피고인 B가 그 주주로서 간접적으로 이익을 얻게 되더라도 그러한 사실상 의 경제적 이익에 관하여 피고인들을 뇌물의 귀속주체로 하여 단순수뢰죄가 별 도로 성립한다고 볼 수 없다.”

```text
decision:
role:
component_id:
component_join:
track_id:
refers_to_unit:
rationale:
proposition_rewrite:
```

## 21. `art130_sec3.corporate_attribution_indicia`

- proposition: 공무원이 법인의 대표이사·임원이거나 법인을 실질적으로 운영하였다는 사정만으로는 법인 귀속 이익을 공무원 개인에게 귀속된 것과 동일하게 평가하기 부족하며, 사실상 1인 회사 운영, 법인 계좌의 뇌물수수 창구 이용, 법인에 대한 공무원의 구체적 지출의무 면제 등 구체적 사정이 요구될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 법인 대표·임원 또는 실질 운영 사실만으로는 부족하다는 보고 판례 기준이며, 추가 귀속 정황을 개별적으로 평가해야 한다.
- bounded sources:

  - `comm_001692_제130조_Ⅲ_9` / `Ⅲ`: “행위자가 법인 등의 대표이사 나 임원이라는 사정 혹은 법인 등을 실질적으로 운영하여 왔다는 사정만으로 부족하고 더 나아가 법인 등을 사실상 1인 회사나 개인 기업처럼 운영해 온 경 우, 법인 등의 계좌를 행위자에 대한 뇌물을 수수하는 창구로 이용하여 온 경우, 법인 등이 뇌물을 받음으로써 행위자가 법인 등에 대한 구체적인 지출의무를 면하게 되는 경우 등 보다 구체적인 사정이 필요한 경우가 많다.”

```text
decision:
role:
component_id:
component_join:
track_id:
refers_to_unit:
rationale:
proposition_rewrite:
```

## 22. `art130_sec3.corporate_benefit_attribution`

- proposition: 법인·단체가 받은 이익을 공무원 개인이 받은 것과 동일하게 평가하여 단순수뢰죄를 인정하려면, 그 이익이 경제적·실질적으로 공무원 개인에게 귀속된 것과 동일하게 평가될 정도에 이르러야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 법인·단체 귀속 이익을 공무원 개인 수뢰로 평가하기 위한 경제적·실질적 귀속 기준의 보고 판례 카드다.
- bounded sources:

  - `comm_001692_제130조_Ⅲ_9` / `Ⅲ`: “제3자가 개인이 아닌 법인이나 단체인 경우에도 법인이나 단체에 귀속된 이”
  - `comm_001692_제130조_Ⅲ_9` / `Ⅲ`: “익이 경제적, 실질적 관점에서 행위자 개인에게 귀속된 것과 동일하게 평가할 수 있을 정도에 이르러야만 단순수뢰죄의 성립을 인정할 수 있다.”

```text
decision:
role:
component_id:
component_join:
track_id:
refers_to_unit:
rationale:
proposition_rewrite:
```

## 23. `art130_sec3.direct_substantial_interest_exception`

- proposition: 행위자와 제3자의 이해관계가 직접적이고 실질적으로 연결되어 행위자가 직접 뇌물을 받은 것처럼 평가되는 경우, 그 상대방은 제3자에 해당하지 않고 단순수뢰죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 직접적·실질적 이해관계 연결 여부는 구체적 사실관계의 평가를 필요로 하며, 제3자성 부정의 예외로 유지한다.
- bounded sources:

  - `comm_001692_제130조_Ⅲ_8` / `Ⅲ`: “자의 이해관계가 직접적이고 실질적으로 연결되어 있는 경우에는 행위자가 직 접 뇌물을 받은 것과 같이 평가할 수 있다는 점에서 제3자에 해당하지 않고 단 순수뢰죄가 성립하게 된다.”

```text
decision:
role:
component_id:
component_join:
track_id:
refers_to_unit:
rationale:
proposition_rewrite:
```

## 24. `art130_sec3.independent_spouse_business_account`

- proposition: 공무원과 처가 독립적으로 수입·계좌를 관리하고 공무원이 처의 업체 운영에 관여하지 않은 경우, 그 업체 계좌가 공여자로부터 용역비를 받았더라도 공무원이 직접 받은 것과 동일하게 볼 수 없다는 사례가 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 독립적 배우자 사업체 계좌 수령을 공무원의 직접 수령과 동일시하지 않은 좁은 사례 카드다.
- bounded sources:

  - `comm_001692_제130조_Ⅲ_9` / `Ⅲ`: “피고인과 처가 재혼으로 결혼 전부터 서로 직업을 가지고 수입을 얻어 왔으며, 결혼 후에도 각각 자신의 계좌를 사용하면서 월급 등을 관리해 왔고, 어 느 일방의 수입원으로 생활비를 부담하지는 않았으며, 피고인이 처가 운영하는 업체에 관여하지 않은 경우 그 업체의 계좌로 공여자로부터 용역비를 받았다면 피고인이 직접받은 것과 동일하게 볼 수 없다고 본 사례도 있다.”

```text
decision:
role:
component_id:
component_join:
track_id:
refers_to_unit:
rationale:
proposition_rewrite:
```

## 25. `art130_sec3.individual_benefit_attribution`

- proposition: 제3자가 받은 이익을 공무원 자신의 이익으로 평가할 수 있는지는 투자관계, 당사자 의사, 독립된 정상거래 가능성 및 정상거래 정황 등을 종합하여 판단한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 개인 제3자 수익을 공무원 자신의 이익으로 볼지에 관한 종합평가 기준으로, 보고된 판례 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제130조_Ⅲ_9` / `Ⅲ`: “이러한 경우에 해당하는지는 공무 원과 그 다른 사람 사이에 투자관계가 형성되어 있거나 장차 형성될 것이 기대 되었는지 여부, 공무원과 증뢰자의 의사가 어떠하였는지 여부, 공무원의 투자금 내지 대여금이라는 계산을 배제하고서도 증뢰자와 그 다른 사람 사이에 정상적 인 거래가 성립될 수 있는 관계였는지 여부, 증뢰자와 그 다른 사람 사이의 정 상적인 거래를 나타내는 정황적인 징표들이 존재하는지 여부 등을 종합하여 판 단하여야 한다.”

```text
decision:
role:
component_id:
component_join:
track_id:
refers_to_unit:
rationale:
proposition_rewrite:
```

## 26. `art130_sec3.lovers_relationship_insufficient`

- proposition: 행위자와 제3자의 연인관계만으로는 제3자가 공여자로부터 받은 금품 또는 교수 임용 이익을 행위자 자신의 이익으로 평가하기 어렵다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 연인관계만으로 이익 귀속을 추인하지 않는다는 좁은 보고 판례 기준이다.
- bounded sources:

  - `comm_001692_제130조_Ⅲ_9` / `Ⅲ`: “행위자와 제3자가 연인관계라는 사정만으로는 제3자가 공여자로부터 금품을 받거나 대학 교수 임용이라는 이익을 제공받은 것을 행위자 자신의 이익으로 평가하기 어렵다.”

```text
decision:
role:
component_id:
component_join:
track_id:
refers_to_unit:
rationale:
proposition_rewrite:
```

## 27. `art130_sec3.nontraditional_benefit_forms`

- proposition: 종교·사회단체나 지방자치단체에 대한 기부, 시설물 기부채납, 재단 설립 출연금 또는 채무의 대위변제 형식으로 제3자에게 이익을 제공한 경우에도 본죄가 성립할 수 있다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 열거된 비전형적 이익 제공 형식도 제3자에 대한 이익 제공으로 다루는 카드이며, 다른 성립요건은 별도로 검토한다.
- bounded sources:

  - `comm_001692_제130조_Ⅲ_8` / `Ⅲ`: “그러한 사실을 모르는 종교단체나 사회단체, 지방자치단체 에 대한 기부나 시설물 기부채납, 재단의 설립 출연금, 채무의 대위변제 등의 형 식으로 이루어진 경우에도 본죄가 성립한다.”

```text
decision:
role:
component_id:
component_join:
track_id:
refers_to_unit:
rationale:
proposition_rewrite:
```

## 28. `art130_sec3.spouse_delivery_inference`

- proposition: 은행 지점장에게 대출승인 선처를 부탁하던 회사 대표가 지점장 처에게 금품을 보낸 사안에서, 지점장과 대표의 지속적·사적 관계 및 처가 그 사실을 숨기기 어려운 사정 등이 있으면 특별한 합리적 근거가 없는 한 그 금품은 지점장에게 전달된 것으로 본다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 특정 배우자 수령 사안에서의 전달 추인에 관한 좁은 보고 판례 카드다. 적용 전 원문 판결과 사실관계의 일치 여부를 확인해야 한다.
- bounded sources:

  - `comm_001692_제130조_Ⅲ_9` / `Ⅲ`: “달리 합리적인 근거가 없는 한 이 금품은 피고인에게 전달되었다고 봄이 상당하다.”

```text
decision:
role:
component_id:
component_join:
track_id:
refers_to_unit:
rationale:
proposition_rewrite:
```

## 29. `art130_sec3.spouse_insurance_opportunity`

- proposition: 금융감독원 선임조사역이 자신의 처를 통하여 보험모집 기회라는 경제적 이익을 제공받은 경우, 대가관계 있는 뇌물수수로 볼 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 배우자를 통한 보험모집 기회 제공에 관한 좁은 보고 판례 카드이며, 대가관계와 경제적 이익의 구체적 내용을 검토해야 한다.
- bounded sources:

  - `comm_001692_제130조_Ⅲ_9` / `Ⅲ`: “금융감독원 선임조사역인 피고인이 자신의 처로 하여금 보험모집의 기회라는 경제적 이익을 제공받은 것은 피고인이 대가관계에 있는 뇌물을 수수한 것으로 볼 수 있다.”

```text
decision:
role:
component_id:
component_join:
track_id:
refers_to_unit:
rationale:
proposition_rewrite:
```

## 30. `art130_sec3.third_party_definition`

- proposition: 제3자란 행위자와 공동정범 이외의 사람을 말하며, 교사자나 방조자도 포함될 수 있다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 제3자의 인적 범위를 설명하는 정의 카드이며, 교사자·방조자의 포함 가능성은 원문 표현 범위로 한정한다.
- bounded sources:

  - `comm_001692_제130조_Ⅲ_8` / `Ⅲ`: “제3자는 행위자와 공동정범 이외의 사람을 말하고, 교사자나 방조자도 포함될 수 있다.”

```text
decision:
role:
component_id:
component_join:
track_id:
refers_to_unit:
rationale:
proposition_rewrite:
```
