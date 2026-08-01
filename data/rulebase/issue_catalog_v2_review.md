# Issue catalog v2 — 카드 재적재 검수

버전 `2.1.0-draft`. 원본 RuleIR 1,848장은 수정하지 않았다.

런타임의 기본 단위는 카드가 아니라 `issue packet`이다. 일반법리 anchor만 issue와 함께 적재하고, 세부 판단기준·구체 사실패턴은 관련 사실이 있을 때만 검색한다.

## 축소 결과

- 전체: 카드 1848장 → issue 372개 → 기본 평가 issue 159개
- 검수 조문: 카드 262장 → issue 40개 → 기본 평가 issue 18개
- 현재 4조문 스모크: Call-2 카드 193장 → 기본 평가 issue 14개
- 검수 조문 load policy: retrieve_candidate=171, anchor_context=57, symbolic_only=34
- 검수 조문 구체 사실패턴: 78장
- 우선 법률 검수: 0개 기본 평가 issue

`anchor_context`는 질문이 아니라 해당 issue 판단에 함께 주는 일반법리다. `retrieval_candidate`는 사건 사실과 관련될 때만 붙인다.

## 우선 법률 검수 큐

| issue | 제목 | anchors | cards | cases | 검수 사유 |
|---|---|---:|---:|---:|---|

> comment:

## art297 — 카드 56장 / 기본 평가 issue 4개

| issue | 제목 | function | runtime | anchors | retrieve | cases | review |
|---|---|---|---|---:|---:|---:|---|
| art297.Ⅰ.support_issue | 의의 | support_issue | retrieve_support | 0 | 1 | 0 |  |
| art297.Ⅱ.element_issue | 주체 | element_issue | assess_issue | 1 | 0 | 1 |  |
| art297.Ⅲ.element_issue | 객체 | element_issue | assess_issue | 2 | 3 | 3 |  |
| art297.Ⅳ.element_issue | 행위 | element_issue | assess_issue | 3 | 10 | 6 |  |
| art297.Ⅳ.participation_issue | 행위 | participation_issue | relation_condition | 1 | 1 | 1 |  |
| art297.Ⅳ.stage_issue | 행위 | stage_issue | relation_condition | 2 | 2 | 0 |  |
| art297.Ⅴ.guard_issue | 피해자의 승낙 | guard_issue | retrieve_guard | 1 | 3 | 0 |  |
| art297.Ⅵ.element_issue | 고의 | element_issue | assess_issue | 1 | 1 | 0 |  |
| art297.Ⅶ.concurrence_issue | 죄수 | concurrence_issue | relation_condition | 1 | 1 | 0 |  |
| art297.Ⅸ.concurrence_issue | 다른 죄와의 관계 | concurrence_issue | relation_condition | 1 | 9 | 2 |  |
| art297.Ⅹ.guard_issue | 피해자 행위의 위법성 조각 | guard_issue | retrieve_guard | 1 | 2 | 2 |  |

### anchor 일반법리

