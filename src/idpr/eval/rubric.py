"""KCL rubric grading harness — §8.1 legal-quality axis (LLM-as-judge).

Ports the *settled* judge design from the sibling project sp_qwen
(``src/eval/kcl/judge.py``, ``gold.py``; user-confirmed 2026-06-21) into the
IDPR evaluation layer, adapted to IDPR conventions:

  - Judge protocol: **one call per question** — a method's long-form answer plus
    that question's full rubric → per-item O/P/X with a verbatim answer quote.
    ``P`` (partial credit, weight 0.5) is an IDPR extension past sp_qwen's
    strictly binary O/X design (user-confirmed 2026-08-06): a rubric item whose
    doctrine is stated correctly but whose application is incomplete, or where
    only some of several required elements are covered.
  - Hallucination block: an O or P is only accepted when the judge cites answer
    text that *actually exists* in the answer (fake O/P → downgraded to X).
  - Article gate: an article-number requirement is enforced only when the rubric
    item asks for citing a specific article; substantive-reasoning items accept
    semantically equivalent phrasing.
  - Normalization: satisfied-weight rubric items / total (0..1 per question,
    where a P item contributes 0.5), the 변시 checklist convention. Split by
    rubric-item type for §8.1 sub-metrics (issue-spotting recall, rule
    statement, application, conclusion).

This module ships the **pure, decision-independent core** only: rubric loading,
item typing, verdict safeguards, and scoring. The concrete model-calling judge
and its active prompt are gated on user approval (prompt-approval gate); until
then :class:`DeferredJudge` refuses to run so no accidental self-judging occurs.
The answer scored is a method's rendered long-form markdown
(``{method_id}_answer.md`` from the matrix). Applies to every method M1..M6.
"""

from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping, Protocol, Sequence

# --------------------------------------------------------------------------- #
# Rubric loading (join IDPR inventory → source parquet). Ports gold.py.
# --------------------------------------------------------------------------- #
_PAREN_SUFFIX = re.compile(r"\((?:전합|전원합의체)\)")


def normalize_case_no(key: str) -> str:
    """KCL ``supporting_precedents`` key → bare case number (ports gold.py)."""
    k = key.strip().lstrip("[").rstrip("]").replace("대법원", "").strip()
    return _PAREN_SUFFIX.sub("", k).strip()


def _gold_case_nos(supporting_precedents: Any) -> list[str]:
    """``list['{"[case_no]": "body"}']`` → ordered unique normalized case numbers."""
    out: list[str] = []
    seen: set[str] = set()
    items = list(supporting_precedents) if supporting_precedents is not None else []
    for raw in items:
        try:
            payload = json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            continue
        for raw_key in payload:
            case_no = normalize_case_no(raw_key)
            if case_no and case_no not in seen:
                seen.add(case_no)
                out.append(case_no)
    return out


@dataclass(frozen=True)
class RubricSet:
    """One KCL sub-question's full grading rubric."""

    sub_question_id: str
    question: str
    rubrics: tuple[str, ...]
    item_types: tuple[str, ...]
    score: int | None = None
    gold_case_nos: tuple[str, ...] = ()

    def __len__(self) -> int:
        return len(self.rubrics)


