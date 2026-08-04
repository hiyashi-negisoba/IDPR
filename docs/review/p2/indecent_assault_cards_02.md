# 강제추행 RuleIR 카드 검수 2

- unit: `indecent_assault`
- articles: art298
- cards: 16–30 / 33
- law snapshot: `kr_criminal_act_effective_2026-08-03`

각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.

- decision: approve, rewrite, context_only, split, reject
- role: component, bar, boundary, waiver, post_outcome, context_only
- component join: mandatory_all, alternative_any, not_applicable

## 기존 결정 C 자동 계승

아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.

- #26 `art298_sec3_2.indecent_act_scope`: `art298_sec3_2.indecent_act_no_body_part_distinction` (status=`valid`)

## 16. `art298_sec3_2.no_contact_minor_elevator_exposure`

- proposition: 아파트 엘리베이터에서 13세 미만 피해자에게 성기를 꺼내 잡고 움직이며 피해자 쪽으로 다가간 경우, 신체 접촉 없이도 강제추행이 인정된 사례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소개된 비접촉 인정 사례의 구체적 연령·장소·행위태양을 넘어 일반화하지 않는다.
- bounded sources:

  - `comm_001692_제298조_Ⅲ.2_12` / `Ⅲ.2`: “피고인이 아파트 엘리베이터 내에 13세 미만인 피해자와 단둘이 탄 다음 피해자를 향하여 성기를 꺼내어 (여, 11세) 잡고 여러 방향으로 움직이다가 이를 보고 놀란 피해자 갑 쪽으로 가까이 다가간 경우”

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

## 17. `art298_sec3_2.no_contact_urination_toward_victim`

- proposition: 피해자 뒤로 다가가 성기를 드러낸 뒤 피해자를 향한 자세에서 피해자의 머리카락 및 옷 위에 소변을 본 경우, 신체 접촉 없이도 강제추행이 인정된 사례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소개된 비접촉 인정 사례의 행위태양 및 피해자에 대한 침해 정도를 개별적으로 검토한다.
- bounded sources:

  - `comm_001692_제298조_Ⅲ.2_12` / `Ⅲ.2`: “피고인이 처음 보는 여성인 피해자를 따라가 피해자가 아파트 (여, 18세) 놀이터의 의자에 앉아 전화통화를 하자 뒤로 몰래 다가가 성기를 드러내고 피해자 를 향한 자세에서 피해자의 머리카락 및 옷 위에 소변을 본 경우”

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

## 18. `art298_sec3_2.recent_precedent_nonsexual_sensitive_contact`

- proposition: 최근 판례는 추행을 성적으로 민감한 부위 접촉에 한정하지 않고, 성희롱적 언사와의 결합, 피해자의 거부의사 표시, 위력관계 등을 고려하여 신체 부위와 관계없이 성적 자기결정권 침해 여부를 판단하는 경향이 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 최근 판례 경향으로 소개된 내용이므로 원전 판례를 확인하기 전까지 확정 규칙으로 취급하지 않는다.
- bounded sources:

  - `comm_001692_제298조_Ⅲ.2_11` / `Ⅲ.2`: “최근 판례는 추행을 반드시 성적으로 민감 한 부위에 대한 접촉행위에 한정하지 않고 넓게 인정하는 경향이 있다.”
  - `comm_001692_제298조_Ⅲ.2_11` / `Ⅲ.2`: “특히 ⅰ) 피고인의 성희롱적 언사와 결합된 경우, ⅱ) 피해자가 평소에 또는 피고인의 행위 무렵 자신의 성적 자유에 반한다는 의미에서 명시적·묵시적으로 같은 행 위를 거부하는 의사를 표시한 경우, ⅲ) 업무상 기타 이유로 위력관계에 있음이 분명한 경우”
  - `comm_001692_제298조_Ⅲ.2_11` / `Ⅲ.2`: “피해자의 성적 자 기결정권의 침해 여부를 궁극적인 기준으로 강제추행죄 성립 여부를 판단하되”

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

## 19. `art298_sec3_2.toddler_hand_contact_not_molestation`

- proposition: 2세 피해자에게 사탕을 건네며 악수하자고 하여 양손으로 피해자의 손을 잡고, 어머니가 손을 빼내는 과정에서 피고인의 손이 옷 위로 피해자 몸에 잠시 닿은 경우에는 추행을 인정하지 않았다는 판례 사례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 소개된 개별 비인정 사례이며, 다른 사실관계에 대한 일반적 부정 규칙으로 확장하지 않는다.
- bounded sources:

  - `comm_001692_제298조_Ⅲ.2_11` / `Ⅲ.2`: “피고인이 피해자가 피해자의 어머니의 손을 잡고 걸어가고 있는 (여, 2세) 것을 발견하고 피해자에게 다가가 사탕을 건네며 “우리 악수하자.”라고 말하면 서 피고인의 양손으로 피해자의 오른손을 잡고”
  - `comm_001692_제298조_Ⅲ.2_11` / `Ⅲ.2`: “어머니가 피해자의 손을 피고인 의 손으로부터 빼내려고 잡아끌면서 피고인의 손이 피해자의 몸에 옷 위로 잠 시 닿은 경우 추행을 인정하지 않았다.”

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

