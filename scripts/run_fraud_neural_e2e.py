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

from idpr.neural import (  # noqa: E402
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
ASSESS_PROMPT_PATH = PROJECT_ROOT / "prompts/fraud_standard_assess.md"
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
    return {
        "task": "assess_host_selected_fraud_norm_cards",
        "case_id": case["case_id"],
        "case_text": case["case_text"],
        "fact_graph": fact_graph,
        "selected_card_ids": selected_card_ids,
        "authority_packet": authority_packet,
        "status_semantics": {
            "satisfied": "카드 proposition이 사건 사실에서 충족됨",
            "not_satisfied": "카드 proposition이 사건 사실에 의해 반증됨",
            "unknown": "필요 사실이 없어 어느 쪽도 입증할 수 없음",
        },
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
) -> dict[str, Any]:
    case = read_json(CASE_PATH)
    rule_ir, compiled_source = verify_symbolic_assets(case)
    norm_cards = read_json(NORM_CARD_PATH)
    run_dir.mkdir(parents=True, exist_ok=True)
    model_stages: dict[str, Any] = {}

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
        fact_graph, model_stages["fact_graph"] = client.complete_json(
            system_prompt=FACT_PROMPT_PATH.read_text(encoding="utf-8"),
            payload=fact_graph_request(case),
            schema_name="fraud_fact_graph",
            schema=contract_schema("fraud_fact_graph.schema.json"),
            max_tokens=5_000,
        )
        write_json(run_dir / "fact_graph_model_output.json", fact_graph)
        validate_fraud_fact_graph(fact_graph, case)
        selected_card_ids = select_fraud_card_plan(fact_graph)
        authority_packet = build_authority_packet(selected_card_ids, norm_cards)
        assessment_bundle, model_stages["assessment_bundle"] = client.complete_json(
            system_prompt=ASSESS_PROMPT_PATH.read_text(encoding="utf-8"),
            payload=assessment_request(
                case=case,
                fact_graph=fact_graph,
                selected_card_ids=selected_card_ids,
                authority_packet=authority_packet,
            ),
            schema_name="fraud_assessment_bundle",
            schema=contract_schema("fraud_assessment_bundle.schema.json"),
            max_tokens=9_000,
        )
        write_json(run_dir / "assessment_bundle_model_output.json", assessment_bundle)
        artifact_origin = "gemma4_vllm"
    else:
        raise ValueError(f"unsupported mode: {mode}")

    validate_fraud_fact_graph(fact_graph, case)
    selected_card_ids = select_fraud_card_plan(fact_graph)
    authority_packet = build_authority_packet(selected_card_ids, norm_cards)
    validate_fraud_assessment_bundle(
        assessment_bundle,
        case=case,
        fact_graph=fact_graph,
        selected_card_ids=selected_card_ids,
        authority_packet=authority_packet,
    )
    write_json(run_dir / "validated_fact_graph.json", fact_graph)
    write_json(run_dir / "retrieved_authority_packet.json", {"cards": authority_packet})
    write_json(run_dir / "validated_assessment_bundle.json", assessment_bundle)

    scenario = build_scallop_scenario(
        case=case,
        fact_graph=fact_graph,
        assessment_bundle=assessment_bundle,
        selected_card_ids=selected_card_ids,
        authority_packet=authority_packet,
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
    report = {
        "version": "1.0.0",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status": "pass",
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
                len(card["sources"]) for card in authority_packet
            ),
            "authority_packet_sha256": canonical_sha256({"cards": authority_packet}),
            "host_derived_provable_count": len(scenario["assessments"]),
        },
        "model_stages": model_stages,
        "symbolic_runtime": {
            "rule_set_id": rule_ir["rule_set_id"],
            "compiled_sha256": sha256_file(COMPILED_PATH),
            "scli_version": runtime_version(SCLI_PATH),
            "observed_nonempty": observed,
        },
        "legal_result": legal_result(observed),
        "run_dir": str(run_dir),
    }
    write_json(report_path, report)
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
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = run_pipeline(
        mode=args.mode,
        run_dir=args.run_dir,
        report_path=args.report_path,
        base_url=args.base_url,
        model=args.model,
        api_key=args.api_key,
    )
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
