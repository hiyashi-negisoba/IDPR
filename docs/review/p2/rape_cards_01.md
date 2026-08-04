# 강간 RuleIR 카드 검수 1

- unit: `rape`
- articles: art297
- cards: 1–15 / 56
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 1. `art297.conduct.violence-threat-rape`

- proposition: 강간죄의 행위는 폭행 또는 협박으로 사람을 강간하는 것이다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 폭행 또는 협박과 강간으로 구성된 행위 요소를 기록한 카드이며, 개별 사실의 해당 여부는 후속 검토가 필요하다.
- bounded sources:

  - `comm_001692_제297조_Ⅳ_7` / `Ⅳ`: “본죄의 행위는 ‘폭행 또는 협박’으로 사람을 ‘강간’하는 것이다.”

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

## 2. `art297.indirect_perpetration`

- proposition: 강간죄는 자수범이 아니므로 간접정범 형태로 범할 수 있다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 강간죄가 자수범이 아니라는 설명에 한정하여 간접정범 가능성을 반영한다.
- bounded sources:

  - `comm_001692_제297조_Ⅱ_1` / `Ⅱ`: “강간죄는 자수범 (⾃ 이 아니므로, 간접정범의 형태로 본죄를 범하는 것도 가능하다.”

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

## 3. `art297.object-person`

- proposition: 강간죄의 객체는 남녀를 불문한 사람이며, 성년·미성년, 기혼 여부, 음행 상습, 기존 성관계 경험 및 성교능력 유무를 불문한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 객체가 사람인지와 열거된 개인적 사정은 분리 가능한 사실 확인 항목으로 검토한다.
- bounded sources:

  - `comm_001692_제297조_Ⅲ.1_2` / `Ⅲ.1`: “본죄의 객체는 ‘사람’이고 남성과 여성을 불문한다.”
  - `comm_001692_제297조_Ⅲ.1_2` / `Ⅲ.1`: “‘사람’인 이상 성년, 률 제11574호) 미성년, 기혼 여부, 음행의 상습 유무, 기존 성관계 경험 유무, 성교능력 유무 등 을 불문한다.”

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

## 4. `art297.relative_special_act`

- proposition: 피해자와 4촌 이내 혈족·인척, 동거 친족 또는 동거 사실상 친족 관계에 있는 자가 범한 경우 성폭력범죄의 처벌 등에 관한 특례법 제5조 제1항이 적용된다고 소개되어 있다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 특례법 조문 원문과 적용 요건 및 법정형은 현재 commentary의 보고 범위에서만 확인되므로 검토가 필요하다.
- bounded sources:

  - `comm_001692_제297조_Ⅱ_1` / `Ⅱ`: “피해자와 사이에 4촌 이내의 혈족·인척과 동거하는 친족 또는 동거하는 사실상의 관계에 있는 친족 관계에 있는 자가 본죄를 범하였을 경우에는 법정 형이 더 높은 성폭력범죄의 처벌 등에 관한 특례법 제5조 제1항”

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

## 5. `art297.special-protection-statutes`

