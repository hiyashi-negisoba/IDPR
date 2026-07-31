"""Local encoder and reranker for L0. Both run on one GPU, both cost $0.

Kept out of ``idpr.retrieval`` proper so the retrieval logic imports and tests without
torch. The protocols in the package are the seam; these are one implementation of them.

``HF_HUB_OFFLINE`` must not be set when these load, even though both snapshots are cached:
``transformers==4.57.3`` calls ``model_info()`` from ``_patch_mistral_regex`` unconditionally
and dies offline. Set ``HF_HOME`` and leave the offline flags alone.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence

DENSE_MODEL = "google/embeddinggemma-300m"
RERANKER_MODEL = "BAAI/bge-reranker-v2-m3"


@dataclass
class SentenceTransformerEncoder:
    """embeddinggemma-300m. Asymmetric: queries and documents get different prompts.

    Using one prompt for both is a silent quality loss on this model -- it is trained with
    task prefixes, and dropping them puts queries and documents in slightly different
    places in the space.
    """

    model_id: str = DENSE_MODEL
    batch_size: int = 64
    _model: Any = field(default=None, init=False, repr=False)

    @property
    def name(self) -> str:
        return self.model_id.split("/")[-1]

    def _load(self) -> Any:
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self.model_id)
        return self._model

    def encode(self, texts: Sequence[str], *, is_query: bool) -> list[list[float]]:
        model = self._load()
        encode = model.encode_query if is_query else model.encode_document
        vectors = encode(list(texts), batch_size=self.batch_size, show_progress_bar=False)
        return [list(map(float, vector)) for vector in vectors]


@dataclass
class CrossEncoderReranker:
    """bge-reranker-v2-m3, applied to a shortlist only.

    A cross-encoder scores the pair jointly, so it cannot be precomputed and its cost is
    linear in candidates. Running it over all 1,848 cards per query is both the wrong tool
    use and, measured, the reason the first attempt's job timed out.
    """

    model_id: str = RERANKER_MODEL
    batch_size: int = 64
    _model: Any = field(default=None, init=False, repr=False)

    @property
    def name(self) -> str:
        return self.model_id.split("/")[-1]

    def _load(self) -> Any:
        if self._model is None:
            from sentence_transformers import CrossEncoder

            self._model = CrossEncoder(self.model_id)
        return self._model

    def score(self, query: str, documents: Sequence[str]) -> list[float]:
        if not documents:
            return []
        model = self._load()
        scores = model.predict(
            [(query, document) for document in documents],
            batch_size=self.batch_size,
            show_progress_bar=False,
        )
        return [float(score) for score in scores]
