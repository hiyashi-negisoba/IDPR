# 사문서등위조·변조 RuleIR 카드 검수 1

- unit: `private_document_forgery`
- articles: art231
- cards: 1–15 / 44
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 1. `art231_sec1.element.object_and_purpose`

- proposition: 타인의 권리·의무 또는 사실증명에 관한 문서 또는 도화를 행사할 목적으로 위조 또는 변조한 경우 본죄가 성립한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 제공된 해설 문구에 따른 본죄의 객체·행사목적·위조 또는 변조 요건을 함께 기록한 초안 카드다.
- bounded sources:

  - `comm_001692_제231조_Ⅰ_0` / `Ⅰ`: “본죄는 행사할 목적으로 권리·의무 또는 사실증명에 관한 타인의 문서 또는 도 화를 위조 또는 변조하는 경우에 성립한다.”

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

## 2. `art231_sec2_1.document_copy`

- proposition: 전자복사기·모사전송기 등으로 복사한 문서 사본 및 그 재사본은 원본과 동일한 의미를 가지는 문서로서 문서위조죄 및 행사죄의 객체가 될 수 있다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 주석에 인용된 형법 제237조의2의 사본 및 재사본 취급을 정리한 카드다.
- bounded sources:

  - `comm_001692_제231조_Ⅱ.1_3` / `Ⅱ.1`: “형법 제237조의2에 따라 전자복사기, 모사전송기 기타 이와 유사한 기기를 사용 하여 복사한 문서의 사본도 문서원본과 동일한 의미를 가지는 문서로서 이를 다시 복사한 문서의 재사본도 문서위조죄 및 동 행사죄의 객체인 문서에 해당”

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

## 3. `art231_sec2_1.fact_certification_classification`

- proposition: 문서가 거래상 중요한 사실을 증명하는 문서인지 여부는 제목만이 아니라 문서 내용, 작성자 의도, 작성의 객관적 상황, 적시사항과 행사예정 상대방의 관계를 종합하여 판단한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 열거된 사정을 종합하는 평가 기준이므로 기계적으로 결정하지 않는다.
- bounded sources:

  - `comm_001692_제231조_Ⅱ.1_2` / `Ⅱ.1`: “이에 해당하는지 여부는 문서의 제목만을 고려할 것이 아니라 문서의 내용 과 더불어 문서 작성자의 의도, 그 문서가 작성된 객관적인 상황, 문서에 적시된 사항과 그 행사가 예정된 상대방과의 관계 등을 종합적으로 고려하여 판단하여야 한다.”

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

## 4. `art231_sec2_1.fact_certification_document`

- proposition: 사실증명에 관한 문서는 권리·의무에 관한 문서 외에 거래상 중요한 사실을 증명하는 문서이며, 사회생활상 모든 사실증명 문서가 아니라 중요한 사실을 증명하는 문서에 한정된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 거래상 중요한 사실인지의 평가는 별도 사실 판단이 필요하다.
- bounded sources:

  - `comm_001692_제231조_Ⅱ.1_2` / `Ⅱ.1`: “사실증명에 관한 문서란 권리·의무에 관한 문서 이외의 문서로서 거래상 중요 한 사실을 증명하는 문서이다. 따라서 일반적으로 사회생활에 있어서 사실을 증명하는 모든 문서가 여기에 포함되는 것은 아니며, 중요한 사실을 증명하는 문서에 한한다.”

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

## 5. `art231_sec2_1.indirectly_related_important_fact_document`

