"""L0's own metric: did retrieval put the articles in issue on the table?

This is the gate the plan makes conditional on everything downstream -- if an article is
missed here, its cards are never assessed, the symbolic layer cannot reason about the
offence, and call 3 cannot write about it. No later stage recovers it.

Where the gold comes from, and where it does not
------------------------------------------------
The gold is the **rubric**. ``rubrics`` is a column of the KCL parquet, it is what
``rubric_score`` is computed against, and its items name the offence outright ("특수절도죄
성부를 논하고 있는지"). Translating those names to article keys is a statutory lookup, kept
in ``data/eval/rubric_crime_article_map.json`` and reviewed by a lawyer.

It is explicitly *not* ``issue_tags``. The approved plan named those as the gold, but the
premise turned out to be false: the parquet has no such column, and the tags were written
by hand into ``CURATED_TAGS`` in ``scripts/build_kcl_criminal_inventory.py`` by an earlier
agent. Scoring retrieval against another agent's guess at what each question asks measures
agreement between two unreviewed artifacts. ``legal_area`` comes from the same dictionary,
so the buckets below are derived from the rubric text instead of from it.

Buckets, and why an empty gold is not a zero
--------------------------------------------
The card corpus covers 51 형법각칙 articles. A procedural question names no offence at all,
and a question about 장물 names one that is outside the corpus. Scoring either as recall
0.0 would report a scope decision as a retrieval failure -- the metric would drop as the
corpus became more honest about its limits. So questions are bucketed and only ``scorable``
ones enter the macro average, with n reported beside it.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Iterable, Mapping, Sequence

PROJECT_ROOT = Path(__file__).resolve().parents[3]
INVENTORY_PATH = PROJECT_ROOT / "data" / "inventory" / "kcl_criminal_v1_draft.jsonl"
CRIME_MAP_PATH = PROJECT_ROOT / "data" / "eval" / "rubric_crime_article_map.json"

#: Offence names in rubric prose. Matches the extraction used to build the review document,
#: so the map and the scorer see the same surface forms.
#:
#: Digits are in the class because 제3자뇌물취득죄 and 제3자뇌물교부죄 exist: a Hangul-only
#: class silently truncated them to 자뇌물취득죄, which the reviewer caught.
CRIME_RE = re.compile(r"[가-힣0-9]{2,14}죄")

SCORABLE = "scorable"
NO_GOLD_NO_OFFENCE = "no_gold_no_offence"
NO_GOLD_OUT_OF_CORPUS = "no_gold_out_of_corpus"


@dataclass(frozen=True)
class QuestionGold:
    """One question's gold articles, plus why it has none when it has none."""

    sub_question_id: str
    articles: tuple[str, ...]
    #: Offence names the rubric used, in order of first appearance.
    crimes: tuple[str, ...]
    #: Named offences that exist but fall outside the 51-article corpus (장물, 특별법,
    #: 형법총칙). A coverage limit, reported rather than scored.
    out_of_corpus_crimes: tuple[str, ...]
    rubric_items: int

    @property
    def bucket(self) -> str:
        if self.articles:
            return SCORABLE
        if self.out_of_corpus_crimes:
            return NO_GOLD_OUT_OF_CORPUS
        return NO_GOLD_NO_OFFENCE


@lru_cache(maxsize=1)
def load_crime_map(path: str | None = None) -> dict:
    return json.loads(Path(path or CRIME_MAP_PATH).read_text(encoding="utf-8"))


def crime_articles(
    crime: str, *, crime_map: Mapping | None = None, with_attempt: bool = True
) -> tuple[str, ...]:
    """Article keys for one offence name, including the attempt article when derived.

    The attempt article rides along because the statute itself says so -- 제254조 punishes
    the attempt of 제250조 -- so it is a reading of the code, not a rule reverse-engineered
    from a list of misses.
    """
    crime_map = crime_map or load_crime_map()
    entry = crime_map["crimes"].get(crime)
    if entry is None:
        return ()
    articles = list(entry["articles"])
    if with_attempt and entry.get("derived") == "attempt":
        attempts = crime_map["attempt_articles"]
        articles.extend(
            attempts[article] for article in entry["articles"] if article in attempts
        )
    return tuple(dict.fromkeys(articles))


def _rubrics_by_question(
    inventory_path: Path, parquet_path: Path
) -> dict[str, list[str]]:
    import pandas as pd

    frame = pd.read_parquet(parquet_path)
    rubrics: dict[str, list[str]] = {}
    for line in inventory_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        row_index = record["source"]["source_row_index"]
        rubrics[record["sub_question_id"]] = [
            str(item) for item in frame.iloc[row_index]["rubrics"]
        ]
    return rubrics


