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
    NativeHostError,
    apply_routing_overrides,
    assess_routing_completeness,
    check_verdict_consistency,
    closed_issue_selection_schema,
    closed_unit_catalog,
    diagnose_unsupported_issues,
    execute_native_case,
    predicate_assessment_schema,
    selected_predicate_requests,
    strip_verdict_manifest,
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
    # Compute nodes running this under sbatch often have no `git` on PATH at
    # all (not just a non-git-repo failure), which raises before returncode
    # is even set — provenance metadata missing is not worth losing an
    # otherwise-complete case run over.
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        return None
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


def _render_directive_block(
    directive: Mapping[str, Any], *, label: str, tier: str
) -> str:
    """Render one executed issue's Scallop result as a Korean brief block.

    ``tier`` is "verified" (established/not_established from a clean derivation —
    follow it absolutely) or "provisional" (undetermined/conflict/no_derived_outcome
    — a required element stayed unresolved, so this is a leaning, not a verdict).
    Collapsing both into one "반드시 그대로 따른다" instruction is what let a wrong
    ``not_established`` from a single mis-assessed predicate reach the answer with
    the same absolute force as a clean one (docs/handoff/CURRENT.md, r14 사기 사례).
    """

    issue_id = str(directive["issue_id"])
    conclusion = str(directive["symbolic_conclusion"])
    verdict_text = _VERDICT_TEXT.get(conclusion, conclusion)
    if tier == "verified":
        lines = [
            f"### 죄명: {label} [issue_id: {issue_id}]",
            f"- **확정 결론: {verdict_text}** "
            "(이 결론은 검증된 규칙 추론의 산물이므로 반드시 그대로 따른다)",
        ]
    else:
        lines = [
            f"### 죄명: {label} [issue_id: {issue_id}] (잠정 결론)",
            f"- **잠정 결론: {verdict_text}** (규칙 추론이 일부 요건을 확정하지 못해 "
            "나온 잠정적 결과다. 이 결론을 기본 방향으로 삼되, 사실관계상 다른 결론이 "
            "분명히 타당하다면 근거를 밝혀 대안을 논증하고 그 대안을 결론으로 삼아도 된다)",
        ]
    _append_directive_detail(lines, directive, conclusion)
    return "\n".join(lines)


