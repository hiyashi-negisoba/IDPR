"""Contract tests for the hand-authored doctrine tables (죄수, 미수·예비).

These are the only part of the rulebase written by hand rather than derived, so they are
the only part that can be wrong in a way no other check would notice. The load-time
validation exists because an entry naming an offence outside the corpus can never fire, and
a rule that can never fire looks exactly like a rule that is correct.
"""

from __future__ import annotations

import textwrap

import pytest

from idpr.rulebase.cards import load_card_corpus
from idpr.rulebase.doctrine import (
    CONCURRENCE_PATH,
    DOCTRINE_REVIEW_PATH,
    OFFENSE_NAMES,
    OPEN_DECISIONS,
    STAGE_PATH,
    DoctrineError,
    load_doctrine,
    offense_name,
    parse_decision_answers,
    unanswered_decisions,
)


@pytest.fixture(scope="module")
def articles():
    return set(load_card_corpus().by_article())


@pytest.fixture(scope="module")
def tables(articles):
    return load_doctrine(articles)


def test_the_checked_in_tables_load_and_validate(tables):
    assert tables.absorbed_by
    assert tables.imaginative_concurrence
    assert tables.attempt_punishable
    assert tables.preparation_punishable


def test_every_offence_named_is_in_the_corpus(tables, articles):
    named = (
        {child for child, _ in tables.absorbed_by}
        | {parent for _, parent in tables.absorbed_by}
        | {off for pair in tables.imaginative_concurrence for off in pair}
        | set(tables.attempt_punishable)
        | set(tables.preparation_punishable)
        | {off for off, _ in tables.not_punishable}
    )
    assert named <= articles


def test_the_tables_are_flagged_as_awaiting_review(tables):
    """They are drafts until a legal reviewer signs off; the flag must not be dropped
    silently when the file is edited."""
    assert tables.awaiting_review


def test_imaginative_concurrence_is_stored_symmetrically_once(tables):
    for first, second in tables.imaginative_concurrence:
        assert first < second, "pairs must be sorted so the rule need not be written twice"
        assert (second, first) not in tables.imaginative_concurrence


def test_a_negative_provision_is_recorded_rather_than_omitted(tables):
    """'위증 예비·음모 처벌규정이 없다' is a fact. Recording it keeps 'absent from the
    table' distinguishable from 'no such provision exists'."""
    assert ("art152", "preparation") in tables.not_punishable
    assert "art152" not in tables.preparation_punishable


def test_every_article_has_an_offence_name(articles):
    """The review document shows offence names, not article keys.

    A reviewer handed ``art356`` has to decode it, and decoding is where a legal review
    goes wrong. Missing names would degrade silently to the key.
    """
    assert articles <= set(OFFENSE_NAMES)
    for article in articles:
        assert offense_name(article) != article


def test_the_doctrine_review_document_leads_with_the_decisions():
    """The reviewer must see what to answer before any reference material.

    The drafted tables contain deliberate contradictions -- the distinctions that separate
    them (결과 발생 여부, 실행의 착수 여부) cannot be expressed by an article pair -- and
    presenting them as settled would hide a legal question inside a data file.
    """
    text = DOCTRINE_REVIEW_PATH.read_text(encoding="utf-8")
    assert text.index("# 결정 사항") < text.index("# 참고 자료")


def _write(tmp_path, concurrence: str, stage: str):
    c = tmp_path / "concurrence.yaml"
    s = tmp_path / "stage.yaml"
    c.write_text(textwrap.dedent(concurrence), encoding="utf-8")
    s.write_text(textwrap.dedent(stage), encoding="utf-8")
    return c, s


_EMPTY_STAGE = """\
    version: "t"
    attempt_punishable: []
"""


def test_an_offence_outside_the_corpus_is_an_error(tmp_path, articles):
    c, s = _write(
        tmp_path,
        """\
        version: "t"
        absorbed_by:
          - child: art999
            parent: art250
        """,
        _EMPTY_STAGE,
    )
    with pytest.raises(DoctrineError, match="art999 is not an article"):
        load_doctrine(articles, c, s)


def test_self_absorption_is_an_error(tmp_path, articles):
    c, s = _write(
        tmp_path,
        """\
        version: "t"
        absorbed_by:
          - child: art250
            parent: art250
        """,
        _EMPTY_STAGE,
    )
    with pytest.raises(DoctrineError, match="cannot absorb itself"):
        load_doctrine(articles, c, s)


