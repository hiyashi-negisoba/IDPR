아래 INPUT_JSON의 `assessment_targets` 각각을 입력 순서대로 평가하라.
`evidence_occurrence.source_text`만 증거로 사용하라. 거기에 없는 사실은 다른 문맥이나
추측으로 보충하지 말고 UNKNOWN으로 판단하라. 각 target에 대응하는 truth를 입력 순서대로 반환하라.
설명 없이 JSON 객체 하나만 출력하라.

<INPUT_JSON>
{{INPUT_JSON}}
</INPUT_JSON>