def _append_directive_detail(
    lines: list[str], directive: Mapping[str, Any], conclusion: str
) -> None:
    """Append the referred-crime/waiver/annotation/evidence detail shared by both tiers."""

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
            "기준을 설명하는 데만 쓰고, 이를 근거로 위 결론과 다른 판단을 하지 마라): "
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
            + " (죄 전체의 성립 여부는 위 결론 그대로다)"
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
        if item.get("normalized_status") == "satisfied"
    ]
    denied = [
        str(item.get("definition", ""))
        for item in evidence.values()
        if item.get("normalized_status") == "not_satisfied"
    ]
    undetermined = [
        str(item.get("definition", ""))
        for item in evidence.values()
        if item.get("normalized_status") == "unknown"
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


def _render_verdict_brief(
    *,
    directives: Sequence[Mapping[str, Any]],
    unsupported: Sequence[Mapping[str, Any]],
    invalid: Sequence[Mapping[str, Any]],
    labels: Mapping[str, str],
) -> str:
    """Render symbolic results as a Korean brief, tiered by how much they deserve.

    Four tiers, not two: ``verified``/``provisional`` executed conclusions each
    get their own directive block (see ``_render_directive_block``); ``unsupported``
    (no registered RuleIR for the unit at all) and ``invalid`` (routing/assessment
    contract violations, missing shared-module dependencies, symbolic execution
    failures) are both handed to the writer as pure autonomous reasoning, but kept
    in separate sections so a coverage gap and a pipeline defect are not read as
    the same kind of finding when this brief is inspected later.
    """

    blocks: list[str] = []
    for directive in directives:
        issue_id = str(directive["issue_id"])
        label = labels.get(issue_id) or str(directive["unit_id"])
        tier = directive.get("trust_status", "verified")
        if tier not in ("verified", "provisional"):
            # execute_native_case only ever puts executed results in
            # conclusion_directives, and classify_symbolic_trust only rates those
            # "verified" or "provisional" — this branch should be unreachable.
            continue
        blocks.append(_render_directive_block(directive, label=label, tier=tier))

    unsupported_labels = dict.fromkeys(
        label
        for item in unsupported
        if (
            label := labels.get(str(item.get("issue_id", "")))
            or str(item.get("reported_label", ""))
        )
    )
    if unsupported_labels:
        blocks.append(
            "### 규칙베이스 범위 밖 쟁점 (전적으로 자율 판단)\n"
            + "\n".join(f"- {label}" for label in unsupported_labels)
            + "\n이 쟁점들에 대응하는 규칙이 아직 등록되어 있지 않다. 확정 결론도 잠정 "
            "결론도 없다. 법학 지식으로 직접 학설·판례를 동원하여 충실히 논증하고 "
            "결론을 내려라."
        )

    invalid_labels = dict.fromkeys(
        label
        for item in invalid
        if (
            label := labels.get(str(item.get("issue_id", "")))
            or str(item.get("reported_label", ""))
            or str(item.get("unit_id", ""))
        )
    )
    if invalid_labels:
        blocks.append(
            "### 규칙 추론이 완료되지 못한 쟁점 (전적으로 자율 판단)\n"
            + "\n".join(f"- {label}" for label in invalid_labels)
            + "\n이 쟁점들은 시스템 내부에서 규칙 추론이 완료되지 못했다 — 그 실패 자체는 "
            "결론에 대해 아무것도 말해주지 않는다. 확정 결론도 잠정 결론도 없다고 보고, "
            "법학 지식으로 직접 학설·판례를 동원하여 처음부터 충실히 논증하고 결론을 "
            "내려라."
        )
    return "\n\n".join(blocks) if blocks else "(확정된 판정 없음)"


def _render_routing_context_block(
    *,
    routing_completeness: Mapping[str, Any],
    labels: Mapping[str, str],
    routing_overrides: Sequence[Mapping[str, Any]] = (),
) -> str | None:
    """Surface the router's declared subissue/branch/alternative/label structure.

    This does not re-run routing or add a second model call — the single
    issue-selection call already declared this structure; this only turns it
    into an explicit checklist so the writer keeps a conditional branch open,
    reaches for an alternative doctrine when a fact stays unresolved, and does
    not generalize a specific charge into its parent category (see
    docs/handoff/CURRENT.md diagnosis #3/#5/#6/#7).

    ``routing_overrides`` (from ``apply_routing_overrides``) are issues the
    router itself declined only over participation form/classification and
    that the host then promoted to the exact unit the router had already
    named. The base charge is now argued as settled by the symbolic layer
    like any other routed issue — but the participation-form doubt the router
    raised must not disappear just because the host resolved which charge
    applies; it is preserved here so the writer still argues it explicitly.
    """

    def _label(issue_id: Any) -> str:
        return labels.get(str(issue_id), str(issue_id))

    lines: list[str] = []

    if routing_overrides:
        lines.append(
            "### 다음 쟁점은 기본 성립 여부가 확정됐으나 참여형태는 별도로 논증하라"
        )
        for record in routing_overrides:
            label = _label(record.get("issue_id"))
            lines.append(
                f"- {label}: 기본 죄책의 성립 여부는 확정됐다. 다만 "
                f"{record.get('unsupported_reason', '')} — 이 참여형태(직접정범/"
                "간접정범/공동정범/교사/방조 등) 또는 세부 분류는 아직 불확정이므로 "
                "답안에서 별도로 논증하고 결론을 내려라."
            )

    subissues = routing_completeness.get("required_subissues", [])
    if subissues:
        lines.append("### 다음 하위 쟁점을 별도로 반드시 논증하라")
        for record in subissues:
            parent = _label(record.get("parent_issue_id"))
            lines.append(f"- {parent}과 관련해: {record.get('reason', '')}")

    facts = routing_completeness.get("conclusion_sensitive_facts", [])
    if facts:
        lines.append(
            "### 다음 사실관계는 그 인정 여부에 따라 결론이 달라진다 — "
            "인정되는 경우와 인정되지 않는 경우를 모두 검토하고 각각 결론까지 내려라"
        )
        for record in facts:
            quote = record.get("fact_source_quote", "")
            affected = ", ".join(
                _label(issue_id) for issue_id in record.get("affects_issue_ids", [])
            )
            lines.append(f"- \"{quote}\" (관련 쟁점: {affected}) — {record.get('reason', '')}")

    branches = routing_completeness.get("unresolved_branch_points", [])
    if branches:
        lines.append(
            "### 다음 사실은 아직 확정되지 않았다 — 그 판단에 따라 갈리는 "
            "경우의 수를 모두 검토하고 각각의 결론까지 내려라"
        )
        for record in branches:
            quote = record.get("branch_trigger_quote", "")
            affected = ", ".join(
                _label(issue_id) for issue_id in record.get("affects_issue_ids", [])
            )
            conditions = "; ".join(record.get("branch_conditions", []))
            lines.append(
                f"- \"{quote}\" (관련 쟁점: {affected}) — 가능한 경우: {conditions} "
                f"— {record.get('reason', '')}"
            )

    alternatives = routing_completeness.get("alternative_legal_routes", [])
    if alternatives:
        lines.append("### 다음 쟁점은 사실관계에 따라 다른 죄로 대체 적용될 수 있다")
        for record in alternatives:
            primary = _label(record.get("primary_issue_id"))
            lines.append(
                f"- {primary}: {record.get('condition', '')} — {record.get('reason', '')}"
            )

    exact_labels = routing_completeness.get("exact_labels", {})
    if exact_labels:
        lines.append(
            "### 다음 쟁점의 정확한 죄명·유형을 그대로 표기하라 "
            "(더 일반적인 명칭으로 단순화하지 마라)"
        )
        for issue_id, label in exact_labels.items():
            lines.append(f"- {_label(issue_id)} → **{label}**")

    return "\n\n".join(lines) if lines else None


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
    # A participation-form-only decline of a candidate the router itself named
    # is not a coverage gap — promote it before the issue ever reaches the
    # writer as "unsupported", so 01_issue_selection.json already reflects the
    # corrected routing (docs/handoff/CURRENT.md "decision 단계 프롬프트 수정
    # 시도" — three prompt-only fixes failed, this replaces them).
    selection, routing_overrides = apply_routing_overrides(selection)
    _write_json(out_dir / "01_issue_selection.json", selection)
    if routing_overrides:
        _write_json(
            out_dir / "01d_routing_overrides.json",
            {"overrides": routing_overrides},
        )
    routing_completeness = assess_routing_completeness(selection)
    _write_json(out_dir / "01b_routing_completeness.json", routing_completeness)
    unsupported_diagnostics = diagnose_unsupported_issues(selection)
    if unsupported_diagnostics:
        _write_json(
            out_dir / "01c_unsupported_diagnostics.json",
            {"unsupported_issues": unsupported_diagnostics},
        )

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
        _write_json(
            out_dir / f"02_assessment_{index:02d}_{issue_id}.json", assessment
        )
        assessment_metadata[issue_id] = metadata
        try:
            validate_predicate_assessment(
                assessment,
                case_id=case_id,
                issue_id=issue_id,
                unit_id=unit_id,
                case_text=case_text,
            )
        except NativeHostError as exc:
            # The model's predicate assessment for this one issue violated the
            # quote/missing-facts contract (e.g. declared not_satisfied with no
            # source quote). That is a defect in this issue, not grounds to
            # discard every other issue the case selected fine — same
            # per-issue degradation as a rejected issue selection.
            rejected.append({
                "issue_id": issue_id,
                "unit_id": unit_id,
                "reported_label": str(request.get("reported_label", "")),
                "issue_status": "contract_degraded",
                "symbolic_verdict": "unavailable",
                "generation_mode": "nonbinding_fallback",
                "degraded_reason": ["predicate_assessment_invalid"],
                "reason": str(exc),
            })
            continue
        unit_runs.append(
            {
                "issue_id": issue_id,
                "unit_id": unit_id,
                "depends_on_issue_ids": request["depends_on_issue_ids"],
                "assessment_payload": assessment,
            }
        )

    if rejected:
        _write_json(out_dir / "01_rejected_issues.json", {"rejected": rejected})

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
    # The router's own required_conclusions overrides the generic reported_label
    # with the precise charge name it declared — this is what stops "특수강도"
    # from surfacing as plain "강도" once it reaches the writer (diagnosis #5).
    labels.update(
        {
            issue_id: label
            for issue_id, label in routing_completeness["exact_labels"].items()
            if label
        }
    )
    directives = contract.get("conclusion_directives", [])
    verdict_brief = _render_verdict_brief(
        directives=directives,
        unsupported=unsupported,
        # A malformed selection or a broken symbolic run both carry zero legal
        # signal, so they are folded into one autonomous-reasoning tier — see
        # classify_symbolic_trust and the "invalid" docstring on it.
        invalid=[*contract.get("skipped_directives", []), *rejected],
        labels=labels,
    )
    routing_context = _render_routing_context_block(
        routing_completeness=routing_completeness,
        labels=labels,
        routing_overrides=routing_overrides,
    )
    if routing_context:
        verdict_brief = f"{verdict_brief}\n\n{routing_context}"

    write_system, write_user = PROMPTS["section_write"]
    user_template = load_prompt(write_user)
    user_prompt = (
        user_template
        .replace("{{CASE_TEXT}}", case_text)
        .replace("{{QUESTION_PROMPT}}", str(case.get("question_prompt", "")))
        .replace("{{SYMBOLIC_DIRECTIVES}}", verdict_brief)
    )
    _write_text(out_dir / "04_write_prompt.md", user_prompt + "\n")
    answer_raw = client.complete_text(
        system_prompt=load_prompt(write_system),
        user_template=user_prompt,
        payload={},
        max_tokens=8000,
        temperature=0.0,
    ).strip()
    # The writer's own VERDICT_MANIFEST trailer is a machine contract, not part of
    # the graded prose (see prompts/rule_ir_native_write.md rule 6) — it must never
    # reach a reader or a judge, but it is exactly what lets us catch the writer
    # silently disagreeing with a verified conclusion instead of just asserting it.
    verdict_contradictions = check_verdict_consistency(
        answer_markdown=answer_raw, directives=directives
    )
    answer_markdown = strip_verdict_manifest(answer_raw)
    writing_metadata = {"characters": len(answer_markdown), "mode": "unified_irac"}
    _write_text(out_dir / "05_answer_raw.md", answer_raw + "\n")
    _write_text(out_dir / "05_answer.md", answer_markdown + "\n")
    if verdict_contradictions:
        _write_json(
            out_dir / "06_verdict_consistency.json",
            {"contradictions": verdict_contradictions},
        )

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
        "verdict_contradiction_count": len(verdict_contradictions),
        "routing_gap_count": len(routing_completeness["gaps"]),
        "unsupported_routing_miss_count": sum(
            1 for item in unsupported_diagnostics if item["likely_routing_miss"]
        ),
        "completed": True,
    }
    _write_json(out_dir / "run_manifest.json", manifest)
    return {
        "selection": selection,
        "resolved_requests": resolved,
        "native_report": native_report,
        "answer_markdown": answer_markdown,
        "verdict_contradictions": verdict_contradictions,
        "routing_completeness": routing_completeness,
        "unsupported_diagnostics": unsupported_diagnostics,
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
