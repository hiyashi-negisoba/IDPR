# homicide RuleIR 승인 원장 감사

- status: `ready_for_rule_ir`
- approval: `data/rulegen/p2/native_review/homicide_approved_decisions.json`
- approval SHA-256: `a2cae14c6d7d1c1d362a2c40466dcb20bfc91a8505ba89d965424480c1d16380`
- law snapshot: `kr_criminal_act_effective_2026-08-03`
- queue cards: 242
- components: 62
- context_only 제외: 73
- 미해결 unit 참조: 2

승인된 판정만 RuleIR 입력이 된다. 미해결 참조는 추측하지 않고 `predicate_ir_missing`으로 보고한다.

## 계약 위반

없음.

## 미해결 unit 참조

- `art250_sec1_16.victim_consent` → `consent_homicide` (predicate_ir_missing)
- `art250_sec1_20.corpse_abandonment_separate` → `corpse_abandonment` (predicate_ir_missing)

## component 구성

| track | component | role | join | 카드 수 | 참조 |
|---|---|---|---|---:|---|
| `attempt` | `attempt_commencement` | component | mandatory_all | 1 | - |
| `attempt` | `attempt_commencement_indicia` | component | alternative_any | 2 | - |
| `attempt` | `attempt_punishability` | component | mandatory_all | 2 | - |
| `base` | `causal_course_error` | bar, component | mandatory_all | 2 | - |
| `base` | `causation` | bar, component | mandatory_all | 2 | - |
| `base` | `causation_attribution` | component | alternative_any | 4 | - |
| `base` | `concurrence` | post_outcome |  | 4 | corpse_abandonment, property_damage |
| `base` | `death_result` | component | mandatory_all | 1 | - |
| `base` | `excessive_defense` | post_outcome |  | 1 | - |
| `base` | `expectability` | bar |  | 1 | - |
| `base` | `intent_error` | bar |  | 2 | - |
| `base` | `justification` | bar, boundary |  | 8 | consent_homicide |
| `base` | `killing_conduct` | component | mandatory_all | 1 | - |
| `base` | `killing_method` | component | alternative_any | 1 | - |
| `base` | `mental_incapacity` | bar |  | 2 | - |
| `base` | `murder_intent` | bar, boundary, component | alternative_any | 7 | intentional_bodily_injury |
| `base` | `murder_intent_indicia` | component | alternative_any | 20 | - |
| `base` | `object_scope` | bar, component | mandatory_all | 3 | - |
| `base` | `offense_count` | post_outcome |  | 6 | - |
| `base` | `offense_definition` | component | mandatory_all | 1 | - |
| `base` | `offense_scope` | boundary |  | 4 | arson_of_occupied_structure, robbery |
| `base` | `person_begins` | bar, component | mandatory_all | 2 | - |
| `base` | `person_begins_basis` | component | alternative_any | 3 | - |
| `base` | `person_ends` | bar, component | mandatory_all | 3 | - |
| `base` | `responsibility_capacity` | component | mandatory_all | 1 | - |
| `complicity` | `aiding` | component | mandatory_all | 1 | - |
| `complicity` | `aiding_causation` | component | mandatory_all | 1 | - |
| `complicity` | `aiding_conduct` | component | alternative_any | 2 | - |
| `complicity` | `aiding_intent` | component | alternative_any | 2 | - |
| `complicity` | `conspiracy` | component | mandatory_all | 2 | - |
| `complicity` | `functional_control` | component | mandatory_all | 1 | - |
| `complicity` | `instigation` | component | mandatory_all | 1 | - |
| `complicity` | `instigation_outcome` | post_outcome |  | 3 | - |
| `complicity` | `joint_principal` | bar, component | mandatory_all | 2 | - |
| `complicity` | `nonstatus_liability` | post_outcome |  | 4 | - |
| `complicity` | `participation_form` | post_outcome |  | 1 | - |
| `complicity` | `preparation_complicity` | bar, component | mandatory_all | 2 | - |
| `complicity` | `shared_intent` | bar, component | mandatory_all | 3 | - |
| `complicity` | `withdrawal` | bar |  | 1 | - |
| `impossible_attempt` | `impossibility_danger` | bar, component | mandatory_all | 3 | - |
| `impossible_attempt` | `impossibility_danger_indicia` | component | alternative_any | 1 | - |
| `omission` | `guarantor_status` | component | mandatory_all | 2 | - |
| `omission` | `guarantor_status_basis` | component | alternative_any | 2 | - |
| `omission` | `omission_causation` | component | mandatory_all | 2 | - |
| `omission` | `omission_equivalence` | component | mandatory_all | 1 | - |
| `omission` | `omission_equivalence_indicia` | component | alternative_any | 2 | - |
| `omission` | `omission_intent` | component | mandatory_all | 2 | - |
| `omission` | `omission_intent_indicia` | component | alternative_any | 1 | - |
| `parricide` | `ancestral_intent` | bar, component | mandatory_all | 3 | - |
| `parricide` | `ancestral_relation` | bar, component | mandatory_all | 10 | - |
| `parricide` | `ancestral_relation_basis` | component | alternative_any | 4 | - |
| `parricide` | `ancestral_relation_timing` | component | mandatory_all | 1 | - |
| `parricide` | `concurrence` | post_outcome |  | 2 | arson_of_occupied_structure |
| `preparation` | `concurrence` | post_outcome |  | 1 | - |
| `preparation` | `conspiracy_agreement` | bar, component | mandatory_all | 2 | - |
| `preparation` | `murder_purpose` | component | alternative_any | 2 | - |
| `preparation` | `offense_count` | post_outcome |  | 1 | - |
| `preparation` | `preparation_conduct` | bar, component | alternative_any | 6 | - |
| `preparation` | `preparation_desistance_mitigation` | post_outcome |  | 1 | - |
| `preparation` | `preparation_intent` | component | mandatory_all | 1 | - |
| `preparation` | `target_specificity` | bar, component | mandatory_all | 2 | - |
| `voluntary_desistance` | `voluntary_desistance` | bar, component | mandatory_all | 7 | - |

