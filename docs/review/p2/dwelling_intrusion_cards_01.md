# 주거침입·퇴거불응 RuleIR 카드 검수 1

- unit: `dwelling_intrusion`
- articles: art319
- cards: 1–15 / 104
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #30 `art319_sec2_1.dwelling_concept`: `art319_sec2_1.dwelling_concept_sleeping` (status=`valid`)
- #31 `art319_sec5_2.private_arrest_home_entry`: `art319_sec5_2.private_arrest_home_entry_affirmative` (status=`valid`)

## 1. `art319.refusal_to_leave.enclosed_yard_and_entrance`

- proposition: 건조물의 위요지 및 사회통념상 건물의 일부인 현관은 퇴거불응죄의 객체에 해당할 수 있고, 소개된 판례는 교회 현관에서 관리인의 퇴거요구에 불응한 경우 퇴거불응죄가 성립한다고 하였다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 위요지 또는 현관이 보호되는 객체인지 여부에는 건조물과의 관계 및 사회통념에 따른 평가가 필요하다. 소개된 판례의 원문 확인 전에는 commentary-reported precedent로만 취급한다.
- bounded sources:

  - `comm_001692_제319조_Ⅶ.2_57` / `Ⅶ.2`: “건조물의 위요지도 퇴거불응죄의 객체에 해당하므로, 문이나 담이 설치 되지 않고 화단이나 수목으로 둘러싸인 병원의 마당도 퇴거불응죄의 성립 범위에 포함되고, 사회통념상 현관도 건물의 일부이므로 교회 건물 현관에 들어간 피고인이 그곳에서 교회 관리인의 퇴거요구를 받고 이에 불응하면 퇴거불응죄 가 성립한다고 하였다.”

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

## 2. `art319.refusal_to_leave.lawful_or_mistaken_entry`

- proposition: 퇴거불응죄는 처음에 적법하게 또는 과실로 타인의 주거 등에 들어간 사람이 거주자, 관리자 또는 점유자의 퇴거요구에 불응하는 경우 성립한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 적법 또는 과실에 의한 최초 출입과 이후 퇴거요구 불응의 관계를 구성요건 요소로 정리한 카드다. 퇴거요구에 묵시적 요구를 포함하는지는 별도 검토가 필요하다.
- bounded sources:

  - `comm_001692_제319조_Ⅶ.2_57` / `Ⅶ.2`: “타인의 주거, 관 리하는 건조물, 선박, 항공기 또는 점유하는 방실에 적법하게 또는 과실로 들어 간 후 거주자나 관리자, 점유자의 퇴거요구에 불응하는 모든 사람이다.”

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

## 3. `art319_sec1_3.co_resident_consent_ordinary_entry`

- proposition: 공동거주자 중 현재 거주자의 현실적 승낙을 받고 통상적 출입방법으로 들어간 경우, 부재중 다른 거주자의 의사에 반한다고 추정되더라도 사실상 주거의 평온을 깼다고 볼 수 없다는 판례 입장이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 현존 공동거주자의 현실적 승낙 및 통상적 출입방법이라는 제한된 사정에서 침입을 부정하는 소개된 판례 입장이다.
- bounded sources:

  - `comm_001692_제319조_Ⅰ.3_6` / `Ⅰ.3`: “공동거주자 중 주거 내에 현재하는 거주자의 현실적인 승낙을 받아 통상적 인 출입방법에 따라 주거에 들어갔다면, 설령 그것이 부재중인 다른 거주자의 의사에 반하는 것으로 추정된다고 하더라도 주거침입죄의 보호법익인 사실상 주거의 평온을 깨트렸다고 볼 수는 없다.”

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

## 4. `art319_sec1_3.entry_assessment`

