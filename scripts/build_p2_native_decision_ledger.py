"""Fold a unit's approved human card decisions into an auditable RuleIR input ledger.

The approval asset is the only source of legal judgment.  This script validates it
against the manifest review contract and the generated review queue, resolves unit
cross-references against declared registries, and reports every gap instead of
inventing a fallback.  Nothing here is crime-specific; all names come from data.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
P2_MANIFEST = ROOT / "data/rulegen/p2/p2_native_unit_manifest.json"
REGISTRY_MANIFEST = ROOT / "data/rulegen/rule_ir_registry_manifest.json"
QUEUE_DIR = ROOT / "data/rulegen/p2/native_review"
LEDGER_DIR = ROOT / "data/rulegen/p2/native_review"
AUDIT_DIR = ROOT / "docs/review/p2"

PLACEMENT_FIELDS = (
    "role",
    "component_id",
    "component_join",
    "track_id",
    "refers_to_unit",
    "rationale",
    "proposition_rewrite",
)


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected object")
    return payload


def declared_unit_ids() -> set[str]:
    units = {item["unit_id"] for item in read_json(P2_MANIFEST)["units"]}
    if REGISTRY_MANIFEST.is_file():
        units |= {item["unit_id"] for item in read_json(REGISTRY_MANIFEST)["units"]}
    return units


def placements(card: dict[str, Any]) -> list[dict[str, Any]]:
    """A card contributes one placement, or several when the reviewer split it."""
    if card["decision"] == "split":
        return [{**part, "decision": card["decision"]} for part in card["parts"]]
    return [{key: card.get(key) for key in (*PLACEMENT_FIELDS, "decision", "part_id")}]


def validate(
    approval: dict[str, Any],
    queue: dict[str, Any],
    contract: dict[str, Any],
    unit_ids: set[str],
) -> tuple[list[str], list[dict[str, Any]]]:
    problems: list[str] = []
    tracks = {item["track_id"] for item in approval["track_vocabulary"]}
    queue_ids = [card["card_id"] for card in queue["cards"]]
    decided_ids = [card["card_id"] for card in approval["cards"]]

    problems.extend(f"decision missing for queue card: {card_id}"
                    for card_id in queue_ids if card_id not in set(decided_ids))
    problems.extend(f"decision for a card outside the queue: {card_id}"
                    for card_id in decided_ids if card_id not in set(queue_ids))
    problems.extend(f"duplicate decision: {card_id}"
                    for card_id, count in Counter(decided_ids).items() if count > 1)

    unresolved: list[dict[str, Any]] = []
    for card in approval["cards"]:
        if card["decision"] not in contract["allowed_decisions"]:
            problems.append(f"{card['card_id']}: decision not allowed: {card['decision']}")
        if card["decision"] == "split" and len(card.get("parts", [])) < 2:
            problems.append(f"{card['card_id']}: split needs at least two parts")
        for placement in placements(card):
            label = f"{card['card_id']}"
            if placement.get("part_id"):
                label = f"{label}#{placement['part_id']}"
            role = placement.get("role")
            if role not in contract["allowed_roles"]:
                problems.append(f"{label}: role not allowed: {role}")
            if role == "context_only":
                continue
            if placement.get("component_join") not in contract["allowed_component_joins"]:
                problems.append(f"{label}: join not allowed: {placement.get('component_join')}")
            if not placement.get("component_id"):
                problems.append(f"{label}: component_id required for role {role}")
            if placement.get("track_id") not in tracks:
                problems.append(f"{label}: track not declared: {placement.get('track_id')}")
            if not placement.get("rationale"):
                problems.append(f"{label}: rationale required")
            if card["decision"] == "rewrite" and not placement.get("proposition_rewrite"):
                problems.append(f"{label}: rewrite requires proposition_rewrite")
            target = placement.get("refers_to_unit")
            if target and target not in unit_ids:
                unresolved.append({
                    "card_id": card["card_id"],
                    "part_id": placement.get("part_id"),
                    "refers_to_unit": target,
                    "status": "predicate_ir_missing",
                })
    return problems, unresolved


def build_ledger(unit_id: str) -> dict[str, Any]:
    manifest = read_json(P2_MANIFEST)
    contract = manifest["review_contract"]
    queue = read_json(QUEUE_DIR / f"{unit_id}_review_queue.json")
    approval_path = QUEUE_DIR / f"{unit_id}_approved_decisions.json"
    approval = read_json(approval_path)
    if approval["unit_id"] != unit_id:
        raise ValueError(f"approval asset declares a different unit: {approval['unit_id']}")

    problems, unresolved = validate(approval, queue, contract, declared_unit_ids())
    queue_index = {card["card_id"]: card for card in queue["cards"]}

    components: dict[str, dict[str, Any]] = {}
    excluded: list[dict[str, Any]] = []
    stats: Counter[str] = Counter()
    for card in approval["cards"]:
        stats[f"decision_{card['decision']}"] += 1
        if card.get("inherited_decision_group"):
            stats["inherited"] += 1
        for placement in placements(card):
            if placement.get("role") == "context_only":
                excluded.append({
                    "card_id": card["card_id"],
                    "reason": placement.get("rationale"),
                })
                stats["context_only_placements"] += 1
                continue
            key = f"{placement['track_id']}::{placement['component_id']}"
            entry = components.setdefault(key, {
                "track_id": placement["track_id"],
                "component_id": placement["component_id"],
                "roles": [],
                "joins": [],
                "refers_to_units": [],
                "norm_card_ids": [],
            })
            entry["roles"].append(placement["role"])
            # bar/boundary/waiver attach to an element without joining its conjunction,
            # so only component placements define how the element is satisfied.
            if placement["role"] == "component":
                entry["joins"].append(placement["component_join"])
            if placement.get("refers_to_unit"):
                entry["refers_to_units"].append(placement["refers_to_unit"])
            entry["norm_card_ids"].append(card["card_id"])
            stats["placements"] += 1

    for entry in components.values():
        for field in ("roles", "joins", "refers_to_units"):
            entry[field] = sorted(set(entry[field]))
        entry["norm_card_ids"] = sorted(set(entry["norm_card_ids"]))
        if len(entry["joins"]) > 1:
            problems.append(
                f"{entry['track_id']}::{entry['component_id']}: "
                f"conflicting joins {entry['joins']}"
            )

    stats["components"] = len(components)
    stats["unresolved_unit_references"] = len(unresolved)
    stats["queue_cards"] = len(queue["cards"])
    return {
        "version": "1.0.0",
        "unit_id": unit_id,
        "law_snapshot": queue["law_snapshot"],
        "approval_document": str(approval_path.relative_to(ROOT)),
        "approval_sha256": hashlib.sha256(approval_path.read_bytes()).hexdigest(),
        "approved_on": approval["approved_on"],
        "status": "ready_for_rule_ir" if not problems else "blocked",
        "problems": problems,
        "unresolved_unit_references": unresolved,
        "excluded_cards": excluded,
        "components": [components[key] for key in sorted(components)],
        "stats": dict(sorted(stats.items())),
    }


def render_audit(ledger: dict[str, Any]) -> str:
    lines = [
        f"# {ledger['unit_id']} RuleIR 승인 원장 감사",
        "",
        f"- status: `{ledger['status']}`",
        f"- approval: `{ledger['approval_document']}`",
        f"- approval SHA-256: `{ledger['approval_sha256']}`",
        f"- law snapshot: `{ledger['law_snapshot']['law_snapshot_id']}`",
        f"- queue cards: {ledger['stats']['queue_cards']}",
        f"- components: {ledger['stats']['components']}",
        f"- context_only 제외: {ledger['stats'].get('context_only_placements', 0)}",
        f"- 미해결 unit 참조: {ledger['stats']['unresolved_unit_references']}",
        "",
        "승인된 판정만 RuleIR 입력이 된다. 미해결 참조는 추측하지 않고 `predicate_ir_missing`으로 보고한다.",
        "",
        "## 계약 위반",
        "",
    ]
    lines.append("없음." if not ledger["problems"] else "")
    lines.extend(f"- {item}" for item in ledger["problems"])
    lines.extend(["", "## 미해결 unit 참조", ""])
    if not ledger["unresolved_unit_references"]:
        lines.append("없음.")
    for item in ledger["unresolved_unit_references"]:
        label = item["card_id"] + (f"#{item['part_id']}" if item["part_id"] else "")
        lines.append(f"- `{label}` → `{item['refers_to_unit']}` ({item['status']})")
    lines.extend(["", "## component 구성", "", "| track | component | role | join | 카드 수 | 참조 |", "|---|---|---|---|---:|---|"])
    for entry in ledger["components"]:
        lines.append(
            f"| `{entry['track_id']}` | `{entry['component_id']}` | "
            f"{', '.join(entry['roles'])} | {', '.join(entry['joins'])} | "
            f"{len(entry['norm_card_ids'])} | {', '.join(entry['refers_to_units']) or '-'} |"
        )
    lines.extend(["", "## RuleIR에서 제외된 카드", ""])
    if not ledger["excluded_cards"]:
        lines.append("없음.")
    for item in ledger["excluded_cards"]:
        lines.append(f"- `{item['card_id']}`: {item['reason']}")
    lines.append("")
    return "\n".join(lines)


def write_outputs(unit_id: str) -> tuple[Path, Path, dict[str, Any]]:
    ledger = build_ledger(unit_id)
    ledger_path = LEDGER_DIR / f"{unit_id}_decision_ledger.json"
    ledger_path.write_text(
        json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    audit_path = AUDIT_DIR / f"{unit_id}_decision_audit.md"
    audit_path.write_text(render_audit(ledger), encoding="utf-8")
    return ledger_path, audit_path, ledger


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--unit", required=True)
    args = parser.parse_args()
    ledger_path, audit_path, ledger = write_outputs(args.unit)
    print(f"ledger={ledger_path.relative_to(ROOT)}")
    print(f"audit={audit_path.relative_to(ROOT)}")
    print(json.dumps(ledger["stats"], ensure_ascii=False, sort_keys=True))
    for problem in ledger["problems"]:
        print(f"problem: {problem}")


if __name__ == "__main__":
    main()
