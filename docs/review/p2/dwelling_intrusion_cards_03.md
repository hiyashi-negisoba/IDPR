# 주거침입·퇴거불응 RuleIR 카드 검수 3

- unit: `dwelling_intrusion`
- articles: art319
- cards: 31–45 / 104
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #30 `art319_sec2_1.dwelling_concept`: `art319_sec2_1.dwelling_concept_sleeping` (status=`valid`)
- #31 `art319_sec5_2.private_arrest_home_entry`: `art319_sec5_2.private_arrest_home_entry_affirmative` (status=`valid`)

## 31. `art319_sec2_2.unmanaged_empty_house`

- proposition: 다른 사람이 살지 않고 관리하지 않는 집 또는 그 울타리 안이나 건조물·배·자동차 안에 정당한 이유 없이 들어간 행위는 주거침입죄가 아니라 경범죄처벌법 제3조 제1항 제1호 위반죄에 해당한다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 거주 및 관리의 부재와 정당한 이유의 유무는 사실관계별 검토가 필요하다.
- bounded sources:

  - `comm_001692_제319조_Ⅱ.2_14` / `Ⅱ.2`: “다른 사람이 살지 않고 관리하지 않는 집 또는 그 울타리 안이나 건조물·배· 자동차 안에 정당한 이유 없이 들어간 행위는 주거침입죄가 아니라 경범죄 처 벌법 제3조 제1항 제1호 위반죄에 해당되고”

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

## 32. `art319_sec2_2.vessel_scale`

- proposition: 선박은 수상교통의 수단으로 사용되는 제조물을 의미하고, 적어도 사람의 주거에 사용될 수 있는 정도의 규모여야 한다는 통설이 소개되어 있으며, 놀이용 소형 모터보트와 카누는 이에 해당하지 않는다고 본다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 사람의 주거에 사용될 수 있는 정도의 규모는 물리적 사정을 확인하여 판단한다.
- bounded sources:

  - `comm_001692_제319조_Ⅱ.2_16` / `Ⅱ.2`: “‘선박’은 수상교통의 수단으로 사용되는 제조물을 의미한다. 그 크기를 묻지 않지만, 적어도 사람의 주거에 사용될 수 있는 정도의 규모는 되어야 한다는 것 이 통설이다. 그러므로 놀이용 소형 모터보트, 카누는 이에 해당되지 않는다 고 본다.”

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

## 33. `art319_sec2_3.occupied_room_building_partition`

- proposition: 점유하는 방실은 건조물 내에서 사실상 지배·관리되는 일정한 구획을 말한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 건조물 내 사실상 지배·관리되는 구획이라는 설명과 건조물 외 이동수단 내부 공간을 포함한다는 학설의 관계를 검토해야 한다.
- bounded sources:

  - `comm_001692_제319조_Ⅱ.3_18` / `Ⅱ.3`: “‘점유하는 방실’은 건조물 내에서 사실상 지배·관리되는 일정한 구획을 말한 다.”

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

## 34. `art319_sec3_1.abnormal_or_forced_entry`

- proposition: 출입문을 통한 정상 출입이 아니거나 출입 방법이 비정상적인 경우, 또는 개방 장소에서 시설 일부를 파괴하거나 흉기를 소지하거나 다수의 위력으로 무리하게 들어간 경우에는 통상 침입에 해당한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 통상성 및 강제성은 객관적 출입 태양으로 평가한다.
- bounded sources:

  - `comm_001692_제319조_Ⅲ.1_21` / `Ⅲ.1`: “출입문을 통한 정상적인 출입이 아닌 경우, 출입 방법이 비정상적인 경우에는 통상 침입에 해당한다고 할 것이다.”
  - `comm_001692_제319조_Ⅲ.1_21` / `Ⅲ.1`: “시설 의 일부를 파괴하거나 흉기를 소지하거나 다수의 위력으로써 무리하게 들어가 면 침입에 해당”

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

## 35. `art319_sec3_1.apartment_common_areas`

