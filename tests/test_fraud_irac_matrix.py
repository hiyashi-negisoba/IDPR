from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from idpr.generation import (
    GenerationContractError,
    apply_section_patches,
    assess_irac_answer_alignment,
    build_fraud_irac_plan,
    build_fraud_rag_packet,
    build_fraud_rag_queries,
    validate_claim_graph,
    validate_fraud_irac_plan,
    validate_fraud_rag_packet,
    validate_long_form_answer,
)
from idpr.neural import (
    anchor_fraud_target_roles,
    build_authority_packet,
    select_fraud_card_plan,
)

from scripts.run_fraud_irac_matrix import answer_contract_violations, answer_request


ROOT = Path(__file__).resolve().parents[1]
CASE_PATH = ROOT / "data/e2e/fraud/kcl_r14_p1_q2_case.json"
REPLAY_PATH = ROOT / "data/e2e/fraud/kcl_r14_p1_q2_replay_neural.json"
NORM_CARD_PATH = ROOT / "data/rulegen/fraud/fraud_core_norm_card_set.json"
SLURM_PATH = ROOT / "scripts/slurm/run_fraud_irac_matrix.sh"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def plan_inputs() -> tuple[dict, dict, dict, list[dict], dict]:
    case = load_json(CASE_PATH)
    replay = load_json(REPLAY_PATH)
    fact_graph, _ = anchor_fraud_target_roles(replay["fact_graph"], case)
    assessments = replay["assessment_bundle"]
    selected = select_fraud_card_plan(fact_graph)
    assert selected == assessments["selected_card_ids"]
    authority = build_authority_packet(selected, load_json(NORM_CARD_PATH))
    symbolic = {
        "legal_result": "established",
        "observed_nonempty": {
            "fraud_elements_satisfied": True,
            "fraud_established": True,
            "fraud_not_established": False,
            "fraud_undetermined": False,
            "fraud_conflict": False,
        },
    }
    return case, fact_graph, assessments, authority, symbolic


def compiled_plan() -> tuple[dict, dict, dict, list[dict], dict]:
    case, fact_graph, assessments, authority, symbolic = plan_inputs()
    plan = build_fraud_irac_plan(
        case=case,
        fact_graph=fact_graph,
        assessment_bundle=assessments,
        authority_packet=authority,
        symbolic_result=symbolic,
    )
    return plan, case, fact_graph, authority, assessments


def valid_answer(plan: dict) -> dict:
    sections = []
    for unit in plan["units"]:
        sections.append(
            {
                "section_id": unit["unit_id"],
                "heading": unit["issue"],
                "body": "법리는 입력 법리에 따른다. 사안의 사실과 법리를 연결하면 요건이 충족된다. 따라서 이 구성요건은 충족된다.",
                "cited_fact_ids": unit["required_fact_ids"],
                "cited_card_ids": [
                    item["card_id"] for item in unit["card_assessments"]
                ],
                "cited_authority_comment_ids": unit[
                    "required_authority_comment_ids"
                ],
                "stated_conclusion": unit["required_conclusion"],
            }
        )
    return {
        "version": "1.0.0",
        "case_id": plan["case_id"],
        "method_id": "m6_claim_verified",
        "title": "乙의 B에 대한 사기죄",
        "sections": sections,
        "overall_conclusion": plan["overall_conclusion"],
        "summary": "乙의 B에 대한 사기죄는 성립한다.",
    }


