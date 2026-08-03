# 허위공문서작성 RuleIR 카드 검수 1

- unit: `false_public_document`
- articles: art227
- cards: 1–15 / 44
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #6 `art227_sec3_2.assistant_indirect_perpetration`: `art227_sec3_2.assistant_indirect_perpetration_affirmative` (status=`valid`)

## 1. `art227.actual_conformity_irrelevant`

- proposition: 정산설계서를 확인하거나 준공검사를 하지 않았음에도 한 것처럼 준공검사용지에 기입한 경우 범의가 명백하며, 준공검사조서 내용이 사후 정산설계서나 실제 준공 상태와 객관적으로 일치해도 본죄 성립에 영향이 없다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 준공검사조서 작성 사실관계에 한정된 commentary-reported precedent로서, 원문 판례 확인 전에는 일반화하지 않는다.
- bounded sources:

  - `comm_001692_제227조_Ⅴ_18` / `Ⅴ`: “준공검사조서를 작 성하면서 정산설계서를 확인하고 준공검사를 한 것이 아님에도 마치 한 것처럼 준공검사용지에 ‘정산설계서에 의하여 준공검사’를 하였다는 내용을 기입하였다 면 허위공문서작성의 범의가 있었음이 명백하여 그것만으로 곧 본죄가 성립하 고”
  - `comm_001692_제227조_Ⅴ_18` / `Ⅴ`: “위 준공검사조서의 내용이 객관적으로 정산설계서 초안이나 그 후에 작성된 정산설계서 원본의 내용과 일치한다거나 공사현장의 준공상태에 부합한다 하더 라도 그 성립에 아무런 영향을 미치지 못한다.”

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

## 2. `art227.authority_bearing_public_official`

- proposition: 본죄의 주체인 공무원에게는 해당 문서를 작성할 직무상 권한이 있어야 한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 작성 직무상 권한은 본죄 주체 판단의 기본 요소로 검토한다.
- bounded sources:

  - `comm_001692_제227조_Ⅲ.1_3` / `Ⅲ.1`: “본죄에서 공무원은 해당 문서를 작성할 직무상 권한이 있어야 한다.”

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

## 3. `art227.delegated_approval_authority`

- proposition: 공문서 명의인이 따로 있더라도 전결 처리되고 전결권자 부재 시 대리 전결하도록 위임된 사람은 본죄의 주체가 된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 전결 및 대리전결 위임의 존재와 범위를 문서별로 확인해야 한다.
- bounded sources:

  - `comm_001692_제227조_Ⅲ.1_3` / `Ⅲ.1`: “공문서의 명의인이 따로 있어도 전결 처리되고 전결권자의 부재 시 피고 인이 대리하여 전결하도록 위임되어 있는 경우에는 본죄의 주체가 된다.”

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

## 4. `art227.false_report_substantive_review_power`

- proposition: 공무원이 신고 기재내용을 조사할 권한이 있는 경우, 신고사실이 허위임을 알면서 기재하면 본죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 조사권한의 범위와 허위 인식은 구체적 업무규정 및 사실관계에 따라 검토한다.
- bounded sources:

  - `comm_001692_제227조_Ⅲ.1_4` / `Ⅲ.1`: “공무원이 신고된 기재내용에 대해서 조사할 권한이 있는 경우 공무원이 신고사실이 허위인 것을 알면서 기재하는 경”
  - `comm_001692_제227조_Ⅲ.1_4` / `Ⅲ.1`: “우에는 본죄가 성립한다.”

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

## 5. `art227.intent_and_purpose`

- proposition: 본죄에는 고의 외에 행사할 목적이 필요하며, 행사 목적은 허위 작성·변개 공문서를 진정하게 작성된 것처럼 사용할 목적을 말한다. 적극적 의욕이나 확정적 인식은 필요하지 않고 미필적 인식으로 충분하다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 행사 목적과 미필적 인식의 존재는 구체적 사정에 따른 평가가 필요하다.
- bounded sources:

  - `comm_001692_제227조_Ⅴ_18` / `Ⅴ`: “본죄는 고의 외에 행사할 목적이 있어야 한다. 행사할 목적은 허위 작성하거나 변개한 공문서를 진정하게 작성된 것처럼 사용할 목적을 말하고, 적극적 의욕이 나 확정적 인식을 요하지 않으며 미필적 인식이 있으면 충분하다”

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

