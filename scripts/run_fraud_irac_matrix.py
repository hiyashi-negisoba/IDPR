from __future__ import annotations

import argparse
import json
import re
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence, TypeVar

from jsonschema import Draft202012Validator


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from idpr.generation import (  # noqa: E402
    GenerationContractError,
    METHOD_IDS,
    apply_section_patches,
    assess_irac_answer_alignment,
    build_fraud_irac_plan,
    build_fraud_rag_packet,
    build_fraud_rag_queries,
    canonical_sha256,
    compile_fraud_whole_irac_answer,
    generation_schema,
    normalize_claim_graph,
    normalize_section_patch_bundle,
    render_long_form_markdown,
    validate_claim_graph,
    validate_fraud_rag_packet,
    validate_long_form_answer,
)
from idpr.fraud_planning import (  # noqa: E402
    build_fraud_assessment_context,
    reasoning_plan_card_ids,
    select_fraud_reasoning_plan,
    validate_fraud_case,
)
from idpr.neural import (  # noqa: E402
    anchor_fraud_target_roles,
    build_authority_packet,
    build_scallop_scenario,
    contract_schema,
    select_fraud_card_plan,
    validate_fraud_assessment_bundle,
    validate_fraud_fact_graph,
)
from idpr.neural.vllm_client import VLLMClient  # noqa: E402
from idpr.rulegen.scallop_runtime import (  # noqa: E402
    run_scenario,
    runtime_version,
    sha256_file,
)


CASE_PATH = PROJECT_ROOT / "data/e2e/fraud/kcl_r14_p1_q2_case.json"
NORM_CARD_PATH = PROJECT_ROOT / "data/rulegen/fraud/fraud_core_norm_card_set.json"
RULE_IR_PATH = (
    PROJECT_ROOT / "data/rulegen/fraud/fraud_full_rule_ir_candidate_unreviewed.json"
)
COMPILED_PATH = PROJECT_ROOT / "rules/generated/fraud_article347_full_v1.scl"
COMPILE_MANIFEST_PATH = (
    PROJECT_ROOT / "data/rulegen/fraud/fraud_scallop_compile_manifest.json"
)
SCLI_PATH = PROJECT_ROOT / "tools/scallop/scli-0.2.4-linux-x86_64"
FACT_PROMPT_PATH = PROJECT_ROOT / "prompts/fraud_fact_graph_extract.md"
FACT_USER_PROMPT_PATH = PROJECT_ROOT / "prompts/fraud_fact_graph_extract_user.md"
ASSESS_PROMPT_PATH = PROJECT_ROOT / "prompts/fraud_standard_assess.md"
ASSESS_USER_PROMPT_PATH = PROJECT_ROOT / "prompts/fraud_standard_assess_user.md"
ANSWER_PROMPT_PATH = PROJECT_ROOT / "prompts/fraud_long_form_generate.md"
CLAIM_PROMPT_PATH = PROJECT_ROOT / "prompts/fraud_claim_graph_extract.md"
REPAIR_PROMPT_PATH = PROJECT_ROOT / "prompts/fraud_section_repair.md"
QUERY_RELATIONS = (
    "fraud_elements_satisfied",
    "fraud_established",
    "fraud_not_established",
    "fraud_undetermined",
    "fraud_conflict",
)

T = TypeVar("T")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_case(path: Path, case_id: str | None = None) -> dict[str, Any]:
    """Load either one case contract or one case from a reusable case set."""

    payload = read_json(path)
    if "cases" not in payload:
        loaded_case_id = payload.get("case_id")
        if case_id is not None and case_id != loaded_case_id:
            raise ValueError(
                f"requested case_id {case_id!r} differs from single case "
                f"{loaded_case_id!r}"
            )
        return payload

    cases = payload.get("cases")
    if not isinstance(cases, list):
        raise ValueError("case set field 'cases' must be an array")
    if case_id is None:
        raise ValueError("--case-id is required when --case-path points to a case set")

    matches = [case for case in cases if case.get("case_id") == case_id]
    if len(matches) != 1:
        raise ValueError(
            f"case set must contain exactly one {case_id!r}; found {len(matches)}"
        )
    return matches[0]


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def timed_host(function: Callable[[], T]) -> tuple[T, float]:
    started = time.perf_counter()
    result = function()
    return result, time.perf_counter() - started


@dataclass(frozen=True)
class SampledClient:
    """Apply one sampling configuration to every model call of a run."""

    client: VLLMClient
    temperature: float = 0.0
    top_p: float | None = None
    top_k: int | None = None

    def complete_json(self, **kwargs: Any) -> tuple[dict[str, Any], dict[str, Any]]:
        return self.client.complete_json(
            temperature=self.temperature,
            top_p=self.top_p,
            top_k=self.top_k,
            **kwargs,
        )


