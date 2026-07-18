"""Derivation-conditioned long-form generation contracts and host logic."""

from __future__ import annotations

import copy
import hashlib
import json
import math
import re
from collections import Counter
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from jsonschema import Draft202012Validator


PROJECT_ROOT = Path(__file__).resolve().parents[3]
CONTRACT_ROOT = PROJECT_ROOT / "docs/contracts"
FRAUD_AUDIT_PATH = (
    PROJECT_ROOT / "data/rulegen/fraud/fraud_norm_card_audit.json"
)
FRAUD_REQUESTS_PATH = (
    PROJECT_ROOT / "data/rulegen/fraud/fraud_rulegen_requests.jsonl"
)

METHOD_IDS = (
    "m1_direct",
    "m2_rag",
    "m3_factgraph_rag",
    "m4_factgraph_scallop",
    "m5_irac_plan",
    "m6_claim_verified",
)

FRAUD_IRAC_UNIT_SPECS = (
    {
        "unit_id": "irac_object_roles",
        "issue": "사기죄의 객체와 대상 거래의 역할 구조",
        "question": "3천만 원이 사기죄의 재물 객체이고 B가 피기망자이자 처분자인가?",
        "component_predicates": [
            "fraud_object_satisfied",
            "fraud_role_structure_satisfied",
            "fraud_beneficiary_attribution_satisfied",
        ],
        "card_ids": [
            "general_object.fraud.element.object-other-possessed-other-property",
            "fraud_mistake.deceived_disposer_identity",
        ],
    },
    {
        "unit_id": "irac_deception",
        "issue": "차용 목적 기망의 중요성",
        "question": "수술비라는 허위 용도 고지가 B의 대여 여부를 좌우하는 기망인가?",
        "component_predicates": ["fraud_deception_satisfied"],
        "card_ids": ["deception.fraud.standard.loan-purpose-materiality"],
    },
    {
        "unit_id": "irac_mistake_disposition",
        "issue": "B의 착오와 재산적 처분행위",
        "question": "용도에 관한 착오가 B의 3천만 원 대여 처분을 유발했는가?",
        "component_predicates": [
            "fraud_mistake_satisfied",
            "fraud_disposition_satisfied",
        ],
        "card_ids": [
            "fraud_mistake.error_definition",
            "fraud_mistake.error_disposition_motivation",
            "fraud_mistake.disposition_definition",
        ],
    },
    {
        "unit_id": "irac_causation_completion",
        "issue": "인과관계, 재물 취득과 기수",
        "question": "기망-착오-처분-교부가 순차적으로 이어져 乙의 취득과 기수가 인정되는가?",
        "component_predicates": [
            "fraud_acquisition_satisfied",
            "fraud_causal_chain_satisfied",
            "fraud_completion_satisfied",
        ],
        "card_ids": [
            "fraud_damage_acquisition.delivery_of_property",
            "fraud_mistake.sequential_causation",
            "fraud_stages_participation.completion_deception_disposition_transfer",
        ],
    },
    {
        "unit_id": "irac_intent",
        "issue": "편취의 범의와 재산적 이득 목적",
        "question": "乙에게 차용 당시 편취의 범의, 처분 유도 의사와 재산적 이득 목적이 있었는가?",
        "component_predicates": ["fraud_intent_satisfied"],
        "card_ids": [
            "deception.fraud.standard.intent-to-defraud-loan-inference",
            "fraud_intent.time_of_conduct",
            "fraud_mistake.gain_purpose",
            "fraud_intent.no_disposition_inducement_intent",
        ],
    },
)

EXPECTED_LOAN_CARD_STATUSES = {
    card_id: "satisfied"
    for unit in FRAUD_IRAC_UNIT_SPECS
    for card_id in unit["card_ids"]
}
EXPECTED_LOAN_CARD_STATUSES[
    "fraud_intent.no_disposition_inducement_intent"
] = "not_satisfied"


class GenerationContractError(ValueError):
    """Raised when generation artifacts cannot safely cross a host boundary."""

    def __init__(self, errors: Sequence[str]) -> None:
        self.errors = list(errors)
        super().__init__("Invalid generation artifact:\n- " + "\n- ".join(self.errors))


@lru_cache(maxsize=None)
def generation_schema(filename: str) -> dict[str, Any]:
    return json.loads((CONTRACT_ROOT / filename).read_text(encoding="utf-8"))


