"""
stage1_extractor.py
Stage 1: Neural Fact Extraction module using Gemma 4 via vLLM.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from idpr.neural.vllm_client import VLLMClient

PROJECT_ROOT = Path(__file__).resolve().parents[3]
STAGE1_PROMPT_PATH = PROJECT_ROOT / "prompts/kcl_1730_fact_extract.md"

class Stage1Extractor:
    """Stage 1: Extracts Datalog relational facts from natural language case text."""

    def __init__(self, client: VLLMClient | None = None) -> None:
        self.client = client
        self.system_prompt = STAGE1_PROMPT_PATH.read_text(encoding="utf-8")

    def extract_facts(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Runs Stage 1 neural fact extraction."""
        case_id = case_data.get("case_id", "CASE_001")
        case_text = case_data.get("case_text") or case_data.get("fact_pattern", "")

        user_prompt = f"""[사건 ID]: {case_id}
[사건 사실관계 (Fact Pattern)]:
{case_text}

[지시사항]:
위 사실관계에서 사건에 나타난 인물, 점유/소유관계, 실행행위, 고의, 결과, 인과관계 및 32개 Datalog Input Predicate 릴레이션 팩트를 추출하여 JSON으로 출력하십시오."""

        if self.client is not None:
            # vLLM Live Execution
            response, _ = self.client.complete_json(
                system_prompt=self.system_prompt,
                user_template=user_prompt,
                payload=case_data,
                schema_name="kcl_1730_fact_graph",
                schema=None,
                max_tokens=8000,
                temperature=0.0,
                chat_template_kwargs={"enable_thinking": False}
            )
            return response

        # Dry-run Simulation Mode
        simulated_facts = case_data.get("simulated_extracted_facts") or {
            "case_id": case_id,
            "actors": [{"entity_id": "actor_A", "roles": ["defendant"]}],
            "facts": [
                {
                    "fact_id": "fact_001",
                    "predicate": "actor",
                    "statement": "피고인 A는 사건의 수사대상 행위자이다.",
                    "source_quote": case_text[:50] if case_text else "피고인 A"
                }
            ]
        }
        return simulated_facts
