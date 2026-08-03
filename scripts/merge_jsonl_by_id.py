#!/usr/bin/env python3
"""Replace rows in a JSONL artifact by a unique identifier, preserving base order."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_rows(path: Path) -> list[dict[str, Any]]:
    rows = [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    if not all(isinstance(row, dict) for row in rows):
        raise ValueError(f"{path} contains a non-object row")
    return rows


def merge_rows(
    base: list[dict[str, Any]],
    replacements: list[dict[str, Any]],
    *,
    id_field: str,
    required_fields: tuple[str, ...],
    rejected_fields: tuple[str, ...],
) -> list[dict[str, Any]]:
    base_ids = [str(row.get(id_field, "")) for row in base]
    replacement_ids = [str(row.get(id_field, "")) for row in replacements]
    if not all(base_ids) or len(base_ids) != len(set(base_ids)):
        raise ValueError("base rows must have unique non-empty identifiers")
    if not all(replacement_ids) or len(replacement_ids) != len(set(replacement_ids)):
        raise ValueError("replacement rows must have unique non-empty identifiers")
    unknown = sorted(set(replacement_ids) - set(base_ids))
    if unknown:
        raise ValueError(f"replacement identifiers are absent from base: {unknown}")
    for row in replacements:
        row_id = str(row[id_field])
        missing = [field for field in required_fields if field not in row]
        rejected = [field for field in rejected_fields if field in row]
        if missing or rejected:
            raise ValueError(
                f"replacement {row_id} failed field gates: missing={missing}, rejected={rejected}"
            )
    replacement_map = {
        str(row[id_field]): dict(row) for row in replacements
    }
    return [replacement_map.get(str(row[id_field]), dict(row)) for row in base]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--replacements", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--id-field", default="sub_question_id")
    parser.add_argument("--require-field", action="append", default=[])
    parser.add_argument("--reject-field", action="append", default=[])
    args = parser.parse_args()
    merged = merge_rows(
        load_rows(args.base),
        load_rows(args.replacements),
        id_field=args.id_field,
        required_fields=tuple(args.require_field),
        rejected_fields=tuple(args.reject_field),
    )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.out.with_suffix(args.out.suffix + ".tmp")
    temporary.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in merged),
        encoding="utf-8",
    )
    temporary.replace(args.out)
    print(f"wrote {len(merged)} rows to {args.out}")


if __name__ == "__main__":
    main()
