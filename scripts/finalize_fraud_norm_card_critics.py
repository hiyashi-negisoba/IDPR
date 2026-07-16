from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from idpr.rulegen import validate_rulegen_critique  # noqa: E402

from scripts.run_fraud_norm_card_critics import (  # noqa: E402
    RUN_ROOT,
    TRACKED_ROOT,
    build_jobs,
)
from scripts.run_fraud_norm_card_merge import MODULE_PREFIXES  # noqa: E402
from scripts.run_fraud_rulegen_critics import read_json  # noqa: E402
from scripts.run_fraud_rulegen_pilot import write_json  # noqa: E402


RUN_ID = "fraud_norm_cards_critic_v4_final"
# The retry reused RUN_ID and overwrote its usage manifest. These cumulative
# values come from the two validated console summaries retained in the work log.
CUMULATIVE_USAGE = {
    "api_calls": 18,
    "prompt_tokens": 403_492,
    "completion_tokens": 27_741,
    "reasoning_tokens": 7_452,
    "total_tokens": 431_233,
    "invalid_contract_responses": 2,
}


def main() -> None:
    jobs, metadata = build_jobs(list(MODULE_PREFIXES), 50, 20_000)
    source_root = RUN_ROOT / RUN_ID / "sol"
    output_root = TRACKED_ROOT / RUN_ID
    findings_by_type: Counter[str] = Counter()
    findings_by_severity: Counter[str] = Counter()
    findings_by_module: Counter[str] = Counter()
    verdicts: Counter[str] = Counter()
    reports: list[dict[str, Any]] = []

    for job in jobs:
        meta = metadata[job.request_id]
        report = read_json(source_root / f"{job.request_id}.json")
        validate_rulegen_critique(
            report,
            expected_stage="norm_card_set",
            expected_target_id=meta["target_id"],
            allowed_source_refs=meta["allowed_source_refs"],
        )
        write_json(output_root / f"{job.request_id}.json", report)
        verdicts[report["verdict"]] += 1
        for finding in report["findings"]:
            findings_by_type[finding["type"]] += 1
            findings_by_severity[finding["severity"]] += 1
            findings_by_module[meta["module"]] += 1
        reports.append(
            {
                "request_id": job.request_id,
                "module": meta["module"],
                "part": meta["part"],
                "cards": meta["cards"],
                "card_ids": meta["card_ids"],
                "verdict": report["verdict"],
                "findings": len(report["findings"]),
                "path": str(
                    (
                        output_root / f"{job.request_id}.json"
                    ).relative_to(PROJECT_ROOT)
                ),
            }
        )

    manifest = {
        "version": "1.0.0",
        "run_id": RUN_ID,
        "status": "draft",
        "stage": "norm_card_set",
        "all_valid": True,
        "reports": reports,
        "totals": {
            "reports": len(reports),
            "cards": sum(report["cards"] for report in reports),
            "findings": sum(report["findings"] for report in reports),
            "verdicts": dict(sorted(verdicts.items())),
            "findings_by_type": dict(sorted(findings_by_type.items())),
            "findings_by_severity": dict(sorted(findings_by_severity.items())),
            "findings_by_module": dict(sorted(findings_by_module.items())),
        },
        "cumulative_usage": CUMULATIVE_USAGE,
        "audit_notes": [
            "v1 findings were invalidated by partial-target source-scope leakage.",
            "v2 and v3 were intermediate structural audits, not final card audits.",
            "The first v4 response and its retry used missing_variant before the "
            "critique contract admitted that precise finding type.",
            "Sol reports are advisory and do not establish legal correctness.",
        ],
    }
    write_json(output_root / "manifest.json", manifest)
    write_json(output_root / "run.json", manifest)
    print(json.dumps(manifest["totals"], ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
