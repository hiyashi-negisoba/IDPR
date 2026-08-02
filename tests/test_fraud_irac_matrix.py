from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from idpr.legacy.fraud_generation import (
    GenerationContractError,
    apply_section_patches,
    assess_irac_answer_alignment,
    build_fraud_irac_plan,
    build_fraud_irac_slot_schema,
    build_fraud_rag_packet,
    build_fraud_rag_queries,
    compile_fraud_irac_slot_draft,
    compile_fraud_whole_irac_answer,
    normalize_claim_graph,
    normalize_section_patch_bundle,
    render_long_form_markdown,
    validate_claim_graph,
    validate_fraud_irac_plan,
    validate_fraud_rag_packet,
    validate_long_form_answer,
)
from idpr.legacy.fraud_neural import (
    NeuralContractError,
    anchor_fraud_target_roles,
    apply_negative_card_safety_net,
    build_authority_packet,
    resolve_neural_query_statuses,
    select_fraud_card_plan,
    validate_fraud_assessment_bundle,
)
from idpr.legacy.fraud_planning import (
    reasoning_plan_card_ids,
    reasoning_plan_neural_queries,
    select_fraud_reasoning_plan,
)

from scripts.run_fraud_irac_matrix import (
    answer_contract_violations,
    answer_request,
    assessment_request,
    whole_irac_allowed_provenance,
)


