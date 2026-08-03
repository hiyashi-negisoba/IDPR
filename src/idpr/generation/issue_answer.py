"""Call-3 contract: translate issue assessments and Scallop signals into prose."""

from __future__ import annotations

import json
import re
from collections import defaultdict
from copy import deepcopy
from functools import lru_cache
from pathlib import Path
from typing import Any, Mapping, Sequence

from jsonschema import Draft202012Validator

from idpr.eval.input_formatter import scoped_question_text
from idpr.neural.fact_graph import assessment_facts
from idpr.rulebase.issue_catalog_v2 import ASSESS_ISSUE, STAGE_ISSUE
from idpr.rulebase.qualification import missing_required_base


PROJECT_ROOT = Path(__file__).resolve().parents[3]
SCHEMA_PATH = PROJECT_ROOT / "docs/contracts/issue_long_form_answer.schema.json"
_INTERNAL_ID_RE = re.compile(r"(?:issue_id|fact_id|card_id|art\d+|Scallop)", re.I)


class IssueAnswerError(ValueError):
    def __init__(self, errors: Sequence[str]) -> None:
        self.errors = list(errors)
        super().__init__("; ".join(self.errors))


@lru_cache(maxsize=1)
def issue_answer_schema() -> dict[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def issue_answer_model_schema(request: Mapping[str, Any]) -> dict[str, Any]:
    """Return a prose-only schema; the host owns all provenance identifiers."""
    final_schema = issue_answer_schema()
    section_template = deepcopy(final_schema["properties"]["sections"]["items"])
    for field in (
        "section_id",
        "conclusion",
        "stated_conclusion",
        "cited_fact_ids",
        "cited_issue_ids",
        "cited_rule_ids",
    ):
        section_template["properties"].pop(field)
        section_template["required"].remove(field)
    # Presentation is a deterministic host decision and must not be delegated to prose.
    section_template["properties"].pop("presentation_mode", None)

    analysis_template = deepcopy(section_template["properties"]["analyses"]["items"])
    for field in ("analysis_id", "issue_status"):
        analysis_template["properties"].pop(field)
        analysis_template["required"].remove(field)

    section_schemas: list[dict[str, Any]] = []
    for required in request.get("required_sections", ()):
        schema = deepcopy(section_template)
        # The prose model does not own legal identity.  Constrain the public heading and
        # each issue heading just as tightly as the host-owned opaque ids.  Previously
        # only the array lengths were constrained; a model could reorder headings and the
        # host would then zip a different Scallop conclusion onto the prose by position.
        schema["properties"]["heading"] = {"const": str(required["heading"])}
        issue_schemas: list[dict[str, Any]] = []
        for issue in required.get("issues", ()):
            issue_schema = deepcopy(analysis_template)
            issue_schema["properties"]["heading"] = {
                "const": str(issue["title"])
            }
            issue_schemas.append(issue_schema)
        analysis_count = len(issue_schemas)
        schema["properties"]["analyses"] = {
            "type": "array",
            "minItems": analysis_count,
            "maxItems": analysis_count,
            "prefixItems": issue_schemas,
            "items": False,
        }
        section_schemas.append(schema)

    model_schema = deepcopy(final_schema)
    model_schema["required"].remove("overall_conclusion")
    model_schema["properties"].pop("overall_conclusion")
    model_schema["properties"]["case_id"] = {"const": request["case_id"]}
    model_schema["properties"]["sections"] = {
        "type": "array",
        "minItems": len(section_schemas),
        "maxItems": len(section_schemas),
        "prefixItems": section_schemas,
        "items": False,
    }
    return model_schema


def issue_answer_model_request(request: Mapping[str, Any]) -> dict[str, Any]:
    """Return the visible-only payload sent to Call 3.

    Suppression diagnostics are persisted for audit, but giving their article names back
    to the prose model would defeat suppression by inviting it to mention them anyway.
    """
    payload = deepcopy(dict(request))
    payload.pop("suppressed_sections", None)
    payload.pop("candidate_lifecycle", None)
    return payload


def _host_section_conclusion(planned: Mapping[str, Any]) -> str:
    """Render an offense conclusion from the symbolic directive, not model prose."""
    label = str(planned.get("heading", planned.get("offense", "범죄")))
    directive = str(planned.get("symbolic_directive", ""))
    status = str(planned.get("stated_conclusion", "undetermined"))
    if directive == "attempt_review":
        return f"{label}: 기수는 성립하지 않으며, 미수 성립 및 유형은 추가 검토가 필요하다."
    if directive == "established_but_absorbed":
        return f"{label}: 성립하나 최종 죄수관계에서는 흡수 여부를 반영해야 한다."
    if status == "established":
        return f"{label}: 성립한다."
    if status == "not_established":
        return f"{label}: 성립하지 않는다."
    return f"{label}: 현재 사실관계만으로 성립 여부를 확정할 수 없다."


def attach_issue_answer_provenance(
    answer: Mapping[str, Any], *, request: Mapping[str, Any]
) -> dict[str, Any]:
    """Attach complete section provenance without making the model copy opaque ids."""
    enriched = deepcopy(dict(answer))
    sections = enriched.get("sections", ())
    required = request.get("required_sections", ())
    if not isinstance(sections, list) or len(sections) != len(required):
        return enriched
    for section, planned in zip(sections, required):
        issues = planned.get("issues", ())
        # Legal labels are deterministic request data.  Never retain a model-authored
        # substitute and then attach provenance/conclusions to it by array position.
        section["heading"] = str(planned["heading"])
        section["presentation_mode"] = str(planned.get("presentation_mode", "full"))
        section["section_id"] = str(planned["section_id"])
        analyses = section.get("analyses", ())
        if isinstance(analyses, list) and len(analyses) == len(issues):
            for analysis, issue in zip(analyses, issues):
                analysis["heading"] = str(issue["title"])
                analysis["analysis_id"] = str(issue["issue_id"])
                analysis["issue_status"] = str(issue["status"])
        section["conclusion"] = _host_section_conclusion(planned)
        section["stated_conclusion"] = str(
            planned.get("stated_conclusion", "undetermined")
        )
        section["cited_issue_ids"] = [str(issue["issue_id"]) for issue in issues]
        section["cited_fact_ids"] = sorted(
            {
                str(fact["fact_id"])
                for issue in issues
                for key in ("basis_facts", "counter_facts")
                for fact in issue.get(key, ())
            }
        )
        section["cited_rule_ids"] = sorted(
            {
                str(rule["rule_id"])
                for issue in issues
                for rule in issue.get("rules", ())
            }
        )
    conclusions = []
    for planned in required:
        label = str(planned.get("heading", planned.get("offense", "범죄")))
        status = str(planned.get("stated_conclusion", "undetermined"))
        directive = str(planned.get("symbolic_directive", ""))
        if directive == "attempt_review":
            conclusions.append(f"{label}: 기수 불성립, 미수 여부 검토")
        elif status == "established":
            conclusions.append(f"{label}: 성립")
        elif status == "not_established":
            conclusions.append(f"{label}: 불성립")
        else:
            conclusions.append(f"{label}: 현재 사실관계만으로 성립 여부 미확정")

    article_labels = {
        str(planned.get("article", "")): str(
            planned.get("heading", planned.get("offense", "범죄"))
        )
        for planned in required
    }
    cross = request.get("cross_offense_directives", {})
    for article in cross.get("absorbed_articles", ()):
        if str(article) in article_labels:
            conclusions.append(f"{article_labels[str(article)]}: 흡수로 별도 최종 죄명에서 제외")
    for pair in cross.get("concurrent_pairs", ()):
        left = article_labels.get(str(pair.get("left_article", "")))
        right = article_labels.get(str(pair.get("right_article", "")))
        if left and right:
            conclusions.append(f"{left}와 {right}: 경합관계")
    enriched["overall_conclusion"] = (
        "; ".join(conclusions) + "."
        if conclusions
        else "현재 제공된 사실과 검수된 법리만으로 독립하여 논증할 죄명을 특정할 수 없다."
    )
    return enriched


def _relation_rows(packet: Mapping[str, Any], relation: str) -> list[list[str]]:
    runtime = packet.get("symbolic_runtime", {})
    relations = runtime.get("relations", {}) if isinstance(runtime, Mapping) else {}
    rows = relations.get(relation, ()) if isinstance(relations, Mapping) else ()
    if not isinstance(rows, Sequence) or isinstance(rows, (str, bytes)):
        raise IssueAnswerError([f"symbolic relation {relation} must be an array"])
    return [
        list(map(str, row))
        for row in rows
        if isinstance(row, Sequence) and not isinstance(row, (str, bytes))
    ]


def _article_set(packet: Mapping[str, Any], relation: str) -> set[str]:
    return {row[1] for row in _relation_rows(packet, relation) if len(row) >= 2}


def _relation_issue_sets(
    packet: Mapping[str, Any], relation: str
) -> dict[str, set[str]]:
    grouped: dict[str, set[str]] = defaultdict(set)
    for row in _relation_rows(packet, relation):
        if len(row) >= 3:
            grouped[row[1]].add(row[2])
    return grouped


def _fact_context(fact_graph: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for fact in assessment_facts(fact_graph):
        assertion = fact.get("assertion", {})
        source_quote = assertion.get("source_quote", "") if isinstance(assertion, Mapping) else ""
        result[str(fact["fact_id"])] = {
            "fact_id": str(fact["fact_id"]),
            "kind": str(fact.get("kind", "")),
            "statement": str(source_quote),
        }
    return result


def _directive(
    article: str,
    *,
    final: set[str],
    established: set[str],
    undetermined: set[str],
    unaddressed: set[str],
    attempts: set[str],
    stage_unresolved: set[str],
    absorbed: set[str],
) -> tuple[str, str]:
    if article in attempts:
        return "attempt_review", "undetermined"
    if article in stage_unresolved:
        return "stage_unresolved", "undetermined"
    if article in undetermined or article in unaddressed:
        return "undetermined", "undetermined"
    if article in absorbed:
        return "established_but_absorbed", "established"
    if article in final:
        return "final_offense_candidate", "established"
    if article in established:
        return "established_candidate", "established"
    return "no_symbolic_conclusion", "undetermined"


def _presentation(
    article: str,
    *,
    directive: str,
    supported_issues: Mapping[str, set[str]],
    refuted_issues: Mapping[str, set[str]],
    grounded_issue_count: int,
    missing_bases: frozenset[str],
    relevance: str = "optional",
    sources: Sequence[str] = (),
) -> tuple[str | None, str]:
    """Choose answer salience without deleting any upstream assessment.

    ``None`` means the article stays in the request diagnostics but is not exposed as an
    answer section.  Counts compare assessed issue groups, not raw retrieved cards, so a
    verbose commentary chapter does not win merely by having more cards.
    """
    supported = len(supported_issues.get(article, ()))
    refuted = len(refuted_issues.get(article, ()))
    if missing_bases:
        if relevance == "must_discuss":
            return "compact", "must_discuss_missing_required_base_offense"
        # Keep a grounded optional result-aggravated candidate found by retrieval as a
        # bounded base/result relationship review.  Mandatory sources were handled
        # above; this branch only governs candidates still subject to the material gate.
        if "retrieval_selected" in sources and grounded_issue_count > 0:
            return "compact", "grounded_result_offense_requires_base_review"
        return None, "missing_required_base_offense"
    if directive in {"final_offense_candidate", "established_candidate"}:
        return "full", "symbolically_established"
    if supported == 0:
        if relevance == "must_discuss":
            return "compact", "must_discuss_no_positive_element_support"
        return None, "no_positive_element_support"
    if refuted >= supported:
        if relevance == "must_discuss":
            return "compact", "must_discuss_explicit_element_refutation"
        return None, "explicit_element_refutation_dominates"
    # A single isolated proposition is enough to keep an offence in symbolic review, but
    # not enough to introduce an unresolved alternative in a reader-facing answer.  This
    # gate applies only to non-established candidates; simple established offences remain
    # unaffected.
    if grounded_issue_count < 2:
        if relevance == "must_discuss":
            return "compact", "must_discuss_insufficient_material_grounding"
        return None, "insufficient_material_grounding"
    return "compact", "partially_supported_or_unresolved"


def _provenance_by_article(
    reasoning_packet: Mapping[str, Any], *, articles: Sequence[str]
) -> dict[str, dict[str, Any]]:
    """Validate the candidate-source handoff and support legacy diagnostic packets."""
    rows = reasoning_packet.get("article_provenance")
    if rows is None:
        return {
            article: {
                "article": article,
                "sources": ["legacy_unspecified"],
                "relevance": "optional",
                "relevance_reason": "legacy_packet_without_provenance",
            }
            for article in articles
        }
    if not isinstance(rows, Sequence) or isinstance(rows, (str, bytes)):
        raise IssueAnswerError(["reasoning_packet.article_provenance must be an array"])
    indexed: dict[str, dict[str, Any]] = {}
    errors: list[str] = []
    for index, raw in enumerate(rows):
        if not isinstance(raw, Mapping):
            errors.append(f"article_provenance[{index}] must be an object")
            continue
        article = str(raw.get("article", ""))
        if not article or article in indexed:
            errors.append(f"article_provenance[{index}] has a missing or duplicate article")
            continue
        sources = raw.get("sources", ())
        relevance = str(raw.get("relevance", ""))
        if not isinstance(sources, Sequence) or isinstance(sources, (str, bytes)):
            errors.append(f"article_provenance[{index}].sources must be an array")
            continue
        if relevance not in {"must_discuss", "optional", "irrelevant"}:
            errors.append(f"article_provenance[{index}] has invalid relevance")
            continue
        indexed[article] = {
            "article": article,
            "sources": [str(source) for source in sources],
            "relevance": relevance,
            "relevance_reason": str(raw.get("relevance_reason", "")),
        }
    missing = sorted(set(articles) - set(indexed))
    extra = sorted(set(indexed) - set(articles))
    if missing:
        errors.append(f"article_provenance is missing articles: {missing}")
    if extra:
        errors.append(f"article_provenance has unknown articles: {extra}")
    if errors:
        raise IssueAnswerError(errors)
    return indexed


def _verdict(
    *, directive: str, supported: int, refuted: int, stated_conclusion: str
) -> str:
    if directive == "attempt_review":
        return "attempt_review"
    if stated_conclusion == "established":
        return "established"
    if refuted > 0 and supported == 0:
        return "not_established"
    return "unknown"


def build_call3_request(
    *,
    case: Mapping[str, Any],
    fact_graph: Mapping[str, Any],
    reasoning_packet: Mapping[str, Any],
) -> dict[str, Any]:
    """Build a rubric-free, prose-oriented view of the symbolic pipeline output."""
    case_id = str(case.get("sub_question_id", case.get("case_id", "")))
    if not case_id or reasoning_packet.get("case_id") != case_id:
        raise IssueAnswerError(["case and reasoning packet ids differ"])
    facts = _fact_context(fact_graph)
    issues = reasoning_packet.get("issues", ())
    if not isinstance(issues, Sequence) or isinstance(issues, (str, bytes)):
        raise IssueAnswerError(["reasoning_packet.issues must be an array"])
    packet_articles = [str(article) for article in reasoning_packet.get("articles", ())]
    if not packet_articles:
        packet_articles = list(
            dict.fromkeys(
                str(issue.get("article", ""))
                for issue in issues
                if isinstance(issue, Mapping) and issue.get("article")
            )
        )
    if len(packet_articles) != len(set(packet_articles)):
        raise IssueAnswerError(["reasoning_packet.articles must be unique"])
    provenance = _provenance_by_article(
        reasoning_packet, articles=packet_articles
    )

    final = _article_set(reasoning_packet, "final_offense")
    established = _article_set(reasoning_packet, "offense_established")
    undetermined = _article_set(reasoning_packet, "offense_undetermined")
    unaddressed = _article_set(reasoning_packet, "element_unaddressed")
    attempts = _article_set(reasoning_packet, "attempt_to_consider")
    stage_unresolved = _article_set(reasoning_packet, "offense_stage_unresolved")
    absorbed = _article_set(reasoning_packet, "is_absorbed")
    concurrence = [
        {"left_article": row[1], "right_article": row[2]}
        for row in _relation_rows(reasoning_packet, "concurrent_offenses")
        if len(row) >= 3
    ]
    supported_issues = _relation_issue_sets(reasoning_packet, "element_supported")
    refuted_issues = _relation_issue_sets(reasoning_packet, "element_refuted")
    established_without_gaps = established - unaddressed

    all_grouped: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    grouped: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    article_order: list[str] = []
    for issue in issues:
        if not isinstance(issue, Mapping):
            raise IssueAnswerError(["reasoning_packet contains a non-object issue"])
        article = str(issue.get("article", ""))
        all_grouped[article].append(issue)
        include = issue.get("include_in_generation")
        if include is None:
            include = (
                issue.get("runtime") == ASSESS_ISSUE
                or issue.get("status") != "unknown"
                or issue.get("function") == STAGE_ISSUE
                or issue.get("symbolic_condition") is True
            )
        if not include:
            # An unsupported deferred possibility (for example an unmentioned extra
            # victim or camera offence) is retrieval noise, not an IRAC issue. Initial
            # constituent elements remain mandatory even when unknown.
            continue
        if article not in grouped:
            article_order.append(article)
        grouped[article].append(issue)

    required_sections: list[dict[str, Any]] = []
    suppressed_sections: list[dict[str, Any]] = []
    allowed_facts: set[str] = set()
    allowed_issues: set[str] = set()
    allowed_rules: set[str] = set()
    for article in article_order:
        article_issues: list[dict[str, Any]] = []
        article_label = str(grouped[article][0].get("article_label", article))
        offense = str(grouped[article][0].get("offense", article_label))
        article_provenance = provenance[article]
        relevance = str(article_provenance["relevance"])
        directive, stated_conclusion = _directive(
            article,
            final=final,
            established=established,
            undetermined=undetermined,
            unaddressed=unaddressed,
            attempts=attempts,
            stage_unresolved=stage_unresolved,
            absorbed=absorbed,
        )
        missing_bases = missing_required_base(
            article, established_without_gaps=established_without_gaps
        )
        grounded_issue_count = sum(
            issue.get("status") != "unknown"
            and bool(issue.get("basis_fact_ids") or issue.get("counter_fact_ids"))
            for issue in grouped[article]
        )
        presentation_mode, visibility_reason = _presentation(
            article,
            directive=directive,
            supported_issues=supported_issues,
            refuted_issues=refuted_issues,
            grounded_issue_count=grounded_issue_count,
            missing_bases=missing_bases,
            relevance=relevance,
            sources=article_provenance["sources"],
        )
        supported_count = len(supported_issues.get(article, ()))
        refuted_count = len(refuted_issues.get(article, ()))
        verdict = _verdict(
            directive=directive,
            supported=supported_count,
            refuted=refuted_count,
            stated_conclusion=stated_conclusion,
        )
        if presentation_mode is None:
            suppressed_sections.append(
                {
                    "article": article,
                    "article_label": article_label,
                    "offense": offense,
                    "reason": visibility_reason,
                    "provenance": article_provenance,
                    "relevance": relevance,
                    "verdict": verdict,
                    "symbolic_directive": directive,
                    "supported_issue_count": supported_count,
                    "refuted_issue_count": refuted_count,
                    "grounded_issue_count": grounded_issue_count,
                    "required_base_articles": sorted(missing_bases),
                }
            )
            continue
        for issue in grouped[article]:
            issue_id = str(issue["issue_id"])
            basis_ids = [str(item) for item in issue.get("basis_fact_ids", ())]
            counter_ids = [str(item) for item in issue.get("counter_fact_ids", ())]
            unknown_facts = sorted((set(basis_ids) | set(counter_ids)) - set(facts))
            if unknown_facts:
                raise IssueAnswerError(
                    [f"{issue_id}: assessment refers to unknown facts {unknown_facts}"]
                )
            rules = [
                {
                    "rule_id": str(rule["rule_id"]),
                    "proposition": str(rule["proposition"]),
                    "rule_type": "anchor" if key == "anchor_rules" else "detail",
                    "basis_card_ids": [
                        str(card_id) for card_id in rule.get("basis_card_ids", ())
                    ],
                    "origin": str(rule.get("origin", "reviewed_card")),
                }
                for key in ("anchor_rules", "detail_rules")
                for rule in issue.get(key, ())
            ]
            rule_ids = [rule["rule_id"] for rule in rules]
            allowed_facts.update((*basis_ids, *counter_ids))
            allowed_issues.add(issue_id)
            allowed_rules.update(rule_ids)
            article_issues.append(
                {
                    "issue_id": issue_id,
                    "title": str(issue.get("title", "")),
                    "function": str(issue.get("function", "element_issue")),
                    "status": str(issue.get("status", "unknown")),
                    "rules": rules,
                    "basis_facts": [facts[fact_id] for fact_id in basis_ids],
                    "counter_facts": [facts[fact_id] for fact_id in counter_ids],
                    "missing_facts": [str(item) for item in issue.get("missing_facts", ())],
                }
            )
        required_sections.append(
            {
                "section_id": f"offense_{article.replace('-', '_').replace('.', '_')}",
                "heading": f"{article_label} {offense}",
                "article_label": article_label,
                "article": article,
                "offense": offense,
                "symbolic_directive": directive,
                "stated_conclusion": stated_conclusion,
                "provenance": article_provenance,
                "relevance": relevance,
                "verdict": verdict,
                "presentation_mode": presentation_mode,
                "visibility_reason": visibility_reason,
                "issues": article_issues,
            }
        )

    represented = {
        str(section["article"])
        for section in (*required_sections, *suppressed_sections)
    }
    for article in packet_articles:
        if article in represented:
            continue
        candidates = all_grouped.get(article, ())
        article_label = str(candidates[0].get("article_label", article)) if candidates else article
        offense = str(candidates[0].get("offense", article_label)) if candidates else article_label
        directive, stated_conclusion = _directive(
            article,
            final=final,
            established=established,
            undetermined=undetermined,
            unaddressed=unaddressed,
            attempts=attempts,
            stage_unresolved=stage_unresolved,
            absorbed=absorbed,
        )
        suppressed_sections.append(
            {
                "article": article,
                "article_label": article_label,
                "offense": offense,
                "reason": "no_generation_issues",
                "provenance": provenance[article],
                "relevance": str(provenance[article]["relevance"]),
                "verdict": _verdict(
                    directive=directive,
                    supported=len(supported_issues.get(article, ())),
                    refuted=len(refuted_issues.get(article, ())),
                    stated_conclusion=stated_conclusion,
                ),
                "symbolic_directive": directive,
                "supported_issue_count": len(supported_issues.get(article, ())),
                "refuted_issue_count": len(refuted_issues.get(article, ())),
                "grounded_issue_count": 0,
                "required_base_articles": [],
            }
        )

    required_by_article = {
        str(section["article"]): section for section in required_sections
    }
    suppressed_by_article = {
        str(section["article"]): section for section in suppressed_sections
    }
    candidate_lifecycle: list[dict[str, Any]] = []
    for article in packet_articles:
        included = article in required_by_article
        decision = required_by_article.get(article) or suppressed_by_article[article]
        status_counts: dict[str, int] = defaultdict(int)
        for issue in all_grouped.get(article, ()):
            status_counts[str(issue.get("status", "unknown"))] += 1
        candidate_lifecycle.append(
            {
                "article": article,
                "provenance": provenance[article],
                "relevance": str(provenance[article]["relevance"]),
                "call2_status_counts": dict(status_counts),
                "symbolic_directive": str(decision["symbolic_directive"]),
                "verdict": str(decision["verdict"]),
                "visibility_decision": (
                    str(decision["presentation_mode"]) if included else "hidden"
                ),
                "visibility_reason": str(
                    decision.get("visibility_reason", decision.get("reason", ""))
                ),
                "included_in_call3": included,
            }
        )
    hidden_mandatory = [
        row["article"]
        for row in candidate_lifecycle
        if row["relevance"] == "must_discuss" and not row["included_in_call3"]
    ]
    if hidden_mandatory:
        raise IssueAnswerError(
            [f"must_discuss articles were hidden: {hidden_mandatory}"]
        )

    question_prompt = str(case.get("question_prompt", ""))
    return {
        "version": "1.0.0",
        "task": "write_issue_scallop_criminal_answer",
        "case_id": case_id,
        "question_text": scoped_question_text(
            str(case.get("question_text", case.get("case_text", ""))),
            question_prompt,
        ),
        "question_prompt": question_prompt,
        "legal_knowledge_policy": "supplied_reviewed_rules_only",
        "rubric_supplied": False,
        "required_sections": required_sections,
        "suppressed_sections": suppressed_sections,
        "candidate_lifecycle": candidate_lifecycle,
        "cross_offense_directives": {
            "absorbed_articles": sorted(absorbed),
            "concurrent_pairs": concurrence,
        },
        "allowed_provenance_ids": {
            "fact_ids": sorted(allowed_facts),
            "issue_ids": sorted(allowed_issues),
            "rule_ids": sorted(allowed_rules),
        },
    }


def validate_issue_answer(
    answer: Mapping[str, Any], *, request: Mapping[str, Any]
) -> None:
    errors = [
        f"{'.'.join(map(str, error.absolute_path)) or '$'}: {error.message}"
        for error in Draft202012Validator(issue_answer_schema()).iter_errors(answer)
    ]
    if answer.get("case_id") != request.get("case_id"):
        errors.append("answer case_id differs from request")
    required = list(request.get("required_sections", ()))
    sections = list(answer.get("sections", ()))
    if [section.get("section_id") for section in sections] != [
        section.get("section_id") for section in required
    ]:
        errors.append("answer sections differ from the required order")
    allowed = request.get("allowed_provenance_ids", {})
    for index, section in enumerate(sections):
        if index < len(required) and section.get("stated_conclusion") != required[index].get(
            "stated_conclusion"
        ):
            errors.append(f"sections[{index}].stated_conclusion differs from Scallop directive")
        if index < len(required):
            if section.get("presentation_mode", "full") != required[index].get(
                "presentation_mode", "full"
            ):
                errors.append(
                    f"sections[{index}].presentation_mode differs from the answer plan"
                )
            if section.get("heading") != required[index].get("heading"):
                errors.append(
                    f"sections[{index}].heading differs from the planned offense"
                )
            expected_issue_ids = {
                str(issue["issue_id"]) for issue in required[index].get("issues", ())
            }
            analyses = section.get("analyses", ())
            if [analysis.get("analysis_id") for analysis in analyses] != [
                issue["issue_id"] for issue in required[index].get("issues", ())
            ]:
                errors.append(
                    f"sections[{index}].analyses differ from the planned issue order"
                )
            for analysis_index, analysis in enumerate(analyses):
                planned_issues = required[index].get("issues", ())
                if (
                    analysis_index < len(planned_issues)
                    and analysis.get("issue_status")
                    != planned_issues[analysis_index].get("status")
                ):
                    errors.append(
                        f"sections[{index}].analyses[{analysis_index}].issue_status "
                        "differs from Call-2 assessment"
                    )
                if (
                    analysis_index < len(planned_issues)
                    and analysis.get("heading")
                    != planned_issues[analysis_index].get("title")
                ):
                    errors.append(
                        f"sections[{index}].analyses[{analysis_index}].heading "
                        "differs from the planned issue"
                    )
                for field in ("heading", "issue", "rule", "application", "conclusion"):
                    if _INTERNAL_ID_RE.search(str(analysis.get(field, ""))):
                        errors.append(
                            f"sections[{index}].analyses[{analysis_index}].{field} "
                            "leaks an internal identifier"
                        )
            if set(section.get("cited_issue_ids", ())) != expected_issue_ids:
                errors.append(
                    f"sections[{index}].cited_issue_ids must cover every planned issue"
                )
            required_fact_ids = {
                str(fact["fact_id"])
                for issue in required[index].get("issues", ())
                for key in ("basis_facts", "counter_facts")
                for fact in issue.get(key, ())
            }
            if not required_fact_ids <= set(section.get("cited_fact_ids", ())):
                errors.append(
                    f"sections[{index}].cited_fact_ids omit assessed evidence"
                )
            required_anchor_ids = {
                str(rule["rule_id"])
                for issue in required[index].get("issues", ())
                for rule in issue.get("rules", ())
                if rule.get("rule_type") == "anchor"
            }
            if not required_anchor_ids <= set(section.get("cited_rule_ids", ())):
                errors.append(
                    f"sections[{index}].cited_rule_ids omit reviewed anchor rules"
                )
        for field, allowed_field in (
            ("cited_fact_ids", "fact_ids"),
            ("cited_issue_ids", "issue_ids"),
            ("cited_rule_ids", "rule_ids"),
        ):
            outside = set(section.get(field, ())) - set(allowed.get(allowed_field, ()))
            if outside:
                errors.append(f"sections[{index}].{field} contains unknown ids {sorted(outside)}")
        for field in ("heading", "conclusion"):
            if _INTERNAL_ID_RE.search(str(section.get(field, ""))):
                errors.append(f"sections[{index}].{field} leaks an internal identifier")
    if errors:
        raise IssueAnswerError(errors)


def render_issue_answer_markdown(answer: Mapping[str, Any]) -> str:
    lines = [f"# {answer['title']}", ""]
    full_sections = [
        section
        for section in answer["sections"]
        if section.get("presentation_mode", "full") == "full"
    ]
    compact_sections = [
        section
        for section in answer["sections"]
        if section.get("presentation_mode") == "compact"
    ]
    for section in full_sections:
        lines.extend((f"## {section['heading']}", ""))

        lines.extend(("### 쟁점 (Issue)", ""))
        for analysis in section["analyses"]:
            lines.extend(
                (
                    f"- **{analysis['heading']}**: {analysis['issue']}",
                )
            )

        lines.extend(("", "### 법리 (Rule)", ""))
        for analysis in section["analyses"]:
            lines.extend(
                (
                    f"#### {analysis['heading']}",
                    "",
                    str(analysis["rule"]),
                    "",
                )
            )

        lines.extend(("### 사안의 적용 (Application)", ""))
        for analysis in section["analyses"]:
            lines.extend(
                (
                    f"#### {analysis['heading']}",
                    "",
                    str(analysis["application"]),
                    "",
                    f"**소결:** {analysis['conclusion']}",
                    "",
                )
            )

        lines.extend((f"### 결론 (Conclusion)\n\n{section['conclusion']}", ""))

    if compact_sections:
        lines.extend(("## 보충적 검토", ""))
        for section in compact_sections:
            lines.extend((f"### {section['heading']}", ""))
            for analysis in section["analyses"]:
                if analysis.get("issue_status") != "satisfied":
                    continue
                lines.extend(
                    (
                        f"- **{analysis['heading']}**: {analysis['application']} "
                        f"{analysis['conclusion']}",
                    )
                )
            lines.extend(("", str(section["conclusion"]), ""))
    lines.extend(("## 종합 결론", "", str(answer["overall_conclusion"]), ""))
    return "\n".join(lines)
