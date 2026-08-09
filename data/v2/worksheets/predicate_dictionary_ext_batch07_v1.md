# Predicate 사전 확장 — 배치 ⑦ 각칙 공무원·사법 범죄 (제122·127·129·130·133·136·137·151·152조) v1

[predicate_dictionary_ext_batch07_v0.md](predicate_dictionary_ext_batch07_v0.md)에 대한 사용자
검수 6건 반영. v0는 그대로 둔다 — 이력 추적용.

**이번 정정의 공통 원인**: v0가 "카드 1차 원칙"을 "카드의 문장 구조까지 predicate 경계로
신뢰"하는 데까지 확장해버렸다. 카드 한 문장 안에 있던 AND/OR, mental/conduct 혼합, "다른
조문으로 전환됨"이라는 서술을 각각 하나의 predicate·하나의 doctrine으로 그대로 옮겨 담았는데,
predicate boundary는 v2 DSL 기준(법적 판단·Completion이 갈리는 단위, DoctrineDef는 Elements
확정 **이후** 층에서만 작동)으로 다시 정규화해야 한다는 지적. 사용자가 명시한 6건 외에,
같은 원칙을 이번 배치 전체에 재적용하면서 **추가로 발견한 동종 오류 5건**도 "정정 7"에
self-audit로 담는다 — 사용자가 지적한 두 사례(third_party_recharacterized,
illegal_duty_act_reduces)와 정확히 같은 패턴이 다른 조문에도 있었다.

---

## 정정 1 — 카드 문장 안의 AND/OR/mental-conduct 합성 분해

**v0 오류**: `job_relatedness_and_quid_pro_quo`가 직무관련성과 대가관계를 한 leaf에,
`bribe_conduct_alternative`가 수수·요구·약속·공여·의사표시 5종 행위태양을 한 leaf에,
`bribery_intermediary_delivery_conduct`가 "금품을 교부받는" conduct와 "그 금품이 증뢰물임을
아는" mental을 한 leaf에 묶었다. "카드가 한 문장"이라는 이유로 하나의 predicate일 필요는
없다.

```text
legal_element.job_relatedness              뇌물이 공무원·중재인의 직무에 관한 것이다
legal_element.quid_pro_quo                 그 뇌물과 직무행위 사이에 대가관계가 있다
                                            (상대방 공무원의 직무를 기준으로 판단)

ground_fact.bribe_acceptance               (129) 뇌물을 수수하였다
ground_fact.bribe_request                  (129) 뇌물을 요구하였다
ground_fact.bribe_promise                  (129·133 공유 — 약속은 양측이 함께 성립시키는
                                            단일 행위라 수뢰측·증뢰측에서 같은 predicate 재사용)
ground_fact.bribe_giving                   (133①) 뇌물을 공여하였다
ground_fact.bribe_offer_expression         (133①) 공여의 의사표시를 하였다(상대방 도달 필요
                                            — 미도달은 아래 CompletionPolicy 참고)
```

`bribery_intermediary_delivery_conduct`는 다음처럼 분해(mental 부분은 정정 7에서 재사용
원칙에 따라 별도 predicate 없이 흡수):

```text
ground_fact.intermediary_delivery_receipt_conduct    (133②) 금품을 현실적으로 교부받았다
-- "그 금품이 증뢰에 공할 금품이라는 인식"은 별도 predicate가 아니라 정정 7의 전역 intent
   재사용(object에 포함)으로 흡수
```

**부수 발견 — 이 분해가 v0 "검수 필요 1"(129 사전수뢰 "청탁" vs 130 "부정한 청탁"이 같은
predicate인가)을 자연히 해소한다.** 청탁 자체와 그 부정성을 별도 leaf로 나누면 두 조문의
요건 강도 차이가 조합으로 표현된다:

```text
legal_element.solicitation_received                 직무에 관하여 청탁을 받았다(129·130 공유)
legal_element.solicitation_impropriety               그 청탁이 부정한 것이다(130 전용 추가 요건)
ground_fact.solicitation_received_before_appointment_timing
    (129 사전수뢰 전용) 그 청탁을 공무원·중재인이 되기 전에 받았다
```

