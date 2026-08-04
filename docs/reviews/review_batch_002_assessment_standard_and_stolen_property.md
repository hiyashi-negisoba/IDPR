# 검수 배치 002 — 검수 필요 항목 전량

작성: 2026-08-05 · 브랜치 `antigravity-0804` · 배치 001 후속

답변: 각 `판정:` 줄에 **O** / **X** / 다른 지시. 의견은 `> comment:`.

---

## 이 문서에 담긴 것

| 절 | 내용 | 항목 |
|---|---|---|
| C | 새 역할 `assessment_standard` 설계 확인 | 2 |
| D | 배치 001 후속 결정 (조건부·분리·target 정합성) | 14 |
| E | 장물죄 146장 역할 배치안 | 6 그룹 + 개별 |
| F | 장물죄 구조 설계 (B-02 재설계 등) | 3 |

---

# C. 새 역할 `assessment_standard`

배치 001에서 X 판정 7건이 모두 같은 지적이었습니다 — *"일반 심사기준·정의 카드가 satisfied라는
이유로 죄를 차단하면 안 된다"*. 그 자리를 만듭니다.

## C-01 컴파일 동작

- 배출: `{unit}_assessment_standard(case_id, defendant_id, norm_card_id)`
- **결론에 연결하지 않음** — `not_established` / `established` 어디에도 들어가지 않습니다.
- 전달: `query_relations` 조건부 등록 → 계약 → 답안 브리핑에 "판단 기준" 항목으로 노출
- 효과: 모델이 정당방위 상당성·정당행위 요건 등의 기준을 **알고 스스로 포섭**합니다.
  기준 카드가 satisfied라는 이유만으로 죄가 차단되는 일은 사라집니다.

- 판정: 

## C-02 적용 대상 — 배치 001 X 판정 7건

| 유닛 | 카드 | 현재 |
|---|---|---|
| extortion | `art350_sec8_2.right_exercise_total_assessment` | bar |
| homicide | `art250_sec1_16.self_defense_social_adequacy` | bar |
| homicide | `art250_sec1_18.mental_disorder_requirements` | bar |
| property_damage | `art366_sec5_2.immediate_self_recovery_assessment` | bar |
| property_damage | `art366_sec5_2.justifiable_act_requirements` | bar |
| property_damage | `art366_sec5_2.socially_acceptable_act` | bar |
| property_damage | `art366_sec5_5.presumed_consent` | bar |

전부 `assessment_standard` 로 이관합니다.

- 판정: 

---

# D. 배치 001 후속 결정

## D-01 조건부 O 7건을 어떻게 할 것인가

아래 7건에 *"조건부 bar 유지"* 로 답하시면서, 공통적으로 **"카드가 satisfied라는 것이 모든
조건이 실제 충족되었다는 의미일 때만 차단해야 한다"** 는 단서를 다셨습니다.

```
A-04 dwelling_intrusion / labor_dispute_incidental_act      (waiver)
A-07 harboring_offender / omission_escape_guarantor         (bar)
A-10 homicide / mutual_fight_excessive_weapon               (bar)
A-13 homicide / advance_directive_life_sustaining_treatment (bar)
A-14 homicide / life_sustaining_treatment_withdrawal        (bar)
A-15 homicide / presumed_will_life_sustaining_treatment     (bar)
A-23 obstruction_of_official_duty / voluntary_accompaniment (bar)
A-24 obstruction_of_official_duty / active_conduct_requirement (bar)
```

현재 구조로는 그 단서를 지킬 수 없습니다. 카드는 하나의 명제이고 평가는 satisfied/not/unknown
셋뿐이라, "조건이 전부 충족된 경우"와 "그런 기준이 있다"를 구분할 방법이 없습니다.

선택지:

- **(가) 현행 bar 유지** — 모델이 "이 카드가 서술하는 상황이 사안에서 성립하는가"로 평가한다고
  믿고 그대로 둡니다. 위험: 기준만 참인 경우에도 차단될 수 있습니다.
- **(나) assessment_standard 로 이관** — 차단하지 않고 기준만 모델에 전달합니다.
  위험: 정당방위·연명치료 중단이 실제 인정되는 사안에서도 심볼릭이 무죄를 못 냅니다.
- **(다) 카드 분리** — 기준 카드와 "조건 충족" 결론 카드를 나눕니다. 정확하지만 카드 재작성이
  필요합니다.

- 제안: **(가) 유지**. 이 카드들은 정의가 아니라 구체적 사실상황을 서술하고 있어
  ("경미한 폭행", "예상 범위를 넘는 흉기 공격", "소극적 거동에 그친 경우") C-02의 7건과 성격이
  다릅니다. 다만 (다)가 정답이며 카드 재작성 시 함께 처리하는 것을 권고합니다.
- 판정: 

## D-02 카드 분리 3건 — 잠정 조치

| 항목 | 카드 | 지시 |
|---|---|---|
| A-03 | `dwelling_intrusion/co_resident_common_space` | 공동거주자 불성립 / 외부인 성립 분리 |
| A-09 | `homicide/defensive_counterattack` | 기준 부분 / 조각 결과 부분 분리 |
| A-32 | `rape/valid_consent` | 피해자 승낙(bar) / 친권자 승낙(무영향) 분리 |

분리는 카드 명제를 새로 쓰는 일이라 제가 임의로 할 수 없습니다. 그때까지의 잠정 조치가 필요합니다.

- 제안: **분리 완료 시까지 `excluded_cards` 로 배제.** A-03에 *"현 상태의 단일 bar는 유지하면
  안 됩니다"* 라고 하셨고, 나머지 둘도 같은 이유입니다. 배제하면 잘못된 차단은 사라지고
  법리는 모델 자율 논증으로 넘어갑니다.
- 판정: 

## D-03 A-19 boundary 방향 반대 — 어떻게 고칠 것인가

`homicide/art250_sec1_20.murder_after_completed_robbery_or_rape` (현재 `boundary` → robbery)

> 살인죄가 강도살인죄나 강간살인죄 등 결합범의 일부가 되려면 살인행위가 강도 또는 강간 등의
> 기회에 이루어져야 하며, 선행 범죄가 완료된 뒤 살해하면 별도 살인죄와 선행 강도죄 또는
> 강간죄는 실체적 경합관계이다.

명제는 **살인죄 성립을 긍정**하는데 boundary가 살인죄를 소멸시킵니다.

- 제안: **`post_outcome` 으로 이관.** 살인죄는 성립하고, 선행 강도·강간과 실체적 경합이라는
  죄수 효과를 기술하는 카드입니다. 차단도 이동도 아닙니다.
- 판정: 

## D-04 A-30 출발 유닛 정합성

`public_document_forgery/art225_sec3_2.name_change_new_document_forgery` → boundary 변경 승인하시며
*"출발 유닛이 `public_document_alteration` 인지 점검"* 하라고 하셨습니다.

