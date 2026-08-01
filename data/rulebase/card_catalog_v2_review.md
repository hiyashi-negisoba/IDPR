# Card catalog v2 — 재분류 검수

버전 `2.0.0-draft`. 원본 RuleIR 카드는 수정하지 않았다.

`canonical_element`는 카드 자체가 `norm_kind=element`일 때만 부여한다. slot이 core라는 이유로 하위 판례·사례 카드가 core를 상속하지 않는다.

## 요약

- 전체 카드: 1848
- 상세 검수 대상: 222 (art297, art298, art301, art319)
- 전체 runtime: always_assess=201, retrieve_assess=517, retrieve_only=507, relation_condition=263, static=360
- 대상 runtime: always_assess=20, retrieve_assess=71, retrieve_only=57, relation_condition=41, static=33
- 대상 중 자동분류 검수 필요: 34
- 우선 검수 큐(구성요건 후보 ∪ 자동분류 주의): 54

먼저 아래 우선 검수 큐를 확인한다. 상세 문맥이 필요하면 각 element group 표를 보고, `> comment:`에 잘못된 분류와 원하는 `function/form/runtime/gate_effect`를 적는다.

## 우선 검수 큐

| article | group | id | kind | function | form | runtime | 주의 사유 | proposition |
|---|---|---|---|---|---|---|---|---|
| art297 | art297_sec10 | art297_sec10.self_defense_against_rape | element | canonical_element | abstract_rule | always_assess | canonical_element 후보 확인 | 피해자가 행위자의 폭행·협박에 의한 강간에 대항하여 방어 또는 적극적 반격행위를 한 경우, 자신의 법익에 대한 현재의 부당한 침해를 방위하기 위한 것이고 상당한 이유가 있으면 정당방위로 위법성이 조각된다. |
| art297 | art297_sec10 | art297_sec10.tongue_biting_self_defense | standard | defeater | precedent_pattern | retrieve_only | function depends on an unreviewed slot-default role | 심야에 귀가 중인 피해자가 공동으로 강간하려는 행위자에게 끌려가 폭행·추행을 당하던 중 정조와 신체를 지키려 혀를 깨물어 혀 절단상을 입힌 경우 정당방위가 인정된 판례가 소개되어 있다. |
| art297 | art297_sec10 | art297_sec10.planned_killing_after_rape_no_self_defense | standard | defeater | precedent_pattern | retrieve_only | function depends on an unreviewed slot-default role | 계속 성관계를 강요받던 피해자가 남자 친구와 사전 공모하여 범행을 준비하고, 술에 취해 잠든 의붓아버지를 식칼로 살해한 경우 사회통념상 상당성이 결여되어 정당방위가 인정되지 않은 판례가 소개되어 있다. |
| art297 | art297 | art297.unrestricted_principal | element | skeleton_meta | abstract_rule | static | element metadata is overridden by a stage/concurrence/static frame | 강간죄의 주체에는 제한이 없고 남성과 여성 모두 주체가 될 수 있다. |
| art297 | art297 | art297.relative_special_act | exception | exception | precedent_pattern | retrieve_only | precedent-pattern form was detected linguistically | 피해자와 4촌 이내 혈족·인척, 동거 친족 또는 동거 사실상 친족 관계에 있는 자가 범한 경우 성폭력범죄의 처벌 등에 관한 특례법 제5조 제1항이 적용된다고 소개되어 있다. |
| art297 | art297 | art297.object-person | element | skeleton_meta | abstract_rule | static | element metadata is overridden by a stage/concurrence/static frame | 강간죄의 객체는 남녀를 불문한 사람이며, 성년·미성년, 기혼 여부, 음행 상습, 기존 성관계 경험 및 성교능력 유무를 불문한다. |
| art297 | art297 | art297.special-protection-statutes | exception | exception | precedent_pattern | retrieve_only | precedent-pattern form was detected linguistically | 피해자가 13세 미만자, 신체적·정신적 장애인 또는 아동·청소년인 경우에는 법정형이 더 높은 특별법 규정이 적용된다고 소개되어 있다. |
| art297 | art297 | art297.conduct.violence-threat-rape | element | canonical_element | abstract_rule | always_assess | canonical_element 후보 확인 | 강간죄의 행위는 폭행 또는 협박으로 사람을 강간하는 것이다. |
| art297 | art297_sec4_1 | art297_sec4_1.direct_violence_threat | element | canonical_element | abstract_rule | always_assess | canonical_element 후보 확인 | 강간죄의 폭행·협박은 행위자가 직접 가한 것이어야 하며, 타인의 폭행·협박을 이용해 간음한 경우에는 준강간죄가 성립할 수 있다. |
| art297 | art297_sec4_3 | art297_sec4_3.attempt_commencement | element | skeleton_meta | abstract_rule | static | element metadata is overridden by a stage/concurrence/static frame | 강간 수단으로 피해자 반항을 불가능하거나 현저히 곤란하게 할 정도의 폭행·협박이 개시되면 실행의 착수가 인정되며, 속옷을 벗기거나 간음에 나아갈 필요는 없다. |
| art297 | art297_sec4_4 | art297_sec4_4.successive_co_perpetration_negative | standard | participation | precedent_pattern | relation_condition | function depends on an unreviewed slot-default role | 선행자와의 공동가공 의사에 기한 기능적 행위지배를 후행자에게 인정할 수 없으면 승계적 공동정범은 성립할 수 없다는 대법원 취지가 소개되어 있다. |
| art297 | art297_sec4_4 | art297_sec4_4.successive_perpetrator_quasi_rape | standard | participation | abstract_rule | relation_condition | function depends on an unreviewed slot-default role | 선행자의 행위를 이용하여 피해자를 간음한 후행자에게는 준강간죄가 성립할 여지가 있다. |
| art297 | art297_sec5 | art297_sec5.consent_assessment | standard | defeater | abstract_rule | retrieve_assess | function depends on an unreviewed slot-default role | 성관계 승낙 여부는 행위 경위와 태양, 피해자 연령, 범행 당시 정황 등을 종합해 성적 자유 또는 성적 자기결정권 침해 여부를 기준으로 구체적·개별적으로 판단한다. |
| art297 | art297_sec5 | art297_sec5.prior_communications_not_consent | standard | defeater | abstract_rule | retrieve_assess | function depends on an unreviewed slot-default role | 피해자가 범행 무렵까지 피고인과 전화·문자 연락을 하고 호감을 보인 정황만으로 성관계 승낙 또는 묵인을 인정할 수는 없다. |
| art297 | art297_sec6 | art297_sec6.intent | element | canonical_element | abstract_rule | always_assess | canonical_element 후보 확인 | 강간죄에는 폭행·협박으로 피해자를 강간한다는 인식과 의사가 필요하고, 미필적 고의로도 충분하다. |
| art297 | art297_sec7 | art297_sec7.continuous_acts_single_offense | standard | concurrence | abstract_rule | relation_condition | function depends on an unreviewed slot-default role | 동일한 폭행·협박으로 피해자의 항거불가능 또는 현저한 곤란 상태가 계속되는 상황에서 수회 간음한 경우, 시간적·장소적 근접성과 범의의 단일성·계속성이 인정되면 포괄 일죄가 성립한다. |
| art297 | art297_sec7 | art297_sec7.new_violence_separate_offense | element | canonical_element | abstract_rule | always_assess | canonical_element 후보 확인 | 항거불능 상태가 종료된 후 다시 폭행·협박을 가하여 간음한 경우 별개의 강간죄가 성립한다. |
| art297 | art297_sec7 | art297_sec7.multiple_victims_multiple_offenses | element | canonical_element | abstract_rule | always_assess | canonical_element 후보 확인 | 피해자가 여러 명이면 동일한 장소에서 동일한 폭행·협박에 의한 경우에도 각 피해자에 따라 수개의 강간죄가 성립한다. |
| art297 | art297_sec9 | art297_sec9.rape_injury_death | standard | concurrence | abstract_rule | relation_condition | function depends on an unreviewed slot-default role | 강간 범행 과정에서 피해자가 상해를 입으면 강간상해죄나 강간치상죄가, 피해자가 사망하면 강간살인죄나 강간치사죄가 성립한다. |
| art297 | art297_sec9 | art297_sec9.nonprosecution_not_false_report_proof | standard | concurrence | precedent_pattern | relation_condition | function depends on an unreviewed slot-default role; precedent-pattern form was detected linguistically | 성폭행 등 피해 신고에 관하여 증거불충분 등의 불기소처분이나 무죄판결이 내려졌다는 사정만으로 신고내용을 허위라고 단정하여 무고의 적극적 근거로 삼아서는 안 된다. |
| art298 | art298 | art298.subject.unrestricted | element | skeleton_meta | abstract_rule | static | element metadata is overridden by a stage/concurrence/static frame | 강제추행죄의 주체에는 제한이 없고 남성과 여성 모두 주체가 될 수 있다. |
| art298 | art298_sec3_2 | art298_sec3_2.recent_precedent_nonsexual_sensitive_contact | standard | application_standard | precedent_pattern | retrieve_only | precedent-pattern form was detected linguistically | 최근 판례는 추행을 성적으로 민감한 부위 접촉에 한정하지 않고, 성희롱적 언사와의 결합, 피해자의 거부의사 표시, 위력관계 등을 고려하여 신체 부위와 관계없이 성적 자기결정권 침해 여부를 판단하는 경향이 소개되어 있다. |
| art298 | art298_sec3_3 | art298_sec3_3.attempt_commencement | causal_link | stage | abstract_rule | relation_condition | function depends on an unreviewed slot-default role | 강제추행의 실행 착수는 강제추행 수단인 폭행·협박이 개시된 때에, 기습추행의 경우에는 상대방 의사에 반하는 유형력 행사가 있는 때에 인정된다. |
| art298 | art298_sec4 | art298_sec4.intent_awareness_conditional | element | canonical_element | abstract_rule | always_assess | canonical_element 후보 확인 | 강제추행죄의 고의는 폭행 또는 협박으로 사람을 추행한다는 인식이며, 미필적 고의로도 충분하다. |
| art298 | art298_sec5 | art298_sec5.consent_after_violence_attempt | standard | defeater | abstract_rule | retrieve_assess | function depends on an unreviewed slot-default role | 강제추행을 위한 폭행·협박 착수 후 피해자가 자유롭고 진정한 의사로 동의한 경우 강제추행미수죄가 성립할 수 있으나, 동의가 폭행·협박으로 강요된 것인지 신중히 판단해야 한다. |
| art298 | art298_sec6 | art298_sec6.multiple_victims_multiple_offenses | element | canonical_element | abstract_rule | always_assess | canonical_element 후보 확인 | 피해자가 여러 명이면 동일 장소에서 동일한 폭행·협박에 의한 경우라도 피해자별로 수개의 죄가 성립한다. |
| art301 | art301_sec2 | art301_sec2.subject_predicate_offenses | element | stage | abstract_rule | relation_condition | element metadata is overridden by a stage/concurrence/static frame | 본죄의 주체는 열거된 강간·유사강간·강제추행·준강간 등 범죄를 범한 자 또는 그 미수에 그친 자이다. |
| art301 | art301_sec5_1 | art301_sec5_1.intentional_rape_injury | element | canonical_element | abstract_rule | always_assess | canonical_element 후보 확인 | 강간 등 상해죄는 강간 등 범행과 상해에 대한 고의가 요구되는 고의범이고, 미필적 고의로도 족하다. |
| art301 | art301_sec5_2 | art301_sec5_2.rape_injury_result_aggravation | element | skeleton_meta | abstract_rule | static | element metadata is overridden by a stage/concurrence/static frame | 강간 등 치상죄는 강간 등 범행의 고의는 필요하지만 상해 결과에 대한 고의는 요구되지 않는 결과적 가중범이다. |
| art301 | art301_sec6 | art301_sec6.intentional_injury_conspirator_intent | element | canonical_element | abstract_rule | always_assess | canonical_element 후보 확인 | 고의범인 강간 등 상해죄에서 공모자에게도 상해에 대한 고의가 필요하므로, 그 고의를 인정하기 어려우면 공동정범으로 처벌할 수 없다. |
| art319 | art319_sec2_1 | art319_sec2_1.enclosed_land_requirements | element | application_standard | precedent_pattern | retrieve_only | element metadata is overridden by a stage/concurrence/static frame | 위요지로 인정되려면 가옥 인접 주변 토지이고, 문·담 등 외부와의 경계가 설치되어 있으며, 가옥 이용에 제공되고 외부인이 함부로 출입할 수 없다는 점이 객관적으로 명확해야 한다. |
| art319 | art319_sec2_2 | art319_sec2_2.management_notice_insufficient | element | canonical_element | abstract_rule | always_assess | canonical_element 후보 확인 | 단순히 출입금지 표지를 해둔 것만으로는 관리라고 할 수 없다. |
| art319 | art319_sec3_1 | art319_sec3_1.bodily_entry_required | element | canonical_element | abstract_rule | always_assess | canonical_element 후보 확인 | 침입은 신체적 침입을 의미하므로 행위자의 신체가 주거에 들어가지 않으면 침입이 아니다. |
| art319 | art319_sec3_1 | art319_sec3_1.partial_entry_intent | element | application_standard | precedent_pattern | retrieve_only | element metadata is overridden by a stage/concurrence/static frame | 주거침입의 고의는 신체 일부라도 타인의 주거 안으로 들어간다는 인식으로 족하다. |
| art319 | art319_sec3_2 | art319_sec3_2.attempt_commencement | element | stage | abstract_rule | relation_condition | element metadata is overridden by a stage/concurrence/static frame | 주거침입죄의 실행의 착수는 사실상 평온을 해치는 방법으로 주거나 관리 건조물 등에 들어가는 행위를 개시하여 구성요건 실현에 이르는 현실적·객관적 위험성을 갖춘 때에 인정된다. |
| art319 | art319_sec3_2 | art319_sec3_2.post_conviction_continued_occupation | standard | stage | precedent_pattern | relation_condition | function depends on an unreviewed slot-default role | 무단침입으로 유죄판결을 받은 사람이 판결 확정 후에도 퇴거하지 않고 해당 주택에 계속 거주한 경우, 확정 이후 행위는 별도의 주거침입죄를 구성한다. |
| art319 | art319_sec4 | art319_sec4.intent_against_resident_will | element | canonical_element | abstract_rule | always_assess | canonical_element 후보 확인 | 통설에 따르면 주거침입죄의 고의에는 거주자·관리자·점유자의 의사 또는 추정적 의사에 반하여 타인의 주거 등에 들어간다는 인식과 의사가 필요하며, 미필적 고의로도 충분하다. |
| art319 | art319_sec5_2 | art319_sec5_2.right_holder_entry_without_procedure | standard | defeater | precedent_pattern | retrieve_only | function depends on an unreviewed slot-default role | 권리자가 자신의 권리를 실행하기 위한 경우라도 법정절차에 따르지 않고 주거에 침입하면 주거침입죄가 성립한다는 판례 입장이 소개되어 있다. |
| art319 | art319_sec5_2 | art319_sec5_2.labor_dispute_exclusive_occupation | standard | defeater | abstract_rule | retrieve_assess | function depends on an unreviewed slot-default role | 사업장 시설을 전면적·배타적으로 점거하여 조합원 외 출입을 저지하거나 사용자 관리지배를 배제해 업무 중단·혼란을 야기하는 행위는 정당한 쟁의행위 한계를 벗어나 위법성조각 없이 건조물침입죄가 성립한다. |
| art319 | art319_sec5_2 | art319_sec5_2.labor_dispute_incidental_act | standard | defeater | abstract_rule | retrieve_assess | function depends on an unreviewed slot-default role | 적법하게 개시된 쟁의행위의 목적을 공지·준비하기 위한 부수행위가 관행적 방식에 편승하여 이루어졌고 전체적으로 수단·방법의 적정성을 벗어나지 않으면 형법상 정당행위에 해당할 수 있다. |
| art319 | art319_sec5_2 | art319_sec5_2.labor_dispute_plant_occupation | standard | defeater | abstract_rule | retrieve_assess | function depends on an unreviewed slot-default role | 회사의 시설관리권을 배제한 전면 점거파업이 구조조정 저지를 목적으로 하여 정당한 쟁의행위로 볼 수 없고, 퇴거요구를 알면서도 공장에 들어간 경우 노동쟁의행위로서 정당행위에 해당하지 않는다. |
| art319 | art319_sec5_2 | art319_sec5_2.labor_dispute_explicit_denial_entry | standard | defeater | abstract_rule | retrieve_assess | function depends on an unreviewed slot-default role | 대회 개최를 위한 장소사용 허가를 명시적으로 불허받았음에도 대회 개최를 위해 대학에 들어간 경우 노동쟁의행위로서 정당행위에 해당하지 않는다. |
| art319 | art319_sec5_3 | art319_sec5_3.rightless_possessor.peace | standard | defeater | precedent_pattern | retrieve_only | function depends on an unreviewed slot-default role | 점유권원이 없는 자의 점유라도 주거의 평온은 보호되므로, 권리자가 권리실행을 위한 자력구제 수단으로 건조물에 침입하면 건조물침입죄가 성립한다는 판례가 소개되어 있다. |
| art319 | art319_sec6_1 | art319_sec6_1.post_final_conviction_continuance_separate_offense | standard | concurrence | precedent_pattern | relation_condition | function depends on an unreviewed slot-default role; precedent-pattern form was detected linguistically | 무단침입으로 유죄판결이 확정된 뒤에도 퇴거하지 않고 계속 거주하면, 판결확정 이후의 침입행위 및 위법상태 계속으로 별도의 주거침입죄가 된다. |
| art319 | art319_sec6_2 | art319_sec6_2.daytime_entry_no_night_intrusion_theft | standard | concurrence | abstract_rule | relation_condition | function depends on an unreviewed slot-default role | 주거침입이 주간에 이루어진 경우 야간주거침입절도죄는 성립하지 않는다. |
| art319 | art319_sec6_2 | art319_sec6_2.night_intrusion_theft_attempt_on_entry | standard | concurrence | abstract_rule | relation_condition | function depends on an unreviewed slot-default role | 야간에 타인의 재물을 절취할 목적으로 사람의 주거에 침입하면, 침입 단계에서 이미 야간주거침입절도 범죄행위의 실행에 착수한다. |
| art319 | art319_sec6_2 | art319_sec6_2.special_theft_entry_absorption | standard | concurrence | abstract_rule | relation_condition | function depends on an unreviewed slot-default role | 야간에 주거 일부를 손괴하고 침입한 뒤 절취한 경우 특수절도죄만 성립한다. |
| art319 | art319_sec7_1 | art319_sec7_1.refusal_to_leave_elements | element | canonical_element | abstract_rule | always_assess | canonical_element 후보 확인 | 퇴거불응죄는 사람의 주거, 관리하는 건조물, 선박, 항공기 또는 점유하는 방실에서 퇴거요구를 받고 이에 응하지 않음으로써 성립한다. |
| art319 | art319 | art319.refusal_to_leave.lawful_or_mistaken_entry | element | canonical_element | abstract_rule | always_assess | canonical_element 후보 확인 | 퇴거불응죄는 처음에 적법하게 또는 과실로 타인의 주거 등에 들어간 사람이 거주자, 관리자 또는 점유자의 퇴거요구에 불응하는 경우 성립한다. |
| art319 | art319_sec7_3 | art319_sec7_3.justified_demand | element | canonical_element | abstract_rule | always_assess | canonical_element 후보 확인 | 퇴거불응죄의 퇴거요구는 정당한 퇴거요구여야 하며, 정당하지 않은 퇴거요구에 불응한 경우에는 퇴거불응죄가 성립하지 않는다. |
| art319 | art319_sec7_3 | art319_sec7_3.refusal_delay | element | canonical_element | abstract_rule | always_assess | canonical_element 후보 확인 | 퇴거요구를 받은 적법 체류자도 즉시 퇴거하여야 하고, 유책한 지체가 있으면 퇴거불응이 된다. |
| art319 | art319_sec7_3 | art319_sec7_3.ability_to_leave | element | canonical_element | abstract_rule | always_assess | canonical_element 후보 확인 | 퇴거불응의 구성요건적 부작위가 되려면 행위자에게 퇴거의 작위의무를 이행할 일반적·개별적 행위가능성이 있어야 한다. |
| art319 | art319_sec7_3 | art319_sec7_3.no_justifiable_reason | element | canonical_element | abstract_rule | always_assess | canonical_element 후보 확인 | 퇴거불응죄가 성립하려면 퇴거에 불응할 정당한 사유가 없어야 하며, 정당한 사유가 있으면 성립하지 않는다. |
| art319 | art319_sec7_4 | art319_sec7_4.intent | element | canonical_element | abstract_rule | always_assess | canonical_element 후보 확인 | 퇴거불응죄의 고의가 인정되려면 거주자 등의 퇴거요구 및 그 정당성, 자신의 체류 정당성 결여를 인식하면서도 퇴거요구에 불응하려는 의사가 있어야 한다. |

