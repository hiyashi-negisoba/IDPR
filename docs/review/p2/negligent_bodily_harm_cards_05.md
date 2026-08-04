# 과실치사·업무상과실치사상 RuleIR 카드 검수 5

- unit: `negligent_bodily_harm`
- articles: art267, art268
- cards: 61–75 / 85
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #25 `art268.unlicensed_activity_work`: `art268.illicit_work_excluded` (status=`valid`)

## 61. `art268_sec2_2.gross_negligence_definition`

- proposition: 중과실은 행위자가 극히 근소한 주의로 결과발생을 인식할 수 있었음에도 부주의로 이를 인식하지 못한 경우를 말하며, 경과실과의 구별은 구체적 사안에서 사회통념을 고려하여 결정한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 극히 근소한 주의에 의한 인식 가능성과 사회통념에 따른 경과실 구별은 평가적 판단을 요구한다.
- bounded sources:

  - `comm_001692_제268조_Ⅱ.2_106` / `Ⅱ.2`: “중과실은 행위자가 극히 근소한 주의를 함으로써 결과발생을 인식할 수 있음에도 불구 하고 부주의로서 이를 인식하지 못한 경우를 말하는 것이고 경과실과의 구별은 구체적 인 경우에 사회통념을 고려하여 결정될 문제”

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

## 62. `art268_sec2_2.landlord_coal_gas_death`

- proposition: 임차 목적물의 방문 틈이나 가스배출시설 결함이 임차인의 통상 수선·관리의무에 속하는 정도라면, 임차인의 연탄가스 중독 사망에 대하여 임대인에게 중과실치사의 책임을 물을 수 없다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 결함의 성질과 수선·관리의무의 귀속이 임차인에게 있는지 검토한다.
- bounded sources:

  - `comm_001692_제268조_Ⅱ.2_106` / `Ⅱ.2`: “이는 임차인의 통상의 수선 및 관리의무에 속하는 것이므로 임차인이 그 방 에서 연탄가스에 중독되어 사망하였더라도 위 사고는 임차인이 그 의무를 게을리 함 으로써 발생한 것으로서 임대인에게 중과실치사의 죄책을 물을 수 없다.”

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

## 63. `art268_sec2_2.parking_entrance_collapse`

- proposition: 관리하는 주차장 출입구 문주에 도괴 위험이 있으면 보수 요청 외에도 임시 받침 설치, 접근 차단 등 인명피해 방지조치를 해야 하며, 보수 요구에만 그친 경우 중대한 과실이 인정될 수 있다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 관리 관계, 도괴 위험 인식 및 가능한 임시 안전조치의 구체적 사정을 검토한다.
- bounded sources:

  - `comm_001692_제268조_Ⅱ.2_104` / `Ⅱ.2`: “소유자에게 그 보수를 요청하는 외에 그 보수가 있을 때까 지 임시적으로라도 받침대를 세우는 등 도괴를 방지하거나 그 근처에 사람이나 자동 차 등의 근접을 막는 등 도괴로 인한 인명의 피해를 막도록 조치를 하여야 할 주의 의무가 있다 할 것이며”
  - `comm_001692_제268조_Ⅱ.2_104` / `Ⅱ.2`: “소유자에게 그 보수를 요구하는데 그쳤다면 그 주의의무를 심히 게을리 한 중대한 과실이 있다.”

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

## 64. `art268_sec2_2.pesticide_disguised_storage`

- proposition: 농약을 평소 판매하던 중조와 같은 모양으로 포장하여 점포 선반에 방치하고 가족에게 알리지 않아 사고가 발생한 경우 중과실치사의 책임을 면할 수 없다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소개된 판례의 구체적 보관·고지 사정에 한정된 중과실치사 판단으로 검토한다.
- bounded sources:

  - `comm_001692_제268조_Ⅱ.2_104` / `Ⅱ.2`: “농약을 평소에 신문지에 포장하여 판매하여 온 “중조”와 같은 모양으로 포장하여 점 포선반에 방치하고 가족에게 알리지 아니하여 사고가 발생하였다면 중과실치사의 죄 책을 면할 수 없다.”

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

## 65. `art268_sec2_2.pesticide_poisoning_home_treatment`

- proposition: 농약 음독 피해자를 병원에 이송하지 않고 집에서 치료하다 사망하게 한 사안에서, 제시된 사정만으로는 중과실이 있다고 볼 수 없다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 제시된 가정 치료 사정만으로 중과실을 인정하지 않은 좁은 판례 소개로 검토한다.
- bounded sources:

  - `comm_001692_제268조_Ⅱ.2_105` / `Ⅱ.2`: “부녀자가 음독하면 소문이 날까 봐 집안에서 치료를 하였다 하여도 중과실이 있 었다고 볼 수 없다.”

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

