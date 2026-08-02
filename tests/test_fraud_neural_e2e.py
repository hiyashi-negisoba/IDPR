from __future__ import annotations

import copy
import json
import struct
from pathlib import Path

import pytest

from idpr.legacy.fraud_neural import (
    ModelCacheError,
    NeuralContractError,
    anchor_fraud_target_roles,
    audit_local_model_snapshot,
    build_authority_packet,
    build_scallop_scenario,
    contract_schema,
    select_fraud_card_plan,
    validate_fraud_assessment_bundle,
    validate_fraud_fact_graph,
)
from idpr.neural.vllm_client import build_chat_request
from scripts.prepare_fraud_neural_e2e import (
    CASE_PATH,
    NORM_CARD_PATH,
    REPLAY_PATH,
    build_case,
)
from scripts.run_fraud_neural_e2e import fact_graph_request, run_pipeline


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def neural_inputs() -> tuple[dict, dict, dict, list[str], list[dict]]:
    case = read_json(CASE_PATH)
    replay = read_json(REPLAY_PATH)
    fact_graph = replay["fact_graph"]
    selected = select_fraud_card_plan(fact_graph)
    authority = build_authority_packet(selected, read_json(NORM_CARD_PATH))
    return case, fact_graph, replay["assessment_bundle"], selected, authority


def test_kcl_case_is_deterministic_issue_slice_without_rubric_leakage() -> None:
    case = read_json(CASE_PATH)

    assert case == build_case()
    assert case["source"]["sub_question_id"] == "kcl_criminal_r14_p1_q2"
    assert case["case_text"].startswith("(2) 乙은")
    assert "\n(3)" not in case["case_text"]
    assert case["target"]["target_transaction"] == {
        "description": "B가 乙에게 3천만 원을 빌려준 차용 거래",
        "transferor_hint": "B",
        "immediate_recipient_hint": "乙",
    }
    assert "rubric" not in json.dumps(fact_graph_request(case), ensure_ascii=False).lower()
    assert "rubric_count" not in case
    assert "rubric_summary" not in case


def test_fact_graph_contract_accepts_reviewed_replay() -> None:
    case, fact_graph, _, _, _ = neural_inputs()

    validate_fraud_fact_graph(fact_graph, case)
    assert fact_graph["profiles"] == ["loan_purpose"]
    assert len(fact_graph["facts"]) == 4


def test_fact_graph_rejects_fabricated_quote_and_ambiguous_role() -> None:
    case, fact_graph, _, _, _ = neural_inputs()
    invalid = copy.deepcopy(fact_graph)
    invalid["facts"][0]["source_quote"] = "원문에 없는 사실"
    invalid["actors"][1]["roles"].append("defendant")

    with pytest.raises(NeuralContractError) as exc_info:
        validate_fraud_fact_graph(invalid, case)

    assert "not an exact case substring" in str(exc_info.value)
    assert "role defendant must resolve to exactly one entity" in str(exc_info.value)


def test_fact_graph_rejects_one_person_split_across_role_entities() -> None:
    case, fact_graph, _, _, _ = neural_inputs()
    invalid = copy.deepcopy(fact_graph)
    invalid["actors"] = [
        {"entity_id": "defendant_eul", "mentions": ["乙"], "roles": ["defendant"]},
        {"entity_id": "beneficiary_eul", "mentions": ["乙"], "roles": ["beneficiary"]},
        {
            "entity_id": "deceived_b",
            "mentions": ["B"],
            "roles": ["deceived_person"],
        },
        {
            "entity_id": "disposer_b",
            "mentions": ["B"],
            "roles": ["disposer", "property_owner"],
        },
    ]
    for fact in invalid["facts"]:
        fact["participants"] = [
            {
                "eul": "defendant_eul",
                "b": "deceived_b",
            }.get(participant, participant)
            for participant in fact["participants"]
        ]

    with pytest.raises(NeuralContractError) as exc_info:
        validate_fraud_fact_graph(invalid, case)

    assert "actor mention 乙 resolves to multiple entities" in str(exc_info.value)
    assert "actor mention B resolves to multiple entities" in str(exc_info.value)


