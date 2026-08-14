"""
vanilla.py
Baseline 1: Vanilla LLM (Zero-shot Direct Prompting)
Strict compliance with Rule 7 (No Fake Execution).
"""

from __future__ import annotations

from typing import Any, Dict
from idpr.baselines.base import BaseBaseline
from idpr.neural.vllm_client import VLLMClient

VANILLA_SYSTEM_PROMPT = (
    "당신은 대한민국 형사법 전문 법률 전문가입니다. "
    "주어진 사실관계와 질문을 바탕으로 형사상 죄책 및 법리적 결론을 명확하고 논리적으로 서술하십시오."
)


def build_vanilla_user_prompt(question_text: str, question_prompt: str) -> str:
    """The zero-shot answer prompt.

    Shared rather than duplicated so that baselines which add one signal on top of
    zero-shot -- LePREC contributes an issue decomposition -- differ from vanilla in
    exactly that signal and nothing else. Editing the wording here moves both.
    """
    return (
        "다음 사실관계를 읽고 질문에 답하십시오.\n\n"
        f"[사실관계 및 질문]\n{question_text}\n\n{question_prompt}"
    )


class VanillaBaseline(BaseBaseline):
    """Vanilla Zero-shot LLM Baseline."""

    def __init__(
        self,
        client: VLLMClient | None = None,
        *,
        temperature: float = 0.0,
        max_tokens: int = 4096,
    ) -> None:
        """``temperature`` and ``max_tokens`` default to the values the first baseline
        sweep ran at, so an unparameterised call reproduces that artifact.  They are
        settable because a condition comparison wants every knob equal across arms except
        the pipeline under test, and the IDPR runs decode at 0.7 / 8192.
        """
        super().__init__(
            baseline_id="vanilla_zero_shot",
            name="Vanilla LLM (Zero-shot)",
            description="Direct zero-shot parametric reasoning by LLM without additional context or structured prompt."
        )
        self.client = client
        self.temperature = temperature
        self.max_tokens = max_tokens

    def run_case(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        question_text = case_data.get("question_text", "")
        question_prompt = case_data.get("question_prompt", "")
        sub_question_id = case_data.get("sub_question_id", case_data.get("case_id", "UNKNOWN"))

        system_prompt = VANILLA_SYSTEM_PROMPT
        user_prompt = build_vanilla_user_prompt(question_text, question_prompt)

        if self.client is not None:
            try:
                response_text = self.client.complete_text(
                    system_prompt=system_prompt,
                    user_template=user_prompt,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                )
            except Exception as e:
                response_text = f"[vLLM Direct Call Failure: {e}]"
        else:
            # Rule 7 (No Fake Execution): Transparent reporting when LLM client is offline
            response_text = (
                f"[Vanilla Zero-Shot Baseline Output (Offline / vLLM Unconnected Mode)]\n"
                f"• Case ID: {sub_question_id}\n"
                f"• System Prompt Configured: '{system_prompt[:50]}...'\n"
                f"• (Note: vLLM server is not connected. Output generation skipped to strictly satisfy Rule 7: No Fake Execution)"
            )

        return {
            "sub_question_id": sub_question_id,
            "baseline_id": self.baseline_id,
            "name": self.name,
            "question_prompt": question_prompt,
            "generated_response": response_text,
            "reasoning_trace": {
                "method": "zero_shot_direct",
                "vllm_connected": self.client is not None,
                "system_prompt": system_prompt,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
            }
        }
