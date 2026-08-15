# dependency ROUTE invocation — 프롬프트/스키마 검수 요청

기준: 2026-08-15 · 결재된 구조: [`PHASE_A12_DESIGN.md`](PHASE_A12_DESIGN.md) §6
검수 범위: **이 invocation이 atomic ROUTE 계약을 실제로 지키는가**, 그것만.

결정론 부분은 이미 서 있다(`4cffa56`). 남은 것은 모델에게 보내는 절반이다.

---

## 0. 이 검수가 지켜야 할 계약

```text
한 ROUTE 호출 = 한 routing basis = 한 종류의 행위자
```

한 호출에서 question-facing seeds와 dependency offense를 동시에 뽑으면 안 된다.
아래 세 가지가 그 계약을 코드·프롬프트 양쪽에서 지키는지가 검수 대상이다.

| | 지켜야 할 것 | 어디서 |
|---|---|---|
| ㄱ | dependency 호출에 `question_prompt`가 실리지 않는다 | 코드 (구현·테스트 완료) |
| ㄴ | 프롬프트가 두 basis를 섞어 지시하지 않는다 | **아래 §2 — 검수 대상** |
| ㄷ | scope가 binding이 carry한 증거를 넘지 않는다 | 코드 (구현·테스트 완료) |

---

## 1. 먼저 보고할 문제 — 현재 user 프롬프트는 재사용할 수 없다

[`prompts/v2_call1_router_user.md`](../../prompts/v2_call1_router_user.md) 끝에 이런 블록이 있다.

```markdown
특히 금전 전달·중간자의 일부 사용·공무원의 수수 후 불입건이 함께 있는 유형은 catalog에
존재한다면 `offense.bribe_giving`, `offense.bribe_delivery_receipt`,
`offense.bribery_taking`, `offense.embezzlement`, `offense.dereliction_of_duty`,
`offense.harboring_or_escape`를 모두 독립 검토 후보로 포함한다.
수사 의무가 있는 공무원이 다른 범인을 의도적으로 입건하지 않은 행위는 부작위에 의한
`offense.harboring_or_escape` 검토 후보이므로 누락하지 않는다.
```

question-facing routing에서는 recall 보강으로 기능해 왔다. 그러나 **dependency routing에
그대로 재사용하면 적극적으로 틀린다** — 선행범죄를 찾는 호출에 "범인도피죄를 누락하지 마라"고
지시하게 되고, 그것은 지금 판단하려는 바로 그 죄다. 순환이다.

따라서 user 프롬프트는 basis별로 갈라야 한다. system 프롬프트는 하나로 유지한다.

> **검수 ①** 이 블록을 dependency 호출에서 빼는 것에 동의하는가?
> (question-facing 호출에서는 지금 그대로 둔다. 그 효과를 재측정할 여유가 없다.)

---

## 2. system 프롬프트 변경안 — 승인 대상 전문

[`prompts/v2_call1_router.md`](../../prompts/v2_call1_router.md)의 2번 항목만 교체하고,
나머지 항목·예시·마지막 줄은 손대지 않는다.

**현재 (2번):**

```markdown
2. `question_prompt`가 이번 평가의 정확한 범위다. 긴 `case_text`에 여러 사실관계나
   행위자가 있어도 question_prompt가 묻는 사실관계와 행위자의 후보만 선택한다.
```

**변경안 (2번):**

```markdown
2. `routed_actor_ids`와 `factual_scope_text`가 이번 호출의 정확한 범위다. 긴 `case_text`에
   여러 사실관계나 행위자가 있어도 그 범위 안의 후보만 선택한다.
   - `routing_basis`가 `question_actors`이면 `question_prompt`가 함께 주어지며, 그것이
     범위를 정한다.
   - `routing_basis`가 `linked_offender`이면 `question_prompt`는 주어지지 않는다. 질문이
     죄책을 묻지 않은 사람에 대한 호출이기 때문이다. `routed_actor_ids`에 적힌 사람이
     `factual_scope_text` 안에서 범했을 가능성이 있는 죄만 고른다. 그 사람을 누가 도왔는지,
     은닉·도피시켰는지는 이 호출의 대상이 아니다.
   한 호출에서 두 범위를 섞지 않는다.
```

