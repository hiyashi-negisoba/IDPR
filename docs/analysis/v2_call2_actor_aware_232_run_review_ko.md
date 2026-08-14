# Call 2 actor-aware realization evidence 232-target 실행 검수

2026-08-14. guard-aware 정본에서 UNKNOWN이었던 exact target 232개를 세 arm으로 재평가했다.
목적은 UNKNOWN 감소율을 만드는 것이 아니라 **한 문장 evidence의 정보 부족과 prompt drift를
분리하고, actor 오귀속 없이 넓힐 수 있는 범위를 찾는 것**이다.

정본 artifact:

- raw: `diagnostics/actor_aware_realization_232_v1.json`
- analysis: `diagnostics/actor_aware_realization_232_analysis_v1.json`
- 3-arm 사용량: 382,340 tokens
- target: 232개, 세 arm exact key 완전 동일

## 세 arm 계약

1. `current_occurrence`: 현재 production prompt + exact occurrence
2. `actor_prompt_occurrence`: actor-aware candidate prompt + exact occurrence
3. `actor_prompt_context`: 같은 candidate prompt + typed actor-aware context

2와 3은 target grouping과 batching까지 같고 evidence context만 다르다. 따라서 1→2는 prompt
drift이고, **2→3만 evidence carrier 효과**다.

typed context는 target actor의 같은 factual episode에서 다음만 운반한다.

- `same_actor_action_evidence`: target actor 자신의 authored action fragment
- `context_evidence`: 객체·피해자·신분·관계·결과를 이해할 맥락
- `excluded_peer_actor_binding_ids`: 같은 episode의 다른 actor binding을 명시적으로 제외

actor-bound GroundFact 35개에는 context를 주지 않았다. 이 35개는 2→3에서 **35/35 완전
동일**했다.

## 결과

| arm | TRUE | FALSE | UNKNOWN |
| --- | ---: | ---: | ---: |
| current occurrence | 25 | 6 | 201 |
| actor prompt + occurrence | 44 | 10 | 178 |
| actor prompt + context | 62 | 12 | 158 |

prompt만 바꿔도 UNKNOWN 27개가 known으로 이동했다. 그러므로 201→158을 evidence 개선이라고
쓰면 안 된다.

같은 candidate prompt 안의 evidence 효과는 다음과 같다.

- UNKNOWN→TRUE 21, UNKNOWN→FALSE 3
- TRUE→TRUE 41, FALSE→FALSE 9
- TRUE→UNKNOWN 3, FALSE→UNKNOWN 1
- **TRUE↔FALSE 직접 역전 0**

즉 typed context는 24개를 해소했지만 known 4개를 후퇴시켰다. 과거 수동 review 49개와
대조하면 `B_SAFE_EPISODE` 32개 intended agreement는 occurrence 12→context 18로 늘었고,
`C_OVERLITERAL` 17개는 2→5로 늘었다. 그러나 `RU-056 foreseeability`는 의도 TRUE와 반대인
FALSE로 이동했다. 따라서 **carrier 구조는 유효하지만 197개 전면 production 채택은 기각**한다.

## 이 결과가 뜻하는 것

사용자의 진단, 즉 "모델이 한 문장만 보고 UNKNOWN을 남발한다"는 것은 맞다. context만 바꾼
paired arm에서 24개가 해소됐기 때문이다. 동시에 단순한 episode 확대가 명쾌한 최종 해법이
아닌 이유도 확인됐다. 정보가 늘면 법적 포섭이 가능해지지만, possession·foreseeability·공동실행
같이 귀속 또는 규범 판단이 필요한 predicate는 같은 문맥이 오히려 모델을 흔든다.

따라서 남은 production 계약은 길이 기준이 아니라 predicate authoring 기준이어야 한다.

```text
evidence_scope = exact_actor_action
               | same_actor_episode
               | offense_realization

discussion_mode = adjudicative_truth
                | authored_dispute
```

- actor-bound conduct/status GroundFact는 `exact_actor_action`
- 사건 전체의 객체·결과·관계가 필요한 predicate만 reviewed `same_actor_episode`
- 여러 episode가 한 범죄를 만드는 경우에만 upstream-authored `offense_realization`
- 학설·판례 대립은 evidence를 넓혀 TRUE/FALSE로 없애지 않고 `authored_dispute`

다음 final Call 2 전에 registry에 이 scope를 명시하고, reviewed safe subset에서 regression 0을
확인해야 한다. 현재 candidate prompt와 carrier는 진단 구현으로 보존하되 active production
prompt는 바꾸지 않는다.

