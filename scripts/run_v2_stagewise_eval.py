#!/usr/bin/env python3
"""Run offline stagewise audits over an already frozen v2 artifact set."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

DEFAULT_DEFINITIONS = ROOT / "data/v2/definitions"
DEFAULT_DEFINITION_GOLD = ROOT / "data/eval/v2_call1_definition_gold_draft.json"
DEFAULT_GOLD_OCCURRENCES = ROOT / "data/v2/gold_occurrences.jsonl"
DEFAULT_PARTIAL_GOLD = ROOT / "data/eval/v2_call2_decisive_predicate_partial_gold.jsonl"
DEFAULT_INVENTORY = ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _rate(numerator: int, denominator: int) -> float | None:
    return numerator / denominator if denominator else None


def _run(command: list[str], *, dry_run: bool) -> None:
    print("$ " + " ".join(command))
    if not dry_run:
        subprocess.run(command, cwd=ROOT, check=True)


def _require_pair(
    parser: argparse.ArgumentParser,
    left: Path | None,
    right: Path | None,
    names: str,
) -> None:
    if (left is None) != (right is None):
        parser.error(f"{names} must be supplied together")


def _symbolic_summary(path: Path) -> dict[str, Any]:
    rows = _load_jsonl(path)
    status_counts = Counter(str(row.get("execution_status", "MISSING")) for row in rows)
    final_views = [row.get("final_responsibility") for row in rows]
    populated = [value for value in final_views if isinstance(value, dict)]
    return {
        "case_count": len(rows),
        "execution_status_counts": dict(sorted(status_counts.items())),
        "cases_with_final_responsibility": len(populated),
        "established_instance_count": sum(
            int(value.get("established_instance_count", 0)) for value in populated
        ),
        "final_instance_count": sum(len(value.get("final_instances", ())) for value in populated),
        "unresolved_finding_count": sum(
            len(value.get("unresolved_findings", ())) for value in populated
        ),
        "unresolved_concurrence_candidate_count": sum(
            len(value.get("unresolved_concurrence_candidates", ())) for value in populated
        ),
        "metric_scope": (
            "execution/typed-result diagnostics only; this is not symbolic conclusion accuracy "
            "without independent structured conclusion gold"
        ),
    }


def _render_summary(summary: dict[str, Any]) -> str:
    lines = [
        "# V2 Stagewise Evaluation Summary",
        "",
        "This report scores frozen artifacts only. It does not invoke a model.",
        "",
        "| Stage | Primary diagnostic | Value | Scope |",
        "|---|---|---:|---|",
    ]
    call1 = summary.get("call1")
    if call1:
        value = call1.get("closure_survival_rate")
        rendered = "—" if value is None else f"{100 * value:.1f}%"
        lines.append(
            f"| Call 1 | Closed-catalog DefinitionRef recall after closure | {rendered} | approved in-scope DefinitionRef gold |"
        )
    call15 = summary.get("call15")
    if call15:
        metric = call15.get("explicit_gold_seed_binding_recall", {})
        value = metric.get("rate")
        rendered = "—" if value is None else f"{100 * value:.1f}%"
        lines.append(
            f"| Call 1.5 | Explicit-gold-seed binding recall | {rendered} | factual binding; host-derived coverage reported separately |"
        )
    call2 = summary.get("call2")
    if call2:
        value = call2.get("strict_match_rate")
        rendered = "—" if value is None else f"{100 * value:.1f}%"
        lines.append(
            f"| Call 2 | Exact truth match | {rendered} | reviewed decisive-predicate partial gold only |"
        )
    symbolic = summary.get("symbolic")
    if symbolic:
        succeeded = symbolic.get("execution_status_counts", {}).get("SUCCEEDED", 0)
        total = int(symbolic.get("case_count", 0))
        rendered = "—" if not total else f"{succeeded}/{total}"
        lines.append(
            f"| Symbolic runtime | Successful execution | {rendered} | execution diagnostic, not legal-conclusion accuracy |"
        )
    call3 = summary.get("call3")
    if call3:
        value = call3.get("final_conclusion_completeness_rate")
        rendered = "—" if value is None else f"{100 * value:.1f}%"
        lines.append(
            f"| Call 3 | Required-final-conclusion completeness | {rendered} | AnswerPlan faithfulness, separate from KCL rubric quality |"
        )
    lines.append("")
    lines.append(
        "KCL end-task rubric scores belong in the main comparison table and are intentionally not folded into these stagewise diagnostics."
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--call1", type=Path)
    parser.add_argument("--call15", type=Path)
    parser.add_argument("--plan", type=Path)
    parser.add_argument("--call2", type=Path)
    parser.add_argument("--scallop", type=Path)
    parser.add_argument("--answer-plans", type=Path)
    parser.add_argument("--answers", type=Path)
    parser.add_argument("--definitions", type=Path, default=DEFAULT_DEFINITIONS)
    parser.add_argument("--definition-gold", type=Path, default=DEFAULT_DEFINITION_GOLD)
    parser.add_argument("--gold-occurrences", type=Path, default=DEFAULT_GOLD_OCCURRENCES)
    parser.add_argument("--partial-gold", type=Path, default=DEFAULT_PARTIAL_GOLD)
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    _require_pair(parser, args.call1, args.call15, "--call1 and --call15")
    _require_pair(parser, args.answer_plans, args.answers, "--answer-plans and --answers")
    if args.call2 is not None and (args.plan is None or args.call15 is None):
        parser.error("--call2 requires --plan and --call15 for the binding-scoped partial-gold audit")

    selected = {
        "call1": args.call1,
        "call15": args.call15,
        "plan": args.plan,
        "call2": args.call2,
        "scallop": args.scallop,
        "answer_plans": args.answer_plans,
        "answers": args.answers,
    }
    if not any(value is not None for value in selected.values()):
        parser.error("at least one stage artifact must be supplied")

    static_inputs = {
        "definitions": args.definitions,
        "definition_gold": args.definition_gold,
        "gold_occurrences": args.gold_occurrences,
        "partial_gold": args.partial_gold,
        "inventory": args.inventory,
    }
    for label, path in {**selected, **static_inputs}.items():
        if path is not None and not path.exists():
            parser.error(f"{label} does not exist: {path}")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "step": "v2_stagewise_offline_evaluation",
        "model_calls": 0,
        "dry_run": args.dry_run,
        "artifacts": {
            label: {"path": str(path), "sha256": _sha256(path)}
            for label, path in selected.items()
            if path is not None
        },
        "supervision": {
            label: {"path": str(path), "sha256": _sha256(path)}
            for label, path in static_inputs.items()
            if path.is_file()
        },
    }
    (args.out_dir / "stagewise_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    python = sys.executable
    if args.call1 is not None:
        _run(
            [
                python,
                "scripts/report_v2_call1_pilot.py",
                "--artifact",
                str(args.call1),
                "--definitions-dir",
                str(args.definitions),
                "--definition-gold",
                str(args.definition_gold),
                "--out",
                str(args.out_dir / "call1_report.json"),
            ],
            dry_run=args.dry_run,
        )
        _run(
            [
                python,
                "scripts/audit_v2_call1_pilot.py",
                "--report",
                str(args.out_dir / "call1_report.json"),
                "--definitions-dir",
                str(args.definitions),
                "--out",
                str(args.out_dir / "call1_audit.json"),
            ],
            dry_run=args.dry_run,
        )

    if args.call15 is not None:
        _run(
            [
                python,
                "scripts/audit_v2_call15_bindings.py",
                "--bindings",
                str(args.call15),
                "--call1",
                str(args.call1),
                "--inventory",
                str(args.inventory),
                "--occurrences",
                str(args.gold_occurrences),
                "--definition-gold",
                str(args.definition_gold),
                "--definitions",
                str(args.definitions),
                "--json-out",
                str(args.out_dir / "call15_audit.json"),
                "--markdown-out",
                str(args.out_dir / "call15_audit.md"),
            ],
            dry_run=args.dry_run,
        )

    if args.call2 is not None:
        _run(
            [
                python,
                "scripts/audit_v2_call2_decisive_partial_gold.py",
                "--partial-gold",
                str(args.partial_gold),
                "--call2",
                str(args.call2),
                "--plan-artifact",
                str(args.plan),
                "--call15-artifact",
                str(args.call15),
                "--inventory",
                str(args.inventory),
                "--gold-occurrences",
                str(args.gold_occurrences),
                "--out",
                str(args.out_dir / "call2_partial_gold_audit.json"),
            ],
            dry_run=args.dry_run,
        )

    if args.answer_plans is not None:
        _run(
            [
                python,
                "scripts/audit_v2_call3_conclusion_completeness.py",
                "--answers",
                str(args.answers),
                "--answer-plans",
                str(args.answer_plans),
                "--out",
                str(args.out_dir / "call3_conclusion_completeness.json"),
            ],
            dry_run=args.dry_run,
        )
        _run(
            [
                python,
                "scripts/audit_v2_call3_conclusion_state.py",
                "--answers",
                str(args.answers),
                "--answer-plans",
                str(args.answer_plans),
                "--out",
                str(args.out_dir / "call3_conclusion_state.json"),
            ],
            dry_run=args.dry_run,
        )

    if args.dry_run:
        print(f"wrote {args.out_dir / 'stagewise_manifest.json'}")
        return

    summary: dict[str, Any] = {
        "step": "v2_stagewise_offline_evaluation_summary",
        "model_calls": 0,
    }
    call1_report = args.out_dir / "call1_report.json"
    if call1_report.exists():
        report = _load_json(call1_report)
        summary["call1"] = {
            **report["summary"],
            "metric_scope": report["metric_contract"],
        }
    call15_report = args.out_dir / "call15_audit.json"
    if call15_report.exists():
        summary["call15"] = _load_json(call15_report)["aggregate"]
    call2_report = args.out_dir / "call2_partial_gold_audit.json"
    if call2_report.exists():
        report = _load_json(call2_report)
        counts = report["summary"]["classification_counts"]
        count = int(report["summary"]["annotation_count"])
        summary["call2"] = {
            **report["summary"],
            "strict_match_rate": _rate(int(counts.get("MATCH", 0)), count),
            "metric_scope": report["scope"],
        }
    if args.scallop is not None:
        summary["symbolic"] = _symbolic_summary(args.scallop)
    completeness_path = args.out_dir / "call3_conclusion_completeness.json"
    state_path = args.out_dir / "call3_conclusion_state.json"
    if completeness_path.exists() and state_path.exists():
        completeness = _load_json(completeness_path)["summary"]
        state = _load_json(state_path)["summary"]
        total_required = int(completeness["total_required"])
        total_missing = int(completeness["total_missing"])
        anchors = int(state["anchors"])
        agrees = int(state["agrees"])
        summary["call3"] = {
            "required_final_conclusion_count": total_required,
            "missing_final_conclusion_count": total_missing,
            "final_conclusion_completeness_rate": _rate(
                total_required - total_missing, total_required
            ),
            "state_anchor_count": anchors,
            "state_agreement_count": agrees,
            "strict_state_agreement_rate": _rate(agrees, anchors),
            "state_verdict_counts": {
                key: int(state[key])
                for key in ("agrees", "diverges", "ambiguous", "unmatched")
            },
            "metric_scope": (
                "AnswerPlan-to-text final-conclusion faithfulness diagnostic; lexical state "
                "audit flags ambiguity/unmatched anchors and is not KCL end-task quality"
            ),
        }

    summary_path = args.out_dir / "stagewise_summary.json"
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    markdown_path = args.out_dir / "stagewise_summary.md"
    markdown_path.write_text(_render_summary(summary), encoding="utf-8")
    print(f"wrote {summary_path}")
    print(f"wrote {markdown_path}")


if __name__ == "__main__":
    main()
