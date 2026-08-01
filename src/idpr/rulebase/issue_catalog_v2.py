"""Load the flat card corpus as offence issues with subordinate support cards.

The unit assessed at runtime is an issue packet, not an individual commentary card.
For example, the theft issue ``타인의 재물`` owns the general rule that explains the
element and all ownership/possession standards and precedents beneath it.  The general
rule is sent as compact normative context; the subordinate cards are retrieved only when
the case facts make them useful.

Grouping follows the commentary's reviewed ``section_path`` provenance.  A top-level
section (Roman numeral) is divided only when its leaf slots have genuinely different
functions such as element, stage, concurrence, or defence.  This preserves every source
card exactly once while preventing a commentary chapter full of examples from becoming
dozens of independent mandatory questions.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Mapping, Sequence

from idpr.rulebase.card_catalog_v2 import (
    PRECEDENT_PATTERN,
    PRECEDENT_RULE,
    classify_card_form,
    compile_card_catalog_v2,
)
from idpr.rulebase.cards import Card, CardCorpus, PROJECT_ROOT, card_corpus
from idpr.rulebase.roles import resolve_card_roles
from idpr.rulebase.skeleton import (
    COMMENTARY_CHUNKS,
    COMMENTARY_SUPPLEMENT,
    CONCURRENCE,
    CONTEXT,
    CORE,
    DEFEATER,
    PARTICIPATION,
    PRESUMED,
    STAGE,
    TITLE_BUCKETS,
    UNCLASSIFIED,
    classify_title,
    commentary_section_titles,
    strip_outline_numbering,
)

ISSUE_CATALOG_VERSION = "2.1.0-draft"

ELEMENT_ISSUE = "element_issue"
GUARD_ISSUE = "guard_issue"
STAGE_ISSUE = "stage_issue"
CONCURRENCE_ISSUE = "concurrence_issue"
PARTICIPATION_ISSUE = "participation_issue"
SUPPORT_ISSUE = "support_issue"
ISSUE_FUNCTIONS = frozenset(
    {
        ELEMENT_ISSUE,
        GUARD_ISSUE,
        STAGE_ISSUE,
        CONCURRENCE_ISSUE,
        PARTICIPATION_ISSUE,
        SUPPORT_ISSUE,
    }
)

ASSESS_ISSUE = "assess_issue"
RETRIEVE_GUARD = "retrieve_guard"
RELATION_CONDITION = "relation_condition"
RETRIEVE_SUPPORT = "retrieve_support"
ISSUE_RUNTIMES = frozenset(
    {ASSESS_ISSUE, RETRIEVE_GUARD, RELATION_CONDITION, RETRIEVE_SUPPORT}
)

ANCHOR_CONTEXT = "anchor_context"
RETRIEVE_CANDIDATE = "retrieve_candidate"
SYMBOLIC_ONLY = "symbolic_only"
SUPPORT_ONLY = "support_only"
LOAD_POLICIES = frozenset(
    {ANCHOR_CONTEXT, RETRIEVE_CANDIDATE, SYMBOLIC_ONLY, SUPPORT_ONLY}
)

_ARTICLE_CATALOG = PROJECT_ROOT / "data/rulebase/article_catalog.json"
_ISSUE_TITLE_REVIEW = PROJECT_ROOT / "data/rulebase/issue_title_review.json"
_ISSUE_RUNTIME_REVIEW = PROJECT_ROOT / "data/rulebase/issue_runtime_review.json"
_ANCHOR_LANGUAGE_RE = re.compile(
    r"성립(?:하려면|에는|한다)|인정되려면|필요(?:하다|하고)|요한다|뜻한다|말한다|"
    r"행위는|객체는|주체는|고의는|의사는"
)
_CANONICAL_DEFINITION_RE = re.compile(
    r"^[^,]{1,30}(?:은|란) .*(?:뜻한다|의미|말한다|행위이다|범죄이다)"
)
_CONTAINER_HEADINGS = frozenset({"구성요건", "객관적 구성요건", "주관적 구성요건"})
_ISSUE_CONTEXT_TERMS = frozenset(
    {"법익", "침해범", "권리행사", "본질", "총설", "신설", "산정", "특례"}
)


@dataclass(frozen=True, slots=True)
class IssuePacket:
    issue_id: str
    article: str
    article_label: str
    offense: str
    section_path: str
    title: str
    function: str
    runtime: str
    slot_ids: tuple[str, ...]
    anchor_card_ids: tuple[str, ...]
    member_card_ids: tuple[str, ...]
    retrieval_card_ids: tuple[str, ...]
    case_pattern_card_ids: tuple[str, ...]
    review_required: bool
    review_reasons: tuple[str, ...]

    def as_dict(self) -> dict:
        return asdict(self)

    def model_payload(
        self,
        cards_by_id: Mapping[str, Card],
        *,
        detail_card_ids: Sequence[str] = (),
    ) -> dict[str, object]:
        """Compact Call-2 input with stable anchors and optional retrieved details."""
        details = tuple(detail_card_ids)
        if len(details) != len(set(details)):
            raise IssueCatalogError(f"{self.issue_id}: duplicate detail cards")
        outside = set(details) - set(self.retrieval_card_ids)
        if outside:
            raise IssueCatalogError(
                f"{self.issue_id}: details are not retrieval children: {sorted(outside)}"
            )
        payload: dict[str, object] = {
            "issue_id": self.issue_id,
            "question": f"사실관계상 {self.offense}의 [{self.title}] 쟁점이 충족되는가?",
            "rules": [cards_by_id[card_id].proposition for card_id in self.anchor_card_ids],
        }
        if details:
            payload["details"] = [
                {
                    "id": card_id,
                    "proposition": cards_by_id[card_id].proposition,
                }
                for card_id in details
            ]
        return payload


@dataclass(frozen=True, slots=True)
class CardPlacement:
    card_id: str
    issue_id: str
    load_policy: str
    case_pattern: bool

    def as_dict(self) -> dict:
        return asdict(self)


class IssueCatalogError(ValueError):
    """Raised when hierarchy generation loses a card or violates a runtime contract."""


def _classify_issue_title(title: str) -> str:
    """Issue-only title precedence; the legacy Phase-2 skeleton stays unchanged."""
    text = strip_outline_numbering(title)
    if "음모 절단" in text:
        return CORE
    priority: tuple[tuple[str, frozenset[str]], ...] = (
        (
            PARTICIPATION,
            frozenset(
                key
                for key, role in TITLE_BUCKETS.items()
                if role == PARTICIPATION and key != "신분"
            ),
        ),
        (
            CONCURRENCE,
            frozenset(
                {
                    *(
                        key
                        for key, role in TITLE_BUCKETS.items()
                        if role == CONCURRENCE and key != "관계"
                    ),
                    "구별",
                }
            ),
        ),
        (
            DEFEATER,
            frozenset(
                key for key, role in TITLE_BUCKETS.items() if role == DEFEATER
            ),
        ),
        (
            STAGE,
            frozenset(key for key, role in TITLE_BUCKETS.items() if role == STAGE),
        ),
        (
            CONTEXT,
            frozenset(
                {
                    *(key for key, role in TITLE_BUCKETS.items() if role == CONTEXT),
                    *_ISSUE_CONTEXT_TERMS,
                }
            ),
        ),
    )
    for role, keywords in priority:
        if any(keyword in text for keyword in sorted(keywords, key=len, reverse=True)):
            return role
    if text.endswith("관계") and "인과관계" not in text:
        return CONCURRENCE
    return classify_title(title)


def _top_section(card: Card) -> str:
    tops = {path.split(".", 1)[0] for path in card.source_section_paths}
    if len(tops) != 1:
        raise IssueCatalogError(f"{card.id}: source refs span top sections {sorted(tops)}")
    return next(iter(tops))


@lru_cache(maxsize=1)
def _article_metadata() -> Mapping[str, tuple[str, str]]:
    payload = json.loads(_ARTICLE_CATALOG.read_text(encoding="utf-8"))
    return {
        item["key"]: (item["label"], item["offense"])
        for item in payload["articles"]
    }


@lru_cache(maxsize=1)
def _title_overrides() -> Mapping[tuple[str, str, str], str]:
    payload = json.loads(_ISSUE_TITLE_REVIEW.read_text(encoding="utf-8"))
    result: dict[tuple[str, str, str], str] = {}
    for item in payload.get("decisions", []):
        key = (item["article"], item["section_path"], item["function"])
        if key in result:
            raise IssueCatalogError(f"duplicate issue title review decision: {key}")
        if item["function"] not in ISSUE_FUNCTIONS or not item.get("title"):
            raise IssueCatalogError(f"invalid issue title review decision: {item}")
        result[key] = item["title"]
    return result


@lru_cache(maxsize=1)
def _runtime_overrides() -> Mapping[str, str]:
    payload = json.loads(_ISSUE_RUNTIME_REVIEW.read_text(encoding="utf-8"))
    result: dict[str, str] = {}
    for item in payload.get("decisions", []):
        issue_id = item["issue_id"]
        runtime = item["runtime"]
        if issue_id in result:
            raise IssueCatalogError(f"duplicate issue runtime review decision: {issue_id}")
        if runtime not in ISSUE_RUNTIMES:
            raise IssueCatalogError(f"invalid reviewed issue runtime: {item}")
        result[issue_id] = runtime
    return result


@lru_cache(maxsize=1)
def _section_titles() -> Mapping[tuple[str, str], str]:
    """Map ``(제NNN조, section_path)`` to the criminal-commentary heading.

    Article numbers overlap with the Criminal Procedure Act, so ``law_id=001692`` is
    part of the join rather than trusting ``article_no`` alone.
    """
    values: dict[tuple[str, str], Counter[str]] = defaultdict(Counter)
    for path in (COMMENTARY_CHUNKS, COMMENTARY_SUPPLEMENT):
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            section_path = row.get("section_path", "")
            if row.get("law_id") != "001692" or not section_path:
                continue
            title = row.get("section_title", "")
            if title:
                values[(row.get("article_no", ""), section_path)][title] += 1
    return {
        key: sorted(counts, key=lambda title: (-counts[title], title))[0]
        for key, counts in values.items()
    }


def _issue_section(
    card: Card,
    *,
    article_label: str,
    section_titles: Mapping[tuple[str, str], str],
    reviewed_sections: frozenset[tuple[str, str]],
) -> str:
    """Use a reviewed top heading when present, otherwise the deepest known leaf.

    Some commentary exports omit the Roman-numeral heading row but retain ``Ⅳ.1 기망``,
    ``Ⅳ.2 착오``, and so on.  Collapsing those leaves back to ``Ⅳ`` merges distinct
    constituent elements.  A card still receives one deterministic parent when a source
    proposition spans adjacent leaves; its other source paths remain preserved on Card.
    """
    top = _top_section(card)
    if (card.article, top) in reviewed_sections:
        return top
    top_title = strip_outline_numbering(
        section_titles.get((article_label, top), "")
    )
    is_container = top_title.endswith("죄") or top_title in _CONTAINER_HEADINGS
    if top_title and not is_container:
        return top
    known = sorted(
        {
            path
            for path in card.source_section_paths
            if section_titles.get((article_label, path))
        },
        key=lambda path: (-path.count("."), path),
    )
    return known[0] if known else top


def _fallback_title(cards: Sequence[Card]) -> str:
    titles = commentary_section_titles()
    counts: Counter[str] = Counter()
    for card in cards:
        for comment_id in card.source_comment_ids:
            title = strip_outline_numbering(titles.get(comment_id, ""))
            if title:
                counts[title] += 1
    if not counts:
        return "미분류 쟁점"
    ranked = sorted(counts, key=lambda title: (-counts[title], title))
    return " / ".join(ranked[:3])


def _base_function(role: str) -> str:
    if role in {CORE, PRESUMED}:
        return ELEMENT_ISSUE
    if role == DEFEATER:
        return GUARD_ISSUE
    if role == STAGE:
        return STAGE_ISSUE
    if role == CONCURRENCE:
        return CONCURRENCE_ISSUE
    if role == PARTICIPATION:
        return PARTICIPATION_ISSUE
    return SUPPORT_ISSUE


def _runtime(function: str) -> str:
    if function == ELEMENT_ISSUE:
        return ASSESS_ISSUE
    if function == GUARD_ISSUE:
        return RETRIEVE_GUARD
    if function in {STAGE_ISSUE, CONCURRENCE_ISSUE, PARTICIPATION_ISSUE}:
        return RELATION_CONDITION
    return RETRIEVE_SUPPORT


def _anchor_score(card: Card, *, top: str, function: str) -> int:
    if classify_card_form(card) == PRECEDENT_PATTERN:
        return -10_000
    if function == ELEMENT_ISSUE and (
        card.polarity == "exception" or card.norm_kind == "exception"
    ):
        return -1_000

    score = {
        "definition": 60,
        "element": 45,
        "causal_link": 30,
        "standard": 15,
        "variant": 10,
        "exception": 0,
    }.get(card.norm_kind, 0)
    if any(path == top for path in card.source_section_paths):
        score += 35
    if card.formalization == "deterministic_rule":
        score += 15
    if card.doctrinal_status == "settled":
        score += 10
    if classify_card_form(card) == PRECEDENT_RULE:
        score += 10
    if _ANCHOR_LANGUAGE_RE.search(card.proposition):
        score += 12
    if card.polarity == "positive":
        score += 5
    if function == GUARD_ISSUE and (
        "성립하지" in card.proposition or "조각" in card.proposition
    ):
        score += 25
    if function == GUARD_ISSUE and card.norm_kind == "exception":
        score += 50
    if _CANONICAL_DEFINITION_RE.search(card.proposition):
        score += 25
    return score


def _select_anchors(
    cards: Sequence[Card], *, top: str, function: str
) -> tuple[str, ...]:
    if function in {ELEMENT_ISSUE, GUARD_ISSUE}:
        limit = 4
    elif function == STAGE_ISSUE:
        limit = 2
    else:
        limit = 1
    if function == SUPPORT_ISSUE:
        return ()
    if function not in {ELEMENT_ISSUE, GUARD_ISSUE}:
        ranked = sorted(
            cards,
            key=lambda card: (-_anchor_score(card, top=top, function=function), card.id),
        )
        return tuple(
            card.id
            for card in ranked
            if _anchor_score(card, top=top, function=function) >= 0
        )[:limit]
    by_slot: dict[str, list[Card]] = defaultdict(list)
    for card in cards:
        by_slot[card.slot].append(card)
    winners = [
        sorted(
            slot_cards,
            key=lambda card: (
                -_anchor_score(card, top=top, function=function),
                card.id,
            ),
        )[0]
        for slot_cards in by_slot.values()
    ]
    ranked = sorted(
        winners,
        key=lambda card: (-_anchor_score(card, top=top, function=function), card.id),
    )
    return tuple(
        card.id
        for card in ranked
        if _anchor_score(card, top=top, function=function) >= 0
    )[:limit]


def compile_issue_catalog_v2(
    corpus: CardCorpus | None = None,
) -> tuple[tuple[IssuePacket, ...], tuple[CardPlacement, ...]]:
    corpus = corpus or card_corpus()
    roles = {item.card_id: item for item in resolve_card_roles(corpus)}
    leaf_catalog = {item.card_id: item for item in compile_card_catalog_v2(corpus)}
    metadata = _article_metadata()
    section_titles = _section_titles()
    title_overrides = _title_overrides()
    runtime_overrides = _runtime_overrides()
    reviewed_sections = frozenset(
        (article, section) for article, section, _ in title_overrides
    )

    by_article_section: dict[tuple[str, str], list[Card]] = defaultdict(list)
    for card in corpus.cards:
        article_label, _ = metadata[card.article]
        section = _issue_section(
            card,
            article_label=article_label,
            section_titles=section_titles,
            reviewed_sections=reviewed_sections,
        )
        by_article_section[(card.article, section)].append(card)

    grouped: dict[tuple[str, str, str], list[Card]] = defaultdict(list)
    group_reasons: dict[tuple[str, str, str], set[str]] = defaultdict(set)
    for (article, section), section_cards in by_article_section.items():
        article_label, _ = metadata[article]
        exact_title = section_titles.get((article_label, section), "")
        exact_role = _classify_issue_title(exact_title) if exact_title else UNCLASSIFIED
        has_element_role = any(
            roles[card.id].role in {CORE, PRESUMED} for card in section_cards
        )
        context_slots_with_definitions = {
            card.slot
            for card in section_cards
            if roles[card.id].role == CONTEXT
            and card.norm_kind in {"definition", "element", "causal_link"}
        }

        for card in section_cards:
            function = _base_function(roles[card.id].role)
            if exact_role == CONTEXT and function == ELEMENT_ISSUE:
                # Slot ids occasionally merge cards from adjacent commentary chapters.
                # The card's own section_path and exact heading take precedence.
                function = SUPPORT_ISSUE
            elif function == SUPPORT_ISSUE and exact_role in {CORE, PRESUMED}:
                function = ELEMENT_ISSUE
            elif (
                function in {ELEMENT_ISSUE, SUPPORT_ISSUE}
                and exact_role in {DEFEATER, STAGE, CONCURRENCE, PARTICIPATION}
            ):
                function = _base_function(exact_role)
            # With no heading at any depth, a definition may still be an element.  Keep
            # the conservative fallback reviewable rather than silently discarding it.
            elif (
                function == SUPPORT_ISSUE
                and not exact_title
                and section != "Ⅰ"
                and (
                    has_element_role
                    or card.slot in context_slots_with_definitions
                )
            ):
                function = ELEMENT_ISSUE
                group_reasons[(article, section, function)].add(
                    "context leaf promoted because the top heading is missing and the card defines an element"
                )
            grouped[(article, section, function)].append(card)

    issues: list[IssuePacket] = []
    placements: list[CardPlacement] = []
    for (article, top, function), members in sorted(grouped.items()):
        article_label, offense = metadata[article]
        exact_title = section_titles.get((article_label, top), "")
        title_override = title_overrides.get((article, top, function), "")
        title = (
            strip_outline_numbering(exact_title)
            if exact_title
            else title_override or _fallback_title(members)
        )
        issue_id = f"{article}.{top}.{function}"
        anchors = _select_anchors(members, top=top, function=function)
        member_ids = tuple(sorted(card.id for card in members))
        case_pattern_ids = tuple(
            sorted(
                card.id
                for card in members
                if leaf_catalog[card.id].form == PRECEDENT_PATTERN
            )
        )
        retrieval_ids = tuple(
            sorted(
                card.id
                for card in members
                if card.id not in anchors and card.is_standard_input
            )
        )
        reasons = set(group_reasons[(article, top, function)])
        if title_override:
            reasons.discard(
                "context leaf promoted because the top heading is missing and the card defines an element"
            )
        elif not exact_title:
            reasons.add("top-level commentary heading is missing; title is synthesized from leaf headings")
        if function != SUPPORT_ISSUE and not anchors:
            reasons.add("runtime issue has no non-precedent anchor rule")
        runtime = _runtime(function)
        if function == ELEMENT_ISSUE and not anchors:
            # Do not turn a precedent fact pattern into a universal core rule merely
            # to make the issue runnable.  Keep it retrievable and require review.
            runtime = RETRIEVE_SUPPORT
        runtime = runtime_overrides.get(issue_id, runtime)

        issue = IssuePacket(
            issue_id=issue_id,
            article=article,
            article_label=article_label,
            offense=offense,
            section_path=top,
            title=title,
            function=function,
            runtime=runtime,
            slot_ids=tuple(sorted({card.slot for card in members})),
            anchor_card_ids=anchors,
            member_card_ids=member_ids,
            retrieval_card_ids=retrieval_ids,
            case_pattern_card_ids=case_pattern_ids,
            review_required=bool(reasons),
            review_reasons=tuple(sorted(reasons)),
        )
        issues.append(issue)

        for card in members:
            if card.id in anchors:
                policy = ANCHOR_CONTEXT
            elif card.is_standard_input:
                policy = RETRIEVE_CANDIDATE
            elif function == SUPPORT_ISSUE:
                policy = SUPPORT_ONLY
            else:
                policy = SYMBOLIC_ONLY
            placements.append(
                CardPlacement(
                    card_id=card.id,
                    issue_id=issue_id,
                    load_policy=policy,
                    case_pattern=card.id in case_pattern_ids,
                )
            )

    issues_tuple = tuple(issues)
    placements_tuple = tuple(sorted(placements, key=lambda item: item.card_id))
    unknown_runtime_reviews = set(runtime_overrides) - {
        issue.issue_id for issue in issues_tuple
    }
    if unknown_runtime_reviews:
        raise IssueCatalogError(
            f"runtime review refers to unknown issues: {sorted(unknown_runtime_reviews)}"
        )
    validate_issue_catalog_v2(
        issues_tuple, placements_tuple, expected_ids={card.id for card in corpus.cards}
    )
    return issues_tuple, placements_tuple


def validate_issue_catalog_v2(
    issues: Sequence[IssuePacket],
    placements: Sequence[CardPlacement],
    *,
    expected_ids: Iterable[str],
) -> None:
    errors: list[str] = []
    expected = set(expected_ids)
    issue_ids = [issue.issue_id for issue in issues]
    if len(issue_ids) != len(set(issue_ids)):
        errors.append("duplicate issue ids")
    known_issues = set(issue_ids)
    placed_ids = [placement.card_id for placement in placements]
    if len(placed_ids) != len(set(placed_ids)):
        errors.append("a card is placed in more than one issue")
    if set(placed_ids) != expected:
        errors.append(
            f"placement coverage differs: missing={sorted(expected - set(placed_ids))}, "
            f"extra={sorted(set(placed_ids) - expected)}"
        )
    for issue in issues:
        if issue.function not in ISSUE_FUNCTIONS:
            errors.append(f"{issue.issue_id}: invalid function {issue.function}")
        if issue.runtime not in ISSUE_RUNTIMES:
            errors.append(f"{issue.issue_id}: invalid runtime {issue.runtime}")
        if not set(issue.anchor_card_ids) <= set(issue.member_card_ids):
            errors.append(f"{issue.issue_id}: anchor outside member set")
        if not set(issue.retrieval_card_ids) <= set(issue.member_card_ids):
            errors.append(f"{issue.issue_id}: retrieval card outside member set")
        if issue.runtime == ASSESS_ISSUE and not issue.anchor_card_ids:
            errors.append(f"{issue.issue_id}: assessable issue lacks an anchor")
    for placement in placements:
        if placement.issue_id not in known_issues:
            errors.append(f"{placement.card_id}: unknown issue {placement.issue_id}")
        if placement.load_policy not in LOAD_POLICIES:
            errors.append(f"{placement.card_id}: invalid load policy {placement.load_policy}")
    if errors:
        raise IssueCatalogError("; ".join(errors))


def issue_catalog_summary(
    issues: Sequence[IssuePacket], placements: Sequence[CardPlacement]
) -> dict[str, object]:
    return {
        "issues": len(issues),
        "cards": len(placements),
        "by_function": dict(Counter(issue.function for issue in issues).most_common()),
        "by_runtime": dict(Counter(issue.runtime for issue in issues).most_common()),
        "by_load_policy": dict(
            Counter(item.load_policy for item in placements).most_common()
        ),
        "anchors": sum(len(issue.anchor_card_ids) for issue in issues),
        "retrieval_candidates": sum(len(issue.retrieval_card_ids) for issue in issues),
        "case_patterns": sum(len(issue.case_pattern_card_ids) for issue in issues),
        "review_required": sum(issue.review_required for issue in issues),
        "articles": len({issue.article for issue in issues}),
    }


def issue_catalog_payload(
    issues: Sequence[IssuePacket], placements: Sequence[CardPlacement]
) -> dict[str, object]:
    return {
        "version": ISSUE_CATALOG_VERSION,
        "source": "live RuleIR cards grouped by reviewed commentary section_path",
        "summary": issue_catalog_summary(issues, placements),
        "issues": [issue.as_dict() for issue in issues],
        "card_placements": [placement.as_dict() for placement in placements],
    }
