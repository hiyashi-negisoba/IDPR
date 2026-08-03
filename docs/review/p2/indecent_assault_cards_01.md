# 강제추행 RuleIR 카드 검수 1

- unit: `indecent_assault`
- articles: art298
- cards: 1–15 / 33
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #26 `art298_sec3_2.indecent_act_scope`: `art298_sec3_2.indecent_act_no_body_part_distinction` (status=`valid`)

## 1. `art298.indirect_perpetration.victim_as_instrument`

- proposition: 피해자를 도구로 삼아 피해자의 신체를 이용하여 추행행위를 한 경우에도 강제추행죄의 간접정범에 해당할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 피해자를 도구로 삼았는지와 그 신체 이용이 추행행위에 해당하는지는 사실관계별 평가가 필요하다.
- bounded sources:

  - `comm_001692_제298조_Ⅱ_1` / `Ⅱ`: “피해자를 도구로 삼아 피해자의 신체를 이용하 여 추행행위를 한 경우에도 강제추행죄의 간접정범에 해당할 수 있다.”

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

## 2. `art298.object.person`

- proposition: 강제추행죄의 객체는 사람이며, 성별·성년·미성년·기혼 여부를 불문한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 객체 범위에 관한 해설상의 분류를 반영하며, 특별법 적용 여부는 별도 예외 카드에서 검토한다.
- bounded sources:

  - `comm_001692_제298조_Ⅱ_1` / `Ⅱ`: “본죄의 객체는 ‘사람’이고, 성별, 성년, 미성년, 기혼 여부 등을 불문한다.”

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

## 3. `art298.offense_conduct`

- proposition: 강제추행죄는 폭행 또는 협박으로 사람에 대하여 추행을 함으로써 성립하는 범죄이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 폭행·협박 및 추행 해당성은 사실관계에 대한 평가가 필요하다. 폭행·협박의 요구 정도에 관한 견해대립은 현재 제공된 후보 및 인용문에 포함되지 않았다.
- bounded sources:

  - `comm_001692_제298조_Ⅰ_0` / `Ⅰ`: “본죄는 폭행 또는 협박으로 사람에 대하여 추행을 함으로써 성립하는 범죄이다.”

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

## 4. `art298.spousal_victim.precedent_position`

- proposition: 해설은 판례가 부부 사이의 강제추행죄 성립을 인정하고 있다고 보고한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 이는 해설이 보고한 판례 입장이다. 판례 원문 및 배우자 객체성에 관한 소개된 견해대립을 사용자 제공 primary precedent index와 대조하여 확인해야 한다.
- bounded sources:

  - `comm_001692_제298조_Ⅱ_1` / `Ⅱ`: “판례는 부부 사이의 강간죄 성립을 긍 정하는 것과 마찬가지로 [대법원 2012. 12. 18. 선고 2012도14788 전원합의체 판결(다수의견)] 부부 사이의 강제추행죄 성립을 인정하고 있다”

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

## 5. `art298.subject.unrestricted`

- proposition: 강제추행죄의 주체에는 제한이 없고 남성과 여성 모두 주체가 될 수 있다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 주체의 성별 및 일반적 자격 제한 부재를 기계적으로 열거하는 카드다.
- bounded sources:

  - `comm_001692_제298조_Ⅱ_1` / `Ⅱ`: “본죄의 주체에는 아무런 제한이 없다. 남성과 여성 모두 본죄의 주체가 될 수 있다.”

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

## 6. `art298_sec3_1.force_threat_totality_assessment`

- proposition: 어떤 행위가 강제추행죄의 폭행 또는 협박에 해당하는지는 목적과 의도, 행위태양·내용, 경위·당시 정황, 당사자 관계 및 상대방 고통 등을 종합하여 판단한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 열거 사정을 기계적으로 충족 여부로 처리하지 않고, 개별 사실관계에 대한 종합적 평가 입력으로 검토해야 한다.
- bounded sources:

  - `comm_001692_제298조_Ⅲ.1_5` / `Ⅲ.1`: “어떠한 행위가 강제추행죄의 ‘폭행 또는 협박’에 해당하는지 여부는 행위의 목적 과 의도, 구체적인 행위태양과 내용, 행위의 경위와 행위 당시의 정황, 행위자와 상대방과의 관계, 그 행위가 상대방에게 주는 고통의 유무와 정도 등을 종합하 여 판단하여야 한다.”

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

