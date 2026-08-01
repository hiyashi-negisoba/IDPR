"""L0 union contracts: card-lossless inside an article, and no silent gate weakening."""

from __future__ import annotations

import pytest

from idpr.candidates import (
    EXCEPTION_POLARITY,
    assessable_card_ids,
    candidate_articles,
    candidate_issues,
    split_candidate_batches,
)
from idpr.rulebase.cards import card_corpus
from idpr.rulebase.formalization import route_corpus
from idpr.rulebase.roles import resolve_card_roles
from idpr.rulebase.skeleton import CONTEXT


def test_every_card_of_a_selected_article_is_present():
    """The invariant. A card that is never assessed can never refute anything."""
    corpus = card_corpus()
    assessable = assessable_card_ids(corpus)
    result = candidate_articles(selected=["art298"], corpus=corpus, assessable=assessable)
    by_article = corpus.by_article()
    # Every selected article, expansion included -- 제298조 pulls in 제300조.
    expected = {
        card.id
        for article in result.articles
        for card in by_article[article]
        if card.id in assessable
    }
    assert "art300" in result.articles
    assert set(result.card_ids) == expected


def test_context_cards_are_excluded_from_assessment():
    """의의·개설·보호법익 are true of every case and no rule reads their status."""
    corpus = card_corpus()
    roles = {r.card_id: r.role for r in resolve_card_roles(corpus)}
    assessable = assessable_card_ids(corpus)
    dropped = [
        c for c in corpus.cards
        if roles.get(c.id) == CONTEXT and c.polarity != EXCEPTION_POLARITY
    ]
    assert dropped
    assert not any(c.id in assessable for c in dropped)


def test_exception_polarity_survives_the_context_exclusion():
    """``element_excluded`` reads polarity without consulting the role.

    Filtering on role alone would delete 조각사유 from the gate silently -- the exact
    failure the card-lossless invariant exists to prevent.
    """
    corpus = card_corpus()
    roles = {r.card_id: r.role for r in resolve_card_roles(corpus)}
    assessed = {r.card_id for r in route_corpus(corpus) if r.assessed_by_model}
    assessable = assessable_card_ids(corpus)
    kept = [
        c for c in corpus.cards
        if c.id in assessed
        and roles.get(c.id) == CONTEXT
        and c.polarity == EXCEPTION_POLARITY
    ]
    assert kept, "fixture assumption: some context cards carry exception polarity"
    assert all(c.id in assessable for c in kept)


def test_assessment_is_a_subset_of_what_routing_sends_to_the_model():
    corpus = card_corpus()
    assessed = {r.card_id for r in route_corpus(corpus) if r.assessed_by_model}
    assert assessable_card_ids(corpus) <= assessed


def test_union_records_which_source_found_each_article():
    result = candidate_articles(selected=["art297"], retrieved=["art298", "art297"])
    assert result.from_model == ("art297",)
    assert result.from_retrieval == ("art298",)
    assert "art300" in result.from_attempt_expansion


def test_model_selections_lead_the_ordering():
    result = candidate_articles(selected=["art319"], retrieved=["art250", "art319"])
    assert result.articles[0] == "art319"


def test_articles_outside_the_corpus_are_dropped_rather_than_carried():
    result = candidate_articles(selected=["art298", "art276"], retrieved=[])
    assert "art276" not in result.articles


def test_payload_is_id_and_proposition_only():
    result = candidate_articles(selected=["art300"])
    assert result.model_payload()
    for item in result.model_payload():
        assert set(item) == {"id", "proposition"}


def test_no_candidates_yields_no_cards():
    result = candidate_articles(selected=[], retrieved=[])
    assert result.articles == ()
    assert result.cards == ()


def test_issue_candidates_cover_every_selected_article_card_exactly_once():
    corpus = card_corpus()
    result = candidate_issues(
        selected=["art297", "art319"], retrieved=["art298"], corpus=corpus
    )
    member_ids = [
        card_id for issue in result.issues for card_id in issue.member_card_ids
    ]
    expected = {
        card.id for card in corpus.cards_for_articles(result.articles)
    }
    assert len(member_ids) == len(set(member_ids))
    assert set(member_ids) == expected
    assert result.initial_issues
    assert result.deferred_issues
    assert len(result.initial_issues) < len(result.issues)


def test_issue_candidates_keep_l0_provenance_and_attempt_expansion():
    result = candidate_issues(
        selected=["art297"], retrieved=["art298", "art297"]
    )
    assert result.from_model == ("art297",)
    assert result.from_retrieval == ("art298",)
    assert "art300" in result.from_attempt_expansion


def test_call2_split_keeps_every_article_and_card_whole():
    result = candidate_articles(
        selected=["art297", "art319"], retrieved=["art298", "art250"]
    )
    batches = split_candidate_batches(result, parts=2)
    assert len(batches) == 2
    assert {article for batch in batches for article in batch.articles} == set(
        result.articles
    )
    assert [card_id for batch in batches for card_id in batch.card_ids]
    assert {card_id for batch in batches for card_id in batch.card_ids} == set(
        result.card_ids
    )
    assert sum(len(batch.card_ids) for batch in batches) == len(result.card_ids)
    article_to_batch = {
        article: index
        for index, batch in enumerate(batches)
        for article in batch.articles
    }
    assert all(card.article in article_to_batch for batch in batches for card in batch.cards)


def test_call2_split_is_deterministic_and_payload_only():
    result = candidate_articles(selected=["art319"], retrieved=["art250", "art298"])
    first = split_candidate_batches(result)
    second = split_candidate_batches(result)
    assert first == second
    for batch in first:
        assert batch.payload_chars == sum(
            len(item["id"]) + len(item["proposition"])
            for item in batch.model_payload()
        )
        assert all(set(item) == {"id", "proposition"} for item in batch.model_payload())


def test_call2_split_rejects_an_invalid_part_count():
    result = candidate_articles(selected=["art319"])
    with pytest.raises(ValueError, match="at least 1"):
        split_candidate_batches(result, parts=0)