- proposition: 피해자가 13세 미만자, 신체적·정신적 장애인 또는 아동·청소년인 경우에는 법정형이 더 높은 특별법 규정이 적용된다고 소개되어 있다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 특별법 적용 및 법정형 가중을 소개하는 예외 카드이며, 각 특별법 조문의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제297조_Ⅲ.1_2` / `Ⅲ.1`: “다만 피해자가 13세 미만의 사람일 경우에는 법정형이 더 높은 성폭력범죄의 처 벌 등에 관한 특례법 제7조 제1항이”
  - `comm_001692_제297조_Ⅲ.1_2` / `Ⅲ.1`: “그리고 피해자가 ‘신체적인 또는 정신적인 장애가 있는 사람’인 경우에는 법정형이 더 높은 성폭력범죄의 처벌 등에 관한 특례법 제6조 제1항 이 적용될 것이다.”
  - `comm_001692_제297조_Ⅲ.1_2` / `Ⅲ.1`: “또한 피해자가 ‘아동·청”
  - `comm_001692_제297조_Ⅲ.1_2` / `Ⅲ.1`: “(19세 미만의 자. 다만 19세에 도달하는 연도의 1월 1일을 맞이한 자는 제외)”
  - `comm_001692_제297조_Ⅲ.1_2` / `Ⅲ.1`: “우에는 법정형이 더 높은 아동·청소년의 성보호에 관한 법률 제7조 제1항”

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

## 6. `art297.unrestricted_principal`

- proposition: 강간죄의 주체에는 제한이 없고 남성과 여성 모두 주체가 될 수 있다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 주체의 성별 제한이 없다는 commentary synthesis를 반영한 카드다.
- bounded sources:

  - `comm_001692_제297조_Ⅱ_1` / `Ⅱ`: “본죄의 주체에는 아무런 제한이 없다.”
  - `comm_001692_제297조_Ⅱ_1` / `Ⅱ`: “현재 본죄의 객체가 ‘사람’ 으로 변경되었으므로 남성과 여성 모두 본죄의 주체가 된다.”

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

## 7. `art297_sec1.rape_definition`

- proposition: 강간죄는 폭행 또는 협박으로 사람을 강간함으로써 성립하는 범죄이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 폭행 또는 협박, 사람, 강간의 개념과 구체적 사실관계 적용 범위는 현재 인용문만으로 확정하지 않는다.
- bounded sources:

  - `comm_001692_제297조_Ⅰ_0` / `Ⅰ`: “본죄는 폭행 또는 협박으로 ‘사람’을 강간함으로써 성립하는 범죄이다.”

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

## 8. `art297_sec10.planned_killing_after_rape_no_self_defense`

- proposition: 계속 성관계를 강요받던 피해자가 남자 친구와 사전 공모하여 범행을 준비하고, 술에 취해 잠든 의붓아버지를 식칼로 살해한 경우 사회통념상 상당성이 결여되어 정당방위가 인정되지 않은 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 사회통념상 상당성 결여를 이유로 정당방위를 부정한 소개 판례의 사실관계 한정 사례이며, 판례 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제297조_Ⅹ_27` / `Ⅹ`: “의붓아버지가 술에 취하여 잠을 자고 있어 제대로 반항 할 수 없는 상태에서 식칼로 심장을 찔러 살해한 행위에 대하여는 사회통념상 의 상당성 결여를 이유로 정당방위를 인정하지 않았다.”

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

## 9. `art297_sec10.self_defense_against_rape`

- proposition: 피해자가 행위자의 폭행·협박에 의한 강간에 대항하여 방어 또는 적극적 반격행위를 한 경우, 자신의 법익에 대한 현재의 부당한 침해를 방위하기 위한 것이고 상당한 이유가 있으면 정당방위로 위법성이 조각된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 현재의 부당한 침해를 방위하기 위한 것인지와 상당한 이유의 유무는 개별 사실관계에 대한 평가를 필요로 한다.
- bounded sources:

  - `comm_001692_제297조_Ⅹ_27` / `Ⅹ`: “그러한 행위가 자신의 법익에 대한 현재의 부당한 침해를 방위하기 위한 것으로서 상당한 이유가 있다고 인 정할 수 있을 때에는 정당방위로서 위법성이 조각된다.”

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

## 10. `art297_sec10.tongue_biting_self_defense`

- proposition: 심야에 귀가 중인 피해자가 공동으로 강간하려는 행위자에게 끌려가 폭행·추행을 당하던 중 정조와 신체를 지키려 혀를 깨물어 혀 절단상을 입힌 경우 정당방위가 인정된 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소개된 판례의 구체적 사실관계에 한정된 정당방위 인정 사례이며, 판례 원문 확인 전에는 commentary-reported precedent로 취급한다.
- bounded sources:

  - `comm_001692_제297조_Ⅹ_27` / `Ⅹ`: “피해자가 자신의 정조와 신체를 지키 려는 일념에서 엉겁결에 피고인 1의 혀를 깨물어 혀 절단상을 입힌 경우에 정당 방위를 인정하였다.”

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

## 11. `art297_sec3_2.spouse_rape_holding`