확인 결과: **등록 유닛에 `public_document_alteration` 은 없습니다.** 제225조가
`public_document_forgery` 하나로 적재돼 있어 위조·변조가 한 유닛에 들어 있습니다.

- 제안: 유닛 분리 없이 **`post_outcome`** 으로 두어 "변조가 아니라 위조로 의율" 이라는 정보만
  답안에 전달. boundary 로 두면 자기 자신을 가리켜 유닛 전체가 불성립합니다.
- 판정: 

## D-05 A-31 target 명칭

`rape/art297_sec4_1.direct_violence_threat` → 현재 `refers_to_unit = quasi_sexual_offense`.
*"추상적 `quasi_sexual_offense` 보다 실제 죄명 유닛에 결박"* 하라고 하셨습니다.

확인 결과: 등록 유닛은 `quasi_sexual_offense` (준강간·준강제추행) 하나뿐이고 `quasi_rape` 는
없습니다. 라벨은 "준강간·준강제추행" 으로 기재돼 있습니다.

- 제안: 유닛은 그대로 두고, **답안에 노출되는 라벨만 "준강간"** 으로 좁힘.
- 판정: 

## D-06 A-01 재검토 — 배제 vs 새 역할

`arson/residence_without_actual_presence` ("실제 현존할 필요가 없다") 에 배제를 승인하시며
*"`requirement_waived` 또는 positive/component-support 역할을 신설할 수 있다면 그쪽이 더 정확"*
이라고 하셨습니다. 이번에 역할을 만드니 다시 여쭙니다.

같은 성격으로 이미 배제한 4건도 함께 걸립니다: 상해 `object_method_mistake` /
`unintended_victim`, 살인 `method_error_precedent` / `time_gap`, 그리고 `object_error`.

- 제안: **P2 에도 `requirement_waived` 를 도입해 되살림.** 재산죄 `waiver` 와 같은 뜻
  (요건 불요 — 성립을 막지 않음)이고, 이 카드들이 바로 그 내용입니다. 배제해 두면 "객체의
  착오는 고의를 조각하지 않는다" 같은 유용한 법리가 모델에게 전달되지 않습니다.
- 주의: P2 의 기존 `waiver` 18건은 위법성·책임 조각 사유라 **뜻이 반대**입니다. 이름을 재사용하면
  안 되고 `requirement_waived` 로 따로 만들어야 합니다.
- 판정: 

## D-07 A-34 역할 명칭

`robbery/art343_sec3.abandonment_before_execution_denied` — *"`waiver` 보다 `defense_unavailable`
또는 post_outcome 이 의미상 명확"* 하다고 하셨습니다.

- 제안: **`post_outcome`.** "예비·음모죄에는 중지미수가 인정되지 않는다" 는 성립 판단이 아니라
  성립 후 감면 가부의 문제입니다. 새 역할을 또 만들지 않아도 됩니다.
- 판정: 

---

# E. 장물죄 146장 역할 배치안

머지·크리틱을 마친 정식 카드 146장입니다. 아래는 명제 문언·극성·규범종류로 만든 **초안**이고,
배치 001에서 드러났듯 이 자동 분류는 신뢰할 수 없습니다. 그룹 단위로 확인해 주시고, 개별
수정은 `> comment:` 에 카드 ID로 적어 주세요.

| 제안 역할 | 장수 | 뜻 |
|---|---|---|
| component | 44 | 요건 인정 경로 |
| bar | 34 | 성립 차단 |
| post_outcome | 22 | 죄수·사후행위 효과 |
| variant(미정) | 22 | 학설 대립 — 채택 여부 결정 필요 |
| assessment_standard | 17 | 정의·판단기준 |
| waiver | 7 | 요건 불요 |

## E-01 component (44)

구성요건을 인정하는 경로. 이 중 하나라도 satisfied 여야 해당 component 가 충족됩니다.

- `sec3_1.instigator_aider_subject`  (positive/element)
  본범의 교사범 또는 방조범은 스스로 본범을 실행한 자가 아니므로 장물죄의 주체가 될 수 있다.
- `sec3_2.precedent_definition`  (positive/standard)
  판례는 장물을 영득죄 또는 재산권 침해 위법행위로 영득한 물건으로서 피해자가 추구권 또는 반환청구권을 가지는 것으로 본다고 소개되어 있다.
- `sec3_2.tangible_property`  (positive/element)
  장물죄는 재물에 관한 범죄이므로 장물은 재물이어야 하며, 유체물인 동산은 장물에 속한다.
- `sec3_2.real_estate`  (positive/standard)
  부동산도 장물죄의 범행객체가 될 수 있으나, 장물의 운반은 가동성을 전제로 하므로 부동산에는 적용될 수 없다.
- `sec3_2.double_sale_real_estate`  (negative/standard)
  부동산 이중매매 등으로 배임죄가 성립하는 경우, 매매대상 부동산은 배임행위에 제공된 물건일 뿐 배임으로 영득한 물건이 아니어서 장물이 아니라는 판례가 소개되어 있다.
- `sec3_2.property_interest`  (negative/element)
  재물이 아닌 재산상 이익, 예금채권이나 무체재산권 등의 권리는 장물죄의 객체가 될 수 없다.
- `sec3_2.embodied_security`  (positive/element)
  재산적 이익이나 권리가 화체된 증권 또는 권리 행사에 필요한 증권·서류는 유체동산이므로 장물이 될 수 있다.
- `sec3_2.deceptive_bank_transfer`  (positive/standard)
  피해자가 본범의 기망에 속아 피고인 명의 예금계좌로 현금을 송금한 경우에는 재물을 교부받은 경우에 해당한다는 판례가 소개되어 있다.
- `sec3_2.prohibited_goods`  (positive/standard)
  금제품은 사인 간 소유·거래가 금지되어도 국가의 소유권이 부정되는 것은 아니므로 절도죄와 장물죄의 범행객체가 될 수 있고, 위조 유가증권도 몰수될 때까지 점유가 보호되어 재물 및 장물이 될 수 있다는 판례가 소개되어 있다.
- `sec3_2.minor_principal`  (positive/standard)
  본범이 만 14세 미만으로 책임능력이 없더라도 그가 절취한 재물은 장물이 될 수 있다.
- `sec3_2.foreign_offense`  (positive/standard)
  외국에서 이루어진 본범 행위도 우리 형법상 재산범죄 구성요건에 해당하는 위법행위이면 장물성이 인정되지만, 우리 형법 또는 특별법령상 대응 재산범죄 유형이 전혀 없으면 장물로 처벌할 수 없다는 견해가 제시되어 있다.
- `sec3_2.extortion_attempt`  (negative/standard)
  공갈 본범이 해악을 고지했으나 피해자가 외포하지 않고 연민으로 재물을 교부하여 공갈미수에 그친 경우, 교부된 재물은 장물이 될 수 없다는 견해가 제시되어 있다.
