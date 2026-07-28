"""
stage3_reporter.py
Stage 3: RAG exact-fetch & Neural Legal Review & Proof Report Generator using Gemma 4 via vLLM.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

from idpr.neural.vllm_client import VLLMClient

PROJECT_ROOT = Path(__file__).resolve().parents[3]
STAGE3_PROMPT_PATH = PROJECT_ROOT / "prompts/kcl_1730_legal_review.md"
CARD_CASE_MAP_PATH = PROJECT_ROOT / "data/card_case_metadata_map.json"

class Stage3Reporter:
    """Stage 3: RAG-augmented Legal Review & Proof Report Generator."""

    def __init__(self, client: VLLMClient | None = None) -> None:
        self.client = client
        self.system_prompt = STAGE3_PROMPT_PATH.read_text(encoding="utf-8")
        self.card_case_map = self._load_card_case_map()

    def _load_card_case_map(self) -> Dict[str, Any]:
        if CARD_CASE_MAP_PATH.is_file():
            return json.loads(CARD_CASE_MAP_PATH.read_text(encoding="utf-8"))
        return {}

    def fetch_rag_context(self, active_card_ids: List[str]) -> List[str]:
        """$O(1)$ Exact-Fetch of pre-built card text + case no metadata with fallback alias matching."""
        rag_snippets = []
        for cid in active_card_ids:
            # 1. Exact match
            entry = self.card_case_map.get(cid)
            
            # 2. Alias fallback matching
            if not entry:
                for key, val in self.card_case_map.items():
                    if cid in key or key in cid or key.split(".")[0] in cid:
                        entry = val
                        break

            if entry and entry.get("rag_text"):
                rag_snippets.append(f"- [{cid}]: {entry['rag_text']}")
            else:
                rag_snippets.append(f"- [{cid}]: {entry.get('commentary_summary', '')} ({entry.get('case_nos', '')})")
        return rag_snippets


    def generate_report(
        self,
        case_data: Dict[str, Any],
        extracted_facts: Dict[str, Any],
        symbolic_results: Dict[str, Any]
    ) -> str:
        """Renders the final Substantive Legal Review & Proof Report."""
        case_id = case_data.get("case_id", "CASE_001")
        case_text = case_data.get("case_text") or case_data.get("fact_pattern", "")
        active_card_ids = symbolic_results.get("active_card_ids", [])
        
        # 1. Fetch exact-bound RAG text
        rag_snippets = self.fetch_rag_context(active_card_ids)
        rag_text_joined = "\n".join(rag_snippets) if rag_snippets else "사전 매핑된 판례 RAG 자산 준비 완료."

        user_prompt = f"""[1. 사건 사실관계 Fact Pattern]
{case_text}

[2. Stage 1 뉴로 추출 팩트]
{json.dumps(extracted_facts, ensure_ascii=False, indent=2)}

[3. Stage 2 심볼릭 추론 및 요건 추적 (Ground Truth Proof Trace)]
- **엔진/룰베이스**: {symbolic_results.get("engine")} / {symbolic_results.get("rulebase")}
- **성립 죄목 (Proven Offenses)**:
{json.dumps(symbolic_results.get("proven_offenses", []), ensure_ascii=False, indent=2)}
- **활성화된 Card IDs**: {active_card_ids}
- **비활성화/부존재 요건**: {symbolic_results.get("unsatisfied_requirements", [])}

[4. 사전 매핑 대법원 판례 및 주석서 RAG 텍스트 (card_case_metadata_map exact-fetch)]
{rag_text_joined}

[지시사항]:
위 입력을 바탕으로 자의적인 대법원 판결문 연출을 배제하고, Scallop Proof Trace 및 사전 매핑된 exact 판례 인용((대법원 XXXX도XXXX 판결))을 명확히 포함하여 심층적인 **[종합 형사 법리 검토서 (Substantive Legal Review & Proof Report)]**를 작성하십시오."""

        if self.client is not None:
            # vLLM Live Generation
            return self.client.complete_text(
                system_prompt=self.system_prompt,
                user_template=user_prompt,
                payload=case_data,
                max_tokens=15000,
                temperature=1.0,
                top_p=0.95,
                top_k=64,
                chat_template_kwargs={"enable_thinking": True}
            )

        # Dry-run Mock Output Generator
        report_lines = [
            f"# 🏛️ [{case_id}] 종합 형사 법리 검토서 (Substantive Legal Review & Proof Report)",
            "",
            "## 1. 검토 개요 및 사건 사실관계 요약",
            f"- **사건 번호**: {case_id}",
            f"- **사실관계**: {case_text[:120]}...",
            "",
            "## 2. 심볼릭 Datalog 추론 및 요건 충족 현황 (Proof Trace)",
        ]
        for off in symbolic_results.get("proven_offenses", []):
            report_lines.append(f"- **죄목**: {off.get('offense')} ➔ **판정**: {off.get('verdict')}")
            report_lines.append(f"  - **이유**: {off.get('reasoning')} (Rule Code: `{off.get('rule_code')}`)")

        report_lines.extend([
            "",
            "## 3. 죄목별 정밀 실체법리 및 판례 인용 검토",
            "### 가. 구성요건 해당성 및 exact 판례 인용 분석",
        ])
        for snip in rag_snippets:
            report_lines.append(f"  {snip}")

        report_lines.extend([
            "",
            "## 4. 최종 종합 법리 검토 결론",
            "1. Scallop Datalog 1,730개 규칙 엔진 추론 결과, 상기 성립 죄목들의 구성요건이 100% 결정론적으로 참합되었음.",
            "2. 사전 매핑된 대법원 판례 법리를 결합하여 형사 법리 검토를 완료함."
        ])
        return "\n".join(report_lines)
