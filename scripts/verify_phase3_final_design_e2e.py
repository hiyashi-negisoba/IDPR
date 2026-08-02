"""Gate final generation on the three general Phase-3 design improvements."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


KCL = "kcl_criminal_r10_p1_q1_ga"
USER = "CASE_KCL1730_2026_BRIBERY_FRAUD_002"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--previous-root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    checks: dict[str, bool] = {}

    kcl = load_json(args.run_root / "cases" / KCL / "issue_assessment.json")
    relations = kcl["symbolic_runtime"]["relations"]
    # A refuted completion issue must never become a completed/final offence.  Whether
    # the attempt itself is established still depends on every upstream element status;
    # preserve it for attempt review instead of making this E2E gate override a neural
    # element assessment.
    checks["kcl_art297_preserves_attempt_review_without_false_completion"] = (
        [KCL, "art297"] in relations.get("attempt_to_consider", [])
        and [KCL, "art297"] not in relations.get("offense_established", [])
        and [KCL, "art297"] not in relations.get("final_offense", [])
    )

    user_graphs = {
        row["sub_question_id"]: row["fact_graph"]
        for row in (
            json.loads(line)
            for line in (args.run_root / "fact_graphs.jsonl").read_text(encoding="utf-8").splitlines()
            if line.strip()
        )
    }
    transfers = user_graphs[USER].get("transfers", [])
    checks["user_property_transfer_is_grounded"] = any(
        item.get("transfer_mode") in {"보관위탁", "자발적교부"}
        and item.get("transfer_purpose") == "전달"
        for item in transfers
    )

    for case_id in (KCL, USER):
        current = load_json(args.run_root / "cases" / case_id / "answer.json")
        previous = load_json(args.previous_root / "cases" / case_id / "answer.json")
        current_sections = current["request"]["required_sections"]
        previous_sections = previous["request"]["required_sections"]
        checks[f"{case_id}_visibility_did_not_expand_materially"] = (
            len(current_sections) <= len(previous_sections) + 1
        )
        checks[f"{case_id}_answer_contract_present"] = bool(current.get("answer", {}).get("sections"))

    failures = sorted(name for name, passed in checks.items() if not passed)
    report = {
        "version": "1.0.0",
        "passed": not failures,
        "checks": checks,
        "failures": failures,
        "comparison_root": str(args.previous_root),
    }
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if failures:
        raise SystemExit(f"final design E2E comparison failed: {failures}")
    print(f"passed final design E2E comparison; wrote {args.out}")


if __name__ == "__main__":
    main()
