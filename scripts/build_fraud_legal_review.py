from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]


CARD_MANIFEST = PROJECT_ROOT / "data/rulegen/fraud/fraud_norm_card_manifest.json"
CANDIDATE_MANIFEST = (
    PROJECT_ROOT / "data/rulegen/fraud/fraud_norm_candidate_manifest.json"
)
CRITIC_ROOT = (
    PROJECT_ROOT
    / "data/rulegen/fraud/norm_card_reviews/fraud_norm_cards_critic_v4_final"
)
CRITIC_MANIFEST = CRITIC_ROOT / "manifest.json"
QUEUE = PROJECT_ROOT / "data/rulegen/fraud/fraud_norm_card_review_queue.json"
DECISIONS = PROJECT_ROOT / "data/rulegen/fraud/fraud_human_review_decisions.jsonl"
READINESS = PROJECT_ROOT / "data/rulegen/fraud/fraud_rule_ir_readiness.json"
GUIDE = PROJECT_ROOT / "data/rulegen/fraud/fraud_legal_review_guide.md"


PRIORITY = {
    "source_scope": 1,
    "source_entailment": 1,
    "overgeneralization": 1,
    "missing_norm": 1,
    "authority_mismatch": 2,
    "formalization_error": 3,
    "missing_variant": 4,
    "collapsed_variant": 4,
    "other": 5,
}


