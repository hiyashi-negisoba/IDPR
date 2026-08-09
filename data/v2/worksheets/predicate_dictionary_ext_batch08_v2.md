# Predicate 사전 확장 — 배치 ⑧ 방화·문서 (제164·225·227·231·234·239조) v2

[predicate_dictionary_ext_batch08_v1.md](predicate_dictionary_ext_batch08_v1.md)에 대한
사용자 검수 1건(문구) 반영 — 구조 변경 없음. 나머지는 v1 그대로.

---

## 정정 — "NOT 조건으로 흡수" 표현이 symbolic `NOT()`과 혼동될 수 있다

**v1의 부정확한 표현**: 수정 3에서 `art239_sec1_3.deceived_nominee_manifestation_not_
improper_use`를 `improper_use_of_genuine_seal`의 canonical_meaning에 "NOT 조건으로
흡수"한다고 썼다. 이 표현은 별도 positive predicate를 만들어 expression 층에서 실제
`NOT()`을 적용하겠다는 뜻으로 읽힐 수 있는데, 의도는 그게 아니다 — 하나의
`improper_use_of_genuine_seal` 평가기준 안에서 그 경계(명의자를 기망해 인영·서명을
현출시킨 뒤 사용해도 명의자의 권한을 수여받아 행사한 것이므로 부정사용이 아니다)를
서술하는 정도로 충분하다.

**v2(정정)**: "canonical_meaning에 NOT 조건으로 흡수" → **"`improper_use_of_genuine_
seal`의 legal_standard상 부정적 한계사례로 흡수"**로 표현 변경. predicate 정의나
구조는 바뀌지 않는다 — 표현만 정정.

---

## 확인 — 239→238 provenance는 그대로 보존한다

238조 원문 열람으로 239의 source-resolution을 완료한 것은 맞다(수정 3). 다만 2패스 실제
저작 시:

```text
target offense = 239
predicate source/provenance = 238조 주석(239 조문 주석이 명시적으로 참조 지시)
```

라는 출처 연결만 그대로 보존하면 된다 — `improper_use_of_genuine_seal`의 근거란에
"238조 Ⅰ.3, Ⅱ.2(239가 참조 지시)"라고 이미 적어둔 것이 그 provenance 기록이다. 새로운
구조(예: cross-article source 필드 등)는 필요 없다.

---

## 배치⑧ v2 — 최종 확정, 종료

방화군(`arson_target_status`/`burning_result` 신규, 기존 `commencement_of_execution`/
`legal_element.intent`/`aggravated_result_attribution` 재사용, 8차 addendum
`derivative_mode.requires` 재사용, 공동정범 예견가능성 gap 아님 잠정)과 문서죄군
(`forgery_without_authority`/`alteration_of_genuine_document`/`content_falsity_by_
authorized_official`/`purpose_to_use_as_genuine`/`utterance_conduct`/`improper_use_of_
genuine_seal` + `public_document_object`/`private_document_object`/`legal_element.
seal_or_signature_object`)는 v1 그대로 확정. 배치⑧(164·225·227·231·234·239조) predicate
사전은 이 v2로 종료 — 다음은 배치⑨(생명·신체: 250·254·255·257·259·263·267·268·2582_2조).
