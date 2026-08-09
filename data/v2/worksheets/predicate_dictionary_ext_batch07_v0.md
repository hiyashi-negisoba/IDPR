# Predicate 사전 확장 — 배치 ⑦ 각칙 공무원·사법 범죄 (제122·127·129·130·133·136·137·151·152조) v0

이 배치부터 **각칙**이다 — 총칙 배치①-⑥(카드 없음, 원문 `section_path`만 사용)과 재료 성격이
다르다. 각칙은 조문마다 카드(`## 카드`)와 원문 주석(`## 조문 주석`)이 둘 다 있고, 15개 조문
파일럿에서 이미 실증된 방식(`predicate_dictionary_draft_v0.md` A-2절 "canonical_element **카드
기반**")을 그대로 재사용한다 — **카드가 1차 재료, 원문 주석은 카드 명제가 모호하거나 구조적
쟁점(HOLD 여부 판단 등)을 확인할 때만 선택적으로 인용**. 표기 규칙은 파일럿과 동일: `id`는
가칭, "근거"란은 워크시트 카드 id.

이번 배치 9개 조문은 두 하위군으로 자연히 갈린다 — 뇌물죄군(129·130·133, 직무관련성·대가관계
공유)과 공무집행방해군(136·137, 적법한 직무집행 요건 공유). 122·127·151·152는 각각 독립
조문이지만 151·152는 "국가 사법작용 방해"라는 보호법익을 공유해 사법방해죄군으로 묶었다.

---

## 뇌물죄군 (129 수뢰·사전수뢰 / 130 제3자뇌물제공 / 133 뇌물공여·증뢰물전달)

### A. 공유 predicate 후보 (dedup)

| id (가칭) | canonical_meaning | 근거 카드 | 검수 필요 |
|---|---|---|---|
| `ground_fact.official_or_arbitrator_status` | 행위자(수뢰측)가 공무원 또는 중재인이다 | art129_sec1.basic_offense | 129·133 공통 주체 개념. 130은 "공무원 또는 중재인"이 그대로 행위자이므로 동일 predicate 재사용 가능 |
| `legal_element.job_relatedness_and_quid_pro_quo` | 뇌물이 공무원·중재인의 직무에 관한 것이고 그 직무행위와 대가관계가 있다(상대방 공무원의 직무를 기준으로 판단) | art129_sec1_2, art133_sec1_2.official_duty_relation_quid_pro_quo | 직무관련성과 대가관계를 카드가 한 문장으로 묶어 제시(133_sec1_2)해 하나의 predicate로 접었다. 129 사전수뢰(2항)는 "청탁"만 요구하고 대가관계 문언이 약한데 같은 predicate를 쓸지 별도 강도의 predicate가 필요한지 아래 129 절에서 별도 검토 |
| `ground_fact.bribe_conduct_alternative` | 뇌물을 수수·요구·약속(129) 또는 공여·공여의사표시(133) 중 하나의 행위태양으로 주고받았다 | art129_sec1.basic_offense, art133_sec1_2.unilateral_offer | 조문마다 선택적 구성요건(수수/요구/약속, 공여/의사표시)이 나열되는 패턴 — `ElementExpression`의 `ONE_OF`로 표현 가능해 보이나, 아래 "Completion 후보" 절처럼 행위태양별로 기수시점이 갈리므로 **단일 ground_fact로 접을지 행위태양별 별도 ground_fact + CompletionPolicy state로 분해할지**가 이번 배치의 핵심 구조 결정 |
| `legal_element.bribery_intent` | 상대방이 공무원·중재인이라는 신분 인식 + 직무관련성·대가관계 인식(미필적 고의로 충분) | art129_sec1_2 | 129 카드 문언 그대로. 130·133에도 대응하는 고의 카드가 있으나 표현이 갈려 있어(133은 "공여" 관점 고의, 133_sec1_2.intent_for_delivery_recipient는 "전달받는" 관점 고의) 방향(수뢰자/증뢰자/전달자)별로 분리 유지가 맞는지 확인 |

### 제129조 수뢰·사전수뢰 (조문 고유)

| id (가칭) | canonical_meaning | 근거 |
|---|---|---|
| `legal_element.acceptance_beyond_appearance` | 수수의 외관만으로는 부족하고, 뇌물성 인식과 영득의사를 갖추고 수수하였다 | art129_sec1_1 |
| `ground_fact.prospective_official_probability` | 행위자가 장래 공무원 또는 중재인이 될 것이 예정되어 있거나 어느 정도의 공직취임 개연성을 갖추었다 | art129_sec2_2.prospective_official_probability |
| `legal_element.solicitation_received_before_appointment` | 공무원·중재인이 되기 전에 담당 직무에 관하여 청탁을 받았다 | art129_sec2_1, art129_sec2_2.post_office_request_no_retroaction(소극 확인) |
| `legal_element.prior_bribery_intent` | 자신이 장래 공무원·중재인이 될 사람이라는 점 + 청탁을 받고 수수·요구·약속한다는 점에 대한 인식(공직취임 개연성은 미필적 인식으로 충분) | art129_sec2_3 |

**검수 필요 1 — 사전수뢰의 "청탁"과 130의 "부정한 청탁"이 같은 predicate인가.** 129 2항 카드는
그냥 "청탁"이라고만 하는데 130조는 명시적으로 "**부정한** 청탁"을 요구한다(아래 130절
`legal_element.improper_solicitation_received`). 두 요건이 실제로 다른 강도(단순 청탁 vs
부정한 청탁)인지, 아니면 카드 추출 과정에서 문언만 갈린 것인지 원문 확인이 필요 — 다르다면
별도 predicate 2개(`solicitation_received` / `improper_solicitation_received`) 유지가 맞고,
같다면 하나로 합쳐야 한다.

**검수 필요 2 — 사기죄 전환 카드는 129조 predicate가 아니다.**
`art129_sec2_4.false_prospective_official_fraud_only`(공무원이 될 것처럼 기망했으나 실제 요건
미충족 시 사기죄만 성립)는 129조 자체의 구성요건이 아니라 **129조가 성립하지 않을 때 다른
조문(347조)이 대신 적용된다는 경계 카드**다 — 별도 predicate로 만들지 않고 사전수뢰
`legal_element`들의 "요건 미충족 시" 주석으로만 남긴다(파일럿 A-1의 "권리행사" 패턴과 달리
같은 stage 내 경계가 아니라 조문 간 배타적 적용이라 doctrine도 아님).

### 제130조 제3자뇌물제공

| id (가칭) | canonical_meaning | 근거 |
|---|---|---|
| `legal_element.improper_solicitation_received` | 공무원·중재인이 그 직무에 관하여 **부정한** 청탁을 받았다 | art130_sec1.basic_conduct |
| `ground_fact.third_party_benefit_conduct` | 제3자에게 뇌물을 공여하게 하거나 공여를 요구·약속하였다(기부·시설물 기부채납·출연·채무 대위변제 등 비전형적 형태 포함) | art130_sec1, art130_sec3.nontraditional_benefit_forms |
| `doctrine.third_party_recharacterized_as_direct_bribery` | 제3자와 행위자의 이해관계가 사회통념상 직접 수수와 같이 평가되거나 직접적·실질적으로 연결되면 130조가 아니라 129조 1항 단순수뢰죄가 성립한다 | art130_sec1.direct_receipt_relationship_exception, art130_sec3.direct_substantial_interest_exception |

**검수 필요 — sec1과 sec3의 배제사유 카드 2장이 같은 법리의 중복인가.** `direct_receipt_
relationship_exception`(sec1, "사회통념상 직접 수수와 같이 평가")과
`direct_substantial_interest_exception`(sec3, "직접적·실질적으로 연결")이 문언은 다르지만
결론(129조로 재분류)이 같다 — 위 표에서는 하나의 `doctrine`으로 합쳤는데, sec3이 비전형적
이익형태(기부 등) 맥락에 **한정된** 별도 기준인지(즉 전형적 뇌물엔 sec1 기준, 기부·출연 등엔
sec3 기준을 따로 적용) 원문 대조가 필요하다.

`art130_sec4_2.third_party_receipt_not_required`(제3자의 실제 수수·인식 불요, 거절해도 성립)는
별도 predicate가 아니라 `third_party_benefit_conduct`의 canonical_meaning에 "제3자가 현실
수수했는지는 요건 아님"을 명시하는 방식으로 흡수.

### 제133조 뇌물공여·증뢰물전달

| id (가칭) | canonical_meaning | 근거 |
|---|---|---|
| `ground_fact.bribe_offer_conduct` | 공무원·중재인에게 뇌물을 약속·공여하거나 공여의 의사표시를 하였다(133조 1항, 객체=뇌물) | art133_sec1_2.object_distinction, .intent_for_bribery_offering |
| `ground_fact.bribery_intermediary_delivery_conduct` | 증뢰자로부터 수뢰자에게 전달될 금품임을 알면서 그 금품을 교부받았다(133조 2항, 객체=금품) | art133_sec1_2.object_distinction, .intent_for_delivery_recipient |
| `legal_element.specific_authority_alleged` | 어떠한 공무원의 직무권한에 관한 것인지 구체적으로 특정되어야 한다(개별 직무행위와의 대가관계까지 특정할 필요는 없음) | art133_sec1_2.specific_duty_authority_allegation |
| `doctrine.self_benefit_intermediary_excludes_delivery_offense` | 제3자가 자기 이득을 위해 청탁이나 중개·알선 명목으로 금품을 수수한 경우 증뢰물전달죄는 성립하지 않는다(다른 죄는 별론) | art133_sec1_2.self_benefit_intermediary |

**검수 필요 1 — 133조는 하나의 offense인가, 두 개(뇌물공여죄/증뢰물전달죄)인가.** 카드가
명시적으로 "1항 객체=뇌물, 2항 객체=금품"이라고 구분한다(`object_distinction`). 뇌물공여죄
(1항, 수뢰측 상대 직접 공여)와 증뢰물전달죄(2항, 전달자가 금품을 받는 구성)는 행위자 위치
자체가 다르다 — `DerivedOffenseDef` 두 개로 분리하는 게 맞아 보이지만, 파일럿에 이런 "한
조문·한 항에 실질적으로 다른 두 죄가 병렬된" 사례가 없었다. 129조 사전수뢰(별항이지만 같은
구조 확장이라 자연스럽게 묶임)와 다른 패턴이므로 **구조 결정이 필요한 첫 사례**.