# Sol's numeric card selectors are not consistently aligned with the submitted arrays.
# These mappings were audited against each finding, source refs, and card propositions.
AUDITED_CARD_MAPPINGS: dict[str, tuple[str, ...]] = {
    "fraud.normcards.concurrence.part001.critic.counterfeit_reason_unsupported": (
        "fraud_concurrence.counterfeit_currency_real_concurrence",
    ),
    "fraud.normcards.concurrence.part001.critic.goods_nonpayment_source_mismatch": (
        "fraud_concurrence.goods_nonpayment_no_benefit_fraud",
    ),
    "fraud.normcards.concurrence.part002.critic.assigned_claim_outcome_overstated": (
        "fraud_concurrence.assigned_claim_mutually_incompatible",
    ),
    "fraud.normcards.general_object.part001.critic.nonproperty_examples_overgeneralized": (
        "fraud_general_object.nonproperty_examples",
    ),
    "fraud.normcards.general_object.part001.critic.triangular_fraud_case_generalized": (
        "fraud_general_object.triangular_fraud_victim",
    ),
    "fraud.normcards.intent.part001.critic.debt_assets_unsupported_conditions": (
        "fraud_intent.debt_exceeds_assets_alone",
    ),
    "fraud.normcards.intent.part001.critic.insurance_overbilling_unsupported_condition": (
        "fraud_intent.insurance_overbilling",
    ),
    "fraud.normcards.intent.part001.critic.vehicle_sale_unsupported_document_fact": (
        "fraud_intent.vehicle_sale_subsequent_theft",
    ),
    "fraud.normcards.damage_acquisition.part002.critic.letter_credit_authority": (
        "fraud_damage_acquisition.letter_of_credit_no_payment_deduction",
    ),
    "fraud.normcards.damage_acquisition.part002.critic.repeated_investment_authority": (
        "fraud_damage_acquisition.repeated_investment_no_return_deduction",
    ),
    "fraud.normcards.deception.part001.critic.bid_rigging_author_view_authority": (
        "deception.fraud.standard.bid-rigging-fraud-concurrence-view",
    ),
    "fraud.normcards.deception.part003.critic.authority.additional-case-cards": (
        "deception.fraud.standard.artwork-assistant-participation",
        "deception.fraud.standard.land-sale-unknown-urban-planning-area",
        "deception.fraud.standard.land-sale-no-known-urban-planning-conflict",
        "deception.fraud.standard.entrusted-car-unknown-arrears-direct-inquiry",
    ),
    "fraud.normcards.deception.part003.critic.authority.case-card-misclassified": (
        "deception.fraud.standard.car-substitute-performance-reservation",
    ),
    "fraud.normcards.deception.part004.critic.authority.false_documents_speculative": (
        "deception.fraud.standard.false-documents-budget-withdrawal",
    ),
    "fraud.normcards.deception.part004.critic.authority.statutory_subsidy_definitions": (
        "deception.fraud.definition.subsidy-and-indirect-subsidy",
    ),
    "fraud.normcards.deception.part005.critic.unsupported-settled-status": (
        "deception.fraud.definition.deception-target-human",
    ),
    "fraud.normcards.deception.part005.critic.unsupported-settled-status-disposal-authority": (
        "deception.fraud.element.deceived-person-disposal-authority",
    ),
    "fraud.normcards.deception.part005.critic.unsupported-settled-status-distinct-persons": (
        "deception.fraud.definition.deceived-person-victim-distinct",
    ),
    "fraud.normcards.deception.part005.critic.unsupported-settled-status-unspecified-person": (
        "deception.fraud.definition.deceived-person-unspecified",
    ),
    "fraud.normcards.general_object.part001.critic.settled_status_not_supported": (
        "general_object.fraud.element.object-other-possessed-other-property",
        "general_object.fraud.definition.property-benefit",
        "general_object.fraud.element.property-benefit-concrete",
        "general_object.fraud.definition.property-benefit-not-numerically-limited",
    ),
    "fraud.normcards.general_object.part001.critic.unquantified_value_authority_unsupported": (
        "fraud_general_object.unquantified_benefit_judgment",
    ),
    "fraud.normcards.intent.part001.critic.no_disposition_authority_unestablished": (
        "fraud_intent.no_disposition_inducement_intent",
    ),
    "fraud.normcards.stages_participation.part001.critic.authority.real_estate_combined_sources": (
        "fraud_stages_participation.real_estate_fraud_completion",
    ),
    (
        "fraud.normcards.stages_participation.part001.critic.authority."
        "voice_phishing_commentary_view"
    ): (
        "fraud_stages_participation.voice_phishing_functional_control",
    ),
    (
        "fraud.normcards.concurrence.part001.critic."
        "commentary_penalties_deterministic_before_verification"
    ): (
        "fraud_concurrence.general_fraud_penalty",
        "fraud_concurrence.attempt_habitual_punishment",
        "fraud_concurrence.aggravated_economic_value_thresholds",
    ),
    "fraud.normcards.deception.part003.critic.formalization.conditional-intent-sufficiency": (
        "deception.fraud.element.intent-to-defraud-conditional-intent",
    ),
    "fraud.normcards.deception.part003.critic.formalization.element-sufficiency": (
        "deception.fraud.element.loan-no-repayment-intent-or-ability",
    ),
    "fraud.normcards.deception.part004.critic.formalization.subsidy_definition": (
        "deception.fraud.definition.subsidy-and-indirect-subsidy",
    ),
    "fraud.normcards.general_object.part001.critic.subjective_elements_formalization": (
        "fraud_general_object.subjective_elements",
    ),
    "fraud.normcards.concurrence.part001.critic.agent_competing_position_group_incomplete": (
        "fraud_concurrence.agent_fraud_only_view",
        "fraud_concurrence.agent_breach_only_view",
        "fraud_concurrence.agent_imaginary_concurrence_view",
        "fraud_concurrence.agent_precedent_imaginary_concurrence",
    ),
    "fraud.normcards.concurrence.part001.critic.counterfeit_variant_group_incomplete": (
        "fraud_concurrence.counterfeit_currency_real_concurrence",
        "fraud_concurrence.counterfeit_currency_imaginary_view",
    ),
    "fraud.normcards.deception.part001.critic.future_facts_variant_group_split": (
        "deception.fraud.variant.future-facts-unlimited",
        "deception.fraud.variant.future-facts-limited",
        "deception.fraud.variant.future-facts-negative",
    ),
    "fraud.normcards.deception.part001.critic.opinion_statement_variant_group_split": (
        "deception.fraud.variant.opinion-statement-negative",
        "deception.fraud.variant.opinion-statement-affirmative",
        "deception.fraud.variant.opinion-statement-mistake-sufficiency",
        "deception.fraud.variant.opinion-statement-third-view-concreteness",
    ),
    "fraud.normcards.deception.part001.critic.third_view_supplement_ungrouped": (
        "deception.fraud.variant.opinion-statement-mistake-sufficiency",
        "deception.fraud.variant.opinion-statement-third-view-concreteness",
    ),
    "fraud.normcards.deception.part003.critic.variants.double-sale": (
        "deception.fraud.standard.double-sale-second-buyer-registered",
        "deception.fraud.standard.double-sale-no-intent-transfer-first-buyer",
        "deception.fraud.standard.second-real-estate-sale-first-contract",
        "deception.fraud.standard.double-sale-first-sale-unregistered",
        "deception.fraud.standard.double-sale-first-buyer-registered",
    ),
    "fraud.normcards.deception.part003.critic.variants.nonmedical-clinic": (
        "deception.fraud.standard.nonmedical-clinic-national-health-insurance",
        "deception.fraud.standard.nonmedical-clinic-indemnity-insurance",
    ),
    "fraud.normcards.deception.part004.critic.variant.medical_corporation_exception": (
        "deception.fraud.standard.medical-corporation-nonmedical-involvement",
        "deception.fraud.exception.medical-corporation-nonmedical-abuse-types",
    ),
    "fraud.normcards.deception.part004.critic.variant.religious_practice_boundary": (
        "deception.fraud.standard.religious-compensation-not-necessarily-fraud",
        "deception.fraud.standard.shamanistic-false-misfortune",
        "deception.fraud.standard.prayer-fee-beyond-permitted-limit",
        "deception.fraud.standard.false-religious-claims-donations",
    ),
    "fraud.normcards.general_object.part001.critic.sex_work_variants_not_grouped": (
        "general_object.fraud.variant.sex-work-contract-fraud-negative",
        "general_object.fraud.variant.sex-work-contract-fraud-affirmative",
    ),
    "fraud.normcards.stages_participation.part001.critic.variant.completion_without_gain": (
        "fraud_stages_participation.completion_deception_disposition_transfer",
        "fraud_stages_participation.victim_loss_completion_view",
        "fraud_stages_participation.payment_guarantee_not_provided_no_completion",
    ),
    "fraud.normcards.concurrence.part002.critic.sanction_cards_missing_review_question": (
        "fraud_concurrence.aggravated_economic_optional_fine",
        "fraud_concurrence.insurance_fraud_sanctions",
        "fraud_concurrence.military_criminal_act_sanctions",
        "fraud_concurrence.military_property_special_act_sanctions",
    ),
}


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return value


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def load_human_decisions() -> dict[str, dict[str, Any]]:
    if not DECISIONS.exists():
        return {}
    decisions: dict[str, dict[str, Any]] = {}
    for line in DECISIONS.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        decision = json.loads(line)
        review_id = decision["review_id"]
        if review_id in decisions:
            raise ValueError(f"Duplicate human review decision: {review_id}")
        decisions[review_id] = decision
    return decisions


def generated_review_question_scopes(
    part_card_ids: list[str],
    cards_by_id: dict[str, dict[str, Any]],
) -> list[tuple[str, list[str]]]:
    part_cards = [cards_by_id[card_id] for card_id in part_card_ids]
    groups = [
        (
            "Verify authority, scope, polarity, and formalization for these "
            "review-required cards: ",
            [card["id"] for card in part_cards if card["review_required"]],
        ),
        (
            "Verify the primary decisions and permissible generalization of these "
            "commentary-reported case cards: ",
            [
                card["id"]
                for card in part_cards
                if card["formalization"] == "context_only"
            ],
        ),
        (
            "Group competing views and select the precedent-aligned practical policy "
            "for these variant cards: ",
            [
                card["id"]
                for card in part_cards
                if card["formalization"] == "policy_variant"
            ],
        ),
    ]
    return [
        (prefix + ", ".join(card_ids), card_ids)
        for prefix, card_ids in groups
        if card_ids
    ]


def load_cards() -> tuple[
    dict[str, dict[str, Any]], dict[str, list[dict[str, Any]]]
]:
    manifest = read_json(CARD_MANIFEST)
    cards_by_id: dict[str, dict[str, Any]] = {}
    cards_by_module: dict[str, list[dict[str, Any]]] = {}
    for module in manifest["modules"]:
        card_set = read_json(PROJECT_ROOT / module["path"])
        cards_by_module[module["module"]] = card_set["cards"]
        cards_by_id.update({card["id"]: card for card in card_set["cards"]})
    return cards_by_id, cards_by_module


def resolve_impacted_cards(
    review_id: str,
    finding: dict[str, Any],
    part_card_ids: list[str],
    cards_by_id: dict[str, dict[str, Any]],
) -> tuple[list[str], dict[str, Any]]:
    target_path = finding["target_path"]
    if review_id in AUDITED_CARD_MAPPINGS:
        impacted = list(AUDITED_CARD_MAPPINGS[review_id])
        unknown = [card_id for card_id in impacted if card_id not in cards_by_id]
        outside_part = [card_id for card_id in impacted if card_id not in part_card_ids]
        finding_refs = {ref["comment_id"] for ref in finding["source_refs"]}
        source_mismatch = [
            card_id
            for card_id in impacted
            if card_id in cards_by_id
            and not finding_refs.intersection(
                ref["comment_id"] for ref in cards_by_id[card_id]["source_refs"]
            )
        ]
        if unknown or outside_part or source_mismatch:
            raise ValueError(
                f"Invalid audited mapping for {review_id}: "
                f"unknown={unknown}, outside_part={outside_part}, "
                f"source_mismatch={source_mismatch}"
            )
        return impacted, {
            "method": "critic_text_audited_override",
            "confidence": 1.0,
            "audit_basis": "finding_text_source_refs_and_card_propositions",
        }

    if "legal_review_questions" in target_path:
        match = re.search(r"legal_review_questions(?:\[|/)(\d+)", target_path)
        if not match:
            return [], {"method": "card_set_metadata", "confidence": 1.0}
        question_index = int(match.group(1))
        questions = generated_review_question_scopes(part_card_ids, cards_by_id)
        if question_index >= len(questions):
            raise ValueError(
                f"Unknown generated review question for {review_id}: {target_path}"
            )
        question, impacted = questions[question_index]
        return impacted, {
            "method": "generated_review_question_scope",
            "confidence": 1.0,
            "review_question": question,
        }

    if "coverage_gaps" in target_path:
        return [], {"method": "card_set_metadata", "confidence": 1.0}

    finding_text = " ".join(
        [
            target_path,
            finding["message"],
            finding["recommended_action"],
        ]
    )
    direct = [card_id for card_id in part_card_ids if card_id in finding_text]
    if direct:
        return direct, {"method": "explicit_card_id", "confidence": 1.0}
    if "cards" not in target_path:
        return [], {"method": "card_set_metadata", "confidence": 1.0}
    if "[*]" in target_path:
        return part_card_ids, {"method": "explicit_wildcard", "confidence": 1.0}
    raise ValueError(
        f"Unaudited numeric card selector for {review_id}: {target_path}"
    )


def build_queue(
    cards_by_id: dict[str, dict[str, Any]],
    decisions: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, set[str]]]:
    manifest = read_json(CRITIC_MANIFEST)
    queue: list[dict[str, Any]] = []
    impacted_by_module: dict[str, set[str]] = defaultdict(set)
    for report_meta in manifest["reports"]:
        report = read_json(PROJECT_ROOT / report_meta["path"])
        for finding in report["findings"]:
            review_id = f"{report_meta['request_id']}.{finding['finding_id']}"
            impacted, mapping = resolve_impacted_cards(
                review_id,
                finding,
                report_meta["card_ids"],
                cards_by_id,
            )
            human_review = decisions.get(
                review_id,
                {
                    "review_id": review_id,
                    "status": "pending",
                    "decision": None,
                    "notes": "",
                    "verified_authority_refs": [],
                },
            )
            if human_review["status"] != "completed":
                impacted_by_module[report_meta["module"]].update(impacted)
            queue.append(
                {
                    "review_id": review_id,
                    "priority": PRIORITY.get(finding["type"], 5),
                    "module": report_meta["module"],
                    "part": report_meta["part"],
                    "severity": finding["severity"],
                    "type": finding["type"],
                    "target_path": finding["target_path"],
                    "message": finding["message"],
                    "recommended_action": finding["recommended_action"],
                    "source_refs": finding["source_refs"],
                    "card_mapping": mapping,
                    "human_review": human_review,
                    "impacted_card_ids": impacted,
                    "impacted_cards": [
                        {
                            "id": card_id,
                            "proposition": cards_by_id[card_id]["proposition"],
                            "formalization": cards_by_id[card_id]["formalization"],
                            "authority_basis": cards_by_id[card_id]["authority_basis"],
                            "source_refs": cards_by_id[card_id]["source_refs"],
                        }
                        for card_id in impacted
                    ],
                }
            )
    queue.sort(key=lambda row: (row["priority"], row["module"], row["review_id"]))
    return queue, impacted_by_module


def build_readiness(
    cards_by_module: dict[str, list[dict[str, Any]]],
    impacted_by_module: dict[str, set[str]],
) -> dict[str, Any]:
    modules: list[dict[str, Any]] = []
    totals: Counter[str] = Counter()
    for module, cards in cards_by_module.items():
        buckets: dict[str, list[str]] = defaultdict(list)
        impacted = impacted_by_module[module]
        for card in cards:
            if card["id"] in impacted:
                bucket = "critic_pending"
            elif card["formalization"] == "context_only":
                bucket = "context_only_excluded"
            elif card["formalization"] == "policy_variant":
                bucket = "policy_choice_pending"
            elif card["review_required"]:
                bucket = "human_review_pending"
            elif card["formalization"] == "standard_input":
                bucket = "neural_grounding_spec_ready"
            elif card["formalization"] == "deterministic_rule":
                bucket = "provisional_rule_ir_ready"
            else:
                raise ValueError(
                    f"Unhandled formalization for readiness: {card['id']}"
                )
            buckets[bucket].append(card["id"])
            totals[bucket] += 1
        modules.append(
            {
                "module": module,
                "cards": len(cards),
                "buckets": dict(sorted(buckets.items())),
                "counts": {
                    key: len(value) for key, value in sorted(buckets.items())
                },
            }
        )
    return {
        "version": "1.1.0",
        "issue_tag": "fraud",
        "status": "draft",
        "legal_review": "pending",
        "full_rule_ir_generation_blocked": True,
        "blocking_reason": (
            "The practical precedent choices, source-entailment findings, and policy "
            "variant groups require human legal review before full RuleIR generation."
        ),
        "modules": modules,
        "totals": dict(sorted(totals.items())),
        "existing_executable_exemplar": (
            "data/rulegen/fraud/fraud_rule_ir_exemplar.json"
        ),
    }


def write_decision_template(queue: list[dict[str, Any]]) -> None:
    if DECISIONS.exists():
        return
    DECISIONS.write_text(
        "".join(
            json.dumps(
                {
                    "review_id": row["review_id"],
                    "status": "pending",
                    "decision": None,
                    "notes": "",
                    "verified_authority_refs": [],
                },
                ensure_ascii=False,
                sort_keys=True,
            )
            + "\n"
            for row in queue
        ),
        encoding="utf-8",
    )