- `sec3_2.registered_imported_car`  (positive/standard)
  장물인 수입자동차를 신규등록하였더라도 최초 등록명의인이 선의취득하는 것이 아니며, 장물양도행위가 범죄가 되지 않는 것도 아니라는 판례가 소개되어 있다.
- `sec3_2.good_faith_third_party_fraud`  (negative/standard)
  본범 아닌 선의·무과실 제3자가 사기·강박 의사표시의 상대방이면 그 의사표시를 취소할 수 없어 장물성이 인정되지 않고, 이를 전제로 한 피해자 환부도 허용될 수 없다는 견해가 제시된다.
- `sec3_2.illegal_cause_benefit_fraud`  (positive/standard)
  수익자가 기망으로 급여자에게 불법원인급여 재물을 제공하게 한 경우 사기죄가 별도로 성립하며, 본범이 사기죄로 영득한 재물에는 장물성이 인정된다는 판례가 소개되어 있다.
- `sec3_2.money_traceability`  (positive/standard)
  재산범죄로 취득한 물건이 금전인 경우 보관·소지 형태가 수표·예금·현금으로 바뀌어도 가액이 명확히 구분되는 한 특별한 사정이 없으면 장물성을 잃지 않는다는 판례가 소개되어 있다.
- `sec3_2.chain_stolen_property`  (positive/element)
  장물죄도 재산범죄이므로 장물죄로 취득한 장물은 다시 장물죄의 본범에서 나온 연쇄장물이 될 수 있다.
- `sec3_3.acquisition.actual_possession`  (positive/element)
  장물취득죄는 단순한 계약 성립이 아니라 장물의 현실적 취득, 즉 점유 이전을 요하며, 낙성계약의 성립 사실만으로는 성립하지 않는다.
- `sec3_3.acquisition.delivery_despite_price`  (positive/standard)
  현실의 인도가 있으면 유상취득에서 대금 지급 전이거나 대금 협상을 미루고 수량·대금이 구체적으로 정해지지 않았어도 장물취득죄 성립에 영향이 없다.
- `sec3_3.acquisition.account_withdrawal`  (negative/standard)
  피고인이 사기방조로 예금계좌를 본범에게 양도하고 피해자가 그 계좌로 송금한 뒤 피고인이 일부를 인출한 경우, 인출은 예금명의자의 예금반환청구 결과일 뿐 본범에게서 점유와 사실상 처분권을 이전받은 것이 아니므로 장물취득죄로 처벌할 수 없다는 판례가 소개되어 있다.
- `sec3_3.acquisition.knowledge_at_delivery`  (positive/element)
  장물취득죄는 계약 체결 당시 장물성을 알 필요는 없지만 적어도 현실적으로 인도받을 당시에는 장물성을 알아야 하며, 취득 후 비로소 장물성을 안 경우에는 성립하지 않는다.
- `sec3_3.transfer.unaware_a_to_aware_b`  (positive/standard)
  A가 장물성을 모르고 취득하였다가 알게 된 후 이를 장물성을 아는 B에게 양도하면 A에게 장물양도죄, B에게 장물취득죄가 성립하고 대향적 공범 관계가 된다고 설명되어 있다.
- `sec3_3.transport.consent_and_delivery`  (positive/element)
  장물운반은 본범 또는 장물취득자의 사전양해나 추정적 승낙 아래 이루어져야 하고, 운반 인수계약만으로는 부족하며 현실적 수여, 즉 점유 이전을 요한다.
- `sec3_3.transport.short_distance`  (positive/standard)
  운반 거리가 짧더라도 장물의 발견 또는 추구·회복을 곤란하게 한 경우 장물운반죄가 성립한다는 견해가 제시되어 있다.
- `sec3_3.transport.knowledge_midway`  (positive/standard)
  장물성을 모르고 운반하다가 운반 도중 장물성을 안 경우 그 후 계속된 운반행위는 장물운반죄를 구성하되, 운반행위를 중지하기 곤란한 경우에는 처벌할 수 없다.
- `sec3_3.custody.actual_receipt`  (positive/element)
  장물보관죄는 보관 인수계약만으로 부족하고 현실적으로 장물을 수취해야 한다.
- `sec3_3.custody.knowledge`  (positive/element)
  장물보관죄는 보관 개시 시 장물성 인식이 필요하고, 장물성을 모르고 보관하다가 나중에 안 경우 반환이 불가능하지 않은데도 보관을 계속하면 그 인식 시점부터 성립한다. 다만 점유할 권한이 있으면 계속 보관하여도 성립하지 않는다.
- `sec3_3.brokering.act_suffices_precedent`  (positive/standard)
  장물알선죄에서 장물임을 알면서 취득·양도·운반·보관하려는 당사자 사이를 연결하여 그 행위를 중개하거나 편의를 도모하면, 실제 계약 성립이나 장물 점유의 현실적 이전이 없어도 장물알선죄가 성립한다는 판례가 소개되어 있다.
- `sec3_3.brokering.unsuccessful_jewelry_sale`  (positive/standard)
  장물인 귀금속의 매도를 부탁받은 자가 장물임을 알면서 매매를 중개하고 매수인에게 전달하려다가 매수인을 만나기 전에 체포된 경우에도, 귀금속 매매를 중개한 이상 장물알선죄가 성립한다는 판례가 소개되어 있다.
- `sec4_1.intent_and_knowledge`  (positive/element)
  장물죄는 고의범으로서 실행행위 및 그 대상이 장물이라는 인식을 요한다.
- `sec4_1.prior_possessor_consensus`  (positive/element)
  장물범의 성립을 위해서는 범행 유형과 관계없이 본범을 포함한 앞선 점유자와 장물범 사이에 행위에 대한 의사의 합치 또는 추정적 승낙이 요구된다.
- `sec4_1.consensus_at_time_of_act`  (positive/element)
  본범 또는 앞선 점유자와의 행위에 관한 의사합치는 행위 당시 존재해야 한다.
- `sec4_1.knowledge_timing_instant_offenses`  (positive/element)
  즉시범적 성격의 장물취득죄·장물양도죄·장물알선죄는 해당 행위 시 장물성 인식이 있어야 한다.
- `sec4_1.abnormal_timber_transaction_knowledge`  (positive/standard)
  야간에 정문을 피하고 후문 판자나 철조망을 제거하여 다량의 목재를 수차 운반한 사정은 정상 거래사회에서 존재할 수 없는 사례이므로 장물성 인식을 부정한 원심에 중대한 사실오인이 있다는 판례 사례가 소개되어 있다.
- `sec4_1.market_price_identity_check_insufficient`  (negative/standard)
  귀금속 매입자가 판매자의 신원을 확인하는 조치를 취하고 시세에 따른 적정 가격으로 매입한 경우에는 장물성 인정을 위한 미필적 고의를 인정하기에 부족하다는 판례 사례가 소개되어 있다.
- `sec4_1.taxi_driver_no_presumption`  (negative/standard)
  영업용 택시 승객의 소지 화물이 장물인 경우 택시 운전사가 그 장물성을 알았다고 추정할 수 없다는 판례 사례가 소개되어 있다.
