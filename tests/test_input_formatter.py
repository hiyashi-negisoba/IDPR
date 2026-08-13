from idpr.eval.input_formatter import scoped_question_text, target_fact_source_spans


def test_scoped_question_text_applies_explicit_underlined_replacement() -> None:
    question_text = (
        "(1) 앞 사실. <u>기존 사실</u> 뒤 사실.\n\n"
        "(2) 다른 사실.\n\n"
        "(1)의 밑줄친 부분을 <u>'대체 사실'</u>로 바꿀 경우 논하시오."
    )
    prompt = "(1)의 밑줄친 부분을 <u>'대체 사실'</u>로 바꿀 경우 논하시오."

    scoped = scoped_question_text(question_text, prompt)

    assert "앞 사실. <u>대체 사실</u> 뒤 사실." in scoped
    assert "기존 사실" not in scoped
    assert "(2) 다른 사실" not in scoped
    assert "밑줄친 부분" not in scoped
    assert scoped.endswith("논하시오.")


def test_scoped_question_text_leaves_ordinary_scope_unchanged() -> None:
    question_text = (
        "(1) 첫 번째 사실.\n\n"
        "(2) 두 번째 사실.\n\n"
        "사실관계 (2)와 관련하여 논하시오."
    )
    prompt = "사실관계 (2)와 관련하여 논하시오."

    assert scoped_question_text(question_text, prompt) == "(2) 두 번째 사실.\n\n논하시오."


def test_scoped_question_text_uses_requested_actors_when_prompt_has_no_fact_label() -> None:
    question_text = (
        "(1) 甲과 乙의 첫 사실.\n"
        "(2) 丁과 戊의 둘째 사실.\n\n"
        "丁, 戊의 죄책을 논하시오."
    )
    prompt = "丁, 戊의 죄책을 논하시오."

    assert scoped_question_text(question_text, prompt) == (
        "(2) 丁과 戊의 둘째 사실.\n\n丁, 戊의 죄책을 논하시오."
    )


def test_scoped_question_text_turns_added_hypothesis_into_direct_text() -> None:
    question_text = (
        "(1) 甲의 사실.\n\n(2) 乙의 기존 사실.\n\n"
        "사실관계 (2)에서 乙은 추가 행동을 하였다. 이 경우 乙의 죄책은?"
    )
    prompt = "사실관계 (2)에서 乙은 추가 행동을 하였다. 이 경우 乙의 죄책은?"

    assert scoped_question_text(question_text, prompt) == (
        "(2) 乙의 기존 사실.\n\n乙은 추가 행동을 하였다. 이 경우 乙의 죄책은?"
    )


def test_scoped_question_text_includes_explicit_numbered_dependency() -> None:
    question_text = (
        "(1) 乙이 첫 범행을 하였다.\n"
        "(2) 乙은 위 (1) 사건으로 수사를 받았다.\n\n"
        "(2)에서 乙의 죄책은?"
    )

    scoped = scoped_question_text(question_text, "(2)에서 乙의 죄책은?")

    assert scoped.startswith("(1) 乙이 첫 범행을 하였다.\n\n(2)")


def test_scoped_question_text_includes_previous_fact_for_next_day_anaphora() -> None:
    question_text = (
        "(1) 乙이 첫 범행을 하였다.\n"
        "(2) 다음 날 乙은 위 범행의 결과를 알았다.\n\n"
        "(2)에서 乙의 죄책은?"
    )

    scoped = scoped_question_text(question_text, "(2)에서 乙의 죄책은?")

    assert scoped.startswith("(1) 乙이 첫 범행을 하였다.\n\n(2)")


def test_target_fact_spans_exclude_dependency_context() -> None:
    question_text = (
        "(1) 乙이 첫 범행을 하였다.\n\n"
        "(2) 다음 날 위 범행을 후회하였다.\n\n"
        "(2)에서 乙의 죄책은?"
    )
    spans = target_fact_source_spans(question_text, "(2)에서 乙의 죄책은?")
    assert spans is not None
    selected = [question_text[start:end].strip() for start, end in spans]
    assert selected == [
        "(2) 다음 날 위 범행을 후회하였다.",
        "(2)에서 乙의 죄책은?",
    ]
