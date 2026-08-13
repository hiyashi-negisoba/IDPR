# Call 3 — Unified IRAC Realization Specification

## 1. 목적

Call 3는 **Scallop까지 끝난 사건 전체의 형사책임 분석을 하나의 장문형 법률답안으로 작성하는 최종 생성 단계**다.

Call 3 자체가 다시 symbolic pipeline을 실행하거나 Scallop의 계산을 재구성하는 단계는 아니다.

그러나 단순한 template renderer도 아니다.

정확한 역할은:

```text
robust symbolic anchors
+
case facts
+
legal reasoning context
+
model's legal-writing / legal-analysis capability
↓
one integrated long-form IRAC answer
```

이다.

즉 **결론의 뼈대는 symbolic result가 잡고, 실제 법리 전개·포섭·쟁점 배열·문장 구성은 모델이 담당한다.**

현재 논문 표현처럼 Call 2 이후 symbolic runtime이 actor/episode identity와 unresolved 상태를 보존하여 typed liability result를 만든다는 구조는 그대로 유지한다. 

---

# 2. 호출 단위

## 반드시 사건당 1회

```text
1 case / sub-question
→ 1 Call 3 request
→ 1 complete answer
```

금지:

```text
offense 1개 → 1 call
actor 1명 → 1 call
issue 1개 → 1 call
section 1개 → 1 call
```

후속 host concatenation도 하지 않는다.

8월 4일에 폐기한 구조가 정확히:

```text
issue별 LLM call
→ host가 죄종별 section 조립
```

이었고, 이를 **전체 Scallop 결론을 한 request에 넣는 단일 unified IRAC call**로 바꿨다. 

---

# 3. Call 3 입력의 최상위 구조

Call 3에는 최소한 다음 네 덩어리가 들어간다.

```text
A. Original Case
B. Original Question
C. Symbolic Answer Context
D. Coverage / Open-Issue Context
```

여기서 중요한 것은 **C를 raw Scallop trace dump로 주지 않는 것**이다.

v2 중간 실행에서 raw trace를 그대로 generation 쪽에 넘겼다가 participation route, principal, completion, decisive obligation, doctrine 같은 답안 작성에 중요한 정보가 사라지는 문제가 있었다. 따라서 Scallop 결과와 Call 3 사이에 **AnswerPlan / typed answer context**가 필요하다. 현재 architecture 문서도 이 중간 표현을 명시하고 있다. 

---

# 4. A — Original Case

사건 원문 **전문**을 준다.

```text
case_text
```

Call 1.5의 evidence quote들만 가지고 답안을 쓰게 하면 안 된다.

Call 1.5 quote는 symbolic provenance를 위한 좁은 근거이고, Call 3의 자연어 포섭은 사건 전체의 맥락을 읽을 수 있어야 한다.

따라서:

```text
original case text
+
selected provenance
```

둘 다 있어야 한다.

모델은 사건 원문에 없는 사실을 새로 만들어서는 안 된다.

---

# 5. B — Original Question

원 질문도 그대로 준다.

예:

```text
甲과 乙의 죄책을 논하시오.
```

Call 3는 planner가 만들어낸 내부 offense 목록을 답안의 질문으로 착각하면 안 되고, **원래 시험문제가 요구하는 답안 범위**를 기준으로 글을 써야 한다.

---

# 6. C — Symbolic Answer Context

이게 현재 구현해야 할 핵심 handoff다.

단위는 raw predicate가 아니라 **답안에서 논의할 수 있는 legal issue / liability instance**다.

각 항목에는 적어도 다음이 필요하다.

```text
issue_id
actor
offense / legal_issue
factual_episode

final_state

completion
participation
principal

elements_state
unlawfulness_state
culpability_state
punishability_state

doctrines
special_effects
concurrence_effect

decisive_obligations
blocking_obligations

supporting_facts
source_quotes

provenance
```

다만 **이 필드명이 그대로 모델에게 노출될 필요는 없다.**

내부 AnswerPlan은 typed structure로 유지하되, Call 3 payload에서는 사람에게 읽히는 형태로 serialize하면 된다.

---

# 7. final_state

각 symbolic issue에는 최종 상태가 있어야 한다.

대략:

```text
ESTABLISHED
NOT_ESTABLISHED
UNRESOLVED
NOT_ATTRIBUTABLE
ABSORBED
SUPERSEDED / SPECIALTY
```

등 현재 runtime이 실제 산출하는 상태를 canonical vocabulary로 매핑한다.

