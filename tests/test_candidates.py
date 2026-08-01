"""L0 union contracts: card-lossless inside an article, and no silent gate weakening."""

from __future__ import annotations

from idpr.candidates import (
    EXCEPTION_POLARITY,
    assessable_card_ids,
    candidate_articles,
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
