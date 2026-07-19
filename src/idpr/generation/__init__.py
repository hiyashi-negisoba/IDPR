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

from idpr.fraud_planning import (
    fraud_case_answer_subject,
    render_reasoning_plan_text,
    select_fraud_reasoning_plan,
)


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

WHOLE_IRAC_SECTION_IDS = (
    "irac_issue",
    "irac_rule",
    "irac_application",
    "irac_conclusion",
)

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
    routing_graph = fact_graph or {"profiles": case.get("required_profiles", [])}
    try:
        reasoning_plan = select_fraud_reasoning_plan(routing_graph, case=case)
    except ValueError as exc:
        raise GenerationContractError([str(exc)]) from exc
    queries = [
        case["question_prompt"],
        transaction["description"],
    ]
    queries.extend(
        render_reasoning_plan_text(template, case)
        for template in reasoning_plan["retrieval_query_templates"]
    )
    if fact_graph is None:
        return _ordered_unique(queries)

    queries.extend(fact_graph.get("retrieval_queries", []))

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
    try:
        reasoning_plan = select_fraud_reasoning_plan(fact_graph, case=case)
    except ValueError as exc:
        raise GenerationContractError([str(exc)]) from exc
    assessments = {
        item["card_id"]: item for item in assessment_bundle["assessments"]
    }
    authorities = {item["card_id"]: item for item in authority_packet}
    units: list[dict[str, Any]] = []
    for order, spec in enumerate(reasoning_plan["units"], start=1):
        card_assessments = []
        deterministic_rules = []
        required_fact_ids: list[str] = []
        required_authorities: list[str] = []
        unit_statuses: list[tuple[str, str]] = []
        expected_statuses: dict[str, str] = {}
        for card_spec in spec["cards"]:
            card_id = card_spec["card_id"]
            expected_statuses[card_id] = card_spec["satisfied_when"]
            assessment = assessments.get(card_id)
            authority = authorities.get(card_id)
            if authority is None:
                raise GenerationContractError(
                    [f"cannot compile IRAC unit; missing authority for {card_id}"]
                )
            if assessment is None:
                if authority.get("formalization") != "deterministic_rule":
                    raise GenerationContractError(
                        [f"cannot compile IRAC unit; missing assessment for {card_id}"]
                    )
                authority_ids = [
                    source["comment_id"] for source in authority.get("sources", [])
                ]
                required_authorities.extend(authority_ids)
                deterministic_rules.append(
                    {
                        "card_id": card_id,
                        "proposition": authority["proposition"],
                        "satisfied_when": card_spec["satisfied_when"],
                        "authority_comment_ids": authority_ids,
                    }
                )
                continue
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
                "issue": render_reasoning_plan_text(spec["issue_template"], case),
                "question": render_reasoning_plan_text(
                    spec["question_template"], case
                ),
                "component_predicates": list(spec["component_predicates"]),
                "card_assessments": card_assessments,
                "deterministic_rules": deterministic_rules,
                "required_fact_ids": _ordered_unique(required_fact_ids),
                "required_authority_comment_ids": _ordered_unique(
                    required_authorities
                ),
                "required_conclusion": _unit_conclusion(
                    unit_statuses, expected_statuses
                ),
            }
        )
    observed = symbolic_result["observed_nonempty"]
    plan = {
        "version": "1.0.0",
        "case_id": case["case_id"],
        "rule_set_id": case["rule_set_id"],
        "reasoning_plan_id": reasoning_plan["plan_id"],
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


def build_fraud_irac_slot_schema(
    plan: Mapping[str, Any], *, method_id: str = "m5_irac_plan"
) -> dict[str, Any]:
    """Build a plan-specific schema that makes every card application mandatory."""

    unit_properties: dict[str, Any] = {}
    unit_ids: list[str] = []
    for unit in plan["units"]:
        unit_id = unit["unit_id"]
        unit_ids.append(unit_id)
        card_properties = {
            item["card_id"]: {
                "type": "string",
                "minLength": 1,
                "maxLength": 2500,
            }
            for item in unit["card_assessments"]
        }
        unit_properties[unit_id] = {
            "type": "object",
            "required": ["card_applications"],
            "additionalProperties": False,
            "properties": {
                "card_applications": {
                    "type": "object",
                    "required": list(card_properties),
                    "additionalProperties": False,
                    "properties": card_properties,
                },
            },
        }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "idpr/FraudIRACSlotDraft",
        "description": (
            "Plan-specific neural application slots compiled deterministically into a "
            "long-form answer."
        ),
        "type": "object",
        "required": [
            "version",
            "case_id",
            "method_id",
            "units",
            "summary_analysis",
        ],
        "additionalProperties": False,
        "properties": {
            "version": {"const": "1.0.0"},
            "case_id": {"const": plan["case_id"]},
            "method_id": {"const": method_id},
            "units": {
                "type": "object",
                "required": unit_ids,
                "additionalProperties": False,
                "properties": unit_properties,
            },
            "summary_analysis": {
                "type": "string",
                "minLength": 1,
                "maxLength": 2000,
            },
        },
    }