- `sec5_1.brokering_initial_transport_storage`  (negative/exception)
  처음부터 장물 매매주선을 의뢰받아 이를 위해 장물을 인수·운반 또는 보관한 후 알선한 경우, 운반·보관은 알선 목적 수행 과정에 불과하여 장물알선죄만 성립한다.
- `sec5_2.principal_excluded`  (negative/element)
  장물죄는 타인이 불법하게 영득한 장물에 대하여 성립하므로 범행주체는 본범 이외의 자여야 하며, 자기 범죄로 취득한 장물에는 장물죄가 성립할 여지가 없다.
- `sec5_2.failed_principal_no_brokering`  (negative/exception)
  장차 절취할 물건의 매각을 주선하였더라도 본범이 절취에 실패한 경우 장물죄는 본범 기수 후에만 성립하므로 장물알선죄가 될 수 없고, 경우에 따라 절도방조죄 또는 절도방조미수죄가 성립할 수 있다.
- `sec5_2.real_estate_breach_of_trust`  (negative/standard)
  소유권이전등기 의무자가 이를 위반하여 제3자에게 부동산을 매도·등기한 경우, 배임으로 영득한 것은 재산상 이익이고 대지는 범죄로 영득한 물건이 아니므로 취득자 또는 전득자를 장물취득죄로 처단할 수 없다는 판례가 소개되어 있다.
- `sec5_2.oil_diversion_prior_agreement`  (negative/standard)
  배임으로 유류를 빼돌린 사안에서 유류가 다른 거래처에 납품되기 전에 매수에 합의하거나 승낙한 행위는 배임으로 취득한 장물을 취득한 행위가 아니라 배임행위 자체의 공동정범이라는 판례가 소개되어 있다.
- `sec5_2.thief_fraudulent_sale`  (positive/standard)
  절도범이 장물을 소유자인 것처럼 가장하여 타인에게 매각하고 대금을 편취한 경우, 매수자에 대한 새로운 법익침해가 있으므로 사기죄가 별도로 성립한다.
- `sec6_1.stolen_character_proof`  (positive/element)
  장물죄의 유죄 인정에는 객관적 구성요건으로서 장물성 자체가 명확하게 증명되어야 한다.
- `sec6_2.storage_conviction_without_indictment_amendment`  (positive/standard)
  장물취득죄로 기소되었으나 실제로 장물보관죄가 인정되는 경우, 객관적 사실관계가 동일하고 방어권에 실질적 불이익 우려가 없다면 공소장변경 없이 직권으로 장물보관죄로 처벌할 수 있다는 판례가 소개되어 있다.

- 판정: 

## E-02 bar (34)

satisfied 이면 장물죄를 차단합니다. **배치 001에서 사고가 난 역할이니 특히 봐주세요.**

- `sec3_1.principal_offender_excluded`  (negative/element)
  본범의 정범자는 장물죄의 주체가 될 수 없고, 자기 범죄로 영득한 재물의 처분은 별도로 장물죄를 구성하지 않는다.
- `sec3_1.co_principal_disposal_excluded`  (negative/standard)
  공동정범이 장물을 취득·양도·운반·보관 또는 알선하더라도 장물죄가 성립하지 않는다는 견해가 소개되어 있다.
- `sec3_1.special_robbery_conspirator_brokerage`  (negative/standard)
  특수강도 범행을 모의한 자가 실행에 가담하지 않고 공모자들이 강취한 장물의 처분만 알선한 경우에도 특수강도의 공동정범이면 장물알선죄는 성립하지 않는다는 판례가 소개되어 있다.
- `sec3_1.instigator_aider_acquisition_negative`  (negative/variant)
  교사범 및 방조범에 대해서도 장물취득죄의 성립을 부정해야 한다는 반대 견해가 있다.
- `sec3_2.information_data`  (negative/standard)
  게임아이템·사이버머니·가상자산 등을 포함한 정보 또는 데이터는 유체물이나 물리적으로 관리 가능한 동력이 아니므로 본범 절도죄 등의 객체가 될 수 없고 장물성도 부정된다는 통설 및 판례가 소개되어 있다.
- `sec3_2.computer_fraud_deposit_claim`  (negative/standard)
  컴퓨터등사용사기죄로 취득한 예금채권은 재물이 아닌 재산상 이익이므로, 그 뒤 현금을 인출하거나 계좌이체 후 일부를 인출하여 정을 아는 자에게 교부해도 장물취득죄는 성립하지 않는다는 판례가 소개되어 있다.
- `sec3_2.completion_theory`  (negative/variant)
  장물죄가 성립하려면 본범의 행위가 기수에 이르러야 하며, 본범이 미수에 그친 경우에는 장물죄가 성립하지 않는다는 기수범설이 있다.
- `sec3_2.embezzlement_purchaser_aiding`  (negative/variant)
  횡령 물건을 단순 매수한 사람에게는 횡령죄 방조만 성립하고 장물취득죄는 성립하지 않는다는 견해가 있다.
- `sec3_2.nominee_real_estate`  (negative/standard)
  명의수탁자는 보관자 지위가 인정되지 않아 횡령죄가 성립하지 않는다는 취지로 판례가 변경된 후, 명의신탁 부동산 처분과 관련해서는 장물취득죄 성립도 문제되지 않는다.
- `sec3_2.good_faith_acquisition`  (exception/exception)
  제3자가 선의취득으로 재물 소유권을 취득하면 장물성은 상실되지만, 장물이 도품 또는 유실물이면 피해자 또는 유실자의 2년 이내 반환청구 기간에는 장물성이 상실되지 않는다.
- `sec3_2.acquisitive_prescription`  (exception/exception)
  취득시효 완성으로 제3자가 장물의 소유권을 취득한 경우 장물성은 상실된다.
- `sec3_2.voidable_transaction_negative`  (negative/variant)
  취소할 수 있는 법률행위에서는 취소 전까지 물건이 적법하게 이전되어 장물이 아니고, 사기 매매에서 피해자의 취소 여부가 분명하지 않으면 장물취득죄가 성립하지 않는다는 반대 견해 및 대법원 판례가 소개되어 있다.
- `sec3_2.illegal_cause_benefit_recovery_right`  (negative/variant)
  추구권설에 따르면 불법원인급여의 급여자는 반환을 청구할 수 없으므로 급여물의 장물성이 부정된다.
- `sec3_2.accession_processing`  (exception/exception)
  장물은 원칙적으로 영득재물 자체 또는 동일성을 가진 물건이며 변형 후에도 동일성이 있으면 장물성이 유지되지만, 첨부로 제3자가 적법하게 소유권을 취득하여 추구권이 소멸하면 장물성도 소멸한다.
- `sec3_2.victim_consent_gift_inheritance`  (exception/exception)
  피해자가 본범의 소유권 취득에 동의·승낙하거나 본범에게 장물을 증여하거나 본범이 피해자 사후 장물을 상속하면 추구권과 위법한 재산상태가 없어 장물성은 소멸한다.
