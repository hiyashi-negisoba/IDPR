"""
cot.py
Baseline 2: Chain-of-Thought (CoT) Prompting
Strict compliance with Rule 7 (No Fake Execution).
"""

from __future__ import annotations

from typing import Any, Dict
from idpr.baselines.base import BaseBaseline
from idpr.neural.vllm_client import VLLMClient

class CoTBaseline(BaseBaseline):
    """Chain-of-Thought (CoT) Prompting Baseline."""

    def __init__(self, client: VLLMClient | None = None) -> None:
        super().__init__(
            baseline_id="chain_of_thought",
            name="Chain-of-Thought (CoT)",
            description="Step-by-step reasoning guiding: Issue Identification -> Substantive Elements -> Defense -> Offense & Concurrence Verdict."
        )
        self.client = client

    def run_case(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        question_text = case_data.get("question_text", "")
        question_prompt = case_data.get("question_prompt", "")
        sub_question_id = case_data.get("sub_question_id", case_data.get("case_id", "UNKNOWN"))

        system_prompt = (
            "당신은 대한민국 형사법 전문 법률 전문가입니다. "
            "반드시 다음 4단계 구조로 단계별로 깊이 생각(Chain of Thought)하여 형사법리 검토 보고서를 작성하십시오:\n"
            "1. 쟁점 도출 (Issue Identification)\n"
            "2. 구성요건 검토 (Substantive Element Analysis)\n"
            "3. 위법성 및 책임 조각 / 항변 배척 (Defense Rejection)\n"
            "4. 최종 죄책 및 죄수·경합 판단 (Final Verdict)"
        )
        user_prompt = f"다음 사실관계를 읽고 위 4단계 추론 절차에 따라 답변하십시오.\n\n[사실관계 및 질문]\n{question_text}\n\n{question_prompt}"

        if self.client is not None:
            try:
                response_text = self.client.complete_text(
                    system_prompt=system_prompt,
                    user_template=user_prompt,
                    temperature=0.0,
                    max_tokens=4096
                )
            except Exception as e:
                response_text = f"[vLLM CoT Call Failure: {e}]"
        else:
            # Rule 7 (No Fake Execution): Transparent reporting when LLM client is offline
            response_text = (
                f"[Chain-of-Thought Baseline Output (Offline / vLLM Unconnected Mode)]\n"
                f"• Case ID: {sub_question_id}\n"
                f"• Configured 4-Step CoT System Prompt Active\n"
                f"• (Note: vLLM server is not connected. Output generation skipped to strictly satisfy Rule 7: No Fake Execution)"
            )

        return {
            "sub_question_id": sub_question_id,
            "baseline_id": self.baseline_id,
            "name": self.name,
            "question_prompt": question_prompt,
            "generated_response": response_text,
            "reasoning_trace": {
                "method": "chain_of_thought",
                "vllm_connected": self.client is not None,
                "steps": [
                    "1. Issue Identification",
                    "2. Substantive Element Analysis",
                    "3. Defense Rejection",
                    "4. Final Verdict"
                ]
            }
        }
