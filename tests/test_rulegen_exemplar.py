from __future__ import annotations

import copy
import json
from collections import Counter
from pathlib import Path

import pytest

from idpr.rulegen import (
    NormCandidateValidationError,
    NormCandidatePatchValidationError,
    NormCardValidationError,
    RuleIRValidationError,
    RulegenCritiqueValidationError,
    compile_rule_ir,
    apply_norm_candidate_patch,
    repair_ocr_interrupted_candidate_quotes,
    validate_norm_candidate_batch,
    validate_norm_card_set,
    validate_rule_ir,
    validate_rulegen_critique,
)
from scripts.build_fraud_legal_review import AUDITED_CARD_MAPPINGS
from scripts.run_fraud_norm_card_merge import build_module_payloads
from scripts.run_fraud_norm_card_critics import (
    build_jobs as build_norm_card_critic_jobs,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
COMMENTARY = PROJECT_ROOT / "data/commentary/kcl_criminal_v1_commentary_chunks.jsonl"
INDEX = PROJECT_ROOT / "data/rulegen/fraud/fraud_commentary_index.json"
REQUESTS = PROJECT_ROOT / "data/rulegen/fraud/fraud_rulegen_requests.jsonl"
NORM_CARDS = PROJECT_ROOT / "data/rulegen/fraud/fraud_norm_card_set_exemplar.json"
REVIEW_ADDENDUM = (
    PROJECT_ROOT / "data/rulegen/fraud/fraud_pass1_001_review_addendum.json"
)
REVISION3_ADJUDICATION = (
    PROJECT_ROOT
    / "data/rulegen/fraud/fraud_pass1_001_revision3_adjudication.json"
)
REVISION4_ADJUDICATION = (
    PROJECT_ROOT
    / "data/rulegen/fraud/fraud_pass1_001_revision4_adjudication.json"
)
REVISION5_ADJUDICATION = (
    PROJECT_ROOT
    / "data/rulegen/fraud/fraud_pass1_001_revision5_adjudication.json"
)
REVISION5_PATCH = (
    PROJECT_ROOT / "data/rulegen/fraud/fraud_pass1_001_revision5_patch.json"
)
FINAL_CANDIDATES = (
    PROJECT_ROOT
    / "data/rulegen/fraud/fraud_norm_candidate_batch_pass1_001_exemplar.json"
)
FINAL_ADJUDICATION = (
    PROJECT_ROOT
    / "data/rulegen/fraud/fraud_pass1_001_revision6_final_adjudication.json"
)
FEWSHOT_GOLD = (
    PROJECT_ROOT
    / "data/rulegen/fraud/fraud_norm_candidate_fewshot_gold.json"
)
CANDIDATE_MANIFEST = (
    PROJECT_ROOT
    / "data/rulegen/fraud/fraud_norm_candidate_manifest.json"
)
NORM_CARD_MANIFEST = (
    PROJECT_ROOT / "data/rulegen/fraud/fraud_norm_card_manifest.json"
)
NORM_CARD_CRITIC_MANIFEST = (
    PROJECT_ROOT
    / "data/rulegen/fraud/norm_card_reviews"
    / "fraud_norm_cards_critic_v4_final/manifest.json"
)
NORM_CARD_REVIEW_QUEUE = (
    PROJECT_ROOT / "data/rulegen/fraud/fraud_norm_card_review_queue.json"
)
HUMAN_REVIEW_DECISIONS = (
    PROJECT_ROOT / "data/rulegen/fraud/fraud_human_review_decisions.jsonl"
)
RULE_IR_READINESS = (
    PROJECT_ROOT / "data/rulegen/fraud/fraud_rule_ir_readiness.json"
)
NORM_CARD_REMEDIATION_LEDGER = (
    PROJECT_ROOT / "data/rulegen/fraud/fraud_norm_card_remediation_ledger.json"
)
NORM_CARD_AUDIT = (
    PROJECT_ROOT / "data/rulegen/fraud/fraud_norm_card_audit.json"
)
POLICY_REVIEW_QUEUE = (
    PROJECT_ROOT / "data/rulegen/fraud/fraud_policy_review_queue.json"
)
POLICY_REVIEW_DECISIONS = (
    PROJECT_ROOT / "data/rulegen/fraud/fraud_policy_review_decisions.jsonl"
)
POLICY_RESOLUTION_AUDIT = (
    PROJECT_ROOT / "data/rulegen/fraud/fraud_policy_resolution_audit.json"
)
CORE_SELECTION_AUDIT = (
    PROJECT_ROOT / "data/rulegen/fraud/fraud_core_rule_selection_audit.json"
)
CORE_REVIEW_QUEUE = (
    PROJECT_ROOT / "data/rulegen/fraud/fraud_core_rule_review_queue.json"
)
CORE_REVIEW_DECISIONS = (
    PROJECT_ROOT / "data/rulegen/fraud/fraud_core_rule_review_decisions.jsonl"
)
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


def request_comment_ids() -> dict[str, set[str]]:
    return {
        request["request_id"]: {
            chunk["comment_id"] for chunk in request["commentary_chunks"]
        }
        for request in load_jsonl(REQUESTS)
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


def test_fraud_norm_cards_are_request_and_source_grounded() -> None:
    payload = json.loads(NORM_CARDS.read_text(encoding="utf-8"))
    commentary = fraud_commentary()

    validate_norm_card_set(payload, commentary, request_comment_ids())
    assert payload["construction"] == "human_exemplar"
    assert payload["status"] == "draft"
    assert payload["legal_review"] == "pending"
    assert len(payload["cards"]) == 8
    assert {
        card["formalization"] for card in payload["cards"]
    } >= {"deterministic_rule", "standard_input", "policy_variant"}
    unlawful_intent = next(
        card for card in payload["cards"] if card["id"] == "fraud.unlawful_gain_intent"
    )
    assert unlawful_intent["authority_basis"] == "commentary_reported_precedent"
    assert len(unlawful_intent["source_refs"]) == 4
    assert len(unlawful_intent["candidate_refs"]) == 4
    assert all(
        len(source["quote"]) <= 300
        for card in payload["cards"]
        for source in card["source_refs"]
    )


def test_fraud_rule_ir_is_provenance_valid_and_compiles_deterministically() -> None:
    payload = json.loads(RULE_IR.read_text(encoding="utf-8"))
    norm_cards = json.loads(NORM_CARDS.read_text(encoding="utf-8"))
    commentary = fraud_commentary()

    validate_rule_ir(payload, commentary, norm_cards)
    assert compile_rule_ir(payload, commentary, norm_cards) == SCALLOP.read_text(
        encoding="utf-8"
    )
    assert payload["version"] == "1.1.0"
    assert payload["norm_card_scope"]["card_set_id"] == norm_cards["card_set_id"]
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
    norm_cards = json.loads(NORM_CARDS.read_text(encoding="utf-8"))
    commentary = fraud_commentary()

    bad_quote = copy.deepcopy(payload)
    bad_quote["predicates"][2]["source_refs"][0]["quote"] = "출처에 없는 문장"
    with pytest.raises(RuleIRValidationError, match="exact commentary substring"):
        validate_rule_ir(bad_quote, commentary, norm_cards)

    bad_identifier = copy.deepcopy(payload)
    bad_identifier["predicates"][2]["id"] = "deception); run_untrusted_code("
    with pytest.raises(RuleIRValidationError, match="does not match"):
        validate_rule_ir(bad_identifier, commentary, norm_cards)

    bad_card_link = copy.deepcopy(payload)
    bad_card_link["predicates"][2]["norm_card_ids"] = ["fraud.mistake"]
    with pytest.raises(RuleIRValidationError, match="not backed by its norm cards"):
        validate_rule_ir(bad_card_link, commentary, norm_cards)


def test_norm_card_validator_rejects_fabricated_quote_and_request_scope() -> None:
    payload = json.loads(NORM_CARDS.read_text(encoding="utf-8"))
    commentary = fraud_commentary()

    bad_quote = copy.deepcopy(payload)
    bad_quote["cards"][0]["source_refs"][0]["quote"] = "출처에 없는 문장"
    with pytest.raises(NormCardValidationError, match="exact commentary substring"):
        validate_norm_card_set(bad_quote, commentary, request_comment_ids())

    bad_request = copy.deepcopy(payload)
    bad_request["cards"][0]["request_ids"] = ["fraud.article347.pass1.999"]
    with pytest.raises(NormCardValidationError, match="unknown request_ids"):
        validate_norm_card_set(bad_request, commentary, request_comment_ids())


def test_raw_norm_candidate_batch_is_bounded_by_its_request() -> None:
    request = load_jsonl(REQUESTS)[0]
    chunk = request["commentary_chunks"][0]
    payload = {
        "request_id": request["request_id"],
        "status": "draft",
        "candidates": [
            {
                "candidate_id": "fraud.raw.001",
                "norm_kind": "definition",
                "polarity": "positive",
                "proposition": "Source-bounded test candidate.",
                "source_refs": [
                    {
                        "comment_id": chunk["comment_id"],
                        "section_path": chunk["section_path"],
                        "quote": chunk["document_text"][:20],
                    }
                ],
                "review_required": False,
            }
        ],
        "unresolved_questions": [],
    }

    validate_norm_candidate_batch(payload, request)
    payload["candidates"][0]["source_refs"][0]["comment_id"] = "outside-request"
    with pytest.raises(NormCandidateValidationError, match="outside source_scope"):
        validate_norm_candidate_batch(payload, request)


def test_ocr_interrupted_quote_repair_is_exact_and_high_confidence() -> None:
    request = load_jsonl(REQUESTS)[0]
    commentary = {
        row["comment_id"]: row for row in request["commentary_chunks"]
    }
    comment_id = "comm_001692_제347조_Ⅲ_7"
    payload = {
        "request_id": request["request_id"],
        "status": "draft",
        "candidates": [
            {
                "candidate_id": "fraud.raw.ocr",
                "norm_kind": "exception",
                "polarity": "exception",
                "proposition": "자기 점유 타인 재물에는 횡령죄 경계가 적용된다.",
                "source_refs": [
                    {
                        "comment_id": comment_id,
                        "section_path": "Ⅲ",
                        "quote": "자기점유의 타인의 재물을 영득한 경우에는 기망행위가 있어도 횡령죄만 성립한다.",
                    }
                ],
                "review_required": True,
            }
        ],
        "unresolved_questions": [],
    }

    repaired, records = repair_ocr_interrupted_candidate_quotes(
        payload, commentary
    )

    assert len(records) == 1
    assert len(repaired["candidates"][0]["source_refs"]) == 2
    validate_norm_candidate_batch(repaired, request)

    fabricated = copy.deepcopy(payload)
    fabricated["candidates"][0]["source_refs"][0]["quote"] = (
        "출처에 전혀 존재하지 않는 조작된 인용문입니다. 충분히 긴 문자열입니다."
    )
    unchanged, records = repair_ocr_interrupted_candidate_quotes(
        fabricated, commentary
    )
    assert not records
    with pytest.raises(NormCandidateValidationError):
        validate_norm_candidate_batch(unchanged, request)


def test_quote_repair_handles_length_and_adjacent_chunk_boundaries() -> None:
    long_quote = "가" * 301
    commentary = {
        "comment.1": {
            "comment_id": "comment.1",
            "section_path": "Ⅰ",
            "document_text": long_quote + " 앞부분에 이어지는 긴 문장",
        },
        "comment.2": {
            "comment_id": "comment.2",
            "section_path": "Ⅰ",
            "document_text": "뒷부분으로 계속되는 문장입니다.",
        },
    }
    payload = {
        "request_id": "request.1",
        "status": "draft",
        "candidates": [
            {
                "candidate_id": "fraud.long-quote",
                "norm_kind": "definition",
                "polarity": "positive",
                "proposition": "긴 인용",
                "source_refs": [
                    {
                        "comment_id": "comment.1",
                        "section_path": "Ⅰ",
                        "quote": long_quote,
                    }
                ],
                "review_required": False,
            },
            {
                "candidate_id": "fraud.chunk-boundary",
                "norm_kind": "definition",
                "polarity": "positive",
                "proposition": "경계 인용",
                "source_refs": [
                    {
                        "comment_id": "comment.2",
                        "section_path": "Ⅰ",
                        "quote": (
                            "앞부분에 이어지는 긴 문장 "
                            "뒷부분으로 계속되는 문장입니다."
                        ),
                    }
                ],
                "review_required": False,
            },
        ],
        "unresolved_questions": [],
    }
    request = {
        "request_id": "request.1",
        "commentary_chunks": list(commentary.values()),
    }

    repaired, records = repair_ocr_interrupted_candidate_quotes(
        payload, commentary
    )

    assert len(records) == 2
    assert len(repaired["candidates"][0]["source_refs"]) == 2
    assert [
        ref["comment_id"]
        for ref in repaired["candidates"][1]["source_refs"]
    ] == ["comment.1", "comment.2"]
    validate_norm_candidate_batch(repaired, request)


def test_rulegen_critic_is_advisory_and_source_bounded() -> None:
    source_ref = json.loads(NORM_CARDS.read_text(encoding="utf-8"))["cards"][0][
        "source_refs"
    ][0]
    critic_ref = {
        "comment_id": source_ref["comment_id"],
        "section_path": source_ref["section_path"],
    }
    payload = {
        "version": "1.1.0",
        "report_id": "fraud.critic.001",
        "stage": "norm_card_set",
        "target_id": "kr.fraud.article347.norms.v1_exemplar",
        "status": "draft",
        "verdict": "revise",
        "findings": [
            {
                "finding_id": "fraud.critic.001.finding.001",
                "severity": "hard",
                "type": "overgeneralization",
                "target_path": "$.cards[0].proposition",
                "message": "The proposition is broader than its exact source.",
                "source_refs": [critic_ref],
                "recommended_action": "Narrow the proposition to the quoted rule.",
            }
        ],
        "summary": "One source-entailment defect requires revision.",
        "review_required": True,
    }

    validate_rulegen_critique(
        payload,
        expected_stage="norm_card_set",
        expected_target_id="kr.fraud.article347.norms.v1_exemplar",
        allowed_source_refs=[source_ref],
    )

    invalid = copy.deepcopy(payload)
    invalid["verdict"] = "pass"
    with pytest.raises(RulegenCritiqueValidationError, match="pass verdict"):
        validate_rulegen_critique(
            invalid,
            expected_stage="norm_card_set",
            expected_target_id="kr.fraud.article347.norms.v1_exemplar",
            allowed_source_refs=[source_ref],
        )


def test_fraud_pilot_review_addendum_is_source_bounded() -> None:
    request = load_jsonl(REQUESTS)[0]
    commentary = {
        row["comment_id"]: row for row in request["commentary_chunks"]
    }
    payload = json.loads(REVIEW_ADDENDUM.read_text(encoding="utf-8"))

    validate_rulegen_critique(
        payload,
        expected_stage="norm_candidate_batch",
        expected_target_id=request["request_id"],
        commentary_by_id=commentary,
        allowed_comment_ids=set(commentary),
    )
    assert len(payload["findings"]) == 13
    assert all(finding["source_refs"] for finding in payload["findings"])


def test_fraud_revision3_adjudication_is_source_bounded() -> None:
    request = load_jsonl(REQUESTS)[0]
    commentary = {
        row["comment_id"]: row for row in request["commentary_chunks"]
    }
    payload = json.loads(REVISION3_ADJUDICATION.read_text(encoding="utf-8"))

    validate_rulegen_critique(
        payload,
        expected_stage="norm_candidate_batch",
        expected_target_id="fraud.article347.pass1.001.revision3",
        commentary_by_id=commentary,
        allowed_comment_ids=set(commentary),
    )
    assert len(payload["findings"]) == 3
    assert "coverage gap" in payload["summary"]


def test_fraud_revision4_adjudication_is_source_bounded() -> None:
    request = load_jsonl(REQUESTS)[0]
    commentary = {
        row["comment_id"]: row for row in request["commentary_chunks"]
    }
    payload = json.loads(REVISION4_ADJUDICATION.read_text(encoding="utf-8"))

    validate_rulegen_critique(
        payload,
        expected_stage="norm_candidate_batch",
        expected_target_id="fraud.article347.pass1.001.revision4",
        commentary_by_id=commentary,
        allowed_comment_ids=set(commentary),
    )
    assert len(payload["findings"]) == 3
    assert "사례 RAG" in payload["summary"]


def test_fraud_revision5_adjudication_and_patch_are_source_bounded() -> None:
    request = load_jsonl(REQUESTS)[0]
    commentary = {
        row["comment_id"]: row for row in request["commentary_chunks"]
    }
    critique = json.loads(REVISION5_ADJUDICATION.read_text(encoding="utf-8"))

    validate_rulegen_critique(
        critique,
        expected_stage="norm_candidate_batch",
        expected_target_id="fraud.article347.pass1.001.revision5",
        commentary_by_id=commentary,
        allowed_comment_ids=set(commentary),
    )
    assert len(critique["findings"]) == 2

    source = {
        "request_id": request["request_id"],
        "status": "draft",
        "candidates": [
            {
                "candidate_id": candidate_id,
                "norm_kind": "variant",
                "polarity": "positive",
                "proposition": "Superseded candidate.",
                "source_refs": [
                    {
                        "comment_id": "comm_001692_제347조_Ⅱ.1_1",
                        "section_path": "Ⅱ.1",
                        "quote": "다수설은 사기죄의 보호 법익을 재산",
                    }
                ],
                "review_required": True,
            }
            for candidate_id in (
                "fraud.variant.protected-interest-main-right",
                "fraud.variant.protected-interest-possession-secondary",
            )
        ],
        "unresolved_questions": [],
    }
    patch = json.loads(REVISION5_PATCH.read_text(encoding="utf-8"))
    result = apply_norm_candidate_patch(
        source,
        patch,
        request,
        expected_target_id="fraud.article347.pass1.001.revision5",
    )
    assert len(result["candidates"]) == 1
    assert result["candidates"][0]["candidate_id"].endswith(
        "main-right-and-secondary-possession"
    )
    assert len(result["unresolved_questions"]) == 1

    bad_patch = copy.deepcopy(patch)
    bad_patch["remove_candidate_ids"] = ["fraud.missing"]
    with pytest.raises(NormCandidatePatchValidationError, match="unknown IDs"):
        apply_norm_candidate_patch(
            source,
            bad_patch,
            request,
            expected_target_id="fraud.article347.pass1.001.revision5",
        )


def test_fraud_final_candidate_exemplar_and_adjudication_are_valid() -> None:
    request = load_jsonl(REQUESTS)[0]
    commentary = {
        row["comment_id"]: row for row in request["commentary_chunks"]
    }
    candidates = json.loads(FINAL_CANDIDATES.read_text(encoding="utf-8"))
    adjudication = json.loads(FINAL_ADJUDICATION.read_text(encoding="utf-8"))

    validate_norm_candidate_batch(candidates, request)
    validate_rulegen_critique(
        adjudication,
        expected_stage="norm_candidate_batch",
        expected_target_id="fraud.article347.pass1.001.revision6",
        commentary_by_id=commentary,
        allowed_comment_ids=set(commentary),
    )
    candidate_ids = {
        candidate["candidate_id"] for candidate in candidates["candidates"]
    }
    assert len(candidates["candidates"]) == 61
    assert {
        candidate["polarity"] for candidate in candidates["candidates"]
    } == {"positive", "negative", "exception"}
    assert (
        "fraud.variant.protected-interest-main-right-and-secondary-possession"
        in candidate_ids
    )
    assert "fraud.variant.protected-interest-main-right" not in candidate_ids
    assert adjudication["verdict"] == "pass"
    assert not adjudication["findings"]
    assert "법률검토 완료를 의미하지 않는다" in adjudication["summary"]


def test_fraud_gold_fewshot_is_an_exact_subset_of_final_exemplar() -> None:
    final = json.loads(FINAL_CANDIDATES.read_text(encoding="utf-8"))
    fewshot = json.loads(FEWSHOT_GOLD.read_text(encoding="utf-8"))
    final_by_id = {
        candidate["candidate_id"]: candidate
        for candidate in final["candidates"]
    }
    expected = fewshot["expected_output"]

    assert fewshot["exemplar_id"] == "fraud.sex-work-authority-scope.gold"
    assert len(expected["candidates"]) == 3
    assert all(
        candidate == final_by_id[candidate["candidate_id"]]
        for candidate in expected["candidates"]
    )
    assert all(
        any(
            ref["comment_id"] == source["comment_id"]
            and ref["section_path"] == source["section_path"]
            and ref["quote"] == source["text"]
            for source in fewshot["source_excerpts"]
        )
        for candidate in expected["candidates"]
        for ref in candidate["source_refs"]
    )


def test_all_fraud_candidate_batches_are_source_bounded() -> None:
    requests = {row["request_id"]: row for row in load_jsonl(REQUESTS)}
    manifest = json.loads(CANDIDATE_MANIFEST.read_text(encoding="utf-8"))

    assert len(manifest["batches"]) == 13
    assert manifest["totals"]["candidates"] == 661
    assert manifest["totals"]["unresolved_questions"] == 37
    assert len(manifest["duplicate_candidate_ids"]) == 2
    for batch in manifest["batches"]:
        payload = json.loads(
            (PROJECT_ROOT / batch["path"]).read_text(encoding="utf-8")
        )
        validate_norm_candidate_batch(payload, requests[batch["request_id"]])
        if batch["batch_number"] == 1:
            continue
        critic = json.loads(
            (
                PROJECT_ROOT
                / batch["review_artifacts"]["critic_pass1"]
            ).read_text(encoding="utf-8")
        )
        commentary = {
            row["comment_id"]: row
            for row in requests[batch["request_id"]]["commentary_chunks"]
        }
        validate_rulegen_critique(
            critic,
            expected_stage="norm_candidate_batch",
            expected_target_id=batch["request_id"],
            commentary_by_id=commentary,
            allowed_comment_ids=set(commentary),
        )


def test_fraud_norm_card_modules_partition_all_candidates() -> None:
    payloads = build_module_payloads()

    assert len(payloads) == 8
    assert sum(
        len(batch["candidates"])
        for payload in payloads.values()
        for batch in payload["validated_batches"]
    ) == 661
    assert all(payload["unresolved_questions"] for payload in payloads.values())


def test_final_fraud_norm_card_modules_cover_all_candidates() -> None:
    requests = load_jsonl(REQUESTS)
    commentary = {
        row["comment_id"]: row
        for request in requests
        for row in request["commentary_chunks"]
    }
    request_scope = {
        request["request_id"]: {
            row["comment_id"] for row in request["commentary_chunks"]
        }
        for request in requests
    }
    payloads = build_module_payloads()
    manifest = json.loads(NORM_CARD_MANIFEST.read_text(encoding="utf-8"))

    assert manifest["totals"]["candidates"] == 661
    assert manifest["totals"]["cards"] == 646
    for module in manifest["modules"]:
        card_set = json.loads(
            (PROJECT_ROOT / module["path"]).read_text(encoding="utf-8")
        )
        candidate_map = {
            (batch["request_id"], candidate["candidate_id"]): candidate
            for batch in payloads[module["module"]]["validated_batches"]
            for candidate in batch["candidates"]
        }
        validate_norm_card_set(
            card_set,
            commentary,
            request_scope,
            allowed_candidates=candidate_map,
        )


def test_user_adjudicated_fraud_cards_are_narrowed() -> None:
    candidates = json.loads(FINAL_CANDIDATES.read_text(encoding="utf-8"))[
        "candidates"
    ]
    candidates_by_id = {
        candidate["candidate_id"]: candidate for candidate in candidates
    }
    assert "fraud.standard.false-passport-no-property-object" not in candidates_by_id
    assert candidates_by_id[
        "fraud.standard.triangular-fraud-victim-property-right-holder"
    ]["proposition"].startswith("법원을 기망하여 제3자로부터 재물을 편취한 경우")

    general_object = json.loads(
        (
            PROJECT_ROOT
            / "data/rulegen/fraud/norm_card_sets/general_object.json"
        ).read_text(encoding="utf-8")
    )
    general_cards = {card["id"]: card for card in general_object["cards"]}
    nonproperty = general_cards["fraud_general_object.nonproperty_examples"]
    assert len(nonproperty["candidate_refs"]) == 1
    assert "여권" not in nonproperty["proposition"]
    assert all("여권" not in ref["quote"] for ref in nonproperty["source_refs"])
    triangular = general_cards["fraud_general_object.triangular_fraud_victim"]
    assert "피기망자인 법원" in triangular["proposition"]
    assert "삼각사기에서" not in triangular["proposition"]

    damage = json.loads(
        (
            PROJECT_ROOT
            / "data/rulegen/fraud/norm_card_sets/damage_acquisition.json"
        ).read_text(encoding="utf-8")
    )
    damage_cards = {card["id"]: card for card in damage["cards"]}
    third_party = damage_cards[
        "fraud_damage_acquisition.third_party_acquisition_intent"
    ]
    assert "제3자로 하여금 재물을 취득하게 할 의사" in third_party[
        "proposition"
    ]
    assert "제3자를 취득하게 할 의사" not in third_party["proposition"]


def test_fraud_norm_card_critic_jobs_partition_every_final_card() -> None:
    jobs, metadata = build_norm_card_critic_jobs(
        list(build_module_payloads()), cards_per_job=50, max_tokens=20_000
    )

    assert len(jobs) == 18
    assert len(metadata) == len(jobs)
    assert sum(record["cards"] for record in metadata.values()) == 646
    assert all(job.role == "sol" for job in jobs)
    assert all(job.payload["stage"] == "norm_card_set" for job in jobs)
    assert all(job.payload["target"]["coverage_gaps"] == [] for job in jobs)
    assert all(
        job.payload["target"]["legal_review_questions"]
        for job in jobs
        if any(card["review_required"] for card in job.payload["target"]["cards"])
    )
    for job in jobs:
        target = job.payload["target"]
        commentary_context = job.payload["bounded_source_material"][
            "commentary_context"
        ]
        actual_comment_ids = {
            ref["comment_id"]
            for card in target["cards"]
            for ref in card["source_refs"]
        }
        assert set(target["source_scope"]["comment_ids"]) == actual_comment_ids
        assert {
            chunk["comment_id"] for chunk in commentary_context
        } == actual_comment_ids
        assert all(chunk["document_text"] for chunk in commentary_context)

    counterfeit_job = next(
        job
        for job in jobs
        if any(
            card["id"]
            == "fraud_concurrence.counterfeit_currency_real_concurrence"
            for card in job.payload["target"]["cards"]
        )
    )
    counterfeit_context = {
        chunk["comment_id"]: chunk["document_text"]
        for chunk in counterfeit_job.payload["bounded_source_material"][
            "commentary_context"
        ]
    }
    assert "그 보호법익을 달리하고 있으므로" in counterfeit_context[
        "comm_001692_제347조_Ⅹ.8_125"
    ]


def test_final_fraud_norm_card_critic_and_review_manifests_are_complete() -> None:
    critic = json.loads(NORM_CARD_CRITIC_MANIFEST.read_text(encoding="utf-8"))
    queue = json.loads(NORM_CARD_REVIEW_QUEUE.read_text(encoding="utf-8"))
    decisions = load_jsonl(HUMAN_REVIEW_DECISIONS)
    readiness = json.loads(RULE_IR_READINESS.read_text(encoding="utf-8"))
    remediation = json.loads(
        NORM_CARD_REMEDIATION_LEDGER.read_text(encoding="utf-8")
    )
    audit = json.loads(NORM_CARD_AUDIT.read_text(encoding="utf-8"))
    policy_queue = json.loads(POLICY_REVIEW_QUEUE.read_text(encoding="utf-8"))
    policy_decisions = load_jsonl(POLICY_REVIEW_DECISIONS)
    policy_resolution = json.loads(
        POLICY_RESOLUTION_AUDIT.read_text(encoding="utf-8")
    )
    core_selection = json.loads(
        CORE_SELECTION_AUDIT.read_text(encoding="utf-8")
    )
    core_queue = json.loads(CORE_REVIEW_QUEUE.read_text(encoding="utf-8"))
    core_decisions = load_jsonl(CORE_REVIEW_DECISIONS)
    card_manifest = json.loads(NORM_CARD_MANIFEST.read_text(encoding="utf-8"))

    assert critic["totals"]["reports"] == 17
    assert critic["totals"]["cards"] == 636
    assert critic["totals"]["findings"] == 67
    assert len(queue["items"]) == critic["totals"]["findings"]
    assert len({item["review_id"] for item in queue["items"]}) == 67
    assert {item["review_id"] for item in decisions} == {
        item["review_id"] for item in queue["items"]
    }
    assert all(item["resolved"] for item in queue["items"])
    assert Counter(item["remediation_status"] for item in queue["items"]) == {
        "applied": 57,
        "not_applicable": 10,
    }
    assert remediation["method"] == "manual_source_and_finding_audit_no_api"
    assert remediation["api_calls"] == 0
    assert remediation["accepted_findings"] == 57
    assert remediation["handled_findings"] == 57
    assert len(remediation["finding_resolutions"]) == 57
    assert readiness["full_rule_ir_generation_blocked"] is True
    assert readiness["core_rule_human_review_blocked"] is True
    assert readiness["core_rule_review"] == {
        "approved": 0,
        "cards": 118,
        "unresolved": 118,
    }
    assert readiness["final_policy_activation_blocked"] is False
    assert readiness["totals"] == {
        "context_only_excluded": 528,
        "neural_grounding_spec_candidate": 89,
        "provisional_rule_ir_candidate": 29,
    }
    assert sum(readiness["totals"].values()) == 646
    assert audit["method"] == "manual_final_audit_no_api"
    assert audit["api_calls"] == 0
    assert audit["cards"] == 646
    assert audit["all_cards_accounted_for"] is True
    assert audit["status_counts"] == {
        "deterministic_rule_review_pending": 29,
        "rag_context_only": 528,
        "standard_input_review_pending": 89,
    }
    assert len(audit["rows"]) == len({row["card_id"] for row in audit["rows"]})
    assert policy_queue["api_calls"] == 0
    assert policy_queue["status"] == "complete"
    assert policy_queue["policy_groups"] == 0
    assert policy_queue["policy_cards"] == 0
    assert policy_queue["collapsed_policy_sources"] == []
    assert len(policy_queue["resolved_split_sources"]) == 3
    assert len(policy_decisions) == policy_queue["policy_groups"]
    assert {row["review_id"] for row in policy_decisions} == {
        row["review_id"] for row in policy_queue["items"]
    }
    assert policy_resolution["api_calls"] == 0
    assert policy_resolution["resolved_groups"] == 12
    assert policy_resolution["remaining_policy_groups"] == 0
    assert policy_resolution["verified_case_count"] == 15
    assert len(policy_resolution["verified_local_primary_records"]) == 15
    assert policy_resolution["local_primary_verification"] == {
        "status": "verified",
        "verified_records": 15,
    }
    assert {
        record["court"]
        for record in policy_resolution["verified_local_primary_records"].values()
    } == {"대법원"}
    assert core_selection["api_calls"] == 0
    assert core_selection["counts"] == {
        "context_only": 528,
        "deterministic_rule": 29,
        "standard_input": 89,
    }
    assert core_queue["api_calls"] == 0
    assert core_queue["cards"] == 118
    assert core_queue["counts"] == {
        "deterministic_rule": 29,
        "standard_input": 89,
    }
    assert core_queue["decision_status_counts"] == {"pending": 118}
    assert core_queue["approved"] == 0
    assert core_queue["unresolved"] == 118
    assert len(core_decisions) == 118
    assert {row["review_id"] for row in core_decisions} == {
        row["review_id"] for row in core_queue["items"]
    }
    core_card_ids = {item["card_id"] for item in core_queue["items"]}
    assert not any(item["module"] == "concurrence" for item in core_queue["items"])
    assert "fraud_intent.conditional_intent" not in core_card_ids
    assert "fraud_general_object.objective_elements" not in core_card_ids
    assert (
        "fraud_general_object.protected_interest_property_only"
        not in core_card_ids
    )
    assert "fraud_general_object.real_estate_property" not in core_card_ids
    assert (
        "deception.fraud.element.deceived-person-disposal-authority"
        not in core_card_ids
    )
    core_roles = {item["card_id"]: item["role"] for item in core_queue["items"]}
    assert core_roles["fraud_mistake.error_definition"] == "standard_input"
    assert (
        core_roles["fraud_damage_acquisition.delivery_factual_control"]
        == "standard_input"
    )
    assert (
        core_roles["general_object.fraud.definition.property-benefit"]
        == "standard_input"
    )
    assert (
        "fraud_stages_participation.inclusive_offense_withdrawal_liability"
        not in core_card_ids
    )
    module_paths = {
        module["module"]: PROJECT_ROOT / module["path"]
        for module in card_manifest["modules"]
    }
    cards_by_id = {
        card["id"]: card
        for module in readiness["modules"]
        for card in json.loads(
            module_paths[module["module"]].read_text(encoding="utf-8")
        )["cards"]
    }
    formalization_by_id = {
        card_id: card["formalization"] for card_id, card in cards_by_id.items()
    }
    objective_summary = cards_by_id["fraud_general_object.objective_elements"]
    assert objective_summary["formalization"] == "context_only"
    assert "재산상 손해" in objective_summary["proposition"]
    no_loss_rule = cards_by_id[
        "fraud_damage_acquisition.property_loss_negative_view"
    ]
    assert no_loss_rule["formalization"] == "deterministic_rule"
    assert "요구하지 않는다" in no_loss_rule["proposition"]
    for module in readiness["modules"]:
        for card_id in module["buckets"].get(
            "provisional_rule_ir_candidate", []
        ):
            assert formalization_by_id[card_id] == "deterministic_rule"
        for card_id in module["buckets"].get(
            "neural_grounding_spec_candidate", []
        ):
            assert formalization_by_id[card_id] == "standard_input"

    items_by_id = {item["review_id"]: item for item in queue["items"]}
    assert Counter(
        item["card_mapping"]["method"] for item in queue["items"]
    ) == {
        "critic_text_audited_override": 45,
        "explicit_card_id": 19,
        "generated_review_question_scope": 1,
        "explicit_wildcard": 2,
    }
    assert Counter(
        item["human_review"]["status"] for item in queue["items"]
    ) == {"completed": 67}
    assert all(item["impacted_card_ids"] for item in queue["items"])
    assert {
        item["review_id"]: tuple(item["impacted_card_ids"])
        for item in queue["items"]
        if item["card_mapping"]["method"] == "critic_text_audited_override"
    } == AUDITED_CARD_MAPPINGS
    assert items_by_id[
        "fraud.normcards.concurrence.part001.critic.counterfeit_reason_unsupported"
    ]["impacted_card_ids"] == [
        "fraud_concurrence.counterfeit_currency_real_concurrence"
    ]
    assert items_by_id[
        "fraud.normcards.general_object.part001.critic.nonproperty_examples_overgeneralized"
    ]["impacted_card_ids"] == ["fraud_general_object.nonproperty_examples"]
    assert items_by_id[
        "fraud.normcards.deception.part003.critic.authority.additional-case-cards"
    ]["impacted_card_ids"] == [
        "deception.fraud.standard.artwork-assistant-participation",
        "deception.fraud.standard.land-sale-unknown-urban-planning-area",
        "deception.fraud.standard.land-sale-no-known-urban-planning-conflict",
        "deception.fraud.standard.entrusted-car-unknown-arrears-direct-inquiry",
    ]
    assert items_by_id[
        "fraud.normcards.concurrence.part001.critic."
        "commentary_penalties_deterministic_before_verification"
    ]["impacted_card_ids"] == [
        "fraud_concurrence.general_fraud_penalty",
        "fraud_concurrence.attempt_habitual_punishment",
        "fraud_concurrence.aggravated_economic_value_thresholds",
    ]
    assert items_by_id[
        "fraud.normcards.deception.part004.critic.variant.religious_practice_boundary"
    ]["impacted_card_ids"] == [
        "deception.fraud.standard.religious-compensation-not-necessarily-fraud",
        "deception.fraud.standard.shamanistic-false-misfortune",
        "deception.fraud.standard.prayer-fee-beyond-permitted-limit",
        "deception.fraud.standard.false-religious-claims-donations",
    ]
    policy_question = items_by_id[
        "fraud.normcards.damage_acquisition.part002.critic."
        "unsupported_variant_policy_question"
    ]
    assert policy_question["card_mapping"]["method"] == (
        "critic_text_audited_override"
    )
    assert policy_question["impacted_card_ids"] == [
        "fraud_damage_acquisition.legitimate_right_deduction_view"
    ]


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
        "norm_candidate_patch.schema.json",
        "norm_card_set.schema.json",
        "rulegen_critique_report.schema.json",
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
    card_prompt = (
        PROJECT_ROOT / "prompts/rulegen_merge_norm_cards.md"
    ).read_text(encoding="utf-8")
    critic_prompt = (PROJECT_ROOT / "prompts/rulegen_critic.md").read_text(
        encoding="utf-8"
    )
    revision_prompt = (
        PROJECT_ROOT / "prompts/rulegen_revise_norm_candidates.md"
    ).read_text(encoding="utf-8")
    assert "exact source reference" in extract_prompt
    assert "independent legal-review units" in card_prompt
    assert "authority is limited to critique" in critic_prompt
    assert "applies only to `source_refs` in the critique report" in critic_prompt
    assert "target quotes are mandatory provenance" in critic_prompt
    assert "critique reports are advisory work products" in revision_prompt
    assert "OCR noise interrupts" in revision_prompt
    assert "never output executable code directly" in merge_prompt