> comment:

## art297

### art297_sec1

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art297_sec1.rape_definition | definition | positive | narrative | abstract_rule | static | none | 강간죄는 폭행 또는 협박으로 사람을 강간함으로써 성립하는 범죄이다. |

> comment:

### art297_sec10

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art297_sec10.self_defense_against_rape | element | positive | canonical_element | abstract_rule | always_assess | support | 피해자가 행위자의 폭행·협박에 의한 강간에 대항하여 방어 또는 적극적 반격행위를 한 경우, 자신의 법익에 대한 현재의 부당한 침해를 방위하기 위한 것이고 상당한 이유가 있으면 정당방위로 위법성이 조각된다. |
| art297_sec10.tongue_biting_self_defense | standard | positive | defeater | precedent_pattern | retrieve_only | block | 심야에 귀가 중인 피해자가 공동으로 강간하려는 행위자에게 끌려가 폭행·추행을 당하던 중 정조와 신체를 지키려 혀를 깨물어 혀 절단상을 입힌 경우 정당방위가 인정된 판례가 소개되어 있다. |
| art297_sec10.planned_killing_after_rape_no_self_defense | standard | negative | defeater | precedent_pattern | retrieve_only | block | 계속 성관계를 강요받던 피해자가 남자 친구와 사전 공모하여 범행을 준비하고, 술에 취해 잠든 의붓아버지를 식칼로 살해한 경우 사회통념상 상당성이 결여되어 정당방위가 인정되지 않은 판례가 소개되어 있다. |

자동분류 주의: function depends on an unreviewed slot-default role

> comment:

### art297

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art297.unrestricted_principal | element | positive | skeleton_meta | abstract_rule | static | none | 강간죄의 주체에는 제한이 없고 남성과 여성 모두 주체가 될 수 있다. |
| art297.indirect_perpetration | variant | positive | application_standard | abstract_rule | retrieve_assess | support | 강간죄는 자수범이 아니므로 간접정범 형태로 범할 수 있다. |
| art297.relative_special_act | exception | exception | exception | precedent_pattern | retrieve_only | exclude | 피해자와 4촌 이내 혈족·인척, 동거 친족 또는 동거 사실상 친족 관계에 있는 자가 범한 경우 성폭력범죄의 처벌 등에 관한 특례법 제5조 제1항이 적용된다고 소개되어 있다. |
| art297.object-person | element | positive | skeleton_meta | abstract_rule | static | none | 강간죄의 객체는 남녀를 불문한 사람이며, 성년·미성년, 기혼 여부, 음행 상습, 기존 성관계 경험 및 성교능력 유무를 불문한다. |
| art297.special-protection-statutes | exception | exception | exception | precedent_pattern | retrieve_only | exclude | 피해자가 13세 미만자, 신체적·정신적 장애인 또는 아동·청소년인 경우에는 법정형이 더 높은 특별법 규정이 적용된다고 소개되어 있다. |
| art297.conduct.violence-threat-rape | element | positive | canonical_element | abstract_rule | always_assess | support | 강간죄의 행위는 폭행 또는 협박으로 사람을 강간하는 것이다. |

자동분류 주의: element metadata is overridden by a stage/concurrence/static frame; precedent-pattern form was detected linguistically

> comment:

