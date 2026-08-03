"""P2 RuleIR-native unit → Scallop 컴파일 (API 0회).

`build_p2_native_rule_ir.py`가 조립한 후보 RuleIR을 `compile_rule_ir`로 `.scl`에 옮긴다.
사기·재산죄 트랙과 같은 컴파일러를 쓴다 — 새로 만들지 않는다. unit 이름 외에는 아무것도
이 파일에 하드코딩하지 않으며, 대상 unit은 인자로 받는다.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from idpr.rulegen import compile_rule_ir  # noqa: E402

from scripts.build_p2_native_rule_ir import (  # noqa: E402
    OUT_DIR,
    UNIT_MANIFEST,
    commentary_index,
    read_json,
)

COMPILED_DIR = ROOT / "rules/generated"


def compile_unit(unit_id: str, out_dir: Path = COMPILED_DIR) -> Path:
    manifest = read_json(UNIT_MANIFEST)
    entry = next(item for item in manifest["units"] if item["unit_id"] == unit_id)
    rule_ir = read_json(OUT_DIR / f"{unit_id}_rule_ir_candidate.json")
    card_set = read_json(OUT_DIR / f"{unit_id}_norm_card_set.json")
    source = compile_rule_ir(rule_ir, commentary_index(entry["articles"]), card_set)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"p2_{unit_id}_v1_candidate.scl"
    out_path.write_text(source, encoding="utf-8")
    return out_path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--unit", required=True)
    parser.add_argument("--out-dir", type=Path, default=COMPILED_DIR)
    args = parser.parse_args()
    out_path = compile_unit(args.unit, args.out_dir)
    source = out_path.read_text(encoding="utf-8")
    print(f"{args.unit}: {len(source):,d} bytes, {len(source.splitlines()):,d} lines "
          f"-> {out_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
