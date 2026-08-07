#!/usr/bin/env python3
"""Recompute a hallucination score restricted to a subset of incident kinds.

``hallucination_score_macro`` as produced by the judge counts every incident
kind (``doctrinal_error``/``statutory_error``/``factual_invention``/``other``
alongside ``nonexistent_offense``/``fabricated_case``) at the same severity
weight. In practice, on the 26-case substantive-law set, 34 of 44 IDPR
incidents were ``doctrinal_error`` (ordinary legal-reasoning mistakes) and
only 1 was true fabrication (``fabricated_case``) — so the aggregate score
mostly measures "how many legal mistakes" rather than "did it make things
up" (docs/handoff/CURRENT.md). This recomputes the same severity-weighted
score from ``data/eval/phase3_judge_protocol.json``'s ``severity_weights``,
but only over the incident kinds passed in ``--kinds`` — entirely from
already-produced judgments.jsonl files, no new judge calls, for every
method that already has one.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import fmean
from typing import Any


ROOT = Path(__file__).resolve().parents[1]


def load_severity_weights(protocol_path: Path) -> dict[str, int]:
    protocol = json.loads(protocol_path.read_text(encoding="utf-8"))
    return {
        str(name): int(weight)
        for name, weight in protocol["hallucination"]["severity_weights"].items()
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--judgments",
        type=Path,
        action="append",
        required=True,
        help="a judgments.jsonl file; pass multiple times to pool several files",
    )
    parser.add_argument("--case-list", type=Path, required=True)
    parser.add_argument(
        "--kinds",
        nargs="+",
        default=["statutory_error", "fabricated_case", "nonexistent_offense"],
    )
    parser.add_argument(
        "--protocol",
        type=Path,
        default=ROOT / "data/eval/phase3_judge_protocol.json",
    )
    args = parser.parse_args()

    case_ids = {
        line.strip()
        for line in args.case_list.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }
    weights = load_severity_weights(args.protocol)
    kinds = set(args.kinds)

    by_method: dict[str, list[dict[str, Any]]] = {}
    for judgments_path in args.judgments:
        with judgments_path.open(encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line:
                    continue
                record = json.loads(line)
                if record.get("status") != "ok":
                    continue
                if str(record.get("sub_question_id", "")) not in case_ids:
                    continue
                method_id = str(record["method_id"])
                by_method.setdefault(method_id, []).append(record)

    report: dict[str, Any] = {}
    for method_id, records in sorted(by_method.items()):
        narrow_scores = []
        narrow_incident_counts = []
        for record in records:
            incidents = record["metrics"]["hallucination"]["incidents"]
            narrow_incidents = [inc for inc in incidents if inc.get("kind") in kinds]
            score = -sum(weights[str(inc["severity"])] for inc in narrow_incidents)
            narrow_scores.append(score)
            narrow_incident_counts.append(len(narrow_incidents))
        report[method_id] = {
            "completed_cases": len(records),
            "narrow_hallucination_score_macro": fmean(narrow_scores) if narrow_scores else None,
            "narrow_hallucination_free_rate": (
                sum(count == 0 for count in narrow_incident_counts) / len(narrow_incident_counts)
                if narrow_incident_counts
                else None
            ),
            "narrow_incident_total": sum(narrow_incident_counts),
        }

    print(json.dumps({"kinds": sorted(kinds), "methods": report}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
