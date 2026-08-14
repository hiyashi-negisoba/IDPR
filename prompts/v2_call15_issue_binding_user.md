아래 INPUT_JSON의 seed를 question_prompt 범위 안에서 full case_text의 factual episode에
결박하라. factual episode를 먼저 한 번만 정의하고, 각 episode를 시간적으로 분리된
`actions`로 나눈 뒤 모든 explicit seed result가 action을 참조하게 하라. 모든 seed_index를
입력 순서대로 정확히 한 번 출력하며, 대응 episode가 없으면 빈 bindings 배열로 남긴다.
모든 quote는 factual_scope_text 안에서 고른다. 수령·사후 소비·후속 전달처럼 다른 시점의
사실은 절대로 하나의 action이나 binding support에 섞지 마라.

같은 seed에 여러 binding이 가능하고, 하나의 교부 action은 교부자와 수령자가 모두 participant일
수 있다. 따라서 책임 actor는 focal action의 source actor와 달라도 된다. 최종적으로 부정될 수
있다는 이유로 사실적으로 대응 가능한 seed를 제거하지 말고, recall을 위해 모든 seed를 모든
actor에게 결박하지도 마라. 법적 결론·participation·dependency·DAG를 만들지 말고 JSON 객체
하나만 출력하라.

`verified_factual_candidate_hints`가 있으면 해당 exact quote를 놓치지 말되, 복합 quote를
그대로 action 하나로 복사하지 말고 시간상 action을 분리하라.

`retry_contract_feedback`가 있으면 이전 출력의 법적 내용을 확장하지 말고, 지적된 exact quote,
episode 범위, identity 계약 오류만 고쳐 전체 JSON을 다시 제출하라.

<INPUT_JSON>
{{INPUT_JSON}}
</INPUT_JSON>
