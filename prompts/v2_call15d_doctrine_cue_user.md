아래 INPUT_JSON의 factual episode 하나만 읽고, `cues`의 각 사실 단서가 그 원문에 적혀 있는지
답하라.

법적 평가를 하지 말고, 적혀 있지 않으면 FALSE를 쓰라. UNKNOWN은 사실의 존재 자체나 그 사실이
누구에 관한 것인지가 원문상 결정되지 않을 때만 쓰고, 법적 의미가 불확실하다는 이유로는 쓰지
말라. 단서가 말하는 사실이 원문에 명시되어 있으면 TRUE다.

TRUE에는 반드시 episode_text의 정확한 부분문자열 인용을 붙이고, 주체는 각 cue의
`subject_instruction`이 지시하는 사람을 넣으라.
`retry_contract_feedback`가 있으면 의미를 확장하지 말고 지적된 cue 집합, exact quote, actor
표지 오류만 고쳐 전체 JSON을 다시 제출하라.

<INPUT_JSON>
{{INPUT_JSON}}
</INPUT_JSON>
