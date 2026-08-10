#!/usr/bin/env python3
"""Audit Call 1 misses and prefix10/full15 structural deltas without a model call."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.v2.closure import compile_closure  # noqa: E402
from idpr.v2.registry import load_definitions  # noqa: E402
from idpr.v2.routing import router_catalog  # noqa: E402


DEFAULT_DEFINITIONS = ROOT / "data/v2/definitions"


def _profile(registry, seeds: Iterable[str]) -> dict[str, Any]:
    closure = compile_closure(registry, tuple(seeds))
    frontier = {
        (
            tuple(fact.occurrence_path),
            tuple(fact.source_path),
            fact.ground_fact_ref,
        )
        for item in closure.items
        for fact in item.ground_fact_frontier
    }
    return {
        "mandatory": frozenset(closure.mandatory_offense_refs),
        "candidates": frozenset(closure.candidate_offense_refs),
        "probe_count": sum(
            len(items)
            for items in (
                closure.offense_probes,
                closure.doctrine_probes,
                closure.completion_probes,
                closure.participation_probes,
            )
        ),
        "frontier": frontier,
    }


def _structural_delta(registry, seeds: tuple[str, ...]) -> dict[str, Any]:
    prefix_seeds = seeds[:10]
    full_seeds = seeds[:15]
    prefix = _profile(registry, prefix_seeds)
    full = _profile(registry, full_seeds)
    return {
        "prefix10_seeds": list(prefix_seeds),
        "full15_seeds": list(full_seeds),
        "beyond_prefix10_seeds": list(full_seeds[10:]),
        "candidate_refs_added": sorted(full["candidates"] - prefix["candidates"]),
        "mandatory_refs_added": sorted(full["mandatory"] - prefix["mandatory"]),
        "probe_count": {"prefix10": prefix["probe_count"], "full15": full["probe_count"],
                        "delta": full["probe_count"] - prefix["probe_count"]},
        "ground_fact_frontier_count": {
            "prefix10": len(prefix["frontier"]),
            "full15": len(full["frontier"]),
            "delta": len(full["frontier"] - prefix["frontier"]),
        },
    }


def _reverse_closure_predecessors(registry) -> dict[str, tuple[str, ...]]:
    predecessors: dict[str, set[str]] = defaultdict(set)
    for entry in router_catalog(registry):
        for candidate in compile_closure(registry, (entry.definition_id,)).candidate_offense_refs:
            if candidate != entry.definition_id:
                predecessors[candidate].add(entry.definition_id)
    return {ref: tuple(sorted(refs)) for ref, refs in predecessors.items()}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--definitions-dir", type=Path, default=DEFAULT_DEFINITIONS)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()

    report = json.loads(args.report.read_text(encoding="utf-8"))
    registry = load_definitions(args.definitions_dir)
    predecessors = _reverse_closure_predecessors(registry)
    cases: list[dict[str, Any]] = []
    miss_kinds: Counter[str] = Counter()
    structural_totals: Counter[str] = Counter()

    for row in report["cases"]:
        if row.get("error"):
            cases.append({"case_id": row["sub_question_id"], "error": row["error"]})
            continue
        seeds = tuple(row["normalized_seeds"])
        delta = _structural_delta(registry, seeds)
        structural_totals["cases"] += 1
        structural_totals["cases_with_beyond_prefix10"] += bool(delta["beyond_prefix10_seeds"])
        structural_totals["candidate_refs_added"] += len(delta["candidate_refs_added"])
        structural_totals["mandatory_refs_added"] += len(delta["mandatory_refs_added"])
        structural_totals["probe_delta"] += delta["probe_count"]["delta"]
        structural_totals["frontier_delta"] += delta["ground_fact_frontier_count"]["delta"]
        structural_totals["cases_with_candidate_delta"] += bool(delta["candidate_refs_added"])
        structural_totals["cases_with_probe_delta"] += bool(delta["probe_count"]["delta"])
        structural_totals["cases_with_frontier_delta"] += bool(delta["ground_fact_frontier_count"]["delta"])

        misses: list[dict[str, Any]] = []
        for gold in row.get("calibration", {}).get("gold_definition_refs", []):
            if gold["closure_success"]:
                continue
            ref = gold["definition_ref"]
            all_predecessors = predecessors.get(ref, ())
            selected_predecessors = tuple(seed for seed in seeds if seed in all_predecessors)
            if not all_predecessors:
                kind = "direct_only_router_miss"
            elif selected_predecessors:
                kind = "topology_investigation_required"
            else:
                kind = "router_missed_closure_entrypoint"
            miss_kinds[kind] += 1
            misses.append({
                "definition_ref": ref,
                "classification": kind,
                "alternate_closure_predecessors": list(all_predecessors),
                "selected_predecessors": list(selected_predecessors),
            })
        cases.append({
            "case_id": row["sub_question_id"],
            "gold_definition_refs": row["gold"]["gold_definition_refs"],
            "scope_notes": row["gold"]["scope_notes"],
            "structural_delta": delta,
            "closure_misses": misses,
        })

    audit = {
        "step": "v2_call1_pilot_post_run_audit",
        "report": str(args.report),
        "metric_name": report["metric_contract"]["metric_name"],
        "miss_classification_note": (
            "This is a registry-topology diagnostic, not an automatic legal-gold judgment. "
            "A direct-only miss has no alternate single-seed closure path in the current registry."
        ),
        "summary": {
            "closure_miss_classes": dict(sorted(miss_kinds.items())),
            "prefix10_full15_structural_totals": dict(sorted(structural_totals.items())),
        },
        "cases": cases,
    }
    output = args.out or args.report.with_suffix(".audit.json")
    output.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {output}")


if __name__ == "__main__":
    main()
