from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT))

from idpr.rulegen import (  # noqa: E402
    render_rule_ir_natural_language_scaffold,
    validate_full_rule_ir_generation,
)
from scripts.prepare_fraud_full_rule_ir_generation import (  # noqa: E402
    atom,
    predicate,
    rule,
    source_union,
    string,
    variable,
)


FRAUD_ROOT = PROJECT_ROOT / "data/rulegen/fraud"
CORE_SET = FRAUD_ROOT / "fraud_core_norm_card_set.json"
COMMENTARY = PROJECT_ROOT / "data/commentary/kcl_criminal_v1_commentary_chunks.jsonl"
RAW_TERRA = (
    PROJECT_ROOT
    / ".cache/llm/runs/fraud_full_rule_ir/fraud-full-rule-ir-v1/terra"
    / "fraud.article347.rule_ir.full.v1.json"
)
RUN_SUMMARY = (
    PROJECT_ROOT
    / ".cache/llm/runs/fraud_full_rule_ir/fraud-full-rule-ir-v1/run.json"
)
CANDIDATE = FRAUD_ROOT / "fraud_full_rule_ir_candidate_unreviewed.json"
SCAFFOLD = FRAUD_ROOT / "fraud_full_rule_ir_natural_language_scaffold.md"
EXPLANATION = FRAUD_ROOT / "fraud_full_rule_ir_natural_language_explanation.md"
AGENT_REVIEW = FRAUD_ROOT / "fraud_full_rule_ir_agent_review.md"
HUMAN_GUIDE = FRAUD_ROOT / "fraud_full_rule_ir_human_review_guide.md"
POST_TERRA_STATUS = FRAUD_ROOT / "fraud_full_rule_ir_post_terra_status.json"
TERRA_AUDIT = FRAUD_ROOT / "fraud_full_rule_ir_terra_failure_audit.json"
TRACKED_TERRA_OUTPUT = FRAUD_ROOT / "fraud_full_rule_ir_terra_partial_output.json"
MODULE_OWNERSHIP = FRAUD_ROOT / "fraud_rule_ir_module_ownership.json"


ACTOR_ARGUMENTS = [
    ("case_id", "String"),
    ("defendant_id", "String"),
    ("deceived_person_id", "String"),
    ("disposer_id", "String"),
    ("property_owner_id", "String"),
    ("subject_id", "String"),
    ("beneficiary_id", "String"),
]
ASSESSMENT_ARGUMENTS = [
    ("case_id", "String"),
    ("assessment_id", "String"),
    *ACTOR_ARGUMENTS[1:],
    ("status", "String"),
]


BAR_CARD_IDS = {
    "deception.fraud.causal-link.loan-purpose-not-sole-trigger",
    "deception.fraud.causal-link.no-disposition-no-deception",
    "deception.fraud.definition.deception-target-human",
    "deception.fraud.element.deception-must-create-false-belief",
    "deception.fraud.element.transaction-purpose-no-impairment",
    "deception.fraud.standard.advertising-tolerable-exaggeration",
    "deception.fraud.standard.easily-detectable-lie",
    "deception.fraud.standard.loan-lender-anticipated-risk",
    "deception.fraud.standard.loan-subsequent-default",
    "deception.fraud.standard.vague-opinion-not-deception",
    "fraud_general_object.causation_required",
    "fraud_general_object.deception_error_causation",
    "fraud_intent.no_disposition_inducement_intent",
    "fraud_mistake.no_capacity_theft",
    "fraud_mistake.no_thought_no_error",
    "fraud_mistake.omission_not_all_nonclaims",
    "fraud_mistake.property_limited_disposition",
    "fraud_mistake.trick_theft_directness",
    "fraud_stages_participation.no_causation_attempt",
    "general_object.fraud.standard.own-possession-other-property-embezzlement",
    "general_object.fraud.standard.own-property-not-object",
    "general_object.fraud.standard.public-interest-only-no-fraud",
    "special_forms.fraud.standard.right-exercise-socially-acceptable-no-crime",
}

MANDATORY_POSITIVE_CARD_IDS = {
    "deception.fraud.definition.deception-good-faith-mistake",
    "fraud_intent.contract_breach_distinction",
    "fraud_mistake.deceived_disposer_identity",
    "fraud_mistake.disposition_definition",
    "fraud_mistake.error_definition",
    "fraud_mistake.gain_purpose",
    "fraud_mistake.property_disposition_element",
    "fraud_mistake.sequential_causation",
    "fraud_stages_participation.completion_deception_disposition_transfer",
    "general_object.fraud.element.object-other-possessed-other-property",
}

COMPONENT_SOURCES = {
    "fraud_object_satisfied": [
        "general_object.fraud.element.object-other-possessed-other-property",
        "general_object.fraud.exception.public-interest-property-equivalence",
    ],
    "fraud_deception_satisfied": [
        "deception.fraud.definition.deception-good-faith-mistake",
        "deception.fraud.definition.exploitation-existing-mistake",
        "deception.fraud.element.loan-no-repayment-intent-or-ability",
        "deception.fraud.standard.advertising-important-concrete-falsehood",
        "deception.fraud.standard.implicit-deception-explanatory-value",
        "deception.fraud.standard.loan-purpose-materiality",
        "fraud_damage_acquisition.right_exercise_unacceptable_deception",
    ],
    "fraud_mistake_satisfied": [
        "fraud_mistake.error_definition",
        "fraud_mistake.error_doubt_ignorance",
        "fraud_mistake.unaware_error",
    ],
    "fraud_disposition_satisfied": [
        "fraud_mistake.disposition_definition",
        "fraud_mistake.conscious_nonexercise",
        "fraud_mistake.disposition_intent_act_awareness",
        "fraud_mistake.disposition_omission",
        "fraud_mistake.factual_act_disposition",
        "fraud_mistake.invalid_act_disposition",
    ],
    "fraud_acquisition_satisfied": [
        "fraud_damage_acquisition.delivery_factual_control",
        "fraud_damage_acquisition.delivery_of_property",
        "fraud_damage_acquisition.property_concept_reported_precedent",
        "fraud_damage_acquisition.property_disposition_types",
        "fraud_mistake.property_disposition_element",
    ],
    "fraud_causal_chain_satisfied": [
        "fraud_mistake.sequential_causation",
    ],
    "fraud_deceived_disposer_identity_satisfied": [
        "fraud_mistake.deceived_disposer_identity",
    ],
    "fraud_completion_satisfied": [
        "fraud_stages_participation.completion_deception_disposition_transfer",
        "fraud_stages_participation.property_fraud_completion_control",
    ],
    "fraud_third_party_acquisition_satisfied": [
        "fraud_intent.third_party_acquisition",
    ],
    "fraud_triangular_authority_satisfied": [
        "mistake_disposition.fraud.variant-triangular-fraud-94do1575-"
        "factual-position-interpretation",
    ],
    "fraud_unlawful_appropriation_intent_supported": [
        "fraud_intent.precedent_illegal_appropriation_intent",
    ],
}