def valid_claim_graph(answer: dict, plan: dict) -> dict:
    claims = []
    claim_number = 1
    for unit in plan["units"]:
        card_ids = [item["card_id"] for item in unit["card_assessments"]]
        entries = (
            {
                "quote": "법리는 입력 법리에 따른다.",
                "claim_type": "rule",
                "support_kind": "authority_rule",
                "fact_ids": [],
                "card_ids": card_ids,
                "relation_ids": [],
            },
            {
                "quote": "사안의 사실과 법리를 연결하면 요건이 충족된다.",
                "claim_type": "application",
                "support_kind": "derived_application",
                "fact_ids": unit["required_fact_ids"],
                "card_ids": card_ids,
                "relation_ids": [],
            },
            {
                "quote": "따라서 이 구성요건은 충족된다.",
                "claim_type": "conclusion",
                "support_kind": "symbolic_conclusion",
                "fact_ids": [],
                "card_ids": [],
                "relation_ids": ["fraud_established"],
            },
        )
        for entry in entries:
            claims.append(
                {
                    "claim_id": f"claim_{claim_number:03d}",
                    "section_id": unit["unit_id"],
                    "polarity": "supports",
                    "authority_comment_ids": [],
                    **entry,
                }
            )
            claim_number += 1
    return {
        "version": "1.0.0",
        "case_id": plan["case_id"],
        "method_id": "m6_claim_verified",
        "claims": claims,
        "section_conclusions": [
            {
                "section_id": unit["unit_id"],
                "conclusion": unit["required_conclusion"],
            }
            for unit in plan["units"]
        ],
        "overall_conclusion": plan["overall_conclusion"],
    }


def all_provenance(plan: dict, fact_graph: dict, authority: list[dict]):
    return (
        [fact["fact_id"] for fact in fact_graph["facts"]],
        [
            item["card_id"]
            for unit in plan["units"]
            for item in unit["card_assessments"]
        ],
        [source["comment_id"] for card in authority for source in card["sources"]],
    )


def test_target_scoped_rag_is_reproducible_and_finds_loan_purpose_rule() -> None:
    case, fact_graph, _, _, _ = plan_inputs()
    queries = build_fraud_rag_queries(case=case, fact_graph=fact_graph)
    first = build_fraud_rag_packet(query_texts=queries, top_k=6)
    second = build_fraud_rag_packet(query_texts=queries, top_k=6)
    validate_fraud_rag_packet(first)
    assert first == second
    assert first["corpus"]["cards"] == 558
    assert first["items"][0]["card_id"] == "fraud_mistake.false_loan_purpose"
    assert all(
        source["excerpt"]
        for item in first["items"]
        for source in item["sources"]
    )


def test_irac_plan_covers_every_selected_card_once() -> None:
    plan, _, _, _, assessments = compiled_plan()
    observed = [
        item["card_id"]
        for unit in plan["units"]
        for item in unit["card_assessments"]
    ]
    assert len(plan["units"]) == 5
    assert len(observed) == 13
    assert len(set(observed)) == 13
    assert set(observed) == set(assessments["selected_card_ids"])
    assert {unit["required_conclusion"] for unit in plan["units"]} == {"satisfied"}


def test_irac_plan_rejects_symbolic_conclusion_mismatch() -> None:
    plan, case, fact_graph, authority, assessments = compiled_plan()
    symbolic = {
        "legal_result": "not_established",
        "observed_nonempty": {
            "fraud_elements_satisfied": True,
            "fraud_established": True,
            "fraud_not_established": False,
            "fraud_undetermined": False,
            "fraud_conflict": False,
        },
    }
    with pytest.raises(GenerationContractError, match="conclusion differs"):
        validate_fraud_irac_plan(
            plan,
            case=case,
            fact_graph=fact_graph,
            assessment_bundle=assessments,
            authority_packet=authority,
            symbolic_result=symbolic,
        )


def test_claim_graph_validates_complete_irac_answer() -> None:
    plan, _, fact_graph, authority, _ = compiled_plan()
    answer = valid_answer(plan)
    facts, cards, sources = all_provenance(plan, fact_graph, authority)
    validate_long_form_answer(
        answer,
        case_id=plan["case_id"],
        method_id="m6_claim_verified",
        allowed_fact_ids=facts,
        allowed_card_ids=cards,
        allowed_authority_ids=sources,
    )
    assert assess_irac_answer_alignment(answer, plan) == []
    assert (
        validate_claim_graph(
            valid_claim_graph(answer, plan),
            answer=answer,
            plan=plan,
            fact_graph=fact_graph,
            authority_packet=authority,
        )
        == []
    )