**검수 필요 2 — 의사표시 미도달의 Completion 표현.**
`art133_sec1_2.expression_not_arrived`(공여 의사표시가 상대방에게 도달하지 않으면 미수이나
미수범 처벌규정이 없어 불처벌)는 10·11조에서 확정한 "MODIFY → punishability_note 자유텍스트"
패턴이 아니라 **13조 배치④에서 다룬 "예비음모 처벌원칙"과 같은 CompletionPolicy
`punishable:false` state** 패턴이다(배치④ 확정 사항 재사용, 새 primitive 아님). 다만
`unilateral_offer`(상대방 수수 없이 일방적 제공·의사표시면 "뇌물공여죄"가 아니라 "뇌물공여의사
표시죄") 카드까지 감안하면 133조 1항 자체가 **약속/공여/의사표시 3단계를 별도 죄명처럼 다루는
게 아니라 하나의 CompletionPolicy states(완성/의사표시만=미완성·불벌)로 흡수 가능**해 보인다 —
검수 필요 1의 구조 결정과 함께 확정할 것.

---

## 제122조 직무유기

| id (가칭) | canonical_meaning | 근거 |
|---|---|---|
| `ground_fact.public_official_status` | 행위자가 공무원(단순 기계적·육체적 노무 종사자 제외)이다 | art122_sec2_1.exception_simple_laborer_not_official |
| `legal_element.duty_has_concrete_lawful_basis` | 직무집행의무가 성문 법령 또는 적법한 상관의 지시·명령에 근거해 구체적으로 확정되어 있다(위법한 상관명령, 추상적·부수적·파생적 의무는 제외) | art122_sec2_2.duty_legal_basis, .unlawful_superior_order, .abstract_or_derivative_duty |
| `legal_element.duty_abandonment_conduct` | 정당한 이유 없이 직무수행을 거부하거나 직무를 의식적으로 방임·포기하였다(작위·부작위 불문, 단순 태만·분망·착각·형식적 집행·절차 미이행은 제외) | art122_sec2_2.mere_negligence_or_defective_performance |
| `legal_element.conscious_abandonment_intent` | 직무를 유기한다는 인식, 즉 의식적인 방임 또는 포기와 같은 적극적 요소가 있었다 | art122_sec2_3.intent_conscious_abandonment |
| `doctrine.concrete_risk_required_for_subject` | 구체적인 작위의무나 국가기능 저해의 구체적 위험성이 없으면(예: 병가 중) 본죄의 주체가 될 수 없다 | art122_sec2_1.exception_sick_leave_official |

**검수 필요 1 — 병가 카드를 별도 doctrine으로 둘지 주체 ground_fact에 흡수할지.** 단순노무자
배제는 "공무원 개념 자체에서 제외"(신분의 문제)라 `ground_fact.public_official_status`에 자연히
흡수했지만, 병가 카드는 "공무원 신분은 있으나 이 시점에 구체적 위험성이 없어 주체가 될 수
없다"는 **시점·상황 종속적 배제**다 — 신분 predicate와 다른 층(사건별 사실판단)이라 별도
`doctrine`으로 뺐다. 이 구분이 133조·151조 등 다른 신분범 조문에도 반복될 패턴인지 확인 필요.

**검수 필요 2 — 136조 `lawful_performance_of_duty`와의 관계.** 122조는 "행위자 자신의 직무가
법령에 근거한 구체적 의무인가"를 묻고, 136조는 "피해자 공무원의 직무집행이 적법한가"를 묻는다
— 판단기준(법령 근거 + 구체적 권한 + 절차 준수)이 사실상 동일해 보인다. 아래 공무집행방해군
절에서 dedup 여부를 함께 검토.

특별법·군형법 참조 카드(`specific_crimes_act_recognition_threshold`,
`military_dereliction_requirements`, `military_inadequate_performance_not_sufficient`)는
형법 122조 자체의 구성요건이 아니라 특정범죄가중처벌법·군형법의 별도 조문 해설이므로 predicate
사전 범위 밖으로 **HOLD 아니라 애초에 제외**(35-36조 배치⑥에서 확정한 "범위 밖 명시 분류"와
같은 처리).

---

## 제127조 공무상비밀누설

| id (가칭) | canonical_meaning | 근거 |
|---|---|---|
| `ground_fact.current_or_former_public_official` | 행위자가 공무원 또는 공무원이었던 자이다 | art127_sec2.subject.current_or_former_public_official |
| `legal_element.job_related_secret_worthy_of_protection` | 누설한 사항이 직무상 지득한, 법적 보호가치 있는 비밀이다(정부의 정치적 이익·행정편의 사항, 직무무관 개인비밀은 제외) | art127_sec3_1.political_interest_administrative_convenience_exception, .non_job_related_private_secret_exception |
| `legal_element.disclosure_conduct` | 어느 관청에 속한 비밀인지 알 수 있을 정도로 구체적으로 고지하였다(막연한 고지, 이미 아는 사람에게 알리는 것은 제외) | art127_sec4.disclosure.specificity, .known_recipient |
| `doctrine.interofficial_transmission_not_disclosure` | 국가기능에 위험이 발생하리라고 볼 특별한 사정이 없는 한 관공서 간 정상적 전달은 누설이 아니다 | art127_sec4.disclosure.interofficial_transmission |
| `doctrine.corruption_report_justified_act` | 다른 공직자의 부패행위에 관한 직무상 비밀을 수사기관 등에 신고하는 과정에서 누설되었다면 법령에 의한 정당행위로 위법성이 조각된다(Unlawfulness DEFEAT) | art127_sec6.statutorily_required_corruption_report |

**검수 필요 — `job_related_secret_worthy_of_protection`이 legal_element(구성요건요소)인지
doctrine(소극적 배제사유)인지.** 두 배제 카드(정치적 이익·행정편의 사항 / 직무무관 개인비밀)를
"비밀"이라는 legal_element의 negative 조건으로 흡수했는데, 122조 "위법한 상관명령"과 같은
패턴(요건 자체를 좁히는 negative exception)으로 처리한 것 — 파일럿 typing pass 기준(v2 수정
3)과 일관되는지 재확인.

---

## 공무집행방해군 (136 공무집행방해·직무강요 / 137 위계에 의한 공무집행방해)

| id (가칭) | canonical_meaning | 근거 |
|---|---|---|
| `legal_element.lawful_performance_of_duty` | 보호대상 직무집행이 공무원의 추상적·일반적 권한 및 구체적 직무권한 내에 속하고, 법정된 방식·절차를 준수하였다(장래 예상되는 직무는 제외) | art136_sec2_3.lawful_performance_requirements, .concrete_authority_requirements, .future_duty_exception |
| `ground_fact.violence_or_threat_against_official` | 공무원에 대한 적극적 행위에 의한 폭행 또는 협박이다(제3자·물건에 대한 유형력, 소극적 거동·불복종은 제외) | art136_sec2_4.assault_not_against_officer_exception, .active_conduct_requirement |
| `legal_element.official_and_violence_awareness` | 상대방이 직무집행 중인 공무원이라는 사실 및 그에 대해 폭행·협박한다는 사실을 인식하였다(미필적 고의로 충분) | art136.intent.officer_and_violence_awareness, .intent.conditional_intent |
| `doctrine.illegal_duty_act_reduces_to_general_offense` | 공무집행 자체가 위법하면 136조 구성요건에 해당하지 않거나 위법성이 조각되어도, 그에 대한 폭행·협박이 별도로 폭행죄·협박죄를 구성할 수 있다(다만 정당방위·정당행위로 그 위법성도 조각될 수 있음) | art136_sec2_6.illegal_duty_act.other_offenses |
| `legal_element.purpose_of_coercing_duty_or_resignation` | (136조 2항, 직무·사직강요죄) 공무원에게 직무상 행위를 강요·저지하거나 사직하게 할 목적이 있다 | art136_sec3_4.article136_2_purpose |
| `ground_fact.deceptive_scheme_conduct` | (137조) 위계로써 공무원 또는 제3자를 상대로 공무집행을 방해하는 행위를 하였다 | art137_sec4_1.element.third_party_deception |

**검수 필요 1 — 122조 `duty_has_concrete_lawful_basis`와 136조 `lawful_performance_of_duty`를
같은 predicate로 통합할지.** 판단기준 문언이 사실상 동일(법령 근거 + 구체적 권한 + 절차)하지만
122조는 **행위자 자신**의 직무를, 136조는 **피해자** 공무원의 직무를 가리킨다 — 슬롯이
가리키는 actor가 반대다. 파일럿의 `duty_of_other_affairs`(355/357 공유, 둘 다 "타인 사무처리자"
방향 일치)와 달리 이번엔 방향이 반대이므로 **같은 predicate 재사용은 위험**해 보이지만, 법적
개념 자체(적법한 직무집행의 요건)는 하나라 legal_standard 본문을 공유할 수는 있다 — predicate는
분리하되 서술은 공유하는 절충안 확인 필요.

**검수 필요 2 — 136조 2항(직무·사직강요죄)의 exception 카드.**
`art136_sec3_4.nonofficial_act_coercion`(비직무 행위 강요 목적이면 강요죄 성립)은 136조 predicate
사전 대상이 아니라 조문 간 배타 경계(129조 사전수뢰의 "검수 필요 2"와 같은 패턴) — 별도
predicate 없이 주석으로만 남긴다.

**검수 필요 3 — 137조와 151조의 경계.** `art137_sec6.non_suspect_impersonation_exception`(피의자
아닌 사람이 자발적으로 피의자를 사칭해 허위진술하면 범인은닉죄는 될 수 있어도 137조는 아님)은
137조 자체의 구성요건이 아니라 **151조와의 조문 간 경계**다 — 아래 사법방해죄군 151절에서 같은
사실관계를 참조 표시만 하고, 137조 predicate로는 만들지 않는다. `art137_sec6.official_misconduct
_absorption`(137조 작위범과 122조 부작위범 동시 충족 시 137조만 성립)도 마찬가지로 122조와의
법조경합 경계 — 두 조문 모두에 "참고: 122조/137조 경합 시 137조 우선"이라는 교차주석만 남긴다.

---

## 사법방해죄군 (151 범인은닉·도피 / 152 위증·모해위증)

### 제151조 범인은닉·도피

| id (가칭) | canonical_meaning | 근거 |
|---|---|---|
| `ground_fact.offender_status_of_object` | 객체가 벌금 이상의 형에 해당하는 죄(정범·공범·미수·예비·음모 포함)를 범한 사람이다(범인 자신은 주체에서 제외) | art151_sec2_2.subject_other_than_offender, .offender_participants_attempt |
| `ground_fact.concealment_or_escape_conduct` | 범인을 은닉하거나 도피하게 하는 행위를 하였다(작위·부작위 모두 가능) | art151_sec2_2 (표제) |
| `legal_element.omission_requires_guarantor_status` | 부작위로 도피하게 한 것으로 인정되려면 체포해야 할 보증인적 지위가 필요하다(신고의무 없는 일반인의 부작위는 불해당) | art151_sec2_2.omission_concealment_general_citizen, .omission_escape_guarantor |
| `doctrine.self_concealment_not_an_offense` | 범인 자신의 은닉·도피, 그리고 외형상 다른 공범을 은닉·도피시키는 결과라도 본질적으로 자기 은닉·도피와 다르지 않은 공범의 행위는 구성요건 해당성이 없다 | art151_sec2_2.self_concealment, .accomplice_substantively_self_defense |
| `doctrine.relative_cohabiting_family_exemption` | 범인의 친족 또는 동거가족이 범인을 위하여 한 행위는 책임이 조각되어 처벌되지 않는다(Culpability DEFEAT) | art151_sec2_2.relative_cohabiting_family |
| `legal_element.intent` | 상대방이 벌금 이상 형에 해당하는 죄를 저지른 사람이라는 점, 그를 은닉·도피시켜 국가 형사사법작용을 곤란·불가능하게 한다는 점에 대한 인식과 의사 | art151_sec2_2.intent_awareness_will |
| `legal_element.for_the_offenders_benefit` | 범인 본인을 위한 것이어야 한다(오로지 공범의 이익만을 위한 경우, 본인에게 불이익한 경우, 형사상 이익이 아닌 경우는 제외) | art151_sec3_2.non_criminal_benefit_exclusion |

**검수 필요 1 — 계속범(繼續犯) 성격이 v2.2.0 Completion 모델과 맞는가.**
`art151_sec2_3.completion_continuing_offense`가 "은닉·도피 상태가 계속되는 동안 범죄행위도
계속되며 그 상태가 끝날 때 종료된다"고 명시한다. 6B가 확정한 `CompletionState`(7치, 단일 시점
도출)는 기수 여부를 하나의 판정으로 다루는데, 계속범은 "기수 이후에도 행위가 계속 진행 중"이라는
**시간축 개념**이 추가로 필요해 보인다 — 이게 죄수론(concurrence, 보류 영역)의 문제인지,
아니면 CompletionPolicy 자체가 다뤄야 할 새 축인지 판단이 안 선다. **아키텍처 호환성 검토가
필요한 후보**로 표시(33조 단서·34조와 같은 급의 이슈일 수 있음 — 2패스 착수 전 확정 필요
목록에 추가할지 검수 요청).

