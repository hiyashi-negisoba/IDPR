# 사문서등위조·변조 RuleIR 카드 검수 3

- unit: `private_document_forgery`
- articles: art231
- cards: 31–44 / 44
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 31. `art231_sec3_3.notarized_private_instrument_alteration`

- proposition: 사서증서 인증서의 인증기재 부분은 공문서이나 사서증서 기재 내용은 그 공문서 인증기재의 내용을 구성하지 않으므로, 사서증서 기재 내용을 일부 변조한 행위는 공문서변조죄가 아니라 사문서변조죄에 해당한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 변경 대상이 인증기재 부분인지 사서증서 기재 내용인지 구분해야 하며, 보고된 판례의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제231조_Ⅲ.3_13` / `Ⅲ.3`: “사서증서 인증서 중 인증기재 부분은 공문서에 해당한다고 하겠 으나, 위와 같은 내용의 인증이 있었다고 하여 사서증서의 기재 내용이 공문서 인 인증기재 부분의 내용을 구성하는 것은 아니므로, 사서증서의 기재 내용을 일부 변조한 행위는 공문서변조죄가 아니라 사문서변조죄에 해당한다.”

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

## 32. `art231_sec3_3.post_contract_price_alteration`

- proposition: 매매계약서 작성 완료 후 매도인 또는 매수인이 상대방 승낙 없이 매매대금 액수나 지급일자 등 내용을 고치면, 그 계약서가 타인 명의 문서에 해당하여 사문서변조죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 계약서 작성 완료, 상대방 승낙 부재 및 변경 내용이 확인되어야 하며, 보고된 판례의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제231조_Ⅲ.3_12` / `Ⅲ.3`: “매매계약서 작성이 완료된 후 매도인 또는 매수인이 상대방의 승낙 없이 그 매매계약서의 내용 (예컨대, 매매대 을 고치는 행위는 위 매매계약서가 타인 명의의 문서에 해당 금의 액수·지불일자) 하므로 사문서변조죄가 성립한다.”

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

## 33. `art231_sec3_3.public_confidence_risk`

- proposition: 변조는 문서에 대한 공공의 신용을 해할 위험성이 있는 정도이면 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 공공의 신용을 해할 위험성은 사실관계별 평가를 요구한다.
- bounded sources:

  - `comm_001692_제231조_Ⅲ.3_13` / `Ⅲ.3`: “변조는 문서에 대한 공공의 신용을 해할 위험성이 있는 정도이면 성립한다.”

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

## 34. `art231_sec4.purpose_of_use`

- proposition: 사문서위조·변조죄는 고의 외에 행사할 목적을 요구하는 목적범이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 행사할 목적의 존재는 개별 사실관계에 대한 평가가 필요하다.
- bounded sources:

  - `comm_001692_제231조_Ⅳ_15` / `Ⅳ`: “본죄는 행사할 목적으로 타인의 문서를 위조·변조하는 것이므로 고의 외에 행 사할 목적이 있어야 하는 목적범이다.”

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

## 35. `art231_sec4_1.expected_consent_does_not_negate_intent`

- proposition: 명의자의 명시적 승낙이나 동의가 없음을 알면서 명의자가 작성 사실을 알면 승낙할 것이라고 기대하거나 예측한 것만으로 승낙이 추정되지는 않으므로 고의는 인정된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 명의자의 승낙 부재에 대한 인식과 단순한 승낙 기대·예측을 사실관계에 따라 구별해 평가한다.
- bounded sources:

  - `comm_001692_제231조_Ⅳ.1_16` / `Ⅳ.1`: “명의자의 명시적인 승낙이나 동의가 없다는 것을 알고 있으면서도 명의자가 문 서작성 사실을 알았다면 승낙하였을 것이라고 기대하거나 예측한 것만으로는 그 승낙이 추정된다고 단정할 수 없다. 따라서 이 경우에도 고의는 인정된다.”

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

## 36. `art231_sec4_1.intent_awareness_and_realization`

- proposition: 사문서위조·변조죄의 고의가 성립하려면 타인 명의 문서라는 인식 및 권리·의무 또는 사실증명 문서를 위조 또는 변조한다는 인식과 실현의사가 인정되어야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 고의의 인식 및 실현의사 요건을 별도 평가 입력으로 유지한다.
- bounded sources:

  - `comm_001692_제231조_Ⅳ.1_16` / `Ⅳ.1`: “본죄가 성립하려면 타인명의의 문서라는 인식을 하고, 권리·의무 또는 사실증명 에 관한 문서를 위조 또는 변조한다는 인식과 실현의사가 인정되어야 한다.”

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

## 37. `art231_sec4_2.genuine_document_utility_purpose`

- proposition: 본래 용법에 따른 진정문서로 사용할 목적이 없더라도 진정문서로서 효용을 갖게 할 목적이 있으면 행사할 목적에는 충분하다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 본래 용법에 따른 사용 목적이 없는 사안에서 진정문서로서의 효용을 갖게 하려는 목적의 인정 여부를 검토한다.
- bounded sources:

  - `comm_001692_제231조_Ⅳ.2_17` / `Ⅳ.2`: “본래 의 용법에 따른 진정문서로 사용할 목적이 없더라도 진정문서로서의 효용을 가 지도록 할 목적이 있으면 충분하다.”

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