- proposition: 거래상 중요한 사실을 증명하는 문서에는 직접 법률관계와 간접적으로만 연관되거나 권리·의무 변동에 사실상 영향을 줄 수 있는 의사표시 문서도 포함될 수 있으나, 단순한 개인적·집단적 의견표현에 그쳐서는 안 되고 구체적 권리·의무와의 관련성이 있어야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 간접적 관련성과 구체적 권리·의무 관련성은 문서별 평가가 필요하며, 보고된 판례 근거는 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제231조_Ⅱ.1_2` / `Ⅱ.1`: “거래상 중요한 사실을 증명하는 문서는, 법률관계의 발생·존속·변경·소멸의 전후 과정을 증명하는 것이 주된 취지인 문서뿐만 아니라 직접적인 법률관계에 단지 간 접적으로만 연관된 의사표시 내지 권리·의무의 변동에 사실상으로만 영향을 줄 수 있는 의사표시를 내용으로 하는 문서도 포함될 수 있다.”
  - `comm_001692_제231조_Ⅱ.1_2` / `Ⅱ.1`: “그러나 문서의 주된 취지 가 단순히 개인적·집단적 의견의 표현에 불과한 것이어서는 안되고, 적어도 실체 법 또는 절차법에서 정한 구체적인 권리·의무와의 관련성이 인정되는 경우이어야 한다.”

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

## 6. `art231_sec2_1.political_signature_list_excluded`

- proposition: 허무인 명의 서명부의 주된 취지가 특정 대통령후보자에 대한 정치적 지지의사를 집단적으로 표현하는 데에 불과한 경우, 구체적 권리·의무 문서나 거래상 중요한 사실을 증명하는 문서로 보기 어렵다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 정치적 지지의사 표현을 주된 취지로 한 허무인 명의 서명부에 관한 좁은 보고된 판단이다.
- bounded sources:

  - `comm_001692_제231조_Ⅱ.1_3` / `Ⅱ.1`: “허무인 명의로 작성된 서명부 21장의 주된 취지가 특정한 대통령후보자에 대한 정치적인 지지의사를 집단적 형태로 표 현하고자 한 것일 뿐인 경우는 실체법 또는 절차법에서 정한 구체적인 권리·의무에 관한 문서 내지 거래상 중요한 사실을 중명하는 문서에 해당한다고 보기 어렵다.”

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

## 7. `art231_sec2_1.right_duty_document`

- proposition: 권리·의무에 관한 문서는 권리·의무의 발생·변경·소멸에 관한 사항을 기재한 문서이다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 권리·의무 문서의 정의를 문서 기재사항 기준으로 정리한 카드다.
- bounded sources:

  - `comm_001692_제231조_Ⅱ.1_2` / `Ⅱ.1`: “권리·의무에 관한 문서란 권리·의무의 발생·변경·소멸에 관한 사항을 기재한 문서를 의미한다.”

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

## 8. `art231_sec2_2.drawing_definition_and_artwork_exclusion`

- proposition: 도화는 상형적 부호로 의사표시 또는 내용을 판단할 수 있도록 기재한 물체이고, 사람의 관념 또는 의사가 화체되어 표현될 것을 요하므로 순수 미술작품으로서의 회화는 도화에 해당하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 도화 해당성은 상형적 부호, 의사표시 또는 내용 판단 가능성, 관념 또는 의사의 화체 여부를 기준으로 검토한다. 순수 미술작품으로서의 회화는 명시적으로 제외된다.
- bounded sources:

  - `comm_001692_제231조_Ⅱ.2_4` / `Ⅱ.2`: “도화는 상형적 부호로써 의사표시 또는 내용을 판단할 수 있도록 기재한 물체 를 말한다.”
  - `comm_001692_제231조_Ⅱ.2_4` / `Ⅱ.2`: “사람의 관념 내지 의사가 화체되어 표현될 것을 요하므로 순수한 미술작품으로서의 회화는 도화에 해당하지 않는다.”

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

## 9. `art231_sec3_1.authority_determination`

- proposition: 작성명의인의 작성권한 침해 여부 및 작성권한의 유무는 법규, 계약, 거래관행 및 당사자 의사 등을 고려하여 개별적·구체적으로 판단한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 작성권한 및 그 침해 여부는 법규, 계약, 거래관행 및 당사자 의사를 사실관계별로 평가해야 한다.
- bounded sources:

  - `comm_001692_제231조_Ⅲ.1_5` / `Ⅲ.1`: “위조에 해당하려면 작성명의인의 작성권한이 침해되어야 하는데, 작성권한의 유 무는 법규·계약·거래관행·당사자의 의사 등을 고려하여 개별적·구체적으로 판 단하여야 한다.”

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

## 10. `art231_sec3_1.fictitious_or_deceased_nominee`

- proposition: 사문서에서 명의인이 실재하지 않는 허무인이거나 작성일 전에 사망하였더라도, 그러한 문서가 공공의 신용을 해할 위험성이 있으면 본죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 공공의 신용을 해할 위험성 및 commentary가 보고한 판시의 원문·적용범위를 검토해야 한다.
- bounded sources:

  - `comm_001692_제231조_Ⅲ.1_6` / `Ⅲ.1`: “사문서의 경우에도 공문서와 같이 명의인이 실재하지 않는 허무인이거나 또는 문서의 작성일자 전에 이미 사망하 였더라도 그러한 문서 역시 공공의 신용을 해할 위험성이 있으므로 본죄가 성 립한다고 판시함으로써, 위의 어느 경우건 본죄가 성립하게 되었다.”

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

## 11. `art231_sec3_1.forgery_definition`

- proposition: 문서위조는 작성권한 없는 자가 타인 명의의 문서를 작성하는 행위이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 작성권한의 유무는 별도 판단기준 카드에 따라 검토한다.
- bounded sources:

  - `comm_001692_제231조_Ⅲ.1_5` / `Ⅲ.1`: “문서위조는 작성권한 없는 자가 타인 명의의 문서를 작성하는 것을 말한다”

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

## 12. `art231_sec3_2.authority_abuse`

- proposition: 타인의 대표자·대리자 또는 본인 명의로 문서를 작성할 권한이 있는 자가 그 지위를 남용하여 자기나 제3자의 이익을 위해 문서를 작성하더라도 문서위조죄는 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 문서작성 권한의 존재와 대표·대리 지위 남용의 사실관계를 구별하여 검토한다.
- bounded sources:

  - `comm_001692_제231조_Ⅲ.2_10` / `Ⅲ.2`: “타인의 대표자 또는 대리자가 그 대표 명의 또는 대리 명의를 써서 또는 직접 본인 명의를 사용하여 문서를 작성할 권한을 가지는 경우에 그 지위를 남용하여 단순히 자기 또는 제3자의 이익을 도모할 목 적으로 마음대로 그 대표자, 대리 명의 또는 직접 본인 명의로 문서를 작성하였 더라도 문서위조죄는 성립하지 않는다.”

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

## 13. `art231_sec3_2.authorized_creation`

- proposition: 명의자의 명시적 또는 묵시적 승낙·위임이 있는 경우에는 타인 명의 문서 작성이라도 사문서위조에 해당하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 명시적 또는 묵시적 승낙·위임의 존재와 그 범위는 문서작성 경위에 따라 검토한다.
- bounded sources:

  - `comm_001692_제231조_Ⅲ.2_8` / `Ⅲ.2`: “전세계약서를 작성하는 데에 그 명의자의 명시적 이거나 묵시적인 승낙(위임)이 있는 경우에는 사문서위조에 해당하지 않는다.”

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

## 14. `art231_sec3_2.comprehensive_delegation`

- proposition: 명의자가 문서작성 관련 사무처리 권한을 포괄적으로 위임하고 작성자가 위임 범위 내에서 그 사무처리를 위해 명의자 명의 문서를 작성·행사한 경우, 개별 문서 작성 승낙이 없더라도 특별한 사정이 없는 한 사문서위조 및 행사죄는 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 포괄위임의 존재, 위임 범위 내 작성·행사 여부 및 특별한 사정의 존재를 각각 검토한다.
- bounded sources:

  - `comm_001692_제231조_Ⅲ.2_8` / `Ⅲ.2`: “문서명의인이 문서작성자에게 사전에 문서 작성과 관련한 사무처리의 권한 을 포괄적으로 위임함으로써 문서작성자가 위임된 권한의 범위 내에서 그 사무 처리를 위하여 문서명의인 명의의 문서를 작성·행사한 경우에는, 비록 문서작성 자가 문서명의인으로부터 개개 문서의 작성에 관한 승낙을 받지 않았더라도 특 별한 사정이 없는 한 사문서위조 및 위조사문서행사죄는 성립하지 않는다.”

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

## 15. `art231_sec3_2.document_appearance`

- proposition: 작성 문서가 일반인으로 하여금 명의인의 권한 내에서 작성된 것으로 믿을 수 있는 정도의 형식과 외관을 갖추면 문서위조죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 일반인이 권한 있는 작성으로 믿을 수 있는 형식과 외관의 충족 여부는 개별 문서 사정에 대한 평가를 필요로 한다.
- bounded sources:

  - `comm_001692_제231조_Ⅲ.2_7` / `Ⅲ.2`: “그 작성된 문서가 일반인으로 하여금 당해 명의인의 권한 내에서 작성된 것 이라고 믿을 수 있는 정도의 형식과 외관을 구비하면 성립한다.”

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
