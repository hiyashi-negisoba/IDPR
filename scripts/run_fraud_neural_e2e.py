from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from idpr.legacy.fraud_neural import (  # noqa: E402
    NeuralContractError,
    anchor_fraud_target_roles,
    build_authority_packet,
    build_scallop_scenario,
    contract_schema,
    select_fraud_card_plan,
    validate_fraud_assessment_bundle,
    validate_fraud_fact_graph,
)
from idpr.legacy.fraud_planning import (  # noqa: E402
    build_fraud_assessment_context,
    reasoning_plan_card_ids,
    select_fraud_reasoning_plan,
)
from idpr.legacy.fraud_generation import (  # noqa: E402
    GenerationContractError,
    build_fraud_irac_plan,
    compile_fraud_whole_irac_answer,
    render_long_form_markdown,
)
from idpr.neural.vllm_client import VLLMClient, VLLMClientError  # noqa: E402
from idpr.rulegen.scallop_runtime import (  # noqa: E402
    run_scenario,
    runtime_version,
    sha256_file,
)


CASE_PATH = PROJECT_ROOT / "data/e2e/fraud/kcl_r14_p1_q2_case.json"
REPLAY_PATH = PROJECT_ROOT / "data/e2e/fraud/kcl_r14_p1_q2_replay_neural.json"
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
QUERY_RELATIONS = (
    "fraud_elements_satisfied",
    "fraud_established",
    "fraud_not_established",
    "fraud_undetermined",
    "fraud_conflict",
)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


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
    selected_card_ids: list[str],
    authority_packet: list[dict[str, Any]],
) -> dict[str, Any]:
    assessment_context = build_fraud_assessment_context(
        fact_graph,
        case=case,
        selected_card_ids=selected_card_ids,
    )
    if [item["card_id"] for item in assessment_context] != selected_card_ids:
        raise RuntimeError("assessment context order differs from selected cards")
    return {
        "task": "assess_host_selected_fraud_norm_cards",
        "case_id": case["case_id"],
        "case_text": case["case_text"],
        "fact_graph": fact_graph,
        "selected_card_ids": selected_card_ids,
        "assessment_context": assessment_context,
        "authority_packet": authority_packet,
    }


def verify_symbolic_assets(case: Mapping[str, Any]) -> tuple[dict[str, Any], str]:
    rule_ir = read_json(RULE_IR_PATH)
    manifest = read_json(COMPILE_MANIFEST_PATH)
    if case["rule_set_id"] != rule_ir["rule_set_id"]:
        raise RuntimeError("case and RuleIR rule_set_id do not match")
    if manifest.get("rule_set_id") != rule_ir["rule_set_id"]:
        raise RuntimeError("compile manifest and RuleIR rule_set_id do not match")
    if manifest.get("output", {}).get("sha256") != sha256_file(COMPILED_PATH):
        raise RuntimeError("compiled Scallop source differs from its approved manifest")
    if not SCLI_PATH.is_file():
        raise RuntimeError("pinned scli runtime is missing")
    return rule_ir, COMPILED_PATH.read_text(encoding="utf-8")