def build_fraud_rag_packet(
    *,
    query_texts: Sequence[str],
    top_k: int = 6,
) -> dict[str, Any]:
    if top_k < 1:
        raise ValueError("top_k must be positive")
    rows, comments = _fraud_retrieval_corpus()
    query = " ".join(text.strip() for text in query_texts if text.strip())
    if not query:
        raise ValueError("at least one non-empty retrieval query is required")
    query_terms = _search_terms(query)
    document_terms = [_search_terms(row["proposition"]) for row in rows]
    document_frequency: Counter[str] = Counter()
    for terms in document_terms:
        document_frequency.update(set(terms))
    corpus_size = len(rows)
    scored: list[tuple[float, str, dict[str, Any]]] = []
    for row, terms in zip(rows, document_terms):
        score = _bm25_score(
            query_terms=query_terms,
            document_terms=terms,
            document_frequency=document_frequency,
            corpus_size=corpus_size,
        )
        scored.append((score, row["card_id"], row))
    selected = sorted(scored, key=lambda item: (-item[0], item[1]))[:top_k]
    items: list[dict[str, Any]] = []
    for rank, (score, _, row) in enumerate(selected, start=1):
        sources = []
        for comment_id in row["source_comment_ids"]:
            comment = comments.get(comment_id)
            if comment is None:
                raise GenerationContractError(
                    [f"retrieval card {row['card_id']} has unknown source {comment_id}"]
                )
            sources.append(
                {
                    "comment_id": comment_id,
                    "section_path": comment["section_path"],
                    "section_title": comment["section_title"],
                    "excerpt": _source_excerpt(comment["document_text"], query_terms),
                }
            )
        items.append(
            {
                "rank": rank,
                "score": round(score, 6),
                "card_id": row["card_id"],
                "module": row["module"],
                "doctrinal_status": row["doctrinal_status"],
                "authority_basis": row["authority_basis"],
                "proposition": row["proposition"],
                "sources": sources,
            }
        )
    return {
        "version": "1.0.0",
        "retrieval_method": "deterministic_bm25_character_bigram",
        "corpus": {
            "cards": len(rows),
            "scope": "fraud retrieval_only NormCards",
        },
        "query_texts": list(query_texts),
        "top_k": top_k,
        "items": items,
    }


def build_fraud_rag_queries(
    *,
    case: Mapping[str, Any],
    fact_graph: Mapping[str, Any] | None = None,
) -> list[str]:
    """Build target-scoped retrieval queries without leaking answer rubrics."""

    target = case["target"]
    transaction = target["target_transaction"]
    queries = [
        case["question_prompt"],
        transaction["description"],
        "차용금 진정한 용도 허위 고지 용도를 속여 돈을 빌린 경우 사기죄 편취 범의",
    ]
    if fact_graph is None:
        return queries

    actors = fact_graph.get("actors", [])
    defendant_ids = {
        actor["entity_id"]
        for actor in actors
        if "defendant" in actor.get("roles", [])
    }
    counterparty_ids = {
        actor["entity_id"]
        for actor in actors
        if {"deceived_person", "disposer"} & set(actor.get("roles", []))
    }
    target_actor_ids = defendant_ids | counterparty_ids
    for fact in fact_graph.get("facts", []):
        participants = set(fact.get("participants", []))
        if participants and participants <= target_actor_ids and participants & counterparty_ids:
            queries.append(fact["statement"])
    return _ordered_unique(queries)


def validate_fraud_rag_packet(packet: Mapping[str, Any]) -> None:
    errors: list[str] = []
    rows, comments = _fraud_retrieval_corpus()
    cards = {row["card_id"]: row for row in rows}
    seen: set[str] = set()
    for index, item in enumerate(packet.get("items", [])):
        card_id = item.get("card_id", "")
        if card_id in seen:
            errors.append(f"duplicate retrieved card {card_id}")
        seen.add(card_id)
        row = cards.get(card_id)
        if row is None:
            errors.append(f"items[{index}] is not a retrieval-only fraud card")
            continue
        if item.get("proposition") != row["proposition"]:
            errors.append(f"items[{index}] proposition differs from audit corpus")
        for source in item.get("sources", []):
            comment = comments.get(source.get("comment_id", ""))
            if comment is None:
                errors.append(f"items[{index}] contains unknown commentary source")
            elif source.get("excerpt", "") not in comment["document_text"]:
                errors.append(f"items[{index}] excerpt is not an exact source substring")
    if len(packet.get("items", [])) != packet.get("top_k"):
        errors.append("retrieved item count does not match top_k")
    if errors:
        raise GenerationContractError(errors)