| issue | card id | proposition |
|---|---|---|
| art297.Ⅱ.element_issue | art297.unrestricted_principal | 강간죄의 주체에는 제한이 없고 남성과 여성 모두 주체가 될 수 있다. |
| art297.Ⅲ.element_issue | art297.object-person | 강간죄의 객체는 남녀를 불문한 사람이며, 성년·미성년, 기혼 여부, 음행 상습, 기존 성관계 경험 및 성교능력 유무를 불문한다. |
| art297.Ⅲ.element_issue | art297_sec3_4.intercourse_opposite_sex | 강간죄의 간음행위는 남성 성기의 여성 성기 삽입 또는 양 성기의 결합을 의미하므로, 단독정범의 경우 행위주체와 객체는 서로 다른 성이어야 한다는 설명이 제시되어 있다. |
| art297.Ⅳ.element_issue | art297.conduct.violence-threat-rape | 강간죄의 행위는 폭행 또는 협박으로 사람을 강간하는 것이다. |
| art297.Ⅳ.element_issue | art297_sec4_2.rape_and_penetration | 강간은 폭행·협박으로 상대방 반항을 불가능하거나 현저히 곤란하게 하여 간음하는 것이며, 간음은 다수설상 남성 성기의 여성 성기에 삽입 또는 양 성기의 결합을 말한다. |
| art297.Ⅳ.element_issue | art297_sec4_1.violence_threat_definition | 강간죄의 수단인 폭행은 사람의 신체에 대한 유형력 행사 등 일체의 불법적 공격이고, 협박은 일반적으로 사람에게 공포심을 일으킬 수 있는 정도의 해악 고지이다. |
| art297.Ⅳ.participation_issue | art297_sec4_4.successive_perpetrator_quasi_rape | 선행자의 행위를 이용하여 피해자를 간음한 후행자에게는 준강간죄가 성립할 여지가 있다. |
| art297.Ⅳ.stage_issue | art297_sec4_3.completion | 남성 성기가 여성 성기에 삽입되거나 결합되는 순간 강간죄는 기수가 되며, 완전한 삽입·결합, 성적 만족 또는 사정은 필요하지 않다. |
| art297.Ⅳ.stage_issue | art297_sec4_3.attempt_commencement | 강간 수단으로 피해자 반항을 불가능하거나 현저히 곤란하게 할 정도의 폭행·협박이 개시되면 실행의 착수가 인정되며, 속옷을 벗기거나 간음에 나아갈 필요는 없다. |
| art297.Ⅴ.guard_issue | art297_sec5.valid_consent | 피해자 본인의 성관계 승낙은 구성요건 해당성을 조각하며, 친권자 등의 승낙은 강간죄 성립에 영향을 주지 않는다. |
| art297.Ⅵ.element_issue | art297_sec6.intent | 강간죄에는 폭행·협박으로 피해자를 강간한다는 인식과 의사가 필요하고, 미필적 고의로도 충분하다. |
| art297.Ⅶ.concurrence_issue | art297_sec7.multiple_victims_multiple_offenses | 피해자가 여러 명이면 동일한 장소에서 동일한 폭행·협박에 의한 경우에도 각 피해자에 따라 수개의 강간죄가 성립한다. |
| art297.Ⅸ.concurrence_issue | art297_sec9.abduction_for_marriage_rape | 결혼을 목적으로 여자를 약취하여 강간한 경우 강간죄와 결혼을 위한 약취죄는 실체적 경합범이 성립한다. |
| art297.Ⅹ.guard_issue | art297_sec10.self_defense_against_rape | 피해자가 행위자의 폭행·협박에 의한 강간에 대항하여 방어 또는 적극적 반격행위를 한 경우, 자신의 법익에 대한 현재의 부당한 침해를 방위하기 위한 것이고 상당한 이유가 있으면 정당방위로 위법성이 조각된다. |

> comment:

## art298 — 카드 32장 / 기본 평가 issue 3개

| issue | 제목 | function | runtime | anchors | retrieve | cases | review |
|---|---|---|---|---:|---:|---:|---|
| art298.Ⅰ.support_issue | 의의 | support_issue | retrieve_support | 0 | 1 | 0 |  |
| art298.Ⅱ.element_issue | 주체 및 객체 | element_issue | assess_issue | 1 | 2 | 1 |  |
| art298.Ⅲ.element_issue | 행위 | element_issue | assess_issue | 2 | 13 | 10 |  |
| art298.Ⅲ.stage_issue | 행위 | stage_issue | relation_condition | 1 | 1 | 1 |  |
| art298.Ⅳ.element_issue | 고의 | element_issue | assess_issue | 1 | 2 | 0 |  |
| art298.Ⅴ.guard_issue | 피해자의 승낙 | guard_issue | retrieve_guard | 1 | 1 | 0 |  |
| art298.Ⅵ.concurrence_issue | 죄수 | concurrence_issue | relation_condition | 1 | 1 | 0 |  |
| art298.Ⅷ.concurrence_issue | 다른 죄와의 관계 | concurrence_issue | relation_condition | 1 | 0 | 0 |  |

