# Call 2 guard-aware scheduling 26문항 실행 검토

2026-08-14. `docs/analysis/v2_call2_unknown_causes_ko.md`의 UNKNOWN 3분할 중
**죽은 completion 가지 타깃**을 처리한 뒤, 정본 531-target plan으로 26문항을 재실행했다.
프롬프트·모델·evidence mode·plan은 동결했고 target scheduling만 바뀌었다.

## 정본

- Call 2: `experiments/v2_call15_directscope_26_causal/call2_guard_sched_26_v2/`
- artifact sha256: `3d002f3b53388cef4771d53b3d1c563039ba433a6869c150d8cb6db6ff1982c6`
- manifest sha256: `cf05955e149f075fe9a9dc25bab36de2e25dea1daa1502b5105b0bc044fb27d4`
- audit sha256: `d56a5e588dc57a9081c98b665e5b64473786d2f4387ed3da23cc756427f8923a`
- plan sha256: `a025da3aa22764bef9ab6033a6afdd94568c8b61ee98c3c8d4f1cc855fbc4122`
- audit: 26 cases, errors 0, `SUCCEEDED`

## 결과

| | flat 동결 실행 | guard-aware v2 | 변화 |
| --- | ---: | ---: | ---: |
| assessment target | 531 | **452** | **-79 (-14.9%)** |
| physical request | 99 | **124** | +25 |
| prompt token | 171,758 | **181,040** | +9,282 |
| total token | 173,356 | **182,580** | **+5.3%** |
| UNKNOWN | 268 | **232** | -36 |

라운드는 19문항이 1회, 6문항이 3회였고 assessment target이 없는 1문항은 0회였다.
3라운드는 `commencement -> means/object defect -> dangerousness`처럼 앞 항이 UNKNOWN이어도
뒤 항의 FALSE가 연언 전체를 죽일 수 있는 경우다.

생략 상위 predicate는 `dangerousness` 21, `means_or_object_defect` 21,
`conspiracy_agreement` 8, `preparatory_conduct` 8,
`voluntary_cessation_or_prevention` 8이었다. `dangerousness`는 12건을 실제 평가했고
그중 UNKNOWN 11 / TRUE 1이었다. 즉 33건 전부를 기계적으로 없앤 것이 아니다.

## correctness 반사실

새 실행이 생략한 79개 자리에 flat 동결 실행의 truth를 다시 채운 진단 artifact를 만들고,
두 artifact를 동일한 현재 symbolic runtime으로 실행했다.

- scheduled:
  `scallop_guard_ab_sched_v2/results.jsonl`
- scheduled + 79 skipped old truths:
  `scallop_guard_ab_sched_v2_counterfactual_fill/results.jsonl`
- 비교: `case_truth_count`를 제외한 실행 상태·관계·doctrine·liability 결과 **26/26 완전 동일**
- 최종 truth에서 `skipped ∩ live = 0`, 다음 scheduling frontier도 0

따라서 79개는 이 실행의 최종 판단에 영향을 주지 않는 타깃이었다. 이는 “과거 truth가 우연히
같았다”가 아니라 생략값을 다시 공급해도 symbolic 결과가 변하지 않는다는 실행 검증이다.

## UNKNOWN 수치를 해석할 때의 주의

총 UNKNOWN은 268 -> 232로 36개 줄었지만 이를 모두 scheduler의 모델 품질 개선으로 쓰면 안
된다. 새로도 물은 공통 452개에서는 flat truth의 UNKNOWN 218개가 새 실행에서 232개가 되어
오히려 14개 늘었다. 같은 모델 재호출의 drift다. flat과 scheduled의 liability signature도
10문항 11 instance에서 바뀌었지만, 위 skipped-truth 반사실에서 차이가 0이므로 그 변화는
스케줄링이 아니라 공통 타깃 재평가값 변화에 귀속한다.

논문에서 방어 가능한 주장은 다음 둘이다.

1. guard-aware scheduling이 이번 run에서 non-influential target 79/531(14.9%)을 제거했다.
2. 제거값을 복원해도 symbolic liability output은 26/26 불변이었다.

토큰 비용은 줄지 않았다. occurrence별 프롬프트를 라운드마다 다시 보내 physical request가
늘었기 때문이다. 이 구현의 현재 가치는 비용 절감이 아니라 **죽은 completion branch의
UNKNOWN을 AnswerPlan의 법적 불확실성으로 올리지 않는 것**이다.

## 첫 실행 v1에서 잡은 결함

`call2_guard_sched_26_v1`은 진단 artifact로만 보존한다.

1. 앞 conjunct가 응답된 UNKNOWN이면 frontier가 그 자리에 고착되어 뒤 conjunct를 열지 않았다.
   그 결과 `dangerousness` 33건을 전부 생략했다. UNKNOWN은 TRUE가 아니지만 이미 평가된 값이므로,
   뒤 FALSE가 전체 연언을 확정할 기회를 주도록 scheduling frontier가 다음 항으로 진행해야 한다.
2. runner의 per-case 계측이 매 라운드 재할당되는 `shards`와 `request_targets`의 마지막 값만
   기록했다. 실제 append-only shard ledger에서 physical/neural count를 집계하도록 고쳤다.
3. auditor가 guard-aware subset을 허용하지 않고 plan 531개와 exact equality만 요구했다.
   planned/asked/skipped, 연속 라운드, planner subset, shard ledger와 aggregate를 함께 검증하도록
   계약을 확장했다.

회귀 테스트는 assessed UNKNOWN 뒤의 conjunct 진입과 다중 라운드 전체 요청 계측을 고정한다.
검증은 `330 passed, 16 skipped`, focused Ruff, `git diff --check` 통과다.

## 다음

UNKNOWN 3분할 중 죽은 가지 scheduling은 여기까지 완료다. 남은 것은 별개다.

1. 새 452-target truth 기준 residual UNKNOWN을 다시 진단한다.
2. occurrence 오배치와 실제 evidence-scope 부족을 분리한다.
3. 초literal 판정과 진짜 법적 논점을 분리한다.
4. 활성 프롬프트 문언 변경은 마지막이며 기존 승인 게이트를 유지한다.
