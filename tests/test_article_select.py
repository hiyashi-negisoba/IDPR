"""Call 1.5 contracts: the catalog is closed, and the host mints the identifiers."""

from __future__ import annotations

import json

import pytest

from idpr.eval.input_formatter import assert_no_leaked_fields
from idpr.neural.article_select import (
    MAX_SELECTED,
    ArticleSelectError,
    article_select_schema,
    attempt_article_map,
    catalog_keys,
    catalog_lines,
    expand_attempt_articles,
    load_catalog,
    selection_payload,
    validate_selection,
)
from idpr.rulebase.cards import card_corpus
from idpr.rulebase.doctrine import OFFENSE_NAMES


def test_catalog_covers_every_article_the_corpus_carries():
    """An article missing from the catalog is one the pipeline can never select."""
    corpus_articles = {card.article for card in card_corpus().cards}
    assert corpus_articles <= set(catalog_keys())


def test_catalog_is_the_source_of_the_offence_names():
    """The names moved out of the code; both readers must see one table."""
    assert OFFENSE_NAMES == {e["key"]: e["offense"] for e in load_catalog()}


def test_catalog_line_leads_with_the_key_the_model_must_emit():
    line = catalog_lines()[0]
    key = catalog_keys()[0]
    assert line.startswith(f"{key} ")
    assert "제" in line


def test_schema_closes_the_article_set():
    """Guided decoding, not a post-hoc check, is what stops an invented article number."""
    schema = article_select_schema()
    enum = schema["properties"]["selected"]["items"]["properties"]["article"]["enum"]
    assert set(enum) == set(catalog_keys())
    assert schema["properties"]["selected"]["maxItems"] == MAX_SELECTED


def test_payload_carries_only_whitelisted_case_fields():
    payload = selection_payload(
        case_id="c1", question_text="甲은 …", question_prompt="죄책을 논하라."
    )
    assert_no_leaked_fields(payload)
    assert set(payload) == {"case_id", "case_text", "question_prompt", "article_catalog"}


def test_payload_never_carries_card_provenance():
    """Plan verification #4: only the reviewed proposition may reach a model.

    Here not even that -- selection sees article names, never card text -- so quotes and
    comment ids must be absent from the serialised request.
    """
    payload = selection_payload(
        case_id="c1", question_text="甲은 …", question_prompt="죄책을 논하라."
    )
    blob = json.dumps(payload, ensure_ascii=False)
    for forbidden in ("source_refs", "comment_id", "quote", "proposition"):
        assert forbidden not in blob


def test_selection_rejects_an_article_outside_the_catalog():
    with pytest.raises(ArticleSelectError):
        validate_selection({"selected": [{"article": "art999", "reason": "x"}]})


def test_selection_requires_a_reason():
    with pytest.raises(ArticleSelectError):
        validate_selection({"selected": [{"article": "art298", "reason": "  "}]})


def test_selection_keeps_the_first_reason_for_a_repeated_article():
    articles, entries = validate_selection(
        {
            "selected": [
                {"article": "art298", "reason": "첫 근거"},
                {"article": "art298", "reason": "둘째 근거"},
            ]
        }
    )
    assert articles == ("art298",)
    assert entries[0]["reason"] == "첫 근거"


def test_empty_selection_is_a_contract_violation():
    with pytest.raises(ArticleSelectError):
        validate_selection({"selected": []})


def test_attempt_expansion_follows_the_statute_reference():
    """제254조 punishes the attempt of 제250조; selecting the base pulls it in."""
    mapping = attempt_article_map()
    assert mapping["art250"] == "art254"
    assert mapping["art329"] == "art342"
    assert expand_attempt_articles(["art250"], mapping=mapping) == ("art250", "art254")


def test_attempt_expansion_preserves_order_and_is_idempotent():
    mapping = attempt_article_map()
    once = expand_attempt_articles(["art319", "art297"], mapping=mapping)
    assert once == ("art319", "art297", "art300")
    assert expand_attempt_articles(once, mapping=mapping) == once


def test_attempt_expansion_only_names_articles_the_corpus_covers():
    """An expansion target with no cards would add a candidate that carries nothing."""
    corpus_articles = {card.article for card in card_corpus().cards}
    assert set(attempt_article_map().values()) <= corpus_articles
