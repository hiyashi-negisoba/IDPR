from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import re
import sys
from dataclasses import replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from idpr.llm import (  # noqa: E402
    GatewayConfig,
    JSONCompletionJob,
    LLMGateway,
    write_usage_manifest,
)
from idpr.rulegen import (  # noqa: E402
    RulegenCritiqueValidationError,
    validate_rulegen_critique,
)


FRAUD_ROOT = PROJECT_ROOT / "data/rulegen/fraud"
CANDIDATE = FRAUD_ROOT / "fraud_full_rule_ir_candidate_unreviewed.json"
CORE_SET = FRAUD_ROOT / "fraud_core_norm_card_set.json"
MODULE_OWNERSHIP = FRAUD_ROOT / "fraud_rule_ir_module_ownership.json"
HUMAN_DECISION = FRAUD_ROOT / "fraud_full_rule_ir_human_review_decision.json"
POST_STATUS = FRAUD_ROOT / "fraud_full_rule_ir_post_terra_status.json"
PROMPT = PROJECT_ROOT / "prompts/fraud_full_rule_ir_critic.md"
CRITIC_SCHEMA = PROJECT_ROOT / "docs/contracts/rulegen_critique_report.schema.json"
TRACKED_REQUEST = FRAUD_ROOT / "fraud_full_rule_ir_sol_request.json"
TRACKED_REPORT = FRAUD_ROOT / "fraud_full_rule_ir_sol_critique.json"
TRACKED_RUN = FRAUD_ROOT / "fraud_full_rule_ir_sol_run.json"
RUN_ROOT = PROJECT_ROOT / ".cache/llm/runs/fraud_full_rule_ir_critic"
TARGET_ID = "kr.fraud.article347.full.v1_candidate"
REQUEST_ID = "fraud.article347.full.rule_ir.sol_critic.v1"
SAFE_RUN_ID = re.compile(r"^[A-Za-z0-9_.-]+$")


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected object: {path}")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_locator(ref: dict[str, Any]) -> dict[str, str]:
    return {
        "comment_id": ref["comment_id"],
        "section_path": ref["section_path"],
    }


def compact_norm_card(card: dict[str, Any], owner: str) -> dict[str, Any]:
    return {
        "id": card["id"],
        "module_id": owner,
        "proposition": card["proposition"],
        "norm_kind": card["norm_kind"],
        "polarity": card["polarity"],
        "formalization": card["formalization"],
        "authority_basis": card["authority_basis"],
        "doctrinal_status": card["doctrinal_status"],
        "variant_group": card["variant_group"],
        "review_notes": card["review_notes"],
        "source_refs": [source_locator(ref) for ref in card["source_refs"]],
    }


def compact_predicate(predicate: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": predicate["id"],
        "arguments": predicate["arguments"],
        "kind": predicate["kind"],
        "role": predicate["role"],
        "definition": predicate["definition"],
        "norm_card_ids": predicate["norm_card_ids"],
    }


def compact_rule(rule: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": rule["id"],
        "head": rule["head"],
        "body": rule["body"],
        "norm_card_ids": rule["norm_card_ids"],
        "review_notes": rule["review_notes"],
    }


