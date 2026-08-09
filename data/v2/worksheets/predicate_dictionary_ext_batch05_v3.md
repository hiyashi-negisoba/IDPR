# Predicate 사전 확장 — 배치 ⑤ 총칙 공범과 신분·간접정범 (제33·34조) v3

[predicate_dictionary_ext_batch05_v2.md](predicate_dictionary_ext_batch05_v2.md)에 대한 사용자
검수 1건 반영 — 34조 compatibility question의 정밀도만 조정. 나머지는 v2 그대로.

---

## 정정 — 34조: stage 결과만으로는 부족하다, predicate-level 원인 구별까지 필요할 수 있다

**v2의 미진한 부분**: "`elements`/`unlawfulness`/`culpability`의 `gate_state`를
세밀하게 참조"라고 했는데, `gate_state`만으로는 부족하다 — 예를 들어 Elements가
`"fails"`라는 사실만으로는 그게 고의 결여인지, 신분 결여인지, 목적 결여인지, 행위
자체의 결여인지 구별이 안 된다. 34조는 이 원인을 구별해야 할 가능성이 있다(예:
목적범에서 목적만 없는 피이용자를 이용한 경우와 고의 자체가 없는 피이용자를 이용한
경우는 34조 워크시트에서 서로 다른 논의로 다뤄진다).

**v3(수정)**:

```text
34조 compatibility question:

피이용자 쪽의
    - LiabilityEvaluation의 stage별 결과(gate_state 등)
    - 그 stage 판정을 구성한 개별 predicate truth(어느 leaf가 실패의 원인이었는지)
    - 필요한 경우 다른 offense_ref에 대한 evaluation 결과(과실범으로만 성립한 경우)

를 이용자 쪽 symbolic dependency에서 선택적으로 참조할 수 있는가?
```

---

## 배치⑤ v3 요약 — 최종

```text
A. 33조 단서 — cross-actor + cross-offense derivative target
   6C core는 가능성 높음, caller/orchestrator(Step 7/8)가 실제로 그 조합을
   호출하는지만 확인하면 된다.

B. 34조 — cross-actor + fine-grained symbolic-state dependency
   stage 결과만이 아니라 필요하면 predicate-level 원인 구별과 다른 offense_ref의
   결과까지 참조해야 할 수 있다 — 2패스 실제 저작 시 기존 구조로 가능한지 확인.
```

나머지(33조 본문 공동정범의 `attributable_slots` 오용 철회, `agent_unpunished_or_
negligent` LegalElement 제거, `instrumentalization_of_agent` 보류, `supervisory_
relationship` 축소)는 v1-v2 그대로. 배치⑤ 종료.
