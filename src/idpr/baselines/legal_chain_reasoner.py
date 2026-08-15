"""LCR 방식을 본뜬 프롬프팅 baseline. 공식 구현의 재현이 아니다.

이 파일은 한때 "공식 저장소를 수정 없이 실행한다"고 적혀 있었지만, `run_case`가 실제로 하는
일은 LCR의 단계 이름(Fact Decomposer -> Rule Selector -> Element Matcher -> Synthesizer)을
문장으로 적은 **하나의 프롬프트**를 로컬 vLLM에 보내는 것이다. 위의 sys.path 주입과 monkey
patch는 저장소를 실행할 준비이지 실행 자체가 아니고, 저장소가 없어도 이 baseline은 그대로
결과를 낸다.

논문에서 이것을 "official LegalChainReasoner baseline"으로 부르면 비교의 성질을 잘못
말하는 것이 된다. 우리 프롬프트로 우리 모델을 돌린 결과이므로, 주장할 수 있는 것은
**LCR-inspired prompting baseline**까지다. 공식 구현 재현이 필요하면 그것은 별도 작업이고,
그때 이 파일이 아니라 실제로 저장소 파이프라인을 호출하는 어댑터를 쓴다.

huggingface_hub·openai monkey patch는 저장소를 오프라인 환경에서 import할 수 있게 하려고
남겨 둔다.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any, Dict
from unittest.mock import MagicMock

# 1. Mock huggingface_hub globally to bypass the blocking huggingface_hub.login("...") call
# which throws 401 Unauthorized / ConnectionError in offline/restricted environments.
mock_hf = MagicMock()
mock_hf.login = MagicMock(return_value=None)
sys.modules["huggingface_hub"] = mock_hf

# Inject dummy environment variables to bypass validation checks in original code
os.environ.setdefault("OPENAI_API_KEY", "dummy-openai-key")

# 2. OpenAI API Monkey-Patching (Interception Layer)
try:
    import openai
    original_openai_init = openai.OpenAI.__init__
    def patched_openai_init(self, *args, **kwargs):
        port = os.environ.get("VLLM_PORT", "8000")
        kwargs["base_url"] = f"http://127.0.0.1:{port}/v1"
        kwargs["api_key"] = "local-idpr"
        kwargs.pop("default_query", None)
        kwargs.pop("default_headers", None)
        original_openai_init(self, *args, **kwargs)
    openai.OpenAI.__init__ = patched_openai_init
except ImportError:
    pass

# Add baselines/LegalChainReasoner to sys.path
LEGAL_CHAIN_DIR = Path(__file__).resolve().parents[3] / "baselines" / "LegalChainReasoner"
if LEGAL_CHAIN_DIR.exists() and str(LEGAL_CHAIN_DIR) not in sys.path:
    sys.path.insert(0, str(LEGAL_CHAIN_DIR))

from idpr.baselines.base import BaseBaseline
from idpr.neural.vllm_client import VLLMClient

class LegalChainReasonerBaseline(BaseBaseline):
    """LCR의 단계 구성을 본뜬 단일 프롬프트 baseline. 공식 파이프라인을 호출하지 않는다."""

    def __init__(self, client: VLLMClient | None = None) -> None:
        super().__init__(
            baseline_id="legal_chain_reasoner",
            # baseline_id는 기존 산출물의 조인 키라 그대로 두고, 무엇을 돌린 것인지를
            # 말하는 이름과 설명만 사실에 맞춘다.
            name="LCR-inspired prompting baseline",
            description=(
                "Sends one prompt that names LegalChainReasoner's stages to the local model. "
                "This is not a reproduction of the official LCR implementation."
            )
        )
        self.client = client
        self.repo_path = LEGAL_CHAIN_DIR

    def run_case(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        sub_question_id = case_data.get("sub_question_id", "UNKNOWN")

        # 단계 이름을 문장으로 적은 프롬프트 하나. 저장소 파이프라인은 호출되지 않는다.
        response_text = ""
        if self.client:
            fact_text = "\n".join(case_data.get("fact_sentences", [])) if "fact_sentences" in case_data else case_data.get("question_text", "")
            prompt = f"Fact Decomposer -> Rule Selector -> Element Matcher -> Synthesizer sequential steps:\nFacts:\n{fact_text}\n\n질문:\n{case_data.get('question_prompt', '죄책을 논하시오.')}\n\n단계별 추론을 거쳐 최종 죄책을 상세히 논하시오."

            try:
                response_text = self.client.complete_text(
                    system_prompt="당신은 단계별 체인 추론을 수행하는 대한민국 형사법 전문 법률 전문가입니다.",
                    user_template=prompt,
                    temperature=0.0,
                    max_tokens=4096
                )
            except Exception as e:
                response_text = f"[vLLM Call Error: {e}]"

        return {
            "sub_question_id": sub_question_id,
            "baseline_id": self.baseline_id,
            "name": self.name,
            "legal_chain_repo_available": self.repo_path.exists(),
            "generated_response": response_text,
            "reasoning_trace": {
                "method": "lcr_inspired_single_prompt",
                "repo_path": str(self.repo_path),
                "repo_available": self.repo_path.exists()
            }
        }
