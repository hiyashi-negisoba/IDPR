아래 INPUT_JSON의 `question_prompt`가 묻는 범위에 한정하여 `case_text`를 분석하고,
`offense_catalog`에서 검토할 가능성이 있는 Definition Layer offense seed를 순서대로 고르라.

관련 없는 후보를 개수 제한까지 채우지 말고 필요한 후보만 선택하라.
다른 필드나 설명을 출력하지 말고 JSON 객체 하나만 출력하라.

<INPUT_JSON>
{{INPUT_JSON}}
</INPUT_JSON>

다시 확인하라: `question_prompt`가 묻는 행위자 각각에 대해 그 범위의 서로 다른 행위와
결과를 모두 훑고, 최종적으로 부정·흡수될 수 있어도 독립 검토가 합리적인 offense 후보를
누락하지 마라. 같은 definition_id는 반복하지 말고 JSON seeds만 출력하라.

특히 금전 전달·중간자의 일부 사용·공무원의 수수 후 불입건이 함께 있는 유형은 catalog에
존재한다면 `offense.bribe_giving`, `offense.bribe_delivery_receipt`,
`offense.bribery_taking`, `offense.embezzlement`, `offense.dereliction_of_duty`,
`offense.harboring_or_escape`를 모두 독립 검토 후보로 포함한다.
수사 의무가 있는 공무원이 다른 범인을 의도적으로 입건하지 않은 행위는 부작위에 의한
`offense.harboring_or_escape` 검토 후보이므로 누락하지 않는다.
