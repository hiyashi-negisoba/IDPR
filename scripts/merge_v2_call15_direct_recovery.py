#!/usr/bin/env python3
"""Merge independently verified direct-conduct recovery into empty Call 1.5 seed slots."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.v2.issue_binding import parse_issue_binding_result, question_actor_ids
from idpr.v2.registry import load_definitions


def _rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _spans(episode: dict[str, Any]) -> set[tuple[int, int]]:
    return {
        (int(value["source_span"]["start"]), int(value["source_span"]["end"]))
        for value in episode.get("source_fragments", ())
    }


def _merge_episode(
    base: dict[str, Any], recovered: dict[str, Any]
) -> str:
    recovered_spans = _spans(recovered)
    destination = next(
        (
            value for value in base["factual_episodes"]
            if _spans(value) & recovered_spans
        ),
        None,
    )
    if destination is None:
        destination = copy.deepcopy(recovered)
        destination["factual_episode_id"] = (
            f"factual_episode:{len(base['factual_episodes']) + 1:03d}"
        )
        base["factual_episodes"].append(destination)
    else:
        known = _spans(destination)
        destination["source_fragments"].extend(
            copy.deepcopy(value)
            for value in recovered.get("source_fragments", ())
            if (
                int(value["source_span"]["start"]),
                int(value["source_span"]["end"]),
            ) not in known
        )
        destination["participants"] = list(dict.fromkeys([
            *destination.get("participants", ()),
            *recovered.get("participants", ()),
        ]))
    return str(destination["factual_episode_id"])


def _renumber(row: dict[str, Any]) -> None:
    for episode_index, episode in enumerate(row["factual_episodes"], 1):
        episode_id = f"factual_episode:{episode_index:03d}"
        old_id = str(episode["factual_episode_id"])
        episode["factual_episode_id"] = episode_id
        for result in row["seed_results"]:
            for binding in result["bindings"]:
                if binding["factual_episode_id"] == old_id:
                    binding["factual_episode_id"] = episode_id
        for fragment_index, fragment in enumerate(episode["source_fragments"], 1):
            fragment["fragment_id"] = (
                f"{episode_id}:episode_source:{fragment_index:03d}"
            )
            fragment["fragment_kind"] = "episode_source"

    binding_index = 0
    for result in row["seed_results"]:
        for binding in result["bindings"]:
            binding_index += 1
            binding_id = f"binding:{binding_index:03d}"
            binding["binding_id"] = binding_id
            for kind, field in (
                ("actor_action", "actor_action_fragments"),
                ("context", "context_fragments"),
            ):
                for fragment_index, fragment in enumerate(binding[field], 1):
                    fragment["fragment_id"] = (
                        f"{binding_id}:{kind}:{fragment_index:03d}"
                    )
                    fragment["fragment_kind"] = kind


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--recovery", type=Path, required=True)
    parser.add_argument("--verification", type=Path, required=True)
    parser.add_argument("--call1", type=Path, required=True)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--definitions", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    output = _rows(args.base)
    base = {str(row["sub_question_id"]): row for row in output}
    recovery = {
        (str(row["sub_question_id"]), str(row["offense_ref"])): row
        for row in _rows(args.recovery)
    }
    verification = {
        (str(row["sub_question_id"]), str(row["offense_ref"])): row
        for row in _rows(args.verification)
    }
    call1 = {str(row["sub_question_id"]): row for row in _rows(args.call1)}
    inventory = {str(row["sub_question_id"]): row for row in _rows(args.inventory)}
    registry = load_definitions(args.definitions)
    merged: list[dict[str, Any]] = []
    derived_base: list[dict[str, Any]] = []

    for key, review in verification.items():
        recovered = recovery[key]
        if recovered.get("error") or not recovered.get("binding_count"):
            continue
        accepted = {
            int(value["proposal_index"])
            for value in review["decisions"] if value["accept"]
        }
        if not accepted:
            continue
        recovered_bindings = recovered["seed_results"][0]["bindings"]
        raw_bindings = recovered["raw_response"]["bindings"]
        if len(recovered_bindings) != len(raw_bindings):
            raise ValueError(f"{key}: normalized recovery changed proposal cardinality")
        row = base[key[0]]
        seed_result = row["seed_results"][int(recovered["seed_index"])]
        if seed_result["offense_ref"] != key[1] or seed_result["bindings"]:
            raise ValueError(f"{key}: recovery target is not an empty exact seed slot")
        episode_by_id = {
            value["factual_episode_id"]: value
            for value in recovered["factual_episodes"]
        }
        for index in sorted(accepted):
            binding = copy.deepcopy(recovered_bindings[index])
            binding["factual_episode_id"] = _merge_episode(
                row, episode_by_id[binding["factual_episode_id"]]
            )
            seed_result["bindings"].append(binding)
            merged.append({
                "sub_question_id": key[0],
                "offense_ref": key[1],
                "proposal_index": index,
                "actor_id": binding["actor_id"],
            })

    # An authored status-aggravated offense shares its physical conduct carrier with
    # its declared base offense.  This is a candidate-universe closure, not a truth
    # projection: status and intent remain separately assessed in Call 2.
    for row in output:
        by_offense = {value["offense_ref"]: value for value in row["seed_results"]}
        for result in tuple(row["seed_results"]):
            if not result["bindings"]:
                continue
            entry = registry.get(str(result["offense_ref"]))
            constraints = entry.payload.get("participation_constraints", {}) if entry else {}
            status_policy = (
                constraints.get("aggravating_status_participation", {})
                if isinstance(constraints, dict) else {}
            )
            base_ref = status_policy.get("base_offense_ref")
            base_result = by_offense.get(base_ref)
            if not base_ref or base_result is None or base_result["bindings"]:
                continue
            base_result["bindings"] = copy.deepcopy(result["bindings"])
            for binding in base_result["bindings"]:
                binding["offense_ref"] = base_ref
                binding["seed_index"] = base_result["seed_index"]
            derived_base.append({
                "sub_question_id": row["sub_question_id"],
                "source_offense_ref": result["offense_ref"],
                "base_offense_ref": base_ref,
                "binding_count": len(base_result["bindings"]),
            })
        _renumber(row)
        source = inventory[str(row["sub_question_id"])]
        parse_issue_binding_result(
            {
                "factual_episodes": row["factual_episodes"],
                "seed_results": row["seed_results"],
            },
            seeds=call1[str(row["sub_question_id"])]["normalized_seeds"],
            case_text=str(source["question_text"]),
            candidate_actor_ids=question_actor_ids(str(source["question_prompt"])),
        )
        row["binding_count"] = sum(
            len(value["bindings"]) for value in row["seed_results"]
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in output)
    )
    manifest = {
        "step": "v2_call15_verified_direct_recovery_merge",
        "status": "SUCCEEDED",
        "base_sha256": _sha(args.base),
        "recovery_sha256": _sha(args.recovery),
        "verification_sha256": _sha(args.verification),
        "merged_direct_bindings": merged,
        "authored_base_offense_closures": derived_base,
        "case_count": len(output),
        "binding_count": sum(int(row["binding_count"]) for row in output),
    }
    args.out.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
