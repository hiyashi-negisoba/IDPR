# 과실치사·업무상과실치사상 RuleIR 카드 검수 4

- unit: `negligent_bodily_harm`
- articles: art267, art268
- cards: 46–60 / 85
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #25 `art268.unlicensed_activity_work`: `art268.illicit_work_excluded` (status=`valid`)

## 46. `art268.train_signal_confirmation`

- proposition: 열차 운전에서 신호 확인은 기본적 의무이므로, 이를 태만히 한 행위는 어떠한 이유가 있어도 주의의무위반을 면할 수 없다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 신호 확인 여부는 운행기록·통신기록 등으로 검증 가능하다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_53` / `Ⅰ.2`: “신호확인의무는 열차운전의 기본으로서 이를 태만히 한 행위는 어떤 이유가 있었다고 해도 주의의무위반이 됨을 면할 수 없다.”

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

## 47. `art268.vertical_medical_division_supervision`

- proposition: 수련병원 등에서 주된 의사가 지휘·감독 관계의 다른 의사에게 특정 의료행위를 위임하는 수직적 분업에서는, 그 다른 의사에게 전적으로 위임된 경우가 아닌 이상 주된 의사는 자신이 주로 담당하는 환자에 대한 다른 의사의 의료행위가 적절한지 확인·감독할 업무상 주의의무가 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 전적 위임 여부, 주된 담당의 지위 및 구체적 감독 범위를 진료기록으로 확인해야 한다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_16` / `Ⅰ.2`: “수련병원의 전문의와 전공의 등의 관계처럼 의료기관 내의 직책상 주된 의사의 지위에서 지휘·감독 관계에 있는 다른 의사에게 특정 의료행위를 위임하는 수직적 분업의 경우에는, 그 다른 의사에게 전적으로 위임된 것이 아닌 이상 주된 의사는 자신이 주로 담당하는 환자에 대하여 다른 의사가 하는 의료행위의 내용이 적절한 것인지 여부를 확인하고 감독하여야 할 업무상 주의의무가 있고”
  - `comm_001692_제268조_Ⅰ.2_69` / `Ⅰ.2`: “그 다른 의사에게 전적으로 위임된 것이 아닌 이상 주된 의사는 자신이 주로 담당하는 환자에 대하여 다른 의사가 하는 의료행위의 내용이 적절한 것인지 여부를 확인하고 감독하여야 할 업무상 주의의무가 있고”

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

## 48. `art268.victim_negligence_no_exemption`

- proposition: 교통사고가 피고인의 전적인 과실만으로 발생한 것이 아니라 피해자 과실도 경합했다는 사정만으로 피고인이 사고 책임을 면할 수는 없다는 판례의 일반적 입장이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 피해자 과실이 독립적·비정상적 개입으로 인과관계 또는 객관적 귀속을 끊는지 여부는 별도 검토한다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_18` / `Ⅰ.2`: “판례도 일반적으로는 교통사고가 피고인의 전적인 과실로 인하여 발생한 것이 아니라 피해자의 과실도 경합하여 발생하였다는 이유로 피고인이 그 교통사고에 대한 책임을 면할 수는 없다고 하고는 있다.”

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

## 49. `art268_sec1_1.medical_negligence_professional_benchmark`

- proposition: 의료사고에서 의료종사자의 과실은 결과 예견·회피 가능성에도 예견·회피하지 못하였는지와, 같은 업무·직무 종사 일반적 보통인의 주의 정도를 기준으로 사고 당시 의학 수준·의료환경·조건 및 의료행위 특수성을 고려하여 판단한다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 주석이 소개한 판례 기준이므로 원판례를 사용자 primary precedent index에서 확인하기 전에는 commentary-reported precedent로만 취급한다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.1_0` / `Ⅰ.1`: “의료사고에 있어서 의료종사 자의 과실을 인정하기 위해서는 의료종사자가 결과발생을 예견할 수 있었음에도 그 결과발생을 예견하지 못하였고 그 결과발생을 회피할 수 있었음에도 그 결 과발생을 회피하지 못한 과실이 검토되어야 하고, 그 과실의 유무를 판단함에는 같은 업무와 직무에 종사하는 일반적 보통인의 주의 정도를 표준으로 하여야 하며, 이에는 사고 당시의 일반적인 의학의 수준과 의료환경 및 조건, 의료행위의 특수성 등이 고려되어야 한다.”

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

## 50. `art268_sec1_1.non_punishable_against_victim_intent`

