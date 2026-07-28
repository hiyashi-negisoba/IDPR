"""
e2e_runner.py
E2E Orchestrator running Stage 1 (Fact Extraction) -> Stage 2 (Datalog Reasoning) -> Stage 3 (Legal Review Report).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

from idpr.neural.vllm_client import VLLMClient
from idpr.pipeline.stage1_extractor import Stage1Extractor
from idpr.pipeline.stage2_symbolic import Stage2SymbolicReasoner
from idpr.pipeline.stage3_reporter import Stage3Reporter

class KCL1730PipelineRunner:
    """E2E Orchestrator for Korean Criminal Law 1,730 Neuro-Symbolic Pipeline."""

    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
        api_key: str = "local-idpr"
    ) -> None:
        self.vllm_client = VLLMClient(base_url=base_url, model=model, api_key=api_key) if (base_url and model) else None
        self.stage1 = Stage1Extractor(client=self.vllm_client)
        self.stage2 = Stage2SymbolicReasoner()
        self.stage3 = Stage3Reporter(client=self.vllm_client)

    def run_e2e(self, case_data: Dict[str, Any]) -> Dict[str, Any]:
        """Executes the complete End-to-End pipeline."""
        case_id = case_data.get("case_id", "CASE_001")
        print(f"============================================================")
        print(f"🚀 Running KCL 1,730 E2E Pipeline for Case [{case_id}]")
        print(f"============================================================")

        # Stage 1: Neural Fact Extraction
        print(f"\n[Stage 1/3] Running Neural Fact Extraction (Gemma 4 temp=0.0)...")
        extracted_facts = self.stage1.extract_facts(case_data)
        print(f"  └─ Extracted {len(extracted_facts.get('facts', []))} facts/predicates.")

        # Stage 2: Scallop Datalog Symbolic Reasoning
        print(f"\n[Stage 2/3] Running Scallop Datalog Symbolic Reasoner (1,730 rules)...")
        symbolic_results = self.stage2.run_datalog_reasoning(extracted_facts)
        print(f"  └─ Proven Offenses Count: {len(symbolic_results.get('proven_offenses', []))}")
        print(f"  └─ Active Card IDs Count: {len(symbolic_results.get('active_card_ids', []))}")

        # Stage 3: RAG Exact-Fetch & Legal Review Report Generation
        print(f"\n[Stage 3/3] RAG Exact-Fetch & Generating Legal Review Report (Gemma 4 temp=1.0)...")
        final_report = self.stage3.generate_report(case_data, extracted_facts, symbolic_results)
        print(f"  └─ Final Legal Review Report rendered ({len(final_report)} chars).")

        print(f"\n✅ E2E Pipeline Execution Completed Successfully.")

        return {
            "case_id": case_id,
            "extracted_facts": extracted_facts,
            "symbolic_results": symbolic_results,
            "final_report": final_report
        }
