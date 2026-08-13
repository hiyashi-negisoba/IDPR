아래 INPUT_JSON의 seed를 question_prompt 범위 안에서 full case_text의 factual episode에
결박하라. factual episode를 먼저 한 번만 정의하고 모든 explicit seed result가 이를 참조하게
하라. 모든 seed_index를 입력 순서대로 정확히 한 번 출력하며, 대응 episode가 없으면 빈
bindings 배열로 남긴다. 모든 quote는 factual_scope_text 안에서 고르고, actor 본인의 행위
quote와 함께 보아야 할 context quote를 구분하라.

같은 seed에 여러 binding, 같은 binding에 여러 quote가 가능하다. 최종적으로 부정될 수 있다는
이유로 사실적으로 대응 가능한 seed를 제거하지 말고, recall을 위해 모든 seed를 모든 actor에게
결박하지도 마라. 법적 결론·participation·dependency·DAG를 만들지 말고 JSON 객체 하나만
출력하라.

`retry_contract_feedback`가 있으면 이전 출력의 법적 내용을 확장하지 말고, 지적된 exact quote,
episode 범위, identity 계약 오류만 고쳐 전체 JSON을 다시 제출하라.

<INPUT_JSON>
{{INPUT_JSON}}
</INPUT_JSON>
