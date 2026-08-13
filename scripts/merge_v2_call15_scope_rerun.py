#!/usr/bin/env python3
"""Merge only explicitly rerun scope-changed rows into a Call 1.5 artifact."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--rerun", type=Path, required=True)
    parser.add_argument("--replace-case", action="append", required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    base_rows = _jsonl(args.base)
    rerun = {row["sub_question_id"]: row for row in _jsonl(args.rerun)}
    replacements = set(args.replace_case)
    if replacements - set(rerun):
        raise ValueError(f"rerun artifact lacks cases: {sorted(replacements - set(rerun))}")
    output = [
        rerun[row["sub_question_id"]]
        if row["sub_question_id"] in replacements
        else row
        for row in base_rows
    ]
    if any(row.get("error") for row in output):
        raise ValueError("merged artifact contains unsuccessful rows")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in output),
        encoding="utf-8",
    )
    manifest = {
        "step": "v2_call15_scope_change_causal_merge",
        "status": "SUCCEEDED",
        "rule": "replace only rows whose deterministic factual scope changed",
        "base_artifact": str(args.base),
        "base_artifact_sha256": _sha256(args.base),
        "rerun_artifact": str(args.rerun),
        "rerun_artifact_sha256": _sha256(args.rerun),
        "replaced_case_ids": sorted(replacements),
        "case_count": len(output),
        "binding_count": sum(int(row.get("binding_count", 0)) for row in output),
    }
    args.out.with_suffix(".manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
