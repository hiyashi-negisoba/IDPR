"""Where each card's content goes: to the model, or into the symbolic layer, and how.

The cards carry a two-valued ``formalization`` field (``standard_input`` /
``deterministic_rule``) which the plan read as "the model assesses this" vs "Datalog
computes this". Measuring the corpus shows the second value does not mean that, because
the Datalog *body* it presupposes does not exist anywhere in the asset:

- 412 cards are labelled ``deterministic_rule``, and not one of them carries a condition
  in any machine-readable form. The body would have to be authored from the Korean
  proposition, 412 times.
- Those 412 are not one kind of thing. Frame-matching them finds 죄의 정의 (57),
  요건 불요 메타명제 (37), 죄수 (22), 기수·미수 (20), 객체 범위 (34), and 152 that match
  no frame at all. Only some of these are card *statuses* even in principle.

The previous rulebase compiled all of them anyway and got 3,487 relations sharing 8
distinct bodies, 1,592 of which reduced to ``actor ∧ action_committed`` -- i.e. it emitted
a rule shaped object with the condition thrown away. A tautological rule is worse than no
rule: it decides an element affirmatively, silently, and unfalsifiably.

So this module routes cards by what their content can actually drive:

``model_assess``      call 2 decides the card's status, and that status feeds the offence
                      gate. The default.
``skeleton_meta``     "X는 필요하지 않다" -- an assertion about which slots are required.
                      Compiles into the element skeleton.
``stage_seed``        기수 timing / 미수 처벌. Compiles into the stage table.
``concurrence_seed``  죄수 relations. Names the offence pair in ``concurrence.yaml``, and
                      the card itself is the rule's *condition*.
``narrative``         a definition or restatement of the offence. Feeds the Rule paragraph.

The route is about what a card's content drives, not about whether call 2 sees it --
:attr:`CardRouting.assessed_by_model` is the separate question. 죄수 and 기수 cards are
assessed as well as tabulated, because their propositions are true of some cases and false
of others.

Cards therefore reach the symbolic layer at the skeleton / stage / concurrence level,
where the offence pair can be written down exactly, while the *condition* under which the
relation holds stays in the card where it was reviewed.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass
from typing import Mapping

from idpr.rulebase.cards import Card, CardCorpus, card_corpus

MODEL_ASSESS = "model_assess"
SKELETON_META = "skeleton_meta"
STAGE_SEED = "stage_seed"
CONCURRENCE_SEED = "concurrence_seed"
NARRATIVE = "narrative"

ROUTES = (MODEL_ASSESS, SKELETON_META, STAGE_SEED, CONCURRENCE_SEED, NARRATIVE)

#: Phrases that make a proposition undecidable by any symbolic procedure, grouped by the
#: kind of openness they signal.
#:
#: Measured against the corpus: these appear in 521 of 1,436 ``standard_input`` cards and
#: in 13 of 412 ``deterministic_rule`` cards. The asymmetry is the point -- a marker is
#: near-conclusive evidence of open texture, while its *absence* proves nothing, exactly
#: as with the element-card signal in :mod:`idpr.rulebase.skeleton`. The 13 are read as
#: mislabelled cards rather than as detector errors, and are reported as such: the
#: markers were chosen for what they mean, not tuned to agree with a field whose
#: reliability is the thing under examination.
OPEN_TEXTURE_MARKERS: Mapping[str, tuple[str, ...]] = {
    "종합판단": ("종합하여", "종합적으로", "제반 사정", "여러 사정", "고려하여", "참작"),
    "규범적 척도": (
        "사회통념", "통념상", "신의칙", "신의성실", "사회상규", "상당한", "상당성",
        "현저", "정도이", "정도에 이르", "정도의", "할 정도", "정도로",
    ),
    "가능·개연": ("가능성", "개연성", "우려", "염려", "위험성"),
    # "…이면 족하다 / 충분하다" is deliberately absent. It reads as an open-texture
    # hedge but in this corpus it almost always closes a 요건 완화 clause -- "법률행위의
    # 중요부분에 관한 것일 필요 없이 … 기망이면 충분하다" asserts that a requirement is
    # *not* imposed. It was measured as the two weakest markers in the table (P(SI) 0.71
    # and 0.81) and inspection showed why, so it is handled by ``skeleton_meta`` instead.
    "평가적 결론": (
        "보기 어렵", "인정하기 어렵", "어렵다", "여지가 있",
        "인정될 수 있", "인정할 수 있", "볼 수 있", "해당할 수 있", "평가할 수 있",
    ),
    "사안의존": (
        "사안에서", "구체적·개별적", "경위", "정황", "특별한 사정", "실질적으로",
    ),
    "판례보고": ("판시가 소개", "판례가", "판례의 태도", "대법원 판단", "라는 대법원"),
    "정도적 주관": ("미필적", "암묵적", "묵시적"),
}

_ALL_MARKERS: tuple[str, ...] = tuple(
    marker for markers in OPEN_TEXTURE_MARKERS.values() for marker in markers
)

#: Route frames, tried in this order. Earlier entries win, because a proposition that
#: speaks to both 기수 and 죄수 ("기수 후 …별도로 …성립하지 않는다") is a 죄수 rule.
_ROUTE_FRAMES: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        CONCURRENCE_SEED,
        re.compile(
            r"상상적 경합|실체적 경합|경합범|포괄일죄|일죄가 된다|일죄로|흡수|법조경합"
            r"|별도로.{0,20}성립하지 않는다|별개의 죄|다른 죄와의 관계"
        ),
    ),
    (
        STAGE_SEED,
        re.compile(
            r"기수에 이른다|기수가 된다|기수시기|기수로 된다|미수범은 처벌|미수가 된다"
            r"|미수에 그친|실행의 착수|착수시기|예비 단계|음모"
        ),
    ),
    (
        SKELETON_META,
        re.compile(
            r"필요하지 않다|필요는 없다|필요는 없고|필요 없이|필요가 없|필요하지 않으며"
            r"|요구되지 않는|요구하지 않는|요하지 않는|요하지 않고|묻지 않는|묻지 않고"
            r"|영향이 없다|영향을 미치지 않는|불문한다|불요하다|제한이 없"
        ),
    ),
    (
        NARRATIVE,
        re.compile(r"범죄이다|범죄를 말한다|라 한다|말한다|뜻한다|이라고 한다"),
    ),
)


@dataclass(frozen=True)
class CardRouting:
    """Where one card's content goes, with both signals kept for audit."""

    card_id: str
    article: str
    slot: str
    norm_kind: str
    corpus_formalization: str
    route: str
    open_texture_markers: tuple[str, ...]
    frames_matched: tuple[str, ...]

    @property
    def is_open_textured(self) -> bool:
        return bool(self.open_texture_markers)

    @property
    def assessed_by_model(self) -> bool:
        """Whether call 2 is asked for this card's status.

        The route says what a card's content *drives*; it does not say whether the card
        has a case-specific truth value. 죄수 and 기수 cards do -- "위법사실을 적극
        은폐할 목적으로 …한 경우에는 직무유기죄가 별도로 성립하지 않는다" is true of some
        cases and false of others, and that is precisely the condition its concurrence rule
        fires on. So they are assessed *and* feed a doctrine table.

        ``narrative`` and ``skeleton_meta`` are not: a definition and a statement that an
        element is not required are both true of every case, so asking would spend tokens
        to be told 'yes'.
        """
        return self.route in {MODEL_ASSESS, CONCURRENCE_SEED, STAGE_SEED}

    @property
    def contradicts_corpus_label(self) -> bool:
        """The corpus calls this card symbolically decidable, and the routing disagrees.

        Only counted when the disagreement is *operational* -- the card is sent to the
        model because its proposition asks for a judgment of degree. A card carrying a
        marker inside a 요건 불요 clause still reaches the symbolic layer through
        ``skeleton_meta``, so it is not a disagreement about where the card goes.
        """
        return (
            self.corpus_formalization == "deterministic_rule"
            and self.route == MODEL_ASSESS
            and self.is_open_textured
        )


