from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any, Mapping


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from idpr.legacy.fraud_planning import (  # noqa: E402
    load_fraud_plan_registry,
    select_fraud_reasoning_plan,
    validate_fraud_case,
)


DEFAULT_CASE_SET = (
    PROJECT_ROOT / "data/e2e/fraud/manual_paraphrases/fraud_manual_paraphrase_cases.json"
)
DEFAULT_SOURCE_INDEX = Path(
    os.environ.get(
        "IDPR_MANUAL_SOURCE_INDEX",
        PROJECT_ROOT / "data/raw/manual_crimefacts_economic_v2/leaf_raw.jsonl",
    )
)
CASE_BOUNDARY = re.compile(r"(?m)(?=^\d+\)\s)")
LEAKAGE_TERMS = ("기망", "편취", "사기죄", "의사나 능력이 없")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_source_leaves(path: Path) -> dict[str, dict[str, Any]]:
    leaves: dict[str, dict[str, Any]] = {}
    with path.open(encoding="utf-8") as source_file:
        for line_number, line in enumerate(source_file, start=1):
            if not line.strip():
                continue
            leaf = json.loads(line)
            leaf_id = leaf.get("leaf_id")
            if not leaf_id:
                raise ValueError(f"source line {line_number} has no leaf_id")
            if leaf_id in leaves:
                raise ValueError(f"duplicate source leaf_id {leaf_id}")
            leaves[leaf_id] = leaf
    return leaves


def source_case_segment(raw_text: str, ordinal: int) -> str:
    segments = [part.strip() for part in CASE_BOUNDARY.split(raw_text) if part.strip()]
    if ordinal < 1 or ordinal > len(segments):
        raise ValueError(f"case ordinal {ordinal} is outside source segment count {len(segments)}")
    return segments[ordinal - 1]


def validate_case_set(
    payload: Mapping[str, Any], leaves: Mapping[str, Mapping[str, Any]]
) -> dict[str, Any]:
    registry = load_fraud_plan_registry()
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("paraphrase case set must contain a non-empty cases array")

    seen: set[str] = set()
    routes: dict[str, int] = {}
    for case in cases:
        validate_fraud_case(case, registry)
        case_id = case["case_id"]
        if case_id in seen:
            raise ValueError(f"duplicate case_id {case_id}")
        seen.add(case_id)

        leakage = [term for term in LEAKAGE_TERMS if term in case["case_text"]]
        if leakage:
            raise ValueError(f"{case_id} contains conclusion leakage: {leakage}")

        source = case["source"]
        leaf = leaves.get(source["leaf_id"])
        if leaf is None:
            raise ValueError(f"{case_id} source leaf is missing: {source['leaf_id']}")
        for field in ("manual_id", "page_start", "page_end"):
            if source[field] != leaf[field]:
                raise ValueError(f"{case_id} source {field} differs from index")

        segment = source_case_segment(leaf["raw_text"], source["case_ordinal"])
        actual_hash = hashlib.sha256(segment.encode("utf-8")).hexdigest()
        if source["source_segment_chars"] != len(segment):
            raise ValueError(f"{case_id} source segment character count differs")
        if source["source_segment_sha256"] != actual_hash:
            raise ValueError(f"{case_id} source segment SHA-256 differs")

        synthetic_graph = {"profiles": case["required_profiles"]}
        plan = select_fraud_reasoning_plan(synthetic_graph, case=case, registry=registry)
        routes[plan["plan_id"]] = routes.get(plan["plan_id"], 0) + 1

    return {
        "status": "valid",
        "case_count": len(cases),
        "unique_case_count": len(seen),
        "source_hashes_verified": len(cases),
        "reasoning_plan_counts": dict(sorted(routes.items())),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--case-set", type=Path, default=DEFAULT_CASE_SET)
    parser.add_argument("--source-index", type=Path, default=DEFAULT_SOURCE_INDEX)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = validate_case_set(read_json(args.case_set), load_source_leaves(args.source_index))
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