- proposition: 판례상 침입은 거주자의 사실상 평온상태를 해치는 행위태양으로 주거에 들어가는 것을 뜻하며, 객관적·외형적으로 드러난 행위태양을 기준으로 장소의 형태·용도·성질, 출입 통제·관리 방식과 상태, 출입 경위와 방법을 종합 고려하여 판단한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 침입 여부는 객관적·외형적 행위태양과 장소 및 출입 상황의 종합 평가를 요구한다.
- bounded sources:

  - `comm_001692_제319조_Ⅰ.3_5` / `Ⅰ.3`: “침입이란 ‘거주자가 주거에서 누리는 사실 상의 평온상태를 해치는 행위태양으로 주거에 들어가는 것’을 의미하고”
  - `comm_001692_제319조_Ⅰ.3_5` / `Ⅰ.3`: “‘출입 당시 객관적·외형적으로 드러난 행위태양을 기준으로 판 단함이 원칙이라면서 단순히 주거에 들어가는 행위 자체가 거주자의 의사에 반 한다는 거주자의 주관적인 사정만으로 바로 침입에 해당한다고 볼 수 없고, 주 거 등의 형태와 용도·성질, 외부인의 출입에 대한 통제·관리 방식과 상태, 출입 의 경위와 방법 등을 종합적으로 고려하여 판단하여야 한다’”

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

## 5. `art319_sec1_3.partial_body_completed_offense`

- proposition: 행위자가 출입할 생각 없이 신체 일부만 타인의 주거 안에 넣었더라도 사실상 주거의 평온을 해할 수 있는 정도에 이르면 주거침입죄는 기수에 이른다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 신체 일부의 진입만으로 기수가 되는지는 사실상 주거의 평온을 해할 수 있는 정도에 대한 평가를 필요로 한다.
- bounded sources:

  - `comm_001692_제319조_Ⅰ.3_6` / `Ⅰ.3`: “행위자가 주거에 출입할 생각이 없어 신체 의 일부만 타인의 주거 안에 들여놓았다고 해도 거주자가 누리는 사실상 주거 의 평온을 해할 수 있는 정도에 이르렀다면 주거침입죄는 기수에 이른다.”

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

## 6. `art319_sec1_3.protected_interest`

- proposition: 판례는 주거침입죄의 보호법익을 사적 생활관계에서 사실상 누리는 주거의 평온으로 보고, 법적 점유권한이 없어도 사실상 권한 있는 거주자의 사실적 지배·관리관계가 평온하게 유지되는 상태를 말한다고 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 보호법익에 관한 판례 소개이며, 원판례 확인 전에는 commentary-reported precedent로 유지한다.
- bounded sources:

  - `comm_001692_제319조_Ⅰ.3_5` / `Ⅰ.3`: “판례는, 주거침입죄의 보호법익을 ‘사적 생활관계에 있어서 사실상 누리고 있는 주거의 평온’, 즉 ‘사실상 주거의 평온’이라고 일관되게 판시하여 왔고”
  - `comm_001692_제319조_Ⅰ.3_5` / `Ⅰ.3`: “여기서 ‘사실상 주거의 평온’이라 함은 주거를 점유할 법적 권한이 없더라도 사 실상의 권한이 있는 거주자가 주거에서 누리는 사실적 지배·관리관계가 평온하 게 유지되는 상태를 말한다.”

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

## 7. `art319_sec1_3.restaurant_entry_with_consent`

- proposition: 일반인의 출입이 허용된 음식점에 영업주의 승낙과 통상적 방법으로 들어간 경우, 범죄 목적이나 실제 목적을 알았다면 승낙하지 않았을 사정만으로는 특별한 사정이 없는 한 침입행위가 아니다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 일반 출입 허용 장소, 영업주 승낙, 통상적 출입방법 및 특별한 사정의 유무를 검토해야 한다.
- bounded sources:

  - `comm_001692_제319조_Ⅰ.3_6` / `Ⅰ.3`: “일반인의 출입이 허용된 음식점에 영업주의 승낙을 받아 통상적인 출입방법으로 들어갔다면 특별한 사 정이 없는 한 주거침입죄에서 규정하는 침입행위에 해당하지 않는다.”
  - `comm_001692_제319조_Ⅰ.3_6` / `Ⅰ.3`: “러한 사정만으로는 출입 당시 객관적·외형적으로 드러난 행위태양에 비추어 사 실상의 평온상태를 해치는 방법으로 음식점에 들어갔다고 평가할 수 없으므로 침입행위에 해당하지 않는다.”

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