핵심은 **Scallop final result가 Call 3의 anchor**라는 점이다.

예:

```text
甲 / 절도죄
→ established
```

이면 모델은 절도죄를 불성립이라고 뒤집으면 안 된다.

반대로:

```text
甲 / 상해죄
→ not attributable by excess
```

이면 그 상해 결과를 甲에게 별도 책임으로 되살려서는 안 된다.

---

# 8. completion 정보

단순히 offense 이름과 final_state만 넘기면 부족하다.

예:

```text
completed
attempt
abandonment
preparation
unresolved
```

를 답안 writer가 알아야 한다.

특히 파생범죄/결과적 가중범/미수 관계가 있는 경우:

```text
offense
+
completion state
+
왜 그 state가 나온 것인지
```

가 함께 전달되어야 한다.

---

# 9. participation 정보

공범 instance에는 반드시 다음이 보존돼야 한다.

```text
mode
principal_actor
principal_offense
principal_realization
participation_relation
```

예:

```text
actor: 甲
offense: theft
mode: instigator
principal: 乙
principal realization: established
```

이걸 잃어버리고 단순히:

```text
甲 theft = established
```

만 주면 Call 3가 정범처럼 쓰거나 공범 구조를 임의 재구성할 수 있다.

그래서 **participation route + principal identity는 mandatory handoff**다.

---

# 10. doctrine / legal effect

active doctrine이나 특수효과가 있으면 결과 이름만 던지면 안 된다.

예:

```text
doctrine
stage
effect
truth/result
```

정도는 전달한다.

예:

```text
self-defense
stage: unlawfulness
effect: defeat
```

또는:

```text
Article 33 proviso
effect: participant offense realization transformed
```

등.

단, doctrine이 raised됐지만 active가 아니었던 경우와 실제 법률효과가 발생한 경우는 구별한다.

---

# 11. concurrence / final responsibility

Call 3에는 **Scallop 중간 offense instances 전체 목록보다 Final Responsibility 결과가 우선**한다.

즉 최종 답안의 죄수론은:

```text
raw established offenses
```

가 아니라

```text
after excess attribution
after §33 effects
after concurrence / absorption
final responsibility set
```

을 기준으로 작성한다.

예를 들어 absorbed offense를 다시 독립된 최종 죄책으로 쓰면 안 된다.

---

# 12. decisive obligations

모든 Call 2 predicate를 모델에 덤프하면 안 된다.

답안에 필요한 것은:

```text
왜 성립했는가
왜 불성립했는가
왜 미해결인가
```

를 설명할 수 있는 **결정적 obligation**이다.

따라서 issue마다:

```text
decisive_satisfied
decisive_failed
blocking_unknown
```

을 압축해서 준다.

예:

```text
절취행위: satisfied
불법영득의사: satisfied
타인소유/점유: satisfied
```

또는:

```text
forgery_without_authority: UNKNOWN
purpose_to_use_as_genuine: UNKNOWN
→ Elements unresolved
```

정도다.

213개 raw trace 같은 것을 통째로 Call 3에 넣는 구조는 피한다.

---

# 13. unresolved

이건 v2에서 특히 중요하다.

```text
UNKNOWN ≠ FALSE
```

이므로 symbolic result가 unresolved라면 Call 3도:

```text
불성립한다
```

라고 단정하면 안 된다.

대신 자연어로:

```text
주어진 사실만으로는 이를 확정하기 어렵다.
해당 요건의 인정 여부가 명확하지 않다.
따라서 이 부분은 결론을 단정하기 어렵다.
```

처럼 서술한다.

**internal UNKNOWN marker를 노출하라는 뜻은 아니다.**

---

# 14. D — Coverage / Open-Issue Context

여기가 8월 4일 원안과 이후 지나치게 제한적인 methodology draft를 구분해야 하는 부분이다.

8월 4일 네가 명시적으로 요구한 것은:

> RuleIR 범주 안에 있더라도 모델에게 자유를 주고 Scallop 결과를 전달해서 알아서 쓰게 하자.

그리고 RuleIR/L0에서 놓친:

* 객체의 착오
* 우연방위
* 불능미수
* 불가벌적 사후행위

같은 문제도 모델이 법학지식으로 보완하도록 했다. 

따라서 **Call 3를 “typed handoff에 존재하는 문장만 말할 수 있는 renderer”로 만들면 원래 승인 스펙을 다시 어기는 것**이다.

