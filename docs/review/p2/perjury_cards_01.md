# 위증·모해위증 RuleIR 카드 검수 1

- unit: `perjury`
- articles: art152
- cards: 1–15 / 36
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #1 `art152_sec1_6.perjury_evidence_destruction_relation`: `art152_sec1_6.perjury_evidence_destruction_special_relation` (status=`valid`)

## 1. `art152_sec1_1.instigation_or_aiding`

- proposition: 위증죄에는 교사범 또는 종범이 성립할 수 있다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 교사범 또는 종범의 성립 가능성에 한정된 관계이며, 공동정범·간접정범에 관한 대립과는 별개다.
- bounded sources:

  - `comm_001692_제152조_Ⅰ.1_0` / `Ⅰ.1`: “위증죄의 경우에 도 교사범 또는 종범은 당연히 성립할 수 있다.”

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

## 2. `art152_sec1_2.falsehood_assessment`

- proposition: 증언의 허위성은 단편적 구절이 아니라 신문절차의 증언 전체와 전후 문맥, 신문 취지 및 진술 경위를 종합하여 판단한다. 지엽적 사항의 허위진술도 위증죄가 성립할 수 있으나, 전체 취지가 기억에 일치하고 일부 사소한 차이가 신문취지 오해 또는 착오에 의한 경우에는 위증이 아니다. 증거능력, 사후 소 취하 또는 절차 무효는 원칙적으로 위증죄 성립에 영향을 주지 않는다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 추상적 위험범 성격과 사소한 불일치 예외의 경계를 사례별로 검토해야 한다.
- bounded sources:

  - `comm_001692_제152조_Ⅰ.2_22` / `Ⅰ.2`: “증인의 증언이 허위인지를 판단함에 있어서는 그 증언의 단편적인 구절에 구애 될 것이 아니라 당해 신문절차에 있어서의 증언 전체를 일체로 파악하여 판단 하여야 한다.”
  - `comm_001692_제152조_Ⅰ.2_16` / `Ⅰ.2`: “증인의 진술 내용이 당해 사건의 증명을 필요로 하는 사실에 관한 것인지 (2) 여부나 재판의 결과에 실제로 영향을 미쳤는지 여부는 위증죄 성립과 아무런 관계가 없다. 또 증언의 내용이 기본적인 사항에 관한 것이 아니고 지엽적인 사항에 관한 것이라고 하더라도 그것이 허위 진술인 이상 위증죄가 성립할 수 있다.”

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

## 3. `art152_sec1_2.intent`

- proposition: 주관설에 따르면 위증죄의 고의는 자신이 법률에 의하여 선서한 증인이라는 점과 진술이 자신의 기억에 반한다는 점에 대한 인식과 의사로 충분하고, 미필적 고의도 충분하다. 기억에 반한다는 인식 없이 증언했거나 신문 취지를 오해 또는 착각한 경우 고의는 인정되지 않으며, 허위진술의 동기나 목적은 주관적 구성요건 판단에서 문제되지 않는다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 허위성 이론의 최종 선택에 따라 고의의 대상과 사실인정 방법을 재검토해야 한다.
- bounded sources:

  - `comm_001692_제152조_Ⅰ.2_23` / `Ⅰ.2`: “위증죄의 고의는, ⅰ) 자신이 법률에 의하여 선서한 증인이라는 점과 ⅱ) 진 술 내용이 허위라는 점에 대한 인식과 의사이다.”
  - `comm_001692_제152조_Ⅰ.2_23` / `Ⅰ.2`: “증인이 무엇인가 착오에 빠져 자신의 기억에 반한다는 인식 없이 증언한 경 우나 증언 당시 신문의 취지를 오해 또는 착각하고 진술한 경우에는 위증죄 의 고의를 인정할 수 없다.”

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

## 4. `art152_sec1_2.lawful_oath_witness`

- proposition: 위증죄의 주체는 법률에 의하여 선서한 증인이며, 증인이라도 선서하지 않은 경우 위증죄의 주체가 될 수 없다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 법률에 의한 선서와 증인 지위는 위증죄 주체 판단의 독립 요건이다.
- bounded sources:

  - `comm_001692_제152조_Ⅰ.2_1` / `Ⅰ.2`: “위증죄의 주체는 ‘법률에 의하여 선서한 증인’이다. 증인이라도 선서를 하지 않 은 경우에는 이유 여하를 불문하고 위증죄의 주체가 될 수 없다.”

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