## 8. `art319_sec1_3.right_holder_entry_unlawful_occupancy`

- proposition: 적법하게 점유 또는 관리를 시작한 자가 권원을 상실하여 사법상 불법점유자가 되었더라도, 권리자가 정당한 절차 없이 그 주거나 건조물에 들어가면 주거침입죄 또는 건조물침입죄가 성립한다는 판례 입장이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 권리자의 출입이라도 정당한 절차를 거치지 않은 경우에 관한 소개된 판례 입장이다.
- bounded sources:

  - `comm_001692_제319조_Ⅰ.3_6` / `Ⅰ.3`: “일단 적법하게 점유나 관리를 개시한 후에 그 권원을 상실하여 사법상 불법점유가 되었다고 하더라도 적법한 절차에 의하여 그 점유를 풀지 않는 한”
  - `comm_001692_제319조_Ⅰ.3_6` / `Ⅰ.3`: “권리자가 부적법한 상태를 배제하려고 정당한 절차에 따르지 않고 그 주거 또는 건조물에 들어간 경우에는 주거침입죄가 성립한다.”

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

## 9. `art319_sec1_4.partial_body_attempt`

- proposition: 신체의 극히 일부가 주거 안으로 들어갔더라도 사실상 주거의 평온을 해하는 정도에 이르지 않으면 주거침입죄 미수에 그친다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 주거의 평온을 해하는 정도는 사실관계 평가가 필요하며, 소개된 판례의 원문과 적용 범위는 사용자 제공 1차 판례 색인으로 확인해야 한다.
- bounded sources:

  - `comm_001692_제319조_Ⅰ.4_7` / `Ⅰ.4`: “신체의 극히 일부분이 주거 안으로 들어갔지만 사실상 주거의 평온을 해하는 정도에 이르지 아니하였다면 주거침 입죄의 미수에 그친다고 하였다.”

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

## 10. `art319_sec2_1.common_area_entry_assessment`

- proposition: 외부인의 공동주택 공용 부분 출입이 주거침입인지 여부는 공용 부분의 공중 출입 허용 여부, 전용부분에의 필수적 부속성, 출입 통제·관리 예정과 실제 관리, 출입 목적·경위·태양·시간을 종합하여 사실상 주거 평온 침해 관점에서 객관적·외형적으로 판단한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 공용 부분의 출입 제한성과 실제 출입 상황을 종합하는 평가 기준이므로 개별 사실관계 검토가 필요하다.
- bounded sources:

  - `comm_001692_제319조_Ⅱ.1_13` / `Ⅱ.1`: “그 공용 부분이 일반 공중에 출입이 허용된 공간이 아니고 주거로 사용되는 각 가구 또는 세대의 전 용 부분에 필수적으로 부속하는 부분으로서 거주자들 또는 관리자에 의하여 외 부인의 출입에 대한 통제·관리가 예정되어 있어 거주자들의 사실상 주거의 평온 을 보호할 필요성이 있는 부분인지”
  - `comm_001692_제319조_Ⅱ.1_13` / `Ⅱ.1`: “외부인의 출입 목 적 및 경위, 출입의 태양과 출입한 시간 등을 종합적으로 고려하여 ‘주거의 사실 상 평온상태를 침해하였는지’의 관점에서 객관적·외형적으로 판단하여야 한다.”

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

## 11. `art319_sec2_1.deceased_victim_possession`

- proposition: 피고인이 피해자의 주거에 침입할 당시 피해자가 이미 사망했고 정확한 사망시기도 밝혀지지 않은 사안에서는 사자의 점유를 인정할 수 없어 야간주거침입절도 후 준강제추행 미수는 무죄로 판단한 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 사망 당시점과 사망시기 불명이라는 사정을 근거로 사자의 점유를 부정한 좁은 보고판례다. 사망 직후 평온 유지 견해와의 조정이 필요하다.
- bounded sources:

  - `comm_001692_제319조_Ⅱ.1_8` / `Ⅱ.1`: “피고 (절도강간등) 인이 피해자의 주거에 침입할 당시 피해자는 이미 사망한 상태였고, 정확한 사 망시기도 밝혀지지 않은 사정 등에 비추어, 사자의 점유를 인정할 수 없다고 보 아 야간주거침입절도 후 준강제추행 미수의 점은 무죄로 판단하고”

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

