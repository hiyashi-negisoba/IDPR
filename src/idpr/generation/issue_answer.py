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

from idpr.neural.fact_graph import assessment_facts
from idpr.rulebase.issue_catalog_v2 import ASSESS_ISSUE, STAGE_ISSUE


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
        "conclusion",
        "stated_conclusion",
        "cited_fact_ids",
        "cited_issue_ids",
        "cited_rule_ids",
    ):
        section_template["properties"].pop(field)
        section_template["required"].remove(field)

    section_schemas: list[dict[str, Any]] = []
    for required in request.get("required_sections", ()):
        schema = deepcopy(section_template)
        schema["properties"]["section_id"] = {"const": required["section_id"]}
        analysis_template = deepcopy(schema["properties"]["analyses"]["items"])
        analyses = []
        for issue in required.get("issues", ()):
            analysis = deepcopy(analysis_template)
            analysis["properties"]["analysis_id"] = {"const": issue["issue_id"]}
            analysis["properties"]["issue_status"] = {"const": issue["status"]}
            analyses.append(analysis)
        schema["properties"]["analyses"] = {
            "type": "array",
            "minItems": len(analyses),
            "maxItems": len(analyses),
            "prefixItems": analyses,
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
    enriched["overall_conclusion"] = "; ".join(conclusions) + "."
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
    absorbed: set[str],
) -> tuple[str, str]:
    if article in attempts:
        return "attempt_review", "undetermined"
    if article in undetermined or article in unaddressed:
        return "undetermined", "undetermined"
    if article in absorbed:
        return "established_but_absorbed", "established"
    if article in final:
        return "final_offense_candidate", "established"
    if article in established:
        return "established_candidate", "established"
    return "no_symbolic_conclusion", "undetermined"


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

    final = _article_set(reasoning_packet, "final_offense")
    established = _article_set(reasoning_packet, "offense_established")
    undetermined = _article_set(reasoning_packet, "offense_undetermined")
    unaddressed = _article_set(reasoning_packet, "element_unaddressed")
    attempts = _article_set(reasoning_packet, "attempt_to_consider")
    absorbed = _article_set(reasoning_packet, "is_absorbed")
    concurrence = [
        {"left_article": row[1], "right_article": row[2]}
        for row in _relation_rows(reasoning_packet, "concurrent_offenses")
        if len(row) >= 3
    ]

    grouped: dict[str, list[Mapping[str, Any]]] = defaultdict(list)
    article_order: list[str] = []
    for issue in issues:
        if not isinstance(issue, Mapping):
            raise IssueAnswerError(["reasoning_packet contains a non-object issue"])
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
        article = str(issue.get("article", ""))
        if article not in grouped:
            article_order.append(article)
        grouped[article].append(issue)

    required_sections: list[dict[str, Any]] = []
    allowed_facts: set[str] = set()
    allowed_issues: set[str] = set()
    allowed_rules: set[str] = set()
    for article in article_order:
        article_issues: list[dict[str, Any]] = []
        article_label = str(grouped[article][0].get("article_label", article))
        offense = str(grouped[article][0].get("offense", article_label))
        directive, stated_conclusion = _directive(
            article,
            final=final,
            established=established,
            undetermined=undetermined,
            unaddressed=unaddressed,
            attempts=attempts,
            absorbed=absorbed,
        )
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
                "issues": article_issues,
            }
        )

    return {
        "version": "1.0.0",
        "task": "write_issue_scallop_criminal_answer",
        "case_id": case_id,
        "question_text": str(case.get("question_text", case.get("case_text", ""))),
        "question_prompt": str(case.get("question_prompt", "")),
        "legal_knowledge_policy": "supplied_reviewed_rules_only",
        "rubric_supplied": False,
        "required_sections": required_sections,
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
    for section in answer["sections"]:
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
    lines.extend(("## 종합 결론", "", str(answer["overall_conclusion"]), ""))
    return "\n".join(lines)
