from __future__ import annotations

import argparse
import asyncio
import hashlib
import json
import os
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
    RuleIRGenerationContractError,
    RuleIRValidationError,
    render_rule_ir_natural_language_scaffold,
    validate_full_rule_ir_generation,
)


FRAUD_ROOT = PROJECT_ROOT / "data/rulegen/fraud"
COMMENTARY = PROJECT_ROOT / "data/commentary/kcl_criminal_v1_commentary_chunks.jsonl"
CORE_SET = FRAUD_ROOT / "fraud_core_norm_card_set.json"
GENERATION_REQUEST = FRAUD_ROOT / "fraud_full_rule_ir_generation_request.json"
FEWSHOT = FRAUD_ROOT / "fraud_rule_ir_generation_fewshot.json"
PROMPT = PROJECT_ROOT / "prompts/rulegen_merge_rule_ir.md"
RULE_IR_SCHEMA = PROJECT_ROOT / "docs/contracts/rule_ir.schema.json"
NORM_CARD_SCHEMA = PROJECT_ROOT / "docs/contracts/norm_card_set.schema.json"
RULEGEN_VALIDATOR = PROJECT_ROOT / "src/idpr/rulegen/__init__.py"
PREP_MANIFEST = FRAUD_ROOT / "fraud_rule_ir_generation_prep_manifest.json"
PREP_DECISIONS = FRAUD_ROOT / "fraud_rule_ir_generation_prep_review_decisions.jsonl"
CANDIDATE = FRAUD_ROOT / "fraud_full_rule_ir_candidate_unreviewed.json"
SCAFFOLD = FRAUD_ROOT / "fraud_full_rule_ir_natural_language_scaffold.md"
POST_TERRA_STATUS = FRAUD_ROOT / "fraud_full_rule_ir_post_terra_status.json"
RUN_ROOT = PROJECT_ROOT / ".cache/llm/runs/fraud_full_rule_ir"
SAFE_RUN_ID = re.compile(r"^[A-Za-z0-9_.-]+$")
EXPECTED_REVIEW_IDS = {
    "fraud.rule_ir.prep.scope",
    "fraud.rule_ir.prep.single_call",
    "fraud.rule_ir.prep.standard_state",
    "fraud.rule_ir.prep.evidence_gate",
    "fraud.rule_ir.prep.actor_roles",
    "fraud.rule_ir.prep.outputs",
    "fraud.rule_ir.prep.open_world",
    "fraud.rule_ir.prep.fewshot",
    "fraud.rule_ir.prep.review_sequence",
    "fraud.rule_ir.prep.api_ceiling",
}
TERRA_MAX_TOKENS = 64_000


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected JSON object: {path}")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def review_gate() -> dict[str, Any]:
    decisions = read_jsonl(PREP_DECISIONS)
    decision_ids = [row.get("review_id") for row in decisions]
    errors: list[str] = []
    if len(decision_ids) != len(set(decision_ids)):
        errors.append("duplicate preflight review IDs")
    if set(decision_ids) != EXPECTED_REVIEW_IDS:
        errors.append("preflight review IDs do not match the exact ten-item contract")
    pending = sorted(
        str(row.get("review_id"))
        for row in decisions
        if row.get("status") != "completed" or row.get("decision") != "approve"
    )
    if pending:
        errors.append(f"preflight decisions not approved: {pending}")
    return {
        "approved": not errors,
        "decision_count": len(decisions),
        "pending_or_rejected": pending,
        "errors": errors,
    }


def artifact_gate() -> dict[str, Any]:
    manifest = read_json(PREP_MANIFEST)
    expected = manifest.get("artifacts", {})
    errors: list[str] = []
    actual: dict[str, str] = {}
    for relative_path, expected_digest in expected.items():
        path = PROJECT_ROOT / relative_path
        if not path.is_file():
            errors.append(f"missing prepared artifact: {relative_path}")
            continue
        actual_digest = sha256(path)
        actual[relative_path] = actual_digest
        if actual_digest != expected_digest:
            errors.append(f"prepared artifact changed after review: {relative_path}")
    required = {
        str(path.relative_to(PROJECT_ROOT))
        for path in (
            CORE_SET,
            GENERATION_REQUEST,
            FEWSHOT,
            COMMENTARY,
            PROMPT,
            RULE_IR_SCHEMA,
            NORM_CARD_SCHEMA,
            RULEGEN_VALIDATOR,
        )
    }
    missing_manifest_entries = sorted(required - set(expected))
    if missing_manifest_entries:
        errors.append(
            f"prep manifest omits execution inputs: {missing_manifest_entries}"
        )
    return {"valid": not errors, "actual_sha256": actual, "errors": errors}


def build_system_prompt() -> str:
    prompt = PROMPT.read_text(encoding="utf-8").rstrip()
    schema = RULE_IR_SCHEMA.read_text(encoding="utf-8").rstrip()
    fewshot = FEWSHOT.read_text(encoding="utf-8").rstrip()
    return (
        f"{prompt}\n\nExact output JSON Schema:\n```json\n{schema}\n```\n\n"
        "Partial structural example only:\n"
        "This two-card example teaches status, evidence-gate, provenance, and actor-signature "
        "structure. It is not a complete statement of fraud doctrine. Do not copy its IDs, "
        "card count, source scope, or limited deception conclusions. The approved aggregate "
        "in the current request is the only substantive generation scope.\n"
        f"```json\n{fewshot}\n```\n"
    )


def load_commentary(norm_card_set: dict[str, Any]) -> dict[str, dict[str, Any]]:
    allowed = set(norm_card_set["source_scope"]["comment_ids"])
    return {
        row["comment_id"]: row
        for row in read_jsonl(COMMENTARY)
        if row["comment_id"] in allowed
    }