def build_request() -> dict[str, Any]:
    candidate = read_json(CANDIDATE)
    norm_cards = read_json(CORE_SET)
    ownership = read_json(MODULE_OWNERSHIP)
    human_decision = read_json(HUMAN_DECISION)
    owners = ownership["card_ownership"]
    predicate_defs = {item["id"]: item for item in candidate["predicates"]}
    card_interfaces = []
    for card in norm_cards["cards"]:
        card_id = card["id"]
        slug = re.sub(r"[^a-z0-9]+", "_", card_id.lower()).strip("_")
        assessment_id = f"assess_{slug}"
        condition_id = f"satisfied_{slug}"
        card_interfaces.append(
            {
                "card_id": card_id,
                "module_id": owners[card_id],
                "assessment_predicate": assessment_id,
                "assessment_kind": predicate_defs[assessment_id]["kind"],
                "condition_predicate": condition_id,
            }
        )

    substantive_rules = [
        compact_rule(item)
        for item in candidate["rules"]
        if ".card." not in item["id"]
    ]
    canonical_predicates = [
        compact_predicate(item)
        for item in candidate["predicates"]
        if item["id"] == "provable"
        or (
            item["role"] == "derived"
            and not item["id"].startswith("satisfied_")
        )
    ]
    return {
        "stage": "rule_ir",
        "target_id": TARGET_ID,
        "target": {
            "projection_version": "1.0.0",
            "rule_set_metadata": {
                key: candidate[key]
                for key in (
                    "version",
                    "rule_set_id",
                    "issue_tag",
                    "status",
                    "legal_review",
                    "legal_review_questions",
                    "coverage_gaps",
                )
            },
            "actor_contract": {
                "argument_order": [
                    argument["name"]
                    for argument in predicate_defs["fraud_established"]["arguments"]
                ],
                "role_identity_policy": (
                    "deceived_person_id equals disposer_id; all other slots may unify "
                    "only where the relevant adapter requires it"
                ),
            },
            "mechanical_card_state_contract": {
                "omitted_rule_count": len(candidate["rules"])
                - len(substantive_rules),
                "statuses": ["satisfied", "not_satisfied", "unknown"],
                "evidence_gate": "every assessment atom is paired with provable",
                "unknown_semantics": "explicit only; relation absence is neither false nor unknown",
                "conflict_semantics": (
                    "provable satisfied and not_satisfied rows for one card emit fraud_conflict"
                ),
                "local_validation": "pass",
            },
            "card_interfaces": card_interfaces,
            "canonical_predicates": canonical_predicates,
            "substantive_rules": substantive_rules,
        },
        "bounded_source_material": {
            "reviewed_norm_cards": [
                compact_norm_card(card, owners[card["id"]])
                for card in norm_cards["cards"]
            ],
            "module_architecture": {
                "architecture": ownership["architecture"],
                "canonical_interfaces": ownership["canonical_interfaces"],
                "modules": ownership["modules"],
            },
            "human_review_decision": human_decision,
            "mechanical_audit": {
                "norm_cards": 88,
                "input_predicates": 88,
                "predicates": len(candidate["predicates"]),
                "rules": len(candidate["rules"]),
                "substantive_rules_in_projection": len(substantive_rules),
                "contract_validation": "pass",
                "tests": "61 passed before critic preparation",
            },
        },
    }


def build_system_prompt() -> str:
    return (
        PROMPT.read_text(encoding="utf-8").rstrip()
        + "\n\nExact output JSON Schema:\n```json\n"
        + CRITIC_SCHEMA.read_text(encoding="utf-8").rstrip()
        + "\n```\n"
    )


def allowed_source_refs(request: dict[str, Any]) -> list[dict[str, str]]:
    return [
        ref
        for card in request["bounded_source_material"]["reviewed_norm_cards"]
        for ref in card["source_refs"]
    ]


def preflight() -> dict[str, Any]:
    status = read_json(POST_STATUS)
    request = build_request()
    errors = []
    if status.get("human_rule_ir_review") != "approved":
        errors.append("human RuleIR review is not approved")
    if not status.get("sol_critic_allowed"):
        errors.append("Sol critic is not allowed by the current gate")
    if not status.get("sol_critic_execution_authorized"):
        errors.append("Sol critic execution is not explicitly authorized")
    if TRACKED_REPORT.exists() or TRACKED_RUN.exists():
        errors.append("tracked Sol critic output already exists")
    return {
        "valid": not errors,
        "errors": errors,
        "planned_api_calls": 1,
        "request_chars": len(
            json.dumps(request, ensure_ascii=False, sort_keys=True)
        ),
        "system_chars": len(build_system_prompt()),
        "candidate_sha256": sha256(CANDIDATE),
        "norm_card_set_sha256": sha256(CORE_SET),
        "substantive_rules": len(request["target"]["substantive_rules"]),
        "cards": len(request["bounded_source_material"]["reviewed_norm_cards"]),
    }


