"""Compile the reviewed cards into one Scallop program.

Three layers, and the layer a thing belongs to is the whole design:

*Facts* (:mod:`idpr.rulebase.facts`) are descriptive and come from call 1.
*Card statuses* come from call 2, one per open-textured card.
*The rulebase* is what this module emits: card metadata as **data tuples**, plus a fixed
set of inference rules.

Card ids are arguments, never relation names
--------------------------------------------
The previous rulebase made each card a relation and produced ``rel rule_art298_…`` 3,487
times, sharing 8 distinct bodies, 1,592 of which reduced to ``actor ∧ action_committed``.
Here 1,848 cards become roughly 7,400 tuples across 5 relations and add **no** predicate.
The rule count is fixed by the doctrine being modelled, not by the size of the corpus.

Why the offence gate does not require every element slot
-------------------------------------------------------
The obvious gate -- an offence is established when every one of its element slots is
affirmatively satisfied -- is unsound here, and measurably so. Element slots come from
commentary section headings, and a heading is not a conjunct: 제298조's ``sec3_1 폭행``,
``sec3_2 협박`` and ``sec3_3 추행`` are parts of *one* 행위 element, not three separate
requirements. Articles carry 4.5 element slots on average and up to 12 (제333조), so
requiring all of them would leave ``offense_established`` unreachable for every offence an
exam answer does not exhaustively brief -- which is all of them. The plan flagged this as
the way to silently disable the pipeline.

So the gate is: supported by at least one element card, and not blocked. Blocking is
positive -- an element card contradicted, an exception card satisfied, or a defeater
satisfied -- so an unaddressed element leaves the offence *supported*, never established
by silence and never killed by silence either. ``element_unaddressed`` is emitted as a
report so the IRAC step can see which elements went unargued, and so a stricter gate can
be measured later without recompiling.

What the symbolic layer therefore decides: 위법성·책임 조각, explicit refutation,
죄수 흡수, and contradiction detection. That is the ``conclusion`` + ``application``
share of the rubric, and it is stated rather than overclaimed.
"""

from __future__ import annotations

import re
from collections import Counter
from typing import Iterable, Mapping, Sequence

from idpr.rulebase.cards import CardCorpus, card_corpus
from idpr.rulebase.doctrine import load_doctrine
from idpr.rulebase.facts import scl_fact_layer
from idpr.rulebase.roles import CardRole, element_slots, resolve_card_roles
from idpr.rulebase.skeleton import CONCURRENCE, CORE, DEFEATER, PRESUMED, STAGE

#: Article keys whose statute label cannot be derived by rule. Only one exists, so it is
#: listed rather than guessed at from a sample of one.
IRREGULAR_ARTICLE_LABELS: Mapping[str, str] = {
    "art2582_2": "제258조의2",
}

_ARTICLE_RE = re.compile(r"^art(\d+)$")


class ArticleLabelError(ValueError):
    """Raised when an article key has no derivable statute label.

    Fatal by design: the IRAC step injects the statute number deterministically, and the
    rubric's article gate zeroes an item that fails to cite it. A silently missing label
    would cost points with no error anywhere.
    """


def article_label(article: str) -> str:
    """``art298`` -> ``제298조``."""
    if article in IRREGULAR_ARTICLE_LABELS:
        return IRREGULAR_ARTICLE_LABELS[article]
    match = _ARTICLE_RE.match(article)
    if match is None:
        raise ArticleLabelError(
            f"cannot derive a statute label for article key {article!r}; "
            f"add it to IRREGULAR_ARTICLE_LABELS"
        )
    return f"제{match.group(1)}조"


def _tuple_literal(values: Sequence[str]) -> str:
    quoted = ", ".join(f'"{value}"' for value in values)
    return f"({quoted})"


def _relation_block(name: str, rows: Iterable[Sequence[str]]) -> list[str]:
    """One bulk fact set. Rows are sorted so the output is byte-identical across runs."""
    literals = sorted(_tuple_literal(row) for row in rows)
    if not literals:
        return [f"// rel {name} — 비어 있음 (아직 채워지지 않았다)"]
    lines = [f"rel {name} = {{"]
    lines += [f"  {literal}," for literal in literals]
    lines.append("}")
    return lines


