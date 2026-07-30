#!/usr/bin/env python3
"""
verify_experiment_integrity.py
Verifies that all 61 cases in data/inventory/kcl_criminal_v1_draft.jsonl have corresponding
outputs in the experiments/results/{baseline_id}_outputs.jsonl files.
"""

import json
import sys
from pathlib import Path

def main():
    repo_root = Path(__file__).resolve().parents[1]
    kcl_draft_path = repo_root / "data" / "inventory" / "kcl_criminal_v1_draft.jsonl"
    results_dir = repo_root / "experiments" / "results"

    if not kcl_draft_path.exists():
        print(f"❌ Error: KCL draft inventory not found at {kcl_draft_path}")
        sys.exit(1)

    # 1. Load all target sub_question_ids
    target_ids = []
    with open(kcl_draft_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    case = json.loads(line)
                    sq_id = case.get("sub_question_id")
                    if sq_id:
                        target_ids.append(sq_id)
                except Exception as e:
                    print(f"⚠️ JSON parsing error in draft: {e}")

    print(f"🔍 Loaded {len(target_ids)} target sub_question_ids from draft inventory.")

    baseline_ids = [
        "vanilla_zero_shot",
        "chain_of_thought",
        "standard_rag",
        "leprec",
        "acal",
        "legal_chain_reasoner",
        "fol_autoformalizer_solver"
    ]

    all_passed = True
    for bid in baseline_ids:
        output_file = results_dir / f"{bid}_outputs.jsonl"
        if not output_file.exists():
            print(f"❌ Baseline '{bid}': Output file missing ({output_file})")
            all_passed = False
            continue

        # Load generated ids
        generated_ids = set()
        with open(output_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        data = json.loads(line)
                        sq_id = data.get("sub_question_id")
                        if sq_id:
                            generated_ids.add(sq_id)
                    except Exception as e:
                        print(f"⚠️ JSON parsing error in {bid} output: {e}")

        # Check for missing cases
        missing = [tid for tid in target_ids if tid not in generated_ids]
        if missing:
            print(f"❌ Baseline '{bid}': Missing {len(missing)} outputs! (Samples: {missing[:3]})")
            all_passed = False
        else:
            print(f"✅ Baseline '{bid}': All {len(target_ids)} cases verified and matched.")

    if all_passed:
        print("\n🎉 INTEGRITY CHECK PASSED: All baselines outputs are fully consistent with the KCL dataset!")
        sys.exit(0)
    else:
        print("\n❌ INTEGRITY CHECK FAILED: Found mismatch or missing outputs.")
        sys.exit(1)

if __name__ == "__main__":
    main()