async def execute(args: argparse.Namespace, config: GatewayConfig) -> dict[str, Any]:
    gate = preflight()
    if not gate["valid"]:
        raise ValueError("Sol critic blocked:\n- " + "\n- ".join(gate["errors"]))
    request = build_request()
    write_json(TRACKED_REQUEST, request)
    run_dir = RUN_ROOT / args.run_id
    gateway = LLMGateway(config)
    job = JSONCompletionJob(
        request_id=REQUEST_ID,
        role="sol",
        system_prompt=build_system_prompt(),
        payload=request,
        max_tokens=args.sol_max_tokens,
        reasoning_effort="low",
    )
    result = await gateway.complete_json(job)
    write_usage_manifest(run_dir / "sol_usage.jsonl", [result])
    raw_path = run_dir / "sol" / f"{REQUEST_ID}.json"
    write_json(raw_path, result.output)
    validation_errors: list[str] = []
    try:
        validate_rulegen_critique(
            result.output,
            expected_stage="rule_ir",
            expected_target_id=TARGET_ID,
            allowed_source_refs=allowed_source_refs(request),
        )
    except RulegenCritiqueValidationError as exc:
        validation_errors.extend(exc.errors)
        gateway.discard_cache(result)
    valid = not validation_errors
    if valid:
        write_json(TRACKED_REPORT, result.output)

    summary = {
        "version": "1.0.0",
        "run_id": args.run_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "request_id": REQUEST_ID,
        "target_id": TARGET_ID,
        "sol_model": config.model_for_role("sol"),
        "api_calls": int(not result.cached),
        "cache_hits": int(result.cached),
        "usage": result.usage,
        "valid": valid,
        "validation_errors": validation_errors,
        "verdict": result.output.get("verdict"),
        "findings": len(result.output.get("findings", [])),
        "raw_output_path": str(raw_path.relative_to(PROJECT_ROOT)),
        "tracked_report_path": (
            str(TRACKED_REPORT.relative_to(PROJECT_ROOT)) if valid else None
        ),
        "next_gate": (
            "agent_source_grounded_rereview" if valid else "invalid_sol_output"
        ),
        "scallop_compile_allowed": False,
    }
    write_json(run_dir / "run.json", summary)
    write_json(TRACKED_RUN, summary)
    status = read_json(POST_STATUS)
    status.update(
        {
            "status": (
                "sol_critic_complete_agent_rereview_pending"
                if valid
                else "sol_critic_invalid_agent_action_required"
            ),
            "sol_critic_allowed": False,
            "sol_critic_execution_authorized": False,
            "sol_critic": "complete" if valid else "invalid_output",
            "sol_critic_report_path": (
                str(TRACKED_REPORT.relative_to(PROJECT_ROOT)) if valid else None
            ),
            "sol_critic_run_path": str(TRACKED_RUN.relative_to(PROJECT_ROOT)),
            "agent_post_sol_rereview": "pending",
            "human_post_sol_rereview": "blocked_pending_agent_rereview",
            "scallop_compile_allowed": False,
        }
    )
    write_json(POST_STATUS, status)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run exactly one Sol critique of the human-approved full fraud RuleIR."
    )
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--sol-max-tokens", type=int, default=20_000)
    parser.add_argument("--env-file", type=Path, default=PROJECT_ROOT / ".env")
    parser.add_argument(
        "--run-id",
        default=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
    )
    args = parser.parse_args()
    if not SAFE_RUN_ID.fullmatch(args.run_id):
        parser.error("--run-id contains unsafe characters")
    if not 1_000 <= args.sol_max_tokens <= 30_000:
        parser.error("--sol-max-tokens must be between 1000 and 30000")
    return args


def main() -> None:
    args = parse_args()
    load_dotenv(args.env_file, override=False)
    gate = preflight()
    if not args.execute:
        print(json.dumps({"mode": "dry_run", **gate}, ensure_ascii=False, indent=2))
        return
    config = GatewayConfig.from_env(require_api_key=True, require_models=True)
    config = replace(
        config,
        max_concurrency=1,
        max_retries=0,
        timeout_seconds=max(config.timeout_seconds, 900.0),
    )
    try:
        summary = asyncio.run(execute(args, config))
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if not summary["valid"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
