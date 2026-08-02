"""Render one issue-first Call-2/Scallop artifact as a long-form legal answer."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from idpr.candidates import candidate_issues
from idpr.eval.issue_recall import INVENTORY_PATH, PROJECT_ROOT
from idpr.generation.issue_answer import (
    attach_issue_answer_provenance,
    build_call3_request,
    issue_answer_model_schema,
    render_issue_answer_markdown,
    validate_issue_answer,
)
from idpr.issue_pipeline import build_issue_reasoning_packet, run_issue_symbolic
from idpr.neural.vllm_client import VLLMClient
from idpr.prompts import load_prompt
from idpr.rulebase.cards import card_corpus


DEFAULT_CASE_ID = "kcl_criminal_r10_p1_q1_ga"
DEFAULT_CALL2 = PROJECT_ROOT / "data/eval/issue_status_smoke.json"
DEFAULT_FACT_GRAPHS = PROJECT_ROOT / "data/eval/fact_graphs.jsonl"
DEFAULT_OUT = PROJECT_ROOT / "data/eval/issue_answer_smoke.json"


def _jsonl_by_id(path: Path) -> dict[str, dict[str, Any]]:
    return {
        row["sub_question_id"]: row
        for row in (
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    }


def prepare_request(args: argparse.Namespace) -> dict[str, Any]:
    report = json.loads(args.call2.read_text(encoding="utf-8"))
    case_id = str(report.get("case_id", args.case_id))
    if case_id != args.case_id:
        raise ValueError("Call-2 artifact case_id differs from --case-id")
    inventory = _jsonl_by_id(args.inventory)
    graph_rows = _jsonl_by_id(args.fact_graphs)
    case = inventory[case_id]
    fact_graph = graph_rows[case_id]["fact_graph"]
    reasoning_packet = report.get("reasoning_packet")
    if not isinstance(reasoning_packet, dict):
        assessment = report.get("issue_status")
        if not isinstance(assessment, dict):
            raise ValueError("Call-2 artifact has neither reasoning_packet nor issue_status")
        articles = tuple(report.get("articles", ()))
        scope = candidate_issues(
            selected=articles,
            attempt_map={},
            corpus=card_corpus(),
        )
        symbolic = report.get("symbolic_runtime")
        if not isinstance(symbolic, dict) or not isinstance(symbolic.get("relations"), dict):
            symbolic = run_issue_symbolic(
                case_id=case_id,
                fact_graph=fact_graph,
                assessment_bundle=assessment,
                work_dir=args.work_dir / "symbolic_replay",
                name=f"{case_id}_call3_replay",
            )
        reasoning_packet = build_issue_reasoning_packet(
            scope=scope,
            assessment_bundle=assessment,
            symbolic_runtime=symbolic,
        )
    return build_call3_request(
        case=case,
        fact_graph=fact_graph,
        reasoning_packet=reasoning_packet,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url")
    parser.add_argument("--model")
    parser.add_argument("--api-key", default="local-idpr")
    parser.add_argument("--case-id", default=DEFAULT_CASE_ID)
    parser.add_argument("--call2", type=Path, default=DEFAULT_CALL2)
    parser.add_argument("--inventory", type=Path, default=INVENTORY_PATH)
    parser.add_argument("--fact-graphs", type=Path, default=DEFAULT_FACT_GRAPHS)
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT)
    parser.add_argument(
        "--work-dir", type=Path, default=PROJECT_ROOT / ".cache/call3_issue_smoke"
    )
    parser.add_argument("--max-tokens", type=int, default=8192)
    parser.add_argument("--timeout-seconds", type=float, default=7200.0)
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    request = prepare_request(args)
    args.work_dir.mkdir(parents=True, exist_ok=True)
    request_path = args.work_dir / f"{args.case_id}_request.json"
    request_path.write_text(
        json.dumps(request, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if args.dry_run:
        print(
            json.dumps(
                {
                    "case_id": args.case_id,
                    "sections": len(request["required_sections"]),
                    "issues": sum(
                        len(section["issues"])
                        for section in request["required_sections"]
                    ),
                    "payload_chars": len(json.dumps(request, ensure_ascii=False)),
                    "request_path": str(request_path),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return
    if not args.base_url or not args.model:
        parser.error("--base-url and --model are required unless --dry-run is used")

    client = VLLMClient(
        base_url=args.base_url,
        model=args.model,
        api_key=args.api_key,
        timeout_seconds=args.timeout_seconds,
    )
    answer, metadata = client.complete_json(
        system_prompt=load_prompt("issue_long_form_generate"),
        user_template=load_prompt("issue_long_form_generate_user"),
        payload=request,
        schema_name="issue_long_form_answer",
        schema=issue_answer_model_schema(request),
        max_tokens=args.max_tokens,
        temperature=args.temperature,
    )
    answer = attach_issue_answer_provenance(answer, request=request)
    validate_issue_answer(answer, request=request)
    result = {
        "case_id": args.case_id,
        "model": args.model,
        "metadata": metadata,
        "request": request,
        "answer": answer,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    args.out.with_suffix(".md").write_text(
        render_issue_answer_markdown(answer), encoding="utf-8"
    )
    print(f"usage={metadata.get('usage', {})}")
    print(f"wrote {args.out} / {args.out.with_suffix('.md')}")


if __name__ == "__main__":
    main()