- proposition: 업무상과실치사상죄는 상해 결과만 발생한 경우에도 반의사불벌죄에 해당하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 상해 결과만 발생한 경우에도 피해자 의사에 따른 불처벌 효과가 없다는 명시적 부정 규범으로 검토한다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.1_0` / `Ⅰ.1`: “무상 과실치사상죄는 상해의 결과만 발생하였다고 하더라도 반의사불벌죄에 해 당하지 아니한다.”

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

## 51. `art268_sec1_1.objective_duty_in_risky_work`

- proposition: 생명·신체 위험을 초래할 수 있는 업무영역에서는 해당 업무 참여자 전부에게 구성요건 단계의 객관적 주의의무로서 더 높은 수준의 주의의무가 요구될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 해당 업무영역의 위험성과 객관적으로 정상적으로 기울여야 할 주의 수준은 개별 사안에서 평가가 필요하다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.1_0` / `Ⅰ.1`: “입법자가 업무 참여 자에게 보다 더 높은 수준의 주의의무를 부과할 수 있다. 이 경우 부과된 높은 수준의 주의의무는 책임 단계에서 논의되는 개별적인 행위자에 대한 것이 아니 라 구성요건 단계에서 해당 업무 영역에 참여하는 사람들 전부에게 ‘정상적으로 기울여야 할 주의’로 요구되는 객관적 주의의무이다.”

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

## 52. `art268_sec1_1.offense_overview`

- proposition: 업무상 과실로 사람을 사망 또는 상해에 이르게 한 경우 업무상과실치사상죄가 성립한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 업무상 과실, 사망 또는 상해 결과, 그리고 결과 발생의 기본 구성요소를 요약한 카드다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.1_0` / `Ⅰ.1`: “본죄는 업무상의 과실로 인하여 사람을 사망이나 상해에 이르게 함으로써 성립 하는 범죄이다.”

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

## 53. `art268_sec1_1.status_aggravated_offense`

- proposition: 업무상과실치사상죄는 행위주체가 업무자라는 신분을 이유로 형이 가중되는 신분적 가중유형이다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 업무자 신분이 형 가중의 기준이라는 점을 나타내며, 가중 근거에 관한 이론 선택은 별도 변형 카드에서 보류한다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.1_0` / `Ⅰ.1`: “업무상 과실치사상죄는 그 행위의 주체가 업무자라는 이유로 형이 가중되는 신 분적 가중유형이라는 점에 대하여는 이론이 없다.”

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

## 54. `art268_sec2_1.gross_negligence_definition`

- proposition: 중과실은 주의의무 위반의 정도가 매우 크고, 행위자가 약간의 주의만 기울였더라도 결과발생을 방지할 수 있었던 경우를 말한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 주의의무 위반 정도와 약간의 주의로 결과회피가 가능했는지에 관한 구체적 사실평가가 필요하다.
- bounded sources:

  - `comm_001692_제268조_Ⅱ.1_103` / `Ⅱ.1`: “중과실은 주의의무 위반의 정도가 매우 큰 경우를 말한다. 행위자가 약간의 주 의만 기울였다면 결과발생을 방지할 수 있었던 경우 중과실이라고 볼 수 있다.”

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

## 55. `art268_sec2_1.gross_negligence_social_notion`

- proposition: 중과실과 경과실의 구별은 구체적 사건에서 사회통념에 따라 판단하며, 일반적 기준을 제시하기 어렵다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 중과실 여부는 기계적으로 확정할 수 없고 사건별 사회통념 평가가 필요하다.
- bounded sources:

  - `comm_001692_제268조_Ⅱ.1_103` / `Ⅱ.1`: “중과실인지 경과실인지 그 구별은 구체적인 사건에서 사회통념을 통하여 판단 하게 되고, 일반적 기준을 제시하는 것은 어렵다.”

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

## 56. `art268_sec2_1.high_risk_situation_gross_negligence`

- proposition: 통상 위험사무가 아닌 업무라도 구체적 상황에서 결과발생의 고도한 위험을 수반하는 행위를 하면서 행위자가 그 위험성을 인식하거나 쉽게 인식할 수 있으면, 결과발생 회피를 위하여 특별히 신중한 태도가 요구되고 이를 위반한 과실은 중과실이 될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 고도의 결과발생 위험, 위험 인식 또는 용이한 인식 가능성, 그리고 특별히 신중한 태도의 내용은 구체적 사실관계에 따라 평가해야 한다.
- bounded sources:

  - `comm_001692_제268조_Ⅱ.1_103` / `Ⅱ.1`: “그 업무 자체로는 위험사무라고 해석되지 않는 것이라도 구체적 상황 하 에 있어서는 결과발생의 고도의 위험성을 수반하는 행위를 함에 있어서는 행위 자가 그 위험성을 인식하고, 혹은 용이하게 인식할 수 있는 한 결과발생의 회피 를 위하여 특히 신중한 태도를 취할 것이 요구될 수 있고 이에 위반한 과실은 중대한 과실이라고 하여도 좋을 것이다.”

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

