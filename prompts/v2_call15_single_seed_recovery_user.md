아래 INPUT_JSON의 단일 seed에 factual binding이 있는지만 다시 확인하라. 출력 형식은 main
Call 1.5와 같다 — factual episode를 먼저 정의하고, 각 episode를 시간적으로 분리된 `actions`로
나눈 뒤, `seed_results`에 `seed_index: 0` 하나만 내고 그 binding이 action을 참조하게 하라.
대응할 사실이 없으면 빈 bindings 배열로 남긴다.

모든 quote는 factual_scope_text에서 정확히 복사한다. 수령·사후 소비·후속 전달처럼 다른 시점의
사실은 하나의 action이나 binding support에 섞지 마라. seed에 `requires_linked_offender` 표시가
없으면 `linked_offender`는 반드시 null이다.

INPUT_JSON:
{{INPUT_JSON}}