def build_fraud_irac_plan(
    *,
    case: Mapping[str, Any],
    fact_graph: Mapping[str, Any],
    assessment_bundle: Mapping[str, Any],
    authority_packet: Sequence[Mapping[str, Any]],
    symbolic_result: Mapping[str, Any],
) -> dict[str, Any]:
    assessments = {
        item["card_id"]: item for item in assessment_bundle["assessments"]
    }
    authorities = {item["card_id"]: item for item in authority_packet}
    units: list[dict[str, Any]] = []
    for order, spec in enumerate(FRAUD_IRAC_UNIT_SPECS, start=1):
        card_assessments = []
        required_fact_ids: list[str] = []
        required_authorities: list[str] = []
        unit_statuses: list[tuple[str, str]] = []
        for card_id in spec["card_ids"]:
            assessment = assessments.get(card_id)
            authority = authorities.get(card_id)
            if assessment is None or authority is None:
                raise GenerationContractError(
                    [f"cannot compile IRAC unit; missing card {card_id}"]
                )
            fact_ids = list(assessment["basis_fact_ids"]) + list(
                assessment["counter_fact_ids"]
            )
            required_fact_ids.extend(fact_ids)
            required_authorities.extend(assessment["authority_comment_ids"])
            unit_statuses.append((card_id, assessment["status"]))
            card_assessments.append(
                {
                    "assessment_id": assessment["assessment_id"],
                    "card_id": card_id,
                    "proposition": authority["proposition"],
                    "status": assessment["status"],
                    "basis_fact_ids": list(assessment["basis_fact_ids"]),
                    "counter_fact_ids": list(assessment["counter_fact_ids"]),
                    "missing_facts": list(assessment["missing_facts"]),
                    "authority_comment_ids": list(
                        assessment["authority_comment_ids"]
                    ),
                    "application_bridge": assessment["rationale"],
                }
            )
        units.append(
            {
                "unit_id": spec["unit_id"],
                "order": order,
                "issue": spec["issue"],
                "question": spec["question"],
                "component_predicates": list(spec["component_predicates"]),
                "card_assessments": card_assessments,
                "required_fact_ids": _ordered_unique(required_fact_ids),
                "required_authority_comment_ids": _ordered_unique(
                    required_authorities
                ),
                "required_conclusion": _unit_conclusion(unit_statuses),
            }
        )
    observed = symbolic_result["observed_nonempty"]
    plan = {
        "version": "1.0.0",
        "case_id": case["case_id"],
        "rule_set_id": case["rule_set_id"],
        "overall_conclusion": symbolic_result["legal_result"],
        "scallop_relations": [
            relation for relation, active in observed.items() if active
        ],
        "units": units,
        "generation_policy": {
            "use_only_supplied_facts": True,
            "use_only_supplied_authorities": True,
            "preserve_unknown": True,
            "match_required_conclusions": True,
        },
    }
    validate_fraud_irac_plan(
        plan,
        case=case,
        fact_graph=fact_graph,
        assessment_bundle=assessment_bundle,
        authority_packet=authority_packet,
        symbolic_result=symbolic_result,
    )
    return plan


