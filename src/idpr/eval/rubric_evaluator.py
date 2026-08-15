"""KCL 사건과 baseline 산출물을 `sub_question_id`로 조인해 채점표를 만든다.

깨진 줄을 조용히 건너뛰면 채점 대상 수 자체가 말없이 줄어든다. 61문항을 다 돌렸다고
믿으면서 실제로는 59문항만 채점한 표를 논문에 싣는 것이 되므로, 여기서는 읽지 못한 줄을
예외로 올린다. 파일이 아예 없는 것은 다르다 -- 아직 돌리지 않은 baseline을 빈 열로 두는
것은 이 표의 정상 동작이다.
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
            for number, line in enumerate(f, start=1):
                if line.strip():
                    try:
                        cases.append(json.loads(line))
                    except json.JSONDecodeError as error:
                        raise ValueError(
                            f"{self.kcl_draft_path}:{number}: unreadable KCL case row"
                        ) from error
        return cases

    def load_baseline_outputs(self, baseline_id: str) -> Dict[str, str]:
        """Reads baseline JSONL output and returns sub_question_id -> response mapping."""
        mapping = {}
        output_file = self.results_dir / f"{baseline_id}_outputs.jsonl"
        if not output_file.exists():
            return mapping
        with open(output_file, "r", encoding="utf-8") as f:
            for number, line in enumerate(f, start=1):
                if not line.strip():
                    continue
                try:
                    data = json.loads(line)
                except json.JSONDecodeError as error:
                    raise ValueError(
                        f"{output_file}:{number}: unreadable baseline output row"
                    ) from error
                sq_id = data.get("sub_question_id")
                if not sq_id:
                    raise ValueError(
                        f"{output_file}:{number}: baseline output row has no sub_question_id"
                    )
                mapping[sq_id] = data.get("generated_response", "")
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
