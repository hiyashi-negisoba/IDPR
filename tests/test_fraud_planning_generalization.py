from __future__ import annotations

import json
from pathlib import Path

import pytest

from idpr.fraud_planning import (
    FRAUD_ROLES,
    build_fraud_assessment_context,
    fraud_case_role_hints,
    load_fraud_plan_registry,
    reasoning_plan_card_ids,
    select_fraud_reasoning_plan,
    validate_fraud_case,
)
from idpr.generation import (
    build_fraud_irac_plan,
    build_fraud_rag_queries,
    compile_fraud_whole_irac_answer,
)
from idpr.neural import (
    build_authority_packet,
    build_scallop_scenario,
    select_fraud_card_plan,
    validate_fraud_assessment_bundle,
    validate_fraud_fact_graph,
)
from idpr.rulegen.scallop_runtime import run_scenario
from scripts.run_fraud_irac_matrix import load_case
from scripts.build_fraud_manual_card_review import render_review


ROOT = Path(__file__).resolve().parents[1]
CASE_SET_PATH = (
    ROOT
    / "data/e2e/fraud/manual_paraphrases/fraud_manual_paraphrase_cases.json"
)
NORM_CARD_PATH = ROOT / "data/rulegen/fraud/fraud_core_norm_card_set.json"
RULE_IR_PATH = (
    ROOT / "data/rulegen/fraud/fraud_full_rule_ir_candidate_unreviewed.json"
)
COMPILED_PATH = ROOT / "rules/generated/fraud_article347_full_v1.scl"
SCLI_PATH = ROOT / "tools/scallop/scli-0.2.4-linux-x86_64"
QUERY_RELATIONS = (
    "fraud_elements_satisfied",
    "fraud_established",
    "fraud_not_established",
    "fraud_undetermined",
    "fraud_conflict",
)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def paraphrase_cases() -> list[dict]:
    return load_json(CASE_SET_PATH)["cases"]


def synthetic_fact_graph(case: dict) -> dict:
    role_hints = fraud_case_role_hints(case)
    mentions = list(dict.fromkeys(role_hints.values()))
    entity_ids = {mention: mention.lower() for mention in mentions}
    actors = []
    for mention in mentions:
        roles = [role for role in FRAUD_ROLES if role_hints[role] == mention]
        actors.append(
            {
                "entity_id": entity_ids[mention],
                "mentions": [mention],
                "roles": roles,
            }
        )
    source_quote = case["case_text"].split(". ", maxsplit=1)[0]
    return {
        "version": "1.0.0",
        "case_id": case["case_id"],
        "target_issue_id": "fraud",
        "actors": actors,
        "facts": [
            {
                "fact_id": "fact_001",
                "fact_kind": "other",
                "statement": "배선 검증용으로 대상 거래의 사실이 주어져 있다.",
                "source_quote": source_quote,
                "participants": [entity_ids[role_hints["defendant"]]],
                "epistemic_status": "given",
                "issue_effects": [
                    {"issue_id": "fraud", "direction": "supports"}
                ],
            }
        ],
        "profiles": list(case["required_profiles"]),
        "retrieval_queries": [case["target"]["target_transaction"]["description"]],
        "unresolved_questions": [],
    }


def synthetic_assessments(
    *, case: dict, fact_graph: dict, authority_packet: list[dict]
) -> dict:
    plan = select_fraud_reasoning_plan(fact_graph, case=case)
    expected_status = {
        card["card_id"]: card["satisfied_when"]
        for unit in plan["units"]
        for card in unit["cards"]
    }
    selected = select_fraud_card_plan(fact_graph, case=case)
    authorities = {
        card["card_id"]: card["sources"][0]["comment_id"]
        for card in authority_packet
    }
    assessments = []
    for index, card_id in enumerate(selected, start=1):
        status = expected_status[card_id]
        assessments.append(
            {
                "assessment_id": f"assessment_{index:03d}",
                "card_id": card_id,
                "status": status,
                "basis_fact_ids": ["fact_001"] if status == "satisfied" else [],
                "counter_fact_ids": (
                    ["fact_001"] if status == "not_satisfied" else []
                ),
                "missing_facts": [],
                "authority_comment_ids": [authorities[card_id]],
                "rationale": "host-only 배선 검증을 위한 registry 기대 상태이다.",
                "confidence": 1.0,
            }
        )
    return {
        "version": "1.0.0",
        "case_id": case["case_id"],
        "selected_card_ids": selected,
        "assessments": assessments,
    }


def test_registry_and_paraphrase_cases_are_contract_valid() -> None:
    registry = load_fraud_plan_registry()
    norm_card_ids = {
        card["id"] for card in load_json(NORM_CARD_PATH)["cards"]
    }
    assert registry["core"]["core_id"] == "fraud_core"
    assert {profile["profile_id"] for profile in registry["profiles"]} == {
        "loan_purpose",
        "loan_repayment",
        "contract_performance",
        "implicit_deception",
        "property_benefit",
        "triangular",
    }
    for case in paraphrase_cases():
        plan = select_fraud_reasoning_plan(
            {"profiles": case["required_profiles"]}, case=case, registry=registry
        )
        selected = reasoning_plan_card_ids(plan)
        assert len(selected) == len(set(selected))
        assert set(selected) <= norm_card_ids

    cases = paraphrase_cases()
    assert len(cases) == 5
    for case in cases:
        validate_fraud_case(case, registry)
        assert "기망" not in case["case_text"]
        assert "편취" not in case["case_text"]
        assert "사기죄" not in case["case_text"]
        assert "의사나 능력이 없" not in case["case_text"]


