# 위계공무집행방해 RuleIR 카드 검수 1

- unit: `deceptive_obstruction_of_official_duty`
- articles: art137
- cards: 1–15 / 50
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 1. `art137.blood_evidence_substitution`

- proposition: 음주운전 교통사고 후 형사처벌을 면하려고 타인의 혈액을 자신의 혈액처럼 경찰관에게 제출하여 감정하게 한 행위는 수사기관 착오를 이용한 적극적 증거조작으로 본죄가 성립한다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 타인 혈액 제출, 수사기관 착오 이용 및 적극적 증거조작의 사실적 연결을 검토해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.2_12` / `Ⅳ.2`: “음주운전을 하다가 교통사고를 야기한 후 그에 대한 형사처벌을 면하기 위하 여 타인의 혈액을 자신의 혈액인 것처럼 교통사고 조사 경찰관에게 제출하여 감정하도록 한 행위는, 단순히 피의자가 수사기관에 대하여 허위사실을 진술하 거나 자신에게 불리한 증거를 은닉하는 데 그친 것이 아니라 수사기관의 착오 를 이용하여 적극적으로 피의사실에 관한 증거를 조작한 것으로서, 본죄가 성립 한다고 판단하였다.”

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

## 2. `art137.fabricated_evidence_undetectable`

- proposition: 피의자 등이 적극적으로 허위증거를 조작·제출하여 충실한 수사에도 그 허위가 발견되지 못할 정도에 이른 경우, 수사행위를 적극적으로 방해한 것으로서 위계에 의한 공무집행방해죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 증거조작의 적극성, 충실한 수사에도 허위 발견이 곤란한 정도 및 수사방해를 검토해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.2_15` / `Ⅳ.2`: “피의자 등이 적극적으로 허위의 증거를 조작”
  - `comm_001692_제137조_Ⅳ.2_15` / `Ⅳ.2`: “하여 제출하고 그 증거 조작의 결과 수사기관이 그 진위에 관하여 나름대로 충”
  - `comm_001692_제137조_Ⅳ.2_15` / `Ⅳ.2`: “실한 수사를 하더라도 제출된 증거가 허위임을 발견하지 못할 정도에 이르렀다”
  - `comm_001692_제137조_Ⅳ.2_15` / `Ⅳ.2`: “면, 이는 위계에 의하여 수사기관의 수사행위를 적극적으로 방해한 것으로서 위”
  - `comm_001692_제137조_Ⅳ.2_15` / `Ⅳ.2`: “계공무집행방해죄가 성립된다고 보았다.”

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

## 3. `art137.fabricated_gift_ledger_bribery_investigation`

- proposition: 뇌물수수 혐의 수사 직전에 기증물관리대장을 조작하고 담당직원에게 정상적 기증 및 관리의 외관에 관한 허위진술을 지시한 행위는 단순 허위진술이나 증거은닉을 넘어 적극적 증거조작으로서 위계에 의한 공무집행방해죄에 해당한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 대장 조작과 허위진술 지시가 적극적 증거조작에 해당하는지 및 수사 대상 사실과의 관련성을 검토해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.2_14` / `Ⅳ.2`: “대법원은 피고인 2가 뇌물수수 사건의 조사 직전에 기증물관리대장을 조작하도록 지시하고 담당직원으로 하여금 동양 화 1점을 정상적인 절차에 따라 기증받아 종전부터 존재하는 기증물관리대장에 등재하여 관리하고 있는 것처럼 허위의 진술을 하도록 지시한 행위는, 단순히 수사기관에 대하여 허위사실을 진술하거나 자신에게 불리한 증거를 은닉하는 데 그친 것이 아니라 적극적으로 피의사실에 관한 증거를 조작한 것으로 볼 수 있으므로, 본죄에 해당한다고 판단하였다.”

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

## 4. `art137.false_industrial_service_dispatch_approval`

- proposition: 지정업체에서 산업기능요원으로 근무할 의사 없이 허위 편입신청서를 제출하고, 실태조사를 회피하려 허위서류로 파견근무 승인을 받은 경우, 승인 결과가 불충분한 심사가 아니라 출원인의 위계행위에 기인한 것으로서 위계에 의한 공무집행방해죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 허위 편입신청과 파견근무 승인 사이의 인과관계 및 관할관청 심사의 충분성을 검토해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.2_14` / `Ⅳ.2`: “대법원은 지정업체에서 산업기능요원으로 근무할 의 사가 없음에도 해당 지정업체의 장과 공모하여 허위내용의 편입신청서를 제출 하여 관할관청으로부터 산업기능요원 편입을 승인받고 나아가 관할관청의 실태 조사를 회피하기 위하여 허위서류를 작성·제출하는 등의 방법으로 파견근무를 신청하여 관할관청으로부터 파견근무를 승인받았다면, 이러한 파견근무의 승인 등은 관할관청의 불충분한 심사가 원인이 된 것이 아니라 출원인의 위계행위가 원인이 된 것이어서 본죄가 성립한다고 판단하였다.”

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

## 5. `art137.false_medical_certificate_taxi_transfer`

