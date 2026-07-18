from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT))

from idpr.rulegen.scallop_runtime import (  # noqa: E402
    run_scenario,
    runtime_version,
    sha256_file,
)
from scripts.build_fraud_full_scallop import (  # noqa: E402
    FRAUD_ROOT,
    MANIFEST_PATH,
    OUTPUT_PATH,
    RULE_IR_PATH,
    build,
    read_json,
)


GOLDEN_PATH = FRAUD_ROOT / "fraud_scallop_golden_cases.json"
REPORT_PATH = FRAUD_ROOT / "fraud_scallop_runtime_report.json"
DEFAULT_SCLI = PROJECT_ROOT / "tools/scallop/scli-0.2.4-linux-x86_64"
QUERY_RELATIONS = (
    "fraud_elements_satisfied",
    "fraud_established",
    "fraud_not_established",
    "fraud_undetermined",
    "fraud_conflict",
)


def expand_scenarios(fixture: dict[str, Any]) -> list[dict[str, Any]]:
    base = fixture["base_assessments"]
    scenarios: list[dict[str, Any]] = []
    for raw in fixture["scenarios"]:
        overrides = raw.get("assessment_status_overrides", {})
        assessments = [
            {
                "card_id": item["card_id"],
                "status": overrides.get(item["card_id"], item["status"]),
                "provable": True,
            }
            for item in base
        ]
        assessments.extend(dict(item) for item in raw.get("additional_assessments", []))
        for index, assessment in enumerate(assessments, 1):
            assessment.setdefault(
                "assessment_id", f"{raw['scenario_id']}.assessment.{index:03d}"
            )
            assessment.setdefault("provable", True)
        selected = list(dict.fromkeys(item["card_id"] for item in assessments))
        selected.extend(raw.get("selected_without_assessment", []))
        scenarios.append(
            {
                "scenario_id": raw["scenario_id"],
                **raw["actors"],
                "selected_card_ids": selected,
                "assessments": assessments,
                "distinct_entities": raw.get("distinct_entities", []),
                "close_case": raw["close_case"],
                "expected_nonempty": raw["expected_nonempty"],
            }
        )
    return scenarios


def run_all(
    *, work_dir: Path | None = None, report_path: Path | None = None
) -> dict[str, Any]:
    manifest = build()
    rule_ir = read_json(RULE_IR_PATH)
    fixture = read_json(GOLDEN_PATH)
    scli_path = Path(os.environ.get("SCALLOP_SCLI", DEFAULT_SCLI))
    if not scli_path.is_file():
        raise FileNotFoundError(
            f"Scallop runtime not found at {scli_path}; run scripts/install_scallop_runtime.sh"
        )
    expected_sha = manifest["runtime_contract"]["sha256"]
    actual_sha = sha256_file(scli_path)
    if actual_sha != expected_sha:
        raise RuntimeError(f"unexpected scli checksum: {actual_sha}")

    compiled_source = OUTPUT_PATH.read_text(encoding="utf-8")
    runtime_work_dir = work_dir or PROJECT_ROOT / ".cache/scallop/fraud_golden"
    scenario_reports: list[dict[str, Any]] = []
    failures: list[str] = []
    for scenario in expand_scenarios(fixture):
        results = run_scenario(
            rule_ir=rule_ir,
            compiled_source=compiled_source,
            scenario=scenario,
            query_relations=QUERY_RELATIONS,
            scli_path=scli_path,
            work_dir=runtime_work_dir,
        )
        observed = {
            relation: result["nonempty"] for relation, result in results.items()
        }
        expected = scenario["expected_nonempty"]
        if observed != expected:
            failures.append(
                f"{scenario['scenario_id']}: expected {expected}, observed {observed}"
            )
        scenario_reports.append(
            {
                "scenario_id": scenario["scenario_id"],
                "expected_nonempty": expected,
                "observed_nonempty": observed,
                "status": "pass" if observed == expected else "fail",
            }
        )

    report = {
        "version": "1.0.0",
        "status": "pass" if not failures else "fail",
        "runtime": {
            "version": runtime_version(scli_path),
            "sha256": actual_sha,
        },
        "compiled_manifest": str(MANIFEST_PATH.relative_to(PROJECT_ROOT)),
        "compiled_sha256": sha256_file(OUTPUT_PATH),
        "golden_cases": str(GOLDEN_PATH.relative_to(PROJECT_ROOT)),
        "scenario_count": len(scenario_reports),
        "scenarios": scenario_reports,
        "failures": failures,
    }
    destination = report_path or REPORT_PATH
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if failures:
        raise AssertionError("\n".join(failures))
    return report


def main() -> None:
    print(json.dumps(run_all(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
