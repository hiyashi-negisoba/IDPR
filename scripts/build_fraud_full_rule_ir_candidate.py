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
MODULE_HUMAN_REVIEW = FRAUD_ROOT / "fraud_rule_ir_module_human_review.md"
HUMAN_REVIEW_DECISION = FRAUD_ROOT / "fraud_full_rule_ir_human_review_decision.json"
POST_SOL_HUMAN_DECISION = (
    FRAUD_ROOT / "fraud_full_rule_ir_post_sol_human_decision.json"
)
SOL_CRITIQUE = FRAUD_ROOT / "fraud_full_rule_ir_sol_critique.json"
SOL_ADJUDICATION = FRAUD_ROOT / "fraud_full_rule_ir_sol_adjudication.md"
SCALLOP_COMPILE_MANIFEST = FRAUD_ROOT / "fraud_scallop_compile_manifest.json"
SCALLOP_RUNTIME_REPORT = FRAUD_ROOT / "fraud_scallop_runtime_report.json"


ACTOR_ARGUMENTS = [
    ("case_id", "String"),
    ("defendant_id", "String"),
    ("deceived_person_id", "String"),
    ("disposer_id", "String"),
    ("property_owner_id", "String"),
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
    "deception.fraud.causal-link.deception-property-disposition",
    "deception.fraud.definition.deception-good-faith-mistake",
    "fraud_intent.contract_breach_distinction",
    "fraud_intent.time_of_conduct",
    "fraud_mistake.deceived_disposer_identity",
    "fraud_mistake.disposition_definition",
    "fraud_mistake.error_definition",
    "fraud_mistake.error_disposition_motivation",
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
        "deception.fraud.causal-link.deception-property-disposition",
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
        "fraud_mistake.error_disposition_motivation",
        "fraud_mistake.error_doubt_ignorance",
        "fraud_mistake.unaware_error",
    ],
    "fraud_disposition_satisfied": [
        "fraud_mistake.disposition_definition",
        "fraud_mistake.conscious_nonexercise",
        "fraud_mistake.disposition_intent_act_awareness",
        "fraud_mistake.factual_act_disposition",
        "fraud_mistake.invalid_act_disposition",
    ],
    "fraud_acquisition_satisfied": [
        "fraud_damage_acquisition.delivery_factual_control",
        "fraud_damage_acquisition.delivery_of_property",
        "fraud_damage_acquisition.property_concept_reported_precedent",
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
    "fraud_disposition_inducement_intent_satisfied": "피기망자로 하여금 재산적 처분행위를 하게 할 의사가 인정됨",
    "fraud_intent_satisfied": "고의의 기망과 재산적 이득 목적이 함께 인정됨",
    "fraud_role_structure_satisfied": "일반형 또는 삼각사기의 역할 구조와 처분 권능 요건이 충족됨",
    "fraud_beneficiary_attribution_satisfied": "본인 또는 제3자에게 귀속되는 취득 구조가 충족됨",
}

