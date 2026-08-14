# Call 2 residual UNKNOWN target-placement 감사

2026-08-14. `A_OR_CASE_CONTEXT_REVIEW` 50개와
`C_OR_D_PERSISTENT_REVIEW` 93개, 합계 143개를 기존 정본 plan과 Call 1.5 binding provenance만으로
다시 분해했다. 이 감사는 target을 이동하거나 truth를 바꾸지 않는다.

정본 packet:

- `diagnostics/residual_unknown_placement_audit_26_v1.{json,md}`
- `diagnostics/episode_scope_attribution_audit_44_v1.{json,md}`
- placement packet sha: `64326f8783f26481266ae008e2368b69ba3492f66f2eb29661a8ccd44a34b160`
- B attribution packet sha: `148c20b6c8263217402e8fe097cb9b87bf1033c6c17d29f218f473307391e902`
- 입력 plan sha: `a025da3aa22764bef9ab6033a6afdd94568c8b61ee98c3c8d4f1cc855fbc4122`
- 입력 Call 1.5 sha: `5d3ca5296cf04a9d0397be298ade5d0b1da5bac700cc066b8fce1130c88f1427`

## 143개에서 실제 placement 문제의 폭

| placement bucket | 수 | 의미 |
| --- | ---: | --- |
| legal-element realization scope | **113** | actor-action 한 조각이 아니라 offense realization 범위가 필요 |
| non-actor GroundFact realization scope | **5** | 결과·수단결함 등 actor 개인 행위가 아닌 factual predicate |
| direct binding content review | **14** | 현재 actor-action이 해당 GroundFact를 실제 담는지 검수 |
| participation role review | **6** | 같은 episode·offense의 여러 actor가 있으므로 개인 실행과 가담을 분리 |
| cross-episode same-actor carrier | **2** | 같은 actor의 다른 episode에 같은 conduct carrier 후보 존재 |
| derived source participation review | **2** | derived provenance는 있으나 source 자체가 다수 actor realization |
| derived exact-actor source | **1** | derived leaf의 exact actor source binding이 하나로 복원됨 |

즉 143개를 전부 occurrence 오배치로 보면 안 된다. **118개는 predicate 종류상 realization scope
문제이고, actor가 직접 수행한 행위에 붙는 GroundFact는 25개다.** 그 25개 안에서만 source
binding 이동·가담 분리를 논할 수 있다.

## 확인된 구조적 사례

- `RU-064`, `r11_p1_q1` 乙 robbery `taking_conduct`: 현재 강도 binding은 체포면탈 폭행
  episode이고, 같은 actor의 앞선 theft `binding:001`이 절취행위 carrier 후보로 유일하게 잡힌다.
  다만 cross-episode 후보라는 사실만으로 자동 복사하지 않고 realization link가 필요하다.
- `RU-130`, `RU-145`, `RU-179`: 丙의 망보기, 乙의 제안·정보제공, 乙의 길 묻기는 같은
  theft episode의 다른 actor 실행과 나란히 존재한다. principal의 `taking_conduct`를 이 actor의
  local GroundFact로 복사하면 안 된다.
- `RU-150`, `RU-169`: derived offense는 `source_binding_ids`로 base leaf carrier를 찾을 수 있다.
  그러나 source가 다수 actor theft realization이면 derived provenance만으로 개인 실행 여부까지
  확정할 수 없다.

이미 존재하는 Call 1.5-P/necessary-gate participation artifact도 같은 canonical plan sha를 사용한다.
`r13_p1_q1`에서는 theft 공동정범 route를 별도로 TRUE로 평가한다. 이것은 오히려 local
`taking_conduct`를 모두 TRUE로 만들 근거가 아니다. **개인 행위 GroundFact는 local evidence로
평가하고, 공동정범 귀속은 participation stage에서만 적용**해야 한다.

Call 1.5-P를 placement detector 하나로 쓰는 것도 불가능하다. `r13_p2_q1`의 distraction episode는
typed interaction이 0개라서 乙의 길 묻기 가담을 놓쳤다. 기존 interaction artifact는 유용한
보조 provenance지만 완전한 역할 oracle은 아니다.

## B 44개의 attribution 안전성

앞선 진단의 `B_EPISODE_SCOPE_CONFIRMED` 44개는 occurrence UNKNOWN이 episode/full에서 같은 known
값으로 풀렸다는 뜻이었다. 이번에는 같은 episode의 다른 actor binding도 같은 predicate를
소비하는지를 별도로 검사했다.

- 구조적 actor 충돌 없음: **32/44**
- 같은 predicate의 다른-actor carrier가 있어 검수 필요: **12/44**

