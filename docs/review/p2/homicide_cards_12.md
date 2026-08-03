# 살인·존속살해 RuleIR 카드 검수 12

- unit: `homicide`
- articles: art250, art254, art255
- cards: 166–180 / 242
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #7 `art250_sec1_10.officer_omission_murder`: all_demoted (status=`valid`)
- #8 `art250_sec1_11.indirect_perpetration_attempt`: `art250_sec1_11.indirect_perpetration_attempt_use_act` (status=`valid`)
- #9 `art250_sec1_17.direct_active_euthanasia_legality`: `art250_sec1_17.direct_active_euthanasia_negative` (status=`valid`)
- #10 `art250_sec1_19.excessive_execution_death`: `art250_sec1_19.excessive_execution_death_precedent` (status=`valid`)
- #11 `art250_sec1_21.death_penalty_threshold`: `art250_sec1_21.death_penalty_special_circumstances_majority` (status=`valid`)
- #12 `art250_sec1_3.birth_onset`: `art250_sec1_3.birth_labor_theory` (status=`valid`)
- #13 `art250_sec1_3.death_onset`: `art250_sec1_3.pulse_cessation_organ_removal` (status=`valid`)
- #14 `art250_sec1_3.organ_transplant_law_effect`: `art250_sec1_3.organ_transplant_law_limited_effect` (status=`valid`)
- #15 `art250_sec2_10.arson_death_parricide_concurrence`: `art250_sec2_10.arson_death_parricide_imaginary_concurrence` (status=`valid`)
- #16 `art250_sec2_6.adoptee_biological_parent_offense`: `art250_sec2_6.adoption_type_determines_offense` (status=`valid`)
- #17 `art250_sec2_6.deceased_spouse_lineal_ascendant_offense`: `art250_sec2_6.deceased_spouse_lineal_ascendant_ordinary_murder` (status=`valid`)
- #18 `art250_sec2_9.nonstatus_accomplice_liability`: `art250_sec2_9.nonstatus_accomplice_parricide_coprincipal_punished_ordinary` (status=`valid`)
- #19 `art250_sec2_9.status_instigator_nonstatus_principal`: `art250_sec2_9.status_instigator_parricide_accomplice` (status=`valid`)
- #20 `art255_sec4.preparation_desistance`: `art255_sec4.preparation_desistance_doctrinal_variants` (status=`valid`)

## 166. `art250_sec1_22.specific_violent_recidivism_enhancement`

- proposition: 특정강력범죄로 형을 선고받고 집행 종료 또는 면제 후 3년 이내 다시 특정강력범죄를 범하면 그 죄의 법정형 장기와 단기를 2배까지 가중한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 재범 전력, 집행 종료 또는 면제, 3년 기간 및 재범 특정강력범죄의 열거 가능한 관계를 기록한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.22_127` / `Ⅰ.22`: “특정강력범죄로 형을 선고받고 그 집행이 끝나거나 면제된 후 3년 이내에 다시 특정강력범죄를 범한 경우에는 그 죄에 대하여 정하여진 형의 장 기 및 단기의 2배까지 가중한다.”

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

## 167. `art250_sec1_22.specific_violent_suspect_identity_disclosure`

- proposition: 특정강력범죄사건 피의자의 신상정보는 범행수단의 잔인성과 중대한 피해, 충분한 범죄혐의 증거, 공공의 이익을 위한 필요성 및 피의자의 비청소년 해당성의 네 요건을 모두 갖추면 공개할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 요건의 충족 여부, 특히 잔인성·중대한 피해, 충분한 증거 및 공공의 이익 필요성은 개별 사안의 평가를 요구한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.22_128` / `Ⅰ.22`: “ⅰ) 범행수단이 잔인하고 중대한 피해가”
  - `comm_001692_제250조_Ⅰ.22_128` / `Ⅰ.22`: “발생한 특정강력범죄사건일 것, ⅱ) 피의자가 그 죄를 범하였다고 믿을 만한 충 분한 증거가 있을 것, ⅲ) 국민의 알권리 보장, 피의자의 재범방지 및 범죄예방 등 오로지 공공의 이익을 위하여 필요할 것, ⅳ) 피의자가 청소년 보호법 제2조 제1호의 청소년에 해당하지 아니할 것 등 4가지의 요건을 모두 갖춘”

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

## 168. `art250_sec1_3.birth_precedent_regular_labor`

