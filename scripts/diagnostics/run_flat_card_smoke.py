"""Diagnostic-only flat-card run retained to reproduce the Phase-2 comparison."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Mapping, Sequence

from idpr.candidates import CandidateBatch, candidate_articles, split_candidate_batches
from idpr.eval.issue_recall import INVENTORY_PATH, PROJECT_ROOT
from idpr.neural.card_assessment import (
    SCHEMA_VERSION,
    assessment_request,
    card_assessment_schema,
    card_status_rows,
    validate_card_assessments,
)
from idpr.neural.fact_graph import assessment_facts, fact_tuples
from idpr.neural.vllm_client import VLLMClient
from idpr.prompts import load_prompt
from idpr.rulebase.compile_scl import QUERY_RELATIONS, compile_rulebase
from idpr.rulebase.scallop import render_card_statuses, render_fact_layer, run_program

DEFAULT_CASE_ID = "kcl_criminal_r10_p1_q1_ga"
FACT_GRAPHS = PROJECT_ROOT / "data/eval/fact_graphs.jsonl"
L0_CANDIDATES = PROJECT_ROOT / "data/eval/l0_candidates.jsonl"
DEFAULT_OUT = PROJECT_ROOT / "data/eval/card_status_smoke.json"
SYSTEM_PROMPT = "card_assess"
USER_PROMPT = "card_assess_user"
DEFAULT_TOKENS_PER_CARD = 80
DEFAULT_OUTPUT_OVERHEAD = 1024


def _jsonl_by_id(path: Path) -> dict[str, dict[str, Any]]:
    return {
        row["sub_question_id"]: row
        for row in (
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    }


def prepare_case(
    *,
    case_id: str,
    inventory_path: Path = INVENTORY_PATH,
    fact_graph_path: Path = FACT_GRAPHS,
    candidates_path: Path = L0_CANDIDATES,
) -> tuple[dict[str, Any], dict[str, Any], tuple[CandidateBatch, ...]]:
    """Load Phase 2 artifacts and prove that reconstruction is byte-for-card complete."""
    inventory = _jsonl_by_id(inventory_path)
    graph_rows = _jsonl_by_id(fact_graph_path)
    candidate_rows = _jsonl_by_id(candidates_path)
    missing = [
        name
        for name, table in (
            ("inventory", inventory),
            ("fact graph", graph_rows),
            ("L0 candidates", candidate_rows),
        )
        if case_id not in table
    ]
    if missing:
        raise ValueError(f"{case_id} missing from {missing}")

    case = inventory[case_id]
    graph = graph_rows[case_id].get("fact_graph")
    if not isinstance(graph, Mapping):
        raise ValueError(f"{case_id} has no admitted fact graph")
    l0 = candidate_rows[case_id]
    candidates = candidate_articles(
        selected=l0["from_model"], retrieved=l0["from_retrieval"]
    )
    if list(candidates.articles) != l0["articles"]:
        raise ValueError("reconstructed article order differs from the Phase 2 artifact")
    if "card_ids" in l0 and list(candidates.card_ids) != l0["card_ids"]:
        raise ValueError("reconstructed card set differs from the Phase 2 artifact")
    batches = split_candidate_batches(candidates, parts=2)
    flattened = [card_id for batch in batches for card_id in batch.card_ids]
    if len(flattened) != len(set(flattened)) or set(flattened) != set(candidates.card_ids):
        raise ValueError("article batching lost or duplicated candidate cards")
    return dict(case), dict(graph), batches


def select_article_batches(
    batches: Sequence[CandidateBatch], articles: Sequence[str]
) -> tuple[CandidateBatch, ...]:
    """Return one complete batch per requested article, in requested order."""
    requested = tuple(articles)
    if not requested:
        raise ValueError("article A/B requires at least one article")
    if len(requested) != len(set(requested)):
        raise ValueError("article A/B articles must be unique")
    cards_by_article: dict[str, list[Any]] = {}
    for batch in batches:
        for card in batch.cards:
            cards_by_article.setdefault(card.article, []).append(card)
    missing = [article for article in requested if article not in cards_by_article]
    if missing:
        raise ValueError(f"article A/B targets are absent from L0 candidates: {missing}")
    return tuple(
        CandidateBatch(
            articles=(article,),
            cards=tuple(cards_by_article[article]),
            payload_chars=sum(
                len(card.id) + len(card.proposition)
                for card in cards_by_article[article]
            ),
        )
        for article in requested
    )


def _cache_key(
    *, model: str, system_prompt: str, user_prompt: str, payload: Mapping, schema: Mapping
) -> str:
    content = json.dumps(
        {
            "model": model,
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "payload": payload,
            "schema": schema,
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _serialise_results(
    results: Mapping[str, Sequence[Sequence[str]]]
) -> dict[str, list[list[str]]]:
    return {
        relation: [list(arguments) for arguments in rows]
        for relation, rows in results.items()
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url")
    parser.add_argument("--model")
    parser.add_argument("--api-key", default="local-idpr")
    parser.add_argument("--case-id", default=DEFAULT_CASE_ID)
    parser.add_argument("--inventory", type=Path, default=INVENTORY_PATH)
    parser.add_argument("--fact-graphs", type=Path, default=FACT_GRAPHS)
    parser.add_argument("--candidates", type=Path, default=L0_CANDIDATES)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--work-dir", type=Path, default=PROJECT_ROOT / ".cache/call2_smoke")
    # The first end-to-end smoke showed that Korean missing-fact strings plus JSON
    # punctuation can exceed 40 tokens per card.  This is only a ceiling: guided
    # decoding stops at the completed object, so the larger allowance does not make
    # successful responses longer.
    parser.add_argument(
        "--tokens-per-card", type=int, default=DEFAULT_TOKENS_PER_CARD
    )
    parser.add_argument(
        "--output-overhead", type=int, default=DEFAULT_OUTPUT_OVERHEAD
    )
    parser.add_argument("--timeout-seconds", type=float, default=7200.0)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--article-batches", nargs="+", metavar="ARTICLE")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-cache", action="store_true")
    args = parser.parse_args()

    case, graph, batches = prepare_case(
        case_id=args.case_id,
        inventory_path=args.inventory,
        fact_graph_path=args.fact_graphs,
        candidates_path=args.candidates,
    )
    mode = "balanced_two_way"
    if args.article_batches:
        batches = select_article_batches(batches, args.article_batches)
        mode = "one_batch_per_article"
    facts = assessment_facts(graph)
    fact_ids = [fact["fact_id"] for fact in facts]
    prompts = (load_prompt(SYSTEM_PROMPT), load_prompt(USER_PROMPT))
    plan = {
        "case_id": args.case_id,
        "batch_mode": mode,
        "facts": len(facts),
        "batches": [
            {
                "index": index,
                "articles": list(batch.articles),
                "cards": len(batch.cards),
                "payload_chars": batch.payload_chars,
                "max_tokens": args.output_overhead + args.tokens_per_card * len(batch.cards),
            }
            for index, batch in enumerate(batches, start=1)
        ],
    }
    if args.dry_run:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return
    if not args.base_url or not args.model:
        parser.error("--base-url and --model are required unless --dry-run is used")

    args.work_dir.mkdir(parents=True, exist_ok=True)
    client = VLLMClient(
        base_url=args.base_url,
        model=args.model,
        api_key=args.api_key,
        timeout_seconds=args.timeout_seconds,
    )
    batch_records: list[dict[str, Any]] = []
    batch_outputs: dict[str, Mapping[str, Any]] = {}
    total_usage: dict[str, int] = {}
    for index, batch in enumerate(batches, start=1):
        payload = assessment_request(
            case=case, fact_graph=graph, cards=batch.model_payload()
        )
        payload["version"] = SCHEMA_VERSION
        schema = card_assessment_schema(
            case_id=args.case_id, card_ids=batch.card_ids, fact_ids=fact_ids
        )
        cache_key = _cache_key(
            model=args.model,
            system_prompt=prompts[0],
            user_prompt=prompts[1],
            payload=payload,
            schema=schema,
        )
        cache_path = args.work_dir / f"{cache_key}.json"
        if cache_path.is_file() and not args.no_cache:
            cached = json.loads(cache_path.read_text(encoding="utf-8"))
            output, metadata = cached["output"], cached.get("metadata", {})
            source = "cache"
        else:
            output, metadata = client.complete_json(
                system_prompt=prompts[0],
                payload=payload,
                schema_name=f"card_assessment_batch_{index}",
                schema=schema,
                max_tokens=args.output_overhead + args.tokens_per_card * len(batch.cards),
                temperature=args.temperature,
                user_template=prompts[1],
            )
            cache_path.write_text(
                json.dumps(
                    {"output": output, "metadata": metadata},
                    ensure_ascii=False,
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            source = "model"
        validate_card_assessments(
            output,
            case_id=args.case_id,
            card_ids=batch.card_ids,
            fact_ids=fact_ids,
        )
        batch_outputs.update(output["assessments"])
        usage = metadata.get("usage", {})
        for key, value in usage.items():
            if isinstance(value, int):
                total_usage[key] = total_usage.get(key, 0) + value
        batch_records.append(
            {
                **plan["batches"][index - 1],
                "source": source,
                "cache_key": cache_key,
                "usage": usage,
            }
        )
        print(f"batch {index}/{len(batches)} ok cards={len(batch.cards)} source={source}")

    all_card_ids = tuple(
        card.id for batch in batches for card in batch.cards
    )
    merged = {
        "version": SCHEMA_VERSION,
        "case_id": args.case_id,
        "assessments": {
            card_id: batch_outputs[card_id] for card_id in all_card_ids
        },
    }
    validate_card_assessments(
        merged, case_id=args.case_id, card_ids=all_card_ids, fact_ids=fact_ids
    )

    statuses = card_status_rows(merged)
    program = (
        compile_rulebase()
        + render_fact_layer(args.case_id, fact_tuples(graph, case_id=args.case_id))
        + render_card_statuses(args.case_id, statuses)
    )
    symbolic = run_program(
        program,
        QUERY_RELATIONS,
        args.work_dir / "scallop",
        name=args.case_id,
    )
    report = {
        "case_id": args.case_id,
        "model": args.model,
        "prompt_sha256": {
            "system": hashlib.sha256(prompts[0].encode("utf-8")).hexdigest(),
            "user": hashlib.sha256(prompts[1].encode("utf-8")).hexdigest(),
        },
        "batches": batch_records,
        "usage": total_usage,
        "card_status": merged,
        "status_counts": {
            status: sum(1 for _, observed in statuses if observed == status)
            for status in ("satisfied", "not_satisfied", "unknown")
        },
        "symbolic_results": _serialise_results(symbolic),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"usage={total_usage}")
    print(f"status_counts={report['status_counts']}")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
