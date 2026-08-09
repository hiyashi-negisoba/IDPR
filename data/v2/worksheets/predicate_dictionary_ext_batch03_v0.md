# Predicate 사전 확장 — 배치 ③ 총칙 위법성조각사유 (제20·22·23·24조) v0

[predicate_dictionary_ext_batch02_v2.md](predicate_dictionary_ext_batch02_v2.md)의 연장. 이
배치는 21조(정당방위, pilot v0-v2에서 이미 저작 완료)와 같은 Unlawfulness 축의 나머지
4개 조문(정당행위·긴급피난·자구행위·피해자의 승낙)을 다룬다. 넷 다 구조가
"상황요건 + 행위요건 + 상당성"으로 21조와 병렬이라 형식은 재사용하되, id는 21조의
`reasonable_grounds`를 그대로 돌려쓰지 않는다 — 각 조문의 상당성 기준이 서로 다르다는
게 판례 자체의 명시적 입장이다(예: "긴급피난의 상당한 이유는 정당방위의 상당한 이유보다
더 엄격한 요건").

---

## 제20조 정당행위 (법령에 의한 행위 / 업무로 인한 행위 / 사회상규에 위배되지 않는 행위)

| id (가칭) | canonical_meaning | 근거(section_path) |
|---|---|---|
| `legal_element.act_pursuant_to_law_or_business` | 법령에 의한 행위 또는 정당한 업무로 인한 행위에 해당한다 | Ⅱ, Ⅲ |
| `legal_element.act_not_against_social_norms` | 사회상규에 위배되지 아니하는 행위에 해당한다(동기·목적의 정당성/수단·방법의 상당성/법익균형성/긴급성/보충성 5요소 종합판단) | Ⅳ.4 |
| `doctrine.justifiable_act_defeat` | 위 둘 중 하나에 해당하면 위법성이 조각된다(DEFEAT) | Ⅰ.1 |

`requires = ANY(act_pursuant_to_law_or_business, act_not_against_social_norms)`. 다수설
(사회상규가 일반원리이고 나머지는 예시)과 소수설(세 유형이 병렬)이 갈리지만, **어느
쪽이든 predicate 구조는 같다** — `ANY`는 "적어도 하나"만 요구하므로 다수설의
포섭관계나 소수설의 병렬관계 둘 다 계산상 같은 결과를 낸다. 학설 대립이 DSL
구조에 영향을 주지 않는 드문 사례라 기록해둔다.

**검수 필요 없음** — 5요소 사회상규 판단기준(Ⅳ.4 대법원 판시)과 방대한 사례군(Ⅳ.5)은
전부 `act_not_against_social_norms`의 `legal_standard`로 흡수, 별도 predicate 없음.

---

## 제22조 긴급피난

| id (가칭) | canonical_meaning | 근거(section_path) |
|---|---|---|
| `legal_element.imminent_danger` | 자기 또는 타인의 법익에 대한 현재의 위난이 있었다 | Ⅱ.1 |
| `legal_element.act_to_avert_danger` | 그 위난을 피하기 위한 행위(피난의사 포함)를 하였다 | Ⅱ.2 |
| `legal_element.necessity_of_avoidance` | 피난행위에 상당한 이유가 있었다(보충성·최소침해·우월적 이익·수단의 사회윤리적 상당성 4요소) | Ⅱ.3 |
| `legal_element.duty_bound_to_endure_danger` | 행위자가 위난에 대비하는 것을 직업·고유업무로 하여 위난을 피하지 못할 책임이 있는 자(군인·경찰관·의사·소방관 등)에 해당한다 | Ⅲ |
| `doctrine.necessity_defeat` | 위 세 요건이 갖춰지고 행위자가 위난을 피하지 못할 책임 있는 자가 아니면 위법성이 조각된다(DEFEAT) | Ⅳ |
| `doctrine.excessive_necessity` | 상당성을 넘은 피난(과잉피난)은 21조 2·3항 준용(정황에 의한 형 감면/야간·공포 등으로 인한 때 불벌) | Ⅴ.1 |

`necessity_defeat.requires = ALL(imminent_danger, act_to_avert_danger,
necessity_of_avoidance, NOT(duty_bound_to_endure_danger))` — 배치①에서 확정한 원칙
("부정은 predicate이 아니라 requires의 NOT()이 담당") 그대로 적용, `duty_bound_to_
endure_danger`는 긍정형으로 짓고 게이트에서 부정.

**신규 doctrine — 의무의 충돌(Ⅵ, 22조 안에 있지만 긴급피난과 별개 법리)**:

| id (가칭) | canonical_meaning | 근거(section_path) |
|---|---|---|
| `legal_element.conflicting_legal_duties` | 둘 이상의 법적 작위의무가 동시에 부과되어 그중 하나만 이행할 수 있는 긴급상태에 있었다 | Ⅵ.1, Ⅵ.4 |
| `legal_element.higher_or_equal_duty_performed` | 이행한 의무가 방치한 의무보다 상위이거나 최소한 동등한 가치였다 | Ⅵ.4 |
| `doctrine.conflict_of_duties_defeat` | 위 요건이 갖춰지면 부작위범의 위법성이 조각된다(DEFEAT) | Ⅵ.5 |

**검수 필요 — 18조 `omission_bundle`과의 관계.** 워크시트가 명시: "의무의 충돌은
작위의무 사이에서만 문제되고", "부진정부작위범의 위법성과 관련하여 문제가 된다." 즉
이 doctrine은 **배치②의 `bundle.omission_bundle`이 이미 충족된 상황을 전제**한다 —
`failure_to_act`(방치한 의무 쪽)는 이미 그 부작위범 offense의 Elements 단계에서 성립돼
있고, `conflict_of_duties_defeat`는 그 Unlawfulness 단계에서 "그래도 정당화된다"는
걸 추가로 판단한다. 두 층(Elements의 omission_bundle / Unlawfulness의 conflict_of_
duties)이 자연스럽게 연결되는지는 2패스에서 실제 저작해봐야 확인된다 — 이번엔
predicate 후보만 제시.

**오상피난(Ⅴ.2)은 새 HOLD 항목이 아니다.** 워크시트 원문이 "오상피난은... 오상방위와
마찬가지로 위법성조각사유의 전제사실에 관한 착오 문제가 된다"고 직접 명시한다 — pilot
v2가 21조에서 이미 HOLD해둔 "위법성조각사유의 전제사실 착오" 문제가 **정당방위
전용이 아니라 모든 정당화사유에 공통되는 일반 논점**이라는 걸 22조 원문이 재확인해줄
뿐이다. 아래 23·24조도 각각 오상자구행위·(피해자 승낙 쪽은 명시 언급 없으나 구조상)
같은 범주다. HOLD 범위를 "21조 오상방위"에서 "모든 정당화doctrine 공통의 전제사실
착오 문제"로 넓혀 기록한다 — 새로 결정할 것은 없고, 기존 HOLD가 이번에 일반화됨을
확인했을 뿐이다.

---

## 제23조 자구행위

| id (가칭) | canonical_meaning | 근거(section_path) |
|---|---|---|
| `legal_element.claim_unpreservable_by_legal_process` | 법정절차에 의하여 (자기의) 청구권을 보전하기 불능한 상태였다 | Ⅱ.1 |
| `legal_element.act_to_prevent_unenforceability` | 청구권의 실행불능 또는 현저한 실행곤란을 피하기 위한 행위(자구의사 포함)를 하였다 | Ⅱ.2 |
| `legal_element.necessity_of_self_help` | 자구행위에 상당한 이유가 있었다(이중의 보충성 + 최소침해, 21·22조보다는 균형성 요건이 완화됨) | Ⅱ.3 |
| `doctrine.self_help_defeat` | 위 세 요건이 갖춰지면 위법성이 조각된다(DEFEAT) | Ⅲ |
| `doctrine.excessive_self_help` | 상당성을 넘은 자구행위(과잉자구행위)는 21조 2항만 준용(형의 임의적 감면) | Ⅳ.1 |

**검수 필요 — `excessive_self_help`는 `excessive_necessity`(22조)와 구조가 다르다.**
22조 과잉피난은 21조 2항(형 감면)과 3항(야간·공포 등 불벌)을 **둘 다** 준용하지만,
23조 과잉자구행위는 워크시트가 명시적으로 "긴급피난의 경우와는 달리 … 형법 제21조
제3항은 준용되지 아니한다"고 적는다 — 2항만 준용(형 감면 MODIFY만 있고, 3항 같은
EXEMPT 변형이 없음). 21조 `excessive_defense`가 이미 MODIFY+EXEMPT 두 효과를
가졌다면, `excessive_self_help`는 그 doctrine을 통째로 재사용할 수 없고 MODIFY
부분만 가진 **별도 doctrine으로 저작**해야 한다 — 이건 확정 사항으로 기록(구조가
다르다는 게 조문 자체의 명문 규정이라 검수랄 것도 없이 확정).

