"""Run the audited RuleIR-native path on selected substantive KCL questions."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from itertools import combinations
from pathlib import Path
from typing import Any, Callable, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.eval.input_formatter import (  # noqa: E402
    ALLOWED_INPUT_FIELDS,
    assert_no_leaked_fields,
    scoped_question_text,
)
from idpr.generation.native_hybrid_answer import (  # noqa: E402
    finalize_hybrid_answer,
    hybrid_answer_schema,
    render_hybrid_markdown,
)
from idpr.neural.fact_graph import (  # noqa: E402
    admit_fact_graph,
    assessment_facts,
    fact_graph_schema,
)
from idpr.neural.issue_assessment import (  # noqa: E402
    SCHEMA_VERSION,
    issue_assessment_schema,
    validate_issue_assessments,
)
from idpr.neural.vllm_client import VLLMClient  # noqa: E402
from idpr.prompts import load_prompt, prompt_path  # noqa: E402
from idpr.rulegen.native_host import (  # noqa: E402
    NativeHostError,
    closed_issue_selection_schema,
    execute_native_unit,
    predicate_assessment_request,
    validate_closed_issue_selection,
)
from idpr.rulegen.registry import build_registry  # noqa: E402


DEFAULT_CASES = (
    "kcl_criminal_r14_p1_q2",
    "kcl_criminal_r12_p1_q2",
)
PROMPTS = {
    "fact": ("rule_ir_native_fact_extract", "rule_ir_native_fact_extract_user"),
    "selection": ("rule_ir_native_issue_select", "rule_ir_native_issue_select_user"),
    "assessment": (
        "rule_ir_native_predicate_assess",
        "rule_ir_native_predicate_assess_user",
    ),
    "generation": (
        "rule_ir_native_hybrid_generate",
        "rule_ir_native_hybrid_generate_user",
    ),
}


def _read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected object")
    return value


def _write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _require_prompt_audit(path: Path) -> dict[str, Any]:
    report = _read_json(path)
    if report.get("status") != "pass" or report.get("api_calls") != 0:
        raise ValueError("prompt audit is absent or did not pass before execution")
    expected = {
        item["system"]: item["system_sha256"] for item in report["prompts"]
    } | {item["user"]: item["user_sha256"] for item in report["prompts"]}
    changed = [name for name, digest in expected.items() if _sha256(prompt_path(name)) != digest]
    if changed:
        raise ValueError(f"prompts changed after audit: {changed}")
    return report


def _inventory(path: Path) -> dict[str, dict[str, Any]]:
    return {
        row["sub_question_id"]: row
        for row in (
            json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    }


def _whitelisted_case(row: Mapping[str, Any]) -> dict[str, Any]:
    case = {key: row[key] for key in ALLOWED_INPUT_FIELDS}
    assert_no_leaked_fields(case)
    return case


def _labels() -> dict[str, str]:
    labels = {"fraud": "사기"}
    property_manifest = _read_json(
        ROOT / "data/rulegen/property/rule_ir_unit_manifest.json"
    )
    labels.update({item["issue_tag"]: item["label"] for item in property_manifest["units"]})
    p2_manifest = _read_json(ROOT / "data/rulegen/p2/p2_native_unit_manifest.json")
    labels.update({item["unit_id"]: item["label"] for item in p2_manifest["units"]})
    return labels


def _native_fact_schema() -> dict[str, Any]:
    schema = fact_graph_schema()
    for field in ("issue_candidates", "retrieval_queries"):
        schema["properties"][field]["minItems"] = 0
        schema["properties"][field]["maxItems"] = 0
    return schema


def _call(
    *,
    client: VLLMClient,
    stage: str,
    payload: Mapping[str, Any],
    schema: Mapping[str, Any],
    max_tokens: int,
    validator: Callable[[Mapping[str, Any]], None],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    system_name, user_name = PROMPTS[stage]
    attempts = []
    active = dict(payload)
    for attempt in range(1, 3):
        output, metadata = client.complete_json(
            system_prompt=load_prompt(system_name),
            user_template=load_prompt(user_name),
            payload=active,
            schema_name=f"rule_ir_native_{stage}_{attempt}",
            schema=schema,
            max_tokens=max_tokens,
            temperature=0.0,
        )
        try:
            validator(output)
        except Exception as error:
            attempts.append({
                "attempt": attempt,
                "metadata": metadata,
                "error": f"{type(error).__name__}: {error}",
            })
            if attempt == 2:
                raise
            active = {
                **dict(payload),
                "contract_correction": {
                    "instruction": "전체 JSON을 다시 출력하고 아래 host 오류를 모두 고쳐라.",
                    "host_error": str(error),
                },
            }
            continue
        attempts.append({"attempt": attempt, "metadata": metadata, "error": None})
        return dict(output), attempts
    raise AssertionError("unreachable")


def _allowed_units() -> list[dict[str, Any]]:
    labels = _labels()
    return [
        {
            "unit_id": unit_id,
            "label": labels.get(unit_id, unit_id),
            "articles": list(entry.article_ids),
            "role_arguments": [
                item["name"] for item in entry.role_predicate["arguments"]
                if item["name"] != "case_id"
            ],
            "shared_module": entry.shared_module,
        }
        for unit_id, entry in sorted(build_registry().items())
    ]


def _role_values(
    *, case_id: str, unit_id: str, candidates: Mapping[str, Any]
) -> dict[str, str]:
    entry = build_registry()[unit_id]
    expected = [item["name"] for item in entry.role_predicate["arguments"]]
    values = {"case_id": case_id}
    for name in expected:
        if name == "case_id":
            continue
        value = candidates.get(name)
        if not isinstance(value, str) or not value:
            raise NativeHostError(f"{unit_id}: role_candidates missing {name}")
        values[name] = value
    extra = sorted(set(candidates) - set(expected))
    if extra:
        raise NativeHostError(f"{unit_id}: role_candidates contains unknown roles {extra}")
    return values


def _validate_selection_with_roles(
    output: Mapping[str, Any], *, case_id: str, question_text: str
) -> None:
    validate_closed_issue_selection(
        output, case_id=case_id, question_text=question_text
    )
    for issue in output["issues"]:
        if issue["unit_id"] != "unsupported":
            _role_values(
                case_id=case_id,
                unit_id=str(issue["unit_id"]),
                candidates=issue["role_candidates"],
            )


def _distinct_pairs(role_values: Mapping[str, str]) -> list[list[str]]:
    values = list(dict.fromkeys(
        value for key, value in role_values.items() if key != "case_id"
    ))
    return [list(pair) for pair in combinations(values, 2)]


def _rich_symbolic_section(
    *,
    issue: Mapping[str, Any],
    runtime: Mapping[str, Any],
) -> dict[str, Any]:
    unit_id = str(issue["unit_id"])
    entry = build_registry()[unit_id]
    labels = _labels()
    evidence = runtime["assessment_evidence"]
    predicates = []
    for predicate in entry.commentary_inputs:
        item = evidence[predicate["id"]]
        source_quotes = [
            source["quote"] for source in predicate.get("source_refs", [])
            if isinstance(source, Mapping) and source.get("quote")
        ]
        predicates.append({
            "predicate": predicate["id"],
            "rule": predicate.get("definition", ""),
            "authority_quote": source_quotes[0] if source_quotes else "",
            **item,
        })
    return {
        "section_id": str(issue["issue_id"]),
        "heading": labels.get(unit_id, unit_id),
        "authority": "rule_ir_scallop",
        "symbolic_directive": runtime["symbolic_conclusion"],
        "established_relations": list(runtime["established_relations"]),
        "predicates": predicates,
    }


def run_case(
    *,
    client: VLLMClient,
    case: Mapping[str, Any],
    case_dir: Path,
    fact_max_tokens: int,
    selection_max_tokens: int,
    assessment_max_tokens: int,
    generation_max_tokens: int,
) -> dict[str, Any]:
    case_id = str(case["sub_question_id"])
    case_dir.mkdir(parents=True, exist_ok=True)
    scoped = scoped_question_text(str(case["question_text"]), str(case["question_prompt"]))
    fact_request = {
        "case_id": case_id,
        "case_text": scoped,
        "question_prompt": case["question_prompt"],
    }
    assert_no_leaked_fields(fact_request)
    fact_output, fact_attempts = _call(
        client=client,
        stage="fact",
        payload=fact_request,
        schema=_native_fact_schema(),
        max_tokens=fact_max_tokens,
        validator=lambda output: admit_fact_graph(
            output, case_id=case_id, question_text=str(case["question_text"])
        ),
    )
    graph = admit_fact_graph(
        fact_output, case_id=case_id, question_text=str(case["question_text"])
    ).payload
    _write_json(case_dir / "01_fact_graph.json", {
        "request": fact_request, "output": graph, "attempts": fact_attempts
    })

    selection_request = {
        "case_id": case_id,
        "question_text": scoped,
        "question_prompt": case["question_prompt"],
        "entities": graph["entities"],
        "facts": assessment_facts(graph),
        "allowed_units": _allowed_units(),
    }
    assert_no_leaked_fields(selection_request)
    selection, selection_attempts = _call(
        client=client,
        stage="selection",
        payload=selection_request,
        schema=closed_issue_selection_schema(case_id=case_id),
        max_tokens=selection_max_tokens,
        validator=lambda output: _validate_selection_with_roles(
            output,
            case_id=case_id,
            question_text=str(case["question_text"]),
        ),
    )
    _write_json(case_dir / "02_issue_selection.json", {
        "request": selection_request, "output": selection, "attempts": selection_attempts
    })

    facts = assessment_facts(graph)
    fact_ids = [item["fact_id"] for item in facts]
    symbolic_sections = []
    unsupported_sections = []
    unit_artifacts = []
    established_issues: list[str] = []
    ordered_issues = sorted(
        selection["issues"],
        key=lambda item: (
            item["unit_id"] == "unsupported",
            item["unit_id"] != "unsupported"
            and build_registry()[item["unit_id"]].shared_module,
        ),
    )
    for issue in ordered_issues:
        unit_id = str(issue["unit_id"])
        if unit_id == "unsupported":
            unsupported_sections.append({
                "section_id": str(issue["issue_id"]),
                "heading": str(issue["reported_label"]),
                "authority": "model_only_general_part_experiment",
                "source_quote": str(issue["source_quote"]),
                "role_candidates": dict(issue["role_candidates"]),
            })
            continue
        entry = build_registry()[unit_id]
        if entry.shared_module and not established_issues:
            unit_artifacts.append({
                "issue_id": issue["issue_id"],
                "unit_id": unit_id,
                "status": "prerequisite_not_established",
            })
            continue
        assessment_request = predicate_assessment_request(
            case=case, fact_graph=graph, unit_id=unit_id
        )
        assessment_request["version"] = SCHEMA_VERSION
        predicate_ids = [item["id"] for item in entry.commentary_inputs]
        assessment_schema = issue_assessment_schema(
            case_id=case_id, issue_ids=predicate_ids, fact_ids=fact_ids
        )
        assessment, assessment_attempts = _call(
            client=client,
            stage="assessment",
            payload=assessment_request,
            schema=assessment_schema,
            max_tokens=assessment_max_tokens,
            validator=lambda output, ids=predicate_ids: validate_issue_assessments(
                output, case_id=case_id, issue_ids=ids, fact_ids=fact_ids
            ),
        )
        roles = _role_values(
            case_id=case_id,
            unit_id=unit_id,
            candidates=issue["role_candidates"],
        )
        runtime = execute_native_unit(
            unit_id=unit_id,
            case_id=case_id,
            role_values=roles,
            fact_graph=graph,
            assessment_payload=assessment,
            distinct_entities=_distinct_pairs(roles),
            work_dir=case_dir / "runtime" / str(issue["issue_id"]),
        )
        if runtime["symbolic_conclusion"] == "established":
            established_issues.append(str(issue["issue_id"]))
        artifact = {
            "issue_id": issue["issue_id"],
            "unit_id": unit_id,
            "role_values": roles,
            "assessment_request": assessment_request,
            "assessment": assessment,
            "assessment_attempts": assessment_attempts,
            "runtime": runtime,
        }
        unit_artifacts.append(artifact)
        symbolic_sections.append(
            _rich_symbolic_section(issue=issue, runtime=runtime)
        )
        _write_json(
            case_dir / f"03_{issue['issue_id']}_{unit_id}.json", artifact
        )

    generation_request = {
        "case_id": case_id,
        "question_text": scoped,
        "question_prompt": case["question_prompt"],
        "facts": facts,
        "sections": [*symbolic_sections, *unsupported_sections],
    }
    assert_no_leaked_fields(generation_request)
    generation, generation_attempts = _call(
        client=client,
        stage="generation",
        payload=generation_request,
        schema=hybrid_answer_schema(generation_request["sections"]),
        max_tokens=generation_max_tokens,
        validator=lambda output: finalize_hybrid_answer(
            request=generation_request, model_payload=output
        ),
    )
    answer = finalize_hybrid_answer(
        request=generation_request, model_payload=generation
    )
    _write_json(case_dir / "04_answer.json", {
        "request": generation_request,
        "model_output": generation,
        "answer": answer,
        "attempts": generation_attempts,
    })
    markdown = render_hybrid_markdown(answer)
    (case_dir / "04_answer.md").write_text(markdown, encoding="utf-8")
    summary = {
        "case_id": case_id,
        "selected_issues": len(selection["issues"]),
        "symbolic_sections": len(symbolic_sections),
        "model_only_general_part_sections": len(unsupported_sections),
        "unit_outcomes": {
            artifact["issue_id"]: (
                artifact["runtime"]["symbolic_conclusion"]
                if "runtime" in artifact else artifact["status"]
            )
            for artifact in unit_artifacts
        },
        "answer_path": str(case_dir / "04_answer.md"),
    }
    _write_json(case_dir / "summary.json", summary)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--api-key", default="local-idpr")
    parser.add_argument(
        "--inventory",
        type=Path,
        default=ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl",
    )
    parser.add_argument(
        "--prompt-audit",
        type=Path,
        default=ROOT / "data/e2e/rule_ir_native/prompt_audit.json",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=ROOT / "experiments/results/rule_ir_native_kcl_e2e",
    )
    parser.add_argument("--case-id", action="append", default=[])
    parser.add_argument("--fact-max-tokens", type=int, default=12288)
    parser.add_argument("--selection-max-tokens", type=int, default=4096)
    parser.add_argument("--assessment-max-tokens", type=int, default=32768)
    parser.add_argument("--generation-max-tokens", type=int, default=16384)
    args = parser.parse_args()

    audit = _require_prompt_audit(args.prompt_audit)
    inventory = _inventory(args.inventory)
    case_ids = tuple(args.case_id) or DEFAULT_CASES
    unknown = sorted(set(case_ids) - set(inventory))
    if unknown:
        raise ValueError(f"unknown KCL cases: {unknown}")
    client = VLLMClient(
        base_url=args.base_url,
        model=args.model,
        api_key=args.api_key,
        timeout_seconds=7200,
    )
    args.out_dir.mkdir(parents=True, exist_ok=True)
    summaries = []
    for index, case_id in enumerate(case_ids, 1):
        print(f"[{index}/{len(case_ids)}] {case_id}", flush=True)
        case = _whitelisted_case(inventory[case_id])
        summary = run_case(
            client=client,
            case=case,
            case_dir=args.out_dir / case_id,
            fact_max_tokens=args.fact_max_tokens,
            selection_max_tokens=args.selection_max_tokens,
            assessment_max_tokens=args.assessment_max_tokens,
            generation_max_tokens=args.generation_max_tokens,
        )
        summaries.append(summary)
        print(json.dumps(summary, ensure_ascii=False), flush=True)
    report = {
        "version": "1.0.0",
        "method": "rule_ir_native_kcl_e2e_experiment",
        "model": args.model,
        "prompt_audit_status": audit["status"],
        "prompt_audit_api_calls": audit["api_calls"],
        "semantic_search_used": False,
        "cases": summaries,
    }
    _write_json(args.out_dir / "report.json", report)
    print(f"wrote {args.out_dir / 'report.json'}")


if __name__ == "__main__":
    main()
