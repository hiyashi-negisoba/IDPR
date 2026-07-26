"""재산죄 RuleIR → Scallop 컴파일 (API 0회).

`build_property_rule_ir.py`가 만든 RuleIR 후보 10개를 `compile_rule_ir`로 `.scl`에 옮긴다.
사기 트랙(`build_fraud_full_scallop.py`)과 같은 컴파일러를 쓴다 — 새로 만들지 않는다.
`test_property_rule_ir.py`가 이 산출물을 재계산해 바이트 단위로 비교하므로, RuleIR을
다시 조립한 뒤에는(레벨·역할표를 고쳤을 때) 이 스크립트도 다시 돌려야 한다.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from idpr.rulegen import compile_rule_ir  # noqa: E402

from scripts.build_property_core_norm_card_sets import commentary_index  # noqa: E402
from scripts.build_property_rule_ir import (  # noqa: E402
    DEFERRED_UNITS,
    OUT_DIR,
    UNIT_MANIFEST,
    UNITS,
    read_json,
)

COMPILED_DIR = ROOT / "rules/generated"


def main() -> None:
    manifest = read_json(UNIT_MANIFEST)
    for entry in manifest["units"]:
        unit = entry["issue_tag"]
        if unit in DEFERRED_UNITS:
            print(f"  {unit:36s} 이월(절차 레이어) — 컴파일 안 함")
            continue
        rule_ir: dict[str, Any] = read_json(OUT_DIR / f"{unit}_rule_ir_candidate.json")
        card_set = read_json(UNITS / f"{unit}.json")
        commentary: dict[str, Any] = {}
        for article in entry["articles"]:
            chunks, _ = commentary_index(article)
            commentary.update(chunks)
        source = compile_rule_ir(rule_ir, commentary, card_set)
        out_path = COMPILED_DIR / f"property_{unit}_v1_candidate.scl"
        out_path.write_text(source, encoding="utf-8")
        print(f"  {unit:36s} {len(source):8,d} bytes -> {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