- proposition: 대법원은 분만 중 태아가 질식사한 사안에서 형법상 사람의 시기를 규칙적 진통을 동반하여 태아가 태반으로부터 이탈하기 시작한 분만개시 때로 보았다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소개된 대법원 판시를 보존하며, 원문 판례 검증 전에는 commentary-reported precedent로 취급한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.3_4` / `Ⅰ.3`: ““사람의 생명과 신체의 안전을 보호법익으로 하고 있는 형법상 의 해석으로서는 사람의 시기는 규칙적인 진통을 동반하면서 태아가 태반으로부터 이탈하기 시작한 때 다시 말하여 분만이 개시된 때”라”
  - `comm_001692_제250조_Ⅰ.3_4` / `Ⅰ.3`: “고 판시함으로써, 진통설의 입장을 취하였다.”

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

## 169. `art250_sec1_3.cesarean_no_labor_precedent`

- proposition: 산모에게 분만개시로 볼 규칙적 진통이 시작되지 않은 제왕절개 관련 사안에서는 태아가 업무상과실치사죄의 사람에 해당하지 않는다는 이유로 무죄를 선고한 원심 판단을 대법원이 지지하였다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 자궁절개 다수설과 긴장관계에 있는 소개된 판례 입장으로서 원문 검증이 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.3_5` / `Ⅰ.3`: “산모에게 분만의 개시라고 할 수 있는 규칙적 진통이 시작된 바 없었으므로 태아가 아직 업무상과실치사죄의 ‘사 람’이 되었다고 볼 수 없다는 이유 등으로 무죄를 선고한 원심 판단을 지지하였 다.”

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

## 170. `art250_sec1_3.death_legal_determination`

- proposition: 사람의 종기는 의학적으로만 결정하지 않고 생명보호에 관한 입법취지 등을 종합하여 판단하여야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 사람의 종기 판단에 요구되는 종합적 법적 평가를 정리한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.3_7` / `Ⅰ.3`: “종기 역시 법적 문제이므로, 의학적으로만 결정할 것이 아니라 생명보호에 대한 입법취지 등을 종합적으로 고려해 판단하여야 한다.”

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

## 171. `art250_sec1_3.fetus_life_at_labor_onset`

- proposition: 분만이 시작될 때 태아는 살인죄 행위객체로서 생명을 가지고 있어야 한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 분만개시 시점에 생명이 존재하여야 한다는 객체 요건이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.3_7` / `Ⅰ.3`: “분만이 시작될 때 태아가 행위객체로서 생명을 가지고 있어야 한다는 점 (진통) 은 당연하다.”

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

## 172. `art250_sec1_3.homicide_object`

- proposition: 살인죄의 행위객체인 사람은 살아 있는 자연인이고, 살아 있는 이상 생존능력 유무는 묻지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 살인죄 객체의 기본적 인적 범위를 정리한 카드다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.3_3` / `Ⅰ.3`: “살인죄의 행위 객체는 사람이다. 사람이란 살아 있는 자연인을 말한다. 살아 있 는 사람인 이상 생존능력의 유무는 묻지 않는다.”

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

## 173. `art250_sec1_3.no_postbirth_survival_capacity`

- proposition: 분만이 시작된 태아가 행위객체가 되기 위하여 출생과정 이후에도 생명을 계속 유지할 능력을 가질 필요는 없다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 출생 후 계속 생존능력이 객체성의 추가 요건이 아니라는 명시적 예외다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.3_7` / `Ⅰ.3`: “출생과정을 거친 이후에도 계속 생명을 유지할 수 있는 능 력을 가지고 있어야 하는 것은 아니다.”

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

## 174. `art250_sec1_3.premature_infant_intent_precedent`

- proposition: 낙태시술 후 살아서 출생한 미숙아에게 상태 확인이나 최소한의 의료행위 없이 적극적으로 염화칼륨을 주입하여 사망하게 한 경우, 정상 생존 확률이 낮더라도 미숙아 살해의 범의를 인정할 수 있다는 대법원 판단이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 고의 인정은 구체적 행위와 의료적 조치의 부재에 대한 평가를 필요로 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.3_5` / `Ⅰ.3`: “살아서 출생한 미숙아가 정상적으로 생존할 확률이 적다고 하더라 도, 그 상태에 대한 확인이나 최소한의 의료행위도 없이 적극적으로 염화칼륨을 주 입하여 미숙아를 사망에 이르게 하였다면, 피고인에게 미숙아를 살해하려는 범의가 인정된다고 한 원심의 판단을 수긍하였다.”

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

## 175. `art250_sec1_3.suicide_exception`

- proposition: 살인죄의 객체인 사람은 타인을 뜻하므로 자기 자신은 이에 해당하지 않고 자살은 살인죄에 해당하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 자살이 살인죄의 객체 요건을 충족하지 않는다는 명시적 부정 규범이다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.3_3` / `Ⅰ.3`: “살인죄의 객체인 사람은 타인을 뜻하므로, 자기 자신은 여기의 ‘사람’이라고 할 수 없다. 그러므로 자살은 살인죄에 해당하지 않는다.”

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