129 사전수뢰 = `ALL(solicitation_received, solicitation_received_before_appointment_timing, ...)`,
130 제3자뇌물제공 = `ALL(solicitation_received, solicitation_impropriety, ...)` — 같은 기초
predicate를 공유하면서 강도 차이는 조합으로만 표현되고, 새 predicate를 만들 필요가 없다.

같은 원칙을 130의 `third_party_benefit_conduct`에도 적용(self-audit 추가 발견) — 이것도
"공여하게 함/요구/약속" 3종 행위태양을 한 leaf에 묶고 있었다:

```text
ground_fact.third_party_benefit_causation     제3자에게 뇌물을 공여하게 하였다
ground_fact.third_party_benefit_demand        제3자에 대한 공여를 요구하였다
ground_fact.third_party_benefit_promise       제3자에 대한 공여를 약속하였다
```

(비전형적 이익형태 — 기부·출연·채무대위변제 — 는 세 leaf 공통의 canonical_meaning 주석으로
유지, 별도 predicate 아님.)

---

## 정정 2 — 133조 ①/②는 별도 OffenseDef, DerivedOffenseDef 아님

**v0 오류**: "같은 조문 안에 두 죄가 있다"는 이유만으로 `DerivedOffenseDef` 후보로 뒀다.
객체(뇌물 vs 금품)와 행위자 위치(증뢰자 vs 전달자)가 완전히 다르므로 QUALIFY/COMPOSE로 파생될
관계가 아니다.

```text
offense.bribery_offering       (133①, 뇌물공여죄)
    Elements = ALL(job_relatedness, quid_pro_quo,
                    official_or_arbitrator_status(상대방),
                    ONE_OF(bribe_promise, bribe_giving, bribe_offer_expression))

offense.bribery_delivery       (133②, 증뢰물전달죄)
    Elements = ALL(job_relatedness, quid_pro_quo,
                    official_or_arbitrator_status(최종 수뢰자),
                    intermediary_delivery_receipt_conduct,
                    act_for_anothers_benefit_not_self)  -- 정정 7 self-audit 참고
```

두 `OffenseDef`가 `job_relatedness`/`quid_pro_quo`/`official_or_arbitrator_status`를 공유
predicate로 재사용하는 것은 정상(355/357의 `duty_of_other_affairs` 공유와 같은 패턴)이지,
구조적 파생 관계를 만드는 게 아니다.

**대조 사례로 152조를 확인.** 아래 정정 7에서 다시 다루지만, 152 위증/모해위증은 반대로
**진짜 QUALIFY 관계**다(같은 허위진술 행위에 목적·절차 요건이 가중되는 구조) — "같은 조문
안에 두 항이 있다"가 기준이 아니라 "한 죄의 완성 위에 추가 요건이 얹히는가"가 기준이라는 걸
133과 152를 나란히 놓고 보면 명확해진다.

`specific_authority_alleged`(art133_sec1_2.specific_duty_authority_allegation, "어떠한
공무원의 직무권한에 관한 것인지 구체적으로 적시하여야 한다")는 predicate 후보에서 제외한다 —
"적시"는 공소사실 기재(형사소송) 요건이지 133조의 실체법 구성요건이 아니다. 122조의 특가법·
군형법 카드와 같은 이유로 범위 밖.

---

## 정정 3·7 — "다른 죄로 전환/구성요건 불해당"을 doctrine으로 만들지 않는다

**v0 오류(사용자 지적 2건)**: `third_party_recharacterized_as_direct_bribery`(130),
`illegal_duty_act_reduces_to_general_offense`(136)를 `DoctrineDef`로 만들었다. 둘 다
DEFEAT/MODIFY/EXEMPT 같은 법률효과가 아니라 "이 조문 Elements가 안 되고 저 조문 Elements가
된다"는 **조문 간 독립 평가 경계**다. `DoctrineDef`는 Elements가 확정된 **이후**(Unlawfulness/
Culpability/Punishability)에서만 작동하는데, 이 카드들은 애초에 Elements 층의 문제라 구조적으로
doctrine이 될 수 없다. 129의 "사기죄만 성립" 카드를 predicate로 만들지 않은 판단과 원칙이
같다 — **제거, 각 offense를 독립 평가하는 것으로 충분, 신규 predicate·doctrine 불필요.**