- `sec3_2.copied_media`  (exception/exception)
  절취한 문서·영상물·USB 등의 내용을 다른 매체에 복제해 생성된 물건은 원래 매체와 별개의 물건이므로 장물이 아니다.
- `sec3_2.breach_of_trust_bribe`  (exception/exception)
  배임죄는 원칙적으로 장물죄의 본범이 될 수 없지만, 배임수증죄에서 수증 대상이 재물이면 장물죄의 본범이 될 수 있다.
- `sec3_3.acquisition.temporary_use`  (negative/standard)
  본범을 위해 장물을 일시 사용하거나 그렇게 사용할 목적으로 장물을 건네받은 것만으로는 장물취득이 아니며, 보수를 조건으로 장물인 신용카드로 물품을 구입해 주기로 받은 경우도 장물취득에 해당하지 않는다는 판례가 소개되어 있다.
- `sec3_3.acquisition.predicate_completion`  (negative/element)
  장물취득은 본범이 기수에 이른 뒤에만 성립하므로, 절도 현장에서 본범이 탈취 중인 재물 일부를 무상으로 얻은 사람은 절도 공범이 될 수 있어도 장물취득죄는 성립하지 않는다.
- `sec3_3.acquisition.from_victim`  (exception/exception)
  피해자로부터 직접 취득한 경우는 장물취득으로 보기 어렵다.
- `sec3_3.acquisition.account_holder_principal`  (exception/exception)
  사기 공범이 아닌 계좌양도자가 피해자 송금금을 영득 목적으로 인출하면 피해자에 대한 횡령죄의 본범이 되므로, 송금자금에 대한 장물취득죄는 구성요건해당성이 결여된다.
- `sec3_3.acquisition.shared_use`  (exception/exception)
  절취한 자동차에 함께 탑승하는 등 장물을 함께 사용하는 경우는 무상 사용대차와 마찬가지로 장물취득죄가 성립하지 않는다.
- `sec3_3.transfer.to_victim`  (exception/exception)
  본범이 피해자에게 장물을 양도한 경우에는 장물양도에 해당하지 않는다.
- `sec3_3.transport.victim_return`  (exception/exception)
  피해자로부터 위탁받거나 피해자에게 반환하기 위해 장물을 운반한 경우 장물운반죄가 성립하지 않는다.
- `sec3_3.transport.bank_transfer`  (exception/exception)
  장물 현금을 계좌에 입금한 뒤 원격 계좌로 이체한 경우에는 현금 자체의 장소적 이동과 동일성 유지가 없어 장물운반죄가 성립하지 않는다.
- `sec4_1.later_knowledge_transport_storage`  (exception/exception)
  계속범적 성격의 장물운반죄와 장물보관죄는 운반 또는 보관을 시작한 뒤에라도 장물성 인식이 성립할 수 있고, 그 이후의 운반·보관행위에 관하여 죄가 성립할 수 있다.
- `sec4_1.no_later_knowledge_acquisition`  (negative/exception)
  재물을 인도받은 후 비로소 장물일 수 있다는 의구심을 가진 경우에는 그 재물수수행위로 장물취득죄가 성립하지 않는다.
- `sec5_2.co_principal_excluded`  (negative/exception)
  본범의 공동정범은 본범이 영득한 장물을 운반·보관·매수하더라도 본범과 동일하게 장물죄를 구성하지 않는다.
- `sec5_2.embezzlement_conspiracy`  (negative/standard)
  타인 물건의 점유자와 횡령을 공모하여 점유물을 수수한 행위는 횡령죄 실행에 불과하여 장물죄를 구성하지 않고, 점유자의 배신행위에 적극 가담한 경우 수수자에게는 횡령죄 공동정범이 성립한다.
- `sec5_2.breach_of_trust_no_receiving`  (negative/exception)
  배임행위로 취득되는 것은 재산상 이익일 뿐 재물이 아니므로, 배임죄를 범한 자는 장물죄의 본범이 될 수 없고 그 재물을 순차 취득한 자에게 장물취득죄가 성립하지 않는다.
- `sec5_2.intent_concurrence_required`  (negative/element)
  장물죄는 본범과의 의사합치를 요하므로, 본범의 의사에 반하여 장물을 절취하거나 강취한 경우에는 장물죄가 성립하지 않는다.
- `sec5_2.secret_taking_against_principal`  (negative/standard)
  본범이 갈취해 둔 재물을 본범의 의사에 반하여 몰래 절취한 경우에는 절도죄만 구성하고 장물취득죄는 성립하지 않는다는 판례가 소개되어 있다.
- `sec5_2.defrauding_principal_no_receiving`  (negative/exception)
  절도범으로부터 장물임을 알고 그 절취물을 편취 또는 갈취한 경우, 본범과 의사합치가 없으므로 절도범에 대한 사기죄 또는 공갈죄만 성립하고 장물취득죄는 성립하지 않는다.
- `sec5_2.lost_property_embezzlement`  (negative/exception)
  재산범죄 본범으로부터 점유를 이탈한 재물을 불법영득한 경우 장물임을 알고 있었더라도 점유이탈물횡령죄만 성립하고 장물취득죄는 성립하지 않는다.

- 판정: 

## E-03 post_outcome (22)

성립 여부가 아니라 죄수·사후행위 효과를 기술합니다. 결론을 막지 않습니다.

- `sec3_1.nonprincipal_group_member_acquisition`  (positive/standard)
  평소 본범과 공동하여 범죄집단을 이루었더라도 당해 범죄행위의 정범이 아닌 사람은 그 장물 취득을 불가벌적 사후행위로 볼 수 없다는 판례가 소개되어 있다.
- `sec3_2.embezzlement_purchaser_concurrence`  (positive/variant)
  횡령 매도 요청에 대한 매수 의사표시로 매수인에게 횡령방조가 성립하고, 현실 매도로 횡령이 기수에 이르면 횡령방조와 장물취득죄의 상상적 경합이 성립한다는 견해가 있다.
- `sec3_2.subsequent_participant`  (positive/definition)
  장물은 본범인 재산범죄에 의하여 영득한 재물이어야 하고 장물범은 본범에 대한 사후종범의 성격을 지니며, 본범 실행과정에서 교사·방조한 후 장물을 취득하면 횡령죄 교사와 장물취득죄의 경합범이 성립한다는 판례가 소개되어 있다.
- `sec3_2.used_to_defraud`  (positive/standard)
  장물을 수단으로 제3자를 기망하여 별개의 금품을 장물 대가로 편취하면 새로운 법익침해로서 절도죄와 별개의 사기죄가 성립하고 불가벌적 사후행위가 아니라는 통설 및 판례가 소개되어 있다.