def compile_fraud_irac_slot_draft(
    draft: Mapping[str, Any],
    *,
    plan: Mapping[str, Any],
    case: Mapping[str, Any],
    method_id: str = "m5_irac_plan",
) -> dict[str, Any]:
    """Compile neural card slots without trusting the model to copy provenance."""

    schema = build_fraud_irac_slot_schema(plan, method_id=method_id)
    errors = [
        f"{'.'.join(str(part) for part in error.absolute_path) or '$'}: {error.message}"
        for error in sorted(
            Draft202012Validator(schema).iter_errors(draft),
            key=lambda item: tuple(str(part) for part in item.path),
        )
    ]
    if errors:
        raise GenerationContractError(errors)

    generated_texts = [draft["summary_analysis"]]
    generated_texts.extend(
        text
        for unit in draft["units"].values()
        for text in unit["card_applications"].values()
    )
    forbidden_markers = (
        "fact_",
        "comm_",
        "card_applications",
        "summary_analysis",
        *(
            item["card_id"]
            for unit in plan["units"]
            for item in [*unit["card_assessments"], *unit["deterministic_rules"]]
        ),
    )
    leaked_markers = sorted(
        {
            marker
            for text in generated_texts
            for marker in forbidden_markers
            if marker in text
        }
    )
    if leaked_markers:
        raise GenerationContractError(
            [f"IRAC slot prose contains internal markers: {leaked_markers}"]
        )

    sections: list[dict[str, Any]] = []
    for unit in plan["units"]:
        generated_unit = draft["units"][unit["unit_id"]]
        assessment_card_ids = [
            item["card_id"] for item in unit["card_assessments"]
        ]
        rule_cards = [*unit["card_assessments"], *unit["deterministic_rules"]]
        card_ids = [item["card_id"] for item in rule_cards]
        rules = " ".join(item["proposition"].strip() for item in rule_cards)
        applications = " ".join(
            generated_unit["card_applications"][card_id].strip()
            for card_id in assessment_card_ids
        )
        conclusion = _section_conclusion_sentence(
            issue=unit["issue"], status=unit["required_conclusion"]
        )
        body = "\n\n".join([rules, applications, conclusion])
        sections.append(
            {
                "section_id": unit["unit_id"],
                "heading": f"{unit['order']}. {unit['issue']}",
                "body": body,
                "cited_fact_ids": list(unit["required_fact_ids"]),
                "cited_card_ids": card_ids,
                "cited_authority_comment_ids": list(
                    unit["required_authority_comment_ids"]
                ),
                "stated_conclusion": unit["required_conclusion"],
            }
        )

    answer_subject = fraud_case_answer_subject(case)
    final_sentence = _overall_conclusion_sentence(
        answer_subject=answer_subject,
        status=plan["overall_conclusion"],
    )
    answer = {
        "version": "1.0.0",
        "case_id": plan["case_id"],
        "method_id": method_id,
        "title": f"{answer_subject} 성부 검토",
        "sections": sections,
        "overall_conclusion": plan["overall_conclusion"],
        "summary": f"{draft['summary_analysis'].strip()} {final_sentence}",
    }
    validate_long_form_answer(
        answer,
        case_id=plan["case_id"],
        method_id=method_id,
        allowed_fact_ids=(
            fact_id for unit in plan["units"] for fact_id in unit["required_fact_ids"]
        ),
        allowed_card_ids=(
            item["card_id"]
            for unit in plan["units"]
            for item in [*unit["card_assessments"], *unit["deterministic_rules"]]
        ),
        allowed_authority_ids=(
            authority_id
            for unit in plan["units"]
            for authority_id in unit["required_authority_comment_ids"]
        ),
    )
    alignment = assess_irac_answer_alignment(answer, plan)
    if alignment:
        raise GenerationContractError([item["message"] for item in alignment])
    return answer


