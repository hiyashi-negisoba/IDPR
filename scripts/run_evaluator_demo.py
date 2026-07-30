#!/usr/bin/env python3
"""
run_evaluator_demo.py
Demonstrates RubricEvaluator dynamic hash-join evaluation over all 61 cases.
"""

import sys
import json
from pathlib import Path

# Add src to sys.path
repo_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(repo_root / "src"))

from idpr.eval.rubric_evaluator import RubricEvaluator

def main():
    kcl_draft_path = repo_root / "data" / "inventory" / "kcl_criminal_v1_draft.jsonl"
    results_dir = repo_root / "experiments" / "results"

    evaluator = RubricEvaluator(kcl_draft_path, results_dir)

    baseline_ids = [
        "vanilla_zero_shot",
        "chain_of_thought",
        "standard_rag",
        "leprec",
        "acal",
        "legal_chain_reasoner",
        "fol_autoformalizer_solver"
    ]

    print("🚀 Running RubricEvaluator Dynamic Hash-Join over 61 KCL cases...")
    joined_rows = evaluator.generate_evaluation_table(baseline_ids)

    print(f"📊 Completed dynamic join. Total rows joined: {len(joined_rows)}")

    # Verification checks
    if len(joined_rows) == 61:
        print("✅ Success: Joined exactly 61 rows.")
    else:
        print(f"❌ Error: Joined row count mismatch ({len(joined_rows)})")
        sys.exit(1)

    # Inspect first row sample details
    sample = joined_rows[0]
    print("\n🔍 Sample Row Trace (Case 1):")
    print(f"  • ID: {sample['sub_question_id']}")
    print(f"  • Rubric Count: {len(sample['rubric_summary'])}")
    for bid in baseline_ids:
        output_len = len(sample.get(f"output_{bid}", ""))
        print(f"  • Baseline output_{bid} char length: {output_len}")

    print("\n🎉 RubricEvaluator Demo verified successfully!")

if __name__ == "__main__":
    main()
