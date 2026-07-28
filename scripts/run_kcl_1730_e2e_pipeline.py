#!/usr/bin/env python3
"""
run_kcl_1730_e2e_pipeline.py
Main single entry-point script to run the End-to-End Korean Criminal Law 1,730 Neuro-Symbolic Pipeline
against the Official 2 Standard Test Cases.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from idpr.pipeline.e2e_runner import KCL1730PipelineRunner

# Official Standard Test Case 1: Realistic Property + Non-Property Complex Case (No hardcoded legal jargon)
TEST_CASE_1 = {
    "case_id": "CASE_KCL1730_2026_REAL_001",
    "title": "아파트 베란다 침입, 재물 인출, 폭행 상해 및 라이터 방화 사안",
    "fact_pattern": (
        "피고인 A는 2026. 3. 15. 23:00경 피해자 B가 살고 있는 아파트 베란다 창문을 드라이버로 제껴 열고 몰래 안으로 들어갔다. "
        "피고인 A는 안방 장롱 안에 들어있던 피해자 B 소유의 현금 500만 원과 롤렉스 시계를 챙겨 자신의 가방에 집어넣었다. "
        "이때 인기척에 깬 피해자 B가 '도둑이야'라고 소리치자, 피고인 A는 도망치기 위해 B의 얼굴과 턱을 주먹으로 3회 강하게 가격하여 B에게 턱뼈 골절 등 전치 3주의 병원 치료를 요하는 상처를 입혔다. "
        "피고인 A는 자신의 지문 등 범행 흔적이 남는 것을 막기 위해 소지하고 있던 일회용 라이터로 거실 소파의 천에 불을 붙였고, 불길은 소파 전체를 타고 올라가 거실 벽면과 천장 합성수지 마감재로 옮겨 붙어 집 전체로 연기가 치솟기 시작했다."
    )
}

# Official Standard Test Case 2: User-Provided Criminal Law Exam Case (Bribery Fraud & Misappropriation Case)
TEST_CASE_2 = {
    "case_id": "CASE_KCL1730_2026_BRIBERY_FRAUD_002",
    "title": "공무원 뇌물 전달 명목 금원 편취 및 丙의 죄책 사안",
    "fact_pattern": (
        "甲은 자신이 운영하는 회사의 관급공사 수주에 관한 편의를 제공받기 위하여 담당 공무원 乙에게 3,000만 원의 뇌물을 제공하기로 마음먹었다. "
        "甲은 평소 친분이 있던 친구 丙에게 “수의계약을 따오기 위해 이 돈을 乙에게 전달해 달라.”라고 말하면서 현금 3,000만 원을 건네주었다.\n"
        "그런데 丙은 甲으로부터 위 돈을 교부받기 전부터 개인적인 채무를 변제할 자금이 필요하였고, 甲으로부터 돈을 받으면 이를 乙에게 전달하지 않고 자신의 채무 변제에 사용할 생각이었다. "
        "丙은 이러한 내심의 의사를 숨긴 채 甲으로부터 위 3,000만 원을 교부받았고, 돈을 받은 직후 이를 자신의 채권자에게 채무 변제 명목으로 지급하였다.\n"
        "丙의 죄책을 논하시오."
    )
}

OFFICIAL_TEST_CASES = [TEST_CASE_1, TEST_CASE_2]

def main():
    parser = argparse.ArgumentParser(description="Run KCL 1,730 E2E Neuro-Symbolic Pipeline")
    parser.add_argument("--mode", choices=["dry-run", "vllm"], default="dry-run", help="Execution mode")
    parser.add_argument("--base-url", type=str, default=None, help="vLLM server base URL")
    parser.add_argument("--model", type=str, default=None, help="vLLM model identifier")
    parser.add_argument("--case-index", type=int, choices=[1, 2], default=None, help="Select official test case index (1 or 2)")
    parser.add_argument("--all-cases", action="store_true", help="Run all official test cases sequentially")
    parser.add_argument("--case-json", type=str, default=None, help="Custom input case JSON file path")
    parser.add_argument("--out-dir", type=str, default=str(PROJECT_ROOT / "data/e2e/output"), help="Output directory")

    args = parser.parse_args()

    if args.mode == "vllm" and (not args.base_url or not args.model):
        print("Error: vllm mode requires --base-url and --model arguments.")
        sys.exit(1)

    runner = KCL1730PipelineRunner(
        base_url=args.base_url if args.mode == "vllm" else None,
        model=args.model if args.mode == "vllm" else None
    )

    cases_to_run = []
    if args.case_json:
        cases_to_run.append(json.loads(Path(args.case_json).read_text(encoding="utf-8")))
    elif args.all_cases:
        cases_to_run = OFFICIAL_TEST_CASES
    elif args.case_index:
        cases_to_run.append(OFFICIAL_TEST_CASES[args.case_index - 1])
    else:
        # Default: Run both official test cases
        cases_to_run = OFFICIAL_TEST_CASES

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    for case_data in cases_to_run:
        result = runner.run_e2e(case_data)
        out_file = out_dir / f"{result['case_id']}_result.json"

        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"\n============================================================")
        print(f"📄 FINAL LEGAL REVIEW REPORT RENDERED FOR [{result['case_id']}]:")
        print(f"============================================================")
        print(result["final_report"])
        print(f"\nSaved execution result JSON to: {out_file}\n")

if __name__ == "__main__":
    main()
