# 과실치사·업무상과실치사상 RuleIR 카드 검수 1

- unit: `negligent_bodily_harm`
- articles: art267, art268
- cards: 1–15 / 85
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #25 `art268.unlicensed_activity_work`: `art268.illicit_work_excluded` (status=`valid`)

## 1. `art267_sec1.negligent_homicide_definition`

- proposition: 과실로 사람을 사망하게 하면 과실치사죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 과실 및 사망 결과의 해당성 판단에는 사실관계 평가가 필요하다.
- bounded sources:

  - `comm_001692_제267조_Ⅰ_0` / `Ⅰ`: “본죄는 과실로 인하여 사람을 사망하게 함으로써 성립하는 범죄이다.”

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

## 2. `art267_sec1.no_intent_to_kill_injure_or_assault`

- proposition: 과실치사죄는 살해의 고의, 상해의 고의 또는 폭행의 고의가 없는 때에만 성립한다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 살해·상해·폭행의 고의 부재가 명시된 소극적 성립 조건이다.
- bounded sources:

  - `comm_001692_제267조_Ⅰ_0` / `Ⅰ`: “본죄는 살해의 고의는 물론 상해나 폭행의 고의도 없는 때에만 성립한다.”

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

## 3. `art267_sec2.causal_link.negligent_act_and_result`

- proposition: 과실치사죄의 성립에는 과실행위와 결과 사이의 인과관계가 충족되어야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 인과관계의 구체적 적용은 사실관계 평가를 필요로 하므로 별도 causal-link 카드로 유지한다.
- bounded sources:

  - `comm_001692_제267조_Ⅱ_1` / `Ⅱ`: “본죄의 성립을 위해서도 (형법 제266조) 주의의무위반의 과실행위, 구성요건적 결과의 발생, 과실행위와 결과 사이의 인 과관계가 충족되어야 한다.”

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

## 4. `art267_sec2.causal_link.prank_throwing_at_sea`

- proposition: 파도가 치고 미끄러운 바닷가 바위 위에서 병사를 헹가래쳐 바다에 빠뜨리려 한 행위와, 일행이 미끄러져 바다에 빠져 사망한 결과 사이에는 인과관계가 인정될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 특정 해안·헹가래 사안의 reported holding으로서, 일반적 인과관계 기준으로 확장하지 않고 원판결을 확인해야 한다.
- bounded sources:

  - `comm_001692_제267조_Ⅱ_2` / `Ⅱ`: “갑을 헹가래쳐서 바다에 빠뜨리려고 한 행위와 피해자가 바다에 빠져 사망한 결과와의 사이에는 인과 관계가 있다고 할 것이고”

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

## 5. `art267_sec2.definition.person_begins_regular_labor`

- proposition: 과실치사죄의 객체인 사람의 시기는 규칙적인 진통을 동반하여 분만이 개시된 때이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 사람의 시기 판단에 규칙적인 진통과 분만개시 사실의 검토가 필요하다.
- bounded sources:

  - `comm_001692_제267조_Ⅱ_1` / `Ⅱ`: “규칙적인 진통을 동반하면서 분만이 개시된 때(소위 진통설 또는 분만개시설)가 사람의 시기 라고 봄이 타당”

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

## 6. `art267_sec2.elements.negligent_breach_and_death`

- proposition: 과실치사죄의 성립에는 주의의무위반의 과실행위와 구성요건적 결과의 발생이 충족되어야 한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 과실치사죄 성립요건 중 과실행위와 결과발생을 열거한 commentary synthesis다.
- bounded sources:

  - `comm_001692_제267조_Ⅱ_1` / `Ⅱ`: “본죄의 성립을 위해서도 (형법 제266조) 주의의무위반의 과실행위, 구성요건적 결과의 발생, 과실행위와 결과 사이의 인 과관계가 충족되어야 한다.”

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

## 7. `art267_sec2.standard.bus_driver_instant_wheel_entry`

- proposition: 피해자가 버스 발차 순간 바퀴 밑으로 들어가 운전자가 발견하지 못한 경우에는 운전자의 과실을 인정할 수 없고, 피해자가 더 일찍 들어갔는지가 밝혀지지 않으면 과실 유무를 가릴 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 발차 전 피해자의 위치·진입 시점 및 운전자의 발견가능성에 관한 증거 평가가 필요하며, reported precedent의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제267조_Ⅱ_3` / `Ⅱ`: “피해자가 발차순”
  - `comm_001692_제267조_Ⅱ_3` / `Ⅱ`: “바퀴 밑으로 들어간 것이라면 운전사가 미처 이를 발견하지 못한 점에 과실이 있다고는 할 수 없을 것이어서, 피해자가 발차순간 바퀴 밑으로 들어간 것인지 아니 면 좀더 일찍 들어간 것인지가 밝혀지지 않는 한 운전사의 과실유무를 가려낼 수 없 다고 할 것이다.”

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

## 8. `art267_sec2.standard.fetus_before_regular_labor_not_person`

- proposition: 분만의 개시라고 할 규칙적인 진통이 시작되지 않은 태아는 업무상과실치사죄의 객체인 사람으로 볼 수 없어, 해당 공소사실에 관하여 무죄가 선고될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: commentary가 보고한 무죄 판단이며, 적용 전 원판결 및 사실관계 확인이 필요하다.
- bounded sources:

  - `comm_001692_제267조_Ⅱ_1` / `Ⅱ`: “분만의 개시라고 할 수 있는 규칙적인 진통 이 시작된 바 없었으므로 이 사건 태아는 아직 업무상과실치사죄의 객체인 ‘사람’이 되었다고 볼 수 없다는 이유 등으로 이 부분 공소사실에 관하여 무죄를 선고한 것은 정당”

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

## 9. `art267_sec2.standard.landlord_failure_gas_warning`

- proposition: 대수선 필요성이 불분명한 가옥에서 임대인이 임차인의 연탄가스 냄새 및 수선 요구를 받고도 원인 조사와 대책 마련을 하지 않은 경우, 가스중독 사망사고는 임대인의 과실로 발생한 것으로 볼 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 임차인의 요구 내용, 임대인의 인식, 조사·대책 미이행 및 사고 사이의 관계를 사실별로 검토해야 하며, reported precedent의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제267조_Ⅱ_2` / `Ⅱ`: “피고인이 임차인으로부터 이러한 요구”
  - `comm_001692_제267조_Ⅱ_2` / `Ⅱ`: “를 받고도 연탄가스 냄새가 나는 원인을 조사하고 그에 대한 대책을 강구”
  - `comm_001692_제267조_Ⅱ_2` / `Ⅱ`: “하는 등의 조처를 취하지 아니한 점에 비추어 보면 이 사건 사고는 임대인인 피고인 의 과실로 인하여 발생하였다고 봄이 상당”

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