- proposition: 개인택시 양도·양수 인가에서 행정청이 사회적 신용성이 보장된 의사 진단서를 신뢰하여 인가한 경우, 사후 진단서 허위가 밝혀져도 충분한 심사가 있었고 인가는 출원인의 위계에 의한 것이므로 본죄가 성립한다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 진단서의 사회적 신용성, 심사의 충분성 및 허위자료와 인가 사이의 인과관계를 검토해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.2_12` / `Ⅳ.2`: “이 경우 허가관청이 개인택시운송사업의 양도·양수에 대한 인가처분을 하게 된 것은 허가관청의 불충분한 심사에 의한 것이 아니라 출원인의 위계에 의한 것으로서 본죄가 성립한다고 판단하였다.”

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

## 6. `art137.false_notification_lax_review`

- proposition: 신고 내용의 허위나 법령 취지 위반을 충분한 확인으로 발견할 수 있었는데도 행정청이 이를 따져보지 않고 경솔하게 처분한 경우에는 신고인의 위계에 의한 결과로 볼 수 없어 위계에 의한 공무집행방해죄가 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 행정청이 충분한 확인을 했다면 허위 또는 법령 취지 위반을 발견할 수 있었는지 검토해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.2_8` / `Ⅳ.2`: “행정청이 나름대로 충분히 사실관계를 확인하더라도 그 신고내용이 허 위이거나 법령의 취지에 맞지 아니함을 발견할 수 없었던 경우가 아니라면 심 사를 담당하는 행정청이 신고내용이나 자료의 진실성을 충분히 따져보지 아니 한 채 경솔하게 이를 믿고 어떠한 행위나 처분에 나아갔다고 하여 이를 신고인 의 위계에 의한 결과로 볼 수 없으므로 본죄는 성립하지 아니한다고 판시하였다.”

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

## 7. `art137.false_report_no_concrete_obstruction_exception`

- proposition: 적법하게 사업을 영위하는 자가 신고 과정에서 허위사실과 허위서류를 제출했더라도 구체적·현실적 직무집행 방해가 없고, 행정청의 진위 미조사 결과를 허위신고로 인한 것으로 보기 어렵다면 본죄가 성립하지 않는다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 구체적·현실적 직무집행 방해 및 행정청의 진위 미조사와의 관계를 사례별로 검토해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.2_10` / `Ⅳ.2`: “이미 허가를 받아 적법하게 사업을 영위하는 피고인이 신고를 하는 과정에 서 신고서에 허위사실을 기재하고 그에 관한 허위의 서류를 첨부하여 제출하였 더라도, 이로써 곧 구체적이고 현실적인 직무집행이 방해받았다고 볼 수 없을 뿐 아니라”

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

## 8. `art137.false_special_naturalization_materials`

- proposition: 특별귀화 신청에서 부모의 국적취득을 적법한 것처럼 허위 기재하고 허위 친속관계공증서를 제출하여 담당공무원의 심사사항에 관한 오인·착각·부지를 일으켜 특별귀화허가를 받은 경우 위계에 의한 공무집행방해죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 허위 기재·공증서가 심사대상 사항의 오인·착각·부지를 초래했는지 및 발견 곤란성을 검토해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.2_16` / `Ⅳ.2`: “피고인이 특별귀화허가를 신청하면서 피고인의 부모가 적법하게 대한민국 국적을 취득한 것처럼 부모의 인적사항을 허위로 기재하고 허위의 친속관계공증서 등을 제출하여 담당공무원의 심사대상인 사항에 관하여 공무원의 오인, 착각, 부지를 일으킴으로써 이를 발견하 기 어려웠던 담당공무원으로부터 특별귀화허가를 받았다면, 이는 피고인의 적극적 인 위계에 의한 것으로써 위계에 의한 공무집행방해죄가 성립한다고 판단하였다.”

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

## 9. `art137.false_statement_in_judicial_investigative_proceedings`

- proposition: 재판 또는 수사절차의 당사자·피고인·피의자·참고인이 허위진술 또는 허위자백을 한 것만으로는 위계에 의한 공무집행방해죄가 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 단순 허위진술·허위자백과 적극적 증거조작을 구별하여 검토해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.2_7` / `Ⅳ.2`: “따라서 당사자나 피고인이 법원에 대하여 허위진술을 하거나 또는 수사기관에 대하여 피의자가 허위자백을 하거나 참고인이 허위진술을 한 것만으로는 본죄가 성립 한다고 할 수 없다.”

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

## 10. `art137.insider_official_deception_approval`

- proposition: 심사업무 담당공무원이 출원사유 허위를 알면서 결재권자를 오인·착각·부지에 빠뜨려 인허가 결재를 받은 경우, 출원인의 허위자료 제출과 달리 적정한 심사업무를 기대할 수 없으므로 결재권자의 직무집행 방해가 된다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 심사업무 담당자의 인식, 결재권자의 오인 및 적정 심사업무 기대 가능성을 검토해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.2_11` / `Ⅳ.2`: “출원에 대한 심사업무를 담당하는 공무원이 출원인의 출원사유가 허위라는 사실을 알면서도 결재권자로 하여금 오인, 착각, 부지를 일으키게 하고 그 오인, 착각, 부지를 이용하여 인·허가처분에 대한 결재를 받아낸 경우라면”

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

