"""Run the issue-first NSN pipeline over a persisted candidate inventory.

The runner is resumable at the case boundary.  Every case keeps its assessment,
symbolic trace, structured answer, and rendered markdown in a separate directory;
the baseline-compatible JSONL is rebuilt only from validated completed artifacts.
"""

from __future__ import annotations

import argparse
import json
import statistics as st
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from idpr.eval.issue_recall import INVENTORY_PATH, PROJECT_ROOT
from idpr.generation.issue_answer import validate_issue_answer
from idpr.issue_pipeline import scope_from_l0_row


DEFAULT_FACT_GRAPHS = PROJECT_ROOT / "data/eval/fact_graphs.jsonl"
DEFAULT_CANDIDATES = PROJECT_ROOT / "data/eval/l0_candidates.jsonl"
DEFAULT_RUN_DIR = PROJECT_ROOT / "experiments/results/idpr_nsn"
DEFAULT_OUTPUT = PROJECT_ROOT / "experiments/results/idpr_nsn_outputs.jsonl"
METHOD_ID = "idpr_nsn"


def _rows(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()
    ]


def _index_unique(rows: Iterable[Mapping[str, Any]], *, source: str) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for row in rows:
        case_id = str(row.get("sub_question_id", ""))
        if not case_id:
            raise ValueError(f"{source} contains a row without sub_question_id")
        if case_id in indexed:
            raise ValueError(f"{source} contains duplicate case {case_id}")
        indexed[case_id] = dict(row)
    return indexed


def _selected_case_ids(
    inventory: Sequence[Mapping[str, Any]],
    *,
    requested: Sequence[str],
    limit: int | None,
) -> list[str]:
    ordered = [str(row["sub_question_id"]) for row in inventory]
    if requested:
        unknown = sorted(set(requested) - set(ordered))
        if unknown:
            raise ValueError(f"unknown --case-id values: {unknown}")
        wanted = set(requested)
        ordered = [case_id for case_id in ordered if case_id in wanted]
    return ordered[:limit] if limit is not None else ordered


def case_commands(
    *,
    python: str,
    base_url: str,
    model: str,
    api_key: str,
    case_id: str,
    inventory: Path,
    fact_graphs: Path,
    candidates: Path,
    case_dir: Path,
    call2_max_tokens: int,
    call3_max_tokens: int,
    timeout_seconds: float,
    no_cache: bool,
) -> tuple[list[str], list[str]]:
    assessment_path = case_dir / "issue_assessment.json"
    answer_path = case_dir / "answer.json"
    common = ["--base-url", base_url, "--model", model, "--api-key", api_key]
    assessment = [
        python,
        "scripts/run_issue_assessment.py",
        *common,
        "--case-id",
        case_id,
        "--inventory",
        str(inventory),
        "--fact-graphs",
        str(fact_graphs),
        "--candidates",
        str(candidates),
        "--out",
        str(assessment_path),
        "--work-dir",
        str(case_dir / "runtime"),
        "--max-tokens",
        str(call2_max_tokens),
        "--timeout-seconds",
        str(timeout_seconds),
    ]
    if no_cache:
        assessment.append("--no-cache")
    answer = [
        python,
        "scripts/run_issue_answer.py",
        *common,
        "--call2",
        str(assessment_path),
        "--inventory",
        str(inventory),
        "--fact-graphs",
        str(fact_graphs),
        "--out",
        str(answer_path),
        "--work-dir",
        str(case_dir / "runtime/answer"),
        "--max-tokens",
        str(call3_max_tokens),
        "--timeout-seconds",
        str(timeout_seconds),
    ]
    return assessment, answer


def _valid_assessment(path: Path, *, case_id: str) -> bool:
    try:
        artifact = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return (
        artifact.get("case_id") == case_id
        and isinstance(artifact.get("issue_status"), Mapping)
        and isinstance(artifact.get("reasoning_packet"), Mapping)
    )


def _load_valid_answer(path: Path, *, case_id: str) -> dict[str, Any] | None:
    try:
        artifact = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if artifact.get("case_id") != case_id:
        return None
    request = artifact.get("request")
    answer = artifact.get("answer")
    if not isinstance(request, Mapping) or not isinstance(answer, Mapping):
        return None
    markdown_path = path.with_suffix(".md")
    if not markdown_path.is_file() or not markdown_path.read_text(encoding="utf-8").strip():
        return None
    validate_issue_answer(answer, request=request)
    return artifact


