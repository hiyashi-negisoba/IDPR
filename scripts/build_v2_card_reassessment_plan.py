"""Build the full KCL-26 atomic Call 2-R plan from existing UNKNOWN assessments."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from collections import Counter, defaultdict
from collections.abc import Mapping
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.retrieval import (
    LexicalIndex,
    retrieve_candidate_issues_from_cards,
    retrieve_issue_cards,
)
from idpr.rulebase.card_catalog_v2 import compile_card_catalog_v2
from idpr.rulebase.cards import card_corpus
from idpr.rulebase.issue_catalog_v2 import (
    ELEMENT_ISSUE,
    STAGE_ISSUE,
    compile_issue_catalog_v2,
)
from idpr.v2.question_assumptions import load_question_assumptions
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.card_issue_bridge import (
    EXACT_AUTHORED_IDENTITY,
    project_offense_articles,
)
from idpr.v2.runtime.card_reassessment import LegalMaterial
from idpr.v2.runtime.grounding import AssessmentTarget, predicate_definitions
from idpr.v2.runtime.identity import OffenseInstanceKey


def _rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _instance(value: Mapping[str, Any]) -> OffenseInstanceKey:
    return OffenseInstanceKey(
        str(value["case_id"]),
        str(value["actor_id"]),
        str(value["offense_ref"]),
        str(value["occurrence_id"]),
    )


def _target(value: Mapping[str, Any]) -> AssessmentTarget:
    return AssessmentTarget(_instance(value["instance_key"]), str(value["predicate_ref"]))


def _target_dict(target: AssessmentTarget) -> dict[str, Any]:
    return target.as_dict()


def _ground_key(target: AssessmentTarget) -> tuple[str, str, str, str]:
    instance = target.instance_key
    return (
        instance.case_id,
        instance.actor_id,
        instance.occurrence_id,
        target.predicate_ref,
    )


def build_plan(
    *,
    definitions: Path,
    planner_path: Path,
    call2_path: Path,
    inventory_path: Path,
    assumptions_path: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    registry = load_definitions(definitions)
    corpus = card_corpus()
    issues, _ = compile_issue_catalog_v2(corpus)
    catalog = compile_card_catalog_v2(corpus)
    card_reviewed = {value.card_id: not value.review_required for value in catalog}
    detail_lexical = LexicalIndex.build(tuple(card.proposition for card in corpus.cards))
    planner_rows = {row["sub_question_id"]: row for row in _rows(planner_path)}
    call2_rows = {row["sub_question_id"]: row for row in _rows(call2_path)}
    inventory = {row["sub_question_id"]: row for row in _rows(inventory_path)}
    assumptions = load_question_assumptions(
        assumptions_path,
        question_prompt_by_id={
            case_id: str(row["question_prompt"]) for case_id, row in inventory.items()
        },
    )
    if set(planner_rows) != set(call2_rows):
        raise ValueError("planner and Call 2 case universes differ")

    output: list[dict[str, Any]] = []
    skip_counts: Counter[str] = Counter()
    function_counts: Counter[str] = Counter()
    material_role_counts: Counter[str] = Counter()
    projected_target_count = 0

    for case_id, plan in planner_rows.items():
        occurrence_by_id = {
            str(value["occurrence_id"]): value for value in plan["occurrences"]
        }
        top_level = {_instance(value) for value in plan["top_level_instances"]}
        raw_assessments = call2_rows[case_id]["assessments"]
        unknown_targets = tuple(
            _target(value) for value in raw_assessments if value["truth"] == "UNKNOWN"
        )
        unknown_set = set(unknown_targets)
        ground_projection: dict[tuple[str, str, str, str], list[AssessmentTarget]] = (
            defaultdict(list)
        )
        for target in unknown_targets:
            if registry.kind_of(target.predicate_ref) == "ground_fact":
                ground_projection[_ground_key(target)].append(target)

        selected: list[tuple[AssessmentTarget, tuple[AssessmentTarget, ...]]] = []
        handled_ground: set[tuple[str, str, str, str]] = set()
        for target in unknown_targets:
            if target.instance_key not in top_level:
                skip_counts["NOT_TOP_LEVEL_INSTANCE"] += 1
                continue
            projection = project_offense_articles(registry, target.instance_key.offense_ref)
            if projection.status != EXACT_AUTHORED_IDENTITY:
                skip_counts[projection.status] += 1
                continue
            if registry.kind_of(target.predicate_ref) == "ground_fact":
                key = _ground_key(target)
                if key in handled_ground:
                    continue
                handled_ground.add(key)
                projection_targets = tuple(ground_projection[key])
            else:
                projection_targets = (target,)
            if any(value not in unknown_set for value in projection_targets):
                raise AssertionError("ground projection crossed the UNKNOWN universe")
            selected.append((target, projection_targets))

        case_recoveries: list[dict[str, Any]] = []
        for target, projection_targets in selected:
            instance = target.instance_key
            occurrence = occurrence_by_id.get(instance.occurrence_id)
            if occurrence is None:
                skip_counts["MISSING_PLANNER_OCCURRENCE"] += 1
                continue
            predicate = predicate_definitions(registry, (target.predicate_ref,))[0]
            projection = project_offense_articles(registry, instance.offense_ref)
            scoped = tuple(
                issue
                for issue in issues
                if issue.article in projection.article_keys
                and issue.function in {ELEMENT_ISSUE, STAGE_ISSUE}
                and not issue.review_required
            )
            if not scoped:
                skip_counts["NO_REVIEWED_ELEMENT_OR_STAGE_ISSUE"] += 1
                continue
            # Parent-issue selection is a legal-concept join.  Including the long factual
            # episode here lets incidental case vocabulary pull a predicate such as intent
            # into an unrelated omission issue.  Facts enter only the subordinate-card
            # retrieval below, after the reviewed parent issue is fixed.
            focus = " ".join(
                value
                for value in (
                    predicate.canonical_meaning,
                    predicate.legal_standard or "",
                )
                if value
            )
            issue_result = retrieve_candidate_issues_from_cards(
                (focus,),
                corpus=corpus,
                issues=scoped,
                top_k_issues=1,
            )
            if not issue_result.retrieved_issue_ids:
                skip_counts["NO_RETRIEVED_ISSUE"] += 1
                continue
            issue_by_id = {value.issue_id: value for value in scoped}
            issue = issue_by_id[issue_result.retrieved_issue_ids[0]]
            details = retrieve_issue_cards(
                (issue,),
                (
                    {
                        "assertion": {
                            "source_quote": str(occurrence["source_text"]),
                        }
                    },
                ),
                focus_by_issue={
                    issue.issue_id: tuple(
                        value
                        for value in (
                            predicate.canonical_meaning,
                            predicate.legal_standard or "",
                        )
                        if value
                    )
                },
                corpus=corpus,
                top_k_per_issue=4,
                lexical=detail_lexical,
            ).by_issue[issue.issue_id]
            detail_ids = tuple(
                value for value in details.card_ids if card_reviewed.get(value, False)
            )[:2]
            materials: list[LegalMaterial] = []
            for card_id in issue.anchor_card_ids:
                if card_reviewed.get(card_id, False):
                    materials.append(
                        LegalMaterial(
                            card_id,
                            corpus.by_id[card_id].proposition,
                            "anchor_rule",
                            (card_id,),
                        )
                    )
            for rule in issue.reviewed_anchor_rules:
                materials.append(
                    LegalMaterial(
                        rule.rule_id,
                        rule.proposition,
                        "reviewed_rule",
                        rule.basis_card_ids,
                    )
                )
            for card_id in detail_ids:
                materials.append(
                    LegalMaterial(
                        card_id,
                        corpus.by_id[card_id].proposition,
                        "retrieved_detail",
                        (card_id,),
                    )
                )
            if not materials:
                skip_counts["NO_REVIEWED_LEGAL_MATERIAL"] += 1
                continue
            payload = issue.model_payload(corpus.by_id)
            recovery_id = f"{case_id}:card_r:{len(case_recoveries) + 1:03d}"
            row = {
                "recovery_id": recovery_id,
                "assessment_target": _target_dict(target),
                "projection_targets": [
                    _target_dict(value) for value in projection_targets
                ],
                "original_truth": "UNKNOWN",
                "evidence_occurrence": occurrence,
                "question_assumptions": [
                    value.as_dict() for value in assumptions.get(case_id, ())
                ],
                "predicate_definition": predicate.as_dict(),
                "reviewed_issue": {
                    "issue_id": issue.issue_id,
                    "article": issue.article,
                    "function": issue.function,
                    "question": payload["question"],
                    "retrieval_score": issue_result.issue_scores[issue.issue_id],
                    "legal_materials": [value.as_dict() for value in materials],
                },
                "selection_provenance": {
                    "article_join": EXACT_AUTHORED_IDENTITY,
                    "issue_selection": "PREDICATE_ONLY_BM25_WITHIN_EXACT_ARTICLE_ELEMENT_STAGE_SCOPE",
                    "detail_selection": "BM25_WITHIN_REVIEWED_PARENT_ISSUE",
                    "symbolic_effect": "NONE_CANDIDATE_CONTEXT_ONLY",
                },
            }
            case_recoveries.append(row)
            function_counts[issue.function] += 1
            for material in materials:
                material_role_counts[material.role] += 1
            projected_target_count += len(projection_targets)
        output.append(
            {
                "sub_question_id": case_id,
                "recovery_target_count": len(case_recoveries),
                "recovery_targets": case_recoveries,
            }
        )

    manifest = {
        "step": "v2_card_informed_unknown_reassessment_plan",
        "status": "SUCCEEDED",
        "case_count": len(output),
        "atomic_recovery_target_count": sum(
            row["recovery_target_count"] for row in output
        ),
        "projected_original_unknown_target_count": projected_target_count,
        "skip_counts": dict(skip_counts.most_common()),
        "issue_function_counts": dict(function_counts.most_common()),
        "material_role_counts": dict(material_role_counts.most_common()),
        "planner_sha256": _sha256(planner_path),
        "call2_sha256": _sha256(call2_path),
        "selection_uses_gold_or_rubric": False,
        "existing_prompt_modified": False,
    }
    return output, manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--definitions", type=Path, default=ROOT / "data/v2/definitions")
    parser.add_argument(
        "--planner",
        type=Path,
        default=ROOT
        / "experiments/v2_call15_directscope_26_causal/evaluation_instance_plan.jsonl",
    )
    parser.add_argument(
        "--call2",
        type=Path,
        default=ROOT
        / "experiments/v2_call15_directscope_26_causal/call2_full_v2/grounding_output.jsonl",
    )
    parser.add_argument(
        "--inventory",
        type=Path,
        default=ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl",
    )
    parser.add_argument(
        "--question-assumptions",
        type=Path,
        default=ROOT / "data/v2/question_assumptions.jsonl",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT
        / "experiments/v2_call15_directscope_26_causal/card_reassessment_plan_v1/plan.jsonl",
    )
    args = parser.parse_args()
    rows, manifest = build_plan(
        definitions=args.definitions,
        planner_path=args.planner,
        call2_path=args.call2,
        inventory_path=args.inventory,
        assumptions_path=args.question_assumptions,
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows)
    )
    args.out.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