## 5. `art152_sec1_2.malicious_perjury`

- proposition: 형사사건 또는 징계사건에서 피고인·피의자 또는 징계혐의자를 모해할 목적으로 허위 진술한 경우에는 일반 위증죄가 아니라 모해위증죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`settled`, review_required=`True`
- source track: `unit_core`
- prior note: 제152조 제2항의 모해 목적 요건 및 일반 위증죄와의 관계는 별도 검토가 필요하다.
- bounded sources:

  - `comm_001692_제152조_Ⅰ.2_23` / `Ⅰ.2`: “증인이 형사사건 또는 징계사건에 관하여 피고인 이나 피의자 또는 징계혐의자를 모해할 목적으로 허위의 진술을 한 때에는 형 법 제152조 제1항에 규정된 위증죄가 아니라 같은 조 제2항에 규정된 모해위증 죄가 성립한다.”

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

## 6. `art152_sec1_2.nonstatutory_or_unauthorized_oath`

- proposition: 선서가 법률상 근거 없이 이루어졌거나 증인에게 선서시킬 권한이 없는 기관에 대하여 이루어진 경우, 그 선서는 위증죄 성립요건인 법률에 의한 선서에 해당하지 않아 위증죄가 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 심문절차 사건과 선서권한 없는 기관에 관한 보고된 판시를 원전 판례 색인으로 확인해야 한다.
- bounded sources:

  - `comm_001692_제152조_Ⅰ.2_1` / `Ⅰ.2`: “증인이 선서를 하였다고 하더라도, 그 선서가 법률에 근거하지 않은 때에는 (3) 위증죄가 성립하지 않는다.”
  - `comm_001692_제152조_Ⅰ.2_2` / `Ⅰ.2`: “검사나 사법경찰관과 같이 증인으로 하여금 선서하도록 할 권한이 없는 기관에 대하여 선서가 이루어졌다면 그 선서는 위증죄가 성립 하기 위한 ‘법률에 의한 선서’에 해당하지 않는다.”

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

## 7. `art152_sec1_2.oath_capacity`

- proposition: 선서무능력자가 선서하고 허위진술한 경우 그 선서는 무효이므로 위증죄가 성립하지 않는다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 선서무능력 판단의 절차법상 요건과 보고된 판례의 원문을 확인해야 한다.
- bounded sources:

  - `comm_001692_제152조_Ⅰ.2_3` / `Ⅰ.2`: “국내 학설은 위증죄의 성립 을 부정하는 데 견해가 일치한다. 판례 역시 선서무능력자의 선서는 무효라고 보고 있으므로, 같은 입장으로 이해된다.”

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

## 8. `art152_sec1_2.oath_lawful_procedure`

- proposition: 위증죄 성립을 위한 증인의 선서는 법률에 근거하고 법률이 정한 절차에 따라 적법하게 이루어져야 하며, 그 법률에는 법률의 위임에 따라 제정된 명령 등 하위법령이 포함될 수 있다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 선서 근거의 법규범 범위와 선서 절차 적법성은 함께 확인한다.
- bounded sources:

  - `comm_001692_제152조_Ⅰ.2_1` / `Ⅰ.2`: “위증죄가 성립하기 위한 증인의 선서는 법률에 근거하여 법률이 정한 절차에 따라 적법하게 이루어져야 한다.”
  - `comm_001692_제152조_Ⅰ.2_1` / `Ⅰ.2`: “선서의 근거가 되는 ‘법률’은 국회의 의결을 거쳐 제정되는 형식적 의미의 법 (1) 률만을 의미하는 것은 아니고, 법률의 위임에 따라 제정된 명령 등 하위법령도 포함될 수 있다.”

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

## 9. `art152_sec1_2.oath_procedural_defects`