오상자구행위(Ⅳ.2)도 22조와 같은 논리로 기존 HOLD 범주에 편입 — 새 항목 아님.

---

## 제24조 피해자의 승낙 (+ 추정적 승낙)

| id (가칭) | canonical_meaning | 근거(section_path) |
|---|---|---|
| `legal_element.valid_consent_by_disposer` | 그 법익을 처분할 수 있는 자(승낙능력 있는 법익주체)의 승낙이 있었다 | Ⅱ.1 |
| `legal_element.harm_caused_pursuant_to_consent` | 행위자가 그 승낙을 인식하고, 승낙의 내용·범위 안에서 그 승낙에 의하여 법익을 훼손하였다 | Ⅱ.2 |
| `legal_element.statutory_bar_on_consent` | 승낙이 있어도 처벌하는 법률의 특별한 규정(촉탁·승낙살인죄 등)이 그 행위에 적용된다 | Ⅱ.3 |
| `legal_element.consent_not_against_social_norms` | 그 승낙(및 승낙에 의한 행위)이 윤리적·도덕적으로 사회상규에 반하지 아니한다 | Ⅱ.4 |
| `doctrine.victim_consent_defeat` | 위 요건이 갖춰지고 statutory_bar가 없으면 위법성이 조각된다(DEFEAT) | Ⅲ |

