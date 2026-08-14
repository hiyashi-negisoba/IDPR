아래 INPUT_JSON의 `assessment_targets` 각각을 입력 순서대로 평가하라.
actor 행위는 `evidence_occurrence.source_text`와, 존재하는 경우 typed
`realization_context.same_actor_action_evidence`만 actor의 행위 증거로 사용한다.
`realization_context.context_evidence`는 객체·피해자·신분·관계·결과·상황의 이해에만 사용한다.
문항의 명시적 전역 사실은 `question_assumptions`만 추가로 사용할 수 있다. 이 carrier들에 없는
사실은 다른 문맥이나 추측으로 보충하지 말고 UNKNOWN으로 판단하라. 각 target에 대응하는 truth를
입력 순서대로 반환하라. 설명 없이 JSON 객체 하나만 출력하라.

<INPUT_JSON>
{{INPUT_JSON}}
</INPUT_JSON>
