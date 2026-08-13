#!/usr/bin/env python3
"""Audit reviewed decisive-predicate partial gold against a Call 2 artifact.

The annotations are deliberately sparse.  Final rubric conclusions are not expanded into
leaf gold; every row must carry its own quoted evidence and evidence-carrier ownership.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _instance_key(value: dict[str, Any]) -> tuple[str, str, str, str]:
    return (
        str(value["case_id"]),
        str(value["actor_id"]),
        str(value["offense_ref"]),
        str(value["occurrence_id"]),
    )


def _observed_predicates(row: dict[str, Any]) -> dict[tuple[tuple[str, str, str, str], str], str]:
    return {
        (_instance_key(value["instance_key"]), str(value["predicate_ref"])): str(value["truth"])
        for value in row["case_truths"]
    }


def _observed_article263(row: dict[str, Any]) -> dict[tuple[str, str], str]:
    output: dict[tuple[str, str], str] = {}
    for assessment in row.get("article263_assessments", []):
        pair_id = str(assessment["pair"]["pair_id"])
        for value in assessment.get("statutory_truths", assessment.get("truths", [])):
            output[(pair_id, str(value["predicate_ref"]))] = str(value["truth"])
    return output


def _classification(annotation: dict[str, Any], row: dict[str, Any], observed: str | None) -> str:
    if observed is None:
        return "TARGET_MISSING"
    if annotation["evidence_carrier"] == "QUESTION_ASSUMPTION" and int(
        row.get("question_assumption_count", 0)
    ) == 0:
        return "EVIDENCE_SCOPE_MISSING"
    if observed == annotation["expected_truth"]:
        return "MATCH"
    if observed == "UNKNOWN":
        return "MODEL_UNDERCALL"
    return "MODEL_SEMANTIC_ERROR"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--partial-gold", type=Path, required=True)
    parser.add_argument("--call2", type=Path, required=True)
    parser.add_argument("--call2-manifest", type=Path)
    parser.add_argument(
        "--plan-artifact",
        type=Path,
        help="binding-scoped planner artifact used to map reviewed evidence to binding identities",
    )
    parser.add_argument(
        "--call15-artifact",
        type=Path,
        help="validated binding artifact supplying source spans for offline identity mapping",
    )
    parser.add_argument(
        "--inventory",
        type=Path,
        default=ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl",
    )
    parser.add_argument(
        "--gold-occurrences",
        type=Path,
        default=ROOT / "data/v2/gold_occurrences.jsonl",
    )
    parser.add_argument(
        "--question-assumptions",
        type=Path,
        default=ROOT / "data/v2/question_assumptions.jsonl",
    )
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    manifest_path = args.call2_manifest or args.call2.with_name(
        args.call2.name.removesuffix(".jsonl") + ".manifest.json"
    )
    if not manifest_path.exists():
        raise ValueError(f"Call 2 manifest not found: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    binding_scoped = manifest.get("evidence_mode") == "binding_scoped_planner_occurrences"
    if binding_scoped:
        if args.plan_artifact is None or args.call15_artifact is None:
            raise ValueError(
                "binding-scoped Call 2 audit requires --plan-artifact and --call15-artifact"
            )
        if manifest.get("plan_artifact_sha256") != _sha256(args.plan_artifact):
            raise ValueError("Call 2 artifact used a different binding-scoped planner artifact")
    elif manifest.get("gold_occurrences_sha256") != _sha256(args.gold_occurrences):
        raise ValueError(
            "Call 2 artifact used a different GOLD occurrence revision; "
            "predicate ownership audit would compare evidence the model did not receive"
        )

    annotations = _jsonl(args.partial_gold)
    gold = {row["sub_question_id"]: row for row in _jsonl(args.gold_occurrences)}
    assumptions = {
        row["sub_question_id"]: row for row in _jsonl(args.question_assumptions)
    }
    for annotation in annotations:
        carrier = annotation["evidence_carrier"]
        case_id = annotation["sub_question_id"]
        if carrier == "LOCAL_OCCURRENCE":
            occurrence_id = annotation["instance_key"]["occurrence_id"]
            occurrence = next(
                (
                    value
                    for value in gold[case_id]["occurrences"]
                    if value["occurrence_id"] == occurrence_id
                ),
                None,
            )
            if occurrence is None or annotation["evidence_text"] not in occurrence["source_text"]:
                raise ValueError(
                    f"{annotation['annotation_id']}: evidence is absent from LOCAL_OCCURRENCE"
                )
        elif carrier == "QUESTION_ASSUMPTION":
            source_texts = {
                value["source_text"] for value in assumptions[case_id]["assumptions"]
            }
            if annotation["evidence_text"] not in source_texts:
                raise ValueError(
                    f"{annotation['annotation_id']}: evidence is absent from QUESTION_ASSUMPTION"
                )
    rows = {str(value["sub_question_id"]): value for value in _jsonl(args.call2)}
    if len(rows) != len(_jsonl(args.call2)):
        raise ValueError("Call 2 artifact contains duplicate sub_question_id")

    planned_occurrence_text: dict[tuple[str, str], str] = {}
    planned_occurrence_spans: dict[tuple[str, str], list[tuple[int, int]]] = {}
    if args.plan_artifact is not None:
        for plan_row in _jsonl(args.plan_artifact):
            case_id = str(plan_row["sub_question_id"])
            for occurrence in plan_row["occurrences"]:
                planned_occurrence_text[(case_id, str(occurrence["occurrence_id"]))] = str(
                    occurrence["source_text"]
                )
            for derived in plan_row.get("derived_binding_candidates", []):
                planned_occurrence_spans[(case_id, str(derived["binding_id"]))] = []

    if args.call15_artifact is not None:
        direct_spans: dict[tuple[str, str], list[tuple[int, int]]] = {}
        for binding_row in _jsonl(args.call15_artifact):
            case_id = str(binding_row["sub_question_id"])
            for seed_result in binding_row["seed_results"]:
                for binding in seed_result["bindings"]:
                    direct_spans[(case_id, str(binding["binding_id"]))] = [
                        (int(fragment["source_span"]["start"]), int(fragment["source_span"]["end"]))
                        for field in ("actor_action_fragments", "context_fragments")
                        for fragment in binding[field]
                    ]
        planned_occurrence_spans.update(direct_spans)
        if args.plan_artifact is not None:
            for plan_row in _jsonl(args.plan_artifact):
                case_id = str(plan_row["sub_question_id"])
                for derived in plan_row.get("derived_binding_candidates", []):
                    planned_occurrence_spans[(case_id, str(derived["binding_id"]))] = [
                        span
                        for source_id in derived["source_binding_ids"]
                        for span in direct_spans.get((case_id, str(source_id)), [])
                    ]

    inventory = {
        row["sub_question_id"]: row for row in _jsonl(args.inventory)
    }

    seen_ids: set[str] = set()
    results = []
    for annotation in annotations:
        annotation_id = str(annotation["annotation_id"])
        if annotation_id in seen_ids:
            raise ValueError(f"duplicate annotation_id: {annotation_id}")
        seen_ids.add(annotation_id)
        case_id = str(annotation["sub_question_id"])
        row = rows.get(case_id)
        if row is None:
            observed = None
            classification = "CASE_MISSING"
        elif annotation["target_kind"] == "predicate_instance":
            key = (_instance_key(annotation["instance_key"]), str(annotation["predicate_ref"]))
            observed_values = _observed_predicates(row)
            observed = observed_values.get(key)
            mapped_instance_key = None
            if observed is None and binding_scoped:
                original = annotation["instance_key"]
                candidates = [
                    (instance, truth)
                    for (instance, predicate_ref), truth in observed_values.items()
                    if predicate_ref == str(annotation["predicate_ref"])
                    and instance[0] == case_id
                    and instance[1] == str(original["actor_id"])
                    and instance[2] == str(original["offense_ref"])
                ]
                evidence_start = str(inventory[case_id]["question_text"]).find(
                    str(annotation["evidence_text"])
                )
                evidence_span = (
                    evidence_start,
                    evidence_start + len(str(annotation["evidence_text"])),
                )
                evidence_candidates = [
                    value
                    for value in candidates
                    if (
                        annotation["evidence_text"]
                        in planned_occurrence_text.get((case_id, value[0][3]), "")
                        or evidence_start >= 0
                        and any(
                            evidence_span[0] < span[1] and span[0] < evidence_span[1]
                            for span in planned_occurrence_spans.get(
                                (case_id, value[0][3]), []
                            )
                        )
                    )
                ]
                mapped = (
                    evidence_candidates[0]
                    if len(evidence_candidates) == 1
                    else candidates[0]
                    if annotation["evidence_carrier"] == "QUESTION_ASSUMPTION"
                    and len(candidates) == 1
                    else None
                )
                if mapped is not None:
                    mapped_instance_key, observed = mapped
                    classification = _classification(annotation, row, observed)
                elif candidates:
                    classification = "EVIDENCE_SCOPE_MISSING"
                elif annotation["expected_truth"] == "FALSE":
                    classification = "NEGATIVE_TARGET_PRUNED"
                else:
                    classification = "POSITIVE_TARGET_PRUNED"
            else:
                classification = _classification(annotation, row, observed)
        elif annotation["target_kind"] == "article263_pair":
            key = (str(annotation["pair_id"]), str(annotation["predicate_ref"]))
            observed = _observed_article263(row).get(key)
            if observed is None and binding_scoped:
                classification = (
                    "NEGATIVE_TARGET_PRUNED"
                    if annotation["expected_truth"] == "FALSE"
                    else "POSITIVE_TARGET_PRUNED"
                )
                mapped_instance_key = None
            else:
                classification = _classification(annotation, row, observed)
        else:
            raise ValueError(f"{annotation_id}: unknown target_kind")
        results.append(
            {
                "annotation_id": annotation_id,
                "sub_question_id": case_id,
                "predicate_ref": annotation["predicate_ref"],
                "evidence_carrier": annotation["evidence_carrier"],
                "expected_truth": annotation["expected_truth"],
                "observed_truth": observed,
                "classification": classification,
                "mapped_instance_key": (
                    {
                        "case_id": mapped_instance_key[0],
                        "actor_id": mapped_instance_key[1],
                        "offense_ref": mapped_instance_key[2],
                        "occurrence_id": mapped_instance_key[3],
                    }
                    if annotation["target_kind"] == "predicate_instance"
                    and binding_scoped
                    and mapped_instance_key is not None
                    else None
                ),
            }
        )

    contextual: dict[tuple[str, str, str, str], dict[str, set[str]]] = defaultdict(
        lambda: defaultdict(set)
    )
    for case_id, row in rows.items():
        for value in row["case_truths"]:
            instance = value["instance_key"]
            context_key = (
                case_id,
                str(instance["actor_id"]),
                str(instance["occurrence_id"]),
                str(value["predicate_ref"]),
            )
            contextual[context_key][str(value["truth"])].add(str(instance["offense_ref"]))
    contextual_variations = [
        {
            "sub_question_id": key[0],
            "actor_id": key[1],
            "occurrence_id": key[2],
            "predicate_ref": key[3],
            "truth_to_offense_refs": {
                truth: sorted(refs) for truth, refs in sorted(truths.items())
            },
        }
        for key, truths in contextual.items()
        if len(truths) > 1
    ]
    payload = {
        "scope": {
            "kind": "reviewed_decisive_predicate_partial_gold_audit",
            "warning": "Sparse explicit-evidence annotations only; not exhaustive leaf gold.",
        },
        "summary": {
            "annotation_count": len(results),
            "classification_counts": dict(Counter(value["classification"] for value in results)),
            # These are triage candidates, not all errors: actor/offense-sensitive legal
            # elements (especially intent) may legitimately differ by offense. Ground facts
            # over the exact same occurrence are the narrower stability warning.
            "contextual_truth_variation_count": len(contextual_variations),
            "ground_fact_contextual_variation_count": sum(
                value["predicate_ref"].startswith("ground_fact.")
                for value in contextual_variations
            ),
        },
        "results": results,
        "contextual_truth_variations": contextual_variations,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
