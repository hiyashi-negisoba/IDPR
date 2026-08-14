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
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    conditions = {
        "N": {
            "answers": args.run_root / "call3_n_26_greedy/answers.jsonl",
            "plans": args.run_root / "answer_plan_v3_case_truths/answer_plans.jsonl",
            "answer_field": "answer",
            "description": "authored authority only; no card retrieval",
            "generation": {"model": "idpr-gemma-4-26b-a4b", "temperature": 0.0, "max_tokens": 8192, "samples": 1},
        },
        "P": {
            "answers": args.run_root / "call3_p_26_greedy/answers.jsonl",
            "plans": args.run_root / "answer_plan_p1_cards/answer_plans.jsonl",
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
                "source": str(spec["answers"].relative_to(ROOT)),
                "source_sha256_16": sha16(spec["answers"]),
                "generation": spec["generation"],
                "answer_chars_total": chars,
                "answer_chars_mean": round(chars / len(case_ids), 1),
                "cases_in_source": len(by_id),
            }
            if spec["plans"] is not None:
                entry["answer_plans"] = str(spec["plans"].relative_to(ROOT))
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
        manifest["conditions"][name]["judge_input"] = str(path.relative_to(ROOT))

    manifest["notes"] = [
        "All three conditions were generated by the same served model, so the comparison "
        "is not confounded by the backbone.",
        "All three arms decode greedily at temperature 0.0 / 8192 tokens on the same "
        "service, so the comparison carries no sampling variance: the same inputs "
        "reproduce the same answers.  Every arm was re-run for this; the earlier "
        "temperature-0.7 answers are kept beside them and are not what the judge scores.",
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
