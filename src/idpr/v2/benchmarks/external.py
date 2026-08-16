from __future__ import annotations

from collections import Counter
from collections.abc import Iterable, Mapping, Sequence
from typing import Any

TRUTH_LABELS = ("TRUE", "FALSE", "UNKNOWN")


def _strings(value: Any, where: str) -> tuple[str, ...]:
    if not isinstance(value, Sequence) or isinstance(value, (str, bytes)):
        raise ValueError(f"{where} must be a sequence of strings")
    output = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item:
            raise ValueError(f"{where}[{index}] must be a non-empty string")
        output.append(item)
    return tuple(dict.fromkeys(output))


def _index(rows: Iterable[Mapping[str, Any]]) -> dict[str, Mapping[str, Any]]:
    output = {}
    for row in rows:
        key = row.get("id")
        if not isinstance(key, str) or not key:
            raise ValueError("every row requires a non-empty string id")
        if key in output:
            raise ValueError(f"duplicate id: {key}")
        output[key] = row
    return output


def _align(gold_rows, prediction_rows):
    gold = _index(gold_rows)
    predictions = _index(prediction_rows)
    if set(gold) != set(predictions):
        missing = sorted(set(gold) - set(predictions))
        extra = sorted(set(predictions) - set(gold))
        raise ValueError(
            f"gold/prediction id mismatch: missing={missing[:10]} extra={extra[:10]}"
        )
    return [(key, gold[key], predictions[key]) for key in gold]


def _div(numerator: int, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


def _f1(precision: float | None, recall: float | None) -> float | None:
    if precision is None or recall is None:
        return None
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def evaluate_call1(gold_rows, prediction_rows):
    cases = []
    counts: Counter[str] = Counter()
    raw_tp = raw_pred = closure_tp = closure_pred = gold_total = 0
    for key, gold, prediction in _align(gold_rows, prediction_rows):
        refs = _strings(gold.get("gold_definition_refs"), "gold_definition_refs")
        seeds = _strings(prediction.get("seeds"), "seeds")
        candidates = _strings(
            prediction.get("candidate_offense_refs"), "candidate_offense_refs"
        )
        if not refs:
            raise ValueError(f"{key}: empty gold_definition_refs")
        gold_set, seed_set, candidate_set = set(refs), set(seeds), set(candidates)
        details = []
        for ref in refs:
            raw_success = ref in seed_set
            closure_success = ref in candidate_set
            counts["raw_successes"] += int(raw_success)
            counts["closure_successes"] += int(closure_success)
            counts["closure_recoveries"] += int(closure_success and not raw_success)
            details.append(
                {
                    "definition_ref": ref,
                    "raw_success": raw_success,
                    "closure_success": closure_success,
                }
            )
        raw_full = gold_set <= seed_set
        closure_full = gold_set <= candidate_set
        counts["raw_case_full_hits"] += int(raw_full)
        counts["closure_case_full_hits"] += int(closure_full)
        counts["cases"] += 1
        gold_total += len(gold_set)
        raw_tp += len(gold_set & seed_set)
        raw_pred += len(seed_set)
        closure_tp += len(gold_set & candidate_set)
        closure_pred += len(candidate_set)
        cases.append(
            {
                "id": key,
                "raw_case_full_hit": raw_full,
                "closure_case_full_hit": closure_full,
                "gold": details,
            }
        )
    raw_precision, raw_recall = _div(raw_tp, raw_pred), _div(raw_tp, gold_total)
    closure_precision = _div(closure_tp, closure_pred)
    closure_recall = _div(closure_tp, gold_total)
    total_cases = counts["cases"]
    return {
        "task": "call1",
        "summary": {
            "cases": total_cases,
            "gold_definition_refs": gold_total,
            "raw_successes": counts["raw_successes"],
            "closure_successes": counts["closure_successes"],
            "closure_recoveries": counts["closure_recoveries"],
            "raw_survival_rate": _div(counts["raw_successes"], gold_total),
            "closure_survival_rate": _div(counts["closure_successes"], gold_total),
            "raw_case_full_hit_rate": _div(counts["raw_case_full_hits"], total_cases),
            "closure_case_full_hit_rate": _div(
                counts["closure_case_full_hits"], total_cases
            ),
            "raw_micro_precision": raw_precision,
            "raw_micro_recall": raw_recall,
            "raw_micro_f1": _f1(raw_precision, raw_recall),
            "closure_micro_precision": closure_precision,
            "closure_micro_recall": closure_recall,
            "closure_micro_f1": _f1(closure_precision, closure_recall),
        },
        "cases": cases,
    }


def evaluate_call2(gold_rows, prediction_rows):
    matrix = {gold: {pred: 0 for pred in TRUTH_LABELS} for gold in TRUTH_LABELS}
    cases = []
    covered = covered_correct = 0
    for key, gold, prediction in _align(gold_rows, prediction_rows):
        gold_label, predicted_label = gold.get("label"), prediction.get("label")
        if gold_label not in TRUTH_LABELS or predicted_label not in TRUTH_LABELS:
            raise ValueError(f"{key}: invalid truth label")
        matrix[gold_label][predicted_label] += 1
        if predicted_label != "UNKNOWN":
            covered += 1
            covered_correct += int(predicted_label == gold_label)
        cases.append({"id": key, "gold": gold_label, "prediction": predicted_label})

    per_class = {}
    for label in TRUTH_LABELS:
        tp = matrix[label][label]
        support = sum(matrix[label].values())
        predicted = sum(matrix[gold][label] for gold in TRUTH_LABELS)
        precision, recall = _div(tp, predicted), _div(tp, support)
        per_class[label] = {
            "support": support,
            "precision": precision,
            "recall": recall,
            "f1": _f1(precision, recall),
        }
    total = len(cases)
    correct = sum(matrix[label][label] for label in TRUTH_LABELS)
    fixed_f1 = [float(per_class[label]["f1"] or 0.0) for label in TRUTH_LABELS]
    observed = [label for label in TRUTH_LABELS if per_class[label]["support"]]
    observed_f1 = [float(per_class[label]["f1"] or 0.0) for label in observed]
    unknown = sum(matrix[gold]["UNKNOWN"] for gold in TRUTH_LABELS)
    return {
        "task": "call2",
        "summary": {
            "cases": total,
            "accuracy": _div(correct, total),
            "macro_f1_fixed_3way": sum(fixed_f1) / 3 if total else None,
            "macro_f1_observed_gold": (
                sum(observed_f1) / len(observed_f1) if observed_f1 else None
            ),
            "coverage": _div(covered, total),
            "selective_accuracy": _div(covered_correct, covered),
            "unknown_rate": _div(unknown, total),
            "per_class": per_class,
            "confusion_matrix": matrix,
        },
        "cases": cases,
    }


__all__ = ["TRUTH_LABELS", "evaluate_call1", "evaluate_call2"]
