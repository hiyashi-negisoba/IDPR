"""Materialise an approved P2 proposal set as the decision-ledger input asset.

The legal judgments live in Markdown proposal tables and an external JSON config.
This parser is deliberately unit-agnostic: it receives all paths, track vocabulary,
table defaults and exact rewrite text as data, and refuses missing or duplicate cards.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
QUEUE_DIR = ROOT / "data/rulegen/p2/native_review"
DECISIONS = {"approve", "rewrite", "context_only", "split", "reject"}
ROLES = {"component", "bar", "boundary", "waiver", "post_outcome", "context_only"}


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected object")
    return payload


def cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def table_rows(paths: list[Path]) -> dict[int, dict[str, Any]]:
    rows: dict[int, dict[str, Any]] = {}
    for path in paths:
        try:
            source_path = path.relative_to(ROOT)
        except ValueError:
            source_path = path
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            values = cells(line)
            if not values or not values[0].isdigit():
                continue
            decision_positions = [i for i, value in enumerate(values) if value in DECISIONS]
            if not decision_positions:
                continue
            number = int(values[0])
            if number in rows:
                raise ValueError(f"duplicate card number {number}: {path}:{line_number}")
            # context_only is both a decision and a role in the full table shape;
            # the first occurrence is always the decision column.
            decision_at = decision_positions[0]
            tail = values[decision_at + 1:]
            row: dict[str, Any] = {
                "decision": values[decision_at],
                "rationale": tail[-1] if tail else "",
                "source": f"{source_path}:{line_number}",
            }
            if tail and tail[0] in ROLES:
                row["role"] = tail[0]
                if tail[0] != "context_only":
                    if len(tail) not in {4, 5}:
                        raise ValueError(f"unrecognised placement columns: {path}:{line_number}")
                    component, join = [part.strip() for part in tail[1].split("/", 1)]
                    row.update({
                        "component_id": component,
                        "component_join": join,
                        "track_id": tail[2],
                        "refers_to_unit": (
                            None if len(tail) == 4 or tail[3] == "-"
                            else tail[3].strip("`")
                        ),
                    })
            rows[number] = row
    return rows


def group_defaults(config: dict[str, Any]) -> dict[int, dict[str, Any]]:
    result: dict[int, dict[str, Any]] = {}
    for group in config.get("placement_defaults", []):
        placement = {key: value for key, value in group.items() if key != "card_numbers"}
        for number in group["card_numbers"]:
            if number in result:
                raise ValueError(f"duplicate placement default for card number {number}")
            result[number] = placement
    return result


def grouped_decisions(config: dict[str, Any]) -> dict[int, dict[str, Any]]:
    """Expand compact machine-reviewed card groups into numbered decisions."""
    result: dict[int, dict[str, Any]] = {}
    for group in config.get("decision_groups", []):
        decision = {key: value for key, value in group.items() if key != "card_numbers"}
        for number in group["card_numbers"]:
            if number in result:
                raise ValueError(f"duplicate grouped decision for card number {number}")
            result[number] = dict(decision)
    return result


def build(config_path: Path) -> dict[str, Any]:
    config = read_json(config_path)
    unit_id = config["unit_id"]
    queue = read_json(QUEUE_DIR / f"{unit_id}_review_queue.json")
    queue_by_number = {index: card for index, card in enumerate(queue["cards"], 1)}
    proposal_documents = config.get("proposal_documents", [])
    proposal_paths = [ROOT / path for path in proposal_documents]
    parsed = table_rows(proposal_paths) if proposal_paths else grouped_decisions(config)
    defaults = group_defaults(config)
    rewrites = {int(number): text for number, text in config.get("proposition_rewrites", {}).items()}

    expected = set(queue_by_number)
    if set(parsed) != expected:
        raise ValueError(
            f"proposal coverage mismatch: missing={sorted(expected - set(parsed))}, "
            f"extra={sorted(set(parsed) - expected)}"
        )

    cards: list[dict[str, Any]] = []
    for number in sorted(parsed):
        source_card = queue_by_number[number]
        row = {**defaults.get(number, {}), **parsed[number]}
        row.pop("source", None)
        decision = row["decision"]
        if decision == "context_only":
            row = {"decision": decision, "role": "context_only", "rationale": row["rationale"]}
        elif "role" not in row:
            raise ValueError(f"card {number}: no placement in table or config")
        if decision == "rewrite":
            if number not in rewrites:
                raise ValueError(f"card {number}: exact proposition rewrite missing")
            row["proposition_rewrite"] = rewrites[number]
        row = {"card_id": source_card["card_id"], **row}
        inherited = source_card.get("inherited_doctrine")
        if inherited:
            row["inherited_decision_group"] = inherited["variant_group"]
        cards.append(row)

    return {
        "version": "1.0.0",
        "authority": config.get("authority", "human_legal_review"),
        "unit_id": unit_id,
        "approved_on": config["approved_on"],
        "approval_basis": [
            *proposal_documents,
            *([config["legal_gate"]] if config.get("legal_gate") else []),
            str(config_path.relative_to(ROOT)),
        ],
        "policy": config["policy"],
        "track_vocabulary": config["track_vocabulary"],
        "cards": cards,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    config_path = args.config if args.config.is_absolute() else ROOT / args.config
    payload = build(config_path)
    output = QUEUE_DIR / f"{payload['unit_id']}_approved_decisions.json"
    output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"approval={output.relative_to(ROOT)} cards={len(payload['cards'])}")


if __name__ == "__main__":
    main()
