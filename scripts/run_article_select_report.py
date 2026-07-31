"""Does selection from the full catalog beat ranking a shortlist -- and at what token cost?

Two numbers per path, never one. Recall says whether the articles the rubric asks about are
there; call-2 payload size says what that recall costs downstream. Reporting recall alone
would hide that a spare article is not free: it is every card that article carries, and the
corpus ranges from 1 card (art342) to 200 (art250).

Retrieval is scored at every k from 1 to the ranked length, not only at 12/18/24. The
ranking is ordered, so truncating it is exact rather than an interpolation, and the
iso-performance question the run exists to answer -- "at the k where retrieval matches
selection, how many tokens does selection save?" -- needs the whole curve.
"""

from __future__ import annotations

import argparse
import collections
import json
import statistics as st
from pathlib import Path
from typing import Iterable, Mapping, Sequence

from idpr.eval.issue_recall import (
    PROJECT_ROOT,
    SCORABLE,
    load_issue_gold,
    recall,
)
from idpr.neural.article_select import attempt_article_map, expand_attempt_articles
from idpr.rulebase.cards import card_corpus
from idpr.rulebase.formalization import route_corpus
from idpr.rulebase.roles import resolve_card_roles

DEFAULT_SELECTION = PROJECT_ROOT / "data" / "eval" / "article_selection.jsonl"
DEFAULT_RETRIEVAL = PROJECT_ROOT / "data" / "eval" / "retrieval_l0_recall_report.json"
DEFAULT_OUT = PROJECT_ROOT / "data" / "eval" / "article_select_report.json"
TOKENIZER = Path(
    "/data5/jaehoonjeong/.cache/huggingface/hub/models--google--gemma-4-26B-A4B-it"
    "/snapshots/01e5b3ee840d3a9e0b0b493c593e85398a30ef75/tokenizer.json"
)


def _encoder():
    """Real tokenizer if it is on disk, character count otherwise.

    The report must run on a login node without the model cache; falling back keeps the
    card counts and the ratios exact and only the absolute token figures approximate, and
    the fallback is named in the output so nobody reads an estimate as a measurement.
    """
    if TOKENIZER.is_file():
        from tokenizers import Tokenizer

        tok = Tokenizer.from_file(str(TOKENIZER))
        return (lambda s: len(tok.encode(s, add_special_tokens=False).ids)), "gemma-4-26B"
    return (lambda s: len(s)), "characters (tokenizer unavailable)"


def article_costs() -> tuple[dict[str, dict[str, int]], dict[str, int]]:
    """Per-article call-2 payload cost, and the corpus totals.

    ``all`` is the current contract (every card call 2 is asked to assess). ``no_context``
    drops the cards whose slot role is ``context`` -- 의의·개설·보호법익·연혁, true of every
    case, and read by no inference rule in the compiled rulebase. It is reported rather than
    applied: the exclusion is a pipeline change, not a measurement.
    """
    encode, _ = _encoder()
    corpus = card_corpus()
    assessed = {r.card_id for r in route_corpus(corpus) if r.assessed_by_model}
    roles = {r.card_id: r.role for r in resolve_card_roles(corpus)}

    costs: dict[str, dict[str, int]] = collections.defaultdict(
        lambda: {"cards": 0, "tokens": 0, "cards_no_context": 0, "tokens_no_context": 0}
    )
    for card in corpus.cards:
        if card.id not in assessed:
            continue
        size = encode(json.dumps(card.model_payload(), ensure_ascii=False))
        entry = costs[card.article]
        entry["cards"] += 1
        entry["tokens"] += size
        if roles.get(card.id) != "context":
            entry["cards_no_context"] += 1
            entry["tokens_no_context"] += size
    totals = {
        key: sum(entry[key] for entry in costs.values())
        for key in ("cards", "tokens", "cards_no_context", "tokens_no_context")
    }
    return dict(costs), totals


def _cost_of(articles: Iterable[str], costs: Mapping[str, Mapping[str, int]]) -> dict[str, int]:
    out = {"cards": 0, "tokens": 0, "cards_no_context": 0, "tokens_no_context": 0}
    for article in articles:
        entry = costs.get(article)
        if entry is None:
            continue
        for key in out:
            out[key] += entry[key]
    return out


def _summarise(
    per_question: Mapping[str, Sequence[str]],
    gold,
    gold_bare,
    costs: Mapping[str, Mapping[str, int]],
) -> dict:
    """Recall on both golds plus the call-2 payload the selection implies."""
    scores, scores_bare, sizes = [], [], []
    for case_id, articles in per_question.items():
        if gold[case_id].bucket != SCORABLE:
            continue
        value = recall(gold[case_id].articles, articles)
        if value is not None:
            scores.append(value)
        bare = recall(gold_bare[case_id].articles, articles)
        if bare is not None:
            scores_bare.append(bare)
        sizes.append(_cost_of(articles, costs))

    def stat(key: str) -> dict[str, float]:
        values = [size[key] for size in sizes]
        return {
            "median": int(st.median(values)),
            "mean": round(st.mean(values), 1),
            "max": max(values),
        }

    return {
        "macro_recall": round(st.mean(scores), 4) if scores else None,
        "macro_recall_without_attempt_articles": (
            round(st.mean(scores_bare), 4) if scores_bare else None
        ),
        "questions": len(scores),
        "fully_recovered": sum(1 for value in scores if value == 1.0),
        "articles_per_question": {
            "median": int(st.median([len(a) for a in per_question.values()])),
            "max": max(len(a) for a in per_question.values()),
        },
        "call2_payload": {key: stat(key) for key in
                          ("cards", "tokens", "cards_no_context", "tokens_no_context")},
    }