def dry_run_summary() -> dict[str, Any]:
    request = read_json(GENERATION_REQUEST)
    system_prompt = build_system_prompt()
    review = review_gate()
    artifacts = artifact_gate()
    payload_chars = len(json.dumps(request, ensure_ascii=False, sort_keys=True))
    existing_outputs = [
        str(path.relative_to(PROJECT_ROOT))
        for path in (CANDIDATE, SCAFFOLD, POST_TERRA_STATUS)
        if path.exists()
    ]
    return {
        "mode": "dry_run",
        "api_calls": 0,
        "planned_api_calls": 1,
        "request_id": request["request_id"],
        "cards": request["coverage_contract"]["cards"],
        "system_chars": len(system_prompt),
        "payload_chars": payload_chars,
        "total_chars": len(system_prompt) + payload_chars,
        "terra_model": os.environ.get("IDPR_TERRA_MODEL", "").strip() or "MISSING",
        "api_key": "set" if os.environ.get("SKIML_API_KEY", "").strip() else "MISSING",
        "terra_max_completion_tokens": TERRA_MAX_TOKENS,
        "max_concurrency": 1,
        "max_retries": 0,
        "review_gate": review,
        "artifact_gate": artifacts,
        "existing_outputs": existing_outputs,
        "execution_allowed": (
            review["approved"] and artifacts["valid"] and not existing_outputs
        ),
        "post_terra_required_sequence": [
            "local_contract_validation",
            "agent_rule_by_rule_review",
            "agent_long_form_natural_language_explanation",
            "human_rule_ir_review",
            "sol_critic",
            "human_re_review",
            "scallop_compile_and_runtime_tests",
        ],
    }


async def execute(args: argparse.Namespace, config: GatewayConfig) -> dict[str, Any]:
    review = review_gate()
    artifacts = artifact_gate()
    gate_errors = [*review["errors"], *artifacts["errors"]]
    existing_outputs = [
        str(path.relative_to(PROJECT_ROOT))
        for path in (CANDIDATE, SCAFFOLD, POST_TERRA_STATUS)
        if path.exists()
    ]
    if existing_outputs:
        gate_errors.append(
            f"refusing to overwrite existing post-Terra artifacts: {existing_outputs}"
        )
    if gate_errors:
        raise ValueError("Terra execution blocked:\n- " + "\n- ".join(gate_errors))

    request = read_json(GENERATION_REQUEST)
    norm_card_set = read_json(CORE_SET)
    commentary = load_commentary(norm_card_set)
    run_dir = RUN_ROOT / args.run_id
    gateway = LLMGateway(config)
    job = JSONCompletionJob(
        request_id=request["request_id"],
        role="terra",
        system_prompt=build_system_prompt(),
        payload=request,
        max_tokens=TERRA_MAX_TOKENS,
    )
    result = await gateway.complete_json(job)
    write_usage_manifest(run_dir / "terra_usage.jsonl", [result])
    raw_path = run_dir / "terra" / f"{job.request_id}.json"
    write_json(raw_path, result.output)

    validation_errors: list[str] = []
    try:
        validate_full_rule_ir_generation(result.output, commentary, norm_card_set)
    except (RuleIRValidationError, RuleIRGenerationContractError) as exc:
        validation_errors.extend(exc.errors)
        gateway.discard_cache(result)

    valid = not validation_errors
    if valid:
        write_json(CANDIDATE, result.output)
        SCAFFOLD.write_text(
            render_rule_ir_natural_language_scaffold(result.output),
            encoding="utf-8",
        )
        write_json(
            POST_TERRA_STATUS,
            {
                "version": "1.0.0",
                "status": "agent_review_pending",
                "candidate_sha256": sha256(CANDIDATE),
                "local_contract_validation": "pass",
                "agent_rule_by_rule_review": "pending",
                "agent_natural_language_explanation": "pending",
                "human_rule_ir_review_allowed": False,
                "sol_critic_allowed": False,
                "scallop_compile_allowed": False,
                "note": (
                    "The scaffold is mechanical and is not the required agent-authored "
                    "natural-language explanation."
                ),
            },
        )

    summary = {
        "version": "1.0.0",
        "run_id": args.run_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "request_id": job.request_id,
        "terra_model": config.model_for_role("terra"),
        "api_calls": int(not result.cached),
        "cache_hits": int(result.cached),
        "usage": result.usage,
        "valid": valid,
        "validation_errors": validation_errors,
        "raw_output_path": str(raw_path.relative_to(PROJECT_ROOT)),
        "candidate_path": (
            str(CANDIDATE.relative_to(PROJECT_ROOT)) if valid else None
        ),
        "next_gate": (
            "agent_review_and_long_form_explanation" if valid else "blocked_invalid_output"
        ),
        "human_rule_ir_review_allowed": False,
        "sol_critic_allowed": False,
        "scallop_compile_allowed": False,
    }
    write_json(run_dir / "run.json", summary)
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate one full fraud RuleIR after explicit human preflight approval."
    )
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--env-file", type=Path, default=PROJECT_ROOT / ".env")
    parser.add_argument(
        "--run-id",
        default=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
    )
    args = parser.parse_args()
    if not SAFE_RUN_ID.fullmatch(args.run_id):
        parser.error("--run-id contains unsafe characters")
    return args


def main() -> None:
    args = parse_args()
    load_dotenv(args.env_file, override=False)
    if not args.execute:
        print(json.dumps(dry_run_summary(), ensure_ascii=False, indent=2))
        return

    config = GatewayConfig.from_env(require_api_key=True, require_models=False)
    config.model_for_role("terra")
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