- proposition: 실질적 부부관계가 유지되는 경우에도 남편이 반항을 불가능하거나 현저히 곤란하게 할 정도의 폭행·협박으로 아내를 간음하면 강간죄가 성립할 수 있다는 전원합의체 판결의 입장이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 주석이 소개한 전원합의체 판결의 입장이다. 원판례를 사용자 primary precedent index에서 확인하기 전에는 배우자 객체성에 관한 경쟁 견해보다 우선하는 정책으로 확정하지 않는다.
- bounded sources:

  - `comm_001692_제297조_Ⅲ.2_3` / `Ⅲ.2`: “전 원합의체 판결을 통해 실질적으로 부부관계가 유지된다고 하더라도 남편의 부 인에 대한 강간죄가 성립할 수 있다고 판단하였다.”
  - `comm_001692_제297조_Ⅲ.2_4` / `Ⅲ.2`: “혼인관계가 파탄된 경우뿐만 아니라 혼인관계가 실질적으로 유지되고 있 는 경우에도 남편이 반항을 불가능하게 하거나 현저히 곤란하게 할 정도의 폭행이나 협박을 가하여 아내를 간음한 경우에는 강간죄가 성립한다고 보아야 한다.”

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

## 12. `art297_sec3_2.spouse_violence_assessment`

- proposition: 배우자 강간에서 폭행·협박이 반항을 불가능하거나 현저히 곤란하게 할 정도인지 여부는 폭행·협박의 내용·정도, 유형력 행사 경위, 혼인생활 형태, 평소 성행, 성교 당시 및 이후 상황 등을 종합하여 신중히 판단한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 폭행·협박의 정도는 열거 사정을 종합하는 평가 판단을 요구한다. 소개된 판례 기준의 원문 및 적용 범위를 확인해야 한다.
- bounded sources:

  - `comm_001692_제297조_Ⅲ.2_4` / `Ⅲ.2`: “그 폭행 또는 협박의 내 용과 정도가 아내의 성적 자기결정권을 본질적으로 침해하는 정도에 이른 것인지 여 부, 남편이 유형력을 행사하게 된 경위, 혼인생활의 형태와 부부의 평소 성행, 성교 당시와 그 후의 상황 등 모든 사정을 종합하여 신중하게 판단하여야 한다.”

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

## 13. `art297_sec3_4.intercourse_opposite_sex`

- proposition: 강간죄의 간음행위는 남성 성기의 여성 성기 삽입 또는 양 성기의 결합을 의미하므로, 단독정범의 경우 행위주체와 객체는 서로 다른 성이어야 한다는 설명이 제시되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 간음행위 및 단독정범의 행위주체·객체 성별 요건의 적용 범위는 성 분류 기준과 함께 검토가 필요하다.
- bounded sources:

  - `comm_001692_제297조_Ⅲ.4_6` / `Ⅲ.4`: “본죄의 구성요건인 ‘간음행위’ 는 남성 성기의 여성 성기에 삽입 내지 남성의 성기와 여성의 성기의 결합을 의 미하므로”
  - `comm_001692_제297조_Ⅲ.4_6` / `Ⅲ.4`: “체의 성별에 따라 동일한 성의 사람은 강간의 단독정범의 주체가 될 수 없다.”

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

## 14. `art297_sec3_4.sex_classification`

- proposition: 강간죄에서 남성과 여성의 구별은 성염색체보다 개인의 성귀속감, 사회적·규범적 성 및 일반인의 평가를 종합하여 판단하는 것이 타당하다는 견해가 제시되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 성귀속감, 사회적·규범적 성 및 일반인의 평가를 종합하는 판단 기준의 구체화가 필요하다.
- bounded sources:

  - `comm_001692_제297조_Ⅲ.4_6` / `Ⅲ.4`: “남성과 여성의 구별은 발생학적인 성인 성염색체의 구성을 판단인자로 삼 기보다는 개인의 성귀속감을 고려하여 사회적·규범적 성 및 사회 일반인의 평 가를 종합적으로 판단하는 것이 타당하다.”

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

## 15. `art297_sec4_1.direct_violence_threat`

- proposition: 강간죄의 폭행·협박은 행위자가 직접 가한 것이어야 하며, 타인의 폭행·협박을 이용해 간음한 경우에는 준강간죄가 성립할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 직접 가한 폭행·협박이라는 제297조 수단요건에 관한 설명이다. 타인 행위의 이용관계와 준강간죄 적용은 구체적 사실관계 검토가 필요하다.
- bounded sources:

  - `comm_001692_제297조_Ⅳ.1_8` / `Ⅳ.1`: “폭행·협박은 행위자가 직접 가한 것이어야 하고, 타인이 행한 폭행·협박을 이용 하여 간음했을 때에는 준강간죄가 성립할 수 있다.”

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