같은 원칙을 배치 전체에 재적용해 **동종 오류 5건을 추가로 발견**(self-audit, 정정 7):

| v0의 잘못된 doctrine | 실제 정체 | v1 처리 |
|---|---|---|
| `third_party_recharacterized_as_direct_bribery`(130) | cross-offense 경계 | 삭제, 130/129 독립 평가 |
| `illegal_duty_act_reduces_to_general_offense`(136) | cross-offense 경계 | 삭제, 136/폭행죄·협박죄 독립 평가 |
| `self_benefit_intermediary_excludes_delivery_offense`(133) | Elements 층 negative 조건(누가 "전달자"인지 자체를 좁힘) | `legal_element.act_for_anothers_benefit_not_self`로 재분류, `bribery_delivery`의 Elements에 흡수 |
| `self_concealment_not_an_offense`(151) | v0 본문이 스스로 "구성요건 해당성이 없다"고 씀 — 정의상 doctrine일 수 없음 | `legal_element.act_directed_at_another_offender`로 재분류(긍정형), `concealment_or_escape_conduct`를 gating |
| `interofficial_transmission_not_disclosure`(127) | "누설이 아니다" = Elements negative 조건 | `disclosure_conduct`의 legal_element에 흡수(별도 predicate 아님) |
| `mohae_requires_criminal_or_disciplinary_case`(152) | 위증→모해위증 QUALIFY의 자연스러운 결과(아래 정정 7-152 참고) | 삭제, `proceeding_commenced`의 정의(형사·징계절차 한정)만으로 자동 처리 |
| `concrete_risk_required_for_subject`(122) | v0 자신이 "검수 필요 1"로 남겼던 질문 — 병가 중 "구체적 위험성 없음"은 직무의 구체성 자체가 흠결된 것(Elements) | `legal_element.concrete_risk_at_time_of_conduct`로 재분류, `duty_abandonment_conduct`를 gating |

**대조 — 진짜 doctrine 2건은 그대로 유지**(제거 대상 아님, 구분 기준을 명확히 하기 위해 명시):

```text
doctrine.corruption_report_justified_act      (127) — 정당행위, Unlawfulness DEFEAT.
    "위법성이 조각된다"는 법률효과가 명시돼 있다 — Elements는 이미 충족된 뒤의 문제.

doctrine.relative_cohabiting_family_exemption (151) — 책임조각, Culpability DEFEAT.
    조문 자체가 "처벌하지 아니한다"고 규정 — 범죄는 완성되나 신분 때문에 처벌만 면제된다.
```

구분 기준: **"범죄가 완성됐는데도 법률효과가 붙는가"(doctrine) vs "애초에 그 요건 자체가
없는가"(legal_element negative 조건).** 후자를 doctrine으로 적으면 이름부터
모순이다("~가 아니다/불성립"이라는 이름의 doctrine은 존재할 수 없다).

---

## 정정 4 — 151조 architecture 후보 정정: 계속범 → offender_status_of_object의 cross-actor dependency

**v0 오류**: `completion_continuing_offense`(계속범 성격)를 architecture-compatibility 검토
후보로 올렸는데, 현 runtime이 "기수 이후 지속기간"까지 계산하는 시스템이 아니라는 걸 놓쳤다.

```text
은닉·도피 상태 성립 → completed
그 이후 지속기간      → 현재 liability 판단 범위 밖(죄수·공소시효 등 후속 scope)
```

CompletionState에 시간축을 추가할 이유가 없다 — **철회.**

**진짜 architecture 후보는 `offender_status_of_object`다.** v0가 이걸 raw fact처럼
`ground_fact`로 뒀는데, "상대방이 벌금 이상의 형에 해당하는 죄를 범한 사람"이라는 건 **다른
actor의 법적 상태**(그 사람의 죄책)다. 같은 사건 안에서 그 범인의 죄책을 IDPR이 이미 별도
offense로 평가한다면, 151조 actor의 Elements가 Call3에게 "이 사람은 범인인가?"를 다시 묻는
게 아니라 **그 다른 actor의 symbolic offense 결과를 참조**해야 한다 — 배치⑤ 34조(간접정범)와
같은 급의 "다른 actor의 stage별 결과를 참조하는 symbolic dependency" 문제.

