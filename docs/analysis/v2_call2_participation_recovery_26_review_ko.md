# Call 2 participation universe 회수 및 mode resolution 검토

2026-08-14. target-placement 감사 뒤 확인된 participation universe 누락을 case truth patch 없이
구조적으로 보완했다. 넓은 LLM recovery는 unrelated actor/action을 끌어온 false positive 때문에
production에서 기각하고, literal coordination 표현과 authored derivation/participation policy만 사용했다.

## 적용한 변경

1. `X가 Y와 공모하여`, `X과 Y은 ... 하기로`처럼 행위자와 공모가 문언에 직접 나타나는 좁은
   deterministic interaction extractor를 사용한다.
2. 검증된 base-offense 공동정범 group에서, 동일 episode의 authored derived offense가
   `distinct_actor_binding_sets`를 요구하면 derived 공동정범 target을 연다.
3. TRUE 공동정범 group은 shared policy가 저작한
   `legal_element.joint_commission_by_two_or_more`를 symbolic TRUE로 투영한다.
4. 동일 participant-principal-offense-realization에 교사와 방조가 모두 TRUE이면 authored policy에
   따라 교사를 우선하고 방조를 최종 derivative link에서 흡수한다. 두 raw truth와 resolution은
   provenance/audit에 그대로 남긴다. policy가 없으면 기존처럼 hard fail한다.

## 26문항 실행 결과

정본 후보:

- plan: `participation_plan_v9_post_derived/evaluation_instance_plan.jsonl`
- plan sha: `962ca6b8a7327615c13a71486b1519cbe218925eafad7c2750e3f5632ab32796`
- raw Call 2: `participation_call2_v9_post_derived/participation_output.jsonl`
- policy 재컴파일: `participation_call2_v10_mode_subsumption/participation_output.jsonl`

실측:

- factual interactions: 34 -> 37
- participation local targets: 49 -> 60
- 60 truth: TRUE 26 / FALSE 30 / UNKNOWN 4
- physical 재호출 없이 26/26 compile 성공
- 과거 누락됐던 수뢰 공동정범과 특수절도 공동정범 target이 열리고 TRUE로 평가됨
- `r12_p2_q1_ga`의 ancestral homicide/homicide 두 logical edge에서 교사 우선 resolution 적용
- focused Ruff 통과, 전체 테스트 `360 passed, 16 skipped`

## 해석과 한계

이는 KCL 정답을 직접 주입한 변경이 아니다. 명시적 coordination이 universe에서 사라지는 결함,
base realization에서 authored derived realization으로 participation closure가 열리지 않는 결함,
검증된 관계가 이미 함의한 predicate를 다시 신경망에 묻는 결함을 각각 일반 규칙으로 수정했다.

반대로 임의의 사건 전문을 읽어 새로운 participant/offense를 제안하는 broad recovery는 채택하지
않았다. 남은 principal/offense 누락과 cross-offense compatibility는 별도 authored closure가 필요한지
downstream impact로 판단한다.