def _resolve_parquet_path(inventory_path: Path, parquet_path: Path | None) -> Path:
    """Resolve the benchmark source without embedding a developer workstation path."""
    if parquet_path is not None:
        return parquet_path
    configured = os.environ.get("IDPR_KCL_PARQUET")
    if configured:
        return Path(configured)
    for line in inventory_path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        recorded = json.loads(line).get("source", {}).get("parquet_path")
        if recorded:
            return Path(recorded)
    raise ValueError(
        "KCL rubric parquet is not configured; pass parquet_path or set IDPR_KCL_PARQUET"
    )


def load_issue_gold(
    *,
    inventory_path: Path | None = None,
    parquet_path: Path | None = None,
    crime_map: Mapping | None = None,
    with_attempt: bool = True,
) -> dict[str, QuestionGold]:
    """Gold articles for every question, read off the rubric."""
    crime_map = crime_map or load_crime_map()
    inventory_path = inventory_path or INVENTORY_PATH
    rubrics = _rubrics_by_question(
        inventory_path, _resolve_parquet_path(inventory_path, parquet_path)
    )

    gold: dict[str, QuestionGold] = {}
    for sub_question_id, items in rubrics.items():
        crimes: list[str] = []
        for item in items:
            for crime in CRIME_RE.findall(item):
                if crime not in crimes:
                    crimes.append(crime)

        articles: list[str] = []
        out_of_corpus: list[str] = []
        for crime in crimes:
            entry = crime_map["crimes"].get(crime)
            if entry is None or entry["confidence"] == "not_an_offence":
                continue
            mapped = crime_articles(crime, crime_map=crime_map, with_attempt=with_attempt)
            if mapped:
                articles.extend(mapped)
            else:
                out_of_corpus.append(crime)

        gold[sub_question_id] = QuestionGold(
            sub_question_id=sub_question_id,
            articles=tuple(sorted(dict.fromkeys(articles))),
            crimes=tuple(crimes),
            out_of_corpus_crimes=tuple(dict.fromkeys(out_of_corpus)),
            rubric_items=len(items),
        )
    return gold


def gold_status(crime_map: Mapping | None = None) -> str:
    """``awaiting_legal_review`` until the 죄명 map is signed off."""
    return str((crime_map or load_crime_map()).get("status", "unknown"))


def recall(gold_articles: Sequence[str], candidates: Iterable[str]) -> float | None:
    """Fraction of gold articles present in the candidates.

    ``None``, never ``0.0``, when there is no gold: an absent denominator is not a failed
    retrieval, and averaging zeros over unscorable questions is how a coverage gap gets
    reported as a model defect.
    """
    if not gold_articles:
        return None
    return len(set(candidates) & set(gold_articles)) / len(gold_articles)


@dataclass(frozen=True)
class PathRecall:
    macro_recall: float
    questions: int
    fully_recovered: int

    def as_dict(self) -> dict[str, float | int]:
        return {
            "macro_recall": round(self.macro_recall, 4),
            "questions": self.questions,
            "fully_recovered": self.fully_recovered,
        }


def summarise_paths(
    gold: Mapping[str, QuestionGold],
    candidates_by_path: Mapping[str, Mapping[str, Sequence[str]]],
) -> dict[str, dict[str, float | int]]:
    """Macro recall per candidate path over the scorable questions only.

    Three paths are reported separately -- retrieval alone, call 1's proposals alone, and
    their union. The union is what the system runs on, but a union number on its own cannot
    answer whether retrieval contributed anything, and that question decides whether the
    retrieval stack belongs in the paper at all.
    """
    scorable = [item for item in gold.values() if item.bucket == SCORABLE]
    summary: dict[str, dict[str, float | int]] = {}
    for path, candidates in candidates_by_path.items():
        scores: list[float] = []
        complete = 0
        for item in scorable:
            score = recall(item.articles, candidates.get(item.sub_question_id, ()))
            if score is None:
                continue
            scores.append(score)
            if score == 1.0:
                complete += 1
        summary[path] = PathRecall(
            macro_recall=sum(scores) / len(scores) if scores else 0.0,
            questions=len(scores),
            fully_recovered=complete,
        ).as_dict()
    return summary


def bucket_counts(gold: Mapping[str, QuestionGold]) -> dict[str, int]:
    counts = {SCORABLE: 0, NO_GOLD_NO_OFFENCE: 0, NO_GOLD_OUT_OF_CORPUS: 0}
    for item in gold.values():
        counts[item.bucket] += 1
    return counts


def missed_articles(
    gold: Mapping[str, QuestionGold], candidates: Mapping[str, Sequence[str]]
) -> dict[str, int]:
    """Gold articles never recovered, by frequency. The list to read after a run."""
    missed: dict[str, int] = {}
    for item in gold.values():
        if item.bucket != SCORABLE:
            continue
        found = set(candidates.get(item.sub_question_id, ()))
        for article in item.articles:
            if article not in found:
                missed[article] = missed.get(article, 0) + 1
    return dict(sorted(missed.items(), key=lambda pair: (-pair[1], pair[0])))
