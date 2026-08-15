# Rulebase → Pipeline 전수감사 보고서

**감사 기준:** 마지막 전수검사 기준 `deadline_v2_0808` / `64fecbf7df3dcd3c8a6f62f12c405ec4cfa02ae9`
**목적:** 기존 pipeline 구조감사 이후에도 남아 있던 **Definition/Rule → Runtime/Pipeline 배선 누락**, KCL-active representation gap, authoring 계약 불일치를 확인하고 structural freeze 전 수정 범위를 확정한다.

---

## 1. Executive Summary

기존 감사에서는 주로 다음 pipeline을 순방향으로 검증했다.

```text
Call 1
→ Call 1.5
→ planner/carrier
→ Call 2
→ symbolic
→ final responsibility
→ AnswerPlan
→ Call 3
```

그 결과 scheduler, participation, doctrine, lineage, carrier, excess, Call 3 fidelity 등 다수의 구조 단절을 제거했고, 최종 production E2E에서 다음을 확인했다.

* Call 2: 26/26
* 758 planned target 중 691 asked
* external opener:

  * doctrine 39/39
  * participation mode requirement 27/27
  * participation candidate probe 4/4
* participation TRUE relation 17건 downstream 경로 손실 0
* active doctrine 5건 downstream 경로 손실 0
* symbolic 26/26
* AnswerPlan 26/26
* Call 3 26/26

그러나 이후 UNKNOWN 진단 과정에서 **제151조 `offender_status_of_object`가 모델 평가 대상이 아님에도 Call 2에 들어가 6/6 UNKNOWN**인 것이 발견되었다.

이를 계기로 감사 방향을 반대로 전환했다.

```text
Definition / Rule
→ 이 값의 authoritative source는 무엇인가?
→ producer가 존재하는가?
→ production caller가 존재하는가?
→ runtime truth/state에 들어가는가?
→ 실제 legal consumer가 사용하는가?
```

이 방식으로 Definition Registry와 특수 runtime을 전수대조한 결과, **제151조 하나만의 우연한 누락이 아니었다.**

현재 결론은 다음과 같다.

> **기존 UNKNOWN 폭증의 대부분은 여전히 Call 2 / definition authoring 문제다.**
> 그러나 KCL 정답 coverage에는 UNKNOWN 숫자로 드러나지 않는 더 중요한 rulebase gap들이 존재한다.
> 이들은 structural freeze 전에 가능한 한 닫는 것이 맞다.

특히 아래 네 항목은 **현재 KCL 정답 trajectory에 직접 영향을 주므로 freeze 전에 처리하는 것을 권고한다.**

1. Article 151 linked-liability route
2. intended-object factual representation
3. assault offense family
4. stolen-property offense family

---

# 2. 감사 범위와 방법

이번 감사에서는 sealed-59 사례 본문을 새로 열지 않았다. 따라서 eval leakage 없이 다음만 검사했다.

### 검사 대상

* `GroundFactDef`
* `LegalElementDef`
* `PrimitiveDef`
* `ElementBundleDef`
* `ExportedComponentDef`
* `OffenseDef`
* `DerivedOffenseDef`
* `QualifierDef`
* `RelationDef`
* completion policies
* participation policies
* mistake / excess policies
* doctrines / doctrine cues
* concurrence / absorption rules
* representation gaps
* special statutory runtime
* Definition Layer schema
* 8-axis type checker
* production planners / orchestration / symbolic consumers
* KCL inventory 및 rubric metadata

### 감사 기준

각 executable rule마다 아래 ownership chain을 확인했다.

```text
authored rule
→ source type
   neural / structural / host-derived / symbolic / constant
→ producer
→ production reachability
→ truth injection
→ legal consumer
```

그리고 다음 두 경우를 별도 결함으로 보았다.

```text
A. authored executable semantics인데 producer/consumer가 없음
B. 동일 semantics를 YAML과 코드 등 둘 이상의 authority가 소유
```

---

# 3. UNKNOWN 폭증과 이번 감사의 관계

최종 production Call 2 결과는 다음과 같다.

| 지표                           |               결과 |
| ---------------------------- | ---------------: |
| Call 2 UNKNOWN               | 418 / 691, 약 60% |
| TRUE                         |              248 |
| FALSE                        |               25 |
| offense instance             |              122 |
| established                  |          21, 17% |
| elements 단계 정지               |               69 |
| completion 단계 정지             |               32 |
| AnswerPlan unresolved anchor |          93, 76% |

