#!/usr/bin/env python3
"""Build an exact-bridge, hybrid-retrieved Call 2 card A/B plan."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.retrieval import DenseIndex, LexicalIndex, issue_retrieval_queries, reciprocal_rank_fusion
from idpr.retrieval.models import CrossEncoderReranker, SentenceTransformerEncoder
from idpr.rulebase.cards import card_corpus
from idpr.rulebase.issue_catalog_v2 import compile_issue_catalog_v2
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.grounding import predicate_definitions

BE_SNAPSHOT = Path(
    "/data5/jaehoonjeong/.cache/huggingface/hub/models--google--embeddinggemma-300m/"
    "snapshots/57c266a740f537b4dc058e1b0cda161fd15afa75"
)
CE_SNAPSHOT = Path(
    "/data5/jaehoonjeong/.cache/huggingface/hub/models--BAAI--bge-reranker-v2-m3/"
    "snapshots/953dc6f6f85a1b2dbfca4c34a2796e7dde08d41e"
)
DENSE_CACHE = ROOT / "data/eval/cache/cards_embeddinggemma-300m_7512d150955707d6.json"


def rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def target_key(value: dict[str, Any]) -> tuple[str, str]:
    instance = value["instance_key"]
    return str(instance["offense_ref"]), str(value["predicate_ref"])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--bridge", type=Path, default=ROOT / "data/v2/card_target_issue_bridge.yaml"
    )
    parser.add_argument(
        "--planner",
        type=Path,
        default=ROOT
        / "experiments/v2_call15_directscope_26_causal/evaluation_instance_plan.jsonl",
    )
    parser.add_argument(
        "--call2",
        type=Path,
        default=ROOT
        / "experiments/v2_call15_directscope_26_causal/call2_full_v2/grounding_output.jsonl",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT
        / "experiments/v2_call15_directscope_26_causal/card_call2_ab_v1/plan.jsonl",
    )
    args = parser.parse_args()

    for path in (BE_SNAPSHOT, CE_SNAPSHOT, DENSE_CACHE):
        if not path.exists():
            raise RuntimeError(f"RETRIEVAL_UNAVAILABLE: missing {path}")

    bridge_doc = yaml.safe_load(args.bridge.read_text())
    routes = {
        (str(row["offense_ref"]), str(row["predicate_ref"])): str(row["issue_id"])
        for row in bridge_doc["routes"]
    }
    if len(routes) != len(bridge_doc["routes"]):
        raise ValueError("bridge contains duplicate routes")

    corpus = card_corpus()
    issues, _ = compile_issue_catalog_v2(corpus)
    issue_by_id = {issue.issue_id: issue for issue in issues}
    registry = load_definitions(ROOT / "data/v2/definitions")
    planner = {row["sub_question_id"]: row for row in rows(args.planner)}
    call2 = {row["sub_question_id"]: row for row in rows(args.call2)}
    if set(planner) != set(call2):
        raise ValueError("planner and Call 2 case universes differ")

    for route, issue_id in routes.items():
        issue = issue_by_id.get(issue_id)
        if issue is None or issue.function != "element_issue":
            raise ValueError(f"invalid element bridge {route}: {issue_id}")
        if registry.kind_of(route[1]) != "legal_element":
            raise ValueError(f"bridge is not LegalElement-only: {route}")

    encoder = SentenceTransformerEncoder(model_id=str(BE_SNAPSHOT), batch_size=32)
    reranker = CrossEncoderReranker(model_id=str(CE_SNAPSHOT), batch_size=32)
    lexical = LexicalIndex.build(tuple(card.proposition for card in corpus.cards))
    dense = DenseIndex(json.loads(DENSE_CACHE.read_text()))

    pending: list[dict[str, Any]] = []
    truth_counts: Counter[str] = Counter()
    issue_counts: Counter[str] = Counter()
    for case_id, plan in planner.items():
        occurrence_by_id = {
            str(value["occurrence_id"]): value for value in plan["occurrences"]
        }
        targets = []
        for assessment in call2[case_id]["assessments"]:
            if assessment["truth"] != "UNKNOWN":
                continue
            route = target_key(assessment)
            issue_id = routes.get(route)
            if issue_id is None:
                continue
            instance = assessment["instance_key"]
            occurrence = occurrence_by_id[str(instance["occurrence_id"])]
            predicate = predicate_definitions(registry, (route[1],))[0]
            issue = issue_by_id[issue_id]
            focus = tuple(
                value
                for value in (predicate.canonical_meaning, predicate.legal_standard or "")
                if value
            )
            query = issue_retrieval_queries(
                issue,
                ({"assertion": {"source_quote": occurrence["source_text"]}},),
                focus_texts=focus,
            )[0]
            pending.append(
                {
                    "case_id": case_id,
                    "case_index": len(targets),
                    "assessment": assessment,
                    "instance": instance,
                    "occurrence": occurrence,
                    "predicate": predicate,
                    "issue": issue,
                    "query": query,
                }
            )
            targets.append(None)
            truth_counts[str(assessment["truth"])] += 1
            issue_counts[issue_id] += 1

    cards = tuple(corpus.cards)
    card_index = {card.id: index for index, card in enumerate(cards)}
    query_vectors = encoder.encode([value["query"] for value in pending], is_query=True)
    shortlists: list[list[int]] = []
    for value, vector in zip(pending, query_vectors):
        candidates = [card_index[card_id] for card_id in value["issue"].retrieval_card_ids]
        lexical_scores = lexical.scores(value["query"])
        lexical_rank = sorted(candidates, key=lambda i: (-lexical_scores[i], i))
        dense_scores = dense.scores(vector)
        dense_rank = sorted(candidates, key=lambda i: (-dense_scores[i], i))
        fused = reciprocal_rank_fusion((lexical_rank, dense_rank))
        shortlists.append(sorted(candidates, key=lambda i: (-fused[i], i))[:100])

    pairs = [
        (value["query"], cards[index].proposition)
        for value, shortlist in zip(pending, shortlists)
        for index in shortlist
    ]
    ce_model = reranker._load()
    all_scores = [
        float(score)
        for score in ce_model.predict(pairs, batch_size=32, show_progress_bar=False)
    ]
    offset = 0
    output_by_case: dict[str, list[dict[str, Any]]] = {case_id: [] for case_id in planner}
    for value, shortlist in zip(pending, shortlists):
        scores = all_scores[offset : offset + len(shortlist)]
        offset += len(shortlist)
        ranked = sorted(zip(shortlist, scores), key=lambda pair: (-pair[1], cards[pair[0]].id))
        selected = ranked[:2]
        issue = value["issue"]
        payload = issue.model_payload(corpus.by_id, detail_card_ids=[cards[i].id for i, _ in selected])
        materials = [
            *(
                {"material_id": card_id, "role": "anchor_context", "proposition": corpus.by_id[card_id].proposition}
                for card_id in issue.anchor_card_ids
            ),
            *(
                {"material_id": rule.rule_id, "role": "reviewed_anchor_rule", "proposition": rule.proposition}
                for rule in issue.reviewed_anchor_rules
            ),
            *(
                {"material_id": cards[index].id, "role": "hybrid_detail", "proposition": cards[index].proposition}
                for index, _ in selected
            ),
        ]
        case_targets = output_by_case[value["case_id"]]
        case_targets.append(
            {
                "ab_target_id": f"{value['case_id']}:card_ab:{len(case_targets)+1:03d}",
                "assessment_target": {"instance_key": value["instance"], "predicate_ref": value["predicate"].predicate_ref},
                "original_truth": value["assessment"]["truth"],
                "evidence_occurrence": value["occurrence"],
                "question_assumptions": call2[value["case_id"]].get("question_assumptions", []),
                "predicate_definition": value["predicate"].as_dict(),
                "reviewed_issue": {"issue_id": issue.issue_id, "question": payload["question"], "legal_materials": materials},
                "retrieval": {
                    "method": "BM25_BE_RRF_CE_WITHIN_EXACT_PARENT_ISSUE",
                    "queries": [value["query"]],
                    "selected_detail_card_ids": [cards[index].id for index, _ in selected],
                    "ce_scores": {cards[index].id: score for index, score in selected},
                },
            }
        )
    output = [
        {"sub_question_id": case_id, "ab_target_count": len(output_by_case[case_id]), "ab_targets": output_by_case[case_id]}
        for case_id in planner
    ]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in output)
    )
    manifest = {
        "status": "SUCCEEDED",
        "case_count": len(output),
        "route_count": len(routes),
        "physical_target_count": sum(row["ab_target_count"] for row in output),
        "original_truth_counts": dict(truth_counts),
        "issue_counts": dict(issue_counts),
        "retrieval": {
            "lexical": "character-bigram BM25",
            "dense_model": "google/embeddinggemma-300m",
            "dense_cache": str(DENSE_CACHE.relative_to(ROOT)),
            "fusion": "RRF(k=60)",
            "reranker_model": "BAAI/bge-reranker-v2-m3",
            "scope": "exact reviewed parent issue retrieval_card_ids",
            "top_k_detail": 2,
            "silent_fallback": False,
        },
        "bridge_sha256": sha256(args.bridge),
        "planner_sha256": sha256(args.planner),
        "call2_sha256": sha256(args.call2),
        "selection_uses_gold_or_rubric": False,
    }
    args.out.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
