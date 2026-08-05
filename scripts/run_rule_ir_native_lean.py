#!/usr/bin/env python3
"""Run the lean closed-unit -> committed Scallop -> section prose pipeline."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Mapping, Protocol, Sequence


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


_VERDICT_TEXT = {
    "established": "성립 (구성요건 충족)",
    "not_established": "불성립 (구성요건 미충족)",
    "undetermined": "미확정 (판단에 필요한 사실이 부족)",
    "conflict": "충돌 (상반된 요건이 동시에 인정)",
    "no_derived_outcome": "미확정 (도출된 결론 없음)",
}
_EVIDENCE_LIMIT = 12


def _render_verdict_brief(
    *,
    directives: Sequence[Mapping[str, Any]],
    skipped: Sequence[Mapping[str, Any]],
    unsupported: Sequence[Mapping[str, Any]],
    labels: Mapping[str, str],
) -> str:
    """Render symbolic results as a Korean brief.

    The writer used to receive the raw contract JSON, which both buried the
    reason behind a verdict under 88 predicate entries and leaked internal
    vocabulary (``Scallop``, relation names) into the finished prose.
    """

    blocks: list[str] = []
    for directive in directives:
        issue_id = str(directive["issue_id"])
        label = labels.get(issue_id) or str(directive["unit_id"])
        conclusion = str(directive["symbolic_conclusion"])
        lines = [
            f"### 죄명: {label}",
            f"- **확정 결론: {_VERDICT_TEXT.get(conclusion, conclusion)}** "
            "(이 결론은 검증된 규칙 추론의 산물이므로 반드시 그대로 따른다)",
        ]
        referred = [str(name) for name in directive.get("referred_crimes", []) if name]
        if referred:
            lines.append(
                "- **이 죄가 아니라 다음 죄로 평가된다: "
                + ", ".join(referred)
                + "** — 이 죄의 불성립으로 끝내지 말고, 넘어간 죄의 성부를 반드시 "
                "이어서 논증하고 결론까지 내려라."
            )
        # ``unmet_requirements`` stays in the report as survey data for the card
        # gaps it exposes, but it is deliberately kept out of the brief: two
        # variants of showing it to the writer both scored below the baseline
        # (7.0 -> 6.5 -> 6.0 on the 27-item rubric).
        waived = [str(name) for name in directive.get("waived_requirements", []) if name]
        if waived:
            lines.append(
                "- 이 죄의 성립에 요구되지 않는 것으로 확인된 요건(불성립 사유가 아니다): "
                + ", ".join(waived)
            )
        annotations = directive.get("annotations", {}) or {}
        standards = [str(name) for name in annotations.get("assessment_standard", []) if name]
        if standards:
            # The standard tells the reader how the element is measured.  It must
            # not become a licence to re-decide the element: the verdict above
            # already owns that, and a model that concludes from a definition has
            # taken the decision back from the symbolic layer.
            lines.append(
                "- 다음 요건에는 판단기준 카드가 적용된다(기준일 뿐 충족 여부의 결론이 아니다. "
                "기준을 설명하는 데만 쓰고, 이를 근거로 위 확정 결론과 다른 판단을 하지 마라): "
                + ", ".join(standards)
            )
        proofs = [str(name) for name in annotations.get("proof_standard", []) if name]
        if proofs:
            lines.append(
                "- 유죄 인정을 위해 증명이 요구되는 사항(구성요건 자체가 아니다): "
                + ", ".join(proofs)
            )
        subtypes = [str(name) for name in annotations.get("subtype_outcome", []) if name]
        if subtypes:
            lines.append(
                "- 같은 죄 안에서 적용되는 유형: " + ", ".join(subtypes)
                + " (죄 전체의 성립은 위 확정 결론 그대로다)"
            )
        post = [str(name) for name in annotations.get("post_outcome", []) if name]
        details = [
            f"{item.get('key')}={item.get('value')}"
            for item in directive.get("outcome_details", []) or []
            if item.get("key")
        ]
        if post or details:
            lines.append(
                "- 구성요건 판단 뒤에 오는 죄수·처벌 효과"
                + (f" [{', '.join(post)}]" if post else "")
                + (f": {', '.join(details)}" if details else "")
                + " — 불가벌적 사후행위는 구성요건 불성립이 아니라 별도 처벌만 배제되는 것이므로 "
                "그렇게 구분해 서술하라."
            )
        evidence = directive.get("evidence", {}) or {}
        met = [
            str(item.get("definition", ""))
            for item in evidence.values()
            if item.get("status") == "satisfied"
        ]
        denied = [
            str(item.get("definition", ""))
            for item in evidence.values()
            if item.get("status") == "not_satisfied"
        ]
        undetermined = [
            str(item.get("definition", ""))
            for item in evidence.values()
            if item.get("status") == "unknown"
        ]
        if met:
            lines.append("- 사실관계상 인정된 요건:")
            lines += [f"  - {text}" for text in met[:_EVIDENCE_LIMIT]]
        if denied:
            lines.append("- 적극적으로 부정된 요건:")
            lines += [f"  - {text}" for text in denied[:_EVIDENCE_LIMIT]]
        if undetermined and conclusion != "established":
            lines.append("- 사실관계만으로 확인되지 않은 요건:")
            lines += [f"  - {text}" for text in undetermined[:_EVIDENCE_LIMIT]]
        blocks.append("\n".join(lines))

    autonomous: list[str] = []
    for item in unsupported:
        label = (
            labels.get(str(item.get("issue_id", "")))
            or str(item.get("reported_label", ""))
        )
        if label:
            autonomous.append(label)
    for item in skipped:
        label = labels.get(str(item.get("issue_id", ""))) or str(item.get("unit_id", ""))
        if label:
            autonomous.append(label)
    if autonomous:
        blocks.append(
            "### 규칙 추론이 판정하지 않은 쟁점 (전적으로 자율 판단)\n"
            + "\n".join(f"- {label}" for label in dict.fromkeys(autonomous))
            + "\n이 쟁점들에는 확정 결론이 없다. 법학 지식으로 직접 학설·판례를 "
            "동원하여 충실히 논증하고 결론을 내려라."
        )
    return "\n\n".join(blocks) if blocks else "(확정된 판정 없음)"


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
    rejected = validate_closed_issue_selection(
        selection,
        case_id=case_id,
        case_text=case_text,
    )
    # A rejected issue cannot be run symbolically — its roles or its quote do not
    # hold up — but it is still a real issue in the case.  Drop it from the
    # symbolic run and hand it to the writer as an autonomous one, rather than
    # discarding the whole case along with the issues that were well formed.
    if rejected:
        rejected_ids = {item["issue_id"] for item in rejected}
        selection = {
            **selection,
            "issues": [
                # A dependency on a dropped issue would dangle, so it goes too.
                {**issue, "depends_on_issue_ids": [
                    dependency
                    for dependency in issue.get("depends_on_issue_ids", [])
                    if dependency not in rejected_ids
                ]}
                for issue in selection.get("issues", [])
                if str(issue.get("issue_id", "")) not in rejected_ids
            ],
        }
        _write_json(out_dir / "01_rejected_issues.json", {"rejected": rejected})
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
    # --- Stage 3: Unified IRAC answer (single LLM call, no host assembly) ---
    contract = native_report.get("generation_contract", {})
    labels = {
        str(issue["issue_id"]): str(issue.get("reported_label", ""))
        for issue in selection.get("issues", [])
    }
    verdict_brief = _render_verdict_brief(
        directives=contract.get("conclusion_directives", []),
        skipped=contract.get("skipped_directives", []),
        # An issue dropped for a malformed selection is still a live issue in
        # the case; it reaches the writer alongside the ones with no RuleIR.
        unsupported=[*unsupported, *rejected],
        labels=labels,
    )

    write_system, write_user = PROMPTS["section_write"]
    user_template = load_prompt(write_user)
    user_prompt = (
        user_template
        .replace("{{CASE_TEXT}}", case_text)
        .replace("{{QUESTION_PROMPT}}", str(case.get("question_prompt", "")))
        .replace("{{SYMBOLIC_DIRECTIVES}}", verdict_brief)
    )
    _write_text(out_dir / "04_write_prompt.md", user_prompt + "\n")
    answer_markdown = client.complete_text(
        system_prompt=load_prompt(write_system),
        user_template=user_prompt,
        payload={},
        max_tokens=8000,
        temperature=0.0,
    ).strip()
    writing_metadata = {"characters": len(answer_markdown), "mode": "unified_irac"}
    _write_text(out_dir / "05_answer.md", answer_markdown + "\n")

    manifest = {
        "version": "1.0.0",
        "case_id": case_id,
        "pipeline": "lean_rule_ir_native",
        "git_commit": _git_commit(),
        "neural_stages": [
            "closed_issue_selection",
            "full_predicate_assessment",
            "unified_irac_answer",
        ],
        "semantic_search_used": False,
        "fact_graph_used": False,
        "core_projection_used": False,
        "symbolic_runtime": "committed_rule_ir_scallop_only",
        "model_calls": {
            "issue_selection": 1,
            "predicate_assessment": len(supported),
            "section_writing": 1,
            "total": 2 + len(supported),
        },
        "prompt_hashes": _prompt_hashes(),
        "selection_metadata": selection_metadata,
        "assessment_metadata": assessment_metadata,
        "writing_metadata": writing_metadata,
        "supported_issue_count": len(supported),
        "unsupported_issue_count": len(unsupported),
        "rejected_issue_count": len(rejected),
        "completed": True,
    }
    _write_json(out_dir / "run_manifest.json", manifest)
    return {
        "selection": selection,
        "resolved_requests": resolved,
        "native_report": native_report,
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
