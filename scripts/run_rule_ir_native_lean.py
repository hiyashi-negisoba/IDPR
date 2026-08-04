#!/usr/bin/env python3
"""Run the lean closed-unit -> committed Scallop -> section prose pipeline."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Mapping, Protocol


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from idpr.eval.input_formatter import (  # noqa: E402
    ALLOWED_INPUT_FIELDS,
    assert_no_leaked_fields,
    scoped_question_text,
)
from idpr.generation.native_rule_ir_answer import (  # noqa: E402
    build_native_section_requests,
    finalize_native_answer,
    render_native_answer,
    validate_native_section_prose,
)
from idpr.neural.vllm_client import VLLMClient  # noqa: E402
from idpr.prompts import load_prompt, prompt_path  # noqa: E402
from idpr.rulegen.native_host import (  # noqa: E402
    DEFAULT_SCLI,
    closed_issue_selection_schema,
    closed_unit_catalog,
    execute_native_case,
    predicate_assessment_schema,
    selected_predicate_requests,
    validate_closed_issue_selection,
    validate_predicate_assessment,
)
from idpr.rulegen.registry import build_registry  # noqa: E402
from scripts.audit_rule_ir_native_prompts import audit as audit_prompts  # noqa: E402


PROMPTS = {
    "issue_select": (
        "rule_ir_native_issue_select",
        "rule_ir_native_issue_select_user",
    ),
    "predicate_assess": (
        "rule_ir_native_predicate_assess",
        "rule_ir_native_predicate_assess_user",
    ),
    "section_write": ("rule_ir_native_write", "rule_ir_native_write_user"),
}


class NativeModelClient(Protocol):
    def complete_json(self, **kwargs: Any) -> tuple[dict[str, Any], dict[str, Any]]: ...

    def complete_text(self, **kwargs: Any) -> str: ...


def _read_jsonl_index(path: Path) -> dict[str, dict[str, Any]]:
    return {
        str(row["sub_question_id"]): row
        for row in (
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    }


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _prompt_hashes() -> dict[str, str]:
    return {
        name: hashlib.sha256(prompt_path(name).read_bytes()).hexdigest()
        for pair in PROMPTS.values()
        for name in pair
    }


def _git_commit() -> str | None:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.strip() or None


def _model_case(raw_case: Mapping[str, Any]) -> dict[str, str]:
    payload = {
        key: raw_case[key]
        for key in ALLOWED_INPUT_FIELDS
        if key in raw_case
    }
    assert_no_leaked_fields(payload)
    case_id = str(payload.get("sub_question_id", ""))
    question_text = str(payload.get("question_text", ""))
    question_prompt = str(payload.get("question_prompt", ""))
    return {
        "sub_question_id": case_id,
        "question_text": scoped_question_text(question_text, question_prompt),
        "question_prompt": question_prompt,
    }


def run_case(
    *,
    client: NativeModelClient,
    raw_case: Mapping[str, Any],
    out_dir: Path,
    scli_path: Path = DEFAULT_SCLI,
) -> dict[str, Any]:
    """Execute one case with no fallback, hidden retry, retrieval, or FactGraph."""

    prompt_audit = audit_prompts()
    if prompt_audit["status"] != "pass":
        raise ValueError(f"native prompt audit failed: {prompt_audit['errors']}")
    case = _model_case(raw_case)
    case_id = case["sub_question_id"]
    case_text = case["question_text"]
    out_dir.mkdir(parents=True, exist_ok=True)

    selection_input = {
        "case_id": case_id,
        "case_text": case_text,
        "question_prompt": case["question_prompt"],
        "allowed_units": closed_unit_catalog(),
    }
    selection_system, selection_user = PROMPTS["issue_select"]
    selection, selection_metadata = client.complete_json(
        system_prompt=load_prompt(selection_system),
        user_template=load_prompt(selection_user),
        payload=selection_input,
        schema_name="rule_ir_native_issue_selection",
        schema=closed_issue_selection_schema(case_id=case_id),
        max_tokens=4096,
        temperature=0.0,
    )
    validate_closed_issue_selection(
        selection,
        case_id=case_id,
        case_text=case_text,
    )
    _write_json(out_dir / "01_issue_selection.json", selection)

    registry = build_registry()
    resolved = selected_predicate_requests(case=case, selection=selection)
    supported = [
        request
        for request in resolved["requests"]
        if request.get("status") != "predicate_ir_missing"
    ]
    unsupported = [
        request
        for request in resolved["requests"]
        if request.get("status") == "predicate_ir_missing"
    ]
    unit_runs = []
    assessment_metadata: dict[str, Any] = {}
    assessment_system, assessment_user = PROMPTS["predicate_assess"]
    for index, request in enumerate(supported, 1):
        issue_id = str(request["issue_id"])
        unit_id = str(request["unit_id"])
        assessment, metadata = client.complete_json(
            system_prompt=load_prompt(assessment_system),
            user_template=load_prompt(assessment_user),
            payload=request["assessment_request"],
            schema_name="rule_ir_native_predicate_assessment",
            schema=predicate_assessment_schema(
                case_id=case_id,
                issue_id=issue_id,
                entry=registry[unit_id],
            ),
            max_tokens=16_384,
            temperature=0.0,
        )
        validate_predicate_assessment(
            assessment,
            case_id=case_id,
            issue_id=issue_id,
            unit_id=unit_id,
            case_text=case_text,
        )
        _write_json(
            out_dir / f"02_assessment_{index:02d}_{issue_id}.json", assessment
        )
        assessment_metadata[issue_id] = metadata
        unit_runs.append(
            {
                "issue_id": issue_id,
                "unit_id": unit_id,
                "depends_on_issue_ids": request["depends_on_issue_ids"],
                "assessment_payload": assessment,
            }
        )

    native_report = execute_native_case(
        case_id=case_id,
        case_text=case_text,
        unit_runs=unit_runs,
        scli_path=scli_path,
        work_dir=out_dir / "runtime",
    )
    _write_json(out_dir / "03_native_report.json", native_report)

    section_requests = build_native_section_requests(
        case=case,
        selection=selection,
        native_report=native_report,
    )
    prose_by_issue: dict[str, str] = {}
    writing_metadata: dict[str, Any] = {}
    write_system, write_user = PROMPTS["section_write"]
    for index, request in enumerate(section_requests, 1):
        issue_id = str(request["issue_id"])
        prose = client.complete_text(
            system_prompt=load_prompt(write_system),
            user_template=load_prompt(write_user),
            payload=request,
            max_tokens=2500,
            temperature=0.0,
        ).strip()
        validate_native_section_prose(prose)
        prose_by_issue[issue_id] = prose
        writing_metadata[issue_id] = {"characters": len(prose)}
        _write_text(out_dir / f"04_section_{index:02d}_{issue_id}.md", prose + "\n")

    answer = finalize_native_answer(
        section_requests=section_requests,
        prose_by_issue=prose_by_issue,
        unsupported_issues=unsupported,
    )
    answer_markdown = render_native_answer(answer)
    _write_json(out_dir / "05_answer.json", answer)
    _write_text(out_dir / "05_answer.md", answer_markdown)

    manifest = {
        "version": "1.0.0",
        "case_id": case_id,
        "pipeline": "lean_rule_ir_native",
        "git_commit": _git_commit(),
        "neural_stages": [
            "closed_issue_selection",
            "full_predicate_assessment",
            "one_section_plain_markdown",
        ],
        "semantic_search_used": False,
        "fact_graph_used": False,
        "core_projection_used": False,
        "symbolic_runtime": "committed_rule_ir_scallop_only",
        "model_calls": {
            "issue_selection": 1,
            "predicate_assessment": len(supported),
            "section_writing": len(section_requests),
            "total": 1 + len(supported) + len(section_requests),
        },
        "prompt_hashes": _prompt_hashes(),
        "selection_metadata": selection_metadata,
        "assessment_metadata": assessment_metadata,
        "writing_metadata": writing_metadata,
        "supported_issue_count": len(supported),
        "unsupported_issue_count": len(unsupported),
        "completed": True,
    }
    _write_json(out_dir / "run_manifest.json", manifest)
    return {
        "selection": selection,
        "resolved_requests": resolved,
        "native_report": native_report,
        "answer": answer,
        "answer_markdown": answer_markdown,
        "manifest": manifest,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--case-id", required=True)
    parser.add_argument(
        "--inventory",
        type=Path,
        default=ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=ROOT / "experiments/results/rule_ir_native_lean",
    )
    parser.add_argument("--scli", type=Path, default=DEFAULT_SCLI)
    args = parser.parse_args()

    inventory = _read_jsonl_index(args.inventory)
    if args.case_id not in inventory:
        raise KeyError(f"case id not found in inventory: {args.case_id}")
    client = VLLMClient(base_url=args.base_url, model=args.model)
    run_case(
        client=client,
        raw_case=inventory[args.case_id],
        out_dir=args.out_dir / args.case_id,
        scli_path=args.scli,
    )
    print(args.out_dir / args.case_id / "05_answer.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