def load_selection(path: Path) -> tuple[dict[str, list[str]], dict[str, list[str]], dict]:
    selected: dict[str, list[str]] = {}
    expanded: dict[str, list[str]] = {}
    meta = {"rows": 0, "failed": 0, "total_tokens": 0, "prompt_tokens": 0}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        meta["rows"] += 1
        if "error" in row:
            meta["failed"] += 1
            continue
        selected[row["sub_question_id"]] = list(row["selected"])
        expanded[row["sub_question_id"]] = list(row["articles"])
        usage = row.get("usage") or {}
        meta["total_tokens"] += int(usage.get("total_tokens", 0) or 0)
        meta["prompt_tokens"] += int(usage.get("prompt_tokens", 0) or 0)
    return selected, expanded, meta


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--selection", type=Path, default=DEFAULT_SELECTION)
    parser.add_argument("--retrieval", type=Path, default=DEFAULT_RETRIEVAL)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    _, tokenizer_name = _encoder()
    gold = load_issue_gold()
    gold_bare = load_issue_gold(with_attempt=False)
    costs, totals = article_costs()
    attempt_map = attempt_article_map()

    selected, expanded, meta = load_selection(args.selection)
    report: dict = {
        "tokenizer": tokenizer_name,
        "corpus_totals": totals,
        "selection_run": meta,
        "paths": {
            "llm_selection": _summarise(selected, gold, gold_bare, costs),
            "llm_selection_plus_attempt": _summarise(expanded, gold, gold_bare, costs),
        },
        "retrieval_curve": {},
    }

    # Retrieval at every k, by truncating the stored top-24 ranking.
    ranked = json.loads(args.retrieval.read_text(encoding="utf-8"))
    top = max(ranked["by_top_k"], key=lambda k: int(k))
    candidates = ranked["by_top_k"][top]["candidates"]
    longest = max(len(c["retrieval"]) for c in candidates.values())
    for k in range(1, longest + 1):
        cut = {q: c["retrieval"][:k] for q, c in candidates.items()}
        cut_expanded = {q: list(expand_attempt_articles(a, mapping=attempt_map))
                        for q, a in cut.items()}
        report["retrieval_curve"][str(k)] = {
            "retrieval": _summarise(cut, gold, gold_bare, costs),
            "retrieval_plus_attempt": _summarise(cut_expanded, gold, gold_bare, costs),
        }

    # Union, because the two paths do not fail on the same articles: of the gold the model
    # misses, most is inside retrieval's shortlist. The model takes the dominant offence of
    # an episode and lets its neighbours go -- 제297조 selected, 제298·301조 not -- which is
    # exactly what a card whose proposition names that offence catches.
    for k in sorted(report["retrieval_curve"], key=int):
        cut = {q: list(dict.fromkeys(selected.get(q, []) + c["retrieval"][:int(k)]))
               for q, c in candidates.items() if q in selected}
        report["retrieval_curve"][k]["union_with_llm_selection"] = _summarise(
            {q: list(expand_attempt_articles(a, mapping=attempt_map)) for q, a in cut.items()},
            gold, gold_bare, costs,
        )

    # The iso-performance question: the smallest k at which retrieval matches selection.
    for label, path_key in (("llm_selection", "retrieval"),
                            ("llm_selection_plus_attempt", "retrieval_plus_attempt")):
        target = report["paths"][label]["macro_recall"]
        match = None
        if target is not None:
            for k in sorted(report["retrieval_curve"], key=int):
                block = report["retrieval_curve"][k][path_key]
                if block["macro_recall"] is not None and block["macro_recall"] >= target:
                    match = {"k": int(k), **block}
                    break
        report["paths"][label]["retrieval_iso_performance"] = match
        if match:
            ours = report["paths"][label]["call2_payload"]
            report["paths"][label]["token_saving_vs_iso_retrieval"] = {
                key: {
                    "retrieval": match["call2_payload"][key]["median"],
                    "selection": ours[key]["median"],
                    "reduction": round(
                        1 - ours[key]["median"] / match["call2_payload"][key]["median"], 4
                    ) if match["call2_payload"][key]["median"] else None,
                }
                for key in ("cards", "tokens", "cards_no_context", "tokens_no_context")
            }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    for label in ("llm_selection", "llm_selection_plus_attempt"):
        block = report["paths"][label]
        iso = block.get("retrieval_iso_performance")
        print(
            f"{label:>28}: recall={block['macro_recall']} "
            f"(준용제외 {block['macro_recall_without_attempt_articles']}) "
            f"articles={block['articles_per_question']['median']} "
            f"cards={block['call2_payload']['cards']['median']} "
            f"tokens={block['call2_payload']['tokens']['median']} "
            f"| iso-retrieval k={iso['k'] if iso else 'none'}"
        )
    for k in ("8", "12", "18", "24"):
        block = report["retrieval_curve"].get(k)
        if block:
            print(
                f"{'union @ retrieval top-' + k:>28}: recall={block['union_with_llm_selection']['macro_recall']} "
                f"(검색 단독 {block['retrieval_plus_attempt']['macro_recall']}) "
                f"tokens={block['union_with_llm_selection']['call2_payload']['tokens']['median']}"
            )
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