**검수 필요 2 — 친족특례를 Culpability DEFEAT로 분류한 것이 맞는가.** 조문 자체가 "처벌하지
아니한다"고 규정하고(총칙 9조 형사미성년자와 동일 문언 구조), 이건 33조 신분범 논의처럼 각칙
고유 조문이 스스로 신분 기반 책임조각사유를 규정한 사례다 — 배치①의 9·11·12·16조 패턴(구조는
Culpability DEFEAT로 통일)을 그대로 따르되, "이 조각사유가 형법총칙이 아니라 각칙 조문 자체에
있다"는 점이 predicate 저작(어느 `offense_ref`에 doctrine을 매달지)에 영향을 주는지 확인.

### 제152조 위증·모해위증

| id (가칭) | canonical_meaning | 근거 |
|---|---|---|
| `ground_fact.witness_took_lawful_oath` | 법률(하위법령 포함)에 근거하고 법정 절차에 따라 적법하게 선서한 증인이다(선서무능력자의 선서는 무효) | art152_sec1_2.lawful_oath_witness, .oath_lawful_procedure, .oath_capacity |
| `ground_fact.false_testimony_conduct` | 허위진술을 하였다 | art152_sec1_1 맥락(표제) |
| `doctrine.retraction_before_examination_end_defeats` | 신문이 끝나기 전에(동일 신문절차 내 다른 신문자의 질문을 통한 시정 포함) 허위진술을 철회·시정하면 위증죄가 성립하지 않는다 | art152_sec1_3.correction_before_examination_end, .correction_through_other_examiner |
| `legal_element.purpose_to_prejudice_specific_party` | (모해위증) 특정 당사자를 불리하게 할 목적이 있다 | art152_sec2_3.noncriminal_case_mohae_exception(반대해석) |
| `ground_fact.proceeding_commenced` | 수사·재판·징계절차가 개시되어 진행 중이다 | art152_sec2_4.proceeding_commenced_requirement |
| `doctrine.mohae_requires_criminal_or_disciplinary_case` | 민사·가사·행정·비송 등 형사·징계 사건이 아닌 사건에서는 모해목적이 있어도 위증죄만 성립하고 모해위증죄는 성립하지 않는다 | art152_sec2_3.noncriminal_case_mohae_exception |

