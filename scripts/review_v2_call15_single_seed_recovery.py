#!/usr/bin/env python3
"""Independently verify recovery proposals against their authored semantic cue."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.neural.vllm_client import VLLMClient
from idpr.v2.issue_binding import binding_seed_cues, load_binding_seed_cue_catalog
from idpr.v2.registry import load_definitions


def _rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _schema(proposal_count: int) -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["decisions"],
        "properties": {
            "decisions": {
                "type": "array",
                "minItems": proposal_count,
                "maxItems": proposal_count,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["proposal_index", "accept", "reason_code", "semantic_anchor_quotes"],
                    "properties": {
                        "proposal_index": {"type": "integer", "minimum": 0},
                        "accept": {"type": "boolean"},
                        "reason_code": {
                            "type": "string",
                            "enum": [
                                "DIRECT_CONDUCT",
                                "CONCRETE_PREPARATION_OR_ATTEMPT",
                                "CONCRETE_REQUEST_OR_ASSISTANCE",
                                "MATCHING_OMISSION_OR_FALSEHOOD",
                                "ONLY_BROAD_TOPIC_OVERLAP",
                                "DIFFERENT_CONDUCT",
                                "INSUFFICIENT_EXPLICIT_LINK",
                            ],
                        },
                        "semantic_anchor_quotes": {
                            "type": "array",
                            "items": {"type": "string"},
                            "uniqueItems": True,
                        },
                    },
                },
            }
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--recovery", type=Path, required=True)
    parser.add_argument("--definitions", type=Path, required=True)
    parser.add_argument("--binding-cues", type=Path, required=True)
    parser.add_argument("--system-prompt", type=Path, required=True)
    parser.add_argument("--user-prompt", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    registry = load_definitions(args.definitions)
    cues = load_binding_seed_cue_catalog(args.binding_cues)
    client = VLLMClient(args.base_url, args.model, "local-idpr")
    system_prompt = args.system_prompt.read_text(encoding="utf-8")
    user_prompt = args.user_prompt.read_text(encoding="utf-8")
    output: list[dict[str, Any]] = []
    for index, row in enumerate(_rows(args.recovery), 1):
        proposals = (row.get("raw_response") or {}).get("bindings") or []
        if not proposals:
            continue
        cue = binding_seed_cues(
            registry, (str(row["offense_ref"]),), cue_catalog=cues
        )[0]
        payload = {"seed": cue.as_dict(), "proposals": proposals}
        raw, metadata = client.complete_json(
            system_prompt=system_prompt,
            user_template=user_prompt,
            payload=payload,
            schema_name="v2_call15_single_seed_recovery_verifier",
            schema=_schema(len(proposals)),
            max_tokens=1024,
            temperature=0.0,
            seed=1,
        )
        decisions = raw["decisions"]
        indices = [int(value["proposal_index"]) for value in decisions]
        if indices != list(range(len(proposals))):
            raise ValueError(f"{row['sub_question_id']}/{row['offense_ref']}: decision order mismatch")
        output.append(
            {
                "sub_question_id": row["sub_question_id"],
                "offense_ref": row["offense_ref"],
                "proposal_count": len(proposals),
                "accepted_count": sum(bool(value["accept"]) for value in decisions),
                "decisions": decisions,
                "usage": metadata.get("usage", {}),
            }
        )
        print(
            f"[{index}] {row['sub_question_id']}/{row['offense_ref']}: "
            f"{output[-1]['accepted_count']}/{len(proposals)}"
        )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as handle:
        for row in output:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