## 7. `art298_sec3_1.surprise_molestation_physical_force`

- proposition: 폭행행위 자체가 곧바로 추행행위에 해당하는 기습추행에서는 상대방 의사에 반하는 유형력 행사가 있으면 힘의 대소강약을 불문하여 폭행이 인정된다는 판례 입장이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 기습추행이라는 제한된 경우의 보고된 판례 입장이다. 원문 판례로 사실관계 및 적용 범위를 확인하기 전에는 일반적 폭행 기준으로 확장하지 않아야 한다.
- bounded sources:

  - `comm_001692_제298조_Ⅲ.1_6` / `Ⅲ.1`: “폭행행위 그 자체가 곧바로 추행행위에 해당하는 경우, 이른바 ‘기습추 행’의 경우 ”상대방의 의사에 반하는 유형력의 행사가 있는 이상 그 힘의 대소 강 약을 불문하고 폭행이 있다고 보아야 한다.”고 판단하고 있다.”

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

## 8. `art298_sec3_2.indecent_act_comprehensive_assessment`

- proposition: 추행 해당 여부는 피해자의 의사·성별·연령, 행위자와 피해자의 관계, 경위, 구체적 행위태양, 객관적 상황 및 시대의 성적 도덕관념 등을 종합하여 신중히 판단한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 열거된 사정을 종합하는 평가 기준이므로 기계적으로 충족 여부를 결정하지 않는다.
- bounded sources:

  - `comm_001692_제298조_Ⅲ.2_8` / `Ⅲ.2`: “이에 해당하는지는 피해자의 의사, 성별, 연령, 행위자와 피해자의 이전부터의 관계, 행위에 이르게 된 경위, 구체적 행위태양, 주위의 객관적 상황과 그 시대의 성적 도덕관념 등을 종합적으로 고려 하여 신중히 결정되어야 한다.”

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

## 9. `art298_sec3_2.indecent_act_definition`

- proposition: 추행은 객관적으로 일반인에게 성적 수치심 또는 혐오감을 일으키고 선량한 성적 도덕관념에 반하여 피해자의 성적 자유를 침해하는 행위이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 성적 자유 침해와 성적 수치심·혐오감 판단에는 구체적 사실관계 평가가 필요하다.
- bounded sources:

  - `comm_001692_제298조_Ⅲ.2_8` / `Ⅲ.2`: “‘추행’이란 객관적으로 일반인에게 성적 수치심이나 혐오감을 일으키게 하고 선량한 성적 도덕관념에 반하는 행위로서 피해자의 성적 자유를 침해하는 것”

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

## 10. `art298_sec3_2.indirect_perpetration`

- proposition: 강제추행죄는 정범 자신이 직접 범죄를 실행해야만 성립하는 자수범이 아니므로, 처벌되지 않는 타인을 도구로 이용하는 간접정범 형태로도 범할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 도구 이용자와 피해자의 행위·통제 관계에 대한 법적 평가는 별도 검토가 필요하다.
- bounded sources:

  - `comm_001692_제298조_Ⅲ.2_12` / `Ⅲ.2`: “강제추행죄는 사람의 성적 자유 내지 성적 자기결정의 자유를 보호하기 위한 죄로서 정범 자신이 직접 범죄를 실행하여야 성립하는 자수범이라고 볼 수 없 으므로, 처벌되지 아니하는 타인을 도구로 삼아 피해자를 강제로 추행하는 간접 정범의 형태로도 범할 수 있다.”

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

## 11. `art298_sec3_2.indirect_perpetration_coerced_self_sexual_acts`

