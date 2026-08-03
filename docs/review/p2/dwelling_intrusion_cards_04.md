# 주거침입·퇴거불응 RuleIR 카드 검수 4

- unit: `dwelling_intrusion`
- articles: art319
- cards: 46–60 / 104
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #30 `art319_sec2_1.dwelling_concept`: `art319_sec2_1.dwelling_concept_sleeping` (status=`valid`)
- #31 `art319_sec5_2.private_arrest_home_entry`: `art319_sec5_2.private_arrest_home_entry_affirmative` (status=`valid`)

## 46. `art319_sec3_1.intrusion_objective_peace`

- proposition: 침입은 거주자가 주거에서 누리는 사실상의 평온상태를 해치는 행위태양으로 주거에 들어가는 것을 의미하며, 침입 여부는 출입 당시 객관적·외형적으로 드러난 행위태양을 기준으로 판단하는 것이 원칙이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 전원합의체로 보고된 객관적·외형적 평온침해 기준이다.
- bounded sources:

  - `comm_001692_제319조_Ⅲ.1_19` / `Ⅲ.1`: “‘침입’이란 거주자가 주거에서 누리는 사실상의 평온상태를 해치는 행위태양으로 주거에 들어가는 것을 의미하고, ‘침입’에 해당하는지 여부는 출입 당시 객관적·외형적으로 드러난 행위태양을 기준으로 판단함이 원칙이며”
  - `comm_001692_제319조_Ⅲ.1_30` / `Ⅲ.1`: “침입은 ‘거주자가 주거에서 가) 누리는 사실상의 평온상태를 해치는 행위태양으로 주거에 들어가는 것’을 의미 하고, 침입에 해당하는지 여부는 출입 당시 객관적·외형적으로 드러난 행위태양 을 기준으로 판단함이 원칙이다.”

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

## 47. `art319_sec3_1.intrusion_subjective_opposition_insufficient`

- proposition: 단순히 주거 등의 출입이 거주자 등의 의사에 반한다는 주관적 사정만으로는 바로 침입에 해당하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 거주자 의사는 독립적·결정적 기준이 아니라 평온침해 평가 요소로 검토한다.
- bounded sources:

  - `comm_001692_제319조_Ⅲ.1_19` / `Ⅲ.1`: “단순히 주거에 들어가는 행위 자체 가 거주자의 의사에 반한다는 주관적 사정만으로 바로 ‘침입’에 해당한다고 볼 수 없다고 판시하였다.”
  - `comm_001692_제319조_Ⅲ.1_30` / `Ⅲ.1`: “단순히 주거 등에 들어가는 행위 자체가 거주자 등의 의사 에 반한다고 하여 바로 침입에 해당한다고 볼 수 없다.”

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

## 48. `art319_sec3_1.minor_child_consent`

- proposition: 피해자의 미성년 자녀의 허락을 받고 피해자 주거에 출입한 경우, 피해자 부재 중 그 의사에 반한다는 사정만으로 주거침입죄가 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 자녀의 현실적 거주 및 허락 경위를 확인한다.
- bounded sources:

  - `comm_001692_제319조_Ⅲ.1_24` / `Ⅲ.1`: “피고인이 피해자의 미성년 자녀(당시 만 14세)의 허락 을 받고 피해자의 주거에 출입한 경우, 부재중인 피해자의 의사에 반하는 사정 만으로 주거침입죄가 성립하지 않는다고 판단”

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

## 49. `art319_sec3_1.no_contemporaneous_resistance`

- proposition: 침입 판단에서 출입 당시 반드시 현실적 저항이나 구체적 제지가 있을 필요는 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 출입금지 통지 및 당시 객관적 상황을 별도 확인한다.
- bounded sources:

  - `comm_001692_제319조_Ⅲ.1_22` / `Ⅲ.1`: “출입 당시 반드시 어떠한 저항을 받을 것을 요하지는 않는다.”
  - `comm_001692_제319조_Ⅲ.1_22` / `Ⅲ.1`: “비록 대학교에 들 어갈 때 구체적으로 제지를 받지 않았더라도 건조물침입죄가 성립”

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

## 50. `art319_sec3_1.open_cityhall_and_commercial_entry`

- proposition: 불법시위·절도·추행 등 범죄 목적이 있더라도, 출입자격 제한 없이 개방된 시청 로비 또는 일반인 출입이 허용된 영업장소에 출입제지 없이 다수의 힘·위세를 이용하지 않고 통상적 방법으로 들어간 경우 건조물침입죄는 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 장소의 실제 개방성, 제지 여부 및 출입 태양을 확인한다.
- bounded sources:

  - `comm_001692_제319조_Ⅲ.1_39` / `Ⅲ.1`: “불법시위를 목적으로 업무시간 중 출입자격 등의 제한 없이 일반적으로 출입이 허용되어 개방된 시청 로비에 관리자의 출입 제한이나 제지가 없는 상태”
  - `comm_001692_제319조_Ⅲ.1_39` / `Ⅲ.1`: “절도 목적으로 교보문고에 통상적으로 들어간 경우”
  - `comm_001692_제319조_Ⅲ.1_39` / `Ⅲ.1`: “는 여성의 몸을 훔쳐볼 목적으로 PC방에 통상적인 방법으로 들어간 경우”

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