### anchor 일반법리

| issue | card id | proposition |
|---|---|---|
| art298.Ⅱ.element_issue | art298.object.person | 강제추행죄의 객체는 사람이며, 성별·성년·미성년·기혼 여부를 불문한다. |
| art298.Ⅲ.element_issue | art298_sec3_2.indecent_act_definition | 추행은 객관적으로 일반인에게 성적 수치심 또는 혐오감을 일으키고 선량한 성적 도덕관념에 반하여 피해자의 성적 자유를 침해하는 행위이다. |
| art298.Ⅲ.element_issue | art298_sec3_1.force_threat_totality_assessment | 어떤 행위가 강제추행죄의 폭행 또는 협박에 해당하는지는 목적과 의도, 행위태양·내용, 경위·당시 정황, 당사자 관계 및 상대방 고통 등을 종합하여 판단한다. |
| art298.Ⅲ.stage_issue | art298_sec3_3.attempt_commencement | 강제추행의 실행 착수는 강제추행 수단인 폭행·협박이 개시된 때에, 기습추행의 경우에는 상대방 의사에 반하는 유형력 행사가 있는 때에 인정된다. |
| art298.Ⅳ.element_issue | art298_sec4.intent_awareness_conditional | 강제추행죄의 고의는 폭행 또는 협박으로 사람을 추행한다는 인식이며, 미필적 고의로도 충분하다. |
| art298.Ⅴ.guard_issue | art298_sec5.revoked_consent | 피해자가 사전에 신체접촉 등을 승낙하였더라도 동의를 번복할 수 있으며, 승낙을 번복한 경우에는 승낙이 있다고 볼 수 없다. |
| art298.Ⅵ.concurrence_issue | art298_sec6.multiple_victims_multiple_offenses | 피해자가 여러 명이면 동일 장소에서 동일한 폭행·협박에 의한 경우라도 피해자별로 수개의 죄가 성립한다. |
| art298.Ⅷ.concurrence_issue | art298_sec8.forced_undressing_camera_concurrence | 피해자를 강제로 옷 벗겨 나체가 되게 한 다음 카메라로 촬영한 행위에는 강제추행죄와 카메라 등을 이용한 촬영죄의 실체적 경합범이 성립한다. |

> comment:

## art301 — 카드 32장 / 기본 평가 issue 4개

| issue | 제목 | function | runtime | anchors | retrieve | cases | review |
|---|---|---|---|---:|---:|---:|---|
| art301.Ⅱ.element_issue | 주체, 객체 | element_issue | assess_issue | 1 | 1 | 0 |  |
| art301.Ⅲ.element_issue | 강간 등의 기회 | element_issue | assess_issue | 1 | 4 | 0 |  |
| art301.Ⅳ.element_issue | 상해 | element_issue | assess_issue | 4 | 7 | 3 |  |
| art301.Ⅴ.element_issue | 고의·인과관계·예견가능성 | element_issue | assess_issue | 2 | 3 | 0 |  |
| art301.Ⅵ.participation_issue | 공동정범 | participation_issue | relation_condition | 1 | 0 | 0 |  |
| art301.Ⅶ.stage_issue | 미수범 처벌규정의 부존재 및 결과적 가중범의 미수 인정 여부 관련 | stage_issue | relation_condition | 1 | 0 | 0 |  |
| art301.Ⅸ.concurrence_issue | 다른 죄와의 관계 등 | concurrence_issue | relation_condition | 1 | 3 | 0 |  |

### anchor 일반법리