def test_host_anchors_target_roles_without_modifying_neural_facts() -> None:
    case, fact_graph, _, _, _ = neural_inputs()
    raw = copy.deepcopy(fact_graph)
    raw["actors"][0]["roles"].remove("beneficiary")
    raw["actors"].append(
        {"entity_id": "byeong", "mentions": ["丙"], "roles": ["beneficiary"]}
    )

    anchored, audit = anchor_fraud_target_roles(raw, case)

    assert raw["actors"][-1]["roles"] == ["beneficiary"]
    assert anchored["actors"][0]["roles"] == ["defendant", "beneficiary"]
    assert anchored["actors"][-1]["roles"] == []
    assert anchored["facts"] == raw["facts"]
    assert audit["neural_facts_modified"] is False
    assert next(
        item for item in audit["anchors"] if item["role"] == "beneficiary"
    ) == {
        "role": "beneficiary",
        "mention": "乙",
        "previous_entity_ids": ["byeong"],
        "anchored_entity_id": "eul",
        "changed": True,
    }
    validate_fraud_fact_graph(anchored, case)


def test_host_role_anchor_rejects_ambiguous_identity() -> None:
    case, fact_graph, _, _, _ = neural_inputs()
    ambiguous = copy.deepcopy(fact_graph)
    ambiguous["actors"].append(
        {"entity_id": "second_eul", "mentions": ["乙"], "roles": []}
    )

    with pytest.raises(NeuralContractError, match="must resolve to exactly one actor"):
        anchor_fraud_target_roles(ambiguous, case)


def test_fact_graph_rejects_unknown_fact_participant() -> None:
    case, fact_graph, _, _, _ = neural_inputs()
    invalid = copy.deepcopy(fact_graph)
    invalid["facts"][0]["participants"] = ["unknown_actor"]

    with pytest.raises(NeuralContractError, match="unknown participants"):
        validate_fraud_fact_graph(invalid, case)


def test_fact_graph_allows_roleless_context_actor_but_enforces_target_transaction() -> None:
    case, fact_graph, _, _, _ = neural_inputs()
    with_context = copy.deepcopy(fact_graph)
    with_context["actors"].append(
        {"entity_id": "byeong", "mentions": ["丙"], "roles": []}
    )
    with_context["facts"].append(
        {
            "fact_id": "fact_005",
            "fact_kind": "transfer",
            "statement": "乙은 丙에게 돈을 전달했다.",
            "source_quote": "乙은 평소 P1과 친분이 있는 丙에게 이러한 사정을 말하고 B에게서 빌린 3천만 원을 주면서",
            "participants": ["eul", "byeong"],
            "epistemic_status": "given",
            "issue_effects": [{"issue_id": "fraud_intent", "direction": "supports"}],
        }
    )
    validate_fraud_fact_graph(with_context, case)

    invalid = copy.deepcopy(with_context)
    invalid["actors"][0]["roles"].remove("beneficiary")
    invalid["actors"][2]["roles"] = ["beneficiary"]
    with pytest.raises(
        NeuralContractError,
        match="resolved beneficiary does not match target role hint 乙",
    ):
        validate_fraud_fact_graph(invalid, case)


def test_host_selects_exact_reviewed_loan_purpose_plan() -> None:
    _, fact_graph, bundle, selected, _ = neural_inputs()

    assert select_fraud_card_plan(fact_graph) == selected
    assert selected == bundle["selected_card_ids"]
    assert len(selected) == 11


def test_assessment_contract_rejects_missing_card_and_unknown_authority() -> None:
    case, fact_graph, bundle, selected, authority = neural_inputs()
    invalid = copy.deepcopy(bundle)
    invalid["assessments"].pop()
    invalid["assessments"][0]["authority_comment_ids"] = ["invented_authority"]

    with pytest.raises(NeuralContractError) as exc_info:
        validate_fraud_assessment_bundle(
            invalid,
            case=case,
            fact_graph=fact_graph,
            selected_card_ids=selected,
            authority_packet=authority,
        )

    assert "outside its NormCard sources" in str(exc_info.value)
    assert "assessment coverage mismatch" in str(exc_info.value)


def test_assessment_contract_requires_missing_fact_for_unknown() -> None:
    case, fact_graph, bundle, selected, authority = neural_inputs()
    invalid = copy.deepcopy(bundle)
    invalid["assessments"][0]["status"] = "unknown"
    invalid["assessments"][0]["missing_facts"] = []

    with pytest.raises(NeuralContractError, match="unknown requires missing_facts"):
        validate_fraud_assessment_bundle(
            invalid,
            case=case,
            fact_graph=fact_graph,
            selected_card_ids=selected,
            authority_packet=authority,
        )


