# Predicate 사전 확장 — 배치 ⑧ 방화·문서 (제164·225·227·231·234·239조) v1

[predicate_dictionary_ext_batch08_v0.md](predicate_dictionary_ext_batch08_v0.md)에 대한
사용자 검수 6건 반영. v0 표의 id·구조는 특별히 언급하지 않는 한 그대로 유지 — 아래는
정정 사항만 다룬다.

---

## 수정 1 — 공유 predicate(`commencement_of_execution`/`legal_element.intent`)의
canonical_meaning을 offense별로 재정의하지 않는다

**v0 오류**: 방화군 절에서 "`commencement_of_execution`... canonical_meaning을 164에
맞게 특화"라고 쓰고, `legal_element.intent`의 legal_standard에 164 특유 사실관계를
"흡수"한다고 썼다. 두 predicate는 이미 전역 공유 정의(각각 15개 파일럿·배치② 13조에서
확정)다 — `predicate_dictionary_draft_v1_feedback.md`/`ext_batch02_v0.md`가 이미 세워둔
원칙(신분범 등 offense 고유 인식 대상이 필요하면 `intent`를 고쳐 쓰지 않고 별도 병렬
legal_element를 만들거나, 아예 정의는 그대로 두고 offense 저작 시 참고 서술로만 남긴다)을
이번 배치에서 스스로 어긴 것.

**정정**:
- `commencement_of_execution` — 공유 정의(구성요건적 행위의 개시, 법적 기준에 대한
  포섭판단) 그대로 재사용. 164의 "점화가 착수", 225·231의 "위조·변조 의사를 확정적으로
  문서에 표시"는 predicate 정의가 아니라 **그 offense를 저작할 때 이 predicate가 어떤
  사실관계에 대응하는지 적어두는 authoring 메모**로 격하한다 — canonical_meaning이나
  legal_standard 필드에 넣지 않는다.
- `legal_element.intent` — 공유 정의(객관적 구성요건요소에 해당하는 사실의 인식+용인)
  그대로 재사용. 164의 "주거사용·현존 인식은 미필적 고의로 족함", 227의 "오기·관행에 의한
  누락은 고의 부인"도 같은 이유로 정의에서 빼고 offense 저작 메모로만 남긴다.
- 164 결과적가중범 절의 `aggravated_result_attribution`도 같은 문제였다(v0 "검수 필요
  1"이 "canonical_meaning에 '고의로 인한 경우도 포함'을 명시"라고 쓴 부분) — **수정
  제안이 아니라 확인 필요 항목으로 격하**한다. 164 판례의 부진정결과적가중범 취급이 기존
  공유 predicate의 정의 범위에 이미 포함되는지만 확인하고, 이 배치 문서에서 정의를
  고치자고 제안하지 않는다 — 정말 전역 정의 수정이 필요하다고 판단되면 그건 이 배치의
  결정 사항이 아니라 별도 결정 지점(예: 해당 predicate를 처음 정의한 지점, 또는 전체
  결과적가중범 조문을 모아 보는 시점)의 일이다.

---

## 수정 2 — `ground_fact.seal_or_signature_object` → `legal_element.seal_or_signature_object`

225의 `public_document_object`, 231의 `private_document_object`와 같은 이유다 —
"인장·서명·기명·기호이다"라는 판정이 법인·단체 명의 포함 여부 등 법적 성질 판단을
수반하므로 raw fact(`ground_fact`)가 아니라 `legal_element`다. id를
`legal_element.seal_or_signature_object`로 재분류.

---

## 수정 3 — 239 "부정사용"은 HOLD가 아니라 source-resolution 문제였다: 238조 원문을
열람해 정의 확정

v0가 "카드에 정의가 없다"며 HOLD로 끝낸 것은 이번 각칙 방법론(카드 → 안 되면 원문 주석 →
주석이 다른 설명을 직접 참조하면 그 설명까지 확인)의 3단계에서 멈춘 것이었다. 239조 주석이
"[공인 등 위조·부정사용죄]에서 설명한 것과 대체로 같다"고 238조를 명시적으로 지목했으므로
238조 원문(`/data5/jaehoonjeong/sp_qwen/data/serve/commentary_chunks/docs.parquet`,
`law_id=001692`, `article_no="제238조"` — 카드 없음, 51개 조문 워크시트 범위 밖이라
이번에 직접 열람)까지 확인해 정의를 확정한다.

238조 Ⅰ.3(행위)·Ⅱ.2 원문: "[부정사용은] (권한)을 남용하여 부당하게 사용하는 것을
말한다. 즉 위조가 공인 등 자체를 거짓으로 만드는 것인데, 부정사용은 이미 진정하게
만들어진 공인 등을 부정하게 사용하여 사용의 진정을 해한다는 점에서 위조와 차이가 있다" /
"공기호의 부정사용은 진정하게 만들어진 공기호를 권한 없는 자가 사용하든가, 권한 있는
자라도 권한을 남용하여 부당하게 사용하는 행위를 말하고".

**신규 predicate**:

| id (가칭) | canonical_meaning | 근거 |
|---|---|---|
| `legal_element.improper_use_of_genuine_seal` | 이미 진정하게 성립된 타인의 인장·서명·기명·기호를, 사용할 권한 없는 자가 사용하거나 권한 있는 자가 그 권한을 남용하여 위임된 범위를 벗어나 사용하였다(위조가 인장·서명 자체를 거짓으로 만드는 것이라면, 부정사용은 이미 진정한 인장·서명의 사용상 진정성을 침해하는 것이라는 점에서 위조와 구별된다) | 238조 Ⅰ.3, Ⅱ.2(원문, 239조가 참조 지시) |

`art239_sec1_3.deceived_nominee_manifestation_not_improper_use`(명의자를 기망해 인영·
서명을 현출시킨 뒤 사용해도 명의자의 권한을 수여받아 행사한 것이므로 부정사용이 아니다)는
위 predicate의 canonical_meaning에 NOT 조건으로 흡수.

238조 열람으로 부수 확인된 사항(239 저작 시 참고): 238조 Ⅱ.2가 "부정사용"과 "부정사용한
것의 행사"를 사례로 명확히 구별한다(허가량 초과 벌채목에 철제극인 타기=부정사용, 그 나무를
반출만 한 것은 아직 행사 아님; 절취 번호판을 다른 차에 부착=부정사용, 그 차를 운행=행사).
이는 239조 자체의 ①(위조·부정사용)과 ②(행사)가 정확히 같은 2단계 구조임을 재확인해준다 —
`improper_use_of_genuine_seal`(①)과 v0 A절의 `utterance_conduct`(②)가 순차적으로 별개
행위라는 점이 238조 사례로 뒷받침된다.