def validate_fraud_irac_plan(
    plan: Mapping[str, Any],
    *,
    case: Mapping[str, Any],
    fact_graph: Mapping[str, Any],
    assessment_bundle: Mapping[str, Any],
    authority_packet: Sequence[Mapping[str, Any]],
    symbolic_result: Mapping[str, Any],
) -> None:
    errors = _schema_errors(plan, "fraud_irac_plan.schema.json")
    if plan.get("case_id") != case.get("case_id"):
        errors.append("IRACPlan case_id does not match case")
    if plan.get("rule_set_id") != case.get("rule_set_id"):
        errors.append("IRACPlan rule_set_id does not match case")
    if plan.get("overall_conclusion") != symbolic_result.get("legal_result"):
        errors.append("IRACPlan conclusion differs from Scallop legal result")
    expected_relations = [
        relation
        for relation, active in symbolic_result.get("observed_nonempty", {}).items()
        if active
    ]
    if list(plan.get("scallop_relations", [])) != expected_relations:
        errors.append("IRACPlan relations differ from active Scallop relations")

    fact_ids = {fact["fact_id"] for fact in fact_graph.get("facts", [])}
    assessment_ids = {
        item["assessment_id"] for item in assessment_bundle.get("assessments", [])
    }
    selected_cards = list(assessment_bundle.get("selected_card_ids", []))
    authority_ids = {
        source["comment_id"]
        for card in authority_packet
        for source in card.get("sources", [])
    }
    observed_cards: list[str] = []
    observed_assessments: list[str] = []
    for index, unit in enumerate(plan.get("units", [])):
        if unit.get("order") != index + 1:
            errors.append(f"units[{index}] order is not contiguous")
        unknown_facts = set(unit.get("required_fact_ids", [])) - fact_ids
        if unknown_facts:
            errors.append(f"units[{index}] has unknown facts: {sorted(unknown_facts)}")
        unknown_authorities = (
            set(unit.get("required_authority_comment_ids", [])) - authority_ids
        )
        if unknown_authorities:
            errors.append(
                f"units[{index}] has unknown authorities: {sorted(unknown_authorities)}"
            )
        for assessment in unit.get("card_assessments", []):
            observed_cards.append(assessment.get("card_id", ""))
            observed_assessments.append(assessment.get("assessment_id", ""))
    if len(observed_cards) != len(set(observed_cards)):
        errors.append("IRACPlan contains duplicate cards across units")
    if set(observed_cards) != set(selected_cards):
        errors.append("IRACPlan card coverage differs from selected cards")
    if set(observed_assessments) != assessment_ids:
        errors.append("IRACPlan assessment coverage is incomplete")
    if errors:
        raise GenerationContractError(errors)


def validate_long_form_answer(
    answer: Mapping[str, Any],
    *,
    case_id: str,
    method_id: str,
    allowed_fact_ids: Iterable[str] = (),
    allowed_card_ids: Iterable[str] = (),
    allowed_authority_ids: Iterable[str] = (),
) -> None:
    errors = _schema_errors(answer, "long_form_answer.schema.json")
    if answer.get("case_id") != case_id:
        errors.append("long-form answer case_id does not match")
    if answer.get("method_id") != method_id:
        errors.append("long-form answer method_id does not match")
    allowed = {
        "cited_fact_ids": set(allowed_fact_ids),
        "cited_card_ids": set(allowed_card_ids),
        "cited_authority_comment_ids": set(allowed_authority_ids),
    }
    seen_sections: set[str] = set()
    for index, section in enumerate(answer.get("sections", [])):
        section_id = section.get("section_id", "")
        if section_id in seen_sections:
            errors.append(f"duplicate answer section {section_id}")
        seen_sections.add(section_id)
        for field, allowed_ids in allowed.items():
            unknown = set(section.get(field, [])) - allowed_ids
            if unknown:
                errors.append(
                    f"sections[{index}].{field} contains unavailable IDs: {sorted(unknown)}"
                )
    if errors:
        raise GenerationContractError(errors)


def assess_irac_answer_alignment(
    answer: Mapping[str, Any], plan: Mapping[str, Any]
) -> list[dict[str, str]]:
    violations: list[dict[str, str]] = []
    expected_units = list(plan["units"])
    sections = list(answer.get("sections", []))
    expected_ids = [unit["unit_id"] for unit in expected_units]
    actual_ids = [section.get("section_id", "") for section in sections]
    if actual_ids != expected_ids:
        violations.append(
            {
                "code": "section_plan_mismatch",
                "section_id": "document",
                "message": f"expected sections {expected_ids}, got {actual_ids}",
            }
        )
    sections_by_id = {section.get("section_id", ""): section for section in sections}
    for unit in expected_units:
        section = sections_by_id.get(unit["unit_id"])
        if section is None:
            continue
        required_cards = {item["card_id"] for item in unit["card_assessments"]}
        missing_cards = required_cards - set(section.get("cited_card_ids", []))
        if missing_cards:
            violations.append(
                {
                    "code": "missing_required_card_metadata",
                    "section_id": unit["unit_id"],
                    "message": f"missing cards {sorted(missing_cards)}",
                }
            )
        missing_facts = set(unit["required_fact_ids"]) - set(
            section.get("cited_fact_ids", [])
        )
        if missing_facts:
            violations.append(
                {
                    "code": "missing_required_fact_metadata",
                    "section_id": unit["unit_id"],
                    "message": f"missing facts {sorted(missing_facts)}",
                }
            )
        if section.get("stated_conclusion") != unit["required_conclusion"]:
            violations.append(
                {
                    "code": "section_conclusion_mismatch",
                    "section_id": unit["unit_id"],
                    "message": (
                        f"expected {unit['required_conclusion']}, got "
                        f"{section.get('stated_conclusion')}"
                    ),
                }
            )
    if answer.get("overall_conclusion") != plan.get("overall_conclusion"):
        violations.append(
            {
                "code": "overall_conclusion_mismatch",
                "section_id": "document",
                "message": (
                    f"expected {plan.get('overall_conclusion')}, got "
                    f"{answer.get('overall_conclusion')}"
                ),
            }
        )
    return violations