- `sec3_2.cashier_check_payment`  (negative/standard)
  절취·습득한 자기앞수표를 음식대금 또는 현금교환에 사용하거나 절취한 열차승차권을 환불받는 행위는 기망이 수반되어도 별도 사기죄가 아니라 절도죄의 불가벌적 사후처분행위라는 판례가 소개되어 있다.
- `sec3_3.acquisition.subsequent_custody`  (exception/exception)
  장물취득 후 보관은 별도 장물보관죄를 구성하지 않으며, 장물성을 알고 보관하다가 후에 취득한 경우에도 보관은 취득에 흡수되어 장물취득죄만 성립한다.
- `sec3_3.transport.acquirer_self_transport`  (exception/exception)
  장물취득자가 스스로 운반한 경우 운반은 불가벌적 사후행위이므로 장물취득죄와 별도로 장물운반죄가 성립하지 않는다.
- `sec3_3.custody.embezzlement`  (negative/standard)
  장물을 보관하던 자가 이를 횡령한 경우 다수설 및 판례는 장물보관죄만 성립하고 횡령죄는 불가벌적 사후행위가 된다고 본다.
- `sec5_1.acquisition_transfer_nonpunishable_followup`  (negative/exception)
  장물임을 알고 취득한 뒤 이를 제3자에게 양도하더라도 장물취득죄만 성립하고 장물양도죄는 별도로 성립하지 않으며, 양도는 불가벌적 사후행위로 본다.
- `sec5_1.transport_storage_inclusive_offense`  (positive/variant)
  장물을 운반한 후 계속 보관한 경우 장물운반죄와 장물보관죄의 포괄일죄를 구성한다는 견해가 있다.
- `sec5_1.transport_storage_absorption`  (negative/variant)
  장물을 운반한 후 보관한 경우 보관은 운반의 불가벌적 사전행위로서 흡수되어 선행 장물운반죄만 성립한다는 견해가 있다.
- `sec5_1.later_brokering_concurrent_offenses`  (positive/variant)
  운반 또는 보관만 의뢰받아 이를 한 후 새로 매매 등의 의뢰를 받아 알선한 경우에는 경합범이라는 견해가 있다.
- `sec5_1.returned_property_later_brokering`  (positive/exception)
  보관하던 장물을 일단 반환한 뒤 곧바로 알선 의뢰를 받아 알선만 한 경우에는 장물보관죄와 장물알선죄의 경합범이 성립한다.
- `sec5_2.instigator_aider_concurrence`  (positive/exception)
  본범의 교사자 또는 방조자가 장물죄 구성행위를 한 경우에는 본범의 교사죄 또는 방조죄와 별도로 장물죄가 성립하고 경합범이 된다.
- `sec5_2.pursuit_right_theory`  (positive/variant)
  추구권설에 따르면 본범과의 의사합치는 장물죄의 요건이 아니며, 장물에 대한 소유자의 추구회복을 더 곤란하게 한 경우 절도죄 등과 장물죄가 상상적 경합할 수 있다.
- `sec5_2.resale_fraud_nonpunishable`  (negative/variant)
  장물임을 알고 취득한 물건을 양도 또는 알선하면서 이를 모르는 매수자로부터 대금을 편취한 경우, 대금 편취는 양도·알선의 당연한 결과인 불가벌적 사후행위이므로 장물죄 외에 사기죄는 성립하지 않는다는 견해가 있다.
- `sec5_2.resale_fraud_nonabsorption`  (positive/standard)
  장물의 양도·알선과 그 과정에서의 매수인 대금 편취는 보호법익의 대상과 성질이 구별되므로 어느 한 죄가 다른 죄에 흡수되지 않고 경합범이 성립한다는 견해가 제시되어 있다.
- `sec5_2.acquisition_brokering_relationship`  (positive/variant)
  선행 장물취득죄와 장물알선죄의 관계에 관하여 경합범이라는 견해와 상상적 경합이라는 견해가 있다.
- `sec5_2.storage_disposal_nonpunishable`  (negative/standard)
  장물보관을 의뢰받아 장물임을 알고 보관하다 임의 처분한 경우, 장물보관죄로 이미 소유자의 추구권을 침해하였으므로 그 후 횡령은 불가벌적 사후행위이고 별도 횡령죄를 구성하지 않는다는 것이 통설 및 판례이다.
- `sec5_2.storage_embezzlement_real_concurrence`  (positive/variant)
  불법원인급여물에 대한 횡령죄 성립을 긍정하는 입장에서는 장물보관죄와 횡령죄가 실체적 경합범이 된다는 견해가 있다.
- `sec5_2.concealment_evidence_imaginary_concurrence`  (positive/variant)
  타인의 형사사건 죄증을 인멸하기 위하여 장물을 은닉한 경우 장물보관죄와 증거인멸죄는 상상적 경합이라는 견해가 제시되어 있다.
- `sec5_2.bribe_receipt_imaginary_concurrence`  (positive/standard)
  장물임을 알면서 이를 뇌물로 수수한 경우 수뢰죄와 장물취득죄는 상상적 경합범이 된다.

- 판정: 

## E-04 variant — 채택 결정 필요 (22)

학설이 대립하는 카드입니다. 어느 견해를 채택할지 정해야 조립할 수 있습니다.

- `sec3_2.expanded_pursuit_right_definition`  (positive/variant)
  권리자의 추구 가능성을 요구하면서도 장물의 취득원인을 재산권 침해 범죄로 넓게 보아 반드시 재산범죄에 한정하지 않는 견해가 소개되어 있다.
- `sec3_2.manageable_energy`  (positive/variant)
  관리 가능한 동력은 본범의 영득 대상인 재물에 포함되므로 장물죄에서 별도의 형법 제346조 준용규정이 없어도 장물이 될 수 있는 재물에 포함된다는 견해가 소개되어 있다.
- `sec3_2.stored_information`  (positive/variant)
  하드디스크 등에 저장되어 물리적으로 관리 가능한 정보는 현행 형법 제346조 해석으로 재물성과 장물성이 인정된다는 견해가 있다.
- `sec3_2.embezzlement_purchaser_receiving`  (positive/variant)
  보관자가 불법영득의사를 가지고 물건을 매도하고 그 정을 아는 매수인이 인도받은 경우, 매도 의사 또는 업무상횡령의 기수와 동시에 물건 또는 금원이 장물이 되어 매수인에게 장물취득죄가 성립한다는 견해 및 판례가 소개되어 있다.
- `sec3_2.voidable_transaction_positive`  (positive/variant)
  취소할 수 있는 법률행위에 따른 재물이라도 취소권 행사 전 피해자가 장래 회복청구권을 보유하므로 장물성을 인정할 수 있다는 견해가 있다.
- `sec3_2.illegal_cause_benefit_illegal_state`  (positive/variant)
  위법상태유지설에 따르면 불법원인급여물에 피해자의 추구권이 없더라도 본범이 조성한 상태가 위법하면 장물성이 인정된다.
- `sec3_2.substitute_property_benefit`  (positive/variant)
  이익관여설 또는 공범설은 본범 이익에 대한 관여를 본질로 보아 대체장물에도 장물죄 성립을 인정한다.
