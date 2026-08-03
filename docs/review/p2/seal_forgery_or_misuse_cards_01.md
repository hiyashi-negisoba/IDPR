# 사인등위조·부정사용 RuleIR 카드 검수 1

- unit: `seal_forgery_or_misuse`
- articles: art239
- cards: 1–15 / 19
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 1. `art239_sec1_1.offense_formation`

- proposition: 타인의 인장·서명·기명·기호를 행사할 목적으로 위조하거나 부정사용하면 사인등의 위조·부정사용죄가 성립한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 본 카드의 범위는 타인의 인장·서명·기명·기호를 행사할 목적으로 위조 또는 부정사용하는 경우에 한정된다.
- bounded sources:

  - `comm_001692_제239조_Ⅰ.1_0` / `Ⅰ.1`: “본죄는 행사할 목적으로 타인의 인장·서명·기명·기호를 위조하거나, 부정사용함 으로써 성립하는 범죄이다.”

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

## 2. `art239_sec1_2.private_person_scope`

- proposition: 사인에는 자연인뿐 아니라 법인 및 법인격 없는 단체도 포함된다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 사인의 인적 범위를 자연인, 법인 및 법인격 없는 단체까지 포함하는 정의로 정리한다.
- bounded sources:

  - `comm_001692_제239조_Ⅰ.2_1` / `Ⅰ.2`: “사인은 자연인뿐만 아니라 법인, 법인격 없는 단 체도 포함한다는 점에는 의문이 없다.”

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

## 3. `art239_sec1_3.authenticity_mistake_assessment`

- proposition: 특정인의 진정한 서명으로 오신하기에 충분한지는 인장·서명의 형식과 외관, 작성경위, 현출 문서에서의 인장·서명 필요성, 문서의 작성경위·종류·내용 및 일반거래상 기능을 함께 고려하여 판단한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 오신 가능성 판단의 고려 요소를 제시하는 독립 표준 카드이며, 요소의 충족 여부는 개별 사실관계에서 평가한다.
- bounded sources:

  - `comm_001692_제239조_Ⅰ.3_2` / `Ⅰ.3`: “일반 인이 특정인의 진정한 서명으로 오신하기에 충분한 정도인지 여부는 그 인장 또는 서명의 형식과 외관, 작성경위 등을 고려하여야 할 뿐만 아니라 그 인장 또는 서명이 현출된 문서에 있어서의 인장 현출 또는 서명 기재의 필요성, 그 문서의 작성경위, 종류, 내용 및 일반거래에 있어서 그 문서가 가지는 기능 등도 함께 고려하여 판단하여야 한다.”

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

## 4. `art239_sec1_3.authenticity_mistake_threshold`

- proposition: 사인위조죄 또는 사서명위조죄는 인장이나 서명이 일반인으로 하여금 특정인의 진정한 인장 또는 서명으로 오신하게 할 정도에 이르러야 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 일반인의 오신 가능성은 외관과 거래 맥락에 대한 평가를 요구하므로 standard input으로 검토한다.
- bounded sources:

  - `comm_001692_제239조_Ⅰ.3_2` / `Ⅰ.3`: “사인위조죄 또는 사서명위조죄는 인장이나 서명이 일반인으로 하여금 특정 인의 진정한 인장 또는 서명으로 오신하게 할 정도에 이르러야 성립한다.”

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

## 5. `art239_sec1_3.authorized_manifestation_not_forgery`

- proposition: 명의자로부터 명시적 또는 묵시적 위임이나 승낙을 받아 인장을 현출하거나 서명한 경우에는 권한 없거나 권한을 넘은 것이 아니므로 위조가 성립하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 명시적 또는 묵시적 위임·승낙이라는 권한 부여 사실이 확인된 경우의 위조 불성립 예외로 검토한다.
- bounded sources:

  - `comm_001692_제239조_Ⅰ.3_2` / `Ⅰ.3`: “명의자로부터 명시적 또는 묵시적 위임 또는 승낙을 받아 인장을 현출시키거나 서명을 한 경우에는 권한이 없거나 권한을 넘은 것이 아니어서 위조가 되지 않 는다.”

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

## 6. `art239_sec1_3.deceived_nominee_manifestation_not_improper_use`

