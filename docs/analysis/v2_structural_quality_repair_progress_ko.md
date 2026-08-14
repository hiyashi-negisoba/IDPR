# KCL 답안 품질 구조 수리 진행 기록

2026-08-14. 이 트랙의 목적은 UNKNOWN 수치 자체가 아니라 KCL 답안이 빠뜨리거나 잘못 단정하게
만드는 upstream 구조 결함을 닫는 것이다. rubric은 사후 감사에만 쓰며 runtime 입력에는 넣지 않는다.

## 닫힌 결함: card evidence 입구

기존 560 `(instance, predicate)` target 중 card 검색이 가능한 것은 417개였다. 원인은 파생범죄의
조문 identity 49건과 derived/participation occurrence의 exact quote provenance 94건이 끊긴 것이었다.

- 파생범죄 정의에 이미 저작 근거가 있는 법명·조문 identity를 명시했다.
- derived occurrence는 planner의 `source_binding_ids`만 따라간다.
- participation occurrence는 planner가 저작한 exact `occurrences[].source_text`만 fallback으로 쓴다.
- full case나 다른 actor 사실을 추측해 채우지 않는다.

dry-run 결과는 **560/560 searchable, no-ground 0**이다. 전역 engineering representation gap 4개도
기본적으로 모든 답안에 복사하지 않게 했다. 이는 case-specific applicability가 입증될 때만 writer로
보내야 한다.

## 기각된 단일-pass binding recovery

완성 실행행위뿐 아니라 준비·미수·요청·도움을 보도록 한 candidate를 모든 UNBOUND_SEED 50개에
동일 적용했다. 21개 seed에서 30개 raw proposal이 나왔지만, 독립 semantic verifier를 통과한 것은
13개뿐이었다. 강도와 무관한 재산 처분을 강도 candidate로 잡는 등 broad-topic false positive가
확인되었고, 반대로 사문서 작성 부탁처럼 여러 fragment에 걸친 참여행위는 verifier가 탈락시켰다.

따라서 한 prompt가 direct offense conduct와 participation을 함께 binding하는 안은 production에서
기각한다. direct conduct/attempt와 offense-free factual interaction을 별도 typed producer로 유지하고,
후자가 principal realization에 구조적으로 join되게 해야 한다.

## 기각된 source-binding 전면 확대

residual UNKNOWN 232개에 같은 actor-aware prompt를 사용하여 occurrence control과 planner source
binding carrier를 paired 실행했다.

- control: TRUE 44 / FALSE 10 / UNKNOWN 178
- source binding: TRUE 52 / FALSE 12 / UNKNOWN 168
- 전이: U→T 10, U→F 3, T→U 3, **F→T 1**

UNKNOWN은 순감했지만 known regression과 직접 polarity reversal이 있어 전면 채택하지 않는다.
same-actor episode보다 좁혀도 predicate별 evidence role이 없으면 안전하지 않다는 실측이다.

## 남은 production 설계

1. direct conduct/attempt binding과 offense-free request/help/agreement interaction을 분리한다.
2. Call 2 evidence는 exact actor action, planner source, typed relation evidence, multi-actor realization을
   predicate별로 허용한다. episode/full-case 일괄 확대는 하지 않는다.
3. 명시 사실 포섭은 prompt 완화가 아니라 definition-level entailment example 또는 typed factual
   relation으로 검증한다. legal dispute는 이 경로에서 강제로 TRUE/FALSE로 만들지 않는다.
4. reviewed card의 `variant_group`과 채택 core card를 이용해 truth와 독립된 dispute registry를 만들고
   AnswerPlan `contested_points`에 연결한다.
5. final lineage가 확정된 뒤 Call 2부터 N/P와 blind judge까지 한 번만 재생성한다.
