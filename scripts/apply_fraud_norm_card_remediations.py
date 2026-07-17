from __future__ import annotations

import copy
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from idpr.rulegen import validate_norm_card_set  # noqa: E402


FRAUD_ROOT = PROJECT_ROOT / "data/rulegen/fraud"
CARD_MANIFEST = FRAUD_ROOT / "fraud_norm_card_manifest.json"
QUEUE = FRAUD_ROOT / "fraud_norm_card_review_queue.json"
DECISIONS = FRAUD_ROOT / "fraud_human_review_decisions.jsonl"
REQUESTS = FRAUD_ROOT / "fraud_rulegen_requests.jsonl"
COMMENTARY = (
    PROJECT_ROOT / "data/commentary/kcl_criminal_v1_commentary_chunks.jsonl"
)
LEDGER = FRAUD_ROOT / "fraud_norm_card_remediation_ledger.json"

PENDING_REMEDIATION = "accept_finding_pending_remediation"
IMMUTABLE_CARD_FIELDS = {
    "id",
    "candidate_refs",
    "norm_kind",
    "polarity",
    "source_refs",
    "request_ids",
}


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected object: {path}")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def append_unique(values: list[str], value: str) -> None:
    if value not in values:
        values.append(value)


def append_note(card: dict[str, Any], note: str) -> None:
    if note not in card["review_notes"]:
        card["review_notes"] = card["review_notes"].rstrip() + " " + note


def validate_card_sets(card_sets: dict[str, dict[str, Any]]) -> None:
    commentary = {
        row["comment_id"]: row
        for row in read_jsonl(COMMENTARY)
        if row["law_id"] == "001692" and row["article_no"] == "제347조"
    }
    request_scope = {
        request["request_id"]: {
            chunk["comment_id"] for chunk in request["commentary_chunks"]
        }
        for request in read_jsonl(REQUESTS)
    }
    for card_set in card_sets.values():
        validate_norm_card_set(card_set, commentary, request_scope)