- proposition: 증인에게 선서를 시킬 일반적 권한이 있는 기관에 대한 선서는 관할 위반이나 공소제기 절차 위반만으로 효력이 부정되지 않지만, 법정 증인보호규정 미준수로 증인보호에 사실상 장애가 초래된 경우에는 법률에 의하여 선서한 증인에 해당하지 않는 것이 원칙이다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 증인보호에 사실상 장애가 없었던 예외의 판단요소와 적용 범위를 검토해야 한다.
- bounded sources:

  - `comm_001692_제152조_Ⅰ.2_2` / `Ⅰ.2`: “증인에게 선서를 시 킬 일반적 권한이 있는 기관에 대하여 선서가 이루어진 경우에는, 설령 관할 위 반, 공소제기 절차의 법률 규정 위반 등의 흠이 있다고 하더라도 그 선서의 효 력 자체가 부정된다고 볼 수 없다.”
  - `comm_001692_제152조_Ⅰ.2_2` / `Ⅰ.2`: “증인신문절차에서 법률에 규정 된 증인 보호를 위한 규정이 지켜진 것으로 인정되지 않은 경우에는 증인이 허 위의 진술을 하였다고 하더라도 위증죄의 구성요건인 ‘법률에 의하여 선서한 증 인’에 해당하지 아니한다고 보아 이를 위증죄로 처벌할 수 없는 것이 원칙이다.”

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

## 10. `art152_sec1_2.oath_refusal_right_notice`

- proposition: 민사소송법이 적용 또는 준용되는 재판에서 증인이 선서거부권 또는 증언거부권을 고지받지 않았더라도 선서능력이 있으면 선서는 유효하며, 선서 후 허위진술에 위증죄가 성립할 수 있다. 형사소송법이 적용 또는 준용되는 재판에서 선서 효력 판단에는 선서거부권 고지 여부가 문제되지 않는다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 민사절차, 형사절차 및 국회 증언의 고지의무와 위증 성립요건을 구별하여 검토해야 한다.
- bounded sources:

  - `comm_001692_제152조_Ⅰ.2_4` / `Ⅰ.2`: “민사 소송법 제324조가 적용 또는 준용되는 재판에서 증인이 선서거부권을 고지 받 지 않은 채 선서를 하였다고 하더라도 선서능력을 갖춘 이상 그 선서는 유효하 고, 만약 선서 후 허위진술을 하였다면 위증죄가 성립할 수 있다고 봄이 옳다.”
  - `comm_001692_제152조_Ⅰ.2_11` / `Ⅰ.2`: “민사소송법이 적용 또는 준용되는 재판에서 증인이 증언거부권 을 고지 받지 않았다고 하더라도 선서 후 허위진술을 하였다면 특별한 사정이 없는 한 위증죄가 성립한다고 보아야 한다.”

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

## 11. `art152_sec1_2.refusal_right_and_perjury`

- proposition: 선서거부권자가 선서거부권을 행사하여 선서하지 않은 채 허위진술한 경우 위증죄는 성립하지 않지만, 증언거부권자가 권리 행사를 포기하고 증언하면서 허위진술한 경우 위증죄가 성립할 수 있다. 증언거부권 미고지로 권리 행사에 사실상 장애가 초래된 경우에는 위증죄 성립을 부정하며, 장애 여부는 증언 당시 상황, 거부사유, 권리 인지 여부, 고지되었어도 허위진술했을 정황 및 진정한 의사를 종합하여 판단한다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 자기부죄 우려와 친족 등 타인 처벌 우려의 구별, 기대가능성설 및 사실상 장애 판단기준을 검토해야 한다.
- bounded sources:

  - `comm_001692_제152조_Ⅰ.2_15` / `Ⅰ.2`: “증언거부권이 있는 증인이 증언거부권을 고지받지 못하였고, 이로 말미암아 증언거부권을 행사하는 데 사 실상 장애가 초래되었다고 볼 수 있다면 위증죄가 성립하지 않는다.”
  - `comm_001692_제152조_Ⅰ.2_5` / `Ⅰ.2`: “당해 사건에서 증언 당시 증인이 처한 구체적인 상황, 증언거부 사유의 내용, 증인이 증언거부사유 또는 증언거부권의 존재를 이미 알고 있었는 지 여부, 증언거부권을 고지받았더라도 허위진술을 하였을 것이라고 볼 만한 정 황이 있는지 등을 전체적·종합적으로 고려하여 증인이 침묵하지 아니하고 진술 한 것이 자신의 진정한 의사에 의한 것인지 여부를 기준으로 위증죄의 성립 여 부를 판단하여야 한다.”

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

