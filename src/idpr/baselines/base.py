"""
base.py
Abstract Base Class for Experimental Baselines.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict

class BaseBaseline(ABC):
    """Abstract Base Class for all legal reasoning baselines."""

    def __init__(self, baseline_id: str, name: str, description: str) -> None:
        self.baseline_id = baseline_id
        self.name = name
        self.description = description

    @abstractmethod
    def run_case(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Runs the baseline logic on a given test case row from KCL benchmark.

        Args:
            case_data: Dictionary containing question_text, question_prompt, etc.

        Returns:
            Dictionary containing:
            - case_id / sub_question_id
            - baseline_id
            - generated_response: str
            - reasoning_trace: dict or str
            - raw_output: Any
        """
        pass
