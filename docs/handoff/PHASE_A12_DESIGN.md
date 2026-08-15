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
| ④ | 형량 metadata | 조건부 승인 — base+derived 모두, Article151 전용 이름, 값은 별도 검수 | 필드 완료 / **값 미저작** |
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

## 6. 남은 승인 대상 — A1 선행범죄 candidate universe

반려 사유가 정확했다. `linked_offender × 기존 instance offense_refs`는 actor universe 문제만
풀고 offense universe 문제를 그대로 남긴다. 제34조가 그 방식을 쓸 수 있는 이유는 "그 사람이
**바로 그 utilizer의 죄**를 실현할 수 있었는가"를 묻기 때문이고, 제151조는 도피시킨 죄와
乙의 선행범죄가 애초에 다른 죄다.

그래서 남은 조각은 하나다.

> **乙이 무슨 죄의 후보인지를 누가 정하는가.**

Call 1.5는 아니다 — 그건 법적 candidate selection이다. Definition catalog를 보는 Call 1이 맞다.
현재 Call 1은 질문이 묻는 actor 기준으로만 seed를 고른다.

### 제안 — Call 1에 dependency candidate를 좁게 추가

```
Call 1 출력에 second, 별도 목록:
  dependency_offense_candidates: [offense_ref, ...]

조건: 이 case의 seed 중 linked_offender_dependency를 선언한 것이 있을 때만 요구한다.
의미: "이 사건에서 **책임 후보가 아닌 사람**이 범했을 수 있는 죄".
      누가 범했는지는 고르지 않는다 -- 사람은 Call 1.5의 linked_offender가 결박한다.
```

그 다음은 전부 결정론이다.

```
linked_offender(사람)  ×  dependency_offense_candidates(죄)
  → LinkedOffenderOutcomeTarget      (participant 수준, instance 아님)
  → 필요한 predicate만 Call 2
  → internal outcome fold
  → article151_penalty_threshold 확인
  → Article151QualifyingLink → resolve_article_151_liability()
```

> **검수 ⑥** Call 1 출력에 `dependency_offense_candidates`를 추가하는 방향에 동의하는가?
> 동의하면 프롬프트·스키마 diff를 같은 형식으로 올린다.
>
> **검수 ⑦** `article151_penalty_threshold` 값 저작 워크시트를 언제 올릴까.
> 조문별 법정형 확인이 필요하고, 현재 저작된 offense 60여 개가 대상이다.

---

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

## 8. 아직 배선되지 않은 마지막 seam

A2의 도출·target 개방·정책 적용 함수는 모두 있고 테스트도 있다. production 체인에서
`apply_mistake_policy`를 호출하는 자리(`scripts/run_v2_scallop_e2e.py`의 truth 변환 구간)는
아직 연결하지 않았다. §6이 정해지면 A1의 outcome 주입과 함께 한 번에 넣는 편이 같은 코드를
두 번 건드리지 않는다.