ROOT = Path(__file__).resolve().parents[1]
CASE_PATH = ROOT / "data/e2e/fraud/kcl_r14_p1_q2_case.json"
REPLAY_PATH = ROOT / "data/e2e/fraud/kcl_r14_p1_q2_replay_neural.json"
NORM_CARD_PATH = ROOT / "data/rulegen/fraud/fraud_core_norm_card_set.json"
SLURM_PATH = ROOT / "scripts/slurm/run_fraud_irac_matrix.sh"
CLAIM_PROMPT_PATH = ROOT / "prompts/fraud_claim_graph_extract.md"
FACT_PROMPT_PATH = ROOT / "prompts/fraud_fact_graph_extract.md"
ASSESS_PROMPT_PATH = ROOT / "prompts/fraud_standard_assess.md"
MATRIX_SCRIPT_PATH = ROOT / "scripts/run_fraud_irac_matrix.py"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def plan_inputs() -> tuple[dict, dict, dict, list[dict], dict]:
    case = load_json(CASE_PATH)
    replay = load_json(REPLAY_PATH)
    fact_graph, _ = anchor_fraud_target_roles(replay["fact_graph"], case)
    assessments = replay["assessment_bundle"]
    selected = select_fraud_card_plan(fact_graph)
    assert selected == assessments["selected_card_ids"]
    reasoning_plan = select_fraud_reasoning_plan(fact_graph, case=case)
    authority = build_authority_packet(
        reasoning_plan_card_ids(reasoning_plan), load_json(NORM_CARD_PATH)
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


def unit_card_ids(unit: dict) -> list[str]:
    return [item["card_id"] for item in unit["card_assessments"]] + [
        item["card_id"] for item in unit["deterministic_rules"]
    ]


def valid_answer(plan: dict) -> dict:
    sections = []
    for unit in plan["units"]:
        sections.append(
            {
                "section_id": unit["unit_id"],
                "heading": unit["issue"],
                "body": "법리는 입력 법리에 따른다. 사안의 사실과 법리를 연결하면 요건이 충족된다. 따라서 이 구성요건은 충족된다.",
                "cited_fact_ids": unit["required_fact_ids"],
                "cited_card_ids": unit_card_ids(unit),
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


def valid_irac_slot_draft(plan: dict) -> dict:
    units = {}
    for unit in plan["units"]:
        applications = {}
        for assessment in unit["card_assessments"]:
            if assessment["card_id"] == "fraud_intent.no_disposition_inducement_intent":
                text = "乙은 돈을 빌려내기 위해 B를 속였으므로 B의 처분을 유도할 의사가 있었다."
            else:
                text = assessment["application_bridge"]
            applications[assessment["card_id"]] = text
        units[unit["unit_id"]] = {
            "card_applications": applications,
        }
    return {
        "version": "1.0.0",
        "case_id": plan["case_id"],
        "method_id": "m5_irac_plan",
        "units": units,
        "summary_analysis": "기망에서 재산 취득까지의 객관적 요건과 주관적 요건이 연결된다.",
    }


def valid_claim_graph(answer: dict, plan: dict) -> dict:
    claims = []
    claim_number = 1
    for unit in plan["units"]:
        card_ids = unit_card_ids(unit)
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
        [card_id for unit in plan["units"] for card_id in unit_card_ids(unit)],
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
    assert "fraud_mistake.false_loan_purpose" in {
        item["card_id"] for item in first["items"]
    }
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
    deterministic = [
        item["card_id"]
        for unit in plan["units"]
        for item in unit["deterministic_rules"]
    ]
    assert len(observed) == 11
    assert len(set(observed)) == 11
    assert set(observed) == set(assessments["selected_card_ids"])
    assert len(deterministic) == 4
    assert len(set(observed + deterministic)) == 15
    assert {unit["required_conclusion"] for unit in plan["units"]} == {"satisfied"}


def test_irac_plan_preserves_unknown_unit_without_inventing_fact_provenance() -> None:
    case, fact_graph, assessments, authority, _ = plan_inputs()
    assessments = copy.deepcopy(assessments)
    target = next(
        item
        for item in assessments["assessments"]
        if item["card_id"] == "deception.fraud.standard.loan-purpose-materiality"
    )
    target["status"] = "unknown"
    target["basis_fact_ids"] = []
    target["counter_fact_ids"] = []
    target["missing_facts"] = ["차용 목적이 대여 결정의 중요한 판단 기초였는지 여부"]
    target["rationale"] = "현재 사실만으로 차용 목적의 중요성을 확정할 수 없다."
    symbolic = {
        "legal_result": "undetermined",
        "observed_nonempty": {
            "fraud_elements_satisfied": False,
            "fraud_established": False,
            "fraud_not_established": False,
            "fraud_undetermined": True,
            "fraud_conflict": False,
        },
    }

    plan = build_fraud_irac_plan(
        case=case,
        fact_graph=fact_graph,
        assessment_bundle=assessments,
        authority_packet=authority,
        symbolic_result=symbolic,
    )
    deception_unit = next(
        unit for unit in plan["units"] if unit["unit_id"] == "irac_deception"
    )
    expected_fact_ids = sorted(
        {
            fact_id
            for assessment in deception_unit["card_assessments"]
            for fact_id in assessment["basis_fact_ids"]
            + assessment["counter_fact_ids"]
        }
    )
    assert deception_unit["required_fact_ids"] == expected_fact_ids
    assert deception_unit["required_conclusion"] == "unknown"

    answer = compile_fraud_irac_slot_draft(
        valid_irac_slot_draft(plan), plan=plan, case=case
    )
    deception_section = next(
        section
        for section in answer["sections"]
        if section["section_id"] == "irac_deception"
    )
    assert deception_section["cited_fact_ids"] == expected_fact_ids
    assert deception_section["stated_conclusion"] == "unknown"
    assert answer["overall_conclusion"] == "undetermined"


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


def test_plan_locked_irac_slots_compile_exact_provenance() -> None:
    plan, case, _, _, _ = compiled_plan()
    draft = valid_irac_slot_draft(plan)
    answer = compile_fraud_irac_slot_draft(draft, plan=plan, case=case)

    assert assess_irac_answer_alignment(answer, plan) == []
    assert answer["method_id"] == "m5_irac_plan"
    assert sum(len(section["cited_card_ids"]) for section in answer["sections"]) == 15
    intent = next(
        section for section in answer["sections"] if section["section_id"] == "irac_intent"
    )
    assert "fraud_intent.no_disposition_inducement_intent" in intent["cited_card_ids"]
    assert "B의 처분을 유도할 의사가 있었다" in intent["body"]
    assert answer["summary"].endswith("乙의 B에 대한 사기죄는 성립한다.")


def test_current_m5_compiles_one_document_level_irac_without_an_answer_call() -> None:
    plan, case, _, _, _ = compiled_plan()
    plan = copy.deepcopy(plan)
    plan["units"][0]["card_assessments"][0]["application_bridge"] = (
        "; 사건의 금전은 B가 乙에게 교부한 재물이다"
    )

    answer = compile_fraud_whole_irac_answer(plan=plan, case=case)
    assert [section["section_id"] for section in answer["sections"]] == [
        "irac_issue",
        "irac_rule",
        "irac_application",
        "irac_conclusion",
    ]
    assert assess_irac_answer_alignment(answer, plan) == []
    application = answer["sections"][2]
    assert "; 사건의 금전" not in application["body"]
    assert "사건의 금전은 B가 乙에게 교부한 재물이다." in application["body"]
    for unit in plan["units"]:
        assert unit["issue"] in application["body"]
    markdown = render_long_form_markdown(answer)
    assert "## 1. 쟁점 (Issue)" in markdown
    assert "## 2. 법리 (Rule)" in markdown
    assert "## 3. 사안의 적용 (Application)" in markdown
    assert "## 4. 결론 (Conclusion)" in markdown
    assert "## 종합 결론" not in markdown

    runner_source = MATRIX_SCRIPT_PATH.read_text(encoding="utf-8")
    assert "compile_fraud_whole_irac_answer" in runner_source
    assert "IRAC_SLOT_PROMPT_PATH" not in runner_source
    assert 'method_dir / "assessment_model_output.json"' in runner_source


def test_whole_irac_never_exposes_internal_uncertainty_metadata() -> None:
    plan, case, _, _, _ = compiled_plan()
    plan = copy.deepcopy(plan)
    card = plan["units"][0]["card_assessments"][0]
    card["status"] = "unknown"
    card["missing_facts"] = ["대상 재물의 소유관계"]
    card["application_bridge"] = (
        "사건 텍스트상 'unresolved_questions'로 남아있다."
    )
    plan["units"][0]["required_conclusion"] = "unknown"
    plan["overall_conclusion"] = "undetermined"

    answer = compile_fraud_whole_irac_answer(plan=plan, case=case)
    serialized = json.dumps(answer, ensure_ascii=False)
    assert "unresolved_questions" not in serialized
    assert "추가 확인이 필요한 사실 또는 증거" in answer["sections"][2]["body"]
    assert "대상 재물의 소유관계" in answer["sections"][2]["body"]

    plan, case, _, _, _ = compiled_plan()
    plan = copy.deepcopy(plan)
    plan["units"][0]["card_assessments"][0]["application_bridge"] = (
        "B가 금전을 교부하였다(fact_101)."
    )
    answer = compile_fraud_whole_irac_answer(plan=plan, case=case)
    serialized = json.dumps(answer, ensure_ascii=False)
    assert "fact_101" not in serialized
    assert "B가 금전을 교부하였다." in answer["sections"][2]["body"]


def test_plan_locked_irac_schema_rejects_a_missing_card_slot() -> None:
    plan, _, _, _, _ = compiled_plan()
    draft = valid_irac_slot_draft(plan)
    missing_card = "fraud_intent.no_disposition_inducement_intent"
    del draft["units"]["irac_intent"]["card_applications"][missing_card]

    schema = build_fraud_irac_slot_schema(plan)
    assert any(
        error.validator == "required"
        for error in Draft202012Validator(schema).iter_errors(draft)
    )
    with pytest.raises(GenerationContractError, match="required property"):
        compile_fraud_irac_slot_draft(draft, plan=plan, case=plan_inputs()[0])


def test_plan_locked_irac_compiler_rejects_internal_marker_leakage() -> None:
    plan, case, _, _, _ = compiled_plan()
    draft = valid_irac_slot_draft(plan)
    draft["summary_analysis"] += '","card_applications'

    with pytest.raises(GenerationContractError, match="internal markers"):
        compile_fraud_irac_slot_draft(draft, plan=plan, case=case)


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


def test_claim_graph_normalizes_duplicate_provenance_ids() -> None:
    plan, _, fact_graph, authority, _ = compiled_plan()
    answer = valid_answer(plan)
    graph = valid_claim_graph(answer, plan)
    graph["claims"][0]["card_ids"] *= 2
    normalized, audit = normalize_claim_graph(graph)
    assert audit["change_count"] >= 1
    assert any(
        change["claim_id"] == "claim_001" and change["field"] == "card_ids"
        for change in audit["changes"]
    )
    assert len(normalized["claims"][0]["card_ids"]) == len(
        set(normalized["claims"][0]["card_ids"])
    )
    assert (
        validate_claim_graph(
            normalized,
            answer=answer,
            plan=plan,
            fact_graph=fact_graph,
            authority_packet=authority,
        )
        == []
    )


def test_claim_graph_uses_provenance_not_support_kind_label() -> None:
    plan, _, fact_graph, authority, _ = compiled_plan()
    answer = valid_answer(plan)
    graph = valid_claim_graph(answer, plan)
    application = next(
        claim for claim in graph["claims"] if claim["claim_type"] == "application"
    )
    application["support_kind"] = "authority_rule"
    assert (
        validate_claim_graph(
            graph,
            answer=answer,
            plan=plan,
            fact_graph=fact_graph,
            authority_packet=authority,
        )
        == []
    )


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


def test_patch_normalization_removes_only_duplicate_provenance_ids() -> None:
    plan, _, _, _, _ = compiled_plan()
    answer = valid_answer(plan)
    failed_id = plan["units"][0]["unit_id"]
    replacement = copy.deepcopy(answer["sections"][0])
    replacement["cited_authority_comment_ids"].append(
        replacement["cited_authority_comment_ids"][0]
    )
    raw = {
        "version": "1.0.0",
        "case_id": plan["case_id"],
        "method_id": "m6_claim_verified",
        "patches": [replacement],
    }

    normalized, audit = normalize_section_patch_bundle(raw)
    normalized_ids = normalized["patches"][0]["cited_authority_comment_ids"]
    assert audit["change_count"] == 1
    assert len(normalized_ids) == len(set(normalized_ids))
    assert raw["patches"][0]["cited_authority_comment_ids"] != normalized_ids
    updated, _ = apply_section_patches(
        answer, normalized, failed_section_ids=[failed_id]
    )
    assert updated["sections"][0] == normalized["patches"][0]


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
    assert "IDPR_CASE_IDS" in source
    assert "IFS=':' read -r -a SELECTED_CASE_IDS" in source


def test_claim_prompt_bounds_graph_to_three_claims_per_section() -> None:
    source = CLAIM_PROMPT_PATH.read_text(encoding="utf-8")
    assert "한 단락당 3개" in source
    assert "총 15개 claim" in source


def test_active_m5_prompts_preserve_explicit_links_and_inference_consistency() -> None:
    fact_prompt = FACT_PROMPT_PATH.read_text(encoding="utf-8")
    assess_prompt = ASSESS_PROMPT_PATH.read_text(encoding="utf-8")
    assert "원문의 문법과 전체 맥락을 대조하여 신중하게 판정" in fact_prompt
    assert "인과적 순서를 직접" in fact_prompt
    assert "명시된 인과관계나 역할관계" in fact_prompt
    assert "발언이나 주문처럼" not in fact_prompt
    assert "`unresolved_questions`는 이전 추출 단계의 메모" in assess_prompt
    assert "처분 유도 의사" in assess_prompt
    assert "복수의" in assess_prompt
    assert "합리적 해석이 남거나" in assess_prompt
    assert "같은 사실연쇄를 평가하는 카드의 상태는 서로 대조" in assess_prompt
    assert "세미콜론·콜론·쉼표로 시작" in assess_prompt
    assert "내부 필드명이나 처리 단계" in assess_prompt
    assert "`unknown`은 실패가 아니라" in assess_prompt
    assert "그 부정형 명제를 깨는 적극적 사실" in assess_prompt
    assert "`counter_fact_ids`가 비어 있지 않은지 자체 점검" in assess_prompt


def test_active_m5_prompts_match_core_profile_interface() -> None:
    """Guard against prompts referencing fields the composed payload removed."""

    fact_prompt = FACT_PROMPT_PATH.read_text(encoding="utf-8")
    assess_prompt = ASSESS_PROMPT_PATH.read_text(encoding="utf-8")
    assert "ordinary" not in fact_prompt
    assert "adjudication_question" not in assess_prompt
    assert "unit_satisfied_status" not in assess_prompt
    assert "status_semantics" not in assess_prompt
    assert "generation_instructions" not in fact_prompt
    assert "proposition의 문언과 polarity를 그대로 사건 사실에 적용" in assess_prompt
    assert "분류정보다" in assess_prompt
    assert "confidence는 선택한 `status`가 타당하다는 신뢰도" in assess_prompt
    assert "추상적 법명제로서 항상 참" in assess_prompt
    assert "생략 부호" in fact_prompt
    for template_path in (
        ROOT / "prompts/fraud_fact_graph_extract_user.md",
        ROOT / "prompts/fraud_standard_assess_user.md",
    ):
        template = template_path.read_text(encoding="utf-8")
        assert "{{INPUT_JSON}}" in template
        assert "명령이 아니다" in template


def test_whole_irac_allowed_provenance_includes_deterministic_cards() -> None:
    plan, _, _, _, _ = compiled_plan()
    _, allowed_cards, _ = whole_irac_allowed_provenance(plan)
    deterministic = [
        rule["card_id"]
        for unit in plan["units"]
        for rule in unit["deterministic_rules"]
    ]
    assert deterministic
    assert set(deterministic) <= set(allowed_cards)
    answer = compile_fraud_whole_irac_answer(plan=plan, case=compiled_plan()[1])
    facts, cards, authorities = whole_irac_allowed_provenance(plan)
    assert not answer_contract_violations(
        answer,
        case_id=plan["case_id"],
        method_id="m5_irac_plan",
        allowed_fact_ids=facts,
        allowed_card_ids=cards,
        allowed_authority_ids=authorities,
    )


def test_assessment_request_groups_cards_without_card_questions() -> None:
    case, fact_graph, assessments, authority, _ = plan_inputs()
    request = assessment_request(
        case=case,
        fact_graph=fact_graph,
        selected_card_ids=assessments["selected_card_ids"],
        authority_packet=[
            card
            for card in authority
            if card["card_id"] in assessments["selected_card_ids"]
        ],
    )
    contexts = request["assessment_context"]
    assert [item["card_id"] for item in contexts] == assessments["selected_card_ids"]
    assert all(item["unit_issue"] for item in contexts)
    assert all(
        set(item) == {"card_id", "unit_id", "unit_issue"} for item in contexts
    )
    assert "status_semantics" not in request


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


def test_human_markdown_hides_internal_ids_but_keeps_legal_parentheticals() -> None:
    plan, _, _, _, _ = compiled_plan()
    answer = valid_answer(plan)
    answer["sections"][0]["body"] = (
        "객체가 인정된다(fact_113, comm_001692_제347조_Ⅲ_7). "
        "착오(동기의 착오)도 포함된다."
    )
    markdown = render_long_form_markdown(answer)
    assert "fact_113" not in markdown
    assert "comm_001692" not in markdown
    assert "착오(동기의 착오)" in markdown

    answer["sections"][0]["body"] = (
        "적용된다(fact_113; general_object.fraud.definition.property-benefit). "
        "결론은 미확정이다(unknown)."
    )
    markdown = render_long_form_markdown(answer)
    assert "fact_113" not in markdown
    assert "general_object.fraud.definition.property-benefit" not in markdown
    assert "(unknown)" not in markdown


def test_registry_asks_the_negative_intent_card_as_an_affirmative_proposition() -> None:
    case = load_json(CASE_PATH)
    replay = load_json(REPLAY_PATH)
    fact_graph, _ = anchor_fraud_target_roles(replay["fact_graph"], case)
    plan = select_fraud_reasoning_plan(fact_graph, case=case)
    queries = reasoning_plan_neural_queries(plan)
    assert set(queries) == {"fraud_intent.no_disposition_inducement_intent"}
    query = queries["fraud_intent.no_disposition_inducement_intent"]
    assert query["card_status_when_query_satisfied"] == "not_satisfied"
    assert "있었다" in query["proposition"]

    packet = build_authority_packet(
        select_fraud_card_plan(fact_graph),
        load_json(NORM_CARD_PATH),
        neural_queries=queries,
    )
    asked = {item["card_id"]: item for item in packet}
    negative = asked["fraud_intent.no_disposition_inducement_intent"]
    assert negative["proposition"] == query["proposition"]
    assert negative["polarity"] == "positive"
    assert "성립하지 않는다" not in negative["proposition"]
    assert negative["sources"], "reviewed authority must survive the substitution"

    reviewed = build_authority_packet(
        reasoning_plan_card_ids(plan), load_json(NORM_CARD_PATH)
    )
    cited = {item["card_id"]: item for item in reviewed}
    assert (
        cited["fraud_intent.no_disposition_inducement_intent"]["proposition"]
        == "피기망자로 하여금 처분행위를 하게 할 의사가 없으면 사기죄가 성립하지 않는다."
    )


def test_negative_card_without_a_registered_query_never_reaches_the_model() -> None:
    with pytest.raises(NeuralContractError) as excinfo:
        build_authority_packet(
            ["fraud_intent.no_disposition_inducement_intent"],
            load_json(NORM_CARD_PATH),
            neural_queries={},
        )
    assert "neural_query" in str(excinfo.value)


def test_inverting_query_swaps_status_and_evidence_arrays() -> None:
    bundle = {
        "version": "1.0.0",
        "case_id": "case_x",
        "selected_card_ids": ["neg", "same"],
        "assessments": [
            {
                "assessment_id": "assessment_001",
                "card_id": "neg",
                "status": "satisfied",
                "basis_fact_ids": ["fact_105"],
                "counter_fact_ids": [],
                "missing_facts": [],
                "authority_comment_ids": ["comm_1"],
                "rationale": "A가 B의 처분행위를 유도하였다.",
                "confidence": 0.9,
            },
            {
                "assessment_id": "assessment_002",
                "card_id": "same",
                "status": "satisfied",
                "basis_fact_ids": ["fact_106"],
                "counter_fact_ids": [],
                "missing_facts": [],
                "authority_comment_ids": ["comm_2"],
                "rationale": "쉽게 간파할 수 있는 거짓말이었다.",
                "confidence": 0.8,
            },
        ],
    }
    resolved, trail = resolve_neural_query_statuses(
        bundle,
        {
            "neg": {
                "proposition": "행위자에게 처분행위를 하게 할 의사가 있었다.",
                "card_status_when_query_satisfied": "not_satisfied",
            },
            "same": {
                "proposition": "쉽게 간파할 수 있는 단순한 거짓말이었다.",
                "card_status_when_query_satisfied": "satisfied",
            },
        },
    )
    inverted, identical = resolved["assessments"]
    assert inverted["status"] == "not_satisfied"
    assert inverted["counter_fact_ids"] == ["fact_105"]
    assert inverted["basis_fact_ids"] == []
    assert identical["status"] == "satisfied"
    assert identical["basis_fact_ids"] == ["fact_106"]
    assert bundle["assessments"][0]["status"] == "satisfied", "input must not mutate"
    assert [item["query_status"] for item in trail] == ["satisfied", "satisfied"]
    assert [item["card_status"] for item in trail] == ["not_satisfied", "satisfied"]


def test_safety_net_demotes_non_establishment_resting_on_establishing_facts() -> None:
    norm_cards = {
        "cards": [
            {"id": "neg", "polarity": "negative"},
            {"id": "pos", "polarity": "positive"},
        ]
    }
    bundle = {
        "assessments": [
            {
                "assessment_id": "assessment_001",
                "card_id": "pos",
                "status": "satisfied",
                "basis_fact_ids": ["fact_105"],
                "counter_fact_ids": [],
                "missing_facts": [],
            },
            {
                "assessment_id": "assessment_002",
                "card_id": "neg",
                "status": "satisfied",
                "basis_fact_ids": ["fact_105"],
                "counter_fact_ids": [],
                "missing_facts": [],
            },
        ]
    }
    guarded, demotions = apply_negative_card_safety_net(
        bundle, norm_card_set=norm_cards
    )
    assert guarded["assessments"][1]["status"] == "unknown"
    assert guarded["assessments"][1]["missing_facts"], "unknown requires missing_facts"
    assert demotions[0]["card_id"] == "neg"
    assert demotions[0]["overlapping_fact_ids"] == "fact_105"
    assert guarded["assessments"][0]["status"] == "satisfied"

    bundle["assessments"][1]["basis_fact_ids"] = ["fact_200"]
    untouched, none_demoted = apply_negative_card_safety_net(
        bundle, norm_card_set=norm_cards
    )
    assert untouched["assessments"][1]["status"] == "satisfied"
    assert none_demoted == []


def test_resolved_bundle_still_satisfies_the_assessment_contract() -> None:
    case = load_json(CASE_PATH)
    replay = load_json(REPLAY_PATH)
    fact_graph, _ = anchor_fraud_target_roles(replay["fact_graph"], case)
    plan = select_fraud_reasoning_plan(fact_graph, case=case)
    queries = reasoning_plan_neural_queries(plan)
    selected = select_fraud_card_plan(fact_graph)
    norm_cards = load_json(NORM_CARD_PATH)

    bundle = copy.deepcopy(replay["assessment_bundle"])
    for assessment in bundle["assessments"]:
        if assessment["card_id"] != "fraud_intent.no_disposition_inducement_intent":
            continue
        assessment["status"] = "satisfied"
        assessment["basis_fact_ids"] = ["fact_002", "fact_003"]
        assessment["counter_fact_ids"] = []

    resolved, trail = resolve_neural_query_statuses(bundle, queries)
    resolved, _ = apply_negative_card_safety_net(resolved, norm_card_set=norm_cards)
    validate_fraud_assessment_bundle(
        resolved,
        case=case,
        fact_graph=fact_graph,
        selected_card_ids=selected,
        authority_packet=build_authority_packet(
            selected, norm_cards, neural_queries=queries
        ),
    )
    assert trail[0]["card_status"] == "not_satisfied"
