# Predicate 사전 확장 — 배치 ④ 총칙 미수론 나머지 (제28·29조) v2

[predicate_dictionary_ext_batch04_v1.md](predicate_dictionary_ext_batch04_v1.md)에 대한 사용자
검수 1건 반영 — `purpose_to_commit_target_offense`의 `when`/`requires` 배치 정정 +
2패스 시 `suspends`/`relation_dispositions` 저작 필요성 명기. 나머지(종범 불성립·31조
연결의 2패스 확인 이월 등)는 v1 그대로 유지, 29조는 변경 없음.

---

## 정정 — `purpose_to_commit_target_offense`는 `when`이 아니라 `requires`

**v1 오류**: `PREPARATION_OR_CONSPIRACY.when`에 목적 요건까지 넣었는데, Completion
설계에서 `when`은 **어느 state인지를 선택하는 조건**이고 `requires`는 그 state에서
**Elements에 추가로 요구되는 요건**이다. `purpose_to_commit_target_offense`는 state를
가르는 사실이 아니라 예비·음모의 주관적 성립요건이므로 `requires` 쪽이 맞다.

**v2(수정)**:

```text
PREPARATION_OR_CONSPIRACY
    when = ALL(
        ANY(preparatory_conduct, conspiracy_agreement),
        NOT(commencement_of_execution)
    )

    requires = purpose_to_commit_target_offense

    punishable = (offense별, 법률에 특별한 규정이 있는 죄만 true — 28조 원칙, 변경 없음)
```

**2패스 저작 시 반드시 채워야 할 것 — `suspends`/`relation_dispositions`.** 예비·음모
단계에서는 목적범죄의 기수 conduct/result/causation 같은 slot들이 아직 충족되지
않은 게 정상이므로, `PREPARATION_OR_CONSPIRACY` state가 이 slot들을 `suspends`로
명시하지 않으면 이후 Elements 단계에서 그 목적범죄 고유 요건 미충족으로 실패해버린다.
이건 신규 구조가 아니라 **Step 6B가 이미 만든 `CompletionPolicyDef.suspends`/
`relations`를 예비·음모에도 실제로 쓰는 것**이다(pilot 25-27조가 미수 state에서 이미
같은 필드를 채웠던 것과 동일 작업) — 이번 predicate 사전 단계에서 구체적으로 어떤
slot을 suspend할지까지 정하지는 않고, 2패스 저작 시 반드시 채워야 한다는 점만
명시적으로 기록해둔다(조용히 빠뜨리면 axis 8이 잡아낼 결함이므로 검증 단계에서
재확인 가능).

---

## 배치④ v2 요약 — 마감

`PREPARATION_OR_CONSPIRACY`(when/requires 분리 완료) + `voluntary_surrender_before_
execution`(자수, downstream 구조는 21-23조와 함께 결정) + 2패스 시 `suspends`/
`relation_dispositions` 저작 의무 명시로 확정. 종범 불성립·31조 연결은 2패스
확인사항으로 이월(v1 유지). 29조는 v0 그대로. 스키마 변경 없음. 배치④ 종료.
