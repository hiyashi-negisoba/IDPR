# Call 2 realization/source-binding link downstream impact

2026-08-14. Call 1.5 output contract와 활성 prompt를 바꾸기 전에, guard-aware 정본의 **452개
scheduled target 전체**에서 cross-realization source link 부재가 실제 downstream에 미치는 범위를
측정했다. 이 실험은 Call 1.5, production Call 2, N/P를 변경하지 않는다.

## 입력과 계약

- all-target placement packet:
  `diagnostics/all_scheduled_target_placement_452_v1.{json,md}`
- 수동 확정 candidate packet:
  `diagnostics/realization_link_candidates_26_v1.json`
- downstream impact:
  `diagnostics/realization_link_downstream_impact_26_v1.json`
- all-target packet sha: `fe30494a0a801800a02fb7b6888b1a9e4c9240a03417e2fb9571e767f9900ddd`
- candidate packet sha: `cd3849ffc68ca6cfce9012ad6ba01ca93024171ed0f53a0392fc64a2955c3a6f`
- impact packet sha: `46c7fd09ec5175f85c58428e899a824ff6cb96332cbc0a98b6e1b2d83c2a8ddf`

452개를 모두 provenance audit에 넣으면 heuristic bucket은 cross-episode same-actor 7,
derived exact-actor source 4 등을 낸다. 이를 그대로 link 결함 수로 세지 않았다. injury와 그
결과적 가중범이 서로를 "다른 episode 후보"로 잡는 대칭 false positive, 이미 local carrier가
충분한 target, participation actor target을 원문과 source chain으로 제외했다.

최종 candidate는 **동일 actor의 절취 source와 여러 episode에 걸친 강도 realization 사이에서
`taking_conduct`를 소비하는 target**만으로 좁혔다. 따라서 앞서 확인한 factual-episode carrier
118개나 participant-local taking을 이 숫자에 섞지 않는다.

## 정확한 범위: 2문항, 5 target

| case | target | 정본 truth | source | 분류 |
| --- | --- | --- | --- | --- |
| `r11_p1_q1` | 乙 robbery / `binding:004` | UNKNOWN | theft `binding:001` = TRUE | cross-episode link 직접 소비 |
| `r11_p1_q1` | 乙 robbery-causing-injury / `derived_binding:001` | TRUE | 위 source의 transitive consumer | 이미 known |
| `r14_p2_q1` | 乙 quasi-robbery / `binding:003` | TRUE | theft `binding:001` = UNKNOWN | 이미 known |
| `r14_p2_q1` | 乙 robbery-causing-intentional-injury / `binding:004` | TRUE | 같은 theft source | 이미 known |
| `r14_p2_q1` | 乙 robbery-causing-injury / `derived_binding:001` | UNKNOWN | 현재 exact source `binding:003` = TRUE | 기존 provenance projection 문제 |

즉 구조상 link consumer는 **5개**지만 정본에서 이미 TRUE인 것이 3개다. UNKNOWN은 2개뿐이고,
그중 `r14_p2_q1` derived target은 새 Call 1.5 cross-episode link가 없어도 현재
`source_binding_ids = [binding:003, binding:002]`와 immediate source truth로 해결 가능한 종류다.
새 upstream contract가 실제로 필요한 후보는 `r11_p1_q1`의 직접 robbery target **1개**까지
줄어든다.

이 5개 중 participation stage가 소유하는 target은 0개다. 망보기·제안·distraction actor의 local
`taking_conduct`는 이번 candidate에서 제외했으며, principal truth를 복사하지 않는다는 기존
계약을 유지했다.

## counterfactual

두 UNKNOWN만 검수된 carrier의 known 값으로 바꿨다.

1. `r11_p1_q1` robbery taking: UNKNOWN -> TRUE
2. `r14_p2_q1` derived robbery-causing-injury taking: UNKNOWN -> TRUE

이는 새로운 gold truth나 모델 성능 주장용 patch가 아니다. **두 blocker가 해소된다는 최선의
경우에도 downstream이 얼마나 움직이는지** 재는 upper-bound counterfactual이다. target universe,
나머지 450 assessment, relation truth, participation truth는 두 arm에서 동일하다.

guard-aware Call 2에는 participation assessment가 없으므로 동결된
`participation_call2_v4_necessary_gate`를 두 arm에 똑같이 병합했다. 기존 mode 충돌
`r12_p2_q1_ga` 한 문항은 typed quarantine했으며 이번 두 candidate case와 무관하다. registry는
bribe-delivery 수정 뒤의 현재 정의를 두 arm에 동일하게 사용했다. 따라서 이 진단은 두 arm의
**차이**만 귀속하며, 새 production lineage라고 부르지 않는다.

## downstream 결과

| 측정 | 결과 |
| --- | ---: |
| 구조적 consumer | **5 target / 2 case** |
| 이미 TRUE | **3 target** |
| counterfactual truth 변경 | **2 target** |
| symbolic liability chain 변화 | **1 target / 1 case** |
| final responsibility 변화 | **0 case** |
| AnswerPlan 생성 blocker 제거 | **2 case** |
| required-final conclusion 확정 전환 | **0 case** |

`r11_p1_q1` robbery는 completion이 `unresolved -> completed`로 진행했지만 elements가 여전히
unresolved라 liability와 final responsibility는 바뀌지 않았다. `r14_p2_q1` derived target은 다른
blocker 때문에 symbolic output이 전혀 바뀌지 않았다.

다만 AnswerPlan의 GroundFact consistency guard에는 영향이 있다.

- baseline: 22/26 생성. `r11_p1_q1`, `r14_p2_q1` 포함 4문항 conflict failure.
- counterfactual: 24/26 생성. 위 두 문항 failure만 정확히 사라짐.
- 남은 `r13_p1_q1`, `r14_p2_q2` conflict는 이번 link와 무관함.

따라서 두 target은 최종 법적 결론을 개선하지는 않았지만 current AnswerPlan을 만들 수 없게 하는
artifact consistency 문제다. 기존 N/P는 과거 Call 2 lineage로 이미 생성된 것이므로 이 결과를
근거로 재생성하지 않았다. 새 essay 품질 상승은 아직 입증되지 않았고, counterfactual
AnswerPlan에서도 두 범죄군의 required conclusion은 다른 UNKNOWN 때문에 확정으로 전환되지 않는다.

## 판단

**Call 1.5 output contract와 활성 prompt를 다시 여는 것은 impact gate를 통과하지 못한다.**

- 실제 새 cross-episode upstream link가 필요한 것은 1 target이다.
- final responsibility 변화는 0이다.
- essay의 required conclusion 확정 전환도 0이다.
- Call 1.5를 바꾸면 26문항 전체 하류를 다시 만드는 비용과 drift가 생긴다.

대신 작은 수정 후보를 둘로 분리한다.

1. `r14_p2_q1`은 이미 있는 `source_binding_ids`에서 actor-bound GroundFact를 exact source로
   project하는 deterministic 경로 후보이다. Call 1.5 prompt 변경이 필요 없다.
2. `r11_p1_q1` 한 건은 final/conclusion 영향이 없으므로 지금은 production prompt를 열지 않는다.
   26/26 AnswerPlan 생성에 필요할 때만, post-theft robbery realization에 theft source를 연결하는
   좁은 typed link를 별도 승인한다. same actor + same predicate 자동 복사는 금지한다.

즉 realization-link 대형 구조 변경은 여기서 끊는다. 다음 Call 2 품질 작업은 A를 무한히 넓히지
말고 C 초literal 후보와 D authored dispute route로 넘어간다. N/P는 계속 동결한다.

