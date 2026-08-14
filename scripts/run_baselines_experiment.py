#!/usr/bin/env python3
"""
run_baselines_experiment.py
User-Friendly CLI Interface for running 7 comparison baselines and collecting output traces.
"""

import argparse
import sys
from pathlib import Path

# Add src to sys.path
SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from idpr.eval.baseline_runner import BaselineExperimentRunner  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(
        description="IDPR Comparison Baseline Experiment Runner CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--baseline",
        "-b",
        type=str,
        default="all",
        help="Baseline ID to run ('all' or comma-separated list e.g. 'vanilla_zero_shot,chain_of_thought,acal')",
    )
    parser.add_argument(
        "--dataset",
        "-d",
        type=str,
        default="data/inventory/kcl_criminal_v1_draft.jsonl",
        help="Path to KCL benchmark dataset jsonl file",
    )
    parser.add_argument(
        "--limit",
        "-l",
        type=int,
        default=None,
        help="Limit the number of dataset cases (useful for a quick diagnostic run)",
    )
    parser.add_argument(
        "--outdir",
        "-o",
        type=str,
        default="experiments/results",
        help="Output directory for generated baseline reasoning traces",
    )
    parser.add_argument(
        "--vllm-url",
        type=str,
        default=None,
        help="vLLM server endpoint URL (e.g. http://localhost:8000)",
    )
    parser.add_argument(
        "--vllm-model",
        type=str,
        default=None,
        help="vLLM model name (e.g. gemma-4-26b-it)",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=None,
        help="Decoding temperature; omit to keep each baseline's own default",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=None,
        help="Decoding max_tokens; omit to keep each baseline's own default",
    )
    parser.add_argument(
        "--case-id-file",
        type=str,
        default=None,
        help="One sub_question_id per line; restricts the run to that subset",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all registered comparison baselines and exit",
    )

    args = parser.parse_args()

    runner = BaselineExperimentRunner(
        vllm_base_url=args.vllm_url,
        vllm_model=args.vllm_model,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        output_dir=args.outdir,
    )

    if args.list:
        print("\n============================================================")
        print("📋 Registered IDPR Comparison Baselines Lineup")
        print("============================================================")
        for item in runner.list_baselines():
            print(f" • ID: {item['baseline_id']:<30} | Name: {item['name']}")
            print(f"   Description: {item['description']}\n")
        print("============================================================\n")
        return

    selected_ids = [b.strip() for b in args.baseline.split(",") if b.strip()]

    print("\n🚀 Initializing IDPR Baseline Experiment Runner...")
    case_ids = None
    if args.case_id_file:
        case_ids = [
            line.strip()
            for line in Path(args.case_id_file).read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.startswith("#")
        ]

    results = runner.run_experiments(
        dataset_path=args.dataset,
        selected_baseline_ids=selected_ids,
        limit=args.limit,
        verbose=True,
        case_ids=case_ids,
    )

    print("\n📊 Summary of Results Generated:")
    for b_id, outputs in results.items():
        print(
            f" • Baseline [{b_id}]: {len(outputs)} outputs generated -> {args.outdir}/{b_id}_outputs.jsonl"
        )


if __name__ == "__main__":
    main()