def timed_model(
    client: VLLMClient,
    *,
    system_prompt: str,
    payload: Mapping[str, Any],
    schema_name: str,
    schema: Mapping[str, Any],
    max_tokens: int,
    user_template: str | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    started = time.perf_counter()
    output, metadata = client.complete_json(
        system_prompt=system_prompt,
        payload=payload,
        schema_name=schema_name,
        schema=schema,
        max_tokens=max_tokens,
        user_template=user_template,
    )
    return output, {**metadata, "latency_seconds": time.perf_counter() - started}


def fact_graph_request(case: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "task": "extract_fraud_fact_graph",
        "case_id": case["case_id"],
        "case_text": case["case_text"],
        "question_prompt": case["question_prompt"],
        "target": case["target"],
        "allowed_profiles": case["allowed_profiles"],
        "required_profiles": case["required_profiles"],
        "required_roles": [
            "defendant",
            "deceived_person",
            "disposer",
            "property_owner",
            "beneficiary",
        ],
    }


def assessment_request(
    *,
    case: Mapping[str, Any],
    fact_graph: Mapping[str, Any],
    selected_card_ids: Sequence[str],
    authority_packet: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    assessment_context = build_fraud_assessment_context(
        fact_graph,
        case=case,
        selected_card_ids=selected_card_ids,
    )
    if [item["card_id"] for item in assessment_context] != list(selected_card_ids):
        raise RuntimeError("assessment context order differs from selected cards")
    return {
        "task": "assess_host_selected_fraud_norm_cards",
        "case_id": case["case_id"],
        "case_text": case["case_text"],
        "fact_graph": fact_graph,
        "selected_card_ids": list(selected_card_ids),
        "assessment_context": assessment_context,
        "authority_packet": list(authority_packet),
    }


def verify_symbolic_assets(case: Mapping[str, Any]) -> tuple[dict[str, Any], str]:
    rule_ir = read_json(RULE_IR_PATH)
    manifest = read_json(COMPILE_MANIFEST_PATH)
    if case["rule_set_id"] != rule_ir["rule_set_id"]:
        raise RuntimeError("case and RuleIR rule_set_id do not match")
    if manifest.get("rule_set_id") != rule_ir["rule_set_id"]:
        raise RuntimeError("compile manifest and RuleIR rule_set_id do not match")
    if manifest.get("output", {}).get("sha256") != sha256_file(COMPILED_PATH):
        raise RuntimeError("compiled Scallop source differs from approved manifest")
    if not SCLI_PATH.is_file():
        raise RuntimeError("pinned scli runtime is missing")
    return rule_ir, COMPILED_PATH.read_text(encoding="utf-8")


def legal_result(observed: Mapping[str, bool]) -> str:
    if observed.get("fraud_conflict"):
        return "conflict"
    if observed.get("fraud_not_established"):
        return "not_established"
    if observed.get("fraud_undetermined"):
        return "undetermined"
    if observed.get("fraud_established"):
        return "established"
    return "blocked_without_final_conclusion"


def run_fact_graph(
    client: VLLMClient,
    case: Mapping[str, Any],
    method_dir: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    fact_graph, metadata = timed_model(
        client,
        system_prompt=FACT_PROMPT_PATH.read_text(encoding="utf-8"),
        user_template=FACT_USER_PROMPT_PATH.read_text(encoding="utf-8"),
        payload=fact_graph_request(case),
        schema_name="fraud_fact_graph",
        schema=contract_schema("fraud_fact_graph.schema.json"),
        max_tokens=5_000,
    )
    write_json(method_dir / "fact_graph_model_output.json", fact_graph)
    fact_graph, normalization = anchor_fraud_target_roles(fact_graph, case)
    validate_fraud_fact_graph(fact_graph, case)
    write_json(method_dir / "validated_fact_graph.json", fact_graph)
    return fact_graph, metadata, normalization


def run_symbolic_core(
    client: VLLMClient,
    *,
    case: Mapping[str, Any],
    fact_graph: Mapping[str, Any],
    norm_cards: Mapping[str, Any],
    rule_ir: Mapping[str, Any],
    compiled_source: str,
    method_dir: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any], dict[str, Any]]:
    reasoning_plan = select_fraud_reasoning_plan(fact_graph, case=case)
    plan_card_ids = reasoning_plan_card_ids(reasoning_plan)
    selected_card_ids = select_fraud_card_plan(
        fact_graph, case=case, norm_card_set=norm_cards
    )
    assessment_authority_packet = build_authority_packet(
        selected_card_ids, norm_cards
    )
    authority_packet = build_authority_packet(plan_card_ids, norm_cards)
    assessment_bundle, assessment_metadata = timed_model(
        client,
        system_prompt=ASSESS_PROMPT_PATH.read_text(encoding="utf-8"),
        user_template=ASSESS_USER_PROMPT_PATH.read_text(encoding="utf-8"),
        payload=assessment_request(
            case=case,
            fact_graph=fact_graph,
            selected_card_ids=selected_card_ids,
            authority_packet=assessment_authority_packet,
        ),
        schema_name="fraud_assessment_bundle",
        schema=contract_schema("fraud_assessment_bundle.schema.json"),
        max_tokens=9_000,
    )
    write_json(method_dir / "assessment_model_output.json", assessment_bundle)
    validate_fraud_assessment_bundle(
        assessment_bundle,
        case=case,
        fact_graph=fact_graph,
        selected_card_ids=selected_card_ids,
        authority_packet=assessment_authority_packet,
    )
    write_json(
        method_dir / "assessment_authority_packet.json",
        {"cards": assessment_authority_packet},
    )
    write_json(method_dir / "authority_packet.json", {"cards": authority_packet})
    write_json(method_dir / "assessment_bundle.json", assessment_bundle)
    scenario = build_scallop_scenario(
        case=case,
        fact_graph=fact_graph,
        assessment_bundle=assessment_bundle,
        selected_card_ids=selected_card_ids,
        authority_packet=assessment_authority_packet,
    )
    write_json(method_dir / "scallop_scenario.json", scenario)
    started = time.perf_counter()
    results = run_scenario(
        rule_ir=rule_ir,
        compiled_source=compiled_source,
        scenario=scenario,
        query_relations=QUERY_RELATIONS,
        scli_path=SCLI_PATH,
        work_dir=method_dir / "scallop_programs",
    )
    scallop_seconds = time.perf_counter() - started
    observed = {relation: result["nonempty"] for relation, result in results.items()}
    symbolic_result = {
        "legal_result": legal_result(observed),
        "observed_nonempty": observed,
    }
    if symbolic_result["legal_result"] == "blocked_without_final_conclusion":
        raise RuntimeError("Scallop produced no final legal conclusion")
    write_json(method_dir / "symbolic_result.json", symbolic_result)
    stage_metadata = {
        "assessment_bundle": assessment_metadata,
        "scallop": {"latency_seconds": scallop_seconds},
    }
    return authority_packet, assessment_bundle, symbolic_result, stage_metadata


def answer_request(
    *,
    case: Mapping[str, Any],
    method_id: str,
    context: Mapping[str, Any],
    allowed_fact_ids: Sequence[str] = (),
    allowed_card_ids: Sequence[str] = (),
    allowed_authority_ids: Sequence[str] = (),
    overall_conclusion: str | None = None,
    irac_plan: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    internal_knowledge = method_id == "m1_direct"
    payload: dict[str, Any] = {
        "task": "write_long_form_fraud_answer",
        "case_id": case["case_id"],
        "method_id": method_id,
        "case_text": case["case_text"],
        "question_prompt": case["question_prompt"],
        "target": case["target"],
        "legal_knowledge_policy": (
            "model_internal" if internal_knowledge else "supplied_context_only"
        ),
        "available_context": context,
        "allowed_provenance_ids": {
            "fact_ids": list(allowed_fact_ids),
            "card_ids": list(allowed_card_ids),
            "authority_comment_ids": list(allowed_authority_ids),
        },
        "rubric_supplied": False,
    }
    if overall_conclusion is not None:
        payload["required_overall_conclusion"] = overall_conclusion
    if irac_plan is not None:
        payload["required_irac_plan"] = irac_plan
    return payload


def run_answer(
    client: VLLMClient,
    *,
    case: Mapping[str, Any],
    method_id: str,
    method_dir: Path,
    context: Mapping[str, Any],
    allowed_fact_ids: Sequence[str] = (),
    allowed_card_ids: Sequence[str] = (),
    allowed_authority_ids: Sequence[str] = (),
    overall_conclusion: str | None = None,
    irac_plan: Mapping[str, Any] | None = None,
) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, str]]]:
    answer, metadata = timed_model(
        client,
        system_prompt=ANSWER_PROMPT_PATH.read_text(encoding="utf-8"),
        payload=answer_request(
            case=case,
            method_id=method_id,
            context=context,
            allowed_fact_ids=allowed_fact_ids,
            allowed_card_ids=allowed_card_ids,
            allowed_authority_ids=allowed_authority_ids,
            overall_conclusion=overall_conclusion,
            irac_plan=irac_plan,
        ),
        schema_name="long_form_answer",
        schema=generation_schema("long_form_answer.schema.json"),
        max_tokens=6_000,
    )
    write_json(method_dir / "answer_model_output.json", answer)
    violations = answer_contract_violations(
        answer,
        case_id=case["case_id"],
        method_id=method_id,
        allowed_fact_ids=allowed_fact_ids,
        allowed_card_ids=allowed_card_ids,
        allowed_authority_ids=allowed_authority_ids,
    )
    if irac_plan:
        violations.extend(assess_irac_answer_alignment(answer, irac_plan))
    write_json(method_dir / "answer.json", answer)
    (method_dir / "answer.md").write_text(
        render_long_form_markdown(answer), encoding="utf-8"
    )
    return answer, metadata, violations


