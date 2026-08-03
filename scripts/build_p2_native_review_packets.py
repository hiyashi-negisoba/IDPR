"""Build source-complete human legal-review packets for one manifest-declared P2 unit."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "data/rulegen/p2/p2_native_unit_manifest.json"
SOURCE_DIR = ROOT / "data/rulegen/p2/rule_ir_units"
QUEUE_DIR = ROOT / "data/rulegen/p2/native_review"
PACKET_DIR = ROOT / "docs/review/p2"
DOCTRINE_LEDGER = ROOT / "data/rulegen/p2/결정C_구조화원장.json"


def read_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected object")
    return payload


def unit_definition(manifest: dict[str, Any], unit_id: str) -> dict[str, Any]:
    matches = [item for item in manifest["units"] if item["unit_id"] == unit_id]
    if len(matches) != 1:
        raise ValueError(f"unit must occur exactly once in manifest: {unit_id}")
    return matches[0]


def cards_for_unit(unit: dict[str, Any]) -> list[dict[str, Any]]:
    articles = tuple(unit["articles"])
    cards: list[dict[str, Any]] = []
    seen: set[str] = set()
    for bundle in unit["source_bundles"]:
        payload = read_json(SOURCE_DIR / f"{bundle}_unit.json")
        for card in payload["cards"]:
            card_id = card["id"]
            if not any(
                card_id.startswith(article) and card_id[len(article):len(article) + 1] in {".", "_"}
                for article in articles
            ):
                continue
            if card_id in seen:
                raise ValueError(f"duplicate card selected for {unit['unit_id']}: {card_id}")
            seen.add(card_id)
            cards.append(card)
    return sorted(cards, key=lambda item: item["id"])


def inherited_doctrine_decisions(unit: dict[str, Any]) -> list[dict[str, Any]]:
    if not DOCTRINE_LEDGER.is_file():
        return []
    ledger = read_json(DOCTRINE_LEDGER)
    articles = set(unit["articles"])
    linked_groups = set(unit.get("inherited_decision_groups", []))
    return [
        {
            "number": item["number"],
            "article": item["article"],
            "variant_group": item["variant_group"],
            "resolution": item["resolution"],
            "selected_card_ids": item["selected_card_ids"],
            "status": item["status"],
            "source_document": ledger["source_document"],
            "source_sha256": ledger["source_sha256"],
        }
        for item in ledger["decisions"]
        if item["article"] in articles or item["variant_group"] in linked_groups
    ]


def selected_doctrine_cards(unit: dict[str, Any]) -> list[dict[str, Any]]:
    decisions = inherited_doctrine_decisions(unit)
    selected = {
        card_id: decision
        for decision in decisions
        if decision["status"] == "valid"
        for card_id in decision["selected_card_ids"]
    }
    if not selected:
        return []

    found: dict[str, dict[str, Any]] = {}
    for path in sorted((ROOT / "data/rulegen/p2/remediated").glob("*/*.json")):
        for card in read_json(path).get("cards", []):
            if card["id"] in selected:
                found[card["id"]] = card
    missing = sorted(set(selected) - set(found))
    if missing:
        raise ValueError(f"selected doctrine cards missing from remediated catalog: {missing}")
    return [
        {**found[card_id], "inherited_doctrine": selected[card_id]}
        for card_id in selected
    ]


def build_queue(manifest: dict[str, Any], unit: dict[str, Any]) -> dict[str, Any]:
    contract = manifest["review_contract"]
    base_cards = cards_for_unit(unit)
    base_ids = {card["id"] for card in base_cards}
    overlay_cards = [card for card in selected_doctrine_cards(unit) if card["id"] not in base_ids]
    rows = []
    for card in [*base_cards, *overlay_cards]:
        rows.append({
            "card_id": card["id"],
            "source_track": "doctrine_overlay" if "inherited_doctrine" in card else "unit_core",
            "inherited_doctrine": card.get("inherited_doctrine"),
            "proposition": card["proposition"],
            "formalization": card.get("formalization"),
            "polarity": card.get("polarity"),
            "doctrinal_status": card.get("doctrinal_status"),
            "review_required": card.get("review_required"),
            "review_notes": card.get("review_notes"),
            "source_refs": card.get("source_refs", []),
            "human": {field: None for field in contract["required_human_fields"]},
        })
    return {
        "version": manifest["version"],
        "law_snapshot": manifest["law_snapshot"],
        "unit": unit,
        "review_contract": contract,
        "status": "human_card_review_pending",
        "inherited_doctrine_decisions": inherited_doctrine_decisions(unit),
        "unit_core_card_count": len(base_cards),
        "doctrine_overlay_card_count": len(overlay_cards),
        "card_count": len(rows),
        "cards": rows,
    }


def render_packet(queue: dict[str, Any], start: int, end: int, packet_index: int) -> str:
    unit = queue["unit"]
    contract = queue["review_contract"]
    lines = [
        f"# {unit['label']} RuleIR 카드 검수 {packet_index}",
        "",
        f"- unit: `{unit['unit_id']}`",
        f"- articles: {', '.join(unit['articles'])}",
        f"- cards: {start + 1}–{end} / {queue['card_count']}",
        f"- law snapshot: `{queue['law_snapshot']['law_snapshot_id']}`",
        "",
        "각 카드에 대해 decision, role, component/track, 근거를 판정한다. 빈칸은 승인으로 간주하지 않는다.",
        "",
        f"- decision: {', '.join(contract['allowed_decisions'])}",
        f"- role: {', '.join(contract['allowed_roles'])}",
        f"- component join: {', '.join(contract['allowed_component_joins'])}",
        "",
    ]
    inherited = queue["inherited_doctrine_decisions"]
    if inherited:
        lines.extend([
            "## 기존 결정 C 자동 계승",
            "",
            "아래 선택은 재질문하지 않는다. 카드의 RuleIR role·join·track만 현재 unit에서 검수한다.",
            "",
        ])
        for decision in inherited:
            selected = ", ".join(f"`{card_id}`" for card_id in decision["selected_card_ids"])
            lines.append(
                f"- #{decision['number']} `{decision['variant_group']}`: "
                f"{selected or decision['resolution']} (status=`{decision['status']}`)"
            )
        lines.append("")
    for number, card in enumerate(queue["cards"][start:end], start + 1):
        lines.extend([
            f"## {number}. `{card['card_id']}`",
            "",
            f"- proposition: {card['proposition']}",
            f"- current metadata: formalization=`{card['formalization']}`, polarity=`{card['polarity']}`, "
            f"doctrinal_status=`{card['doctrinal_status']}`, review_required=`{card['review_required']}`",
            f"- source track: `{card['source_track']}`",
            f"- prior note: {card['review_notes'] or '-'}",
            "- bounded sources:",
            "",
        ])
        for source in card["source_refs"]:
            lines.append(
                f"  - `{source.get('comment_id', '-')}` / `{source.get('section_path', '-')}`: "
                f"“{source.get('quote', '')}”"
            )
        lines.extend([
            "",
            "```text",
            "decision:",
            "role:",
            "component_id:",
            "component_join:",
            "track_id:",
            "refers_to_unit:",
            "rationale:",
            "proposition_rewrite:",
            "```",
            "",
        ])
    return "\n".join(lines)


def write_packets(unit_id: str, packet_size: int) -> tuple[Path, list[Path]]:
    if packet_size < 1:
        raise ValueError("packet_size must be positive")
    manifest = read_json(MANIFEST)
    unit = unit_definition(manifest, unit_id)
    queue = build_queue(manifest, unit)
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    PACKET_DIR.mkdir(parents=True, exist_ok=True)
    queue_path = QUEUE_DIR / f"{unit_id}_review_queue.json"
    queue_path.write_text(
        json.dumps(queue, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    packet_paths = []
    for packet_index, start in enumerate(range(0, queue["card_count"], packet_size), 1):
        end = min(start + packet_size, queue["card_count"])
        path = PACKET_DIR / f"{unit_id}_cards_{packet_index:02d}.md"
        path.write_text(render_packet(queue, start, end, packet_index), encoding="utf-8")
        packet_paths.append(path)
    return queue_path, packet_paths


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--unit", required=True)
    parser.add_argument("--packet-size", type=int, default=15)
    args = parser.parse_args()
    queue_path, packets = write_packets(args.unit, args.packet_size)
    print(f"queue={queue_path.relative_to(ROOT)} cards={read_json(queue_path)['card_count']}")
    for path in packets:
        print(f"packet={path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
