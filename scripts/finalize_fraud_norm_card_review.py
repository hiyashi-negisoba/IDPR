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
    if orphan_ids:
        raise ValueError(f"Orphan policy decisions: {sorted(orphan_ids)}")

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

    # `review_required` had been overloaded to mean that neural application is needed.
    # After the full critic pass and the 57 accepted remediations, every non-policy,
    # non-context card is legally source-bounded; neural standards remain input specs.
    for card in cards_by_id.values():
        if card["formalization"] in {"deterministic_rule", "standard_input"}:
            if card["authority_basis"] == "commentary_reported_precedent":
                raise ValueError(
                    f"Case-specific card still formalized as core: {card['id']}"
                )
            card["review_required"] = False
            append_note(
                card,
                "최종 수동 감사에서 법률검토와 neural grounding을 분리하여 RuleIR 입력 가능으로 확정했다.",
            )
        elif card["formalization"] == "policy_variant":
            card["review_required"] = True
        else:
            card["review_required"] = True

    if len(cards_by_id) != 646:
        raise ValueError(
            f"Expected 646 cards after splitting merged variants, found {len(cards_by_id)}"
        )

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
            review_status = "deterministic_rule_ready"
            rule_ir_role = "derived_rule"
            user_action_required = False
        elif card["formalization"] == "standard_input":
            review_status = "standard_input_ready"
            rule_ir_role = "neural_input_predicate"
            user_action_required = False
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
            "status": "pending",
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
        f"- 자동 확정된 deterministic rule: {status_counts['deterministic_rule_ready']}개",
        f"- 자동 확정된 standard input: {status_counts['standard_input_ready']}개",
        f"- RAG 전용: {status_counts['rag_context_only']}개",
        f"- 사용자 정책 선택: {len(policy_items)}개 그룹, {sum(len(item['selectable_card_ids']) for item in policy_items)}개 카드",
        "",
        "기존 67개 critic finding은 모두 판정·수정 완료되었다. 아래에는 현재 corpus만으로 판례 우선 선택을 확정할 수 없는 쟁점만 남겼다.",
        "각 결정은 `fraud_policy_review_decisions.jsonl`의 같은 review_id 행에 기록한다.",
        "원판례 인덱스에서 확인한 식별자는 `verified_authority_refs`에 넣는다.",
        "",
    ]
    for index, item in enumerate(policy_items, 1):
        guide_lines.extend(
            [
                f"## {index}. {item['policy_group']}",
                "",
                f"- review_id: `{item['review_id']}`",
                "- 현재 corpus의 직접 판례 근거: 없음",
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