def run_whole_irac_answer(
    *,
    case: Mapping[str, Any],
    method_dir: Path,
    plan: Mapping[str, Any],
) -> tuple[dict[str, Any], list[dict[str, str]], float]:
    answer, compile_seconds = timed_host(
        lambda: compile_fraud_whole_irac_answer(plan=plan, case=case)
    )
    facts, cards, authorities = whole_irac_allowed_provenance(plan)
    violations = answer_contract_violations(
        answer,
        case_id=case["case_id"],
        method_id="m5_irac_plan",
        allowed_fact_ids=facts,
        allowed_card_ids=cards,
        allowed_authority_ids=authorities,
    )
    violations.extend(assess_irac_answer_alignment(answer, plan))
    write_json(method_dir / "answer.json", answer)
    (method_dir / "answer.md").write_text(
        render_long_form_markdown(answer), encoding="utf-8"
    )
    return answer, violations, compile_seconds


def whole_irac_allowed_provenance(
    plan: Mapping[str, Any],
) -> tuple[list[str], list[str], list[str]]:
    """Whole-IRAC answers cite neural card assessments and Scallop-backed
    deterministic rules alike, so both card groups are allowed provenance."""

    facts = [
        fact_id for unit in plan["units"] for fact_id in unit["required_fact_ids"]
    ]
    cards = [
        assessment["card_id"]
        for unit in plan["units"]
        for assessment in unit["card_assessments"]
    ] + [
        rule["card_id"]
        for unit in plan["units"]
        for rule in unit.get("deterministic_rules", [])
    ]
    authorities = [
        comment_id
        for unit in plan["units"]
        for comment_id in unit["required_authority_comment_ids"]
    ]
    return facts, cards, authorities