```text
legal_element.offender_status_of_object
    (잠정) target actor가 벌금 이상의 형에 해당하는 죄를 범하였다
    -- 2-pass에서 확인 필요: 이게 151조 actor 자신의 case 안에서 완결되는 leaf인지,
       아니면 target actor의 OffenseRealization/LiabilityEvaluation 결과를 참조하는
       cross-actor dependency가 필요한지. 34조와 함께 architecture-compatibility 목록에 추가.
```

---

## 정정 5 — 152조 철회·시정/사후선서 → CompletionPolicy로

**v0가 스스로 제기한 두 선택지 중 후자(CompletionPolicy)가 6B와 맞다는 지적 반영.** 철회를
"일단 완성된 죄가 사후 소멸"하는 doctrine이 아니라, **애초에 `completed` state의 `when`이
철회 없음을 전제로 도출**되는 구조로 표현한다. 사전선서/사후선서도 같은 legal state(completed)로
수렴하므로 state를 둘로 나누지 않고 `when` 안의 대체 경로(`ANY`)로 처리한다.

```text
ground_fact.false_testimony_conduct           허위진술을 하였다
legal_element.witness_took_lawful_oath        적법하게 선서한 증인이다 (정정 6에서 재분류)
ground_fact.examination_ended                 해당 증인 신문절차가 종료하였다(사전선서형)
ground_fact.post_oath_completed               사후선서에서 선서를 마쳤다(사후선서형)
legal_element.correction_before_examination_end
    신문이 끝나기 전에(동일 신문절차 내 다른 신문자의 질문을 통한 시정 포함) 허위진술을
    철회·시정하였다 — 긍정형으로 저작(배치① 12조 정정과 같은 원칙, NOT()으로 부정)

completion_policy_def.states.completed.when =
    ALL(
        false_testimony_conduct,
        witness_took_lawful_oath,
        ANY(examination_ended, post_oath_completed),
        NOT(correction_before_examination_end)
    )
```

`preparation_not_punishable`(준비단계 불처벌)은 기존대로 착수 미달 문제로 별도 처리(변경 없음).

---

## 정정 6 — GroundFact/LegalElement typing pass

총칙에서 확정한 기준(원시 사실 vs 법적 포섭·평가) 그대로 적용. 법적 지위 판정·적법성 판단·
구성요건 해당 여부 평가가 들어간 항목은 legal_element다.

```text
ground_fact.public_official_status              →  legal_element.public_official_status
ground_fact.official_or_arbitrator_status       →  legal_element.official_or_arbitrator_status
ground_fact.current_or_former_public_official   →  legal_element.current_or_former_public_official
ground_fact.witness_took_lawful_oath            →  legal_element.witness_took_lawful_oath
ground_fact.violence_or_threat_against_official →  legal_element.violence_or_threat_against_official
    (canonical_meaning 자체에 "폭행 또는 협박에 해당한다"는 구성요건 평가가 들어 있었음)
```

self-audit로 두 건 추가:

```text
ground_fact.prospective_official_probability    →  legal_element.prospective_official_probability
    ("어느 정도의 개연성"이라는 규범적 평가 기준을 포함)
ground_fact.deceptive_scheme_conduct            →  legal_element.deceptive_scheme_conduct
    ("위계"에 해당하는지는 평가적 판단)
```

---

## 정정 7 — 전역 `legal_element.intent`(배치② 13조) 재사용, offense-specific 재정의 금지

사용자가 151조에서 지적한 원칙("일반 고의를 재사용하고 범인은닉에 특유한 인식대상이 별도로
필요하면 그 leaf만 추가")을 이번 배치 전체에 재적용. 판단 기준: **generic intent(객관적
구성요건요소 인식+용인)로 완전히 설명되면 재사용, 판례가 그 이상의 요소(적극적 의사·특별한
목적 등)를 명시적으로 요구하면 별도 predicate 유지.**

