from __future__ import annotations

from idpr.v2.runtime.answer_plan import (
    ABSORBED,
    ESTABLISHED,
    NOT_ESTABLISHED,
    UNRESOLVED,
    AnchoredIssue,
    AnswerPlan,
    FinalResponsibility,
    ParticipationRoute,
    RequiredFinalConclusion,
    _required_final_conclusions,
    extract_final_conclusion_section,
    missing_required_final_conclusions,
    serialize_required_final_conclusions,
)


def _issue(
    issue_id: str,
    actor: str,
    offense_label: str,
    final_state: str,
    *,
    completion_state: str | None = None,
    participation: ParticipationRoute | None = None,
) -> AnchoredIssue:
    return AnchoredIssue(
        issue_id=issue_id,
        actor=actor,
        offense_label=offense_label,
        governing_provision=None,
        episode_quotes=(),
        final_state=final_state,
        completion_state=completion_state,
        completion_why=None,
        participation=participation,
        decisive_stage=None,
        satisfied=(),
        failed=(),
        blocking=(),
        doctrines=(),
        contested_points=(),
        gate_failed=final_state == NOT_ESTABLISHED,
    )


def _plan(issues: tuple[AnchoredIssue, ...]) -> AnswerPlan:
    return AnswerPlan(
        case_id="case",
        case_text="",
        question="",
        discussion_order=tuple(issue.issue_id for issue in issues),
        anchored_issues=issues,
        required_final_conclusions=_required_final_conclusions(issues),
        final_responsibility=FinalResponsibility((), (), (), (), ()),
    )


def test_one_anchor_per_issue_reuses_analysis_vocabulary() -> None:
    issues = (
        _issue("i1", "甲", "사기죄", NOT_ESTABLISHED),
        _issue("i2", "乙", "강간치상죄", UNRESOLVED),
        _issue(
            "i3",
            "丙",
            "절도죄",
            ESTABLISHED,
            completion_state="completed",
            participation=ParticipationRoute("instigator", None, None, None),
        ),
    )
    anchors = _required_final_conclusions(issues)
    assert anchors == (
        RequiredFinalConclusion("甲", "사기죄", "성립하지 않는다."),
        RequiredFinalConclusion("乙", "강간치상죄", "주어진 사실만으로는 성부를 확정하기 어렵다."),
        RequiredFinalConclusion("丙", "절도죄", "성립한다.", completion_state="기수", participation_mode="교사범"),
    )


def test_serialization_carries_no_internal_markers() -> None:
    issues = (_issue("i1", "甲", "횡령죄", ABSORBED),)
    payload = serialize_required_final_conclusions(_plan(issues))
    assert "甲" in payload and "횡령죄" in payload
    assert "ABSORBED" not in payload
    assert "UNKNOWN" not in payload


def test_missing_required_conclusions_flags_an_issue_dropped_from_the_closing_section() -> None:
    """The exact F4 shape: 乙 was discussed in the body but dropped from the closing summary."""
    issues = (
        _issue("i1", "丙", "횡령죄", ESTABLISHED),
        _issue("i2", "乙", "사기죄", NOT_ESTABLISHED),
    )
    plan = _plan(issues)
    answer_text = (
        "II. 각 행위자의 죄책\n"
        "乙의 사기죄는 기망행위가 인정되지 않아 성립하지 않는다.\n\n"
        "III. 최종 죄책\n"
        "丙의 최종 죄책은 횡령죄이다."
    )
    missing = missing_required_final_conclusions(answer_text, plan)
    assert [item.actor for item in missing] == ["乙"]


def test_whole_document_mention_outside_the_closing_section_does_not_count() -> None:
    """A body-only mention must not satisfy the closing-paragraph completeness check.

    This is the exact gap a whole-document presence check would miss: 乙 and 사기죄 both
    appear in the answer, just never in the section the closing-paragraph instruction is
    about.
    """
    issues = (_issue("i1", "乙", "사기죄", NOT_ESTABLISHED),)
    plan = _plan(issues)
    answer_text = (
        "II. 각 행위자의 죄책\n"
        "乙의 사기죄는 기망행위가 인정되지 않아 성립하지 않는다.\n\n"
        "III. 최종 죄책\n"
        "丙의 최종 죄책은 횡령죄이다."
    )
    assert extract_final_conclusion_section(answer_text).count("乙") == 0
    missing = missing_required_final_conclusions(answer_text, plan)
    assert [item.actor for item in missing] == ["乙"]


def test_no_missing_when_every_anchor_actor_and_offense_appear_in_the_closing_section() -> None:
    issues = (_issue("i1", "甲", "사기죄", NOT_ESTABLISHED),)
    plan = _plan(issues)
    answer_text = "I. 쟁점\n...\n\n최종 죄책\n甲의 사기죄는 성립하지 않는다."
    assert missing_required_final_conclusions(answer_text, plan) == ()


def test_closing_section_falls_back_to_last_paragraph_without_a_heading() -> None:
    answer_text = "첫 문단.\n\n둘째 문단.\n\n甲의 사기죄는 성립하지 않는다."
    assert extract_final_conclusion_section(answer_text) == "甲의 사기죄는 성립하지 않는다."