`seal_or_signature_object`의 명의 실재성 쟁점(사자·허무인 포함 여부)은 238조에도 명확한
언급이 없어 HOLD 유지 — 이건 source-resolution 미완료가 아니라 실제 법리 미확정 문제.

---

## 수정 4 — `forgery_without_authority` 재사용 판단에서 schema argument typing 논의 삭제

v0가 "225·231·239 재사용이 안전한지는 스키마 arguments를 entity로 다형화해야 하는지에
달렸다"고 쓴 것은 잘못된 프레이밍이었다 — predicate DSL은 애초에 object argument 타입을
선언해 호출하는 함수형 구조가 아니다. 판단은 훨씬 단순하다:

- 225(공문서)·231(사문서)·239(인장)에서 "권한 없이 타인 명의를 현출한다"가 **동일한
  법적 판단**이면 → `forgery_without_authority` 공유 유지.
- 실제로 법적 판단기준이 다르다면 → 그때 분리.

세 조문 모두 "명의자의 명시적·묵시적 승낙이 있으면 위조가 아니다 / 권한 범위 내 남용은
위조가 아니다 / 위임범위 초과는 위조다"라는 동일한 3갈래 기준을 공유한다(225
`author_instruction_or_consent`, 231 `authorized_creation`/`comprehensive_delegation`/
`authority_abuse`, 239 `authorized_manifestation_not_forgery`) — **공유 확정**. entity
다형화 검토 항목은 이슈 목록에서 삭제한다.

---

## 수정 5 — 227의 간접정범 doctrine 후보 삭제

v0가 남겨둔 `doctrine.nonofficial_cannot_be_indirect_perpetrator_of_status_offense`는
불필요 — **삭제**. `official_with_writing_authority`가 FALSE면 227의 Elements 자체가
불성립하므로(진정신분범, 정범적격 없음) 별도 predicate로 이 결론을 다시 표현할 필요가
없다. "신분 없는 자가 신분자를 도구로 쓰는 간접정범" 일반 문제는 33조(배치⑤)가 이미
다루는 영역이고, 그 architecture-compatibility 확장은 34조 검토 범위에서 함께 처리한다 —
227 고유 predicate/doctrine을 만들지 않는다.

225의 `deceived_official_no_indirect_perpetration`(→ `forgery_without_authority`
canonical_meaning 경계로 흡수, v0 그대로 유지)과의 대조도 정리된다 — 225·227 둘 다
"간접정범 불성립"이라는 결론은 같지만, 227은 **predicate 자체가 불필요**(정범적격
부존재가 이미 다른 legal_element에서 커버됨)하고 225는 **forgery_without_authority의
경계로 흡수**된다는 점에서 서로 다르게 처리된다는 것이 최종 정리.

---

## 수정 6 — 234 착수 기준: predicate HOLD가 아니라 legal-standard 확인사항

`commencement_of_execution`이 이미 존재하므로 234도 기본적으로 그것을 재사용한다.
"234 전용 predicate가 필요한가"라는 architecture 질문이 아니라 "원문에 234 고유의 착수
기준이 별도로 있는가"라는 authoring-time 확인사항으로 격하한다 — 지금까지 확인된 카드에는
234 고유 착수 기준이 없으므로 기본값(`commencement_of_execution` 그대로)으로 저작하고,
항목 성격을 v0의 "검수 필요 5(HOLD)"에서 "확인사항"으로 표기 변경. 2패스 착수 전 원문
재확인 목록에는 남긴다(단, gap 후보가 아니라 단순 확인 항목으로).

---

## 나머지는 v0 그대로 확정

방화군의 `arson_target_status`/`burning_result`(신규), 164 결과적가중범 구조(기존
COMPOSE + `aggravated_result_attribution` 재사용, 신규 구조결정 없음), 164 공동정범
예견가능성 = gap 아님(잠정, 2패스 재확인), 164 교사·방조 예견가능성 = 8차 addendum
`derivative_mode.requires` 재사용(신규 아님); 문서죄군의 225/227/231 위조·변조·허위작성
3분(`forgery_without_authority`/`alteration_of_genuine_document`/`content_falsity_by_
authorized_official`), `purpose_to_use_as_genuine`(234 제외), `utterance_conduct`,
`public_document_object`(225·227 공유), `private_document_object`, 227의
`no_intent_clerical_or_customary_entry` 흡수 — 전부 v0 그대로 확정.

v0 대비 6건 정정 반영 — 사용자 검수 대기.