```text
제거(전역 intent 재사용, object만 offense-specific):
    legal_element.intent (151, "범인이라는 점+국가 사법작용 곤란화 인식")
    legal_element.bribery_intent (129, 공유)
    legal_element.prior_bribery_intent (129 사전수뢰)
    legal_element.official_and_violence_awareness (136)
    "그 금품이 증뢰에 공할 금품이라는 인식" (133②, intent_for_delivery_recipient의 mental 부분)
    → 위 전부 총칙 13조 legal_element.intent 재사용, object는 offense별
      legal_standard에서 지정(신규 predicate 없음)

유지(판례가 generic intent 이상을 명시적으로 요구):
    legal_element.conscious_abandonment_intent (122)
        "그 인식에는 의식적인 방임 또는 포기와 같은 적극적 요소가 요구된다" — 단순 인식
        이상의 heightened 요건, 판례 문언이 명시적으로 구분
    legal_element.appropriation_intent_of_bribe (129, 신규 — 아래 참고)
    legal_element.purpose_to_prejudice_specific_party (152, 모해목적)
        목적범의 초과주관적 요건, generic intent와 별개 층
```

**부수 발견 — 129 `acceptance_beyond_appearance`도 conduct+intent 합성이었다**(self-audit,
정정 1과 같은 종류). "수수 외관만으로는 부족하고, 뇌물성을 인식하지 못하거나 영득의사 없이
수수한 경우 수수가 성립하지 않는다"를 분해하면:

```text
ground_fact.bribe_acceptance          (이미 정정 1에서 확정, 외관상 수수 행위)
legal_element.intent                  (재사용, 뇌물성 인식)
legal_element.appropriation_intent_of_bribe   (신규, 영득의사 — 단순 인식을 넘는 처분의사라
                                        conscious_abandonment_intent와 같은 급의 heightened
                                        mental element, generic intent로 흡수 불가)
```

**152 위증/모해위증은 정정 2·3에서 다룬 133과 정반대 사례임을 명시.** 위증(기본)과
모해위증(가중)은 QUALIFY 관계가 진짜로 성립한다 — `purpose_to_prejudice_specific_party` +
`proceeding_commenced`(형사·징계절차로 정의를 좁힘)가 위증의 완성 위에 얹히는 추가 요건이고,
그 요건이 갖춰지지 않으면(예: 민사사건) 모해위증의 Elements가 그냥 불성립해 기본 위증죄만
독립 평가된다 — **`mohae_requires_criminal_or_disciplinary_case`라는 별도 doctrine이 필요
없는 이유가 바로 이것**(정정 3 표에 이미 반영).

---

## 배치⑦ v1 최종 predicate 표 (조문별)

### 뇌물죄군 공유

| id | canonical_meaning |
|---|---|
| `legal_element.official_or_arbitrator_status` | 대상자가 공무원 또는 중재인이다 |
| `legal_element.job_relatedness` | 뇌물이 그 직무에 관한 것이다 |
| `legal_element.quid_pro_quo` | 뇌물과 직무행위 사이 대가관계가 있다 |
| `legal_element.solicitation_received` | 직무에 관하여 청탁을 받았다 |

### 제129조 수뢰·사전수뢰

| id | canonical_meaning |
|---|---|
| `ground_fact.bribe_acceptance` / `bribe_request` / `bribe_promise` | 수수/요구/약속(정정 1) |
| `legal_element.appropriation_intent_of_bribe` | 영득의사(정정 7) |
| `legal_element.prospective_official_probability` | 공직취임 개연성(정정 6) |
| `ground_fact.solicitation_received_before_appointment_timing` | 임용 전 청탁 수령 시점(정정 1) |
| (intent) | 전역 재사용(정정 7) |

### 제130조 제3자뇌물제공

| id | canonical_meaning |
|---|---|
| `legal_element.solicitation_impropriety` | 청탁의 부정성(정정 1) |
| `ground_fact.third_party_benefit_causation` / `_demand` / `_promise` | 행위태양 3종(정정 1) |
| ~~`doctrine.third_party_recharacterized_as_direct_bribery`~~ | 삭제(정정 3) |

### 제133조 뇌물공여·증뢰물전달 — 별도 OffenseDef 2개(정정 2)

| offense | id | canonical_meaning |
|---|---|---|
| `offense.bribery_offering`(①) | `ground_fact.bribe_promise` / `bribe_giving` / `bribe_offer_expression` | 행위태양 3종(정정 1) |
| `offense.bribery_delivery`(②) | `ground_fact.intermediary_delivery_receipt_conduct` | 현실적 교부 수령(정정 1) |
| `offense.bribery_delivery`(②) | `legal_element.act_for_anothers_benefit_not_self` | 자기이득 목적 배제(정정 3) |
| (양쪽) | (intent) | 전역 재사용(정정 7), `specific_authority_alleged`는 범위 밖(정정 2) |

