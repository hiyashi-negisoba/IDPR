# Call 1.5 unbound seed direct-conduct recovery 전수 검토

2026-08-14. Call 1이 이미 선택했지만 Call 1.5가 binding하지 못한 50 seed를 모두 동일한
direct-conduct-only 계약으로 재검토했다. offline gold는 target 선택에 사용하지 않았으며 사후
recall 측정에만 사용했다.

## 계약

- actor 본인의 실행·구체적 준비·착수·부작위·기망만 direct binding 후보로 허용
- 결과 미발생만으로 candidate를 제거하지 않음
- 요청·지시·도움만 있는 actor는 별도 factual-interaction/participation route에 남김
- 모든 quote는 factual scope 안 exact substring으로 host 검증
- 독립 verifier가 seed cue와 direct conduct의 연결을 다시 판정

정본 후보:

- raw: `diagnostics/single_seed_direct_recovery_all50_v1.jsonl`
- verifier: `diagnostics/single_seed_direct_recovery_verify_v1.jsonl`
- merged Call 1.5: `issue_bindings_direct_recovery_v1.jsonl`
- rebuilt plan: `direct_recovery_participation_plan_v1/evaluation_instance_plan.jsonl`

## 결과

- 50 seed 중 raw candidate: 12 seed / 12 bindings
- contract failure: 1
- verifier와 host contract를 모두 통과한 direct binding: 7
- authored aggravated-status -> base-offense carrier closure: 1
- 전체 binding: 78 -> 86
- unbound seed: 50 -> 42
- top-level instance: 87 -> 95
- participation target: 60 -> 60 (후보 폭증 없음)

evaluation-only explicit miss 9개는 기존 top-level 2 / missing 7에서 top-level 5 / missing 4로
변했다. 새로 회수한 것은 강도, 존속살해 carrier, 그리고 authored base offense인 보통살인이다.

## 남은 네 결함

1. `r10_p1_q1_ga` 주거침입은 주거침입강간·치상 특별법 결합범이 Definition Layer에 없어
   단순 offense binding을 넘어 representation 보강이 필요하다.
2. `r10_p1_q3_ga` 범인도피는 丙의 동일 부작위가 직무유기 binding에는 있으나, 법적 대안
   offense가 동일 factual carrier를 공유하는 authored route가 없다.
3. `r12_p2_q1_na`는 타인예비, 예비의 방조, 예비의 중지라는 discussion route가 필요하다.
   (1)의 살인 binding은 target span 밖 context-only이며 (2)의 독극물 구입을 그 정범 살인으로
   승격시키면 안 된다.
4. `r13_p2_q1` 위계공무집행방해는 허위진술이 명시되어도 법적으로 불성립할 수 있다는 이유로
   binding이 사라졌다. negative legal alternative도 평가 carrier를 가져야 한다.

따라서 추가 generic recovery 반복은 중단한다. 남은 네 건은 각각 authored compound offense,
carrier compatibility, preparation dispute route, negative-alternative carrier라는 일반 구조로
해결한다.
