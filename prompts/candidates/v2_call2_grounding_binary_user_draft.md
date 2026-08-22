아래 INPUT_JSON의 `assessment_targets` 각각을 입력 순서대로 평가하라.
actor 행위는 `evidence_occurrence.source_text`만 증거로 사용하고, 문항의 명시적 전역
사실은 `question_assumptions`만 추가로 사용할 수 있다. 두 carrier에서 확정할 수 없거나
언급되지 않은 사실은 FALSE를 선택하라. carrier가 그 사실의 불발생을 직접 보여 주면
FALSE다. 각 target에 대응하는 truth를 입력 순서대로 반환하라.
설명 없이 JSON 객체 하나만 출력하라.

<INPUT_JSON>
{{INPUT_JSON}}
</INPUT_JSON>
