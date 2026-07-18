from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from idpr.rulegen import validate_norm_card_set  # noqa: E402


FRAUD_ROOT = PROJECT_ROOT / "data/rulegen/fraud"
CARD_MANIFEST = FRAUD_ROOT / "fraud_norm_card_manifest.json"
REMEDIATION_LEDGER = FRAUD_ROOT / "fraud_norm_card_remediation_ledger.json"
REQUESTS = FRAUD_ROOT / "fraud_rulegen_requests.jsonl"
COMMENTARY = (
    PROJECT_ROOT / "data/commentary/kcl_criminal_v1_commentary_chunks.jsonl"
)
AUDIT = FRAUD_ROOT / "fraud_norm_card_audit.json"
POLICY_QUEUE = FRAUD_ROOT / "fraud_policy_review_queue.json"
POLICY_DECISIONS = FRAUD_ROOT / "fraud_policy_review_decisions.jsonl"
POLICY_GUIDE = FRAUD_ROOT / "fraud_policy_review_guide.md"
POLICY_RESOLUTION_AUDIT = FRAUD_ROOT / "fraud_policy_resolution_audit.json"
CORE_SELECTION_AUDIT = FRAUD_ROOT / "fraud_core_rule_selection_audit.json"
CORE_REVIEW_QUEUE = FRAUD_ROOT / "fraud_core_rule_review_queue.json"
CORE_REVIEW_DECISIONS = FRAUD_ROOT / "fraud_core_rule_review_decisions.jsonl"
CORE_REVIEW_GUIDE = FRAUD_ROOT / "fraud_core_rule_review_guide.md"
LOCAL_PRIMARY_SOURCE = (
    PROJECT_ROOT.parent
    / "sp/data/processed/Case_DB/clean_open_precedents.parquet"
)


def primary_record(record_id: int, decision_date: str) -> dict[str, Any]:
    return {
        "record_id": record_id,
        "decision_date": decision_date,
        "court": "대법원",
    }


VERIFIED_LOCAL_PRIMARY_RECORDS = {
    "75도760": primary_record(92643, "1975-05-27"),
    "2001도2991": primary_record(81008, "2001-10-23"),
    "2003도4914": primary_record(83025, "2003-12-26"),
    "2017도21196": primary_record(205752, "2018-04-12"),
    "95도2466": primary_record(113475, "1996-04-09"),
    "84도882": primary_record(99745, "1984-09-25"),
    "2018도13696": primary_record(211733, "2020-06-25"),
    "2007도2595": primary_record(191973, "2007-08-23"),
    "66도132": primary_record(152569, "1966-03-15"),
    "2021도8468": primary_record(219381, "2021-09-09"),
    "2016도13362": primary_record(184471, "2017-02-16"),
    "94도1575": primary_record(110881, "1994-10-11"),
    "2022도12494": primary_record(233095, "2022-12-29"),
    "80도2667": primary_record(96475, "1982-04-13"),
    "2001도1825": primary_record(82595, "2003-05-16"),
}


# Only general legal rules belong in the symbolic core. Concrete holdings, offense-value
# calculations, and cross-offense examples remain searchable RAG context.
CORE_DETERMINISTIC_IDS = {
    "fraud_general_object.causation_required",
    "deception.fraud.element.deception-must-create-false-belief",
    "deception.fraud.causal-link.deception-property-disposition",
    "deception.fraud.causal-link.no-disposition-no-deception",
    "deception.fraud.element.deception-not-legal-act-important-part",
    "deception.fraud.element.victim-negligence-no-bar",
    "deception.fraud.definition.deception-means-unrestricted",
    "deception.fraud.element.omission-deception-legal-notice-duty",
    "deception.fraud.element.omission-deception-independent-error",
    "deception.fraud.definition.notice-duty-violation-omission",
    "deception.fraud.definition.other-includes-corporation",
    "deception.fraud.definition.deception-counterparty-is-other",
    "deception.fraud.definition.deceived-person-unspecified",
    "deception.fraud.definition.deceived-person-victim-distinct",
    "fraud_mistake.invalid_act_disposition",
    "fraud_mistake.sequential_causation",
    "fraud_mistake.property_disposition_element",
    "fraud_mistake.factual_act_disposition",
    "fraud_mistake.property_limited_disposition",
    "fraud_mistake.triangular_fraud_definition",
    "fraud_mistake.deceived_disposer_identity",
    "fraud_damage_acquisition.property_concept_reported_precedent",
    "fraud_damage_acquisition.property_loss_negative_view",
    "fraud_intent.no_disposition_inducement_intent",
    "fraud_stages_participation.attempt_deceptive_act",
    "fraud_stages_participation.litigation_service_not_required",
    "fraud_stages_participation.completion_deception_disposition_transfer",
    "fraud_stages_participation.no_causation_attempt",
    "fraud_stages_participation.property_fraud_completion_control",
}


