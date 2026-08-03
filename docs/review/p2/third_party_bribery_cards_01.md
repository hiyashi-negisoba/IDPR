# 제3자뇌물제공 RuleIR 카드 검수 1

- unit: `third_party_bribery`
- articles: art130
- cards: 1–15 / 38
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 1. `art130_sec1.basic_conduct`

- proposition: 공무원 또는 중재인이 그 직무에 관하여 부정한 청탁을 받고 제3자에게 뇌물을 공여하게 하거나 공여를 요구 또는 약속하면 제3자뇌물제공죄가 성립한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 제130조 제3자뇌물제공죄의 기본 행위 유형을 열거한 commentary synthesis이다.
- bounded sources:

  - `comm_001692_제130조_Ⅰ_0` / `Ⅰ`: “공무원 또는 중재인이 그 직무에 관하여 부정한 청탁을 받고 제3자에게 뇌물을 공여하게 하거나 공여를 요구 또는 약속하면 성립한다.”

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

## 2. `art130_sec1.direct_receipt_relationship_exception`

- proposition: 사회통념상 제3자가 뇌물을 받은 것을 공무원이 직접 받은 것과 같이 평가할 수 있는 관계가 있으면 제3자뇌물제공죄가 아니라 형법 제129조 제1항의 뇌물수수죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 직접 수수와 같이 평가할 수 있는 관계는 사회통념에 따른 평가를 요구하므로 사실관계별 법률 검토가 필요하다.
- bounded sources:

  - `comm_001692_제130조_Ⅰ_0` / `Ⅰ`: “사회통념상 그 다른 사람이 뇌물을 받은 것을 공무원이 직접 받은 것과 같이 평가할 수 있는 관계가 있는 경우에는 형법 제130조의 제3자뇌 물제공죄가 아니라, 형법 제129조 제1항의 뇌물수수죄가 성립한다.”

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

## 3. `art130_sec2_1.exchange_linked_request`

- proposition: 청탁 대상 직무집행 자체가 위법·부당하지 않더라도, 직무집행을 대가관계와 연결하여 그 대가 교부를 내용으로 하는 청탁은 부정한 청탁에 해당한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 직무집행과 대가 교부가 연결된 청탁인지는 청탁의 내용과 경위에 따라 검토한다.
- bounded sources:

  - `comm_001692_제130조_Ⅱ.1_1` / `Ⅱ.1`: “청탁의 대상이 된 직무집행이 그 자체는 위법·부당한 것이 아니라고 하더라도 당해 직무집행을 어떤 대가관계와 연결시켜 그 직무집행에 관한 대가 의 교부를 내용으로 하는 청탁이라면 ‘부정한 청탁’에 해당한다.”

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

## 4. `art130_sec2_1.improper_request_assessment`

- proposition: 직무관련 뇌물 또는 부정한 청탁 여부는 직무·청탁 내용, 이익제공자와의 관계, 이익의 다과, 수수 경위와 시기 및 직무집행 공정성에 대한 사회적 의심 여부 등을 종합하여 판단한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 열거 사정의 상대적 비중과 사회적 의심 여부는 기계적으로 열거할 수 없는 종합평가다.
- bounded sources:

  - `comm_001692_제130조_Ⅱ.1_1` / `Ⅱ.1`: “그 직무 혹은 청탁의 내용, 이익 제공자와의 관계, 이익의 다과 및 수수 경위와 시기 등의 제반 사정과 아울러 직무집행의 공정과 이에 대한 사회 의 신뢰 및 직무수행의 불가매수성이라고 하는 뇌물죄의 보호법익에 비추어”

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

## 5. `art130_sec2_1.improper_request_scope`

- proposition: 부정한 청탁에는 위법하거나 부당한 직무집행을 내용으로 하는 청탁뿐 아니라 사회상규나 신의성실 원칙에 위배되는 청탁도 포함된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 사회상규 또는 신의성실 원칙 위반 여부는 구체적 청탁 내용에 대한 평가를 필요로 한다.
- bounded sources:

  - `comm_001692_제130조_Ⅱ.1_1` / `Ⅱ.1`: “본죄에 있어서 ‘부정한 청탁’은, 그 청탁이 위법하거나 부당한 직무집행 을 내용으로 하는 경우는 물론, 사회상규나 신의성실의 원칙에 위배되는 경우도 포함된다.”

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

## 6. `art130_sec2_2.case_engineering_introduction_conviction`