def validate_claim_graph(
    claim_graph: Mapping[str, Any],
    *,
    answer: Mapping[str, Any],
    plan: Mapping[str, Any],
    fact_graph: Mapping[str, Any],
    authority_packet: Sequence[Mapping[str, Any]],
) -> list[dict[str, str]]:
    violations: list[dict[str, str]] = []
    try:
        schema_errors = _schema_errors(claim_graph, "claim_graph.schema.json")
    except (TypeError, AttributeError) as exc:
        schema_errors = [f"claim graph is not a JSON object: {exc}"]
    for message in schema_errors:
        violations.append(
            {"code": "claim_schema", "section_id": "document", "message": message}
        )
    if schema_errors:
        return violations
    if claim_graph.get("case_id") != answer.get("case_id"):
        violations.append(
            {
                "code": "claim_case_mismatch",
                "section_id": "document",
                "message": "ClaimGraph case_id differs from answer",
            }
        )
    sections = {section["section_id"]: section for section in answer["sections"]}
    fact_ids = {fact["fact_id"] for fact in fact_graph["facts"]}
    card_ids = {
        card["card_id"]
        for unit in plan["units"]
        for card in unit["card_assessments"]
    }
    authority_ids = {
        source["comment_id"]
        for card in authority_packet
        for source in card["sources"]
    }
    relation_ids = set(plan["scallop_relations"])
    claims_by_section: dict[str, list[Mapping[str, Any]]] = {
        section_id: [] for section_id in sections
    }
    seen_claim_ids: set[str] = set()
    for index, claim in enumerate(claim_graph["claims"]):
        claim_id = claim["claim_id"]
        section_id = claim["section_id"]
        if claim_id in seen_claim_ids:
            violations.append(
                {
                    "code": "duplicate_claim",
                    "section_id": section_id,
                    "message": f"duplicate claim ID {claim_id}",
                }
            )
        seen_claim_ids.add(claim_id)
        section = sections.get(section_id)
        if section is None:
            violations.append(
                {
                    "code": "unknown_section",
                    "section_id": section_id,
                    "message": f"claim {claim_id} references an unknown section",
                }
            )
            continue
        claims_by_section[section_id].append(claim)
        if claim["quote"] not in section["body"]:
            violations.append(
                {
                    "code": "inexact_claim_quote",
                    "section_id": section_id,
                    "message": f"claim {claim_id} quote is not an exact body substring",
                }
            )
        for field, supplied, allowed in (
            ("fact_ids", claim["fact_ids"], fact_ids),
            ("card_ids", claim["card_ids"], card_ids),
            ("authority_comment_ids", claim["authority_comment_ids"], authority_ids),
            ("relation_ids", claim["relation_ids"], relation_ids),
        ):
            unknown = set(supplied) - allowed
            if unknown:
                violations.append(
                    {
                        "code": "unknown_provenance_id",
                        "section_id": section_id,
                        "message": f"claim {claim_id} {field}: {sorted(unknown)}",
                    }
                )
        _check_claim_support(claim, violations)

    plan_units = {unit["unit_id"]: unit for unit in plan["units"]}
    conclusion_map: dict[str, str] = {}
    for item in claim_graph["section_conclusions"]:
        section_id = item["section_id"]
        if section_id in conclusion_map:
            violations.append(
                {
                    "code": "duplicate_section_conclusion",
                    "section_id": section_id,
                    "message": "ClaimGraph repeats a section conclusion",
                }
            )
        conclusion_map[section_id] = item["conclusion"]
    unknown_conclusion_sections = set(conclusion_map) - set(plan_units)
    for section_id in sorted(unknown_conclusion_sections):
        violations.append(
            {
                "code": "unknown_section_conclusion",
                "section_id": section_id,
                "message": "ClaimGraph concludes an unplanned section",
            }
        )
    for section_id, unit in plan_units.items():
        claims = claims_by_section.get(section_id, [])
        claim_types = {claim["claim_type"] for claim in claims}
        for required_type in ("rule", "application", "conclusion"):
            if required_type not in claim_types:
                violations.append(
                    {
                        "code": f"missing_{required_type}_claim",
                        "section_id": section_id,
                        "message": f"section lacks a {required_type} claim",
                    }
                )
        observed_cards = {
            card_id for claim in claims for card_id in claim.get("card_ids", [])
        }
        required_cards = {item["card_id"] for item in unit["card_assessments"]}
        missing_cards = required_cards - observed_cards
        if missing_cards:
            violations.append(
                {
                    "code": "claim_card_coverage",
                    "section_id": section_id,
                    "message": f"claims omit cards {sorted(missing_cards)}",
                }
            )
        observed_facts = {
            fact_id for claim in claims for fact_id in claim.get("fact_ids", [])
        }
        missing_facts = set(unit["required_fact_ids"]) - observed_facts
        if missing_facts:
            violations.append(
                {
                    "code": "claim_fact_coverage",
                    "section_id": section_id,
                    "message": f"claims omit facts {sorted(missing_facts)}",
                }
            )
        if conclusion_map.get(section_id) != unit["required_conclusion"]:
            violations.append(
                {
                    "code": "backparsed_section_conclusion",
                    "section_id": section_id,
                    "message": (
                        f"expected {unit['required_conclusion']}, got "
                        f"{conclusion_map.get(section_id)}"
                    ),
                }
            )
    if claim_graph.get("overall_conclusion") != plan.get("overall_conclusion"):
        violations.append(
            {
                "code": "backparsed_overall_conclusion",
                "section_id": "document",
                "message": (
                    f"expected {plan.get('overall_conclusion')}, got "
                    f"{claim_graph.get('overall_conclusion')}"
                ),
            }
        )
    return violations


