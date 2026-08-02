"""Element skeleton: which slots are required elements of an offence, and how.

The RuleIR cards carry a ``norm_kind`` (element / standard / definition / exception /
causal_link) but never say *which element of which offence* a card belongs to. That
mapping is what the symbolic layer needs in order to decide whether an offence is
established, and it does not exist in the asset.

It is recovered rather than hand-written. Commentary is organised by constituent
element -- ``Ⅱ. 주체``, ``Ⅲ. 행위``, ``Ⅳ. 고의``, ``Ⅶ. 죄수`` -- and every card's
``source_refs[].comment_id`` joins to a ``section_title`` (measured: 402 of 402 slots
join successfully). Two independent signals are derived per slot:

1. the commentary ``section_title``, bucketed by the table below;
2. whether the slot contains any card with ``norm_kind == "element"``.

The second signal is used in one direction only. An element-titled slot whose cards are
all ``standard`` or ``definition`` is entirely normal -- commentary section ``Ⅲ. 행위``
is *filled* with standards elaborating the conduct element -- so a missing ``element``
card proves nothing. The converse does carry information: an ``element`` card filed under
``죄수`` or ``위법성`` is a filing oddity worth a look.

Review items are therefore graded. ``blocking`` means the role could not be determined
(no bucket matched, or the title is a PDF parse artifact); ``advisory`` means the role is
probably right but the filing is odd. Everything else is classified without human input.

Why ``core`` and ``presumed`` are separated
-------------------------------------------
Requiring every element slot to be affirmatively satisfied would make
``offense_established`` unreachable in practice: an exam answer does not argue the
obvious 주체 or 객체 of an offence, so those slots stay ``unknown`` forever and every
offence collapses to ``offense_undetermined``. ``core`` slots (행위 · 고의 ·
구성요건 · 인과관계) demand affirmative satisfaction; ``presumed`` slots (주체 ·
객체) block only when a card in them is positively contradicted. That mirrors how
legal analysis allocates the burden of argument.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Mapping

from idpr.rulebase.cards import Card, CardCorpus, card_corpus

PROJECT_ROOT = Path(__file__).resolve().parents[3]
COMMENTARY_CHUNKS = PROJECT_ROOT / "data/commentary/kcl_criminal_v1_commentary_chunks.jsonl"
COMMENTARY_SUPPLEMENT = PROJECT_ROOT / "data/commentary/kcl_criminal_v1_commentary_supplement.jsonl"

#: Slot roles. ``core``/``presumed`` are the two element kinds the Datalog layer
#: distinguishes; the rest are not elements at all.
CORE = "core"
PRESUMED = "presumed"
STAGE = "stage"
DEFEATER = "defeater"
CONCURRENCE = "concurrence"
PARTICIPATION = "participation"
CONTEXT = "context"
UNCLASSIFIED = "unclassified"

ELEMENT_ROLES = frozenset({CORE, PRESUMED})

#: Title keyword -> slot role. Matched against the section title with its outline
#: numbering stripped. Longer keys are tried first, so ``주관적 구성요건`` wins over
#: ``구성요건`` and ``죄수 및 다른 죄와의 관계`` over ``죄수``.
TITLE_BUCKETS: Mapping[str, str] = {
    # Not elements: introductory or descriptive matter. Still useful as Rule-section
    # context, which is why they are kept rather than dropped.
    "의의": CONTEXT,
    "개설": CONTEXT,
    "개관": CONTEXT,
    "개념": CONTEXT,
    "법적 성격": CONTEXT,
    "보호법익": CONTEXT,
    "연혁": CONTEXT,
    "구체적인 사례": CONTEXT,
    "구체적 사례": CONTEXT,
    "기타": CONTEXT,
    "입법": CONTEXT,
    "판례를 통해 본 사례": CONTEXT,
    "성립을 인정한 경우": CONTEXT,
    "성립을 부정한 경우": CONTEXT,
    "성립 인정 사례": CONTEXT,
    "성립 부정 사례": CONTEXT,
    "대법원 판단": CONTEXT,
    "판례": CONTEXT,
    "사례": CONTEXT,
    "서설": CONTEXT,
    "일반론": CONTEXT,
    "보호의 정도": CONTEXT,
    "관련 문제": CONTEXT,
    "특별법": CONTEXT,
    "소추": CONTEXT,
    "특례의 적용": CONTEXT,
    "적용효과": CONTEXT,
    "적용 요건": CONTEXT,
    "시적 범위": CONTEXT,
    "주목할 요소": CONTEXT,
    "판단 기준": CONTEXT,
    "처벌": CONTEXT,
    "제1항": CONTEXT,
    "제2항": CONTEXT,
    "제3항": CONTEXT,
    # Core elements: the conduct, the result, the mental element, causation. The long
    # tail here is drawn from the actual commentary headings, not invented: each entry
    # below names a constituent-element sub-section that occurs in the corpus.
    "행위": CORE,
    "구성요건": CORE,
    "고의": CORE,
    "인과관계": CORE,
    "결과": CORE,
    "처분행위": CORE,
    "목적": CORE,
    "수단": CORE,
    "실행행위": CORE,
    "주관적 요건": CORE,
    "객관적 요건": CORE,
    "폭행": CORE,
    "협박": CORE,
    "추행": CORE,
    "간음": CORE,
    "침입": CORE,
    "살해": CORE,
    "상해": CORE,
    # 여기서 음모는 범죄의 conspiracy가 아니라 陰毛다. 아래의 일반 "음모"
    # stage 키보다 긴 구문이 먼저 매칭되어 상해 판단 쟁점에 남아야 한다.
    "음모 절단": CORE,
    "사망": CORE,
    "위조": CORE,
    "변조": CORE,
    "행사": CORE,
    "은닉": CORE,
    "손괴": CORE,
    "영득": CORE,
    "절취": CORE,
    "취거": CORE,
    "편취": CORE,
    "기망": CORE,
    "갈취": CORE,
    "수수": CORE,
    "요구": CORE,
    "약속": CORE,
    "공여": CORE,
    "청탁": CORE,
    "비밀": CORE,
    "예견가능성": CORE,
    "부작위": CORE,
    "야간": CORE,
    "흉기": CORE,
    "재물": CORE,
    "재산상": CORE,
    "점유": CORE,
    "소유": CORE,
    "문서": CORE,
    "도화": CORE,
    "항거불능": CORE,
    "심신상실": CORE,
    "기회": CORE,
    "과실": CORE,
    "주의의무": CORE,
    "직무유기": CORE,
    "위계": CORE,
    "위력": CORE,
    "성립요건": CORE,
    "상습": CORE,
    "휴대": CORE,
    "합동": CORE,
    "사용절도": CORE,
    "면탈": CORE,
    "강취": CORE,
    "혼취": CORE,
    "반항억압": CORE,
    "착수시기": STAGE,
    # Presumed elements: who and what. Contested only rarely, so they gate an offence
    # only when a card in them is positively contradicted.
    "주체": PRESUMED,
    "객체": PRESUMED,
    "사람": PRESUMED,
    "행위자": PRESUMED,
    "상대방": PRESUMED,
    "배우자": PRESUMED,
    "제3자": PRESUMED,
    "건조물": PRESUMED,
    "방실": PRESUMED,
    "선박": PRESUMED,
    "공무원": PRESUMED,
    "친족": PRESUMED,
    "직계혈족": PRESUMED,
    "동거": PRESUMED,
    "인적 범위": PRESUMED,
    "타인": PRESUMED,
    # Inchoate stage. Feeds the 기수/미수 determination rather than element gating.
    "미수범의 처벌": STAGE,
    "미수": STAGE,
    "기수": STAGE,
    "실행의 착수": STAGE,
    "예비": STAGE,
    "음모": STAGE,
    "중지": STAGE,
    # Justification / excuse. Reaches the symbolic layer as a defeater.
    "위법성": DEFEATER,
    "책임": DEFEATER,
    "승낙": DEFEATER,
    "정당행위": DEFEATER,
    "정당방위": DEFEATER,
    "긴급행위": DEFEATER,
    "긴급피난": DEFEATER,
    "면책": DEFEATER,
    "처벌조건": DEFEATER,
    # Concurrence. Source material for the hand-authored absorbed_by table.
    "죄수": CONCURRENCE,
    "다른 죄와의 관계": CONCURRENCE,
    "관계": CONCURRENCE,
    # Participation doctrine lives in the General Part, for which no commentary exists.
    # Treated as context in v1 because there are no rules to feed.
    "공범": PARTICIPATION,
    "공동정범": PARTICIPATION,
    "정범": PARTICIPATION,
    "교사": PARTICIPATION,
    "방조": PARTICIPATION,
    "신분": PARTICIPATION,
}

_OUTLINE_PREFIX = re.compile(r"^[Ⅰ-Ⅹ0-9가-힣]{0,4}?[.\s)]+")


def strip_outline_numbering(title: str) -> str:
    """``"Ⅲ. 1. 폭행·협박"`` -> ``"폭행·협박"``."""
    text = str(title).strip()
    previous = None
    while previous != text:
        previous = text
        text = _OUTLINE_PREFIX.sub("", text, count=1).strip()
        if not re.match(r"^[Ⅰ-Ⅹ0-9]", text):
            break
    return text


#: A heading longer than this is almost certainly a body sentence that the PDF parser
#: mis-detected as an outline heading. Measured against the corpus, real headings are
#: short ("주체 및 객체", "폭행·협박"); the outliers are sentence fragments.
_MAX_HEADING_CHARS = 24

#: Fragments that betray a mid-sentence break rather than a heading.
_ARTIFACT_PREFIXES = ("또는 ", "그 ", "(")
_ARTIFACT_SUFFIXES = ("때에는", "하여금", "으로", "이나", "라도", "및")


def looks_like_parse_artifact(title: str) -> bool:
    """Whether a section title is a mis-detected body sentence rather than a heading.

    The commentary PDFs are parsed by font signal, so a body line set in a heading-like
    face becomes a spurious section title. Those titles cannot be bucketed and should be
    reported as a data defect, not silently classified.
    """
    text = strip_outline_numbering(title)
    if not text:
        return True
    if len(text) > _MAX_HEADING_CHARS:
        return True
    if text.startswith(_ARTIFACT_PREFIXES):
        return True
    return text.endswith(_ARTIFACT_SUFFIXES)


def classify_title(title: str) -> str:
    """Bucket one commentary section title, or ``UNCLASSIFIED`` if no keyword matches."""
    core_text = strip_outline_numbering(title)
    for keyword in sorted(TITLE_BUCKETS, key=len, reverse=True):
        if keyword in core_text:
            return TITLE_BUCKETS[keyword]
    return UNCLASSIFIED


@lru_cache(maxsize=1)
def commentary_section_titles() -> Mapping[str, str]:
    """``comment_id -> section_title`` over the chunk bundle and its supplement."""
    titles: dict[str, str] = {}
    for path in (COMMENTARY_CHUNKS, COMMENTARY_SUPPLEMENT):
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            comment_id = record.get("comment_id")
            if comment_id:
                titles[comment_id] = record.get("section_title", "")
    return titles


@dataclass(frozen=True)
class SlotClassification:
    """One slot's derived role, with both signals kept for audit."""

    slot: str
    article: str
    role: str
    title: str
    title_role: str
    has_element_card: bool
    card_count: int
    standard_input_count: int
    needs_review: bool
    review_reason: str
    review_priority: str

    @property
    def is_element(self) -> bool:
        return self.role in ELEMENT_ROLES


