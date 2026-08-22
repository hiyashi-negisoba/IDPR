#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.v2.benchmarks.external import evaluate_call1, evaluate_call2


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


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", choices=("lbox_call1", "kbl_call2"), required=True)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    manifest = _read_json(args.input_dir / "manifest.json")
    if manifest.get("benchmark") != args.benchmark:
        raise ValueError("benchmark does not match materialization manifest")
    expected_gold_hash = ((manifest.get("artifacts") or {}).get("gold") or {}).get("sha256")
    gold_path = args.input_dir / "gold.jsonl"
    if _file_hash(gold_path) != expected_gold_hash:
        raise ValueError("gold artifact drifted after preparation")

    prediction_manifest_path = args.predictions.with_suffix(".manifest.json")
    prediction_manifest = _read_json(prediction_manifest_path)
    if prediction_manifest.get("benchmark") != args.benchmark:
        raise ValueError("benchmark does not match prediction manifest")
    input_manifest_hash = _file_hash(args.input_dir / "manifest.json")
    if prediction_manifest.get("input_manifest_sha256") != input_manifest_hash:
        raise ValueError("predictions were produced from a different materialization manifest")
    if prediction_manifest.get("predictions_sha256") != _file_hash(args.predictions):
        raise ValueError("prediction artifact drifted after model execution")

    gold = _read_jsonl(gold_path)
    predictions = _read_jsonl(args.predictions)
    failed = [row.get("id") for row in predictions if row.get("error")]
    if failed:
        raise ValueError(f"predictions contain failed model calls: {failed[:20]}")

    if args.benchmark == "lbox_call1":
        result = evaluate_call1(gold, predictions)
    else:
        result = evaluate_call2(gold, predictions)
        summary = result["summary"]
        summary["macro_f1"] = summary["macro_f1_observed_gold"]
        summary["macro_f1_labels"] = [
            label
            for label, metrics in summary["per_class"].items()
            if metrics["support"]
        ]
    result["benchmark"] = args.benchmark
    result["dataset_scope"] = {
        "source": manifest.get("source"),
        "summary": manifest.get("summary"),
        "coverage": manifest.get("coverage"),
    }
    result["artifacts"] = {
        "materialization_manifest_sha256": input_manifest_hash,
        "prediction_manifest_sha256": _file_hash(prediction_manifest_path),
        "gold_sha256": _file_hash(gold_path),
        "predictions_sha256": _file_hash(args.predictions),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