이번 rulebase 감사가 이 418 UNKNOWN을 **전부 설명하지는 않는다.**

오히려 두 종류를 구별해야 한다.

### 3.1 실제 UNKNOWN을 만드는 wiring gap

대표가 Article 151이다.

```text
offender_status_of_object
→ linked liability로 host가 결정해야 함
→ production linked-liability route 없음
→ Call 2에 잘못 질문
→ 6/6 UNKNOWN
```

이런 항목은 수정하면 raw UNKNOWN도 감소한다.

하지만 현재 발견된 직접 사례의 규모는 수백 건이 아니다.

### 3.2 UNKNOWN에도 나타나지 않는 missing branch

더 중요한 것은 이쪽이다.

예를 들어 폭행치상죄 자체가 registry에 없다면:

```text
offense candidate 없음
→ predicate target 없음
→ Call 2 question 없음
→ UNKNOWN도 없음
→ 정답 trajectory 자체가 없음
```

따라서 **raw UNKNOWN count만으로 rulebase completeness를 평가해서는 안 된다.**

현재 rulebase gap 중 일부는 UNKNOWN을 증가시키는 것이 아니라 오히려 **평가해야 할 branch 자체를 없애기 때문에 UNKNOWN 통계 바깥에 존재한다.**

이 때문에 현재 76% unresolved와 rulebase coverage를 별개로 봐야 한다.

---

# 4. Structural Freeze 전 KCL-active 수정 사항

## P0-R1. Article 151 linked-liability route

### 현 상태

`legal_element.offender_status_of_object`는 definition상 다음 의미다.

> 대상자가 벌금 이상의 형에 해당하는 죄를 범한 사람인지 여부는 linked offense instance의 qualifying liability result로만 결정한다.

즉 neural predicate가 아니다.

runtime에는 이미:

```text
Article151QualifyingLink
resolve_article_151_liability()
```

가 존재하며 raw target-instance truth를 override하도록 올바르게 구현되어 있다.

하지만 production에는 두 단계가 빠져 있다.

```text
linked offense identity 생성
→ Article151QualifyingLink 생성
→ resolver 호출
```

특히 현재 `IssueBinding`에도 이를 표현할 typed linked-offense representation이 존재하지 않는다.

따라서 단순 caller 한 줄 누락보다 큰 gap이다.

### KCL 영향

`r10_p2_q2`가 직접 영향을 받는다.

rubric은 丙의 범인도피죄에서:

* 乙이 벌금 이상의 형에 해당하는 죄를 범한 자인지
* 丙의 도피자금 제공
* 범인도피죄 성립

을 직접 요구한다.

따라서 **freeze blocker**다.

### 필요한 수정

```text
typed linked-offender/offense identity
→ linked offense liability
→ Article151QualifyingLink
→ resolve_article_151_liability()
→ offender_status_of_object override
```

그리고 이 predicate는 정상 연결 후 ordinary Call 2 neural workload에서는 제거되어야 한다.

---

## P0-R2. Intended-object factual representation

현재 `gap.intended_object_identity` 때문에 다음을 표현할 수 없다.

```text
행위자가 향한 대상
vs.
실제로 결과가 발생한 대상
```

기존 `factual_targets`를 intended object로 재해석하는 것은 이미 금지되어 있다. 그 필드는 counterpart, recipient 등 더 넓은 의미를 가지므로 host가 사실을 만들어내게 된다.

필요한 구조는 좁은 typed factual representation이다.

예:

```text
directed_action_target
actual_result_bearer
```

그리고 host는 둘이 모두 존재할 때만 structural하게:

```text
relation.intended_object_divergence
```

를 도출해야 한다.

### KCL 영향

representation gap 파일 자체가 `affects_kcl26: 9`를 기록하고 있다.

대표적으로:

* `r10_p2_q1`: 乙을 상해하려다가 C를 乙로 오인
* `r12_p2_q1_ga`: A를 살해하려 했으나 B를 A로 오인

등에서 객체착오가 핵심 rubric이다.

또 이 representation gap은:

```text
legal_element.object_misidentification
mistake_policy.korean_law_concrete_fact
```

뿐 아니라 `mistaken_justifying_circumstance`의 안정적인 raising도 막고 있다.

### 2026-08-15에 드러난 두 번째 결함 — 이쪽이 실제 structural blocker였다

