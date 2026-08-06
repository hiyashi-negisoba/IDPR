"""Pure contracts and aggregation for the sealed Phase-3 KCL LLM judge."""

from __future__ import annotations

import hashlib
import json
import random
from collections import Counter
from pathlib import Path
from statistics import fmean
from typing import Any, Iterable, Mapping, Sequence

from idpr.eval.rubric import RubricSet, Verdict, apply_safeguards, score_answer


class JudgeContractError(ValueError):
    """The model response or a method artifact violates the evaluation contract."""


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise JudgeContractError(f"expected a JSON object: {path}")
    return value


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise JudgeContractError(f"{path}:{line_number} is not an object")
        rows.append(value)
    return rows


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_sha256(value: Any) -> str:
    encoded = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def index_unique(
    rows: Iterable[Mapping[str, Any]], *, key: str, source: str
) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for row in rows:
        row_id = str(row.get(key, "")).strip()
        if not row_id:
            raise JudgeContractError(f"{source} has a row without {key}")
        if row_id in indexed:
            raise JudgeContractError(f"{source} has duplicate {key}={row_id}")
        indexed[row_id] = dict(row)
    return indexed


def load_method_answers(
    *,
    project_root: Path,
    methods_manifest_path: Path,
    expected_case_ids: Sequence[str],
    selected_methods: Sequence[str] = (),
) -> tuple[dict[str, dict[str, str]], dict[str, Path]]:
    """Load and strictly inner-join baseline-compatible method outputs."""

    manifest = read_json(methods_manifest_path)
    raw_methods = manifest.get("methods")
    if not isinstance(raw_methods, Mapping):
        raise JudgeContractError("methods manifest has no methods object")
    method_ids = list(selected_methods) if selected_methods else list(raw_methods)
    unknown = sorted(set(method_ids) - set(raw_methods))
    if unknown:
        raise JudgeContractError(f"unknown methods: {unknown}")

    expected = set(expected_case_ids)
    answers: dict[str, dict[str, str]] = {}
    paths: dict[str, Path] = {}
    for method_id in method_ids:
        configured = Path(str(raw_methods[method_id]))
        path = configured if configured.is_absolute() else project_root / configured
        if not path.is_file():
            raise JudgeContractError(f"method output is missing: {method_id} -> {path}")
        indexed = index_unique(
            read_jsonl(path), key="sub_question_id", source=f"method {method_id}"
        )
        missing = sorted(expected - set(indexed))
        if missing:
            raise JudgeContractError(
                f"method {method_id} is missing {len(missing)} sealed cases: {missing}"
            )
        joined: dict[str, str] = {}
        for case_id in expected_case_ids:
            row = indexed[case_id]
            if row.get("error"):
                raise JudgeContractError(f"method {method_id} case {case_id} has an error")
            answer = str(row.get("generated_response", "")).strip()
            if not answer:
                raise JudgeContractError(f"method {method_id} case {case_id} is empty")
            joined[case_id] = answer
        answers[method_id] = joined
        paths[method_id] = path
    return answers, paths


def _normalized(text: str) -> str:
    return "".join(character for character in str(text) if character.isalnum())


def evidence_in_answer(quote: str, answer: str, *, minimum: int) -> bool:
    normalized_quote = _normalized(quote)
    return len(normalized_quote) >= minimum and normalized_quote in _normalized(answer)


def _validate_rubric_indices(
    assessments: Sequence[Mapping[str, Any]], rubric_count: int
) -> None:
    indices = [int(item["index"]) for item in assessments]
    expected = list(range(1, rubric_count + 1))
    if indices != expected:
        raise JudgeContractError(
            "rubric_assessments must contain every rubric exactly once in input order; "
            f"got {indices}, expected {expected}"
        )