## 12. `art152_sec1_2.statement_scope`

- proposition: 위증죄의 진술은 구체적 사실에 관한 진술을 말하며, 단순한 가치판단·평가 또는 경험 사실에 부가된 법률적·주관적 의견의 오류는 진술에 해당하지 않거나 위증죄를 구성하지 않는다. 진술은 언어뿐 아니라 몸짓이나 표정의 답변도 포함할 수 있으나, 조서나 증인진술서 내용이 사실이라는 일반적 확인만으로는 특별한 사정이 없는 한 그 구체적 내용을 반복 진술한 것으로 볼 수 없다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 일반적 서면 확인이 특정 사실의 반복진술에 이르는 특별한 사정은 사실심 판단이 필요하다.
- bounded sources:

  - `comm_001692_제152조_Ⅰ.2_15` / `Ⅰ.2`: “증인의 증언 중 가치 판단이나 평가에 관한 부분은 위증죄의 객관적 구성요건인 ‘진술’에 해당하 지 않는다.”
  - `comm_001692_제152조_Ⅰ.2_17` / `Ⅰ.2`: “말에 의한 진술이 일반적인 방법 이겠지만 말에 의하지 않더라도 몸짓이나 표정 등의 방법으로 답변하였다고 볼 수 있다면 진술에 포함될 수 있다.”

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

## 13. `art152_sec1_2.witness_status`

- proposition: 위증죄의 증인은 재판절차나 징계절차에서 자신이 경험한 사실을 진술하는 당사자가 아닌 제3자이다. 별개 범죄사실의 공범 아닌 공동피고인은 다른 피고인의 범죄사실에 관하여 증인 지위에 있을 수 있고, 공범인 공동피고인도 절차 분리로 피고인 지위에서 벗어나거나 유죄판결 확정 후 다른 공범 사건에서 증인이 될 수 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 공범 공동피고인의 증인적격에 관한 학설 대립과 보고된 판례의 적용 범위를 검토해야 한다.
- bounded sources:

  - `comm_001692_제152조_Ⅰ.2_13` / `Ⅰ.2`: “위증죄의 주체가 되는 증인은 재판절차, 징계절차 등에서 자신이 과거에 경 (가) 험한 사실에 관하여 진술하는 사람으로서 당사자가 아닌 제3자를 말한다.”
  - `comm_001692_제152조_Ⅰ.2_14` / `Ⅰ.2`: “공범인 공동피고인은 당해 소송절차에 서는 피고인의 지위에 있으므로 다른 공동피고인에 대한 공소사실에 관하여 증 인이 될 수 없으나, 소송절차가 분리되어 피고인의 지위에서 벗어나게 되면 다 른 공동피고인에 대한 공소사실에 관하여 증인이 될 수 있다고 판시”

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

## 14. `art152_sec1_3.attempt_false_testimony_start`

- proposition: 위증죄의 실행의 착수는 증인이 허위진술을 시작한 때에 인정된다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 허위진술의 시작 시점을 실행의 착수 시점으로 정리한 카드다.
- bounded sources:

  - `comm_001692_제152조_Ⅰ.3_24` / `Ⅰ.3`: “위증죄의 실행의 착수는 증인이 허위의 진술을 시작한 때에 인정된다.”

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

## 15. `art152_sec1_3.completion_examination_end`

- proposition: 위증죄는 해당 증인에 대한 신문절차가 종료하여 더 이상 진술을 철회·시정할 수 없게 된 때 기수에 이른다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`settled`, review_required=`False`
- source track: `unit_core`
- prior note: 증인신문절차 종료 및 철회·시정 불가능 시점을 기수 시점으로 정리한 학설 일치 사항이다.
- bounded sources:

  - `comm_001692_제152조_Ⅰ.3_24` / `Ⅰ.3`: “당해 증인에 대한 신문절차가 마쳐졌을 때, 다시 말하면 증인 신문절차가 종료하여 더는 진술을 철회·시정할 수 없게 되었을 때 기수가 된다는 데 학설이 일치한 다.”

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