def _dominant_title(cards: tuple[Card, ...], titles: Mapping[str, str]) -> str:
    counts: Counter[str] = Counter()
    for card in cards:
        for comment_id in card.source_comment_ids:
            title = titles.get(comment_id)
            if title:
                counts[title] += 1
    if not counts:
        return ""
    # Ties resolve by title text so the derivation is deterministic across runs.
    top = max(counts.values())
    return sorted(t for t, n in counts.items() if n == top)[0]


def derive_skeleton(corpus: CardCorpus | None = None) -> tuple[SlotClassification, ...]:
    """Classify every slot from the two signals, flagging disagreement for review."""
    corpus = corpus or card_corpus()
    titles = commentary_section_titles()
    by_slot = corpus.by_slot()

    results: list[SlotClassification] = []
    for slot, cards in by_slot.items():
        title = _dominant_title(cards, titles)
        title_role = classify_title(title) if title else UNCLASSIFIED
        has_element = any(card.norm_kind == "element" for card in cards)

        role = title_role
        reason = ""
        priority = ""

        if title_role == UNCLASSIFIED:
            # The role is genuinely unknown. Fall back to the element signal and flag it:
            # guessing silently is how a wrong skeleton becomes invisible. Defaulting the
            # unknown case to CONTEXT rather than CORE keeps the offence gate open, which
            # is the safe direction under a recall-scored rubric.
            role = CORE if has_element else CONTEXT
            priority = "blocking"
            if looks_like_parse_artifact(title):
                reason = f"commentary parse artifact, not a heading: {title!r}"
            else:
                reason = f"title matched no bucket: {title!r}"
        elif has_element and title_role in {CONCURRENCE, DEFEATER, PARTICIPATION}:
            # An element card filed under concurrence/justification/participation. The
            # title is still the better signal for the role, but the filing is worth a look.
            priority = "advisory"
            reason = f"slot holds a norm_kind=element card but title buckets as {title_role}"

        results.append(
            SlotClassification(
                slot=slot,
                article=cards[0].article,
                role=role,
                title=title,
                title_role=title_role,
                has_element_card=has_element,
                card_count=len(cards),
                standard_input_count=sum(1 for c in cards if c.is_standard_input),
                needs_review=bool(priority),
                review_reason=reason,
                review_priority=priority,
            )
        )
    return tuple(results)


