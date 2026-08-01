"""The v2 catalog separates canonical elements from cases sharing their slot."""

from __future__ import annotations

from collections import Counter

from idpr.rulebase.card_catalog_v2 import (
    ALWAYS_ASSESS,
    CANONICAL_ELEMENT,
    PRECEDENT_PATTERN,
    PRECEDENT_RULE,
    RETRIEVE_ONLY,
    catalog_summary,
    compile_card_catalog_v2,
)
from idpr.rulebase.cards import card_corpus


def test_catalog_v2_covers_the_exact_original_corpus_once():
    corpus = card_corpus()
    compiled = compile_card_catalog_v2(corpus)
    assert len(compiled) == len(corpus.cards) == 1_848
    assert {card.card_id for card in compiled} == {card.id for card in corpus.cards}


def test_only_card_level_element_metadata_can_become_canonical():
    compiled = compile_card_catalog_v2()
    canonical = [card for card in compiled if card.function == CANONICAL_ELEMENT]
    assert canonical
    assert all(card.norm_kind == "element" for card in canonical)
    assert all(card.runtime == ALWAYS_ASSESS for card in canonical)


def test_precedent_patterns_are_not_loaded_as_mandatory_core_cards():
    corpus = card_corpus()
    compiled = compile_card_catalog_v2()
    by_id = {card.card_id: card for card in compiled}
    patterns = [card for card in compiled if card.form == PRECEDENT_PATTERN]
    assert patterns
    assert all(
        by_id[card.id].form in {PRECEDENT_RULE, PRECEDENT_PATTERN}
        for card in corpus.cards
        if card.doctrinal_status == "precedent_position"
    )
    assert all(card.runtime != ALWAYS_ASSESS for card in patterns)
    assert any(card.runtime == RETRIEVE_ONLY for card in patterns)


def test_focus_articles_no_longer_inherit_every_slot_card_as_core():
    compiled = compile_card_catalog_v2()
    focus = [
        card
        for card in compiled
        if card.article in {"art297", "art298", "art301", "art319"}
    ]
    functions = Counter(card.function for card in focus)
    assert len(focus) > functions[CANONICAL_ELEMENT]
    assert functions[CANONICAL_ELEMENT] > 0
    assert catalog_summary(compiled)["cards"] == 1_848
