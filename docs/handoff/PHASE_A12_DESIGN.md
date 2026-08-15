# Phase A1·A2 — 결재된 설계와 시공 기록

기준: 2026-08-15 · 브랜치 `deadline_v2_0808` · 상위 지시서 [`RULEBASE_AUDIT.md`](RULEBASE_AUDIT.md) §4 P0-R1·P0-R2
검수 결재: 2026-08-15 (①~⑤ + A1 §2-2 반려)

**이 문서의 §1~§4는 결정 기록이다.** 남은 승인 대상은 §6 하나뿐이다.

---

## 1. 결재 결과

| | 항목 | 판정 | 반영 |
|---|---|---|---|
| ① | `directed_action_target`의 원문 명시 봉쇄 | 조건부 승인 — episode가 아니라 **carried participant**로 제한 | 완료 |
| ② | 위법성조각 전제사실 착오 cue | 승인 — 이번에 열지 않음 | 완료 (gap 유지) |
| ③ | `linked_offender` 별도 필드 (나) | 승인 — activation은 host/저작이 소유 | 완료 |
| ④ | 형량 metadata | 조건부 승인 — base+derived 모두, Article151 전용 이름, 값은 별도 검수 | 필드 완료 / 값 워크시트 제출 → [`ARTICLE151_PENALTY_WORKSHEET.md`](ARTICLE151_PENALTY_WORKSHEET.md) |
| ⑤ | 프롬프트 문구 | 수정 후 승인 | 완료 (main·recovery 양쪽) |
| — | A1 §2-2 outcome universe | **반려** | 재설계, §6 참조 |

---

## 2. 시공된 것 — Call 1.5 계약

binding에 좁은 사실 세 개가 들어갔다. required이되 nullable이다 — 누락과 "원문이 말하지
않는다"가 같은 wire 값이 되면 안 되기 때문이다.

| 필드 | 제한 |
|---|---|
| `directed_action_target` | 이 binding의 focal/supporting action이 carry하는 participant, 또는 null |
| `actual_result_bearer` | 같음 |
| `linked_offender` | 같음 + **저작이 `linked_offender_dependency`를 선언한 seed에서만** |

`factual_targets`는 손대지 않았다. episode가 아니라 carried participant로 좁힌 것이 ①의 조건이다
— episode는 의도적으로 넓은 서사 맥락이라, episode 범위로 검사하면 이 행위와 무관한 사람이
"이 행위가 겨냥한 대상"으로 들어올 수 있다.

`linked_offender` activation은 코드가 offense id를 아는 방식이 아니다.
`offense.harboring_or_escape`가 정의에서 다음을 선언하고, host가 그것을 읽어 seed cue에
`requires_linked_offender`로 실어 보낸다.

```yaml
linked_offender_dependency:
  role: article151_offender
  resolved_element: legal_element.offender_status_of_object
```

### recovery — 지적하신 split contract는 이미 존재했다

recovery는 제 변경 이전부터 깨져 있었다. `1607b70`(8/14)이 `ef0f4a5`(8/15, action-atomic)보다
하루 먼저라, 현재 recovery의 변환 출력은 main validator를 통과하지 못한다.

두 포맷을 유지하는 대신 **recovery를 main 계약으로 흡수**했다 —
`issue_binding_schema(seed_count=1)`을 그대로 쓰고 검증도 같은 함수를 탄다. 이제 split이
구조적으로 불가능하다.

---

## 3. 시공된 것 — A2 하류

```
directed_action_target + actual_result_bearer
  → (다르면 TRUE / 같으면 FALSE / 하나라도 없으면 미확정)
  → relation.intended_object_divergence   ← host가 셈, 모델에게 묻지 않음
  → TRUE인 instance에서만 legal_element.object_misidentification target 개방
  → mistake_findings → apply_mistake_policy
```

**감사 문서가 분리하지 않은 결함이 하나 더 있었다.** `applies_to: offense_instance` probe에는
target producer가 아예 없었다 — `policy_probe_targets`는 참가 후보만 처리했다. 그래서 착오
정책의 leaf가 한 번도 계획되지 않았고, `apply_mistake_policy`는 테스트만 있고 production
호출부가 없었다. 저작·런타임·Scallop 경로가 다 있는데 정책이 어떤 사건에서도 발화할 수 없는
상태였다. 제33조 단서에서 이미 한 번 나온 고장과 같은 모양이다.

`gap.intended_object_identity`는 삭제했고, 테스트가 "gap이 사라졌다"와 "거부된 재해석이
되살아나지 않았다"를 함께 지킨다.

### 남긴 한계 (코드 주석에도 기록)

