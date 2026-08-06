#!/usr/bin/env python3
"""Run the lean RuleIR-native pipeline against the SKI-ML gateway's Sonnet route.

Same pipeline as ``run_rule_ir_native_lean.py``; only the model client differs. Kept
as a separate entry point rather than a flag on the tested CLI so the vLLM path's
contract (and its tests) stay untouched while this route is still an experiment.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from idpr.neural.skiml_litellm_client import SkimlLiteLLMClient  # noqa: E402
from idpr.rulegen.native_host import DEFAULT_SCLI  # noqa: E402
from scripts.run_rule_ir_native_lean import _read_jsonl_index, run_case  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", default="anthropic/claude-sonnet-4-6")
    parser.add_argument("--case-id", required=True)
    parser.add_argument(
        "--inventory",
        type=Path,
        default=ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl",
    )
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--scli", type=Path, default=DEFAULT_SCLI)
    args = parser.parse_args()

    inventory = _read_jsonl_index(args.inventory)
    if args.case_id not in inventory:
        raise KeyError(f"case id not found in inventory: {args.case_id}")
    client = SkimlLiteLLMClient.from_env(model=args.model)
    result = run_case(
        client=client,
        raw_case=inventory[args.case_id],
        out_dir=args.out_dir / args.case_id,
        scli_path=args.scli,
    )
    print(args.out_dir / args.case_id / "05_answer.md")
    print(
        "verdict_contradictions="
        + json.dumps(result["verdict_contradictions"], ensure_ascii=False)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
