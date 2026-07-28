"""
stage1_extractor.py
Stage 1: Neural Fact Extraction module using Gemma 4 via vLLM.
Uses valid JSON Schema (Draft 7) for vLLM structured output execution.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from idpr.neural.vllm_client import VLLMClient
from idpr.pipeline.schema_registry import get_fact_graph_json_schema

PROJECT_ROOT = Path(__file__).resolve().parents[3]
STAGE1_PROMPT_PATH = PROJECT_ROOT / "prompts/kcl_1730_fact_extract.md"

class Stage1Extractor:
    """Stage 1: Extracts Datalog relational facts from natural language case text."""

    def __init__(self, client: VLLMClient | None = None) -> None:
        self.client = client
        self.system_prompt = STAGE1_PROMPT_PATH.read_text(encoding="utf-8")
        self.schema = get_fact_graph_json_schema()

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
            # vLLM Live Execution with Valid Draft 7 JSON Schema
            response, _ = self.client.complete_json(
                system_prompt=self.system_prompt,
                user_template=user_prompt,
                payload=case_data,
                schema_name="kcl_1730_fact_graph",
                schema=self.schema,
                max_tokens=8000,
                temperature=0.0,
                chat_template_kwargs={"enable_thinking": False}
            )
            return response

        # Dry-run Simulation Mode (Selected by Case ID)
        if "BRIBERY_FRAUD" in case_id or "사기" in case_data.get("title", ""):
            return {
                "case_id": case_id,
                "actors": [{"entity_id": "actor_C", "roles": ["defendant"]}],
                "facts": [
                    {
                        "fact_id": "fact_001",
                        "predicate": "bribery_delivery_committed",
                        "statement": "丙은 甲으로부터 乙에게 전달할 뇌물이라는 정을 알면서 3,000만 원을 교부받았다.",
                        "arguments": ["actor_A", "official_B"]
                    },
                    {
                        "fact_id": "fact_002",
                        "predicate": "deception_committed",
                        "statement": "丙은 뇌물 전달 의사 없이 3,000만 원을 乙에게 전달해 주겠다고 묵시적으로 甲을 속였다.",
                        "arguments": ["deception_bribery_delivery"]
                    },
                    {
                        "fact_id": "fact_003",
                        "predicate": "disposition_committed",
                        "statement": "甲은 丙의 묵시적 기망을 믿고 현금 3,000만 원을 丙에게 교부하였다.",
                        "arguments": ["disposition_cash_30m"]
                    },
                    {
                        "fact_id": "fact_004",
                        "predicate": "unlawful_intent",
                        "statement": "丙은 처음부터 위 3,000만 원을 편취하여 자신의 채무 변제에 사용할 불법이득의사를 가졌다.",
                        "arguments": ["fraud"]
                    },
                    {
                        "fact_id": "fact_005",
                        "predicate": "result_occurred",
                        "statement": "甲은 3,000만 원의 재산적 손해를 입었다.",
                        "arguments": ["property_loss"]
                    }
                ]
            }

        # Case 1 Simulation Fallback
        return {
            "case_id": case_id,
            "actors": [{"entity_id": "actor_A", "roles": ["defendant"]}],
            "facts": [
                {
                    "fact_id": "fact_001",
                    "predicate": "dwelling_intrusion_committed",
                    "statement": "피고인 A는 피해자 B의 아파트 베란다 창문을 제끼고 무단 침입하였다.",
                    "arguments": ["place_dwelling"]
                },
                {
                    "fact_id": "fact_002",
                    "predicate": "action_committed",
                    "statement": "피고인 A는 재물 절취 행위를 수행하였다.",
                    "arguments": ["act_theft"]
                },
                {
                    "fact_id": "fact_003",
                    "predicate": "unlawful_taking",
                    "statement": "피고인 A는 B 소유의 현금 500만 원과 시계를 챙겨 집어넣었다.",
                    "arguments": ["act_theft", "prop_cash"]
                },
                {
                    "fact_id": "fact_004",
                    "predicate": "unlawful_intent",
                    "statement": "피고인 A는 불법영득의사를 가졌다.",
                    "arguments": ["theft"]
                },
                {
                    "fact_id": "fact_005",
                    "predicate": "arson_act",
                    "statement": "피고인 A는 거실 소파에 불을 붙였다.",
                    "arguments": ["place_dwelling"]
                },
                {
                    "fact_id": "fact_006",
                    "predicate": "independent_combustion",
                    "statement": "불길은 벽면과 천장 마감재로 옮겨 붙어 독립 연소에 이르렀다.",
                    "arguments": ["place_dwelling"]
                },
                {
                    "fact_id": "fact_007",
                    "predicate": "unlawful_intent",
                    "statement": "피고인 A는 방화의 의사를 가졌다.",
                    "arguments": ["arson"]
                }
            ]
        }
