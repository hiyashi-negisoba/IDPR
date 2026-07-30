"""Resolve one role per card, from the review where it exists and the slot elsewhere.

The legal review returned roles at card granularity, and 9 of the 25 slots it settled
split across two or more roles. So a card's role cannot be read off its slot. But the
review covered 86 cards out of 1,848, and the remaining 1,762 need a role too.

The resolution is therefore two-tier and the tier is recorded:

``reviewed``      the reviewer named this card's role. Authoritative.
``slot_default``  inherited from the slot's derived role in :mod:`idpr.rulebase.skeleton`.

Keeping the tier on the resolved role matters for two reasons. It tells the next review
pass which roles have actually been looked at, and it lets the offence gate be measured
with and without the inherited tier -- if the pipeline's behaviour turns on 1,762 inherited
guesses, that is a result to report rather than a detail to hide.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Mapping, Sequence

from idpr.rulebase.cards import CardCorpus, card_corpus
from idpr.rulebase.review import Verdict, parse_review
from idpr.rulebase.skeleton import (
    CONTEXT,
    CORE,
    ELEMENT_ROLES,
    PRESUMED,
    SlotClassification,
    derive_skeleton,
)

REVIEWED = "reviewed"
SLOT_DEFAULT = "slot_default"


@dataclass(frozen=True)
class CardRole:
    """One card's resolved role and where the role came from."""

    card_id: str
    article: str
    slot: str
    role: str
    source: str
    #: Set when a reviewed verdict carried a qualification, so a later pass can find it.
    tentative: bool = False

    @property
    def is_element(self) -> bool:
        return self.role in ELEMENT_ROLES


def resolve_card_roles(
    corpus: CardCorpus | None = None,
    verdicts: Sequence[Verdict] | None = None,
    classifications: Sequence[SlotClassification] | None = None,
) -> tuple[CardRole, ...]:
    """Every card's role, reviewed verdicts taking precedence over the slot default."""
    corpus = corpus or card_corpus()
    if verdicts is None:
        verdicts = parse_review(corpus=corpus)
    if classifications is None:
        classifications = derive_skeleton(corpus)

    reviewed = {verdict.card_id: verdict for verdict in verdicts}
    slot_roles = {c.slot: c.role for c in classifications}

    roles: list[CardRole] = []
    for card in corpus.cards:
        verdict = reviewed.get(card.id)
        if verdict is not None:
            roles.append(
                CardRole(
                    card_id=card.id,
                    article=card.article,
                    slot=card.slot,
                    role=verdict.role,
                    source=REVIEWED,
                    tentative=verdict.tentative,
                )
            )
            continue
        roles.append(
            CardRole(
                card_id=card.id,
                article=card.article,
                slot=card.slot,
                # A slot with no derived role at all would be a skeleton gap; CONTEXT is
                # the inert default, which keeps an unknown card out of the gate rather
                # than letting it decide an element.
                role=slot_roles.get(card.slot, CONTEXT),
                source=SLOT_DEFAULT,
            )
        )
    return tuple(roles)


def element_slots(roles: Sequence[CardRole]) -> Mapping[str, str]:
    """``slot -> core | presumed``, derived from the roles of the cards it holds.

    This is the dependency the review inverted. A slot is an element slot because it holds
    a card stating an element, not the other way round. ``core`` wins a tie: a slot holding
    both kinds demands the affirmative showing.
    """
    derived: dict[str, str] = {}
    for role in roles:
        if role.role == CORE:
            derived[role.slot] = CORE
        elif role.role == PRESUMED and derived.get(role.slot) != CORE:
            derived[role.slot] = PRESUMED
    return derived


def role_summary(roles: Sequence[CardRole]) -> dict[str, object]:
    slots = element_slots(roles)
    return {
        "cards": len(roles),
        "by_role": dict(Counter(r.role for r in roles).most_common()),
        "by_source": dict(Counter(r.source for r in roles).most_common()),
        "reviewed_overriding_slot_default": sum(
            1 for r in roles if r.source == REVIEWED
        ),
        "tentative": sum(1 for r in roles if r.tentative),
        "element_slots": len(slots),
        "element_slots_by_kind": dict(Counter(slots.values()).most_common()),
        "articles_with_an_element_slot": len(
            {r.article for r in roles if r.slot in slots}
        ),
    }