## 176. `art250_sec1_4.killing_definition`

- proposition: 살해는 고의로 사람의 생명을 자연적인 사기에 앞서 단절시키는 것을 말한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 살해의 설명적 정의이며, 사람의 종기 판단기준 자체는 이 카드의 범위에 포함되지 않는다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.4_10` / `Ⅰ.4`: “살해란 고의로 사람의 생명을 자연 적인 사기에 앞서서 단절시키는 것을 말한다.”

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

## 177. `art250_sec1_4.methods_of_killing`

- proposition: 살해의 수단·방법에는 제한이 없고 유형적 방법이나 정신적 고통·충격을 주는 무형적 방법인지 여부를 묻지 않는다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 무형적 방법이 구체적 사안에서 살해행위에 해당하는지의 적용에는 평가가 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.4_10` / `Ⅰ.4`: “살해의 수단·방법에는 제한이 없다. 타살·사살·교살·독살·자살·참살·익살·”
  - `comm_001692_제250조_Ⅰ.4_10` / `Ⅰ.4`: “추락사 등과 같은 유형적 방법에 의하건, 정신적 고통이나 충격을 주는 무형적 방법에 의하건 묻지 않는다.”

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

## 178. `art250_sec1_5.circumstantial_murder_conviction`

- proposition: 살인죄와 같이 법정형이 무거운 범죄도 직접증거 없이 간접증거만으로 유죄를 인정할 수 있으나, 공소사실과 관련성이 깊은 간접증거들에 의한 신중한 판단이 요구된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 간접증거만에 의한 유죄 인정의 가능성과 신중한 판단 요구를 함께 확인한 commentary-reported precedent이다. 원판례 확인이 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.5_12` / `Ⅰ.5`: “살인죄 등과 같이 법정형이 무거운 범죄의 경우에 도 직접증거 없이 간접증거 만에 의하여 유죄를 인정할 수 있으나, 그러한 유죄 인정에 있어서는 공소사실에 대한 관련성이 깊은 간접증거들에 의하여 신중한 판단이 요구된다.”

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

## 179. `art250_sec1_7.pesticide_cider_circumstantial_proof`

- proposition: 피고인에게 살해 동기가 있고, 범행 시각 무렵 농약 혼입 정황, 피해자들의 음용 상황, 농약 검출된 용기와 피고인 집에서 발견된 용기의 연결 정황 등이 종합되는 농약 사이다 사건에서는 살인죄를 인정한 원심 판단이 수긍되었다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 보고된 사건의 복수 간접사실을 종합한 원심 수긍 판단이며, 다른 사건에 적용하려면 각 정황의 존재와 종합적 증명력을 평가해야 한다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.7_20` / `Ⅰ.7`: “대법원은 다음과 같은 여러 사정 등을 종합하여, 살인죄를 인정한 원심 판단을 수긍하였다.”
  - `comm_001692_제250조_Ⅰ.7_20` / `Ⅰ.7`: “피고인에게 피해자를 살해하려고 할 만한 동기가 있었던 것으로 보인다.”
  - `comm_001692_제250조_Ⅰ.7_20` / `Ⅰ.7`: “피고인 이외의 제”
  - `comm_001692_제250조_Ⅰ.7_20` / `Ⅰ.7`: “3자가 이 사건 박카스 병을 피고인의 집 풀숲에 버렸을 가능성은 거의 없다.”

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

## 180. `art250_sec1_7.poisoning_alternative_source`

- proposition: 피해자들이 섭취한 건강음료에 청산가리가 들어 있었을 가능성을 완전히 배제할 수 없는 경우, 피로회복제로 위장한 청산가리 캡슐에 의한 살해라는 공소사실의 증명은 제한된다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 건강음료의 청산가리 혼입 가능성이 배제되는지와 해당 대체 가능성이 공소사실 증명에 미치는 영향의 평가가 필요하다.
- bounded sources:

  - `comm_001692_제250조_Ⅰ.7_19` / `Ⅰ.7`: “그렇다면 위 건강음료에 청산”
  - `comm_001692_제250조_Ⅰ.7_19` / `Ⅰ.7`: “가리가 들어 있을 가능성도 완전히 배제할 수 없다.”

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