def apply_section_patches(
    answer: Mapping[str, Any],
    patch_bundle: Mapping[str, Any],
    *,
    failed_section_ids: Sequence[str],
) -> tuple[dict[str, Any], dict[str, Any]]:
    errors = _schema_errors(patch_bundle, "section_patch_bundle.schema.json")
    if patch_bundle.get("case_id") != answer.get("case_id"):
        errors.append("patch case_id differs from answer")
    expected = list(dict.fromkeys(failed_section_ids))
    patches = list(patch_bundle.get("patches", []))
    observed = [patch.get("section_id", "") for patch in patches]
    if observed != expected:
        errors.append(f"patch sections must be exactly {expected}, got {observed}")
    sections_by_id = {section["section_id"]: section for section in answer["sections"]}
    unknown = set(observed) - set(sections_by_id)
    if unknown:
        errors.append(f"patch references unknown sections: {sorted(unknown)}")
    if errors:
        raise GenerationContractError(errors)

    updated = copy.deepcopy(answer)
    before_hashes = {
        section["section_id"]: canonical_sha256(section)
        for section in updated["sections"]
    }
    replacements = {patch["section_id"]: patch for patch in patches}
    updated["sections"] = [
        copy.deepcopy(replacements.get(section["section_id"], section))
        for section in updated["sections"]
    ]
    after_hashes = {
        section["section_id"]: canonical_sha256(section)
        for section in updated["sections"]
    }
    preserved = [
        section_id
        for section_id, before_hash in before_hashes.items()
        if section_id not in replacements and after_hashes[section_id] == before_hash
    ]
    return updated, {
        "patched_section_ids": observed,
        "preserved_section_ids": preserved,
        "unaffected_sections_preserved": len(preserved)
        == len(before_hashes) - len(observed),
        "before_section_sha256": before_hashes,
        "after_section_sha256": after_hashes,
    }


def render_long_form_markdown(answer: Mapping[str, Any]) -> str:
    lines = [f"# {answer['title']}", ""]
    for section in answer["sections"]:
        lines.extend([f"## {section['heading']}", "", section["body"], ""])
    lines.extend(["## 종합 결론", "", answer["summary"], ""])
    return "\n".join(lines)