## 20. `art298_sec3_2.victim_actual_awareness_not_required`

- proposition: 추행행위는 행위자가 대상자를 상대로 객관적으로 성적 수치심 또는 혐오감을 일으킬 만하고 선량한 성적 도덕관념에 반하는 행위를 실행하면 충분하며, 대상자가 실제로 이를 느끼거나 행위사실을 인식할 필요는 없다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 피해자의 실제 감정 또는 인식 부재를 자동적 비추행 사유로 취급하지 않되, 객관적 평가 기준은 별도로 적용한다.
- bounded sources:

  - `comm_001692_제298조_Ⅲ.2_9` / `Ⅲ.2`: “그 행위로 말미암아 대상자가 성적 수치심이나 혐오감 을 반드시 실제로 느껴야 하는 것은 아니다.”

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

## 21. `art298_sec3_3.attempt_commencement`

- proposition: 강제추행의 실행 착수는 강제추행 수단인 폭행·협박이 개시된 때에, 기습추행의 경우에는 상대방 의사에 반하는 유형력 행사가 있는 때에 인정된다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 폭행·협박의 개시 및 기습추행에서 의사에 반하는 유형력 행사 여부는 개별 사실관계 평가가 필요하다.
- bounded sources:

  - `comm_001692_제298조_Ⅲ.3_14` / `Ⅲ.3`: “본죄는 피해자에 대한 강제추행의 수단으로서의 폭행·협박이 개시된 때, 그리고 이른바 ‘기습추행’의 경우에는 상대방의 의사에 반하는 유형력의 행사가 있는 때 에 실행의 착수가 있다고 보아야 한다.”

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

## 22. `art298_sec3_3.surprise_assault_attempt_hugging`

- proposition: 피고인의 팔이 피해자의 몸에 닿지 않았더라도 양팔을 높이 들어 갑자기 뒤에서 껴안으려는 행위는 피해자의 의사에 반하는 유형력 행사로서 폭행행위에 해당하고, 그때 기습추행에 관한 실행의 착수가 있어 강제추행미수죄에 해당한다는 사례가 소개되어 있다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`precedent_position`, review_required=`True`
- source track: `unit_core`
- prior note: 댓글이 소개한 사례의 원판례 및 사실관계 범위를 primary precedent index에서 확인해야 한다.
- bounded sources:

  - `comm_001692_제298조_Ⅲ.3_14` / `Ⅲ.3`: “피고인의 팔이 피해자의 몸에 닿지는 않았더 라도 양팔을 높이 들어 갑자기 뒤에서 껴안으려는 행위는 피해자의 의사에 반 하는 유형력의 행사로서 폭행행위에 해당하고, 그때 ‘기습추행’에 관한 실행의 착수가 있었다고 할 것이므로, 강제추행미수죄에 해당한다.”

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

## 23. `art298_sec4.disability_intent_assessment`

- proposition: 피고인이 자폐성 장애 또는 지적장애인인 경우 비장애인 관점에서 언행이 이례적·비합리적이라는 이유만으로 고의를 함부로 추단해서는 안 되며, 장애 정도와 지적·판단능력 및 행동양식을 구체적으로 심리하여 고의를 판단해야 한다.
- current metadata: formalization=`standard_input`, polarity=`negative`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 비장애인 관점의 이례성·비합리성만으로 고의를 추단하지 않는 제한 규범이다. 장애 특성과 판단능력에 관한 구체적 심리 및 보고된 판례 원문 확인이 필요하다.
- bounded sources:

  - `comm_001692_제298조_Ⅳ_15` / `Ⅳ`: “외관상 드러난 피 고인의 언행이 비장애인의 관점에서 이례적이라거나 합리적이지 않다는 이유만 으로 함부로 고의를 추단하거나 이를 뒷받침하는 간접사실로 편가해서는 안 되 고, 전문가의 진단이나 감정 등을 통해 피고인의 장애 정도, 지적·판단능력 및 행동양식 등을 구체적으로 심리하여 고의 유무를 판단하여야 할 것이다.”

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

## 24. `art298_sec4.intent_awareness_conditional`

- proposition: 강제추행죄의 고의는 폭행 또는 협박으로 사람을 추행한다는 인식이며, 미필적 고의로도 충분하다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 고의의 존재와 미필적 고의 해당 여부는 사건별 사실관계 평가가 필요하므로 standard input으로 유지한다.
- bounded sources:

  - `comm_001692_제298조_Ⅳ_15` / `Ⅳ`: “본죄의 고의는 폭행 또는 협박으로 사람에 대하여 추행하는 것에 대한 인식을 말한다. 미필적 고의로도 족하다.”

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

## 25. `art298_sec4.intent_inference`

