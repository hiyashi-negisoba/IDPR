#!/usr/bin/env python3
"""Audit Call 1.5 bindings against reviewed rubric refs and factual-only gold spans."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.eval.input_formatter import scoped_question_text
from idpr.v2.closure import compile_closure
from idpr.v2.registry import load_definitions


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def _overlaps(left: tuple[int, int], right: tuple[int, int]) -> bool:
    return left[0] < right[1] and right[0] < left[1]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bindings", type=Path, required=True)
    parser.add_argument("--call1", type=Path, required=True)
    parser.add_argument(
        "--inventory",
        type=Path,
        default=ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl",
    )
    parser.add_argument(
        "--occurrences", type=Path, default=ROOT / "data/v2/gold_occurrences.jsonl"
    )
    parser.add_argument(
        "--definition-gold",
        type=Path,
        default=ROOT / "data/eval/v2_call1_definition_gold_draft.json",
    )
    parser.add_argument(
        "--definitions", type=Path, default=ROOT / "data/v2/definitions"
    )
    parser.add_argument("--json-out", type=Path, required=True)
    parser.add_argument("--markdown-out", type=Path, required=True)
    args = parser.parse_args()

    binding_rows = {row["sub_question_id"]: row for row in _jsonl(args.bindings)}
    call1_rows = {row["sub_question_id"]: row for row in _jsonl(args.call1)}
    inventory = {row["sub_question_id"]: row for row in _jsonl(args.inventory)}
    occurrence_rows = {row["sub_question_id"]: row for row in _jsonl(args.occurrences)}
    definition_gold = {
        row["case_id"]: row
        for row in json.loads(args.definition_gold.read_text(encoding="utf-8"))["cases"]
    }
    case_ids = tuple(binding_rows)
    if not all(
        case_id in call1_rows
        and case_id in inventory
        and case_id in occurrence_rows
        and case_id in definition_gold
        for case_id in case_ids
    ):
        raise ValueError("audit inputs have different case universes")
    registry = load_definitions(args.definitions)

    reports: list[dict[str, Any]] = []
    gold_ref_total = gold_ref_covered = call1_survivor_total = preserved_total = 0
    explicit_gold_seed_total = explicit_gold_seed_bound = 0
    direct_gold_ref_covered = direct_call1_survivor_preserved = 0
    binding_total = extraneous_total = 0
    occurrence_total = occurrence_covered = 0
    status_counts: Counter[str] = Counter()
    grouping_counts: Counter[str] = Counter()
    scope_errors: list[str] = []
    actor_scope_errors: list[str] = []
    explicit_seed_misses: list[dict[str, str]] = []
    host_derived_pending: list[dict[str, str]] = []
    exhaustive_seed_processing_errors: list[str] = []
    for case_id in case_ids:
        row = binding_rows[case_id]
        if row.get("error"):
            raise ValueError(f"{case_id}: unsuccessful binding row")
        source = inventory[case_id]
        raw_seed_results = row.get("seed_results")
        if not isinstance(raw_seed_results, list) or [
            value.get("seed_index") for value in raw_seed_results
        ] != list(range(len(call1_rows[case_id]["normalized_seeds"]))):
            exhaustive_seed_processing_errors.append(case_id)
            direct_bindings: list[dict[str, Any]] = []
        else:
            direct_bindings = [
                binding
                for result in raw_seed_results
                for binding in result.get("bindings", [])
            ]
        case_text = str(source["question_text"])
        scope = scoped_question_text(case_text, str(source["question_prompt"]))
        gold_refs = set(definition_gold[case_id]["gold_definition_refs"])
        call1_candidates = set(
            compile_closure(registry, call1_rows[case_id]["normalized_seeds"]).candidate_offense_refs
        )
        call1_survivors = gold_refs & call1_candidates
        explicit_gold_seeds = gold_refs & set(call1_rows[case_id]["normalized_seeds"])
        allowed_actors = set(
            re.findall(r"[甲乙丙丁戊己庚辛壬癸]", str(source["question_prompt"]))
        )
        occurrences = []
        for occurrence in occurrence_rows[case_id]["occurrences"]:
            quote = occurrence["source_text"]
            start = case_text.index(quote)
            occurrences.append(
                {
                    **occurrence,
                    "span": (start, start + len(quote)),
                }
            )

        case_candidate_refs: set[str] = set()
        case_bindings = []
        covered_occurrence_ids: set[str] = set()
        for binding in direct_bindings:
            closure_refs = set(
                compile_closure(registry, [binding["offense_ref"]]).candidate_offense_refs
            )
            case_candidate_refs.update(closure_refs)
            relevant_refs = sorted(closure_refs & gold_refs)
            action_spans = [
                (item["source_span"]["start"], item["source_span"]["end"])
                for item in binding["actor_action_fragments"]
            ]
            matched = [
                occurrence
                for occurrence in occurrences
                if any(_overlaps(span, occurrence["span"]) for span in action_spans)
            ]
            same_actor = [
                occurrence
                for occurrence in matched
                if occurrence["actor_id"] == binding["actor_id"]
            ]
            if same_actor:
                actor_status = "SUPPORTED_BY_GOLD_OCCURRENCE"
                covered_occurrence_ids.update(value["occurrence_id"] for value in same_actor)
            elif matched:
                actor_status = "CONFLICTS_WITH_GOLD_OCCURRENCE_ACTOR"
            else:
                actor_status = "OUTSIDE_OCCURRENCE_SUPERVISION"
            matched_ids = sorted({value["occurrence_id"] for value in matched})
            if len(matched_ids) > 1:
                grouping = "MIXES_GOLD_OCCURRENCES"
            elif matched_ids:
                grouping = "ONE_GOLD_OCCURRENCE"
            else:
                grouping = "OUTSIDE_OCCURRENCE_SUPERVISION"
            status_counts[actor_status] += 1
            grouping_counts[grouping] += 1
            binding_total += 1
            if not relevant_refs:
                extraneous_total += 1
            all_quotes = [
                item["source_quote"]
                for key in ("actor_action_fragments", "context_fragments")
                for item in binding[key]
            ]
            outside_scope = [quote for quote in all_quotes if quote not in scope]
            if outside_scope:
                scope_errors.append(f"{case_id}/{binding['binding_id']}")
            if allowed_actors and binding["actor_id"] not in allowed_actors:
                actor_scope_errors.append(f"{case_id}/{binding['binding_id']}")
            case_bindings.append(
                {
                    "binding_id": binding["binding_id"],
                    "offense_ref": binding["offense_ref"],
                    "actor_id": binding["actor_id"],
                    "actor_action_quotes": [
                        item["source_quote"] for item in binding["actor_action_fragments"]
                    ],
                    "context_quotes": [
                        item["source_quote"] for item in binding["context_fragments"]
                    ],
                    "factual_targets": binding["factual_targets"],
                    "rubric_relevant_closure_refs": relevant_refs,
                    "extraneous_proxy": not relevant_refs,
                    "actor_occurrence_status": actor_status,
                    "matched_gold_occurrence_ids": matched_ids,
                    "fragment_grouping_proxy": grouping,
                    "outside_scope_quotes": outside_scope,
                }
            )
        covered_refs = gold_refs & case_candidate_refs
        preserved = call1_survivors & case_candidate_refs
        direct_bound_refs = {value["offense_ref"] for value in direct_bindings}
        for ref in sorted(explicit_gold_seeds - direct_bound_refs):
            explicit_seed_misses.append({"sub_question_id": case_id, "offense_ref": ref})
        for ref in sorted((call1_survivors - explicit_gold_seeds) - direct_bound_refs):
            host_derived_pending.append({"sub_question_id": case_id, "offense_ref": ref})
        gold_ref_total += len(gold_refs)
        gold_ref_covered += len(covered_refs)
        call1_survivor_total += len(call1_survivors)
        preserved_total += len(preserved)
        direct_gold_ref_covered += len(gold_refs & direct_bound_refs)
        direct_call1_survivor_preserved += len(call1_survivors & direct_bound_refs)
        explicit_gold_seed_total += len(explicit_gold_seeds)
        explicit_gold_seed_bound += len(explicit_gold_seeds & direct_bound_refs)
        occurrence_total += len(occurrences)
        occurrence_covered += len(covered_occurrence_ids)
        reports.append(
            {
                "sub_question_id": case_id,
                "question_prompt": source["question_prompt"],
                "rubric_summary": source.get("rubric_summary", []),
                "gold_definition_refs": sorted(gold_refs),
                "covered_definition_refs": sorted(covered_refs),
                "explicit_gold_seed_misses": sorted(explicit_gold_seeds - direct_bound_refs),
                "closure_survivor_not_covered": sorted(call1_survivors - preserved),
                "bindings": case_bindings,
            }
        )

    aggregate = {
        "case_count": len(case_ids),
        "binding_count": binding_total,
        "direct_top_level_gold_definition_ref_coverage": {
            "covered": direct_gold_ref_covered,
            "total": gold_ref_total,
            "rate": direct_gold_ref_covered / gold_ref_total,
        },
        "structurally_reachable_gold_definition_ref_coverage": {
            "covered": gold_ref_covered,
            "total": gold_ref_total,
            "rate": gold_ref_covered / gold_ref_total,
        },
        "direct_top_level_call1_survivor_preservation": {
            "covered": direct_call1_survivor_preserved,
            "total": call1_survivor_total,
            "rate": direct_call1_survivor_preserved / call1_survivor_total,
        },
        "structurally_reachable_call1_survivor_preservation": {
            "covered": preserved_total,
            "total": call1_survivor_total,
            "rate": preserved_total / call1_survivor_total,
        },
        "explicit_gold_seed_binding_recall": {
            "covered": explicit_gold_seed_bound,
            "total": explicit_gold_seed_total,
            "rate": explicit_gold_seed_bound / explicit_gold_seed_total,
            "misses": explicit_seed_misses,
        },
        "host_derived_binding_pending": host_derived_pending,
        "explicit_seed_processing": {
            "processed_case_count": len(case_ids) - len(exhaustive_seed_processing_errors),
            "total_case_count": len(case_ids),
            "errors": exhaustive_seed_processing_errors,
        },
        "gold_occurrence_action_span_coverage": {
            "covered": occurrence_covered,
            "total": occurrence_total,
            "rate": occurrence_covered / occurrence_total,
        },
        "extraneous_binding_proxy": {
            "count": extraneous_total,
            "total": binding_total,
            "rate": extraneous_total / binding_total,
        },
        "actor_occurrence_status_counts": dict(status_counts),
        "fragment_grouping_proxy_counts": dict(grouping_counts),
        "outside_question_scope_binding_count": len(scope_errors),
        "outside_question_scope_bindings": scope_errors,
        "outside_requested_actor_scope_binding_count": len(actor_scope_errors),
        "outside_requested_actor_scope_bindings": actor_scope_errors,
        "interpretation_limits": [
            "DefinitionRef gold contains theories to examine, including rejected theories.",
            "GoldOccurrence is actor-action supervision and can omit results, other-party acts, and context.",
            "Extraneous and grouping values are conservative proxies, not final legal correctness labels.",
        ],
    }
    payload = {"aggregate": aggregate, "cases": reports}
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Call 1.5 rubric and factual-binding audit",
        "",
        "This is an offline audit. Rubrics and gold artifacts were never model inputs.",
        "",
        f"- Bindings: {binding_total}",
        f"- Direct top-level DefinitionRef coverage: {direct_gold_ref_covered}/{gold_ref_total} ({direct_gold_ref_covered / gold_ref_total:.1%})",
        f"- Structurally reachable DefinitionRef coverage: {gold_ref_covered}/{gold_ref_total} ({gold_ref_covered / gold_ref_total:.1%})",
        f"- Direct top-level Call 1 survivor preservation: {direct_call1_survivor_preserved}/{call1_survivor_total} ({direct_call1_survivor_preserved / call1_survivor_total:.1%})",
        f"- Explicit gold seed binding recall: {explicit_gold_seed_bound}/{explicit_gold_seed_total} ({explicit_gold_seed_bound / explicit_gold_seed_total:.1%})",
        f"- GoldOccurrence action-span coverage: {occurrence_covered}/{occurrence_total} ({occurrence_covered / occurrence_total:.1%})",
        f"- Extraneous proxy: {extraneous_total}/{binding_total} ({extraneous_total / binding_total:.1%})",
        f"- Outside question scope: {len(scope_errors)}",
        "",
        "| case | bindings | covered refs | explicit seed misses | extraneous proxy |",
        "|---|---:|---|---|---:|",
    ]
    for report in reports:
        extras = sum(value["extraneous_proxy"] for value in report["bindings"])
        lines.append(
            f"| `{report['sub_question_id']}` | {len(report['bindings'])} | "
            f"{', '.join(report['covered_definition_refs']) or '—'} | "
            f"{', '.join(report['explicit_gold_seed_misses']) or '—'} | {extras} |"
        )
    args.markdown_out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(aggregate, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
