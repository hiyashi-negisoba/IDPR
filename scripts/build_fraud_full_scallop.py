from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from idpr.rulegen import compile_rule_ir, validate_full_rule_ir_generation  # noqa: E402
from idpr.rulegen.scallop_runtime import sha256_file  # noqa: E402


FRAUD_ROOT = PROJECT_ROOT / "data/rulegen/fraud"
RULE_IR_PATH = FRAUD_ROOT / "fraud_full_rule_ir_candidate_unreviewed.json"
NORM_CARD_PATH = FRAUD_ROOT / "fraud_core_norm_card_set.json"
COMMENTARY_PATH = PROJECT_ROOT / "data/commentary/kcl_criminal_v1_commentary_chunks.jsonl"
APPROVAL_PATH = FRAUD_ROOT / "fraud_full_rule_ir_post_sol_human_decision.json"
OUTPUT_PATH = PROJECT_ROOT / "rules/generated/fraud_article347_full_v1.scl"
MANIFEST_PATH = FRAUD_ROOT / "fraud_scallop_compile_manifest.json"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def build() -> dict[str, Any]:
    rule_ir = read_json(RULE_IR_PATH)
    norm_cards = read_json(NORM_CARD_PATH)
    approval = read_json(APPROVAL_PATH)
    if approval.get("status") != "approved_for_scallop_runtime":
        raise RuntimeError("post-Sol human approval is required before Scallop compilation")

    allowed_comment_ids = set(rule_ir["source_scope"]["comment_ids"])
    commentary = {
        row["comment_id"]: row
        for row in read_jsonl(COMMENTARY_PATH)
        if row["comment_id"] in allowed_comment_ids
    }
    validate_full_rule_ir_generation(rule_ir, commentary, norm_cards)
    source = compile_rule_ir(rule_ir, commentary, norm_cards)
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(source, encoding="utf-8")

    manifest = {
        "version": "1.0.0",
        "status": "compiled",
        "rule_set_id": rule_ir["rule_set_id"],
        "compiler": "idpr.rulegen.compile_rule_ir",
        "model_output_executed_directly": False,
        "human_approval": str(APPROVAL_PATH.relative_to(PROJECT_ROOT)),
        "inputs": {
            str(path.relative_to(PROJECT_ROOT)): sha256_file(path)
            for path in (RULE_IR_PATH, NORM_CARD_PATH, APPROVAL_PATH)
        },
        "output": {
            "path": str(OUTPUT_PATH.relative_to(PROJECT_ROOT)),
            "sha256": sha256_file(OUTPUT_PATH),
        },
        "counts": {
            "norm_cards": len(norm_cards["cards"]),
            "predicates": len(rule_ir["predicates"]),
            "rules": len(rule_ir["rules"]),
        },
        "runtime_contract": {
            "name": "scli",
            "version": "0.2.4",
            "asset": "scli-0.2.4-linux-x86_64",
            "sha256": "8c5ec86fcdb0dbd55698eff7570ac7396d0b0878e601207f868d61f9d6482b9a",
        },
    }
    MANIFEST_PATH.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return manifest


def main() -> None:
    manifest = build()
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
