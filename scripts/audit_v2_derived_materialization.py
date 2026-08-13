#!/usr/bin/env python3
"""Audit evidence-gated derived materialization against Call 1 survivor gold."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.v2.closure import compile_closure
from idpr.v2.registry import load_definitions


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--call1", type=Path, required=True)
    parser.add_argument("--definition-gold", type=Path, required=True)
    parser.add_argument("--definitions", type=Path, required=True)
    parser.add_argument("--json-out", type=Path, required=True)
    parser.add_argument("--markdown-out", type=Path, required=True)
    parser.add_argument("--cartesian-top-level", type=int, default=815)
    parser.add_argument("--cartesian-assessment", type=int, default=849)
    parser.add_argument("--cartesian-neural", type=int, default=4998)
    args = parser.parse_args()

    registry = load_definitions(args.definitions)
    plans = {row["sub_question_id"]: row for row in _jsonl(args.plan)}
    call1 = {row["sub_question_id"]: row for row in _jsonl(args.call1)}
    gold = {
        row["case_id"]: set(row["gold_definition_refs"])
        for row in json.loads(args.definition_gold.read_text(encoding="utf-8"))["cases"]
    }
    if set(plans) != set(call1) or set(plans) != set(gold):
        raise ValueError("plan, Call 1, and definition gold case universes differ")

    survivor_total = direct_covered = total_covered = 0
    closure_only_total = 0
    generated_unique: set[tuple[str, str]] = set()
    recovered_unique: set[tuple[str, str]] = set()
    generated_physical = recovered_physical = 0
    for case_id, plan in plans.items():
        survivors = gold[case_id] & set(
            compile_closure(
                registry, call1[case_id]["normalized_seeds"]
            ).candidate_offense_refs
        )
        explicit = set(call1[case_id]["normalized_seeds"])
        closure_only_total += len(survivors - explicit)
        survivor_total += len(survivors)
        direct_refs = {
            value["offense_ref"]
            for value in plan["top_level_instances"]
            if value["occurrence_id"].startswith("binding:")
        }
        all_refs = {value["offense_ref"] for value in plan["top_level_instances"]}
        direct_covered += len(survivors & direct_refs)
        total_covered += len(survivors & all_refs)
        for value in plan["derived_binding_candidates"]:
            key = (case_id, value["offense_ref"])
            generated_unique.add(key)
            generated_physical += 1
            if value["offense_ref"] in survivors:
                recovered_unique.add(key)
                recovered_physical += 1

    counts = {
        key: sum(int(row[key]) for row in plans.values())
        for key in (
            "top_level_instance_count",
            "assessment_instance_count",
            "neural_predicate_request_target_count",
            "derived_binding_candidate_count",
            "unbound_seed_count",
        )
    }
    baselines = {
        "top_level_instance_count": args.cartesian_top_level,
        "assessment_instance_count": args.cartesian_assessment,
        "neural_predicate_request_target_count": args.cartesian_neural,
    }
    reduction = {
        key: 1 - counts[key] / baseline for key, baseline in baselines.items()
    }
    report = {
        "case_count": len(plans),
        "call15_direct_binding_count": sum(
            1
            for row in plans.values()
            for value in row["top_level_instances"]
            if value["occurrence_id"].startswith("binding:")
        ),
        "call1_gold_survivor": {
            "direct_covered": direct_covered,
            "total_covered": total_covered,
            "total": survivor_total,
        },
        "closure_only_gold": {
            "recovered": len(recovered_unique),
            "total": closure_only_total,
        },
        "derived_materialization": {
            "unique_generated": len(generated_unique),
            "unique_gold_relevant": len(recovered_unique),
            "unique_precision": (
                len(recovered_unique) / len(generated_unique) if generated_unique else None
            ),
            "physical_generated": generated_physical,
            "physical_gold_relevant": recovered_physical,
            "physical_precision_proxy": (
                recovered_physical / generated_physical if generated_physical else None
            ),
            "generated": [
                {"sub_question_id": case_id, "offense_ref": ref}
                for case_id, ref in sorted(generated_unique)
            ],
        },
        "planner_counts": counts,
        "cartesian_baseline": baselines,
        "cartesian_reduction": reduction,
        "interpretation": (
            "Rubric/DefinitionRef gold is offline audit supervision only. Physical precision "
            "is a conservative case/ref relevance proxy because gold has no actor identity."
        ),
    }
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Evidence-gated derived materialization audit",
        "",
        f"- Direct bindings: {report['call15_direct_binding_count']}",
        f"- Call 1 survivor coverage: {total_covered}/{survivor_total} (direct {direct_covered}/{survivor_total})",
        f"- Closure-only recovery: {len(recovered_unique)}/{closure_only_total}",
        f"- Derived: {len(generated_unique)} unique / {generated_physical} physical; gold-relevant {len(recovered_unique)} unique / {recovered_physical} physical",
        f"- Top-level: {counts['top_level_instance_count']} vs {args.cartesian_top_level} ({reduction['top_level_instance_count']:.1%} reduction)",
        f"- Call 2 neural targets: {counts['neural_predicate_request_target_count']} vs {args.cartesian_neural} ({reduction['neural_predicate_request_target_count']:.1%} reduction)",
        f"- UNBOUND_SEED diagnostics: {counts['unbound_seed_count']}",
        "",
        "| case | derived candidate |",
        "|---|---|",
        *[f"| `{case_id}` | `{ref}` |" for case_id, ref in sorted(generated_unique)],
    ]
    args.markdown_out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