- proposition: 고의를 부인하는 경우 피고인의 능력·경력, 동기와 경위, 피해자와의 관계, 행위태양과 전후 정황 및 평소 행동양태 등 간접사실을 종합하여 판단하고, 고의 징표와 어긋나는 사실의 의문점이 해소되어야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 댓글에 보고된 판단기준이므로 해당 판례 원문을 사용자 제공 primary precedent index에서 확인해야 한다.
- bounded sources:

  - `comm_001692_제298조_Ⅳ_15` / `Ⅳ`: “피고인의 나이·지능·지적능력 및 판단능력, 직업 및 경력, 피고인이 행위에 이르게 된 경위와 동기, 피고인과 피해자의 관계, 구체적 행위 태양 및 행위 전후의 정황, 피고인의 평소 행동양태·습관 등 객관적 사정 을 종합하여 판단해야 하고, 피고인이 고의로 추행을 하였다고 볼 만한 징표와 어긋나는 사실의 의문점이 해소되어야 한다.”

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

## 26. `art298_sec5.consent_after_violence_attempt`

- proposition: 강제추행을 위한 폭행·협박 착수 후 피해자가 자유롭고 진정한 의사로 동의한 경우 강제추행미수죄가 성립할 수 있으나, 동의가 폭행·협박으로 강요된 것인지 신중히 판단해야 한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 폭행·협박 착수 후 동의의 자유성·진정성과 강제추행미수 성립 여부는 사실관계별 법률 검토가 필요하다.
- bounded sources:

  - `comm_001692_제298조_Ⅴ_16` / `Ⅴ`: “강제추행을 위한 폭행·협박에 착수한 후에 자유롭고 진정한 의사로서 행 위자의 행위에 동의한 경우에는 강제추행미수죄가 성립할 것이나 피해자의 동 의는 행위자의 폭행·협박으로 인하여 강요된 것일 수 있으므로 진정성 판단에 는 신중을 기해야 한다.”

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

## 27. `art298_sec5.revoked_consent`

- proposition: 피해자가 사전에 신체접촉 등을 승낙하였더라도 동의를 번복할 수 있으며, 승낙을 번복한 경우에는 승낙이 있다고 볼 수 없다.
- current metadata: formalization=`standard_input`, polarity=`exception`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 동의의 번복 및 사전 용인의 범위 초과 여부는 개별 사정에 대한 평가가 필요하다.
- bounded sources:

  - `comm_001692_제298조_Ⅴ_16` / `Ⅴ`: “피해자가 사전에 신체접촉 등을 승낙하였다고 하더 라도 그 동의를 번복할 수 있고, 일정 수준의 신체접촉을 용인하였더라도 자신 이 예상하거나 동의한 범위를 넘어서는 신체접촉을 거부할 수 있다. 승낙을 번복한 경우에는 승낙이 있다고 볼 수 없다.”

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

## 28. `art298_sec6.multiple_acts_comprehensive_offense`

- proposition: 원칙적으로 각 추행행위마다 하나의 범죄가 성립하지만, 각 행위가 시간적·장소적으로 가깝고 범의의 단일성과 계속성이 인정되면 포괄일죄가 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 시간적·장소적 근접성 및 범의의 단일성·계속성 판단에는 개별 사실관계에 대한 평가가 필요하다.
- bounded sources:

  - `comm_001692_제298조_Ⅵ_17` / `Ⅵ`: “원칙적으로 각 추행행위마다 하나의 범죄가 성립한다. 다만 각 추행행위가 시간적·장소적으 로 가까워 범의의 단일성과 계속성을 인정할 수 있을 때에는 포괄하여 일 (犯意) 죄가 성립한다.”

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

## 29. `art298_sec6.multiple_victims_multiple_offenses`

- proposition: 피해자가 여러 명이면 동일 장소에서 동일한 폭행·협박에 의한 경우라도 피해자별로 수개의 죄가 성립한다.
- current metadata: formalization=`deterministic_rule`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`False`
- source track: `unit_core`
- prior note: 동일 장소 및 동일한 폭행·협박 여부와 무관하게 피해자별 죄수 산정 관계를 정하는 카드다.
- bounded sources:

  - `comm_001692_제298조_Ⅵ_17` / `Ⅵ`: “피해자가 여러 명인 경우에는 비록 동일한 장소에서 동일한 폭행·협박에 의한 것이라고 하더라도 각 피해자에 따 라 수개의 죄가 성립한다.”

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

## 30. `art298_sec8.forced_undressing_camera_concurrence`

- proposition: 피해자를 강제로 옷 벗겨 나체가 되게 한 다음 카메라로 촬영한 행위에는 강제추행죄와 카메라 등을 이용한 촬영죄의 실체적 경합범이 성립한다.
- current metadata: formalization=`standard_input`, polarity=`positive`, doctrinal_status=`descriptive`, review_required=`True`
- source track: `unit_core`
- prior note: 강제 탈의·나체 상태·카메라 촬영이라는 사실관계가 인용문 범위에 해당하는지 검토가 필요하다.
- bounded sources:

  - `comm_001692_제298조_Ⅷ_19` / `Ⅷ`: “피해자로 하여금 강제로 옷을 벗어 나체가 되게 한 다음 카메라로 이를 촬영하 는 행위는 본죄와 성폭력범죄의 처벌 등에 관한 특례법 제14조 (카메라 등을 이용 의 실체적 경합범이 성립한다.”

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