**검수 필요 1 — 철회·시정 조각사유를 doctrine(DEFEAT)으로 볼지, Completion 미도달로 볼지.**
122조의 "단순 태만은 애초에 구성요건 미해당"과 비슷한 구도 — 철회·시정을 "일단 완성된 위증죄가
사후에 소멸하는 것"(doctrine EXEMPT/DEFEAT류)으로 볼지, 아니면 "신문 종료 전에는 애초에
Completion이 도출되지 않는다"(즉 `completion_examination_end` state의 `when` 조건 자체가
철회·시정 없음을 전제)는 구조로 흡수할지 — 후자가 6B가 확정한 "state가 도출조건을 저작한다"는
원칙과 더 맞아 보이지만, 그러면 `doctrine`이 아니라 `completion_policy_def.states.completed.when`
안에 표현돼야 한다. 위 표는 잠정적으로 doctrine으로 뒀으나 **구조 결정 필요**.

**검수 필요 2 — 사후선서(post_oath_completion)를 별도 CompletionPolicy state로 둘지.**
`art152_sec1_3.post_oath_completion`(신문 마친 후 선서하는 경우 선서 시 기수)은 통상적
기수시점(`completion_examination_end`)과 다른 시점을 요구하는 예외 케이스 — 두 카드가 사실상
서로 다른 소송절차 유형(사전선서/사후선서)에 대응하는 대체 state인지, 아니면 하나의 `when`
표현식 안에서 `ONE_OF`로 흡수 가능한지 확인.