def canonical_sha256(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _unit_conclusion(statuses: Sequence[tuple[str, str]]) -> str:
    if any(status == "unknown" for _, status in statuses):
        return "unknown"
    if all(EXPECTED_LOAN_CARD_STATUSES.get(card_id) == status for card_id, status in statuses):
        return "satisfied"
    return "not_satisfied"


def _check_claim_support(
    claim: Mapping[str, Any], violations: list[dict[str, str]]
) -> None:
    expected_support_kinds = {
        "fact": "explicit_fact",
        "rule": "authority_rule",
        "application": "derived_application",
        "conclusion": "symbolic_conclusion",
    }
    expected_support = expected_support_kinds[claim["claim_type"]]
    if claim["support_kind"] != expected_support:
        violations.append(
            {
                "code": "claim_support_kind_mismatch",
                "section_id": claim["section_id"],
                "message": (
                    f"claim {claim['claim_id']} uses {claim['support_kind']} for "
                    f"{claim['claim_type']}; expected {expected_support}"
                ),
            }
        )
    requirements = {
        "fact": bool(claim["fact_ids"]),
        "rule": bool(claim["card_ids"] or claim["authority_comment_ids"]),
        "application": bool(claim["fact_ids"] and claim["card_ids"]),
        "conclusion": bool(claim["relation_ids"] or claim["card_ids"]),
    }
    if not requirements[claim["claim_type"]]:
        violations.append(
            {
                "code": "unsupported_claim",
                "section_id": claim["section_id"],
                "message": (
                    f"claim {claim['claim_id']} lacks required provenance for "
                    f"{claim['claim_type']}"
                ),
            }
        )


def _schema_errors(payload: Mapping[str, Any], filename: str) -> list[str]:
    validator = Draft202012Validator(generation_schema(filename))
    return [
        f"{'.'.join(str(part) for part in error.absolute_path) or '$'}: {error.message}"
        for error in sorted(
            validator.iter_errors(payload),
            key=lambda item: tuple(str(part) for part in item.path),
        )
    ]


@lru_cache(maxsize=1)
def _fraud_retrieval_corpus() -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    audit = json.loads(FRAUD_AUDIT_PATH.read_text(encoding="utf-8"))
    rows = [
        row
        for row in audit["rows"]
        if row.get("review_status") == "rag_context_only"
        and row.get("rule_ir_role") == "retrieval_only"
    ]
    comments: dict[str, dict[str, Any]] = {}
    for line in FRAUD_REQUESTS_PATH.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        request = json.loads(line)
        for comment in request.get("commentary_chunks", []):
            comments[comment["comment_id"]] = comment
    if len(rows) != 558:
        raise GenerationContractError(
            [f"expected 558 fraud retrieval cards, found {len(rows)}"]
        )
    return rows, comments


def _search_terms(text: str) -> list[str]:
    normalized = re.sub(r"[^가-힣a-z0-9]", "", text.lower())
    bigrams = [normalized[index : index + 2] for index in range(len(normalized) - 1)]
    words = re.findall(r"[가-힣]{2,}|[a-z0-9]{2,}", text.lower())
    return words + bigrams


def _bm25_score(
    *,
    query_terms: Sequence[str],
    document_terms: Sequence[str],
    document_frequency: Mapping[str, int],
    corpus_size: int,
    k1: float = 1.2,
) -> float:
    frequencies = Counter(document_terms)
    score = 0.0
    for term in set(query_terms):
        frequency = frequencies.get(term, 0)
        if not frequency:
            continue
        df = document_frequency.get(term, 0)
        inverse_document_frequency = math.log(1 + (corpus_size - df + 0.5) / (df + 0.5))
        score += inverse_document_frequency * frequency * (k1 + 1) / (frequency + k1)
    return score


def _source_excerpt(document: str, query_terms: Sequence[str], limit: int = 1800) -> str:
    if len(document) <= limit:
        return document
    word_terms = [term for term in query_terms if len(term) >= 2]
    positions = [document.lower().find(term) for term in word_terms]
    positions = [position for position in positions if position >= 0]
    center = min(positions) if positions else 0
    start = max(0, center - limit // 4)
    return document[start : start + limit]


def _ordered_unique(values: Iterable[str]) -> list[str]:
    return list(dict.fromkeys(values))
