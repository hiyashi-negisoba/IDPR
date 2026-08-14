#!/usr/bin/env python3
"""Ask whether the UNKNOWNs Call 2 returns were questions worth asking.

The evidence-window diagnostic showed that widening the evidence only removes about a
quarter of the UNKNOWNs, so the rest are produced by something else.  Two candidates
remain: the predicate definitions demand more than a fact pattern ever states, or the
planner emits targets that the case's own truths have already made moot.

This separates them without any model call.  For each assessed instance it evaluates the
offense's completion-policy branches under Kleene logic using the frozen Call 2 truths.
A target that appears only inside branches whose guard already evaluates to FALSE is
moot: nothing the assessor could have said about it would change an outcome.  What
remains after removing the moot targets is the honest denominator, and the predicates
that stay UNKNOWN in it are the ones whose definitions are the real cost.

Nothing is rebuilt or installed; the output is a report.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]

TRUE, FALSE, UNKNOWN = "TRUE", "FALSE", "UNKNOWN"


def rows(path: Path) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            out[str(row["sub_question_id"])] = row
    return out


def evaluate(node: Any, truths: dict[str, str]) -> str:
    """Kleene three-valued evaluation of a definition expression tree."""
    op = node.get("op")
    if op == "ref":
        return truths.get(str(node["ref"]), UNKNOWN)
    if op == "not":
        inner = evaluate(node["arg"], truths)
        return {TRUE: FALSE, FALSE: TRUE}.get(inner, UNKNOWN)
    if op in {"all", "any"}:
        values = [evaluate(arg, truths) for arg in node["args"]]
        if op == "all":
            if FALSE in values:
                return FALSE
            return TRUE if all(v == TRUE for v in values) else UNKNOWN
        if TRUE in values:
            return TRUE
        return FALSE if all(v == FALSE for v in values) else UNKNOWN
    # An operator this script does not model must not silently read as decided.
    return UNKNOWN


def refs(node: Any) -> set[str]:
    op = node.get("op")
    if op == "ref":
        return {str(node["ref"])}
    if op == "not":
        return refs(node["arg"])
    if op in {"all", "any"}:
        return set().union(*(refs(arg) for arg in node["args"])) if node["args"] else set()
    return set()


def decisive(node: Any, predicate: str, truths: dict[str, str]) -> bool:
    """Would knowing this predicate change what the expression says?

    Appearing inside a guard is not the same as mattering to it.  `dangerousness` sits in
    the impossible-attempt guard, but once `means_or_object_defect` is FALSE that guard is
    FALSE whichever way `dangerousness` goes -- so the assessor was asked a question with
    no consequence.  This holds the rest of the case fixed and varies only this predicate.

    The substitution ranges over all three values, not just TRUE and FALSE.  UNKNOWN is a
    meaning here, not a missing answer: a predicate whose TRUE and FALSE both leave a
    guard UNKNOWN can still be the reason the guard is UNKNOWN rather than decided, and
    calling it moot on a two-point comparison would silently drop live work.
    """
    if predicate not in refs(node):
        return False
    outcomes = {evaluate(node, {**truths, predicate: value}) for value in (TRUE, FALSE, UNKNOWN)}
    return len(outcomes) > 1


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, default=ROOT / "experiments/v2_call15_directscope_26_causal")
    parser.add_argument("--definitions", type=Path, default=ROOT / "data/v2/definitions")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument(
        "--assessed",
        type=Path,
        help="evidence-scope diagnostic output; reconciles planned targets against the "
        "keys Call 2 actually answers, so the two reports share one closed denominator",
    )
    args = parser.parse_args()

    policies = {
        str(entry["offense"]): entry
        for entry in yaml.safe_load((args.definitions / "completion_policies.yaml").read_text(encoding="utf-8"))
        if isinstance(entry, dict) and entry.get("offense")
    }
    offenses = {
        str(entry["id"]): entry
        for entry in yaml.safe_load((args.definitions / "offenses.yaml").read_text(encoding="utf-8"))
    }
    meanings: dict[str, str] = {}
    for name in ("legal_elements.yaml", "ground_facts.yaml"):
        for entry in yaml.safe_load((args.definitions / name).read_text(encoding="utf-8")):
            meanings[str(entry["id"])] = str(entry.get("canonical_meaning") or "")

    plans = rows(args.run_root / "call15d_v4/evaluation_instance_plan.jsonl")
    frozen = rows(args.run_root / "call2_v10_ground_fact_rebase/grounding_output_rebased.jsonl")

    per_predicate: dict[str, Counter[str]] = defaultdict(Counter)
    dead_branches: Counter[str] = Counter()
    case_report: list[dict[str, Any]] = []
    totals: Counter[str] = Counter()
    bucket_by_key: dict[tuple[str, str, str], str] = {}

    for case_id, plan in plans.items():
        truths_by_instance: dict[str, dict[str, str]] = defaultdict(dict)
        for value in frozen.get(case_id, {}).get("case_truths") or []:
            key = json.dumps(value["instance_key"], sort_keys=True, ensure_ascii=False)
            truths_by_instance[key][str(value["predicate_ref"])] = str(value["truth"])

        by_instance: dict[str, set[str]] = defaultdict(set)
        for target in plan.get("assessment_targets") or []:
            key = json.dumps(target["instance_key"], sort_keys=True, ensure_ascii=False)
            by_instance[key].add(str(target["predicate_ref"]))

        moot_here = 0
        for key, predicates in by_instance.items():
            instance = json.loads(key)
            truths = truths_by_instance.get(key, {})
            offense_ref = str(instance["offense_ref"])
            policy = policies.get(offense_ref) or {}
            branches = policy.get("states") or {}
            if not isinstance(branches, dict):
                branches = {}
            elements = list((offenses.get(offense_ref, {}).get("elements") or {}).values())

            for name, branch in branches.items():
                if evaluate(branch["when"], truths) == FALSE:
                    dead_branches[f"{offense_ref}::{name}"] += 1

            for predicate in predicates:
                truth = truths.get(predicate, "(missing)")
                # A target is live if flipping it would change some element of the offence,
                # some state guard, or the requirement of a state that is not already ruled
                # out.  If nothing moves, the answer could not have mattered.
                matters = any(decisive(element, predicate, truths) for element in elements)
                for branch in branches.values():
                    if matters:
                        break
                    if decisive(branch["when"], predicate, truths):
                        matters = True
                    elif branch.get("requires") and evaluate(branch["when"], truths) != FALSE:
                        matters = decisive(branch["requires"], predicate, truths)
                if matters:
                    bucket = "live_"
                elif branches or elements:
                    bucket = "moot_"
                else:
                    # No policy and no element tree for this offence: mootness is not a
                    # claim this script can make, so it is reported separately rather
                    # than counted as either.
                    bucket = "undefined_"
                totals[bucket + truth] += 1
                per_predicate[predicate][bucket + truth] += 1
                moot_here += 1 if bucket == "moot_" else 0
                # Several instances can share one occurrence, and Call 2 answers a
                # GroundFact once per factual episode.  Liveness on the shared key is the
                # disjunction: if any instance needed the answer, the question was live.
                shared = (case_id, str(instance["occurrence_id"]), predicate)
                if bucket_by_key.get(shared) != "live_":
                    bucket_by_key[shared] = bucket

        case_report.append(
            {"case_id": case_id, "targets": sum(len(v) for v in by_instance.values()), "moot_targets": moot_here}
        )

    live = {k[5:]: v for k, v in totals.items() if k.startswith("live_")}
    moot = {k[5:]: v for k, v in totals.items() if k.startswith("moot_")}
    undefined = {k[10:]: v for k, v in totals.items() if k.startswith("undefined_")}
    live_n, moot_n, undef_n = sum(live.values()), sum(moot.values()), sum(undefined.values())

    print(f"targets: {live_n + moot_n + undef_n}   live: {live_n}   moot: {moot_n}   no definition: {undef_n}")
    print(f"  live      : {dict(live)}   UNKNOWN {100 * live.get(UNKNOWN, 0) / max(live_n, 1):.1f}%")
    print(f"  moot      : {dict(moot)}   UNKNOWN {100 * moot.get(UNKNOWN, 0) / max(moot_n, 1):.1f}%")
    print(f"  undefined : {dict(undefined)}")
    print("\ndead branches raised anyway (instance count):")
    for name, count in dead_branches.most_common(12):
        print(f"  {name:66} {count}")

    print("\npredicates by live UNKNOWN (definition cost, not planning cost):")
    ranked = sorted(
        per_predicate.items(),
        key=lambda kv: -kv[1].get("live_" + UNKNOWN, 0),
    )
    print(f"  {'predicate':56} {'live_n':>6} {'live_UNK':>8} {'rate':>6} {'moot':>5}  meaning")
    for predicate, counter in ranked[:20]:
        ln = sum(v for k, v in counter.items() if k.startswith("live_"))
        lu = counter.get("live_" + UNKNOWN, 0)
        mn = sum(v for k, v in counter.items() if k.startswith("moot_"))
        if not lu and not mn:
            continue
        print(f"  {predicate:56} {ln:6d} {lu:8d} {100 * lu / max(ln, 1):5.0f}% {mn:5d}  {meanings.get(predicate, '')[:34]}")

    reconciliation: dict[str, Any] = {}
    if args.assessed:
        scope = json.loads(args.assessed.read_text(encoding="utf-8"))
        answered: set[tuple[str, str, str]] = set()
        for finding in scope["findings"]:
            if finding["arm"] != "occurrence_span":
                continue
            for composite in finding["truths"]:
                occurrence_id, predicate = composite.split("|", 1)
                answered.add((str(finding["case_id"]), occurrence_id, predicate))
        replayed = {finding["case_id"] for finding in scope["findings"]}
        collapsed = Counter()
        for (case_id, occurrence_id, predicate), bucket in bucket_by_key.items():
            if case_id in replayed and (case_id, occurrence_id, predicate) not in answered:
                collapsed[bucket.rstrip("_")] += 1
                collapsed["by_kind:" + predicate.split(".")[0]] += 1
        answered_buckets = Counter(
            bucket.rstrip("_")
            for key, bucket in bucket_by_key.items()
            if key in answered
        )
        reconciliation = {
            "planned_instance_predicate_targets": live_n + moot_n + undef_n,
            "cases_not_replayed": sorted(set(plans) - replayed),
            "assessed_occurrence_predicate_keys": len(answered),
            # Call 2 assesses a GroundFact once per factual episode, so planned targets
            # that repeat one across sibling occurrences never come back as their own
            # key.  This is the whole of the gap between the two denominators.
            "collapsed_by_factual_episode_dedup": dict(collapsed),
            "assessed_buckets": dict(answered_buckets),
        }
        print("\ndenominator reconciliation:")
        print(f"  planned (instance, predicate)        {reconciliation['planned_instance_predicate_targets']}")
        print(f"  collapsed by GroundFact episode dedup {sum(v for k, v in collapsed.items() if not k.startswith('by_kind:'))}"
              f"   {dict((k[8:], v) for k, v in collapsed.items() if k.startswith('by_kind:'))}")
        print(f"  assessed (occurrence, predicate)      {len(answered)}   {dict(answered_buckets)}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(
            {
                "totals": {"live": live, "moot": moot, "undefined": undefined},
                "reconciliation": reconciliation,
                "dead_branches": dict(dead_branches),
                "per_predicate": {k: dict(v) for k, v in per_predicate.items()},
                "per_case": case_report,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