def main() -> None:
    manifest = read_json(CARD_MANIFEST)
    module_paths = {
        row["module"]: PROJECT_ROOT / row["path"]
        for row in manifest["modules"]
    }
    card_sets = {module: read_json(path) for module, path in module_paths.items()}
    cards_by_id = {
        card["id"]: card
        for card_set in card_sets.values()
        for card in card_set["cards"]
    }
    card_module = {
        card["id"]: module
        for module, card_set in card_sets.items()
        for card in card_set["cards"]
    }
    originals = copy.deepcopy(cards_by_id)

    decision_rows = read_jsonl(DECISIONS)
    decisions = {row["review_id"]: row for row in decision_rows}
    queue = read_json(QUEUE)["items"]
    queue_by_id = {row["review_id"]: row for row in queue}
    accepted = {
        review_id
        for review_id, decision in decisions.items()
        if decision.get("decision") == PENDING_REMEDIATION
    }
    if len(accepted) != 57:
        raise ValueError(f"Expected 57 accepted remediations, found {len(accepted)}")
    expected = {
        review_id
        for review_id in accepted
        if decisions[review_id].get("status") == "pending"
    }
    completed = {
        review_id
        for review_id in accepted
        if decisions[review_id].get("status") == "completed"
    }
    if completed == accepted:
        ledger = read_json(LEDGER)
        applied = {
            row["review_id"]
            for row in ledger.get("finding_resolutions", [])
            if row.get("remediation_status") == "applied"
        }
        if (
            ledger.get("api_calls") != 0
            or ledger.get("accepted_findings") != 57
            or ledger.get("handled_findings") != 57
            or applied != accepted
        ):
            raise ValueError("Completed remediation state does not match the ledger")
        validate_card_sets(card_sets)
        print(
            json.dumps(
                {
                    "accepted_findings": 57,
                    "already_applied": True,
                    "api_calls": 0,
                    "changed_cards": ledger["changed_cards"],
                    "handled_findings": 57,
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return
    if completed or expected != accepted:
        raise ValueError("Accepted remediations must be uniformly pending or completed")
    if not expected <= set(queue_by_id):
        raise ValueError("A remediation decision is missing from the review queue")

    handled: set[str] = set()
    records: dict[str, dict[str, Any]] = {}

    def impacted(review_id: str) -> list[str]:
        return queue_by_id[review_id]["impacted_card_ids"]

    def resolve(
        review_id: str,
        *,
        summary: str,
        card_ids: list[str] | tuple[str, ...] = (),
        questions: list[str] | tuple[str, ...] = (),
        gaps: list[str] | tuple[str, ...] = (),
    ) -> None:
        if review_id in handled:
            raise ValueError(f"Duplicate remediation handler: {review_id}")
        if review_id not in expected:
            raise ValueError(f"Unexpected remediation handler: {review_id}")
        handled.add(review_id)
        records[review_id] = {
            "review_id": review_id,
            "module": queue_by_id[review_id]["module"],
            "finding_type": queue_by_id[review_id]["type"],
            "decision": PENDING_REMEDIATION,
            "remediation_status": "applied",
            "summary": summary,
            "card_ids": sorted(set(card_ids)),
            "legal_review_questions": list(questions),
            "coverage_gaps": list(gaps),
        }

    def update(card_id: str, **changes: Any) -> None:
        card = cards_by_id[card_id]
        unknown = set(changes) - set(card)
        if unknown:
            raise ValueError(f"Unknown fields for {card_id}: {sorted(unknown)}")
        card.update(changes)

    def mark_cards(
        card_ids: list[str] | tuple[str, ...],
        note: str,
        **changes: Any,
    ) -> None:
        for card_id in card_ids:
            update(card_id, **changes)
            append_note(cards_by_id[card_id], note)

    def add_question(module: str, question: str) -> None:
        append_unique(card_sets[module]["legal_review_questions"], question)

    def add_gap(module: str, gap: str) -> None:
        append_unique(card_sets[module]["coverage_gaps"], gap)

    # Proposition and source-scope corrections.
    review_id = (
        "fraud.normcards.concurrence.part002.critic."
        "assigned_claim_outcome_overstated"
    )
    card_id = "fraud_concurrence.assigned_claim_mutually_incompatible"
    update(
        card_id,
        proposition=(
            "2011도1442 사안에서는 담보 양도채권의 가치와 채권양도에 관한 "
            "피고인의 진정성 등을 심리하여 차용금 사기와 양도채권 횡령 중 어느 "
            "죄에 해당하는지 가려야 하므로, 두 죄를 모두 인정한 원심에 법리오해와 "
            "심리미진의 위법이 있다고 판단하였다."
        ),
    )
    append_note(cards_by_id[card_id], "2011도1442의 사안별 판단 범위로 한정했다.")
    resolve(review_id, summary="사안별 판례 결론으로 명제를 축소했다.", card_ids=[card_id])

    review_id = (
        "fraud.normcards.damage_acquisition.part002.critic."
        "unsupported_variant_policy_question"
    )
    question = (
        "재산상 손해 필요성에 관한 부정설·긍정설·제한적 긍정설과 관련 판례의 "
        "존재 및 적용 범위를 추가 권위로 확인하고, 확인 전에는 특정 실무 정책을 "
        "선택하지 않는다."
    )
    card_sets["damage_acquisition"]["legal_review_questions"][2] = question
    resolve(review_id, summary="근거 없는 정책 선택 요구를 권위 확인 질문으로 바꿨다.", questions=[question])

    # Authority corrections. Case outcomes without direct primary verification remain
    # context-only even when the commentary clearly reports a precedent.
    authority_actions: dict[str, dict[str, Any]] = {
        "fraud.normcards.damage_acquisition.part001.critic.authority.case_cards_mislabeled": {
            "authority_basis": "commentary_reported_precedent",
            "doctrinal_status": "precedent_position",
            "review_required": True,
        },
        "fraud.normcards.damage_acquisition.part002.critic.letter_credit_authority": {
            "authority_basis": "commentary_reported_precedent",
            "doctrinal_status": "precedent_position",
            "formalization": "context_only",
            "review_required": True,
        },
        "fraud.normcards.damage_acquisition.part002.critic.repeated_investment_authority": {
            "authority_basis": "commentary_reported_precedent",
            "doctrinal_status": "precedent_position",
            "formalization": "context_only",
            "review_required": True,
        },
        "fraud.normcards.deception.part002.critic.authority.explicit_denial_opinion": {
            "authority_basis": "commentary_reported_doctrine",
            "doctrinal_status": "disputed",
            "formalization": "policy_variant",
            "review_required": True,
            "variant_group": "fraud_deception.encumbrance_disclosure_classification",
        },
        "fraud.normcards.deception.part003.critic.authority.additional-case-cards": {
            "authority_basis": "commentary_reported_precedent",
            "doctrinal_status": "precedent_position",
            "formalization": "context_only",
            "review_required": True,
        },
        "fraud.normcards.deception.part003.critic.authority.case-card-misclassified": {
            "authority_basis": "commentary_reported_precedent",
            "doctrinal_status": "precedent_position",
            "formalization": "context_only",
            "review_required": True,
        },
        "fraud.normcards.deception.part004.critic.authority.false_documents_speculative": {
            "authority_basis": "commentary_synthesis",
            "doctrinal_status": "descriptive",
            "formalization": "context_only",
            "review_required": True,
        },
        "fraud.normcards.deception.part004.critic.authority.statutory_subsidy_definitions": {
            "authority_basis": "statutory_text_in_commentary",
            "doctrinal_status": "descriptive",
            "formalization": "context_only",
            "review_required": True,
        },
        "fraud.normcards.general_object.part001.critic.unquantified_value_authority_unsupported": {
            "authority_basis": "commentary_synthesis",
            "doctrinal_status": "descriptive",
            "formalization": "context_only",
            "review_required": True,
        },
        "fraud.normcards.stages_participation.part001.critic.authority.real_estate_combined_sources": {
            "authority_basis": "commentary_reported_precedent",
            "doctrinal_status": "precedent_position",
            "formalization": "context_only",
            "review_required": True,
        },
        "fraud.normcards.stages_participation.part001.critic.authority.voice_phishing_commentary_view": {
            "authority_basis": "commentary_synthesis",
            "doctrinal_status": "descriptive",
            "formalization": "context_only",
            "review_required": True,
        },
    }
    for review_id, changes in authority_actions.items():
        card_ids = impacted(review_id)
        mark_cards(
            card_ids,
            "비평 지적에 따라 권위·법리상태·형식화를 보수적으로 재분류했다.",
            **changes,
        )
        resolve(review_id, summary="권위와 법리상태를 source-bounded 수준으로 낮췄다.", card_ids=card_ids)

    review_id = (
        "fraud.normcards.deception.part001.critic."
        "bid_rigging_author_view_authority"
    )
    card_ids = impacted(review_id)
    mark_cards(
        card_ids,
        "일반 학설이나 판례가 아니라 주석 작성자의 사견으로 한정했다.",
        authority_basis="commentary_synthesis",
        doctrinal_status="descriptive",
        formalization="context_only",
        review_required=True,
        variant_group=None,
    )
    resolve(review_id, summary="입찰담합 견해를 주석자 사견 및 context_only로 정정했다.", card_ids=card_ids)

    review_id = (
        "fraud.normcards.deception.part001.critic."
        "bid_rigging_policy_question_overstates_alignment"
    )
    question = (
        "입찰담합과 사기죄의 관계는 주석 작성자의 사견과 사기죄 판단을 명시적으로 "
        "유보한 판례 설명을 구별하고, 원판례 또는 추가 권위를 확인하기 전에는 "
        "RuleIR 정책으로 선택하지 않는다."
    )
    card_sets["deception"]["legal_review_questions"][2] = question
    resolve(review_id, summary="주석자 사견과 판례 유보를 구별하는 질문으로 축소했다.", questions=[question])

    descriptive_status_findings = (
        "fraud.normcards.deception.part002.critic.status.unsupported_settled",
        "fraud.normcards.deception.part005.critic.unsupported-settled-status",
        "fraud.normcards.deception.part005.critic.unsupported-settled-status-disposal-authority",
        "fraud.normcards.deception.part005.critic.unsupported-settled-status-distinct-persons",
        "fraud.normcards.deception.part005.critic.unsupported-settled-status-unspecified-person",
        "fraud.normcards.general_object.part001.critic.settled_status_not_supported",
    )
    for review_id in descriptive_status_findings:
        card_ids = impacted(review_id)
        mark_cards(
            card_ids,
            "bounded source가 settled를 입증하지 않아 descriptive로 낮췄다.",
            doctrinal_status="descriptive",
            review_required=True,
        )
        resolve(review_id, summary="근거 없는 settled 지정을 descriptive로 낮췄다.", card_ids=card_ids)

    review_id = "fraud.normcards.intent.part001.critic.no_disposition_authority_unestablished"
    card_ids = impacted(review_id)
    mark_cards(
        card_ids,
        "일반 설명의 권위 확인 전 법률검토를 유지한다.",
        doctrinal_status="descriptive",
        review_required=True,
    )
    resolve(review_id, summary="권위 미확인 상태를 명시하고 법률검토 대상으로 전환했다.", card_ids=card_ids)

    # The part004 critic correctly identified mass case-law overformalization. Keep the
    # two general definitions as rules, but move all case applications to RAG context.
    review_id = (
        "fraud.normcards.deception.part004.critic."
        "authority.classification_not_source_grounded"
    )
    card_ids = impacted(review_id)
    for card_id in card_ids:
        card = cards_by_id[card_id]
        changes: dict[str, Any] = {"review_required": True}
        if card["formalization"] == "standard_input":
            changes["formalization"] = "context_only"
        if card["doctrinal_status"] == "settled":
            changes["doctrinal_status"] = "descriptive"
        update(card_id, **changes)
        append_note(
            card,
            "사안별 판례·권위 확인 전 RuleIR 입력에서 제외하고 RAG 문맥으로 보존한다.",
        )
    question = (
        "어음·보조금·종교·의료기관·법인 피해자 관련 사안별 카드의 원판례와 "
        "일반화 가능 범위를 확인하기 전에는 context_only/RAG 자료로만 사용한다."
    )
    add_question("deception", question)
    resolve(
        review_id,
        summary="사안별 카드 44개를 context_only로 내리고 전 카드 권위검토를 표시했다.",
        card_ids=card_ids,
        questions=[question],
    )

    # Special-form authority findings concern four cumulative litigation-fraud elements,
    # not only the one card named by Sol's unstable numeric selector.
    review_id = (
        "fraud.normcards.special_forms.part001.critic."
        "f3.unsupported_authority_and_settled_designations"
    )
    card_ids = [
        "special_forms.fraud.element.litigation-fraud-knowing-nonexistence",
        "special_forms.fraud.element.litigation-fraud-deceptive-act",
        "special_forms.fraud.element.judgment-substitutes-victim-disposition",
        "special_forms.fraud.element.litigation-fraud-commencement",
    ]
    mark_cards(
        card_ids,
        "원판례 확인 전 독립 deterministic rule이 아닌 standard input으로 유지한다.",
        doctrinal_status="descriptive",
        formalization="standard_input",
        review_required=True,
    )
    resolve(review_id, summary="영향받은 소송사기 요소 4개를 보수적으로 재분류했다.", card_ids=card_ids)

    review_id = (
        "fraud.normcards.special_forms.part001.critic."
        "f4.definition_authority_mismatch"
    )
    card_ids = impacted(review_id)
    mark_cards(
        card_ids,
        "특정 판례가 아니라 주석의 일반 설명으로 정정했다.",
        authority_basis="commentary_synthesis",
        doctrinal_status="descriptive",
        review_required=True,
    )
    resolve(review_id, summary="소송사기 정의의 권위를 commentary_synthesis로 정정했다.", card_ids=card_ids)

    review_id = (
        "fraud.normcards.special_forms.part002.critic."
        "authority_status.settled_unsupported"
    )
    card_ids = impacted(review_id)
    mark_cards(
        card_ids,
        "현재 bounded source만으로 settled를 확정하지 않는다.",
        doctrinal_status="descriptive",
        review_required=True,
    )
    resolve(review_id, summary="보험사기 관련 settled 지정을 descriptive로 낮췄다.", card_ids=card_ids)

    review_id = (
        "fraud.normcards.mistake_disposition.part001.critic."
        "f4.unsupported_settled_status"
    )
    card_ids = impacted(review_id)
    mark_cards(
        card_ids,
        "권위 확인 전 인과관계 standard input으로 보존한다.",
        doctrinal_status="descriptive",
        formalization="standard_input",
        review_required=True,
    )
    resolve(review_id, summary="두 인과관계 카드를 standard_input/descriptive로 낮췄다.", card_ids=card_ids)

    # Formalization corrections.
    review_id = (
        "fraud.normcards.concurrence.part001.critic."
        "commentary_penalties_deterministic_before_verification"
    )
    card_ids = impacted(review_id)
    mark_cards(
        card_ids,
        "현행 법령 직접 확인 전 형벌 규칙을 실행하지 않는다.",
        formalization="context_only",
        review_required=True,
    )
    question = "형법 및 특정경제범죄법상 사기죄 법정형·상습·미수 규정의 현행 조문을 직접 확인한다."
    add_question("concurrence", question)
    resolve(review_id, summary="현행법 미확인 형벌 카드 3개를 context_only로 내렸다.", card_ids=card_ids, questions=[question])

    review_id = (
        "fraud.normcards.damage_acquisition.part001.critic."
        "exception.variant_link_missing"
    )
    card_ids = impacted(review_id)
    mark_cards(
        card_ids,
        "후순위 근저당권 이득액 원칙의 예외로 같은 그룹에 연결했다.",
        variant_group="fraud_damage_acquisition.junior_mortgage_gain_cap",
        review_required=True,
    )
    resolve(review_id, summary="후순위 근저당권 원칙과 예외의 그룹을 연결했다.", card_ids=card_ids)

    formalization_actions: dict[str, dict[str, Any]] = {
        "fraud.normcards.deception.part003.critic.formalization.conditional-intent-sufficiency": {
            "formalization": "standard_input",
            "review_required": True,
        },
        "fraud.normcards.deception.part003.critic.formalization.element-sufficiency": {
            "formalization": "standard_input",
            "review_required": True,
        },
        "fraud.normcards.deception.part004.critic.formalization.subsidy_definition": {
            "formalization": "context_only",
            "review_required": True,
        },
        "fraud.normcards.general_object.part001.critic.subjective_elements_formalization": {
            "formalization": "policy_variant",
            "variant_group": "fraud_intent.illegal_appropriation_requirement",
            "review_required": True,
        },
    }
    for review_id, changes in formalization_actions.items():
        card_ids = impacted(review_id)
        mark_cards(
            card_ids,
            "이 카드만으로 사기죄 전체 성립을 도출하지 않도록 형식화를 수정했다.",
            **changes,
        )
        resolve(review_id, summary="독립 충분조건으로 오해되지 않도록 형식화를 수정했다.", card_ids=card_ids)

    review_id = (
        "fraud.normcards.intent.part001.critic."
        "practical_consequence_not_selectable_variant"
    )
    practical_card = "fraud_intent.property_only_appropriation_practical_consequence"
    update(practical_card, formalization="context_only", review_required=True)
    append_note(cards_by_id[practical_card], "재물편취죄 한정 필요설의 설명적 귀결로만 사용한다.")
    question = (
        "불법영득의사 정책 선택은 불요설·전면 필요설·재물편취죄 한정 필요설의 "
        "세 견해와 판례 입장만 대상으로 하고, 설명적 귀결 카드는 선택지로 삼지 않는다."
    )
    card_sets["intent"]["legal_review_questions"][1] = question
    resolve(review_id, summary="설명적 귀결을 정책 선택지에서 제외했다.", card_ids=[practical_card], questions=[question])

    # Explicitly unify every accepted competing-view or fact-variant group.
    group_actions: dict[str, tuple[str, list[str]]] = {
        "fraud.normcards.mistake_disposition.part001.critic.f2.disposition_intent_variant_groups": (
            "fraud_mistake.disposition_intent_requirement",
            impacted("fraud.normcards.mistake_disposition.part001.critic.f2.disposition_intent_variant_groups"),
        ),
        "fraud.normcards.mistake_disposition.part001.critic.f3.voluntariness_variant_groups": (
            "fraud_mistake.disposition_voluntariness",
            impacted("fraud.normcards.mistake_disposition.part001.critic.f3.voluntariness_variant_groups"),
        ),
        "fraud.normcards.concurrence.part001.critic.agent_competing_position_group_incomplete": (
            "fraud_concurrence.agent_deceives_principal",
            impacted("fraud.normcards.concurrence.part001.critic.agent_competing_position_group_incomplete"),
        ),
        "fraud.normcards.concurrence.part001.critic.counterfeit_variant_group_incomplete": (
            "fraud_concurrence.counterfeit_currency_fraud",
            impacted("fraud.normcards.concurrence.part001.critic.counterfeit_variant_group_incomplete"),
        ),
        "fraud.normcards.deception.part001.critic.future_facts_variant_group_split": (
            "fraud_deception.future_fact_scope",
            impacted("fraud.normcards.deception.part001.critic.future_facts_variant_group_split"),
        ),
        "fraud.normcards.deception.part001.critic.opinion_statement_variant_group_split": (
            "fraud_deception.opinion_statement",
            impacted("fraud.normcards.deception.part001.critic.opinion_statement_variant_group_split"),
        ),
        "fraud.normcards.deception.part001.critic.third_view_supplement_ungrouped": (
            "fraud_deception.opinion_statement",
            impacted("fraud.normcards.deception.part001.critic.third_view_supplement_ungrouped"),
        ),
        "fraud.normcards.deception.part002.critic.variant_group.dine_stay_views": (
            "fraud_deception.dine_stay_classification",
            impacted("fraud.normcards.deception.part002.critic.variant_group.dine_stay_views"),
        ),
        "fraud.normcards.deception.part002.critic.variant_group.disposition_views": (
            "fraud_deception.disposition_nondisclosure_classification",
            impacted("fraud.normcards.deception.part002.critic.variant_group.disposition_views"),
        ),
        "fraud.normcards.deception.part003.critic.variants.double-sale": (
            "fraud_deception.double_sale_fact_variants",
            impacted("fraud.normcards.deception.part003.critic.variants.double-sale"),
        ),
        "fraud.normcards.deception.part003.critic.variants.nonmedical-clinic": (
            "fraud_deception.nonmedical_clinic_claimant",
            impacted("fraud.normcards.deception.part003.critic.variants.nonmedical-clinic"),
        ),
        "fraud.normcards.deception.part004.critic.variant.medical_corporation_exception": (
            "fraud_deception.medical_corporation_involvement",
            impacted("fraud.normcards.deception.part004.critic.variant.medical_corporation_exception"),
        ),
        "fraud.normcards.deception.part004.critic.variant.religious_practice_boundary": (
            "fraud_deception.religious_practice_boundary",
            impacted("fraud.normcards.deception.part004.critic.variant.religious_practice_boundary"),
        ),
        "fraud.normcards.general_object.part001.critic.sex_work_variants_not_grouped": (
            "fraud_general_object.sex_work_contract",
            impacted("fraud.normcards.general_object.part001.critic.sex_work_variants_not_grouped"),
        ),
        "fraud.normcards.special_forms.part002.critic.variant_group.illegal_cause_split": (
            "fraud_special_forms.illegal_cause_benefit",
            impacted("fraud.normcards.special_forms.part002.critic.variant_group.illegal_cause_split")
            + ["special_forms.fraud.standard.illegal-cause-benefit-precedent-affirmative"],
        ),
        "fraud.normcards.special_forms.part002.critic.variant_group.right_exercise_split": (
            "fraud_special_forms.right_exercise_boundary",
            impacted("fraud.normcards.special_forms.part002.critic.variant_group.right_exercise_split")
            + [
                "special_forms.fraud.standard.right-exercise-over-limit-fraud",
                "special_forms.fraud.standard.right-exercise-socially-acceptable-no-crime",
            ],
        ),
        "fraud.normcards.stages_participation.part001.critic.variant.completion_without_gain": (
            "fraud_stages_participation.completion_threshold",
            impacted("fraud.normcards.stages_participation.part001.critic.variant.completion_without_gain"),
        ),
    }
    for review_id, (group_id, card_ids) in group_actions.items():
        mark_cards(
            card_ids,
            f"관련 경쟁 견해 또는 사실변형을 {group_id}로 연결했다.",
            variant_group=group_id,
            review_required=True,
        )
        resolve(review_id, summary=f"관련 카드를 공통 그룹 {group_id}로 통합했다.", card_ids=card_ids)

    review_id = (
        "fraud.normcards.damage_acquisition.part001.critic."
        "variant_group.property_loss_fragmented"
    )
    card_ids = [
        card_id
        for card_id, card in cards_by_id.items()
        if card_module[card_id] == "damage_acquisition"
        and (
            card_id.startswith("damage_acquisition.fraud.variant-property-loss-requirement-")
            or card["variant_group"] == "fraud_damage_acquisition.property_loss_requirement"
        )
    ]
    mark_cards(
        card_ids,
        "재산상 손해 필요성의 개괄·구체 견해를 하나의 정책 그룹으로 연결했다.",
        variant_group="fraud_damage_acquisition.property_loss_requirement",
        review_required=True,
    )
    resolve(review_id, summary="분절된 재산상 손해 필요성 카드를 공통 그룹으로 통합했다.", card_ids=card_ids)

    review_id = (
        "fraud.normcards.mistake_disposition.part001.critic."
        "f1.collapsed_triangular_fraud_variants"
    )
    card_ids = [
        card_id
        for card_id in cards_by_id
        if card_module[card_id] == "mistake_disposition"
        and "triangular-fraud" in card_id
    ] + ["fraud_mistake.triangular_fraud_theories"]
    card_ids = sorted(set(card_ids))
    mark_cards(
        card_ids,
        "삼각사기 권한기준의 개별 학설·판례해석을 하나의 정책 그룹에 보존했다.",
        variant_group="fraud_mistake.triangular_fraud_authority",
        review_required=True,
    )
    resolve(review_id, summary="이미 분리된 삼각사기 세부 카드를 공통 그룹으로 연결했다.", card_ids=card_ids)

    # The litigation-fraud critic used variant_group for a broader issue taxonomy.
    # Preserve that accepted relationship without pretending cumulative elements are
    # mutually exclusive policy choices: only fact-pattern alternatives get groups.
    review_id = (
        "fraud.normcards.special_forms.part001.critic."
        "f5.missing_variant_grouping"
    )
    special_ids = impacted(review_id)
    litigation_groups = {
        "fraud_special_forms.litigation_strict_proof": {
            card_id
            for card_id in special_ids
            if any(
                token in card_id
                for token in (
                    "strict-interpretation",
                    "objectively-false-or-knowing",
                    "knowing-nonexistence",
                    "mistake-of-fact-or-law",
                    "civil-loss-alone",
                    "excess-distribution",
                    "duplicate-mortgage",
                    "loan-claim-lack",
                    "excessive-hospitalization",
                    "inflated-construction",
                    "circular-remittance",
                    "attorney-fee",
                )
            )
        },
        "fraud_special_forms.litigation_deceptive_means": {
            card_id
            for card_id in special_ids
            if any(
                token in card_id
                for token in (
                    "defendant-active",
                    "deceptive-act",
                    "omission-of-favorable",
                    "false-claim-alone",
                    "forged-possession",
                    "unilateral-notice",
                    "altered-evidence",
                    "false-payment-order",
                    "payment-order-premature",
                )
            )
        },
        "fraud_special_forms.litigation_disposition_effect": {
            card_id
            for card_id in special_ids
            if any(
                token in card_id
                for token in (
                    "definition.litigation-fraud-triangular",
                    "judgment-substitutes",
                    "dead-or-nonexistent",
                    "building-permit",
                    "nominal-permit",
                    "litigation-costs",
                    "nominal-depositor",
                    "bill-public-summons",
                    "compensation-claim",
                    "adverse-possession",
                    "collusive-suit",
                    "false-illegal-occupancy",
                    "false-title-transfer",
                    "invalid-mortgage",
                    "assignment-order",
                    "changed-tenant",
                    "third-party-real-property",
                    "false-loss-public-summons",
                )
            )
        },
        "fraud_special_forms.litigation_stage": {
            card_id
            for card_id in special_ids
            if any(
                token in card_id
                for token in (
                    "indirect-perpetration",
                    "completion-final-judgment",
                    "false-land-registration",
                    "false-guarantee-letter",
                    "provisional-attachment",
                    "enforcement-",
                    "sham-mortgage",
                    "inflated-lien",
                    "litigation-fraud-commencement",
                )
            )
        },
    }
    grouped = set().union(*litigation_groups.values())
    remaining = set(special_ids) - grouped
    if remaining:
        litigation_groups["fraud_special_forms.litigation_case_applications"] = remaining
    for group_id, card_ids_in_group in litigation_groups.items():
        mark_cards(
            sorted(card_ids_in_group),
            f"소송사기 검토상 관련 사실변형을 {group_id}로 연결했다.",
            variant_group=group_id,
            review_required=True,
        )
    question = (
        "소송사기 카드의 strict proof, 기망수단, 처분효과, 착수·기수 사실변형은 "
        "검색용 그룹으로만 사용하고, 누적 구성요건을 상호배타적 정책으로 해석하지 않는다."
    )
    add_question("special_forms", question)
    resolve(
        review_id,
        summary="50개 소송사기 카드를 5개 사실변형 그룹으로 분류하고 정책그룹 오해를 금지했다.",
        card_ids=special_ids,
        questions=[question],
    )

    # Remaining metadata and duplication findings.
    review_id = (
        "fraud.normcards.concurrence.part002.critic."
        "sanction_cards_missing_review_question"
    )
    card_ids = impacted(review_id)
    mark_cards(
        card_ids,
        "현행 특별법 법정형과 적용요건 확인 전 RAG 문맥으로만 사용한다.",
        formalization="context_only",
        review_required=True,
    )
    question = (
        "특정경제범죄법, 보험사기방지 특별법, 군형법 및 군용물 관련 특별법의 "
        "현행 법정형과 적용요건을 직접 법령으로 확인한다."
    )
    add_question("concurrence", question)
    resolve(review_id, summary="특별법 제재 카드 4개를 context_only로 내리고 현행법 확인 질문을 추가했다.", card_ids=card_ids, questions=[question])

    review_id = (
        "fraud.normcards.damage_acquisition.part001.critic."
        "review_questions.reported_cases_incomplete"
    )
    card_ids = impacted(review_id)
    mark_cards(
        card_ids,
        "원판결과 일반화 범위 확인 전 사안별 판례로만 사용한다.",
        authority_basis="commentary_reported_precedent",
        doctrinal_status="precedent_position",
        formalization="context_only",
        review_required=True,
    )
    question = (
        "항소취하·가압류해제·신용장·반복투자 등 사안별 판례 카드의 원판결과 "
        "허용 가능한 일반화 범위를 확인한다."
    )
    add_question("damage_acquisition", question)
    resolve(review_id, summary="누락된 사안별 판례 확인 범위를 검토 질문에 추가했다.", card_ids=card_ids, questions=[question])

    review_id = (
        "fraud.normcards.mistake_disposition.part001.critic."
        "f5.duplicated_negligence_norm"
    )
    first = "mistake_disposition.fraud.causal-link.victim-negligence-irrelevant"
    second = "mistake_disposition.fraud.causal-link-mistake-not-sole-cause"
    update(
        first,
        proposition=(
            "기망행위는 착오의 유일한 원인일 필요가 없으므로, 피기망자 측 과실이 "
            "착오 발생에 함께 작용해도 기망행위와 착오 사이 인과관계는 부정되지 않는다."
        ),
    )
    update(
        second,
        proposition=(
            "착오는 처분행위의 유일한 원인일 필요가 없으므로, 피해자 과실이 함께 "
            "작용해도 착오와 처분행위 사이 인과관계는 부정되지 않는다."
        ),
    )
    append_note(cards_by_id[first], "기망행위-착오 단계에만 적용한다.")
    append_note(cards_by_id[second], "착오-처분행위 단계에만 적용한다.")
    resolve(review_id, summary="중복처럼 보인 두 인과관계 카드를 적용 단계별로 명확히 분리했다.", card_ids=[first, second])

    missing_handlers = sorted(expected - handled)
    extra_handlers = sorted(handled - expected)
    if missing_handlers or extra_handlers:
        raise ValueError(
            f"Remediation coverage mismatch: missing={missing_handlers}, extra={extra_handlers}"
        )

    # Prove that no patch changed provenance, identity, norm kind, or polarity.
    for card_id, original in originals.items():
        current = cards_by_id[card_id]
        for field in IMMUTABLE_CARD_FIELDS:
            if current[field] != original[field]:
                raise ValueError(f"Forbidden change: {card_id}.{field}")

    validate_card_sets(card_sets)

    change_records: list[dict[str, Any]] = []
    for card_id, original in originals.items():
        current = cards_by_id[card_id]
        changes = {
            field: {"before": original[field], "after": current[field]}
            for field in current
            if field not in IMMUTABLE_CARD_FIELDS and current[field] != original[field]
        }
        if changes:
            change_records.append(
                {
                    "card_id": card_id,
                    "module": card_module[card_id],
                    "changes": changes,
                }
            )

    for module, path in module_paths.items():
        write_json(path, card_sets[module])
    for decision in decision_rows:
        if decision["review_id"] not in expected:
            continue
        decision["status"] = "completed"
        completion_note = "승인된 지적을 수동 remediation ledger에 반영하고 검증했다."
        if completion_note not in decision["notes"]:
            decision["notes"] = decision["notes"].rstrip() + " " + completion_note
    DECISIONS.write_text(
        "".join(
            json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n"
            for row in decision_rows
        ),
        encoding="utf-8",
    )
    write_json(
        LEDGER,
        {
            "version": "1.0.0",
            "issue_tag": "fraud",
            "status": "draft",
            "legal_review": "pending",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "method": "manual_source_and_finding_audit_no_api",
            "api_calls": 0,
            "accepted_findings": len(expected),
            "handled_findings": len(handled),
            "changed_cards": len(change_records),
            "finding_resolutions": [records[key] for key in sorted(records)],
            "card_changes": sorted(change_records, key=lambda row: row["card_id"]),
        },
    )
    print(
        json.dumps(
            {
                "api_calls": 0,
                "accepted_findings": len(expected),
                "handled_findings": len(handled),
                "changed_cards": len(change_records),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
