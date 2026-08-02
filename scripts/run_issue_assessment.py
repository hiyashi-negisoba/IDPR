"""Assess normalized legal issues for one case and run symbolic composition.

The default scope is read from the persisted L0 candidate artifact.  ``--articles`` is
an explicit diagnostic override; production callers should omit it so that no case or
offence selection is embedded in the runner.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Mapping, Sequence

from idpr.candidates import candidate_issues
from idpr.eval.issue_recall import INVENTORY_PATH, PROJECT_ROOT
from idpr.issue_pipeline import (
    build_issue_reasoning_packet,
    followup_issues,
    generation_issues,
    run_issue_symbolic,
    scope_from_l0_row,
)
from idpr.neural.fact_graph import assessment_facts
from idpr.neural.issue_assessment import (
    SCHEMA_VERSION,
    UNKNOWN_REASONS,
    IssueAssessmentError,
    issue_assessment_request,
    issue_assessment_schema,
    validate_issue_assessments,
)
from idpr.neural.vllm_client import VLLMClient
from idpr.prompts import load_prompt
from idpr.rulebase.cards import card_corpus
from idpr.retrieval import DEFAULT_TOP_K_CARDS_PER_ISSUE, retrieve_issue_cards

FACT_GRAPHS = PROJECT_ROOT / "data/eval/fact_graphs.jsonl"
L0_CANDIDATES = PROJECT_ROOT / "data/eval/l0_candidates.jsonl"
SYSTEM_PROMPT = "issue_assess"
USER_PROMPT = "issue_assess_user"
_LAWLIKE_MISSING_RE = re.compile(r"법리|판례|정의|기준|요건|성립|해석|적용|해당")


def _write_json_atomic(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def _jsonl_by_id(path: Path) -> dict[str, dict[str, Any]]:
    return {
        row["sub_question_id"]: row
        for row in (
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    }


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


def prepare_issue_case(
    *,
    case_id: str,
    articles: tuple[str, ...] | None = None,
    inventory_path: Path = INVENTORY_PATH,
    fact_graph_path: Path = FACT_GRAPHS,
    candidates_path: Path = L0_CANDIDATES,
) -> tuple[dict[str, Any], dict[str, Any], Any]:
    inventory = _jsonl_by_id(inventory_path)
    graph_rows = _jsonl_by_id(fact_graph_path)
    candidate_rows = _jsonl_by_id(candidates_path)
    for name, table in (
        ("inventory", inventory),
        ("fact graph", graph_rows),
        ("L0 candidates", candidate_rows),
    ):
        if case_id not in table:
            raise ValueError(f"{case_id} missing from {name}")
    candidate_row = candidate_rows[case_id]
    persisted_articles = tuple(candidate_row.get("articles", ()))
    selected_articles = articles if articles is not None else persisted_articles
    if not selected_articles:
        raise ValueError(f"{case_id} has no candidate articles")
    if len(selected_articles) != len(set(selected_articles)):
        raise ValueError("articles must be unique")
    l0_articles = set(persisted_articles)
    missing = [article for article in selected_articles if article not in l0_articles]
    if missing:
        raise ValueError(f"requested articles are absent from L0 candidates: {missing}")

    graph = graph_rows[case_id].get("fact_graph")
    if not isinstance(graph, Mapping):
        raise ValueError(f"{case_id} has no admitted fact graph")
    scope = (
        scope_from_l0_row(candidate_row)
        if articles is None
        else candidate_issues(selected=selected_articles, attempt_map={})
    )
    if not scope.initial_issues:
        raise ValueError("no assessable issues selected")
    return dict(inventory[case_id]), dict(graph), scope


def _missing_diagnostic(output: Mapping[str, Any]) -> dict[str, Any]:
    missing = [
        text
        for assessment in output["assessments"].values()
        for text in assessment["missing_facts"]
    ]
    lawlike = sum(bool(_LAWLIKE_MISSING_RE.search(text)) for text in missing)
    reasons: dict[str, int] = {}
    for assessment in output["assessments"].values():
        reason = assessment.get("unknown_reason")
        if reason in UNKNOWN_REASONS:
            reasons[str(reason)] = reasons.get(str(reason), 0) + 1
    return {
        "missing_items": len(missing),
        "lawlike_items": lawlike,
        "lawlike_rate": lawlike / len(missing) if missing else 0.0,
        "unknown_reasons": reasons,
    }


def _complete_bundle(
    *,
    client: VLLMClient,
    request: Mapping[str, Any],
    schema: Mapping[str, Any],
    issue_ids: Sequence[str],
    fact_ids: Sequence[str],
    prompts: tuple[str, str],
    model: str,
    work_dir: Path,
    stage: str,
    max_tokens: int,
    temperature: float,
    no_cache: bool,
) -> tuple[Mapping[str, Any], list[dict[str, Any]], dict[str, int]]:
    correction_errors: list[str] = []
    attempt_records: list[dict[str, Any]] = []
    total_usage: dict[str, int] = {}
    output: Mapping[str, Any] = {}
    for attempt in range(1, 3):
        attempt_request = dict(request)
        if correction_errors:
            attempt_request["contract_correction"] = {
                "errors": correction_errors,
                "instruction": (
                    "모든 issue를 다시 출력하라. 반대 fact가 없으면 not_satisfied가 아니라 "
                    "unknown이며, unknown에는 구체적 missing_facts와 원인별 "
                    "unknown_reason이 필요하다. 비-unknown은 unknown_reason을 "
                    "not_applicable로 출력하라."
                ),
            }
        cache_key = _cache_key(
            model=model,
            system_prompt=prompts[0],
            user_prompt=prompts[1],
            payload=attempt_request,
            schema=schema,
        )
        cache_path = work_dir / f"{cache_key}.json"
        if cache_path.is_file() and not no_cache:
            cached = json.loads(cache_path.read_text(encoding="utf-8"))
            output, metadata = cached["output"], cached.get("metadata", {})
            source = "cache"
        else:
            output, metadata = client.complete_json(
                system_prompt=prompts[0],
                payload=attempt_request,
                schema_name=f"issue_assessment_{stage}_{attempt}",
                schema=schema,
                max_tokens=max_tokens,
                temperature=temperature,
                user_template=prompts[1],
            )
            _write_json_atomic(
                cache_path,
                {"output": output, "metadata": metadata},
            )
            source = "model"
        usage = metadata.get("usage", {})
        for key, value in usage.items():
            if isinstance(value, int):
                total_usage[key] = total_usage.get(key, 0) + value
        try:
            validate_issue_assessments(
                output,
                case_id=str(request["case_id"]),
                issue_ids=issue_ids,
                fact_ids=fact_ids,
            )
        except IssueAssessmentError as error:
            attempt_records.append(
                {
                    "attempt": attempt,
                    "source": source,
                    "errors": error.errors,
                    "usage": usage,
                }
            )
            if attempt == 2:
                raise
            correction_errors = error.errors
            continue
        attempt_records.append({"attempt": attempt, "source": source, "errors": [], "usage": usage})
        break
    return output, attempt_records, total_usage


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url")
    parser.add_argument("--model")
    parser.add_argument("--api-key", default="local-idpr")
    parser.add_argument("--case-id", required=True)
    parser.add_argument(
        "--articles",
        nargs="+",
        help="diagnostic subset override; default is this case's complete L0 scope",
    )
    parser.add_argument("--inventory", type=Path, default=INVENTORY_PATH)
    parser.add_argument("--fact-graphs", type=Path, default=FACT_GRAPHS)
    parser.add_argument("--candidates", type=Path, default=L0_CANDIDATES)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument(
        "--work-dir",
        type=Path,
        help="cache/runtime directory (default: .cache/issue_pipeline/<case-id>)",
    )
    parser.add_argument("--max-tokens", type=int, default=4096)
    parser.add_argument("--timeout-seconds", type=float, default=7200.0)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--no-cache", action="store_true")
    parser.add_argument(
        "--detail-cards-per-issue",
        type=int,
        default=DEFAULT_TOP_K_CARDS_PER_ISSUE,
    )
    parser.add_argument("--no-refine-unknown", action="store_true")
    parser.add_argument(
        "--no-followup-relations",
        action="store_true",
        help="skip the post-element stage/participation/concurrence/guard pass",
    )
    args = parser.parse_args()
    if args.detail_cards_per_issue < 1:
        parser.error("--detail-cards-per-issue must be at least 1")

    args.work_dir = args.work_dir or PROJECT_ROOT / ".cache/issue_pipeline" / args.case_id
    case, graph, scope = prepare_issue_case(
        case_id=args.case_id,
        articles=tuple(args.articles) if args.articles else None,
        inventory_path=args.inventory,
        fact_graph_path=args.fact_graphs,
        candidates_path=args.candidates,
    )
    issues = scope.initial_issues
    corpus = card_corpus()
    issue_payloads = [issue.model_payload(corpus.by_id) for issue in issues]
    request = issue_assessment_request(case=case, fact_graph=graph, issues=issue_payloads)
    request["version"] = SCHEMA_VERSION
    facts = assessment_facts(graph)
    fact_ids = [fact["fact_id"] for fact in facts]
    issue_ids = [issue.issue_id for issue in issues]
    schema = issue_assessment_schema(case_id=args.case_id, issue_ids=issue_ids, fact_ids=fact_ids)
    prompts = (load_prompt(SYSTEM_PROMPT), load_prompt(USER_PROMPT))
    plan = {
        "case_id": args.case_id,
        "articles": list(scope.articles),
        "facts": len(facts),
        "issues": len(issues),
        "anchor_rules": sum(len(issue.anchor_card_ids) for issue in issues),
        "retrieval_cards_not_loaded": sum(len(issue.retrieval_card_ids) for issue in issues),
        "payload_chars": len(json.dumps(request, ensure_ascii=False)),
        "max_tokens": args.max_tokens,
        "detail_cards_per_issue": args.detail_cards_per_issue,
        "refine_unknown": not args.no_refine_unknown,
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
    output, initial_attempts, initial_usage = _complete_bundle(
        client=client,
        request=request,
        schema=schema,
        issue_ids=issue_ids,
        fact_ids=fact_ids,
        prompts=prompts,
        model=args.model,
        work_dir=args.work_dir,
        stage="initial",
        max_tokens=args.max_tokens,
        temperature=args.temperature,
        no_cache=args.no_cache,
    )
    initial_output = output
    total_usage = dict(initial_usage)
    issue_by_id = {issue.issue_id: issue for issue in issues}
    unknown_ids = [
        issue_id for issue_id in issue_ids if output["assessments"][issue_id]["status"] == "unknown"
    ]
    refinement: dict[str, Any] = {
        "triggered_issue_ids": unknown_ids,
        "routes": {},
        "retrieved": {},
        "attempts": [],
        "usage": {},
    }
    if unknown_ids and not args.no_refine_unknown:
        routes = {
            issue_id: output["assessments"][issue_id].get("unknown_reason")
            for issue_id in unknown_ids
        }
        refinement["routes"] = routes
        # Legal detail retrieval can cure only a rule gap. A missing record stays
        # unknown; a FactGraph omission is reported for bounded Call-1 repair; and a
        # compound issue is an offline catalog-review item. Mixing these routes was the
        # source of irrelevant legal-card retries.
        retrievable_ids = [
            issue_id for issue_id in unknown_ids if routes[issue_id] == "rule_gap"
        ]
        unknown_issues = [issue_by_id[issue_id] for issue_id in retrievable_ids]
        focus = {
            issue_id: output["assessments"][issue_id]["missing_facts"] for issue_id in unknown_ids
            if issue_id in retrievable_ids
        }
        retrieved_details = retrieve_issue_cards(
            unknown_issues,
            facts,
            focus_by_issue=focus,
            corpus=corpus,
            top_k_per_issue=args.detail_cards_per_issue,
        )
        detail_by_issue = {
            result.issue_id: result.card_ids
            for result in retrieved_details.results
            if result.card_ids
        }
        refinement["retrieved"] = {
            result.issue_id: list(result.card_ids) for result in retrieved_details.results
        }
        refined_issues = [
            issue_by_id[issue_id] for issue_id in unknown_ids if issue_id in detail_by_issue
        ]
        if refined_issues:
            refined_payloads = [
                issue.model_payload(
                    corpus.by_id,
                    detail_card_ids=detail_by_issue[issue.issue_id],
                )
                for issue in refined_issues
            ]
            refined_request = issue_assessment_request(
                case=case, fact_graph=graph, issues=refined_payloads
            )
            refined_request["version"] = SCHEMA_VERSION
            refined_ids = [issue.issue_id for issue in refined_issues]
            refined_schema = issue_assessment_schema(
                case_id=args.case_id,
                issue_ids=refined_ids,
                fact_ids=fact_ids,
            )
            refined_output, refined_attempts, refined_usage = _complete_bundle(
                client=client,
                request=refined_request,
                schema=refined_schema,
                issue_ids=refined_ids,
                fact_ids=fact_ids,
                prompts=prompts,
                model=args.model,
                work_dir=args.work_dir,
                stage="refined",
                max_tokens=args.max_tokens,
                temperature=args.temperature,
                no_cache=args.no_cache,
            )
            merged = dict(output["assessments"])
            merged.update(refined_output["assessments"])
            output = {
                "version": SCHEMA_VERSION,
                "case_id": args.case_id,
                "assessments": merged,
            }
            refinement["attempts"] = refined_attempts
            refinement["usage"] = refined_usage
            for key, value in refined_usage.items():
                total_usage[key] = total_usage.get(key, 0) + value
    status_counts = {
        status: sum(assessment["status"] == status for assessment in output["assessments"].values())
        for status in ("satisfied", "not_satisfied", "unknown")
    }
    initial_status_counts = {
        status: sum(
            assessment["status"] == status for assessment in initial_output["assessments"].values()
        )
        for status in ("satisfied", "not_satisfied", "unknown")
    }
    initial_symbolic_runtime = run_issue_symbolic(
        case_id=args.case_id,
        fact_graph=graph,
        assessment_bundle=output,
        work_dir=args.work_dir / "symbolic",
        corpus=corpus,
        name=f"{args.case_id}_initial_issue",
    )
    relation_followup: dict[str, Any] = {
        "issue_ids": [],
        "attempts": [],
        "usage": {},
    }
    if not args.no_followup_relations:
        selected_followups = followup_issues(
            scope,
            symbolic_runtime=initial_symbolic_runtime,
        )
        followup_ids = [issue.issue_id for issue in selected_followups]
        relation_followup["issue_ids"] = followup_ids
        if selected_followups:
            followup_request = issue_assessment_request(
                case=case,
                fact_graph=graph,
                issues=[issue.model_payload(corpus.by_id) for issue in selected_followups],
            )
            followup_request["version"] = SCHEMA_VERSION
            followup_schema = issue_assessment_schema(
                case_id=args.case_id,
                issue_ids=followup_ids,
                fact_ids=fact_ids,
            )
            followup_output, followup_attempts, followup_usage = _complete_bundle(
                client=client,
                request=followup_request,
                schema=followup_schema,
                issue_ids=followup_ids,
                fact_ids=fact_ids,
                prompts=prompts,
                model=args.model,
                work_dir=args.work_dir,
                stage="relation_followup",
                max_tokens=args.max_tokens,
                temperature=args.temperature,
                no_cache=args.no_cache,
            )
            merged = dict(output["assessments"])
            merged.update(followup_output["assessments"])
            output = {
                "version": SCHEMA_VERSION,
                "case_id": args.case_id,
                "assessments": merged,
            }
            relation_followup["attempts"] = followup_attempts
            relation_followup["usage"] = followup_usage
            for key, value in followup_usage.items():
                total_usage[key] = total_usage.get(key, 0) + value

    symbolic_runtime = run_issue_symbolic(
        case_id=args.case_id,
        fact_graph=graph,
        assessment_bundle=output,
        work_dir=args.work_dir / "symbolic",
        corpus=corpus,
        name=f"{args.case_id}_issue",
    )
    status_counts = {
        status: sum(assessment["status"] == status for assessment in output["assessments"].values())
        for status in ("satisfied", "not_satisfied", "unknown")
    }
    assessed_by_id = {
        issue.issue_id: issue
        for issue in generation_issues(
            scope.issues,
            assessment_bundle=output,
            corpus=corpus,
        )
    }
    generation_retrieval = retrieve_issue_cards(
        list(assessed_by_id.values()),
        facts,
        corpus=corpus,
        top_k_per_issue=args.detail_cards_per_issue,
    )
    generation_details: dict[str, tuple[str, ...]] = {}
    for issue_id in assessed_by_id:
        prioritized = [
            *refinement["retrieved"].get(issue_id, ()),
            *generation_retrieval.by_issue[issue_id].card_ids,
        ]
        selected = tuple(dict.fromkeys(prioritized))[: args.detail_cards_per_issue]
        if selected:
            generation_details[issue_id] = selected
    reasoning_packet = build_issue_reasoning_packet(
        scope=scope,
        assessment_bundle=output,
        symbolic_runtime=symbolic_runtime,
        corpus=corpus,
        details_by_issue=generation_details,
    )
    report = {
        **plan,
        "model": args.model,
        "attempts": initial_attempts,
        "prompt_sha256": {
            "system": hashlib.sha256(prompts[0].encode("utf-8")).hexdigest(),
            "user": hashlib.sha256(prompts[1].encode("utf-8")).hexdigest(),
        },
        "usage": total_usage,
        "initial_usage": initial_usage,
        "initial_status_counts": initial_status_counts,
        "status_counts": status_counts,
        "missing_diagnostic": _missing_diagnostic(output),
        "initial_issue_status": initial_output,
        "refinement": refinement,
        "relation_followup": relation_followup,
        "generation_detail_retrieval": {
            result.issue_id: {
                "card_ids": list(generation_details.get(result.issue_id, ())),
                "scores": {
                    card_id: result.card_scores[card_id]
                    for card_id in generation_details.get(result.issue_id, ())
                    if card_id in result.card_scores
                },
            }
            for result in generation_retrieval.results
            if generation_details.get(result.issue_id)
        },
        "issue_status": output,
        "initial_symbolic_runtime": initial_symbolic_runtime,
        "symbolic_runtime": symbolic_runtime,
        "reasoning_packet": reasoning_packet,
    }
    _write_json_atomic(args.out, report)
    print(f"usage={report['usage']}")
    print(f"status_counts={status_counts}")
    print(f"missing_diagnostic={report['missing_diagnostic']}")
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
