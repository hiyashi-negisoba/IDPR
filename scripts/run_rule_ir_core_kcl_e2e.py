#!/usr/bin/env python3
"""Run the lean closed-unit → core assessment → Scallop → prose pipeline."""

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
from idpr.neural.core_contract import (  # noqa: E402
    core_issue_selection_schema,
    core_unit_analysis_schema,
    needed_predicate_ids,
    validate_core_issue_selection,
    validate_core_unit_analysis,
)
from idpr.neural.vllm_client import VLLMClient, VLLMClientError  # noqa: E402
from idpr.prompts import load_prompt, prompt_path  # noqa: E402
from idpr.rulegen.core_profile import load_core_profiles  # noqa: E402
from idpr.rulegen.core_runtime import execute_core_unit  # noqa: E402


DEFAULT_CASES = ("kcl_criminal_r14_p1_q2", "kcl_criminal_r12_p1_q2")
JSON_PROMPTS = {
    "selection": ("rule_ir_core_issue_select", "rule_ir_core_issue_select_user"),
    "analysis": ("rule_ir_core_assess", "rule_ir_core_assess_user"),
}
WRITE_PROMPT = ("rule_ir_core_write", "rule_ir_core_write_user")


class CoreStageCallError(RuntimeError):
    def __init__(self, *, stage: str, attempts: list[dict[str, Any]]) -> None:
        self.stage = stage
        self.attempts = attempts
        super().__init__(str(attempts[-1]["error"]))


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def _inventory(path: Path) -> dict[str, dict[str, Any]]:
    return {
        row["sub_question_id"]: row
        for row in (
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    }


def _labels() -> dict[str, str]:
    labels = {"fraud": "사기"}
    property_manifest = _read_json(
        ROOT / "data/rulegen/property/rule_ir_unit_manifest.json"
    )
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
        }
        for unit_id, profile in sorted(profiles.items())
    ]


def _predicate_contract(profile: Mapping[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "predicate_id": item["predicate_id"],
            "definition": item["definition"],
            "authority": [
                source["quote"]
                for source in item["source_refs"][:2]
                if source.get("quote")
            ],
        }
        for item in profile["model_input_predicates"]
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
    """One structured call plus one semantic repair; transport may retry twice."""

    system_name, user_name = JSON_PROMPTS[stage]
    attempts: list[dict[str, Any]] = []
    active = dict(payload)
    for attempt in range(1, 4):
        try:
            output, metadata = client.complete_json(
                system_prompt=load_prompt(system_name),
                user_template=load_prompt(user_name),
                payload=active,
                schema_name=f"rule_ir_core_{stage}_{attempt}",
                schema=schema,
                max_tokens=max_tokens,
                temperature=0.0,
            )
        except VLLMClientError as error:
            attempts.append({"attempt": attempt, "metadata": None, "error": str(error)})
            if attempt == 3:
                raise CoreStageCallError(stage=stage, attempts=attempts) from error
            continue
        try:
            validator(output)
        except Exception as error:
            attempts.append({
                "attempt": attempt,
                "metadata": metadata,
                "error": str(error),
                "invalid_output": output,
            })
            if any(item.get("invalid_output") is not None for item in attempts[:-1]):
                raise CoreStageCallError(stage=stage, attempts=attempts) from error
            active = {
                **dict(payload),
                "repair": {
                    "error": str(error),
                    "previous_output": output,
                    "instruction": "내용은 유지하고 표시된 JSON 구조 오류만 고쳐라.",
                },
            }
            continue
        attempts.append({"attempt": attempt, "metadata": metadata, "error": None})
        return dict(output), attempts
    raise AssertionError("unreachable")


def _write_section(
    *, client: VLLMClient, payload: Mapping[str, Any]
) -> str:
    system_name, user_name = WRITE_PROMPT
    try:
        text = client.complete_text(
            system_prompt=load_prompt(system_name),
            user_template=load_prompt(user_name),
            payload=payload,
            max_tokens=2048,
            temperature=0.0,
        ).strip()
    except VLLMClientError as error:
        raise CoreStageCallError(
            stage="writing", attempts=[{"attempt": 1, "error": str(error)}]
        ) from error
    if not text:
        raise CoreStageCallError(
            stage="writing", attempts=[{"attempt": 1, "error": "empty prose"}]
        )
    return text


def _prompt_hashes() -> dict[str, str]:
    names = [
        *(name for pair in JSON_PROMPTS.values() for name in pair),
        *WRITE_PROMPT,
    ]
    return {
        name: hashlib.sha256(prompt_path(name).read_bytes()).hexdigest()
        for name in names
    }


def _require_audit(path: Path) -> dict[str, Any]:
    report = _read_json(path)
    if report.get("status") != "pass" or report.get("api_calls") != 0:
        raise ValueError("lean core prompt audit did not pass")
    if report.get("prompt_hashes") != _prompt_hashes():
        raise ValueError("lean core prompts changed after preflight")
    return report


def _conclusion_label(status: str) -> str:
    return {
        "established": "성립",
        "not_established": "불성립",
        "undetermined": "현재 사실만으로 성립 여부 미확정",
        "conflict": "predicate 평가 충돌로 결론 유보",
        "no_derived_outcome": "RuleIR에서 결론 미도출",
    }[status]


def _writer_predicates(
    *, profile: Mapping[str, Any], analysis: Mapping[str, Any], track_id: str
) -> list[dict[str, Any]]:
    by_id = {
        item["predicate_id"]: item for item in profile["model_input_predicates"]
    }
    return [
        {
            "법적 판단사항": by_id[predicate_id]["definition"],
            "판단": {
                "satisfied": "인정됨",
                "not_satisfied": "부정됨",
                "unknown": "사실 부족으로 미확정",
            }[analysis["assessments"][predicate_id]["status"]],
            "이유": analysis["assessments"][predicate_id]["reason"],
            "권위자료": [
                source["quote"]
                for source in by_id[predicate_id]["source_refs"][:2]
                if source.get("quote")
            ],
        }
        for predicate_id in needed_predicate_ids(profile, [track_id])
    ]


def _render_answer(*, case_id: str, sections: list[dict[str, Any]]) -> str:
    lines = ["# 형법 사례 답안", ""]
    for index, section in enumerate(sections, 1):
        lines.extend([f"## {index}. {section['heading']}", "", section["prose"], ""])
        if section.get("conclusion"):
            lines.extend(["### 결론", "", section["conclusion"], ""])
    return "\n".join(lines).rstrip() + "\n"


def run_case(
    *,
    case: Mapping[str, Any],
    profiles: Mapping[str, Any],
    client: VLLMClient,
    case_dir: Path,
) -> dict[str, Any]:
    case_id = str(case["sub_question_id"])
    question_prompt = str(case["question_prompt"])
    scoped = scoped_question_text(str(case["question_text"]), question_prompt)
    selection_request = {
        "case_id": case_id,
        "question_text": scoped,
        "question_prompt": question_prompt,
        "allowed_units": _catalog(profiles),
    }
    assert_no_leaked_fields(selection_request)
    selection, selection_attempts = _call(
        client=client,
        stage="selection",
        payload=selection_request,
        schema=core_issue_selection_schema(case_id=case_id, unit_ids=sorted(profiles)),
        max_tokens=4096,
        validator=lambda output: validate_core_issue_selection(
            output, case_id=case_id, unit_ids=sorted(profiles)
        ),
    )
    _write_json(case_dir / "00_issue_selection.json", {
        "request": selection_request,
        "output": selection,
        "attempts": selection_attempts,
    })

    labels = _labels()
    sections: list[dict[str, Any]] = []
    outcomes: dict[str, Any] = {}
    for index, issue in enumerate(selection["issues"], 1):
        issue_id = f"issue_{index:02d}"
        unit_id = str(issue["unit_id"])
        if unit_id == "unsupported":
            prose_request = {
                "사건과 질문": scoped,
                "답변 대상": issue["subject"],
                "검토 쟁점": issue["issue_label"],
                "관련 행위": issue["conduct"],
                "결론 처리": "일반 법률지식에 따라 잠정 결론을 직접 제시",
            }
            prose = _write_section(client=client, payload=prose_request)
            sections.append({
                "heading": f"{issue['subject']} — {issue['issue_label']}",
                "prose": prose,
                "conclusion": None,
                "authority": "model_only",
            })
            _write_json(case_dir / f"03_{issue_id}_writing.json", {
                "request": prose_request, "output": prose
            })
            outcomes[issue_id] = {"status": "model_only", "unit_id": unit_id}
            continue

        profile = profiles[unit_id]
        analysis_request = {
            "case_id": case_id,
            "issue_id": issue_id,
            "question_text": scoped,
            "question_prompt": question_prompt,
            "issue": issue,
            "role_contract": profile["role_contract"],
            "tracks": [
                {
                    "track_id": track["track_id"],
                    "components": [
                        component
                        for path in track["paths"]
                        for component in path["components"]
                    ],
                }
                for track in profile["tracks"]
            ],
            "predicates": _predicate_contract(profile),
        }
        analysis, analysis_attempts = _call(
            client=client,
            stage="analysis",
            payload=analysis_request,
            schema=core_unit_analysis_schema(
                case_id=case_id, issue_id=issue_id, profile=profile
            ),
            max_tokens=16384,
            validator=lambda output, p=profile, i=issue_id: validate_core_unit_analysis(
                output, case_id=case_id, issue_id=i, profile=p
            ),
        )
        _write_json(case_dir / f"01_{issue_id}_{unit_id}_analysis.json", {
            "request": analysis_request,
            "output": analysis,
            "attempts": analysis_attempts,
        })

        selected_tracks = [str(item) for item in analysis["selected_tracks"]]
        needed = needed_predicate_ids(profile, selected_tracks)
        runtime = execute_core_unit(
            profile=profile,
            case_id=case_id,
            role_values={"case_id": case_id, **analysis["role_values"]},
            selected_tracks=selected_tracks,
            assessments={key: analysis["assessments"][key] for key in needed},
            work_dir=case_dir / "runtime" / issue_id,
        )
        _write_json(case_dir / f"02_{issue_id}_{unit_id}_runtime.json", runtime)
        outcomes[issue_id] = runtime["track_outcomes"]

        for track_id in selected_tracks:
            status = runtime["track_outcomes"][track_id]["symbolic_conclusion"]
            conclusion = _conclusion_label(status)
            prose_request = {
                "사건과 질문": scoped,
                "답변 대상": issue["subject"],
                "검토 쟁점": issue["issue_label"],
                "관련 행위": issue["conduct"],
                "역할": analysis["role_values"],
                "법리와 사실 판단": _writer_predicates(
                    profile=profile, analysis=analysis, track_id=track_id
                ),
                "호스트가 고정한 결론": conclusion,
            }
            prose = _write_section(client=client, payload=prose_request)
            heading = f"{issue['subject']} — {labels.get(unit_id, issue['issue_label'])}"
            if len(profile["tracks"]) > 1:
                heading += f" — {track_id}"
            sections.append({
                "heading": heading,
                "prose": prose,
                "conclusion": conclusion,
                "authority": "rule_ir_scallop",
            })
            _write_json(case_dir / f"03_{issue_id}_{track_id}_writing.json", {
                "request": prose_request, "output": prose
            })

    markdown = _render_answer(case_id=case_id, sections=sections)
    (case_dir / "04_answer.md").write_text(markdown, encoding="utf-8")
    _write_json(case_dir / "04_answer.json", {
        "case_id": case_id, "sections": sections, "markdown": markdown
    })
    summary = {
        "case_id": case_id,
        "selected_issues": len(selection["issues"]),
        "sections": len(sections),
        "outcomes": outcomes,
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
        try:
            summaries.append(run_case(
                case=inventory[case_id], profiles=profiles, client=client,
                case_dir=args.out_dir / case_id,
            ))
        except CoreStageCallError as error:
            failure = {
                "case_id": case_id,
                "status": "contract_failure",
                "failed_stage": error.stage,
                "error": str(error),
                "attempts": error.attempts,
            }
            _write_json(args.out_dir / case_id / f"00_{error.stage}_failure.json", failure)
            summaries.append(failure)
    report = {
        "version": "1.0.0",
        "pipeline": "rule_ir_core_lean",
        "status": (
            "pass" if all(item.get("status") != "contract_failure" for item in summaries)
            else "contract_failure"
        ),
        "prompt_audit": audit,
        "cases": summaries,
    }
    _write_json(args.out_dir / "report.json", report)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