def run_pipeline(
    *,
    mode: str,
    run_dir: Path,
    report_path: Path,
    base_url: str | None = None,
    model: str | None = None,
    api_key: str = "local-idpr",
    temperature: float = 0.0,
    top_p: float | None = None,
    top_k: int | None = None,
    enable_thinking: bool = False,
) -> dict[str, Any]:
    case = read_json(CASE_PATH)
    rule_ir, compiled_source = verify_symbolic_assets(case)
    norm_cards = read_json(NORM_CARD_PATH)
    run_dir.mkdir(parents=True, exist_ok=True)
    model_stages: dict[str, Any] = {}
    host_normalization: dict[str, Any]

    if mode == "replay":
        replay = read_json(REPLAY_PATH)
        if replay.get("artifact_type") != "synthetic_contract_replay":
            raise RuntimeError("replay input is not marked as synthetic")
        fact_graph = replay["fact_graph"]
        assessment_bundle = replay["assessment_bundle"]
        artifact_origin = "synthetic_contract_replay"
    elif mode == "vllm":
        if not base_url or not model:
            raise ValueError("vllm mode requires --base-url and --model")
        client = VLLMClient(base_url=base_url, model=model, api_key=api_key)
        chat_template_kwargs = {"enable_thinking": True} if enable_thinking else None
        # Thinking shares the completion budget with the final JSON, so give
        # reasoning runs enough headroom to reach the answer channel.
        fact_max_tokens = 12_000 if enable_thinking else 5_000
        assess_max_tokens = 20_000 if enable_thinking else 9_000
        try:
            fact_graph, model_stages["fact_graph"] = client.complete_json(
                system_prompt=FACT_PROMPT_PATH.read_text(encoding="utf-8"),
                user_template=FACT_USER_PROMPT_PATH.read_text(encoding="utf-8"),
                payload=fact_graph_request(case),
                schema_name="fraud_fact_graph",
                schema=contract_schema("fraud_fact_graph.schema.json"),
                max_tokens=fact_max_tokens,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                chat_template_kwargs=chat_template_kwargs,
            )
        except VLLMClientError as exc:
            return _graceful_failure(case, mode, str(exc), run_dir, report_path)
        write_json(run_dir / "fact_graph_model_output.json", fact_graph)
        fact_graph, host_normalization = anchor_fraud_target_roles(fact_graph, case)
        write_json(run_dir / "fact_graph_role_anchored.json", fact_graph)
        validate_fraud_fact_graph(fact_graph, case)
        selected_card_ids = select_fraud_card_plan(fact_graph)
        assessment_authority_packet = build_authority_packet(selected_card_ids, norm_cards)
        try:
            assessment_bundle, model_stages["assessment_bundle"] = client.complete_json(
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
                max_tokens=assess_max_tokens,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                chat_template_kwargs=chat_template_kwargs,
            )
        except VLLMClientError as exc:
            return _graceful_failure(case, mode, str(exc), run_dir, report_path)
        write_json(run_dir / "assessment_bundle_model_output.json", assessment_bundle)
        artifact_origin = "gemma4_vllm"
    else:
        raise ValueError(f"unsupported mode: {mode}")

    if mode == "replay":
        fact_graph, host_normalization = anchor_fraud_target_roles(fact_graph, case)
    validate_fraud_fact_graph(fact_graph, case)
    selected_card_ids = select_fraud_card_plan(fact_graph)
    assessment_authority_packet = build_authority_packet(selected_card_ids, norm_cards)
    validate_fraud_assessment_bundle(
        assessment_bundle,
        case=case,
        fact_graph=fact_graph,
        selected_card_ids=selected_card_ids,
        authority_packet=assessment_authority_packet,
    )
    write_json(run_dir / "validated_fact_graph.json", fact_graph)
    write_json(run_dir / "retrieved_authority_packet.json", {"cards": assessment_authority_packet})
    write_json(run_dir / "validated_assessment_bundle.json", assessment_bundle)

    scenario = build_scallop_scenario(
        case=case,
        fact_graph=fact_graph,
        assessment_bundle=assessment_bundle,
        selected_card_ids=selected_card_ids,
        authority_packet=assessment_authority_packet,
    )
    write_json(run_dir / "scallop_scenario.json", scenario)
    results = run_scenario(
        rule_ir=rule_ir,
        compiled_source=compiled_source,
        scenario=scenario,
        query_relations=QUERY_RELATIONS,
        scli_path=SCLI_PATH,
        work_dir=run_dir / "scallop_programs",
    )
    observed = {relation: result["nonempty"] for relation, result in results.items()}
    final_legal_result = legal_result(observed)
    report = {
        "version": "1.0.0",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": (
            "fail"
            if final_legal_result == "blocked_without_final_conclusion"
            else "pass"
        ),
        "mode": mode,
        "artifact_origin": artifact_origin,
        "case": {
            "case_id": case["case_id"],
            "source_sub_question_id": case["source"]["sub_question_id"],
            "case_text_sha256": case["source"]["case_text_sha256"],
            "rubric_supplied_to_model": False,
        },
        "neural_interface": {
            "fact_count": len(fact_graph["facts"]),
            "fact_graph_sha256": canonical_sha256(fact_graph),
            "profiles": fact_graph["profiles"],
            "selected_card_count": len(selected_card_ids),
            "assessment_count": len(assessment_bundle["assessments"]),
            "assessment_bundle_sha256": canonical_sha256(assessment_bundle),
            "authority_source_count": sum(
                len(card["sources"]) for card in assessment_authority_packet
            ),
            "authority_packet_sha256": canonical_sha256({"cards": assessment_authority_packet}),
            "host_derived_provable_count": len(scenario["assessments"]),
        },
        "model_stages": model_stages,
        "host_normalization": host_normalization,
        "symbolic_runtime": {
            "rule_set_id": rule_ir["rule_set_id"],
            "compiled_sha256": sha256_file(COMPILED_PATH),
            "scli_version": runtime_version(SCLI_PATH),
            "observed_nonempty": observed,
        },
        "legal_result": final_legal_result,
        "run_dir": str(run_dir),
    }
    if report["status"] == "pass" and mode == "vllm":
        reasoning_plan = select_fraud_reasoning_plan(fact_graph, case=case)
        plan_card_ids = reasoning_plan_card_ids(reasoning_plan)
        whole_authority_packet = build_authority_packet(plan_card_ids, norm_cards)
        irac_plan = build_fraud_irac_plan(
            case=case,
            fact_graph=fact_graph,
            assessment_bundle=assessment_bundle,
            authority_packet=whole_authority_packet,
            symbolic_result={
                "legal_result": final_legal_result,
                "observed_nonempty": observed,
            },
        )
        write_json(run_dir / "m5_irac_plan.json", irac_plan)
        long_form_answer = compile_fraud_whole_irac_answer(plan=irac_plan, case=case)
        write_json(run_dir / "m5_irac_plan_answer.json", long_form_answer)
        (run_dir / "m5_irac_plan_answer.md").write_text(
            render_long_form_markdown(long_form_answer), encoding="utf-8",
        )

    write_json(report_path, report)
    if report["status"] != "pass":
        raise RuntimeError(
            "Scallop produced no final established/not-established/undetermined/conflict relation"
        )
    return report


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