## 57. `art268_sec2_1.nonprofessional_dangerous_work_gross_negligence`

- proposition: 업무상 과실치사상죄의 위험사무에 속하는 유형의 행위를 비업무자가 한 경우, 비업무자가 업무자와 같은 수준의 주의를 하지 않거나 위험행위를 삼가지 않고 업무자에게 허용될 정도의 위험도 억제하지 않아 그 주의의무를 위반하면 그 과실은 중과실로 볼 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 행위가 위험사무 유형에 속하는지, 행위자가 비업무자인지 및 요구되는 위험억제 조치가 무엇인지에 대한 사실평가가 필요하다.
- bounded sources:

  - `comm_001692_제268조_Ⅱ.1_103` / `Ⅱ.1`: “업무상 과실치사상죄의 요건으로서의 위험사무에 속하는 유형의 행위를 비업무자가 한 경우 그 과실은 중과실이라고 볼 수 있다고 할 것이다.”
  - `comm_001692_제268조_Ⅱ.1_103` / `Ⅱ.1`: “비업무자로서는 업무자와 같은 수준의 주의를 하던지, 그렇지 못하면 그러한 위험한 행위를 삼 가거나, 업무자라면 감행하는 것을 허용할 정도의 위험에 대해서도 그 위험을 억제할 주의의무를 부담한다고 보아야 하고, 이를 어길 경우 중대한 과실이라고 인정함이 타당하다.”

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

## 58. `art268_sec2_2.candle_in_warehouse`

- proposition: 창고에 인화물질이 없고 촛불 주변에 헌 가마니와 쓰레기 등이 있을 뿐인 사정에서 촛불을 끄지 않고 창고문을 닫은 과실은 경과실에 불과하다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 인화물질 부재 및 촛불 주변 물건의 구체적 사정에 한정하여 경과실 판단을 검토한다.
- bounded sources:

  - `comm_001692_제268조_Ⅱ.2_106` / `Ⅱ.2`: “위 경우에 인정되는 피고인이 촛불을 들 고 나오든가 소화하고 나오지 아니한 과실은 어디까지나 경과실에 불과하다 할 것이다.”

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

## 59. `art268_sec2_2.cigarette_fire_inn`

- proposition: 인화하기 쉬운 침구와 휴지통 등이 있는 좁은 여관방에서 술에 취해 담뱃불을 제대로 끄지 않고 잠든 행위는 중대한 과실에 해당한다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 실내의 가연물, 공간적 근접성 및 담뱃불 소화 여부를 구체적으로 검토한다.
- bounded sources:

  - `comm_001692_제268조_Ⅱ.2_105` / `Ⅱ.2`: “인화하기 쉬운 침대 옆에 놓아 둔 휴지통과 침대시트커버와 솜이불 및 매 트리스 등이 있는 4평도 안되는 좁은 여관방안에서 술을 마시고 담배를 피우다가 술 에 취하여 담배불을 제대로 끄지 않고 침대에 누워 잠이 든 것은 중대한 과실이 있 는 경우에 해당한다.”

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

## 60. `art268_sec2_2.cigarette_fire_motel`

- proposition: 담뱃불이 완전히 꺼졌는지 확인하지 않고 불이 붙기 쉬운 휴지를 재떨이에 버린 후 잠들어 화재가 난 경우 그 과실은 중대한 과실에 해당한다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 점화원 소화 확인, 가연물의 성질 및 취침 전 위험방지 조치의 사정을 검토한다.
- bounded sources:

  - `comm_001692_제268조_Ⅱ.2_105` / `Ⅱ.2`: “담뱃불이 완전 히 꺼졌는지 여부를 확인하지 않은 채 불이 붙기 쉬운 휴지를 재떨이에 버리고 잠을 잔 과실로”
  - `comm_001692_제268조_Ⅱ.2_105` / `Ⅱ.2`: “이러한 피고인의 과실은 중대한 과실에 해당한다.”

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