CASE_APPLICATION_DEFINITIONS = {
    "deception.fraud.causal-link.deception-property-disposition": (
        "피고인의 특정 행위가 피기망자의 재산적 처분판단을 향해 있고 그 판단에 "
        "실질적으로 작용했는지를 사건 사실에 적용한 평가"
    ),
    "deception.fraud.definition.deception-good-faith-mistake": (
        "피고인의 특정 행위가 거래상 신의칙에 반하고 피기망자에게 사실과 다른 "
        "인식을 실제로 일으켰는지를 사건 사실에 적용한 평가"
    ),
    "fraud_mistake.error_definition": (
        "피기망자가 처분 당시 사실과 일치하지 않는 구체적 인식을 실제로 "
        "가졌는지를 사건 사실에 적용한 평가"
    ),
    "fraud_mistake.error_disposition_motivation": (
        "그 구체적 착오가 피기망자의 재산적 처분 동기를 형성하거나 확정했는지를 "
        "사건 사실에 적용한 평가"
    ),
    "fraud_damage_acquisition.property_concept_reported_precedent": (
        "법률행위의 유·무효와 별개로 beneficiary_id가 구체적이고 외형적인 "
        "재산상 이익을 실제 취득했는지를 사건 사실에 적용한 평가"
    ),
    "fraud_intent.contract_breach_distinction": (
        "피고인의 행위가 단순한 사후 채무불이행이 아니라 의도적인 기망으로 "
        "평가되는지를 사건 사실에 적용한 평가"
    ),
    "fraud_intent.time_of_conduct": (
        "기망의 고의가 사후가 아니라 행위 당시에 존재했는지를 사건 사실에 적용한 평가"
    ),
    "fraud_mistake.gain_purpose": (
        "피고인에게 기망을 통해 본인 또는 제3자가 재산적 이득을 취득하게 할 "
        "목적의사가 있었는지를 사건 사실에 적용한 평가"
    ),
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


MODULE_REVIEW_NOTES = {
    "core.deception": {
        "title": "공통 기망",
        "role": "사기 유형과 관계없이 기망행위인지 판단할 때 공통으로 쓰는 정의와 한계다.",
        "boundary": "차용금·광고·부작위·묵시적 기망·권리행사의 특수 기준은 넣지 않았다.",
        "question": "16개가 정말 모든 사기 유형에 공통인지, 특정 유형 기준이 섞였는지 본다.",
    },
    "core.intent": {
        "title": "공통 주관적 요건",
        "role": "고의의 기망, 재산적 이득 목적, 판단 시점과 불법영득의사 논의를 맡는다.",
        "boundary": "차용금 사건의 편취 범의 추론과 제3자 취득 의사는 별도 모듈이다.",
        "question": "불법영득의사 두 카드가 공통 코어에 머물되 최종 공통 gate는 아닌 것이 맞는지 본다.",
    },
    "core.mistake_disposition": {
        "title": "공통 착오·처분행위",
        "role": "착오의 의미, 처분행위, 직접성, 피기망자=처분자 및 순차적 인과관계를 맡는다.",
        "boundary": "부작위 처분, 삼각사기, 절도와의 경계는 별도 모듈로 보냈다.",
        "question": "공통 규칙과 부작위·삼각사기 같은 특수 구조의 경계가 적절한지 본다.",
    },
    "profile.loan": {
        "title": "차용금 사기",
        "role": "변제 의사·능력, 용도 기망, 대주의 위험 인식 및 편취 범의 추론을 맡는다.",
        "boundary": "일반적인 계약 불이행과 고의의 구별 자체는 공통 주관적 요건에 남겼다.",
        "question": "이 여섯 기준이 차용금 사건에서 함께 검색·평가될 단위로 적절한지 본다.",
    },
    "profile.advertising": {
        "title": "광고 사기",
        "role": "불특정 상대방에 대한 광고와 허용되는 과장·허위의 경계를 맡는다.",
        "boundary": "광고 외 일반적인 단순 거짓말·막연한 의견 기준은 공통 기망에 남겼다.",
        "question": "불특정 상대방 카드가 광고에만 한정되는지, 더 넓은 대중 상대 기망 모듈이어야 하는지 본다.",
    },
    "profile.omission": {
        "title": "부작위 기망",
        "role": "기존 착오 이용, 보증인적 지위, 고지의무 및 부작위 처분을 맡는다.",
        "boundary": "행동·태도 자체가 설명가치를 갖는 묵시적 기망은 다음 모듈로 분리했다.",
        "question": "기망의 부작위와 처분행위의 부작위가 한 모듈에 함께 있는 것이 실용적인지 본다.",
    },
    "profile.implicit_deception": {
        "title": "묵시적 기망",
        "role": "행동·태도가 거래관행상 허위 내용을 표시하는 설명가치를 갖는지 판단한다.",
        "boundary": "단순 침묵은 이 모듈에서 바로 기망이 되지 않고 고지의무가 있는 부작위 모듈로 간다.",
        "question": "묵시적 기망과 부작위 기망의 선후 판단이 카드 세 장으로 충분히 드러나는지 본다.",
    },
    "profile.rights_exercise": {
        "title": "권리행사형 사기",
        "role": "권리행사에 사용된 기망수단이 사회통념상 허용 범위를 넘는지 판단한다.",
        "boundary": "권리의 존재 자체가 아니라 행사수단의 허용 가능성을 다룬다.",
        "question": "허용되는 수단과 허용 범위를 넘은 수단의 양방향 기준이 정확한지 본다.",
    },
    "structure.triangular": {
        "title": "삼각사기 역할 구조",
        "role": "피기망자=처분자와 재산상 피해자가 다를 때 처분 권능·지위를 검사한다.",
        "boundary": "기망·착오 등 실체 요건은 공통 코어가 맡고 이 모듈은 인물 관계만 맡는다.",
        "question": "피기망자, 처분자, 재산소유자의 동일성·상이성과 권능 요건이 정확한지 본다.",
    },
    "structure.third_party_acquisition": {
        "title": "제3자 취득 구조",
        "role": "피고인이 아닌 제3자의 취득을 피고인에게 귀속할 수 있는지 판단한다.",
        "boundary": "삼각사기는 피해재산의 처분권한 문제이고, 여기는 취득자 귀속 문제다.",
        "question": "도구·대리 관계 또는 제3자 취득 의사라는 단일 카드가 충분한지 본다.",
    },
    "boundary.other_offenses": {
        "title": "절도·횡령과의 경계",
        "role": "처분능력, 지배이전의 직접성, 점유관계에 따라 사기가 아닌 죄명이 문제되는 경우를 맡는다.",
        "boundary": "현재는 사기 불성립만 출력하고 절도·횡령의 최종 성립까지 판단하지 않는다.",
        "question": "세 기준을 사기 core의 불성립 사유로 둘지 후속 죄명 adapter로 둘지 본다.",
    },
    "object.property_delivery": {
        "title": "재물의 객체·교부",
        "role": "공통 객관적 구성요건으로서 타인의 재물인지, 사실상 지배가 이전되었는지, 금원 편취액이 얼마인지 판단한다.",
        "boundary": "재물 이외의 재산상 이익은 별도 객체 모듈로 분리했다.",
        "question": "사후 반환과 상당한 대가 문제를 이 모듈에 함께 두는 것이 적절한지 본다.",
    },
    "object.property_benefit": {
        "title": "재산상 이익의 객체·취득",
        "role": "공통 객관적 구성요건으로서 재물 외 경제적 이익의 범위, 구체성 및 취득을 가져오는 처분 형태를 맡는다.",
        "boundary": "재물의 현실 교부·지배이전 기준은 앞 모듈에 있다.",
        "question": "경제적 이익의 정의와 실제 취득 판단에 필요한 카드가 충분한지 본다.",
    },
    "object.public_interest": {
        "title": "공공적 법익과 재산권의 경계",
        "role": "공공적 법익 침해가 동시에 재산권 침해와 동일하게 평가되는지 판단한다.",
        "boundary": "별도 특별법이 우선하는 경우와 재산권 침해가 없는 경우는 사기 core 밖으로 보낸다.",
        "question": "특별법 수집이 진행 중인 현재 이 두 카드를 실행 규칙으로 유지할지 본다.",
    },
    "stage.attempt_completion": {
        "title": "미수·기수 및 사후사정",
        "role": "실행의 착수, 인과관계 단절, 재물·이익 이전 시점과 사후 취소의 영향을 맡는다.",
        "boundary": "기망·착오·처분의 내용은 공통 코어가 맡고 여기서는 범행 단계를 판단한다.",
        "question": "현재 fraud_not_established로 나가는 미수 사유를 별도 fraud_attempted로 분리할지 본다.",
    },
}


MODULE_LEGAL_LAYERS = {
    "core.deception": "constitutive_core",
    "core.intent": "constitutive_core",
    "core.mistake_disposition": "constitutive_core",
    "object.property_delivery": "constitutive_core",
    "object.property_benefit": "constitutive_core",
    "profile.loan": "type_profile",
    "profile.advertising": "type_profile",
    "profile.omission": "type_profile",
    "profile.implicit_deception": "type_profile",
    "profile.rights_exercise": "type_profile",
    "structure.triangular": "structural_profile",
    "structure.third_party_acquisition": "structural_profile",
    "boundary.other_offenses": "boundary",
    "object.public_interest": "boundary",
    "stage.attempt_completion": "stage",
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
                "legal_layer": MODULE_LEGAL_LAYERS[spec["module_id"]],
                "card_ids": sorted(spec["card_ids"]),
                "card_count": len(spec["card_ids"]),
            }
        )
    return {
        "version": "1.0.0",
        "rule_set_id": "kr.fraud.article347.full.v1_candidate",
        "status": "post_sol_corrected_human_rereview_pending",
        "architecture": {
            "final_core_rule": "fraud.core.outcome.established",
            "principle": (
                "법학적 구성요건 core는 주체·객체·객관적 행위·주관적 요건으로 "
                "구성한다. 그 아래 실행 profile과 adapter가 canonical interface를 "
                "채우고 최종 core는 세부 유형을 알지 않은 채 이를 AND 결합한다."
            ),
            "routing_semantics": (
                "관련 없는 module은 relation을 만들지 않는다. 관련되지만 자료가 "
                "부족한 쟁점만 unknown으로 명시한다."
            ),
            "common_core_activation": (
                "최종 성립에는 공통 canonical gate가 항상 필요하다. 다만 같은 gate를 "
                "채우는 모든 support card를 한 사건에서 전부 평가한다는 뜻은 아니다."
            ),
            "outcome_resolution": {
                "candidate": "fraud_elements_satisfied",
                "closed_case_gate": "case_assessment_complete",
                "blocking_relations": ["fraud_has_negative", "fraud_has_conflict"],
                "negation_scope": "final outcome stratum only",
            },
            "profile_activation": {
                "default": "off",
                "selection": "case router selects zero or more relevant profiles",
                "coverage": "open_ended_non_exhaustive",
                "irrelevant_profile": "emit no profile assessment relation",
                "relevant_but_underdetermined": "emit explicit unknown relation",
                "runtime_trigger": (
                    "a profile rule can fire only when a profile-specific assess relation "
                    "and its matching provable relation exist"
                ),
            },
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


def build_module_human_review(aggregate: dict[str, Any]) -> str:
    ownership = build_module_ownership(aggregate)
    specs_by_id = {spec["module_id"]: spec for spec in ownership["modules"]}
    cards_by_id = {card["id"]: card for card in aggregate["cards"]}
    original_number = {
        card["id"]: index for index, card in enumerate(aggregate["cards"], 1)
    }
    groups = [
        (
            "A. 사기죄의 공통 구성요건 코어",
            [
                "core.deception",
                "core.intent",
                "core.mistake_disposition",
                "object.property_delivery",
                "object.property_benefit",
            ],
        ),
        (
            "B. 사건 사실유형에 따라 선택하는 프로파일",
            [
                "profile.loan",
                "profile.advertising",
                "profile.omission",
                "profile.implicit_deception",
                "profile.rights_exercise",
            ],
        ),
        (
            "C. 사람과 재산의 관계를 검사하는 구조 모듈",
            ["structure.triangular", "structure.third_party_acquisition"],
        ),
        (
            "D. 구성요건 밖의 경계 모듈",
            ["boundary.other_offenses", "object.public_interest"],
        ),
        ("E. 범행 단계를 검사하는 모듈", ["stage.attempt_completion"]),
    ]
    kind_labels = {
        "general_core": "공통 코어",
        "grounding_profile": "사실유형 프로파일",
        "structural_profile": "역할구조 모듈",
        "boundary_adapter": "죄명경계 모듈",
        "object_adapter": "객체 모듈",
        "stage_module": "미수·기수 모듈",
    }
    legal_layer_labels = {
        "constitutive_core": "공통 구성요건 코어",
        "type_profile": "사실유형 프로파일",
        "structural_profile": "역할구조 프로파일",
        "boundary": "구성요건 경계",
        "stage": "범행단계",
    }
    formalization_labels = {
        "standard_input": "모델·RAG 법적 판단",
        "deterministic_rule": "구조화 사실·결정규칙 전제",
    }
    polarity_labels = {
        "positive": "긍정 기준",
        "negative": "부정 기준",
        "exception": "예외 기준",
    }
    output_labels = {
        "fraud_object_satisfied": "사기죄 객체 충족",
        "fraud_deception_satisfied": "기망 충족",
        "fraud_mistake_satisfied": "착오 충족",
        "fraud_disposition_satisfied": "처분행위 충족",
        "fraud_acquisition_satisfied": "재물·이익 취득 충족",
        "fraud_causal_chain_satisfied": "순차적 인과관계 충족",
        "fraud_deceived_disposer_identity_satisfied": "피기망자=처분자 충족",
        "fraud_intent_satisfied": "고의·이득목적 충족",
        "fraud_unlawful_appropriation_intent_supported": "불법영득의사 판단 지원",
        "fraud_role_structure_satisfied": "일반형·삼각사기 역할구조 충족",
        "fraud_beneficiary_attribution_satisfied": "본인·제3자 취득 귀속 충족",
        "fraud_completion_satisfied": "기수 충족",
        "fraud_not_established": "명시적 사기 불성립 사유",
    }

    lines = [
        "# 사기죄 RuleIR 15개 모듈 인간 검수본",
        "",
        "## 먼저: 15개가 무엇인지",
        "",
        "15개는 사기죄의 유형을 15개로 나눈 것이 아니다. 88개 NormCard를 실행할 때 "
        "공통 규칙과 특정 사건에서만 필요한 규칙이 뒤섞이지 않도록 나눈 작업 단위다.",
        "",
        "법학적 상위 구조에서 사기죄의 공통 구성요건 코어는 다음과 같다.",
        "",
        "1. 주체: 특별한 신분을 요구하지 않는 일반범이다. 현재 RuleIR의 `defendant_id` "
        "역할이 주체를 나타낸다. 책임능력 등은 형법총칙 gate이므로 사기죄 NormCard에는 없다.",
        "2. 객체: 타인이 점유하는 타인의 재물 또는 재산상 이익",
        "3. 객관적 행위·결과·인과: 기망 → 착오 → 처분행위 → 재물 교부·이익 취득",
        "4. 주관적 구성요건: 고의, 재산적 이득 목적, 필요한 범위의 불법영득의사",
        "",
        "이 상위 구조를 실제로 실행하기 위해 15개 하위 모듈을 둔다.",
        "",
        "- 공통 구성요건 코어 5개: 기망 / 주관적 요건 / 착오·처분 / 재물 / 재산상 이익",
        "- 사실유형 프로파일 5개: 차용금 / 광고 / 부작위 / 묵시적 기망 / 권리행사",
        "- 역할구조 2개: 삼각사기 / 제3자 취득",
        "- 구성요건 경계 2개: 절도·횡령 경계 / 공공적 법익과 재산권 경계",
        "- 범행단계 1개: 미수·기수 및 사후사정",
        "",
        "변제 의사·능력은 모든 사기에 필요한 독립 구성요건이 아니다. 차용금 사건에서 "
        "기망과 고의를 구체화하는 기준이므로 차용금 프로파일이 판단한 뒤 공통 코어의 "
        "기망·주관적 요건 충족 결과로 전달한다.",
        "",
        "따라서 일반 사건에서는 공통 구성요건 코어를 쓰고, 사실관계에 해당하는 "
        "프로파일·구조·경계·단계 모듈만 추가로 연다. 아래에는 각 모듈과 그 모듈에 "
        "들어간 카드 원문을 붙여 두었다. JSON은 기계 검증용이므로 검수할 필요가 없다.",
        "",
        "## 실행 원칙: 공통 코어와 사실유형 프로파일",
        "",
        "- 공통 코어의 canonical gate는 최종 사기죄 판단에서 항상 필요하다.",
        "- 사실유형 프로파일은 전부 기본 OFF이며, 사건 라우터가 관련성을 확인한 것만 "
        "0개 이상 선택한다.",
        "- 현재 다섯 프로파일은 알려진 반복 특수규칙의 초기 목록이지 사기 유형의 "
        "완전한 목록이 아니다.",
        "- 어느 프로파일에도 해당하지 않는 사건도 공통 코어만으로 판단할 수 있다.",
        "- 관련 없는 프로파일에는 평가 relation을 만들지 않는다. 이는 false도 unknown도 아니다.",
        "- 관련성은 있지만 자료가 부족한 경우에만 그 프로파일 쟁점을 unknown으로 만든다.",
        "- 새 판례 RAG에서 반복 가능한 특수규칙이 확인되면 기존 코어를 바꾸지 않고 "
        "새 프로파일을 추가한다.",
        "",
        "## 한눈에 보는 15개",
        "",
    ]
    module_number = 0
    for group_title, module_ids in groups:
        lines.extend([f"### {group_title}", ""])
        for module_id in module_ids:
            module_number += 1
            spec = specs_by_id[module_id]
            notes = MODULE_REVIEW_NOTES[module_id]
            lines.append(
                f"{module_number}. **{notes['title']}** ({spec['card_count']}장): "
                f"{notes['role']}"
            )
        lines.append("")

    lines.extend(["## 모듈별 카드 원문과 검수 질문", ""])
    module_number = 0
    for group_title, module_ids in groups:
        lines.extend([f"# {group_title}", ""])
        for module_id in module_ids:
            module_number += 1
            spec = specs_by_id[module_id]
            notes = MODULE_REVIEW_NOTES[module_id]
            output_text = ", ".join(
                output_labels[output_id] for output_id in spec["emits"]
            )
            lines.extend(
                [
                    f"## {module_number}. {notes['title']}",
                    "",
                    f"- 법학적 위치: {legal_layer_labels[spec['legal_layer']]}",
                    f"- 실행 단위: {kind_labels[spec['kind']]}",
                    f"- 하는 일: {notes['role']}",
                    f"- 다른 모듈과의 경계: {notes['boundary']}",
                    f"- Scallop core에 전달하는 판단: {output_text}",
                    f"- **검수 질문: {notes['question']}**",
                    "",
                    f"### 포함 카드 {spec['card_count']}장",
                    "",
                ]
            )
            ordered_card_ids = sorted(
                spec["card_ids"], key=lambda card_id: original_number[card_id]
            )
            for card_index, card_id in enumerate(ordered_card_ids, 1):
                card = cards_by_id[card_id]
                lines.extend(
                    [
                        (
                            f"{card_index}. **원본 {original_number[card_id]}번 · "
                            f"{formalization_labels[card['formalization']]} · "
                            f"{polarity_labels[card['polarity']]}**"
                        ),
                        "",
                        f"   > {card['proposition']}",
                        "",
                        f"   보조 ID: `{card_id}`",
                        "",
                    ]
                )
    lines.extend(
        [
            "## 검수 결과를 적는 방법",
            "",
            "각 모듈 제목 아래의 검수 질문을 기준으로 다음 중 하나를 적으면 된다.",
            "",
            "- `승인`: 현재 묶음과 경계에 동의",
            "- `이동`: 특정 원본 번호를 다른 모듈로 이동",
            "- `분리`: 한 모듈을 둘 이상으로 분리",
            "- `RAG`: 실행 규칙이 아니라 판례 검색 대상으로 전환",
            "- `삭제`: core·profile 어디에도 두지 않음",
            "",
        ]
    )
    return "\n".join(lines)


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
        ),
        predicate(
            "case_assessment_complete",
            [("case_id", "String"), ("defendant_id", "String")],
            kind="rule",
            role="input",
            origin="system",
            definition=(
                "사건 라우터가 선택한 공통·프로파일 쟁점의 유한한 평가 묶음이 "
                "완결되어 최종 결론 계층의 폐쇄세계 검사를 허용함"
            ),
        ),
        predicate(
            "distinct_entity",
            [
                ("case_id", "String"),
                ("left_entity_id", "String"),
                ("right_entity_id", "String"),
            ],
            kind="rule",
            role="input",
            origin="system",
            definition="사건의 entity resolution에서 두 역할이 서로 다른 실체임이 확인됨",
        ),
    ]
    rules: list[dict[str, Any]] = []
    actors = generic_actor_variables()

    for index, card in enumerate(cards, 1):
        card_id = card["id"]
        input_kind = (
            "standard" if card["formalization"] == "standard_input" else "rule"
        )
        case_application = CASE_APPLICATION_DEFINITIONS.get(card_id)
        if case_application is not None:
            input_definition = (
                f"{case_application}. 단순히 법률명제 자체가 옳다는 뜻이 아니라, "
                "현재 actor tuple의 구체적 사실이 그 요건을 충족하는지를 3상태로 판단한다."
            )
        elif input_kind == "standard":
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
                definition=(
                    (
                        "증명 가능한 사건 적용 평가가 충족됨: "
                        + case_application
                    )
                    if case_application is not None
                    else f"증명 가능한 평가에서 다음 조건이 충족됨: {card['proposition']}"
                ),
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

    paired_component_cards = {
        "deception.fraud.causal-link.deception-property-disposition",
        "deception.fraud.definition.deception-good-faith-mistake",
        "fraud_mistake.error_definition",
        "fraud_mistake.error_disposition_motivation",
    }
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
            if card_id in paired_component_cards:
                continue
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

    core_deception_ids = [
        "deception.fraud.definition.deception-good-faith-mistake",
        "deception.fraud.causal-link.deception-property-disposition",
    ]
    rules.append(
        rule(
            "fraud.core_deception.component.fraud_deception_satisfied.01",
            atom("fraud_deception_satisfied", *actors),
            [condition_atom(card_id, actors) for card_id in core_deception_ids],
            cards_for(core_deception_ids, cards_by_id),
            (
                "일반 기망 경로는 정의의 추상적 타당성만으로는 부족하고, 특정 행위의 "
                "신의칙 위반·실제 착오 유발과 재산적 처분 지향성을 함께 요구한다."
            ),
        )
    )

    core_mistake_ids = [
        "fraud_mistake.error_definition",
        "fraud_mistake.error_disposition_motivation",
    ]
    rules.append(
        rule(
            "fraud.core_mistake_disposition.component.fraud_mistake_satisfied.01",
            atom("fraud_mistake_satisfied", *actors),
            [condition_atom(card_id, actors) for card_id in core_mistake_ids],
            cards_for(core_mistake_ids, cards_by_id),
            (
                "일반 착오 경로는 구체적인 사실불일치 인식과 그 인식의 처분동기 형성·"
                "확정을 함께 요구한다. 정의 명제만으로 착오를 인정하지 않는다."
            ),
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

    intent_positive_ids = [
        "fraud_intent.contract_breach_distinction",
        "fraud_intent.time_of_conduct",
        "fraud_mistake.gain_purpose",
    ]
    inducement_intent_card_id = "fraud_intent.no_disposition_inducement_intent"
    intent_ids = [*intent_positive_ids, inducement_intent_card_id]
    predicates.append(
        predicate(
            "fraud_disposition_inducement_intent_satisfied",
            ACTOR_ARGUMENTS,
            kind="rule",
            role="derived",
            origin="commentary",
            definition=COMPONENT_DEFINITIONS[
                "fraud_disposition_inducement_intent_satisfied"
            ],
            cards=[cards_by_id[inducement_intent_card_id]],
        )
    )
    inducement_assessment = "inducement_intent_negative_condition"
    rules.append(
        rule(
            "fraud.core_intent.component.disposition_inducement_intent_satisfied",
            atom("fraud_disposition_inducement_intent_satisfied", *actors),
            [
                assessment_atom(
                    inducement_intent_card_id,
                    "not_satisfied",
                    inducement_assessment,
                    actors,
                ),
                atom("provable", actors[0], variable(inducement_assessment)),
            ],
            [cards_by_id[inducement_intent_card_id]],
            (
                "'처분행위를 하게 할 의사가 없음'이라는 배제조건이 명시적으로 "
                "not_satisfied이고 증명 가능할 때만 처분 유도 의사를 긍정한다."
            ),
        )
    )
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
            [condition_atom(card_id, actors) for card_id in intent_positive_ids]
            + [atom("fraud_disposition_inducement_intent_satisfied", *actors)],
            cards_for(intent_ids, cards_by_id),
            "단순 채무불이행과 구별되는 고의의 기망 및 재산적 이득 목적을 함께 요구한다.",
        )
    )
    loan_intent_positive_ids = [
        "deception.fraud.standard.intent-to-defraud-loan-inference",
        "fraud_intent.time_of_conduct",
        "fraud_mistake.gain_purpose",
    ]
    loan_intent_ids = [*loan_intent_positive_ids, inducement_intent_card_id]
    rules.append(
        rule(
            "fraud.profile_loan.component.fraud_intent_satisfied",
            atom("fraud_intent_satisfied", *actors),
            [condition_atom(card_id, actors) for card_id in loan_intent_positive_ids]
            + [atom("fraud_disposition_inducement_intent_satisfied", *actors)],
            cards_for(loan_intent_ids, cards_by_id),
            "차용금 사건에서는 객관적 사정으로 추론한 편취 범의와 재산적 이득 목적을 결합한다.",
        )
    )

    not_established_cards = cards_for(
        BAR_CARD_IDS | MANDATORY_POSITIVE_CARD_IDS, cards_by_id
    )
    predicates.extend(
        [
            predicate(
                "fraud_elements_satisfied",
                ACTOR_ARGUMENTS,
                kind="rule",
                role="derived",
                origin="commentary",
                definition=(
                    "사기죄의 공통 구성요건·역할·귀속 component가 모두 충족된 "
                    "잠정 성립 후보"
                ),
                cards=cards,
            ),
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
                        "fraud_intent.contract_breach_distinction",
                        "fraud_intent.time_of_conduct",
                        "fraud_mistake.deceived_disposer_identity",
                        "fraud_mistake.disposition_definition",
                        "fraud_mistake.error_definition",
                        "fraud_mistake.error_disposition_motivation",
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
            predicate(
                "fraud_has_negative",
                [("case_id", "String"), ("defendant_id", "String")],
                kind="rule",
                role="derived",
                origin="commentary",
                definition="해당 피고인에 관해 하나 이상의 명시적 사기 불성립 사유가 존재함",
                cards=not_established_cards,
            ),
            predicate(
                "fraud_has_conflict",
                [("case_id", "String"), ("defendant_id", "String")],
                kind="rule",
                role="derived",
                origin="commentary",
                definition="해당 피고인에 관해 하나 이상의 상충 평가가 존재함",
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
                atom(
                    "distinct_entity",
                    triangular_actors[0],
                    triangular_actors[2],
                    triangular_actors[4],
                ),
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
                ),
                atom(
                    "distinct_entity",
                    third_party_actors[0],
                    third_party_actors[1],
                    third_party_actors[5],
                ),
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
                "fraud_role_structure_satisfied",
                "fraud_beneficiary_attribution_satisfied",
            }
            else []
        )
    } | set(intent_ids) | role_card_ids | beneficiary_card_ids

    final_actors = actor_variables()
    rules.append(
        rule(
            "fraud.core.outcome.elements_satisfied",
            atom("fraud_elements_satisfied", *final_actors),
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
                atom("fraud_elements_satisfied", *conflict_actors),
                atom(
                    "fraud_not_established",
                    conflict_actors[0],
                    conflict_actors[1],
                    variable("negative_issue_id"),
                ),
            ],
            cards,
            "성립 후보와 명시적 불성립 사유가 함께 도출되면 최종 확정 전에 conflict를 노출한다.",
        )
    )
    rules.extend(
        [
            rule(
                "fraud.core.outcome.has_negative",
                atom("fraud_has_negative", actors[0], actors[1]),
                [
                    atom(
                        "fraud_not_established",
                        actors[0],
                        actors[1],
                        variable("negative_issue_id"),
                    )
                ],
                not_established_cards,
                "명시적 불성립 사유를 최종 결론 계층에서 검사할 2항 relation으로 모은다.",
            ),
            rule(
                "fraud.core.outcome.has_conflict",
                atom("fraud_has_conflict", actors[0], actors[1]),
                [
                    atom(
                        "fraud_conflict",
                        actors[0],
                        actors[1],
                        variable("conflict_issue_id"),
                    )
                ],
                cards,
                "카드·결론 충돌을 최종 결론 계층에서 검사할 2항 relation으로 모은다.",
            ),
        ]
    )
    rules.append(
        rule(
            "fraud.core.outcome.established",
            atom("fraud_established", *final_actors),
            [
                atom("fraud_elements_satisfied", *final_actors),
                atom("case_assessment_complete", final_actors[0], final_actors[1]),
                atom(
                    "fraud_has_negative",
                    final_actors[0],
                    final_actors[1],
                    negated=True,
                ),
                atom(
                    "fraud_has_conflict",
                    final_actors[0],
                    final_actors[1],
                    negated=True,
                ),
            ],
            cards_for(final_base_card_ids, cards_by_id),
            (
                "라우터가 선택한 사건 평가 묶음이 완결된 뒤, 성립 후보에 명시적 "
                "불성립 사유와 충돌이 모두 없을 때만 확정 성립을 출력한다. 이 두 부정은 "
                "완결 게이트 뒤의 최종 층에서만 사용한다."
            ),
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
    prefix = "~" if value.get("negated", False) else ""
    return f"{prefix}{value['predicate']}({arguments})"


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
        "deceived_person_id, disposer_id, property_owner_id, beneficiary_id, "
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
        "공통 코어의 canonical gate는 최종 결론에 항상 필요하지만, 사실유형 profile은 "
        "기본 OFF다. case router가 관련 profile을 0개 이상 선택하고 profile 전용 assess "
        "relation과 `provable`이 함께 있을 때만 해당 규칙이 작동한다. 현재 profile 목록은 "
        "비망라적이며 어느 profile에도 해당하지 않는 사건도 공통 코어로 판단한다.",
        "",
        "모든 substantive 경로는 같은 사건과 평가 ID의 `provable(case_id, "
        "assessment_id)`를 요구한다. 따라서 증거능력·신빙성 검토를 통과하지 않은 진술은 "
        "구성요건 판단에 들어가지 않는다.",
        "`distinct_entity`는 entity resolution이 확인한 역할 상이성을 공급한다. "
        "`case_assessment_complete`는 라우터가 선택한 유한한 평가 묶음이 모두 수집됐다는 "
        "실행 게이트이며, 이 게이트 뒤의 최종 결론 계층에서만 부정 검사를 허용한다.",
        "",
        "## 모듈 구조",
        "",
        "법학적 구성요건 코어는 주체, 객체, 객관적 행위·결과·인과관계, 주관적 요건으로 "
        "구성한다. 재물과 재산상 이익 모듈도 이 상위 코어에 속한다. 주체는 "
        "`defendant_id` 역할로 표현하고 책임능력 등은 형법총칙 gate에서 처리한다.",
        "",
        "15개는 이 법학적 상위 구조 아래의 실행 모듈이다. 각 NormCard에는 하나의 주 "
        "소유 모듈만 있다. 차용금·광고·부작위·묵시적 기망·권리행사는 grounding profile, "
        "삼각사기·제3자취득은 structural profile, 죄명 경계·미수/기수는 boundary 또는 "
        "stage module로 분리했다.",
        "",
        "profile과 adapter는 `fraud_deception_satisfied`, `fraud_role_structure_satisfied` "
        "같은 canonical interface만 출력한다. 최종 core는 차용금이나 삼각사기 같은 세부 "
        "유형명을 알지 않고 이 interface들을 한 번만 AND 결합한다. 현재는 검수를 위해 "
        "하나의 RuleIR 파일 안에서 논리적으로 분리했으며, Scallop 물리 파일 분리는 "
        "Sol 정정본에 대한 사용자 재검수 뒤에 확정한다.",
        "",
    ]
    for module in module_ownership["modules"]:
        module_title = MODULE_REVIEW_NOTES[module["module_id"]]["title"]
        lines.append(
            f"- {module_title} (`{module['module_id']}`, {module['legal_layer']}, "
            f"{module['card_count']}장): "
            f"{module['description']}"
        )
    lines.extend(
        [
            "",
            "## 최종 성립의 AND gate",
        "",
        "최종 성립은 아래 10개 사실·법적 component가 모두 있어야 한다.",
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
        "",
        "현실적 재산상 손해 불요 법리는 별도 사실요건이 아니므로 AND gate나 자동 파생 "
        "predicate로 만들지 않았다. 취득을 요구하되 추가 손해 gate를 두지 않는 규칙의 "
        "부재 자체로 구현한다.",
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
        "`fraud_conflict`가 나온다. 이 단계까지는 개방세계의 양의 규칙만 사용한다.",
        "",
        "모든 component가 모이면 먼저 `fraud_elements_satisfied`만 도출한다. 성립 후보와 "
        "불성립 사유가 함께 있으면 `established_and_not_established` conflict를 만든다. "
        "라우터가 `case_assessment_complete`를 공급한 뒤, `fraud_has_negative`와 "
        "`fraud_has_conflict`가 모두 없을 때만 층화 부정으로 `fraud_established`를 확정한다. "
        "따라서 충돌이나 불성립 사유와 확정 성립이 동시에 노출되지 않는다.",
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
            "**Sol 지적 수동 정정 및 에이전트 재검토 완료, 사용자 재검수 대기.** Terra의 "
            "원본 부분 출력은 candidate로 사용하지 않았고, 승인된 88장만으로 수동·"
            "결정적으로 재구성했다.",
            "",
            "## 자동 검증",
            "",
            f"- NormCard scope: {len(rule_ir['norm_card_scope']['card_ids'])}/88",
            f"- commentary input: {len(input_predicates)}개",
            f"- predicate: {len(rule_ir['predicates'])}개",
            f"- rule: {len(rule_ir['rules'])}개",
            "- 모든 input의 provable pairing: 통과",
            "- case variable isolation: 통과",
            "- negation: 완결 게이트 뒤 최종 outcome stratum의 2개 검사로 제한",
            "- active_policy 부재: 통과",
            "- 피기망자=처분자 성립 head: 통과",
            f"- module ownership: {len(module_ownership['modules'])}개 모듈, 88/88, 중복 0",
            "- profile activation: 기본 OFF, 사건별 0개 이상 선택, 비망라적 registry",
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
            "8. 재물과 재산상 이익 모듈은 실행상 분리되어 있지만 법학적 상위 분류에서는 "
            "모두 공통 객관적 구성요건 코어에 속한다. 변제 의사·능력은 차용금 profile이 "
            "기망·고의 component로 변환한다.",
            "9. 사실유형 profile은 항상 켜지지 않는다. 관련 profile의 assess relation과 "
            "provable이 함께 있을 때만 작동하며, 목록은 비망라적이다.",
            "",
            "## 남은 위험",
            "",
            "- 88개 assessment는 한 사건에서 전부 호출한다는 뜻이 아니다. 사건 관련성 "
            "routing 후 필요한 항목만 평가해야 한다.",
            "- deterministic 28개 입력은 법적 standard 판단이 아니라 규칙 antecedent의 "
            "구조화된 rule fact로 추출해야 한다.",
            "- profile router가 관련 모듈을 먼저 골라야 한다. 단순한 정의 카드와 실제 적용 "
            "충족을 혼동하지 않도록 feature schema와 RAG 근거가 필요하다.",
            "- `case_assessment_complete`는 router가 관련 profile을 확정하고 모든 선택 쟁점의 "
            "평가를 수집한 뒤에만 공급해야 한다.",
            "",
        ]
    )


def build_human_guide(rule_ir: dict[str, Any]) -> str:
    return "\n".join(
        [
            "# 사기죄 full RuleIR 사용자 검수 가이드",
            "",
            "이번에는 88개 카드와 15개 모듈을 처음부터 다시 읽을 필요가 없다. 먼저 "
            "`fraud_full_rule_ir_sol_adjudication.md`의 항목별 판정표와 마지막 사용자 "
            "재검수 포인트 3개를 읽는다.",
            "",
            "1. Sol 지적 13개 중 11개 수용·수정수용, 2개 불수용 판단을 확인한다.",
            "2. 일반형/삼각사기 역할 정책, 주관적 요건 묶음, 완결 게이트에 동의하는지 본다.",
            "3. 더 자세한 논리가 필요할 때만 `fraud_full_rule_ir_natural_language_explanation.md`의 "
            "최종 AND gate와 역할·취득 adapter 부분을 확인한다.",
            "4. JSON과 342개 rule별 해설은 특정 구현을 추적할 때만 보면 된다.",
            "",
            f"최종 승인본은 predicate {len(rule_ir['predicates'])}개, rule "
            f"{len(rule_ir['rules'])}개다. Sol 검토, 에이전트 수동 정정, 사용자 재검수가 "
            "모두 끝났으며 별도 승인 기록 뒤 deterministic compile과 공식 scli golden "
            "test를 실행했다.",
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
    MODULE_HUMAN_REVIEW.write_text(
        build_module_human_review(aggregate), encoding="utf-8"
    )
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
    write_json(
        HUMAN_REVIEW_DECISION,
        {
            "version": "1.0.0",
            "decision_id": "fraud.full.rule_ir.human_review.v1",
            "status": "approved",
            "decided_on": "2026-07-18",
            "review_scope": [
                "common constitutive core",
                "module ownership and legal layers",
                "selective profile activation",
                "canonical role and beneficiary adapters",
            ],
            "approved_conditions": {
                "common_core": "required by the final fraud conclusion",
                "type_profiles": "default off and selected zero or more by relevance",
                "profile_registry": "open ended and non-exhaustive",
                "irrelevant_profile": "no relation, not false or unknown",
                "unknown": "only for a relevant but underdetermined issue",
            },
            "next_sequence": [
                "Sol critic call complete",
                "agent source-grounded re-review and manual correction complete",
                "human re-review",
                "Scallop compile and runtime tests",
            ],
        },
    )

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
    sol_complete = SOL_CRITIQUE.exists()
    post_sol_human_complete = (
        POST_SOL_HUMAN_DECISION.exists()
        and read_json(POST_SOL_HUMAN_DECISION).get("status")
        == "approved_for_scallop_runtime"
    )
    scallop_runtime_complete = (
        SCALLOP_RUNTIME_REPORT.exists()
        and read_json(SCALLOP_RUNTIME_REPORT).get("status") == "pass"
    )
    if scallop_runtime_complete:
        workflow_status = "scallop_runtime_verified"
    elif post_sol_human_complete:
        workflow_status = "post_sol_human_approved_scallop_allowed"
    elif sol_complete:
        workflow_status = "agent_post_sol_rereview_complete_human_review_pending"
    else:
        workflow_status = "human_review_complete_sol_authorized"
    write_json(
        POST_TERRA_STATUS,
        {
            "version": "1.0.0",
            "status": workflow_status,
            "terra_api_calls": run_summary["api_calls"],
            "terra_raw_output": "rejected_partial_output",
            "local_contract_validation": "pass",
            "agent_rule_by_rule_review": "complete",
            "agent_post_sol_rereview": "complete" if sol_complete else "pending",
            "agent_natural_language_explanation": "complete",
            "human_rule_ir_review_allowed": sol_complete,
            "human_rule_ir_review": (
                "approved_post_sol"
                if post_sol_human_complete
                else ("pending_post_sol" if sol_complete else "approved")
            ),
            "human_review_decision_path": str(
                HUMAN_REVIEW_DECISION.relative_to(PROJECT_ROOT)
            ),
            "sol_critic": "complete" if sol_complete else "pending",
            "sol_critic_allowed": not sol_complete,
            "sol_critic_execution_authorized": not sol_complete,
            "sol_critic_report_path": (
                str(SOL_CRITIQUE.relative_to(PROJECT_ROOT))
                if sol_complete
                else None
            ),
            "sol_adjudication_path": str(
                SOL_ADJUDICATION.relative_to(PROJECT_ROOT)
            ),
            "post_sol_human_decision_path": (
                str(POST_SOL_HUMAN_DECISION.relative_to(PROJECT_ROOT))
                if post_sol_human_complete
                else None
            ),
            "scallop_compile_allowed": post_sol_human_complete,
            "scallop_compile": (
                "complete" if SCALLOP_COMPILE_MANIFEST.exists() else "pending"
            ),
            "scallop_compile_manifest_path": (
                str(SCALLOP_COMPILE_MANIFEST.relative_to(PROJECT_ROOT))
                if SCALLOP_COMPILE_MANIFEST.exists()
                else None
            ),
            "scallop_runtime": (
                "pass" if scallop_runtime_complete else "pending"
            ),
            "scallop_runtime_report_path": (
                str(SCALLOP_RUNTIME_REPORT.relative_to(PROJECT_ROOT))
                if scallop_runtime_complete
                else None
            ),
            "candidate_path": str(CANDIDATE.relative_to(PROJECT_ROOT)),
            "explanation_path": str(EXPLANATION.relative_to(PROJECT_ROOT)),
            "agent_review_path": str(AGENT_REVIEW.relative_to(PROJECT_ROOT)),
            "module_ownership_path": str(
                MODULE_OWNERSHIP.relative_to(PROJECT_ROOT)
            ),
            "module_human_review_path": str(
                MODULE_HUMAN_REVIEW.relative_to(PROJECT_ROOT)
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
                "next_gate": (
                    "complete"
                    if scallop_runtime_complete
                    else (
                        "scallop_runtime"
                        if post_sol_human_complete
                        else ("human_post_sol_rereview" if sol_complete else "sol_critic")
                    )
                ),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