def open_texture_markers(proposition: str) -> tuple[str, ...]:
    """Every open-texture marker present, in table order."""
    return tuple(marker for marker in _ALL_MARKERS if marker in proposition)


def matched_frames(proposition: str) -> tuple[str, ...]:
    return tuple(route for route, pattern in _ROUTE_FRAMES if pattern.search(proposition))


def route_card(card: Card) -> CardRouting:
    """Decide where one card's content goes.

    Open texture beats every frame but one: a 죄수 proposition that turns on whether two
    acts count as one act 사회통념상 is still a judgment, and a judgment cannot be
    tabulated.

    ``skeleton_meta`` is the exception, and it must be, because its marker sits *inside*
    the negation. "손해 발생 우려는 요구하지 않는다" contains 우려 while asserting that
    the very thing 우려 names is not an element. Reading the marker there would send a
    requirement-structure statement to the model to be assessed as though it were a
    standard.
    """
    markers = open_texture_markers(card.proposition)
    frames = matched_frames(card.proposition)
    if SKELETON_META in frames:
        route = SKELETON_META
    elif markers or not frames:
        route = MODEL_ASSESS
    else:
        route = frames[0]
    return CardRouting(
        card_id=card.id,
        article=card.article,
        slot=card.slot,
        norm_kind=card.norm_kind,
        corpus_formalization=card.formalization,
        route=route,
        open_texture_markers=markers,
        frames_matched=frames,
    )


def route_corpus(corpus: CardCorpus | None = None) -> tuple[CardRouting, ...]:
    corpus = corpus or card_corpus()
    return tuple(route_card(card) for card in corpus.cards)


def routing_summary(routings: tuple[CardRouting, ...]) -> dict[str, object]:
    """Counts by route, plus the two disagreement measures worth reporting."""
    by_route: Counter[str] = Counter(r.route for r in routings)
    open_by_label: Counter[str] = Counter(
        r.corpus_formalization for r in routings if r.is_open_textured
    )
    label_counts: Counter[str] = Counter(r.corpus_formalization for r in routings)
    seeds = [r for r in routings if r.route in {STAGE_SEED, CONCURRENCE_SEED, SKELETON_META}]
    return {
        "cards": len(routings),
        "by_route": dict(by_route.most_common()),
        "by_corpus_formalization": dict(label_counts.most_common()),
        "open_textured": sum(1 for r in routings if r.is_open_textured),
        "open_textured_by_corpus_label": dict(open_by_label.most_common()),
        "contradicting_cards": sum(1 for r in routings if r.contradicts_corpus_label),
        "symbolic_seed_cards": len(seeds),
        "symbolic_seed_articles": len({r.article for r in seeds}),
    }