## 66. `art268_sec2_2.prayer_physical_force_death`

- proposition: 고령자 또는 어린이의 배와 가슴을 반복하여 세게 때리고 누르는 행위는 치명적 결과를 쉽게 예견할 수 있는데도 주의를 다하지 않은 경우 중대한 과실로 평가될 수 있다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 피해자의 취약성, 행사된 물리력 및 행위자의 예견 가능성을 구체적으로 검토한다.
- bounded sources:

  - `comm_001692_제268조_Ⅱ.2_104` / `Ⅱ.2`: “고령의 여자 노인이나 나이 어린 연약한 여자아이들은 약간의 물 리력을 가하더라도 골절이나 타박상을 당하기 쉽고, 더욱이 배나 가슴 등에 그와 같은 상처가 생기면 치명적 결과가 올 수 있다는 것은 피고인 정도의 연령이나 경험 지식을 가진 사람으로서는 약간의 주의만 하더라도 쉽게 예견할 수 있음에도”
  - `comm_001692_제268조_Ⅱ.2_104` / `Ⅱ.2`: “그러한 결과에 대하여 주의를 다하지 않아 사람을 죽음으로까지 이르게 한 행위는 중대한 과실이다.”

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

## 67. `art268_sec2_2.russian_roulette_failure_to_stop`

- proposition: 술자리 중 동료가 갑자기 러시안 룰렛을 하는 상황에서 경찰관들이 말로 만류하였으나 즉시 물리력으로 제지하지 못한 것만으로는 중과실치사죄 책임을 지울 위법한 주의의무위반으로 평가할 수 없다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 사고의 돌발성, 이미 한 만류 조치 및 즉시 물리력 제지의 현실적 가능성을 검토한다.
- bounded sources:

  - `comm_001692_제268조_Ⅱ.2_105` / `Ⅱ.2`: “이 사건 사고는 피고인들이 “장난치지 말라”며 말로 위 갑을 (신뢰의 원칙) 만류하던 중에 순식간에 일어난 사고여서”
  - `comm_001692_제268조_Ⅱ.2_105` / `Ⅱ.2`: “위와 같은 상황에서 피고인들이 이 사 건 “러시안 룰렛” 게임을 즉시 물리력으로 제지하지 못하였다 한들 그것만으로는 위 갑의 과실과 더불어 중과실치사죄의 형사상 책임을 지울 만한 위법한 주의의무위반 이 있었다고 평가할 수 없다.”

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

## 68. `art268_sec2_2.unextinguished_match_trash`

- proposition: 담배에 불을 붙인 성냥불이 꺼졌는지 확인하지 않은 채 휴지가 든 플라스틱 휴지통에 버린 행위는 중대한 과실에 해당한다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 점화원 확인 여부와 가연성 폐기물 용기의 구체적 상태를 검토한다.
- bounded sources:

  - `comm_001692_제268조_Ⅱ.2_104` / `Ⅱ.2`: “피고인이 성냥불로 담배를 붙인 다음 그 성냥불이 꺼진 것을 확인하지 아니한 채 휴 지가 들어 있는 플라스틱 휴지통에 던진 것은 중대한 과실이 있는 경우에 해당한다.”

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

## 69. `art268_sec2_2.unqualified_electrician_fire`

- proposition: 전문지식 없는 오락실 경영자가 무자격 전기기술자에게 공사를 맡긴 경우에도, 부실공사와 합선화재를 쉽게 예견하기 어려운 사정에서는 그 과실을 화재발생에 관한 중대한 과실로 평가하기 어렵다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 경영자의 전기 전문지식 유무와 부실공사·합선화재의 예견 가능성을 검토한다.
- bounded sources:

  - `comm_001692_제268조_Ⅱ.2_106` / `Ⅱ.2`: “전기에 관한 전문지식이 없는 오락실경영자로서는”
  - `comm_001692_제268조_Ⅱ.2_106` / `Ⅱ.2`: “위 오락실경영자에게 위와 같은 과실이 있었더라도 사회통념상 이를 화재발생에 관한 중대한 과실이라고 평가하기는 어렵다.”

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

## 70. `art268_sec3_2.dangerous_driving_inclusion`

- proposition: 음주로 인한 위험운전치사상죄가 성립하면, 형법 제268조의 죄를 범한 것을 내용으로 하는 교통사고처리특례법위반죄는 흡수되어 별죄를 구성하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 댓글의 선행 문맥상 음주로 인한 위험운전치사상죄 성립을 전제로 한 흡수 관계이며 원판례 확인이 필요하다.
- bounded sources:

  - `comm_001692_제268조_Ⅲ.2_111` / `Ⅲ.2`: “따라서 그 죄가 성립하는 때에는 차의 운전자가 형법 제268조의 죄를 범한 것을 내용으로 하는 교통사고처리특례법위반죄는 그 죄에 흡수되어 별죄 를 구성하지 아니한다.”

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