현재 명세는 두 영역으로 나눈다.

### Symbolically anchored issues

Scallop이 실제로 판단한 부분.

```text
symbolic conclusion = binding anchor
```

모델은 이 결론을 뒤집을 수 없다.

그러나 그 안에서:

* 법리 설명
* 논증 순서
* 구성요건별 서술
* 사실 포섭
* 반대 논거 검토
* 자연스러운 형법 답안 구성

은 자유롭게 한다.

즉 **“결론만 anchor, 글은 자유”**가 원칙이다.

### Open / unsupported issues

Rule base가 지원하지 않았거나 representation gap으로 남은 부분.

여기는 모델에게 법학적 자율성을 준다.

모델은:

```text
case text
+
question
+
its legal knowledge
```

를 사용해 일반적인 형사법 답안처럼 분석할 수 있다.

그리고 8월 4일 원안 취지대로 **명시적으로 전달된 gap뿐 아니라 사건 전체를 읽으면서 필요한 보충 쟁점을 제기하는 것도 허용**한다.

단 하나의 제한은:

> autonomous supplement가 symbolically anchored issue의 확정 결론을 뒤집거나 재정의해서는 안 된다.

---

# 15. 즉 Call 3의 자율성 경계

정확히 이거다.

```text
                    ┌──────────────────────────┐
                    │ Symbolically anchored    │
                    │ issues                   │
                    └────────────┬─────────────┘
                                 │
                conclusion / identity는 고정
                                 │
                exposition / application은 자유
                                 │
                                 ▼

CASE + QUESTION ────────────→ Unified IRAC

                                 ▲
                                 │
                  모델 자체 법학지식 사용 가능
                                 │
                    ┌────────────┴─────────────┐
                    │ unsupported / uncovered  │
                    │ / supplementary issues   │
                    └──────────────────────────┘
```

이게 **8월 4일의 “Scallop은 로버스트한 결론, 모델은 자유로운 포섭”**을 현재 v2에 가장 충실하게 옮긴 형태다.

---

# 16. 출력 구조

JSON 출력이 아니다.

**최종 출력은 완성된 Markdown 또는 plain-text 장문 법률답안 하나**다.

강제적인 machine section schema를 두지 않는다.

다만 system prompt에서 큰 구조만 안내한다.

기본 권고:

```text
I. 쟁점의 정리

II. 각 행위자의 죄책
    필요한 쟁점들을 자연스럽게 통합하여
    Rule → Application → Conclusion 방식으로 논증

III. 죄수 및 종합 결론
```

8월 4일 당시 승인된 표현도 정확히:

```text
I. 쟁점의 정리
II. 죄책별 법리 및 사안의 포섭
III. 종합 결론
```

이었다. 

이건 **rigid schema가 아니라 discourse guidance**다.

모델이 사건 특성상:

```text
I. 甲의 죄책
II. 乙의 죄책
III. 죄수관계
```

처럼 쓰는 것이 더 자연스러우면 그렇게 써도 된다.

---

# 17. 죄종별 mini-IRAC 금지

다음과 같은 기계적 반복은 피한다.

```text
사기죄
  법리
  적용
  결론

횡령죄
  법리
  적용
  결론

절도죄
  법리
  적용
  결론
```

사건 전체에서 여러 쟁점이 서로 연결된다면 큰 논증 안에서 통합한다.

특히:

* 본범 ↔ 공범
* 기본범 ↔ 결과적 가중범
* 구성요건 ↔ 착오
* 정당화사유 ↔ 책임
* 본죄 ↔ 죄수관계

같은 상호작용을 section 경계 때문에 잘라먹지 않는다.

---

# 18. Host의 역할

여기는 원안 그대로 강하게 잡아야 한다.

## Call 3 전

host가 해도 되는 것:

```text
Scallop 결과 읽기
→ AnswerPlan 생성
→ 사람-readable payload 직렬화
→ prompt 생성
→ 모델 호출
```

## Call 3 후

host가 해도 되는 것:

```text
raw answer 저장
metadata 저장
generation provenance 저장
```

그리고 필요하다면 **별도 audit**에서 위반 여부를 기록할 수 있다.

하지만 host는:

* 문단 삽입
* 결론 문장 덧붙이기
* 죄종별 section 재조립
* 모델 문장 수정
* symbolic conclusion을 마지막에 강제 append
* model answer와 symbolic result를 섞어 최종 답안 생성

을 하면 안 된다.

