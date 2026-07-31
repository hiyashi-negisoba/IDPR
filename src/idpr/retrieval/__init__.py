"""L0: which articles does this case put in issue?

Retrieval decides scope, not law. It picks candidate articles; call 2 then assesses every
card those articles carry. That division is why the one invariant here is *card-lossless
within a selected article*: dropping a card inside a relevant article is exactly how a
rubric item is lost, and -- worse -- the symbolic gate blocks only on cards it was given,
so a card that is never assessed can never refute anything. Partial retrieval inside an
article does not fail safe; it fails permissive.

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

#: Reciprocal-rank-fusion constant. The standard value; not tuned.
RRF_K = 60

#: Articles handed to call 2. The plan's own sizing: 14 articles actually bear on the
#: smoke case, so 18 leaves headroom. Precision costs little here -- the rubric has no
#: precision penalty and a spare article costs a few ``unknown`` card statuses -- while a
#: missed article is unrecoverable downstream.
DEFAULT_TOP_K_ARTICLES = 18

#: Cards per query carried into cross-encoder reranking. A reranker is a shortlist tool;
#: scoring all 1,848 cards per query is both wrong and slow.
DEFAULT_SHORTLIST_PER_QUERY = 100

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


# --------------------------------------------------------------------------- #
# Retrieval
# --------------------------------------------------------------------------- #


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
