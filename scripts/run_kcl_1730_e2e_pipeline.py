#!/usr/bin/env python3
"""
run_kcl_1730_e2e_pipeline.py
Main single entry-point script to run the End-to-End Korean Criminal Law 1,730 Neuro-Symbolic Pipeline.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from idpr.pipeline.e2e_runner import KCL1730PipelineRunner

# Sample Test Case (P1 + P2 Complex Crime)
TEST_CASE = {
    "case_id": "CASE_KCL1730_2026_001",
    "title": "야간 주거침입 후 재물 절취, 피해자 상해 및 불 지른 사안 (복합 사건)",
    "fact_pattern": (
        "피고인 A는 2026. 3. 15. 23:00경 피해자 B의 아파트 창문을 열고 무단 침입하였다. "
        "피고인 A는 B 소유의 현금 500만 원과 시계를 불법영득의 의사로 절취하였다. "
        "절도 직후 잠에서 깬 피해자 B가 소리치자 피고인 A는 B의 턱을 주먹으로 가격하여 전치 3주의 상해를 가하였다. "
        "이어 피고인 A는 범행 흔적을 은폐할 목적으로 거실 소파에 불을 질렀으며, 불은 소파와 건조물 벽면에 붙어 독립적으로 연소하기 시작하였다."

    )
}

def main():
    parser = argparse.ArgumentParser(description="Run KCL 1,730 E2E Neuro-Symbolic Pipeline")
    parser.add_argument("--mode", choices=["dry-run", "vllm"], default="dry-run", help="Execution mode")
    parser.add_argument("--base-url", type=str, default=None, help="vLLM server base URL")
    parser.add_argument("--model", type=str, default=None, help="vLLM model identifier")
    parser.add_argument("--case-json", type=str, default=None, help="Input case JSON file path")
    parser.add_argument("--out-dir", type=str, default=str(PROJECT_ROOT / "data/e2e/output"), help="Output directory")

    args = parser.parse_args()

    if args.case_json:
        case_data = json.loads(Path(args.case_json).read_text(encoding="utf-8"))
    else:
        case_data = TEST_CASE

    if args.mode == "vllm" and (not args.base_url or not args.model):
        print("Error: vllm mode requires --base-url and --model arguments.")
        sys.exit(1)

    runner = KCL1730PipelineRunner(
        base_url=args.base_url if args.mode == "vllm" else None,
        model=args.model if args.mode == "vllm" else None
    )

    result = runner.run_e2e(case_data)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{result['case_id']}_result.json"

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n============================================================")
    print(f"📄 FINAL LEGAL REVIEW REPORT RENDERED:")
    print(f"============================================================")
    print(result["final_report"])
    print(f"\nSaved execution result JSON to: {out_file}")

if __name__ == "__main__":
    main()