COMPONENT_DEFINITIONS = {
    "fraud_object_satisfied": "사기죄의 객체가 되는 타인의 재물 또는 구체적 재산상 이익이 인정됨",
    "fraud_deception_satisfied": "사건에 적용되는 기망 기준이 충족됨",
    "fraud_mistake_satisfied": "피기망자에게 법적 의미의 착오가 인정됨",
    "fraud_disposition_satisfied": "착오에 기한 재산적 처분행위가 인정됨",
    "fraud_acquisition_satisfied": "재물 교부 또는 재산상 이익의 취득이 인정됨",
    "fraud_causal_chain_satisfied": "기망·착오·처분·취득 사이의 순차적 인과관계가 인정됨",
    "fraud_deceived_disposer_identity_satisfied": "피기망자와 처분행위자가 동일한 행위주체임",
    "fraud_completion_satisfied": "사기죄가 미수를 넘어 기수에 이른 이전 또는 지배취득이 인정됨",
    "fraud_third_party_acquisition_satisfied": "제3자 취득을 피고인에게 귀속할 주관적·도구적 관계가 인정됨",
    "fraud_triangular_authority_satisfied": "피기망자 겸 처분자에게 피해자 재산을 처분할 권능 또는 지위가 인정됨",
    "fraud_unlawful_appropriation_intent_supported": "불법영득의사가 요구되는 유형에서 그 의사가 인정됨",
    "fraud_intent_satisfied": "고의의 기망과 재산적 이득 목적이 함께 인정됨",
    "fraud_no_separate_loss_gate": "재물 교부 또는 이익 취득 외에 현실적 재산상 손해를 별도 요건으로 요구하지 않음",
    "fraud_role_structure_satisfied": "일반형 또는 삼각사기의 역할 구조와 처분 권능 요건이 충족됨",
    "fraud_beneficiary_attribution_satisfied": "본인 또는 제3자에게 귀속되는 취득 구조가 충족됨",
}


