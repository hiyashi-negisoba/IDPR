"""
rubric_evaluator.py
Implements dynamic hash-join evaluation for Rubric Evaluator (Alternative B).
Dynamically joins baseline evaluation outputs with immutable KCL cases by sub_question_id.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

class RubricEvaluator:
    """Loads immutable KCL cases and dynamically joins baseline outputs by sub_question_id for rubric grading."""

    def __init__(self, kcl_draft_path: str | Path, results_dir: str | Path) -> None:
        self.kcl_draft_path = Path(kcl_draft_path)
        self.results_dir = Path(results_dir)

    def load_kcl_cases(self) -> List[Dict[str, Any]]:
        """Loads canonical immutable KCL cases."""
        cases = []
        if not self.kcl_draft_path.exists():
            return cases
        with open(self.kcl_draft_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        cases.append(json.loads(line))
                    except Exception:
                        pass
        return cases

    def load_baseline_outputs(self, baseline_id: str) -> Dict[str, str]:
        """Reads baseline JSONL output and returns sub_question_id -> response mapping."""
        mapping = {}
        output_file = self.results_dir / f"{baseline_id}_outputs.jsonl"
        if not output_file.exists():
            return mapping
        with open(output_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        data = json.loads(line)
                        sq_id = data.get("sub_question_id")
                        resp = data.get("generated_response", "")
                        if sq_id:
                            mapping[sq_id] = resp
                    except Exception:
                        pass
        return mapping

    def generate_evaluation_table(self, baseline_ids: List[str]) -> List[Dict[str, Any]]:
        """Joins baseline outputs with KCL inventory dynamically."""
        cases = self.load_kcl_cases()
        baseline_maps = {bid: self.load_baseline_outputs(bid) for bid in baseline_ids}

        evaluation_rows = []
        for case in cases:
            sq_id = case.get("sub_question_id")
            row = {
                "sub_question_id": sq_id,
                "question_text": case.get("question_text", ""),
                "rubric_summary": case.get("rubric_summary", []),
            }
            # Join baseline outputs dynamically
            for bid in baseline_ids:
                row[f"output_{bid}"] = baseline_maps[bid].get(sq_id, "N/A")
            evaluation_rows.append(row)

        return evaluation_rows