- `sec3_2.non_property_crime`  (negative/variant)
  재산범죄가 아닌 본범으로 취득한 재물은 원칙적으로 장물이 아니지만, 사기도박 또는 위조통화·문서 행사가 별도 사기죄를 구성해 취득한 재물은 장물성이 인정되고, 광업법 위반 광물 등 예외를 인정하는 견해도 있다.
- `sec3_2.own_property_crimes_positive`  (positive/variant)
  권리행사방해죄나 점유강취·준점유강취죄처럼 자기 물건이 범행객체인 재산범죄도 재물을 대상으로 한 재산범죄이므로 장물죄의 본범이 될 수 있다는 견해가 있다.
- `sec3_2.own_property_crimes_negative`  (negative/variant)
  권리행사방해죄나 점유강취·준점유강취죄처럼 자기 물건이 범행객체인 재산범죄는 자기 물건에 대한 영득행위가 있을 수 없으므로 장물죄의 본범이 될 수 없다는 견해가 있다.
- `sec3_3.acquisition.third_party`  (positive/variant)
  장물취득은 자신을 위한 취득에 한정되지 않고 제3자를 위한 취득도 포함한다.
- `sec3_3.acquisition.indirect_possession`  (positive/variant)
  간접점유를 취득한 경우에도 장물취득죄가 성립한다.
- `sec3_3.acquisition.resale`  (positive/variant)
  본범으로부터 직접 취득하지 않고 전매로 취득한 경우에도 장물취득죄 성립이 가능하다.
- `sec3_3.acquisition.food_consumption`  (positive/variant)
  절취한 음식의 공동 섭취 또는 단독 소비가 장물취득죄를 구성하는지에 관하여, 공동 섭취는 부정하는 견해, 단독 섭취만 긍정하는 견해 및 소비 일반을 긍정하는 견해가 대립한다.
- `sec3_3.transfer.knowledge_and_subsequent_transfer`  (positive/variant)
  장물양도죄에서 취득 당시 장물성 인식의 필요 여부 및 장물성을 알고 취득한 뒤 양도한 경우 별도 양도죄 성립 여부에 관하여 다수설과 반대 견해가 대립한다.
- `sec3_3.brokering.completion_doctrines`  (positive/variant)
  장물알선죄의 성립 시점에 관하여 주선행위만으로 충분하다는 견해, 알선에 의한 계약 성립을 요구하는 견해 및 점유 이전까지 요구하는 견해가 대립한다.
- `sec4_3.acquisition_gain_intent`  (positive/variant)
  장물죄에서 장물취득의 경우에는 영득의사를, 그 밖의 양도·운반·보관·알선의 경우에는 이득의사를 각각 필요로 한다는 견해가 있다.
- `sec4_3.illegal_gain_intent_all_types`  (positive/variant)
  장물죄 전반에 불법영득의사가 필요하되, 운반·보관·알선의 경우에는 타인의 불법영득을 유지하거나 다른 사람에게 불법영득을 시키려는 의사가 필요하다는 견해가 있다.
- `sec5_1.later_brokering_near_time_single_offense`  (positive/variant)
  운반 또는 보관 후 새로 알선을 의뢰받은 경우에도 각 행위가 시간적으로 근접하면 최종 결과인 장물알선죄의 일죄만 성립한다는 지배적 견해가 있다.
- `sec5_2.resale_fraud_concurrence`  (positive/variant)
  장물임을 알고 취득한 물건을 다시 양도 또는 알선하면서 이를 모르는 매수자로부터 대금을 편취한 경우 장물죄와 사기죄가 경합한다는 견해가 있다.
- `sec5_2.concealment_evidence_only`  (negative/variant)
  타인의 죄증을 인멸할 목적으로 장물을 보관한 경우 이득의 의사가 없으므로 증거인멸죄만 성립한다는 견해가 있다.
- `sec5_2.concealment_receiving_only`  (positive/variant)
  타인의 죄증 인멸 목적으로 장물 점유를 이전받아 보관한 경우, 죄증 인멸에 이바지함을 용인한 것이므로 법조경합에 따라 장물보관죄만 성립한다는 견해가 있다.

- 판정: 

## E-05 assessment_standard (17)

정의·판단기준. 새 역할이며 결론에 영향을 주지 않고 모델에 전달만 됩니다.

- `sec1.conduct_types`  (positive/definition)
  장물죄는 장물을 취득·양도·운반·보관하거나 이러한 행위를 알선함으로써 성립하는 범죄이다.
- `sec1.object_movable_property`  (positive/definition)
  장물죄의 객체는 재물이다.
- `sec3_2.pursuit_right_definition`  (positive/definition)
  장물이란 재산범죄에 의하여 영득된 재물로서 피해자가 법률상 반환을 청구할 수 있는 물건이라는 추구권설의 정의가 소개되어 있다.
- `sec3_2.illegal_state_definition`  (positive/variant)
  위법상태유지설은 장물을 재산권 침해 범죄로 취득한 재산으로 정의하고, 피해자의 법률상 추구 가능성이나 반드시 재산범죄에 의한 영득을 요구하지 않는다.
- `sec3_2.acquisition_completion_theory`  (positive/variant)
  장물성은 본범의 기수·미수 여부가 아니라 본범에 의한 재물 영득이 시간적으로 종결되었는지를 기준으로 판단해야 한다는 재물영득설이 있다.
- `sec3_2.substitute_property`  (negative/definition)
  장물의 매각대금·교환물·장물인 금전으로 매입한 물건 등 대체장물은 원칙적으로 장물성이 인정되지 않지만, 별개의 재산범죄를 통해 불법적으로 영득한 것이 인정되면 새로운 원인에 의해 장물이 될 수 있다.
- `sec3_2.shopping_cart`  (negative/standard)
  정상 제품의 마트 쇼핑카트가 고물상에 보관된 사안에서, 방치된 쇼핑카트를 마트가 정기 회수하고 일부가 파지 운반에 사용된 사정 등을 고려하여 재산범죄로 영득된 장물이라고 볼 수 없어 장물보관죄가 성립하지 않는다는 판례가 소개되어 있다.
- `sec3_3.acquisition.definition`  (positive/definition)
  장물의 취득은 유상·무상을 불문하고 소유권에 기한 사실상 처분권을 갖게 되는 경우이며, 점유 이전과 사실상 처분권 취득이 필요하다.
- `sec3_3.acquisition.loan_for_use`  (negative/definition)
  장물의 사용대차는 당해 물건을 그대로 반환해야 하고 처분권을 취득하지 않으므로 취득이 아니라 보관에 해당한다.
- `sec3_3.knowledge.conditional_intent`  (positive/definition)
  장물죄에서 장물 인식은 확정적 인식이 아니라 장물일 수 있다는 의심 정도의 미필적 인식으로도 충분하며, 인정 여부는 소지자 신분·재물 성질·거래 대가 등 상황을 참작한다는 판례가 소개되어 있다.