## 11. `art137.insufficient_investigation_false_statement`

- proposition: 피의자 등의 허위진술, 증거은닉 또는 허위증거 제출만으로 수사기관이 충분한 수사 없이 이를 믿고 수사를 마친 경우에는 수사기관의 불충분한 수사에 기인한 것이므로 위계에 의한 공무집행방해죄가 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 수사의 충분성 및 수사 종결이 허위행위가 아닌 수사기관의 불충분한 수사에 기인했는지 검토해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.2_15` / `Ⅳ.2`: “피의자 등이 수사기관에 대하여 허위사실을 진술하거나 피의”
  - `comm_001692_제137조_Ⅳ.2_15` / `Ⅳ.2`: “사실 인정에 필요한 증거를 감추고 허위의 증거를 제출하였더라도, 수사기관이 충분한 수사를 하지 아니한 채 이와 같은 허위의 진술과 증거만으로 증거의 수”
  - `comm_001692_제137조_Ⅳ.2_15` / `Ⅳ.2`: “집·조사를 마쳤다면, 이는 수사기관의 불충분한 수사에 의한 것으로서 피의자 등의 위계에 의하여 수사가 방해되었다고 볼 수 없어 위계에 의한 공무집행방”
  - `comm_001692_제137조_Ⅳ.2_15` / `Ⅳ.2`: “해죄가 성립된다고 할 수 없지만”

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

## 12. `art137.notification_general_rule`

- proposition: 행정청의 처분을 예정하지 않고 신고만으로 법률효과가 완성되는 신고에서 허위사실이나 허위 소명자료를 제출한 행위는 원칙적으로 위계에 의한 공무집행방해죄를 구성하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 해당 신고가 행정청 처분을 예정하지 않는 자기완결적 신고인지 법령 및 절차에 따라 검토해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.2_8` / `Ⅳ.2`: “신고는 사인이 행정청에 대하여 일정한 사실 또는 관념을 통지함으로 써 공법상 법률효과가 발생하는 행위로서 원칙적으로 행정청에 대한 일방적 통 고로 그 효과가 완성될 뿐 이에 대응하여 신고내용에 따라 법률효과를 부여하 는 행정청의 행위나 처분을 예정하고 있지 아니하므로, 신고인이 허위사실을 신 고서에 기재하거나 허위의 소명자료를 첨부하여 제출하였더라도”

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

## 13. `art137.notification_substantively_permit_application_exception`

- proposition: 법령상 신고라는 용어를 사용하더라도 실질적으로 인허가 등 처분의 신청행위와 다름없는 예외적 경우에는 위계에 의한 공무집행방해죄가 성립할 여지가 있다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 신고의 명칭과 별개로 실질적으로 인허가 등 처분의 신청행위인지 검토해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.2_8` / `Ⅳ.2`: “다만 관계 법령이 비록 신 고라는 용어를 사용하고 있더라도 사실상 인허가 등 처분의 신청행위와 다를 바 없다고 평가되는 등의 예외적인 경우에는 본죄가 성립할 여지가 있으나”

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

## 14. `art137.permit_false_application_insufficient_review`

- proposition: 행정관청이 신청사유나 소명자료를 충분히 확인하지 않고 믿어 인허가처분을 한 경우, 그 처분은 행정관청의 불충분한 심사에 기인하므로 신청인의 위계에 의한 공무집행방해죄가 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 관계 법령상 요구되는 심사 범위와 실제 심사의 충분성을 검토해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.2_7` / `Ⅳ.2`: “행정관청이 사실을 충 분히 확인하지 아니한 채 사실에 부합하지 아니하는 신청인 제출의 신청사유나 소명자료를 가볍게 믿고 인·허가처분을 하였다면, 이는 행정관청의 불충분한 심 사에 기인한 것이지 신청인의 위계에 의한 것이라고 볼 수 없기 때문에 본죄가 성립하지 아니한다.”

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

## 15. `art137.permit_false_materials_undetectable`

- proposition: 행정관청이 인허가 요건을 충분히 심사했음에도 허위 신청사유나 허위 소명자료를 발견하지 못하여 인허가처분을 한 경우, 신청인의 위계로 인한 것으로서 위계에 의한 공무집행방해죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 충분한 심사에도 허위자료를 발견하지 못한 경우인지 및 위계와 처분의 인과관계를 검토해야 한다.
- bounded sources:

  - `comm_001692_제137조_Ⅳ.2_7` / `Ⅳ.2`: “당사자가 행정관청에 사실과 다른 신청사유를 제출하면서 이에 부합하는 허위 의 소명자료를 첨부한 경우 행정관청이 관계법령에 따라 인·허가 요건에 해당 하는지 충분히 심사하였음에도 신청사유나 그 소명자료가 허위임을 발견하지 못하여 인·허가처분을 하게 되었다면, 이는 행정관청의 불충분한 심사로 인한 것이 아니라 신청인의 위계에 의한 것이라 할 수 있으므로, 본죄가 성립한다고 보아야 한다.”

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
