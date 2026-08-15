"""Deterministic Phase-3 E2E freeze contract.

주의: 여기서 말하는 E2E는 **Phase-3 issue/card 파이프라인**이다. 현재 정본인 `idpr.v2`
체인(Call 1 → 1.5 → 2 → symbolic → AnswerPlan → Call 3)과는 다른 실행이고, 이 모듈의
freeze 게이트는 v2 산출물에 대해 아무것도 말하지 않는다. v2의 계보·해시 계약은
`idpr.v2.runtime.plan_lineage`에 있다.

This module validates persisted stage boundaries.  It does not grade legal quality and it
does not read a rubric to construct any model request.  The two activities are deliberately
separated: contract validity is the freeze gate; rubric review happens only after the tagged
run has been frozen.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any, Iterable, Mapping

from idpr.eval.input_formatter import ALLOWED_INPUT_FIELDS
from idpr.generation.issue_answer import validate_issue_answer
from idpr.issue_pipeline import scope_from_l0_row
from idpr.neural.article_select import expand_attempt_articles, load_catalog, validate_selection
from idpr.neural.fact_graph import admit_fact_graph, assessment_facts, fact_tuples
from idpr.neural.issue_assessment import validate_issue_assessments
from idpr.prompts import prompt_path
from idpr.rulebase.compile_scl import QUERY_RELATIONS
from idpr.rulebase.scallop import DEFAULT_SCLI, runtime_version

SMOKE_CASE_IDS = (
    "kcl_criminal_r10_p1_q1_ga",
    "CASE_KCL1730_2026_BRIBERY_FRAUD_002",
)
PROMPT_NAMES = (
    "fact_graph_extract",
    "fact_graph_extract_user",
    "article_select",
    "article_select_user",
    "issue_assess",
    "issue_assess_user",
    "issue_long_form_generate",
    "issue_long_form_generate_user",
)


class E2EContractError(ValueError):
    """Raised when a persisted E2E artifact violates the freeze contract."""


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise E2EContractError(f"{path}: expected a JSON object")
    return payload


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        row = json.loads(line)
        if not isinstance(row, dict):
            raise E2EContractError(f"{path}:{line_number}: expected a JSON object")
        rows.append(row)
    return rows


def index_exact(
    rows: Iterable[Mapping[str, Any]], *, source: str, expected_ids: Iterable[str]
) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for row in rows:
        case_id = str(row.get("sub_question_id", ""))
        if not case_id:
            raise E2EContractError(f"{source}: row has no sub_question_id")
        if case_id in indexed:
            raise E2EContractError(f"{source}: duplicate case {case_id}")
        indexed[case_id] = dict(row)
    expected = tuple(expected_ids)
    if set(indexed) != set(expected):
        raise E2EContractError(
            f"{source}: expected exactly {list(expected)}, got {list(indexed)}"
        )
    return indexed


def validate_smoke_inventory(rows: Iterable[Mapping[str, Any]]) -> dict[str, dict[str, Any]]:
    inventory = index_exact(rows, source="smoke inventory", expected_ids=SMOKE_CASE_IDS)
    for case_id, row in inventory.items():
        extra = sorted(set(row) - ALLOWED_INPUT_FIELDS)
        missing = sorted(ALLOWED_INPUT_FIELDS - set(row))
        if extra or missing:
            raise E2EContractError(
                f"{case_id}: inventory whitelist mismatch; extra={extra}, missing={missing}"
            )
        if not str(row["question_text"]).strip() or not str(row["question_prompt"]).strip():
            raise E2EContractError(f"{case_id}: question text and prompt must be non-empty")
    return inventory


def validate_symbolic_relations(relations: Any, *, case_id: str) -> None:
    if not isinstance(relations, Mapping):
        raise E2EContractError(f"{case_id}: symbolic relations must be an object")
    if set(relations) != set(QUERY_RELATIONS):
        missing = sorted(set(QUERY_RELATIONS) - set(relations))
        extra = sorted(set(relations) - set(QUERY_RELATIONS))
        raise E2EContractError(
            f"{case_id}: symbolic relation mismatch; missing={missing}, extra={extra}"
        )
    for relation, rows in relations.items():
        if not isinstance(rows, list):
            raise E2EContractError(f"{case_id}: {relation} rows must be an array")
        for index, row in enumerate(rows):
            if not isinstance(row, list) or not row or row[0] != case_id:
                raise E2EContractError(
                    f"{case_id}: {relation}[{index}] has a mismatched case id"
                )


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def project_relative(path: Path, project_root: Path) -> str:
    """Return a stable project path even when the workspace is reached through a symlink."""
    try:
        return str(path.resolve().relative_to(project_root.resolve()))
    except ValueError as error:
        raise E2EContractError(f"{path} is outside project root {project_root}") from error


def _git_sha(project_root: Path) -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=project_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _attempt_summary(call2: Mapping[str, Any]) -> dict[str, Any]:
    groups = {
        "initial": call2.get("attempts", []),
        "unknown_refinement": call2.get("refinement", {}).get("attempts", []),
        "relation_followup": call2.get("relation_followup", {}).get("attempts", []),
    }
    return {
        name: {
            "count": len(attempts),
            "sources": [row.get("source") for row in attempts],
            "errors": [error for row in attempts for error in row.get("errors", [])],
        }
        for name, attempts in groups.items()
    }


def verify_run(
    *,
    project_root: Path,
    run_root: Path,
    inventory_path: Path,
    rubric_path: Path,
    model: str,
    slurm_job_id: str,
    parameters: Mapping[str, Any],
    stage_seconds: Mapping[str, float],
    tested_code_commit: str | None = None,
) -> dict[str, Any]:
    inventory = validate_smoke_inventory(read_jsonl(inventory_path))
    rubric = read_json(rubric_path)
    if rubric.get("model_input") is not False:
        raise E2EContractError("rubric must be explicitly marked model_input=false")
    rubric_ids = [str(case.get("sub_question_id", "")) for case in rubric.get("cases", [])]
    if set(rubric_ids) != set(SMOKE_CASE_IDS) or len(rubric_ids) != len(SMOKE_CASE_IDS):
        raise E2EContractError("rubric case ids do not match the smoke inventory")

    graph_rows = index_exact(
        read_jsonl(run_root / "fact_graphs.jsonl"),
        source="Call 1",
        expected_ids=SMOKE_CASE_IDS,
    )
    selection_rows = index_exact(
        read_jsonl(run_root / "article_selection.jsonl"),
        source="Call 1.5",
        expected_ids=SMOKE_CASE_IDS,
    )
    candidate_rows = index_exact(
        read_jsonl(run_root / "l0_candidates.jsonl"),
        source="L0",
        expected_ids=SMOKE_CASE_IDS,
    )
    output_rows = index_exact(
        read_jsonl(run_root / "idpr_nsn_outputs.jsonl"),
        source="Call 3 output",
        expected_ids=SMOKE_CASE_IDS,
    )

    cases: dict[str, Any] = {}
    catalog = load_catalog()
    for case_id in SMOKE_CASE_IDS:
        graph_row = graph_rows[case_id]
        if "error" in graph_row or "fallback" in graph_row:
            raise E2EContractError(f"{case_id}: Call 1 error/fallback is forbidden")
        graph = graph_row.get("fact_graph")
        if not isinstance(graph, Mapping):
            raise E2EContractError(f"{case_id}: Call 1 has no fact graph")
        admitted = admit_fact_graph(
            graph,
            case_id=case_id,
            question_text=str(inventory[case_id]["question_text"]),
        )
        if admitted.dropped_total:
            raise E2EContractError(f"{case_id}: persisted admitted graph is not idempotent")
        fact_tuples(graph, case_id=case_id)

        selection = selection_rows[case_id]
        if "error" in selection:
            raise E2EContractError(f"{case_id}: Call 1.5 contains an error")
        selected, entries = validate_selection({"selected": selection.get("entries")}, catalog=catalog)
        if list(selected) != selection.get("selected") or list(entries) != selection.get("entries"):
            raise E2EContractError(f"{case_id}: Call 1.5 normalized selection differs")
        if list(expand_attempt_articles(selected)) != selection.get("articles"):
            raise E2EContractError(f"{case_id}: Call 1.5 attempt expansion differs")

        scope = scope_from_l0_row(candidate_rows[case_id])
        if not scope.articles or not scope.initial_issues:
            raise E2EContractError(f"{case_id}: L0 produced an empty scope")

        case_dir = run_root / "cases" / case_id
        call2 = read_json(case_dir / "issue_assessment.json")
        if call2.get("case_id") != case_id:
            raise E2EContractError(f"{case_id}: Call 2 case id differs")
        issue_status = call2.get("issue_status")
        if not isinstance(issue_status, Mapping):
            raise E2EContractError(f"{case_id}: Call 2 issue_status is absent")
        assessments = issue_status.get("assessments")
        if not isinstance(assessments, Mapping) or not assessments:
            raise E2EContractError(f"{case_id}: Call 2 assessments are absent")
        validate_issue_assessments(
            issue_status,
            case_id=case_id,
            issue_ids=list(assessments),
            fact_ids=[fact["fact_id"] for fact in assessment_facts(graph)],
        )
        packet = call2.get("reasoning_packet")
        if not isinstance(packet, Mapping) or packet.get("case_id") != case_id:
            raise E2EContractError(f"{case_id}: reasoning packet case id differs")
        symbolic = call2.get("symbolic_runtime")
        if not isinstance(symbolic, Mapping):
            raise E2EContractError(f"{case_id}: symbolic runtime is absent")
        validate_symbolic_relations(symbolic.get("relations"), case_id=case_id)

        call3 = read_json(case_dir / "answer.json")
        if call3.get("case_id") != case_id or call3.get("model") != model:
            raise E2EContractError(f"{case_id}: Call 3 case/model differs")
        request, answer = call3.get("request"), call3.get("answer")
        if not isinstance(request, Mapping) or not isinstance(answer, Mapping):
            raise E2EContractError(f"{case_id}: Call 3 request/answer is absent")
        validate_issue_answer(answer, request=request)
        markdown = (case_dir / "answer.md").read_text(encoding="utf-8")
        if not markdown.strip() or output_rows[case_id].get("generated_response") != markdown:
            raise E2EContractError(f"{case_id}: final markdown/output JSONL differs")

        cases[case_id] = {
            "articles": list(scope.articles),
            "initial_issue_count": len(scope.initial_issues),
            "fact_graph_admission": graph_row.get("admission", {}),
            "fallbacks": [],
            "call2_attempts": _attempt_summary(call2),
            "usage": output_rows[case_id].get("usage", {}),
            "symbolic_relation_counts": {
                relation: len(symbolic["relations"][relation]) for relation in QUERY_RELATIONS
            },
        }

    hashed_files = [
        path
        for path in sorted(run_root.rglob("*"))
        if path.is_file() and path.name != "freeze_manifest.json"
    ]
    return {
        "version": "1.0.0",
        "status": "passed",
        "contract_scope": "two-case structural E2E; no rubric scoring or retrieval gate",
        "tested_code_commit": tested_code_commit or _git_sha(project_root),
        "verifier_commit": _git_sha(project_root),
        "freeze_tag": "phase3-e2e-freeze-v1",
        "slurm_job_id": slurm_job_id,
        "model": model,
        "parameters": dict(parameters),
        "stage_seconds": dict(stage_seconds),
        "prompt_sha256": {name: sha256_file(prompt_path(name)) for name in PROMPT_NAMES},
        "scallop": {
            "path": project_relative(DEFAULT_SCLI, project_root),
            "version": runtime_version(),
            "sha256": sha256_file(DEFAULT_SCLI),
        },
        "inputs": {
            project_relative(inventory_path, project_root): sha256_file(inventory_path),
            project_relative(rubric_path, project_root): sha256_file(rubric_path),
        },
        "artifacts": {
            str(path.relative_to(run_root)): sha256_file(path) for path in hashed_files
        },
        "cases": cases,
    }