# Every approved card has exactly one primary owner. Modules may emit the same
# canonical interface, but the final core consumes interfaces rather than subtype rules.
MODULE_SPECS = [
    {
        "module_id": "core.deception",
        "kind": "general_core",
        "description": "모든 사기 유형에 공통되는 기망의 정의, 한계 및 판단 기준",
        "emits": ["fraud_deception_satisfied", "fraud_not_established"],
        "card_ids": [
            "deception.fraud.causal-link.deception-property-disposition",
            "deception.fraud.causal-link.no-disposition-no-deception",
            "deception.fraud.definition.deception-content-basis-fact",
            "deception.fraud.definition.deception-counterparty-is-other",
            "deception.fraud.definition.deception-good-faith-mistake",
            "deception.fraud.definition.deception-means-unrestricted",
            "deception.fraud.definition.deception-object-facts",
            "deception.fraud.definition.deception-target-human",
            "deception.fraud.definition.other-includes-corporation",
            "deception.fraud.element.deception-must-create-false-belief",
            "deception.fraud.element.deception-not-legal-act-important-part",
            "deception.fraud.element.transaction-purpose-no-impairment",
            "deception.fraud.element.victim-negligence-no-bar",
            "deception.fraud.standard.deception-concrete-circumstances",
            "deception.fraud.standard.easily-detectable-lie",
            "deception.fraud.standard.vague-opinion-not-deception",
        ],
    },
    {
        "module_id": "core.intent",
        "kind": "general_core",
        "description": "편취 범의, 재산적 이득 목적 및 행위시 판단 기준",
        "emits": [
            "fraud_intent_satisfied",
            "fraud_unlawful_appropriation_intent_supported",
            "fraud_not_established",
        ],
        "card_ids": [
            "fraud_intent.contract_breach_distinction",
            "fraud_intent.illegal_appropriation_definition",
            "fraud_intent.no_disposition_inducement_intent",
            "fraud_intent.precedent_illegal_appropriation_intent",
            "fraud_intent.time_of_conduct",
            "fraud_mistake.gain_purpose",
        ],
    },
    {
        "module_id": "core.mistake_disposition",
        "kind": "general_core",
        "description": "착오, 처분행위, 직접성 및 순차적 인과관계의 공통 규칙",
        "emits": [
            "fraud_mistake_satisfied",
            "fraud_disposition_satisfied",
            "fraud_acquisition_satisfied",
            "fraud_causal_chain_satisfied",
            "fraud_deceived_disposer_identity_satisfied",
            "fraud_not_established",
        ],
        "card_ids": [
            "fraud_mistake.deceived_disposer_identity",
            "fraud_mistake.disposition_definition",
            "fraud_mistake.disposition_directness",
            "fraud_mistake.disposition_intent_act_awareness",
            "fraud_mistake.error_definition",
            "fraud_mistake.error_disposition_motivation",
            "fraud_mistake.error_doubt_ignorance",
            "fraud_mistake.factual_act_disposition",
            "fraud_mistake.invalid_act_disposition",
            "fraud_mistake.no_thought_no_error",
            "fraud_mistake.property_disposition_element",
            "fraud_mistake.property_limited_disposition",
            "fraud_mistake.sequential_causation",
            "fraud_mistake.unaware_error",
        ],
    },
    {
        "module_id": "profile.loan",
        "kind": "grounding_profile",
        "description": "차용금 사기의 변제능력·의사, 용도, 위험인식 및 범의 추론",
        "emits": [
            "fraud_deception_satisfied",
            "fraud_intent_satisfied",
            "fraud_not_established",
        ],
        "card_ids": [
            "deception.fraud.causal-link.loan-purpose-not-sole-trigger",
            "deception.fraud.element.loan-no-repayment-intent-or-ability",
            "deception.fraud.standard.intent-to-defraud-loan-inference",
            "deception.fraud.standard.loan-lender-anticipated-risk",
            "deception.fraud.standard.loan-purpose-materiality",
            "deception.fraud.standard.loan-subsequent-default",
        ],
    },
    {
        "module_id": "profile.advertising",
        "kind": "grounding_profile",
        "description": "광고 상대방과 허용되는 과장·허위의 경계",
        "emits": ["fraud_deception_satisfied", "fraud_not_established"],
        "card_ids": [
            "deception.fraud.definition.deceived-person-unspecified",
            "deception.fraud.standard.advertising-important-concrete-falsehood",
            "deception.fraud.standard.advertising-tolerable-exaggeration",
        ],
    },
    {
        "module_id": "profile.omission",
        "kind": "grounding_profile",
        "description": "기존 착오 이용, 고지의무 및 부작위 처분행위",
        "emits": [
            "fraud_deception_satisfied",
            "fraud_disposition_satisfied",
            "fraud_not_established",
        ],
        "card_ids": [
            "deception.fraud.definition.exploitation-existing-mistake",
            "deception.fraud.definition.notice-duty-violation-omission",
            "deception.fraud.element.omission-deception-guarantor-equivalence",
            "deception.fraud.element.omission-deception-independent-error",
            "deception.fraud.element.omission-deception-legal-notice-duty",
            "deception.fraud.standard.precedent-notice-duty-materiality",
            "fraud_mistake.conscious_nonexercise",
            "fraud_mistake.disposition_omission",
            "fraud_mistake.omission_not_all_nonclaims",
        ],
    },
    {
        "module_id": "profile.implicit_deception",
        "kind": "grounding_profile",
        "description": "행동·태도의 설명가치에 의한 묵시적 기망과 부작위 기망의 구별",
        "emits": ["fraud_deception_satisfied"],
        "card_ids": [
            "deception.fraud.definition.implicit-deception",
            "deception.fraud.standard.implicit-deception-explanatory-value",
            "deception.fraud.standard.implicit-omission-deception-distinction",
        ],
    },
    {
        "module_id": "profile.rights_exercise",
        "kind": "grounding_profile",
        "description": "권리행사에 사용된 기망수단의 사회통념상 허용 범위",
        "emits": ["fraud_deception_satisfied", "fraud_not_established"],
        "card_ids": [
            "fraud_damage_acquisition.right_exercise_unacceptable_deception",
            "special_forms.fraud.standard.right-exercise-socially-acceptable-no-crime",
        ],
    },
    {
        "module_id": "structure.triangular",
        "kind": "structural_profile",
        "description": "피기망자·처분자와 재산소유자가 다른 삼각사기 역할 구조",
        "emits": ["fraud_role_structure_satisfied"],
        "card_ids": [
            "deception.fraud.definition.deceived-person-victim-distinct",
            "fraud_mistake.triangular_fraud_definition",
            "mistake_disposition.fraud.variant-triangular-fraud-94do1575-"
            "factual-position-interpretation",
        ],
    },
    {
        "module_id": "structure.third_party_acquisition",
        "kind": "structural_profile",
        "description": "제3자 취득을 피고인에게 귀속하는 의사·도구·대리 관계",
        "emits": ["fraud_beneficiary_attribution_satisfied"],
        "card_ids": ["fraud_intent.third_party_acquisition"],
    },
    {
        "module_id": "boundary.other_offenses",
        "kind": "boundary_adapter",
        "description": "처분능력·직접성·점유에 따른 절도 및 횡령과의 죄명 경계",
        "emits": ["fraud_not_established"],
        "card_ids": [
            "fraud_mistake.no_capacity_theft",
            "fraud_mistake.trick_theft_directness",
            "general_object.fraud.standard.own-possession-other-property-embezzlement",
        ],
    },
    {
        "module_id": "object.property_delivery",
        "kind": "object_adapter",
        "description": "타인의 재물, 교부, 사실상 지배 및 금원 편취액",
        "emits": [
            "fraud_object_satisfied",
            "fraud_acquisition_satisfied",
            "fraud_not_established",
        ],
        "card_ids": [
            "fraud_damage_acquisition.delivery_factual_control",
            "fraud_damage_acquisition.delivery_of_property",
            "fraud_damage_acquisition.money_delivery_full_amount",
            "fraud_damage_acquisition.subsequent_return_irrelevant",
            "general_object.fraud.element.object-other-possessed-other-property",
            "general_object.fraud.standard.own-property-not-object",
        ],
    },
    {
        "module_id": "object.property_benefit",
        "kind": "object_adapter",
        "description": "재물 외 구체적 재산상 이익과 그 취득·처분 형태",
        "emits": ["fraud_object_satisfied", "fraud_acquisition_satisfied"],
        "card_ids": [
            "fraud_damage_acquisition.property_concept_reported_precedent",
            "fraud_damage_acquisition.property_disposition_types",
            "fraud_damage_acquisition.protected_economic_interest",
            "general_object.fraud.definition.property-benefit",
            "general_object.fraud.definition.property-benefit-not-numerically-limited",
            "general_object.fraud.element.property-benefit-concrete",
        ],
    },
    {
        "module_id": "object.public_interest",
        "kind": "object_adapter",
        "description": "공공적 법익 침해를 재산권 침해와 동일하게 평가할 수 있는지의 경계",
        "emits": ["fraud_object_satisfied", "fraud_not_established"],
        "card_ids": [
            "general_object.fraud.exception.public-interest-property-equivalence",
            "general_object.fraud.standard.public-interest-only-no-fraud",
        ],
    },
    {
        "module_id": "stage.attempt_completion",
        "kind": "stage_module",
        "description": "실행의 착수, 인과관계 단절에 따른 미수, 기수 및 사후사정",
        "emits": [
            "fraud_completion_satisfied",
            "fraud_no_separate_loss_gate",
            "fraud_not_established",
        ],
        "card_ids": [
            "fraud_damage_acquisition.property_loss_negative_view",
            "fraud_general_object.causation_required",
            "fraud_general_object.deception_error_causation",
            "fraud_stages_participation.attempt_deceptive_act",
            "fraud_stages_participation.completion_deception_disposition_transfer",
            "fraud_stages_participation.no_causation_attempt",
            "fraud_stages_participation.property_fraud_completion_control",
            "general_object.fraud.standard.later-cancellation-no-effect",
        ],
    },
]


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


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def build_module_ownership(aggregate: dict[str, Any]) -> dict[str, Any]:
    expected = {card["id"] for card in aggregate["cards"]}
    owners: dict[str, str] = {}
    duplicates: set[str] = set()
    for spec in MODULE_SPECS:
        for card_id in spec["card_ids"]:
            if card_id in owners:
                duplicates.add(card_id)
            owners[card_id] = spec["module_id"]
    missing = expected - set(owners)
    unknown = set(owners) - expected
    if missing or unknown or duplicates:
        raise ValueError(
            "Invalid module ownership: "
            f"missing={sorted(missing)}, unknown={sorted(unknown)}, "
            f"duplicates={sorted(duplicates)}"
        )

    modules = []
    for spec in MODULE_SPECS:
        modules.append(
            {
                **spec,
                "card_ids": sorted(spec["card_ids"]),
                "card_count": len(spec["card_ids"]),
            }
        )
    return {
        "version": "1.0.0",
        "rule_set_id": "kr.fraud.article347.full.v1_candidate",
        "status": "draft_human_review_pending",
        "architecture": {
            "final_core_rule": "fraud.core.outcome.established",
            "principle": (
                "유형별 profile과 adapter가 canonical interface를 채우고, "
                "공통 core는 세부 유형을 알지 않은 채 interface만 AND 결합한다."
            ),
            "routing_semantics": (
                "관련 없는 module은 relation을 만들지 않는다. 관련되지만 자료가 "
                "부족한 쟁점만 unknown으로 명시한다."
            ),
            "physical_layout": (
                "현재는 단일 RuleIR 안의 논리 모듈이다. 사용자·Sol 검수 후 Scallop "
                "import 경계를 확정하면서 물리 파일 분리를 검토한다."
            ),
        },
        "canonical_interfaces": {
            "fraud_object_satisfied": "객체 adapter의 공통 출력",
            "fraud_deception_satisfied": "기망 core/profile의 공통 출력",
            "fraud_mistake_satisfied": "착오 core의 공통 출력",
            "fraud_disposition_satisfied": "처분 core/profile의 공통 출력",
            "fraud_acquisition_satisfied": "취득 adapter의 공통 출력",
            "fraud_causal_chain_satisfied": "순차적 인과관계 core의 공통 출력",
            "fraud_intent_satisfied": "주관적 요건 core/profile의 공통 출력",
            "fraud_role_structure_satisfied": "일반형·삼각사기 구조 adapter의 출력",
            "fraud_beneficiary_attribution_satisfied": "본인·제3자 취득 귀속 adapter의 출력",
            "fraud_completion_satisfied": "미수·기수 module의 공통 출력",
            "fraud_no_separate_loss_gate": "별도 현실손해를 중복 요구하지 않는 출력",
        },
        "modules": modules,
        "card_ownership": dict(sorted(owners.items())),
        "coverage": {
            "expected_cards": len(expected),
            "owned_cards": len(owners),
            "duplicate_cards": 0,
            "missing_cards": 0,
        },
    }


def module_id_for_card(card_id: str) -> str:
    for spec in MODULE_SPECS:
        if card_id in spec["card_ids"]:
            return spec["module_id"]
    raise KeyError(f"No module owns {card_id}")


def module_slug(module_id: str) -> str:
    return module_id.replace(".", "_")


