#!/usr/bin/env python3
"""Compile authored doctrine alternatives around each reviewed live variant card."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.rulebase.cards import card_corpus


def _documents(root: Path) -> list[tuple[Path, dict[str, Any]]]:
    output = []
    for path in sorted(root.rglob("*.json")):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
        if isinstance(value, dict) and isinstance(value.get("cards"), list):
            output.append((path, value))
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rulegen-root", type=Path, default=ROOT / "data/rulegen")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    live = [card for card in card_corpus().cards if card.variant_group]
    live_counts = Counter(card.variant_group for card in live)
    by_group: dict[str, list[dict[str, Any]]] = {}
    source_paths: dict[str, set[str]] = {}
    for path, document in _documents(args.rulegen_root):
        for raw in document["cards"]:
            group = raw.get("variant_group")
            if not group or raw.get("doctrinal_status") != "disputed":
                continue
            if raw.get("formalization") not in {"policy_variant", "context_only"}:
                continue
            proposition = str(raw.get("proposition", "")).strip()
            if not proposition:
                continue
            item = {"card_id": str(raw.get("id", "")), "position": proposition}
            if item not in by_group.setdefault(str(group), []):
                by_group[str(group)].append(item)
                source_paths.setdefault(str(group), set()).add(str(path.relative_to(ROOT)))

    disputes = []
    for card in live:
        # More than one promoted card means the group is not a single-choice route (or
        # its review normalization is incomplete).  Do not invent an adopted position.
        if live_counts[card.variant_group] != 1:
            continue
        positions = by_group.get(str(card.variant_group), [])
        all_positions = list(dict.fromkeys([value["position"] for value in positions]))
        if card.proposition not in all_positions:
            all_positions.append(card.proposition)
        if len(all_positions) < 2:
            continue
        why = (
            "검수된 판례 태도를 채택한다."
            if card.doctrinal_status == "precedent_position"
            else "검수된 core 법리로 채택된 견해를 따른다."
        )
        disputes.append(
            {
                "dispute_id": f"dispute.{card.variant_group}",
                "label": "이 쟁점에 관한 견해 대립",
                "trigger_card_id": card.id,
                "variant_group": card.variant_group,
                "positions": all_positions,
                "adopted": card.proposition,
                "why_adopted": why,
                "origin": "authored_doctrine",
                "source_paths": sorted(source_paths.get(str(card.variant_group), set())),
            }
        )
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(
            {
                "version": 1,
                "construction": "reviewed_live_variant_plus_authored_doctrine_alternatives",
                "dispute_count": len(disputes),
                "disputes": disputes,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps({"disputes": len(disputes)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