def _graceful_failure(
    case: Mapping[str, Any],
    mode: str,
    error_msg: str,
    run_dir: Path,
    report_path: Path,
) -> dict[str, Any]:
    report = {
        "version": "1.0.0",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "fail",
        "mode": mode,
        "case": {"case_id": case["case_id"]},
        "error": error_msg,
        "run_dir": str(run_dir),
    }
    write_json(report_path, report)
    return report


def canonical_sha256(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("replay", "vllm"), required=True)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--report-path", type=Path, required=True)
    parser.add_argument("--base-url")
    parser.add_argument("--model")
    parser.add_argument("--api-key", default="local-idpr")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--top-p", type=float)
    parser.add_argument("--top-k", type=int)
    parser.add_argument("--enable-thinking", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        report = run_pipeline(
            mode=args.mode,
            run_dir=args.run_dir,
            report_path=args.report_path,
            base_url=args.base_url,
            model=args.model,
            api_key=args.api_key,
            temperature=args.temperature,
            top_p=args.top_p,
            top_k=args.top_k,
            enable_thinking=args.enable_thinking,
        )
    except (NeuralContractError, GenerationContractError) as exc:
        # Contract failures must replace any previous report file, otherwise a
        # stale success report from an earlier run keeps masquerading as current.
        _graceful_failure(
            read_json(CASE_PATH), args.mode, str(exc), args.run_dir, args.report_path
        )
        raise
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