네가 당시 명시한 문장이 정확히:

> “답안 출력에는 호스트가 절대 개입을 안했으면 좋겠어”

였고, 그에 따라:

> “모델이 전체 답안을 자유롭게 쓰고, 호스트는 출력을 그대로 저장만 한다.”

로 바뀌었다. 

---

# 19. 후처리 consistency validation

**답안을 다시 parse해서 host가 고치는 구조는 쓰지 않는다.**

가능한 것은 offline/evaluation audit다.

예:

```text
anchored conclusion reversed?
actor identity mixed?
UNKNOWN converted to acquittal?
absorbed offense resurrected?
internal marker exposed?
```

를 기록할 수 있다.

하지만 이 validator가:

```text
answer rewrite
answer assembly
symbolic sentence injection
```

을 하면 안 된다.

그리고 예전에 논의했던 **semantic back-parse 결과를 production hard-fail로 삼는 방식도 쓰지 않는다.**

---

# 20. 내부 표현 노출 금지

모델에게 내부 자료를 주더라도 최종 답안에서 다음을 그대로 쓰지 않는다.

```text
binding:004
factual_episode:002
offense.theft
UNKNOWN
stage=elements
ParticipationDependencyObligation
Scallop
Call 2
DSL node
source_run=delta
```

자연스러운 법학용어로 번역한다.

예:

```text
elements = unresolved
```

→

```text
주어진 사실만으로는 해당 구성요건 충족 여부를 확정하기 어렵다.
```

---

# 21. Call 3 prompt가 모델에게 명시해야 할 우선순위

우선순위는 이 순서가 맞다.

```text
1. 사건 원문을 왜곡하지 않는다.
2. symbolically anchored final conclusions를 뒤집지 않는다.
3. actor / episode / participation identity를 혼동하지 않는다.
4. unresolved를 임의의 성립·불성립으로 바꾸지 않는다.
5. 위 경계 안에서는 법률가처럼 자유롭게 논증한다.
6. symbolic coverage 밖의 관련 쟁점은 필요하면 스스로 보완한다.
7. 전체 사건을 하나의 통합된 IRAC 답안으로 작성한다.
```

---

# 22. AnswerPlan의 최소 production schema

현재 구현 단계에서 나는 이 정도면 충분하다고 본다.

```text
AnswerPlan
├── case_id
├── case_text
├── question
│
├── anchored_issues[]
│   ├── actor
│   ├── offense_or_issue_label
│   ├── episode_facts
│   ├── final_state
│   ├── completion
│   ├── participation
│   │   ├── mode
│   │   └── principal
│   ├── stage_results
│   ├── doctrines
│   ├── legal_effects
│   ├── concurrence
│   ├── decisive_findings
│   ├── blocking_findings
│   └── provenance
│
├── final_responsibility[]
│
└── open_issues[]
    ├── known_representation_gaps
    └── known_unsupported_issues
```

**중요:** 이건 output skeleton이 아니다.

Call 3가 이 배열 순서대로 1:1 문단을 생성하는 게 아니다.

이건 오직 **모델에게 사건 reasoning state를 손실 없이 전달하기 위한 input representation**이다.

현재 v2 문서도 typed answer representation에는 issue/actor, participation/completion, 핵심 obligation, doctrine/effect, final liability, provenance가 필요하다고 정리하고 있다. 

---

# 23. 현재 문서 중 폐기해야 할 Call 3 설명

조사하면서 중요한 충돌도 하나 찾았다.

일부 8월 13일 초안 문서에는 아직:

```text
host 프로그램이 생성된 분석과 상징 결론을 결합한다
```

가 남아 있다. 

**이건 Call 3 production 명세로 쓰면 안 된다.**

8월 4일 네가 직접 폐기한 host-assembly 구조와 충돌한다.

또 일부 후대 methodology 초안의:

> “Call 3는 typed handoff에 없는 새로운 offense/legal effect를 절대로 추가할 수 없다.”

라는 강한 표현도  **8월 4일에 승인된 autonomous supplementary issue 정책과 그대로는 양립하지 않는다.**

따라서 최종 논문도 나중에는 표현을 이렇게 바꾸는 게 맞다:

> **For symbolically resolved issues, the final model must preserve the derived liability conclusions and typed relations. Within those anchors it remains free to construct the legal exposition, and it may discuss supplementary issues outside symbolic coverage using the case facts and its legal knowledge.**

이게 실제 설계와 맞다.