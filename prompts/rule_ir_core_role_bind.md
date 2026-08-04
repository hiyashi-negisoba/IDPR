# 역할

고정된 죄종의 구성요건 판단에 필요한 entity·관계·legal role과 적용 track을 배정한다.

# 지시

- 죄종과 predicate 집합은 바꾸지 않는다.
- issue 주체를 현재 죄책 검토 대상인 `defendant_id`로 삼고, `role_contract`의 모든 필수 role을
  법적 의미에 따라 배정한다. 서로 다른 role이 같은 사람일 수도 있다.
- `role_definitions`와 `assignment_rules`를 적용하여 소유자·점유자·위탁자·처분자·피기망자 등을
  구별한다. 단순한 최초 등장이나 자금 출처만으로 role을 정하지 않는다.
- `track_contracts` 중 현재 주체의 실제 행위에 해당하는 track만 선택한다.
- entity와 relation은 뒤의 predicate 판단에 필요한 범위로 간결하게 작성한다. 근거 문구는 원문을
  그대로 쓰거나 의미를 보존하여 paraphrase할 수 있다.
- 아직 predicate 충족 여부나 유죄 결론을 쓰지 않는다.

JSON Schema를 만족하는 JSON 객체 하나만 출력한다.