| issue | card id | proposition |
|---|---|---|
| art301.Ⅱ.element_issue | art301_sec2.object_victim | 본죄의 객체인 사람은 강간 등의 피해자를 의미한다. |
| art301.Ⅲ.element_issue | art301_sec3.result_after_completion | 강간 등이 완료되기 전에 고의 또는 과실에 의한 상해 원인행위가 있으면, 상해 결과가 강간 등의 완료 후 발생하여도 본죄가 성립한다. |
| art301.Ⅳ.element_issue | art301_sec4_5.functional_impairment_injury | 외부 상처가 없더라도 육체적·정신적 생리기능 훼손, 예컨대 보행불능·수면장애·식욕감퇴 등의 기능장애가 발생하면 상해로 인정될 수 있다. |
| art301.Ⅳ.element_issue | art301_sec4_4.injury_recognition_factors | 상해 인정 여부에서는 상처가 일상생활에서 흔히 발생할 수 있는지, 별다른 치료 없이 단기간 내 자연치유되는지, 그리고 피해자가 피해 후 곧바로 상처를 자각하여 의사에게 호소했는지를 고려한다. |
| art301.Ⅳ.element_issue | art301_sec4_7.pubic_hair_pulling_injury | 음모를 잡아당겨 음부 부근에 염증을 발생시키거나 음모를 모근부터 뽑는 경우 상해에 해당한다고 볼 수 있다. |
| art301.Ⅳ.element_issue | art301_sec4_2.minor_injury_exclusion | 상처가 극히 경미하여 치료할 필요가 없고, 치료 없이도 일상생활에 아무런 지장이 없으며, 시간이 지나 자연적으로 치유될 수 있는 정도이면 상해에 해당하지 않는다. |
| art301.Ⅴ.element_issue | art301_sec5_2.rape_injury_result_aggravation | 강간 등 치상죄는 강간 등 범행의 고의는 필요하지만 상해 결과에 대한 고의는 요구되지 않는 결과적 가중범이다. |
| art301.Ⅴ.element_issue | art301_sec5_1.intentional_rape_injury | 강간 등 상해죄는 강간 등 범행과 상해에 대한 고의가 요구되는 고의범이고, 미필적 고의로도 족하다. |
| art301.Ⅵ.participation_issue | art301_sec6.intentional_injury_conspirator_intent | 고의범인 강간 등 상해죄에서 공모자에게도 상해에 대한 고의가 필요하므로, 그 고의를 인정하기 어려우면 공동정범으로 처벌할 수 없다. |
| art301.Ⅶ.stage_issue | art301_sec7.no_general_attempt_punishment | 형법상 강간 등 상해·치상죄에는 미수범 처벌규정이 없다. |
| art301.Ⅸ.concurrence_issue | art301.death_absorbs_injury | 강간으로 피해자에게 상해를 입힌 후 그로 인해 사망한 경우 상해는 사망에 흡수되어 강간치사죄만 성립한다. |

> comment:

## art319 — 카드 102장 / 기본 평가 issue 3개

| issue | 제목 | function | runtime | anchors | retrieve | cases | review |
|---|---|---|---|---:|---:|---:|---|
| art319.Ⅰ.support_issue | 보호법익 | support_issue | retrieve_support | 0 | 7 | 7 |  |
| art319.Ⅱ.element_issue | 객체 | element_issue | assess_issue | 3 | 16 | 8 |  |
| art319.Ⅲ.element_issue | 침입 | element_issue | assess_issue | 1 | 21 | 16 |  |
| art319.Ⅲ.stage_issue | 실행의 착수·기수 | stage_issue | relation_condition | 2 | 4 | 2 |  |
| art319.Ⅳ.element_issue | 고의 | element_issue | assess_issue | 1 | 1 | 0 |  |
| art319.Ⅴ.guard_issue | 위법성 조각 | guard_issue | retrieve_guard | 2 | 12 | 2 |  |
| art319.Ⅵ.concurrence_issue | 죄수·다른 죄와의 관계 | concurrence_issue | relation_condition | 1 | 6 | 1 |  |
| art319.Ⅶ.element_issue | 퇴거불응 | element_issue | retrieve_support | 4 | 11 | 2 |  |

### anchor 일반법리