## RuleIR에서 제외된 카드

- `art250.causation.autopsy-alternative-causes`: 부검소견에 의지하려면 다른 사인을 배제하는 논증이 필요하다는 증명 법리
- `art250.causation.strangulation-remand`: 교살 혐의 사건의 심리미진 파기환송. 사실심리
- `art250.parricide.status_offense`: 부진정신분범이라는 성격 규정. 효과는 #240·#241이 담고 있다
- `art250_sec1_1.ordinary_murder_victim`: 보통살인·존속살해의 구분 서술이며 track 어휘가 이미 담고 있음
- `art250_sec1_12.insufficient_pesticide_further_inquiry`: 치사량을 더 심리해야 한다는 심리 지침이며 사실심리 영역
- `art250_sec1_16.child_danger_alternatives`: 위급하지 않고 비치명적 수단이 있었으면 과잉방위 부정 — 조각의 한계
- `art250_sec1_16.defense_ends_after_subdual`: 침해 종료 후 제압된 침입자에 대한 폭행 — 조각의 한계
- `art250_sec1_16.domestic_violence_killing`: 지속적 가정폭력이 있어도 회피 가능하면 부정 — 조각의 한계
- `art250_sec1_16.mutual_fight`: 싸움은 방위·공격 양면이므로 정당방위 불가 — 조각의 한계
- `art250_sec1_16.necessity_defense_life`: 살인죄에 긴급피난이 적용되지 않는다는 한계
- `art250_sec1_16.planned_killing_not_self_defense`: 계획된 심장 자상은 상당성 부정 — 조각의 한계
- `art250_sec1_16.stabbing_after_assault`: 폭행·협박을 받았어도 칼로 자상하면 한도 초과 — 조각의 한계
- `art250_sec1_17.supreme_court_active_euthanasia`: 1957년 판결의 결론 인용에 그치고 적용 요건이 없음
- `art250_sec1_18.actio_libera_in_causa`: 원인에 있어서 자유로운 행위. 감경 배제이므로 성립 결론과 무관
- `art250_sec1_18.impulse_control_personality_defect_exception`: 성격적 결함은 원칙적으로 심신장애가 아니라는 한계
- `art250_sec1_18.mental_appraisal_when_suspected`: 정신감정 없이 배척하면 위법. 심리 절차 영역
- `art250_sec1_18.mental_disability_judicial_assessment`: 감정 의견에 기속되지 않는다는 판단 방법. 심리 영역
- `art250_sec1_18.mental_disorder_normal_capacity_exception`: 정상적 능력이 있으면 심신장애가 아니라는 한계
- `art250_sec1_18.pathological_personality_defect`: 병적/성격적 결함의 구분 기준이며 #97·#101과 중복
- `art250_sec1_18.self_induced_methamphetamine_impairment`: 필로폰 자의 투약 사안. #91과 같은 규칙
- `art250_sec1_19.instigation_indirect_facts_proof`: 교사사실을 간접사실로 증명하는 방법 — 증거법
- `art250_sec1_19.instigation_strict_proof`: 교사 사실은 엄격한 증명을 요한다 — 증거법 영역
- `art250_sec1_19.joint_principal_charge_aiding_conviction`: 공소장 변경 없이 방조 인정 — 형사소송법 영역
- `art250_sec1_19.military_beating_case`: 군 폭행 사건의 고의·공동정범 파기환송 사례. 사실인정 판단
- `art250_sec1_19.school_murder_conspiracy_evidence`: 인천 초등생 사건의 공모 증거 부족 판단. 증거법
- `art250_sec1_19.withdrawal_mere_flight_insufficient`: 총을 버리고 도망간 것만으로는 부족 — 이탈 인정의 한계
- `art250_sec1_19.withdrawal_remove_influence`: 주도자는 영향력을 제거해야 이탈 — 이탈 인정의 한계
- `art250_sec1_20.kidnapped_minor_injury_rape_attempted_murder`: 특정범죄가중법·성폭력처벌법 사이의 경합이며 특별법 영역
- `art250_sec1_20.retaliatory_murder_purpose`: 보복목적 판단 기준이며 특정범죄가중법 영역
- `art250_sec1_21.brutal_led_murder_no_plan`: 사체 훼손·암매장 사안의 사형 양정. 양형
- `art250_sec1_21.child_victims_repeat_offense`: 어린이 2명 유인·살해 사안의 사형 양정. 양형
- `art250_sec1_21.death_penalty_exceptional_punishment`: 사형은 특별한 사정과 철저한 심리를 거쳐야 한다는 사형 선택 기준
- `art250_sec1_21.death_penalty_special_circumstances_explicit`: 사형 선고 시 특별한 사정을 명시해야 한다는 판시 방법
- `art250_sec1_21.death_penalty_thorough_inquiry`: 사형 심사 시 전문의견 등 깊이 있는 심리 요구. 심리 절차
- `art250_sec1_21.death_penalty_unavoidable`: 죄책이 심히 중대하고 극형이 불가피할 것이라는 사형 요건
- `art250_sec1_21.foreign_acquittal_detention_credit`: 외국 무죄판결의 미결구금은 제7조 산입 대상이 아님. 형 집행
- `art250_sec1_21.homicide_sentencing_considerations`: 계획성·동기·피해자 관계 등을 양형에 반영하는 일반론
- `art250_sec1_21.indeterminate_midpoint_nonaggravation`: 부정기형을 정기형으로 파기할 때의 불이익변경 기준. 형 산정
- `art250_sec1_21.juvenile_age_at_fact_judgment`: 소년법 19세 미만 판단은 사실심 선고 시 기준. 형 산정
- `art250_sec1_21.leader_spontaneous_joining`: 우발적 살인과 계획범행의 수괴 책임 차이. 양형
- `art250_sec1_21.murder_proceeds_forfeiture`: 범죄수익 몰수·추징 대상. 부수처분
- `art250_sec1_21.murder_recidivism_assessment`: 재범 위험성의 종합 판단과 판결시 기준. 부착명령
- `art250_sec1_21.murder_recidivism_substantial_probability`: 재범 위험성은 상당한 개연성을 의미한다는 정의. 부착명령
- `art250_sec1_21.ordinary_homicide_penalty`: 보통살인죄의 법정형. 이 unit은 형을 산출하지 않는다
- `art250_sec1_21.organized_cult_murders`: 조직적·잔혹한 다수범행 주범의 사형 양정. 양형
- `art250_sec1_21.planned_double_murder`: 계획된 2명 살해 사안의 사형 양정. 양형
- `art250_sec1_21.principal_vs_accomplices`: 주도자 사형·나머지 무기징역의 형평. 양형
- `art250_sec1_21.prisoner_homicide_death_reversal`: 미필적 고의·피해자 1명 등을 고려하지 않은 사형 선택의 위법. 양형
- `art250_sec1_21.second_life_sentence`: 무기징역 집행 중 재차 무기징역 선고의 의미. 양형
- `art250_sec1_21.sequential_offense_planning`: 연속 범행의 계획성과 우발성을 나누어 심리하라는 요구. 양형
- `art250_sec1_21.spontaneous_single_offense`: 우발적·일회적 범행과 뉘우침은 사형 선택의 양형사정
- `art250_sec1_21.treatment_custody_not_attachment_risk`: 치료감호의 재범 위험성만으로 부착명령 위험성을 단정 금지
- `art250_sec1_22.specific_violent_recidivism_enhancement`: 누범 가중은 처단형 문제이며 특별법 영역
- `art250_sec1_22.specific_violent_suspect_identity_disclosure`: 피의자 신상정보 공개 요건이며 성립과 무관
- `art250_sec1_5.circumstantial_murder_conviction`: 간접증거만으로 유죄 인정이 가능하나 신중한 판단이 필요하다는 증명 법리
- `art250_sec1_7.pesticide_cider_circumstantial_proof`: 농약 사이다 사건의 간접증거 종합. 사실인정
- `art250_sec1_7.poisoning_alternative_source`: 청산가리 캡슐 사안에서 다른 섭취 경로를 배제할 수 없는 경우. 증명
- `art250_sec1_7.poisoning_victim_statement_credibility`: 피해자 진술의 신빙성 평가. 증명력
- `art250_sec1_8.death_time_integrated_assessment`: 사망시간 추정의 종합적 증명력. 증명력
- `art250_sec1_8.direct_and_circumstantial_evidence`: 직접증거와 간접증거의 종합. 증명 방법
- `art250_sec1_8.financial_gain_motive_caution`: 보험금 수령만으로 살해 동기를 인정하지 말라는 사실인정 지침
- `art250_sec1_8.financial_motive_family_killing`: 금전적 동기가 수긍되기 위한 사정. 사실인정
- `art250_sec1_8.objective_evidence_despite_weak_motive`: 동기가 미약해도 객관적 증거가 충분하면 유죄. 증명
- `art250_sec1_8.scientific_evidence_reliability`: 과학적 증거방법의 구속력 요건. 증거법
- `art250_sec1_8.third_party_access`: 제3자 열쇠 소지 시 정황증거의 증명력 감소. 증명력
- `art250_sec1_9.bodyless_circumstantial_proof`: 시신이 없어도 간접증거 종합으로 유죄 인정 가능. 증명
- `art250_sec1_9.bodyless_insufficient_linkage`: 시신 없고 연결 정황이 부족하면 책임 인정 곤란. 증명
- `art250_sec1_9.bodyless_summary_requirements`: 시신 없는 살인의 유죄 인정 요소 정리. 증명
- `art250_sec2_5.parricide_improper_status_offense`: #4와 같은 성격 규정
- `art254.attempt_penalty_mitigation`: 미수범 형의 임의적 감경은 양형 사항
- `art254.electronic_device_attachment`: 전자장치 부착명령은 특별법 영역이며 성립 결론과 무관
- `art250_sec1_17.direct_active_euthanasia_negative`: 결정 C 선택(적극적 안락사 부정설). 조각의 한계이므로 자리가 없음
- `art250_sec1_21.death_penalty_special_circumstances_majority`: 결정 C 선택(사형 정당화 특별사정의 전원합의체 다수의견). 양형 기준
