아래 INPUT_JSON의 `routed_actor_ids`에 적힌 사람이 `factual_scope_text` 안에서 범했을
가능성이 있는 Definition Layer offense seed를 `offense_catalog`에서 순서대로 고르라.

이 호출에는 `question_prompt`가 없다. 질문이 죄책을 묻는 사람이 아니라, 다른 사람의 죄책을
판단하는 데 필요해서 조회되는 사람이다. 따라서 `routed_actor_ids`에 적힌 사람에게 귀속될 수
있는 행위·부작위·상태·결과만 본다. 그를 도운·숨겨준·도피시킨 다른 사람의 행위는 이 호출의
대상이 아니다.

`factual_scope_text` 밖의 사실은 쓰지 않는다. 범위가 좁으므로 후보도 대개 적다.
개수를 채우지 말고 그 범위에서 실제로 읽히는 후보만 고르라.
최종 성립 여부는 판단하지 않는다.

다른 필드나 설명을 출력하지 말고 JSON 객체 하나만 출력하라.

<INPUT_JSON>
{{INPUT_JSON}}
</INPUT_JSON>
