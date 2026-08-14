#!/usr/bin/env python3
"""Add narrow exact-text deterministic interactions to a validated Call 1.5-P run."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.v2.deterministic_interactions import explicit_conspiracy_interactions
from idpr.v2.factual_interaction import validate_factual_interaction_output
from idpr.v2.issue_binding import parse_issue_binding_result, question_actor_ids


def _rows(path: Path) -> dict[str, dict[str, Any]]:
    return {
        row["sub_question_id"]: row
        for row in (json.loads(line) for line in path.read_text().splitlines() if line.strip())
    }


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _raw(value: dict[str, Any]) -> dict[str, Any]:
    return {
        "interaction_type": value["interaction_type"],
        "source_actor_id": value["source_actor_id"],
        "target_actor_ids": value["target_actor_ids"],
        "evidence_quotes": [item["source_quote"] for item in value["evidence"]],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--call15", type=Path, required=True)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    base = _rows(args.base)
    call15 = _rows(args.call15)
    inventory = _rows(args.inventory)
    output: list[dict[str, Any]] = []
    added = 0
    for case_id, row in base.items():
        source = inventory[case_id]
        binding_row = call15[case_id]
        binding_result = parse_issue_binding_result(
            {
                "factual_episodes": binding_row["factual_episodes"],
                "seed_results": binding_row["seed_results"],
            },
            seeds=binding_row["seeds"],
            case_text=source["question_text"],
            candidate_actor_ids=question_actor_ids(source["question_prompt"]),
        )
        by_id = {value.factual_episode_id: value for value in binding_result.factual_episodes}
        rebuilt: list[dict[str, Any]] = []
        all_interactions: list[dict[str, Any]] = []
        for episode_row in row["episode_results"]:
            episode = by_id[episode_row["factual_episode_id"]]
            existing = [_raw(value) for value in episode_row.get("interactions", ())]
            routes = {
                (value["interaction_type"], value["source_actor_id"], tuple(value["target_actor_ids"]))
                for value in existing
            }
            deterministic = explicit_conspiracy_interactions(
                episode_source_quotes=[value.source_quote for value in episode.source_fragments],
                episode_participant_ids=episode.participants,
                responsibility_actor_ids=question_actor_ids(source["question_prompt"]),
            )
            additions = [
                value
                for value in deterministic
                if (value["interaction_type"], value["source_actor_id"], tuple(value["target_actor_ids"]))
                not in routes
            ]
            validated = validate_factual_interaction_output(
                {"interactions": [*existing, *additions]},
                case_text=source["question_text"],
                episode=episode,
            )
            serialized = [value.as_dict() for value in validated]
            added += len(additions)
            all_interactions.extend(serialized)
            rebuilt.append(
                {**episode_row, "interactions": serialized, "interaction_count": len(serialized)}
            )
        output.append(
            {
                **row,
                "episode_results": rebuilt,
                "interactions": all_interactions,
                "interaction_count": len(all_interactions),
            }
        )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in output),
        encoding="utf-8",
    )
    args.out.with_suffix(".manifest.json").write_text(
        json.dumps(
            {
                "step": "v2_call15p_deterministic_augmentation",
                "base": str(args.base),
                "base_sha256": _sha(args.base),
                "call15_sha256": _sha(args.call15),
                "added_interaction_count": added,
                "total_interaction_count": sum(row["interaction_count"] for row in output),
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"cases": len(output), "added": added}, ensure_ascii=False))


if __name__ == "__main__":
    main()