def test_a_concurrence_entry_that_is_not_a_pair_is_an_error(tmp_path, articles):
    c, s = _write(
        tmp_path,
        """\
        version: "t"
        imaginative_concurrence:
          - offenses: [art250]
        """,
        _EMPTY_STAGE,
    )
    with pytest.raises(DoctrineError, match="must be a pair"):
        load_doctrine(articles, c, s)


def test_contradicting_stage_entries_are_an_error(tmp_path, articles):
    c, s = _write(
        tmp_path,
        'version: "t"\n',
        """\
        version: "t"
        attempt_punishable:
          - offense: art250
        not_punishable:
          - offense: art250
            stage: attempt
        """,
    )
    with pytest.raises(DoctrineError, match="both as attempt-punishable and not"):
        load_doctrine(articles, c, s)


def test_an_unknown_stage_name_is_an_error(tmp_path, articles):
    c, s = _write(
        tmp_path,
        'version: "t"\n',
        """\
        version: "t"
        not_punishable:
          - offense: art250
            stage: 미수
        """,
    )
    with pytest.raises(DoctrineError, match="stage must be"):
        load_doctrine(articles, c, s)


def test_all_errors_are_reported_together(tmp_path, articles):
    c, s = _write(
        tmp_path,
        """\
        version: "t"
        absorbed_by:
          - child: art998
            parent: art997
        """,
        _EMPTY_STAGE,
    )
    with pytest.raises(DoctrineError) as excinfo:
        load_doctrine(articles, c, s)
    assert len(excinfo.value.errors) == 2


def test_a_missing_table_is_an_error(tmp_path, articles):
    with pytest.raises(DoctrineError, match="missing doctrine table"):
        load_doctrine(articles, tmp_path / "nope.yaml", STAGE_PATH)


def test_the_tables_document_what_they_cannot_express():
    """The 죄수 doctrine that no article-pair table can hold.

    Recorded in the file itself so a reviewer asking "why is 포괄일죄 missing" finds the
    answer next to the entries rather than in a commit message.
    """
    text = CONCURRENCE_PATH.read_text(encoding="utf-8")
    for section in ("same_article", "multiplicity", "outside_corpus"):
        assert section in text


# --------------------------------------------------------------------------- #
# The open decisions must be answerable
# --------------------------------------------------------------------------- #


def test_every_decision_is_answerable_without_reading_the_code():
    """The first draft of the review document stated the problems and stopped there, so
    it could not be acted on. Each decision must carry the options, what each one does,
    a recommendation with its reason, and what happens if it is skipped."""
    for decision in OPEN_DECISIONS:
        assert decision.question.endswith("?"), decision.key
        assert len(decision.choices) >= 2, decision.key
        assert decision.why_it_cannot_be_derived.strip(), decision.key
        assert decision.default_if_unanswered.strip(), decision.key
        assert decision.recommendation_reason.strip(), decision.key
        labels = [choice.label for choice in decision.choices]
        assert any(
            label.startswith(f"{decision.recommended}.") for label in labels
        ), f"{decision.key}: recommended {decision.recommended} is not one of {labels}"
        for choice in decision.choices:
            assert choice.effect.strip(), f"{decision.key}/{choice.label}"


def test_the_review_document_has_an_answer_slot_for_every_decision():
    text = DOCTRINE_REVIEW_PATH.read_text(encoding="utf-8")
    for decision in OPEN_DECISIONS:
        assert f"## {decision.key}." in text, decision.key
    assert text.count("> answer:") >= len(OPEN_DECISIONS)


def test_answers_are_parsed_back_out_of_the_document(tmp_path):
    path = tmp_path / "doctrine_review.md"
    path.write_text(
        "## D1. 질문?\n> answer: 1\n\n"
        "## D2. 질문?\n> answer: 제122조는 빼고 나머지는 남겨\n\n"
        "## D3. 질문?\n> answer:  \n",
        encoding="utf-8",
    )
    answers = parse_decision_answers(path)
    assert answers == {"D1": "1", "D2": "제122조는 빼고 나머지는 남겨"}
    # A blank slot is not an answer: an unanswered decision must stay visibly unanswered.
    assert "D3" not in answers


def test_the_decisions_are_currently_unanswered():
    """Sanity check on the checked-in document: if this starts failing, the answers have
    arrived and the tables need updating."""
    assert unanswered_decisions(parse_decision_answers()) == tuple(
        d.key for d in OPEN_DECISIONS
    )