`intent_toward_intended_object`를 이 instance의 `legal_element.intent`에서 읽는다. 저작된 probe가
요구하는 고의가 그것 하나뿐이기 때문이다. 착오 사안에서 Call 2가 "**실제 피해자**를 해할
고의"로 읽으면 FALSE가 돌아오고 정책은 침묵한다. 침묵이 틀린 귀속보다 안전하므로 그대로 두되,
**지향 대상 기준 고의를 별도 target으로 물을지는 저작 결정**이다.

2026-08-15 결재: **이번 A2에서 새 predicate를 만들지 않는다.** generic `legal_element.intent`가
`intent_toward_intended_object`와 같은 semantics라고 보기 어렵다는 점은 인정하되, 지금 새
predicate를 만들면 법률 저작이 다시 들어간다. 명시적 **authoring-review item**으로 남기고,
UNKNOWN 작업 마지막 단계에서 실제 병목으로 드러나면 그때 검수한다.

---

## 4. 시공된 것 — A1 중 결정론적인 부분

**타입 정직성.** `Article151QualifyingLink`가 `LiabilityEvaluation`을 들고 있어서 재설계를
담을 수 없다는 지적이 맞았다. 이제 제34조와 같은 participant 수준 `UtilizedParticipantOutcome`을
받고, obligation도 `linked_participant` / `qualifying_offense_ref`를 기록한다. 가짜
`OffenseInstanceKey`는 만들지 않는다.

**threshold.** `article151_penalty_threshold`를 offense·derived_offense 스키마 양쪽에 넣었다.
값은 하나도 저작하지 않았다 — 미저작은 UNKNOWN이고, 지금 제151조 status leaf는 UNKNOWN이다.
정확하고, 눈에 보인다.

**잘못된 질문 제거.** `legal_element.offender_status_of_object`가 ordinary predicate scope에
있어서 모든 제151조 instance가 모델에게 "다른 사람의 법적 결과"를 이 instance의 사실인 것처럼
물어 왔다. 6/6 UNKNOWN은 정확한 응답이었고 결함은 물었다는 데 있었다. 저작이 host-resolved라고
선언한 element는 이제 neural scope에서 빠진다.

**테스트.** 제151조 테스트 파일이 이번에 처음 생겼다. 그 부재가 이 결함이 오래 남은 배경이다 —
호출부도 테스트도 없으니 "구현되어 있다"와 "한 번도 실행되지 않는다"가 공존할 수 있었다.

---

## 5. B 계열 (같은 세션에서 닫음)

* **B2** 제263조 authority 단일화 — 감사는 2중이라 했지만 실제로는 **4중**이었다(YAML, wire
  튜플, resolver, Scallop backend). resolver와 backend가 저작을 읽고, wire 순서는 테스트가 못박는다.
* **B3** `blocked_when` traversal — 잠재 위험이 아니라 **이미 발동 중인 결함**이었다.
  defeat doctrine 5개의 blocker predicate(자초한 심신장애·자초한 강요상태·위난감수의무·
  승낙의 법률상 제한)는 다른 어디에도 없어서, 수집되지 않으면 그 예외들이 영원히 발동하지
  않는다. closure와 planner 양쪽에 넣었고, 변경 전후 대조로 정확히 그 5건만 늘고
  `candidate_offense_refs`는 동일함을 확인한 뒤 Step 7 봉인을 다시 찍었다.
* **B4** `candidate_materialization` ref checker.

---

## 6. A1의 남은 조각 — ROUTE를 재사용 가능한 operation으로 (2026-08-15 결재)

제 제안(`dependency_offense_candidates`를 최초 Call 1 출력에 추가)은 **반려되었다.** 그러면
한 Call이 서로 다른 두 atomic task를 하게 된다.

```text
1) 질문받은 actor의 offense routing
2) 아직 binding되지도 않은 다른 actor의 선행범죄 routing
```

두 번째를 같이 시키면 Call 1이 linked offender를 사실상 다시 찾아야 하고, 지금까지 지킨
atomicity가 깨진다. 제151조 전용 Call을 새로 만드는 것도 반려 — 조문 하나 때문에 stage를
늘리는 땜질이다.

### 결재된 구조

진짜 missing abstraction은 이것이다.

> **법적 rule이 다른 participant의 legal outcome을 요구할 때, binding된 participant를 대상으로
> 기존 atomic offense-routing operation을 재사용할 수 있어야 한다.**

Call 1을 "맨 처음 한 번 도는 stage"가 아니라 operator로 본다.

```text
ROUTE(actor, factual_scope, offense_catalog) → offense candidates
```

* 최초: `ROUTE(question_actor, question_scope)` → answer-facing seeds  (지금과 동일)
* A1: Call 1.5가 `linked_offender = 乙`을 **사실로 먼저 결박한 뒤**, dependency planner가
  필요할 때 같은 ROUTE를 다시 호출한다.