def card_slug(card_id: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", card_id.lower()).strip("_")


def input_id(card_id: str) -> str:
    return f"assess_{card_slug(card_id)}"


def condition_id(card_id: str) -> str:
    return f"satisfied_{card_slug(card_id)}"


def actor_variables(
    *,
    owner: str = "property_owner_id",
    beneficiary: str = "beneficiary_id",
) -> list[dict[str, str]]:
    return [
        variable("case_id"),
        variable("defendant_id"),
        variable("deceived_person_id"),
        variable("deceived_person_id"),
        variable(owner),
        variable("subject_id"),
        variable(beneficiary),
    ]


def generic_actor_variables() -> list[dict[str, str]]:
    return [variable(name) for name, _ in ACTOR_ARGUMENTS]


def assessment_atom(
    card_id: str,
    status: str,
    assessment_variable: str,
    actors: list[dict[str, str]],
) -> dict[str, Any]:
    return atom(
        input_id(card_id),
        actors[0],
        variable(assessment_variable),
        *actors[1:],
        string(status),
    )


def condition_atom(
    card_id: str, actors: list[dict[str, str]]
) -> dict[str, Any]:
    return atom(condition_id(card_id), *actors)


def cards_for(
    card_ids: list[str] | set[str], cards_by_id: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    return [cards_by_id[card_id] for card_id in card_ids]


def build_rule_ir(aggregate: dict[str, Any]) -> dict[str, Any]:
    cards = aggregate["cards"]
    cards_by_id = {card["id"]: card for card in cards}
    if len(cards_by_id) != 88:
        raise ValueError("Expected 88 unique approved cards")
    build_module_ownership(aggregate)
    unknown_bars = BAR_CARD_IDS - set(cards_by_id)
    unknown_mandatory = MANDATORY_POSITIVE_CARD_IDS - set(cards_by_id)
    unknown_components = {
        card_id
        for card_ids in COMPONENT_SOURCES.values()
        for card_id in card_ids
        if card_id not in cards_by_id
    }
    if unknown_bars or unknown_mandatory or unknown_components:
        raise ValueError(
            f"Unknown mappings: bars={unknown_bars}, mandatory={unknown_mandatory}, "
            f"components={unknown_components}"
        )

    predicates: list[dict[str, Any]] = [
        predicate(
            "provable",
            [("case_id", "String"), ("assessment_id", "String")],
            kind="rule",
            role="input",
            origin="system",
            definition="해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음",
        )
    ]
    rules: list[dict[str, Any]] = []
    actors = generic_actor_variables()

    for index, card in enumerate(cards, 1):
        card_id = card["id"]
        input_kind = (
            "standard" if card["formalization"] == "standard_input" else "rule"
        )
        if input_kind == "standard":
            input_definition = (
                "현재 사건 사실에 다음 개방형 법적 기준을 적용한 명시적 3상태 평가: "
                f"{card['proposition']}"
            )
        else:
            input_definition = (
                "다음 결정규칙을 적용하는 데 필요한 사건의 구조화된 사실적 전제가 "
                f"충족되는지에 대한 명시적 3상태 rule fact: {card['proposition']}"
            )
        predicates.append(
            predicate(
                input_id(card_id),
                ASSESSMENT_ARGUMENTS,
                kind=input_kind,
                role="input",
                origin="commentary",
                definition=input_definition,
                cards=[card],
            )
        )
        predicates.append(
            predicate(
                condition_id(card_id),
                ACTOR_ARGUMENTS,
                kind="rule",
                role="derived",
                origin="commentary",
                definition=f"증명 가능한 평가에서 다음 조건이 충족됨: {card['proposition']}",
                cards=[card],
            )
        )
        assessment = f"assessment_{index:03d}"
        rules.append(
            rule(
                (
                    f"fraud.{module_slug(module_id_for_card(card_id))}."
                    f"card.{index:03d}.satisfied"
                ),
                condition_atom(card_id, actors),
                [
                    assessment_atom(card_id, "satisfied", assessment, actors),
                    atom("provable", actors[0], variable(assessment)),
                ],
                [card],
                "이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다.",
            )
        )

    for component_id, source_ids in COMPONENT_SOURCES.items():
        predicates.append(
            predicate(
                component_id,
                ACTOR_ARGUMENTS,
                kind="rule",
                role="derived",
                origin="commentary",
                definition=COMPONENT_DEFINITIONS[component_id],
                cards=cards_for(source_ids, cards_by_id),
            )
        )
        for branch_index, card_id in enumerate(source_ids, 1):
            owner = module_slug(module_id_for_card(card_id))
            rules.append(
                rule(
                    f"fraud.{owner}.component.{component_id}.{branch_index:02d}",
                    atom(component_id, *actors),
                    [condition_atom(card_id, actors)],
                    [cards_by_id[card_id]],
                    "해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다.",
                )
            )

    omission_ids = [
        "deception.fraud.element.omission-deception-guarantor-equivalence",
        "deception.fraud.element.omission-deception-independent-error",
        "deception.fraud.element.omission-deception-legal-notice-duty",
    ]
    rules.append(
        rule(
            "fraud.profile_omission.component.fraud_deception_satisfied",
            atom("fraud_deception_satisfied", *actors),
            [condition_atom(card_id, actors) for card_id in omission_ids],
            cards_for(omission_ids, cards_by_id),
            "부작위 기망은 보증인적 지위·독립 착오·법률상 고지의무가 함께 확인된 경로다.",
        )
    )

    object_benefit_ids = [
        "general_object.fraud.definition.property-benefit",
        "general_object.fraud.element.property-benefit-concrete",
    ]
    rules.append(
        rule(
            "fraud.object_property_benefit.component.fraud_object_satisfied",
            atom("fraud_object_satisfied", *actors),
            [condition_atom(card_id, actors) for card_id in object_benefit_ids],
            cards_for(object_benefit_ids, cards_by_id),
            "재물 외 재산상 이익 branch는 경제적 가치 증가와 구체성을 함께 요구한다.",
        )
    )

    intent_ids = [
        "fraud_intent.contract_breach_distinction",
        "fraud_mistake.gain_purpose",
    ]
    predicates.append(
        predicate(
            "fraud_intent_satisfied",
            ACTOR_ARGUMENTS,
            kind="rule",
            role="derived",
            origin="commentary",
            definition=COMPONENT_DEFINITIONS["fraud_intent_satisfied"],
            cards=cards_for(intent_ids, cards_by_id),
        )
    )
    rules.append(
        rule(
            "fraud.core_intent.component.fraud_intent_satisfied",
            atom("fraud_intent_satisfied", *actors),
            [condition_atom(card_id, actors) for card_id in intent_ids],
            cards_for(intent_ids, cards_by_id),
            "단순 채무불이행과 구별되는 고의의 기망 및 재산적 이득 목적을 함께 요구한다.",
        )
    )
    loan_intent_ids = [
        "deception.fraud.standard.intent-to-defraud-loan-inference",
        "fraud_mistake.gain_purpose",
    ]
    rules.append(
        rule(
            "fraud.profile_loan.component.fraud_intent_satisfied",
            atom("fraud_intent_satisfied", *actors),
            [condition_atom(card_id, actors) for card_id in loan_intent_ids],
            cards_for(loan_intent_ids, cards_by_id),
            "차용금 사건에서는 객관적 사정으로 추론한 편취 범의와 재산적 이득 목적을 결합한다.",
        )
    )

    no_loss_card = cards_by_id[
        "fraud_damage_acquisition.property_loss_negative_view"
    ]
    predicates.append(
        predicate(
            "fraud_no_separate_loss_gate",
            ACTOR_ARGUMENTS,
            kind="rule",
            role="derived",
            origin="commentary",
            definition=COMPONENT_DEFINITIONS["fraud_no_separate_loss_gate"],
            cards=[no_loss_card],
        )
    )
    rules.append(
        rule(
            "fraud.stage_attempt_completion.component.no_separate_loss_gate",
            atom("fraud_no_separate_loss_gate", *actors),
            [atom("fraud_acquisition_satisfied", *actors)],
            [no_loss_card],
            "취득이 인정되면 현실적 손해를 별도 입력 gate로 다시 요구하지 않는다.",
        )
    )

    not_established_cards = cards_for(
        BAR_CARD_IDS | MANDATORY_POSITIVE_CARD_IDS, cards_by_id
    )
    predicates.extend(
        [
            predicate(
                "fraud_established",
                ACTOR_ARGUMENTS,
                kind="rule",
                role="derived",
                origin="commentary",
                definition="승인된 사기죄 core 구성요건과 역할·인과·기수 조건이 모두 충족됨",
                cards=cards_for(
                    {
                        "deception.fraud.causal-link.deception-property-disposition",
                        "fraud_damage_acquisition.property_loss_negative_view",
                        "fraud_intent.contract_breach_distinction",
                        "fraud_mistake.deceived_disposer_identity",
                        "fraud_mistake.disposition_definition",
                        "fraud_mistake.error_definition",
                        "fraud_mistake.gain_purpose",
                        "fraud_mistake.property_disposition_element",
                        "fraud_mistake.sequential_causation",
                        "fraud_stages_participation.completion_deception_disposition_transfer",
                        "general_object.fraud.element.object-other-possessed-other-property",
                    },
                    cards_by_id,
                ),
            ),
            predicate(
                "fraud_not_established",
                [
                    ("case_id", "String"),
                    ("defendant_id", "String"),
                    ("issue_id", "String"),
                ],
                kind="rule",
                role="derived",
                origin="commentary",
                definition="명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함",
                cards=not_established_cards,
            ),
            predicate(
                "fraud_undetermined",
                [
                    ("case_id", "String"),
                    ("defendant_id", "String"),
                    ("issue_id", "String"),
                ],
                kind="rule",
                role="derived",
                origin="commentary",
                definition="관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음",
                cards=cards,
            ),
            predicate(
                "fraud_conflict",
                [
                    ("case_id", "String"),
                    ("defendant_id", "String"),
                    ("issue_id", "String"),
                ],
                kind="rule",
                role="derived",
                origin="commentary",
                definition="같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨",
                cards=cards,
            ),
        ]
    )

    for index, card in enumerate(cards, 1):
        card_id = card["id"]
        owner = module_slug(module_id_for_card(card_id))
        assessment = f"unknown_assessment_{index:03d}"
        rules.append(
            rule(
                f"fraud.{owner}.card.{index:03d}.undetermined",
                atom(
                    "fraud_undetermined",
                    actors[0],
                    actors[1],
                    string(card_id),
                ),
                [
                    assessment_atom(card_id, "unknown", assessment, actors),
                    atom("provable", actors[0], variable(assessment)),
                ],
                [card],
                "관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다.",
            )
        )
        positive_assessment = f"positive_assessment_{index:03d}"
        negative_assessment = f"negative_assessment_{index:03d}"
        rules.append(
            rule(
                f"fraud.{owner}.card.{index:03d}.conflict",
                atom(
                    "fraud_conflict",
                    actors[0],
                    actors[1],
                    string(card_id),
                ),
                [
                    assessment_atom(
                        card_id, "satisfied", positive_assessment, actors
                    ),
                    atom("provable", actors[0], variable(positive_assessment)),
                    assessment_atom(
                        card_id, "not_satisfied", negative_assessment, actors
                    ),
                    atom("provable", actors[0], variable(negative_assessment)),
                ],
                [card],
                "상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다.",
            )
        )

    for index, card_id in enumerate(sorted(BAR_CARD_IDS), 1):
        card = cards_by_id[card_id]
        owner = module_slug(module_id_for_card(card_id))
        rules.append(
            rule(
                f"fraud.{owner}.bar.{index:03d}",
                atom(
                    "fraud_not_established",
                    actors[0],
                    actors[1],
                    string(card_id),
                ),
                [condition_atom(card_id, actors)],
                [card],
                "이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 사기죄 성립을 부정한다.",
            )
        )

    for index, card_id in enumerate(sorted(MANDATORY_POSITIVE_CARD_IDS), 1):
        card = cards_by_id[card_id]
        owner = module_slug(module_id_for_card(card_id))
        assessment = f"mandatory_negative_{index:03d}"
        rules.append(
            rule(
                f"fraud.{owner}.mandatory_negative.{index:03d}",
                atom(
                    "fraud_not_established",
                    actors[0],
                    actors[1],
                    string(card_id),
                ),
                [
                    assessment_atom(
                        card_id, "not_satisfied", assessment, actors
                    ),
                    atom("provable", actors[0], variable(assessment)),
                ],
                [card],
                "필수 core 요건이 명시적으로 not_satisfied이면 불성립 사유를 도출한다.",
            )
        )

    role_card_ids = {
        "fraud_mistake.deceived_disposer_identity",
        "deception.fraud.definition.deceived-person-victim-distinct",
        "fraud_mistake.triangular_fraud_definition",
        "mistake_disposition.fraud.variant-triangular-fraud-94do1575-"
        "factual-position-interpretation",
    }
    beneficiary_card_ids = set(intent_ids) | set(
        COMPONENT_SOURCES["fraud_third_party_acquisition_satisfied"]
    )
    predicates.extend(
        [
            predicate(
                "fraud_role_structure_satisfied",
                ACTOR_ARGUMENTS,
                kind="rule",
                role="derived",
                origin="commentary",
                definition=COMPONENT_DEFINITIONS["fraud_role_structure_satisfied"],
                cards=cards_for(role_card_ids, cards_by_id),
            ),
            predicate(
                "fraud_beneficiary_attribution_satisfied",
                ACTOR_ARGUMENTS,
                kind="rule",
                role="derived",
                origin="commentary",
                definition=COMPONENT_DEFINITIONS[
                    "fraud_beneficiary_attribution_satisfied"
                ],
                cards=cards_for(beneficiary_card_ids, cards_by_id),
            ),
        ]
    )

    ordinary_actors = actor_variables(owner="deceived_person_id")
    rules.append(
        rule(
            "fraud.structure_ordinary.role_structure",
            atom("fraud_role_structure_satisfied", *ordinary_actors),
            [
                atom(
                    "fraud_deceived_disposer_identity_satisfied",
                    *ordinary_actors,
                )
            ],
            [cards_by_id["fraud_mistake.deceived_disposer_identity"]],
            "일반형은 피기망자·처분자·재산소유자에 같은 entity ID를 사용한다.",
        )
    )

    triangular_actors = actor_variables()
    triangular_required_ids = {
        "fraud_mistake.deceived_disposer_identity",
        "fraud_mistake.triangular_fraud_definition",
        "mistake_disposition.fraud.variant-triangular-fraud-94do1575-"
        "factual-position-interpretation",
    }
    rules.append(
        rule(
            "fraud.structure_triangular.role_structure",
            atom("fraud_role_structure_satisfied", *triangular_actors),
            [
                atom(
                    "fraud_deceived_disposer_identity_satisfied",
                    *triangular_actors,
                ),
                condition_atom(
                    "fraud_mistake.triangular_fraud_definition",
                    triangular_actors,
                ),
                atom("fraud_triangular_authority_satisfied", *triangular_actors),
            ],
            cards_for(triangular_required_ids, cards_by_id),
            (
                "삼각사기는 피기망자=처분자를 유지하면서 별도 재산소유자와 그 재산을 "
                "처분할 권능 또는 지위를 요구한다."
            ),
        )
    )

    self_acquisition_actors = actor_variables(beneficiary="defendant_id")
    rules.append(
        rule(
            "fraud.structure_self_acquisition.beneficiary_attribution",
            atom(
                "fraud_beneficiary_attribution_satisfied",
                *self_acquisition_actors,
            ),
            [atom("fraud_intent_satisfied", *self_acquisition_actors)],
            cards_for(intent_ids, cards_by_id),
            "피고인과 수익자에 같은 entity ID를 쓰는 본인취득 경로다.",
        )
    )

    third_party_actors = actor_variables()
    rules.append(
        rule(
            "fraud.structure_third_party_acquisition.beneficiary_attribution",
            atom(
                "fraud_beneficiary_attribution_satisfied",
                *third_party_actors,
            ),
            [
                atom(
                    "fraud_third_party_acquisition_satisfied",
                    *third_party_actors,
                )
            ],
            cards_for(
                COMPONENT_SOURCES["fraud_third_party_acquisition_satisfied"],
                cards_by_id,
            ),
            "제3자취득은 도구·대리 관계 또는 제3자 취득 의사를 별도 귀속 gate로 요구한다.",
        )
    )

    core_component_ids = [
        "fraud_object_satisfied",
        "fraud_deception_satisfied",
        "fraud_mistake_satisfied",
        "fraud_disposition_satisfied",
        "fraud_acquisition_satisfied",
        "fraud_causal_chain_satisfied",
        "fraud_completion_satisfied",
        "fraud_intent_satisfied",
        "fraud_no_separate_loss_gate",
        "fraud_role_structure_satisfied",
        "fraud_beneficiary_attribution_satisfied",
    ]
    final_base_card_ids = {
        card_id
        for component_id in core_component_ids
        for card_id in (
            COMPONENT_SOURCES.get(component_id, [])
            if component_id not in {
                "fraud_intent_satisfied",
                "fraud_no_separate_loss_gate",
                "fraud_role_structure_satisfied",
                "fraud_beneficiary_attribution_satisfied",
            }
            else []
        )
    } | set(intent_ids) | {no_loss_card["id"]} | role_card_ids | beneficiary_card_ids

    final_actors = actor_variables()
    rules.append(
        rule(
            "fraud.core.outcome.established",
            atom("fraud_established", *final_actors),
            [atom(component_id, *final_actors) for component_id in core_component_ids],
            cards_for(final_base_card_ids, cards_by_id),
            (
                "공통 core는 세부 사기유형을 직접 분기하지 않는다. profile과 adapter가 "
                "채운 canonical component, 역할 구조 및 수익 귀속 interface만 AND 결합한다."
            ),
        )
    )

    conflict_actors = generic_actor_variables()
    rules.append(
        rule(
            "fraud.core.outcome.conflict.established_and_not_established",
            atom(
                "fraud_conflict",
                conflict_actors[0],
                conflict_actors[1],
                string("established_and_not_established"),
            ),
            [
                atom("fraud_established", *conflict_actors),
                atom(
                    "fraud_not_established",
                    conflict_actors[0],
                    conflict_actors[1],
                    variable("negative_issue_id"),
                ),
            ],
            cards,
            "최종 성립과 명시적 불성립 사유가 함께 도출되면 상위 conflict를 노출한다.",
        )
    )

    return {
        "version": "1.1.0",
        "rule_set_id": "kr.fraud.article347.full.v1_candidate",
        "issue_tag": "fraud",
        "status": "draft",
        "legal_review": "pending",
        "source_scope": aggregate["source_scope"],
        "norm_card_scope": {
            "card_set_id": aggregate["card_set_id"],
            "card_ids": sorted(cards_by_id),
        },
        "predicates": predicates,
        "rules": rules,
        "legal_review_questions": [
            "불법영득의사 standard를 재물 편취의 특정 branch에 추가로 강제할 범위를 검토해야 한다.",
            "불성립 output에서 사기미수·절도·횡령·정당행위를 별도 후속 죄명 predicate로 분리할지 검토해야 한다.",
            "모든 assessment에 공통 actor tuple을 쓰는 현재 interface를 runtime extraction에서 더 좁힐지 검토해야 한다.",
        ],
        "coverage_gaps": [
            "사용자가 RAG/future work로 분리한 558개 구체 판례·학설·형법총칙 쟁점은 포함하지 않는다.",
            "정보통신망법 등 수집 중인 특별법과 형법총칙의 죄수·공범·미필적 고의는 별도 rule set이 필요하다.",
        ],
    }


def card_logical_use(card: dict[str, Any], rule_ir: dict[str, Any]) -> str:
    card_id = card["id"]
    uses = ["unknown이면 undetermined", "상반된 두 평가면 conflict"]
    outputs = {
        item["head"]["predicate"]
        for item in rule_ir["rules"]
        if card_id in item["norm_card_ids"]
        and ".card." not in item["id"]
        and item["id"]
        not in {
            "fraud.core.outcome.established",
            "fraud.core.outcome.conflict.established_and_not_established",
        }
    }
    if outputs:
        uses.insert(0, "연결 output: " + ", ".join(sorted(outputs)))
    else:
        uses.insert(0, "개별 쟁점의 증명 가능한 support fact")
    return "; ".join(uses)


def atom_text(value: dict[str, Any]) -> str:
    arguments = ", ".join(str(arg["value"]) for arg in value["arguments"])
    return f"{value['predicate']}({arguments})"


def build_explanation(rule_ir: dict[str, Any], aggregate: dict[str, Any]) -> str:
    predicate_defs = {item["id"]: item for item in rule_ir["predicates"]}
    module_ownership = build_module_ownership(aggregate)
    owner_by_card = module_ownership["card_ownership"]
    lines = [
        "# 사기죄 전체 RuleIR 자연어 설명",
        "",
        "## 먼저 읽을 결론",
        "",
        "이 RuleIR은 사실관계를 곧바로 유죄·무죄 문장으로 생성하지 않는다. neural/RAG "
        "단계가 승인된 88개 NormCard별로 사건의 긍정사실, 반대사실, 미확인사실과 근거를 "
        "평가하고, Scallop은 그중 `provable`을 통과한 평가만 결합한다.",
        "",
        "역할 인자는 법적 기능을 분리하기 위한 슬롯이다. 서로 다른 사람이라는 뜻이 "
        "아니므로 동일인이 여러 역할을 맡으면 같은 entity ID를 쓴다. 모든 성립 rule에서 "
        "피기망자와 처분자는 같은 변수다. 일반형은 재산소유자도 같은 변수이고, 삼각사기는 "
        "재산소유자를 별도 변수로 두면서 처분 권능 또는 지위를 추가로 요구한다.",
        "",
        "## 런타임 입력",
        "",
        "각 `assess_*` predicate는 `(case_id, assessment_id, defendant_id, "
        "deceived_person_id, disposer_id, property_owner_id, subject_id, beneficiary_id, "
        "status)`를 받는다. `status`는 `satisfied`, `not_satisfied`, `unknown`뿐이다. "
        "모델이 사실을 찾지 못했다는 이유로 `not_satisfied`를 만들면 안 된다.",
        "",
        "60개 `kind=standard` 입력은 기망의 신의칙 위반, 고의, 인과의 실질성처럼 "
        "개방형 법적 기준을 사건에 적용한 판단이다. 28개 `kind=rule` 입력은 모델이 법적 "
        "결론을 대신 내리는 것이 아니라 동일인 여부, 이전·지배취득, 순서 같은 결정규칙의 "
        "사실적 전제를 구조화한 rule fact다.",
        "",
        "88개 relation을 모든 사건에 전부 생성하지 않는다. 사건 유형 routing에서 관련 "
        "없는 카드는 relation을 만들지 않는다. 관련 쟁점이지만 자료가 부족할 때만 "
        "`unknown` 행을 명시적으로 만들며, relation 부재는 false도 unknown도 아니다.",
        "",
        "모든 substantive 경로는 같은 사건과 평가 ID의 `provable(case_id, "
        "assessment_id)`를 요구한다. 따라서 증거능력·신빙성 검토를 통과하지 않은 진술은 "
        "구성요건 판단에 들어가지 않는다.",
        "",
        "## 모듈 구조",
        "",
        "각 NormCard에는 하나의 주 소유 모듈만 있다. 차용금·광고·부작위·묵시적 기망·"
        "권리행사는 grounding profile, 삼각사기·제3자취득은 structural profile, 객체·"
        "죄명 경계·미수/기수는 adapter 또는 stage module로 분리했다.",
        "",
        "profile과 adapter는 `fraud_deception_satisfied`, `fraud_role_structure_satisfied` "
        "같은 canonical interface만 출력한다. 최종 core는 차용금이나 삼각사기 같은 세부 "
        "유형명을 알지 않고 이 interface들을 한 번만 AND 결합한다. 현재는 검수를 위해 "
        "하나의 RuleIR 파일 안에서 논리적으로 분리했으며, Scallop 물리 파일 분리는 "
        "Sol·사용자 검수 뒤에 확정한다.",
        "",
    ]
    for module in module_ownership["modules"]:
        lines.append(
            f"- `{module['module_id']}` (`{module['kind']}`, {module['card_count']}장): "
            f"{module['description']}"
        )
    lines.extend(
        [
            "",
            "## 최종 성립의 AND gate와 손해 불요 규칙",
        "",
        "최종 성립은 1번부터 10번까지의 사실·법적 component가 모두 있어야 한다. 11번은 "
        "별도 사실요건이 아니라 취득 component에서 자동으로 파생되는 compilation 규칙이다.",
        "",
        "1. 사기죄의 객체인 타인의 재물 또는 구체적 재산상 이익",
        "2. 신의칙에 반하여 착오를 일으키는 기망 또는 승인된 구체 유형의 기망",
        "3. 사실과 다른 인식인 착오",
        "4. 착오에 기한 재산적 처분행위",
        "5. 재물 교부 또는 재산상 이익 취득",
        "6. 기망·착오·처분·취득의 순차적 인과관계",
        "7. 단순 채무불이행과 구별되는 고의의 기망 및 재산적 이득 목적",
        "8. 미수를 넘어선 이전 또는 사실상 지배 취득",
        "9. 피기망자=처분자를 포함한 일반형 또는 삼각사기의 역할 구조",
        "10. 본인취득 또는 제3자취득의 피고인 귀속 구조",
        "11. 취득 외에 현실적 재산상 손해를 별도 gate로 중복 요구하지 않는 판례 기준",
        "",
        "불법영득의사 평가는 별도 support predicate로 보존하지만 모든 사기 유형의 공통 "
        "AND gate로 강제하지 않았다. 이는 사용자가 앞서 정한 실무지향 정책을 반영한다.",
        "",
        "## 역할·취득 adapter와 단일 최종 규칙",
        "",
        "- 일반형 역할 adapter: 피기망자=처분자=재산소유자",
        "- 삼각사기 역할 adapter: 피기망자=처분자, 별도 재산소유자, 처분 권능·지위",
        "- 본인취득 귀속 adapter: 수익자=피고인",
        "- 제3자취득 귀속 adapter: 제3자의 도구·대리 관계 또는 제3자 취득 의사",
        "",
        "위 두 축은 독립적으로 canonical relation을 만든다. `fraud.core.outcome.established` "
        "하나가 나머지 구성요건과 두 relation을 결합하므로 네 조합을 최종 core에 반복하지 않는다.",
        "",
        "## 부정·미확인·충돌",
        "",
        "명시적 불성립 카드가 satisfied이거나 필수 positive 카드가 not_satisfied이면 "
        "`fraud_not_established`가 쟁점 ID와 함께 나온다. 관련 평가가 unknown이면 "
        "`fraud_undetermined`, 같은 카드에 satisfied와 not_satisfied가 모두 provable이면 "
        "`fraud_conflict`가 나온다. 부재를 부정으로 간주하는 negation은 사용하지 않는다.",
        "",
        "`fraud_established`와 `fraud_not_established`가 동시에 나오면 "
        "`fraud_conflict(..., established_and_not_established)`도 도출한다. 후속 long-form "
        "generator는 conflict와 undetermined를 먼저 해소하거나 양측 논거로 표시해야 하며, "
        "established만 선택해 유죄 결론을 써서는 안 된다.",
        "",
        "## 88개 입력의 의미와 논리적 사용",
        "",
        "| No. | NormCard | 소유 모듈 | 형식 | 극성 | 논리적 사용 |",
            "|---:|---|---|---|---|---|",
        ]
    )
    for index, card in enumerate(aggregate["cards"], 1):
        lines.append(
            f"| {index} | `{card['id']}`<br>{card['proposition']} | "
            f"`{owner_by_card[card['id']]}` | "
            f"`{card['formalization']}` | `{card['polarity']}` | "
            f"{card_logical_use(card, rule_ir)} |"
        )

    lines.extend(
        [
            "",
            "## Rule별 자연어 해설",
            "",
            "아래 목록은 모든 rule의 head와 body를 빠짐없이 펼친 것이다. body의 각 항목이 "
            "모두 참일 때만 head가 도출된다.",
            "",
        ]
    )
    for item in rule_ir["rules"]:
        head = item["head"]
        head_definition = predicate_defs[head["predicate"]]["definition"]
        lines.extend(
            [
                f"### `{item['id']}`",
                "",
                f"결론: **{head_definition}** (`{atom_text(head)}`)",
                "",
                "필요조건:",
                "",
            ]
        )
        for body_atom in item["body"]:
            definition = predicate_defs[body_atom["predicate"]]["definition"]
            lines.append(f"- {definition} (`{atom_text(body_atom)}`)")
        lines.extend(
            [
                "",
                "근거 NormCard: "
                + ", ".join(f"`{card_id}`" for card_id in item["norm_card_ids"]),
                "",
                f"해석 메모: {item['review_notes']}",
                "",
            ]
        )

    lines.extend(
        [
            "## RAG와의 경계",
            "",
            "이 RuleIR은 558개 구체 판례·희귀 유형을 실행 rule로 복제하지 않는다. 사건이 "
            "소송사기, 보험사기, 특정 거래관행처럼 세부 적용례를 요구하면 RAG가 관련 판례를 "
            "검색하고, 그 판례를 근거로 현재 사건의 `assess_*` 값을 만든다. 검색된 판례의 "
            "결론 자체를 Scallop fact로 넣어서는 안 된다.",
            "",
            "## 사람이 중점적으로 볼 세 항목",
            "",
            "1. 불법영득의사를 특정 재물 편취 branch에만 추가할 범위",
            "2. 불성립 결과를 사기미수·절도·횡령·정당행위로 별도 분기할지",
            "3. 공통 actor tuple을 predicate별 최소 인자로 축소할지",
            "",
        ]
    )
    return "\n".join(lines)


def build_agent_review(rule_ir: dict[str, Any], aggregate: dict[str, Any]) -> str:
    input_predicates = [
        item
        for item in rule_ir["predicates"]
        if item["origin"] == "commentary" and item["role"] == "input"
    ]
    module_ownership = build_module_ownership(aggregate)
    return "\n".join(
        [
            "# 사기죄 full RuleIR 에이전트 검토",
            "",
            "## 판정",
            "",
            "**구조 검증 통과, 사용자 법률 검수 필요.** Terra의 원본 부분 출력은 candidate로 "
            "사용하지 않았고, 승인된 88장만으로 수동·결정적으로 재구성했다.",
            "",
            "## 자동 검증",
            "",
            f"- NormCard scope: {len(rule_ir['norm_card_scope']['card_ids'])}/88",
            f"- commentary input: {len(input_predicates)}개",
            f"- predicate: {len(rule_ir['predicates'])}개",
            f"- rule: {len(rule_ir['rules'])}개",
            "- 모든 input의 provable pairing: 통과",
            "- case variable isolation: 통과",
            "- negation 및 active_policy 부재: 통과",
            "- 피기망자=처분자 성립 head: 통과",
            f"- module ownership: {len(module_ownership['modules'])}개 모듈, 88/88, 중복 0",
            "- 최종 fraud_established rule: 1개",
            "- established/not_established/undetermined/conflict 구현: 통과",
            "",
            "## 법리 검토",
            "",
            "1. 피기망자와 처분행위자는 최종 성립 rule에서 같은 변수다. 역할 슬롯을 "
            "분리했지만 별개의 사람으로 강제하지 않았다.",
            "2. 일반형과 삼각사기는 역할 adapter가 분리한다. 삼각사기는 별도 재산소유자, "
            "삼각사기 관련성 및 94도1575 계열의 처분 권능·지위를 요구한다.",
            "3. 본인취득과 제3자취득은 수익 귀속 adapter가 분리한다. 제3자취득은 의사·"
            "도구·대리 관계를 추가 gate로 요구한다.",
            "4. 현실적 재산상 손해는 재물 교부 또는 이익 취득과 별개의 공통 gate로 두지 "
            "않았다.",
            "5. 불법영득의사 카드는 보존·소비하지만 모든 사기 유형의 최종 공통 gate로 "
            "강제하지 않았다.",
            "6. 사기미수·절도·횡령·정당행위가 문제되는 bar는 현재 fraud_not_established의 "
            "issue_id로 노출한다. 후속 죄명 결론은 아직 만들지 않았다.",
            "7. 차용금·광고·부작위·묵시적 기망·권리행사 기준은 각각 profile 소유다. "
            "공통 core는 이들의 세부 카드 대신 canonical component만 소비한다.",
            "",
            "## 남은 위험",
            "",
            "- 88개 assessment는 한 사건에서 전부 호출한다는 뜻이 아니다. 사건 관련성 "
            "routing 후 필요한 항목만 평가해야 한다.",
            "- deterministic 28개 입력은 법적 standard 판단이 아니라 규칙 antecedent의 "
            "구조화된 rule fact로 추출해야 한다.",
            "- profile router가 관련 모듈을 먼저 골라야 한다. 단순한 정의 카드와 실제 적용 "
            "충족을 혼동하지 않도록 feature schema와 RAG 근거가 필요하다.",
            "- established와 not_established가 동시에 나올 수 있다. long-form 생성 전 conflict "
            "resolution 정책을 반드시 적용해야 한다.",
            "",
        ]
    )


def build_human_guide(rule_ir: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# 사기죄 full RuleIR 사용자 검수 가이드",
            "",
            "검수 순서는 자연어 설명을 먼저 읽고, 필요한 경우 원본 JSON의 rule ID를 "
            "대조하는 방식이 가장 효율적이다.",
            "",
            "1. 15개 모듈의 카드 소유권, 특히 profile과 RAG의 경계가 적절한지",
            "2. 최종 10개 사실·법적 AND gate와 자동 손해불요 규칙이 적절한지",
            "3. 일반형/삼각사기 역할 adapter와 본인/제3자취득 귀속 adapter가 맞는지",
            "4. BAR_CARD_IDS의 각 항목이 일반 불성립인지 특정 profile 불성립인지",
            "5. mandatory positive 10개가 명시적 부정 시 불성립으로 가도 되는지",
            "6. 불법영득의사를 공통 gate에서 제외한 현재 정책이 맞는지",
            "7. 사기미수·절도·횡령·정당행위 output을 지금 분리할지",
            "8. standard assessment의 공통 actor tuple이 실제 feature extraction에 적합한지",
            "",
            f"현재 predicate {len(rule_ir['predicates'])}개, rule {len(rule_ir['rules'])}개다. "
            "사용자 승인 전 Sol과 Scallop compile/runtime은 차단한다.",
            "",
        ]
    )


def main() -> None:
    aggregate = read_json(CORE_SET)
    commentary = {
        row["comment_id"]: row
        for row in read_jsonl(COMMENTARY)
        if row["comment_id"] in set(aggregate["source_scope"]["comment_ids"])
    }
    raw_terra = read_json(RAW_TERRA)
    run_summary = read_json(RUN_SUMMARY)
    rule_ir = build_rule_ir(aggregate)
    module_ownership = build_module_ownership(aggregate)
    validate_full_rule_ir_generation(rule_ir, commentary, aggregate)

    write_json(CANDIDATE, rule_ir)
    write_json(MODULE_OWNERSHIP, module_ownership)
    write_json(TRACKED_TERRA_OUTPUT, raw_terra)
    SCAFFOLD.write_text(
        render_rule_ir_natural_language_scaffold(rule_ir), encoding="utf-8"
    )
    EXPLANATION.write_text(
        build_explanation(rule_ir, aggregate), encoding="utf-8"
    )
    AGENT_REVIEW.write_text(
        build_agent_review(rule_ir, aggregate), encoding="utf-8"
    )
    HUMAN_GUIDE.write_text(build_human_guide(rule_ir), encoding="utf-8")

    terra_audit = {
        "version": "1.0.0",
        "status": "rejected_partial_output",
        "api_calls": run_summary["api_calls"],
        "usage": run_summary["usage"],
        "raw_output_path": str(TRACKED_TERRA_OUTPUT.relative_to(PROJECT_ROOT)),
        "run_raw_output_path": str(RAW_TERRA.relative_to(PROJECT_ROOT)),
        "terra_counts": {
            "norm_cards": len(raw_terra["norm_card_scope"]["card_ids"]),
            "predicates": len(raw_terra["predicates"]),
            "rules": len(raw_terra["rules"]),
        },
        "required_counts": {"norm_cards": 88},
        "validation_errors": run_summary["validation_errors"],
        "substantive_failure": (
            "Terra explicitly emitted only 8 of 88 approved cards and requested separate "
            "translation for the remainder. The raw output was not promoted."
        ),
        "repair_method": "agent-authored deterministic reconstruction; no additional API call",
    }
    write_json(TERRA_AUDIT, terra_audit)
    write_json(
        POST_TERRA_STATUS,
        {
            "version": "1.0.0",
            "status": "agent_review_complete_human_review_pending",
            "terra_api_calls": run_summary["api_calls"],
            "terra_raw_output": "rejected_partial_output",
            "local_contract_validation": "pass",
            "agent_rule_by_rule_review": "complete",
            "agent_natural_language_explanation": "complete",
            "human_rule_ir_review_allowed": True,
            "human_rule_ir_review": "pending",
            "sol_critic_allowed": False,
            "scallop_compile_allowed": False,
            "candidate_path": str(CANDIDATE.relative_to(PROJECT_ROOT)),
            "explanation_path": str(EXPLANATION.relative_to(PROJECT_ROOT)),
            "agent_review_path": str(AGENT_REVIEW.relative_to(PROJECT_ROOT)),
            "module_ownership_path": str(
                MODULE_OWNERSHIP.relative_to(PROJECT_ROOT)
            ),
        },
    )
    print(
        json.dumps(
            {
                "api_calls": run_summary["api_calls"],
                "additional_api_calls": 0,
                "cards": len(rule_ir["norm_card_scope"]["card_ids"]),
                "predicates": len(rule_ir["predicates"]),
                "rules": len(rule_ir["rules"]),
                "modules": len(module_ownership["modules"]),
                "validation": "pass",
                "next_gate": "human_rule_ir_review",
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
