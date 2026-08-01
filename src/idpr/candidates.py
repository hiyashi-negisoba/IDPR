"""L0: the article candidates call 2 assesses, and the cards they carry.

One entry point, because the article decision now has three sources and downstream must not
have to know that. The model selects from the whole 51-article catalog (call 1.5), hybrid
retrieval contributes its shortlist, and the statute's attempt references expand
deterministically. Measured over 31 scorable questions:

    LLM 선정 단독              0.727   (4.5 articles,  8.1k call-2 tokens)
    검색 top-18 단독           0.877   (20.3 articles, 62.0k)
    합집합 top-18              0.927   (21.1 articles, 62.0k)

The union is what runs, and it is not a hedge: the two sources fail on different articles.
23 of the model's 34 misses sit inside retrieval's shortlist, because the model takes an
episode's dominant offence and lets its neighbours go -- 제297조 selected, 제298·301조 not --
while a card whose proposition names 강제추행 is exactly what retrieval scores. At top-18 the
union costs no more than retrieval alone: the model's picks are already inside it.

Two invariants hold here, both load-bearing rather than decorative:

* **Card-lossless inside a selected article.** Cutting happens at article granularity and
  nowhere else. The symbolic gate blocks only on cards it was given, so a card that is
  never assessed can never refute anything -- partial retrieval inside an article does not
  fail safe, it fails permissive.
* **Assessment excludes only what no rule can read.** ``context`` cards are 의의·개설·
  보호법익·연혁: true of every case, and no inference rule in the compiled rulebase reads
  their status. The exception is literal -- 13 of them carry ``exception`` polarity, which
  ``element_excluded`` *does* read -- so the filter is role *and* polarity, never role
  alone. Dropping those 13 would delete 조각사유 silently, which is the same failure mode
  the card-lossless invariant exists to prevent.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Sequence

from idpr.neural.article_select import expand_attempt_articles
from idpr.rulebase.cards import Card, CardCorpus, card_corpus
from idpr.rulebase.formalization import route_corpus
from idpr.rulebase.roles import resolve_card_roles
from idpr.rulebase.skeleton import CONTEXT

#: Polarity whose status is read regardless of role, by ``element_excluded``. A card with
#: it is never excluded from assessment.
EXCEPTION_POLARITY = "exception"


@dataclass(frozen=True)
class CandidateSet:
    """The articles in issue for one case, with the cards call 2 will assess.

    The three provenance fields are kept apart rather than merged into ``articles`` alone,
    because "which source found this article" is the measurement that decides whether both
    sources stay in the pipeline. Merging them would make that unanswerable after the fact.
    """

    articles: tuple[str, ...]
    from_model: tuple[str, ...]
    from_retrieval: tuple[str, ...]
    from_attempt_expansion: tuple[str, ...]
    cards: tuple[Card, ...]

    @property
    def card_ids(self) -> tuple[str, ...]:
        return tuple(card.id for card in self.cards)

    def model_payload(self) -> list[dict[str, str]]:
        """What call 2 receives: ``id`` and ``proposition``, nothing else."""
        return [card.model_payload() for card in self.cards]

    def as_dict(self) -> dict:
        return {
            "articles": list(self.articles),
            "from_model": list(self.from_model),
            "from_retrieval": list(self.from_retrieval),
            "from_attempt_expansion": list(self.from_attempt_expansion),
            "cards": len(self.cards),
        }


def assessable_card_ids(corpus: CardCorpus | None = None) -> frozenset[str]:
    """Card ids call 2 is asked for a status on.

    Starts from ``CardRouting.assessed_by_model`` -- the cards whose truth varies by case --
    and removes the ``context`` cards whose status no rule reads, keeping any that carry
    ``exception`` polarity.
    """
    corpus = corpus or card_corpus()
    assessed = {r.card_id for r in route_corpus(corpus) if r.assessed_by_model}
    roles = {r.card_id: r.role for r in resolve_card_roles(corpus)}
    return frozenset(
        card.id
        for card in corpus.cards
        if card.id in assessed
        and (roles.get(card.id) != CONTEXT or card.polarity == EXCEPTION_POLARITY)
    )


def candidate_articles(
    *,
    selected: Sequence[str] = (),
    retrieved: Sequence[str] = (),
    corpus: CardCorpus | None = None,
    assessable: Iterable[str] | None = None,
    attempt_map: Mapping[str, str] | None = None,
) -> CandidateSet:
    """Union the two article sources, expand attempt references, and gather the cards.

    Model selections lead the ordering: they carry a stated reason and are the higher-
    precision source, so a downstream step that has to truncate truncates the weaker tail.
    """
    corpus = corpus or card_corpus()
    assessable = frozenset(assessable) if assessable is not None else assessable_card_ids(corpus)

    from_model = tuple(dict.fromkeys(selected))
    union = tuple(dict.fromkeys((*from_model, *retrieved)))
    expanded = expand_attempt_articles(union, mapping=attempt_map)

    known = set(corpus.by_article())
    articles = tuple(article for article in expanded if article in known)
    cards = tuple(
        card for card in corpus.cards_for_articles(articles) if card.id in assessable
    )
    return CandidateSet(
        articles=articles,
        from_model=tuple(a for a in from_model if a in known),
        from_retrieval=tuple(a for a in retrieved if a in known and a not in set(from_model)),
        from_attempt_expansion=tuple(a for a in articles if a not in set(union)),
        cards=cards,
    )
