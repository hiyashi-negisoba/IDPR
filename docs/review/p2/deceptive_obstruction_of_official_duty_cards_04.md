# 위계공무집행방해 RuleIR 카드 검수 4

- unit: `deceptive_obstruction_of_official_duty`
- articles: art137
- cards: 46–50 / 50
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 46. `art137_sec6.certificate_preparation_joint_principal`

- proposition: 간호보조원 응시자격 증명서가 허위로 작성·교부된 뒤 다른 사람이 이를 시험관리 당국에 제출하여 응시자격을 인정받고 시험관리 공무집행 방해 상태가 초래된 경우, 작성·교부자는 본죄 공동정범 책임을 질 수 있다는 판례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 허위 문서 작성·교부자와 제출자의 공동정범 성립은 구체적 행위 분담 및 시험관리 공무집행 방해 상태를 검토해야 한다. 소개된 판례는 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제137조_Ⅵ_32` / `Ⅵ`: “그들이 위와 같은 문서를 진정한 문서인 것처럼 시험관리 당국에 제출하여 응시자격을 인정받아 응시함으로써 그 시험관리에 관한 공무집행을 방해하는 상태를 초래하였다면, 피고인들은 본죄의 공동정범의 죄책을 면할 수 없고”

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

## 47. `art137_sec6.false_report_absorption`

- proposition: 거짓신고가 위계의 수단·방법·태양이 되어 본죄가 성립한 경우, 거짓신고 경범죄는 본죄에 흡수되어 별도로 성립하지 않는다는 대법원 입장이 소개되어 있다.
- current metadata: formalization=`deterministic_rule`, polarity=`exception`, doctrinal_status=`precedent_position`, review_required=`False`
- source track: `unit_core`
- prior note: 거짓신고가 위계의 수단·방법·태양 중 하나가 된 경우에 한정된 법조경합 관계다. 소개된 대법원 입장은 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제137조_Ⅵ_32` / `Ⅵ`: “경범죄 처벌법 제3조 제3항 제2호의 거짓신고가 위계의 수단·방법·태양의 하나가 된 경우에는 거짓신고로 인한 경범죄 처벌법 위반죄가 위계에 의한 공무집행방해죄에 흡수되 는 법조경합 관계에 있으므로, 위계에 의한 공무집행방해죄만 성립할 뿐 이와 별 도로 거짓신고로 인한 경범죄 처벌법 위반죄가 성립하지는 아니한다고 보았다.”

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

## 48. `art137_sec6.false_report_response_obstruction`

- proposition: 거짓신고로 공무원이 범죄 발생을 오인하여 진실을 알았다면 하지 않았을 대응조치를 취하게 된 경우에는 구체적·현실적 공무집행 방해가 발생하여 본죄가 성립한다는 대법원 입장이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 거짓신고, 공무원의 오인, 반사실적으로 하지 않았을 대응조치 및 구체적·현실적 방해의 연결을 사실관계에 따라 검토해야 한다. 소개된 대법원 입장은 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제137조_Ⅵ_32` / `Ⅵ`: “거짓신고 행위가 원인이 되어 상대방인 공무원이 범죄가 발생한 것으로 오인함으로 인하여 공무원이 그러한 사정을 알았더라면 하지 않 았을 대응조치를 취하기에 이르렀다면, 이로써 구체적이고 현실적인 공무집행이 방해되어 위계에 의한 공무집행방해죄가 성립하지만”

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

## 49. `art137_sec6.non_suspect_impersonation_exception`

- proposition: 피의자나 참고인이 아닌 사람이 자발적·계획적으로 피의자를 가장하여 수사기관에 허위 진술한 경우에는 범인은닉죄가 성립할 수 있어도 본죄는 성립하지 않는다는 설명이 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 비피의자·비참고인의 자발적·계획적 가장과 허위진술 해당성은 사실관계 평가가 필요하다.
- bounded sources:

  - `comm_001692_제137조_Ⅵ_32` / `Ⅵ`: “피의자나 참고인이 아닌 자가 자발적이고 계획적으로 피의자를 가장하여 수사 기관에 허위사실을 진술한 경우 범인은닉죄는 성립할 수 있더라도 본죄는 성립 하지 아니한다.”

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

## 50. `art137_sec6.official_misconduct_absorption`

- proposition: 작위범인 본죄와 부작위범인 직무유기죄의 구성요건이 동시에 충족되면 본죄만 성립하고 직무유기죄는 성립하지 않는다는 설명이 있다.
- current metadata: formalization=`deterministic_rule`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 두 구성요건의 동시 충족을 전제로 한 죄수 관계 설명이다.
- bounded sources:

  - `comm_001692_제137조_Ⅵ_32` / `Ⅵ`: “작위범인 본죄의 구성요건과 부작위범인 직무유기죄의 구성요건이 동시에 충족 되는 경우에는 본죄만이 성립하고 직무유기죄는 성립하지 아니한다.”

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
