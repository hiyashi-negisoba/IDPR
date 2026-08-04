"""Generate deterministic JSON and Markdown audits for the RuleIR-native registry."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.rulegen.registry import audit_rule_ir_assets  # noqa: E402


def render_markdown(report: dict) -> str:
    lines = [
        "# RuleIR registry audit",
        "",
        f"- Status: `{report['status']}`",
        f"- Scope: {report['scope']}",
        "",
        "| Unit | Articles | Commentary inputs | System inputs | Queries | Result |",
        "|---|---|---:|---:|---|---|",
    ]
    for unit in report["units"]:
        result = "pass" if not unit["errors"] else "; ".join(unit["errors"])
        values = {
            "unit_id": unit["unit_id"],
            "articles": ", ".join(unit.get("article_ids", [])) or "-",
            "commentary_input_count": unit.get("commentary_input_count", "-"),
            "system_input_count": unit.get("system_input_count", "-"),
            "queries": ", ".join(unit.get("query_relations", [])) or "-",
            "result": result.replace("|", "\\|"),
        }
        lines.append(
            "| {unit_id} | {articles} | {commentary_input_count} | {system_input_count} | "
            "{queries} | {result} |".format(**values)
        )
    if report["errors"]:
        lines.extend(["", "## Errors", "", *[f"- {item}" for item in report["errors"]]])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-out", type=Path, default=ROOT / "data/rulegen/rule_ir_registry_audit.json")
    parser.add_argument("--markdown-out", type=Path, default=ROOT / "docs/2026-08-03_rule_ir_registry_audit.md")
    args = parser.parse_args()
    report = audit_rule_ir_assets(ROOT)
    for path, content in (
        (args.json_out, json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"),
        (args.markdown_out, render_markdown(report)),
    ):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    print(f"{report['status']}: {len(report['units'])} units, {len(report['errors'])} errors")
    return 0 if report["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
