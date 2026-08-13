#!/usr/bin/env python3
"""Build a read-only rubric-supervised debugging packet for the V2 vertical slice.

This does not infer predicate gold from final rubric conclusions.  It only joins the
evidence needed for a human to localize failures across Call 2, participation, Scallop,
and the Call 3 handoff.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

CONCLUSION_MARKERS = (
    "결론",
    "죄책을 진",
    "성립한다",
    "성립하지",
    "인정된다",
    "인정되지",
    "무죄",
    "불성립",
)
INTERNAL_MARKERS = (
    "occurrence_id",
    "elements_state",
    "offense_ref",
    "liability_established",
    "symbolic_conclusions",
    "gocc:",
)


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def _index(path: Path) -> dict[str, dict[str, Any]]:
    values = _jsonl(path)
    output = {str(value["sub_question_id"]): value for value in values}
    if len(output) != len(values):
        raise ValueError(f"{path}: duplicate sub_question_id")
    return output


def _state(result: dict[str, Any]) -> str:
    if result.get("liability_result") is not None:
        return "ESTABLISHED"
    stage = result.get("decisive_stage")
    if stage == "completion":
        completion = result.get("completion")
        return f"COMPLETION_{str((completion or {}).get('state', 'NONE')).upper()}"
    if stage:
        value = result.get(stage) or {}
        gate = value.get("gate_state") or value.get("legal_state") or "UNKNOWN"
        return f"{str(stage).upper()}_{str(gate).upper()}"
    return "NO_LIABILITY_RESULT"


def _conclusion_atoms(items: list[str]) -> list[dict[str, Any]]:
    return [
        {"rubric_index": index, "text": text}
        for index, text in enumerate(items, 1)
        if any(marker in text for marker in CONCLUSION_MARKERS)
    ]


def _participation_true(row: dict[str, Any]) -> list[dict[str, Any]]:
    output = []
    for value in row["participation_local_assessments"]:
        if value["truth"] != "TRUE":
            continue
        output.append(
            {
                "relation_kind": value["relation_kind"],
                "offense_ref": value["group_key"]["offense_ref"],
                "members": [
                    {
                        "actor_id": member["actor_id"],
                        "occurrence_id": member["occurrence_id"],
                    }
                    for member in value["member_instances"]
                ],
            }
        )
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--definition-gold", type=Path, required=True)
    parser.add_argument("--call2", type=Path, required=True)
    parser.add_argument("--scallop", type=Path, required=True)
    parser.add_argument("--call3", type=Path, required=True)
    parser.add_argument("--json-out", type=Path, required=True)
    parser.add_argument("--markdown-out", type=Path, required=True)
    args = parser.parse_args()

    inventory = _index(args.inventory)
    call2 = _index(args.call2)
    scallop = _index(args.scallop)
    call3 = _index(args.call3)
    raw_gold = json.loads(args.definition_gold.read_text(encoding="utf-8"))
    gold = {str(value["case_id"]): value for value in raw_gold["cases"]}
    case_ids = tuple(call2)
    if tuple(scallop) != case_ids:
        raise ValueError("Call 2 and Scallop case order/universe differ")
    if any(case_id not in inventory or case_id not in gold for case_id in case_ids):
        raise ValueError("rubric supervision source is missing a Call 2 case")

    cases = []
    aggregate_truths: Counter[str] = Counter()
    aggregate_states: Counter[str] = Counter()
    gold_ref_reachability: Counter[str] = Counter()
    participation_true_counts: Counter[str] = Counter()
    article263_pair_count = 0
    active_doctrine_count = 0
    for case_id in case_ids:
        source = inventory[case_id]
        grounding = call2[case_id]
        symbolic = scallop[case_id]
        gold_refs = tuple(str(value) for value in gold[case_id]["gold_definition_refs"])
        top_level_refs = {
            str(value["offense_ref"]) for value in grounding["top_level_instances"]
        }
        assessment_refs = {
            str(value["offense_ref"]) for value in grounding["assessment_instances"]
        }
        truths_by_ref: dict[str, Counter[str]] = defaultdict(Counter)
        predicates_by_ref: dict[str, dict[str, list[str]]] = defaultdict(
            lambda: defaultdict(list)
        )
        for value in grounding["case_truths"]:
            ref = str(value["instance_key"]["offense_ref"])
            truth = str(value["truth"])
            truths_by_ref[ref][truth] += 1
            aggregate_truths[truth] += 1
            if ref in gold_refs and truth != "UNKNOWN":
                predicates_by_ref[ref][truth].append(str(value["predicate_ref"]))

        symbolic_rows = []
        established_refs = set()
        for value in symbolic["liability_results"]:
            key = value["instance_key"]
            result = value["result"]
            state = _state(result)
            aggregate_states[state] += 1
            if state == "ESTABLISHED":
                established_refs.add(str(key["offense_ref"]))
            symbolic_rows.append(
                {
                    "actor_id": key["actor_id"],
                    "offense_ref": key["offense_ref"],
                    "occurrence_id": key["occurrence_id"],
                    "state": state,
                    "decisive_stage": result.get("decisive_stage"),
                    "completion_state": (
                        result["completion"].get("state")
                        if result.get("completion") is not None
                        else None
                    ),
                }
            )

        reachability = []
        for ref in gold_refs:
            planned = ref in top_level_refs
            assessed = ref in assessment_refs
            established = ref in established_refs
            gold_ref_reachability["total"] += 1
            gold_ref_reachability["planned"] += int(planned)
            gold_ref_reachability["assessed"] += int(assessed)
            gold_ref_reachability["established"] += int(established)
            reachability.append(
                {
                    "offense_ref": ref,
                    "planned_top_level": planned,
                    "assessment_reachable": assessed,
                    "truth_counts": dict(truths_by_ref[ref]),
                    "non_unknown_predicates": {
                        truth: sorted(set(values))
                        for truth, values in predicates_by_ref[ref].items()
                    },
                    "established": established,
                }
            )

        true_relations = _participation_true(grounding)
        for value in true_relations:
            participation_true_counts[value["relation_kind"]] += 1
        answer = call3.get(case_id)
        answer_text = str((answer or {}).get("answer_markdown", ""))
        article263 = list(grounding.get("article263_assessments", []))
        article263_pair_count += len(article263)
        active_doctrine_count += len(symbolic.get("active_doctrines", []))
        cases.append(
            {
                "sub_question_id": case_id,
                "question_prompt": source.get("question_prompt", ""),
                "rubric_count": len(source.get("rubric_summary", [])),
                "rubric_conclusion_atoms": _conclusion_atoms(
                    list(source.get("rubric_summary", []))
                ),
                "gold_definition_refs": list(gold_refs),
                "gold_scope_notes": list(gold[case_id].get("scope_notes", [])),
                "gold_ref_reachability": reachability,
                "call2_truth_counts": dict(
                    Counter(value["truth"] for value in grounding["case_truths"])
                ),
                "participation_compile_status": grounding[
                    "participation_compile_status"
                ],
                "participation_compile_errors": list(
                    grounding.get("participation_compile_errors", [])
                ),
                "participation_true": true_relations,
                "article263_assessments": article263,
                "scallop_execution_status": symbolic["execution_status"],
                "active_doctrines": list(symbolic.get("active_doctrines", [])),
                "symbolic_results": symbolic_rows,
                "call3_generated": answer is not None,
                "call3_internal_markers": [
                    marker for marker in INTERNAL_MARKERS if marker in answer_text
                ],
            }
        )

    aggregate = {
        "case_count": len(case_ids),
        "rubric_atom_count": sum(value["rubric_count"] for value in cases),
        "rubric_conclusion_atom_count": sum(
            len(value["rubric_conclusion_atoms"]) for value in cases
        ),
        "call2_truth_counts": dict(aggregate_truths),
        "participation_status_counts": dict(
            Counter(value["participation_compile_status"] for value in cases)
        ),
        "participation_true_counts": dict(participation_true_counts),
        "article263_pair_count": article263_pair_count,
        "scallop_state_counts": dict(aggregate_states),
        "active_doctrine_count": active_doctrine_count,
        "gold_ref_reachability": dict(gold_ref_reachability),
        "call3_generated_case_count": sum(value["call3_generated"] for value in cases),
        "call3_internal_marker_case_count": sum(
            bool(value["call3_internal_markers"]) for value in cases
        ),
    }
    payload = {
        "scope": {
            "kind": "rubric_supervised_failure_debug_packet",
            "warning": (
                "Rubric conclusions are not predicate gold. Non-UNKNOWN predicate lists "
                "are evidence for human failure localization only."
            ),
        },
        "aggregate": aggregate,
        "cases": cases,
    }
    args.json_out.parent.mkdir(parents=True, exist_ok=True)
    args.json_out.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    lines = [
        "# V2 rubric-supervised failure debug packet",
        "",
        "> Rubric conclusions are not predicate gold. This packet joins evidence for human debugging; it does not infer all leaf truths from final answers.",
        "",
        f"- Cases: {aggregate['case_count']}",
        f"- Rubric atoms: {aggregate['rubric_atom_count']}",
        f"- Conclusion-like rubric atoms: {aggregate['rubric_conclusion_atom_count']}",
        f"- Call 2 truths: {aggregate['call2_truth_counts']}",
        f"- Participation status: {aggregate['participation_status_counts']}",
        f"- Article 263 assessed pairs: {aggregate['article263_pair_count']}",
        f"- Scallop states: {aggregate['scallop_state_counts']}",
        f"- Active doctrine rows: {aggregate['active_doctrine_count']}",
        f"- Gold ref reachability: {aggregate['gold_ref_reachability']}",
        "",
        "| case | rubric conclusions | gold refs planned/total | participation | Scallop established | Call 3 |",
        "|---|---:|---:|---|---:|---|",
    ]
    for value in cases:
        planned = sum(
            item["planned_top_level"] for item in value["gold_ref_reachability"]
        )
        total = len(value["gold_ref_reachability"])
        established = sum(
            item["state"] == "ESTABLISHED" for item in value["symbolic_results"]
        )
        call3_status = "generated" if value["call3_generated"] else "skipped"
        if value["call3_internal_markers"]:
            call3_status += ":internal-marker"
        lines.append(
            f"| `{value['sub_question_id']}` | "
            f"{len(value['rubric_conclusion_atoms'])} | {planned}/{total} | "
            f"{value['participation_compile_status']} | {established} | {call3_status} |"
        )
    args.markdown_out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(aggregate, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
