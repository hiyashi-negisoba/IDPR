# 주거침입·퇴거불응 RuleIR 카드 검수 2

- unit: `dwelling_intrusion`
- articles: art319
- cards: 16–30 / 104
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #30 `art319_sec2_1.dwelling_concept`: `art319_sec2_1.dwelling_concept_sleeping` (status=`valid`)
- #31 `art319_sec5_2.private_arrest_home_entry`: `art319_sec5_2.private_arrest_home_entry_affirmative` (status=`valid`)

## 16. `art319_sec2_1.runaway_child_parent_home`

- proposition: 가출한 자녀가 야간에 절도 목적으로 종래 함께 살던 부모 집에 침입한 경우 주거침입이 인정되어 야간주거침입절도죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 가출 상태, 야간성 및 절도 목적이 포함된 좁은 보고판례 사안이다.
- bounded sources:

  - `comm_001692_제319조_Ⅱ.1_8` / `Ⅱ.1`: “가출한 자 녀가 야간에 절도의 목적으로 종래 함께 살던 부모 집에 침입하였다면, 주거침 입이 인정되어 야간주거침입절도죄가 성립하게 된다.”

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

## 17. `art319_sec2_1.seasonally_unused_villa`

- proposition: 별장은 계절적으로 전혀 사용하지 않는 기간에는 주거가 아니라 건조물에 해당한다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 별장이 계절적으로 전혀 사용되지 않는 기간에 한정된 명시적 예외다.
- bounded sources:

  - `comm_001692_제319조_Ⅱ.1_9` / `Ⅱ.1`: “다만, 별장의 경우 계절적으로 전혀 사용하지 않는 기간 동안은 주거가 아니라 건조물에 해당한다.”

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

## 18. `art319_sec2_1.separated_husband_owned_home`

- proposition: 별거 중인 남편이 처의 부정행위 현장을 촬영하려고 처가 거주하는 자기 소유 가옥에 침입한 경우에도 주거침입죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소유권이 있으나 별거 중인 배우자가 거주하는 가옥이라는 한정된 사정의 보고판례다.
- bounded sources:

  - `comm_001692_제319조_Ⅱ.1_8` / `Ⅱ.1`: “별거 중인 남편이 처가 부정행위를 하는 현장에 대한 촬영을 하기 위하여 처가 거주하는 자기 소 유의 가옥에 침입하는 경우에도 주거침입죄가 성립한다.”

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

## 19. `art319_sec2_1.temporary_dwelling`

- proposition: 일시적으로 기거하고 침식에 사용하는 장소도 주거가 될 수 있으며, 낮에만 기거하는 곳, 휴가 기간 중 설치한 텐트, 별장 및 주거용 차량이 이에 해당할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 지속적 사용은 요구하지 않되 일시적 기거·침식 사용 여부를 사실관계에서 확인하는 정의 카드다.
- bounded sources:

  - `comm_001692_제319조_Ⅱ.1_9` / `Ⅱ.1`: “지속적으로 침식에 사용될 것을 요하지 않고 일시적으로 기거하고 침식에 사용되는 장소라도 무방하므로 낮에만 기거하는 곳, 휴가기간 동안 일시적으로 설치한 텐트, 별장 또는 주거용 차량 역시 주거 에 해당한다.”

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

## 20. `art319_sec2_1.uncontrolled_adjacent_land`

- proposition: 주거 이용에 기여하는 인접 부속토지라도 인적·물적 설비에 의한 구획이나 통제가 없어 통상 보행으로 쉽게 경계를 넘을 수 있으면, 외부인 출입 제한이 객관적으로 명확하지 않아 위요지에 해당하지 어렵다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 구획·통제의 정도와 통상 보행에 의한 경계 통과 가능성의 평가는 사실관계별 검토가 필요하다.
- bounded sources:

  - `comm_001692_제319조_Ⅱ.1_12` / `Ⅱ.1`: “주거의 이용에 기여하 는 인접 부속 토지라고 하더라도 인적 또는 물적 설비 등에 의한 구획 내지 통 제가 없어 통상의 보행으로 그 경계를 쉽사리 넘을 수 있는 정도라고 한다면 일 반적으로 외부인의 출입이 제한된다는 사정이 객관적으로 명확하게 드러났다고 보기 어려우므로 이는 위요지에 해당하지 않는다고 한다.”

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

