#!/usr/bin/env python3
"""Report predicates whose truth disagrees across instances of the same actor.

No model is called and nothing is repaired.  A ground fact is a fact about the case, so
one actor cannot both have and not have done the thing depending on which offence is
being scored; those disagreements are contract violations to be fixed upstream.  A legal
element can legitimately be evaluated inside an offence's own context, so those are
classified rather than condemned -- only the ones asking demonstrably the same question
are called conflicts.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.v2.registry import load_definitions

GROUND_FACT_CONFLICT = "CROSS_INSTANCE_GROUND_FACT_CONFLICT"
LEGAL_ELEMENT_CONFLICT = "CROSS_INSTANCE_LEGAL_ELEMENT_CONFLICT"
LEGAL_ELEMENT_DIVERGENCE = "CROSS_INSTANCE_LEGAL_ELEMENT_DIVERGENCE"


UNRESOLVED_EPISODE = "?"


def _episode_index(path: Path) -> dict[tuple[str, str], str]:
    """occurrence -> factual episode, as Call 1.5 bound them.

    The episode is what makes two assessments the same question.  The same predicate asked
    about two different episodes is two questions and may legitimately differ; asked twice
    about one episode it is one question, and one question has one answer.
    """
    index: dict[tuple[str, str], str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        case_id = str(row["sub_question_id"])
        for seed in row.get("seed_results") or []:
            for binding in seed.get("bindings") or []:
                occurrence = str(binding.get("binding_id", ""))
                episode = str(binding.get("factual_episode_id", ""))
                if occurrence and episode:
                    index[(case_id, occurrence)] = episode
    return index


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--call2-artifact", type=Path, required=True)
    parser.add_argument("--issue-bindings", type=Path, required=True)
    parser.add_argument("--definitions", type=Path, default=ROOT / "data/v2/definitions")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    registry = load_definitions(args.definitions)
    episodes = _episode_index(args.issue_bindings)
    rows = [
        json.loads(line)
        for line in args.call2_artifact.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    findings: list[dict[str, Any]] = []
    for row in rows:
        case_id = row["sub_question_id"]
        grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
        for assessment in row.get("assessments") or []:
            instance = assessment.get("instance_key") or {}
            key = (str(instance.get("actor_id", "")), str(assessment.get("predicate_ref", "")))
            grouped[key].append(
                {
                    "offense_ref": str(instance.get("offense_ref", "")),
                    "occurrence_id": str(instance.get("occurrence_id", "")),
                    "factual_episode_id": episodes.get(
                        (case_id, str(instance.get("occurrence_id", ""))), UNRESOLVED_EPISODE
                    ),
                    "truth": str(assessment.get("truth", "")),
                }
            )
        for (actor, predicate_ref), observations in sorted(grouped.items()):
            truths = {observation["truth"] for observation in observations}
            if len(truths) < 2:
                continue
            seen_episodes = {observation["factual_episode_id"] for observation in observations}
            if UNRESOLVED_EPISODE in seen_episodes:
                # A derived occurrence carries its own id and does not resolve to a base
                # binding.  Without the episode we cannot say the two asked one question,
                # so it is recorded and not condemned.
                marker = LEGAL_ELEMENT_DIVERGENCE
            elif len(seen_episodes) > 1:
                # Different episodes are different questions.  Not a finding at all.
                continue
            elif predicate_ref.startswith("ground_fact."):
                marker = GROUND_FACT_CONFLICT
            else:
                marker = LEGAL_ELEMENT_CONFLICT
            findings.append(
                {
                    "marker": marker,
                    "case_id": case_id,
                    "actor_id": actor,
                    "predicate_ref": predicate_ref,
                    "truths": sorted(truths),
                    "hard_conflict": "TRUE" in truths and "FALSE" in truths,
                    "observations": sorted(observations, key=lambda o: o["offense_ref"]),
                }
            )

    summary = {
        "call2_artifact": str(args.call2_artifact),
        "cases": len(rows),
        "cases_affected": len({finding["case_id"] for finding in findings}),
        "by_marker": {
            marker: sum(1 for finding in findings if finding["marker"] == marker)
            for marker in (GROUND_FACT_CONFLICT, LEGAL_ELEMENT_CONFLICT, LEGAL_ELEMENT_DIVERGENCE)
        },
        "hard_conflicts": sum(1 for finding in findings if finding["hard_conflict"]),
        "repaired": False,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps({"summary": summary, "findings": findings}, ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
