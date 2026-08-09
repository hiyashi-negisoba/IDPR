# Predicate 사전 확장 — 배치 ⑪ 주거·권리행사 (제319·323·328조) v2

[predicate_dictionary_ext_batch11_v1.md](predicate_dictionary_ext_batch11_v1.md)에 대한
사용자 검수 1건 반영(그 외 전부 승인) — HOLD 3(퇴거불응 미수) 문구만 좁힌다. v1의
필수 정정 1·2·3(positive-predicate 교체, 322조 반영, 328조 전면 재작성)은 그대로 확정.

---

## 정정 — HOLD 3 문구: `result_not_occurred` 재언급 삭제, "punishable=true" 조건부 표현으로 좁힘

**v1 오류 1**: HOLD 3에서 "기존 25-27조 predicate 패턴(`commencement_of_execution`/
`result_not_occurred` 등)"이라고 썼는데, `result_not_occurred`는 배치④(28·29조)에서
이미 삭제가 확정된 predicate다 — 되살리면 안 된다. `commencement_of_execution` 등
현재 살아있는 Completion predicate/`when` 조합으로만 표현을 좁힌다.

**v1 오류 2**: "`attempted.punishable = true`(322조 문언, 다수설 긍정설)로 잠정
표시"라는 서술이 마치 punishable=true 자체가 이미 확정된 것처럼 읽힌다. 실제로 확정된
것은 **"322조가 미수 처벌의 법적 근거를 제공한다"**는 사실뿐이고, **"퇴거불응에
attempted state가 애초에 성립하는가"** 자체가 학설대립의 대상이다 — 이 순서를
뒤집으면 안 된다.

**v2(수정) — 위 두 지점을 다음으로 교체한다**:

```text
확정: 322조는 퇴거불응죄를 포함한 본장(319-321조) 전체에 대해 미수 처벌의 법적
      근거를 제공한다(문언 확인 완료).

미확정(학설대립, 2패스로 이월): 퇴거불응에 실제로 attempted state가 성립하는가 자체.

  긍정설 채택 시 → attempted.punishable = true
                  (그 구체 completion 기준 — "불응=착수, 시간경과=기수" — 을
                  기존 Completion predicate/when 조합으로 표현 가능한지 확인)
  부정설 채택 시 → attempted state 자체가 이 offense에서 발생하지 않는다
                  (퇴거불응은 불응과 동시에 즉시 기수이므로 completed 외의 state가
                  존재할 수 없다는 뜻 — CompletionPolicy에 attempted state를
                  아예 두지 않는 선택)
```

즉 "punishable=true"는 긍정설을 전제로 한 조건부 결론이지, v0/v1처럼 그 자체가 이미
확정된 사실인 것처럼 서술하지 않는다. HOLD 3 항목을 이 표현으로 교체하고, 본문 A-2절의
"v1 판단" 단락도 같은 뜻이었으나 표현이 앞서갔던 부분을 이 문구로 대체된 것으로
간주한다(본문 재작성 없이 이 정정으로 상위 문서 표현을 덮어쓴다).

---

## 배치⑪ v2 요약 — 마감

v1의 세 필수 정정(positive-predicate+`NOT()`, 322조 source coverage, 328조 구법 EXEMPT
폐기·procedure-scope 전환) + 이번 v2의 HOLD 3 문구 정정으로 배치⑪ predicate 사전을
확정한다. 최종 확정 predicate: 319 A-1(주거침입) `dwelling_or_managed_premises_object`/
`trespass_entry`/`intent`(13조 재사용), A-2(퇴거불응) `retreat_demand_by_authorized_
person`/`justifiable_reason_for_refusal`(+`NOT()`)/`ability_to_comply_with_retreat_
demand`/`failure_to_comply_without_delay`/`intent`(13조 재사용) + 323 `own_property_
object`/`third_party_possession_or_right_object`/`taking_conduct`/`concealment_
conduct`/`damage_conduct`/`obstruction_of_right_exercise`/`intent`(13조 재사용) — 328은
predicate/doctrine 없음(procedure-scope 밖으로 확정). 신규 스키마·DSL primitive 없음(v0·
v1과 동일).

HOLD/architecture-compatibility 최종 목록(기존 목록 + 이번 배치 3건): 33조 단서, 34조,
151조 offender_status_of_object, 263조 특례, 257·298조 자상·도구 간접정범, 250조
비신분자 존속살해 가담, 301조 결합범+결과적가중범 병존, 299조 예비음모 conduct 갈래
제한, **art323 소유자 아닌 자의 가담 ↔ 33조 본문 공동정범 gap**, **art319 계절적
미사용 별장 서브타입 재분류**, **art319 퇴거불응 미수 성립 가능 여부(322조, 위 정정
반영본으로 확정)**.

---

## 다음 세션 시작점 — 배치⑫ 절도·강도 나머지 (330·331·332·334·335·337·338·342·343·344·356·360조)

v1이 이미 정리한 대로 328·344 친족관계는 소추조건(procedure scope 밖)으로 확정됐으므로
330조 저작 시 재검토 불필요. 344조 저작 시에도 328조 인용 부분은 predicate 사전에
반영하지 않고 소추조건 참고로만 authoring 메모에 남긴다.