- proposition: 공동주택 공용 부분의 외부인 출입은 통제·관리 예정과 실제 통제, 출입 목적·경위·태양·시간 등을 종합하여 객관적·외형적으로 판단하며, 엘리베이터·계단·복도 등 세대 전용부분에 필수적으로 부속되어 일상적 감시·관리가 예정된 부분에 침입하면 주거침입죄를 구성한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 공용부의 개방성·통제 상태를 구체적으로 평가한다.
- bounded sources:

  - `comm_001692_제319조_Ⅲ.1_29` / `Ⅲ.1`: “외부인의 출입 목적 및 경 위, 출입의 태양과 출입한 시간 등을 종합적으로 고려하여 주거의 사실상 평온 상태를 침해하였는지의 관점에서 객관적·외형적으로 판단하여야 한다.”
  - `comm_001692_제319조_Ⅲ.1_30` / `Ⅲ.1`: “엘리베이터, 계단, 복도 등의 경우도 각 가구 또는 세대의 전용 부분에 필수적으로 부속하는 부분으로서 그 거주자들에 의하여 일상생활에서 감시·관리가 예정되어 있고”

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

## 36. `art319_sec3_1.apartment_common_door_unauthorized_entry`

- proposition: 외부인 출입이 통제·관리되는 공동주택 공동현관에서 승낙이나 정당한 이유 없이 비밀번호를 임의 입력·조작하여 출입하는 등 거주자의 사실상 주거 평온을 해치는 행위태양인 경우 주거침입에 해당한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 공동현관의 실제 통제 상태와 정당한 출입 사유를 검토한다.
- bounded sources:

  - `comm_001692_제319조_Ⅲ.1_22` / `Ⅲ.1`: “피해자나 다른 입주자의 승낙 없이 피해자와 헤어지기 전 알고 있던 공동현관 출입문의 비밀번호를 입 력하는 방법으로 아파트의 공용 부분에 출입한 경우에는 주거침입죄가 성립”
  - `comm_001692_제319조_Ⅲ.1_30` / `Ⅲ.1`: “그 출입 목적 및 경위, 출입의 태양과 출입한 시간 등을 종합적으로 고려할 때 공동주택 거주자의 사실상 주거의 평온상태를 해치는 행위태양이라고 볼 수 있는 경우라 면 공동주택 거주자들에 대한 주거침입에 해당한다.”

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

## 37. `art319_sec3_1.bodily_entry_required`

- proposition: 침입은 신체적 침입을 의미하므로 행위자의 신체가 주거에 들어가지 않으면 침입이 아니다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 신체 진입의 최소 요건으로만 사용한다.
- bounded sources:

  - `comm_001692_제319조_Ⅲ.1_20` / `Ⅲ.1`: “‘침입’은 신체적 침입을 의미하므로 행위자의 신체가 주거에 들어가지 않으면 침입이라고 할 수 없다.”

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

## 38. `art319_sec3_1.co_resident_common_space`

- proposition: 공동거주자는 다른 공동거주자의 정당하지 않은 출입금지에 대항하여 공동생활 장소를 이용하여도 주거침입죄가 성립하지 않지만, 공동거주관계가 형성되지 않은 외부인은 사실상 주거 평온을 해치는 태양으로 출입하면 주거침입죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 공동거주관계 성립 여부 및 공동생활 장소 범위를 확인한다.
- bounded sources:

  - `comm_001692_제319조_Ⅲ.1_28` / `Ⅲ.1`: “다른 공동거주자가 이에 대항하여 공동생활의 장소에 들어 갔더라도”
  - `comm_001692_제319조_Ⅲ.1_29` / `Ⅲ.1`: “피고인이 공동거주자가 아닌 경우, 피고인이 피해자의 집에서 짧은 기간 동안만 함께 생활하여 공동주거관계를 형성하였다고 볼 수 (약 1개월) 없는 경우에는”

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

## 39. `art319_sec3_1.commercial_corridor_implied_consent`

- proposition: 다방·당구장·독서실 등이 있는 건물의 공용 계단과 복도는 관리자가 1층 출입문을 특별히 시정하지 않은 경우 관리자 또는 소유자의 묵시적 승낙이 추정되어 출입행위가 주거침입죄를 구성하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 출입문 시정 여부와 영업시설의 개방 상태를 확인한다.
- bounded sources:

  - `comm_001692_제319조_Ⅲ.1_32` / `Ⅲ.1`: “관리자가 1층 출입문을 특 별히 시정하지 않는 한 그 출입에 관하여 관리자나 소유자의 묵시적 승낙이 있 다고 봄이 상당하여 그 출입행위는 주거침입죄를 구성하지 않는다고 하였다.”

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

## 40. `art319_sec3_1.concealed_device_and_key_entry`

- proposition: 승낙 또는 접견허가 아래 통상적 방법으로 출입한 경우, CCTV·녹음장비의 은닉이나 집기 철거 목적 등 상대방이 알았다면 승낙하지 않았을 사정만으로는 사실상 평온을 해치는 출입 태양으로 평가되지 않아 주거·건조물침입죄가 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 각 사례의 승낙 범위와 통상적 출입 방법을 확인한다.
- bounded sources:

  - `comm_001692_제319조_Ⅲ.1_36` / `Ⅲ.1`: “피해자의 승낙을 받고 통상적인 방 법으로 피해자의 주거지 안방에 들어가 TV를 설치한 경우 피해자의 사실상 평 온상태가 침해되지 않았다고 보아 주거침입죄가 성립하지 않는다고 하였다.”
  - `comm_001692_제319조_Ⅲ.1_36` / `Ⅲ.1`: “한 사정만으로는 사실상의 평온상태를 해치는 행위 태양으로 접견실에 출입하 였다고 평가할 수 없으므로 피고인들에 대하여는 건조물침입죄가 성립하지 않 는다고 하였다.”
  - `comm_001692_제319조_Ⅲ.1_37` / `Ⅲ.1`: “피고인이 이러한 A의 승낙 아래 통상적인 출입방법에 따라 위 점포에 들어간 이 상 사실상의 평온상태를 해치는 행위태양으로 위 점포에 들어갔다고 볼 수 없 으므로”

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

## 41. `art319_sec3_1.consent_and_coerced_consent`

- proposition: 거주자 등의 명시적·일반적·묵시적 동의나 승낙으로 사실상 평온을 해치는 태양으로 볼 수 없는 경우 침입이 아니지만, 강박에 의한 승낙 의사표시는 무효이므로 주거침입죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 승낙의 존재와 강박 여부를 분리하여 검토한다.
- bounded sources:

  - `comm_001692_제319조_Ⅲ.1_31` / `Ⅲ.1`: “거주자 등의 출입에 대한 승낙이나 동의가 있어 사실상의 평온상태를 해치 는 행위태양으로 볼 수 없는 경우에는 침입에 해당하지 않게 된다.”
  - `comm_001692_제319조_Ⅲ.1_32` / `Ⅲ.1`: “승낙의 의사표시가 강박에 의한 것일 경우에는 무효이므로 주거침입죄가 성립 한다고 할 것이다.”

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

## 42. `art319_sec3_1.consenting_current_co_resident`

- proposition: 외부인이 주거 내에 현재하는 공동거주자의 현실적 승낙을 받아 통상적 출입방법으로 들어간 경우에는 특별한 사정이 없는 한, 부재중 다른 거주자의 의사에 반하는 것으로 추정되더라도 침입에 해당하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 현재 거주자의 승낙 범위와 반대 공동거주자 상황을 검토한다.
- bounded sources:

  - `comm_001692_제319조_Ⅲ.1_20` / `Ⅲ.1`: “외부인이 공동거주자 중 주거 내에 현재하는 거 주자로부터 현실적인 승낙을 받아 통상적인 출입방법에 따라 주거에 들어간 경 우라면, 특별한 사정이 없는 한”
  - `comm_001692_제319조_Ⅲ.1_27` / `Ⅲ.1`: “공동거주 자 중 주거 내에 현재하는 거주자의 현실적인 승낙을 받아 통상적인 출입방법 에 따라 들어갔다면, 설령 그것이 부재중인 다른 거주자의 의사에 반하는 것으 로 추정된다고 하더라도”

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