## 21. `art319_sec2_1.unlawful_construction_site_occupancy`

- proposition: 피해자 측이 불법적으로 공사현장을 점거하였더라도 경찰 신고·허가에 따라 경비원을 상주시켜 약 65일간 점유·관리한 상황에서, 정당하고 적법한 절차 없이 공사현장과 건조물에 침입하면 건조물침입죄가 성립한다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 불법 점거와 현실의 점유·관리 상태가 공존하는 좁은 보고판례 사안이다. 원판결 및 적용 범위를 확인해야 한다.
- bounded sources:

  - `comm_001692_제319조_Ⅱ.1_11` / `Ⅱ.1`: “피해자들 측이 불법적으로 공사현장을 점거하였지만 ‘관할 경찰서로부터 집단민원현 장 경비원배치신고 및 관련 허가를 받아 약 65일간 경비원을 상주시키면서 점유·관 리하여 온 상황’에서 피고인들이 정당하고 적법한 절차에 의하지 않고 공사현장 및 건조물에 침입한 경우 건조물침입죄가 성립한다.”

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

## 22. `art319_sec2_2.aircraft_and_vehicle_exclusion`

- proposition: 항공기는 사람의 조종에 의하여 공중을 운행하는 기기 중 적어도 사람의 주거에 사용될 수 있는 정도의 규모여야 하며, 자동차·기차·지하철·전동차는 본죄의 객체에 해당하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 항공기의 주거 사용 가능 규모는 개별 기기의 물리적 사정에 따라 검토한다.
- bounded sources:

  - `comm_001692_제319조_Ⅱ.2_17` / `Ⅱ.2`: “‘항공기’란 사람의 조종에 의하여 공중을 운행하는 기기를 말한다. 본죄의 객 체인 항공기에 해당하려면 적어도 사람의 주거에 사용될 수 있는 정도의 규모 는 되어야 한다.”
  - `comm_001692_제319조_Ⅱ.2_17` / `Ⅱ.2`: “자동차, 기차, 지하철, 전동차는 본죄의 객체에 해당하지 않는다.”

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

## 23. `art319_sec2_2.building_structure`

- proposition: 건조물은 주거를 제외한 일체의 건물과 그 부속 구조물 및 위요지를 의미하며, 일반적으로 주위벽 또는 기둥과 지붕 또는 천정으로 구성되어 사람이 기거하거나 출입할 수 있는 구조물이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 구조물의 물리적 구성과 사람이 기거하거나 출입할 수 있는지의 확인이 필요하다.
- bounded sources:

  - `comm_001692_제319조_Ⅱ.2_14` / `Ⅱ.2`: “‘건조물’은 ‘주거’를 제외한 일체의 건물과 이에 부속된 구조물 및 그 위요지를 의미한다. ‘건조물’에 해당하려면, 일반적으로 주위벽 또는 기둥과 지붕 또 는 천정으로 구성된 구조물로서 사람이 기거하거나 출입할 수 있는 장소를 말 하며”

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

## 24. `art319_sec2_2.construction_site_not_enclosed_land`

- proposition: 공사현장에 현장사무실이나 경비실 외 별도의 건조물이 없고 공사현장이 그 시설들의 이용을 위하여 제공된 토지라고 보기 어려운 경우, 공사현장 출입은 건조물침입죄가 성립할 수 없다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소개된 판례의 원문과 사실관계는 사용자 제공 1차 판례 인덱스에서 확인해야 한다.
- bounded sources:

  - `comm_001692_제319조_Ⅱ.2_16` / `Ⅱ.2`: “공사현 장에 현장사무실이나 경비실 외에 별도의 건조물은 없는 경우 공사현장이 현장 사무실이나 경비실의 이용을 위하여 제공된 토지라고 보기 어려우므로 공사현 장에 출입한 행위는 건조물침입죄가 성립할 수 없다고 하였다.”

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