def reduce_judge_output(
    *,
    output: Mapping[str, Any],
    answer: str,
    rubric_set: RubricSet,
    protocol: Mapping[str, Any],
) -> dict[str, Any]:
    """Apply evidence safeguards and reduce one structured judge response."""

    status_to_verdict = {"met": "O", "partially_met": "P", "not_met": "X"}
    status_to_weight = {"met": 1.0, "partially_met": 0.5, "not_met": 0.0}
    rubric_assessments = list(output["rubric_assessments"])
    _validate_rubric_indices(rubric_assessments, len(rubric_set))
    verdicts = [
        Verdict(
            index=int(item["index"]),
            verdict=status_to_verdict[str(item["status"])],
            quote=str(item["answer_quote"]),
        )
        for item in rubric_assessments
    ]
    raw_binary = [status_to_weight[str(item["status"])] for item in rubric_assessments]
    binary = apply_safeguards(verdicts, answer=answer, rubrics=rubric_set.rubrics)
    coverage = score_answer(binary, rubric_set.item_types)

    minimum = int(protocol["evidence_min_normalized_characters"])
    precision_config = protocol["precision"]
    allowed_claim_classes = set(precision_config["claim_classes"])
    numerator_classes = set(precision_config["numerator_classes"])
    claims = list(output["claims"])
    claim_ids = [int(claim["claim_id"]) for claim in claims]
    if len(claim_ids) != len(set(claim_ids)):
        raise JudgeContractError("claim_id values must be unique")
    claim_counts: Counter[str] = Counter()
    for claim in claims:
        classification = str(claim["classification"])
        if classification not in allowed_claim_classes:
            raise JudgeContractError(f"unknown claim classification: {classification}")
        if not evidence_in_answer(str(claim["answer_quote"]), answer, minimum=minimum):
            raise JudgeContractError(
                f"claim {claim['claim_id']} cites text absent from the answer"
            )
        rubric_indices = [int(index) for index in claim["rubric_indices"]]
        if any(index < 1 or index > len(rubric_set) for index in rubric_indices):
            raise JudgeContractError(
                f"claim {claim['claim_id']} has an out-of-range rubric index"
            )
        claim_counts[classification] += 1
    claim_total = len(claims)
    precision_numerator = sum(claim_counts[name] for name in numerator_classes)

    severity_weights = {
        str(name): int(weight)
        for name, weight in protocol["hallucination"]["severity_weights"].items()
    }
    valid_hallucinations: list[dict[str, Any]] = []
    dropped_hallucinations = 0
    for incident in output["hallucinations"]:
        if evidence_in_answer(str(incident["answer_quote"]), answer, minimum=minimum):
            valid_hallucinations.append(dict(incident))
        else:
            dropped_hallucinations += 1
    hallucination_penalty = sum(
        severity_weights[str(incident["severity"])] for incident in valid_hallucinations
    )

    consistency_config = protocol["consistency"]
    maximum_consistency = int(consistency_config["maximum"])
    raw_consistency = dict(output["consistency"])
    valid_violations: list[dict[str, Any]] = []
    dropped_consistency_violations = 0
    for violation in raw_consistency["violations"]:
        quotes = [str(quote) for quote in violation["answer_quotes"]]
        if all(evidence_in_answer(quote, answer, minimum=minimum) for quote in quotes):
            valid_violations.append(dict(violation))
        else:
            dropped_consistency_violations += 1
    consistency_score = int(raw_consistency["score"])
    if not valid_violations:
        consistency_score = maximum_consistency

    return {
        "coverage": {
            **coverage,
            "binary": binary,
            "raw_binary": raw_binary,
        },
        "precision": {
            "numerator": precision_numerator,
            "total_claims": claim_total,
            "score": precision_numerator / claim_total if claim_total else None,
            "claim_counts": dict(claim_counts),
        },
        "hallucination": {
            "score": -hallucination_penalty,
            "penalty": hallucination_penalty,
            "incident_count": len(valid_hallucinations),
            "incidents": valid_hallucinations,
        },
        "consistency": {
            "score": consistency_score,
            "normalized_score": consistency_score / maximum_consistency,
            "violations": valid_violations,
            "rationale": raw_consistency["rationale"],
        },
        "safeguards": {
            "rubric_met_downgrades": sum(raw_binary) - sum(binary),
            "dropped_hallucinations": dropped_hallucinations,
            "dropped_consistency_violations": dropped_consistency_violations,
        },
    }


