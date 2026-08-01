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
from idpr.rulebase.issue_catalog_v2 import (
    ASSESS_ISSUE,
    IssuePacket,
    compile_issue_catalog_v2,
)
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


@dataclass(frozen=True)
class IssueCandidateSet:
    """Selected article scope represented as issues, not a flat card list.

    ``issues`` preserves the complete hierarchy for every selected article.  Only
    ``initial_issues`` are sent to the first assessment call; deferred packets keep
    guards, stage, concurrence, participation, and support material addressable without
    treating every source card as an independent constituent element.
    """

    articles: tuple[str, ...]
    from_model: tuple[str, ...]
    from_retrieval: tuple[str, ...]
    from_attempt_expansion: tuple[str, ...]
    issues: tuple[IssuePacket, ...]

    @property
    def issue_ids(self) -> tuple[str, ...]:
        return tuple(issue.issue_id for issue in self.issues)

    @property
    def initial_issues(self) -> tuple[IssuePacket, ...]:
        return tuple(issue for issue in self.issues if issue.runtime == ASSESS_ISSUE)

    @property
    def deferred_issues(self) -> tuple[IssuePacket, ...]:
        return tuple(issue for issue in self.issues if issue.runtime != ASSESS_ISSUE)

    def as_dict(self) -> dict:
        return {
            "articles": list(self.articles),
            "from_model": list(self.from_model),
            "from_retrieval": list(self.from_retrieval),
            "from_attempt_expansion": list(self.from_attempt_expansion),
            "issues": len(self.issues),
            "initial_issues": len(self.initial_issues),
            "deferred_issues": len(self.deferred_issues),
            "anchor_cards": sum(len(issue.anchor_card_ids) for issue in self.issues),
            "retrieval_cards": sum(
                len(issue.retrieval_card_ids) for issue in self.issues
            ),
        }


@dataclass(frozen=True)
class CandidateBatch:
    """One call-2 batch containing whole articles and all their assessable cards."""

    articles: tuple[str, ...]
    cards: tuple[Card, ...]
    payload_chars: int

    @property
    def card_ids(self) -> tuple[str, ...]:
        return tuple(card.id for card in self.cards)

    def model_payload(self) -> list[dict[str, str]]:
        return [card.model_payload() for card in self.cards]


def split_candidate_batches(
    candidates: CandidateSet, *, parts: int = 2
) -> tuple[CandidateBatch, ...]:
    """Balance call 2 by payload size without ever splitting an article's cards.

    The symbolic gate fails permissively when a refuting card is absent, so card-level
    truncation is forbidden. Articles are assigned, in candidate order, to the currently
    lightest batch; the weight is the exact character count of the two model-visible card
    fields and is independent of any legal label or offence-specific rule. Largest article
    payloads are assigned first, with original candidate order as the deterministic tie
    break and restored inside each finished batch.
    """
    if parts < 1:
        raise ValueError("parts must be at least 1")
    if not candidates.articles:
        return ()

    by_article: dict[str, list[Card]] = {article: [] for article in candidates.articles}
    for card in candidates.cards:
        by_article[card.article].append(card)
    bin_count = min(parts, len(candidates.articles))
    article_bins: list[list[str]] = [[] for _ in range(bin_count)]
    weights = [0] * bin_count
    order = {article: index for index, article in enumerate(candidates.articles)}
    article_weights = {
        article: sum(len(card.id) + len(card.proposition) for card in cards)
        for article, cards in by_article.items()
    }
    for article in sorted(
        candidates.articles, key=lambda item: (-article_weights[item], order[item])
    ):
        weight = article_weights[article]
        target = min(range(bin_count), key=lambda index: (weights[index], index))
        article_bins[target].append(article)
        weights[target] += weight

    batches: list[CandidateBatch] = []
    for articles, weight in zip(article_bins, weights):
        articles.sort(key=order.__getitem__)
        article_set = set(articles)
        cards = tuple(card for card in candidates.cards if card.article in article_set)
        batches.append(
            CandidateBatch(
                articles=tuple(articles),
                cards=cards,
                payload_chars=weight,
            )
        )
    return tuple(batches)


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


def candidate_issues(
    *,
    selected: Sequence[str] = (),
    retrieved: Sequence[str] = (),
    corpus: CardCorpus | None = None,
    attempt_map: Mapping[str, str] | None = None,
) -> IssueCandidateSet:
    """Apply the L0 article union while loading the issue hierarchy exactly once.

    This is the Phase-3 entry point.  L0 still decides article scope and attempt
    expansion, but selecting an article no longer expands it into hundreds of independent
    card questions.  Every source card remains reachable through exactly one returned
    issue packet as an anchor, retrieval candidate, symbolic condition, or support card.
    """
    corpus = corpus or card_corpus()
    from_model = tuple(dict.fromkeys(selected))
    union = tuple(dict.fromkeys((*from_model, *retrieved)))
    expanded = expand_attempt_articles(union, mapping=attempt_map)

    known = set(corpus.by_article())
    articles = tuple(article for article in expanded if article in known)
    article_order = {article: index for index, article in enumerate(articles)}
    all_issues, _ = compile_issue_catalog_v2(corpus)
    issues = tuple(
        sorted(
            (issue for issue in all_issues if issue.article in article_order),
            key=lambda issue: (
                article_order[issue.article],
                issue.section_path,
                issue.function,
                issue.issue_id,
            ),
        )
    )
    member_ids = [card_id for issue in issues for card_id in issue.member_card_ids]
    expected_ids = {
        card.id for card in corpus.cards_for_articles(articles)
    }
    if len(member_ids) != len(set(member_ids)) or set(member_ids) != expected_ids:
        raise ValueError("candidate issue hierarchy does not cover selected cards exactly once")

    return IssueCandidateSet(
        articles=articles,
        from_model=tuple(article for article in from_model if article in known),
        from_retrieval=tuple(
            article
            for article in retrieved
            if article in known and article not in set(from_model)
        ),
        from_attempt_expansion=tuple(
            article for article in articles if article not in set(union)
        ),
        issues=issues,
    )
