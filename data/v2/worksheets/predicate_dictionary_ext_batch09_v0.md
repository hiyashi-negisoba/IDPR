# Predicate 사전 확장 — 배치 ⑨ 생명·신체 (제250·254·255·257·259·263·267·268·258의2조) v0

배치⑧(방화·문서) 종료 시 확정한
[`shared-predicate-canonical-meaning-is-immutable`](메모리)와
[`predicate-authoring-self-check-checklist`](메모리)를 제출 **전**에 직접 대입했다 — 문서
끝 "self-check 적용 메모" 절에 항목별 결과를 남긴다. 방법론은 배치⑦·⑧과 동일(카드 1차,
원문 주석은 모호할 때만 보조).

9개 조문은 세 군으로 갈린다 — **살인군**(250 살인·존속살해 / 254 미수범 / 255 예비·음모),
**상해·치사군**(257 상해·존속상해 / 259 상해치사 / 263 동시범 특례 / 258의2 특수상해),
**과실치사상군**(267 과실치사 / 268 업무상과실·중과실치사상). 이번 배치는 두 개의
architecture-compatibility 연결점을 실제로 만난다 — **art263과 총칙 19조**(CURRENT.md가
이미 예고해둔 연결점)와 **art257 자상의 간접정범과 총칙 34조**(배치⑤가 미해결로 남긴
"34조 실제 gap"의 첫 구체 사례 후보, 이번에 새로 발견) — 둘 다 predicate 사전 단계에서
해결하지 않고 2패스 착수 전 확인 목록에 추가한다.

이번 배치는 이미 존재하는 fixture 예시(`docs/contracts/v2/examples/*.yaml`)와 처음으로
직접 맞물린다 — `offense.homicide`/`offense.injury`가 Step 6B 이후 "(예시)"로 스키마
검증용으로만 있었는데, 이제 그 실제 저작 대상(250·257조)을 이번 배치가 다룬다. 아래
predicate 다수가 그 fixture의 `ground_fact.killing_conduct`/`death_of_victim`/
`legal_element.death_causation`/`ground_fact.violence_used`/`injury_occurred`를 이름 그대로
재사용한다 — 신규 조어가 아니라 이미 컴파일러가 검증해온 이름과의 정합을 확인하는 작업.

---

## 공유 predicate 후보 (생명·신체 장 전체, 250·257 최초 정의 → 이후 조문 재사용)

| id (가칭) | canonical_meaning | 근거 카드 | 비고 |
|---|---|---|---|
| `legal_element.natural_person_victim_status` | 객체가 출생하여 아직 사망하지 아니한 자연인으로서 행위자 이외의 타인이다(법인·동물·사체는 제외되고, 사람은 출생한 자에 한정되어 태아는 포함되지 않으며, 자기 자신은 제외되어 자상·자살은 이 요건을 충족하지 않는다) | art250_sec1_3.suicide_exception, .fetus_life_at_labor_onset, art257_sec1_2의 다수 카드(법인·동물·사체·태아 제외) | 250·257 공유 — 두 조문 모두 "사람"의 정의가 동일 판단기준(자연인·타인·생존 중)이므로 하나로 통합. `fetus_life_at_labor_onset`(분만개시=사람의 시기)은 267 과실치사 원문(Ⅱ절)에도 그대로 인용되므로 267·268도 이 predicate를 재사용 |
| `legal_element.death_causation` (fixture 재사용, `ground_facts.yaml`/`legal_elements.yaml` 기존) | 행위와 사망 결과 사이에 상당인과관계가 인정된다(인과관계가 없으면 미수 또는 결과 미발생에 그친다) | art250_sec1_14, art259_sec1_1.causation.victim_negligence_no_proximate_cause | fixture canonical_meaning은 "살해행위"를 전제하지 않는 일반형 — 250(고의 살해행위)·259(상해행위)·267/268(과실행위) 전부 같은 "행위→사망" 인과관계 판단구조라 재사용 가능해 보이나, **검수 필요**(아래) |

**검수 필요 1 — `death_causation`을 결과적가중범·과실범까지 재사용해도 되는가.**
fixture의 canonical_meaning이 지금은 250(고의 살해)만 검증해본 것이라, 259(상해→사망,
`aggravated_result_attribution`이 이미 있음)·267/268(과실→사망)에 그대로 재사용하면
`aggravated_result_attribution`/`negligence_bundle`의 인과관계 요소와 중복되거나 충돌할
가능성이 있다. 이번 배치 결론은 아래 각 조문 절에서 "어느 predicate가 인과관계를
맡는지" 조문별로 명시하는 것으로 대신하고, `death_causation` 자체의 정의 확장은
제안하지 않는다(불변성 원칙) — 확정은 2패스.

---

## A. 살인군 (제250·254·255조)

### 제250조 살인·존속살해