## 12. `art319_sec2_1.enclosed_land_requirements`

- proposition: 위요지로 인정되려면 가옥 인접 주변 토지이고, 문·담 등 외부와의 경계가 설치되어 있으며, 가옥 이용에 제공되고 외부인이 함부로 출입할 수 없다는 점이 객관적으로 명확해야 한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`False`
- source track: `unit_core`
- prior note: 인접성, 경계시설, 가옥 이용 제공 및 객관적으로 명확한 외부인 출입 제한을 누적 확인하는 요소 카드다.
- bounded sources:

  - `comm_001692_제319조_Ⅱ.1_12` / `Ⅱ.1`: “‘위요지’가 되기 위해서는 ⅰ) 가옥에 인접한 주변 토지로서, ⅱ) 외부와의 경 계에 문과 담 등이 설치되어 있어, ⅲ) 그 토지가 가옥의 이용을 위하여 제공되고 또 외부인이 함부로 출입할 수 없다는 점이 객관적으로 명확하게 드러나야 한다.”

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

## 13. `art319_sec2_1.enforcement_dissipated_peace`

- proposition: 매수인이 매매계약 해제와 중도금반환 승소판결에 기초하여 강제집행에 착수한 뒤 매도인이 잠긴 출입문을 열고 들어간 사안에서는, 매수인이 권리를 포기한 것으로 알았고 보호할 주거 평온상태도 소멸하였다고 볼 수 있어 주거침입죄가 성립하지 않는다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 강제집행 착수, 권리 포기에 관한 인식 및 보호할 평온상태 소멸이라는 구체적 사정을 전제로 한 부정 보고판례다.
- bounded sources:

  - `comm_001692_제319조_Ⅱ.1_11` / `Ⅱ.1`: “매도인으로서는 매수인이 그 주택에 대한 모든 권리를 포기한 것 으로 알고 그 주택에 들어간 것이라고 할 수 있을 뿐만 아니라, 또한 주택에 대하여 보호받아야 할 피해자의 주거에 대한 평온상태는 소멸되었다고 볼 수 있으므로, 매 도인의 위와 같은 행위는 주거침입죄를 구성하지 않는다.”

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

## 14. `art319_sec2_1.former_cohabitant_loss_of_control`

- proposition: 공동생활하던 주거에서 이탈하거나 주거에 대한 사실상의 지배·관리를 상실한 자에 대해서는 특별한 사정이 있으면 그 주거가 타인의 주거가 되어 주거침입죄가 성립할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 공동생활 이탈 또는 사실상 지배·관리 상실 및 특별한 사정의 존재를 개별적으로 검토해야 한다.
- bounded sources:

  - `comm_001692_제319조_Ⅱ.1_8` / `Ⅱ.1`: “다른 사람과 공동생활하고 있는 있었던 주거라 할지라도 그로부터 이탈하거나 주거에 대한 사실상의 지배·관 리를 상실한 경우 등 특별한 사정이 있는 경우에는 타인의 주거가 되므로, 위 와 같은 경우에는 주거침입죄가 성립할 수 있다.”

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

## 15. `art319_sec2_1.non_dwelling_occupied_room`

- proposition: 빌딩사무실·실험실·점포와 호텔·여관의 객실처럼 하룻밤 숙박이나 단시간 휴식을 위해 사용하는 장소는 주거가 아니라 점유하는 방실에 해당한다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 열거된 사용 형태의 장소를 주거가 아닌 점유하는 방실로 분류하는 정의 카드다.
- bounded sources:

  - `comm_001692_제319조_Ⅱ.1_9` / `Ⅱ.1`: “따라서 빌딩사무실, 실험실, 점포와 호텔·여관 의 한 방과 같이 하룻밤 숙박이나 단시간의 휴식을 위해 사용되는 장소는 주거 가 아니라 점유하는 방실에 해당한다.”

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