감사는 A2를 representation gap 하나로 보았으나, 그 gap을 닫아도 정책은 발화하지 못했을 것이다.

**`applies_to: offense_instance` probe에는 target producer가 아예 없었다.**
`policy_probe_targets`는 참가 후보(`participation_candidate`)만 처리한다. 그래서 착오 정책의
neural leaf가 한 번도 계획된 적이 없고, `apply_mistake_policy`는 테스트만 있고 production
호출부가 없었다. 저작·런타임·Scallop 경로가 모두 갖춰진 채로 정책이 어떤 사건에서도 발화할 수
없는 상태 — **제33조 단서에서 이미 한 번 나온 고장과 같은 모양이다.**

즉 P0-R2는 "표현 공백" 하나가 아니라 **표현 공백 + producer 부재** 두 겹이었다.
`5529287`에서 둘 다 닫았다.

### 필요한 수정

기존 field를 재해석하지 않고 **새 factual representation을 추가**한다.

그 후:

```text
directed target / actual bearer
→ structural divergence
→ mistake policy
```

를 연결한다.

가능하면 같은 factual identity를 이용하여 현재 representation gap으로 꺼둔 `mistaken_justifying_circumstance` cue도 재검토한다.

---

## P0-R3. Assault offense family

현재 다음 family가 없다.

```text
offense.assault
offense.special_assault
derived_offense.assault_causing_injury_or_death
```

이는 단순 registry completeness 문제가 아니다.

### KCL 영향

`r11_p1_q1`에서 직접 필요하다.

rubric은:

```text
乙: 준강도치상 불성립
→ 폭행치상죄 성립

丙: 乙의 폭행치상은 공동범행의 질적 초과
→ 책임 없음

甲: 교사한 절도에 대한 폭행치상은 질적 초과
→ 책임 없음
```

을 요구한다.

현재는 excess machinery가 있어도 비교 대상 offense 자체가 없으므로 이 reasoning path를 표현할 수 없다.

### 필요한 수정

폭행죄 family를 Definition Layer에 정상적으로 저작하고 기존 excess/participation/concurrence machinery와 연결한다.

특정 KCL 정답을 host heuristic으로 박아 넣어서는 안 되고, 기존 DSL의 offense/derivation 구조로 처리해야 한다.

---

## P0-R4. Stolen-property offense family

현재 다음이 없다.

```text
offense.stolen_property_acquisition
offense.stolen_property_custody
```

### KCL 영향

`r10_p2_q1`에서 직접 필요하다.

정답 trajectory는:

```text
장물보관죄 성립
→ 이후 보관 장물 영득
→ 횡령은 불가벌적 사후행위
→ 별도 횡령죄 불성립
```

이다.

장물보관죄가 존재하지 않으므로 현재 absorption rule 자체를 완성할 수 없다.

### 필요한 수정

장물죄 family를 저작하고 기존 concurrence/absorption layer에서 해당 관계를 표현한다.

---

# 5. Freeze 전에 같이 닫을 structural hardening

아래는 현재 KCL 결과를 반드시 바꾸는 문제는 아니지만, 이번에 같이 닫는 편이 비용 대비 효과가 높다.

## H1. Qualifier menu single-source

`OffenseDef.qualifiers[]` schema는 “이 offense에 적용 가능한 qualifier menu”라고 선언한다.

그러나 현재:

* base offense의 `qualifiers:` 선언: **2곳**
* 실제 QUALIFY derived offense: **11건**

즉 9개 QUALIFY는 선언된 menu 밖에서 실행된다.

현재 derivation 자체가 틀렸다고 볼 이유는 없지만:

```text
OffenseDef.qualifiers
vs.
DerivedOffense.derivation
```

두 authority가 서로 다른 언어를 정의하고 있다.

### 조치

둘 중 하나를 정해야 한다.

**권고:** `qualifiers[]`를 authoritative applicability contract로 유지한다면 실제 menu를 완전 저작하고 compiler/checker가 membership을 강제한다.

아니라면 해당 field를 normative menu로 설명하지 않도록 contract를 바꿔야 한다.

---

## H2. Article 263 single-source — **4-authority drift로 승격 (2026-08-15)**