## 10. `art267_sec2.standard.landlord_negligence_assessment_factors`

- proposition: 임대인의 과실 유무는 하자 자체의 상태뿐 아니라 목적물의 구조와 전반적 노후화 상태를 함께 참작하여 대규모 수선 필요성을 판단하여야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 목적물 상태와 대규모 수선 필요성에 대한 종합적 평가가 필요하며, reported precedent의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제267조_Ⅱ_2` / `Ⅱ`: “이러한 판단을 함에 있어서 단순히 하자 자체의 상태만을 고려할 것이 아니라 그 목 적물의 구조 및 전반적인 노후화 상태 등을 아울러 참작하여 과연 대규모적인 방법 에 의한 수선이 요구되는지를 판단하여야 할 것이며”

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

## 11. `art267_sec2.standard.landlord_no_negligence_minor_defect`

- proposition: 임대차 목적물의 하자가 임차인의 통상적인 수선·관리의무 범위에 속하면, 그 하자로 가스중독사가 발생하더라도 임대인에게 과실이 있다고 할 수 없다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 하자가 임차인의 통상 수선·관리의무 범위인지에 관한 평가가 필요하며, commentary-reported precedent의 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제267조_Ⅱ_2` / `Ⅱ`: “임차인의 통상의 수선 및 관리의무에 속한다고 보여지는 경우에는 그 하자로 인 하여 가스중독사가 발생하였다고 하더라도 임대인에게 과실이 있다고 할 수 없으나”

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

## 12. `art267_sec2.standard.prank_throwing_foreseeability`

- proposition: 폭풍주의보 아래 미끄러운 바닷가 바위 위에서 헹가래로 사람을 바다에 빠뜨리려 한 경우 결과발생의 예견가능성이 인정되어, 참가자는 사망에 관한 과실책임을 면할 수 없다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 예견가능성은 폭풍주의보와 미끄러운 바위 등 구체적 상황에 의존하므로 fact-sensitive assessment가 필요하다.
- bounded sources:

  - `comm_001692_제267조_Ⅱ_2` / `Ⅱ`: “위와 같은 경우 결과발생에 관한 예견가능성도 있다고 할 것이므로 갑을 붙들고 헹가래치려고 한 피고인들로서는 비록 피해자가 위와 같이 헹가래치려고 한 일행 중의 한 사람이었다고 하여도 동인의 사망에 대하여 과실책임 을 면할 수 없다.”

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

## 13. `art267_sec4.death_and_injury_single_negligent_act`

- proposition: 하나의 과실행위로 한 사람을 사망하게 하고 다른 사람을 상해하게 하면 과실치사죄와 과실치상죄의 상상적 경합이 된다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 하나의 과실행위로 사망 결과와 별인의 상해 결과가 함께 발생한 경우의 죄수 관계에 관한 서술이다.
- bounded sources:

  - `comm_001692_제267조_Ⅳ_5` / `Ⅳ`: “1개의 과실행위로 한 사람은 사망에 이르게 하고, 다른 사람은 상해에 이르게 한 경우에는 과실치사죄와 과실치상죄의 상상적 경합이 된다.”

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

## 14. `art267_sec4.multiple_deaths_single_negligent_act`

- proposition: 하나의 과실행위로 여러 사람을 사망하게 하면 수개의 과실치사죄의 상상적 경합이 된다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 하나의 과실행위와 복수 사망 결과가 제시된 경우의 죄수 관계에 관한 서술이다.
- bounded sources:

  - `comm_001692_제267조_Ⅳ_5` / `Ⅳ`: “1 개의 과실행위로 수인을 사망에 이르게 하면 수개의 과실치사죄의 상상적 경합 이 된다.”

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

## 15. `art268.adequate_causation`

- proposition: 업무상 주의의무 위반 과실행위와 발생한 사망 또는 상해 결과 사이에 상당인과관계 또는 객관적 귀속관계가 인정되어야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 구체적 결과회피 가능성과 대체 원인 여부를 개별 사안에서 검토한다.
- bounded sources:

  - `comm_001692_제268조_Ⅰ.2_102` / `Ⅰ.2`: “업무상 주의의무 위반의 과실행위가 있더라도 그 행위와 발생한 사망이나 상해의 결과 사이에 상당인과관계 내지 객관적 귀속관계가 인정되어야 한다.”

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