### 제122조 직무유기

| id | canonical_meaning |
|---|---|
| `legal_element.public_official_status` | 공무원 지위(정정 6) |
| `legal_element.duty_has_concrete_lawful_basis` | 법령·적법명령 근거(변경 없음) |
| `legal_element.concrete_risk_at_time_of_conduct` | 구체적 위험성(정정 3, doctrine→legal_element) |
| `legal_element.duty_abandonment_conduct` | 방임·포기 행위(변경 없음) |
| `legal_element.conscious_abandonment_intent` | 의식적 방임 인식(정정 7에서 유지 확인) |

### 제127조 공무상비밀누설

| id | canonical_meaning |
|---|---|
| `legal_element.current_or_former_public_official` | 공무원/전직 공무원(정정 6) |
| `legal_element.job_related_secret_worthy_of_protection` | 보호가치 있는 직무상 비밀(변경 없음) |
| `legal_element.disclosure_conduct` | 누설 행위(관공서 간 정상 전달 제외 흡수, 정정 3) |
| `doctrine.corruption_report_justified_act` | 정당행위 DEFEAT(유지) |

### 공무집행방해군 (136·137)

| id | canonical_meaning |
|---|---|
| `legal_element.lawful_performance_of_duty` | 적법한 직무집행(변경 없음) |
| `legal_element.violence_or_threat_against_official` | 폭행·협박(정정 6) |
| `legal_element.purpose_of_coercing_duty_or_resignation` | 강요목적(136②, 변경 없음) |
| `legal_element.deceptive_scheme_conduct` | 위계(137, 정정 6) |
| (intent) | 전역 재사용(정정 7) |
| ~~`doctrine.illegal_duty_act_reduces_to_general_offense`~~ | 삭제(정정 3) |

### 사법방해죄군 (151·152)

| id | canonical_meaning |
|---|---|
| `legal_element.offender_status_of_object` | **cross-actor dependency 확인 필요(정정 4)** |
| `ground_fact.concealment_or_escape_conduct` | 은닉·도피 행위(변경 없음) |
| `legal_element.act_directed_at_another_offender` | 타인 지향성(정정 3, doctrine→legal_element) |
| `legal_element.omission_requires_guarantor_status` | 부작위 보증인지위(변경 없음) |
| `doctrine.relative_cohabiting_family_exemption` | 친족특례 DEFEAT(유지) |
| `legal_element.for_the_offenders_benefit` | 본인을 위함(변경 없음) |
| `legal_element.witness_took_lawful_oath` | 적법 선서(정정 6) |
| `ground_fact.false_testimony_conduct` | 허위진술(변경 없음) |
| `legal_element.correction_before_examination_end` | 철회·시정(정정 5, CompletionPolicy로) |
| `ground_fact.examination_ended` / `post_oath_completed` | 완료 시점 2종(정정 5) |
| `legal_element.purpose_to_prejudice_specific_party` | 모해목적(정정 7에서 유지 확인) |
| `legal_element.proceeding_commenced` | 형사·징계절차 진행중(정정 6) |
| ~~`doctrine.mohae_requires_criminal_or_disciplinary_case`~~ | 삭제(정정 3·7) |

---

## 이번 배치 v1 요약 — 신규 스키마·DSL primitive 필요 여부

**여전히 없음.** 133조가 별도 `OffenseDef` 2개로 결정된 것도 기존 스키마(여러 `OffenseDef`가
같은 predicate를 재사용하는 것)로 충분하고, 152조 CompletionPolicy도 6B가 이미 확정한
`states.when`/`ANY`/`NOT` 조합 그대로다.

**남은 architecture-compatibility 후보는 하나로 정리됐다**: 151조
`offender_status_of_object`의 cross-actor dependency(정정 4) — 34조와 함께 2-pass
착수 전 실제 코드로 확인해야 할 목록에 추가. 계속범(v0가 잘못 올렸던 후보)은 철회.