핵심은 마지막 두 문장이다. "그 사람을 누가 도왔는지는 대상이 아니다"가 없으면 모델이
`factual_scope_text`에 함께 들어 있는 도피 조력 행위를 보고 다시 범인도피죄를 고른다 —
§1의 순환이 프롬프트 본문에서 되살아난다.

> **검수 ②** 이 문구를 그대로 설치해도 되는가?

---

## 3. dependency user 프롬프트 — 신규 파일 전문

`prompts/v2_call1_router_dependency_user.md`

```markdown
아래 INPUT_JSON의 `routed_actor_ids`에 적힌 사람이 `factual_scope_text` 안에서 범했을
가능성이 있는 Definition Layer offense seed를 `offense_catalog`에서 순서대로 고르라.

이 호출에는 `question_prompt`가 없다. 질문이 죄책을 묻는 사람이 아니라, 다른 사람의 죄책을
판단하는 데 필요해서 조회되는 사람이다. 따라서 그 사람 **자신의** 행위만 본다.
그를 도운·숨겨준·도피시킨 사람의 행위는 이 호출의 대상이 아니다.

`factual_scope_text` 밖의 사실은 쓰지 않는다. 범위가 좁으므로 후보도 대개 적다.
개수를 채우지 말고 그 범위에서 실제로 읽히는 후보만 고르라.
최종 성립 여부는 판단하지 않는다.

다른 필드나 설명을 출력하지 말고 JSON 객체 하나만 출력하라.

<INPUT_JSON>
{{INPUT_JSON}}
</INPUT_JSON>
```

question-facing user 프롬프트에 있는 사례별 recall 힌트는 넣지 않는다(§1).

> **검수 ③** 이 문구로 설치해도 되는가?

---

## 4. 스키마 — 변경 없음

출력 계약은 `{"seeds": [...]}` 그대로이고 `validate_router_output()`을 그대로 재사용한다.
같은 operation이므로 출력 형태가 달라야 할 이유가 없다.

한 가지만 다르게 하는 것을 제안한다.

| | question-facing | dependency |
|---|---|---|
| `maxItems` | 10 (현행 `MAX_SEEDS_PER_CASE`) | **3** |

이유는 비용이 아니라 계약이다. dependency scope는 binding이 carry한 action 몇 개뿐이라
그 범위에서 10개가 읽히는 일은 없다. 상한이 10이면 모델이 case_text 전체를 다시 보고
채우려는 압력이 생긴다. 상한 자체가 "이건 좁은 조회다"라는 신호가 된다.

> **검수 ④** dependency 호출의 seed 상한을 3으로 두는 데 동의하는가?
> (근거가 약하다고 보시면 10 유지도 무방하다 — 범위 제한은 프롬프트와 scope가 이미 건다.)

---

## 5. 설치 후 남는 것

승인되면 A1은 다음만 남는다. 전부 결정론이고 승인이 필요 없다.

```text
dependency ROUTE 결과(선행범죄 후보)
→ LinkedOffenderOutcomeTarget  (participant × 후보, 제34조와 같은 모양)
→ Call 2 predicate assessment
→ internal outcome fold
→ qualifies_for_article_151()   ← 저작된 한 비트
→ Article151QualifyingLink → resolve_article_151_liability()
→ offender_status_of_object
```

제151조는 이 경로의 **첫 consumer**이지 예외처리가 아니다. 같은 경로를 쓰는 다음 후보는
제33조 신분관계와 제34조 이용된 참가자다 — 둘 다 이미 "다른 actor의 상태가 필요함"을
각자 다른 코드로 처리하고 있다.

> **검수 ⑤** 위 순서로 닫는 데 동의하는가? 동의하면 승인 즉시 착수한다.
