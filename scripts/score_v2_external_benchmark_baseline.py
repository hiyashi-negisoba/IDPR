#!/usr/bin/env python3
"""Deterministic keyword-match scorer for baseline free-text answers on LBOX/KBL.

Baselines (`run_baselines_experiment.py`, unmodified) only produce free text, so they
cannot be scored by the production `evaluate_call1`/`evaluate_call2` exact-match scorers,
which require closed-set structured output. This is a separate, new scorer for baseline
comparison only -- it does not touch `src/idpr/v2/benchmarks/external.py`.

LBOX: a catalog offense counts as "mentioned" if its canonical display_name (NFKC
normalized) appears verbatim in the answer text. KBL: a fixed conclusion phrase is
searched for first, falling back to a small positive/negative keyword scan (negative
checked first, since "인정되지 않는다" contains the substring "인정").
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.v2.registry import load_definitions
from idpr.v2.routing import router_catalog

DEFAULT_DEFINITIONS = ROOT / "data/v2/definitions"

KBL_POS_ANCHOR = "결론: 인과관계 인정"
KBL_NEG_ANCHOR = "결론: 인과관계 부정"
KBL_NEG_RE = re.compile(r"인과관계[가는을를]?\s*(부정|없다|없음|불성립|인정되지\s*않)")
KBL_POS_RE = re.compile(r"인과관계[가는을를]?\s*(인정|있다|있음|성립)")


def _normalize(text: str) -> str:
    return unicodedata.normalize("NFKC", text)


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


def _index_predictions(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    for row in rows:
        key = row.get("sub_question_id")
        if not isinstance(key, str) or not key:
            raise ValueError("every prediction row requires a non-empty sub_question_id")
        if key in output:
            raise ValueError(f"duplicate sub_question_id: {key}")
        output[key] = row
    return output


def _div(numerator: int, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


def _f1(precision: float | None, recall: float | None) -> float | None:
    if precision is None or recall is None:
        return None
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def score_lbox(gold_rows, prediction_rows, catalog) -> dict[str, Any]:
    predictions = _index_predictions(prediction_rows)
    names = {entry.definition_id: _normalize(entry.display_name) for entry in catalog}
    cases = []
    tp = pred_total = gold_total = full_hits = 0
    for gold in gold_rows:
        key = gold["id"]
        row = predictions.get(key)
        if row is None:
            raise ValueError(f"missing prediction for {key}")
        if row.get("error"):
            raise ValueError(f"{key}: prediction contains a failed baseline call")
        text = _normalize(row.get("generated_response", ""))
        mentioned = {ref for ref, name in names.items() if name and name in text}
        gold_refs = set(gold["gold_definition_refs"])
        tp += len(gold_refs & mentioned)
        pred_total += len(mentioned)
        gold_total += len(gold_refs)
        full_hit = gold_refs <= mentioned
        full_hits += int(full_hit)
        cases.append({"id": key, "gold": sorted(gold_refs), "mentioned": sorted(mentioned), "full_hit": full_hit})
    precision, recall = _div(tp, pred_total), _div(tp, gold_total)
    return {
        "task": "call1_baseline",
        "summary": {
            "cases": len(cases),
            "gold_definition_refs": gold_total,
            "mentioned_hits": tp,
            "case_full_hit_rate": _div(full_hits, len(cases)),
            "micro_precision": precision,
            "micro_recall": recall,
            "micro_f1": _f1(precision, recall),
        },
        "cases": cases,
    }


def _kbl_predicted_label(text: str) -> str:
    normalized = _normalize(text)
    if KBL_NEG_ANCHOR in normalized:
        return "FALSE"
    if KBL_POS_ANCHOR in normalized:
        return "TRUE"
    # Negative phrasing ("인정되지 않는다") contains the positive substring "인정", so the
    # negative scan must run first or every hedged negative reads back as positive.
    if KBL_NEG_RE.search(normalized):
        return "FALSE"
    if KBL_POS_RE.search(normalized):
        return "TRUE"
    return "UNKNOWN"


def score_kbl(gold_rows, prediction_rows) -> dict[str, Any]:
    predictions = _index_predictions(prediction_rows)
    labels = ("TRUE", "FALSE", "UNKNOWN")
    matrix = {gold: {pred: 0 for pred in labels} for gold in labels}
    cases = []
    covered = covered_correct = 0
    for gold in gold_rows:
        key = gold["id"]
        row = predictions.get(key)
        if row is None:
            raise ValueError(f"missing prediction for {key}")
        if row.get("error"):
            raise ValueError(f"{key}: prediction contains a failed baseline call")
        gold_label = gold["label"]
        predicted_label = _kbl_predicted_label(row.get("generated_response", ""))
        matrix[gold_label][predicted_label] += 1
        if predicted_label != "UNKNOWN":
            covered += 1
            covered_correct += int(predicted_label == gold_label)
        cases.append({"id": key, "gold": gold_label, "prediction": predicted_label})

    per_class = {}
    for label in labels:
        tp = matrix[label][label]
        support = sum(matrix[label].values())
        predicted = sum(matrix[gold][label] for gold in labels)
        precision, recall = _div(tp, predicted), _div(tp, support)
        per_class[label] = {"support": support, "precision": precision, "recall": recall, "f1": _f1(precision, recall)}
    total = len(cases)
    correct = sum(matrix[label][label] for label in labels)
    observed = [label for label in ("TRUE", "FALSE") if per_class[label]["support"]]
    observed_f1 = [float(per_class[label]["f1"] or 0.0) for label in observed]
    unknown = sum(matrix[gold]["UNKNOWN"] for gold in labels)
    return {
        "task": "call2_baseline",
        "summary": {
            "cases": total,
            "accuracy": _div(correct, total),
            "macro_f1_observed_gold": sum(observed_f1) / len(observed_f1) if observed_f1 else None,
            "macro_f1_labels": observed,
            "coverage": _div(covered, total),
            "selective_accuracy": _div(covered_correct, covered),
            "unknown_rate": _div(unknown, total),
            "per_class": per_class,
            "confusion_matrix": matrix,
        },
        "cases": cases,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmark", choices=("lbox_call1", "kbl_call2"), required=True)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--predictions", type=Path, required=True)
    parser.add_argument("--baseline-id", required=True)
    parser.add_argument("--definitions-dir", type=Path, default=DEFAULT_DEFINITIONS)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    manifest = _read_json(args.input_dir / "manifest.json")
    if manifest.get("benchmark") != args.benchmark:
        raise ValueError("benchmark does not match materialization manifest")
    expected_gold_hash = ((manifest.get("artifacts") or {}).get("gold") or {}).get("sha256")
    gold_path = args.input_dir / "gold.jsonl"
    if _file_hash(gold_path) != expected_gold_hash:
        raise ValueError("gold artifact drifted after preparation")

    gold = _read_jsonl(gold_path)
    predictions = [row for row in _read_jsonl(args.predictions) if row.get("baseline_id") == args.baseline_id]
    if not predictions:
        raise ValueError(f"no prediction rows found for baseline_id={args.baseline_id!r}")

    if args.benchmark == "lbox_call1":
        registry = load_definitions(args.definitions_dir)
        catalog = router_catalog(registry)
        result = score_lbox(gold, predictions, catalog)
    else:
        result = score_kbl(gold, predictions)

    result["benchmark"] = args.benchmark
    result["baseline_id"] = args.baseline_id
    result["scoring_method"] = "deterministic_keyword_match"
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))
    print(f"wrote {args.out}")


if __name__ == "__main__":
    main()
