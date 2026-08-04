#!/usr/bin/env python3
"""Run the normalized minimal-predicate RuleIR pipeline on KCL cases."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Callable, Mapping


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.eval.input_formatter import assert_no_leaked_fields, scoped_question_text  # noqa: E402
from idpr.generation.native_hybrid_answer import (  # noqa: E402
    finalize_hybrid_answer,
    hybrid_answer_schema,
    render_hybrid_markdown,
)
from idpr.neural.core_contract import (  # noqa: E402
    assessment_groups,
    context_packet,
    core_assessment_schema,
    core_issue_selection_schema,
    role_binding_schema,
    selected_track_closure,
    validate_core_assessments,
    validate_core_issue_selection,
    validate_role_binding,
)
from idpr.neural.vllm_client import VLLMClient  # noqa: E402
from idpr.prompts import load_prompt, prompt_path  # noqa: E402
from idpr.rulegen.core_profile import load_core_profiles  # noqa: E402
from idpr.rulegen.core_runtime import execute_core_unit  # noqa: E402


DEFAULT_CASES = ("kcl_criminal_r14_p1_q2", "kcl_criminal_r12_p1_q2")
PROMPTS = {
    "selection": ("rule_ir_core_issue_select", "rule_ir_core_issue_select_user"),
    "binding": ("rule_ir_core_role_bind", "rule_ir_core_role_bind_user"),
    "assessment": ("rule_ir_core_assess", "rule_ir_core_assess_user"),
    "generation": ("rule_ir_native_hybrid_generate", "rule_ir_native_hybrid_generate_user"),
}


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _inventory(path: Path) -> dict[str, dict[str, Any]]:
    return {
        row["sub_question_id"]: row
        for row in (
            json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    }


def _labels() -> dict[str, str]:
    labels = {"fraud": "사기"}
    property_manifest = _read_json(ROOT / "data/rulegen/property/rule_ir_unit_manifest.json")
    labels.update({item["issue_tag"]: item["label"] for item in property_manifest["units"]})
    p2_manifest = _read_json(ROOT / "data/rulegen/p2/p2_native_unit_manifest.json")
    labels.update({item["unit_id"]: item["label"] for item in p2_manifest["units"]})
    return labels


def _catalog(profiles: Mapping[str, Any]) -> list[dict[str, Any]]:
    labels = _labels()
    return [
        {
            "unit_id": unit_id,
            "label": labels.get(unit_id, unit_id),
            "articles": profile["article_ids"],
            "role_scope": profile["role_contract"]["definition"],
            "role_arguments": [
                item["name"] for item in profile["role_contract"]["arguments"]
                if item["name"] != "case_id"
            ],
            "tracks": [item["track_id"] for item in profile["tracks"]],
            "shared_module": profile["shared_module"],
        }
        for unit_id, profile in sorted(profiles.items())
    ]


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
    active: dict[str, Any] = dict(payload)
    for attempt in range(1, 3):
        output, metadata = client.complete_json(
            system_prompt=load_prompt(system_name),
            user_template=load_prompt(user_name),
            payload=active,
            schema_name=f"rule_ir_core_{stage}_{attempt}",
            schema=schema,
            max_tokens=max_tokens,
            temperature=0.0,
        )
        try:
            validator(output)
        except Exception as error:
            attempts.append({"attempt": attempt, "metadata": metadata, "error": str(error)})
            if attempt == 2:
                raise
            active = {
                **dict(payload),
                "contract_correction": {
                    "instruction": "전체 JSON을 다시 출력하고 host 오류를 모두 고쳐라.",
                    "host_error": str(error),
                },
            }
            continue
        attempts.append({"attempt": attempt, "metadata": metadata, "error": None})
        return dict(output), attempts
    raise AssertionError("unreachable")


def _prompt_hashes() -> dict[str, str]:
    result = {}
    for system, user in PROMPTS.values():
        for name in (system, user):
            result[name] = hashlib.sha256(prompt_path(name).read_bytes()).hexdigest()
    return result


def _require_audit(path: Path) -> dict[str, Any]:
    report = _read_json(path)
    if report.get("status") != "pass" or report.get("api_calls") != 0:
        raise ValueError("normalized core prompt audit did not pass")
    if report.get("prompt_hashes") != _prompt_hashes():
        raise ValueError("normalized core prompts changed after preflight")
    return report


def _role_values(binding: Mapping[str, Any]) -> dict[str, str]:
    return {
        "case_id": str(binding["case_id"]),
        **{
            role: str(item["entity_id"])
            for role, item in binding["role_bindings"].items()
        },
    }


def _symbolic_sections(
    *,
    issue: Mapping[str, Any],
    profile: Mapping[str, Any],
    binding: Mapping[str, Any],
    assessments: Mapping[str, Mapping[str, Any]],
    runtime: Mapping[str, Any],
) -> list[dict[str, Any]]:
    labels = _labels()
    predicates = {item["predicate_id"]: item for item in profile["model_input_predicates"]}
    tracks = {item["track_id"]: item for item in profile["tracks"]}
    sections = []
    for track_id in binding["selected_tracks"]:
        relevant = list(dict.fromkeys(
            component
            for path in tracks[track_id]["paths"]
            for component in path["components"]
        ))
        outcome = runtime["track_outcomes"][track_id]
        heading = labels.get(profile["unit_id"], profile["unit_id"])
        if len(profile["tracks"]) > 1:
            heading = f"{heading} — {track_id}"
        sections.append({
            "section_id": f"{issue['issue_id']}.{track_id}",
            "heading": heading,
            "authority": "rule_ir_scallop",
            "unit_id": profile["unit_id"],
            "track_id": track_id,
            "role_bindings": binding["role_bindings"],
            "relations": binding["relations"],
            "predicates": [
                {
                    "definition": predicates[predicate_id]["definition"],
                    "status": assessments[predicate_id]["status"],
                    "source_quotes": assessments[predicate_id]["source_quotes"],
                    "reason": assessments[predicate_id]["reason"],
                    "authority_card_ids": predicates[predicate_id]["authority_card_ids"],
                }
                for predicate_id in relevant
            ],
            "symbolic_directive": outcome["symbolic_conclusion"],
            "established_relations": (
                [outcome["established_relation"]]
                if outcome["symbolic_conclusion"] == "established" else []
            ),
        })
    return sections


def run_case(
    *,
    case: Mapping[str, Any],
    profiles: Mapping[str, Any],
    client: VLLMClient,
    case_dir: Path,
    max_group: int,
) -> dict[str, Any]:
    case_id = str(case["sub_question_id"])
    scoped = scoped_question_text(str(case["question_text"]), str(case["question_prompt"]))
    selection_request = {
        "case_id": case_id, "question_text": scoped,
        "question_prompt": case["question_prompt"], "allowed_units": _catalog(profiles),
    }
    assert_no_leaked_fields(selection_request)
    selection, attempts = _call(
        client=client, stage="selection", payload=selection_request,
        schema=core_issue_selection_schema(case_id=case_id, unit_ids=sorted(profiles)),
        max_tokens=4096,
        validator=lambda output: validate_core_issue_selection(
            output, case_id=case_id, case_text=scoped, unit_ids=sorted(profiles)
        ),
    )
    _write_json(case_dir / "01_issue_selection.json", {
        "request": selection_request, "output": selection, "attempts": attempts,
    })

    symbolic_sections: list[dict[str, Any]] = []
    unsupported_sections: list[dict[str, Any]] = []
    outcomes: dict[str, Any] = {}
    for issue in selection["issues"]:
        issue_id = str(issue["issue_id"])
        unit_id = str(issue["unit_id"])
        if unit_id == "unsupported":
            unsupported_sections.append({
                "section_id": issue_id, "heading": issue["reported_label"],
                "authority": "model_only_general_part_experiment",
                "source_quote": issue["source_quote"],
            })
            continue
        profile = profiles[unit_id]
        if profile["shared_module"]:
            outcomes[issue_id] = {"status": "shared_module_bridge_missing", "unit_id": unit_id}
            continue
        binding_request = {
            "case_id": case_id, "issue_id": issue_id, "unit_id": unit_id,
            "question_text": scoped, "issue_source_quote": issue["source_quote"],
            "role_contract": profile["role_contract"],
            "available_tracks": profile["tracks"],
            "core_predicates": [
                {"predicate_id": item["predicate_id"], "definition": item["definition"]}
                for item in profile["model_input_predicates"]
            ],
        }
        binding, binding_attempts = _call(
            client=client, stage="binding", payload=binding_request,
            schema=role_binding_schema(case_id=case_id, issue_id=issue_id, profile=profile),
            max_tokens=8192,
            validator=lambda output, p=profile, i=issue_id: validate_role_binding(
                output, case_text=scoped, case_id=case_id, issue_id=i, profile=p
            ),
        )
        _write_json(case_dir / f"02_{issue_id}_{unit_id}_binding.json", {
            "request": binding_request, "output": binding, "attempts": binding_attempts,
        })
        all_assessments: dict[str, Any] = {}
        group_artifacts = []
        for group in assessment_groups(
            profile, binding["selected_tracks"], max_predicates=max_group
        ):
            predicate_ids = [item["predicate_id"] for item in group["predicates"]]
            request = {
                "case_id": case_id, "issue_id": issue_id, "unit_id": unit_id,
                "track_id": group["track_id"], "question_text": scoped,
                "entities": binding["entities"], "role_bindings": binding["role_bindings"],
                "relations": binding["relations"], "predicates": group["predicates"],
                "authority_context": context_packet(profile, predicate_ids, max_sources=2),
            }
            assessment, assessment_attempts = _call(
                client=client, stage="assessment", payload=request,
                schema=core_assessment_schema(case_id=case_id, predicate_ids=predicate_ids),
                max_tokens=12288,
                validator=lambda output, ids=predicate_ids: validate_core_assessments(
                    output, case_id=case_id, case_text=scoped, predicate_ids=ids
                ),
            )
            all_assessments.update(assessment["assessments"])
            group_artifacts.append({
                "group": group, "request": request, "output": assessment,
                "attempts": assessment_attempts,
            })
        needed = {
            component
            for track_id in selected_track_closure(profile, binding["selected_tracks"])
            for path in next(
                item for item in profile["tracks"] if item["track_id"] == track_id
            )["paths"]
            for component in path["components"]
        }
        if set(all_assessments) != needed:
            raise ValueError(f"{issue_id}: incomplete core assessment merge")
        _write_json(case_dir / f"03_{issue_id}_{unit_id}_assessments.json", {
            "groups": group_artifacts, "merged_assessments": all_assessments,
        })
        runtime = execute_core_unit(
            profile=profile, case_id=case_id, role_values=_role_values(binding),
            selected_tracks=binding["selected_tracks"], assessments=all_assessments,
            work_dir=case_dir / "runtime" / issue_id,
        )
        _write_json(case_dir / f"04_{issue_id}_{unit_id}_runtime.json", runtime)
        symbolic_sections.extend(_symbolic_sections(
            issue=issue, profile=profile, binding=binding,
            assessments=all_assessments, runtime=runtime,
        ))
        outcomes[issue_id] = runtime["track_outcomes"]

    generation_request = {
        "case_id": case_id, "question_text": scoped,
        "question_prompt": case["question_prompt"],
        "sections": [*symbolic_sections, *unsupported_sections],
    }
    generation, generation_attempts = _call(
        client=client, stage="generation", payload=generation_request,
        schema=hybrid_answer_schema(generation_request["sections"]),
        max_tokens=16384,
        validator=lambda output: finalize_hybrid_answer(
            request=generation_request, model_payload=output
        ),
    )
    answer = finalize_hybrid_answer(request=generation_request, model_payload=generation)
    _write_json(case_dir / "05_answer.json", {
        "request": generation_request, "model_output": generation,
        "answer": answer, "attempts": generation_attempts,
    })
    markdown = render_hybrid_markdown(answer)
    (case_dir / "05_answer.md").write_text(markdown, encoding="utf-8")
    summary = {
        "case_id": case_id,
        "selected_issues": len(selection["issues"]),
        "symbolic_sections": len(symbolic_sections),
        "model_only_general_part_sections": len(unsupported_sections),
        "outcomes": outcomes,
        "answer_path": str(case_dir / "05_answer.md"),
    }
    _write_json(case_dir / "summary.json", summary)
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--api-key", default="local-idpr")
    parser.add_argument(
        "--inventory", type=Path,
        default=ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl",
    )
    parser.add_argument(
        "--prompt-audit", type=Path,
        default=ROOT / "data/e2e/rule_ir_core/prompt_audit.json",
    )
    parser.add_argument(
        "--out-dir", type=Path,
        default=ROOT / "experiments/results/rule_ir_core_kcl_e2e",
    )
    parser.add_argument("--case-id", action="append", default=[])
    parser.add_argument("--max-group", type=int, default=10)
    args = parser.parse_args()
    audit = _require_audit(args.prompt_audit)
    profiles = load_core_profiles()["units"]
    inventory = _inventory(args.inventory)
    case_ids = tuple(args.case_id) or DEFAULT_CASES
    client = VLLMClient(
        base_url=args.base_url, model=args.model, api_key=args.api_key,
        timeout_seconds=7200,
    )
    summaries = []
    for index, case_id in enumerate(case_ids, 1):
        if case_id not in inventory:
            raise ValueError(f"unknown KCL case: {case_id}")
        print(f"[{index}/{len(case_ids)}] {case_id}", flush=True)
        summaries.append(run_case(
            case=inventory[case_id], profiles=profiles, client=client,
            case_dir=args.out_dir / case_id, max_group=args.max_group,
        ))
    report = {
        "version": "1.0.0", "pipeline": "rule_ir_core_normalized",
        "prompt_audit": audit, "cases": summaries,
    }
    _write_json(args.out_dir / "report.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