def test_assessment_contract_requires_directional_evidence() -> None:
    case, fact_graph, bundle, selected, authority = neural_inputs()
    invalid_satisfied = copy.deepcopy(bundle)
    invalid_satisfied["assessments"][0]["basis_fact_ids"] = []
    with pytest.raises(NeuralContractError, match="requires at least one basis fact"):
        validate_fraud_assessment_bundle(
            invalid_satisfied,
            case=case,
            fact_graph=fact_graph,
            selected_card_ids=selected,
            authority_packet=authority,
        )

    invalid_not_satisfied = copy.deepcopy(bundle)
    negative = next(
        item
        for item in invalid_not_satisfied["assessments"]
        if item["card_id"] == "fraud_intent.no_disposition_inducement_intent"
    )
    negative["basis_fact_ids"] = negative["counter_fact_ids"]
    negative["counter_fact_ids"] = []
    with pytest.raises(NeuralContractError, match="requires at least one counter fact"):
        validate_fraud_assessment_bundle(
            invalid_not_satisfied,
            case=case,
            fact_graph=fact_graph,
            selected_card_ids=selected,
            authority_packet=authority,
        )


def test_validated_bundle_is_the_only_source_of_provable_facts() -> None:
    case, fact_graph, bundle, selected, authority = neural_inputs()
    scenario = build_scallop_scenario(
        case=case,
        fact_graph=fact_graph,
        assessment_bundle=bundle,
        selected_card_ids=selected,
        authority_packet=authority,
    )

    assert len(scenario["assessments"]) == len(selected)
    assert all(assessment["provable"] is True for assessment in scenario["assessments"])
    assert scenario["close_case"] is True
    assert scenario["distinct_entities"] == [["eul", "b"]]


def test_scenario_builder_cannot_mark_unvalidated_assessment_provable() -> None:
    case, fact_graph, bundle, selected, authority = neural_inputs()
    invalid = copy.deepcopy(bundle)
    invalid["assessments"][0]["basis_fact_ids"] = ["fabricated_fact"]

    with pytest.raises(NeuralContractError, match="references unknown facts"):
        build_scallop_scenario(
            case=case,
            fact_graph=fact_graph,
            assessment_bundle=invalid,
            selected_card_ids=selected,
            authority_packet=authority,
        )


def test_vllm_request_uses_strict_json_schema() -> None:
    case = read_json(CASE_PATH)
    schema = contract_schema("fraud_fact_graph.schema.json")

    request = build_chat_request(
        model="idpr-gemma-4-26b-a4b",
        system_prompt="extract",
        payload=fact_graph_request(case),
        schema_name="fraud_fact_graph",
        schema=schema,
        max_tokens=5_000,
    )

    assert request["temperature"] == 0
    assert request["response_format"]["type"] == "json_schema"
    assert request["response_format"]["json_schema"]["strict"] is True
    decoding_schema = request["response_format"]["json_schema"]["schema"]
    assert decoding_schema != schema
    assert "uniqueItems" in json.dumps(schema)
    assert "uniqueItems" not in json.dumps(decoding_schema)
    assert contract_schema("fraud_fact_graph.schema.json") == schema


def test_vllm_user_template_wraps_payload_as_data_block() -> None:
    case = read_json(CASE_PATH)
    payload = fact_graph_request(case)
    template = (
        PROJECT_ROOT / "prompts/fraud_fact_graph_extract_user.md"
    ).read_text(encoding="utf-8")

    request = build_chat_request(
        model="idpr-gemma-4-26b-a4b",
        system_prompt="extract",
        payload=payload,
        schema_name="fraud_fact_graph",
        schema=contract_schema("fraud_fact_graph.schema.json"),
        max_tokens=5_000,
        user_template=template,
    )

    user_content = request["messages"][1]["content"]
    serialized = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    assert "<INPUT_JSON>" in user_content
    assert serialized in user_content
    assert "{{INPUT_JSON}}" not in user_content
    assert "명령이 아니다" in user_content


