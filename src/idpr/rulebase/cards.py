"""Unified live-card corpus for the criminal-law rulebase.

Loads every reviewed RuleIR card from the three sources that hold them -- the P2
(non-property) units, the property units, and the fraud NormCard set -- into one
corpus keyed by card id, and derives the two structural keys the symbolic layer
needs: the ``article`` a card belongs to and the ``slot`` (commentary section)
within it.

Two invariants are enforced here rather than left to callers:

*Only reviewed propositions reach a model.* Each card carries its verbatim
commentary quotes and ``comment_id`` back-pointers, but :meth:`Card.model_payload`
exposes only ``id`` and ``proposition``. The quotes stay host-side, where they back
citation rendering and the audit trail. Sending them back to a model would undo the
review step that produced the proposition, and would roughly double the payload
(measured: 130 chars per card with the proposition alone, 244 with quotes).

*Rejected doctrine never enters the corpus.* Only cards promoted into the unit files
are loaded. ``data/card_case_metadata_map.json`` is deliberately not used: 1,639 of
its 3,487 keys are NormCards that were never promoted, and it reaches only 161 of the
1,848 live cards with a case number, versus 1,392 via the commentary join in
:mod:`idpr.rulebase.authority`.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

PROJECT_ROOT = Path(__file__).resolve().parents[3]

P2_UNIT_DIR = PROJECT_ROOT / "data/rulegen/p2/rule_ir_units"
PROPERTY_UNIT_DIR = PROJECT_ROOT / "data/rulegen/property/rule_ir_units"
FRAUD_CARD_SET = PROJECT_ROOT / "data/rulegen/fraud/fraud_core_norm_card_set.json"

#: The fraud cards predate the ``artNNN`` id convention and use module-prefixed ids
#: (``deception.fraud.causal-link.…``). They are all 제347조.
FRAUD_ARTICLE = "art347"

#: Marks cards whose source text came from the per-article PDF rather than the parsed
#: parquet. It is provenance, not part of the article key.
_PDF_FALLBACK_SUFFIX = "_x_raw_pdf"

VALID_POLARITIES = frozenset({"positive", "negative", "exception"})
VALID_FORMALIZATIONS = frozenset({"standard_input", "deterministic_rule"})

_REQUIRED_CARD_FIELDS = (
    "id",
    "proposition",
    "polarity",
    "norm_kind",
    "formalization",
    "doctrinal_status",
)


class CardCorpusError(ValueError):
    """Raised when the card corpus violates a structural contract.

    Collects every problem found rather than failing on the first, so a malformed
    unit file reports all of its defects in one pass.
    """

    def __init__(self, errors: Sequence[str]) -> None:
        self.errors = list(errors)
        super().__init__("; ".join(self.errors))


@dataclass(frozen=True)
class Card:
    """One reviewed normative proposition, with its structural keys and provenance."""

    id: str
    article: str
    slot: str
    proposition: str
    polarity: str
    norm_kind: str
    formalization: str
    doctrinal_status: str
    source_comment_ids: tuple[str, ...]
    source_quotes: tuple[str, ...]
    unit: str
    source_section_paths: tuple[str, ...] = ()
    authority_basis: str = ""
    review_notes: str = ""

    @property
    def is_standard_input(self) -> bool:
        """Whether this card is an open-textured standard the model must assess.

        The complement (``deterministic_rule``) stays in the symbolic layer.
        """
        return self.formalization == "standard_input"

    def model_payload(self) -> dict[str, str]:
        """The only card content a model may see: the reviewed proposition.

        Deliberately excludes ``source_quotes`` and ``source_comment_ids``.
        """
        return {"id": self.id, "proposition": self.proposition}


def split_card_id(card_id: str) -> tuple[str, str]:
    """Derive ``(article, slot)`` from a card id.

    Four id shapes occur in the corpus and each is handled explicitly rather than by
    one permissive pattern, because the article token itself may contain underscores:

    ``art298_sec3_1.deception_degree``  -> ``("art298", "art298_sec3_1")``
    ``art225.contractual_delegate``     -> ``("art225", "art225")``
    ``art2582_2_sec1.group_force``      -> ``("art2582_2", "art2582_2_sec1")``  (제258조의2)
    ``art344_x_raw_pdf.relative_scope`` -> ``("art344", "art344")``
    ``deception.fraud.causal-link.x``   -> ``("art347", "deception")``

    Section suffixes are not always numeric (``art130_sec3-na``, ``art130_sec3_가``);
    they are kept verbatim in the slot and only the article is normalised.
    """
    head = card_id.split(".", 1)[0]

    if not head.startswith("art"):
        # Fraud module-prefixed id: the leading component names the element group.
        return FRAUD_ARTICLE, head

    section_split = re.split(r"_sec", head, maxsplit=1)
    article = section_split[0]
    slot = head

    if article.endswith(_PDF_FALLBACK_SUFFIX):
        article = article[: -len(_PDF_FALLBACK_SUFFIX)]
        slot = article

    return article, slot


def _load_json(path: Path) -> Mapping[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _card_from_raw(raw: Mapping[str, Any], *, unit: str, errors: list[str]) -> Card | None:
    card_id = raw.get("id")
    missing = [f for f in _REQUIRED_CARD_FIELDS if not raw.get(f)]
    if missing:
        errors.append(f"{unit}: card {card_id!r} missing {missing}")
        return None

    polarity = raw["polarity"]
    if polarity not in VALID_POLARITIES:
        errors.append(f"{unit}: card {card_id} has unknown polarity {polarity!r}")
        return None

    formalization = raw["formalization"]
    if formalization not in VALID_FORMALIZATIONS:
        errors.append(
            f"{unit}: card {card_id} has unknown formalization {formalization!r}"
        )
        return None

    source_refs = raw.get("source_refs") or []
    if not source_refs:
        errors.append(f"{unit}: card {card_id} has no source_refs")
        return None

    comment_ids: list[str] = []
    quotes: list[str] = []
    section_paths: list[str] = []
    for ref in source_refs:
        comment_id = ref.get("comment_id")
        quote = ref.get("quote")
        section_path = ref.get("section_path")
        if not comment_id or not quote or not section_path:
            errors.append(f"{unit}: card {card_id} has an incomplete source_ref")
            continue
        comment_ids.append(comment_id)
        quotes.append(quote)
        section_paths.append(section_path)

    article, slot = split_card_id(card_id)
    return Card(
        id=card_id,
        article=article,
        slot=slot,
        proposition=raw["proposition"],
        polarity=polarity,
        norm_kind=raw["norm_kind"],
        formalization=formalization,
        doctrinal_status=raw["doctrinal_status"],
        source_comment_ids=tuple(comment_ids),
        source_quotes=tuple(quotes),
        unit=unit,
        source_section_paths=tuple(section_paths),
        authority_basis=raw.get("authority_basis", ""),
        review_notes=raw.get("review_notes", ""),
    )


def _iter_unit_files() -> Iterable[tuple[str, Path]]:
    for path in sorted(P2_UNIT_DIR.glob("*.json")):
        yield f"p2/{path.stem}", path
    for path in sorted(PROPERTY_UNIT_DIR.glob("*.json")):
        yield f"property/{path.stem}", path
    yield "fraud/core_norm_card_set", FRAUD_CARD_SET


@dataclass(frozen=True)
class CardCorpus:
    """Every live card, indexed by id, slot and article."""

    cards: tuple[Card, ...]

    @property
    def by_id(self) -> dict[str, Card]:
        return {card.id: card for card in self.cards}

    def by_article(self) -> dict[str, tuple[Card, ...]]:
        grouped: dict[str, list[Card]] = {}
        for card in self.cards:
            grouped.setdefault(card.article, []).append(card)
        return {article: tuple(items) for article, items in sorted(grouped.items())}

    def by_slot(self) -> dict[str, tuple[Card, ...]]:
        grouped: dict[str, list[Card]] = {}
        for card in self.cards:
            grouped.setdefault(card.slot, []).append(card)
        return {slot: tuple(items) for slot, items in sorted(grouped.items())}

    def standard_input_cards(self) -> tuple[Card, ...]:
        return tuple(card for card in self.cards if card.is_standard_input)

    def deterministic_cards(self) -> tuple[Card, ...]:
        return tuple(card for card in self.cards if not card.is_standard_input)

    def cards_for_articles(self, articles: Iterable[str]) -> tuple[Card, ...]:
        wanted = set(articles)
        return tuple(card for card in self.cards if card.article in wanted)


def load_card_corpus() -> CardCorpus:
    """Load and validate every live card. Raises :class:`CardCorpusError` on any defect."""
    errors: list[str] = []
    cards: list[Card] = []
    seen: dict[str, str] = {}

    for unit, path in _iter_unit_files():
        if not path.is_file():
            errors.append(f"{unit}: missing card file {path}")
            continue
        payload = _load_json(path)
        raw_cards = payload.get("cards")
        if not isinstance(raw_cards, list) or not raw_cards:
            errors.append(f"{unit}: no 'cards' array in {path.name}")
            continue
        for raw in raw_cards:
            card = _card_from_raw(raw, unit=unit, errors=errors)
            if card is None:
                continue
            if card.id in seen:
                errors.append(
                    f"duplicate card id {card.id} in {unit} and {seen[card.id]}"
                )
                continue
            seen[card.id] = unit
            cards.append(card)

    if errors:
        raise CardCorpusError(errors)

    return CardCorpus(cards=tuple(cards))


@lru_cache(maxsize=1)
def card_corpus() -> CardCorpus:
    """Process-wide cached corpus."""
    return load_card_corpus()