- proposition: 피고인이 협박으로 겁먹은 피해자들에게 나체 또는 속옷 상태에서 스스로 촬영하거나 성기에 이물질 삽입 또는 자위를 하게 한 경우 강제추행죄의 간접정범에 해당할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 협박, 피해자의 불가피한 자기행위 및 도구 이용 관계가 충족되는지 개별적으로 평가해야 한다.
- bounded sources:

  - `comm_001692_제298조_Ⅲ.2_13` / `Ⅲ.2`: “피고인이 피해자들을 협박하여 겁을 먹은 피해 자들로 하여금 어쩔 수 없이 나체나 속옷만 입은 상태가 되게 하여 스스로를 촬 영하게 하거나, 성기에 이물질을 삽입하거나 자위를 하는 등의 행위를 하게 하 였다면 강제추행죄의 간접정범에 해당할 수 있다.”

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

## 12. `art298_sec3_2.no_contact_assessment_factors`

- proposition: 신체 접촉 없는 행위가 강제추행에 해당하는지는 피해자의 의사·성별·연령, 당사자 관계, 경위, 구체적 행위태양 및 객관적 상황 등을 종합 고려하여 판단한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 비접촉 상황에 특화된 종합 판단 요소이며, 일반 추행 판단 카드와 별도로 검토한다.
- bounded sources:

  - `comm_001692_제298조_Ⅲ.2_12` / `Ⅲ.2`: “이에 해당하는지 여부는 피해자의 의사·성별·연령, 행위자와 피해자의 관계, 그 행위에 이르게 된 경위, 구체적 행위태양, 주위의 객관적 상황 등을 종 합적으로 고려하여 정하여진다.”

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

## 13. `art298_sec3_2.no_contact_elevator_threat_masturbation`

- proposition: 폐쇄된 엘리베이터에서 피해자들을 칼로 위협하여 실력적으로 지배한 뒤 자위행위 모습을 보여주고 피하거나 외면할 수 없게 한 경우, 신체 접촉 없이도 강제추행이 인정된 사례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소개된 비접촉 인정 사례의 구체적 사실관계에 한정하여 검토한다.
- bounded sources:

  - `comm_001692_제298조_Ⅲ.2_12` / `Ⅲ.2`: “피고인이 엘리베이터라는 폐쇄된 공간에서 피해자들을 칼로 위협하는 등으로 꼼짝하지 못하도록 자신의 실력적인 지배하에 둔 다음 피해자들에게 자신의 자위행위 모습을 보여 주고 피해자들로 하 여금 이를 외면하거나 피할 수 없게 한 경우”

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

## 14. `art298_sec3_2.no_contact_equivalent_infringement`

- proposition: 신체 접촉이 없더라도 성적 수치심·혐오감 또는 성적 자기결정권 침해가 신체 접촉이 있는 경우와 동등한 정도라고 평가되면 강제추행죄 성립을 인정할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 비접촉 행위의 침해 정도가 접촉 행위와 동등한지 여부는 규칙화하지 않고 평가 입력으로 처리한다.
- bounded sources:

  - `comm_001692_제298조_Ⅲ.2_12` / `Ⅲ.2`: “신체 적 접촉이 없는 경우라고 하더라도 성적 수치심 내지 혐오감의 정도나 그로 인 한 성적 자기결정권의 침해가 피해자의 신체에 대한 접촉이 있는 경우와 비교 하여 동등한 정도라고 평가될 수 있는 경우라면 강제추행죄의 성립을 인정할 수 있다.”

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

## 15. `art298_sec3_2.no_contact_kitchen_gesture_not_molestation`

- proposition: 중국음식점 주방장이 주방에서 여성 피해자에게 성기 모양을 손으로 만들고 반바지를 벌리며 보여주겠다고 말한 경우에는 신체 접촉 없는 강제추행이 인정되지 않은 사례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소개된 개별 비인정 사례이며, 신체 접촉 없는 성적 언동 전반에 대한 부정 규칙으로 확장하지 않는다.
- bounded sources:

  - `comm_001692_제298조_Ⅲ.2_12` / `Ⅲ.2`: “중국음식점 주방장이 주방 내에서 반바 으로 ‘추행’을 하였다고 볼 수 없음) 지 차림으로 의자에 앉아 있다가 역시 주방 내에 앉아 있던 여자 피해자를 불러 서 피해자가 쳐다보자 손으로 성기 모양을 만들고 반바지를 벌리면서 ‘보여줄까’ 라고 말한 경우”

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
