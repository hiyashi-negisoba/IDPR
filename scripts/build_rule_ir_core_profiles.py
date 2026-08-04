#!/usr/bin/env python3
"""Build the minimal model-input projection for every registered RuleIR unit."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.rulegen.core_profile import build_core_profiles  # noqa: E402


def main() -> None:
    payload = build_core_profiles(ROOT)
    target = ROOT / "data/rulegen/rule_ir_core_profiles.json"
    target.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    detailed = sum(
        item["detailed_card_predicates"]["count"]
        for item in payload["units"].values()
    )
    core = sum(
        len(item["model_input_predicates"])
        for item in payload["units"].values()
    )
    print(f"units={len(payload['units'])} detailed={detailed} core={core} path={target}")


if __name__ == "__main__":
    main()
