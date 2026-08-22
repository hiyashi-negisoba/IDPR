#!/usr/bin/env python3
"""Adapts a frozen LBOX/KBL materialization into `run_baselines_experiment.py`'s
dataset jsonl shape (`sub_question_id`, `question_text`, `question_prompt`, `source`).

Baselines are run through the existing, unmodified `BaselineExperimentRunner` --
this script only reshapes rows into the schema that runner already expects.
Gold never passes through: only `model_inputs.jsonl` (already gold-free) is read.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

KBL_QUESTION_PROMPT = (
    "위 사실관계에서 [판단대상 원인]과 [판단대상 결과] 사이에 형법상 인과관계가 "
    "인정되는지 판단하시오. 마지막 줄에 반드시 다음 두 표현 중 하나만 정확히 사용하여 "
    "결론을 명시하시오: '결론: 인과관계 인정' 또는 '결론: 인과관계 부정'."
)


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected JSON object")
    return value


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    output = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{line_number}: expected JSON object")
        output.append(value)
    return output


def _file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _verify_lineage(manifest: dict[str, Any], *, benchmark: str, input_dir: Path) -> None:
    if manifest.get("benchmark") != benchmark:
        raise ValueError(f"manifest benchmark mismatch: {manifest.get('benchmark')!r} != {benchmark!r}")
    artifacts = manifest.get("artifacts") or {}
    for key, filename in (("gold", "gold.jsonl"), ("model_inputs", "model_inputs.jsonl")):
        expected = (artifacts.get(key) or {}).get("sha256")
        actual = _file_hash(input_dir / filename)
        if expected != actual:
            raise ValueError(f"materialized artifact drifted: {filename}")


def _lbox_row(row: dict[str, Any]) -> dict[str, Any]:
    payload = row["payload"]
    return {
        "sub_question_id": row["id"],
        "question_text": payload["case_text"],
        "question_prompt": payload["question_prompt"],
        "source": row.get("source", {}),
    }


def _kbl_row(row: dict[str, Any]) -> dict[str, Any]:
    payload = row["payload"]
    return {
        "sub_question_id": row["id"],
        "question_text": payload["evidence_occurrence"]["source_text"],
        "question_prompt": KBL_QUESTION_PROMPT,
        "source": row.get("source", {}),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", choices=("lbox_call1", "kbl_call2"), required=True)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    manifest = _read_json(args.input_dir / "manifest.json")
    _verify_lineage(manifest, benchmark=args.benchmark, input_dir=args.input_dir)

    rows = _read_jsonl(args.input_dir / "model_inputs.jsonl")
    convert = _lbox_row if args.benchmark == "lbox_call1" else _kbl_row
    converted = [convert(row) for row in rows]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in converted),
        encoding="utf-8",
    )
    print(f"{args.benchmark}: wrote {len(converted)} rows -> {args.out}")


if __name__ == "__main__":
    main()
