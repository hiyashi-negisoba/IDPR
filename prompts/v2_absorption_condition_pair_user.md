아래 INPUT_JSON의 사건 서술을 읽고 `condition_statement`가 묻는 관계 하나만 답하라.

두 행위가 각각 죄가 되는지, 행위자에게 권한이 있었는지는 판단하지 말라. 그 관계가 원문에
나타나면 TRUE, 원문이 그 관계가 아님을 보여 주면 FALSE, 원문만으로 결정되지 않으면 UNKNOWN이다.

TRUE에는 반드시 보낸 문자열의 정확한 부분문자열 인용을 붙이라.
`retry_contract_feedback`가 있으면 판단을 바꾸지 말고 지적된 계약 오류만 고쳐 전체 JSON을
다시 제출하라.

<INPUT_JSON>
{{INPUT_JSON}}
</INPUT_JSON>
