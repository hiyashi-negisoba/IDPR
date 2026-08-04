# 성범죄 미수 RuleIR 카드 검수 1

- unit: `sexual_offense_attempt`
- articles: art300
- cards: 1–5 / 5
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 1. `art300_x_raw_pdf.art305_under_sixteen_attempt_interpretation`

- proposition: 위 판례의 해석에 따르면 형법 제305조 제2항의 16세 미만 미성년자에 대한 간음·추행죄도 미수범이 처벌되는 것으로 해석할 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 이는 주석이 선행 판례로부터 제305조 제2항에 관해 제시한 해석 가능성으로서, 독립된 확인 완료 판례 규칙으로 취급하지 않는다.
- bounded sources:

  - `raw_001692_제300조_p002` / `raw_pdf.page_2`: “이에 따르면 16세 미만의 미성년자에 대한 간음·추행죄(형법 제305조 제2항)에 대하여도 미수범이 처벌되는 것으로 해석할 수 있다.”

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

## 2. `art300_x_raw_pdf.commencement_of_execution`

- proposition: 미수가 성립하려면 실행의 착수가 있어야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 실행의 착수 해당성은 구체적 행위의 위험성과 행위 진행을 평가해야 하므로 standard input으로 둔다.
- bounded sources:

  - `raw_001692_제300조_p002` / `raw_pdf.page_2`: “미수가 성립하기”
  - `raw_001692_제300조_p002` / `raw_pdf.page_2`: “위해서는  실행의 착수가  있어야 한다.”

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

## 3. `art300_x_raw_pdf.enumerated_offenses_attempts`

- proposition: 강간죄, 유사강간죄, 강제추행죄 및 준강간·준유사강간·준강제추행죄의 미수범은 처벌된다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 열거된 죄명과 미수범 처벌의 연결은 기계적으로 열거할 수 있으나, 인용문은 원문 주석 내 단편이므로 조문 원문 대조가 필요하다.
- bounded sources:

  - `raw_001692_제300조_p001` / `raw_pdf.page_1`: “강간죄(형법 제297조), 유사강간죄(제297조의2), 강제추행죄(제298조), 준강간·준유”
  - `raw_001692_제300조_p001` / `raw_pdf.page_1`: “사강간·준강제추행죄(제299조)의 미수범은”

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

## 4. `art300_x_raw_pdf.other_offenses_exclusion`

- proposition: 강간 등 상해·치상죄, 강간 등 살인·치사죄, 미성년자 등에 대한 간음죄 및 업무상 위력 등에 의한 간음죄의 미수범에는 형법 제300조가 적용되지 않는다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 제300조의 적용 대상 밖이라는 명시적 부정 범위이며, 열거된 죄에만 한정한다.
- bounded sources:

  - `raw_001692_제300조_p001` / `raw_pdf.page_1`: “위 죄 이외에  강간 등  상”
  - `raw_001692_제300조_p001` / `raw_pdf.page_1`: “해·치상죄(제301조), 강간 등 살인·치사죄(제301조의2), 미성년자 등에 대한 간음”
  - `raw_001692_제300조_p001` / `raw_pdf.page_1`: “죄(제302조), 업무상 위력 등에 의한 간음죄(제303조)의 미수범에 대하여는 형법”
  - `raw_001692_제300조_p001` / `raw_pdf.page_1`: “제300조가 적용되지 않는다.”

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

## 5. `art300_x_raw_pdf.pre_amendment_art305_under_thirteen_attempt`

- proposition: 판례는 구 형법 제305조의 13세 미만 미성년자에 대한 간음·추행죄에 형법 제300조를 적용하여 그 미수범 처벌을 긍정하였다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 주석이 보고한 판례 입장으로만 기록하였다. 적용된 판례 원문과 구 제305조의 적용 범위는 primary precedent index에서 확인해야 한다.
- bounded sources:

  - `raw_001692_제300조_p002` / `raw_pdf.page_2`: “판례는 13세 미만의 미성년자에”
  - `raw_001692_제300조_p002` / `raw_pdf.page_2`: “대한 간음·추행죄(2020. 5. 19. 법률”
  - `raw_001692_제300조_p002` / `raw_pdf.page_2`: “제17265호로 제305조 제2항이 신설되기 전 구 형법 제305조)에 대하여 이를 긍정하였”

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