| issue | card id | proposition |
|---|---|---|
| art319.Ⅱ.element_issue | art319_sec2_3.occupied_room_building_partition | 점유하는 방실은 건조물 내에서 사실상 지배·관리되는 일정한 구획을 말한다. |
| art319.Ⅱ.element_issue | art319_sec2_2.building_structure | 건조물은 주거를 제외한 일체의 건물과 그 부속 구조물 및 위요지를 의미하며, 일반적으로 주위벽 또는 기둥과 지붕 또는 천정으로 구성되어 사람이 기거하거나 출입할 수 있는 구조물이다. |
| art319.Ⅱ.element_issue | art319_sec2_1.temporary_dwelling | 일시적으로 기거하고 침식에 사용하는 장소도 주거가 될 수 있으며, 낮에만 기거하는 곳, 휴가 기간 중 설치한 텐트, 별장 및 주거용 차량이 이에 해당할 수 있다. |
| art319.Ⅲ.element_issue | art319_sec3_1.intrusion_objective_peace | 침입은 거주자가 주거에서 누리는 사실상의 평온상태를 해치는 행위태양으로 주거에 들어가는 것을 의미하며, 침입 여부는 출입 당시 객관적·외형적으로 드러난 행위태양을 기준으로 판단하는 것이 원칙이다. |
| art319.Ⅲ.stage_issue | art319_sec3_2.continuing_offense | 주거침입죄는 사실상 주거의 평온 침해가 계속되는 동안 계속 성립하는 계속범이며, 침입행위는 퇴거하거나 새 체류승낙이 있을 때까지 계속된다. |
| art319.Ⅲ.stage_issue | art319_sec3_2.attempt_commencement | 주거침입죄의 실행의 착수는 사실상 평온을 해치는 방법으로 주거나 관리 건조물 등에 들어가는 행위를 개시하여 구성요건 실현에 이르는 현실적·객관적 위험성을 갖춘 때에 인정된다. |
| art319.Ⅳ.element_issue | art319_sec4.intent_against_resident_will | 통설에 따르면 주거침입죄의 고의에는 거주자·관리자·점유자의 의사 또는 추정적 의사에 반하여 타인의 주거 등에 들어간다는 인식과 의사가 필요하며, 미필적 고의로도 충분하다. |
| art319.Ⅴ.guard_issue | art319_sec5_2.lawful_authority_entry | 적법한 권한에 따라 주거에 들어가는 행위는 공법상 또는 사법상 권한인지와 관계없이 위법성이 조각된다. |
| art319.Ⅴ.guard_issue | art319_sec5_3.justification.emergency_escape | 맹견의 추격이나 강도를 피하여 타인의 가옥에 몸을 피한 경우 긴급피난에 해당하여 위법성이 조각된다. |
| art319.Ⅵ.concurrence_issue | art319_sec6_1.continuing_offense | 주거침입죄는 사실상 주거의 평온 침해가 계속되는 동안 계속 성립하는 계속범이다. |
| art319.Ⅶ.element_issue | art319.refusal_to_leave.lawful_or_mistaken_entry | 퇴거불응죄는 처음에 적법하게 또는 과실로 타인의 주거 등에 들어간 사람이 거주자, 관리자 또는 점유자의 퇴거요구에 불응하는 경우 성립한다. |
| art319.Ⅶ.element_issue | art319_sec7_3.no_justifiable_reason | 퇴거불응죄가 성립하려면 퇴거에 불응할 정당한 사유가 없어야 하며, 정당한 사유가 있으면 성립하지 않는다. |
| art319.Ⅶ.element_issue | art319_sec7_1.refusal_to_leave_elements | 퇴거불응죄는 사람의 주거, 관리하는 건조물, 선박, 항공기 또는 점유하는 방실에서 퇴거요구를 받고 이에 응하지 않음으로써 성립한다. |
| art319.Ⅶ.element_issue | art319_sec7_4.intent | 퇴거불응죄의 고의가 인정되려면 거주자 등의 퇴거요구 및 그 정당성, 자신의 체류 정당성 결여를 인식하면서도 퇴거요구에 불응하려는 의사가 있어야 한다. |