## 43. `art319_sec3_1.entry_decision_authority`

- proposition: 거주자·관리자·점유자는 주거 등에 대한 출입과 체류를 결정하거나 허용할 수 있는 사람이며, 수위 등 현실 감시자의 묵인·승낙은 관리권자의 의사에 반함이 명백한 경우 유효한 승낙이 아니다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 승낙자의 관리·점유 권한을 사실적으로 확인한다.
- bounded sources:

  - `comm_001692_제319조_Ⅲ.1_23` / `Ⅲ.1`: “거주자, 관리자, 점유자는 주거 등에 대한 출입과 체류를 결정하거나 허용할 수 있는 사람을 말한다.”
  - `comm_001692_제319조_Ⅲ.1_24` / `Ⅲ.1`: “숙직원이나 수위 등은 관리권자가 아니므로 가령 수위 등이 들어가는 것을 묵인 또는 승낙했더라도 관리권자의 의사에 반하는 것이 명백한 경우라면 승낙 이 있다고 할 수 없다.”

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

## 44. `art319_sec3_1.external_entry_and_partition_exception`

- proposition: 침입은 원칙적으로 외부로부터의 침입에 한정되어 이미 내부에 있는 사람은 퇴거불응죄만 문제되지만, 적법하게 들어간 뒤 독립적으로 구획되고 무상 출입이 가능한 공간이 아닌 다른 공간으로 옮겨가면 침입이 될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 내부 구획의 독립성 및 출입 권한을 검토한다.
- bounded sources:

  - `comm_001692_제319조_Ⅲ.1_23` / `Ⅲ.1`: “침입은 외부로부터의 침입에 제한된다. 즉 이미 주거 내부에 있는 사람은 주 거침입을 범할 수 없고, 퇴거불응죄만 범할 수 있을 뿐이다.”
  - `comm_001692_제319조_Ⅲ.1_23` / `Ⅲ.1`: “적법하게 들어간 공간 내에서 옮겨간 다른 공간이 독립적으로 구획된 공간이고 출입이 무상으로 이루어질 수 있는 것이 아니라면 침입이 될 수도 있다.”

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

## 45. `art319_sec3_1.intrusion_factors`

- proposition: 침입 여부는 장소의 형태·용도·성질, 외부인 출입 통제·관리 방식과 상태, 출입 경위와 태양 등을 종합하여 출입 당시 객관적·외형적으로 사실상 평온상태가 침해되었는지 평가하며, 거주자 등의 의사에 반하는지는 그 평가 요소 중 하나이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 사안별 종합평가가 필요한 기준이다.
- bounded sources:

  - `comm_001692_제319조_Ⅲ.1_19` / `Ⅲ.1`: “출입하려는 주거 등의 형태와 용도·성질, 외부인 에 대한 출입의 통제·관리 방식과 상태, 행위자의 출입 경위와 태양 등을 종합 적으로 고려하여”
  - `comm_001692_제319조_Ⅲ.1_21` / `Ⅲ.1`: “‘침입’에 해당하는지는 거주자 등의 의사에 반한다는 사정만으로는 부족하고, 출입하려는 주거 등의 형 태와 용도·성질, 외부인에 대한 출입의 통제·관리 방식과 상태, 행위자의 출입 경위와 태양 등을 종합적으로 고려하여 판단”
  - `comm_001692_제319조_Ⅲ.1_31` / `Ⅲ.1`: “거주자 등의 의사에 반 하는지는 사실상의 평온상태를 해치는 행위태양인지를 평가할 때 고려할 요소 중 하나이다.”

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