## 25. `art319_sec2_2.enclosed_land_requirements`

- proposition: 건조물의 위요지가 되기 위해서는 건조물에 인접한 주변 토지에 관리자가 외부와의 경계로 문과 담 등을 설치하여 그 토지가 건조물 이용을 위하여 제공되었다는 점이 명확히 드러나야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 인접성, 경계시설, 건조물 이용 제공 여부를 개별적으로 평가해야 한다.
- bounded sources:

  - `comm_001692_제319조_Ⅱ.2_16` / `Ⅱ.2`: “건조물의 위요지가 되기 위해서는 건조물에 인접한 그 주변 토지로서 관리자가 외부와의 경계에 문과 담 등을 설치하여 그 토지가 건조물의 이용을 위하여 제 공되었다는 것이 명확히 드러나야 한다.”

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

## 26. `art319_sec2_2.incomplete_construction_not_building`

- proposition: 벽·기둥·지붕·천정 등을 완전히 갖추지 못한 건축 중인 건축물은 건조물에 해당하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 불완전한 건축 중 건축물에 관한 명시적 제외 규범이다.
- bounded sources:

  - `comm_001692_제319조_Ⅱ.2_15` / `Ⅱ.2`: “그러나 벽·기둥·지붕·천정 등을 완전히 갖추지 못한 건축 중인 건축물은 건조물에 해당하지 않는다.”

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

## 27. `art319_sec2_2.joint_occupier_entry`

- proposition: 공동관리 중인 건조물에 공동점유자 중 1인이 임의로 출입하였다고 하여 건조물침입죄는 성립하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 공동관리 및 공동점유의 관계가 확인된 경우의 명시적 예외다.
- bounded sources:

  - `comm_001692_제319조_Ⅱ.2_14` / `Ⅱ.2`: “공동관리 중인 건조물에 공동점유자 중의 1인이 임의로 출입하였다고 하여 건조물침입죄는 성립하지 않는다.”

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

## 28. `art319_sec2_2.managed_building_control`

- proposition: 관리하는 건조물로 인정되려면 타인의 함부로운 침입을 방지할 만한 인적·물적 설비를 갖추어야 하며, 사무적으로만 관리되는 건조물은 건조물침입죄의 객체가 될 수 없다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 침입 방지 설비와 관리의 실질은 개별 사실관계에서 평가가 필요하다.
- bounded sources:

  - `comm_001692_제319조_Ⅱ.2_14` / `Ⅱ.2`: “타인이 함 부로 침입하는 것을 방지할 만한 인적·물적 설비를 갖출 것을 요하고, 사무적으 로만 관리되는 건조물은 건조물침입죄의 객체가 될 수 없다.”

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

## 29. `art319_sec2_2.management_notice_insufficient`

- proposition: 단순히 출입금지 표지를 해둔 것만으로는 관리라고 할 수 없다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 출입금지 표지의 존재만으로 관리가 충족되는 것은 아니라는 제한이다.
- bounded sources:

  - `comm_001692_제319조_Ⅱ.2_14` / `Ⅱ.2`: “단순히 출입금지의 표지를 해둔 것 만으로는 관리라고 할 수 없다.”

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

## 30. `art319_sec2_2.public_place_management`

- proposition: 관공서의 출입구·계단, 역 구내, 백화점 등 공중에게 개방되어 사실상 출입이 자유로운 장소라도 정상적 용무가 있는 사람의 출입 편의를 위한 개방에 그치는 경우 관리되지 않는 장소라고 할 수 없다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 개방의 목적과 출입자의 용무가 정상적인지에 관한 평가가 필요하다.
- bounded sources:

  - `comm_001692_제319조_Ⅱ.2_14` / `Ⅱ.2`: “관공서의 출입구나 계단, 역 구내, 백화점 등 공중에게 개방되고 사실상 사람의 출입이 자유로운 장소도 그곳이 일반인에게 개방되어 있다는 이유는 그 직무와 관련하여 정상적인 용무를 가진 사람들의 출입 편의를 도모하기 위한 것에 지 나지 않으므로 관리되지 않는 장소라고 할 수 없다.”

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