### art297_sec3_2

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art297_sec3_2.spouse_rape_holding | standard | positive | application_standard | precedent_pattern | retrieve_only | support | 실질적 부부관계가 유지되는 경우에도 남편이 반항을 불가능하거나 현저히 곤란하게 할 정도의 폭행·협박으로 아내를 간음하면 강간죄가 성립할 수 있다는 전원합의체 판결의 입장이 소개되어 있다. |
| art297_sec3_2.spouse_violence_assessment | standard | positive | application_standard | precedent_pattern | retrieve_only | support | 배우자 강간에서 폭행·협박이 반항을 불가능하거나 현저히 곤란하게 할 정도인지 여부는 폭행·협박의 내용·정도, 유형력 행사 경위, 혼인생활 형태, 평소 성행, 성교 당시 및 이후 상황 등을 종합하여 신중히 판단한다. |

> comment:

### art297_sec3_4

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art297_sec3_4.intercourse_opposite_sex | definition | positive | narrative | abstract_rule | static | none | 강간죄의 간음행위는 남성 성기의 여성 성기 삽입 또는 양 성기의 결합을 의미하므로, 단독정범의 경우 행위주체와 객체는 서로 다른 성이어야 한다는 설명이 제시되어 있다. |
| art297_sec3_4.sex_classification | standard | positive | application_standard | abstract_rule | retrieve_assess | support | 강간죄에서 남성과 여성의 구별은 성염색체보다 개인의 성귀속감, 사회적·규범적 성 및 일반인의 평가를 종합하여 판단하는 것이 타당하다는 견해가 제시되어 있다. |

> comment:

### art297_sec4_1

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art297_sec4_1.violence_threat_definition | definition | positive | narrative | abstract_rule | static | none | 강간죄의 수단인 폭행은 사람의 신체에 대한 유형력 행사 등 일체의 불법적 공격이고, 협박은 일반적으로 사람에게 공포심을 일으킬 수 있는 정도의 해악 고지이다. |
| art297_sec4_1.direct_violence_threat | element | positive | canonical_element | abstract_rule | always_assess | support | 강간죄의 폭행·협박은 행위자가 직접 가한 것이어야 하며, 타인의 폭행·협박을 이용해 간음한 경우에는 준강간죄가 성립할 수 있다. |
| art297_sec4_1.third_party_or_property_threat | standard | positive | application_standard | abstract_rule | retrieve_assess | support | 제3자에 대한 폭행, 피해자 소유 기물 파괴 또는 피해자 가족 위협 등의 방법으로 피해자의 저항 의지를 꺾은 뒤 간음한 경우에도 강간죄가 성립할 수 있다. |
| art297_sec4_1.no_retrospective_inference | standard | negative | application_standard | precedent_pattern | retrieve_only | refute | 피해자가 사후적으로 범행 현장을 벗어날 수 있었거나 사력을 다해 반항하지 않았다는 사정만으로 폭행·협박이 항거를 현저히 곤란하게 할 정도가 아니었다고 섣불리 단정해서는 안 된다. |
| art297_sec4_1.threat_alone | standard | positive | application_standard | precedent_pattern | retrieve_only | support | 폭행 없이 협박만으로 피해자를 간음한 경우에도 그 협박이 항거를 불가능하게 하거나 현저히 곤란하게 할 정도이면 강간죄가 성립한다. |
| art297_sec4_1.extramarital_exposure_threat | standard | positive | application_standard | precedent_pattern | retrieve_only | support | 유부녀에게 혼인 외 성관계 사실 폭로를 협박하여 간음 또는 추행한 경우, 협박 정도는 폭로의 상대방·범위·방법, 협박 경위, 당사자 신분·사회적 지위와 관계, 당시 및 이후 정황, 심리적 압박 등을 종합하여 판단한다. |
| art297_sec4_1.force_threat_timing_before_completion | causal_link | positive | skeleton_meta | abstract_rule | static | none | 폭행·협박은 반드시 간음행위보다 선행할 필요는 없고, 간음행위 종료 전까지 있으면 충분하다. |
| art297_sec4_1.force_threat_temporal_gap | causal_link | positive | application_standard | abstract_rule | retrieve_assess | support | 폭행·협박이 선행된 경우 폭행·협박과 간음 사이에는 시간적 간격이 있을 수 있다. |
| art297_sec4_1.victim_testimony_reliability | standard | positive | application_standard | precedent_pattern | retrieve_only | support | 성폭력 사건에서 피해자 진술이 유일한 직접증거인 경우, 주요 부분의 일관성·구체성, 논리와 경험칙상 합리성, 객관적 사실과의 모순 여부 및 허위 불리진술 동기 등을 종합하여 신빙성을 신중히 판단해야 한다. |
| art297_sec4_1.gender_sensitive_testimony | standard | negative | application_standard | precedent_pattern | retrieve_only | refute | 성폭력 피해자 진술의 신빙성을 판단할 때 성인지 감수성을 잃지 않아야 하며, 피해자에게 특정한 피해자다움을 요구하거나 그와 다른 반응만으로 진술을 함부로 배척해서는 안 된다. |
| art297_sec4_1.gender_sensitive_limit | standard | negative | application_standard | precedent_pattern | retrieve_only | refute | 성인지적 관점을 유지하더라도 성범죄 피해자 진술의 합리성·타당성 및 객관적 정황 등에 비추어 증명력을 인정할 수 없는 경우는 있을 수 있다. |

> comment:

### art297_sec4_2

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art297_sec4_2.rape_and_penetration | definition | positive | narrative | abstract_rule | static | none | 강간은 폭행·협박으로 상대방 반항을 불가능하거나 현저히 곤란하게 하여 간음하는 것이며, 간음은 다수설상 남성 성기의 여성 성기에 삽입 또는 양 성기의 결합을 말한다. |
| art297_sec4_2.non_vaginal_acts_exception | exception | exception | exception | abstract_rule | retrieve_assess | exclude | 구강성교나 항문성교 등은 강간죄의 간음에 해당하지 않으며, 이 경우 유사강간죄가 성립할 수 있다. |
| art297_sec4_2.violence_intercourse_causation | causal_link | positive | application_standard | abstract_rule | retrieve_assess | support | 강간죄에서는 폭행·협박과 간음 사이에 인과관계가 있어야 하며, 시간적 간격이 있어도 폭행·협박에 의해 간음이 이루어진 것으로 인정되면 성립한다. |

> comment:

### art297_sec4_3

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art297_sec4_3.attempt_commencement | element | positive | skeleton_meta | abstract_rule | static | none | 강간 수단으로 피해자 반항을 불가능하거나 현저히 곤란하게 할 정도의 폭행·협박이 개시되면 실행의 착수가 인정되며, 속옷을 벗기거나 간음에 나아갈 필요는 없다. |
| art297_sec4_3.attempt_commencement_context | standard | positive | stage | abstract_rule | relation_condition | none | 강간죄 실행의 착수에 필요한 폭행·협박 정도는 행위자의 언행·행동 및 당시 주변 정황을 종합하여 개별 사안마다 판단한다. |
| art297_sec4_3.completion | definition | positive | skeleton_meta | abstract_rule | static | none | 남성 성기가 여성 성기에 삽입되거나 결합되는 순간 강간죄는 기수가 되며, 완전한 삽입·결합, 성적 만족 또는 사정은 필요하지 않다. |
| art297_sec4_3.voluntary_abandonment | exception | exception | exception | abstract_rule | retrieve_assess | exclude | 행위자가 자의로 강간 범행의 실행을 중지한 경우 중지미수가 성립한다. |

자동분류 주의: element metadata is overridden by a stage/concurrence/static frame

> comment:

### art297_sec4_4

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art297_sec4_4.successive_co_perpetration_negative | standard | negative | participation | precedent_pattern | relation_condition | none | 선행자와의 공동가공 의사에 기한 기능적 행위지배를 후행자에게 인정할 수 없으면 승계적 공동정범은 성립할 수 없다는 대법원 취지가 소개되어 있다. |
| art297_sec4_4.successive_perpetrator_quasi_rape | standard | positive | participation | abstract_rule | relation_condition | none | 선행자의 행위를 이용하여 피해자를 간음한 후행자에게는 준강간죄가 성립할 여지가 있다. |

자동분류 주의: function depends on an unreviewed slot-default role

> comment:

### art297_sec5

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art297_sec5.valid_consent | exception | exception | exception | abstract_rule | retrieve_assess | exclude | 피해자 본인의 성관계 승낙은 구성요건 해당성을 조각하며, 친권자 등의 승낙은 강간죄 성립에 영향을 주지 않는다. |
| art297_sec5.withdrawn_consent | exception | negative | exception | abstract_rule | retrieve_assess | exclude | 피해자가 사전에 성관계를 승낙했더라도 동의를 번복하면 승낙이 있다고 볼 수 없다. |
| art297_sec5.consent_assessment | standard | positive | defeater | abstract_rule | retrieve_assess | block | 성관계 승낙 여부는 행위 경위와 태양, 피해자 연령, 범행 당시 정황 등을 종합해 성적 자유 또는 성적 자기결정권 침해 여부를 기준으로 구체적·개별적으로 판단한다. |
| art297_sec5.prior_communications_not_consent | standard | negative | defeater | abstract_rule | retrieve_assess | block | 피해자가 범행 무렵까지 피고인과 전화·문자 연락을 하고 호감을 보인 정황만으로 성관계 승낙 또는 묵인을 인정할 수는 없다. |

자동분류 주의: function depends on an unreviewed slot-default role

> comment:

### art297_sec6

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art297_sec6.intent | element | positive | canonical_element | abstract_rule | always_assess | support | 강간죄에는 폭행·협박으로 피해자를 강간한다는 인식과 의사가 필요하고, 미필적 고의로도 충분하다. |
| art297_sec6.mistake_of_consent | exception | negative | exception | abstract_rule | retrieve_assess | exclude | 피해자 승낙이 없음에도 승낙이 있다고 오인한 경우 강간죄의 고의가 조각된다. |

> comment:

### art297_sec7

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art297_sec7.continuous_acts_single_offense | standard | positive | concurrence | abstract_rule | relation_condition | none | 동일한 폭행·협박으로 피해자의 항거불가능 또는 현저한 곤란 상태가 계속되는 상황에서 수회 간음한 경우, 시간적·장소적 근접성과 범의의 단일성·계속성이 인정되면 포괄 일죄가 성립한다. |
| art297_sec7.new_violence_separate_offense | element | positive | canonical_element | abstract_rule | always_assess | support | 항거불능 상태가 종료된 후 다시 폭행·협박을 가하여 간음한 경우 별개의 강간죄가 성립한다. |
| art297_sec7.multiple_victims_multiple_offenses | element | positive | canonical_element | abstract_rule | always_assess | support | 피해자가 여러 명이면 동일한 장소에서 동일한 폭행·협박에 의한 경우에도 각 피해자에 따라 수개의 강간죄가 성립한다. |

자동분류 주의: function depends on an unreviewed slot-default role

> comment:

### art297_sec9

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art297_sec9.special_rape | exception | exception | exception | abstract_rule | retrieve_assess | exclude | 흉기 등 위험한 물건을 지니거나 2인 이상이 합동하여 강간한 경우에는 강간죄가 아니라 특수강간죄가 성립하여 가중처벌된다. |
| art297_sec9.means_violence_absorption | exception | negative | concurrence | abstract_rule | relation_condition | none | 강간죄 수단으로 행해진 폭행·협박은 강간죄에 흡수되어 별도로 폭행죄나 협박죄를 구성하지 않는다. |
| art297_sec9.robbery_rape | exception | exception | exception | abstract_rule | retrieve_assess | exclude | 강도죄를 범한 자가 그 기회에 동일 피해자를 강간하면 강도강간죄의 단순일죄가 성립한다. |
| art297_sec9.special_robbery_rape | standard | positive | concurrence | abstract_rule | relation_condition | none | 특수강도죄를 범한 자가 강간죄를 범한 때에는 성폭력범죄의 처벌 등에 관한 특례법상 특수강도강간죄가 단순일죄로 성립하여 가중처벌된다. |
| art297_sec9.theft_rape_concurrence | standard | positive | concurrence | abstract_rule | relation_condition | none | 절도죄를 범한 자가 피해자를 강간한 경우 절도죄와 강간죄는 실체적 경합범이 된다. |
| art297_sec9.special_theft_rape | standard | positive | concurrence | abstract_rule | relation_condition | none | 야간주거침입절도죄 또는 특수절도죄를 범한 자가 강간죄를 범한 경우 성폭력범죄의 처벌 등에 관한 특례법상 특수절도강간 등의 죄가 단순일죄로 성립하여 가중처벌된다. |
| art297_sec9.residence_intrusion_rape | standard | positive | concurrence | abstract_rule | relation_condition | none | 주거침입죄를 범한 자가 강간죄를 범한 때에는 성폭력범죄의 처벌 등에 관한 특례법상 주거침입강간죄가 단순일죄로 성립하여 가중처벌된다. |
| art297_sec9.rape_injury_death | standard | positive | concurrence | abstract_rule | relation_condition | none | 강간 범행 과정에서 피해자가 상해를 입으면 강간상해죄나 강간치상죄가, 피해자가 사망하면 강간살인죄나 강간치사죄가 성립한다. |
| art297_sec9.confinement_rape_attempted_case | standard | positive | concurrence | precedent_pattern | relation_condition | none | 피해자가 주행 중인 자동차에서 탈출할 수 없는 상태를 이용하여 약 50km 강제연행한 후 강간하려다 미수에 그친 사안에서, 협박이 감금죄와 강간미수죄의 실행착수에 동시에 해당하면 두 죄는 상상적 경합에 해당한다고 한 판시가 소개되어 있다. |
| art297_sec9.continued_confinement_after_rape | standard | positive | concurrence | abstract_rule | relation_condition | none | 감금행위가 강간의 수단에 그치지 않고 강간 범행이 끝난 뒤에도 계속된 경우 감금죄와 강간죄는 실체적 경합범이 성립한다. |
| art297_sec9.separate_confinement_rape_violence | standard | positive | concurrence | abstract_rule | relation_condition | none | 감금 중 강간의 고의가 생겨 별도의 폭행·협박을 통해 강간한 경우 감금죄와 강간죄는 실체적 경합범이 성립한다. |
| art297_sec9.abduction_for_marriage_rape | standard | positive | concurrence | abstract_rule | relation_condition | none | 결혼을 목적으로 여자를 약취하여 강간한 경우 강간죄와 결혼을 위한 약취죄는 실체적 경합범이 성립한다. |
| art297_sec9.nonprosecution_not_false_report_proof | standard | negative | concurrence | precedent_pattern | relation_condition | none | 성폭행 등 피해 신고에 관하여 증거불충분 등의 불기소처분이나 무죄판결이 내려졌다는 사정만으로 신고내용을 허위라고 단정하여 무고의 적극적 근거로 삼아서는 안 된다. |

자동분류 주의: function depends on an unreviewed slot-default role; precedent-pattern form was detected linguistically

> comment:

## art298

### art298

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art298.offense_conduct | definition | positive | narrative | abstract_rule | static | none | 강제추행죄는 폭행 또는 협박으로 사람에 대하여 추행을 함으로써 성립하는 범죄이다. |
| art298.subject.unrestricted | element | positive | skeleton_meta | abstract_rule | static | none | 강제추행죄의 주체에는 제한이 없고 남성과 여성 모두 주체가 될 수 있다. |
| art298.indirect_perpetration.victim_as_instrument | standard | positive | application_standard | abstract_rule | retrieve_assess | support | 피해자를 도구로 삼아 피해자의 신체를 이용하여 추행행위를 한 경우에도 강제추행죄의 간접정범에 해당할 수 있다. |
| art298.object.person | definition | positive | skeleton_meta | abstract_rule | static | none | 강제추행죄의 객체는 사람이며, 성별·성년·미성년·기혼 여부를 불문한다. |
| art298.spousal_victim.precedent_position | standard | positive | application_standard | precedent_pattern | retrieve_only | support | 해설은 판례가 부부 사이의 강제추행죄 성립을 인정하고 있다고 보고한다. |

자동분류 주의: element metadata is overridden by a stage/concurrence/static frame

> comment:

### art298_sec3_1

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art298_sec3_1.force_threat_totality_assessment | standard | positive | application_standard | abstract_rule | retrieve_assess | support | 어떤 행위가 강제추행죄의 폭행 또는 협박에 해당하는지는 목적과 의도, 행위태양·내용, 경위·당시 정황, 당사자 관계 및 상대방 고통 등을 종합하여 판단한다. |
| art298_sec3_1.surprise_molestation_physical_force | standard | positive | application_standard | precedent_pattern | retrieve_only | support | 폭행행위 자체가 곧바로 추행행위에 해당하는 기습추행에서는 상대방 의사에 반하는 유형력 행사가 있으면 힘의 대소강약을 불문하여 폭행이 인정된다는 판례 입장이 소개되어 있다. |

> comment:

### art298_sec3_2

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art298_sec3_2.indecent_act_definition | definition | positive | narrative | abstract_rule | static | none | 추행은 객관적으로 일반인에게 성적 수치심 또는 혐오감을 일으키고 선량한 성적 도덕관념에 반하여 피해자의 성적 자유를 침해하는 행위이다. |
| art298_sec3_2.indecent_act_comprehensive_assessment | standard | positive | application_standard | abstract_rule | retrieve_assess | support | 추행 해당 여부는 피해자의 의사·성별·연령, 행위자와 피해자의 관계, 경위, 구체적 행위태양, 객관적 상황 및 시대의 성적 도덕관념 등을 종합하여 신중히 판단한다. |
| art298_sec3_2.victim_actual_awareness_not_required | standard | positive | skeleton_meta | abstract_rule | static | none | 추행행위는 행위자가 대상자를 상대로 객관적으로 성적 수치심 또는 혐오감을 일으킬 만하고 선량한 성적 도덕관념에 반하는 행위를 실행하면 충분하며, 대상자가 실제로 이를 느끼거나 행위사실을 인식할 필요는 없다. |
| art298_sec3_2.recent_precedent_nonsexual_sensitive_contact | standard | positive | application_standard | precedent_pattern | retrieve_only | support | 최근 판례는 추행을 성적으로 민감한 부위 접촉에 한정하지 않고, 성희롱적 언사와의 결합, 피해자의 거부의사 표시, 위력관계 등을 고려하여 신체 부위와 관계없이 성적 자기결정권 침해 여부를 판단하는 경향이 소개되어 있다. |
| art298_sec3_2.toddler_hand_contact_not_molestation | standard | negative | application_standard | precedent_pattern | retrieve_only | refute | 2세 피해자에게 사탕을 건네며 악수하자고 하여 양손으로 피해자의 손을 잡고, 어머니가 손을 빼내는 과정에서 피고인의 손이 옷 위로 피해자 몸에 잠시 닿은 경우에는 추행을 인정하지 않았다는 판례 사례가 소개되어 있다. |
| art298_sec3_2.no_contact_equivalent_infringement | standard | positive | application_standard | precedent_pattern | retrieve_only | support | 신체 접촉이 없더라도 성적 수치심·혐오감 또는 성적 자기결정권 침해가 신체 접촉이 있는 경우와 동등한 정도라고 평가되면 강제추행죄 성립을 인정할 수 있다. |
| art298_sec3_2.no_contact_assessment_factors | standard | positive | application_standard | precedent_pattern | retrieve_only | support | 신체 접촉 없는 행위가 강제추행에 해당하는지는 피해자의 의사·성별·연령, 당사자 관계, 경위, 구체적 행위태양 및 객관적 상황 등을 종합 고려하여 판단한다. |
| art298_sec3_2.no_contact_elevator_threat_masturbation | standard | positive | application_standard | precedent_pattern | retrieve_only | support | 폐쇄된 엘리베이터에서 피해자들을 칼로 위협하여 실력적으로 지배한 뒤 자위행위 모습을 보여주고 피하거나 외면할 수 없게 한 경우, 신체 접촉 없이도 강제추행이 인정된 사례가 소개되어 있다. |
| art298_sec3_2.no_contact_minor_elevator_exposure | standard | positive | application_standard | precedent_pattern | retrieve_only | support | 아파트 엘리베이터에서 13세 미만 피해자에게 성기를 꺼내 잡고 움직이며 피해자 쪽으로 다가간 경우, 신체 접촉 없이도 강제추행이 인정된 사례가 소개되어 있다. |
| art298_sec3_2.no_contact_urination_toward_victim | standard | positive | application_standard | precedent_pattern | retrieve_only | support | 피해자 뒤로 다가가 성기를 드러낸 뒤 피해자를 향한 자세에서 피해자의 머리카락 및 옷 위에 소변을 본 경우, 신체 접촉 없이도 강제추행이 인정된 사례가 소개되어 있다. |
| art298_sec3_2.no_contact_kitchen_gesture_not_molestation | standard | negative | application_standard | precedent_pattern | retrieve_only | refute | 중국음식점 주방장이 주방에서 여성 피해자에게 성기 모양을 손으로 만들고 반바지를 벌리며 보여주겠다고 말한 경우에는 신체 접촉 없는 강제추행이 인정되지 않은 사례가 소개되어 있다. |
| art298_sec3_2.indirect_perpetration | definition | positive | narrative | precedent_rule | static | none | 강제추행죄는 정범 자신이 직접 범죄를 실행해야만 성립하는 자수범이 아니므로, 처벌되지 않는 타인을 도구로 이용하는 간접정범 형태로도 범할 수 있다. |
| art298_sec3_2.indirect_perpetration_coerced_self_sexual_acts | standard | positive | application_standard | precedent_pattern | retrieve_only | support | 피고인이 협박으로 겁먹은 피해자들에게 나체 또는 속옷 상태에서 스스로 촬영하거나 성기에 이물질 삽입 또는 자위를 하게 한 경우 강제추행죄의 간접정범에 해당할 수 있다. |

자동분류 주의: precedent-pattern form was detected linguistically

> comment:

### art298_sec3_3

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art298_sec3_3.attempt_commencement | causal_link | positive | stage | abstract_rule | relation_condition | none | 강제추행의 실행 착수는 강제추행 수단인 폭행·협박이 개시된 때에, 기습추행의 경우에는 상대방 의사에 반하는 유형력 행사가 있는 때에 인정된다. |
| art298_sec3_3.surprise_assault_attempt_hugging | standard | positive | stage | precedent_pattern | relation_condition | none | 피고인의 팔이 피해자의 몸에 닿지 않았더라도 양팔을 높이 들어 갑자기 뒤에서 껴안으려는 행위는 피해자의 의사에 반하는 유형력 행사로서 폭행행위에 해당하고, 그때 기습추행에 관한 실행의 착수가 있어 강제추행미수죄에 해당한다는 사례가 소개되어 있다. |

자동분류 주의: function depends on an unreviewed slot-default role

> comment:

### art298_sec4

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art298_sec4.intent_awareness_conditional | element | positive | canonical_element | abstract_rule | always_assess | support | 강제추행죄의 고의는 폭행 또는 협박으로 사람을 추행한다는 인식이며, 미필적 고의로도 충분하다. |
| art298_sec4.intent_inference | standard | positive | application_standard | abstract_rule | retrieve_assess | support | 고의를 부인하는 경우 피고인의 능력·경력, 동기와 경위, 피해자와의 관계, 행위태양과 전후 정황 및 평소 행동양태 등 간접사실을 종합하여 판단하고, 고의 징표와 어긋나는 사실의 의문점이 해소되어야 한다. |
| art298_sec4.disability_intent_assessment | standard | negative | application_standard | abstract_rule | retrieve_assess | refute | 피고인이 자폐성 장애 또는 지적장애인인 경우 비장애인 관점에서 언행이 이례적·비합리적이라는 이유만으로 고의를 함부로 추단해서는 안 되며, 장애 정도와 지적·판단능력 및 행동양식을 구체적으로 심리하여 고의를 판단해야 한다. |

> comment:

### art298_sec5

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art298_sec5.revoked_consent | exception | exception | exception | abstract_rule | retrieve_assess | exclude | 피해자가 사전에 신체접촉 등을 승낙하였더라도 동의를 번복할 수 있으며, 승낙을 번복한 경우에는 승낙이 있다고 볼 수 없다. |
| art298_sec5.consent_after_violence_attempt | standard | positive | defeater | abstract_rule | retrieve_assess | block | 강제추행을 위한 폭행·협박 착수 후 피해자가 자유롭고 진정한 의사로 동의한 경우 강제추행미수죄가 성립할 수 있으나, 동의가 폭행·협박으로 강요된 것인지 신중히 판단해야 한다. |

자동분류 주의: function depends on an unreviewed slot-default role

