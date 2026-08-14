#!/usr/bin/env python3
"""Build the Call 3 answer plans from the canonical symbolic artifacts.

No model is called here and no legal judgment is made.  The script reads the finished run
and rearranges it, so it can be re-run at any time without spending anything.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import yaml

from idpr.v2.registry import load_definitions
from idpr.v2.runtime.answer_plan import (
    AnswerPlanError,
    ContestedPoint,
    RuleStatement,
    build_answer_plan,
    serialize_analysis,
    serialize_open_points,
    serialize_required_authorities,
    serialize_required_final_conclusions,
)


def _rows(path: Path, key: str = "sub_question_id") -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        out[str(row[key])] = row
    return out


def _inventory(path: Path) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        out[str(row["sub_question_id"])] = row
    return out


def _representation_gaps(path: Path) -> list[str]:
    """Authored gaps, stated as the areas the analysis does not cover."""
    if not path.exists():
        return []
    document = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    gaps = document.get("gaps") or document.get("representation_gaps") or []
    out: list[str] = []
    for gap in gaps:
        if isinstance(gap, str):
            out.append(gap)
        elif isinstance(gap, dict):
            text = gap.get("description") or gap.get("summary") or gap.get("id")
            if text:
                out.append(str(text))
    return out


def _card_rule_statements(
    path: Path | None,
) -> dict[str, dict[tuple[str, str], tuple[RuleStatement, ...]]]:
    """Load the SPEC 5.5 retrieval, keyed per case on `(instance ref, predicate ref)`.

    Only ``reviewed_card`` statements are accepted here.  The authored precedent refs are
    projected from the predicate dictionary inside the builder and are present in both
    conditions, so letting a second origin in through this file would blur which of the two
    P-N actually measures.
    """
    if path is None:
        return {}
    out: dict[str, dict[tuple[str, str], tuple[RuleStatement, ...]]] = {}
    for row in path.read_text(encoding="utf-8").splitlines():
        if not row.strip():
            continue
        record = json.loads(row)
        case = out.setdefault(str(record["sub_question_id"]), {})
        for entry in record.get("rule_statements") or []:
            key = (str(entry["instance_ref"]), str(entry["predicate_ref"]))
            case[key] = case.get(key, ()) + tuple(
                RuleStatement(
                    statement=str(statement["statement"]),
                    origin=str(statement["origin"]),
                    source_id=str(statement["source_id"]),
                )
                for statement in entry.get("statements") or []
                if str(statement.get("origin")) == "reviewed_card"
            )
    return out


def _dispute_registry(path: Path) -> dict[str, ContestedPoint]:
    document = json.loads(path.read_text(encoding="utf-8"))
    output: dict[str, ContestedPoint] = {}
    for row in document.get("disputes") or ():
        trigger = str(row["trigger_card_id"])
        if trigger in output:
            raise ValueError(f"duplicate dispute trigger card: {trigger}")
        output[trigger] = ContestedPoint(
            label=str(row["label"]),
            positions=tuple(str(value) for value in row["positions"]),
            adopted=str(row["adopted"]),
            why_adopted=str(row["why_adopted"]),
            origin=str(row["origin"]),
            source_id=str(row["dispute_id"]),
        )
    return output


def _case_contested_points(
    statements: dict[tuple[str, str], tuple[RuleStatement, ...]],
    registry: dict[str, ContestedPoint],
) -> dict[str, tuple[ContestedPoint, ...]]:
    output: dict[str, list[ContestedPoint]] = {}
    seen: set[tuple[str, str]] = set()
    for (instance_ref, _predicate_ref), values in statements.items():
        for statement in values:
            point = registry.get(statement.source_id)
            if point is None or (instance_ref, point.source_id) in seen:
                continue
            seen.add((instance_ref, point.source_id))
            output.setdefault(instance_ref, []).append(point)
    return {key: tuple(value) for key, value in output.items()}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--e2e-results", type=Path, required=True)
    parser.add_argument("--call2-artifact", type=Path, required=True)
    parser.add_argument("--issue-bindings", type=Path, required=True)
    parser.add_argument(
        "--plan-artifact",
        type=Path,
        help=(
            "Step 8 planner JSONL; extends the GroundFact conflict guard's episode "
            "identity to derived bindings absent from --issue-bindings"
        ),
    )
    parser.add_argument(
        "--inventory", type=Path, default=ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl"
    )
    parser.add_argument("--definitions", type=Path, default=ROOT / "data/v2/definitions")
    parser.add_argument(
        "--representation-gaps", type=Path, default=ROOT / "data/v2/representation_gaps.yaml"
    )
    parser.add_argument(
        "--dispute-registry",
        type=Path,
        default=ROOT / "data/v2/dispute_registry.json",
    )
    parser.add_argument(
        "--expose-global-representation-gaps",
        action="store_true",
        help=(
            "Diagnostic only: copy repository-wide engineering gaps into every case plan. "
            "Production leaves these out unless a later case-scoped route proves applicability."
        ),
    )
    parser.add_argument(
        "--offense-labels",
        type=Path,
        default=ROOT / "data/v2/binding_seed_cues.yaml",
        help="reviewed catalogue carrying the Korean name of each offence",
    )
    parser.add_argument(
        "--rule-statements",
        type=Path,
        help=(
            "SPEC 5.5 card retrieval artifact from build_v2_card_rule_statements.py.  "
            "Its absence is the N condition; its presence is P.  It can only add to "
            "rule_statements[] -- no truth, state or conclusion derives from it (SPEC 4-10)"
        ),
    )
    parser.add_argument(
        "--dispute-triggers",
        type=Path,
        help=(
            "The same reviewed retrieval artifact for both N and P, used only to open "
            "authored dispute obligations. It never adds rule_statements."
        ),
    )
    parser.add_argument("--case-id-file", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    registry = load_definitions(args.definitions)
    e2e = _rows(args.e2e_results)
    call2 = _rows(args.call2_artifact)
    bindings = _rows(args.issue_bindings)
    plans = _rows(args.plan_artifact) if args.plan_artifact else {}
    inventory = _inventory(args.inventory)
    global_gaps = _representation_gaps(args.representation_gaps)
    gaps = global_gaps if args.expose_global_representation_gaps else ()
    card_statements = _card_rule_statements(args.rule_statements)
    dispute_trigger_statements = _card_rule_statements(
        args.dispute_triggers or args.rule_statements
    )
    dispute_registry = _dispute_registry(args.dispute_registry)
    cue_catalogue = yaml.safe_load(args.offense_labels.read_text(encoding="utf-8")) or {}
    offense_labels = {
        ref: str(entry["display_name"])
        for ref, entry in cue_catalogue.items()
        if isinstance(entry, dict) and entry.get("display_name")
    }

    case_ids = sorted(e2e)
    if args.case_id_file:
        wanted = {
            line.strip()
            for line in args.case_id_file.read_text(encoding="utf-8").splitlines()
            if line.strip()
        }
        case_ids = [case_id for case_id in case_ids if case_id in wanted]

    args.out.mkdir(parents=True, exist_ok=True)
    written = 0
    failures: list[tuple[str, str]] = []
    with (args.out / "answer_plans.jsonl").open("w", encoding="utf-8") as handle:
        for case_id in case_ids:
            question = inventory.get(case_id, {})
            case_statements = card_statements.get(case_id, {})
            case_dispute_triggers = dispute_trigger_statements.get(case_id, {})
            try:
                plan = build_answer_plan(
                    case_id=case_id,
                    case_text=str(question.get("question_text", "")),
                    question=str(question.get("question_prompt", "")),
                    binding_row=bindings.get(case_id, {}),
                    call2_row=call2.get(case_id, {}),
                    e2e_row=e2e[case_id],
                    registry=registry,
                    offense_labels=offense_labels,
                    representation_gaps=gaps,
                    rule_statements=case_statements,
                    contested_points=_case_contested_points(
                        case_dispute_triggers, dispute_registry
                    ),
                    plan_row=plans.get(case_id),
                )
                analysis = serialize_analysis(plan)
                open_points = serialize_open_points(plan)
                required_authorities = serialize_required_authorities(plan)
                required_final_conclusions = serialize_required_final_conclusions(plan)
            except AnswerPlanError as error:
                failures.append((case_id, str(error)))
                continue
            handle.write(
                json.dumps(
                    {
                        "sub_question_id": case_id,
                        "case_text": plan.case_text,
                        "question": plan.question,
                        "analysis": analysis,
                        "open_points": open_points,
                        "required_authorities": required_authorities,
                        "required_authority_count": (
                            0 if required_authorities == "없음" else len(required_authorities.splitlines())
                        ),
                        "required_final_conclusions": required_final_conclusions,
                        "anchored_issue_count": len(plan.anchored_issues),
                        "required_final_conclusion_count": len(plan.required_final_conclusions),
                        "retained_offense_count": len(plan.final_responsibility.retained),
                        "contested_point_count": sum(
                            len(issue.contested_points) for issue in plan.anchored_issues
                        ),
                        "absorbed_pair_count": len(plan.final_responsibility.absorbed),
                    },
                    ensure_ascii=False,
                )
                + "\n"
            )
            written += 1

    manifest = {
        "e2e_results": str(args.e2e_results),
        "call2_artifact": str(args.call2_artifact),
        "issue_bindings": str(args.issue_bindings),
        "plan_artifact": str(args.plan_artifact) if args.plan_artifact else None,
        "cases_requested": len(case_ids),
        "cases_written": written,
        "failures": [{"case_id": case_id, "error": error} for case_id, error in failures],
        "global_representation_gap_count": len(global_gaps),
        "global_representation_gaps_exposed_to_writer": bool(
            args.expose_global_representation_gaps
        ),
        "dispute_registry": str(args.dispute_registry),
        "dispute_registry_entry_count": len(dispute_registry),
        "dispute_triggers": str(args.dispute_triggers or args.rule_statements),
        "gold_precedents_read": False,
        "rubric_fields_read": False,
    }
    (args.out / "answer_plans.manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    if failures:
        sys.exit(1)


if __name__ == "__main__":
    main()
