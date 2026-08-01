"""Issue-first retrieval for L0 scope and conditional detail lookup.

Retrieval decides scope, not law. The production L0 path may use every card as a search
signal, but it immediately projects each hit to its reviewed parent issue and then to its
article. Runtime assessment receives issues and anchor rules, never the flat hit cards.
When an issue remains unknown, detail retrieval is restricted to that same parent issue.

Three signals, and why
----------------------
``standard_rag``, one of the baselines, is BM25 alone. Beating it with BM25 alone would
say nothing, and the failure mode is known and lexical: the case says "가슴과 음부를 스스로
만지게 하였다" while the card says "피해자를 도구로 삼아 …추행행위를 한 경우". No term
overlaps. Dense retrieval closes that; BM25 holds the statutory vocabulary dense encoders
blur; the cross-encoder reorders a shortlist neither got right alone.

Multi-query, and why not one string
-----------------------------------
``question_text`` is a multi-episode narrative -- median 1,291 characters, and the smoke
case packs an indirect-principal indecent act, a residential intrusion with an abandoned
rape, a joint assault causing death, and bribery into three paragraphs. Encoding all of it
as one vector averages away the article that appears in one paragraph only. Call 1 already
decomposes the case by issue, so its ``retrieval_queries`` are the decomposition, and each
is ranked separately and fused. Fusion across queries takes the **max**, not the sum: a
card that ranks first for one episode must beat a card that ranks middling for all of
them, which is the same dilution one level up.

Fusion within a query is RRF (k=60) over the signal rankings. RRF has no weights to tune,
which matters here for a reason beyond convenience -- the scoring knobs must not be turned
while looking at the 61-question recall, or the number stops measuring retrieval and
starts measuring the fit.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping, Protocol, Sequence

from idpr.generation import _bm25_score, _search_terms
from idpr.rulebase.cards import Card, CardCorpus, card_corpus
from idpr.rulebase.issue_catalog_v2 import IssuePacket, compile_issue_catalog_v2

#: Reciprocal-rank-fusion constant. The standard value; not tuned.
RRF_K = 60

#: Articles expanded into issue scopes. The reviewed sweep still needs 18 for recall;
#: normalization reduces downstream issue payload rather than silently lowering this gate.
DEFAULT_TOP_K_ARTICLES = 18

#: Issue documents handed to the L0 ranker before collapsing them to unique articles.
#: This remains an evaluation default until the 61-question sweep selects the production
#: value; unlike DEFAULT_TOP_K_ARTICLES, it does not imply 18 resulting articles.
DEFAULT_TOP_K_ISSUES = 18

#: Cards per query carried into cross-encoder reranking. A reranker is a shortlist tool;
#: scoring all 1,848 cards per query is both wrong and slow.
DEFAULT_SHORTLIST_PER_QUERY = 100

#: The issue hierarchy keeps the candidate pool small.  Two details leave room
#: for competing standards without recreating the old all-cards prompt.
DEFAULT_TOP_K_CARDS_PER_ISSUE = 2

CACHE_ROOT = Path(__file__).resolve().parents[3] / "data" / "eval" / "cache"


class DenseEncoder(Protocol):
    """Sentence encoder. Injected so CPU tests run without loading a model."""

    name: str

    def encode(self, texts: Sequence[str], *, is_query: bool) -> list[list[float]]: ...


class Reranker(Protocol):
    """Cross-encoder. Scores ``(query, document)`` pairs jointly."""

    name: str

    def score(self, query: str, documents: Sequence[str]) -> list[float]: ...


@dataclass(frozen=True)
class RetrievalResult:
    """Candidate articles and the cards they carry.

    ``retrieved`` and ``proposed`` are kept apart deliberately. The union is what the
    pipeline runs on, but reporting only the union would hide whether retrieval or call 1
    found the article -- and if call 1 carries the recall, retrieval is not earning its
    place in the system.
    """

    articles: tuple[str, ...]
    retrieved: tuple[str, ...]
    proposed: tuple[str, ...]
    cards: tuple[Card, ...]
    article_scores: Mapping[str, float]

    @property
    def card_ids(self) -> tuple[str, ...]:
        return tuple(card.id for card in self.cards)

    def provenance(self) -> dict[str, str]:
        """Per article: ``retrieved`` / ``proposed`` / ``both``."""
        retrieved, proposed = set(self.retrieved), set(self.proposed)
        return {
            article: (
                "both"
                if article in retrieved and article in proposed
                else "retrieved"
                if article in retrieved
                else "proposed"
            )
            for article in self.articles
        }


@dataclass(frozen=True)
class IssueRetrievalResult:
    """L0 result ranked over normalized issue documents.

    retrieved_issue_ids is the actual ranking output. Articles are a deterministic
    projection used by L0 scope expansion; no detail or precedent card becomes an
    independent retrieval document.
    """

    articles: tuple[str, ...]
    retrieved_articles: tuple[str, ...]
    proposed: tuple[str, ...]
    retrieved_issue_ids: tuple[str, ...]
    issue_scores: Mapping[str, float]

    def provenance(self) -> dict[str, str]:
        retrieved, proposed = set(self.retrieved_articles), set(self.proposed)
        return {
            article: (
                "both"
                if article in retrieved and article in proposed
                else "retrieved"
                if article in retrieved
                else "proposed"
            )
            for article in self.articles
        }


@dataclass(frozen=True)
class RetrievedIssueCards:
    """Detailed standards selected underneath one already-active legal issue."""

    issue_id: str
    queries: tuple[str, ...]
    cards: tuple[Card, ...]
    card_scores: Mapping[str, float]

    @property
    def card_ids(self) -> tuple[str, ...]:
        return tuple(card.id for card in self.cards)

    def model_payload(self) -> list[dict[str, str]]:
        return [card.model_payload() for card in self.cards]


@dataclass(frozen=True)
class IssueCardRetrievalResult:
    """Per-issue retrieval result; cards never cross their reviewed parent issue."""

    results: tuple[RetrievedIssueCards, ...]

    @property
    def by_issue(self) -> Mapping[str, RetrievedIssueCards]:
        return {result.issue_id: result for result in self.results}

    @property
    def card_ids(self) -> tuple[str, ...]:
        return tuple(
            card_id for result in self.results for card_id in result.card_ids
        )


# --------------------------------------------------------------------------- #
# Lexical index
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class LexicalIndex:
    """Character-bigram BM25 over card propositions.

    Built once per corpus. ``_search_terms`` and ``_bm25_score`` are the fraud stack's,
    reused rather than rewritten: the character bigrams are what make this work on Korean
    without a tokeniser.
    """

    documents: tuple[tuple[str, ...], ...]
    document_frequency: Mapping[str, int]
    size: int

    @classmethod
    def build(cls, propositions: Sequence[str]) -> "LexicalIndex":
        documents = tuple(tuple(_search_terms(text)) for text in propositions)
        frequency: Counter[str] = Counter()
        for terms in documents:
            frequency.update(set(terms))
        return cls(documents=documents, document_frequency=frequency, size=len(documents))

    def scores(self, query: str) -> list[float]:
        query_terms = _search_terms(query)
        return [
            _bm25_score(
                query_terms=query_terms,
                document_terms=terms,
                document_frequency=self.document_frequency,
                corpus_size=self.size,
            )
            for terms in self.documents
        ]


# --------------------------------------------------------------------------- #
# Dense index
# --------------------------------------------------------------------------- #


def corpus_fingerprint(propositions: Sequence[str]) -> str:
    digest = hashlib.sha256()
    for text in propositions:
        digest.update(text.encode("utf-8"))
        digest.update(b"\x00")
    return digest.hexdigest()[:16]


class DenseIndex:
    """Card embeddings, computed once and cached on disk.

    The cache is keyed by encoder name and corpus fingerprint, so a card edit or a model
    swap invalidates it without anyone remembering to clear anything.
    """

    def __init__(self, vectors: Sequence[Sequence[float]]) -> None:
        self._vectors = [_normalise(vector) for vector in vectors]

    @classmethod
    def build(
        cls,
        propositions: Sequence[str],
        encoder: DenseEncoder,
        *,
        cache_root: Path | None = None,
    ) -> "DenseIndex":
        cache_root = cache_root or CACHE_ROOT
        fingerprint = corpus_fingerprint(propositions)
        path = cache_root / f"cards_{encoder.name}_{fingerprint}.json"
        if path.is_file():
            return cls(json.loads(path.read_text()))
        vectors = encoder.encode(list(propositions), is_query=False)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps([list(map(float, v)) for v in vectors]))
        return cls(vectors)

    def scores(self, query_vector: Sequence[float]) -> list[float]:
        query = _normalise(query_vector)
        return [sum(a * b for a, b in zip(query, vector)) for vector in self._vectors]


def _normalise(vector: Sequence[float]) -> list[float]:
    norm = math.sqrt(sum(value * value for value in vector)) or 1.0
    return [value / norm for value in vector]


# --------------------------------------------------------------------------- #
# Fusion
# --------------------------------------------------------------------------- #


def _ranking(scores: Sequence[float]) -> list[int]:
    """Document indices, best first. Ties break by index so runs are reproducible."""
    return sorted(range(len(scores)), key=lambda index: (-scores[index], index))


def reciprocal_rank_fusion(rankings: Sequence[Sequence[int]], *, k: int = RRF_K) -> dict[int, float]:
    """Fuse rankings. A document absent from a ranking simply scores nothing from it."""
    fused: dict[int, float] = {}
    for ranking in rankings:
        for position, index in enumerate(ranking):
            fused[index] = fused.get(index, 0.0) + 1.0 / (k + position + 1)
    return fused


def issue_index_documents(
    issues: Sequence[IssuePacket] | None = None,
    *,
    corpus: CardCorpus | None = None,
) -> tuple[tuple[IssuePacket, ...], tuple[str, ...]]:
    """Return one compact L0 document per issue that has reviewed anchor context."""
    corpus = corpus or card_corpus()
    if issues is None:
        issues = compile_issue_catalog_v2(corpus)[0]
    indexed = tuple(issue for issue in issues if issue.anchor_card_ids)
    texts = tuple(
        " ".join(
            (
                issue.article_label,
                issue.offense,
                issue.title,
                *(corpus.by_id[card_id].proposition for card_id in issue.anchor_card_ids),
            )
        )
        for issue in indexed
    )
    return indexed, texts


# --------------------------------------------------------------------------- #
# Retrieval
# --------------------------------------------------------------------------- #


def retrieve_candidate_issues(
    queries: Sequence[str],
    *,
    corpus: CardCorpus | None = None,
    issues: Sequence[IssuePacket] | None = None,
    proposed: Iterable[str] = (),
    top_k_issues: int = DEFAULT_TOP_K_ISSUES,
    encoder: DenseEncoder | None = None,
    reranker: Reranker | None = None,
    lexical: LexicalIndex | None = None,
    dense: DenseIndex | None = None,
    shortlist_per_query: int = DEFAULT_SHORTLIST_PER_QUERY,
) -> IssueRetrievalResult:
    """Rank normalized legal issues and project the hits to candidate articles."""
    if top_k_issues < 1:
        raise ValueError("top_k_issues must be at least 1")
    if shortlist_per_query < 1:
        raise ValueError("shortlist_per_query must be at least 1")
    corpus = corpus or card_corpus()
    indexed, documents = issue_index_documents(issues, corpus=corpus)
    lexical = lexical or LexicalIndex.build(documents)
    if dense is None and encoder is not None:
        dense = DenseIndex.build(documents, encoder)

    best_scores: dict[int, float] = {}
    for query in queries:
        rankings = [_ranking(lexical.scores(query))]
        if dense is not None and encoder is not None:
            query_vector = encoder.encode([query], is_query=True)[0]
            rankings.append(_ranking(dense.scores(query_vector)))
        fused = reciprocal_rank_fusion(rankings)
        shortlist = sorted(fused, key=lambda index: (-fused[index], index))[
            :shortlist_per_query
        ]
        if reranker is not None and shortlist:
            reranked = reranker.score(
                query, [documents[index] for index in shortlist]
            )
            query_scores = dict(zip(shortlist, reranked))
        else:
            query_scores = {index: fused[index] for index in shortlist}
        for index, score in query_scores.items():
            if score > best_scores.get(index, float("-inf")):
                best_scores[index] = score

    ranked = sorted(
        best_scores,
        key=lambda index: (-best_scores[index], indexed[index].issue_id),
    )
    selected = ranked[:top_k_issues]
    retrieved_issue_ids = tuple(indexed[index].issue_id for index in selected)
    retrieved_articles = tuple(
        dict.fromkeys(indexed[index].article for index in selected)
    )
    proposed_articles = tuple(dict.fromkeys(proposed))
    articles = tuple(dict.fromkeys((*retrieved_articles, *proposed_articles)))
    return IssueRetrievalResult(
        articles=articles,
        retrieved_articles=retrieved_articles,
        proposed=proposed_articles,
        retrieved_issue_ids=retrieved_issue_ids,
        issue_scores={
            indexed[index].issue_id: best_scores[index] for index in ranked
        },
    )


def retrieve_candidate_issues_from_cards(
    queries: Sequence[str],
    *,
    corpus: CardCorpus | None = None,
    issues: Sequence[IssuePacket] | None = None,
    proposed: Iterable[str] = (),
    top_k_issues: int = DEFAULT_TOP_K_ISSUES,
    encoder: DenseEncoder | None = None,
    reranker: Reranker | None = None,
    lexical: LexicalIndex | None = None,
    dense: DenseIndex | None = None,
    shortlist_per_query: int = DEFAULT_SHORTLIST_PER_QUERY,
) -> IssueRetrievalResult:
    """Use every card as a search signal, then collapse hits to parent issues.

    Member cards are never returned as runtime payload. They only contribute a score to
    their reviewed parent issue, preserving case-pattern vocabulary without recreating
    flat-card assessment.
    """
    if top_k_issues < 1:
        raise ValueError("top_k_issues must be at least 1")
    if shortlist_per_query < 1:
        raise ValueError("shortlist_per_query must be at least 1")
    corpus = corpus or card_corpus()
    if issues is None:
        issues, placements = compile_issue_catalog_v2(corpus)
    else:
        all_issues, all_placements = compile_issue_catalog_v2(corpus)
        wanted = {issue.issue_id for issue in issues}
        placements = tuple(
            placement
            for placement in all_placements
            if placement.issue_id in wanted
        )
    issues = tuple(issues)
    issue_by_id = {issue.issue_id: issue for issue in issues}
    issue_by_card = {
        placement.card_id: placement.issue_id for placement in placements
    }
    cards = tuple(
        card for card in corpus.cards if card.id in issue_by_card
    )
    documents = tuple(card.proposition for card in cards)
    lexical = lexical or LexicalIndex.build(documents)
    if dense is None and encoder is not None:
        dense = DenseIndex.build(documents, encoder)

    best_card_scores: dict[int, float] = {}
    for query in queries:
        rankings = [_ranking(lexical.scores(query))]
        if dense is not None and encoder is not None:
            query_vector = encoder.encode([query], is_query=True)[0]
            rankings.append(_ranking(dense.scores(query_vector)))
        fused = reciprocal_rank_fusion(rankings)
        shortlist = sorted(fused, key=lambda index: (-fused[index], index))[
            :shortlist_per_query
        ]
        if reranker is not None and shortlist:
            reranked = reranker.score(
                query, [documents[index] for index in shortlist]
            )
            query_scores = dict(zip(shortlist, reranked))
        else:
            query_scores = {index: fused[index] for index in shortlist}
        for index, score in query_scores.items():
            if score > best_card_scores.get(index, float("-inf")):
                best_card_scores[index] = score

    best_issue_scores: dict[str, float] = {}
    for index, score in best_card_scores.items():
        issue_id = issue_by_card[cards[index].id]
        if score > best_issue_scores.get(issue_id, float("-inf")):
            best_issue_scores[issue_id] = score
    ranked_issue_ids = sorted(
        best_issue_scores,
        key=lambda issue_id: (-best_issue_scores[issue_id], issue_id),
    )
    retrieved_issue_ids = tuple(ranked_issue_ids[:top_k_issues])
    retrieved_articles = tuple(
        dict.fromkeys(issue_by_id[issue_id].article for issue_id in retrieved_issue_ids)
    )
    proposed_articles = tuple(dict.fromkeys(proposed))
    articles = tuple(dict.fromkeys((*retrieved_articles, *proposed_articles)))
    return IssueRetrievalResult(
        articles=articles,
        retrieved_articles=retrieved_articles,
        proposed=proposed_articles,
        retrieved_issue_ids=retrieved_issue_ids,
        issue_scores={
            issue_id: best_issue_scores[issue_id] for issue_id in ranked_issue_ids
        },
    )


def retrieve_candidate_articles_via_issues(
    queries: Sequence[str],
    *,
    corpus: CardCorpus | None = None,
    issues: Sequence[IssuePacket] | None = None,
    proposed: Iterable[str] = (),
    top_k_articles: int = DEFAULT_TOP_K_ARTICLES,
    encoder: DenseEncoder | None = None,
    reranker: Reranker | None = None,
    lexical: LexicalIndex | None = None,
    dense: DenseIndex | None = None,
    shortlist_per_query: int = DEFAULT_SHORTLIST_PER_QUERY,
) -> IssueRetrievalResult:
    """Preserve article recall through the explicit card→issue→article hierarchy."""
    if top_k_articles < 1:
        raise ValueError("top_k_articles must be at least 1")
    corpus = corpus or card_corpus()
    issues = tuple(issues) if issues is not None else compile_issue_catalog_v2(corpus)[0]
    issue_by_id = {issue.issue_id: issue for issue in issues}
    projected = retrieve_candidate_issues_from_cards(
        queries,
        corpus=corpus,
        issues=issues,
        top_k_issues=len(issues),
        encoder=encoder,
        reranker=reranker,
        lexical=lexical,
        dense=dense,
        shortlist_per_query=shortlist_per_query,
    )
    article_scores: dict[str, float] = {}
    top_issue_by_article: dict[str, str] = {}
    for issue_id, score in projected.issue_scores.items():
        article = issue_by_id[issue_id].article
        if score > article_scores.get(article, float("-inf")):
            article_scores[article] = score
            top_issue_by_article[article] = issue_id
    ranked_articles = sorted(
        article_scores,
        key=lambda article: (-article_scores[article], article),
    )
    retrieved_articles = tuple(ranked_articles[:top_k_articles])
    proposed_articles = tuple(dict.fromkeys(proposed))
    articles = tuple(dict.fromkeys((*retrieved_articles, *proposed_articles)))
    return IssueRetrievalResult(
        articles=articles,
        retrieved_articles=retrieved_articles,
        proposed=proposed_articles,
        retrieved_issue_ids=tuple(
            top_issue_by_article[article] for article in retrieved_articles
        ),
        issue_scores=projected.issue_scores,
    )


def retrieve_candidate_articles(
    queries: Sequence[str],
    *,
    corpus: CardCorpus | None = None,
    proposed: Iterable[str] = (),
    top_k_articles: int = DEFAULT_TOP_K_ARTICLES,
    encoder: DenseEncoder | None = None,
    reranker: Reranker | None = None,
    lexical: LexicalIndex | None = None,
    dense: DenseIndex | None = None,
    shortlist_per_query: int = DEFAULT_SHORTLIST_PER_QUERY,
) -> RetrievalResult:
    """Rank articles for one case and return them with all of their cards.

    ``queries`` are ranked independently and fused by max; ``proposed`` (call 1's issue
    candidates) is unioned in afterwards without competing for a rank, since a proposal is
    a claim that the article is in issue, not a similarity score.
    """
    corpus = corpus or card_corpus()
    cards = tuple(corpus.by_id.values())
    propositions = [card.proposition for card in cards]
    lexical = lexical or LexicalIndex.build(propositions)
    if dense is None and encoder is not None:
        dense = DenseIndex.build(propositions, encoder)

    card_scores = [0.0] * len(cards)
    for query in queries:
        rankings = [_ranking(lexical.scores(query))]
        if dense is not None and encoder is not None:
            query_vector = encoder.encode([query], is_query=True)[0]
            rankings.append(_ranking(dense.scores(query_vector)))
        fused = reciprocal_rank_fusion(rankings)
        shortlist = sorted(fused, key=lambda index: (-fused[index], index))[
            :shortlist_per_query
        ]

        if reranker is not None and shortlist:
            reranked = reranker.score(query, [propositions[index] for index in shortlist])
            query_scores = dict(zip(shortlist, reranked))
        else:
            query_scores = {index: fused[index] for index in shortlist}

        for index, score in query_scores.items():
            # Max, not sum: one episode's best card must not lose to a card that is
            # mediocre for every episode.
            if score > card_scores[index]:
                card_scores[index] = score

    article_scores: dict[str, float] = {}
    for card, score in zip(cards, card_scores):
        if score > article_scores.get(card.article, float("-inf")):
            article_scores[card.article] = score

    ranked = sorted(article_scores, key=lambda a: (-article_scores[a], a))
    retrieved = tuple(ranked[:top_k_articles])
    proposed_articles = tuple(dict.fromkeys(proposed))
    articles = tuple(dict.fromkeys((*retrieved, *proposed_articles)))

    return RetrievalResult(
        articles=articles,
        retrieved=retrieved,
        proposed=proposed_articles,
        # The invariant: every card of every selected article, no exceptions.
        cards=corpus.cards_for_articles(articles),
        article_scores={article: article_scores[article] for article in ranked},
    )


def _flatten_fact_value(value: object) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, Mapping):
        return [
            text
            for key, item in value.items()
            if key not in {"fact_id", "epistemic_status"}
            for text in _flatten_fact_value(item)
        ]
    if isinstance(value, Sequence) and not isinstance(value, (str, bytes)):
        return [text for item in value for text in _flatten_fact_value(item)]
    return []


def issue_retrieval_queries(
    issue: IssuePacket,
    facts: Sequence[Mapping[str, object]],
    *,
    focus_texts: Sequence[str] = (),
    max_fact_queries: int = 32,
) -> tuple[str, ...]:
    """Build independent, issue-scoped queries without averaging case episodes.

    Each fact stays a separate query and is prefixed by the parent issue.  Max fusion can
    therefore let one highly relevant episode win, while restricting the candidate ids to
    the issue prevents a residential-entry fact from pulling in an unrelated offence.
    ``focus_texts`` normally carries the first pass's concrete missing-fact descriptions.
    """
    if max_fact_queries < 1:
        raise ValueError("max_fact_queries must be at least 1")
    prefix = f"{issue.offense} {issue.title}"
    focus = [str(text).strip() for text in focus_texts if str(text).strip()]
    fact_texts: list[str] = []
    for fact in facts:
        assertion = fact.get("assertion", fact)
        if not isinstance(assertion, Mapping):
            continue
        values = _flatten_fact_value(assertion)
        source_quote = assertion.get("source_quote")
        ordered = ([str(source_quote)] if source_quote else []) + values
        text = " ".join(dict.fromkeys(item.strip() for item in ordered if item.strip()))
        if text:
            fact_texts.append(text)
    fact_texts = list(dict.fromkeys(fact_texts))
    if focus:
        signature = set(_search_terms(f"{prefix} {' '.join(focus)}"))
        ranked_facts = sorted(
            fact_texts,
            key=lambda text: (
                -len(signature & set(_search_terms(text))),
                fact_texts.index(text),
            ),
        )
        # The first-pass omission description is the strongest query.  A few closest
        # admitted facts add case vocabulary without letting unrelated episodes win max
        # fusion merely because the case is long.
        related_facts = [
            text
            for text in ranked_facts
            if signature & set(_search_terms(text))
        ][:4]
        texts = [" ".join((*focus, *related_facts))]
    else:
        texts = fact_texts
    texts = list(dict.fromkeys(texts))[:max_fact_queries]
    if not texts:
        return (prefix,)
    return tuple(f"{prefix} {text}" for text in texts)


def retrieve_issue_cards(
    issues: Sequence[IssuePacket],
    facts: Sequence[Mapping[str, object]],
    *,
    focus_by_issue: Mapping[str, Sequence[str]] | None = None,
    corpus: CardCorpus | None = None,
    top_k_per_issue: int = DEFAULT_TOP_K_CARDS_PER_ISSUE,
    encoder: DenseEncoder | None = None,
    reranker: Reranker | None = None,
    lexical: LexicalIndex | None = None,
    dense: DenseIndex | None = None,
    shortlist_per_query: int = DEFAULT_SHORTLIST_PER_QUERY,
) -> IssueCardRetrievalResult:
    """Retrieve detailed cards only under their reviewed parent issues.

    This is deliberately separate from L0 article retrieval.  L0 remains article-lossless;
    after an issue is active, this function narrows only that issue's subordinate standards
    and case patterns.  Anchor rules are structurally ineligible and can never be returned.
    """
    if top_k_per_issue < 1:
        raise ValueError("top_k_per_issue must be at least 1")
    if shortlist_per_query < 1:
        raise ValueError("shortlist_per_query must be at least 1")
    issue_ids = [issue.issue_id for issue in issues]
    if len(issue_ids) != len(set(issue_ids)):
        raise ValueError("issues must be unique")

    corpus = corpus or card_corpus()
    cards = tuple(corpus.by_id.values())
    propositions = [card.proposition for card in cards]
    index_by_id = {card.id: index for index, card in enumerate(cards)}
    lexical = lexical or LexicalIndex.build(propositions)
    if dense is None and encoder is not None:
        dense = DenseIndex.build(propositions, encoder)
    focus_by_issue = focus_by_issue or {}

    results: list[RetrievedIssueCards] = []
    for issue in issues:
        unknown_ids = set(issue.retrieval_card_ids) - set(index_by_id)
        if unknown_ids:
            raise ValueError(
                f"{issue.issue_id}: retrieval ids absent from corpus: {sorted(unknown_ids)}"
            )
        candidate_indices = [index_by_id[card_id] for card_id in issue.retrieval_card_ids]
        queries = issue_retrieval_queries(
            issue,
            facts,
            focus_texts=focus_by_issue.get(issue.issue_id, ()),
        )
        best_scores: dict[int, float] = {}
        for query in queries:
            lexical_scores = lexical.scores(query)
            lexical_ranking = sorted(
                (
                    index
                    for index in candidate_indices
                    if lexical_scores[index] > 0.0
                ),
                key=lambda index: (-lexical_scores[index], index),
            )
            rankings: list[Sequence[int]] = []
            if lexical_ranking:
                rankings.append(lexical_ranking)
            if dense is not None and encoder is not None and candidate_indices:
                query_vector = encoder.encode([query], is_query=True)[0]
                dense_scores = dense.scores(query_vector)
                rankings.append(
                    sorted(
                        candidate_indices,
                        key=lambda index: (-dense_scores[index], index),
                    )
                )
            if not rankings:
                continue
            fused = reciprocal_rank_fusion(rankings)
            shortlist = sorted(
                fused, key=lambda index: (-fused[index], index)
            )[:shortlist_per_query]
            if reranker is not None and shortlist:
                reranked = reranker.score(
                    query, [propositions[index] for index in shortlist]
                )
                query_scores = dict(zip(shortlist, reranked))
            else:
                query_scores = {index: fused[index] for index in shortlist}
            for index, score in query_scores.items():
                if score > best_scores.get(index, float("-inf")):
                    best_scores[index] = score

        selected = sorted(
            best_scores,
            key=lambda index: (-best_scores[index], cards[index].id),
        )[:top_k_per_issue]
        selected_cards = tuple(cards[index] for index in selected)
        results.append(
            RetrievedIssueCards(
                issue_id=issue.issue_id,
                queries=queries,
                cards=selected_cards,
                card_scores={card.id: best_scores[index] for card, index in zip(selected_cards, selected)},
            )
        )
    return IssueCardRetrievalResult(results=tuple(results))