> comment:

## art329 — 카드 40장 / 기본 평가 issue 4개

| issue | 제목 | function | runtime | anchors | retrieve | cases | review |
|---|---|---|---|---:|---:|---:|---|
| art329.Ⅱ.element_issue | 타인의 재물 | element_issue | assess_issue | 3 | 11 | 7 |  |
| art329.Ⅲ.element_issue | 절취 | element_issue | assess_issue | 1 | 1 | 0 |  |
| art329.Ⅲ.stage_issue | 기수시기 | stage_issue | relation_condition | 2 | 0 | 0 |  |
| art329.Ⅳ.element_issue | 고의 | element_issue | assess_issue | 1 | 3 | 1 |  |
| art329.Ⅴ.element_issue | 불법영득의사 | element_issue | assess_issue | 2 | 5 | 1 |  |
| art329.Ⅵ.guard_issue | 위법성·책임성의 문제 | guard_issue | retrieve_guard | 1 | 1 | 1 |  |

### anchor 일반법리

| issue | card id | proposition |
|---|---|---|
| art329.Ⅱ.element_issue | art329_sec2.theft_object_anothers_property_in_possession | 절도죄의 객체인 타인의 재물은 타인 소유이면서 타인의 점유 아래 있는 재물을 뜻한다. |
| art329.Ⅱ.element_issue | art329_sec2_2.possession_intent_definition | 점유의 의사는 개별적·법률적 의사가 아니라 일반적·포괄적이고 사실적인 의사이며, 잠재적인 의사로도 충분하다. |
| art329.Ⅱ.element_issue | art329_sec2_1.other_person_legal_entity | 절도죄에서 타인은 범인 이외의 자이며, 자연인뿐 아니라 소유권 주체가 될 수 있는 법인·공공단체·국가 등 단체를 포함한다. |
| art329.Ⅲ.element_issue | art329_sec3_1.taking_transfer_of_control | 절취는 단순히 재물을 타인의 지배에서 이탈시키는 것만으로는 부족하고, 재물을 자기 또는 제3자의 지배 아래로 옮기는 것을 뜻한다. |
| art329.Ⅲ.stage_issue | art329_sec3_3.completion.control_and_disposal | 절도는 타인의 재물을 자기의 실력적 지배 아래 두어 배타적·자유롭게 처분할 수 있는 상태가 되면 기수에 이르며, 영구적·안전한 경제적 가치 보전 상태에 둘 필요는 없다. |
| art329.Ⅲ.stage_issue | art329_sec3_3.completion.property_circumstances | 재물 취득 여부는 재물의 크기·무게·보관 장소·상태 등 제반 사정을 종합하여 사회통념에 맞게 판단한다. |
| art329.Ⅳ.element_issue | art329_sec4.intent.theft_intent_definition | 절도죄의 고의는 타인의 재물을 절취한다는 인식·인용이며, 점유자의 의사에 반하여 타인의 점유를 배제하고 자기 또는 제3자의 점유 아래로 재물을 취거한다는 인식·인용을 필요로 한다. |
| art329.Ⅴ.element_issue | art329_sec5_1.unlawful_appropriation_required | 절도죄 성립에는 주관적 불법요소로서 불법영득의사가 필요하며, 영득의사가 없으면 점유자의 의사에 반하여 점유를 침해하고 목적물을 자기 또는 제3자의 점유로 옮겨도 절도죄가 되지 않는다. |
| art329.Ⅴ.element_issue | art329_sec5_2.collateral_taking_unlawful_appropriation | 자기 채권의 담보로 삼기 위하여 채무자나 제3자 소유 물건을 자기 점유 아래로 옮긴 경우에는, 장래 채권변제를 받으면 반환할 의사가 있어도 불법영득의사가 인정된다. |
| art329.Ⅵ.guard_issue | art329_sec6.consent_manifestation | 절도에서 승낙은 외부적으로 표시되면 명시적·묵시적 여부를 불문하고 추정적 승낙도 가능하다. |

> comment:
