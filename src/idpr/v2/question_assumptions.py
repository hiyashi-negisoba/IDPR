"""Reviewed factual assumptions stated in a KCL sub-question prompt.

These are benchmark-provided facts that apply globally to the selected sub-question but
are not part of an actor occurrence span.  They are deliberately kept separate from
manual GOLD occurrences and from legal-analysis branch directives.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class QuestionAssumptionError(ValueError):
    pass


@dataclass(frozen=True)
class QuestionAssumption:
    assumption_id: str
    source_text: str
    source_start: int
    source_end: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "assumption_id": self.assumption_id,
            "source_text": self.source_text,
            "source_span": {"start": self.source_start, "end": self.source_end},
        }


def load_question_assumptions(
    path: Path, *, question_prompt_by_id: Mapping[str, str]
) -> dict[str, tuple[QuestionAssumption, ...]]:
    """Load a sparse exact-substring carrier; unlisted cases have no assumption."""
    output: dict[str, tuple[QuestionAssumption, ...]] = {}
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError as exc:
            raise QuestionAssumptionError(f"{path}:{line_number}: invalid JSON") from exc
        if not isinstance(row, Mapping) or set(row) != {
            "sub_question_id",
            "assumptions",
        }:
            raise QuestionAssumptionError(f"{path}:{line_number}: invalid row shape")
        case_id = row["sub_question_id"]
        raw_values = row["assumptions"]
        if not isinstance(case_id, str) or case_id not in question_prompt_by_id:
            raise QuestionAssumptionError(f"{path}:{line_number}: unknown case")
        if case_id in output:
            raise QuestionAssumptionError(f"{path}:{line_number}: duplicate case")
        if not isinstance(raw_values, list) or not raw_values:
            raise QuestionAssumptionError(f"{case_id}: assumptions must be nonempty")
        prompt = question_prompt_by_id[case_id]
        values = []
        for index, raw in enumerate(raw_values, 1):
            if not isinstance(raw, Mapping) or set(raw) != {
                "assumption_id",
                "source_text",
            }:
                raise QuestionAssumptionError(
                    f"{case_id}: assumption {index} has invalid shape"
                )
            assumption_id = raw["assumption_id"]
            source_text = raw["source_text"]
            expected_id = f"qassump:{index:03d}"
            if assumption_id != expected_id:
                raise QuestionAssumptionError(
                    f"{case_id}: expected assumption_id {expected_id!r}"
                )
            if not isinstance(source_text, str) or not source_text.strip():
                raise QuestionAssumptionError(f"{case_id}/{assumption_id}: empty text")
            start = prompt.find(source_text)
            if start < 0 or prompt.find(source_text, start + 1) >= 0:
                raise QuestionAssumptionError(
                    f"{case_id}/{assumption_id}: text must occur exactly once in prompt"
                )
            values.append(
                QuestionAssumption(
                    assumption_id,
                    source_text,
                    start,
                    start + len(source_text),
                )
            )
        output[case_id] = tuple(values)
    return output


__all__ = [
    "QuestionAssumption",
    "QuestionAssumptionError",
    "load_question_assumptions",
]
