from __future__ import annotations

from collections import Counter
from typing import Any, Iterable, Mapping

TRUTH_LABELS = ("TRUE", "FALSE", "UNKNOWN")


def _index(rows: Iterable[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    out = {}
    for row in rows:
        key = row.get("id")
        if not isinstance(key, str) or not key:
            raise ValueError("every row requires id")
        if key in out:
            raise ValueError(f"duplicate id: {key}")
        out[key] = row
    return out


def _align(gold, pred):
    g, p = _index(gold), _index(pred)
    if set(g) != set(p):
        raise ValueError("gold/prediction id mismatch")
    return [(i, g[i], p[i]) for i in g]


def evaluate_call1(gold_rows, prediction_rows):
    results = []
    raw = closure = recovery = 0
    total = 0
    for key, gold, pred in _align(gold_rows, prediction_rows):
        refs = list(dict.fromkeys(gold.get("gold_definition_refs", [])))
        seeds = set(pred.get("seeds", []))
        candidates = set(pred.get("candidate_offense_refs", []))
        rows = []
        for ref in refs:
            total += 1
            r = ref in seeds
            c = ref in candidates
            raw += r
            closure += c
            recovery += c and not r
            rows.append({"definition_ref": ref, "raw_success": r, "closure_success": c})
        results.append({"id": key, "gold": rows})
    return {"task": "call1", "summary": {"gold_refs": total, "raw_successes": raw, "closure_successes": closure, "closure_recoveries": recovery}, "cases": results}


def evaluate_call2(gold_rows, prediction_rows):
    matrix = {x: {y: 0 for y in TRUTH_LABELS} for x in TRUTH_LABELS}
    cases = []
    for key, gold, pred in _align(gold_rows, prediction_rows):
        g, p = gold.get("label"), pred.get("label")
        if g not in TRUTH_LABELS or p not in TRUTH_LABELS:
            raise ValueError("invalid truth label")
        matrix[g][p] += 1
        cases.append({"id": key, "gold": g, "prediction": p})
    total = len(cases)
    correct = sum(matrix[x][x] for x in TRUTH_LABELS)
    return {"task": "call2", "summary": {"cases": total, "accuracy": correct / total if total else None, "confusion_matrix": matrix}, "cases": cases}


__all__ = ["TRUTH_LABELS", "evaluate_call1", "evaluate_call2"]
