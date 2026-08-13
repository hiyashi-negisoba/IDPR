#!/usr/bin/env python3
"""Revalidate only failed Call 1.5 rows with bounded host normalization."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.eval.input_formatter import scoped_question_text
from idpr.v2.issue_binding import (
    normalize_issue_binding_output,
    question_actor_ids,
    validate_issue_binding_output,
)


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    inventory = {
        row["sub_question_id"]: row for row in _jsonl(args.inventory)
    }
    rows = _jsonl(args.input)
    repaired_ids: list[str] = []
    normalization_count = 0
    for row in rows:
        if "error" not in row:
            continue
        case_id = row["sub_question_id"]
        source = inventory[case_id]
        case_text = source["question_text"]
        factual_scope_text = scoped_question_text(
            case_text, source["question_prompt"]
        )
        model_raw = row["raw_response"]
        normalized, changes = normalize_issue_binding_output(
            model_raw,
            case_text=case_text,
            factual_scope_text=factual_scope_text,
        )
        result = validate_issue_binding_output(
            normalized,
            seeds=row["seeds"],
            case_text=case_text,
            factual_scope_text=factual_scope_text,
            candidate_actor_ids=question_actor_ids(source["question_prompt"]),
        )
        row.pop("error", None)
        row.pop("errors", None)
        row.update(
            {
                **result.as_dict(),
                "binding_count": len(result.bindings),
                "model_raw_response": model_raw,
                "raw_response": normalized,
                "host_normalizations": list(changes),
                "recovered_from_contract_error": True,
            }
        )
        repaired_ids.append(case_id)
        normalization_count += len(changes)

    remaining = [row["sub_question_id"] for row in rows if "error" in row]
    if remaining:
        raise ValueError(f"rows remain invalid: {remaining}")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )

    source_manifest_path = args.input.with_suffix(".manifest.json")
    manifest = json.loads(source_manifest_path.read_text(encoding="utf-8"))
    manifest.update(
        {
            "status": "SUCCEEDED",
            "failed_case_count": 0,
            "binding_count": sum(int(row.get("binding_count", 0)) for row in rows),
            "host_contract_repair": {
                "source_artifact": str(args.input),
                "source_artifact_sha256": _sha256(args.input),
                "repaired_case_ids": repaired_ids,
                "repaired_case_count": len(repaired_ids),
                "normalization_count": normalization_count,
                "new_model_calls": 0,
                "rules": [
                    "unique_single_edit_source_quote",
                    "unique_single_elision_split",
                    "binding_quote_added_to_declared_episode_scope",
                ],
            },
        }
    )
    args.out.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"repaired {len(repaired_ids)} failed rows with {normalization_count} "
        f"recorded normalizations; wrote {args.out}"
    )


if __name__ == "__main__":
    main()