> comment:

### art298_sec6

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art298_sec6.multiple_acts_comprehensive_offense | standard | positive | concurrence | abstract_rule | relation_condition | none | 원칙적으로 각 추행행위마다 하나의 범죄가 성립하지만, 각 행위가 시간적·장소적으로 가깝고 범의의 단일성과 계속성이 인정되면 포괄일죄가 성립한다. |
| art298_sec6.multiple_victims_multiple_offenses | element | positive | canonical_element | abstract_rule | always_assess | support | 피해자가 여러 명이면 동일 장소에서 동일한 폭행·협박에 의한 경우라도 피해자별로 수개의 죄가 성립한다. |

> comment:

### art298_sec8

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art298_sec8.special_forcible_indecency | exception | exception | exception | abstract_rule | retrieve_assess | exclude | 흉기 기타 위험한 물건을 지니거나 2인 이상이 합동하여 강제추행한 경우에는 강제추행죄가 아니라 특수강제추행죄가 성립하여 가중처벌된다. |
| art298_sec8.forcible_indecency_followed_by_rape | exception | exception | exception | abstract_rule | retrieve_assess | exclude | 동일 피해자에 대해 강제로 추행한 뒤 이어 강간한 경우에는 포괄하여 강간죄만 성립한다. |
| art298_sec8.forced_undressing_camera_concurrence | standard | positive | concurrence | abstract_rule | relation_condition | none | 피해자를 강제로 옷 벗겨 나체가 되게 한 다음 카메라로 촬영한 행위에는 강제추행죄와 카메라 등을 이용한 촬영죄의 실체적 경합범이 성립한다. |

> comment:

## art301

### art301_sec2

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art301_sec2.subject_predicate_offenses | element | positive | stage | abstract_rule | relation_condition | none | 본죄의 주체는 열거된 강간·유사강간·강제추행·준강간 등 범죄를 범한 자 또는 그 미수에 그친 자이다. |
| art301_sec2.attempt_injury | standard | positive | stage | abstract_rule | relation_condition | none | 강간 등이 미수에 그친 경우에도 그 수단이 된 폭행으로 피해자가 상해를 입으면 본죄가 성립하며, 미수가 자의중지인지 실행 미완료인지는 가리지 않는다. |
| art301_sec2.object_victim | definition | positive | narrative | abstract_rule | static | none | 본죄의 객체인 사람은 강간 등의 피해자를 의미한다. |

자동분류 주의: element metadata is overridden by a stage/concurrence/static frame

> comment:

### art301_sec3

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art301_sec3.injury_occasion_causation | causal_link | positive | application_standard | abstract_rule | retrieve_assess | support | 본죄 성립을 위해서는 강간 등의 죄 외에, 강간 등의 기회 또는 시간적·장소적으로 밀접하게 관련된 행위로 발생한 상해 결과가 필요하다. |
| art301_sec3.injury_occasion_categories | causal_link | positive | application_standard | abstract_rule | retrieve_assess | support | 강간 등의 기회에 발생한 상해에는 강간 등 자체에 기인한 경우, 그 수단인 폭행으로 발생한 경우 및 강간 등에 수반하여 발생한 경우가 포함된다. |
| art301_sec3.unrelated_injury_exception | exception | negative | exception | abstract_rule | retrieve_assess | exclude | 강간 등의 기회가 아닌 다른 사정으로 상해 결과가 발생한 경우 본죄는 성립하지 않는다. |
| art301_sec3.continuing_criminal_stage | standard | positive | application_standard | abstract_rule | retrieve_assess | support | 상해 결과는 강간 등 실행 중, 실행 직후 또는 실행범의 포기 직후로서 사회통념상 범죄행위가 완료되지 않은 단계의 행위로 발생하여야 하며, 강간 등이 기수에 이르기 전 원인행위가 반드시 있어야 하는 것은 아니다. |
| art301_sec3.post_rape_injury_connection | standard | positive | application_standard | abstract_rule | retrieve_assess | support | 강간 후에도 피해자의 심리적 저항불능 상태가 해소되지 않은 상태에서 강간범의 상해행위가 있으면, 시간적·공간적 간격이 있더라도 강간상해죄가 성립할 수 있다. |
| art301_sec3.result_after_completion | causal_link | positive | application_standard | abstract_rule | retrieve_assess | support | 강간 등이 완료되기 전에 고의 또는 과실에 의한 상해 원인행위가 있으면, 상해 결과가 강간 등의 완료 후 발생하여도 본죄가 성립한다. |

> comment:

### art301_sec4_2

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art301_sec4_2.minor_injury_exclusion | standard | negative | skeleton_meta | abstract_rule | static | none | 상처가 극히 경미하여 치료할 필요가 없고, 치료 없이도 일상생활에 아무런 지장이 없으며, 시간이 지나 자연적으로 치유될 수 있는 정도이면 상해에 해당하지 않는다. |
| art301_sec4_2.injury_diagnosis_evidence | standard | positive | application_standard | precedent_pattern | retrieve_only | support | 상해진단서는 특별한 사정이 없으면 피해자 진술과 함께 상해 사실의 유력한 증거가 되며, 합리적 근거 없이 그 증명력을 함부로 배척할 수 없다. 다만 객관성·신빙성을 의심할 사정이 있으면 그 증명력을 매우 신중히 판단해야 한다는 대법원 판시가 소개되어 있다. |
| art301_sec4_2.delayed_diagnosis_case | standard | negative | application_standard | precedent_pattern | retrieve_only | refute | 대법원이 강제추행치상죄를 유죄로 판단한 원심판결에 상해에 관한 법리오해가 있다고 보아 이를 파기·환송한 사례가 소개되어 있다. |

> comment:

### art301_sec4_4

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art301_sec4_4.injury_recognition_factors | standard | positive | application_standard | abstract_rule | retrieve_assess | support | 상해 인정 여부에서는 상처가 일상생활에서 흔히 발생할 수 있는지, 별다른 치료 없이 단기간 내 자연치유되는지, 그리고 피해자가 피해 후 곧바로 상처를 자각하여 의사에게 호소했는지를 고려한다. |
| art301_sec4_4.minor_broader_injury | standard | positive | application_standard | precedent_pattern | retrieve_only | support | 판례는 피해자가 미성년자인 경우 상해의 범위를 다소 넓게 인정하는 경향이 있다. |

> comment:

### art301_sec4_5

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art301_sec4_5.functional_impairment_injury | definition | positive | narrative | abstract_rule | static | none | 외부 상처가 없더라도 육체적·정신적 생리기능 훼손, 예컨대 보행불능·수면장애·식욕감퇴 등의 기능장애가 발생하면 상해로 인정될 수 있다. |
| art301_sec4_5.ptsd_as_injury | definition | positive | narrative | abstract_rule | static | none | 심각한 외상 후 나타나는 외상 후 스트레스 장애도 상해로 인정될 수 있다. |
| art301_sec4_5.drug_induced_consciousness_impairment | standard | positive | application_standard | abstract_rule | retrieve_assess | support | 수면유도 약물로 피해자가 일시적 수면 또는 의식불명 상태가 되고 건강상태가 불량하게 변경되거나 생활기능 장애가 초래되면, 외부 상처가 없거나 자연 회복하더라도 상해에 해당한다. |
| art301_sec4_5.ptsd_causation_assessment | standard | positive | application_standard | abstract_rule | retrieve_assess | support | 성범죄 후 외상 후 스트레스 장애의 상해 여부 및 인과관계는 피해자가 필연적으로 겪는 정도의 증상인지, 의사 진단·소견, 범행 내용, 구체적 증상, 치료 내용과 경과, 기존 정신과 치료 전력 등을 고려하여 판단한다. |

> comment:

### art301_sec4_7

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art301_sec4_7.pubic_hair_cutting_not_injury | standard | negative | stage | abstract_rule | relation_condition | none | 음모 모근을 남기고 모간 일부만 잘라 외관 변형이 생긴 경우, 수치심이나 폭행 해당 가능성과 별개로 건강상태의 병리적 불량 변경이나 생활기능 장애가 없으므로 강제추행치상죄의 상해에 해당하지 않는다. |
| art301_sec4_7.pubic_hair_pulling_injury | standard | positive | stage | abstract_rule | relation_condition | none | 음모를 잡아당겨 음부 부근에 염증을 발생시키거나 음모를 모근부터 뽑는 경우 상해에 해당한다고 볼 수 있다. |

> comment:

### art301_sec5_1

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art301_sec5_1.intentional_rape_injury | element | positive | canonical_element | abstract_rule | always_assess | support | 강간 등 상해죄는 강간 등 범행과 상해에 대한 고의가 요구되는 고의범이고, 미필적 고의로도 족하다. |

> comment:

### art301_sec5_2

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art301_sec5_2.rape_injury_result_aggravation | element | positive | skeleton_meta | abstract_rule | static | none | 강간 등 치상죄는 강간 등 범행의 고의는 필요하지만 상해 결과에 대한 고의는 요구되지 않는 결과적 가중범이다. |
| art301_sec5_2.rape_injury_causation_foreseeability | causal_link | positive | application_standard | abstract_rule | retrieve_assess | support | 강간 등 치상죄는 강간 등 행위와 상해 결과 사이 인과관계 및 결과발생에 대한 예견가능성을 요한다. |
| art301_sec5_2.injury_foreseeability_assessment | standard | positive | application_standard | abstract_rule | retrieve_assess | support | 상해 결과의 예견가능성은 폭행·협박 정도, 피해자의 나이와 대응상태 등 당시 구체적 상황을 종합하여 엄격히 판단하며, 일반인이 예견하기 어려운 이례적 결과는 인정하기 어렵다. |
| art301_sec5_2.fleeing_traffic_injury | causal_link | positive | application_standard | abstract_rule | retrieve_assess | support | 피해자가 강간 등 범행을 피해 도망가다가 자동차에 치여 상해를 입은 경우 인과관계와 예견가능성이 충분히 인정되어 강간 등 치상죄가 성립한다. |

자동분류 주의: element metadata is overridden by a stage/concurrence/static frame

> comment:

### art301_sec6

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art301_sec6.pre_execution_withdrawal | exception | exception | exception | abstract_rule | retrieve_assess | exclude | 강간 등을 공모한 공범이 다른 공범자의 실행착수 전, 즉 폭행·협박 전 공범관계에서 이탈한 경우 다른 공범자의 행위에 대해 공동정범 책임을 지지 않는다. |
| art301_sec6.intentional_injury_conspirator_intent | element | negative | canonical_element | abstract_rule | always_assess | refute | 고의범인 강간 등 상해죄에서 공모자에게도 상해에 대한 고의가 필요하므로, 그 고의를 인정하기 어려우면 공동정범으로 처벌할 수 없다. |

> comment:

### art301_sec7

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art301_sec7.no_general_attempt_punishment | exception | negative | exception | abstract_rule | retrieve_assess | exclude | 형법상 강간 등 상해·치상죄에는 미수범 처벌규정이 없다. |

> comment:

### art301

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art301.post_rape_new_intent_separate_concurrence | exception | negative | concurrence | abstract_rule | relation_condition | none | 강간 등 행위가 종료된 뒤 새로 상해 고의가 생겨 상해한 경우에는 강간 등 죄와 상해죄의 실체적 경합범이 성립한다. |
| art301.assault_before_forced_indecency_no_result_injury | exception | negative | exception | abstract_rule | retrieve_assess | exclude | 폭행으로 상해를 입힌 다음 강제추행을 한 경우에는 강제추행치상죄가 성립하지 않는다. |
| art301.death_absorbs_injury | exception | negative | concurrence | abstract_rule | relation_condition | none | 강간으로 피해자에게 상해를 입힌 후 그로 인해 사망한 경우 상해는 사망에 흡수되어 강간치사죄만 성립한다. |
| art301.no_abandonment_offense_after_rape_injury | exception | negative | exception | abstract_rule | retrieve_assess | exclude | 강간치상죄를 범한 자가 실신한 피해자를 구호하지 않고 방치했더라도 포괄적으로 강간치상죄만 구성하고 별도 유기죄는 구성하지 않는다. |

> comment:

## art319

