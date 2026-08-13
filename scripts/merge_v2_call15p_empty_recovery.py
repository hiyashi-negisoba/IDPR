#!/usr/bin/env python3
"""Causally replace selected empty Call 1.5-P episodes with reviewed recovery rows."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _rows(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--recovery", type=Path, required=True)
    parser.add_argument("--replace", action="append", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    selections = set()
    for value in args.replace:
        try:
            case_id, episode_id = value.split("/", 1)
        except ValueError as exc:
            raise ValueError("--replace must be CASE_ID/EPISODE_ID") from exc
        selections.add((case_id, episode_id))
    base = _rows(args.base)
    recovery = {
        row["sub_question_id"]: row for row in _rows(args.recovery)
    }
    seen: set[tuple[str, str]] = set()
    for row in base:
        case_id = row["sub_question_id"]
        recovered_by_episode = {
            value["factual_episode_id"]: value
            for value in recovery[case_id]["episode_results"]
        }
        for index, episode in enumerate(row["episode_results"]):
            key = (case_id, episode["factual_episode_id"])
            if key not in selections:
                continue
            replacement = recovered_by_episode[episode["factual_episode_id"]]
            if episode.get("interaction_count") != 0:
                raise ValueError(f"{key}: base episode is not empty")
            if replacement.get("interaction_count", 0) <= 0 or "error" in replacement:
                raise ValueError(f"{key}: recovery episode is not successful/non-empty")
            row["episode_results"][index] = replacement
            seen.add(key)
        row["interactions"] = [
            interaction
            for episode in row["episode_results"]
            for interaction in episode.get("interactions", [])
        ]
        row["interaction_count"] = len(row["interactions"])
        row["error"] = None
    if seen != selections:
        raise ValueError(f"unresolved replacements: {sorted(selections - seen)}")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in base),
        encoding="utf-8",
    )
    manifest = {
        "step": "v2_call15_factual_interaction_causal_merge",
        "status": "SUCCEEDED",
        "replacement_count": len(selections),
        "replacements": [
            {"sub_question_id": case_id, "factual_episode_id": episode_id}
            for case_id, episode_id in sorted(selections)
        ],
        "case_count": len(base),
        "interaction_count": sum(row["interaction_count"] for row in base),
        "base_artifact": str(args.base),
        "base_sha256": _sha256(args.base),
        "recovery_artifact": str(args.recovery),
        "recovery_sha256": _sha256(args.recovery),
    }
    args.out.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