| id (가칭) | canonical_meaning | 근거 카드 |
|---|---|---|
| `ground_fact.killing_conduct` (fixture 재사용) | 사람을 살해하는 행위(수단·방법 불문)를 하였다 | art250_sec1_9, sec1_11 |
| `ground_fact.death_of_victim` (fixture 재사용) | 피해자가 사망하는 결과가 발생하였다 | art250_sec1_11.completed_murder |
| `legal_element.natural_person_victim_status` (위 공유 predicate 재사용) | — | art250_sec1_3 |
| `legal_element.death_causation` (위 공유 predicate 재사용) | — | art250_sec1_14 |
| `legal_element.intent`(총칙13조 재사용) | — | 250 저작 메모(아래) |

`legal_element.intent`는 정의를 손대지 않고 재사용한다 — "살인의 고의 없이 사람을
사망에 이르게 한 경우 과실치사·상해치사·폭행치사는 될 수 있어도 살인죄는 성립하지
않는다"(art250_sec1_15)는 `intent`가 결여되면 Elements 자체가 불성립한다는 것을
서술한 것일 뿐, 별도 doctrine이 아니다(self-check 2번 적용 — 이미 다른 predicate의
negative 조건이 결론을 구조적으로 만들어낸다).

**부작위** — `bundle.omission_bundle`(총칙18조) 재사용, 보증인적 지위(art250_sec1_10)는
그 bundle의 기존 구성요소로 이미 커버된다(신규 없음, 2패스에서 실제 구성요소 대조만
필요).

**미수·불능미수·중지미수** — `legal_element.commencement_of_execution`(25조)/
`means_or_object_defect`+`dangerousness`(27조)/`voluntary_cessation_or_prevention`(26조)
전부 정의를 손대지 않고 재사용한다. "살의를 가지고 생명을 위태롭게 하는 행위를 직접
개시한 때"(art250_sec1_11.attempt_commencement)는 250이 이 predicate에 대응하는
사실관계일 뿐 canonical_meaning에 넣지 않는다(불변성 원칙, 배치⑧ 정정 1과 동일 패턴).

**위법성조각 — 21·22·23·24·20조 재사용, 250 고유 한계는 authoring 메모로만 기록:**

- `doctrine.necessity_defeat`(22조)는 250에서 사실상 항상 요건 미충족이다
  (art250_sec1_16.necessity_defense_life) — `legal_element.necessity_of_avoidance`의
  기존 4요소 중 "우월적 이익" 요건이 생명 대 생명 비교에서 구조적으로 충족되지 않기
  때문이지, 250 전용 예외 doctrine이 필요한 게 아니다. 정의를 고치지 않고 authoring
  메모로만 남긴다.
- `doctrine.victim_consent_defeat`(24조)의 `legal_element.statutory_bar_on_consent`는
  이미 24조 v0 canonical_meaning 예시에 "촉탁·승낙살인죄 등"이 명시돼 있다
  (art250_sec1_16.victim_consent) — 250이 이 predicate를 그대로 채우면 되고, 정의를
  다시 쓸 필요가 없다.
- `doctrine.self_defense`(21조) `reasonable_grounds`의 250 authoring 메모: "생명 대
  생명의 정당방위는 사회적 상당성 판단이 특히 엄격하다"(art250_sec1_16.
  self_defense_social_adequacy, .mutual_fight) — legal_standard를 고치지 않는다.
- 연명의료중단(art250_sec1_17)은 `legal_element.act_pursuant_to_law`(20조) 재사용.

**책임** — 9·10·11·12·16조(책임능력·심신장애·법률의 착오) 전부 정의를 손대지 않고
재사용한다(art250_sec1_18 다수 카드가 대응).

**공범** — 33조 participation runtime(ATTRIBUTE, `resolve_derivative_liability`) +
8차 addendum `derivative_mode.requires` 재사용. 살인교사(art250_sec1_19.
instigation_murder_completed)·방조(.aiding_murder, .aiding_murder_intent)는
`derivative_mode.requires`에 "피교사자의 살인 결의·실행에 대한 인식"/"정범의 살인
실행행위를 용이하게 한다는 고의"를 채우면 되고, 신규 필드는 필요 없다(8차 addendum이
정확히 이 요건을 위한 필드 — 배치⑧ 164와 동일 확인).