### art319_sec1_3

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art319_sec1_3.protected_interest | standard | positive | narrative | precedent_pattern | static | none | 판례는 주거침입죄의 보호법익을 사적 생활관계에서 사실상 누리는 주거의 평온으로 보고, 법적 점유권한이 없어도 사실상 권한 있는 거주자의 사실적 지배·관리관계가 평온하게 유지되는 상태를 말한다고 한다. |
| art319_sec1_3.entry_assessment | standard | positive | application_standard | precedent_pattern | retrieve_only | support | 판례상 침입은 거주자의 사실상 평온상태를 해치는 행위태양으로 주거에 들어가는 것을 뜻하며, 객관적·외형적으로 드러난 행위태양을 기준으로 장소의 형태·용도·성질, 출입 통제·관리 방식과 상태, 출입 경위와 방법을 종합 고려하여 판단한다. |
| art319_sec1_3.right_holder_entry_unlawful_occupancy | standard | positive | application_standard | precedent_pattern | retrieve_only | support | 적법하게 점유 또는 관리를 시작한 자가 권원을 상실하여 사법상 불법점유자가 되었더라도, 권리자가 정당한 절차 없이 그 주거나 건조물에 들어가면 주거침입죄 또는 건조물침입죄가 성립한다는 판례 입장이 소개되어 있다. |
| art319_sec1_3.co_resident_consent_ordinary_entry | standard | negative | application_standard | precedent_pattern | retrieve_only | refute | 공동거주자 중 현재 거주자의 현실적 승낙을 받고 통상적 출입방법으로 들어간 경우, 부재중 다른 거주자의 의사에 반한다고 추정되더라도 사실상 주거의 평온을 깼다고 볼 수 없다는 판례 입장이 소개되어 있다. |
| art319_sec1_3.restaurant_entry_with_consent | standard | negative | application_standard | precedent_pattern | retrieve_only | refute | 일반인의 출입이 허용된 음식점에 영업주의 승낙과 통상적 방법으로 들어간 경우, 범죄 목적이나 실제 목적을 알았다면 승낙하지 않았을 사정만으로는 특별한 사정이 없는 한 침입행위가 아니다. |
| art319_sec1_3.partial_body_completed_offense | standard | positive | stage | precedent_pattern | relation_condition | none | 행위자가 출입할 생각 없이 신체 일부만 타인의 주거 안에 넣었더라도 사실상 주거의 평온을 해할 수 있는 정도에 이르면 주거침입죄는 기수에 이른다. |

> comment:

### art319_sec1_4

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art319_sec1_4.partial_body_attempt | standard | negative | stage | precedent_pattern | relation_condition | none | 신체의 극히 일부가 주거 안으로 들어갔더라도 사실상 주거의 평온을 해하는 정도에 이르지 않으면 주거침입죄 미수에 그친다는 판례가 소개되어 있다. |

> comment:

### art319_sec2_1

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art319_sec2_1.unlawful_construction_site_occupancy | standard | positive | application_standard | precedent_pattern | retrieve_only | support | 피해자 측이 불법적으로 공사현장을 점거하였더라도 경찰 신고·허가에 따라 경비원을 상주시켜 약 65일간 점유·관리한 상황에서, 정당하고 적법한 절차 없이 공사현장과 건조물에 침입하면 건조물침입죄가 성립한다는 판례가 소개되어 있다. |
| art319_sec2_1.enforcement_dissipated_peace | standard | negative | application_standard | precedent_pattern | retrieve_only | refute | 매수인이 매매계약 해제와 중도금반환 승소판결에 기초하여 강제집행에 착수한 뒤 매도인이 잠긴 출입문을 열고 들어간 사안에서는, 매수인이 권리를 포기한 것으로 알았고 보호할 주거 평온상태도 소멸하였다고 볼 수 있어 주거침입죄가 성립하지 않는다는 판례가 소개되어 있다. |
| art319_sec2_1.enclosed_land_requirements | element | positive | application_standard | precedent_pattern | retrieve_only | support | 위요지로 인정되려면 가옥 인접 주변 토지이고, 문·담 등 외부와의 경계가 설치되어 있으며, 가옥 이용에 제공되고 외부인이 함부로 출입할 수 없다는 점이 객관적으로 명확해야 한다. |
| art319_sec2_1.uncontrolled_adjacent_land | standard | negative | application_standard | precedent_pattern | retrieve_only | refute | 주거 이용에 기여하는 인접 부속토지라도 인적·물적 설비에 의한 구획이나 통제가 없어 통상 보행으로 쉽게 경계를 넘을 수 있으면, 외부인 출입 제한이 객관적으로 명확하지 않아 위요지에 해당하지 어렵다. |
| art319_sec2_1.common_area_entry_assessment | standard | positive | application_standard | abstract_rule | retrieve_assess | support | 외부인의 공동주택 공용 부분 출입이 주거침입인지 여부는 공용 부분의 공중 출입 허용 여부, 전용부분에의 필수적 부속성, 출입 통제·관리 예정과 실제 관리, 출입 목적·경위·태양·시간을 종합하여 사실상 주거 평온 침해 관점에서 객관적·외형적으로 판단한다. |
| art319_sec2_1.former_cohabitant_loss_of_control | standard | positive | application_standard | abstract_rule | retrieve_assess | support | 공동생활하던 주거에서 이탈하거나 주거에 대한 사실상의 지배·관리를 상실한 자에 대해서는 특별한 사정이 있으면 그 주거가 타인의 주거가 되어 주거침입죄가 성립할 수 있다. |
| art319_sec2_1.runaway_child_parent_home | standard | positive | application_standard | precedent_pattern | retrieve_only | support | 가출한 자녀가 야간에 절도 목적으로 종래 함께 살던 부모 집에 침입한 경우 주거침입이 인정되어 야간주거침입절도죄가 성립한다. |
| art319_sec2_1.separated_husband_owned_home | standard | positive | application_standard | precedent_pattern | retrieve_only | support | 별거 중인 남편이 처의 부정행위 현장을 촬영하려고 처가 거주하는 자기 소유 가옥에 침입한 경우에도 주거침입죄가 성립한다. |
| art319_sec2_1.deceased_victim_possession | standard | negative | application_standard | precedent_pattern | retrieve_only | refute | 피고인이 피해자의 주거에 침입할 당시 피해자가 이미 사망했고 정확한 사망시기도 밝혀지지 않은 사안에서는 사자의 점유를 인정할 수 없어 야간주거침입절도 후 준강제추행 미수는 무죄로 판단한 판례가 소개되어 있다. |
| art319_sec2_1.temporary_dwelling | definition | positive | narrative | abstract_rule | static | none | 일시적으로 기거하고 침식에 사용하는 장소도 주거가 될 수 있으며, 낮에만 기거하는 곳, 휴가 기간 중 설치한 텐트, 별장 및 주거용 차량이 이에 해당할 수 있다. |
| art319_sec2_1.seasonally_unused_villa | exception | exception | exception | abstract_rule | retrieve_assess | exclude | 별장은 계절적으로 전혀 사용하지 않는 기간에는 주거가 아니라 건조물에 해당한다. |
| art319_sec2_1.non_dwelling_occupied_room | definition | negative | narrative | abstract_rule | static | none | 빌딩사무실·실험실·점포와 호텔·여관의 객실처럼 하룻밤 숙박이나 단시간 휴식을 위해 사용하는 장소는 주거가 아니라 점유하는 방실에 해당한다. |

자동분류 주의: element metadata is overridden by a stage/concurrence/static frame

> comment:

### art319_sec2_2

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art319_sec2_2.managed_building_control | definition | positive | narrative | abstract_rule | static | none | 관리하는 건조물로 인정되려면 타인의 함부로운 침입을 방지할 만한 인적·물적 설비를 갖추어야 하며, 사무적으로만 관리되는 건조물은 건조물침입죄의 객체가 될 수 없다. |
| art319_sec2_2.management_notice_insufficient | element | negative | canonical_element | abstract_rule | always_assess | refute | 단순히 출입금지 표지를 해둔 것만으로는 관리라고 할 수 없다. |
| art319_sec2_2.public_place_management | standard | positive | application_standard | abstract_rule | retrieve_assess | support | 관공서의 출입구·계단, 역 구내, 백화점 등 공중에게 개방되어 사실상 출입이 자유로운 장소라도 정상적 용무가 있는 사람의 출입 편의를 위한 개방에 그치는 경우 관리되지 않는 장소라고 할 수 없다. |
| art319_sec2_2.unmanaged_empty_house | exception | exception | exception | abstract_rule | retrieve_assess | exclude | 다른 사람이 살지 않고 관리하지 않는 집 또는 그 울타리 안이나 건조물·배·자동차 안에 정당한 이유 없이 들어간 행위는 주거침입죄가 아니라 경범죄처벌법 제3조 제1항 제1호 위반죄에 해당한다. |
| art319_sec2_2.joint_occupier_entry | exception | exception | exception | abstract_rule | retrieve_assess | exclude | 공동관리 중인 건조물에 공동점유자 중 1인이 임의로 출입하였다고 하여 건조물침입죄는 성립하지 않는다. |
| art319_sec2_2.building_structure | definition | positive | narrative | abstract_rule | static | none | 건조물은 주거를 제외한 일체의 건물과 그 부속 구조물 및 위요지를 의미하며, 일반적으로 주위벽 또는 기둥과 지붕 또는 천정으로 구성되어 사람이 기거하거나 출입할 수 있는 구조물이다. |
| art319_sec2_2.incomplete_construction_not_building | exception | exception | exception | abstract_rule | retrieve_assess | exclude | 벽·기둥·지붕·천정 등을 완전히 갖추지 못한 건축 중인 건축물은 건조물에 해당하지 않는다. |
| art319_sec2_2.enclosed_land_requirements | standard | positive | application_standard | abstract_rule | retrieve_assess | support | 건조물의 위요지가 되기 위해서는 건조물에 인접한 주변 토지에 관리자가 외부와의 경계로 문과 담 등을 설치하여 그 토지가 건조물 이용을 위하여 제공되었다는 점이 명확히 드러나야 한다. |
| art319_sec2_2.construction_site_not_enclosed_land | exception | exception | exception | precedent_pattern | retrieve_only | exclude | 공사현장에 현장사무실이나 경비실 외 별도의 건조물이 없고 공사현장이 그 시설들의 이용을 위하여 제공된 토지라고 보기 어려운 경우, 공사현장 출입은 건조물침입죄가 성립할 수 없다는 판례가 소개되어 있다. |
| art319_sec2_2.vessel_scale | definition | negative | narrative | abstract_rule | static | none | 선박은 수상교통의 수단으로 사용되는 제조물을 의미하고, 적어도 사람의 주거에 사용될 수 있는 정도의 규모여야 한다는 통설이 소개되어 있으며, 놀이용 소형 모터보트와 카누는 이에 해당하지 않는다고 본다. |
| art319_sec2_2.aircraft_and_vehicle_exclusion | definition | negative | narrative | abstract_rule | static | none | 항공기는 사람의 조종에 의하여 공중을 운행하는 기기 중 적어도 사람의 주거에 사용될 수 있는 정도의 규모여야 하며, 자동차·기차·지하철·전동차는 본죄의 객체에 해당하지 않는다. |

> comment:

### art319_sec2_3

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art319_sec2_3.occupied_room_building_partition | definition | positive | narrative | abstract_rule | static | none | 점유하는 방실은 건조물 내에서 사실상 지배·관리되는 일정한 구획을 말한다. |

> comment:

### art319_sec3_1

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art319_sec3_1.intrusion_objective_peace | definition | positive | narrative | precedent_rule | static | none | 침입은 거주자가 주거에서 누리는 사실상의 평온상태를 해치는 행위태양으로 주거에 들어가는 것을 의미하며, 침입 여부는 출입 당시 객관적·외형적으로 드러난 행위태양을 기준으로 판단하는 것이 원칙이다. |
| art319_sec3_1.intrusion_subjective_opposition_insufficient | standard | negative | application_standard | precedent_pattern | retrieve_only | refute | 단순히 주거 등의 출입이 거주자 등의 의사에 반한다는 주관적 사정만으로는 바로 침입에 해당하지 않는다. |
| art319_sec3_1.intrusion_factors | standard | positive | application_standard | precedent_pattern | retrieve_only | support | 침입 여부는 장소의 형태·용도·성질, 외부인 출입 통제·관리 방식과 상태, 출입 경위와 태양 등을 종합하여 출입 당시 객관적·외형적으로 사실상 평온상태가 침해되었는지 평가하며, 거주자 등의 의사에 반하는지는 그 평가 요소 중 하나이다. |
| art319_sec3_1.consenting_current_co_resident | standard | negative | application_standard | precedent_pattern | retrieve_only | refute | 외부인이 주거 내에 현재하는 공동거주자의 현실적 승낙을 받아 통상적 출입방법으로 들어간 경우에는 특별한 사정이 없는 한, 부재중 다른 거주자의 의사에 반하는 것으로 추정되더라도 침입에 해당하지 않는다. |
| art319_sec3_1.restaurant_consented_entry | standard | negative | application_standard | precedent_pattern | retrieve_only | refute | 일반인 출입이 허용된 음식점에 영업주 승낙을 받아 통상적 방법으로 들어간 경우, 범죄 목적이 있었거나 영업주가 실제 목적을 알았다면 승낙하지 않았을 사정만으로는 특별한 사정이 없는 한 침입행위가 아니다. |
| art319_sec3_1.bodily_entry_required | element | negative | canonical_element | abstract_rule | always_assess | refute | 침입은 신체적 침입을 의미하므로 행위자의 신체가 주거에 들어가지 않으면 침입이 아니다. |
| art319_sec3_1.partial_entry_intent | element | positive | application_standard | precedent_pattern | retrieve_only | support | 주거침입의 고의는 신체 일부라도 타인의 주거 안으로 들어간다는 인식으로 족하다. |
| art319_sec3_1.abnormal_or_forced_entry | standard | positive | application_standard | abstract_rule | retrieve_assess | support | 출입문을 통한 정상 출입이 아니거나 출입 방법이 비정상적인 경우, 또는 개방 장소에서 시설 일부를 파괴하거나 흉기를 소지하거나 다수의 위력으로 무리하게 들어간 경우에는 통상 침입에 해당한다. |
| art319_sec3_1.no_contemporaneous_resistance | standard | negative | skeleton_meta | precedent_pattern | static | none | 침입 판단에서 출입 당시 반드시 현실적 저항이나 구체적 제지가 있을 필요는 없다. |
| art319_sec3_1.apartment_common_door_unauthorized_entry | standard | positive | application_standard | precedent_pattern | retrieve_only | support | 외부인 출입이 통제·관리되는 공동주택 공동현관에서 승낙이나 정당한 이유 없이 비밀번호를 임의 입력·조작하여 출입하는 등 거주자의 사실상 주거 평온을 해치는 행위태양인 경우 주거침입에 해당한다. |
| art319_sec3_1.external_entry_and_partition_exception | exception | exception | exception | abstract_rule | retrieve_assess | exclude | 침입은 원칙적으로 외부로부터의 침입에 한정되어 이미 내부에 있는 사람은 퇴거불응죄만 문제되지만, 적법하게 들어간 뒤 독립적으로 구획되고 무상 출입이 가능한 공간이 아닌 다른 공간으로 옮겨가면 침입이 될 수 있다. |
| art319_sec3_1.entry_decision_authority | definition | positive | narrative | abstract_rule | static | none | 거주자·관리자·점유자는 주거 등에 대한 출입과 체류를 결정하거나 허용할 수 있는 사람이며, 수위 등 현실 감시자의 묵인·승낙은 관리권자의 의사에 반함이 명백한 경우 유효한 승낙이 아니다. |
| art319_sec3_1.minor_child_consent | standard | negative | application_standard | precedent_pattern | retrieve_only | refute | 피해자의 미성년 자녀의 허락을 받고 피해자 주거에 출입한 경우, 피해자 부재 중 그 의사에 반한다는 사정만으로 주거침입죄가 성립하지 않는다. |
| art319_sec3_1.possession_dispute_and_owner_tenant | standard | positive | application_standard | precedent_pattern | retrieve_only | support | 점유·관리권 분쟁에서는 타인이 관리하는 건조물에 들어간다는 고의가 부정될 수 있고, 임대차 종료 후에도 계속 점유하는 임차인의 허락 없이 소유자가 출입하면 주거침입죄가 성립할 수 있으나, 소유자가 임의 폐쇄한 건물에 계속 점유 임차인이 들어간 경우에는 성립하지 않을 수 있다. |
| art319_sec3_1.co_resident_common_space | standard | positive | application_standard | precedent_pattern | retrieve_only | support | 공동거주자는 다른 공동거주자의 정당하지 않은 출입금지에 대항하여 공동생활 장소를 이용하여도 주거침입죄가 성립하지 않지만, 공동거주관계가 형성되지 않은 외부인은 사실상 주거 평온을 해치는 태양으로 출입하면 주거침입죄가 성립한다. |
| art319_sec3_1.apartment_common_areas | standard | positive | application_standard | precedent_pattern | retrieve_only | support | 공동주택 공용 부분의 외부인 출입은 통제·관리 예정과 실제 통제, 출입 목적·경위·태양·시간 등을 종합하여 객관적·외형적으로 판단하며, 엘리베이터·계단·복도 등 세대 전용부분에 필수적으로 부속되어 일상적 감시·관리가 예정된 부분에 침입하면 주거침입죄를 구성한다. |
| art319_sec3_1.consent_and_coerced_consent | exception | exception | exception | abstract_rule | retrieve_assess | exclude | 거주자 등의 명시적·일반적·묵시적 동의나 승낙으로 사실상 평온을 해치는 태양으로 볼 수 없는 경우 침입이 아니지만, 강박에 의한 승낙 의사표시는 무효이므로 주거침입죄가 성립한다. |
| art319_sec3_1.commercial_corridor_implied_consent | standard | negative | application_standard | precedent_pattern | retrieve_only | refute | 다방·당구장·독서실 등이 있는 건물의 공용 계단과 복도는 관리자가 1층 출입문을 특별히 시정하지 않은 경우 관리자 또는 소유자의 묵시적 승낙이 추정되어 출입행위가 주거침입죄를 구성하지 않는다. |
| art319_sec3_1.restricted_place_deceptive_entry | standard | positive | application_standard | precedent_pattern | retrieve_only | support | 출입이 엄격히 제한되는 고사장·사적 주거나 건조물에 출입자격 또는 조건을 기망하여 승낙을 받고 출입하는 행위는, 장소의 형태·용도·통제 상태에 비추어 그 기망적 출입 자체가 사실상 평온상태를 해치는 행위태양일 수 있다. |
| art319_sec3_1.concealed_device_and_key_entry | standard | negative | application_standard | precedent_pattern | retrieve_only | refute | 승낙 또는 접견허가 아래 통상적 방법으로 출입한 경우, CCTV·녹음장비의 은닉이나 집기 철거 목적 등 상대방이 알았다면 승낙하지 않았을 사정만으로는 사실상 평온을 해치는 출입 태양으로 평가되지 않아 주거·건조물침입죄가 성립하지 않는다. |
| art319_sec3_1.open_place_special_prohibition | standard | positive | application_standard | abstract_rule | retrieve_assess | support | 공중 출입이 개방된 장소라도 개인적으로 내려진 출입금지에 위반하거나 일반적이지 않은 시간·방법으로 출입하여 사실상 평온을 해하면 주거침입죄가 성립한다. |
| art319_sec3_1.open_public_place_entry | exception | negative | exception | abstract_rule | retrieve_assess | exclude | 개별 자격을 문제 삼지 않고 일반인의 출입이 허용된 공개장소에 들어가는 것은 소유자·관리인의 의사 또는 추정적 의사에 반하지 않으며, 적법하게 들어간 뒤 불법한 목적이 생긴 경우 주거침입죄는 성립하지 않는다. |
| art319_sec3_1.open_cityhall_and_commercial_entry | standard | negative | application_standard | precedent_pattern | retrieve_only | refute | 불법시위·절도·추행 등 범죄 목적이 있더라도, 출입자격 제한 없이 개방된 시청 로비 또는 일반인 출입이 허용된 영업장소에 출입제지 없이 다수의 힘·위세를 이용하지 않고 통상적 방법으로 들어간 경우 건조물침입죄는 성립하지 않는다. |
| art319_sec3_1.shop_absence_and_protective_order | standard | positive | application_standard | precedent_pattern | retrieve_only | support | 피해자 부재를 이용하여 상점에 들어가거나 법원의 접근금지 임시조치를 위반하여 영업장소에 들어간 경우, 출입 당시 객관적·외형적으로 사실상 평온상태를 해치는 행위태양이면 건조물침입죄가 성립한다. |

자동분류 주의: element metadata is overridden by a stage/concurrence/static frame

> comment:

### art319_sec3_2

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art319_sec3_2.attempt_commencement | element | positive | stage | abstract_rule | relation_condition | none | 주거침입죄의 실행의 착수는 사실상 평온을 해치는 방법으로 주거나 관리 건조물 등에 들어가는 행위를 개시하여 구성요건 실현에 이르는 현실적·객관적 위험성을 갖춘 때에 인정된다. |
| art319_sec3_2.attempt_door_opening | standard | positive | stage | abstract_rule | relation_condition | none | 주거침입 고의로 문을 열거나 문의 시정장치를 부순 경우 실행의 착수가 인정된다. |
| art319_sec3_2.attempt_construction_site_negative | standard | negative | stage | abstract_rule | relation_condition | none | 현장사무실 또는 경비실이 아니라 담장과 경비가 있는 공사현장 외곽에 들어간 것만으로는 주거침입 실행의 착수가 부정된다. |
| art319_sec3_2.completion_minimal_partial_entry_attempt | standard | negative | stage | precedent_pattern | relation_condition | none | 신체의 극히 일부분이 주거 안에 들어갔더라도 사실상 주거의 평온을 해하는 정도에 이르지 않으면 주거침입죄는 미수에 그친다. |
| art319_sec3_2.continuing_offense | definition | positive | narrative | abstract_rule | static | none | 주거침입죄는 사실상 주거의 평온 침해가 계속되는 동안 계속 성립하는 계속범이며, 침입행위는 퇴거하거나 새 체류승낙이 있을 때까지 계속된다. |
| art319_sec3_2.no_refusal_to_leave_after_trespass | exception | exception | concurrence | abstract_rule | relation_condition | exclude | 무단침입이 완성된 뒤 퇴거요구에 불응하여도, 적법하게 주거에 들어간 경우를 전제로 하는 퇴거불응죄는 별도로 성립하지 않는다. |
| art319_sec3_2.post_conviction_continued_occupation | standard | positive | stage | precedent_pattern | relation_condition | none | 무단침입으로 유죄판결을 받은 사람이 판결 확정 후에도 퇴거하지 않고 해당 주택에 계속 거주한 경우, 확정 이후 행위는 별도의 주거침입죄를 구성한다. |

자동분류 주의: element metadata is overridden by a stage/concurrence/static frame; function depends on an unreviewed slot-default role

> comment:

### art319_sec4

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art319_sec4.intent_against_resident_will | element | positive | canonical_element | abstract_rule | always_assess | support | 통설에 따르면 주거침입죄의 고의에는 거주자·관리자·점유자의 의사 또는 추정적 의사에 반하여 타인의 주거 등에 들어간다는 인식과 의사가 필요하며, 미필적 고의로도 충분하다. |
| art319_sec4.intent_factual_peace_entry | standard | positive | application_standard | abstract_rule | retrieve_assess | support | 전원합의체 판결 취지에 따르면 주거침입의 고의는 사실상 평온을 해치는 행위태양으로 타인의 주거에 들어간다는 점을 인식하고 용인하는 것이며, 고의 여부는 주거 등의 형태·용도·성질, 외부인 출입의 통제·관리 방식과 상태, 행위자의 출입 경위와 방법 등을 종합하여 판단한다. |

> comment:

### art319_sec5_2

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art319_sec5_2.lawful_authority_entry | exception | exception | exception | abstract_rule | retrieve_assess | exclude | 적법한 권한에 따라 주거에 들어가는 행위는 공법상 또는 사법상 권한인지와 관계없이 위법성이 조각된다. |
| art319_sec5_2.socially_acceptable_entry | exception | exception | exception | abstract_rule | retrieve_assess | exclude | 사회상규에 반하지 않는 주거침입은 위법성이 조각된다. |
| art319_sec5_2.water_tank_repair_entry | standard | exception | exception | abstract_rule | retrieve_assess | exclude | 물탱크·수도관 밸브의 점검 또는 수리를 위해 반드시 건물의 거실과 부엌을 통과해야 하고 주거 평온을 심하게 침해하지 않는 경우, 특별한 사정이 없으면 해당 출입은 허용되어 사회상규에 위배되지 않는다. |
| art319_sec5_2.right_holder_entry_without_procedure | standard | positive | defeater | precedent_pattern | retrieve_only | block | 권리자가 자신의 권리를 실행하기 위한 경우라도 법정절차에 따르지 않고 주거에 침입하면 주거침입죄가 성립한다는 판례 입장이 소개되어 있다. |
| art319_sec5_2.lawful_labor_dispute_entry | exception | exception | exception | abstract_rule | retrieve_assess | exclude | 노동조합법상 쟁의행위를 위해 승낙 없이 사업장에 들어가더라도 권리남용에 해당하지 않으면 건조물침입죄가 성립하지 않지만, 쟁의행위 자체가 위법하면 위법성조각의 여지가 없다. |
| art319_sec5_2.labor_dispute_exclusive_occupation | standard | positive | defeater | abstract_rule | retrieve_assess | block | 사업장 시설을 전면적·배타적으로 점거하여 조합원 외 출입을 저지하거나 사용자 관리지배를 배제해 업무 중단·혼란을 야기하는 행위는 정당한 쟁의행위 한계를 벗어나 위법성조각 없이 건조물침입죄가 성립한다. |
| art319_sec5_2.labor_dispute_incidental_act | standard | positive | defeater | abstract_rule | retrieve_assess | block | 적법하게 개시된 쟁의행위의 목적을 공지·준비하기 위한 부수행위가 관행적 방식에 편승하여 이루어졌고 전체적으로 수단·방법의 적정성을 벗어나지 않으면 형법상 정당행위에 해당할 수 있다. |
| art319_sec5_2.labor_dispute_plant_occupation | standard | negative | defeater | abstract_rule | retrieve_assess | block | 회사의 시설관리권을 배제한 전면 점거파업이 구조조정 저지를 목적으로 하여 정당한 쟁의행위로 볼 수 없고, 퇴거요구를 알면서도 공장에 들어간 경우 노동쟁의행위로서 정당행위에 해당하지 않는다. |
| art319_sec5_2.labor_dispute_explicit_denial_entry | standard | negative | defeater | abstract_rule | retrieve_assess | block | 대회 개최를 위한 장소사용 허가를 명시적으로 불허받았음에도 대회 개최를 위해 대학에 들어간 경우 노동쟁의행위로서 정당행위에 해당하지 않는다. |

자동분류 주의: function depends on an unreviewed slot-default role

> comment:

### art319_sec5_3

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art319_sec5_3.justification.general | exception | exception | exception | abstract_rule | retrieve_assess | exclude | 주거침입행위가 정당방위·긴급피난·자구행위 등에 해당하면 위법성이 조각된다. |
| art319_sec5_3.justification.emergency_escape | exception | exception | exception | abstract_rule | retrieve_assess | exclude | 맹견의 추격이나 강도를 피하여 타인의 가옥에 몸을 피한 경우 긴급피난에 해당하여 위법성이 조각된다. |
| art319_sec5_3.justification.fire_suppression | exception | exception | exception | abstract_rule | retrieve_assess | exclude | 화재 초기 진화를 위하여 담을 넘어 이웃집에 들어가거나 다른 이웃집 지붕 위로 올라가 물을 뿌린 경우 긴급피난 또는 피해자의 추정적 승낙으로 위법성이 조각될 수 있다. |
| art319_sec5_3.self_help.right_holder_negative | exception | negative | exception | abstract_rule | retrieve_assess | exclude | 사법상 권리자라 하더라도 주거침입죄와 관련하여 자구행위를 할 수 없다. |
| art319_sec5_3.rightless_possessor.peace | standard | positive | defeater | precedent_pattern | retrieve_only | block | 점유권원이 없는 자의 점유라도 주거의 평온은 보호되므로, 권리자가 권리실행을 위한 자력구제 수단으로 건조물에 침입하면 건조물침입죄가 성립한다는 판례가 소개되어 있다. |

자동분류 주의: function depends on an unreviewed slot-default role

> comment:

### art319_sec6_1

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art319_sec6_1.continuing_offense | definition | positive | narrative | abstract_rule | static | none | 주거침입죄는 사실상 주거의 평온 침해가 계속되는 동안 계속 성립하는 계속범이다. |
| art319_sec6_1.no_separate_refusal_after_completed_intrusion | exception | negative | concurrence | abstract_rule | relation_condition | none | 주거침입죄 기수 후 퇴거요구에 불응하더라도 별도로 퇴거불응죄는 성립하지 않는다. |
| art319_sec6_1.repeat_entry_inclusive_crime | standard | positive | concurrence | abstract_rule | relation_condition | none | 주거침입 후 잠시 나왔다가 다시 들어간 경우 포괄일죄가 된다. |
| art319_sec6_1.post_final_conviction_continuance_separate_offense | standard | positive | concurrence | precedent_pattern | relation_condition | none | 무단침입으로 유죄판결이 확정된 뒤에도 퇴거하지 않고 계속 거주하면, 판결확정 이후의 침입행위 및 위법상태 계속으로 별도의 주거침입죄가 된다. |

자동분류 주의: function depends on an unreviewed slot-default role; precedent-pattern form was detected linguistically

> comment:

### art319_sec6_2

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art319_sec6_2.instrumental_intrusion_real_concurrence | standard | positive | concurrence | abstract_rule | relation_condition | none | 주거침입이 다른 범죄의 수단으로 이루어진 경우 수단인 주거침입죄와 목적범죄는 원칙적으로 실체적 경합관계에 있다. |
| art319_sec6_2.combined_offense_absorption | exception | negative | concurrence | abstract_rule | relation_condition | none | 주거침입을 목적범죄와 결합한 독립범죄로 규정하는 경우 주거침입은 결합범에 흡수되어 별도 주거침입죄가 성립하지 않는다. |
| art319_sec6_2.daytime_entry_no_night_intrusion_theft | standard | negative | concurrence | abstract_rule | relation_condition | none | 주거침입이 주간에 이루어진 경우 야간주거침입절도죄는 성립하지 않는다. |
| art319_sec6_2.night_intrusion_theft_attempt_on_entry | standard | positive | concurrence | abstract_rule | relation_condition | none | 야간에 타인의 재물을 절취할 목적으로 사람의 주거에 침입하면, 침입 단계에서 이미 야간주거침입절도 범죄행위의 실행에 착수한다. |
| art319_sec6_2.special_theft_entry_absorption | standard | negative | concurrence | abstract_rule | relation_condition | none | 야간에 주거 일부를 손괴하고 침입한 뒤 절취한 경우 특수절도죄만 성립한다. |

자동분류 주의: function depends on an unreviewed slot-default role

> comment:

### art319_sec7_1

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art319_sec7_1.refusal_to_leave_elements | element | positive | canonical_element | abstract_rule | always_assess | support | 퇴거불응죄는 사람의 주거, 관리하는 건조물, 선박, 항공기 또는 점유하는 방실에서 퇴거요구를 받고 이에 응하지 않음으로써 성립한다. |

> comment:

### art319

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art319.refusal_to_leave.lawful_or_mistaken_entry | element | positive | canonical_element | abstract_rule | always_assess | support | 퇴거불응죄는 처음에 적법하게 또는 과실로 타인의 주거 등에 들어간 사람이 거주자, 관리자 또는 점유자의 퇴거요구에 불응하는 경우 성립한다. |
| art319.refusal_to_leave.enclosed_yard_and_entrance | standard | positive | application_standard | precedent_pattern | retrieve_only | support | 건조물의 위요지 및 사회통념상 건물의 일부인 현관은 퇴거불응죄의 객체에 해당할 수 있고, 소개된 판례는 교회 현관에서 관리인의 퇴거요구에 불응한 경우 퇴거불응죄가 성립한다고 하였다. |

> comment:

### art319_sec7_3

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art319_sec7_3.justified_demand | element | positive | canonical_element | abstract_rule | always_assess | support | 퇴거불응죄의 퇴거요구는 정당한 퇴거요구여야 하며, 정당하지 않은 퇴거요구에 불응한 경우에는 퇴거불응죄가 성립하지 않는다. |
| art319_sec7_3.open_place_manager_demand | standard | positive | application_standard | abstract_rule | retrieve_assess | support | 일반적으로 개방된 장소라도 관리자는 필요에 따라 출입을 제한할 수 있으므로, 관리자의 퇴거요구에도 건조물에서 퇴거하지 않으면 퇴거불응죄를 구성한다. |
| art319_sec7_3.refusal_delay | element | positive | canonical_element | abstract_rule | always_assess | support | 퇴거요구를 받은 적법 체류자도 즉시 퇴거하여야 하고, 유책한 지체가 있으면 퇴거불응이 된다. |
| art319_sec7_3.ability_to_leave | element | positive | canonical_element | abstract_rule | always_assess | support | 퇴거불응의 구성요건적 부작위가 되려면 행위자에게 퇴거의 작위의무를 이행할 일반적·개별적 행위가능성이 있어야 한다. |
| art319_sec7_3.impossible_leaving | exception | exception | exception | abstract_rule | retrieve_assess | exclude | 퇴거요구를 받은 사람이 객관적·주관적으로 그 요구에 응할 수 없거나, 퇴거가 인간 일반 또는 행위자 개인에게 실현 불가능하면 퇴거불응죄는 성립하지 않는다. |
| art319_sec7_3.time_to_comply | standard | negative | application_standard | abstract_rule | retrieve_assess | refute | 거동이 어렵거나 목욕탕에서 옷을 모두 벗고 있는 사람은 퇴거요구에 응할 수 있는 시간 동안에는, 요구 후 시간이 지체되더라도 위법한 체류로 볼 수 없다. |
| art319_sec7_3.no_justifiable_reason | element | positive | canonical_element | abstract_rule | always_assess | support | 퇴거불응죄가 성립하려면 퇴거에 불응할 정당한 사유가 없어야 하며, 정당한 사유가 있으면 성립하지 않는다. |
| art319_sec7_3.debt_dispute_motive | standard | negative | application_standard | precedent_pattern | retrieve_only | refute | 채무를 부인하는 피해자가 피고인을 만나주지 않고 경찰관을 동원하여 내보내려 하였다는 사정에 분노하여 퇴거요구에 불응한 동기나 목적은, 피해자의 주거생활 평온 침해를 정당화할 이유가 될 수 없다는 판례가 소개되어 있다. |
| art319_sec7_3.lawful_lockout_demand | standard | positive | application_standard | abstract_rule | retrieve_assess | support | 근로자 직장점거가 쟁의 목적 달성에 필요한 범위에서 제한적으로 개시되어 적법하더라도, 사용자가 적법하게 직장폐쇄를 하면 사업장에 대한 물권적 지배권이 전면 회복되어 사용자에게 점거 근로자에 대한 퇴거요구 권한이 생긴다. |
| art319_sec7_3.lawful_lockout_noncompliance | standard | positive | application_standard | abstract_rule | retrieve_assess | support | 적법하게 직장폐쇄를 단행한 사용자로부터 퇴거요구를 받고도 불응하여 직장점거를 계속한 행위는 퇴거불응죄에 해당한다. |
| art319_sec7_3.unlawful_lockout_noncompliance | standard | negative | application_standard | abstract_rule | retrieve_assess | refute | 사용자의 직장폐쇄가 정당한 쟁의행위로 인정되지 않는 경우, 사용자가 직장폐쇄를 이유로 적법한 쟁의행위로 사업장을 점거 중인 근로자에게 퇴거요구를 하여도 근로자가 불응해 직장점거를 계속한 경우 퇴거불응죄는 성립하지 않는다. |

> comment:

### art319_sec7_4

| id | kind | polarity | function | form | runtime | gate | proposition |
|---|---|---|---|---|---|---|---|
| art319_sec7_4.intent | element | positive | canonical_element | abstract_rule | always_assess | support | 퇴거불응죄의 고의가 인정되려면 거주자 등의 퇴거요구 및 그 정당성, 자신의 체류 정당성 결여를 인식하면서도 퇴거요구에 불응하려는 의사가 있어야 한다. |

> comment:
