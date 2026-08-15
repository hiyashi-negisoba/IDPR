# Phase A1·A2 설계안 — 검수 요청

기준: 2026-08-15 · 브랜치 `deadline_v2_0808` · 상위 지시서 [`RULEBASE_AUDIT.md`](RULEBASE_AUDIT.md) §4 P0-R1·P0-R2

이 문서는 **승인 대상**이다. 카드 단위로 판정해 주면 그대로 설치한다.
아직 코드·정의·프롬프트는 하나도 고치지 않았다.

---

## 0. 왜 A1과 A2를 한 묶음으로 내는가

둘 다 `IssueBinding`에 **없는 사실**을 요구한다.

현재 binding이 싣는 것은 이게 전부다([`issue_binding.py:117-124`](../../src/idpr/v2/issue_binding.py#L117-L124)).

```
binding_id / factual_episode_id / seed_index / offense_ref
actor_id / focal_action_id / supporting_action_ids / factual_targets
```

`factual_targets` 재해석은 2026-08-13에 승인 거부되었고 그 결정을 유지한다.
따라서 A1·A2 모두 **Call 1.5 wire schema + 프롬프트 변경 → Call 1.5 재생성**을 요구한다.
따로 처리하면 26문항 Call 1.5를 두 번 돌린다. 그래서 한 번에 낸다.

---

## 1. A2 — 객체 동일성 (P0-R2)

### 1-1. 제안하는 사실 필드

[`representation_gaps.yaml`](../../data/v2/representation_gaps.yaml)의 `future_design`을 그대로 따른다.
binding에 좁은 optional 필드 **두 개**를 추가한다.

| 필드 | 타입 | 의미 |
|---|---|---|
| `directed_action_target` | episode participant 1명 또는 `null` | 원문이 **행위자가 겨냥한 대상으로 명시**한 사람 |
| `actual_result_bearer` | episode participant 1명 또는 `null` | 원문이 **실제로 결과를 입었다고 서술**한 사람 |

`factual_targets`는 지금 의미 그대로 둔다. 제263조 동일객체 판정이 이미 그 필드를
쓰고 있고([`evaluation_instance_planner.py:1041-1051`](../../src/idpr/v2/runtime/evaluation_instance_planner.py#L1041-L1051)),
그 용법은 "복수 대상 집합"이라 이번 건과 충돌하지 않는다.

### 1-2. host가 하는 일 (결정론적)

```
둘 다 non-null  &&  서로 다름   → relation.intended_object_divergence = TRUE
둘 다 non-null  &&  같음        → relation.intended_object_divergence = FALSE
하나라도 null                   → UNRESOLVED_MISTAKE_BINDING 유지 (현행과 동일)
```

host는 그 이상 추론하지 않는다. divergence가 structural TRUE인 instance에서만
`legal_element.object_misidentification`을 Call 2 target으로 연다 — 객체의 착오와
방법의 착오를 가르는 것은 여전히 모델의 사실 판단이지만, **대상 동일성이 먼저 사실로
확정된 뒤에만** 묻는다. gap 파일이 금지한 것(대상이 미확정인 채로 모델에게 묻는 것)은
그대로 금지된다.

### 1-3. ⚠ 검수가 필요한 지점 — "겨냥한 대상"은 순수 사실인가

이 설계의 유일한 약점이다. 객체착오 사안의 원문은 이렇게 쓰인다.

> 乙인 줄 알고 C를 칼로 찔렀다

여기서 `directed_action_target = 乙`은 **행위자의 인식**이지 물리적 사실이 아니다.
그대로 물으면 Call 1.5가 "법률 판단을 하지 않는다"는 계약을 넘어설 위험이 있다.

**제안하는 봉쇄:** 원문이 그 인식을 **명시적으로 서술한 경우에만** 적고, 아니면 `null`.
즉 "乙인 줄 알고", "A로 착각하여", "B를 겨누어" 같은 서술이 원문에 있을 때만 채운다.
서술이 없으면 divergence는 미확정으로 남고 지금과 같은 상태가 된다.
이것은 모델에게 착오 여부를 판단시키는 것이 아니라 **원문에 이미 적힌 지향 대상을
전사**시키는 것이다.

> **검수 ①** 이 봉쇄로 충분한가? 아니면 "원문 명시" 요건을 더 좁혀야 하는가?

### 1-4. `gap.justifying_premise_vs_object_identity` 재개 여부

gap 파일은 이 두 필드가 결박되면 위법성조각사유 전제사실 착오 cue를 다시 열 수 있다고
적어 두었다. **이번에는 열지 않기를 권고한다.** 2026-08-13에 `r12_p2_q1_ga`에서
false raise로 Call 2 target 8개가 열린 전력이 있고, 데드라인 안에서 재발을 측정할
여유가 없다.

> **검수 ②** 이번 묶음에서 이 cue는 닫아 둔 채로 간다 — 동의하는가?

---

## 2. A1 — 제151조 링크 (P0-R1)

### 2-1. 감사 문서보다 나쁜 상태를 발견했다

`RULEBASE_AUDIT.md`는 "caller 한 줄 누락보다 큰 gap"이라고 적었다. 맞지만 그 이유가
하나 더 있다.

case는 **문항 단위**이고 `candidate_actor_ids`는 질문 원문에서만 뽑힌다
([`issue_binding.py:171-178`](../../src/idpr/v2/issue_binding.py#L171-L178)).
`r10_p2_q2`는 丙의 책임만 묻는다. 따라서 **乙의 `OffenseInstanceKey`는 이 case에
아예 생성되지 않는다.**

결론: `resolve_article_151_liability()`에 호출부를 붙이고 typed 필드를 추가해도,
링크할 liability result가 없어 여전히 UNKNOWN이다. **배선만으로는 A1이 닫히지 않는다.**

### 2-2. 제안 — 제34조 경로를 그대로 본뜬다

이미 같은 문제를 푼 자산이 있다. 간접정범은 비후보 참가자를 `OffenseInstanceKey` 없이
predicate 수준에서 평가한다([`utilized_participant_outcome.py:71-108`](../../src/idpr/v2/runtime/utilized_participant_outcome.py#L71-L108)).
그 universe는 `participant × (authored capability를 가진 offense)`로 희소하게 열린다.

제151조도 같은 모양으로 만든다.

```
linked_offender (아래 2-3)
  × 이 case의 instance universe에 이미 있는 offense_ref 중
    authored penalty class가 "벌금 이상"인 것
→ LinkedOffenderOutcome  (predicate 수준, instance 아님)
→ Article151QualifyingLink
→ resolve_article_151_liability()
→ legal_element.offender_status_of_object override
```

그리고 `offender_status_of_object`는 **ordinary Call 2 workload에서 제거**한다
(현재 6/6 UNKNOWN을 만드는 잘못된 질문이다).

universe를 case 안에 이미 등장한 offense_ref로 제한하므로 Call 2 증가분은 작다.

### 2-3. `linked_offender`를 어떻게 결박하는가 — 선택지 두 개

**(가) A2의 `directed_action_target`을 재사용한다.** 도피자금 제공 행위가 향한 대상이
곧 제151조의 대상자다. 필드가 하나로 끝나고 프롬프트도 짧아진다.
위험: 한 필드가 "공격 대상"과 "은닉 대상"을 겸하게 되어 의미가 넓어진다 —
`factual_targets`를 거부한 것과 같은 종류의 오염이다.

**(나) `linked_offender` 필드를 따로 둔다.** seed가 제151조일 때만 채운다.
의미가 좁게 유지되지만 필드가 하나 늘고 seed-조건부 필드라는 예외가 생긴다.

> **검수 ③** (가)와 (나) 중 무엇으로 가는가? **권고는 (나)** — 좁은 의미 유지가
> 이 프로젝트가 지금까지 지켜 온 원칙이고, A2 필드를 오염시키면 객체착오까지 같이 무너진다.

### 2-4. "벌금 이상의 형" 을 무엇으로 판단하는가

현재 `OffenseDef`에 형량 메타데이터가 **전혀 없다**(`offenses.yaml`에 penalty 필드 0건).

**제안:** `OffenseDef`에 authored 필드 `statutory_penalty_class`를 추가하고,
값은 `fine_or_greater` / `below_fine` 두 가지. **기본값을 두지 않는다** — 미저작
offense는 링크 자격 판단에서 UNKNOWN으로 떨어진다(fail-closed).

형법각칙의 죄는 사실상 전부 `fine_or_greater`이므로 저작 부담은 작지만,
"전부 벌금 이상이니 host가 True로 간주" 같은 지름길은 쓰지 않는다.

> **검수 ④** 이 필드를 추가하고 현재 저작된 offense 전체에 값을 채우는 것에 동의하는가?
> (동의하면 제가 초안을 채워 별도 워크시트로 다시 올린다 — 조문별 법정형 확인이 필요하다.)

---

## 3. 프롬프트 변경안 (승인 대상 전문)

[`prompts/v2_call15_issue_binding.md`](../../prompts/v2_call15_issue_binding.md)의
binding 필드 목록(34행 `factual_targets` 뒤)에 아래를 **추가**한다. 나머지 줄은 건드리지 않는다.

```markdown
- `directed_action_target`: 원문이 "그 사람인 줄 알고", "…를 겨누어"처럼 행위자가
  겨냥한 대상을 명시적으로 서술한 경우 그 사람 하나. 서술이 없으면 null이다.
  누구를 겨냥했을지 추측하지 않는다.
- `actual_result_bearer`: 원문이 그 행위로 실제 결과를 입었다고 서술한 사람 하나.
  결과 서술이 없거나 대상이 특정되지 않으면 null이다.
- `linked_offender`: 이 seed가 타인의 범죄를 전제로 하는 경우(은닉·도피 대상 등)
  원문이 그 타인으로 지목한 사람 하나. 해당 없으면 null이다.

이 세 필드는 대상을 잘못 알았는지, 그 사람이 죄를 지었는지 판단하지 않는다.
원문이 지목한 대로만 적고, 지목이 없으면 반드시 null이다.
```

wire schema 쪽은 세 필드를 `["string", "null"]`로 required에 추가하고
(모델이 조용히 누락하지 못하게 required로 둔다), 검증에서 episode participant
소속을 강제한다.

> **검수 ⑤** 이 프롬프트 문구를 그대로 설치해도 되는가?

---

## 4. 설치 후 재실행 범위

| 단계 | 재실행 | 이유 |
|---|---|---|
| Call 1 routing | ✗ | offense universe 불변 (A3·A4가 들어오면 그때 재실행) |
| Call 1.5 | **✓ 26문항** | wire schema·프롬프트 변경 |
| planner | ✓ | 결정론적 |
| Call 2 | **✓ 1회만** | A3·A4·B·C까지 모두 모은 뒤 마지막에 |
| symbolic / AnswerPlan / Call 3 | ✓ | 결정론적 + Call 3 |

`758 target`은 invariant가 아니다. 늘거나 줄어드는 것이 정상이다.

---

## 5. 검수 항목 요약

| | 내용 | 권고 |
|---|---|---|
| ① | "원문 명시" 봉쇄로 `directed_action_target`의 인식성 문제가 충분히 막히는가 | 충분하다고 봄 |
| ② | 위법성조각 전제사실 착오 cue는 이번에 열지 않는다 | 열지 않음 |
| ③ | `linked_offender`를 별도 필드로 둘 것인가 | 별도 필드 (나) |
| ④ | `statutory_penalty_class`를 authored 필드로 추가할 것인가 | 추가 |
| ⑤ | §3 프롬프트 문구 설치 승인 | — |
