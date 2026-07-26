"""Crime-agnostic rulegen downstream: NormCard merge + NormCard critic.

The fraud downstream scripts (`run_fraud_norm_card_merge.py`,
`run_fraud_norm_card_critics.py`) hard-code 제347조 paths, the fraud module
taxonomy (`MODULE_PREFIXES`), and fraud exemplars. The KCL substantive campaign
needs the same two stages for 47 other 조문, so this driver lifts the fraud
constants into a `CrimeSpec` resolved from the command line and derives the
module grouping automatically from candidate `section_path`s.

Scope is deliberately the two auto-runnable stages only. The next stage —
RuleIR generation — is gated behind a per-crime human NormCard review
(`run_fraud_full_rule_ir_generation.py`'s `review_gate`/`artifact_gate`), so it
cannot run for a fresh crime without that review and is out of scope here.

terra(=gpt-5.6) is a reasoning model: the merge call sets reasoning_effort=low
with a generous completion budget, mirroring the extraction-stage fix (a bare
budget lets reasoning consume the whole limit and fail with finish_reason=length).

Prompts/schemas/validators/gold exemplar are reused unchanged from the approved
fraud pipeline. The gold NormCard set is a *structural* example only (the merge
prompt forbids copying its content), so reusing it across crimes is sound.

Safety: dry-run by default. Real terra/sol spend requires --execute.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from idpr.llm import (  # noqa: E402
    GatewayConfig,
    JSONCompletionJob,
    LLMGateway,
    write_usage_manifest,
)
from idpr.rulegen import (  # noqa: E402
    NormCardValidationError,
    RulegenCritiqueValidationError,
    validate_norm_card_set,
    validate_rulegen_critique,
)

from scripts.run_fraud_norm_card_critics import (  # noqa: E402
    partition_cards,
)
from scripts.run_fraud_rulegen_critics import read_json  # noqa: E402
from scripts.run_fraud_rulegen_pilot import (  # noqa: E402
    CRITIC_PROMPT,
    CRITIC_SCHEMA,
    SAFE_RUN_ID,
    load_jsonl,
    prompt_with_schema,
    write_json,
)


MERGE_PROMPT = PROJECT_ROOT / "prompts/rulegen_merge_norm_cards.md"
NORM_CARD_SCHEMA = PROJECT_ROOT / "docs/contracts/norm_card_set.schema.json"
# Structural gold example only (content copying is forbidden by the merge prompt),
# so the fraud exemplar is reused for every crime.
NORM_CARD_GOLD = PROJECT_ROOT / "data/rulegen/fraud/fraud_norm_card_set_exemplar.json"
RUN_ROOT = PROJECT_ROOT / ".cache/llm/runs/rulegen_downstream"

# Unicode roman-numeral section headers (U+2160..) → arabic, for ascii module slugs.
_ROMAN = {chr(0x2160 + i): i + 1 for i in range(10)}


@dataclass(frozen=True)
class CrimeSpec:
    slug: str  # e.g. "stolen_property" (issue_tag/card_set_id namespace)
    article_slug: str  # e.g. "article362"
    article: str  # e.g. "제362조" (commentary:// target)
    law_id: str  # e.g. "001692"
    requests: Path  # rulegen requests JSONL (carries commentary_chunks)
    candidates_dir: Path  # extraction run dir holding terra/*.json candidate batches


def module_slug(section_path: str, depth: int) -> str:
    """Deterministic ascii module key from a section_path prefix.

    "Ⅲ.2" (depth 2) -> "sec3_2"; "Ⅰ" -> "sec1". Groups candidates so that a
    dominant top-level section (e.g. 장물 Ⅲ = 153 candidates) is split into
    reviewable per-issue modules rather than one oversized merge call.
    """

    parts = section_path.split(".")[:depth]
    head = _ROMAN.get(parts[0])
    if head is None:
        # Non-roman section (e.g. raw_pdf.page_N fallback chunks for 주석서-부재
        # 스텁 조문): route to a single ascii-safe fallback module instead of
        # crashing, so those 조문 still merge into one card set.
        slug = re.sub(r"[^a-z0-9]+", "_", parts[0].lower()).strip("_") or "misc"
        return f"x_{slug}"
    tail = "_".join(parts[1:])
    return f"sec{head}" + (f"_{tail}" if tail else "")


def load_candidate_batches(candidates_dir: Path) -> dict[str, dict[str, Any]]:
    batches: dict[str, dict[str, Any]] = {}
    for path in sorted(candidates_dir.glob("*.json")):
        batch = read_json(path)
        if "candidates" not in batch:
            continue
        batches[batch["request_id"]] = batch
    if not batches:
        raise SystemExit(f"no candidate batches (*.json with 'candidates') under {candidates_dir}")
    return batches


def build_module_payloads(
    spec: CrimeSpec, depth: int
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    """Group candidates by module and build one merge payload per module.

    Returns (payloads_by_slug, requests_by_id). Mirrors the fraud
    build_module_payloads contract with crime-generic identifiers.
    """

    requests = load_jsonl(spec.requests)
    requests_by_id = {r["request_id"]: r for r in requests}
    batches = load_candidate_batches(spec.candidates_dir)

    grouped: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(
        lambda: defaultdict(list)
    )
    modules_by_request: dict[str, set[str]] = defaultdict(set)
    for request_id, batch in batches.items():
        for candidate in batch["candidates"]:
            slug = module_slug(candidate["source_refs"][0]["section_path"], depth)
            grouped[slug][request_id].append(candidate)
            modules_by_request[request_id].add(slug)

    payloads: dict[str, dict[str, Any]] = {}
    for slug in sorted(grouped):
        validated_batches: list[dict[str, Any]] = []
        comment_ids: set[str] = set()
        for request_id, candidates in sorted(grouped[slug].items()):
            batch = batches[request_id]
            validated_batches.append(
                {
                    "request_id": request_id,
                    "status": "draft",
                    "candidates": candidates,
                    "unresolved_questions": (
                        batch.get("unresolved_questions", [])
                        if len(modules_by_request[request_id]) == 1
                        else []
                    ),
                }
            )
            comment_ids.update(
                ref["comment_id"]
                for candidate in candidates
                for ref in candidate["source_refs"]
            )
        payloads[slug] = {
            "task": "merge_norm_cards",
            "card_set_id": f"kr.{spec.slug}.{spec.article_slug}.{slug}.norms.v1",
            "issue_tag": f"{spec.slug}_{slug}",
            "target_paths": [f"commentary://{spec.law_id}/{spec.article}#{slug}"],
            "allowed_comment_ids": sorted(comment_ids),
            "validated_batches": validated_batches,
            "unresolved_questions": sorted(
                {
                    q
                    for request_id in grouped[slug]
                    for q in batches[request_id].get("unresolved_questions", [])
                }
            ),
            "constraints": {
                "status": "draft",
                "legal_review": "pending",
                "construction": "api_merged",
            },
        }
    return payloads, requests_by_id


def allowed_candidates(payload: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    return {
        (batch["request_id"], candidate["candidate_id"]): candidate
        for batch in payload["validated_batches"]
        for candidate in batch["candidates"]
    }


def candidate_payload_for_cards(
    cards: list[dict[str, Any]],
    candidates: dict[tuple[str, str], dict[str, Any]],
) -> list[dict[str, Any]]:
    """Collect the bounded validated candidates a card group links to.

    Robust variant of the fraud helper: a first-pass merge on a fresh crime may
    emit candidate_refs pointing outside the module's candidate set (flagged by
    the merge validator as "source is outside linked candidates"). Skip those
    missing keys rather than KeyError, so critic cost can still be measured.
    """

    by_request: dict[str, list[dict[str, Any]]] = defaultdict(list)
    seen: set[tuple[str, str]] = set()
    for card in cards:
        for ref in card.get("candidate_refs", []):
            key = (ref.get("request_id", ""), ref.get("candidate_id", ""))
            if key in seen or key not in candidates:
                continue
            seen.add(key)
            by_request[key[0]].append(candidates[key])
    return [
        {"request_id": request_id, "candidates": request_candidates}
        for request_id, request_candidates in sorted(by_request.items())
    ]


def merge_system_prompt() -> str:
    prompt = prompt_with_schema(MERGE_PROMPT, NORM_CARD_SCHEMA)
    prompt += (
        "\nGold structural example:\n"
        "Learn only its candidate-to-card transformation. Never copy a card, source, "
        "authority choice, or conclusion absent from the current module payload.\n"
        "```json\n"
        + NORM_CARD_GOLD.read_text(encoding="utf-8").rstrip()
        + "\n```\n"
    )
    return prompt


def commentary_index(
    requests_by_id: dict[str, dict[str, Any]],
) -> tuple[dict[str, dict[str, Any]], dict[str, set[str]]]:
    commentary_by_id = {
        row["comment_id"]: row
        for request in requests_by_id.values()
        for row in request.get("commentary_chunks", [])
    }
    request_comment_ids = {
        request_id: {row["comment_id"] for row in request.get("commentary_chunks", [])}
        for request_id, request in requests_by_id.items()
    }
    return commentary_by_id, request_comment_ids


async def run_merge(
    spec: CrimeSpec,
    payloads: dict[str, dict[str, Any]],
    requests_by_id: dict[str, dict[str, Any]],
    run_dir: Path,
    max_tokens: int,
    config: GatewayConfig,
) -> dict[str, Any]:
    prompt = merge_system_prompt()
    jobs = [
        JSONCompletionJob(
            request_id=f"{spec.slug}.{slug}.normcards.v1",
            role="terra",
            system_prompt=prompt,
            payload=payload,
            max_tokens=max_tokens,
            reasoning_effort="low",  # terra=gpt-5.6 reasoning model
        )
        for slug, payload in payloads.items()
    ]
    job_slug = {job.request_id: slug for slug, job in zip(payloads, jobs)}

    gateway = LLMGateway(config)
    results = await gateway.complete_many(jobs)
    write_usage_manifest(run_dir / "merge_terra_usage.jsonl", results)

    commentary_by_id, request_comment_ids = commentary_index(requests_by_id)
    manifest_modules: list[dict[str, Any]] = []
    validation: list[dict[str, Any]] = []
    for result in results:
        slug = job_slug[result.request_id]
        payload = payloads[slug]
        output_path = run_dir / "norm_cards" / f"{slug}.json"
        write_json(output_path, result.output)
        errors: list[str] = []
        if result.output.get("card_set_id") != payload["card_set_id"]:
            errors.append("card_set_id does not match the module request")
        if result.output.get("issue_tag") != payload["issue_tag"]:
            errors.append("issue_tag does not match the module request")
        try:
            validate_norm_card_set(
                result.output,
                commentary_by_id,
                request_comment_ids,
                allowed_candidates=allowed_candidates(payload),
            )
        except NormCardValidationError as exc:
            errors.extend(exc.errors)
        if errors:
            gateway.discard_cache(result)
        manifest_modules.append(
            {"module": slug, "path": str(output_path.relative_to(PROJECT_ROOT))}
        )
        validation.append(
            {
                "module": slug,
                "valid": not errors,
                "errors": errors,
                "input_candidates": sum(
                    len(b["candidates"]) for b in payload["validated_batches"]
                ),
                "cards": len(result.output.get("cards", [])),
                "output_path": str(output_path.relative_to(PROJECT_ROOT)),
            }
        )

    write_json(
        run_dir / "norm_card_manifest.json",
        {"crime": spec.slug, "modules": manifest_modules},
    )
    usage = _sum_usage(results)
    summary = {
        "stage": "norm_card_merge",
        "run_id": run_dir.name,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "crime": spec.slug,
        "modules": list(payloads),
        "terra_model": config.model_for_role("terra"),
        "api_calls": sum(not r.cached for r in results),
        "cache_hits": sum(r.cached for r in results),
        "usage": usage,
        "validation": validation,
        "all_valid": all(v["valid"] for v in validation),
    }
    write_json(run_dir / "merge_run.json", summary)
    return summary


async def run_critic(
    spec: CrimeSpec,
    payloads: dict[str, dict[str, Any]],
    requests_by_id: dict[str, dict[str, Any]],
    run_dir: Path,
    cards_per_job: int,
    max_tokens: int,
    config: GatewayConfig,
) -> dict[str, Any]:
    manifest = read_json(run_dir / "norm_card_manifest.json")
    card_sets = {m["module"]: read_json(PROJECT_ROOT / m["path"]) for m in manifest["modules"]}
    commentary_by_id, _ = commentary_index(requests_by_id)
    prompt = prompt_with_schema(CRITIC_PROMPT, CRITIC_SCHEMA)

    jobs: list[JSONCompletionJob] = []
    metadata: dict[str, dict[str, Any]] = {}
    for slug, card_set in card_sets.items():
        candidates = allowed_candidates(payloads[slug])
        for index, target in enumerate(partition_cards(card_set, cards_per_job), start=1):
            target_id = f"{target['card_set_id']}.part{index:03d}"
            request_id = f"{spec.slug}.normcards.{slug}.part{index:03d}.critic"
            jobs.append(
                JSONCompletionJob(
                    request_id=request_id,
                    role="sol",
                    system_prompt=prompt,
                    payload={
                        "stage": "norm_card_set",
                        "target_id": target_id,
                        "target": target,
                        "bounded_source_material": {
                            "validated_candidates": candidate_payload_for_cards(
                                target["cards"], candidates
                            ),
                            "commentary_context": [
                                commentary_by_id[cid]
                                for cid in target["source_scope"]["comment_ids"]
                                if cid in commentary_by_id
                            ],
                        },
                    },
                    max_tokens=max_tokens,
                    reasoning_effort="low",
                )
            )
            metadata[request_id] = {
                "module": slug,
                "part": index,
                "target_id": target_id,
                "cards": len(target["cards"]),
                "allowed_source_refs": [
                    ref for card in target["cards"] for ref in card["source_refs"]
                ],
            }

    gateway = LLMGateway(config)
    results = await gateway.complete_many(jobs)
    write_usage_manifest(run_dir / "critic_sol_usage.jsonl", results)

    validation: list[dict[str, Any]] = []
    for result in results:
        meta = metadata[result.request_id]
        output_path = run_dir / "sol" / f"{result.request_id}.json"
        write_json(output_path, result.output)
        errors: list[str] = []
        try:
            validate_rulegen_critique(
                result.output,
                expected_stage="norm_card_set",
                expected_target_id=meta["target_id"],
                allowed_source_refs=meta["allowed_source_refs"],
            )
        except RulegenCritiqueValidationError as exc:
            gateway.discard_cache(result)
            errors.extend(exc.errors)
        validation.append(
            {
                "request_id": result.request_id,
                "module": meta["module"],
                "cards": meta["cards"],
                "valid": not errors,
                "errors": errors,
                "verdict": result.output.get("verdict"),
                "findings": len(result.output.get("findings", [])),
                "output_path": str(output_path.relative_to(PROJECT_ROOT)),
            }
        )

    usage = _sum_usage(results)
    summary = {
        "stage": "norm_card_critic",
        "run_id": run_dir.name,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "crime": spec.slug,
        "cards_per_job": cards_per_job,
        "sol_model": config.model_for_role("sol"),
        "api_calls": sum(not r.cached for r in results),
        "cache_hits": sum(r.cached for r in results),
        "usage": usage,
        "validation": validation,
        "all_valid": all(v["valid"] for v in validation),
    }
    write_json(run_dir / "critic_run.json", summary)
    return summary


def _sum_usage(results: list[Any]) -> dict[str, int]:
    return {
        key: sum(r.usage.get(key, 0) for r in results if not r.cached)
        for key in ("prompt_tokens", "completion_tokens", "reasoning_tokens", "total_tokens")
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--crime-slug", default="stolen_property")
    parser.add_argument("--article-slug", default="article362")
    parser.add_argument("--article", default="제362조")
    parser.add_argument("--law-id", default="001692")
    parser.add_argument(
        "--requests",
        type=Path,
        default=PROJECT_ROOT
        / "data/rulegen/stolen_property/stolen_property_rulegen_requests.jsonl",
    )
    parser.add_argument(
        "--candidates-dir",
        type=Path,
        default=PROJECT_ROOT
        / ".cache/llm/runs/stolen_property_rulegen/stolen_property_full/terra",
    )
    parser.add_argument("--stage", choices=["merge", "critic", "all"], default="all")
    parser.add_argument("--group-depth", type=int, default=2)
    parser.add_argument("--cards-per-job", type=int, default=50)
    parser.add_argument("--terra-max-tokens", type=int, default=64_000)
    parser.add_argument("--sol-max-tokens", type=int, default=20_000)
    parser.add_argument("--concurrency", type=int, default=2)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--env-file", type=Path, default=PROJECT_ROOT / ".env")
    parser.add_argument(
        "--run-id",
        default=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
    )
    args = parser.parse_args()
    if args.group_depth < 1:
        parser.error("--group-depth must be positive")
    if not SAFE_RUN_ID.fullmatch(args.run_id):
        parser.error("--run-id contains unsafe characters")
    return args


def main() -> None:
    args = parse_args()
    load_dotenv(args.env_file, override=False)
    spec = CrimeSpec(
        slug=args.crime_slug,
        article_slug=args.article_slug,
        article=args.article,
        law_id=args.law_id,
        requests=args.requests.resolve(),
        candidates_dir=args.candidates_dir.resolve(),
    )
    payloads, requests_by_id = build_module_payloads(spec, args.group_depth)
    run_dir = RUN_ROOT / spec.slug / args.run_id

    if not args.execute:
        summary = {
            "mode": "dry_run",
            "crime": spec.slug,
            "stage": args.stage,
            "group_depth": args.group_depth,
            "modules": {
                slug: {
                    "candidates": sum(
                        len(b["candidates"]) for b in payload["validated_batches"]
                    ),
                    "comment_ids": len(payload["allowed_comment_ids"]),
                    "payload_chars": len(json.dumps(payload, ensure_ascii=False)),
                }
                for slug, payload in payloads.items()
            },
            "planned_merge_calls": len(payloads),
            "run_dir": str(run_dir.relative_to(PROJECT_ROOT)),
        }
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return

    config = GatewayConfig.from_env(require_api_key=True, require_models=True)
    from dataclasses import replace

    config = replace(config, max_concurrency=args.concurrency)

    summaries: dict[str, Any] = {}
    if args.stage in ("merge", "all"):
        summaries["merge"] = asyncio.run(
            run_merge(spec, payloads, requests_by_id, run_dir, args.terra_max_tokens, config)
        )
    if args.stage in ("critic", "all"):
        summaries["critic"] = asyncio.run(
            run_critic(
                spec,
                payloads,
                requests_by_id,
                run_dir,
                args.cards_per_job,
                args.sol_max_tokens,
                config,
            )
        )
    print(json.dumps(summaries, ensure_ascii=False, indent=2))
    if not all(s["all_valid"] for s in summaries.values()):
        raise SystemExit(2)


if __name__ == "__main__":
    main()