def test_matrix_runner_selects_a_case_from_the_paraphrase_set() -> None:
    selected = load_case(CASE_SET_PATH, "manual_fraud_063_01_parcel_triangular")
    composed = select_fraud_reasoning_plan(
        {"profiles": selected["required_profiles"]}, case=selected
    )
    assert composed["plan_id"] == "fraud_core__triangular"
    with pytest.raises(ValueError, match="--case-id is required"):
        load_case(CASE_SET_PATH)
    with pytest.raises(ValueError, match="found 0"):
        load_case(CASE_SET_PATH, "missing_case")


def test_human_card_review_contains_every_case_and_selected_card() -> None:
    case_set = load_json(CASE_SET_PATH)
    review = render_review(case_set, load_json(NORM_CARD_PATH))
    for case in case_set["cases"]:
        assert case["case_id"] in review
        plan = select_fraud_reasoning_plan(
            {"profiles": case["required_profiles"]}, case=case
        )
        for card_id in reasoning_plan_card_ids(plan):
            assert card_id in review
    assert "C5-" in review
    assert "사용자 판정" in review


def test_every_paraphrase_case_routes_and_compiles_without_a_model() -> None:
    norm_cards = load_json(NORM_CARD_PATH)
    for case in paraphrase_cases():
        fact_graph = synthetic_fact_graph(case)
        validate_fraud_fact_graph(fact_graph, case)
        plan_spec = select_fraud_reasoning_plan(fact_graph, case=case)
        selected = select_fraud_card_plan(fact_graph, case=case)
        assert set(selected) < set(reasoning_plan_card_ids(plan_spec))
        cards_by_id = {card["id"]: card for card in norm_cards["cards"]}
        assert {
            cards_by_id[card_id]["formalization"] for card_id in selected
        } == {"standard_input"}
        assessment_context = build_fraud_assessment_context(
            fact_graph,
            case=case,
            selected_card_ids=selected,
        )
        assert [item["card_id"] for item in assessment_context] == selected
        assert all(set(item) == {"card_id", "unit_id", "unit_issue"} for item in assessment_context)

        assessment_authority_packet = build_authority_packet(selected, norm_cards)
        authority_packet = build_authority_packet(
            reasoning_plan_card_ids(plan_spec), norm_cards
        )
        assessment_bundle = synthetic_assessments(
            case=case,
            fact_graph=fact_graph,
            authority_packet=assessment_authority_packet,
        )
        validate_fraud_assessment_bundle(
            assessment_bundle,
            case=case,
            fact_graph=fact_graph,
            selected_card_ids=selected,
            authority_packet=assessment_authority_packet,
        )
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
        irac_plan = build_fraud_irac_plan(
            case=case,
            fact_graph=fact_graph,
            assessment_bundle=assessment_bundle,
            authority_packet=authority_packet,
            symbolic_result=symbolic,
        )
        assert irac_plan["reasoning_plan_id"] == plan_spec["plan_id"]
        deterministic_ids = {
            item["card_id"]
            for unit in irac_plan["units"]
            for item in unit["deterministic_rules"]
        }
        assert deterministic_ids == set(reasoning_plan_card_ids(plan_spec)) - set(
            selected
        )
        answer = compile_fraud_whole_irac_answer(plan=irac_plan, case=case)
        assert answer["title"].startswith(case["target"]["answer_subject"])
        assert [section["section_id"] for section in answer["sections"]] == [
            "irac_issue",
            "irac_rule",
            "irac_application",
            "irac_conclusion",
        ]
        application = answer["sections"][2]["body"]
        assert all(unit["issue"] in application for unit in irac_plan["units"])
        queries = build_fraud_rag_queries(case=case, fact_graph=fact_graph)
        assert case["question_prompt"] in queries
        assert fact_graph["retrieval_queries"][0] in queries


@pytest.mark.skipif(not SCLI_PATH.is_file(), reason="pinned scli is not installed")
def test_every_paraphrase_plan_reaches_scallop_established_wiring(tmp_path: Path) -> None:
    norm_cards = load_json(NORM_CARD_PATH)
    rule_ir = load_json(RULE_IR_PATH)
    compiled_source = COMPILED_PATH.read_text(encoding="utf-8")
    for case in paraphrase_cases():
        fact_graph = synthetic_fact_graph(case)
        selected = select_fraud_card_plan(fact_graph, case=case)
        authority_packet = build_authority_packet(selected, norm_cards)
        assessment_bundle = synthetic_assessments(
            case=case,
            fact_graph=fact_graph,
            authority_packet=authority_packet,
        )
        scenario = build_scallop_scenario(
            case=case,
            fact_graph=fact_graph,
            assessment_bundle=assessment_bundle,
            selected_card_ids=selected,
            authority_packet=authority_packet,
        )
        results = run_scenario(
            rule_ir=rule_ir,
            compiled_source=compiled_source,
            scenario=scenario,
            query_relations=QUERY_RELATIONS,
            scli_path=SCLI_PATH,
            work_dir=tmp_path / case["case_id"],
        )
        assert results["fraud_elements_satisfied"]["nonempty"] is True
        assert results["fraud_established"]["nonempty"] is True
        assert results["fraud_not_established"]["nonempty"] is False
        assert results["fraud_undetermined"]["nonempty"] is False
        assert results["fraud_conflict"]["nonempty"] is False
