#!/usr/bin/env python3
"""Ask what the Call 2 UNKNOWN rate is actually caused by: the evidence window.

73% of the plan's anchors end up undetermined, which costs the rubric's conclusion
items.  The assessor sees one occurrence's quoted span and is told that a fact merely
absent from it is UNKNOWN, so the question is whether those UNKNOWNs are genuine legal
indeterminacy or an artifact of showing it a third of the case.

This replays the frozen targets for a few cases twice against the same served model:
once with the evidence the run used, and once with the case's full fact pattern as the
evidence span.  Prompt, schema, predicate catalogue and target set are identical
between the arms -- only `evidence_occurrence.source_text` differs.

Nothing is installed and no artifact is rebuilt.  The output is a comparison table.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.neural.vllm_client import VLLMClient
from idpr.v2.gold_factual_identity import GoldOccurrence
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.grounding import (
    call2_request_payload,
    call2_schema,
    grounding_request_targets,
    predicate_definitions,
    shard_assessment_targets_by_occurrence,
    validate_call2_output,
)


def rows(path: Path) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            out[str(row["sub_question_id"])] = row
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--run-root", type=Path, default=ROOT / "experiments/v2_call15_directscope_26_causal")
    parser.add_argument("--inventory", type=Path, default=ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl")
    parser.add_argument("--definitions", type=Path, default=ROOT / "data/v2/definitions")
    parser.add_argument("--case-id", action="append", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-tokens", type=int, default=4096)
    args = parser.parse_args()

    registry = load_definitions(args.definitions)
    inventory = rows(args.inventory)
    plans = rows(args.run_root / "call15d_v4/evaluation_instance_plan.jsonl")
    frozen = rows(args.run_root / "call2_v10_ground_fact_rebase/grounding_output_rebased.jsonl")

    system_prompt = (ROOT / "prompts/v2_call2_grounding.md").read_text(encoding="utf-8")
    user_prompt = (ROOT / "prompts/v2_call2_grounding_user.md").read_text(encoding="utf-8")
    client = VLLMClient(base_url=args.base_url, model=args.model)

    findings: list[dict[str, Any]] = []
    for case_id in args.case_id:
        plan_row = plans[case_id]
        case_text = str(inventory[case_id]["question_text"])
        occurrences = {
            str(value["occurrence_id"]): GoldOccurrence(
                str(value["occurrence_id"]),
                str(value["actor_id"]),
                str(value["source_text"]),
                int(value["source_span"]["start"]),
                int(value["source_span"]["end"]),
            )
            for value in plan_row["occurrences"]
        }
        episode_by_occurrence = {
            str(value["occurrence_id"]): str(value.get("factual_episode_id", ""))
            for value in plan_row["occurrences"]
        }

        targets = tuple(
            _target(value) for value in plan_row.get("assessment_targets") or []
        )
        if not targets:
            print(f"{case_id}: planner row carries no assessment targets", file=sys.stderr)
            continue
        request_targets = grounding_request_targets(
            registry, targets, episode_by_occurrence=episode_by_occurrence
        )
        shards = shard_assessment_targets_by_occurrence(request_targets, max_targets=24)

        for arm in ("occurrence_span", "full_case_text"):
            truths: dict[tuple[str, str], str] = {}
            for shard in shards:
                occurrence_id = shard[0].instance_key.occurrence_id
                evidence = occurrences[occurrence_id]
                if arm == "full_case_text":
                    # Same occurrence identity, widened span: the assessor now sees every
                    # fact the question states, not only the sentence this occurrence was
                    # bound to.
                    evidence = GoldOccurrence(
                        evidence.occurrence_id,
                        evidence.actor_id,
                        case_text,
                        0,
                        len(case_text),
                    )
                refs = tuple(dict.fromkeys(value.predicate_ref for value in shard))
                payload = call2_request_payload(
                    evidence_occurrence=evidence,
                    predicates=predicate_definitions(registry, refs),
                    targets=shard,
                )
                raw, _ = client.complete_json(
                    system_prompt=system_prompt,
                    payload=payload,
                    schema_name="v2_occurrence_scoped_call2",
                    schema=call2_schema(shard),
                    max_tokens=args.max_tokens,
                    temperature=0.0,
                    user_template=user_prompt,
                )
                for value in validate_call2_output(raw, targets=shard):
                    truths[(value.target.instance_key.occurrence_id, value.target.predicate_ref)] = value.truth
            findings.append(
                {
                    "case_id": case_id,
                    "arm": arm,
                    "counts": dict(Counter(truths.values())),
                    "truths": {f"{k[0]}|{k[1]}": v for k, v in sorted(truths.items())},
                }
            )
            print(f"{case_id:28} {arm:16} {dict(Counter(truths.values()))}")

    baseline = {
        case_id: dict(
            Counter(t["truth"] for t in (frozen[case_id].get("case_truths") or []))
        )
        for case_id in args.case_id
        if case_id in frozen
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps({"frozen_run": baseline, "findings": findings}, ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    print(f"\nfrozen run, for reference: {baseline}")


def _target(value: dict[str, Any]):
    from idpr.v2.runtime.grounding import AssessmentTarget
    from idpr.v2.runtime.identity import OffenseInstanceKey

    instance = value["instance_key"]
    return AssessmentTarget(
        instance_key=OffenseInstanceKey(
            case_id=str(instance["case_id"]),
            actor_id=str(instance["actor_id"]),
            offense_ref=str(instance["offense_ref"]),
            occurrence_id=str(instance["occurrence_id"]),
        ),
        predicate_ref=str(value["predicate_ref"]),
    )


if __name__ == "__main__":
    main()