## 71. `art268_sec3_2.drunk_driving_negligent_injury`

- proposition: 주취운전으로 사고를 내어 인명을 살상한 경우, 주취운전이 사고 과실의 원인이 되었더라도 음주운전 도로교통법위반죄와 업무상과실치사상죄가 성립하며 상호 실체적 경합범이.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 주취운전과 사고 결과 및 과실의 관계를 해당 사실관계에서 검토해야 한다.
- bounded sources:

  - `comm_001692_제268조_Ⅲ.2_109` / `Ⅲ.2`: “주취 중 운전으로 사고를 내어 인명을 살상한 경우 주취 운전이 사고를 낸 과실 의 원인이 되었다 하더라도 음주운전으로 인한 도로교통법위반죄와 업무상과실 치사상죄가 성립하고”
  - `comm_001692_제268조_Ⅲ.2_109` / `Ⅲ.2`: “상호간의 관계는 실체적 경합범이다.”

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

## 72. `art268_sec3_2.failure_to_rescue_after_accident`

- proposition: 운전자가 업무상 또는 중과실로 사람을 상해에 이르게 하거나 재물을 손괴하고도 사고 후 필요한 구호조치를 하지 않은 경우, 업무상·중과실치상죄 또는 과실재물손괴죄 외에 도로교통법상 조치의무위반죄가 성립하며 실체적 경합범이 된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 사고 후 필요한 조치의 이행 여부와 선행 범죄의 성립을 검토해야 한다.
- bounded sources:

  - `comm_001692_제268조_Ⅲ.2_109` / `Ⅲ.2`: “차의 운전자가 업무상과실 또는 중과실에 의하여 사람을 상해에 이르게 하거나 재물을 손괴하고 같은 법 제54조 제1항 소 정의 구호조치 등 필요한 조치를 취하지 아니한 경우에는 업무상과실, 중과실치 상죄 또는 같은 법 제151조의 죄외에 같은 법 제148조의 죄가 성립하고 이는 실 체적 경합범이라고 보아야 한다.”

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

## 73. `art268_sec3_2.hit_and_run_inclusion`

- proposition: 도주차량운전자의 가중처벌죄가 성립하는 경우 업무상과실치사상죄는 그 죄에 포함되어 별죄를 구성하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`precedent_position`, review_required=`False`
- source track: `unit_core`
- prior note: 도주차량운전자의 가중처벌죄 성립을 전제로 한 업무상과실치사상죄의 포함 관계다.
- bounded sources:

  - `comm_001692_제268조_Ⅲ.2_111` / `Ⅲ.2`: “특정범죄가중처벌등에관한법률 제5조의3 제1항 소정 (도주차량운전자의 가중처벌) 의 죄는 형법 제268조의 죄를 범한 당해 차량의 운전자가 피 (업무상과실치사상죄) 해자를 구호하는 등 도로교통법 제54조 제1항의 규정에 의한 조치를 취하지 아 니하고 도주한 때에 성립하는 것으로서 업무상과실치사상죄는 위의 죄에 포함 되어 있는 것이므로, 별죄를 구성하지 아니한다.”

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

## 74. `art268_sec3_2.imaginary_concurrence_single_act`

- proposition: 상상적 경합에서 1개의 행위란 법적 평가를 떠나 사회관념상 사물자연의 상태로서 하나로 평가되는 행위를 의미한다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 사회관념상 행위 단일성은 구체적 사실관계에 대한 평가를 필요로 하며 원판례 확인이 필요하다.
- bounded sources:

  - `comm_001692_제268조_Ⅲ.2_110` / `Ⅲ.2`: “여기 에서 1개의 행위라 함은 법적 평가를 떠나 사회관념상 행위가 사물자연의 상태로서 1개로 평가되는 것을 의미한다”

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

## 75. `art268_sec3_2.industrial_safety_negligent_death`

- proposition: 도로공사 현장소장이 지반붕괴 위험 방지조치를 하지 않아 산업안전보건법상 의무위반 및 업무상과실로 근로자를 사망하게 한 경우, 두 의무가 일치하여 상상적 경합 관계라는 사례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 댓글에 소개된 사례의 원판례와 사실관계를 확인해야 한다.
- bounded sources:

  - `comm_001692_제268조_Ⅲ.2_110` / `Ⅲ.2`: “위의 산업안전보건법상의 위험방지조치의무와 업무상주의의무가 일치하고 이는 1개의 행위가 2개의 업무 상과실치사죄와 산업안전보건법위반죄에 해당하고, 둘 사이는 상상적 경합 관계 에 해당한다.”

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