> 감사 당시 2중으로 보았으나 실제로는 **네 곳**이 같은 semantics를 소유하고 있었다:
> offense YAML, dedicated Call 2 wire 튜플, `statutory.py`의 resolver, Scallop backend.
> resolver와 backend가 저작을 읽도록 단일화하고 wire 순서는 테스트가 못박는 것으로 닫았다
> (`015f267`).

YAML은:

```text
statutory_deeming.requires
```

에 3개 predicate를 저작한다.

Article263 dedicated route는 같은 3개를:

```text
ARTICLE263_PREDICATE_REFS
```

로 다시 하드코딩한다.

현재 두 값은 정확히 일치하므로 결과 오류는 없다.

하지만 YAML 변경 시 dedicated Call 2 route가 따라오지 않는 **two-authority contract**다.

### 조치

dedicated route가 definition의 `statutory_deeming.requires`에서 executable refs를 읽도록 단일화한다.

---

## H3. `blocked_when` target collection — **latent이 아니라 active blocker였다 (2026-08-15)**

> 감사는 completion 쪽만 보고 "현재는 실제 bug가 발생하지 않는다"고 판단했다. 그 판단은
> completion에 대해서는 맞지만 **doctrine에 대해서는 틀렸다.**
>
> defeat doctrine 5개가 blocker에만 등장하는 predicate를 저작하고 있다 —
> `self_induced_disorder`(자초한 심신장애), `self_induced_coercion`(자초한 강요상태),
> `duty_bound_to_endure_danger`(위난감수의무), `statutory_bar_on_consent`(승낙의 법률상 제한,
> 2개 doctrine 공유). 이 leaf들은 다른 어디에도 없으므로, closure가 수집하지 않으면 target이
> 생기지 않고 → 묻지 않고 → UNKNOWN → **그 예외들이 어떤 사건에서도 발동하지 않는다.**
> 원인에 있어서 자유로운 행위가 심신장애를 깨뜨리는 경로가 통째로 죽어 있었다는 뜻이다.
>
> closure와 planner 양쪽에 넣어 닫았다(`015f267`, `3608840`). 변경 전후 대조로 정확히 그
> 5건만 늘고 completion frontier와 `candidate_offense_refs`는 동일함을 확인했다.

runtime과 checker는 `blocked_when`을 처리하지만 일부 generic planner/closure predicate collector는 직접 수집하지 않는다.

현재는 blocker인 `means_or_object_defect`가 다른 completion state에도 등장하므로 target이 열려 실제 bug가 발생하지 않는다.

하지만 blocker-only predicate를 저작하면:

```text
target 미생성
→ UNKNOWN
→ blocker fail-open
```

이 될 수 있다.

### 조치

`blocked_when` leaf도 planner/closure dependency traversal의 정식 입력으로 포함한다.

---

## H4. `candidate_materialization` ref checker

`binding_sets` / `distinct_actor_binding_sets`는 실제 candidate를 여는 executable metadata다.

현재 작성된 refs는 모두 유효하다.

하지만 checker는 해당 offense refs를 검증하지 않으므로 typo가 생기면:

```text
invalid ref
→ candidate materialization 실패
→ 단순히 binding이 없었던 것처럼 조용히 사라짐
```

이 가능하다.

### 조치

Definition reference checker에 추가한다.

---

# 6. 현재 KCL-active로 확인되지 않은 gap / latent issue

이들은 이번 freeze에서 전부 기능 구현할 필요는 없다.

다만 **지원되는 기능처럼 보이면서 실제로는 작동하지 않는 상태는 금지**해야 한다.

## Article 33 `co_principal`

Definition은:

```text
instigator
aider
co_principal
```

모두 지원한다고 저작하지만 실제 redirection path는 derivative participation 중심이고 공동정범 branch는 production에서 도달할 수 없다.

현재 KCL-26에서 이 specific branch가 반드시 필요한 사례는 이번 감사에서 확인하지 못했다.

따라서 둘 중 하나면 된다.

1. 실제 co-principal path 구현
2. 현 baseline에서는 미지원이라고 typed representation gap으로 승격

**silent capability mismatch인 현재 상태만 제거하면 된다.**

---

## `LegalElement.grounded_by`

schema는 GroundFact assessment가 LegalElement evaluation을 feed한다고 설명한다.

하지만 generic runtime consumer는 없다.

현재 registry 사용량은 **0**이므로 KCL 영향도 없다.

### 조치

지금 기능 구현까지 할 필요는 없다.

대신:

* 아직 unsupported라고 checker가 금지하거나,
* 실제 implementation이 들어올 때까지 schema capability를 축소

하는 편이 안전하다.

---

## `participation_constraints.disabled_modes`

generic contract에는 존재하지만 실제 Call1.5-P factual participation production path는 이를 소비하지 않는다.

현재 사용량 **0**.

`grounded_by`와 동일하게 당장 구현보다 fail-closed contract가 우선이다.

---

## Generic structural relation

Relation schema는 `evaluation: structural`이면 runtime이 binding에서 resolve한다고 일반적으로 표현하지만 generic structural relation engine은 없다.

현재 사용 중인 `relation.intended_object_divergence`는 이미 explicit representation gap으로 기록되어 있으므로 **silent bug는 아니다.**

---

# 7. Authoring Review — Structural bug와 분리할 것

## `means_or_object_defect`

현재 실측:

```text
45 asked
TRUE 1
UNKNOWN 44
FALSE 0
```

그리고 이 때문에 `dangerousness`도 거의 전부 UNKNOWN이다.

다만 `GroundFactDef`는 애초에 `legal_standard`가 필수가 아니다.

따라서:

> `legal_standard` 부재 = schema/structural bug

라고 보면 안 된다.

문제는 해당 predicate의 positive meaning과 semantic exclusions가 **FALSE를 안정적으로 판정할 수 있게 저작되어 있는가**다.

따라서 이 항목은:

> **법률/definition authoring review**

로 남긴다.

프롬프트나 정의는 승인 없이 수정하지 않는다.

---

## 기타 0-TRUE predicates

예:

```text
dangerous_weapon_carriage
bribe_promise
job_relatedness
...
```

일부는 모든 응답이 UNKNOWN이지만, sealed 사례를 열지 않고는:

```text
실제로 사실이 없음
vs.
Call2 판독 실패
```

를 구별할 수 없다.

따라서 현재는 **미측정**으로 유지한다.

---

# 8. Explicit representation gaps 중 KCL 영향

현재 gap 파일에는 적어도 다음이 있다.

### `gap.intended_object_identity`

* KCL 영향 큼
* 지금 닫는 것을 권고
* 객체착오 및 doctrine raising과 연계

### `gap.assault_offense_family`

* `r11_p1_q1` 직접 영향
* 지금 저작 권고

### `gap.stolen_property_offense_family`

* `r10_p2_q1` 직접 영향
* 지금 저작 권고

### `gap.justifying_premise_vs_object_identity`

* doctrine 자체는 구현돼 있으나 raising representation이 없음
* intended-object factual representation과 같은 뿌리
* P0-R2를 고친 후 재검토

이 gap들은 **“정답을 UNKNOWN으로 냈다”기보다 “정답 reasoning branch를 표현하지 못한다”는 문제**이므로 KCL 평가 전에 닫는 가치가 높다.

---

# 9. 수정 우선순위

## Phase A — KCL-active gaps

다음 네 개를 먼저 닫는다.

```text
A1. Article 151 linked liability
A2. intended-object factual identity
A3. assault offense family
A4. stolen-property offense family
```

이 단계가 KCL 결과를 실제로 바꿀 수 있다.

---

## Phase B — Structural hardening

같은 변경 묶음에서 처리한다.

```text
B1. qualifier menu authority 단일화
B2. Article263 predicate authority 단일화
B3. blocked_when dependency traversal
B4. candidate_materialization ref checker
B5. Article33 co-principal 구현 또는 explicit gap
```

---

## Phase C — Unsupported schema cleanup

당장 기능 구현하지 않는다면:

```text
grounded_by
disabled_modes
generic structural relation
```

을 “사용 가능하지만 아무도 소비하지 않는 executable field” 상태로 두지 않는다.

**사용 시 checker가 실패하게 하거나 capability description을 축소**하는 것이 맞다.

---

# 10. 수정 후 재실행 정책

중요한 점은 **758 target을 더 이상 invariant로 보면 안 된다는 것**이다.

758은 현재 incomplete rulebase에서 생성된 target universe다.

A2~A4가 들어가면:

* 새 factual representation
* 새 offense candidates
* 새 predicates
* 새 absorption/excess paths

가 생기므로 target 수가 변하는 것이 정상이다.

따라서 수정 후에는:

```text
영향받은 upstream만 재생성
→ deterministic plan regeneration
→ 새 target universe audit
→ planned/carried/scheduled consistency
→ 최종 Call 2 한 번
→ symbolic
→ AnswerPlan
→ Call 3
```

순서로 가야 한다.

모든 변경을 모은 뒤 **Call 2는 마지막에 한 번만** 돌리는 것이 좋다.

특히 새 offense family가 Call 1 routing universe를 바꾸거나 새 factual identity가 Call 1.5 output schema를 바꾸는 경우에는 해당 upstream부터 다시 생성해야 한다. 반대로 qualifier/checker/Article263 single-source 같은 순수 deterministic hardening 때문에 neural stage를 다시 돌릴 필요는 없다.

---

# 11. Structural Freeze 기준 수정

기존 freeze 기준에 이번 감사축을 하나 추가해야 한다.

기존:

```text
planned
→ carried
→ scheduled
→ asked
→ truth
→ symbolic consumer
→ AnswerPlan
→ Call3
```

여기에 **rule-level predecessor**를 붙인다.

```text
authored executable rule
→ exactly one semantic owner
→ reachable producer
→ reachable production caller
→ typed injection
→ legal consumer
→ downstream result
```

그리고 모든 authored executable field는 다음 중 하나여야 한다.

```text
1. production-reachable
2. explicitly unsupported
3. typed representation gap
```

**네 번째 상태인 “schema에는 있는데 아무도 안 읽음”은 허용하지 않는다.**

---

# 11-bis. 2026-08-15 감사 갱신 요약

이번 시공 중 감사 시점에 보이지 않던 세 건이 드러났고, 셋 다 freeze 전 필수로 승격한다.

| | 감사 당시 판정 | 갱신된 판정 | 상태 |
|---|---|---|---|
| `offense_instance` probe producer 부재 | (미발견) | **P0-R2의 실제 structural blocker** — 표현 공백을 닫아도 정책은 발화 못 했다 | 닫힘 `5529287` |
| doctrine `blocked_when` 미수집 | H3, latent | **active blocker** — defeat doctrine 5개가 영원히 발동 불가였다 | 닫힘 `015f267`·`3608840` |
| Article 263 authority | H2, 2중 | **4중 drift** (YAML·wire·resolver·backend) | 닫힘 `015f267` |

공통 교훈은 §11의 freeze 기준에 그대로 들어간다. 세 건 모두 "저작도 런타임도 있는데 그것을
**호출하거나 계획하는 자리**가 없다"는 같은 형태였고, 정적으로 정의만 읽어서는 보이지 않는다.
따라서 freeze 기준의 `reachable production caller` 항목은 **테스트로 강제되어야** 한다 --
제151조 resolver가 Phase 5.1부터 호출부도 테스트도 없이 남아 있었던 것이 그 증거다.

---

# 12. 최종 판정

현재 pipeline 자체는 이전보다 훨씬 안정화되었다.

특히 production E2E에서:

* external Call2 target 전부 질문됨
* participation path 손실 0
* doctrine path 손실 0
* symbolic/AnswerPlan/Call3 전부 관통

이 확인되었다.

따라서 현재 가장 큰 위험은 더 이상 **pipeline stage 간 연결**이 아니라:

> **우리가 저작했다고 믿는 법적 rule/capability가 실제 runtime에 존재하는가**

로 이동했다.

이번 감사에서 확인된 KCL-active 문제는 단순한 정리 작업이 아니다.

* Article151은 실제 정답 offense를 영구 UNKNOWN으로 만든다.
* 객체착오 gap은 여러 KCL 핵심 rubric을 표현하지 못하게 한다.
* 폭행죄 family 부재는 질적 초과 reasoning branch를 제거한다.
* 장물죄 family 부재는 불가벌적 사후행위 reasoning branch를 제거한다.

따라서 **이 네 가지를 그대로 둔 채 KCL rubric 평가를 시작하면 모델/Call2 성능 실점과 rulebase coverage 실점이 섞인다.**

현재 권고는 명확하다.

> **KCL-active 4개 gap을 먼저 닫고, 저비용 structural hardening을 함께 적용한 뒤 rulebase를 freeze한다. 그 후 새 target universe로 final Call2 → symbolic → AnswerPlan → Call3를 한 번 수행하고, 그 결과의 UNKNOWN부터 비로소 Call2/model performance로 해석한다.**

이게 이번 전수감사와 UNKNOWN 분석을 합친 최종 조치안이다.