따라서 B 44개라는 evidence 효과는 유지되지만, production에 factual episode를 채택할 때 44개
전부를 attribution-safe라고 부를 수는 없다. 12개에는 수뢰 actor/status, 목적, 주거침입, 절취행위
같이 다른 actor 사실을 빌릴 위험이 있다. `NO_STRUCTURAL_RISK`도 안전성의 충분조건이 아니라
현재 metadata에서 같은-predicate actor collision이 없다는 뜻이다.

## production contract가 가져야 할 형태

target별 evidence carrier를 한 종류로 통일하면 안 된다.

1. actor-bound GroundFact는 그 actor의 actual actor-action binding을 사용한다.
2. derived offense의 actor-bound GroundFact는 leaf를 공급하는 exact source binding으로 project한다.
3. legal element와 non-actor GroundFact는 offense realization/factual episode를 후보 scope로 쓴다.
4. principal의 실행행위는 participant local GroundFact에 복사하지 않는다. attribution은 검증된
   participation dependency가 symbolic stage에서만 수행한다.
5. robbery처럼 여러 episode에 걸친 realization은 같은 actor·같은 predicate라는 heuristic으로
   잇지 않고, upstream이 명시한 realization/source-binding link를 요구한다.

이 계약이면 full case 전면 확대를 피하면서도 B를 살릴 수 있다. 다음 구현은 먼저 target별
carrier를 **진단 arm**으로 만들고, 12개 collision queue와 cross-episode 2개를 따로 검수해야 한다.
그 결과를 보기 전에는 production Call 2 정본이나 N/P를 바꾸지 않는다.

검증은 `333 passed, 16 skipped`, focused Ruff, `git diff --check`를 통과했다.

## mixed-carrier paired 실행

위 contract를 production에 넣기 전에 같은 residual 232 target을 occurrence control과 mixed evidence로
paired 실행했다. 정본은 다음이다.

- `diagnostics/residual_unknown_mixed_evidence_paired_26_v3.json`
- `diagnostics/residual_unknown_mixed_evidence_review_26_v1.{json,md}`
- paired artifact sha: `72a11d65171b5e1c19a7f095f9afbdd7fd49b29ef1a8bb0d7c26d9f032f48e50`
- review sha: `f03aa7400842be2b4bfab1794cc11a69d8588a9d1b5ed381957934a7d9dd239d`
- 94 requests/arm, 244,700 tokens

v1은 mixed arm만 실행해 drift control이 없으므로 preflight다. v2는 두 arm의 target batching이 달라
evidence와 batching 효과가 섞였으므로 기각했다. **v3는 mixed carrier 종류대로 control도 같은 target
group으로 나눠, 두 arm 사이에 evidence text만 다르다.**

| carrier | target | paired transition |
| --- | ---: | --- |
| actor-action binding | 31 | U->U 29, T->T 2 |
| derived exact-actor source | 4 | U->U 4 |
| factual episode | 197 | U->U 121, U->T 46, U->F 5, T->T 19, F->F 1, known->U 4, F->T 1 |

전체 UNKNOWN은 control 205에서 mixed 158로 47개 줄었지만 이것을 성능 향상으로 채택하지 않는다.
같은 evidence와 같은 batching인 actor-action 31개가 전부 동일했다는 것은 local carrier의 안정성을
확인한다. 반면 episode arm에는 51개 U->known과 함께 4개 known->UNKNOWN, 1개 FALSE->TRUE가 있다.

known regression/reversal queue는 `RU-081`, `RU-093`, `RU-095`, `RU-113`, `RU-118`이다. 특히
`RU-081`은 사채업자 乙의 공무원성을 같은 episode의 군수 甲 사실과 함께 보자 FALSE에서 UNKNOWN으로
후퇴했다. 이는 episode 전면 채택 전에 막아야 할 actor attribution 혼선의 직접 반례다.

두 번의 독립 episode 실행에서 같은 known 값을 낸 target은 66개지만, 그중 14개는 same-predicate
다른-actor collision이 있다. 반복 안정성도 attribution 정확성의 충분조건이 아니다. 따라서 현재
결론은 다음과 같다.

1. actor-bound GroundFact의 local/source-binding carrier는 유지할 수 있다. 다만 이번 residual
   subset의 derived source 4개는 모두 UNKNOWN이라 회복 효과는 없었다.
2. factual episode는 정보 carrier로 유효하지만 predicate별 attribution gate 없이 production에
   전면 적용할 수 없다.
3. 다음 검수는 regression/reversal 5개와 B collision 12개를 먼저 닫고, 그 뒤 반복-stable known
   66개 중 안전한 subset만 candidate로 남긴다.
4. 아직 production Call 2, symbolic truth, N/P는 변경하지 않는다.
