from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Mapping


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from idpr.generation import (  # noqa: E402
    compile_fraud_whole_irac_answer,
    render_long_form_markdown,
)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def parse_plan_argument(value: str) -> tuple[str, Path]:
    case_id, separator, raw_path = value.partition("=")
    if not separator or not case_id or not raw_path:
        raise argparse.ArgumentTypeError("plan must use CASE_ID=PATH")
    return case_id, Path(raw_path)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Replay validated M5 plans through the host-only whole-IRAC compiler."
    )
    parser.add_argument("--case-set", type=Path, required=True)
    parser.add_argument(
        "--plan",
        action="append",
        type=parse_plan_argument,
        required=True,
        metavar="CASE_ID=PATH",
    )
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()

    case_set = read_json(args.case_set)
    cases = {case["case_id"]: case for case in case_set["cases"]}
    seen: set[str] = set()
    for case_id, plan_path in args.plan:
        if case_id in seen:
            parser.error(f"duplicate case ID: {case_id}")
        seen.add(case_id)
        if case_id not in cases:
            parser.error(f"case set does not contain: {case_id}")
        plan = read_json(plan_path)
        if plan.get("case_id") != case_id:
            parser.error(f"plan case_id differs for {case_id}: {plan_path}")
        answer = compile_fraud_whole_irac_answer(
            plan=plan,
            case=cases[case_id],
        )
        output_dir = args.output_root / case_id
        write_json(output_dir / "m5_whole_irac_answer.json", answer)
        (output_dir / "m5_whole_irac_answer.md").write_text(
            render_long_form_markdown(answer),
            encoding="utf-8",
        )

    print(
        json.dumps(
            {
                "case_count": len(seen),
                "model_calls": 0,
                "output_root": str(args.output_root),
                "status": "completed",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