def test_claim_graph_catches_missing_application_support() -> None:
    plan, _, fact_graph, authority, _ = compiled_plan()
    answer = valid_answer(plan)
    graph = valid_claim_graph(answer, plan)
    target = next(
        claim
        for claim in graph["claims"]
        if claim["section_id"] == "irac_deception"
        and claim["claim_type"] == "application"
    )
    target["fact_ids"] = []
    target["card_ids"] = []
    violations = validate_claim_graph(
        graph,
        answer=answer,
        plan=plan,
        fact_graph=fact_graph,
        authority_packet=authority,
    )
    codes = {item["code"] for item in violations}
    assert "unsupported_claim" in codes
    assert "claim_fact_coverage" in codes


def test_failed_section_patch_preserves_every_unaffected_section() -> None:
    plan, _, fact_graph, authority, _ = compiled_plan()
    answer = valid_answer(plan)
    failed_id = "irac_deception"
    replacement = copy.deepcopy(
        next(section for section in answer["sections"] if section["section_id"] == failed_id)
    )
    replacement["body"] = (
        "법리는 입력 법리에 따른다. 사안의 사실과 법리를 연결하면 요건이 충족된다. "
        "따라서 이 구성요건은 충족된다. 검증 실패 원인을 교정하였다."
    )
    bundle = {
        "version": "1.0.0",
        "case_id": plan["case_id"],
        "method_id": "m6_claim_verified",
        "patches": [replacement],
    }
    updated, audit = apply_section_patches(
        answer, bundle, failed_section_ids=[failed_id]
    )
    assert audit["unaffected_sections_preserved"] is True
    assert audit["patched_section_ids"] == [failed_id]
    assert len(audit["preserved_section_ids"]) == len(answer["sections"]) - 1
    facts, cards, sources = all_provenance(plan, fact_graph, authority)
    validate_long_form_answer(
        updated,
        case_id=plan["case_id"],
        method_id="m6_claim_verified",
        allowed_fact_ids=facts,
        allowed_card_ids=cards,
        allowed_authority_ids=sources,
    )
    assert (
        validate_claim_graph(
            valid_claim_graph(updated, plan),
            answer=updated,
            plan=plan,
            fact_graph=fact_graph,
            authority_packet=authority,
        )
        == []
    )


def test_slurm_matrix_uses_exact_resources_and_disables_prefix_cache() -> None:
    source = SLURM_PATH.read_text(encoding="utf-8")
    assert "#SBATCH --time=48:00:00" in source
    assert "#SBATCH --cpus-per-task=2" in source
    assert "#SBATCH --gres=gpu:PRO6000:1" in source
    assert "#SBATCH --mem=32G" in source
    assert "#SBATCH --nodelist" not in source
    assert "#SBATCH --constraint" not in source
    assert "--no-enable-prefix-caching" in source
    assert "scripts/run_fraud_irac_matrix.py" in source


def test_direct_answer_request_declares_case_text_as_only_fact_provenance() -> None:
    case = load_json(CASE_PATH)
    request = answer_request(
        case=case,
        method_id="m1_direct",
        context={"case_only": True},
        allowed_fact_ids=["case_text"],
    )
    assert request["allowed_provenance_ids"] == {
        "fact_ids": ["case_text"],
        "card_ids": [],
        "authority_comment_ids": [],
    }


def test_answer_contract_error_is_a_section_quality_violation() -> None:
    plan, _, _, _, _ = compiled_plan()
    answer = valid_answer(plan)
    answer["sections"][0]["cited_card_ids"] = ["invented.card"]
    violations = answer_contract_violations(
        answer,
        case_id=plan["case_id"],
        method_id="m6_claim_verified",
        allowed_fact_ids=[
            fact_id
            for unit in plan["units"]
            for fact_id in unit["required_fact_ids"]
        ],
        allowed_card_ids=[
            item["card_id"]
            for unit in plan["units"]
            for item in unit["card_assessments"]
        ],
        allowed_authority_ids=[
            source_id
            for unit in plan["units"]
            for source_id in unit["required_authority_comment_ids"]
        ],
    )
    assert violations[0]["code"] == "answer_contract_violation"
    assert violations[0]["section_id"] == "irac_object_roles"