## 38. `art231_sec4_2.purpose_of_use_broader_than_exercise`

- proposition: 행사할 목적에서의 행사는 위조문서행사죄의 행사와 반드시 같은 의미가 아니므로, 행사라고 할 수 없는 경우에도 행사할 목적이 인정될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 구체적 사안에서 행사할 목적을 인정할 수 있는지는 위조문서행사죄의 행사 여부와 구별하여 평가한다.
- bounded sources:

  - `comm_001692_제231조_Ⅳ.2_17` / `Ⅳ.2`: “본죄의 행사할 목적에서 ‘행사’는 위조문서행사죄의 ‘행사’와 반드시 같은 의미는 아니므로, 행사라고 할 수 없는 경우에도 행사할 목적이 인정될 수 있다.”

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

## 39. `art231_sec5.attempt_commencement_and_incompletion`

- proposition: 위조·변조 의사를 확정적으로 문서에 표시하면 실행의 착수가 있고, 일반인으로 하여금 진정문서라고 오신할 정도에 이르지 못한 때에는 미수죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 문서 표시가 확정적인지 및 일반인의 진정문서 오신 가능성에 이르지 못했는지는 사실관계에 대한 평가를 필요로 한다.
- bounded sources:

  - `comm_001692_제231조_Ⅴ_18` / `Ⅴ`: “실행의 착수는 위조·변조 의사를 확정적으로 문서에 표시하는 행위가 있는 때 이고, 일반인으로 하여금 진정문서라고 오신할 정도에 이르지 못한 때에는 미수 죄가 성립한다.”

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

## 40. `art231_sec5.attempt_punishable`

- proposition: 사문서위조·변조죄의 미수범은 처벌된다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 형법 제235조를 인용한 commentary 내 법문 설명에 근거한 미수 처벌 규정이다.
- bounded sources:

  - `comm_001692_제231조_Ⅴ_18` / `Ⅴ`: “본죄의 미수범은 처벌한다. (형법 제235조)”

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

## 41. `art231_sec6.deceived_nominee_true_content_fraud`

- proposition: 명의인에게 문서 내용을 진실하다고 속여 작성하게 한 뒤 그 문서를 취득한 경우에는 사문서위조·변조죄가 아니라 사기죄를 구성한다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 명의인에게 진실한 내용이라고 속여 작성하게 하고 문서를 취득한 경우에 한정된 사문서위조·변조죄의 배제 설명으로 검토한다.
- bounded sources:

  - `comm_001692_제231조_Ⅵ_19` / `Ⅵ`: “그 내용을 진실한 것이라고 속여 작성하게 한 다음 그 문서를 취득한 때에는 사기죄를 구성한다.”

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

## 42. `art231_sec6.illiterate_nominee_unknown_content`

- proposition: 문맹인 명의인을 이용해 문서를 작성하게 한 경우 명의인이 문서 내용을 모르고 작성하였다면 사문서위조·변조죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 명의인의 문서 내용 인식 여부는 사실관계에 따라 평가가 필요하다.
- bounded sources:

  - `comm_001692_제231조_Ⅵ_19` / `Ⅵ`: “문맹인 명의인을 이용하여 문서를 작성하게 한 경우 명의인이 문서의 내용을 모르고 문서를 작성한 때에는 본죄가 성립”

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

## 43. `art231_sec6.own_document_altered_in_anothers_possession`

- proposition: 타인의 수중에 있는 자기 명의 문서의 내용을 임의로 변경한 경우에는 문서손괴죄만 성립한다는 것이 통설과 판례이다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 통설과 판례로 보고된 문서손괴죄만 성립한다는 설명은 primary precedent index 확인이 필요하다.
- bounded sources:

  - `comm_001692_제231조_Ⅵ_19` / `Ⅵ`: “타인의 수중에 있는 자기 명의 문서의 내용을 임의로 변경하는 경우 문서손괴죄만 성 립한다는 것이 통설, 판례이다”

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

## 44. `art231_sec6.seal_forgery_absorbed`

- proposition: 행사할 목적으로 타인의 인장을 위조하고 그 인장으로 타인의 사문서를 위조한 경우 인장위조죄는 사문서위조죄에 흡수되어 별도로 성립하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 인장위조와 그 인장을 사용한 타인의 사문서위조가 함께 있는 경우에 한정된 흡수 관계로 검토한다.
- bounded sources:

  - `comm_001692_제231조_Ⅵ_19` / `Ⅵ`: “행사할 목적으로 타인의 인장을 위조하고 그 위조한 인장을 사용하여 권리·의무 또는 사실증명에 관한 타인의 사문서를 위조한 경우 인장위조죄는 사문서위조죄에 흡수되고 따로 인장위조죄 가 성립하는 것은 아니다.”

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