- proposition: 행위자가 명의자를 기망하여 그로 하여금 인영 또는 서명을 현출하게 한 뒤 이를 제3자에게 사용하였더라도, 명의자의 권한을 받아 행사한 것이므로 부정사용이 아니다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 명의자의 인영·서명 현출 및 권한 수여가 있었는지, 그리고 사용이 그 권한 범위 안인지 사실관계별 검토가 필요하다.
- bounded sources:

  - `comm_001692_제239조_Ⅰ.3_2` / `Ⅰ.3`: “행위자가 사인 등의 명의자를 기망하여 그로 하여금 인 영 또는 서명을 현출하게 한 다음 그 인영 또는 서명을 제3자에게 사용한 것은 비록 기망이 있었지만 명의자의 권한을 수여받아 행사한 것이기 때문에 부정사 용이라고 할 수 없다.”

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

## 7. `art239_sec1_3.incomplete_document_signature_forgery`

- proposition: 문서가 완성되지 않았어도 현출된 인장 또는 서명이 명의인의 진정한 서명으로 오신할 정도이면 인장 또는 서명위조죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 문서 미완성은 오신 가능성이 있는 인장·서명 위조 성립을 당연히 배제하지 않는다는 범위의 카드다.
- bounded sources:

  - `comm_001692_제239조_Ⅰ.3_2` / `Ⅰ.3`: “문서에 현출된 인장 또는 서명이 명의 인의 진정한 서명으로 오신할 정도에 이르면 일단 인장 또는 서명이 완성된 이 상 문서가 완성되지 아니한 경우에도 인장 또는 서명위조죄는 성립한다.”

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

## 8. `art239_sec1_3.interrogation_record_incomplete_holding`

- proposition: 을로 행세한 피의자가 피의자신문조서 말미에 을의 서명만 기재하여 조서가 미완성인 경우에도, 일반인이 을의 서명으로 현출된 것이라고 오신하기에 충분하면 사서명위조죄가 성립한다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 피의자신문조서의 구체적 미완성 상태와 서명 외관을 전제로 한 commentary-reported holding이므로 원판결 확인 전에는 해당 사실관계 범위에서만 검토한다.
- bounded sources:

  - `comm_001692_제239조_Ⅰ.3_2` / `Ⅰ.3`: “판례는 갑이 을로 행세하면서 피의자로서 조사를 받은 다음 피의자신문조서 말미에 을 의 서명만을 기재한 사안에서 피의자의 간인이나 무인이 끝나지 않았고 조사한 경찰관의 서명날인이 완료되지 않아 경찰관 작성의 피의자신문조서가 완성되지 않은 상태이지만 일반인이 보기에 을의 서명에 의하여 현출된 것이라고 오신하 기에 충분하므로 사서명위조죄는 성립한다고 판시하였다.”

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

## 9. `art239_sec1_3.union_chairman_seal_authority`

- proposition: 연합회 회장이 업무상 필요한 회장 직인을 새로 조각하여 날인한 사안에서, 회장에게 자기 명의 직인을 새길 권한이 있다고 보아 위조를 인정하지 않은 하급심 판례가 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 업무상 필요와 회장의 직인 조각 권한을 인정한 하급심의 개별 사안으로서, 일반적 권한 규칙으로 확대하기 전에 원판결을 확인해야 한다.
- bounded sources:

  - `comm_001692_제239조_Ⅰ.3_2` / `Ⅰ.3`: “하급심 판례로 연합회 회장이 업 무상 필요에 의해 연합회 회장 직인이 필요하였으나 갈등을 빚고 있던 사무국 장이 이를 보관하면서 반환을 거부하자 새로 회장 직인을 조각하여 날인한 사 안에서 회장으로서 업무상 필요에 의해 그 명의의 직인을 새로 새길 권한이 있 다고 보아 위조를 인정하지 않은 것이 있다.”

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

## 10. `art239_sec1_4.future_consent_no_purpose_holding`

