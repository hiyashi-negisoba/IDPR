# V2 restart — next session entry point

기준: 2026-08-11, commit 전 working tree checkpoint.

## 한 줄 상태

G0 rollback과 26문항 수동 GOLD occurrence, Call 1, occurrence-aware planner까지 완료했다.
Call 2의 predicate/relation/Article263 경계는 검증됐지만 participation의 전역 결정을
새 closed-option 계약으로 바꾼 직후이므로, **새 계약의 real-Gemma smoke부터 재개**한다.
이 checkpoint의 어떤 full Call 2 결과도 Scallop 입력으로 승인하지 않는다.

## 지금 고정된 파이프라인

```text
Case -> Call 1 routing -> Step 7
     -> manual GOLD factual occurrence
     -> occurrence-aware planner
     -> Call 2 predicate / relation / participation / Article263
     -> CaseTruths -> Scallop -> Call 3
```

- Call 수는 3회라는 논리 구조를 유지한다. Call 2 내부 physical shard 수는 별도다.
- GOLD에는 actor, factual occurrence, source span/text만 있다. 죄명·predicate truth·참여
  역할·기수·법률 결론은 없다.
- Call 2 predicate physical request는 정확히 한 occurrence만 본다.
- compact truth array는 입력 순서와 zip하며 length/order/missing/extra/unique key를
  hard-fail한다.
- confidence는 production Call 1/2에서 제거했다. 향후 self-consistency 실험용이다.

## 완료 및 검증 evidence

- `data/v2/gold_occurrences.jsonl`: 26문항, 67 occurrences.
- `data/v2/gold_article263_pairs.jsonl`: caller binding 1 pair.
- Call 1 실제 Gemma: 26/26 성공, Step 7 closure recall 74/86 (86.05%).
- Call 1 artifact: `experiments/v2_restart_rebuild/call1/router_output.jsonl`.
- 최신 planner artifact: `experiments/v2_restart_rebuild/evaluation_instance_plan.jsonl`.
- 최신 planner audit: 26/26, errors 0, collision 0.
- cardinality: top-level 815, assessment instance 849, predicate 5,182,
  relation 423, participation global target 719.
- 새 테스트 전면 재구축 결과: `84 passed, 6 skipped`.
- 이전 real-Gemma semantic gate는 6개가 통과했지만, participation wire contract가
  바뀌었으므로 participation gate는 다시 실행해야 한다.

## 왜 participation을 다시 바꿨는가

pair별로 co-principal/instigator/aider를 독립 판정한 full v3는 구조 audit 자체는
통과했지만 8개 사건에서 한 participant/offense가 여러 counterpart 또는 여러 mode를
동시에 선택했다. 이는 모델 반례를 더 붙여 해결할 문제가 아니라 caller contract가
상호배타성을 표현하지 못한 설계 결함이다.

현재 계약은 participant instance × offense마다 단 하나의 `option_id`를 고른다.
host가 `none`, `unknown`, source별 instigator/aider, source subset별 co-principal을
닫힌 enum으로 제공한다. 따라서 한 응답에서 co/derivative 충돌이나 복수 derivative
link는 구조적으로 만들 수 없다.

## 보존하되 승인하지 않는 실패 artifact

- `experiments/v2_restart_rebuild/call2_full`: 구형 독립 mode truth 방식. 의미 실패.
- `experiments/v2_restart_rebuild/call2_full_v3`: pair별 단일 decision 방식. structural
  audit은 성공했으나 global participation binding이 8개 사건에서 실패.
- 위 두 결과를 Scallop/Call 3 acceptance evidence로 사용하지 않는다.

## 다음 세션 실행 순서

1. `tests/live/test_gemma_call2_semantics.py`의 새 participation option gate를 job 221593에서
   실행한다. prompt에 사건별 반례를 추가하지 않는다.
2. 새 planner를 사용해 `call2_smoke_v4`를 실행하고 audit의 exact correspondence와
   participation option_id 유효성을 직접 본다.
3. smoke가 통과할 때만 `call2_full_v4`를 실행한다.
4. full artifact에서 duplicate participant target, derivative cycle, CaseTruth cardinality를
   hard-validate한다. 문제가 있으면 임의 tie-break하지 않는다.
5. 통과 후에만 Scallop을 실행하고 CaseTruths/Scallop 결과를 문항별 rubric과 대조한다.
6. 그 뒤 Call 3와 26-case 평가를 실행한다.

## 주의할 코드 경계

- 새 participation core: `src/idpr/v2/runtime/participation_grounding.py`.
- planner/runner/audit/Scallop parser는 새 `route_options` + `option_id` 형식으로 맞췄다.
- Scallop active doctrine universe는 top-level instances로 제한했다.
- derivative graph cycle은 아직 실제 full 결과로 검증하지 않았다.
- `src/idpr/neural/vllm_client.py`의 seed 전달은 live deterministic gate에 사용한다.
- 사용자가 명시적으로 요청해 기존 테스트 suite 전체를 삭제하고 새 suite만 남겼다.

## 다음 세션에 보낼 메시지

> `docs/handoff/NEXT_SESSION.md`부터 읽고 시작해. 새로운 설계나 반례 prompt를 더하지
> 말고, global closed-option participation 계약의 real-Gemma gate -> smoke v4 -> full v4
> 순서로 검증해. 이전 call2_full/call2_full_v3는 실패 분석용일 뿐 Scallop에 넣지 마.
> exact correspondence와 global binding이 통과한 뒤에만 Scallop, rubric 대조, Call 3로 가.