def answer_contract_violations(
    answer: Mapping[str, Any],
    *,
    case_id: str,
    method_id: str,
    allowed_fact_ids: Sequence[str],
    allowed_card_ids: Sequence[str],
    allowed_authority_ids: Sequence[str],
) -> list[dict[str, str]]:
    try:
        validate_long_form_answer(
            answer,
            case_id=case_id,
            method_id=method_id,
            allowed_fact_ids=allowed_fact_ids,
            allowed_card_ids=allowed_card_ids,
            allowed_authority_ids=allowed_authority_ids,
        )
    except GenerationContractError as exc:
        violations: list[dict[str, str]] = []
        sections = list(answer.get("sections", []))
        for message in exc.errors:
            match = re.match(r"sections\[(\d+)\]", message)
            section_id = "document"
            if match and int(match.group(1)) < len(sections):
                section_id = sections[int(match.group(1))].get(
                    "section_id", "document"
                )
            violations.append(
                {
                    "code": "answer_contract_violation",
                    "section_id": section_id,
                    "message": message,
                }
            )
        return violations
    return []


def provenance_ids(
    fact_graph: Mapping[str, Any], authority_packet: Sequence[Mapping[str, Any]]
) -> tuple[list[str], list[str], list[str]]:
    facts = [fact["fact_id"] for fact in fact_graph["facts"]]
    cards = [card["card_id"] for card in authority_packet]
    authorities = [
        source["comment_id"] for card in authority_packet for source in card["sources"]
    ]
    return facts, cards, authorities


