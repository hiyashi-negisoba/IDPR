#!/usr/bin/env python3
"""Collect the three conditions the judge will score into one bundle.

Baseline, N and P answer the same 26 questions and were produced at different times by
different code paths, so the bundle normalizes them to one schema and records where each
one came from.  Nothing here scores or edits an answer.

The manifest is the point of this script as much as the answers are: it carries the
provenance of each condition, every automatic audit number already established, and the
generation parameters that differ between conditions.  A difference recorded in the
manifest can be reasoned about later; one that is quietly normalized away cannot.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def rows(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def sha16(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def manifest_path(path: Path) -> str:
    """Keep project-local artifacts portable, without rejecting an explicit path."""
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(ROOT))
    except ValueError:
        return str(resolved)


def audit(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8")).get("summary")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, default=ROOT / "experiments/v2_call15_directscope_26_causal")
    parser.add_argument(
        "--baseline",
        type=Path,
        default=ROOT / "experiments/results/baseline_greedy_26/vanilla_zero_shot_outputs.jsonl",
    )
    parser.add_argument(
        "--n-answers",
        type=Path,
        help="fresh N-condition Call 3 answers; defaults to the historical run-root layout",
    )
    parser.add_argument(
        "--n-plans",
        type=Path,
        help="fresh N-condition AnswerPlan artifact; defaults to the historical run-root layout",
    )
    parser.add_argument(
        "--p-answers",
        type=Path,
        help="fresh P-condition Call 3 answers; defaults to the historical run-root layout",
    )
    parser.add_argument(
        "--p-plans",
        type=Path,
        help="fresh P-condition AnswerPlan artifact; defaults to the historical run-root layout",
    )
    parser.add_argument(
        "--before-n-answers",
        type=Path,
        help="frozen pre-improvement N answers to include beside the fresh integrated run",
    )
    parser.add_argument(
        "--before-n-plans",
        type=Path,
        help="frozen pre-improvement N AnswerPlan artifact",
    )
    parser.add_argument(
        "--before-p-answers",
        type=Path,
        help="frozen pre-improvement P answers to include beside the fresh integrated run",
    )
    parser.add_argument(
        "--before-p-plans",
        type=Path,
        help="frozen pre-improvement P AnswerPlan artifact",
    )
    parser.add_argument("--n-method-id", default="v2_idpr_n_greedy_26")
    parser.add_argument("--p-method-id", default="v2_idpr_p_greedy_26")
    parser.add_argument("--before-n-method-id", default="v2_before_n_greedy_26")
    parser.add_argument("--before-p-method-id", default="v2_before_p_greedy_26")
    parser.add_argument(
        "--baseline-method-id", default="v2_baseline_vanilla_greedy_26"
    )
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    if bool(args.before_n_answers) != bool(args.before_n_plans):
        parser.error("--before-n-answers and --before-n-plans must be supplied together")
    if bool(args.before_p_answers) != bool(args.before_p_plans):
        parser.error("--before-p-answers and --before-p-plans must be supplied together")

    n_answers = args.n_answers or args.run_root / "call3_n_26_greedy/answers.jsonl"
    n_plans = args.n_plans or args.run_root / "answer_plan_v3_case_truths/answer_plans.jsonl"
    p_answers = args.p_answers or args.run_root / "call3_p_26_greedy/answers.jsonl"
    p_plans = args.p_plans or args.run_root / "answer_plan_p1_cards/answer_plans.jsonl"

    conditions = {
        "N": {
            "answers": n_answers,
            "plans": n_plans,
            "answer_field": "answer",
            "description": "authored authority only; no card retrieval",
            "generation": {"model": "idpr-gemma-4-26b-a4b", "temperature": 0.0, "max_tokens": 8192, "samples": 1},
        },
        "P": {
            "answers": p_answers,
            "plans": p_plans,
            "answer_field": "answer",
            "description": "authored authority + ANSWERPLAN_SPEC 5.5 card retrieval",
            "generation": {"model": "idpr-gemma-4-26b-a4b", "temperature": 0.0, "max_tokens": 8192, "samples": 1},
        },
        "baseline_vanilla_zero_shot": {
            "answers": args.baseline,
            "plans": None,
            "answer_field": "generated_response",
            "description": "vanilla zero-shot LLM, no symbolic layer",
            "generation": {"model": "idpr-gemma-4-26b-a4b", "temperature": 0.0, "max_tokens": 8192, "samples": 1},
        },
    }
    if args.before_n_answers is not None:
        conditions["before_N"] = {
            "answers": args.before_n_answers,
            "plans": args.before_n_plans,
            "answer_field": "answer",
            "description": "frozen pre-improvement authored-authority N condition",
            "generation": {
                "model": "idpr-gemma-4-26b-a4b",
                "temperature": 0.0,
                "max_tokens": 8192,
                "samples": 1,
            },
        }
    if args.before_p_answers is not None:
        conditions["before_P"] = {
            "answers": args.before_p_answers,
            "plans": args.before_p_plans,
            "answer_field": "answer",
            "description": "frozen pre-improvement authored-authority plus card condition",
            "generation": {
                "model": "idpr-gemma-4-26b-a4b",
                "temperature": 0.0,
                "max_tokens": 8192,
                "samples": 1,
            },
        }
    method_id_by_condition = {
        "N": args.n_method_id,
        "P": args.p_method_id,
        "baseline_vanilla_zero_shot": args.baseline_method_id,
        "before_N": args.before_n_method_id,
        "before_P": args.before_p_method_id,
    }
    active_method_ids = [method_id_by_condition[name] for name in conditions]
    if len(active_method_ids) != len(set(active_method_ids)):
        parser.error("judge method ids must be distinct")

    case_ids = [row["sub_question_id"] for row in rows(conditions["N"]["answers"])]
    if len(set(case_ids)) != len(case_ids):
        raise ValueError("duplicate case ids in the N run")

    args.out.mkdir(parents=True, exist_ok=True)
    manifest: dict[str, Any] = {
        "cases": len(case_ids),
        "case_ids": case_ids,
        "conditions": {},
        "notes": [],
    }

    with (args.out / "answers.jsonl").open("w", encoding="utf-8") as handle:
        for name, spec in conditions.items():
            by_id = {str(row["sub_question_id"]): row for row in rows(spec["answers"])}
            missing = [case_id for case_id in case_ids if case_id not in by_id]
            if missing:
                raise ValueError(f"{name} does not cover {len(missing)} of the 26 cases: {missing[:3]}")
            chars = 0
            for case_id in case_ids:
                answer = str(by_id[case_id][spec["answer_field"]])
                chars += len(answer)
                handle.write(
                    json.dumps(
                        {"sub_question_id": case_id, "condition": name, "answer": answer},
                        ensure_ascii=False,
                    )
                    + "\n"
                )
            entry: dict[str, Any] = {
                "description": spec["description"],
                "source": manifest_path(spec["answers"]),
                "source_sha256_16": sha16(spec["answers"]),
                "generation": spec["generation"],
                "answer_chars_total": chars,
                "answer_chars_mean": round(chars / len(case_ids), 1),
                "cases_in_source": len(by_id),
            }
            if spec["plans"] is not None:
                entry["answer_plans"] = manifest_path(spec["plans"])
                entry["answer_plans_sha256_16"] = sha16(spec["plans"])
                run_dir = spec["answers"].parent
                entry["audits"] = {
                    "conclusion_completeness": audit(run_dir / "conclusion_completeness.json"),
                    "answer_hygiene": audit(run_dir / "answer_hygiene.json"),
                    "conclusion_state": audit(run_dir / "conclusion_state.json"),
                }
            manifest["conditions"][name] = entry

    # The judge reads `generated_response`; the Call 3 runs write `answer`.  One
    # judge-ready file per arm keeps that rename out of the judge and out of the runs.
    judge_dir = args.out.resolve() / "judge_inputs"
    judge_dir.mkdir(parents=True, exist_ok=True)
    for name, spec in conditions.items():
        by_id = {str(row["sub_question_id"]): row for row in rows(spec["answers"])}
        path = judge_dir / f"{name}_outputs.jsonl"
        with path.open("w", encoding="utf-8") as handle:
            for case_id in case_ids:
                handle.write(
                    json.dumps(
                        {
                            "sub_question_id": case_id,
                            "baseline_id": name,
                            "generated_response": str(by_id[case_id][spec["answer_field"]]),
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                )
        manifest["conditions"][name]["judge_input"] = manifest_path(path)

    # Keep the judge wiring next to the bundle.  Mutating the repository-global
    # methods manifest would make the frozen before artifact point at a new run.
    methods = {
        method_id_by_condition[name]: manifest_path(judge_dir / f"{name}_outputs.jsonl")
        for name in conditions
    }
    methods_path = args.out / "methods.json"
    methods_path.write_text(
        json.dumps({"version": "1.0.0", "methods": methods}, ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    manifest["judge_methods_manifest"] = manifest_path(methods_path)
    manifest["judge_method_ids"] = methods

    manifest["notes"] = [
        "All bundled conditions were generated by the same served model, so the comparison "
        "is not confounded by the backbone.",
        "All bundled generated arms decode greedily at temperature 0.0 / 8192 tokens on "
        "the same service, so the comparison carries no sampling variance: the same inputs "
        "reproduce the same answers.  Frozen before arms are retained as historical outputs "
        "and are identified as such in their condition descriptions.",
        "Baseline rows carry a rubric_summary field; it is stored metadata and is absent "
        "from the baseline's formatted_input_schema, so no rubric text reached the model.",
        "The baseline artifact covers 61 questions; only the 26 substantive-law subset is "
        "bundled, matching the judge subset decided on 2026-08-13.",
    ]
    (args.out / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({**manifest, "case_ids": f"[{len(case_ids)} ids]"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