TYPE_DECLARATIONS = """\
// ── 규범층: 콜 2가 채운다 ─────────────────────────────────────
type card_status(String, String, String)  // case, cardId, satisfied|not_satisfied|unknown

// ── 룰베이스: 카드에서 컴파일된 데이터 튜플 ──────────────────
// 카드 id는 인자다. 관계 이름이 아니다.
type card_offense(String, String)         // cardId, offense (= 조문 키)
type card_slot(String, String)            // cardId, slot
type card_polarity(String, String)        // cardId, positive|negative|exception
type card_role(String, String)            // cardId, core|presumed|stage|defeater|...
type slot_offense(String, String)         // slot, offense
type element_slot(String, String)         // slot, core|presumed
type offense_article(String, String)      // offense, "제298조"

// ── 죄수·미수: 수기 작성 후 법리 검수 (data/rulebase/*.yaml) ──
type absorbed_by(String, String)          // child offense, parent offense
type imaginative_concurrence(String, String)
type attempt_punishable(String)           // offense
type preparation_punishable(String)       // offense"""

INFERENCE_RULES = """\
// 사건 하나를 근거지어 준다. 평가가 없는 사건에는 아무 결론도 없다.
rel assessed_case(c) = card_status(c, _, _)

// ── 요건의 지지·반증 ─────────────────────────────────────────
rel element_supported(c, off, s) = card_offense(cid, off), card_slot(cid, s),
    card_role(cid, "core"), card_polarity(cid, "positive"),
    card_status(c, cid, "satisfied")
rel element_supported(c, off, s) = card_offense(cid, off), card_slot(cid, s),
    card_role(cid, "presumed"), card_polarity(cid, "positive"),
    card_status(c, cid, "satisfied")

rel element_refuted(c, off, s) = card_offense(cid, off), card_slot(cid, s),
    card_role(cid, "core"), card_polarity(cid, "positive"),
    card_status(c, cid, "not_satisfied")
rel element_refuted(c, off, s) = card_offense(cid, off), card_slot(cid, s),
    card_role(cid, "presumed"), card_polarity(cid, "positive"),
    card_status(c, cid, "not_satisfied")

// negative polarity 카드는 "이런 경우에는 아니다"를 말한다. 충족되면 반증이다.
rel element_refuted(c, off, s) = card_offense(cid, off), card_slot(cid, s),
    card_role(cid, "core"), card_polarity(cid, "negative"),
    card_status(c, cid, "satisfied")

// 예외 카드가 충족되면 그 요건은 조각된다.
rel element_excluded(c, off, s) = card_offense(cid, off), card_slot(cid, s),
    card_polarity(cid, "exception"), card_status(c, cid, "satisfied")

// ── 위법성·책임 조각 ────────────────────────────────────────
rel offense_defeated(c, off) = card_offense(cid, off), card_role(cid, "defeater"),
    card_status(c, cid, "satisfied")

// ── 죄의 성립 ───────────────────────────────────────────────
rel offense_supported(c, off) = element_supported(c, off, _)
rel offense_blocked(c, off) = element_refuted(c, off, _)
rel offense_blocked(c, off) = element_excluded(c, off, _)
rel offense_blocked(c, off) = offense_defeated(c, off)

rel offense_established(c, off) = offense_supported(c, off), not offense_blocked(c, off)
// 삭제하지 않는다. 막힌 죄명도 콜 3에 그대로 넘겨 논증하게 한다.
rel offense_undetermined(c, off) = offense_supported(c, off), offense_blocked(c, off)

// ── 죄수 ────────────────────────────────────────────────────
rel is_absorbed(c, child) = offense_established(c, child),
    offense_established(c, parent), absorbed_by(child, parent)
rel final_offense(c, off) = offense_established(c, off), not is_absorbed(c, off)
rel concurrent_offenses(c, a, b) = offense_established(c, a), offense_established(c, b),
    imaginative_concurrence(a, b)

// ── 미수 ────────────────────────────────────────────────────
// 기수가 막힌 죄명에 미수 처벌 규정이 있으면 미수를 검토해야 한다. 스모크 케이스의
// 중지미수 논점이 이 경로다 — 강간 기수는 막혔고 제300조가 미수를 처벌한다.
rel attempt_to_consider(c, off) = offense_undetermined(c, off), attempt_punishable(off)

// ── 보고용 (게이트가 아니다) ────────────────────────────────
// 논증되지 않은 요건 슬롯. 이것으로 죄를 막지 않는다 — 시험 답안은 자명한 요건을
// 논하지 않으므로 막으면 어떤 죄도 성립하지 않는다.
rel element_unaddressed(c, off, s) = assessed_case(c), element_slot(s, _),
    slot_offense(s, off), not element_supported(c, off, s),
    not element_refuted(c, off, s)

// 콜 2가 한 카드에 두 상태를 준 경우. JSON 스키마가 막지만 값싼 방어다.
rel contradiction(c, "card_status_conflict") = card_status(c, cid, "satisfied"),
    card_status(c, cid, "not_satisfied")"""