`victim_consent_defeat.requires = ALL(valid_consent_by_disposer,
harm_caused_pursuant_to_consent, NOT(statutory_bar_on_consent),
consent_not_against_social_norms)` — `statutory_bar_on_consent`도 배치①·22조와 같은
긍정형+`NOT()` 패턴.

**신규 — 추정적 승낙(Ⅳ, 24조 준용 별도 doctrine)**:

| id (가칭) | canonical_meaning | 근거(section_path) |
|---|---|---|
| `legal_element.presumed_consent` | 현실적 승낙은 없었으나 행위 당시 모든 객관적 사정에 비추어 피해자가 그 내용을 알았다면 당연히 승낙하였을 것으로 예견되었다(행위자의 성실한 검토를 거침) | Ⅳ.1, Ⅳ.4 |
| `legal_element.actual_consent_unobtainable` | 현실적 승낙을 적시에 얻는 것이 불가능하였다(추정적 승낙의 보충성) | Ⅳ.4 |
| `doctrine.presumed_consent_defeat` | 위 요건이 갖춰지고 statutory_bar가 없으며 사회상규에 반하지 않으면 위법성이 조각된다(DEFEAT) | Ⅳ.5 |

**검수 필요 — 추정적 승낙 doctrine이 20조가 아니라 24조를 준용한다는 점을 명시.**
워크시트 Ⅳ.5가 학설 대립("사회상규에 위배되지 않는 행위"로 볼지 vs "피해자의 승낙"의
연장으로 볼지)을 정리하며 "추정적 승낙은 기본적인 구조가 피해자의 승낙과 유사하고
그 요건도 상당 부분 중첩되므로 … 본조(24조)를 준용하는 것이 타당하다"는 저자의
결론을 명시한다 — 이 결론을 따라 `presumed_consent_defeat`가
`consent_not_against_social_norms`/`statutory_bar_on_consent`를 **24조에서 그대로
재사용**하도록 구성했다(20조의 `act_not_against_social_norms`를 쓰지 않음). 사용자
확인 필요.

**신규 predicate 아님 — 양해(사실상 동의, 구성요건해당성 배제).** 다수설이 구별하는
"양해"(주거침입죄의 거주자 동의처럼 구성요건해당성 자체를 배제)는 Unlawfulness의
`victim_consent_defeat`가 아니라 그 **offense 고유의 canonical_element**(예:
주거침입죄의 "침입" predicate 자체가 "거주자의 의사에 반하여"를 포함) 문제다 —
24조가 만드는 predicate는 여기 해당하지 않는다는 점만 기록, 2패스에서 offense별로
확인.

---

## 이번 배치 신규 스키마·DSL primitive 필요 여부

**없음.** 20·22·23·24조 전부 기존 `LegalElementDef`/`DoctrineDef(stage=unlawfulness)`/
`ElementExpression`(`ALL`/`ANY`/`NOT`)로 표현된다. 22조의 의무의 충돌이 18조
omission_bundle과 맞물리는 지점만 2패스 확인사항으로 남긴다.