- proposition: 건축 관련 민원 담당 공무원이 인허가 지연 가능성을 언급하고 특정 엔지니어링 업체만 소개하며 계약 이행과정에도 관여하여 사업자가 그 업체와 고가 용역계약을 체결한 경우, 해당 업체 관련 제3자뇌물수수죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 이는 특정 엔지니어링 업체 소개와 용역계약 이행 관여가 결합된 좁은 보고 판례의 결론으로, 원문 판례와 전체 사실인정 범위를 확인해야 한다.
- bounded sources:

  - `comm_001692_제130조_Ⅱ.2_7` / `Ⅱ.2`: “A는 ○○엔지니어링 사무실을 찾아가서 B를 만나 다소 비싼 가격으로 용역계약을 체결하였으며, 피고인이 위 용역계약 이행과정에 관여하기 도 하였다면 피고인에게 ○○엔지니어링 관련 제3자뇌물수수죄가 성립한다.”

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

## 7. `art130_sec2_2.case_foundation_contributions_no_exchange`

- proposition: 대통령 측근 등이 특정 기업집단 총수로 하여금 재단 설립자금을 지급하게 한 사안에서, 해당 기업집단에만 대가관계나 승계작업 현안에 대한 대가 인식이 있었다고 보기 어려워 묵시적 청탁과 재단 출연금 사이 대가관계를 단정하기 어려우면 제3자뇌물수수죄는 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 이는 재단 출연금과 승계작업 관련 묵시적 청탁의 대가관계를 단정하기 어려웠던 개별 보고 판례의 좁은 결론으로 검토해야 한다.
- bounded sources:

  - `comm_001692_제130조_Ⅱ.2_6` / `Ⅱ.2`: “따라서 승계작업에 관한 공여자의 묵시적 청탁과 이 사건 각 재단 출연금 사이에 대가 관계가 존재한다고 단정하기 어려우므로, 제3자뇌물수수죄는 성립하지 않는다.”

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

## 8. `art130_sec2_2.future_pending_matter`

- proposition: 부정한 청탁의 내용은 이미 발생한 현안뿐 아니라 장래 발생이 예상되는 현안도 필요한 정도로 특정되면 될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 장래 현안이 필요한 정도로 특정되었는지는 개별 사실관계에 따라 평가해야 하며, 보고된 판례의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제130조_Ⅱ.2_3` / `Ⅱ.2`: “부정한 청탁의 내용은 이미 발생한 현안뿐만 아니라 장래 발생될 것으로 예상되는 현안도 위와 같은 정도 로 특정되면 부정한 청탁의 내용이 될 수 있다.”

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

## 9. `art130_sec2_2.implied_request`

- proposition: 부정한 청탁은 명시적 의사표시가 없어도, 청탁 대상 직무집행과 제3자 제공 금품이 직무집행의 대가라는 점에 관하여 당사자 사이에 공통 인식 또는 양해가 있으면 묵시적으로 가능하다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 묵시적 청탁의 공통 인식 또는 양해는 사실관계에 대한 평가가 필요하며, 보고된 판례의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제130조_Ⅱ.2_3` / `Ⅱ.2`: “부정한 청탁은 명시적인 의사표 시가 없더라도 청탁의 대상이 되는 직무집행의 내용과 제3자에게 제공되는 금 품이 직무집행에 대한 대가라는 점에 대하여 당사자 사이에 공통의 인식이나 양해가 있는 경우에는 묵시적 의사표시로 가능하다.”

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

## 10. `art130_sec2_2.indictment_particularity`