`art151_sec2_2.omission_concealment_general_citizen`와의 대칭으로,
`art152_sec1_1.instigation_or_aiding`(위증죄의 교사·종범 성립)은 총칙 31·32조가 이미 커버하는
일반 참가형태이므로 별도 predicate 불필요 — 참고 카드로만 표시.

`art137_sec6.non_suspect_impersonation_exception`(위 공무집행방해군 검수 필요 3)이 151조
`self_concealment`/`accomplice_substantively_self_defense`와 사실관계가 겹치는지도 2패스
착수 전 교차 확인 대상으로 남긴다.

---

## 이번 배치 신규 스키마·DSL primitive 필요 여부

**대체로 없음 — 기존 v2.2 DSL(`GroundFactDef`/`LegalElementDef`/`DoctrineDef`/
`CompletionPolicyDef.states`)로 표현된다.** 다만 두 항목이 구조 검토 없이 넘어가면 안 된다:

1. **151조 계속범 completion**(위 "검수 필요 1") — 단일 시점 기수 판정을 넘어서는 시간축 개념이
   `CompletionState`/죄수론(concurrence) 중 어디에 속하는지 미확정. 33조 단서·34조와 같은 급의
   architecture-compatibility 이슈 후보.
2. **133조가 한 조문·한 항에 실질적으로 두 개의 죄(뇌물공여죄/증뢰물전달죄)를 담고 있는 첫
   사례**(위 "검수 필요 1") — `DerivedOffenseDef` 분리 여부가 스키마 문제는 아니지만 저작
   패턴의 첫 선례가 되므로 이번에 결정해두는 게 이후 배치(⑧-⑫)의 유사 사례 처리에 영향을 준다.

나머지(122·127·136·137·152)는 전부 기존 primitive 안에서 legal_element negative 조건 흡수,
doctrine DEFEAT/EXEMPT, CompletionPolicy states 재배치로 해결된다 — 15개 파일럿·배치①-⑥과
같은 결론.