def _mean(values: Sequence[float]) -> float | None:
    return fmean(values) if values else None


def aggregate_records(
    records: Sequence[Mapping[str, Any]], *, expected_case_ids: Sequence[str]
) -> dict[str, Any]:
    """Produce method-level macro/micro summaries without dropping failures silently."""

    by_method: dict[str, list[Mapping[str, Any]]] = {}
    for record in records:
        by_method.setdefault(str(record["method_id"]), []).append(record)
    summary: dict[str, Any] = {}
    expected = set(expected_case_ids)
    for method_id, method_records in sorted(by_method.items()):
        completed = [record for record in method_records if record.get("status") == "ok"]
        completed_ids = {str(record["sub_question_id"]) for record in completed}
        metrics = [record["metrics"] for record in completed]
        coverage_values = [float(value["coverage"]["rubric_score"]) for value in metrics]
        precision_values = [
            float(value["precision"]["score"])
            for value in metrics
            if value["precision"]["score"] is not None
        ]
        claim_numerator = sum(int(value["precision"]["numerator"]) for value in metrics)
        claim_total = sum(int(value["precision"]["total_claims"]) for value in metrics)
        hallucination_scores = [float(value["hallucination"]["score"]) for value in metrics]
        consistency_values = [
            float(value["consistency"]["normalized_score"]) for value in metrics
        ]
        question_variants: Counter[str] = Counter(
            str(record.get("question_variant", "unknown")) for record in completed
        )
        summary[method_id] = {
            "completed_cases": len(completed),
            "failed_cases": len(method_records) - len(completed),
            "missing_cases": sorted(expected - completed_ids),
            "coverage_macro": _mean(coverage_values),
            "precision_macro": _mean(precision_values),
            "precision_micro": claim_numerator / claim_total if claim_total else None,
            "precision_null_cases": len(metrics) - len(precision_values),
            "hallucination_score_total": sum(hallucination_scores),
            "hallucination_score_macro": _mean(hallucination_scores),
            "hallucination_free_rate": (
                sum(score == 0 for score in hallucination_scores) / len(hallucination_scores)
                if hallucination_scores
                else None
            ),
            "consistency_macro": _mean(consistency_values),
            "question_variants": dict(question_variants),
        }
    return {"methods": summary}


def paired_bootstrap_deltas(
    records: Sequence[Mapping[str, Any]],
    *,
    target_method: str,
    metric_path: Sequence[str],
    samples: int,
    seed: int,
) -> dict[str, Any]:
    """Case-paired macro delta confidence intervals against every other method."""

    values: dict[str, dict[str, float]] = {}
    for record in records:
        if record.get("status") != "ok":
            continue
        value: Any = record["metrics"]
        for key in metric_path:
            value = value[key]
        if value is not None:
            values.setdefault(str(record["method_id"]), {})[
                str(record["sub_question_id"])
            ] = float(value)
    if target_method not in values:
        raise JudgeContractError(f"bootstrap target has no values: {target_method}")
    rng = random.Random(seed)
    comparisons: dict[str, Any] = {}
    for baseline, baseline_values in sorted(values.items()):
        if baseline == target_method:
            continue
        case_ids = sorted(set(values[target_method]) & set(baseline_values))
        observed = fmean(
            values[target_method][case_id] - baseline_values[case_id]
            for case_id in case_ids
        )
        draws = []
        for _ in range(samples):
            sampled = [rng.choice(case_ids) for _ in case_ids]
            draws.append(
                fmean(
                    values[target_method][case_id] - baseline_values[case_id]
                    for case_id in sampled
                )
            )
        draws.sort()
        lower = draws[int(0.025 * (samples - 1))]
        upper = draws[int(0.975 * (samples - 1))]
        comparisons[baseline] = {
            "paired_cases": len(case_ids),
            "delta": observed,
            "ci95": [lower, upper],
        }
    return {
        "target_method": target_method,
        "metric_path": list(metric_path),
        "samples": samples,
        "seed": seed,
        "comparisons": comparisons,
    }