def build_guide(
    queue: list[dict[str, Any]],
    readiness: dict[str, Any],
    cards_by_module: dict[str, list[dict[str, Any]]],
    candidate_count: int,
) -> str:
    by_type = Counter(row["type"] for row in queue)
    by_module = Counter(row["module"] for row in queue)
    by_review_status = Counter(
        row["human_review"]["status"] for row in queue
    )
    lines = [
        "# 사기죄 NormCard 법률 검수 가이드",
        "",
        "## 현재 상태",
        "",
        "- 범위: 형법 제347조 사기죄 주석서 13개 배치만 포함한다.",
        f"- 검증 후보 {candidate_count}개가 NormCard "
        f"{sum(map(len, cards_by_module.values()))}개에 연결되어 있다.",
        "- Sol 최종 비평은 17개 묶음 전부 계약 검증을 통과했다.",
        f"- 검토 지적은 {len(queue)}개이며, 모든 산출물은 draft/legal_review=pending이다.",
        f"- 사용자 판정은 completed {by_review_status['completed']}개, "
        f"pending {by_review_status['pending']}개다.",
        "- 주석서가 보고한 판례로 추정되는 카드는 원판례 확인 전 context_only로 격리했다.",
        "",
        "## 지적-카드 매핑",
        "",
        "- Sol 보고서의 `target_path` 숫자 인덱스는 제출 배열과 일관되게 대응하지 않아 검수 대상으로 직접 사용하지 않는다.",
        "- 숫자 경로가 있던 40개 지적은 지적 문구, source_refs, 카드 proposition을 대조하여 카드 ID로 고정했다.",
        "- 검수할 실제 대상은 각 항목의 `impacted_card_ids`와 `impacted_cards`이며, 매핑 근거는 `card_mapping`에 기록했다.",
        "- `legal_review_questions` 지적은 질문을 생성한 카드와 원 질문을 `card_mapping.review_question`에 표시한다.",
        "- 이후 미등록 숫자 경로가 추가되면 큐 생성은 추측하지 않고 실패한다.",
        "",
        "## Source entailment 판정",
        "",
        "- 카드의 source quote는 provenance용 정확 인용구이지 해당 chunk의 유일한 의미 범위가 아니다.",
        "- source_entailment 지적은 같은 comment_id의 전체 document_text까지 대조한다.",
        "- 이번 8건 중 7건은 전체 chunk가 해당 문구를 명시하여 기각했고, 제3자 취득형 번역 오류 1건만 수정했다.",
        "",
        "## 검수 순서",
        "",
        "1. 출처 의미: source_entailment, overgeneralization, missing_norm, source_scope를 먼저 본다.",
        "2. 권위: commentary_reported_precedent 여부와 원판례의 실제 법리를 판례 인덱스로 확인한다.",
        "3. 형식화: deterministic_rule, standard_input, context_only 구분을 확인한다.",
        "4. 학설 대립: 같은 쟁점의 variant_group을 묶고 실무상 판례 입장을 선택한다.",
        "5. 승인된 카드만 RuleIR로 내린다. 미확인 사실이나 반대사실은 unknown으로 유지한다.",
        "",
        "## 결정값",
        "",
        "`fraud_human_review_decisions.jsonl`에서 각 review_id의 status를 completed로 "
        "바꾸고 decision을 기록한다.",
        "허용 결정 예시는 approve_as_is, accept_finding_pending_remediation, "
        "correct_translation, narrow_proposition, reclassify_authority, "
        "set_context_only, "
        "group_variant, select_precedent_variant, reject_card, needs_more_source이다.",
        "원판례를 확인한 경우 verified_authority_refs에 사용자의 판례 인덱스 식별자를 넣는다.",
        "",
        "## 지적 분포",
        "",
        "| 유형 | 건수 |",
        "|---|---:|",
    ]
    lines.extend(f"| {key} | {value} |" for key, value in sorted(by_type.items()))
    lines.extend(
        [
            "",
            "## 모듈별 우선순위",
            "",
            "| 모듈 | 카드 | 지적 | context_only | policy_variant |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for module, cards in cards_by_module.items():
        lines.append(
            f"| {module} | {len(cards)} | {by_module[module]} | "
            f"{sum(card['formalization'] == 'context_only' for card in cards)} | "
            f"{sum(card['formalization'] == 'policy_variant' for card in cards)} |"
        )
    lines.extend(
        [
            "",
            "## RuleIR 게이트",
            "",
            f"- critic_pending: {readiness['totals'].get('critic_pending', 0)}",
            f"- context_only_excluded: {readiness['totals'].get('context_only_excluded', 0)}",
            f"- policy_choice_pending: {readiness['totals'].get('policy_choice_pending', 0)}",
            f"- human_review_pending: {readiness['totals'].get('human_review_pending', 0)}",
            "- neural_grounding_spec_ready: "
            f"{readiness['totals'].get('neural_grounding_spec_ready', 0)}",
            "- provisional_rule_ir_ready: "
            f"{readiness['totals'].get('provisional_rule_ir_ready', 0)}",
            "",
            "현재 전체 RuleIR 생성은 차단되어 있다. 기존 8장짜리 사기죄 모범 NormCard/RuleIR/Scallop은 구조 예시로만 유지하며, "
            "636장 전체에 대한 법적 승인으로 간주하지 않는다.",
            "",
            "## 파일",
            "",
            "- 상세 검수 큐: `data/rulegen/fraud/fraud_norm_card_review_queue.json`",
            "- 결정 입력: `data/rulegen/fraud/fraud_human_review_decisions.jsonl`",
            "- RuleIR readiness: `data/rulegen/fraud/fraud_rule_ir_readiness.json`",
            "- Sol 원보고서: `data/rulegen/fraud/norm_card_reviews/fraud_norm_cards_critic_v4_final/`",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    cards_by_id, cards_by_module = load_cards()
    candidate_count = read_json(CANDIDATE_MANIFEST)["totals"]["candidates"]
    decisions = load_human_decisions()
    queue, impacted_by_module = build_queue(cards_by_id, decisions)
    readiness = build_readiness(cards_by_module, impacted_by_module)
    write_json(
        QUEUE,
        {
            "version": "1.1.0",
            "issue_tag": "fraud",
            "status": "draft",
            "legal_review": "pending",
            "items": queue,
        },
    )
    write_json(READINESS, readiness)
    write_decision_template(queue)
    GUIDE.write_text(
        build_guide(queue, readiness, cards_by_module, candidate_count),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {"review_items": len(queue), **readiness["totals"]},
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