def run_claim_verification(
    client: VLLMClient,
    *,
    case: Mapping[str, Any],
    answer: Mapping[str, Any],
    plan: Mapping[str, Any],
    fact_graph: Mapping[str, Any],
    authority_packet: Sequence[Mapping[str, Any]],
    method_dir: Path,
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    claim_payload = {
        "task": "backparse_long_form_answer",
        "case_id": case["case_id"],
        "method_id": "m6_claim_verified",
        "answer": answer,
        "irac_plan": plan,
        "fact_graph": fact_graph,
        "authority_packet": list(authority_packet),
        "allowed_relation_ids": plan["scallop_relations"],
    }
    claim_graph_raw, claim_metadata = timed_model(
        client,
        system_prompt=CLAIM_PROMPT_PATH.read_text(encoding="utf-8"),
        payload=claim_payload,
        schema_name="claim_graph",
        schema=generation_schema("claim_graph.schema.json"),
        max_tokens=9_000,
    )
    write_json(method_dir / "claim_graph_before_model_output.json", claim_graph_raw)
    claim_graph, normalization_before = normalize_claim_graph(claim_graph_raw)
    facts, cards, authorities = provenance_ids(fact_graph, authority_packet)
    violations_before = answer_contract_violations(
        answer,
        case_id=case["case_id"],
        method_id="m6_claim_verified",
        allowed_fact_ids=facts,
        allowed_card_ids=cards,
        allowed_authority_ids=authorities,
    )
    violations_before.extend(assess_irac_answer_alignment(answer, plan))
    violations_before.extend(
        validate_claim_graph(
            claim_graph,
            answer=answer,
            plan=plan,
            fact_graph=fact_graph,
            authority_packet=authority_packet,
        )
    )
    write_json(method_dir / "claim_graph_before.json", claim_graph)
    write_json(method_dir / "claim_violations_before.json", {"items": violations_before})
    verification: dict[str, Any] = {
        "violations_before": violations_before,
        "repair_attempted": False,
        "patch_audit": None,
        "violations_after": violations_before,
        "claim_graph_normalization_before": normalization_before,
        "claim_graph_normalization_after": None,
    }
    model_stages: dict[str, Any] = {"claim_graph_before": claim_metadata}
    final_answer = dict(answer)

    failed_ids = _failed_plan_sections(violations_before, plan)
    if failed_ids:
        verification["repair_attempted"] = True
        failed_units = [unit for unit in plan["units"] if unit["unit_id"] in failed_ids]
        patch_payload = {
            "task": "repair_failed_irac_sections",
            "case_id": case["case_id"],
            "method_id": "m6_claim_verified",
            "failed_section_ids": failed_ids,
            "violations": violations_before,
            "original_answer": answer,
            "failed_irac_units": failed_units,
            "fact_graph": fact_graph,
            "authority_packet": list(authority_packet),
        }
        patches, patch_metadata = timed_model(
            client,
            system_prompt=REPAIR_PROMPT_PATH.read_text(encoding="utf-8"),
            payload=patch_payload,
            schema_name="section_patch_bundle",
            schema=generation_schema("section_patch_bundle.schema.json"),
            max_tokens=6_000,
        )
        write_json(method_dir / "section_patches_model_output.json", patches)
        patches, patch_normalization = normalize_section_patch_bundle(patches)
        final_answer, patch_audit = apply_section_patches(
            answer, patches, failed_section_ids=failed_ids
        )
        patch_audit["normalization"] = patch_normalization
        post_repair_contract = answer_contract_violations(
            final_answer,
            case_id=case["case_id"],
            method_id="m6_claim_verified",
            allowed_fact_ids=facts,
            allowed_card_ids=cards,
            allowed_authority_ids=authorities,
        )
        write_json(method_dir / "section_patches.json", patches)
        write_json(method_dir / "answer_after_repair.json", final_answer)
        (method_dir / "answer_after_repair.md").write_text(
            render_long_form_markdown(final_answer), encoding="utf-8"
        )
        model_stages["section_repair"] = patch_metadata
        verification["patch_audit"] = patch_audit

        claim_payload["answer"] = final_answer
        claim_graph_after_raw, claim_after_metadata = timed_model(
            client,
            system_prompt=CLAIM_PROMPT_PATH.read_text(encoding="utf-8"),
            payload=claim_payload,
            schema_name="claim_graph",
            schema=generation_schema("claim_graph.schema.json"),
            max_tokens=9_000,
        )
        write_json(
            method_dir / "claim_graph_after_model_output.json", claim_graph_after_raw
        )
        claim_graph_after, normalization_after = normalize_claim_graph(
            claim_graph_after_raw
        )
        violations_after = post_repair_contract
        violations_after.extend(assess_irac_answer_alignment(final_answer, plan))
        violations_after.extend(
            validate_claim_graph(
                claim_graph_after,
                answer=final_answer,
                plan=plan,
                fact_graph=fact_graph,
                authority_packet=authority_packet,
            )
        )
        verification["violations_after"] = violations_after
        verification["claim_graph_normalization_after"] = normalization_after
        model_stages["claim_graph_after"] = claim_after_metadata
        write_json(method_dir / "claim_graph_after.json", claim_graph_after)
        write_json(
            method_dir / "claim_violations_after.json", {"items": violations_after}
        )
    return final_answer, model_stages, verification


def _failed_plan_sections(
    violations: Sequence[Mapping[str, str]], plan: Mapping[str, Any]
) -> list[str]:
    plan_ids = [unit["unit_id"] for unit in plan["units"]]
    explicit = {
        violation["section_id"]
        for violation in violations
        if violation.get("section_id") in plan_ids
    }
    if any(violation.get("section_id") == "document" for violation in violations):
        explicit.update(plan_ids)
    return [section_id for section_id in plan_ids if section_id in explicit]


def warm_structured_schemas(client: VLLMClient) -> dict[str, Any]:
    templates = {
        "fraud_fact_graph": (
            contract_schema("fraud_fact_graph.schema.json"),
            {
                "version": "1.0.0",
                "case_id": "warmup",
                "target_issue_id": "fraud",
                "actors": [
                    {
                        "entity_id": "actor_a",
                        "mentions": ["A"],
                        "roles": ["defendant", "beneficiary"],
                    },
                    {
                        "entity_id": "actor_b",
                        "mentions": ["B"],
                        "roles": ["deceived_person", "disposer", "property_owner"],
                    },
                ],
                "facts": [
                    {
                        "fact_id": "fact_001",
                        "fact_kind": "other",
                        "statement": "워밍업 사실",
                        "source_quote": "워밍업 사실",
                        "participants": ["actor_a"],
                        "epistemic_status": "given",
                        "issue_effects": [
                            {"issue_id": "fraud", "direction": "neutral"}
                        ],
                    }
                ],
                "profiles": [],
                "retrieval_queries": ["워밍업"],
                "unresolved_questions": [],
            },
        ),
        "fraud_assessment_bundle": (
            contract_schema("fraud_assessment_bundle.schema.json"),
            {
                "version": "1.0.0",
                "case_id": "warmup",
                "selected_card_ids": ["card"],
                "assessments": [
                    {
                        "assessment_id": "assessment_001",
                        "card_id": "card",
                        "status": "unknown",
                        "basis_fact_ids": [],
                        "counter_fact_ids": [],
                        "missing_facts": ["워밍업"],
                        "authority_comment_ids": ["source"],
                        "rationale": "워밍업",
                        "confidence": 0,
                    }
                ],
            },
        ),
        "long_form_answer": (
            generation_schema("long_form_answer.schema.json"),
            {
                "version": "1.0.0",
                "case_id": "warmup",
                "method_id": "m1_direct",
                "title": "워밍업",
                "sections": [
                    {
                        "section_id": "warmup_section",
                        "heading": "워밍업",
                        "body": "워밍업",
                        "cited_fact_ids": [],
                        "cited_card_ids": [],
                        "cited_authority_comment_ids": [],
                        "stated_conclusion": "unknown",
                    }
                ],
                "overall_conclusion": "undetermined",
                "summary": "워밍업",
            },
        ),
        "claim_graph": (
            generation_schema("claim_graph.schema.json"),
            {
                "version": "1.0.0",
                "case_id": "warmup",
                "method_id": "m6_claim_verified",
                "claims": [
                    {
                        "claim_id": "claim_001",
                        "section_id": "warmup_section",
                        "quote": "워밍업",
                        "claim_type": "fact",
                        "support_kind": "explicit_fact",
                        "polarity": "neutral",
                        "fact_ids": ["fact_001"],
                        "card_ids": [],
                        "authority_comment_ids": [],
                        "relation_ids": [],
                    }
                ],
                "section_conclusions": [
                    {"section_id": "warmup_section", "conclusion": "unknown"}
                ],
                "overall_conclusion": "undetermined",
            },
        ),
        "section_patch_bundle": (
            generation_schema("section_patch_bundle.schema.json"),
            {
                "version": "1.0.0",
                "case_id": "warmup",
                "method_id": "m6_claim_verified",
                "patches": [
                    {
                        "section_id": "warmup_section",
                        "heading": "워밍업",
                        "body": "워밍업",
                        "cited_fact_ids": [],
                        "cited_card_ids": [],
                        "cited_authority_comment_ids": [],
                        "stated_conclusion": "unknown",
                    }
                ],
            },
        ),
    }
    results: dict[str, Any] = {}
    for schema_name, (schema, template) in templates.items():
        output, metadata = timed_model(
            client,
            system_prompt="입력의 template JSON을 글자와 값의 의미를 바꾸지 말고 JSON 객체 하나로 출력하라.",
            payload={"template": template},
            schema_name=f"warm_{schema_name}",
            schema=schema,
            max_tokens=1_500,
        )
        Draft202012Validator(schema).validate(output)
        results[schema_name] = {
            **metadata,
            "schema_valid": True,
        }
    return results


def method_summary(
    *,
    method_id: str,
    started: float,
    answer: Mapping[str, Any],
    model_stages: Mapping[str, Any],
    host_stages: Mapping[str, float],
    answer_violations: Sequence[Mapping[str, str]],
    verification: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    usages = [
        stage.get("usage", {})
        for stage in model_stages.values()
        if isinstance(stage, Mapping) and "usage" in stage
    ]
    residual_violations = list(answer_violations)
    if verification:
        residual_violations.extend(verification.get("violations_after", []))
    return {
        "method_id": method_id,
        "status": (
            "completed_with_violations" if residual_violations else "completed"
        ),
        "warm_latency_seconds": time.perf_counter() - started,
        "model_call_count": len(usages),
        "model_prompt_tokens": sum(item.get("prompt_tokens", 0) or 0 for item in usages),
        "model_completion_tokens": sum(item.get("completion_tokens", 0) or 0 for item in usages),
        "model_stages": dict(model_stages),
        "host_stages_seconds": dict(host_stages),
        "answer": {
            "sha256": canonical_sha256(answer),
            "section_count": len(answer["sections"]),
            "body_characters": sum(len(section["body"]) for section in answer["sections"]),
            "overall_conclusion": answer["overall_conclusion"],
            "cited_fact_count": sum(
                len(section["cited_fact_ids"]) for section in answer["sections"]
            ),
            "cited_card_count": sum(
                len(section["cited_card_ids"]) for section in answer["sections"]
            ),
            "cited_authority_count": sum(
                len(section["cited_authority_comment_ids"])
                for section in answer["sections"]
            ),
        },
        "answer_validation_violations": list(answer_violations),
        "claim_verification": dict(verification) if verification else None,
    }


def run_matrix(
    *,
    base_url: str,
    model: str,
    api_key: str,
    run_dir: Path,
    report_path: Path,
    method_ids: Sequence[str] = METHOD_IDS,
    case_path: Path = CASE_PATH,
    case_id: str | None = None,
    temperature: float = 0.0,
    top_p: float | None = None,
    top_k: int | None = None,
) -> dict[str, Any]:
    selected_methods = tuple(method_ids)
    if not selected_methods:
        raise ValueError("at least one method is required")
    if len(selected_methods) != len(set(selected_methods)):
        raise ValueError("method_ids contains duplicates")
    unknown_methods = set(selected_methods) - set(METHOD_IDS)
    if unknown_methods:
        raise ValueError(f"unknown methods: {sorted(unknown_methods)}")
    case = load_case(case_path, case_id)
    validate_fraud_case(case)
    norm_cards = read_json(NORM_CARD_PATH)
    rule_ir, compiled_source = verify_symbolic_assets(case)
    client = SampledClient(
        VLLMClient(base_url=base_url, model=model, api_key=api_key),
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
    )
    run_dir.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    warmup = warm_structured_schemas(client)
    write_json(run_dir / "schema_warmup.json", warmup)
    methods: list[dict[str, Any]] = []

    for method_id in selected_methods:
        method_dir = run_dir / method_id
        method_dir.mkdir(parents=True, exist_ok=True)
        started = time.perf_counter()
        model_stages: dict[str, Any] = {}
        host_stages: dict[str, float] = {}
        alignment: list[dict[str, str]] = []
        verification: dict[str, Any] | None = None

        if method_id == "m1_direct":
            answer, model_stages["answer"], alignment = run_answer(
                client,
                case=case,
                method_id=method_id,
                method_dir=method_dir,
                context={"case_only": True},
                allowed_fact_ids=["case_text"],
            )

        elif method_id == "m2_rag":
            rag, host_stages["rag_retrieval"] = timed_host(
                lambda: build_fraud_rag_packet(
                    query_texts=build_fraud_rag_queries(case=case), top_k=6
                )
            )
            validate_fraud_rag_packet(rag)
            write_json(method_dir / "rag_packet.json", rag)
            cards = [item["card_id"] for item in rag["items"]]
            authorities = [
                source["comment_id"] for item in rag["items"] for source in item["sources"]
            ]
            answer, model_stages["answer"], alignment = run_answer(
                client,
                case=case,
                method_id=method_id,
                method_dir=method_dir,
                context={"rag_packet": rag},
                allowed_fact_ids=["case_text"],
                allowed_card_ids=cards,
                allowed_authority_ids=authorities,
            )

        elif method_id == "m3_factgraph_rag":
            fact_graph, model_stages["fact_graph"], normalization = run_fact_graph(
                client, case, method_dir
            )
            write_json(method_dir / "host_role_normalization.json", normalization)
            rag, host_stages["rag_retrieval"] = timed_host(
                lambda: build_fraud_rag_packet(
                    query_texts=build_fraud_rag_queries(case=case, fact_graph=fact_graph),
                    top_k=6,
                )
            )
            validate_fraud_rag_packet(rag)
            write_json(method_dir / "rag_packet.json", rag)
            facts = [fact["fact_id"] for fact in fact_graph["facts"]]
            cards = [item["card_id"] for item in rag["items"]]
            authorities = [
                source["comment_id"] for item in rag["items"] for source in item["sources"]
            ]
            answer, model_stages["answer"], alignment = run_answer(
                client,
                case=case,
                method_id=method_id,
                method_dir=method_dir,
                context={"fact_graph": fact_graph, "rag_packet": rag},
                allowed_fact_ids=facts,
                allowed_card_ids=cards,
                allowed_authority_ids=authorities,
            )

        else:
            fact_graph, model_stages["fact_graph"], normalization = run_fact_graph(
                client, case, method_dir
            )
            write_json(method_dir / "host_role_normalization.json", normalization)
            authority_packet, assessments, symbolic, symbolic_stages = run_symbolic_core(
                client,
                case=case,
                fact_graph=fact_graph,
                norm_cards=norm_cards,
                rule_ir=rule_ir,
                compiled_source=compiled_source,
                method_dir=method_dir,
            )
            model_stages["assessment_bundle"] = symbolic_stages["assessment_bundle"]
            host_stages["scallop"] = symbolic_stages["scallop"]["latency_seconds"]
            facts, cards, authorities = provenance_ids(fact_graph, authority_packet)
            plan = None
            if method_id in {"m5_irac_plan", "m6_claim_verified"}:
                plan, host_stages["irac_plan_compile"] = timed_host(
                    lambda: build_fraud_irac_plan(
                        case=case,
                        fact_graph=fact_graph,
                        assessment_bundle=assessments,
                        authority_packet=authority_packet,
                        symbolic_result=symbolic,
                    )
                )
                write_json(method_dir / "irac_plan.json", plan)
            context: dict[str, Any] = {
                "fact_graph": fact_graph,
                "authority_packet": authority_packet,
                "assessment_bundle": assessments,
                "symbolic_result": symbolic,
            }
            if plan is not None:
                context["irac_plan"] = plan
            if method_id == "m5_irac_plan":
                assert plan is not None
                (
                    answer,
                    alignment,
                    host_stages["irac_answer_compile"],
                ) = run_whole_irac_answer(
                    case=case,
                    method_dir=method_dir,
                    plan=plan,
                )
            else:
                answer, model_stages["answer"], alignment = run_answer(
                    client,
                    case=case,
                    method_id=method_id,
                    method_dir=method_dir,
                    context=context,
                    allowed_fact_ids=facts,
                    allowed_card_ids=cards,
                    allowed_authority_ids=authorities,
                    overall_conclusion=symbolic["legal_result"],
                    irac_plan=plan,
                )
            if method_id == "m6_claim_verified":
                assert plan is not None
                answer, claim_stages, verification = run_claim_verification(
                    client,
                    case=case,
                    answer=answer,
                    plan=plan,
                    fact_graph=fact_graph,
                    authority_packet=authority_packet,
                    method_dir=method_dir,
                )
                model_stages.update(claim_stages)
                alignment = answer_contract_violations(
                    answer,
                    case_id=case["case_id"],
                    method_id="m6_claim_verified",
                    allowed_fact_ids=facts,
                    allowed_card_ids=cards,
                    allowed_authority_ids=authorities,
                )
                alignment.extend(assess_irac_answer_alignment(answer, plan))

        method_report = method_summary(
            method_id=method_id,
            started=started,
            answer=answer,
            model_stages=model_stages,
            host_stages=host_stages,
            answer_violations=alignment,
            verification=verification,
        )
        published_json = report_path.parent / f"{method_id}_answer.json"
        published_markdown = report_path.parent / f"{method_id}_answer.md"
        write_json(published_json, answer)
        published_markdown.write_text(
            render_long_form_markdown(answer), encoding="utf-8"
        )
        method_report["answer"]["json_path"] = str(published_json)
        method_report["answer"]["markdown_path"] = str(published_markdown)
        write_json(method_dir / "method_report.json", method_report)
        methods.append(method_report)

    report = {
        "version": "1.0.0",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "completed",
        "case": {
            "case_id": case["case_id"],
            "source_record_id": case["source"].get(
                "sub_question_id",
                case["source"].get("source_case_id", case["case_id"]),
            ),
            "case_path": str(case_path),
            "case_selector": case_id,
            "reasoning_plan_id": select_fraud_reasoning_plan(
                {"profiles": case.get("required_profiles", [])}, case=case
            )["plan_id"],
            "rubric_supplied_to_model": False,
        },
        "experiment": {
            "model": model,
            "sampling": {
                "temperature": temperature,
                "top_p": top_p,
                "top_k": top_k,
                "thinking": False,
            },
            "method_order": list(selected_methods),
            "warm_latency_definition": (
                "wall time from method input to final answer after static structured schemas "
                "were prewarmed; model server startup and static schema warmup excluded; "
                "plan-specific dynamic schema compilation remains inside method latency"
            ),
            "plan_specific_schema_compilation": "included_in_method_latency",
            "independent_methods": True,
            "prefix_caching_required_disabled": True,
            "schema_warmup": warmup,
        },
        "symbolic_runtime": {
            "rule_set_id": rule_ir["rule_set_id"],
            "compiled_sha256": sha256_file(COMPILED_PATH),
            "scli_version": runtime_version(SCLI_PATH),
        },
        "methods": methods,
        "run_dir": str(run_dir),
    }
    write_json(report_path, report)
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--api-key", default="local-idpr")
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--report-path", type=Path, required=True)
    parser.add_argument("--case-path", type=Path, default=CASE_PATH)
    parser.add_argument(
        "--case-id",
        help="case_id to select when --case-path contains a case set",
    )
    parser.add_argument("--methods", nargs="+", choices=METHOD_IDS, default=list(METHOD_IDS))
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--top-p", type=float)
    parser.add_argument("--top-k", type=int)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = run_matrix(
        base_url=args.base_url,
        model=args.model,
        api_key=args.api_key,
        run_dir=args.run_dir,
        report_path=args.report_path,
        method_ids=args.methods,
        case_path=args.case_path,
        case_id=args.case_id,
        temperature=args.temperature,
        top_p=args.top_p,
        top_k=args.top_k,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