## 6. `art227.intent_definition`

- proposition: 본죄의 고의는 공문서 내용이 허위라는 점, 직무에 관한 것이라는 점 및 문서 또는 도화를 허위로 작성·변개한다는 점에 대한 인식과 의사이다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 각 인식·의사 요소의 충족 여부는 개별 행위와 문서 내용에 비추어 평가한다.
- bounded sources:

  - `comm_001692_제227조_Ⅴ_18` / `Ⅴ`: “본죄의 고의는 작성 또는 변개한 공문서의 내용이 허위라는 점, 그 직무에 관한 것이라는 점, 문서 또는 도화를 허위로 작성 또는 변개한다는 점에 대한 인식과 의사이다.”

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

## 7. `art227.no_intent_clerical_or_customary_entry`

- proposition: 단순 오기, 부주의에 의한 기재 누락, 선례나 업무상 관행에 따른 기재 또는 보통 있을 수 있는 사소한 차이의 잘못된 기재는 허위 작성의 고의가 부인된다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 오기·관행·사소한 차이에 해당하는지는 문서 작성 경위와 업무 관행을 포함한 구체적 사정으로 평가한다.
- bounded sources:

  - `comm_001692_제227조_Ⅴ_18` / `Ⅴ`: “그러나 단순 오기나 부주의에 의한 기재 누락, 선례나 업무상 관행에 따른 기 재, 잘못된 기재가 보통 있을 수 있는 사소한 차이에 불과한 경우에는 허위 작성의 고의가 부인된다.”

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

## 8. `art227.no_writing_authority_exception`

- proposition: 작성권한 없는 공무원이 공문서를 허위로 작성한 경우에는 허위공문서작성죄에 해당하지 않고, 공문서위조죄 및 자격모용에 의한 공문서작성죄의 문제가 된다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 본죄의 작성권한 요소가 충족되지 않는 경우에 한정된 제외 규범이다.
- bounded sources:

  - `comm_001692_제227조_Ⅲ.1_3` / `Ⅲ.1`: “작성권한이 없는 공무원이 공문서를 허위로 작성하 였을 경우에는 본죄에 해당하지 않으며, 공문서위조죄 및 자격모용”

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

## 9. `art227.nonofficial_joint_principal`

- proposition: 공무원이 아닌 사람도 공무원과 공동하여 본죄를 범하면 형법 제33조 및 제30조에 따라 공동정범이 될 수 있다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 비공무자의 공동정범 성립은 공무원과의 공동 범행이라는 전제에서만 검토한다.
- bounded sources:

  - `comm_001692_제227조_Ⅲ.1_4` / `Ⅲ.1`: “공무원이 아닌 자가 공무원과 공동하여 허위공문서작성죄를 범한 때에는 공무원 이 아닌 자도 형법 제33조, 제30조에 의하여 허위공문서작성죄의 공동정범이 된다.”

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

## 10. `art227.nonpublic_status_exception`

- proposition: 국가 사무를 수행하거나 소속 기관의 행정기관성이 인정된다는 사정만으로는 본죄가 성립하지 않으며, 신분상 공무원이 아닌 사람을 처벌하려면 특별규정이 필요하다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 국가사무 수행이나 기관 성격만으로 공무원 신분을 대체하지 않는다는 제한이다.
- bounded sources:

  - `comm_001692_제227조_Ⅲ.1_3` / `Ⅲ.1`: “수행 업무가 국가의 사무에 해당한다거나 소속 기관의 행정기관성이 인정된다는 사정만으로 본죄가 성립하지 않는다. 즉 신 분상 공무원이 아님이 분명한 사람을 본죄로 처벌하려면 그에 관한 특별규정이 있 어야 한다.”

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