CORE_STANDARD_IDS = {
    "general_object.fraud.element.object-other-possessed-other-property",
    "general_object.fraud.definition.property-benefit",
    "general_object.fraud.element.property-benefit-concrete",
    "general_object.fraud.definition.property-benefit-not-numerically-limited",
    "deception.fraud.definition.deception-good-faith-mistake",
    "deception.fraud.definition.exploitation-existing-mistake",
    "deception.fraud.definition.deception-content-basis-fact",
    "deception.fraud.definition.deception-object-facts",
    "deception.fraud.definition.implicit-deception",
    "deception.fraud.definition.deception-target-human",
    "general_object.fraud.standard.later-cancellation-no-effect",
    "general_object.fraud.standard.own-property-not-object",
    "fraud_general_object.deception_error_causation",
    "general_object.fraud.standard.public-interest-only-no-fraud",
    "general_object.fraud.exception.public-interest-property-equivalence",
    "general_object.fraud.standard.own-possession-other-property-embezzlement",
    "deception.fraud.standard.loan-purpose-materiality",
    "deception.fraud.causal-link.loan-purpose-not-sole-trigger",
    "deception.fraud.standard.deception-concrete-circumstances",
    "deception.fraud.standard.easily-detectable-lie",
    "deception.fraud.element.transaction-purpose-no-impairment",
    "deception.fraud.standard.advertising-tolerable-exaggeration",
    "deception.fraud.standard.advertising-important-concrete-falsehood",
    "deception.fraud.standard.abstract-or-immaterial-advertising",
    "deception.fraud.standard.vague-opinion-not-deception",
    "deception.fraud.standard.implicit-deception-explanatory-value",
    "deception.fraud.element.omission-deception-guarantor-equivalence",
    "deception.fraud.standard.precedent-notice-duty-materiality",
    "deception.fraud.exception.no-notice-duty-no-effect-on-rights",
    "deception.fraud.standard.implicit-omission-deception-distinction",
    "deception.fraud.element.loan-no-repayment-intent-or-ability",
    "deception.fraud.standard.intent-to-defraud-loan-inference",
    "deception.fraud.standard.financial-loan-omission-caution",
    "deception.fraud.standard.loan-subsequent-default",
    "deception.fraud.standard.loan-lender-anticipated-risk",
    "fraud_mistake.error_doubt_ignorance",
    "fraud_mistake.error_definition",
    "fraud_mistake.error_disposition_motivation",
    "fraud_mistake.no_thought_no_error",
    "fraud_mistake.unaware_error",
    "fraud_mistake.disposition_definition",
    "fraud_mistake.disposition_omission",
    "fraud_mistake.disposition_intent_act_awareness",
    "fraud_mistake.disposition_directness",
    "fraud_mistake.trick_theft_directness",
    "fraud_mistake.no_capacity_theft",
    "fraud_mistake.gain_purpose",
    "fraud_mistake.active_creditor_extension",
    "fraud_mistake.conscious_nonexercise",
    "fraud_mistake.assignment_debt_extinguishment",
    "mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation",
    "fraud_mistake.omission_not_all_nonclaims",
    "fraud_damage_acquisition.money_delivery_full_amount",
    "fraud_damage_acquisition.delivery_of_property",
    "fraud_damage_acquisition.delivery_factual_control",
    "fraud_damage_acquisition.property_disposition_types",
    "fraud_damage_acquisition.protected_economic_interest",
    "fraud_damage_acquisition.subsequent_return_irrelevant",
    "fraud_damage_acquisition.right_exercise_unacceptable_deception",
    "fraud_intent.contract_breach_distinction",
    "fraud_intent.time_of_conduct",
    "fraud_intent.objective_circumstances",
    "fraud_intent.precedent_illegal_appropriation_intent",
    "fraud_intent.illegal_appropriation_definition",
    "fraud_intent.illegal_gain_unauthorized",
    "fraud_intent.third_party_acquisition",
    "special_forms.fraud.standard.litigation-fraud-strict-interpretation",
    "special_forms.fraud.standard.litigation-fraud-objectively-false-or-knowing",
    "special_forms.fraud.element.litigation-fraud-knowing-nonexistence",
    "special_forms.fraud.exception.litigation-fraud-mistake-of-fact-or-law",
    "special_forms.fraud.standard.indirect-perpetration-through-unaware-third-party",
    "special_forms.fraud.element.litigation-fraud-deceptive-act",
    "special_forms.fraud.exception.omission-of-favorable-evidence",
    "special_forms.fraud.standard.false-claim-alone-can-deceive",
    "special_forms.fraud.element.judgment-substitutes-victim-disposition",
    "special_forms.fraud.element.litigation-fraud-commencement",
    "special_forms.fraud.standard.insurance-concealed-existing-accident",
    "special_forms.fraud.standard.insurance-intentional-accident-claim",
    "special_forms.fraud.standard.insurance-false-accident-claim",
    "special_forms.fraud.standard.insurance-omission-destroys-contingency",
    "special_forms.fraud.standard.insurance-injury-disease-contingency-factors",
    "special_forms.fraud.standard.insurance-defective-life-contract-preparatory-act",
    "special_forms.fraud.standard.right-exercise-socially-acceptable-no-crime",
    "fraud_stages_participation.insurance_false_claim_attempt",
    "fraud_stages_participation.gambling_fraud_attempt",
    "fraud_stages_participation.false_claim_provisional_seizure_no_attempt",
    "fraud_stages_participation.enforcement_application_attempt",
    "fraud_stages_participation.payment_order_attempt",
    "fraud_stages_participation.post_filing_false_claim_attempt",
}


