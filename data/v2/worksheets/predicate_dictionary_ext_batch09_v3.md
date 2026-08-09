# Predicate 사전 확장 — 배치 ⑨ 생명·신체 (제250·254·255·257·259·263·267·268·258의2조) v3

[predicate_dictionary_ext_batch09_v2.md](predicate_dictionary_ext_batch09_v2.md)에 대한
사용자 검수 1건(문구) 반영 — 구조 변경 없음. 나머지는 v2 그대로.

---

## 정정 — "잘못된 branch 조합 자체가 애초에 생기지 않는다"는 표현이 과도했다

**v2의 부정확한 표현**: 정정10에서 268의 `result = ANY(death_of_victim,
injury_result)` / `causation = result_causation` 조합을 설명하며 "잘못된 branch
조합 자체가 애초에 생기지 않는다"고 썼다. 이 표현은 symbolic structure 자체가
death/injury 중 어느 결과와 causation이 연결됐는지를 별도로 binding한다는 뜻으로
읽힐 수 있는데, 실제로는 그런 구조적 binding이 있는 게 아니다.

**v3(정정)** — 아래 두 문장으로 대체:

> result별 causation predicate를 분기하지 않으므로 slot 수준의 잘못된 cross-branch
> 조합을 만들지 않는다. 어느 결과에 대한 인과관계인지는 `result_causation`의 legal
> assessment에서 해당 offense instance의 실제 결과 사실과 함께 판단한다.

`result_causation`이 하나의 법적 판정("현재 offense instance에서 실제로 인정되는
구성요건적 결과와 행위 사이에 인과관계가 인정된다")으로 묶여 있기 때문에
`death_causation`/`injury_causation`을 따로 뒀을 때 생기는 단순 slot cross-match를
피한다는 것이지, 구조가 자동으로 어느 result인지 알아서 연결해준다는 뜻이 아니다 —
predicate 정의나 구조는 바뀌지 않는다, 설명 문구만 정정.

---

## 배치⑨ v3 — 최종 확정, 종료

인과관계 이층 모델(base OffenseDef=`legal_element.result_causation`(250·267·268 공유
신규) / COMPOSE=`relation.causal_nexus`(259)), `death_causation`(기존 fixture 정의
보존, 현재 real Rulebase에서는 미사용) — 전부 v2 확정 그대로. 추가 스키마·DSL
primitive 불필요. 배치⑨(250·254·255·257·259·263·267·268·258의2조) predicate 사전은
이 v3로 종료 — 다음은 배치⑩(성적 자유: 297·298·299·300·301조).