#: Relations the host reads back. scli 0.2.4 prints only declared queries when run without
#: ``--query``, so an undeclared relation is silently invisible -- the defect that made the
#: previous rulebase's 3,487 rules contribute nothing.
QUERY_RELATIONS: tuple[str, ...] = (
    "element_supported",
    "element_refuted",
    "element_excluded",
    "element_unaddressed",
    "offense_defeated",
    "offense_established",
    "offense_undetermined",
    "is_absorbed",
    "final_offense",
    "concurrent_offenses",
    "attempt_to_consider",
    "contradiction",
)


def compile_rulebase(
    corpus: CardCorpus | None = None,
    roles: Sequence[CardRole] | None = None,
    absorbed_by: Sequence[tuple[str, str]] | None = None,
    imaginative_concurrence: Sequence[tuple[str, str]] | None = None,
    attempt_punishable: Sequence[str] | None = None,
    preparation_punishable: Sequence[str] | None = None,
) -> str:
    """Emit the whole Scallop program.

    The four doctrine tables default to the reviewed YAML on disk. Passing one explicitly
    replaces it, which is how a golden scenario isolates a single concurrence rule from the
    rest of the table.
    """
    corpus = corpus or card_corpus()
    roles = roles or resolve_card_roles(corpus)
    if None in (
        absorbed_by,
        imaginative_concurrence,
        attempt_punishable,
        preparation_punishable,
    ):
        tables = load_doctrine(corpus.by_article())
        if absorbed_by is None:
            absorbed_by = tables.absorbed_by
        if imaginative_concurrence is None:
            imaginative_concurrence = tables.imaginative_concurrence
        if attempt_punishable is None:
            attempt_punishable = tables.attempt_punishable
        if preparation_punishable is None:
            preparation_punishable = tables.preparation_punishable
    role_by_card = {role.card_id: role.role for role in roles}
    slots = element_slots(roles)

    articles = sorted(corpus.by_article())
    slot_to_article = {
        slot: cards[0].article for slot, cards in corpus.by_slot().items()
    }

    lines = [
        "// KCL 형법각칙 룰베이스 — 검수된 RuleIR 카드에서 결정론적으로 컴파일",
        "//",
        f"// 카드 {len(corpus.cards)}장 / 조문 {len(articles)}개 / 슬롯 "
        f"{len(slot_to_article)}개 / 요건 슬롯 {len(slots)}개",
        "// 카드는 데이터 튜플이다. 카드 수가 늘어도 술어는 늘지 않는다.",
        "",
        scl_fact_layer(),
        "",
        TYPE_DECLARATIONS,
        "",
        "// ── 카드 메타데이터 ─────────────────────────────────────────",
    ]

    lines += _relation_block(
        "card_offense", ((card.id, card.article) for card in corpus.cards)
    )
    lines.append("")
    lines += _relation_block(
        "card_slot", ((card.id, card.slot) for card in corpus.cards)
    )
    lines.append("")
    lines += _relation_block(
        "card_polarity", ((card.id, card.polarity) for card in corpus.cards)
    )
    lines.append("")
    lines += _relation_block(
        "card_role", ((card.id, role_by_card[card.id]) for card in corpus.cards)
    )
    lines.append("")
    lines += _relation_block("slot_offense", slot_to_article.items())
    lines.append("")
    lines += _relation_block("element_slot", slots.items())
    lines.append("")
    lines += _relation_block(
        "offense_article", ((article, article_label(article)) for article in articles)
    )
    lines.append("")
    lines.append("// ── 죄수론 (Phase 1e에서 검수 후 채워진다) ──────────────────")
    lines += _relation_block("absorbed_by", absorbed_by)
    lines.append("")
    lines += _relation_block("imaginative_concurrence", imaginative_concurrence)
    lines.append("")
    lines += _relation_block(
        "attempt_punishable", ((offence,) for offence in attempt_punishable)
    )
    lines.append("")
    lines += _relation_block(
        "preparation_punishable",
        ((offence,) for offence in preparation_punishable),
    )
    lines += ["", "// ── 추론 규칙 ───────────────────────────────────────────────", ""]
    lines.append(INFERENCE_RULES)
    lines += ["", "// ── 질의 선언 ───────────────────────────────────────────────"]
    lines += [f"query {relation}" for relation in QUERY_RELATIONS]
    return "\n".join(lines) + "\n"


def rulebase_stats(program: str, roles: Sequence[CardRole]) -> dict[str, object]:
    """Counts that make the inversion from the previous rulebase checkable."""
    return {
        "lines": program.count("\n"),
        "declared_types": program.count("\ntype "),
        "inference_rules": program.count("\nrel "),
        "queries": len(QUERY_RELATIONS),
        "card_tuples": sum(
            1 for line in program.splitlines() if line.startswith('  ("')
        ),
        "cards": len(roles),
        "roles": dict(Counter(role.role for role in roles).most_common()),
    }