def _baseline_row(
    *,
    case: Mapping[str, Any],
    case_dir: Path,
    assessment: Mapping[str, Any],
    answer_artifact: Mapping[str, Any],
) -> dict[str, Any]:
    answer_path = case_dir / "answer.md"
    return {
        "sub_question_id": case["sub_question_id"],
        "baseline_id": METHOD_ID,
        "name": "IDPR Neural-Symbolic-Neural",
        "question_prompt": case.get("question_prompt", ""),
        "generated_response": answer_path.read_text(encoding="utf-8"),
        "usage": {
            "issue_assessment": assessment.get("usage", {}),
            "answer_generation": answer_artifact.get("metadata", {}).get("usage", {}),
        },
        "artifacts": {
            "issue_assessment": str(case_dir / "issue_assessment.json"),
            "answer": str(case_dir / "answer.json"),
            "answer_markdown": str(answer_path),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url")
    parser.add_argument("--model")
    parser.add_argument("--api-key", default="local-idpr")
    parser.add_argument("--inventory", type=Path, default=INVENTORY_PATH)
    parser.add_argument("--fact-graphs", type=Path, default=DEFAULT_FACT_GRAPHS)
    parser.add_argument("--candidates", type=Path, default=DEFAULT_CANDIDATES)
    parser.add_argument("--run-dir", type=Path, default=DEFAULT_RUN_DIR)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--case-id", action="append", default=[])
    parser.add_argument("--limit", type=int)
    parser.add_argument("--call2-max-tokens", type=int, default=12288)
    parser.add_argument("--call3-max-tokens", type=int, default=16384)
    parser.add_argument("--timeout-seconds", type=float, default=7200.0)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--no-cache", action="store_true")
    parser.add_argument(
        "--plan-only",
        action="store_true",
        help="validate all stage boundaries and report scope sizes without model calls",
    )
    args = parser.parse_args()
    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be positive")
    if args.call2_max_tokens < 1 or args.call3_max_tokens < 1:
        parser.error("generation token limits must be positive")
    if not args.plan_only and (not args.base_url or not args.model):
        parser.error("--base-url and --model are required unless --plan-only is used")

    inventory_rows = _rows(args.inventory)
    inventory = _index_unique(inventory_rows, source=str(args.inventory))
    candidates = _index_unique(_rows(args.candidates), source=str(args.candidates))
    graph_ids = set(_index_unique(_rows(args.fact_graphs), source=str(args.fact_graphs)))
    case_ids = _selected_case_ids(inventory_rows, requested=args.case_id, limit=args.limit)
    for source, ids in (("candidate", set(candidates)), ("fact graph", graph_ids)):
        missing = sorted(set(case_ids) - ids)
        if missing:
            raise ValueError(f"{source} artifact is missing cases: {missing}")

    if args.plan_only:
        scopes = {case_id: scope_from_l0_row(candidates[case_id]) for case_id in case_ids}
        issue_counts = [len(scope.initial_issues) for scope in scopes.values()]
        anchor_counts = [
            sum(
                len(issue.anchor_card_ids) + len(issue.reviewed_anchor_rules)
                for issue in scope.initial_issues
            )
            for scope in scopes.values()
        ]
        article_counts = [len(scope.articles) for scope in scopes.values()]
        print(
            json.dumps(
                {
                    "cases": len(scopes),
                    "articles": {
                        "median": st.median(article_counts),
                        "max": max(article_counts),
                    },
                    "initial_issues": {
                        "median": st.median(issue_counts),
                        "max": max(issue_counts),
                    },
                    "anchor_rules": {
                        "median": st.median(anchor_counts),
                        "max": max(anchor_counts),
                    },
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return

    args.run_dir.mkdir(parents=True, exist_ok=True)
    completed: list[dict[str, Any]] = []
    for index, case_id in enumerate(case_ids, start=1):
        case_dir = args.run_dir / case_id
        case_dir.mkdir(parents=True, exist_ok=True)
        assessment_path = case_dir / "issue_assessment.json"
        answer_path = case_dir / "answer.json"
        assessment_cmd, answer_cmd = case_commands(
            python=sys.executable,
            base_url=str(args.base_url),
            model=str(args.model),
            api_key=args.api_key,
            case_id=case_id,
            inventory=args.inventory,
            fact_graphs=args.fact_graphs,
            candidates=args.candidates,
            case_dir=case_dir,
            call2_max_tokens=args.call2_max_tokens,
            call3_max_tokens=args.call3_max_tokens,
            timeout_seconds=args.timeout_seconds,
            no_cache=args.no_cache,
        )
        print(f"[{index}/{len(case_ids)}] {case_id}", flush=True)
        if args.overwrite or not _valid_assessment(assessment_path, case_id=case_id):
            subprocess.run(assessment_cmd, cwd=PROJECT_ROOT, check=True)
        artifact = None if args.overwrite else _load_valid_answer(answer_path, case_id=case_id)
        if artifact is None:
            subprocess.run(answer_cmd, cwd=PROJECT_ROOT, check=True)
            artifact = _load_valid_answer(answer_path, case_id=case_id)
        if artifact is None:
            raise RuntimeError(f"{case_id}: answer artifact failed validation")
        assessment = json.loads(assessment_path.read_text(encoding="utf-8"))
        completed.append(
            _baseline_row(
                case=inventory[case_id],
                case_dir=case_dir,
                assessment=assessment,
                answer_artifact=artifact,
            )
        )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    temporary = args.out.with_suffix(args.out.suffix + ".tmp")
    temporary.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in completed),
        encoding="utf-8",
    )
    temporary.replace(args.out)
    print(f"wrote {len(completed)} answers to {args.out}")


if __name__ == "__main__":
    main()
