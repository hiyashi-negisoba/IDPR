from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from idpr.rulegen import RuleIRValidationError, compile_rule_ir, validate_rule_ir


PROJECT_ROOT = Path(__file__).resolve().parents[1]
COMMENTARY = PROJECT_ROOT / "data/commentary/kcl_criminal_v1_commentary_chunks.jsonl"
INDEX = PROJECT_ROOT / "data/rulegen/fraud/fraud_commentary_index.json"
REQUESTS = PROJECT_ROOT / "data/rulegen/fraud/fraud_rulegen_requests.jsonl"
RULE_IR = PROJECT_ROOT / "data/rulegen/fraud/fraud_rule_ir_exemplar.json"
SCALLOP = PROJECT_ROOT / "rules/exemplars/fraud_v1_candidate.scl"
PROCEDURAL_GATE = PROJECT_ROOT / "rules/exemplars/procedural_gate_v1_candidate.scl"


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def fraud_commentary() -> dict[str, dict]:
    return {
        row["comment_id"]: row
        for row in load_jsonl(COMMENTARY)
        if row["law_id"] == "001692" and row["article_no"] == "제347조"
    }


def test_fraud_rulegen_batches_cover_the_exact_article_pool() -> None:
    index = json.loads(INDEX.read_text(encoding="utf-8"))
    requests = load_jsonl(REQUESTS)
    expected_comment_ids = set(fraud_commentary())
    request_comment_ids = [
        chunk["comment_id"]
        for request in requests
        for chunk in request["commentary_chunks"]
    ]

    assert index["target_path"] == "commentary://001692/제347조"
    assert index["chunks"] == 127
    assert index["n_chars"] == 144018
    assert index["batches"] == 13
    assert len(requests) == 13
    assert len(request_comment_ids) == len(set(request_comment_ids)) == 127
    assert set(request_comment_ids) == expected_comment_ids
    assert all(request["batch"]["n_chars"] <= 12_000 for request in requests)
    assert all(request["constraints"]["preserve_disagreements"] for request in requests)


def test_fraud_rule_ir_is_provenance_valid_and_compiles_deterministically() -> None:
    payload = json.loads(RULE_IR.read_text(encoding="utf-8"))
    commentary = fraud_commentary()

    validate_rule_ir(payload, commentary)
    assert compile_rule_ir(payload, commentary) == SCALLOP.read_text(encoding="utf-8")
    assert payload["status"] == "draft"
    assert payload["legal_review"] == "pending"
    assert len(payload["legal_review_questions"]) == 4

    source_refs = [
        source
        for predicate in payload["predicates"]
        for source in predicate["source_refs"]
    ] + [source for rule in payload["rules"] for source in rule["source_refs"]]
    assert source_refs
    assert all(
        source["quote"] in commentary[source["comment_id"]]["document_text"]
        for source in source_refs
    )


def test_rule_ir_validator_rejects_fabricated_quote_and_unsafe_model_code() -> None:
    payload = json.loads(RULE_IR.read_text(encoding="utf-8"))
    commentary = fraud_commentary()

    bad_quote = copy.deepcopy(payload)
    bad_quote["predicates"][2]["source_refs"][0]["quote"] = "출처에 없는 문장"
    with pytest.raises(RuleIRValidationError, match="exact commentary substring"):
        validate_rule_ir(bad_quote, commentary)

    bad_identifier = copy.deepcopy(payload)
    bad_identifier["predicates"][2]["id"] = "deception); run_untrusted_code("
    with pytest.raises(RuleIRValidationError, match="valid Scallop identifier"):
        validate_rule_ir(bad_identifier, commentary)


def test_fraud_and_procedural_exemplars_enforce_positive_evidence_gates() -> None:
    fraud = SCALLOP.read_text(encoding="utf-8")
    procedure = PROCEDURAL_GATE.read_text(encoding="utf-8")

    assert "provable(f)" in fraud
    assert "proven_disposition_acquisition_causal" in fraud
    assert 'active_policy("kr_fraud_damage_and_unlawful_intent")' in fraud
    assert "status: draft" in fraud
    assert "admissibility_review_complete(e)" in procedure
    assert "not excluded" not in procedure
    assert "~excluded" not in procedure


def test_rulegen_contracts_and_prompts_exist() -> None:
    contract_names = {
        "rulegen_request.schema.json",
        "norm_candidate_batch.schema.json",
        "rule_ir.schema.json",
    }
    for name in contract_names:
        schema = json.loads(
            (PROJECT_ROOT / "docs/contracts" / name).read_text(encoding="utf-8")
        )
        assert schema["type"] == "object"

    extract_prompt = (
        PROJECT_ROOT / "prompts/rulegen_extract_norm_candidates.md"
    ).read_text(encoding="utf-8")
    merge_prompt = (PROJECT_ROOT / "prompts/rulegen_merge_rule_ir.md").read_text(
        encoding="utf-8"
    )
    assert "exact source reference" in extract_prompt
    assert "never output executable code directly" in merge_prompt
