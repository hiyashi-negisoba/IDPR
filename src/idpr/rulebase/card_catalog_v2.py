"""Compile flat RuleIR cards into an explicit runtime-oriented catalog.

The source corpus is intentionally preserved.  This module adds the distinction the flat
cards lack: a commentary slot may be a core element group while most cards inside it are
definitions, application standards, or precedent fact patterns rather than independent
core elements.  No card inherits ``canonical_element`` from its slot.

The compiler is provisional rather than a substitute for legal review.  It records every
signal used and flags classifications that still depend on a slot-derived role or on a
linguistic precedent detector.  The resulting asset is therefore both a runtime proposal
and a finite review queue.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import asdict, dataclass
from typing import Iterable, Sequence

from idpr.rulebase.cards import Card, CardCorpus, card_corpus
from idpr.rulebase.formalization import (
    CONCURRENCE_SEED,
    NARRATIVE,
    SKELETON_META,
    STAGE_SEED,
    CardRouting,
    route_corpus,
)
from idpr.rulebase.roles import CardRole, SLOT_DEFAULT, resolve_card_roles

CATALOG_VERSION = "2.0.0-draft"

CANONICAL_ELEMENT = "canonical_element"
APPLICATION_STANDARD = "application_standard"
EXCEPTION = "exception"
DEFEATER = "defeater"
STAGE = "stage"
CONCURRENCE = "concurrence"
PARTICIPATION = "participation"
NARRATIVE_FUNCTION = "narrative"
SKELETON_META_FUNCTION = "skeleton_meta"

FUNCTIONS = frozenset(
    {
        CANONICAL_ELEMENT,
        APPLICATION_STANDARD,
        EXCEPTION,
        DEFEATER,
        STAGE,
        CONCURRENCE,
        PARTICIPATION,
        NARRATIVE_FUNCTION,
        SKELETON_META_FUNCTION,
    }
)

ABSTRACT_RULE = "abstract_rule"
PRECEDENT_RULE = "precedent_rule"
PRECEDENT_PATTERN = "precedent_pattern"
FORMS = frozenset({ABSTRACT_RULE, PRECEDENT_RULE, PRECEDENT_PATTERN})

ALWAYS_ASSESS = "always_assess"
RETRIEVE_ASSESS = "retrieve_assess"
RETRIEVE_ONLY = "retrieve_only"
RELATION_CONDITION = "relation_condition"
STATIC = "static"
RUNTIMES = frozenset(
    {ALWAYS_ASSESS, RETRIEVE_ASSESS, RETRIEVE_ONLY, RELATION_CONDITION, STATIC}
)

SUPPORT = "support"
REFUTE = "refute"
EXCLUDE = "exclude"
BLOCK = "block"
NONE = "none"
GATE_EFFECTS = frozenset({SUPPORT, REFUTE, EXCLUDE, BLOCK, NONE})

# Conservative by design: only explicit case-report language makes a precedent pattern.
# A missed pattern stays in the review queue as an application standard; a general legal
# rule should not be demoted merely because it mentions 판례.
_PRECEDENT_PATTERN_RE = re.compile(
    r"사례(?:가|를|로|에서|에서는)|사안(?:에서|에서는)|판결(?:이|에서|에서는|의)"
    r"|소개되어 있다|판시한 사례|인정한 사례|부정한 사례"
)
_FACT_LIMITED_REVIEW_RE = re.compile(
    r"사실관계에 한정|구체적 사실관계|소개된 사례|구체적 판례 결론|판단례"
)


@dataclass(frozen=True, slots=True)
class CatalogCard:
    card_id: str
    article: str
    element_group: str
    proposition: str
    polarity: str
    norm_kind: str
    function: str
    form: str
    runtime: str
    gate_effect: str
    classification_signals: tuple[str, ...]
    review_required: bool
    review_reasons: tuple[str, ...]

    def as_dict(self) -> dict:
        payload = asdict(self)
        payload["classification_signals"] = list(self.classification_signals)
        payload["review_reasons"] = list(self.review_reasons)
        return payload


class CardCatalogV2Error(ValueError):
    """Raised when the compiled catalog loses a card or emits an invalid category."""


def classify_card_form(card: Card) -> str:
    """Separate general precedent holdings from fact-bound precedent patterns."""
    if card.doctrinal_status == "precedent_position":
        if (
            card.norm_kind == "definition"
            and not _PRECEDENT_PATTERN_RE.search(card.proposition)
            and not _FACT_LIMITED_REVIEW_RE.search(card.review_notes)
        ):
            return PRECEDENT_RULE
        return PRECEDENT_PATTERN
    return (
        PRECEDENT_PATTERN
        if _PRECEDENT_PATTERN_RE.search(card.proposition)
        else ABSTRACT_RULE
    )


def _function(
    card: Card, routing: CardRouting, role: CardRole, form: str
) -> tuple[str, str]:
    frames = set(routing.frames_matched)
    if routing.route == SKELETON_META:
        return SKELETON_META_FUNCTION, "route:skeleton_meta"
    if routing.route == NARRATIVE:
        return NARRATIVE_FUNCTION, "route:narrative"
    if CONCURRENCE_SEED in frames or routing.route == CONCURRENCE_SEED:
        return CONCURRENCE, "frame:concurrence"
    if STAGE_SEED in frames or routing.route == STAGE_SEED:
        return STAGE, "frame:stage"
    if card.norm_kind == "definition":
        return NARRATIVE_FUNCTION, "norm_kind:definition"
    if card.polarity == "exception" or card.norm_kind == "exception":
        return EXCEPTION, "metadata:exception"
    # A canonical element must be stated by the card itself.  Slot role is never enough.
    if card.norm_kind == "element":
        if form == PRECEDENT_PATTERN:
            return APPLICATION_STANDARD, "element:precedent_pattern_demoted"
        return CANONICAL_ELEMENT, "norm_kind:element"
    if role.role == DEFEATER:
        return DEFEATER, "role:defeater"
    if role.role == PARTICIPATION:
        return PARTICIPATION, "role:participation"
    if role.role == STAGE:
        return STAGE, "role:stage"
    if role.role == CONCURRENCE:
        return CONCURRENCE, "role:concurrence"
    return APPLICATION_STANDARD, f"norm_kind:{card.norm_kind}"


def _runtime(function: str, form: str) -> str:
    if function in {NARRATIVE_FUNCTION, SKELETON_META_FUNCTION}:
        return STATIC
    if function == CANONICAL_ELEMENT:
        return ALWAYS_ASSESS
    if function in {STAGE, CONCURRENCE, PARTICIPATION}:
        return RELATION_CONDITION
    if form == PRECEDENT_PATTERN:
        return RETRIEVE_ONLY
    return RETRIEVE_ASSESS


def _gate_effect(card: Card, function: str) -> str:
    if card.polarity == "exception" or function == EXCEPTION:
        return EXCLUDE
    if function == DEFEATER:
        return BLOCK
    if function in {CANONICAL_ELEMENT, APPLICATION_STANDARD}:
        return REFUTE if card.polarity == "negative" else SUPPORT
    return NONE


def classify_card(card: Card, routing: CardRouting, role: CardRole) -> CatalogCard:
    """Classify one card without promoting any slot-default card to canonical element."""
    form = classify_card_form(card)
    function, primary_signal = _function(card, routing, role, form)
    reasons: list[str] = []
    signals = [primary_signal, f"role:{role.role}/{role.source}", f"form:{form}"]

    if primary_signal.startswith("role:") and role.source == SLOT_DEFAULT:
        reasons.append("function depends on an unreviewed slot-default role")
    if form == PRECEDENT_PATTERN:
        if card.doctrinal_status == "precedent_position":
            signals.append("doctrinal_status:precedent_position")
        else:
            reasons.append("precedent-pattern form was detected linguistically")
    elif form == PRECEDENT_RULE:
        signals.append("doctrinal_status:precedent_general_rule")
    if card.norm_kind == "element" and function != CANONICAL_ELEMENT:
        reasons.append("element metadata is overridden by a stage/concurrence/static frame")
    if card.norm_kind == "definition" and function not in {
        NARRATIVE_FUNCTION,
        STAGE,
        CONCURRENCE,
        SKELETON_META_FUNCTION,
    }:
        reasons.append("definition metadata conflicts with runtime function")

    return CatalogCard(
        card_id=card.id,
        article=card.article,
        element_group=card.slot,
        proposition=card.proposition,
        polarity=card.polarity,
        norm_kind=card.norm_kind,
        function=function,
        form=form,
        runtime=_runtime(function, form),
        gate_effect=_gate_effect(card, function),
        classification_signals=tuple(signals),
        review_required=bool(reasons),
        review_reasons=tuple(reasons),
    )


def compile_card_catalog_v2(
    corpus: CardCorpus | None = None,
    *,
    routings: Sequence[CardRouting] | None = None,
    roles: Sequence[CardRole] | None = None,
) -> tuple[CatalogCard, ...]:
    corpus = corpus or card_corpus()
    routings = tuple(routings or route_corpus(corpus))
    roles = tuple(roles or resolve_card_roles(corpus))
    routing_by_id = {item.card_id: item for item in routings}
    role_by_id = {item.card_id: item for item in roles}
    expected = {card.id for card in corpus.cards}
    if set(routing_by_id) != expected or set(role_by_id) != expected:
        raise CardCatalogV2Error("routing and role inputs must cover the exact card corpus")
    compiled = tuple(
        classify_card(card, routing_by_id[card.id], role_by_id[card.id])
        for card in corpus.cards
    )
    validate_card_catalog_v2(compiled, expected_ids=expected)
    return compiled


def validate_card_catalog_v2(
    cards: Sequence[CatalogCard], *, expected_ids: Iterable[str]
) -> None:
    errors: list[str] = []
    ids = [card.card_id for card in cards]
    expected = set(expected_ids)
    if len(ids) != len(set(ids)):
        errors.append("catalog contains duplicate card ids")
    if set(ids) != expected:
        errors.append(
            f"catalog card coverage differs: missing={sorted(expected - set(ids))}, "
            f"extra={sorted(set(ids) - expected)}"
        )
    for card in cards:
        if card.function not in FUNCTIONS:
            errors.append(f"{card.card_id}: invalid function {card.function}")
        if card.form not in FORMS:
            errors.append(f"{card.card_id}: invalid form {card.form}")
        if card.runtime not in RUNTIMES:
            errors.append(f"{card.card_id}: invalid runtime {card.runtime}")
        if card.gate_effect not in GATE_EFFECTS:
            errors.append(f"{card.card_id}: invalid gate effect {card.gate_effect}")
        if card.function == CANONICAL_ELEMENT and card.norm_kind != "element":
            errors.append(f"{card.card_id}: canonical element lacks element metadata")
        if card.runtime == ALWAYS_ASSESS and card.function != CANONICAL_ELEMENT:
            errors.append(f"{card.card_id}: only canonical elements may be always_assess")
    if errors:
        raise CardCatalogV2Error("; ".join(errors))


def catalog_summary(cards: Sequence[CatalogCard]) -> dict[str, object]:
    return {
        "cards": len(cards),
        "by_function": dict(Counter(card.function for card in cards).most_common()),
        "by_form": dict(Counter(card.form for card in cards).most_common()),
        "by_runtime": dict(Counter(card.runtime for card in cards).most_common()),
        "by_gate_effect": dict(
            Counter(card.gate_effect for card in cards).most_common()
        ),
        "review_required": sum(card.review_required for card in cards),
        "articles": len({card.article for card in cards}),
        "element_groups": len({card.element_group for card in cards}),
    }


def catalog_payload(cards: Sequence[CatalogCard]) -> dict[str, object]:
    return {
        "version": CATALOG_VERSION,
        "source": "live reviewed RuleIR corpus; original cards preserved",
        "summary": catalog_summary(cards),
        "cards": [card.as_dict() for card in cards],
    }
