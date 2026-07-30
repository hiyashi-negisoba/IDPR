"""Read the legal reviewer's verdicts back out of the review document.

The review document is the reviewer's working surface: they annotate it in place with
``> comment:`` lines under each item. This module parses those lines so the markdown stays
the single source of truth -- transcribing the verdicts into a second file by hand would
put two versions of a legal judgment in the repository and let them drift.

What the review established
---------------------------
The verdicts arrived at *card* granularity, not slot granularity. Of the 23 blocking items
the reviewer settled, 10 split a single slot across two or more roles -- 제355조 총설's 18
불법영득의사 cards divide into core, defeater and context. So the role is a property of a
card, and the slot-level derivation in :mod:`idpr.rulebase.skeleton` is a *default* that
card-level verdicts override, not an answer in its own right.

This inverts the dependency the plan assumed: slot roles are now derived from card roles
(a slot is an element slot because it holds a card that states an element), rather than
card roles being inherited from a slot.

Interpretation
--------------
Four annotations needed a reading rather than a transcription, and each is recorded on the
verdict so the choice is visible:

``coree``               a typo for ``core``.
``defeater-context``    read as ``defeater``. The card states the test governing when the
                        defeater applies, so it gates the offence the way a defeater does.
``B1``'s conditional    "context (수뢰죄에서 구성요건 다루는 카드가 없다면 core)" resolves
                        to ``context``: 제129조 does have 구성요건 slots
                        (``art129_sec1_1`` 13장, ``art129_sec1_2`` 8장), both already core.
``A1``'s "…같기도해"      kept as the stated role and flagged tentative.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping, Sequence

from idpr.rulebase.cards import CardCorpus, card_corpus
from idpr.rulebase.skeleton import (
    CONCURRENCE,
    CONTEXT,
    CORE,
    DEFEATER,
    PARTICIPATION,
    PRESUMED,
    STAGE,
)

PROJECT_ROOT = Path(__file__).resolve().parents[3]
REVIEW_PATH = PROJECT_ROOT / "data/rulebase/element_skeleton_review.md"

#: Spellings the reviewer used, mapped to canonical roles. Longer keys are matched first
#: so ``defeater-context`` is not read as ``defeater`` followed by stray text.
ROLE_ALIASES: Mapping[str, str] = {
    "core": CORE,
    "coree": CORE,
    "presumed": PRESUMED,
    "stage": STAGE,
    "defeater": DEFEATER,
    "defeater-context": DEFEATER,
    "concurrence": CONCURRENCE,
    "participation": PARTICIPATION,
    "context": CONTEXT,
}

_ROLE_PATTERN = "|".join(
    re.escape(alias) for alias in sorted(ROLE_ALIASES, key=len, reverse=True)
)

#: ``### B16. art355 · `art355_sec4_1` — 총설``
_ITEM_RE = re.compile(r"^###\s+([BA])(\d+)\.\s+(\S+)\s+·\s+`([^`]+)`\s+—\s*(.*)$")
_COMMENT_RE = re.compile(r"^>\s*comment:\s*(.*)$")

#: ``1, 2, 3번 core`` / ``1,2번 core`` / ``2, 3번은 context`` / ``1, 2, 3 context``
_NUMBERED_RE = re.compile(
    rf"((?:\d+\s*[,·]\s*)*\d+)\s*번?(?:은|이)?\s*({_ROLE_PATTERN})"
)
_BARE_ROLE_RE = re.compile(rf"({_ROLE_PATTERN})")

#: Markers that qualify a verdict rather than change it.
_QUESTION_MARK = "?"
_CONDITIONAL_MARKERS = ("만약", "없다면", "있다면")
_TENTATIVE_MARKERS = ("같기도", "같기는", "듯")


@dataclass(frozen=True)
class Verdict:
    """One reviewed role assignment, with the annotation it came from."""

    card_id: str
    slot: str
    article: str
    role: str
    item: str
    #: 1-based position of the card within its slot, as rendered in the review document.
    card_index: int
    comment: str
    applies_to_whole_slot: bool
    tentative: bool
    conditional: bool
    has_question: bool


class ReviewParseError(ValueError):
    """Raised when an annotation cannot be resolved to a role, or names a missing card."""


def _flags(comment: str) -> tuple[bool, bool, bool]:
    tentative = any(marker in comment for marker in _TENTATIVE_MARKERS)
    conditional = any(marker in comment for marker in _CONDITIONAL_MARKERS)
    return tentative, conditional, _QUESTION_MARK in comment


def parse_role_assignments(comment: str) -> tuple[Mapping[int, str], str | None]:
    """Turn one ``> comment:`` body into ``({card index: role}, whole-slot role)``.

    Exactly one of the two is populated. A comment naming no card number applies to every
    card in the slot, which is how the reviewer wrote the unanimous items ("all context").
    """
    numbered = list(_NUMBERED_RE.finditer(comment))
    if numbered:
        assignments: dict[int, str] = {}
        for match in numbered:
            role = ROLE_ALIASES[match.group(2)]
            for token in re.split(r"[,·]", match.group(1)):
                token = token.strip()
                if token:
                    assignments[int(token)] = role
        return assignments, None

    bare = _BARE_ROLE_RE.search(comment)
    if bare is None:
        raise ReviewParseError(f"no role found in annotation: {comment!r}")
    # The first role named wins. B1's "context (… 없다면 core)" states the verdict first
    # and the discarded alternative second.
    return {}, ROLE_ALIASES[bare.group(1)]


def parse_review(
    path: Path | None = None, corpus: CardCorpus | None = None
) -> tuple[Verdict, ...]:
    """Every verdict in the review document, expanded to individual cards.

    Card numbers are resolved against ``corpus.by_slot()``, which is the order the review
    document renders them in, so a reordering of the corpus would be caught here as a
    missing index rather than silently relabelling a different card.
    """
    corpus = corpus or card_corpus()
    by_slot = corpus.by_slot()
    text = (path or REVIEW_PATH).read_text(encoding="utf-8")

    verdicts: list[Verdict] = []
    item = ""
    slot = ""
    article = ""

    for line in text.splitlines():
        header = _ITEM_RE.match(line)
        if header:
            item = f"{header.group(1)}{header.group(2)}"
            article = header.group(3)
            slot = header.group(4)
            continue

        comment_match = _COMMENT_RE.match(line)
        if not comment_match:
            continue
        comment = comment_match.group(1).strip()
        if not slot:
            raise ReviewParseError(f"annotation before any item header: {comment!r}")

        cards = by_slot.get(slot)
        if not cards:
            raise ReviewParseError(f"{item}: slot {slot!r} is not in the corpus")

        assignments, whole_slot_role = parse_role_assignments(comment)
        tentative, conditional, has_question = _flags(comment)

        if whole_slot_role is not None:
            assignments = {index: whole_slot_role for index in range(1, len(cards) + 1)}

        for index, role in sorted(assignments.items()):
            if not 1 <= index <= len(cards):
                raise ReviewParseError(
                    f"{item}: card {index} is out of range for slot {slot} "
                    f"({len(cards)} cards)"
                )
            verdicts.append(
                Verdict(
                    card_id=cards[index - 1].id,
                    slot=slot,
                    article=article,
                    role=role,
                    item=item,
                    card_index=index,
                    comment=comment,
                    applies_to_whole_slot=whole_slot_role is not None,
                    tentative=tentative,
                    conditional=conditional,
                    has_question=has_question,
                )
            )

    return tuple(verdicts)


def verdict_map(verdicts: Sequence[Verdict]) -> Mapping[str, str]:
    """``card_id -> reviewed role``."""
    return {verdict.card_id: verdict.role for verdict in verdicts}


def review_summary(verdicts: Sequence[Verdict]) -> dict[str, object]:
    """Counts worth reporting, including how often a slot split across roles."""
    by_slot: dict[str, set[str]] = {}
    for verdict in verdicts:
        by_slot.setdefault(verdict.slot, set()).add(verdict.role)
    split = sorted(slot for slot, roles in by_slot.items() if len(roles) > 1)
    return {
        "verdicts": len(verdicts),
        "items": len({verdict.item for verdict in verdicts}),
        "slots": len(by_slot),
        "by_role": dict(Counter(v.role for v in verdicts).most_common()),
        "slots_split_across_roles": split,
        "tentative": sorted({v.item for v in verdicts if v.tentative}),
        "questions": sorted({v.item for v in verdicts if v.has_question}),
    }