FUTURE_WORK_GENERAL_PART_IDS = {
    "fraud_intent.conditional_intent",
    "fraud_stages_participation.inclusive_offense_withdrawal_liability",
    "fraud_stages_participation.gambling_normal_gambling_included",
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


def verify_local_primary_records() -> dict[str, Any]:
    if not LOCAL_PRIMARY_SOURCE.exists():
        return {
            "status": "not_available",
            "verified_records": 0,
        }

    import pandas as pd

    frame = pd.read_parquet(
        LOCAL_PRIMARY_SOURCE,
        columns=["판례정보일련번호", "사건번호", "선고일자", "법원명"],
    ).set_index("판례정보일련번호")
    errors: list[str] = []
    for case_no, expected in VERIFIED_LOCAL_PRIMARY_RECORDS.items():
        record_id = expected["record_id"]
        if record_id not in frame.index:
            errors.append(f"missing record_id={record_id} case_no={case_no}")
            continue
        row = frame.loc[record_id]
        actual = {
            "case_no": str(row["사건번호"]),
            "decision_date": str(int(row["선고일자"])),
            "court": str(row["법원명"]),
        }
        expected_date = expected["decision_date"].replace("-", "")
        if (
            actual["case_no"] != case_no
            or actual["decision_date"] != expected_date
            or actual["court"] != expected["court"]
        ):
            errors.append(
                f"record_id={record_id} expected={case_no}/{expected_date}/"
                f"{expected['court']} actual={actual}"
            )
    if errors:
        raise ValueError("Local primary precedent mismatch: " + "; ".join(errors))
    return {
        "status": "verified",
        "verified_records": len(VERIFIED_LOCAL_PRIMARY_RECORDS),
    }


def append_note(card: dict[str, Any], note: str) -> None:
    if note not in card["review_notes"]:
        card["review_notes"] = card["review_notes"].rstrip() + " " + note


def preserve_policy_decisions(
    policy_items: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    existing_rows = read_jsonl(POLICY_DECISIONS) if POLICY_DECISIONS.exists() else []
    existing: dict[str, dict[str, Any]] = {}
    for row in existing_rows:
        review_id = row["review_id"]
        if review_id in existing:
            raise ValueError(f"Duplicate policy decision: {review_id}")
        existing[review_id] = row

    current_ids = {item["review_id"] for item in policy_items}
    orphan_ids = set(existing) - current_ids
    nonempty_orphans = {
        review_id
        for review_id in orphan_ids
        if existing[review_id].get("status") != "pending"
        or existing[review_id].get("decision") is not None
        or existing[review_id].get("selected_card_ids")
        or existing[review_id].get("verified_authority_refs")
        or existing[review_id].get("notes")
    }
    if nonempty_orphans:
        raise ValueError(
            f"User-entered orphan policy decisions: {sorted(nonempty_orphans)}"
        )

    decisions: list[dict[str, Any]] = []
    for item in policy_items:
        review_id = item["review_id"]
        row = existing.get(
            review_id,
            {
                "review_id": review_id,
                "status": "pending",
                "decision": None,
                "selected_card_ids": [],
                "verified_authority_refs": [],
                "notes": "",
            },
        )
        selected = set(row.get("selected_card_ids", []))
        allowed = set(item["selectable_card_ids"])
        if not selected <= allowed:
            raise ValueError(
                f"Invalid selected cards for {review_id}: {sorted(selected - allowed)}"
            )
        decisions.append(row)
    return decisions


def preserve_core_review_decisions(
    review_items: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    existing_rows = (
        read_jsonl(CORE_REVIEW_DECISIONS) if CORE_REVIEW_DECISIONS.exists() else []
    )
    existing: dict[str, dict[str, Any]] = {}
    for row in existing_rows:
        review_id = row["review_id"]
        if review_id in existing:
            raise ValueError(f"Duplicate core review decision: {review_id}")
        existing[review_id] = row

    current_ids = {item["review_id"] for item in review_items}
    orphan_ids = set(existing) - current_ids
    nonempty_orphans = {
        review_id
        for review_id in orphan_ids
        if existing[review_id].get("status") != "pending"
        or existing[review_id].get("decision") is not None
        or existing[review_id].get("verified_authority_refs")
        or existing[review_id].get("notes")
    }
    if nonempty_orphans:
        raise ValueError(
            f"User-entered orphan core decisions: {sorted(nonempty_orphans)}"
        )

    decisions: list[dict[str, Any]] = []
    allowed_decisions = {"approve", "narrow", "reclassify_to_rag", "reject"}
    for item in review_items:
        review_id = item["review_id"]
        row = existing.get(
            review_id,
            {
                "review_id": review_id,
                "status": "pending",
                "decision": None,
                "verified_authority_refs": [],
                "notes": "",
            },
        )
        status = row.get("status")
        decision = row.get("decision")
        if status not in {"pending", "completed"}:
            raise ValueError(f"Invalid core review status for {review_id}: {status}")
        if status == "completed" and decision not in allowed_decisions:
            raise ValueError(
                f"Invalid completed core decision for {review_id}: {decision}"
            )
        if status == "pending" and decision is not None:
            raise ValueError(
                f"Pending core review must not have a decision: {review_id}"
            )
        decisions.append(row)
    return decisions


def main() -> None:
    remediation = read_json(REMEDIATION_LEDGER)
    if remediation.get("api_calls") != 0:
        raise ValueError("NormCard remediation must not use API calls")
    if remediation.get("accepted_findings") != 57 or remediation.get(
        "handled_findings"
    ) != 57:
        raise ValueError("All 57 accepted findings must be remediated first")

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
    if len(cards_by_id) not in {636, 646}:
        raise ValueError(f"Expected 636 or 646 unique cards, found {len(cards_by_id)}")

    def split_variant_card(
        *,
        module: str,
        base_card_id: str,
        card_id: str,
        candidate_index: int,
        source_index: int,
        proposition: str,
        variant_group: str,
    ) -> None:
        if card_id in cards_by_id:
            return
        base = cards_by_id[base_card_id]
        card = {
            "id": card_id,
            "candidate_refs": [base["candidate_refs"][candidate_index]],
            "norm_kind": "variant",
            "proposition": proposition,
            "formalization": "policy_variant",
            "authority_basis": "commentary_reported_doctrine",
            "doctrinal_status": "disputed",
            "polarity": "positive",
            "source_refs": [base["source_refs"][source_index]],
            "request_ids": base["request_ids"],
            "variant_group": variant_group,
            "review_required": True,
            "review_notes": (
                "수동 최종 감사에서 합쳐진 경쟁 견해를 독립 policy card로 분리했다."
            ),
        }
        card_sets[module]["cards"].append(card)
        cards_by_id[card_id] = card
        card_module[card_id] = module

    split_specs = [
        (
            "general_object",
            "fraud_general_object.property_scope_variant",
            "fraud_general_object.property_scope_whole_property",
            0,
            0,
            "전체로서의 재산설은 사기죄의 보호대상인 재산을 전체로서의 재산으로 파악한다.",
            "fraud_general_object.property_scope",
        ),
        (
            "general_object",
            "fraud_general_object.property_scope_variant",
            "fraud_general_object.property_scope_individual_property",
            1,
            0,
            "개별적 재산설은 사기죄의 보호대상인 재산을 개개의 재산으로 파악한다.",
            "fraud_general_object.property_scope",
        ),
        (
            "general_object",
            "fraud_general_object.property_value_variant",
            "fraud_general_object.property_value_exchange_required",
            0,
            0,
            "사기죄의 객체인 재물은 교환가치가 있는 재물에 한정된다는 견해가 있다.",
            "fraud_general_object.property_value",
        ),
        (
            "general_object",
            "fraud_general_object.property_value_variant",
            "fraud_general_object.property_value_subjective_sufficient",
            1,
            0,
            "행위자에게 주관적 가치만 있는 물건도 사기죄의 객체인 재물이 될 수 있다는 견해가 있다.",
            "fraud_general_object.property_value",
        ),
        (
            "general_object",
            "fraud_general_object.protected_interest_truth_variant",
            "fraud_general_object.protected_interest_property_only",
            1,
            0,
            "다수설은 사기죄의 보호법익을 재산만으로 본다.",
            "fraud_general_object.protected_interest",
        ),
        (
            "general_object",
            "fraud_general_object.protected_interest_truth_variant",
            "fraud_general_object.protected_interest_truth_duty_included",
            0,
            0,
            "소수설은 거래의 진실성 또는 신의의무도 사기죄의 보호법익에 포함된다고 본다.",
            "fraud_general_object.protected_interest",
        ),
        (
            "mistake_disposition",
            "fraud_mistake.triangular_fraud_theories",
            "fraud_mistake.triangular_fraud_causation_theory",
            0,
            0,
            "인과관계설은 삼각사기에서 피기망자의 처분과 행위자의 이득 사이에 인과관계가 있으면 충분하다고 본다.",
            "fraud_mistake.triangular_fraud_authority",
        ),
        (
            "mistake_disposition",
            "fraud_mistake.triangular_fraud_theories",
            "fraud_mistake.triangular_fraud_contractual_authority",
            1,
            1,
            "계약관계설은 처분행위자가 계약관계에 따라 피해자의 재산을 처분할 권한을 가져야 한다고 본다.",
            "fraud_mistake.triangular_fraud_authority",
        ),
        (
            "mistake_disposition",
            "fraud_mistake.triangular_fraud_theories",
            "fraud_mistake.triangular_fraud_legal_authority",
            2,
            2,
            "법적 권한설은 처분행위자에게 법률·계약 또는 최소한 묵시적 위임에 따른 피해자 재산 처분권한이 있어야 한다고 본다.",
            "fraud_mistake.triangular_fraud_authority",
        ),
        (
            "mistake_disposition",
            "fraud_mistake.triangular_fraud_theories",
            "fraud_mistake.triangular_fraud_factual_position",
            3,
            3,
            "사실상 지위설은 처분행위자가 타인의 재산을 사실상 처분할 수 있는 지위에 있으면 충분하다고 본다.",
            "fraud_mistake.triangular_fraud_authority",
        ),
    ]
    for spec in split_specs:
        split_variant_card(
            module=spec[0],
            base_card_id=spec[1],
            card_id=spec[2],
            candidate_index=spec[3],
            source_index=spec[4],
            proposition=spec[5],
            variant_group=spec[6],
        )

    # These are source-bounded case outcomes or current-law statements, not reusable
    # neural standards or deterministic rules.
    context_only = {
        "fraud_damage_acquisition.provisional_seizure_release_disposition": (
            "가압류 해제 판례의 사안별 결과이므로 RAG 사례로 보존한다."
        ),
        "special_forms.fraud.exception.insurance-special-act-temporal-application": (
            "보험사기방지 특별법의 현행 시간적 적용범위를 직접 확인하기 전 RAG 자료로 보존한다."
        ),
        "fraud_damage_acquisition.legitimate_right_deduction_view": (
            "단일 학설 설명으로서 판례 우선 정책을 정할 근거가 없어 RAG 자료로 보존한다."
        ),
        "deception.fraud.standard.explicit-denial-encumbrance": (
            "단일 학설 설명으로서 채택하지 않고 RAG 자료로 보존한다."
        ),
        "fraud_general_object.property_concept_variant": (
            "여러 재산개념을 한 카드에 합친 개괄 설명이므로 선택 가능한 정책 카드로 쓰지 않는다."
        ),
        "fraud_general_object.property_scope_variant": (
            "전체재산설과 개별재산설이 분리되지 않은 개괄 카드이므로 RAG 자료로 보존한다."
        ),
        "fraud_general_object.property_value_variant": (
            "교환가치설과 주관적 가치설이 분리되지 않은 개괄 카드이므로 RAG 자료로 보존한다."
        ),
        "fraud_general_object.protected_interest_truth_variant": (
            "보호법익 대립을 한 카드에 합친 개괄 설명이므로 RAG 자료로 보존한다."
        ),
        "fraud_general_object.protected_interest_possession": (
            "보호법익에 소지를 포함한다는 단일 학설 설명이므로 RAG 자료로 보존한다."
        ),
        "fraud_general_object.victim_responsibility_variant": (
            "피해자 책임을 이유로 기망을 제한하는 단일 학설 설명이며 판례 우선 근거가 없어 RAG 자료로 보존한다."
        ),
        "general_object.fraud.variant.road-occupancy-permit-no-property-benefit": (
            "도로점용허가 판례에 대한 주석자의 유보적 분석이므로 정책으로 선택하지 않는다."
        ),
        "fraud_general_object.subjective_elements": (
            "불법영득의사 필요 여부의 개괄 카드이며 세부 정책 카드와 중복되어 RAG 설명으로 보존한다."
        ),
    }
    for card_id, note in context_only.items():
        card = cards_by_id[card_id]
        card["formalization"] = "context_only"
        card["review_required"] = True
        append_note(card, note)

    non_selectable_policy_cards = {
        "fraud_damage_acquisition.property_concept_reported_precedent",
        "damage_acquisition.fraud.variant-property-loss-requirement-negative",
        "damage_acquisition.fraud.variant-property-loss-requirement-affirmative",
        "damage_acquisition.fraud.variant-property-loss-requirement-limited-affirmative",
        "fraud_damage_acquisition.property_risk_infringement_offense",
        "deception.fraud.variant.opinion-statement-third-view-concreteness",
        "fraud_mistake.triangular_fraud_theories",
        "mistake_disposition.fraud.variant-triangular-fraud-precedent-legal-authority-interpretation",
        "mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation",
        "mistake_disposition.fraud.variant-triangular-fraud-precedent-transition-not-conclusive",
        "mistake_disposition.fraud.variant-triangular-fraud-commentator-factual-position-evaluation",
    }
    for card_id in non_selectable_policy_cards:
        card = cards_by_id[card_id]
        card["formalization"] = "context_only"
        card["review_required"] = True
        append_note(card, "정책 선택지가 아니라 판례 설명·중복 요약·보충 논거로 분류했다.")

    # A stated general rule plus its bounded exception is composable and does not need
    # an active-policy switch merely because the source says "in principle".
    junior_mortgage = cards_by_id[
        "fraud_damage_acquisition.mortgage_setting_junior_gain_cap"
    ]
    junior_mortgage["formalization"] = "deterministic_rule"
    junior_mortgage["doctrinal_status"] = "descriptive"
    junior_mortgage["review_required"] = False
    append_note(
        junior_mortgage,
        "후순위 근저당권 이득액 원칙으로 사용하고 동일 그룹의 예외 카드를 함께 적용한다.",
    )

    # These standards are genuinely competing positions and therefore require a policy
    # choice rather than an ordinary neural judgment.
    promote_to_policy = {
        "fraud_concurrence.counterfeit_currency_real_concurrence": (
            "fraud_concurrence.counterfeit_currency_fraud"
        ),
        "fraud_stages_participation.victim_loss_completion_view": (
            "fraud_stages_participation.completion_threshold"
        ),
    }
    for card_id, group_id in promote_to_policy.items():
        card = cards_by_id[card_id]
        card["formalization"] = "policy_variant"
        card["variant_group"] = group_id
        card["review_required"] = True
        append_note(card, "경쟁 견해와 함께 active policy 선택이 필요한 카드로 정정했다.")

    # Previously singleton notice-duty cards describe one shared broad-vs-limited issue.
    notice_duty_cards = {
        "deception.fraud.variant.guarantee-status-bases",
        "deception.fraud.variant.notice-duty-good-faith-transaction",
        "deception.fraud.variant.notice-duty-special-trust-factors",
        "deception.fraud.variant.prior-conduct-notice-duty",
        "deception.fraud.variant.real-estate-notice-duty-explicit-duty",
    }
    for card_id in notice_duty_cards:
        card = cards_by_id[card_id]
        card["variant_group"] = "fraud_deception.omission_notice_duty_scope"
        append_note(card, "부작위 기망의 고지의무 범위에 관한 공통 정책 그룹으로 통합했다.")

    excess_change_group = "fraud_deception.excess_change_notice_duty"
    excess_change_cards = {
        "deception.fraud.variant.excess-change-no-duty-to-check",
        "deception.fraud.standard.excess-change-given-at-scene",
        "deception.fraud.standard.excess-change-later-discovery",
        "deception.fraud.standard.excess-change-denial-after-demand",
    }
    for card_id in excess_change_cards:
        cards_by_id[card_id]["variant_group"] = excess_change_group
        append_note(cards_by_id[card_id], "과다 거스름돈 인식 시점과 고지의무 정책 그룹에 연결했다.")

    excess_change = cards_by_id[
        "deception.fraud.variant.excess-change-no-duty-to-check"
    ]
    excess_change["formalization"] = "deterministic_rule"
    excess_change["doctrinal_status"] = "descriptive"
    excess_change["review_required"] = False
    append_note(
        excess_change,
        "판례의 실제 인식 시점 구별과 함께 적용할 일반 확인·고지의무 규칙으로 분류했다.",
    )

    evidence_groups = {
        "fraud_general_object.partial_consideration": (
            "fraud_general_object.property_scope"
        ),
        "fraud_general_object.protected_interest_commentary_position": (
            "fraud_general_object.protected_interest"
        ),
        "fraud_general_object.triangular_fraud_victim": (
            "fraud_general_object.protected_interest"
        ),
    }
    for card_id, group_id in evidence_groups.items():
        cards_by_id[card_id]["variant_group"] = group_id
        append_note(cards_by_id[card_id], "판례 우선 정책 선택을 위한 관련 근거 카드로 연결했다.")

    def adopt_practical_rule(
        card_id: str,
        *,
        formalization: str = "deterministic_rule",
        note: str,
    ) -> None:
        card = cards_by_id[card_id]
        card["formalization"] = formalization
        card["authority_basis"] = "commentary_synthesis"
        card["doctrinal_status"] = "descriptive"
        card["review_required"] = False
        append_note(card, note)

    def demote_policy_cards(card_ids: set[str], note: str) -> None:
        for card_id in card_ids:
            card = cards_by_id[card_id]
            card["formalization"] = "context_only"
            card["review_required"] = True
            append_note(card, note)

    adopt_practical_rule(
        "fraud_concurrence.agent_imaginary_concurrence_view",
        note="관련 판례 카드가 양 구성요건을 충족한 한 행위의 상상적 경합을 보고하여 실무 규칙으로 채택했다.",
    )
    demote_policy_cards(
        {
            "fraud_concurrence.agent_fraud_only_view",
            "fraud_concurrence.agent_breach_only_view",
        },
        "관련 판례와 다른 학설 선택지이므로 RAG 비교자료로 보존한다.",
    )

    adopt_practical_rule(
        "fraud_concurrence.counterfeit_currency_real_concurrence",
        formalization="standard_input",
        note="주석서가 보호법익 차이에 따른 실체적 경합을 규범으로 제시하므로 실무 규칙으로 채택했다.",
    )
    demote_policy_cards(
        {"fraud_concurrence.counterfeit_currency_imaginary_view"},
        "주석서 규범과 다른 학설이므로 RAG 비교자료로 보존한다.",
    )

    adopt_practical_rule(
        "fraud_general_object.property_scope_individual_property",
        note="재물교부 자체의 재산침해를 인정하는 판례 카드와 부합하여 실무 규칙으로 채택했다.",
    )
    demote_policy_cards(
        {"fraud_general_object.property_scope_whole_property"},
        "전체재산 손해를 요구하지 않는 판례 입장과 달라 RAG 비교자료로 보존한다.",
    )

    adopt_practical_rule(
        "fraud_general_object.protected_interest_property_only",
        note="재산권만을 보호법익으로 보는 주석 결론과 대법원 피해자 판단에 맞추어 실무 규칙으로 채택했다.",
    )
    demote_policy_cards(
        {"fraud_general_object.protected_interest_truth_duty_included"},
        "판례·주석 결론과 다른 소수설이므로 RAG 비교자료로 보존한다.",
    )

    adopt_practical_rule(
        "special_forms.fraud.variant.illegal-cause-benefit-affirmative",
        note="불법원인급여에서도 사기죄를 긍정하는 판례 카드에 따라 실무 규칙으로 채택했다.",
    )
    demote_policy_cards(
        {"special_forms.fraud.variant.illegal-cause-benefit-negative"},
        "판례와 다른 소수설이므로 RAG 비교자료로 보존한다.",
    )

    adopt_practical_rule(
        "special_forms.fraud.variant.right-exercise-abuse-positive",
        note="사회통념상 허용 범위를 넘은 기망수단의 위법성을 인정하는 판례 카드에 따라 채택했다.",
    )
    demote_policy_cards(
        {
            "special_forms.fraud.variant.right-exercise-within-scope-negative",
            "special_forms.fraud.variant.right-exercise-social-acceptability",
        },
        "권리 범위만으로 일률 결정하지 않고 사회통념상 수단의 허용성을 보는 판례 기준에 통합했다.",
    )

    demote_policy_cards(
        {
            "deception.fraud.variant.dine-stay-implicit-deception-majority",
            "deception.fraud.variant.dine-stay-omission-deception",
            "deception.fraud.variant.disposition-implied-representation",
            "deception.fraud.variant.disposition-omission-deception",
        },
        "사기 성립 결론이 아니라 기망행위 분류 방식의 차이이므로 RAG 해설로 보존한다.",
    )

    for card_id in {
        "mistake_disposition.fraud.variant.disposition-voluntariness-coercive-seizure-negative",
        "mistake_disposition.fraud.variant.disposition-voluntariness-coercive-seizure-positive",
    }:
        adopt_practical_rule(
            card_id,
            formalization="standard_input",
            note="서로 배척하는 학설이 아니라 상이한 사실조건의 자의성 판단 기준으로 정리했다.",
        )

    # The remaining 12 groups were incorrectly presented as unresolved global policy
    # switches. Direct holdings in the commentary and the local primary-precedent index
    # resolve the practical rules. Pure academic disputes and rare edge cases stay in RAG.
    policy_resolutions = [
        {
            "policy_group": "fraud_damage_acquisition.property_concept",
            "resolution": "activate_narrow_precedent_rule",
            "activated_card_ids": [
                "fraud_damage_acquisition.property_concept_reported_precedent"
            ],
            "authority_refs": ["75도760", "2001도2991"],
            "reason": (
                "법률상 유효 취득이나 사법상 보호되는 이익에 한정하지 않는다는 "
                "판시를 좁은 실행 규칙으로 사용하고 추상적 재산개념 학설은 RAG로 보존한다."
            ),
        },
        {
            "policy_group": "fraud_damage_acquisition.property_loss_requirement",
            "resolution": "adopt_precedent_no_actual_loss_requirement",
            "activated_card_ids": [
                "fraud_damage_acquisition.property_loss_negative_view"
            ],
            "authority_refs": ["2003도4914", "2017도21196"],
            "reason": "현실적 재산상 손해는 별도 구성요건이 아니라는 판례를 채택한다.",
        },
        {
            "policy_group": "fraud_damage_acquisition.property_risk_as_loss",
            "resolution": "rag_only_not_independent_liability_gate",
            "activated_card_ids": [],
            "authority_refs": ["95도2466", "2003도4914"],
            "reason": (
                "현실적 손해가 독립 구성요건이 아니므로 재산위험 학설을 전역 성립 게이트로 "
                "선택하지 않고 신용카드·보증 등 구체적 이익 취득 규칙에서 처리한다."
            ),
        },
        {
            "policy_group": "fraud_deception.future_fact_scope",
            "resolution": "rag_only_use_present_intent_and_ability_rules",
            "activated_card_ids": [],
            "authority_refs": [],
            "reason": (
                "순수 장래사실의 포괄 범위는 주석서도 학설 대립으로만 제시한다. 현재의 "
                "의사·능력 등 심리적 사실에 관한 기존 기망 규칙만 core에서 사용한다."
            ),
        },
        {
            "policy_group": "fraud_deception.omission_notice_duty_scope",
            "resolution": "activate_precedent_materiality_standard",
            "activated_card_ids": [
                "deception.fraud.standard.precedent-notice-duty-materiality"
            ],
            "authority_refs": ["84도882", "2018도13696"],
            "reason": (
                "법령·계약·관습·조리와 구체적 거래실정·신의칙 및 거래 중요성을 보는 "
                "판례 기준을 사용하고 학설상 제한 방식은 RAG로 보존한다."
            ),
        },
        {
            "policy_group": "fraud_deception.opinion_statement",
            "resolution": "rag_only_keep_vague_opinion_standard",
            "activated_card_ids": [],
            "authority_refs": ["2018도13696"],
            "reason": (
                "주석서가 정면 판례 부재를 명시하므로 학설 하나를 전역 선택하지 않는다. "
                "막연한 의견의 착오유발 충분성과 구체적 거래 중요성은 기존 standard에서 판단한다."
            ),
        },
        {
            "policy_group": "fraud_general_object.property_value",
            "resolution": "rag_only_no_fraud_precedent_transplant",
            "activated_card_ids": [],
            "authority_refs": ["2007도2595"],
            "reason": (
                "주관적 가치 판시는 절도죄 판례이므로 사기죄의 전역 재물 기준으로 승격하지 "
                "않고 희귀 쟁점 검색 문맥으로 보존한다."
            ),
        },
        {
            "policy_group": "fraud_general_object.sex_work_contract",
            "resolution": "resolve_with_precedent_keep_case_specific_rag",
            "activated_card_ids": [],
            "authority_refs": ["2001도2991"],
            "reason": (
                "성행위 대가 지급을 면한 구체적 판례는 긍정하지만 희귀 적용례이므로 "
                "전역 core rule이 아니라 판례 RAG로 보존한다."
            ),
        },
        {
            "policy_group": "fraud_intent.illegal_appropriation_requirement",
            "resolution": "activate_single_centralized_precedent_standard",
            "activated_card_ids": [
                "fraud_intent.precedent_illegal_appropriation_intent"
            ],
            "authority_refs": ["66도132", "2021도8468"],
            "reason": (
                "판례의 불법영득의사 내지 편취 범의 기준을 intent 모듈에서 한 번만 적용하고 "
                "사기 유형마다 중복 게이트를 만들지 않는다."
            ),
        },
        {
            "policy_group": "fraud_mistake.disposition_intent_requirement",
            "resolution": "use_existing_en_banc_standard",
            "activated_card_ids": [
                "fraud_mistake.disposition_intent_act_awareness"
            ],
            "authority_refs": ["2016도13362"],
            "reason": (
                "처분행위 자체에 대한 인식은 필요하지만 처분결과 인식은 필요 없다는 "
                "전원합의체 기준이 이미 standard input으로 존재한다."
            ),
        },
        {
            "policy_group": "fraud_mistake.triangular_fraud_authority",
            "resolution": "activate_precedent_authority_or_position_standard",
            "activated_card_ids": [
                "mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation"
            ],
            "authority_refs": ["94도1575", "2022도12494"],
            "reason": (
                "피기망자에게 피해자 재산을 처분할 권능 또는 지위가 필요하되 사법상 "
                "위임·대리권과 일치할 필요는 없다는 판례의 조작적 기준을 사용한다."
            ),
        },
        {
            "policy_group": "fraud_stages_participation.completion_threshold",
            "resolution": "use_existing_transfer_or_acquisition_rule",
            "activated_card_ids": [
                "fraud_stages_participation.completion_deception_disposition_transfer"
            ],
            "authority_refs": ["80도2667", "2001도1825"],
            "reason": (
                "재물 교부 또는 재산상 이익 취득이 있어야 기수라는 기존 deterministic rule을 "
                "유지하고 피해자 손해만으로 기수라는 학설은 RAG로 보존한다."
            ),
        },
    ]

    academic_policy_cards = {
        card["id"]
        for card in cards_by_id.values()
        if card["formalization"] == "policy_variant"
    }
    practical_loss_rule = "fraud_damage_acquisition.property_loss_negative_view"
    academic_policy_cards.discard(practical_loss_rule)
    demote_policy_cards(
        academic_policy_cards,
        "판례 우선 core 규칙과 구체적 RAG의 구분에 따라 전역 active policy 대상에서 제외했다.",
    )

    property_concept_rule = cards_by_id[
        "fraud_damage_acquisition.property_concept_reported_precedent"
    ]
    property_concept_rule.update(
        {
            "proposition": (
                "사기죄의 재산상 이익 취득은 법률상 유효할 필요가 없고, 법률상 무효라도 "
                "외형상 재산상 이익을 취득하면 족하다."
            ),
            "formalization": "deterministic_rule",
            "authority_basis": "commentary_reported_precedent",
            "doctrinal_status": "precedent_position",
            "review_required": False,
        }
    )
    append_note(property_concept_rule, "75도760 및 2001도2991의 좁은 판시 범위로 활성화했다.")

    loss_rule = cards_by_id[practical_loss_rule]
    loss_rule.update(
        {
            "proposition": (
                "사기죄는 기망에 의한 재물 교부 또는 재산상 이익 취득으로 성립하며, "
                "상대방에게 현실적인 재산상 손해가 별도로 발생할 것을 요구하지 않는다."
            ),
            "formalization": "deterministic_rule",
            "authority_basis": "commentary_reported_precedent",
            "doctrinal_status": "precedent_position",
            "review_required": False,
        }
    )
    append_note(loss_rule, "2003도4914 및 2017도21196의 판례 기준으로 활성화했다.")

    loss_assessment = cards_by_id[
        "fraud_damage_acquisition.property_loss_assessment"
    ]
    loss_assessment["formalization"] = "context_only"
    loss_assessment["review_required"] = True
    append_note(loss_assessment, "손해가 독립 성립요건이 아니므로 학설상 손해평가 문맥으로만 보존한다.")

    notice_rule = cards_by_id[
        "deception.fraud.standard.precedent-notice-duty-materiality"
    ]
    notice_rule["formalization"] = "standard_input"
    notice_rule["review_required"] = False
    append_note(notice_rule, "84도882 및 2018도13696의 판례 기준으로 활성화했다.")

    intent_rule = cards_by_id[
        "fraud_intent.precedent_illegal_appropriation_intent"
    ]
    intent_rule["formalization"] = "standard_input"
    intent_rule["review_required"] = False
    append_note(intent_rule, "유형별 중복 없이 intent 모듈의 중앙 판례 기준으로 한 번만 적용한다.")

    triangular_rule = cards_by_id[
        "mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation"
    ]
    triangular_rule.update(
        {
            "proposition": (
                "피기망자와 재산상 피해자가 다르면 피기망자에게 피해자를 위하여 그 재산을 "
                "처분할 권능 또는 지위가 있어야 한다. 그 권능 또는 지위는 사법상 위임이나 "
                "대리권과 일치할 필요는 없고, 피해자의 의사에 따라 처분서류를 교부받은 "
                "경우에도 인정될 수 있다."
            ),
            "formalization": "standard_input",
            "authority_basis": "commentary_reported_precedent",
            "doctrinal_status": "precedent_position",
            "review_required": False,
        }
    )
    append_note(triangular_rule, "94도1575와 2022도12494의 권능 또는 지위 기준으로 활성화했다.")

    sex_work_case = cards_by_id[
        "general_object.fraud.variant.sex-work-contract-fraud-affirmative"
    ]
    sex_work_case.update(
        {
            "proposition": (
                "금품 지급을 전제로 한 성행위 약정이 민법상 무효이더라도, 대가 지급 의사 "
                "없이 상대방을 기망하여 성행위 대가 지급을 면하면 사기죄가 성립한다."
            ),
            "authority_basis": "commentary_reported_precedent",
            "doctrinal_status": "precedent_position",
        }
    )
    append_note(sex_work_case, "2001도2991의 구체적 판시 범위로 좁혀 RAG에 보존했다.")

    objective_elements = cards_by_id["fraud_general_object.objective_elements"]
    objective_elements["proposition"] = (
        "사기죄의 객관적 구성요건은 기망행위, 피기망자의 착오, 재산적 처분행위, "
        "재산상 손해, 재물 또는 재산상 이익의 취득 및 이들 사이의 인과관계이다."
    )
    append_note(
        objective_elements,
        "서론의 요약은 손해를 열거하지만 2003도4914 및 2017도21196의 판례 카드와 "
        "충돌하므로 실행 규칙이 아니라 출처 충돌을 보여 주는 RAG 문맥으로 보존했다.",
    )

    deceived_disposer = cards_by_id["fraud_mistake.deceiver_disposer_text"]
    deceived_disposer["proposition"] = (
        "피기망자, 즉 기망행위의 상대방과 재산적 처분행위자는 동일인이어야 한다."
    )
    append_note(deceived_disposer, "기망자를 피기망자로 잘못 옮긴 번역 오류를 정정했다.")

    all_core_ids = CORE_DETERMINISTIC_IDS | CORE_STANDARD_IDS
    if CORE_DETERMINISTIC_IDS & CORE_STANDARD_IDS:
        raise ValueError("Core deterministic and standard IDs must be disjoint")
    unknown_core_ids = all_core_ids - set(cards_by_id)
    if unknown_core_ids:
        raise ValueError(f"Unknown core card IDs: {sorted(unknown_core_ids)}")

    core_selection_rows: list[dict[str, Any]] = []
    for card_id, card in sorted(cards_by_id.items()):
        previous_formalization = card["formalization"]
        if card_id in CORE_DETERMINISTIC_IDS:
            role = "deterministic_rule"
            reason = "general_legal_rule_or_symbolic_composition"
            card["review_required"] = True
        elif card_id in CORE_STANDARD_IDS:
            role = "standard_input"
            reason = "general_fact_condition_requiring_neural_judgment"
            card["review_required"] = True
        else:
            role = "context_only"
            if (
                card_module[card_id] == "concurrence"
                or card_id in FUTURE_WORK_GENERAL_PART_IDS
            ):
                reason = "future_work_requires_general_part_corpus"
            else:
                reason = "case_specific_academic_or_noncore_context"
            card["review_required"] = True
        card["formalization"] = role
        if previous_formalization != role:
            append_note(
                card,
                "Scallop core 전수 감사에서 일반 법리와 neural 판단 기준만 core에 남기고 "
                "구체적 적용례·학설·부수 쟁점은 RAG로 분리했다.",
            )
        core_selection_rows.append(
            {
                "card_id": card_id,
                "module": card_module[card_id],
                "role": role,
                "selection_reason": reason,
            }
        )

    general_precedent_core = {
        "fraud_damage_acquisition.property_concept_reported_precedent",
        "fraud_damage_acquisition.property_loss_negative_view",
        "deception.fraud.standard.precedent-notice-duty-materiality",
        "fraud_intent.precedent_illegal_appropriation_intent",
        "mistake_disposition.fraud.variant-triangular-fraud-94do1575-factual-position-interpretation",
    }

    # Core selection is an agent-authored proposal. Keep every selected core card under
    # explicit human review even when its source boundary has been checked locally.
    for card in cards_by_id.values():
        if card["formalization"] in {"deterministic_rule", "standard_input"}:
            if (
                card["authority_basis"] == "commentary_reported_precedent"
                and card["id"] not in general_precedent_core
            ):
                raise ValueError(
                    f"Case-specific card still formalized as core: {card['id']}"
                )
            card["review_required"] = True
            append_note(
                card,
                "최종 수동 감사에서 core 후보로 선별했으며 사용자 승인 전에는 RuleIR 생성을 차단한다.",
            )
        elif card["formalization"] == "policy_variant":
            card["review_required"] = True
        else:
            card["review_required"] = True

    if len(cards_by_id) != 646:
        raise ValueError(
            f"Expected 646 cards after splitting merged variants, found {len(cards_by_id)}"
        )

    core_review_items: list[dict[str, Any]] = []
    for card_id in sorted(all_core_ids):
        card = cards_by_id[card_id]
        role = card["formalization"]
        core_review_items.append(
            {
                "review_id": f"fraud.core.{card_id}",
                "card_id": card_id,
                "module": card_module[card_id],
                "role": role,
                "norm_kind": card["norm_kind"],
                "proposition": card["proposition"],
                "authority_basis": card["authority_basis"],
                "doctrinal_status": card["doctrinal_status"],
                "candidate_refs": card["candidate_refs"],
                "source_refs": card["source_refs"],
                "review_notes": card["review_notes"],
                "review_question": (
                    "이 일반 법리를 Scallop의 결정적 규칙으로 사용하는 데 동의하는가?"
                    if role == "deterministic_rule"
                    else "이 기준을 사실관계에서 모델이 판정할 neural input으로 사용하는 데 동의하는가?"
                ),
            }
        )
    core_review_decisions = preserve_core_review_decisions(core_review_items)
    core_decisions_by_id = {
        row["review_id"]: row for row in core_review_decisions
    }
    for item in core_review_items:
        decision = core_decisions_by_id[item["review_id"]]
        item["human_review"] = decision
        cards_by_id[item["card_id"]]["review_required"] = not (
            decision.get("status") == "completed"
            and decision.get("decision") == "approve"
        )
    core_review_statuses = Counter(
        row.get("status", "pending") for row in core_review_decisions
    )
    core_review_approved = sum(
        row.get("status") == "completed" and row.get("decision") == "approve"
        for row in core_review_decisions
    )
    core_review_unresolved = len(core_review_decisions) - core_review_approved

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

    audit_rows: list[dict[str, Any]] = []
    status_counts: Counter[str] = Counter()
    for card_id, card in sorted(cards_by_id.items()):
        if card["formalization"] == "deterministic_rule":
            review_status = (
                "deterministic_rule_review_pending"
                if card["review_required"]
                else "deterministic_rule_ready"
            )
            rule_ir_role = "derived_rule"
            user_action_required = card["review_required"]
        elif card["formalization"] == "standard_input":
            review_status = (
                "standard_input_review_pending"
                if card["review_required"]
                else "standard_input_ready"
            )
            rule_ir_role = "neural_input_predicate"
            user_action_required = card["review_required"]
        elif card["formalization"] == "policy_variant":
            review_status = "policy_choice_pending"
            rule_ir_role = "active_policy_variant"
            user_action_required = True
        else:
            review_status = "rag_context_only"
            rule_ir_role = "retrieval_only"
            user_action_required = False
        status_counts[review_status] += 1
        audit_rows.append(
            {
                "card_id": card_id,
                "module": card_module[card_id],
                "proposition": card["proposition"],
                "formalization": card["formalization"],
                "authority_basis": card["authority_basis"],
                "doctrinal_status": card["doctrinal_status"],
                "variant_group": card["variant_group"],
                "review_required": card["review_required"],
                "review_status": review_status,
                "rule_ir_role": rule_ir_role,
                "user_action_required": user_action_required,
                "source_comment_ids": sorted(
                    {ref["comment_id"] for ref in card["source_refs"]}
                ),
            }
        )

    grouped_cards: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for card in cards_by_id.values():
        if card["variant_group"]:
            grouped_cards[card["variant_group"]].append(card)

    policy_items: list[dict[str, Any]] = []
    for group_id in sorted(
        {
            card["variant_group"]
            for card in cards_by_id.values()
            if card["formalization"] == "policy_variant"
        }
    ):
        group_cards = sorted(grouped_cards[group_id], key=lambda card: card["id"])
        selectable = [
            card for card in group_cards if card["formalization"] == "policy_variant"
        ]
        precedent_evidence = [
            card
            for card in group_cards
            if card["authority_basis"] == "commentary_reported_precedent"
            or card["doctrinal_status"] == "precedent_position"
        ]
        policy_items.append(
            {
                "review_id": f"fraud.policy.{group_id}",
                "status": "pending",
                "policy_group": group_id,
                "selectable_card_ids": [card["id"] for card in selectable],
                "all_related_card_ids": [card["id"] for card in group_cards],
                "precedent_evidence_card_ids": [
                    card["id"] for card in precedent_evidence
                ],
                "cards": [
                    {
                        "id": card["id"],
                        "formalization": card["formalization"],
                        "authority_basis": card["authority_basis"],
                        "doctrinal_status": card["doctrinal_status"],
                        "proposition": card["proposition"],
                        "source_refs": card["source_refs"],
                    }
                    for card in group_cards
                ],
                "decision_required": (
                    "판례 우선 원칙에 따라 selectable_card_ids 중 활성 정책을 정한다. "
                    "precedent_evidence_card_ids가 비어 있으면 원판례 인덱스 확인이 필요하다."
                ),
            }
        )

    resolved_split_sources = [
        {
            "card_id": card_id,
            "proposition": cards_by_id[card_id]["proposition"],
            "reason": context_only[card_id],
        }
        for card_id in sorted(
            {
                "fraud_general_object.property_scope_variant",
                "fraud_general_object.property_value_variant",
                "fraud_general_object.protected_interest_truth_variant",
            }
        )
    ]

    for module_record in manifest["modules"]:
        module_cards = card_sets[module_record["module"]]["cards"]
        module_record["cards"] = len(module_cards)
        module_record["formalizations"] = dict(
            sorted(Counter(card["formalization"] for card in module_cards).items())
        )
    manifest["totals"]["cards"] = len(cards_by_id)

    for module, path in module_paths.items():
        write_json(path, card_sets[module])
    write_json(CARD_MANIFEST, manifest)
    audit_created_at = (
        read_json(AUDIT).get("created_at")
        if AUDIT.exists()
        else datetime.now(timezone.utc).isoformat()
    )
    write_json(
        AUDIT,
        {
            "version": "1.0.0",
            "issue_tag": "fraud",
            "created_at": audit_created_at,
            "method": "manual_final_audit_no_api",
            "api_calls": 0,
            "cards": len(audit_rows),
            "status_counts": dict(sorted(status_counts.items())),
            "all_cards_accounted_for": len(audit_rows) == 646,
            "rows": audit_rows,
        },
    )
    write_json(
        POLICY_QUEUE,
        {
            "version": "1.0.0",
            "issue_tag": "fraud",
            "status": "complete" if not policy_items else "pending",
            "method": "manual_policy_group_audit_no_api",
            "api_calls": 0,
            "policy_groups": len(policy_items),
            "policy_cards": sum(
                len(item["selectable_card_ids"]) for item in policy_items
            ),
            "items": policy_items,
            "collapsed_policy_sources": [],
            "resolved_split_sources": resolved_split_sources,
        },
    )
    write_json(
        POLICY_RESOLUTION_AUDIT,
        {
            "version": "1.0.0",
            "issue_tag": "fraud",
            "status": "complete",
            "method": "manual_commentary_and_local_primary_precedent_audit_no_api",
            "api_calls": 0,
            "local_primary_source": (
                "../sp/data/processed/Case_DB/clean_open_precedents.parquet"
            ),
            "verified_local_primary_records": VERIFIED_LOCAL_PRIMARY_RECORDS,
            "verified_case_count": len(VERIFIED_LOCAL_PRIMARY_RECORDS),
            "local_primary_verification": verify_local_primary_records(),
            "resolved_groups": len(policy_resolutions),
            "remaining_policy_groups": len(policy_items),
            "resolutions": policy_resolutions,
        },
    )
    write_json(
        CORE_SELECTION_AUDIT,
        {
            "version": "1.0.0",
            "issue_tag": "fraud",
            "status": "draft",
            "legal_review": "pending",
            "method": "manual_full_core_scope_audit_no_api",
            "api_calls": 0,
            "criteria": {
                "deterministic_rule": (
                    "일반 법리, 정의 또는 다른 predicate를 결합하는 상징 규칙"
                ),
                "standard_input": (
                    "일반화된 법적 기준이지만 사실 적용에 neural judgment가 필요한 입력"
                ),
                "context_only": (
                    "구체적 판례 결과, 학설, 희귀 적용례, 이득액 계산 또는 다른 죄명 문맥"
                ),
            },
            "counts": dict(
                sorted(Counter(row["role"] for row in core_selection_rows).items())
            ),
            "rows": core_selection_rows,
        },
    )
    write_json(
        CORE_REVIEW_QUEUE,
        {
            "version": "1.0.0",
            "issue_tag": "fraud",
            "status": (
                "complete" if core_review_unresolved == 0 else "pending"
            ),
            "method": "full_core_card_human_review_queue_no_api",
            "api_calls": 0,
            "cards": len(core_review_items),
            "counts": dict(
                sorted(Counter(item["role"] for item in core_review_items).items())
            ),
            "decision_status_counts": dict(sorted(core_review_statuses.items())),
            "approved": core_review_approved,
            "unresolved": core_review_unresolved,
            "items": core_review_items,
        },
    )
    CORE_REVIEW_DECISIONS.write_text(
        "".join(
            json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n"
            for row in core_review_decisions
        ),
        encoding="utf-8",
    )
    core_guide_lines = [
        "# 사기죄 Scallop core 검수 가이드",
        "",
        "## 범위",
        "",
        "- API 사용: 0회",
        f"- deterministic rule 검수 후보: {len(CORE_DETERMINISTIC_IDS)}개",
        f"- standard input 검수 후보: {len(CORE_STANDARD_IDS)}개",
        f"- RAG/future-work context: {status_counts['rag_context_only']}개",
        f"- 현재 unresolved: {core_review_unresolved}개",
        "",
        "`fraud_core_rule_review_decisions.jsonl`에서 검토한 행의 status를 `completed`로 "
        "바꾸고 decision에 `approve`, `narrow`, `reclassify_to_rag`, `reject` 중 하나를 "
        "기록한다. 수정이 필요하면 notes에 범위와 문구를 적는다.",
        "",
    ]
    for role, title in (
        ("deterministic_rule", "Deterministic Rules"),
        ("standard_input", "Standard Inputs"),
    ):
        core_guide_lines.extend(
            [
                f"## {title}",
                "",
                "| module | card_id | proposition |",
                "|---|---|---|",
            ]
        )
        for item in core_review_items:
            if item["role"] == role:
                core_guide_lines.append(
                    f"| {item['module']} | `{item['card_id']}` | {item['proposition']} |"
                )
        core_guide_lines.append("")
    CORE_REVIEW_GUIDE.write_text(
        "\n".join(core_guide_lines), encoding="utf-8"
    )
    policy_decisions = preserve_policy_decisions(policy_items)
    POLICY_DECISIONS.write_text(
        "".join(
            json.dumps(row, ensure_ascii=False, sort_keys=True)
            + "\n"
            for row in policy_decisions
        ),
        encoding="utf-8",
    )
    guide_lines = [
        "# 사기죄 정책 선택 검수 가이드",
        "",
        "## 상태",
        "",
        "- API 사용: 0회",
        f"- 전체 NormCard: {len(audit_rows)}개",
        f"- deterministic rule 검수 후보: {len(CORE_DETERMINISTIC_IDS)}개",
        f"- standard input 검수 후보: {len(CORE_STANDARD_IDS)}개",
        f"- RAG 전용: {status_counts['rag_context_only']}개",
        f"- 사용자 정책 선택: {len(policy_items)}개 그룹, {sum(len(item['selectable_card_ids']) for item in policy_items)}개 카드",
        "",
        (
            "기존 67개 critic finding과 12개 정책 그룹은 모두 판정·수정 완료되었다. "
            "직접 판례가 있는 쟁점은 실무 규칙으로 활성화했고, 순수 학설 또는 희귀 "
            "적용례는 전역 정책이 아니라 RAG 문맥으로 보존했다."
            if not policy_items
            else "아래에는 판례 우선 선택을 확정할 수 없는 쟁점만 남겼다."
        ),
        "",
    ]
    if policy_items:
        guide_lines.extend(
            [
                "각 결정은 `fraud_policy_review_decisions.jsonl`의 같은 review_id 행에 기록한다.",
                "원판례 인덱스에서 확인한 식별자는 `verified_authority_refs`에 넣는다.",
                "",
            ]
        )
    for index, item in enumerate(policy_items, 1):
        precedent_evidence = item["precedent_evidence_card_ids"]
        evidence_line = (
            "- 현재 corpus의 직접 판례 근거 카드: "
            + ", ".join(f"`{card_id}`" for card_id in precedent_evidence)
            if precedent_evidence
            else "- 현재 corpus의 직접 판례 근거 카드: 없음"
        )
        guide_lines.extend(
            [
                f"## {index}. {item['policy_group']}",
                "",
                f"- review_id: `{item['review_id']}`",
                evidence_line,
                "- 필요한 결정: 아래 선택지 중 판례가 채택한 규칙을 선택하거나, 복합 규칙이면 복수 선택 후 적용관계를 notes에 기재",
                "",
                "| card_id | 선택지 |",
                "|---|---|",
            ]
        )
        for card in item["cards"]:
            if card["id"] not in item["selectable_card_ids"]:
                continue
            guide_lines.append(f"| `{card['id']}` | {card['proposition']} |")
        guide_lines.append("")
    POLICY_GUIDE.write_text("\n".join(guide_lines), encoding="utf-8")
    print(
        json.dumps(
            {
                "api_calls": 0,
                "cards": len(audit_rows),
                "status_counts": dict(sorted(status_counts.items())),
                "policy_groups": len(policy_items),
                "collapsed_policy_sources": 0,
                "resolved_split_sources": len(resolved_split_sources),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