def compile_fraud_whole_irac_answer(
    *,
    plan: Mapping[str, Any],
    case: Mapping[str, Any],
    method_id: str = "m5_irac_plan",
) -> dict[str, Any]:
    """Compile one document-level IRAC from validated card assessments."""

    unit_labels = ("가", "나", "다", "라", "마", "바", "사", "아")
    rule_blocks: list[str] = []
    application_blocks: list[str] = []
    fact_ids: list[str] = []
    card_ids: list[str] = []
    authority_ids: list[str] = []

    for label, unit in zip(unit_labels, plan["units"]):
        unit_cards = list(unit["card_assessments"])
        unit_rules = [*unit_cards, *unit["deterministic_rules"]]
        rules = " ".join(
            _normalize_legal_sentence(card["proposition"]) for card in unit_rules
        )
        applications = " ".join(
            _normalize_application_bridge(card) for card in unit_cards
        )
        unit_conclusion = _section_conclusion_sentence(
            issue=unit["issue"], status=unit["required_conclusion"]
        )
        rule_blocks.append(f"### {label}. {unit['issue']}\n\n{rules}")
        application_blocks.append(
            f"### {label}. {unit['issue']}\n\n{applications} {unit_conclusion}"
        )
        fact_ids.extend(unit["required_fact_ids"])
        card_ids.extend(card["card_id"] for card in unit_rules)
        authority_ids.extend(unit["required_authority_comment_ids"])

    fact_ids = _ordered_unique(fact_ids)
    card_ids = _ordered_unique(card_ids)
    authority_ids = _ordered_unique(authority_ids)
    answer_subject = fraud_case_answer_subject(case)
    final_sentence = _overall_conclusion_sentence(
        answer_subject=answer_subject, status=plan["overall_conclusion"]
    )
    answer = {
        "version": "1.0.0",
        "case_id": plan["case_id"],
        "method_id": method_id,
        "title": f"{answer_subject} 성부 검토",
        "sections": [
            {
                "section_id": "irac_issue",
                "heading": "1. 쟁점 (Issue)",
                "body": f"이 사건의 쟁점은 {answer_subject}의 성립 여부이다.",
                "cited_fact_ids": [],
                "cited_card_ids": [],
                "cited_authority_comment_ids": [],
                "stated_conclusion": "not_applicable",
            },
            {
                "section_id": "irac_rule",
                "heading": "2. 법리 (Rule)",
                "body": "검토에 적용할 법리는 다음과 같다.\n\n"
                + "\n\n".join(rule_blocks),
                "cited_fact_ids": [],
                "cited_card_ids": card_ids,
                "cited_authority_comment_ids": authority_ids,
                "stated_conclusion": "not_applicable",
            },
            {
                "section_id": "irac_application",
                "heading": "3. 사안의 적용 (Application)",
                "body": "위 법리를 사건 사실에 적용하면 다음과 같다.\n\n"
                + "\n\n".join(application_blocks),
                "cited_fact_ids": fact_ids,
                "cited_card_ids": card_ids,
                "cited_authority_comment_ids": authority_ids,
                "stated_conclusion": "not_applicable",
            },
            {
                "section_id": "irac_conclusion",
                "heading": "4. 결론 (Conclusion)",
                "body": final_sentence,
                "cited_fact_ids": [],
                "cited_card_ids": [],
                "cited_authority_comment_ids": [],
                "stated_conclusion": _overall_section_conclusion(
                    plan["overall_conclusion"]
                ),
            },
        ],
        "overall_conclusion": plan["overall_conclusion"],
        "summary": final_sentence,
    }
    validate_long_form_answer(
        answer,
        case_id=plan["case_id"],
        method_id=method_id,
        allowed_fact_ids=fact_ids,
        allowed_card_ids=card_ids,
        allowed_authority_ids=authority_ids,
    )
    alignment = assess_irac_answer_alignment(answer, plan)
    if alignment:
        raise GenerationContractError([item["message"] for item in alignment])
    return answer


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
    try:
        expected_plan_id = select_fraud_reasoning_plan(
            fact_graph, case=case
        )["plan_id"]
    except ValueError as exc:
        errors.append(str(exc))
        expected_plan_id = ""
    if plan.get("reasoning_plan_id") != expected_plan_id:
        errors.append("IRACPlan reasoning_plan_id differs from composed plan")
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
    observed_deterministic_cards: list[str] = []
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
        for deterministic_rule in unit.get("deterministic_rules", []):
            observed_deterministic_cards.append(
                deterministic_rule.get("card_id", "")
            )
    if len(observed_cards) != len(set(observed_cards)):
        errors.append("IRACPlan contains duplicate cards across units")
    if set(observed_cards) != set(selected_cards):
        errors.append("IRACPlan card coverage differs from selected cards")
    if set(observed_assessments) != assessment_ids:
        errors.append("IRACPlan assessment coverage is incomplete")
    if len(observed_deterministic_cards) != len(set(observed_deterministic_cards)):
        errors.append("IRACPlan contains duplicate deterministic cards")
    try:
        composed = select_fraud_reasoning_plan(fact_graph, case=case)
        composed_cards = {
            card["card_id"]
            for unit in composed["units"]
            for card in unit["cards"]
        }
        expected_deterministic = composed_cards - set(selected_cards)
        if set(observed_deterministic_cards) != expected_deterministic:
            errors.append("IRACPlan deterministic card coverage is incomplete")
    except ValueError:
        pass
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
    actual_ids = [
        section.get("section_id", "") for section in answer.get("sections", [])
    ]
    if any(section_id in WHOLE_IRAC_SECTION_IDS for section_id in actual_ids):
        return _assess_whole_irac_alignment(answer, plan)

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
        required_cards = {
            item["card_id"]
            for item in [*unit["card_assessments"], *unit["deterministic_rules"]]
        }
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
        for card in [*unit["card_assessments"], *unit["deterministic_rules"]]
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
        if not any(claim["fact_ids"] and claim["card_ids"] for claim in claims):
            violations.append(
                {
                    "code": "missing_grounded_application",
                    "section_id": section_id,
                    "message": "section lacks a claim grounded in both facts and rules",
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


def normalize_claim_graph(
    claim_graph: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Remove grammar-backend duplicate IDs without changing claim semantics."""

    normalized = copy.deepcopy(dict(claim_graph))
    changes: list[dict[str, Any]] = []
    for claim in normalized.get("claims", []):
        for field in (
            "fact_ids",
            "card_ids",
            "authority_comment_ids",
            "relation_ids",
        ):
            values = list(claim.get(field, []))
            deduplicated = _ordered_unique(values)
            if deduplicated != values:
                changes.append(
                    {
                        "claim_id": claim.get("claim_id"),
                        "field": field,
                        "before": values,
                        "after": deduplicated,
                    }
                )
                claim[field] = deduplicated
    return normalized, {
        "method": "ordered_unique_provenance_ids",
        "change_count": len(changes),
        "changes": changes,
    }


def normalize_section_patch_bundle(
    patch_bundle: Mapping[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Remove duplicate patch provenance IDs without changing prose or sections."""

    normalized = copy.deepcopy(dict(patch_bundle))
    changes: list[dict[str, Any]] = []
    for patch in normalized.get("patches", []):
        for field in (
            "cited_fact_ids",
            "cited_card_ids",
            "cited_authority_comment_ids",
        ):
            values = list(patch.get(field, []))
            deduplicated = _ordered_unique(values)
            if deduplicated != values:
                changes.append(
                    {
                        "section_id": patch.get("section_id"),
                        "field": field,
                        "before": values,
                        "after": deduplicated,
                    }
                )
                patch[field] = deduplicated
    return normalized, {
        "method": "ordered_unique_patch_provenance_ids",
        "change_count": len(changes),
        "changes": changes,
    }


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
        lines.extend(
            [f"## {section['heading']}", "", _human_visible_body(section["body"]), ""]
        )
    if "irac_conclusion" not in {
        section["section_id"] for section in answer["sections"]
    }:
        lines.extend(["## 종합 결론", "", answer["summary"], ""])
    return "\n".join(lines)


def canonical_sha256(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _human_visible_body(body: str) -> str:
    def replace_parenthetical(match: re.Match[str]) -> str:
        values = [
            value.strip() for value in re.split(r"[,;]", match.group(1))
        ]
        if values and all(
            re.fullmatch(
                r"(?:fact_[0-9]{3}|comm_[^,;\s()]+|"
                r"[a-z][a-z0-9_-]*(?:\.[a-z0-9_-]+)+|"
                r"unknown|satisfied|not_satisfied)",
                value,
            )
            for value in values
        ):
            return ""
        return match.group(0)

    return re.sub(r"\(([^()]*)\)", replace_parenthetical, body)


def _unit_conclusion(
    statuses: Sequence[tuple[str, str]], expected_statuses: Mapping[str, str]
) -> str:
    if any(status == "unknown" for _, status in statuses):
        return "unknown"
    if all(expected_statuses.get(card_id) == status for card_id, status in statuses):
        return "satisfied"
    return "not_satisfied"


def _normalize_legal_sentence(text: str) -> str:
    normalized = re.sub(r"\s+", " ", text.strip())
    normalized = re.sub(r"^[;；,:：·-]+\s*", "", normalized)
    if not normalized:
        raise GenerationContractError(["application bridge is empty after normalization"])
    if normalized[-1] not in ".!?。":
        normalized += "."
    return normalized


def _normalize_application_bridge(card: Mapping[str, Any]) -> str:
    text = _human_visible_body(str(card["application_bridge"]))
    internal_markers = (
        "unresolved_questions",
        "assessment_context",
        "basis_fact_ids",
        "counter_fact_ids",
        "missing_facts",
        "authority_comment_ids",
        "fact_",
        "comm_",
    )
    if not any(marker in text for marker in internal_markers):
        return _normalize_legal_sentence(text)
    if card.get("status") != "unknown":
        raise GenerationContractError(
            [f"application bridge exposes internal metadata for {card.get('card_id')}"]
        )
    missing = [
        re.sub(r"\s+", " ", str(item).strip()).rstrip(".!?。")
        for item in card.get("missing_facts", [])
        if not any(marker in str(item) for marker in internal_markers)
    ]
    if missing:
        details = "”, “".join(missing)
        return (
            f"추가 확인이 필요한 사실 또는 증거는 “{details}”이다. "
            "현재 사실만으로 해당 기준의 충족 여부를 확정할 수 없다."
        )
    return "현재 사실만으로 해당 기준의 충족 여부를 확정할 수 없다."


def _overall_section_conclusion(status: str) -> str:
    mapping = {
        "established": "satisfied",
        "not_established": "not_satisfied",
        "undetermined": "unknown",
        "conflict": "conflict",
    }
    try:
        return mapping[status]
    except KeyError as exc:
        raise GenerationContractError(
            [f"unsupported overall conclusion {status}"]
        ) from exc


def _assess_whole_irac_alignment(
    answer: Mapping[str, Any], plan: Mapping[str, Any]
) -> list[dict[str, str]]:
    violations: list[dict[str, str]] = []
    sections = list(answer.get("sections", []))
    actual_ids = [section.get("section_id", "") for section in sections]
    if actual_ids != list(WHOLE_IRAC_SECTION_IDS):
        violations.append(
            {
                "code": "whole_irac_structure_mismatch",
                "section_id": "document",
                "message": (
                    f"expected sections {list(WHOLE_IRAC_SECTION_IDS)}, got {actual_ids}"
                ),
            }
        )
    sections_by_id = {section.get("section_id", ""): section for section in sections}
    rule = sections_by_id.get("irac_rule", {})
    application = sections_by_id.get("irac_application", {})
    conclusion = sections_by_id.get("irac_conclusion", {})
    required_cards = {
        card["card_id"]
        for unit in plan["units"]
        for card in [*unit["card_assessments"], *unit["deterministic_rules"]]
    }
    required_facts = {
        fact_id for unit in plan["units"] for fact_id in unit["required_fact_ids"]
    }
    required_authorities = {
        authority_id
        for unit in plan["units"]
        for authority_id in unit["required_authority_comment_ids"]
    }
    required_fields = (
        (
            "irac_rule",
            rule,
            (
                ("cited_card_ids", required_cards),
                ("cited_authority_comment_ids", required_authorities),
            ),
        ),
        (
            "irac_application",
            application,
            (
                ("cited_fact_ids", required_facts),
                ("cited_card_ids", required_cards),
                ("cited_authority_comment_ids", required_authorities),
            ),
        ),
    )
    for section_id, section, fields in required_fields:
        for field, required in fields:
            missing = required - set(section.get(field, []))
            if missing:
                violations.append(
                    {
                        "code": "whole_irac_provenance_missing",
                        "section_id": section_id,
                        "message": f"{field} omits {sorted(missing)}",
                    }
                )
    application_body = str(application.get("body", ""))
    for unit in plan["units"]:
        expected_sentence = _section_conclusion_sentence(
            issue=unit["issue"], status=unit["required_conclusion"]
        )
        if unit["issue"] not in application_body or expected_sentence not in application_body:
            violations.append(
                {
                    "code": "whole_irac_application_unit_missing",
                    "section_id": "irac_application",
                    "message": f"application omits compiled unit {unit['unit_id']}",
                }
            )
    expected_conclusion = _overall_section_conclusion(plan["overall_conclusion"])
    if conclusion.get("stated_conclusion") != expected_conclusion:
        violations.append(
            {
                "code": "whole_irac_conclusion_mismatch",
                "section_id": "irac_conclusion",
                "message": (
                    f"expected {expected_conclusion}, got "
                    f"{conclusion.get('stated_conclusion')}"
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


def _section_conclusion_sentence(*, issue: str, status: str) -> str:
    if status == "satisfied":
        return f"따라서 {issue}에 관한 요건은 충족된다."
    if status == "not_satisfied":
        return f"따라서 {issue}에 관한 요건은 충족되지 않는다."
    if status == "unknown":
        return f"따라서 {issue}에 관한 요건은 현재 사실만으로 확정할 수 없다."
    if status == "conflict":
        return f"따라서 {issue}에 관한 판단에는 상충하는 결과가 남는다."
    raise GenerationContractError([f"unsupported IRAC unit conclusion {status}"])


def _overall_conclusion_sentence(*, answer_subject: str, status: str) -> str:
    if status == "established":
        return f"따라서 {answer_subject}는 성립한다."
    if status == "not_established":
        return f"따라서 {answer_subject}는 성립하지 않는다."
    if status == "undetermined":
        return f"따라서 {answer_subject}의 성립 여부는 현재 사실만으로 확정할 수 없다."
    if status == "conflict":
        return f"따라서 {answer_subject}의 성립 여부에는 상충하는 결과가 남는다."
    raise GenerationContractError([f"unsupported overall conclusion {status}"])


def _check_claim_support(
    claim: Mapping[str, Any], violations: list[dict[str, str]]
) -> None:
    requirements = {
        "fact": bool(claim["fact_ids"]),
        "rule": bool(claim["card_ids"] or claim["authority_comment_ids"]),
        "application": bool(claim["fact_ids"] and claim["card_ids"]),
        "conclusion": True,
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