```text
Article151 rule
→ linked legal dependency 필요 (저작된 linked_offender_dependency)
→ linked_offender = 乙 확인            ← Call 1.5가 이미 결박
→ ROUTE(乙, carried factual scope)      ← 기존 router capability 재사용
→ predecessor offense candidates
→ participant 수준 assessment / outcome  ← 제34조와 같은 모양
→ article151_penalty_threshold
→ offender_status_of_object
```

새 pipeline stage가 아니라 **기존 capability의 재사용**이다. 그래서 제151조가 아닌 다른
cross-actor dependency가 나와도 같은 abstraction을 쓴다 — 제33조·제34조·participation에서
이미 반복해 나타난 "다른 actor의 상태가 필요함"을 조문마다 별도 코드로 처리하지 않는다.

### 이 결재가 정정한 제 서술

제가 "선행범죄 candidate universe는 Call 1의 것"이라고 쓴 것은 절반만 맞았다. 정확히는:

> 선행범죄의 법적 routing **capability**는 Call 1의 것이 맞지만, **최초 invocation에 같이
> 넣는 것은 아니다.** Call 1.5가 dependency participant를 결박한 뒤 동일 ROUTE primitive를
> 재사용한다.

### 구현 순서

```text
1. ROUTE를 (actor, scope, catalog) → candidates 로 재호출 가능하게 분리
2. dependency planner: linked_offender_dependency 선언 + 결박된 linked_offender → ROUTE 재호출
3. LinkedOffenderOutcomeTarget (participant 수준) → Call 2 → outcome fold
4. Article151QualifyingLink → resolve_article_151_liability  (타입은 이미 완료, §4)
```

## 7. 재실행 계획 (승인대로 수정)

Call 1.5만 먼저 돌리지 않는다. A3·A4가 offense universe를 바꾸고 §6이 Call 1 계약을 바꾸므로,
전부 모은 뒤 한 번씩만 돈다.

```
A1 나머지 + A3 + A4 + B/C
→ Call 1 (1회)
→ Call 1.5 (1회)
→ deterministic planner
→ rule→target accounting
→ Call 2 (1회)
→ symbolic → AnswerPlan → Call 3
```

`758 target`은 invariant가 아니다.

---

## 8. 현재 상태 (2026-08-15 마감)

### 닫힌 것

| 조각 | 상태 |
|---|---|
| Call 1.5 세 사실 필드 (main·recovery·persisted parser) | 완료 |
| A2 structural divergence → target 개방 → 정책 적용 | 완료, **production 호출부 연결됨** |
| `offense_instance` probe producer 부재 | 완료 |
| ROUTE 일반화 + dependency planner + carried scope | 완료 |
| threshold pre-gate (qualifying/non_qualifying/unauthored 3분기) | 완료 |
| linked-offender predicate targets + participant 수준 fold | 완료 |
| `article151_penalty_threshold` 63개 저작 | 완료 |
| dependency ROUTE 실행 스크립트 | 완료 (`scripts/run_v2_dependency_route.py`) |
| 라우터 프롬프트 basis-neutral화 | 완료 |
| B2·B3·B4 | 완료 |

### Scallop parity path는 만들지 않는다 (2026-08-15 결재)

제263조가 별도 경로를 가진 것은 그 조문이 **책임 자체를 의제**하기 때문이다. 제151조는
`offender_status_of_object` 하나만 공급하고 최종 죄책은 기존 offense program이 그대로
소유하므로, 신분 계산 결과를 predicate truth로 넘기는 것으로 충분하다. 경로를 늘리면 같은
죄에 두 개의 책임 계산이 생긴다.

`article151_status_truths()`가 그 공급자이고, symbolic 러너가 truth 조립 구간에서 얹는다.
`qualifying`이 아닌 값은 FALSE로 내리지 않고 UNKNOWN으로 둔다 — 이 좁은 조회는 "자격 있는
선행범죄가 존재하지 않는다"를 증명하지 못한다.

`resolve_article_151_liability()`는 Scallop을 타지 않는 직접 런타임 경로로 남는다.

### authoring-review로 남긴 것 (승인된 상태로 유지)

1. `intent_toward_intended_object`를 generic `legal_element.intent`로 읽는 것
   — UNKNOWN 작업 마지막 단계에서 병목으로 드러나면 재검수.
2. ~~linked-offender fold가 completion을 평가하지 않는 것~~ — **해소됨.** 근거가
   "미수도 죄"가 아니라 **제151조 고유의 범인 개념**(범죄 혐의로 수사대상이 된 자를 포함)임이
   확정되었다. 그 개념은 대상자의 죄책을 완결적으로 확정할 것을 요구하지 않으므로 completion은
   애초에 이 신분의 요소가 아니다. 결과 타입도 `Article151PredecessorStatus`로 분리해
   ordinary liability와 섞이지 않게 했다.