- proposition: 타인의 승낙 없이 장차 명의인의 승낙을 얻어 타인 명의 문서 작성에 사용할 의도로 인장을 조각했으나 승낙을 얻지 못해 사용하지 않고 돌려준 경우, 행사의 목적이 인정되지 않는다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 장래 승낙을 얻을 의도, 실제 불승낙, 미사용 및 반환이라는 제한된 사실관계의 소개된 판례이다. 판례 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제239조_Ⅰ.4_4` / `Ⅰ.4`: “판례는 타인의 인장을 조각할 당 시에 타인의 승낙을 얻지 아니한 채 나중에 명의인의 승낙을 얻어 타인 명의의 문서를 작성하는 데 사용할 의도로 인장을 조각하였으나 타인의 승낙을 얻지 못하여 이를 사용하지 아니하고 타인에게 돌려주었다면 행사의 목적이 있었다 고 인정되지 않는다고 판시하였다.”

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

## 11. `art239_sec1_4.intent_awareness`

- proposition: 사인위조의 고의는 타인 명의를 도용하여 인장을 도용한다는 인식을 필요로 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 고의에 필요한 인식 요소를 정리한 카드이며, 개별 행위자의 인식은 사실관계에 따라 평가한다.
- bounded sources:

  - `comm_001692_제239조_Ⅰ.4_4` / `Ⅰ.4`: “먼저 사인위조의 고의가 문제된 사안으로 타인 명의를 도용하여 인장을 도용한 다는 인식이 있어야 할 것인데”

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

## 12. `art239_sec1_4.purpose_of_use`

- proposition: 사인 등의 위조·부정사용에는 행사하려는 의사, 즉 타인의 의사에 반하여 위법하게 사용하려는 행사의 목적이 필요하다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 행사의 목적은 타인의 의사에 반하는 위법한 사용 의도를 포함하는 주관적 요소로 정리한다.
- bounded sources:

  - `comm_001692_제239조_Ⅰ.4_4` / `Ⅰ.4`: “하려는 의사, 즉 행사의 목적이 필요하다. 이때 행사의 목적은 타인의 의사에 반 하여 위법하게 사용하려고 할 것이 요구된다.”

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

## 13. `art239_sec1_4.putative_representative_no_forgery_intent`

- proposition: 대표자 선임결의가 중대·명백한 하자로 무효 또는 부존재가 되었더라도, 형식상 선임절차를 거쳐 대표자가 된 사람이 자신을 정당한 대표자로 믿고 직인을 조각한 경우 사인위조의 고의를 인정하지 않은 사례가 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 대표자 선임절차, 결의 하자의 성격, 정당한 대표자라는 믿음 등 구체적 사실의 평가가 필요하다. 소개된 판례의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제239조_Ⅰ.4_4` / `Ⅰ.4`: “대표자로 선임하게 된 결의에 중대하고도 명백 한 하자가 있어 무효하거나 부존재한 것으로 귀결이 되었다 하더라도 형식상 대표자 선임절차를 밟고 대표자로 된 자는 스스로를 정당한 대표자로 믿고 직 인을 조각하였을 것으로 사인위조의 고의가 있음을 인정하지 아니하였다.”

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

## 14. `art239_sec1_4.union_seal_no_illicit_purpose_holding`

- proposition: 노조지부장 당선이 무효가 된 뒤 인계 거부에 대응하여 지부장직무대리의 승인하에 노조 활동용 지부인 등을 새로 조각한 사안에서, 정당한 인장인 양 가장하려는 부정한 방법의 위조·행사 의사가 없다고 한 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 당선 무효, 기존 인장의 인계 거부, 직무대리 승인 및 노조 활동 목적이라는 제한된 사안의 소개된 판례이다. 판례 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제239조_Ⅰ.4_4` / `Ⅰ.4`: “그리고 노동조합지부 지부장으로 당선되었 던 갑이 그 당선이 무효로 된 뒤에도 계속하여 지부인 및 지부장인의 인계를 거 부하자 이에 대한 대응책으로 을이 지부장직무대리 병의 승인 하에 노조지부의 활동에 사용하기 위하여 새로 지부인 및 지부장인을 조각한 사안에서 을이 부 정한 방법으로 정당한 인장인 양 가장하기 위하여 직인 등을 위조하거나 행사 할 의사가 있었다고 볼 수 없다고 판시하기도 하였다.”

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

## 15. `art239_sec1_5.foreign_national_overseas_jurisdiction`

- proposition: 사인위조죄는 형법 제6조의 대한민국 또는 대한민국국민에 대하여 범한 죄에 해당하지 아니하므로, 중국 국적의 피고인이 중국에서 대한민국 국적 주식회사의 인장을 위조한 공소사실에 대하여는 외국인의 국외범으로서 피고인에 대한 재판권이 없다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 댓글에 보고된 판례 입장이다. 적용 전 판례 원문 및 사실관계가 대한민국 국적 주식회사 명의 인장과 중국 내 위조라는 범위에 한정되는지 확인해야 한다.
- bounded sources:

  - `comm_001692_제239조_Ⅰ.5_5` / `Ⅰ.5`: “사인위조죄는 형법 제6조의 대한민국 또는 대한민국국민에 대하여 범한 죄에 해당하지 아니하므로 중국 국적의 피고인이 중국에서 대한민국 국적 주식회사 의 인장을 위조하였다는 공소사실은 외국인의 국외범으로서 피고인에 대하여 재판권이 없다.”

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