## 11. `art227.notary_false_certification`

- proposition: 사서증서 인증을 촉탁받은 공증인이 당사자의 면전 서명·날인 또는 본인 확인이 없었음에도 그러한 확인이 있었던 것처럼 인증서에 기재하면 허위공문서작성죄의 죄책을 면할 수 없다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 면전 서명·날인 또는 본인 확인의 부재와 인증서 기재 내용의 불일치를 확인해야 한다.
- bounded sources:

  - `comm_001692_제227조_Ⅲ.1_5` / `Ⅲ.1`: “당사자가 공증인의 면전에서 사서증서에 서명 또는 날인을 하거나 당사자 본인이나 그 대리인으로 하여금 사서증서의 서명 또는 날인이 본인의 것임을 확인하게 한 바가 없음에도, 당사자가 공증인의 면전에서 사서증서에 서명 또는 날인을 하거 나 본인이나 그 대리인이 사서증서의 서명 또는 날인이 본인의 것임을 확인한 것처럼 인증서에 기재하였다면, 허위공문서작성죄의 죄책을 면할 수 없다.”

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

## 12. `art227.omission_of_required_entry`

- proposition: 검사가 피의자신문조서에서 피의자의 자백사실을 고의로 누락하거나 출납담당 공무원이 수입사실을 출납부에 고의로 기재하지 않은 경우, 부작위에 의한 본죄가 성립할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 기재의무, 누락 사실 및 고의의 존재를 개별 기록과 담당업무에 따라 검토한다.
- bounded sources:

  - `comm_001692_제227조_Ⅲ.1_4` / `Ⅲ.1`: “검사가 피의자신문조서를 작 성하면서 피의자의 자백사실을 고의로 누락한 경우, 출납을 담당하는 공무원 이 수입사실을 고의적으로 출납부에 기재하지 않은 경우 부작위에 의한 본죄 가 성립할 수 있고”

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

## 13. `art227.recording_statement_as_stated_exception`

- proposition: 수사기록·공판기록 작성에서 진술자가 허위 진술한 사실을 알면서도 그 진술대로 조서에 기재한 것은 진술 그대로의 적법한 조서 작성이므로 본죄에 해당하지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 진술 내용을 그대로 기록하는 조서 작성의 경우에 한정된 예외다.
- bounded sources:

  - `comm_001692_제227조_Ⅲ.1_4` / `Ⅲ.1`: “수사기록·공판기록의 작성에서 진술자가 허위 진술한 것을 알면서도 사법경찰 관 또는 법원사무관 등이 조서에 그대로 기재한 것은 진술 그대로의 적법한 조 서 작성이므로 본죄에 해당하지 않는다.”

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

## 14. `art227.scope_of_official_duties`

- proposition: 구체적 행위가 공무원의 직무에 속하는지는 공무 수행의 일환인지와 해당 공무원이 수행할 직무와의 관계에서 합리적으로 필요한지를 함께 고려하여 판단한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 직무 해당성은 형식적 공무 연관성과 실질적 필요성에 대한 평가를 필요로 한다.
- bounded sources:

  - `comm_001692_제227조_Ⅲ.1_3` / `Ⅲ.1`: “그것이 공무의 일환으로 행 하여졌는가 하는 형식적 측면과 함께, 그 공무원이 수행해야 할 직무와의 관계 에서 합리적으로 필요하다고 인정될 수 있는가 하는 실질적 측면을 아울러 고 려하여 결정된다.”

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

## 15. `art227_sec1.offense_concept`

- proposition: 허위공문서작성등죄는 공무원이 그 직무에 관한 문서를 허위로 작성·변개하는 범죄이다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 공무원, 직무 관련 문서, 허위 작성·변개라는 범죄 개념을 기술하는 commentary synthesis이다.
- bounded sources:

  - `comm_001692_제227조_Ⅰ_0` / `Ⅰ`: “본죄는 행위자인 공무원이 그 직무에 관한 문서를 허위로 작성·변개하는 것을 말한다.”

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