강도살인 공동정범에 "살인 부분 고의의 공동"까지 필요하다는 카드(art250_sec1_19.
robbery_murder_shared_intent)는 6C가 이미 확정한 계약("ATTRIBUTE는 slot-scoped,
predicate-level")과 정확히 일치한다 — 강도의 고의와 살인의 고의가 서로 다른 slot이라
각각 개별적으로 귀속돼야 한다는 것일 뿐, 신규 구조가 필요 없다.

**존속살해 (가중적/부진정신분범):**

| id (가칭) | canonical_meaning | 근거 |
|---|---|---|
| `legal_element.lineal_ascendant_of_self_or_spouse_status` | 객체가 자기 또는 배우자의 직계존속이다(방계혈족·계부모는 제외되고, 신분관계는 살해행위 착수 당시 존재하면 충분하다) | art250_sec2_6 다수 카드 |
| `legal_element.awareness_of_lineal_ascendant_status` | 행위자가 객체가 자기 또는 배우자의 직계존속임을 인식하였다 | art250_sec2_8 |

`legal_element.intent`를 고치지 않고, 존속살해는 `ALL(intent,
awareness_of_lineal_ascendant_status)`로 합성한다(129 `appropriation_intent_of_bribe`와
같은 급의 "판례가 명시적으로 heightened 인식 대상을 요구하는 예외" 패턴 — 배치②가
이미 세운 "intent 자체는 안 고치고 별도 병렬 legal_element를 만든다"는 원칙 그대로
적용).

**architecture-compatibility 후보 — 비신분자의 존속살해 가담(art250_sec2_9).**
비신분자가 존속살해에 가담하면 어느 학설을 따르든 결론은 보통살인죄로 수렴한다는
카드다. 이건 **33조 단서(책임개별화)가 이미 배치⑤에서 "architecture-compatibility
검토 대상"으로 이월해둔 문제의 실제 사례**다 — 존속살해(가중적 신분)에 비신분자가
가담했을 때 그 비신분자에게 가중되지 않은 보통살인죄 책임만 지우려면, 6C
`resolve_derivative_liability`나 ATTRIBUTE가 "가담자별로 다른 offense_ref 결과"를
낼 수 있어야 한다. **새로 결정하지 않고, 33조 단서·34조와 함께 2패스 착수 전 확인
목록에 250을 추가**한다(배치⑤가 이미 "33조 단서는 orchestrator 확인만 남았다"고
판단했던 것과 같은 급).

**범위 밖(predicate 아님)**: 죄수(피해자 수 기준, art250_sec1_20.
homicide_count_by_victims)는 occurrence 단위 판단 문제(9조 검수2와 같은 패턴), 사체유기
별죄 성립(.corpse_abandonment_separate)·채무면탈살인의 강도살인 부정(.
debt_evasion_no_robbery_murder)·강도범행은폐목적살인의 강도살인 긍정(.
robbery_concealment_not_retaliatory)은 다른 offense와의 경계(배치⑦ 129/137식 패턴,
250 자체 predicate 아님), 특정강력범죄 가중·신상정보공개·전자장치부착·범죄수익
몰수추징은 특별법·형사절차 사항(배치⑥ "이 DSL은 구체적 형량 계산기가 아니다" 원칙
재적용).

**HOLD(기존 HOLD 재확인, 신규 아님)**: 오상방위·오상과잉방위(16조 v0 검수 필요 2가
이미 HOLD해둔 "위법성조각사유 전제사실 착오" 문제).

---

### 제254조 살인의 미수범

독자 predicate 없음 — `legal_element.commencement_of_execution`(25조)/
`voluntary_cessation_or_prevention`(26조) 재사용, 250이 만든 CompletionPolicy
states를 그대로 쓴다(신규 없음). 전자장치부착·공소시효 배제·범죄수익 몰수추징은
250과 같은 이유로 범위 밖.

---

### 제255조 살인의 예비·음모

`PREPARATION_OR_CONSPIRACY` 패턴(28·29조) 재사용:

| id (가칭) | canonical_meaning | 근거 |
|---|---|---|
| `ground_fact.preparatory_conduct`(28조 재사용) | — | art255_sec2_1 |
| `ground_fact.conspiracy_agreement`(29조 재사용) | — | art255_sec2_2 |
| `legal_element.purpose_to_commit_target_offense`(28·29조 재사용) | — | art255_sec3.murder_purpose |

**신규 — 살인예비·음모 고유 heightened 요건:**

| id (가칭) | canonical_meaning | 근거 |
|---|---|---|
| `legal_element.specific_victim_identified` | 시기는 미정이더라도 적어도 살해 대상자가 구체적으로 확정되어 있었다 | art255_sec3.specific_target_requirement |

`purpose_to_commit_target_offense`를 고치지 않고 `ALL(purpose_to_commit_target_offense,
specific_victim_identified)`로 합성한다(250 존속살해와 같은 "heightened 요건은 별도
병렬 legal_element" 패턴). 조건부 목적 허용(art255_sec3.conditional_murder_purpose)·
살인 준비에 관한 고의 별도 요구(.preparation_intent)·인터넷 게시만으로는 부족
(.online_murder_notice_insufficient)은 전부 `purpose_to_commit_target_offense`/
`preparatory_conduct`의 legal_standard 확장 메모로 흡수, 신규 predicate 아님.

**예비의 중지미수 불인정(art255 Ⅳ절)은 CompletionPolicy 구조에서 자연히 도출된다** —
`PREPARATION_OR_CONSPIRACY` state 자체가 `voluntary_cessation_or_prevention`이
정의된 "미수 이후" state가 아니므로, 26조 중지미수 규정이 적용될 대상 자체가 없다.
신규 predicate나 구조 결정 불필요.

**예비의 공범** — 공동정범 긍정(art255 Ⅴ절)은 30조 participation 재사용, 예비의
교사 특별처벌(31조②, "예비에 준하여 처벌")은 art250_sec1_19.instigation_no_execution
카드와 정확히 같은 사안(살인 교사했으나 미실행 시 예비·음모에 준하여 처벌)이므로
31조가 확정될 때 함께 참조, 예비의 방조 불인정(판례)은 32조 종범 predicate의
legal_standard에 "예비죄에는 적용되지 않는다"는 한계로 흡수 — 전부 신규 없음.

**범위 밖**: 예비 죄수(여러 예비행위→하나의 죄, art255_sec6)는 occurrence 단위 판단
(9조 검수2와 같은 패턴), 보충관계(예비→미수→기수 흡수, 공소장변경 불요)는
CompletionPolicy exact-one이 이미 보장하는 부분(state 상호배타)과 형사소송법 사항이
섞여 있으나, predicate 사전이 다룰 부분은 "예비 state가 미수·기수 state와 상호
배타"라는 것뿐 — 이건 6B exact-one으로 이미 보장되므로 신규 없음. 특정범죄
전자장치부착·범죄수익몰수추징은 범위 밖.

---

## B. 상해·치사군 (제257·259·263·258의2조)

### 제257조 상해·존속상해

| id (가칭) | canonical_meaning | 근거 카드 |
|---|---|---|
| `legal_element.natural_person_victim_status`(위 공유 predicate 재사용) | — | art257_sec1_2 다수 카드 |
| `ground_fact.violence_used`(fixture 재사용, canonical_meaning 확장 필요 — 아래) | 상해의 수단이 되는 유형력 또는 그 밖의 방법을 사용하였다 | art257_sec3 |
| `ground_fact.injury_occurred`(fixture 재사용) | 신체의 생리적 기능 훼손 등 상해의 결과가 발생하였다 | art257_sec1_1 |
| `legal_element.intent`(총칙13조 재사용) | — | art257_sec1_4 |
| `legal_element.lineal_ascendant_of_self_or_spouse_status`(250과 공유 재사용) | — | art257_sec2 |

**검수 필요 2 — `ground_fact.violence_used`라는 fixture 이름이 257의 실제 범위보다
좁아 보인다.** art257_sec3 카드는 "수단이 폭행이든 그 밖의 방법이든" 미수에 그치면
처벌한다고 명시한다 — "폭행"(violence)에 한정되지 않는 상해 수단(예: 병균 감염, 약물
투여 등 무형적 방법)까지 포함해야 하는데, fixture 이름 자체가 `violence_used`라
canonical_meaning을 넓혀도 이름이 오독을 유발할 수 있다. 이름을 바꿀지
(`injury_conduct` 등), 이름은 그대로 두되 canonical_meaning에 "유형력에 한정되지
않는다"를 명시할지 — 2패스 이전 확정 필요.

**자상 불벌 + 강요·기망에 의한 간접정범 — architecture-compatibility 후보(신규
발견).** art257_sec1_2.self_injury_not_punishable_principle(자상 원칙 불벌) +
.indirect_perpetration_self_injury(강요·기망으로 의사에 반해 자상하게 하면 상해죄의
간접정범 성립)는 **배치⑤가 34조에서 미해결로 남긴 "실제 gap"의 구체적 사례일
가능성이 높다.** 34조의 문제는 "`principal_realization_truth`가 정범 성공을
조건으로 하는데 간접정범은 피이용자 불처벌을 조건으로 해 방향이 반대"였다 — 여기서는
"피이용자(자상한 피해자 본인)가 강요·기망으로 상해죄의 구성요건적 고의 또는 책임을
결여한 도구가 되고, 배후자가 간접정범으로 상해죄 전체 책임을 진다"는 구조라 정확히
같은 유형이다. **predicate 사전 단계에서 해결하지 않고, 33조 단서·34조·250 존속살해
가담과 함께 2패스 착수 전 확인 목록에 257을 추가**한다.

모발·수염 등 절단은 상해 아님(art257.hair_nails_cutting_not_injury) —
`injury_occurred`의 legal_standard 한계사례로 흡수.

**위법성조각 — 21·24·20조 재사용, 257 고유 한계는 authoring 메모:**

- 정당방위 사회적 상당성/싸움 상호공격 배제/새로운 공격 아닌 방어(art257_sec1_6의
  `mutual_fight_no_self_defense`/`defensive_force_not_new_attack`)는 21조
  `reasonable_grounds`의 authoring 메모(250과 동일 패턴).
- 스포츠 규칙준수 상해(.sport_rules_consent)·위험감수 동승(.passenger_risk_consent)은
  24조 `victim_consent_defeat`(현실적 승낙) 재사용 — 운동경기 규칙준수·위험감수
  동승은 학설상 이미 승낙 법리의 대표 사례로 분류된다.
- 징계행위 원칙 불허(.disciplinary_injury)·친권자 체벌의 극히 제한적 허용(.
  parental_corporal_punishment)은 20조 `act_due_to_legitimate_business`/
  `act_not_against_social_norms`의 한계사례(음의 한계)로 흡수.

`legal_element.intent`는 손대지 않고 재사용(art257_sec1_4). 미수 — 250과 같은
CompletionPolicy 재사용.

**범위 밖**: 상해진단서 증명력 판단(art257 Ⅰ.3 원문 다수)은 형사소송 증거법 사항,
predicate 사전 대상 아님.

---

### 제259조 상해치사

**구조 결정 없음 — 배치⑧ 164, fixture `derived_offense.robbery_causing_injury`와
정확히 같은 COMPOSE 패턴.** base = `offense.injury`(257) + `primitive.
aggravated_result_attribution` + 가중결과 = `ground_fact.death_of_victim`(공유
predicate) + `relation.causal_nexus`(base와 가중결과 연결) — robbery_causing_injury가
"강도(base) + 상해(가중결과)"였다면, 259는 "상해(base) + 사망(가중결과)"로 한 단계
평행이동한 것뿐이다. `aggravated_result_attribution`의 기존 legal_standard("결과에
대한 예견가능성과 상당인과관계")가 art259_sec1.basic_offense_and_death,
art259_sec1_1.causation.victim_negligence_no_proximate_cause를 그대로 커버한다 — 신규
predicate 불필요.

- 사망에 고의 있으면 살인죄로 전환(art259_sec1.intentional_death_murder_exception)은
  cross-offense boundary 서술이지 doctrine이 아니다(self-check 2번).
- 상해 공동정범 중 1인이 살인 고의로 살해해도 나머지는 상해치사 책임만 지고 살인죄
  책임은 못 진다(art259_sec2_1.murder_intent_exception)는 164 배치⑧의 "공동정범
  예견가능성 = gap 아님" 판단과 동일 논리(각자 자기 case truths로
  `aggravated_result_attribution`을 평가) — 신규 없음, 2패스 재확인.
- 강도치사와 경합 배제(art259_sec2_3.robbery_resulting_death_exclusion)는 cross-offense
  경계(범위 밖).
- 상해를 교사·방조했으나 피교사자가 살인을 실행해도 예견가능성이 있으면 교사·방조자가
  상해치사의 교사·방조범 책임을 진다(원문 Ⅱ.2)는 8차 addendum `derivative_mode.
  requires` 재사용 — 250의 살인 교사·방조 예견가능성 처리와 정확히 같은 필드.

---

### 제263조 동시범 — architecture-compatibility 핵심 항목

**Elements 후보(전부 재사용):**

```text
legal_element.concurrent_independent_acts   (19조 재사용)
legal_element.same_object_of_result         (19조 재사용)
legal_element.causal_origin_unascertained   (19조 재사용)
ground_fact.injury_occurred                 (257 재사용 — "상해의 결과"가 발생해야
                                             한다는 art263_sec3_2.injury_result 요건)
```

**"공동정범의 예에 의한다"는 법률상 의제이지 6C ATTRIBUTE가 아니다 — 배치②(19조 v1)가
이미 이월해둔 검토를 이번에 실제로 수행한다.** 6C `apply_attribution`은 실제
공동가공의 의사(ATTRIBUTE 대상 slot을 상대 공동정범과 `fold_any`로 병합)를 전제하는데,
263조는 정확히 그 반대(의사연락 **없음**, `concurrent_independent_acts`)를 요건으로
하면서도 처벌효과만 공동정범과 동일하게 만든다. 이건 "실제 공동가공을 판정하는" 문제가
아니라 "법률이 특정 요건(원인불명)이 갖춰지면 실제 귀속 없이 처벌효과를 의제하는"
문제라 33조 단서·34조와 같은 급의 architecture-compatibility 검토 대상이다 — **predicate
사전 단계에서 결정하지 않고, 250 존속살해 가담·257 간접정범과 함께 2패스 착수 전
확인 목록에 추가**한다(19조 v1이 예고했던 대로, 이번에 실제 후보 목록에 편입).

**나머지 요건·한계는 legal_standard 확장 메모로 흡수(신규 없음):**

- 원인행위가 판명되거나 특정인이 원인이 아님이 적극 증명되면 그 특정인에게는 적용
  안 됨(art263.identified_cause_exclusion) — `causal_origin_unascertained`의
  legal_standard 한계.
- 가해행위 자체가 불분명하거나 의사연락이 있어 공동정범이 성립하면 애초에 적용 문제가
  안 생김(art263_sec3_1.no_clear_assault_act, .co_perpetration_contact) —
  `concurrent_independent_acts`의 legal_standard.
- 폭행에 그치고 상해에 이르지 않으면 적용 안 됨(art263_sec3_2.injury_result) —
  `injury_occurred`가 이미 요구하는 바 그대로.
- 강간치상·강도치상·체포감금치상·현주건조물방화치상·낙태치상에는 부적용(art263.
  exception.other_result_crimes) — cross-offense 경계, 263 자체 predicate 아님.
- 원문(Ⅳ.1)이 확인하는 "상해치사·폭행치사에도 특례가 적용된다"는 판례 입장은 259와의
  연결 authoring 메모로 남긴다 — `same_object_of_result`/`causal_origin_unascertained`가
  "사망의 원인 판명불능"에도 그대로 적용된다는 것이지 신규 predicate가 아니다.
- 순수 과실범(과실치상)에는 특례 부정(원문 Ⅳ.2) — `concurrent_independent_acts`의
  legal_standard 한계(공동정범 개념 자체가 과실범에는 의사연락 없는 결합을 인정하지
  않는다는 취지).

---

### 제258조의2 특수상해

**신규 — 전역 재사용 후보(향후 "특수-" 계열 조문에서 반복될 가능성이 높음, 231조
`forgery_without_authority`류와 같은 급의 후보):**

| id (가칭) | canonical_meaning | 근거 |
|---|---|---|
| `legal_element.group_or_multiple_force` | 단체 또는 다중의 위력을 보였다 | art2582_2_sec1.group_or_multiple_force |
| `legal_element.dangerous_object_carriage` | 위험한 물건을 휴대하였다 | art2582_2_sec1.dangerous_object_carriage |

`requires = ANY(group_or_multiple_force, dangerous_object_carriage)`를 base
offense(상해·존속상해·중상해·존속중상해)의 Elements에 추가하는 가중 구조 —
133①/②(별도 OffenseDef) vs 152(QUALIFY) 대조에 비추면 258의2는 **QUALIFY에
가깝다**(같은 상해 행위에 수단의 위험성만 얹히는 구조, 객체·행위자 위치가 달라지지
않는다).

**HOLD — base offense 중 258조(중상해·존속중상해) 부분은 이번 배치 범위 밖.** 258의2가
가중하는 base offense 4개(상해·존속상해·중상해·존속중상해) 중 상해·존속상해(257)는
이번 배치가 확정하지만, 중상해·존속중상해(258)는 51개 조문 워크시트 범위에 없어
predicate가 아직 없다 — 239→238 열람(배치⑧)과 달리 이번엔 대상 조문 자체가 향후
배치에 들어올 예정이므로 지금 원문을 열람해 대신 확정하지 않고, **258이 저작될 때
258의2의 QUALIFY 대상을 258까지 넓힌다는 점만 표시**해 HOLD.

**범위 밖**: 상습범 가중(art2582_2_sec3.habitual_offender_aggravation)·누범 가중
(.recidivist_aggravation, 폭력행위처벌법)은 35조 누범과 같은 패턴(Punishability MODIFY,
`punishability_note` 자유텍스트로 흡수, 구조화된 법정형 메타데이터는 이 DSL 범위
밖 — 배치⑥ 원칙 재적용). 미수(art2582_2_sec3.attempt_punishable)는 250·254와 같은
CompletionPolicy 재사용, 신규 없음.

---

## C. 과실치사상군 (제267·268조)

### 제267조 과실치사

`bundle.negligence_bundle`(14조, `ALL(duty_of_care, foreseeability, avoidability,
breach_of_duty)`) 재사용 + `ground_fact.death_of_victim`(공유 predicate) + 인과관계는
아래 268 검수사항과 함께 조문별로 확정.

살해·상해·폭행의 고의가 없어야 함(art267_sec1.no_intent_to_kill_injure_or_assault)은
cross-offense negative 경계다 — Elements의 mental slot이 `intent`가 아니라
`negligence_bundle`이라는 것 자체가 이미 250/257/262(폭행치사상, 범위 밖)와의 구별을
구조적으로 만든다(self-check 2번), 별도 doctrine 불필요.

**검수 필요 3 — 인과관계를 `death_causation`(250 재사용)으로 할지 별도
`negligence_bundle` 내부 요소로 흡수할지.** `bundle.negligence_bundle`의 4요소 중
`avoidability`(결과회피가능성)는 "주의를 기울였다면 회피할 수 있었는가"라는 규범적
가정 판단이고, `death_causation`은 "실제로 그 행위가 결과의 원인이었는가"라는 사실적
인과 판단이라 서로 다른 질문이다 — 267의 offense.result/causation slot에
`death_causation`을 별도로 채워야 하는지(homicide fixture와 평행), 아니면
`negligence_bundle`이 이미 인과관계까지 포함하는 걸로 볼지 2패스 확정 필요(v0은
결정하지 않는다).

---

### 제268조 업무상과실·중과실치사상

`bundle.negligence_bundle`(14조 재사용) + `ANY(ground_fact.death_of_victim,
ground_fact.injury_occurred)`(공유 predicate 재사용) 위에, **배치②(14조 v1)가 이미
"각칙 특유 가중요건이므로 art268이 다룬다"고 이번 배치로 이월해둔 것을 이제 확정**:

| id (가칭) | canonical_meaning | 근거 |
|---|---|---|
| `legal_element.occupational_duty_of_care` | 행위자가 사람의 생명·신체에 위험을 초래할 수 있는 업무에 사회생활상 계속적으로 종사하는 자로서, 그 업무 수행상 일반인보다 무거운 주의의무를 부담한다 | art268.general_requirements, .personal_capacity_no_exemption |
| `legal_element.gross_negligence` | 주의의무 위반의 정도가 현저하여 조금만 주의를 기울였다면 결과 발생을 쉽게 예견·회피할 수 있었음에도 이를 게을리하였다 | art268조 표제("중과실") — 카드에 직접 대응하는 canonical_element는 없어 조문 표제·통상적 정의로 잠정 확정, 2패스 전 원문 재확인 |

`ANY(occupational_duty_of_care, gross_negligence)`를 `negligence_bundle`에 추가
요건으로 얹는다(둘 중 하나만 충족해도 268이 적용되고 법정형이 같으므로 `ONE_OF`가
아니라 `ANY` — 한 사건이 업무상과실이면서 동시에 중과실일 수도 있어 배타적이지 않다,
self-check 4번 반례 대입 결과).

**허용된 위험·신뢰의 원칙·의료행위 허용된 위험·응급처치 위험형량·개인적 능력부족
면책 불가는 전부 `duty_of_care`(14조)의 legal_standard 확장 메모다 — 신규 doctrine이
아니다.** 배치②(14조 v1)가 이미 "허용된 위험·신뢰의 원칙에 따른 한계를
`duty_of_care`의 legal_standard에 포함시킨다"고 설계해뒀고, art268의 원문(Ⅱ절
방대한 교통사고·의료 판례군)이 정확히 그 재료다:

- `permitted_risk`/`medical_allowed_risk`/`emergency_treatment_risk_balance` —
  사회적 유용성이 인정되는 위험은 애초에 `duty_of_care`(또는 `breach_of_duty`) 요건이
  성립하지 않는다는 Elements negative 조건(self-check 2번 — doctrine처럼 보이지만
  실은 duty_of_care 판단기준의 일부).
- `reliance_principle_general`/`road_reliance_principle`/`reliance_known_or_
  unreliable_other` — 신뢰의 원칙도 같은 이유로 `duty_of_care`/`breach_of_duty`
  판단기준(신뢰가 상당하면 결과회피의무 자체가 없다, 상당성이 부정되는 예외 사유도
  legal_standard 안에 함께 서술).
- `personal_capacity_no_exemption`(개인적 능력부족은 면책 안 됨, 객관적 과실기준)·
  `train_signal_confirmation`(열차 신호확인은 절대적 의무)은 `duty_of_care`가 객관적
  기준(행위자 개인이 아니라 그 업무 종사자 일반의 기준)이라는 legal_standard 확인
  사례.

**확인 필요(HOLD) — 반의사불벌 아님(art268_sec1_1.non_punishable_against_victim_
intent)이 이 DSL의 어느 축에 대응하는지 미확인.** "상해 결과만 발생해도 반의사불벌죄가
아니다"는 처벌조건(피해자 의사)에 관한 절차적 서술인데, `PunishabilityDef`나 다른
스키마에 이런 절차적 처벌조건을 담는 필드가 있는지 이번 v0에서 확인하지 못했다 —
스키마 검색 후 2패스 이전에 결론 필요(35조 누범이 Punishability MODIFY로 표현됐던
것과 같은 축인지, 아니면 36조처럼 predicate 사전 범위 밖(형사소송법 사항)인지).

---

## 이번 배치 신규 스키마·DSL primitive 필요 여부

**없음.** 살인군·상해치사군은 기존 `LegalElementDef`/`GroundFactDef`/
`primitive.aggravated_result_attribution`(COMPOSE)/8차 addendum `derivative_mode.
requires`로, 과실치사상군은 기존 `bundle.negligence_bundle`(`ElementBundleDef`)의
두 번째 실사용 사례로 전부 표현된다. 258의2의 QUALIFY 구조도 152(위증/모해위증)가
이미 실증한 `DerivedOffenseDef` QUALIFY 패턴 재사용이다.

다만 다음은 이번에 구조 결정 없이 넘어가면 안 된다:

1. **art263과 총칙 19조** — "법률상 의제 co-principal"이 6C ATTRIBUTE 계약과
   호환되는지(위 263절).
2. **art257 강요·기망에 의한 자상 간접정범과 34조** — 34조 gap의 첫 구체 offense
   사례(위 257절).
3. **art250 비신분자의 존속살해 가담과 33조 단서** — 가담자별로 다른 offense_ref
   결과가 나오는 구조(위 250절).
4. **art268 반의사불벌 카드가 이 DSL의 어느 축에 대응하는지** — 스키마 재확인 필요.
5. **`legal_element.death_causation`을 259/267/268까지 재사용할지** — 259는
   `aggravated_result_attribution`이 대신 맡고, 267/268은 `negligence_bundle`의
   `avoidability`와 관계 정리가 필요(위 267 검수 필요 3).

---

## self-check 체크리스트 적용 메모 (제출 전 직접 대입 결과)

1. **카드 분해**: art268.general_requirements(과실+결과+인과관계 결합), art255_sec3.
   murder_purpose(목적+대상특정 결합) 등 AND로 묶인 카드를 분해해 별도 predicate로
   나눴다(`negligence_bundle` 4요소, `purpose_to_commit_target_offense`/
   `specific_victim_identified` 분리).
2. **doctrine 자격 검사**: art268의 "허용된 위험"·"신뢰의 원칙"을 doctrine 후보로
   먼저 고려했으나, "범죄가 완성된 뒤에도 이 효과가 붙는가?"에 답이 "아니오 —
   애초에 duty_of_care 요건 자체가 미충족"이므로 duty_of_care의 legal_standard로
   격하했다(위 268절). art259 "사망에 고의 있으면 살인죄"도 cross-offense 전환
   서술이라 doctrine으로 만들지 않았다.
3. **긍정형 이름**: 이번 배치 신규 predicate id 중 `not_`/`no_`/`non_` 접두는 없다
   (`natural_person_victim_status`처럼 부정 사실은 canonical_meaning의 서술로
   담고 이름은 긍정형 유지).
4. **`ONE_OF` 사용 전 배타성 증명**: 268의 업무상과실/중과실 후보에 실제로
   반례(한 사건이 둘 다 해당하는 경우)를 대입해 배타적이지 않음을 확인, `ANY`로
   확정(위 268절) — `ONE_OF`를 쓰지 않았다.
5. **CompletionPolicy state 반례 대입**: 255의 `PREPARATION_OR_CONSPIRACY`는
   28·29조 기존 state를 그대로 재사용(신규 state 없음)이라 이번엔 해당 없음.
   250/254/257/259의 미수 state도 25-27조 기존 구조 재사용.
6. **일반원칙 서술 전 인접 대조**: 250의 "간접정범" 관련 authoring(존속살해
   비신분자 가담)과 257의 "간접정범"(자상 강요·기망)을 서로 다른 architecture 문제로
   구분해뒀다(250은 33조 단서=가담자별 결과 분기, 257은 34조=방향 반대 문제) — 같은
   "간접정범" 단어에 휩쓸려 하나로 합치지 않았다(배치⑧ 225 vs 227 대조와 같은 방식).
7. **stage 라벨-설명 일치**: 이번 배치에 신규 DEFEAT/MODIFY/EXEMPT stage를 가진
   doctrine 후보가 없다(전부 기존 21-24·9-12·16조 doctrine 재사용이거나
   architecture-compatibility로 이월) — 별도 stage 배정을 하지 않았다.

---

## HOLD/architecture-compatibility 종합 (2패스 착수 전 확인 목록에 추가)

기존 목록(33조 단서, 34조, 151조 offender_status_of_object, 263조 특례
—19조 v1이 예고)에 이번 배치로 다음이 추가된다:

1. art263 특례 ↔ 19조/6C ATTRIBUTE 계약 호환성(위 263절) — **예고돼 있던 항목의
   실제 착수**.
2. art257 자상 강요·기망 간접정범 ↔ 34조 gap(위 257절) — **신규 발견**.
3. art250 비신분자 존속살해 가담 ↔ 33조 단서(위 250절) — **신규 발견**.

세 항목 모두 predicate 사전으로는 해결되지 않고, 2패스에서 33/34조를 실제로 저작할 때
함께 검토한다(배치⑤가 이미 세운 원칙).
