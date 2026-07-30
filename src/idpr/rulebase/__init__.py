"""Rulebase construction: live cards, element skeleton, authority index, SCL emission.

This package replaces the removed ``idpr.pipeline`` stack. Its organising principle is
that card ids are *data*, not schema: a card becomes tuples in a small fixed set of
relations rather than a relation of its own. Naming relations after cards is what
produced 3,487 ``rel rule_*`` declarations with only 8 distinct bodies.
"""

from __future__ import annotations

from idpr.rulebase.cards import (
    Card,
    CardCorpus,
    CardCorpusError,
    card_corpus,
    load_card_corpus,
    split_card_id,
)

__all__ = [
    "Card",
    "CardCorpus",
    "CardCorpusError",
    "card_corpus",
    "load_card_corpus",
    "split_card_id",
]