## 51. `art319_sec3_1.open_place_special_prohibition`

- proposition: 공중 출입이 개방된 장소라도 개인적으로 내려진 출입금지에 위반하거나 일반적이지 않은 시간·방법으로 출입하여 사실상 평온을 해하면 주거침입죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 금지 통지와 비정상적 출입 시간·방법을 확인한다.
- bounded sources:

  - `comm_001692_제319조_Ⅲ.1_38` / `Ⅲ.1`: “공중의 출입이 개방된 장소라도 특별히 개인적으로 내려진 출입금지에 위반”
  - `comm_001692_제319조_Ⅲ.1_38` / `Ⅲ.1`: “하였거나 일반적이지 않은 시간·방법으로 출입하면”

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

## 52. `art319_sec3_1.open_public_place_entry`

- proposition: 개별 자격을 문제 삼지 않고 일반인의 출입이 허용된 공개장소에 들어가는 것은 소유자·관리인의 의사 또는 추정적 의사에 반하지 않으며, 적법하게 들어간 뒤 불법한 목적이 생긴 경우 주거침입죄는 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 처음 출입의 적법성과 불법 목적 발생 시점을 구별한다.
- bounded sources:

  - `comm_001692_제319조_Ⅲ.1_38` / `Ⅲ.1`: “개별적인 자격을 문제 삼지 않고 일반인의 출입을 허용하고 있는 공개된 장소”
  - `comm_001692_제319조_Ⅲ.1_38` / `Ⅲ.1`: “는 경우에는 건물 소유자·관리인의 의사 또는 추정적 의사에 반하지 않는다.”
  - `comm_001692_제319조_Ⅲ.1_38` / `Ⅲ.1`: “의 불법한 목적이 생긴 경우는 주거침입죄가 성립하지 않는다.”

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

## 53. `art319_sec3_1.partial_entry_intent`

- proposition: 주거침입의 고의는 신체 일부라도 타인의 주거 안으로 들어간다는 인식으로 족하다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`False`
- source track: `unit_core`
- prior note: 소개된 판례의 고의 판단을 제한적으로 반영한다.
- bounded sources:

  - `comm_001692_제319조_Ⅲ.1_21` / `Ⅲ.1`: “신체의 일부라도 타인의 주거 안으로 들어간다는 인식이 있으면 족하다고 판시”

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

## 54. `art319_sec3_1.possession_dispute_and_owner_tenant`

- proposition: 점유·관리권 분쟁에서는 타인이 관리하는 건조물에 들어간다는 고의가 부정될 수 있고, 임대차 종료 후에도 계속 점유하는 임차인의 허락 없이 소유자가 출입하면 주거침입죄가 성립할 수 있으나, 소유자가 임의 폐쇄한 건물에 계속 점유 임차인이 들어간 경우에는 성립하지 않을 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 각 보고 사례의 점유관계와 사실관계는 별도로 유지한다.
- bounded sources:

  - `comm_001692_제319조_Ⅲ.1_25` / `Ⅲ.1`: “‘타인이 관리하는’ 건조물에 들어간다는 범의가 있었다고 보기는 어렵다고 판단하였다.”
  - `comm_001692_제319조_Ⅲ.1_25` / `Ⅲ.1`: “임대차기간이 종료한 이후에 임차인이 계속 점유하고 있는 건물에 대해 소유자가 임차인의 허락을 받지 않고 출입하면 주거침입죄가 성립”
  - `comm_001692_제319조_Ⅲ.1_25` / `Ⅲ.1`: “임차인이 자력으로 판자를 뜯어 건물에 들어갔다 하여도 주거침입죄는 성립하지 않는다고 한다.”

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

## 55. `art319_sec3_1.restaurant_consented_entry`

- proposition: 일반인 출입이 허용된 음식점에 영업주 승낙을 받아 통상적 방법으로 들어간 경우, 범죄 목적이 있었거나 영업주가 실제 목적을 알았다면 승낙하지 않았을 사정만으로는 특별한 사정이 없는 한 침입행위가 아니다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 승낙·통상 출입 및 장소 개방성의 구체적 사실을 확인한다.
- bounded sources:

  - `comm_001692_제319조_Ⅲ.1_20` / `Ⅲ.1`: “일반인의 출입이 허용된 음식점에 영업주 의 승낙을 받아 통상적인 출입방법으로 들어갔다면 특별한 사정이 없는 한 주 거침입죄에서 규정하는 침입행위에 해당하지 않고”
  - `comm_001692_제319조_Ⅲ.1_34` / `Ⅲ.1`: “일반인의 출입이 허용된 음식점에 영업주의 승낙을 받아 통상적인 출입방법으로 들어갔다면 특별한 사정이 없는 한 주거침입죄에서 규정하는 침입행위에 해당하지 않는다.”

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