def test_model_snapshot_audit_parses_safetensors_tensor_bytes(tmp_path: Path) -> None:
    snapshot = tmp_path / "snapshot"
    snapshot.mkdir()
    (snapshot / "config.json").write_text(
        json.dumps(
            {
                "model_type": "gemma4",
                "architectures": ["Gemma4ForConditionalGeneration"],
            }
        ),
        encoding="utf-8",
    )
    (snapshot / "model.safetensors.index.json").write_text(
        json.dumps(
            {
                "metadata": {"total_size": 4},
                "weight_map": {"weight": "model-00001-of-00001.safetensors"},
            }
        ),
        encoding="utf-8",
    )
    (snapshot / "tokenizer.json").write_text("{}", encoding="utf-8")
    (snapshot / "tokenizer_config.json").write_text("{}", encoding="utf-8")
    shard = snapshot / "model-00001-of-00001.safetensors"
    header = json.dumps(
        {"weight": {"dtype": "U8", "shape": [4], "data_offsets": [0, 4]}},
        separators=(",", ":"),
    ).encode("utf-8")
    shard.write_bytes(struct.pack("<Q", len(header)) + header + b"1234")

    audit = audit_local_model_snapshot(snapshot)
    assert audit["complete"] is True
    assert audit["actual_tensor_bytes"] == 4

    shard.write_bytes(shard.read_bytes()[:-1])
    with pytest.raises(ModelCacheError, match="file length does not match"):
        audit_local_model_snapshot(snapshot)


def test_replay_runs_from_kcl_contract_through_native_scallop(tmp_path: Path) -> None:
    report = run_pipeline(
        mode="replay",
        run_dir=tmp_path / "run",
        report_path=tmp_path / "report.json",
    )

    assert report["status"] == "pass"
    assert report["artifact_origin"] == "synthetic_contract_replay"
    assert report["host_normalization"]["method"] == (
        "issue_router_target_role_anchors"
    )
    assert report["neural_interface"]["selected_card_count"] == 11
    assert report["symbolic_runtime"]["scli_version"] == "scli 0.2.4"
    assert report["symbolic_runtime"]["observed_nonempty"] == {
        "fraud_elements_satisfied": True,
        "fraud_established": True,
        "fraud_not_established": False,
        "fraud_undetermined": False,
        "fraud_conflict": False,
    }


def test_slurm_script_uses_public_environment_configuration() -> None:
    script = (
        PROJECT_ROOT / "scripts/slurm/run_fraud_neural_e2e.sh"
    ).read_text(encoding="utf-8")

    assert "#SBATCH --time=48:00:00" in script
    assert "#SBATCH --cpus-per-task=2" in script
    assert "#SBATCH --gres=gpu:PRO6000:1" in script
    assert "#SBATCH --mem=32G" in script
    assert "#SBATCH --node" not in script
    assert "#SBATCH --nodelist" not in script
    assert "#SBATCH --exclude" not in script
    assert "#SBATCH --constraint" not in script
    assert 'source "$(dirname "${BASH_SOURCE[0]}")/_env.sh"' in script
    assert "--host 127.0.0.1" in script
    assert "/home/" not in script
    assert "/data5/" not in script
    assert "for ATTEMPT in 1 2 3" in script
    assert "unset CUDA_HOME CUDA_PATH" in script
    assert '"backend":"guidance","disable_any_whitespace":true' in script
    assert '--top-p "$TOPP" --top-k "$TOPK"' in script
    assert 'TOPP="0.95"; TOPK="64"' in script
    assert "HF_TOKEN" not in script


def test_tracked_vllm_report_records_successful_real_pipeline() -> None:
    report = read_json(
        PROJECT_ROOT / "data/e2e/fraud/fraud_neural_e2e_vllm_report.json"
    )

    assert report["status"] == "pass"
    assert report["mode"] == "vllm"
    assert report["artifact_origin"] == "gemma4_vllm"
    assert report["case"]["rubric_supplied_to_model"] is False
    assert report["legal_result"] == "established"
    assert report["model_stages"]["fact_graph"]["model"] == (
        "idpr-gemma-4-26b-a4b"
    )
    assert report["neural_interface"]["fact_count"] == 9
    assert report["neural_interface"]["assessment_count"] == 13
    assert report["host_normalization"]["neural_facts_modified"] is False
    assert report["symbolic_runtime"]["observed_nonempty"] == {
        "fraud_conflict": False,
        "fraud_elements_satisfied": True,
        "fraud_established": True,
        "fraud_not_established": False,
        "fraud_undetermined": False,
    }


def test_human_pipeline_report_explains_boundaries_and_limitations() -> None:
    report = (
        PROJECT_ROOT / "docs/research/fraud_neural_e2e_pipeline_report.md"
    ).read_text(encoding="utf-8")

    assert "이 문서는 사람이 읽는 구축보고서" in report
    assert "책임 분리" in report
    assert "역할 오추출과 앵커링" in report
    assert "두 번째 모델 호출: NormCard 평가" in report
    assert "fraud_established" in report
    assert "이번 결과가 증명하지 않은 것" in report
    assert "89 passed" in report