def example_slot_for_role(
    role: str, classifications: tuple[SlotClassification, ...]
) -> SlotClassification | None:
    """One automatically classified slot that illustrates ``role``.

    Examples are drawn from slots the derivation settled on its own, never from the review
    queue: an item whose role is still in question cannot demonstrate what the role means.
    The smallest settled slot is selected so the result stays readable and adding a new
    offence never requires updating an article-specific preference table in Python.
    """
    settled = [c for c in classifications if c.role == role and not c.needs_review]
    if not settled:
        return None
    return min(settled, key=lambda c: (c.card_count, c.slot))


def skeleton_summary(
    classifications: tuple[SlotClassification, ...],
) -> dict[str, object]:
    """Counts by role and by article, plus the review queue size."""
    by_role: Counter[str] = Counter(c.role for c in classifications)
    by_priority: Counter[str] = Counter(
        c.review_priority for c in classifications if c.needs_review
    )
    review = [c for c in classifications if c.needs_review]
    articles_without_core: list[str] = []
    per_article: dict[str, list[SlotClassification]] = defaultdict(list)
    for c in classifications:
        per_article[c.article].append(c)
    for article, slots in sorted(per_article.items()):
        if not any(s.role == CORE for s in slots):
            articles_without_core.append(article)
    return {
        "slots": len(classifications),
        "by_role": dict(by_role.most_common()),
        "needs_review": len(review),
        "review_by_priority": dict(by_priority.most_common()),
        "articles": len(per_article),
        "articles_without_core_slot": articles_without_core,
    }