- proposition: 제3자뇌물수수죄 공소사실에서 부정한 청탁 내용은 구체적으로 기재되지 않아도 공무원 등의 직무와 제3자 제공 이익 사이 대가관계를 인정할 수 있을 정도로 특정되면 충분하며, 청탁 대상 직무행위 내용을 구체적으로 특정할 필요는 없다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 대가관계를 인정할 수 있을 정도의 특정성은 개별 공소사실과 증거관계에 대한 평가를 요구하며, 보고된 판례의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제130조_Ⅱ.2_3` / `Ⅱ.2`: “그중 부정한 청탁의 내용은 구체적으로 기 재되어 있지 않더라도 공무원 또는 중재인의 직무와 제3자에게 제공되는 이익 사이의 대가관계를 인정할 수 있을 정도로 특정되면 충분하다. 청탁의 대상인 직무행위의 내용을 구체적으로 특정할 필요도 없다.”

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

## 11. `art130_sec2_2.introduction_recommendation_assessment`

- proposition: 공무원이 직무관련자에게 제3자를 거래상대방으로 소개·추천한 행위가 제3자에게 직무 관련 부정한 이익을 공여하게 한 행위인지 여부는 소개·추천 경위, 제3자 이익과 공무원의 인식, 공무원의 이익 기대, 이후 직무행위 및 관계 등을 종합 고려하여 판단한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 열거된 사정은 종합평가 요소이며, 어느 요소가 필수인지 및 제3자성 판단과의 관계는 원문 판례로 검토해야 한다.
- bounded sources:

  - `comm_001692_제130조_Ⅱ.2_6` / `Ⅱ.2`: “그 소개·추천에 이르게 된 경위, 소개·추천을 통하여 제3자가 얻는 이익의 내용과 이에 대한 공무원의 인식 정도, 소개·추천과 관련하여 공무원이 이익을 기대하였 는지 여부, 소개·추천 이후에 한 공무원의 직무행위 내용, 공무원과 직무관련자 또는 제3자와의 관계 등 여러 사정을 종합적으로 고려하여 판단하여야 한다.”

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

## 12. `art130_sec2_2.no_implied_request_without_exchange_awareness`

- proposition: 당사자 사이에 직무집행과 제3자 금품 제공의 대가관계에 관한 공통 인식이나 양해 없이 단지 선처 기대 또는 직무와 무관한 동기로 제3자에게 금품을 공여한 경우에는 묵시적 부정한 청탁을 인정하기 어렵다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 이는 공통 인식 또는 양해가 없다는 실제 사실판단을 전제로 하는 부정적 기준이며, 단순한 긍정 사실의 부재를 부정으로 추정하지 않는다.
- bounded sources:

  - `comm_001692_제130조_Ⅱ.2_5` / `Ⅱ.2`: “그러한 인식이나 양해 없이 막연히 선처하여 줄 것이라는 기대 에 의하거나 직무집행과는 무관한 다른 동기에 의하여 제3자에게 금품을 공여한 경우에는 묵시적인 의사표시에 의한 부정한 청탁이 있다고 보기 어렵다.”

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

## 13. `art130_sec2_2.no_retrospective_exchange_link`

- proposition: 청탁 당시 대가관계에 관한 양해가 없으면 나중에 제3자와 금품 수수가 있었다는 사정만으로 청탁을 소급하여 부정한 것으로 평가할 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 청탁 당시 양해의 존재와 후속 금품 수수의 증명 관계를 구별하여 검토해야 하며, 보고된 판례의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제130조_Ⅱ.2_5` / `Ⅱ.2`: “청탁과 관련하여 대가관계에 대한 양해가 존재하지 않는다면 단지 나중에 제3 자와 금품 수수가 있었다는 사정만으로 소급하여 청탁이 부정한 것으로 평가할 수는 없다.”

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

## 14. `art130_sec3-na.company-legal-service`

- proposition: 대통령이 상당한 영향력을 행사하던 회사가 미국 법률사무소의 법률용역을 이용할 기회와 권리를 제공받고 다른 회사가 그 비용을 지급한 경우, 이를 대통령이 직접 받은 것으로 볼 수 없어 뇌물수수죄는 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 법률용역 이용 기회와 권리의 귀속 및 공무원의 직접 수령 여부는 사회통념에 따른 평가를 필요로 한다.
- bounded sources:

  - `comm_001692_제130조_Ⅲ.나_11` / `Ⅲ.나`: “미국 법률사무소가 제공하는 법률용역을 이용할 기회와 권리를 제공받은 것은 A주식회사이고, 이를 사회통념상 피고인이 직접 받은 것 으로 볼 수 없으므로, 뇌물수수죄는 성립하지 않는다.”

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

## 15. `art130_sec3-na.joint-bribery-conspiracy`

- proposition: 뇌물수수죄 공범 사이에 직무 관련 금품·이익 수수의 명시적 또는 묵시적 공모가 있고, 공모에 따라 공범 중 1인이 이를 주고받으면 특별한 사정이 없는 한 전부에 관하여 공동정범이 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`False`
- source track: `unit_core`
- prior note: 명시적 또는 묵시적 공모와 특별한 사정의 존재는 증거에 따른 평가가 필요하다.
- bounded sources:

  - `comm_001692_제130조_Ⅲ.나_12` / `Ⅲ.나`: “뇌물수수죄의 공범들 사이에 직무 와 관련하여 금품이나 이익을 수수하기로 하는 명시적 또는 암묵적 공모관계가 성립하고 공모 내용에 따라 공범 중 1인이 금품이나 이익을 주고받았다면, 특별 한 사정이 없는 한 이를 주고받은 때 그 금품이나 이익 전부에 관하여 뇌물수수 죄의 공동정범이 성립”

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