## 56. `art319_sec3_1.restricted_place_deceptive_entry`

- proposition: 출입이 엄격히 제한되는 고사장·사적 주거나 건조물에 출입자격 또는 조건을 기망하여 승낙을 받고 출입하는 행위는, 장소의 형태·용도·통제 상태에 비추어 그 기망적 출입 자체가 사실상 평온상태를 해치는 행위태양일 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 출입자격 제한 및 기망이 외형적 출입 태양에 미친 영향을 평가한다.
- bounded sources:

  - `comm_001692_제319조_Ⅲ.1_34` / `Ⅲ.1`: “일반인의 자유로운 출입이 허용되지 않고 출입자격이 실제 시험을 응시하는 수험생으로 엄격히 제한되는 고사장에 출입하기 위해 관리자를 기망하여 출입 승낙을 받아 시험장에 출입한 행위는”
  - `comm_001692_제319조_Ⅲ.1_34` / `Ⅲ.1`: “출입이 엄격히 제한되는 사적 주거나 건조물 등에 출입하기 위해 출입자격이나 조건을 기망하 여 거주자나 관리자로부터 승낙을 받아 출입한 행위는”

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

## 57. `art319_sec3_1.shop_absence_and_protective_order`

- proposition: 피해자 부재를 이용하여 상점에 들어가거나 법원의 접근금지 임시조치를 위반하여 영업장소에 들어간 경우, 출입 당시 객관적·외형적으로 사실상 평온상태를 해치는 행위태양이면 건조물침입죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 각 사안의 구체적 출입 경위와 보호명령 내용을 확인한다.
- bounded sources:

  - `comm_001692_제319조_Ⅲ.1_40` / `Ⅲ.1`: “피고인이 범죄의 기회를 노리고 있다가 피해자가 자리를 비운 사이에 상점에 들어갔다는 점에서 사실상의 평온상태를 해치는 행위태양으로 침입하였다고 인정한 것으로 볼 수 있다.”
  - `comm_001692_제319조_Ⅲ.1_40` / `Ⅲ.1`: “‘피해자가 운영하는 미용실에서 100m 이내의 접근 금지’를 명하는 임시조치 결정을 받았음에도 이를 위반하여 위 미용실에 들어간 경우에는”
  - `comm_001692_제319조_Ⅲ.1_40` / `Ⅲ.1`: “객관적·외형적으로 사실상 평온상태를 해치는 행위태양에 해당한다고 보아 건조물침입죄의 성립을 인정하였다.”

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

## 58. `art319_sec3_2.attempt_commencement`

- proposition: 주거침입죄의 실행의 착수는 사실상 평온을 해치는 방법으로 주거나 관리 건조물 등에 들어가는 행위를 개시하여 구성요건 실현에 이르는 현실적·객관적 위험성을 갖춘 때에 인정된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 사실상 평온 침해 방법과 현실적·객관적 위험성의 적용에는 개별 사실관계 평가가 필요하다.
- bounded sources:

  - `comm_001692_제319조_Ⅲ.2_41` / `Ⅲ.2`: “주거침입죄의 실행의 착수시기는 사실상의 평온을 해치는 방법으로 주거나 관”
  - `comm_001692_제319조_Ⅲ.2_41` / `Ⅲ.2`: “리하는 건조물 등에 들어가는 행위를 개시한 때로서, 구성요건의 일부를 실현하”
  - `comm_001692_제319조_Ⅲ.2_41` / `Ⅲ.2`: “는 행위까지 요하는 것은 아니고, 구성요건의 실현에 이르는 현실적·객관적 위”
  - `comm_001692_제319조_Ⅲ.2_41` / `Ⅲ.2`: “험성을 갖는 행위를 개시하는 것으로 충분하다.”

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

## 59. `art319_sec3_2.attempt_construction_site_negative`

- proposition: 현장사무실 또는 경비실이 아니라 담장과 경비가 있는 공사현장 외곽에 들어간 것만으로는 주거침입 실행의 착수가 부정된다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 이 카드는 공사현장 외곽 출입이라는 제한된 사실관계에 관한 부정적 판단으로 검토한다.
- bounded sources:

  - `comm_001692_제319조_Ⅲ.2_41` / `Ⅲ.2`: “공사의 현장사무실 또는 경비실에 들어간 것이 아니라 외곽에 담장이 설치되”
  - `comm_001692_제319조_Ⅲ.2_41` / `Ⅲ.2`: “고 경비를 둔 공사현장에 들어간 경우”

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

## 60. `art319_sec3_2.attempt_door_opening`

- proposition: 주거침입 고의로 문을 열거나 문의 시정장치를 부순 경우 실행의 착수가 인정된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 출입 목적과 시정장치 훼손 또는 문을 여는 행위의 사실인정이 필요하다.
- bounded sources:

  - `comm_001692_제319조_Ⅲ.2_41` / `Ⅲ.2`: “행위자가 주거침입의 고의를 가지고 문을 열거나 문의 시정장치를 부순 경”

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