def load_rubric_sets(
    inventory_path: Path | str,
    *,
    parquet_path: Path | str | None = None,
) -> dict[str, RubricSet]:
    """Load full rubrics keyed by ``sub_question_id``.

    The IDPR inventory (``kcl_criminal_v1_draft.jsonl``) stores only a rubric
    *summary*; the full rubric lives in the source parquet each record points to
    (``source.parquet_path`` / ``source.source_row_index``). ``parquet_path``
    overrides the path recorded in the inventory.
    """
    import pandas as pd

    records = [
        json.loads(line)
        for line in Path(inventory_path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    frames: dict[str, "pd.DataFrame"] = {}
    sets: dict[str, RubricSet] = {}
    for record in records:
        source = record.get("source", {})
        path = str(parquet_path) if parquet_path is not None else source.get("parquet_path", "")
        if not path:
            continue
        if path not in frames:
            frames[path] = pd.read_parquet(path)
        row = frames[path].iloc[int(source["source_row_index"])]
        rubrics = tuple(str(r) for r in list(row["rubrics"] if row["rubrics"] is not None else []))
        sets[record["sub_question_id"]] = RubricSet(
            sub_question_id=record["sub_question_id"],
            question=str(row["question"]),
            rubrics=rubrics,
            item_types=tuple(classify_rubric_item(r) for r in rubrics),
            score=int(row["score"]) if "score" in frames[path].columns else None,
            gold_case_nos=tuple(_gold_case_nos(row.get("supporting_precedents"))),
        )
    return sets


def resolve_rubric_set(
    report_case: Mapping[str, Any], rubric_sets: Mapping[str, RubricSet]
) -> RubricSet | None:
    """Find the rubric set for a matrix report's ``case`` block by its
    ``source_sub_question_id`` (exact match; the 61 inventory ids are unique)."""
    sid = report_case.get("source_sub_question_id") or report_case.get("source_record_id")
    return rubric_sets.get(sid) if sid else None


# --------------------------------------------------------------------------- #
# Rubric item typing → §8.1 sub-metrics.
# --------------------------------------------------------------------------- #
RUBRIC_TYPES: tuple[str, ...] = ("issue", "rule", "application", "conclusion", "other")

# Heuristic typing. The dataset does not label item types — this is an imposed
# split for the §8.1 sub-metrics and is calibratable. "Spotting" phrasing (does
# the answer *raise/discuss* the issue) is checked first so it wins over the bare
# outcome keyword (죄책/성립) that such items also contain; a declarative outcome
# assertion is a conclusion; citing/stating a rule or precedent is rule; applying
# to the facts is application.
_ISSUE = re.compile(
    r"쟁점|성부를?\s*(?:논|검토)|성부와\s*관련|여부를?\s*(?:논|검토|문제)"
    r"|문제(?:점|가\s*되는지)|논하고\s*있는지|검토하며|언급하고\s*있는지"
)
_RULE = re.compile(
    r"판례|법리|요건|성립요건|정의|설명하는지|인용하여|인용하고\s*있는지|조를?\s*인용"
)
_APPLICATION = re.compile(r"사안에서|사안의|적용하는지|해당한다고|포섭|인정되는지")
_CONCLUSION = re.compile(r"^\s*따라서|성립한다\b|성립하지\s*(?:아니|않)|불성립|무죄|유죄")


def classify_rubric_item(text: str) -> str:
    """Coarse IRAC type of a rubric checkpoint. Spotting phrasing wins first, then
    conclusion (declarative outcome), then application, then rule; else ``other``."""
    s = str(text)
    if _ISSUE.search(s):
        return "issue"
    if _CONCLUSION.search(s):
        return "conclusion"
    if _APPLICATION.search(s):
        return "application"
    if _RULE.search(s):
        return "rule"
    return "other"


# --------------------------------------------------------------------------- #
# Verdict safeguards (ports judge.py). Applied to already-parsed verdict triples
# so they work for both structured-JSON and free-text judge output.
# --------------------------------------------------------------------------- #
_KEEP = re.compile(r"[^가-힣0-9a-zA-Z]")
_P_ART_NUM = re.compile(r"제\s*(\d+)\s*조(?:\s*의\s*(\d+))?")
_MUST_CITE_ART = re.compile(r"(조문|조항|법조|법문|규정|명시|언급|적시|제시|인용|검토)")


def _norm_ws(s: str) -> str:
    return _KEEP.sub("", str(s))


def quote_in_answer(quote: str, answer_norm: str, *, min_chars: int = 14) -> bool:
    """Whether the judge's cited evidence actually occurs in the answer
    (hallucination block). Markdown/punctuation ignored; prefix match."""
    q = _norm_ws(quote)
    if len(q) < min_chars:
        return False
    return q[:22] in answer_norm


def _answer_articles(answer: str) -> tuple[set[tuple[str, str | None]], set[str]]:
    pairs = {(m.group(1), m.group(2)) for m in _P_ART_NUM.finditer(answer)}
    return pairs, {jo for jo, _ in pairs}


_VERDICT_WEIGHTS = {"O": 1.0, "P": 0.5, "X": 0.0}


@dataclass(frozen=True)
class Verdict:
    """A judge's per-item ruling before safeguards: index is 1-based."""

    index: int
    verdict: str  # "O" (met) / "P" (partially_met, weight 0.5) / "X" (not_met)
    quote: str = ""


def apply_safeguards(
    verdicts: Sequence[Verdict], *, answer: str, rubrics: Sequence[str]
) -> list[float]:
    """Turn raw judge verdicts into a 0/0.5/1 list of length ``len(rubrics)``.

    (a) An O or P survives only if its quote really exists in the answer.
    (b) Article gate: when a rubric item demands a *specific article*, an O or P
        is void unless the answer actually cites that article (with branch
        number). Missing verdicts default to 0. Ports ``parse_verdicts`` from
        judge.py, extended with the ``P`` partial-credit weight.
    """
    answer_norm = _norm_ws(answer)
    ans_pairs, ans_jos = _answer_articles(answer)
    by_index: dict[int, float] = {}
    for v in verdicts:
        verdict_upper = v.verdict.upper()
        weight = _VERDICT_WEIGHTS.get(verdict_upper, 0.0)
        ok = weight > 0 and quote_in_answer(v.quote, answer_norm)
        by_index[v.index] = weight if ok else 0.0
    result: list[float] = []
    for i, rubric in enumerate(rubrics):
        value = by_index.get(i + 1, 0.0)
        if value:
            rub = str(rubric)
            art = _P_ART_NUM.search(rub)
            if art and _MUST_CITE_ART.search(rub):
                jo, ga = art.group(1), art.group(2)
                cited = (jo, ga) in ans_pairs if ga else (jo in ans_jos)
                if not cited:
                    value = 0
        result.append(value)
    return result


# "번호 | O/X | 근거: <인용>" — free-text fallback parser (sp_qwen compatible).
_LINE = re.compile(
    r"(?m)^\s*\**\s*(\d+)\s*[|｜).:：]\s*\**\s*([OXox])\b\s*[|｜]?\s*(?:근거\s*[:：]?\s*)?(.*)$"
)


def parse_free_text_verdicts(out: str) -> list[Verdict]:
    """Parse a free-text judge transcript into verdict triples."""
    verdicts: list[Verdict] = []
    for m in _LINE.finditer(out):
        verdicts.append(
            Verdict(index=int(m.group(1)), verdict=m.group(2).upper(), quote=m.group(3))
        )
    return verdicts


# --------------------------------------------------------------------------- #
# Scoring → §8.1 metrics for one (answer, rubric set) pair.
# --------------------------------------------------------------------------- #
def score_answer(binary: Sequence[float], item_types: Sequence[str]) -> dict[str, Any]:
    """Aggregate a 0/0.5/1 verdict list into §8.1 quality metrics for one answer.

    ``rubric_score`` = satisfied / total (vari; issue-spotting checklist), where
    a partially-met (``P``, weight 0.5) item contributes half a point. Per-type
    recall gives issue-spotting recall, rule-statement, application, conclusion
    sub-scores. ``binary`` and ``item_types`` are aligned per item.
    """
    total = len(binary)
    satisfied = float(sum(binary))
    by_type_total: Counter[str] = Counter(item_types)
    by_type_hit: dict[str, float] = {kind: 0.0 for kind in by_type_total}
    for value, kind in zip(binary, item_types):
        if value:
            by_type_hit[kind] += value
    recall_by_type = {
        kind: (by_type_hit[kind] / by_type_total[kind]) if by_type_total[kind] else None
        for kind in RUBRIC_TYPES
        if by_type_total[kind]
    }
    return {
        "satisfied": satisfied,
        "total": total,
        "rubric_score": (satisfied / total) if total else None,
        "issue_spotting_recall": recall_by_type.get("issue"),
        "recall_by_type": recall_by_type,
        "hits_by_type": dict(by_type_hit),
        "totals_by_type": dict(by_type_total),
    }


# --------------------------------------------------------------------------- #
# Judge interface — concrete model call is gated on approval.
# --------------------------------------------------------------------------- #
class EssayJudge(Protocol):
    def score_rubrics(self, question: str, answer: str, rubrics: Sequence[str]) -> list[int]:
        """Return a 0/1 satisfaction list, ``len == len(rubrics)``."""
        ...


class DeferredJudge:
    """Explicit not-yet-approved state — refuses to run so nothing self-judges.

    Mirrors sp_qwen's DeferredJudge. Replace with an approved model-calling judge
    only after the active judge prompt and the judge *model* (self-judge vs an
    independent model, §12.5 circularity) are settled with the user.
    """

    def score_rubrics(self, question: str, answer: str, rubrics: Sequence[str]) -> list[int]:
        raise NotImplementedError(
            "EssayJudge is not approved yet: settle the judge prompt and the judge "
            "model (independent vs self-judge, §12.5) with the user before wiring."
        )


def score_with_judge(
    judge: EssayJudge,
    *,
    question: str,
    answer: str,
    rubric_set: RubricSet,
) -> dict[str, Any]:
    """Score one answer against a rubric set with a provided judge, then reduce
    to §8.1 metrics. The judge is responsible for applying :func:`apply_safeguards`
    (an approved judge does so internally); this only reduces the 0/1 list."""
    binary = judge.score_rubrics(question, answer, list(rubric_set.rubrics))
    if len(binary) != len(rubric_set):
        raise ValueError(
            f"judge returned {len(binary)} verdicts for {len(rubric_set)} rubric items"
        )
    return score_answer(binary, rubric_set.item_types)