- `sec3_3.transfer.definition`  (positive/definition)
  장물양도는 장물을 제3자에게 수여하는 행위이고, 양도계약의 성립만으로는 부족하며 현실적 수여, 즉 점유 이전을 요한다.
- `sec3_3.transport.definition`  (positive/definition)
  장물운반은 장물을 장소적으로 이전하는 행위이며 유상·무상을 불문한다.
- `sec3_3.custody.definition`  (positive/definition)
  장물보관은 위탁을 받아 장물을 자기 점유 아래 두는 것이며, 장물에 대한 사실상 처분권이 없다는 점에서 취득과 구별된다.
- `sec3_3.brokering.definition`  (positive/definition)
  장물알선은 장물의 취득·양도·운반·보관 행위를 매개·주선하는 행위로서, 본범 또는 장물취득자와의 합의나 추정적 승낙 아래 이루어져야 하며, 단순한 주선계약만으로는 부족하고 추가 주선행위를 요한다.
- `sec4_1.inference_of_knowledge`  (positive/standard)
  장물성 인식 여부는 장물 소지자의 신분, 재물의 성질, 거래 대가 및 그 밖의 상황을 종합적으로 참작하여 인정할 수 있다.
- `sec5_2.intent_concurrence_implied`  (positive/definition)
  장물죄에서 본범과의 의사합치는 사실상 또는 묵시적인 것으로도 충분하다.
- `sec6_1.indictment_underlying_offense_unspecified`  (positive/definition)
  장물죄에서 장물은 절도·강도·사기·공갈·횡령 등 재산범죄로 영득한 물건이면 충분하고, 그 중 어느 범죄로 영득되었는지를 구체적으로 명시할 필요가 없다는 것이 판례이다.

- 판정: 

## E-06 waiver (7)

요건 불요 — 성립을 막지 않습니다.

- `sec3_2.predicate_property_crime`  (positive/element)
  장물의 출처가 되는 본범은 재물죄 또는 재물영득죄인 재산범죄의 구성요건에 해당하는 위법행위이면 충분하고, 본범의 유책성, 객관적 처벌조건, 정식기소 또는 유죄 확정판결은 요구되지 않는다.
- `sec3_3.transport.completion`  (positive/variant)
  장물운반죄는 사실상 운반행위가 개시되면 기수가 되고 목적 달성까지 필요하지 않다는 견해가 있으며, 필자는 이를 타당하다고 본다.
- `sec4_1.conditional_knowledge`  (positive/element)
  장물성의 인식은 확정적 인식까지 필요하지 않고 장물일지도 모른다는 의심 정도의 미필적 인식으로 충분하다.
- `sec4_1.no_specific_principal_offense_knowledge`  (negative/exception)
  장물죄에서 본범의 구체적 범죄사실, 본범자·피해자의 신원, 범행 일시·방법 등에 관한 인식은 필요하지 않고, 누군가의 재산범죄로 영득된 물건이라는 인식이면 충분하다.
- `sec4_2.knowledge_of_recovery_right`  (exception/exception)
  장물이라는 정에 대한 인식만을 요하고, 피해자에게 추구권이 있다는 사실에 대한 인식은 필요하지 않다. 피해자에게 추구권이 없는 경우는 고의의 문제가 아니라 객관적 구성요건에 해당하지 않는 문제로 본다.
- `sec4_3.no_independent_gain_intent`  (negative/variant)
  다수설은 장물죄에 고의와 별개의 주관적 구성요건으로 영득의사 또는 이득의사가 필요하지 않다고 본다.
- `sec6_1.principal_and_victim_identification_not_required`  (negative/element)
  장물죄에서 본범이 누구인지 및 본범의 피해자가 누구인지에 관한 구체적 인식이나 특정은 요구되지 않는다.

- 판정: 

---

# F. 장물죄 구조 설계

## F-01 불가벌적 사후행위 — 재설계안

배치 001 B-02 에서 제 boundary 안을 반려하시며 **cross-unit 흡수 규칙**이 맞다고 하셨습니다.
제시하신 구조를 그대로 옮기면:

```
1. 장물보관죄 구성요건 판단 — 독립 완료
2. 후속 횡령죄 구성요건 판단 — 필요하면 별도 수행
3. 조건 확인: 동일 행위자 · 동일 장물 · 선행 장물보관 성립 · 후속 영득행위
4. embezzlement_punishment_suppressed_by_post_offense 발화
5. 출력: "장물보관죄는 성립하고, 후속 횡령은 불가벌적 사후행위로 별죄를 구성하지 않는다"
```

구현 시 확인이 필요한 점이 하나 있습니다. 현재 호스트는 **쟁점별로 유닛을 독립 실행**하고
유닛 간 사실을 주고받지 않습니다. 4번의 cross-unit 규칙을 넣으려면 두 방법 중 하나가 필요합니다.

- **(가) 호스트 레벨 후처리** — 두 유닛 결과를 받은 뒤 조건을 검사해 브리핑에 흡수 사실을 추가.
  SCL 변경 없음. 단 규칙이 SCL 밖에 존재하게 됩니다.
- **(나) shared module** — `relative_property_crime_exception` 처럼 의존성 브리지를 받는
  공유 모듈로 만듦. SCL 안에 남지만 브리지 배선이 필요합니다.

- 제안: **(나)**. 이미 shared module 기제가 있고, (가)는 "결론은 Scallop 이 계산한다" 는
  원칙에서 벗어납니다.
- 판정: 

## F-02 어휘 체계 최종 확인

배치 001 B-01 에서 재산죄 어휘를 승인하셨습니다. 새 역할까지 반영한 최종 어휘는:

| 역할 | 뜻 | 결론 영향 |
|---|---|---|
| `component` | 요건 인정 경로 | 성립 방향 |
| `bar` | 성립 차단 | 불성립 |
| `boundary` | 다른 죄로 이동 | 불성립 + 이동 죄명 |
| `waiver` | 요건 불요 | **없음** |
| `assessment_standard` | 정의·판단기준 | **없음** (신설) |
| `post_outcome` | 죄수·사후행위 효과 | **없음** |

- 판정: 

## F-03 극성/규범종류 분리 (배치 001 B-03-a) 적용 범위

`polarity` 에 `exception` 이 들어간 카드가 장물죄 146장 중 **16장**입니다.
`norm_kind=exception` 은 유지하고 `polarity` 는 negative/positive 로 바로잡아야 합니다.

기존 룰베이스에도 같은 혼동이 있습니다 — P2 96건 + 재산죄 46건 = **142건**
입니다. 배치 001의 극성 기반 검출이 이 카드들을 통과시켰습니다.

- 제안: 장물죄 16장은 적재 전 교정. 기존 룰베이스 142건은 **별도 배치**로 분리 (이번에
  같이 하면 장물죄 적재가 무기한 늦어집니다).
- 판정: 

