from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from idpr.rulegen import apply_norm_candidate_patch  # noqa: E402
from scripts.run_fraud_rulegen_pilot import (  # noqa: E402
    REQUESTS,
    load_jsonl,
    write_json,
)


DEFAULT_INPUT = (
    PROJECT_ROOT
    / ".cache/llm/runs/fraud_rulegen_correction/pilot_20260716_correction6"
    / "terra_revision/fraud.article347.pass1.001.json"
)
DEFAULT_PATCH = (
    PROJECT_ROOT
    / "data/rulegen/fraud/fraud_pass1_001_revision5_patch.json"
)
DEFAULT_OUTPUT = (
    PROJECT_ROOT
    / ".cache/llm/runs/fraud_rulegen_patch/pilot_20260716_revision6"
    / "fraud.article347.pass1.001.json"
)


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Apply and validate an adjudicated NormCandidate patch."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--patch", type=Path, default=DEFAULT_PATCH)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument(
        "--target-id", default="fraud.article347.pass1.001.revision5"
    )
    parser.add_argument(
        "--request-id", default="fraud.article347.pass1.001"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    requests = {row["request_id"]: row for row in load_jsonl(REQUESTS)}
    result = apply_norm_candidate_patch(
        read_json(args.input),
        read_json(args.patch),
        requests[args.request_id],
        expected_target_id=args.target_id,
    )
    write_json(args.output, result)
    print(
        json.dumps(
            {
                "output_path": str(args.output),
                "candidates": len(result["candidates"]),
                "unresolved_questions": len(result["unresolved_questions"]),
                "valid": True,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
