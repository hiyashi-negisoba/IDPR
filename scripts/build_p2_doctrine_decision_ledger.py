"""Convert the human-approved P2 doctrine Markdown into an auditable JSON ledger.

The source document remains authoritative.  This script does not guess invalid
option numbers and does not promote cards into RuleIR; it records what can be
inherited and exposes any source/selection mismatch for human correction.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
P2 = ROOT / "data/rulegen/p2"
SOURCE = P2 / "결정C_학설선택.md"
LEGACY_QUEUE = P2 / "p2_norm_card_review_queue.json"
LEDGER = P2 / "결정C_구조화원장.json"
AUDIT = ROOT / "docs/review/2026-08-03_p2_doctrine_decision_audit.md"

SECTION_RE = re.compile(
    r"^###\s+(?P<number>\d+)\.\s+`(?P<article>[^`]+)`\s+/\s+`(?P<module>[^`]+)`"
    r"\s+-.*?\((?P<group>[^()\s]+)\)\s*$",
    re.MULTILINE,
)
OPTION_RE = re.compile(r"^- \*\*`(?P<card_id>[^`]+)`\*\*\s*$", re.MULTILINE)
ANSWER_RE = re.compile(
    r"^\*\*선택할 카드 ID \(또는 모두유지 / 모두강등\):\*\*\s*(?P<answer>.+?)\s*$",
    re.MULTILINE,
)


def read_object(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path}: expected JSON object")
    return payload


def card_indexes() -> tuple[dict[str, dict[str, Any]], set[str]]:
    cards: dict[str, dict[str, Any]] = {}
    for path in sorted((P2 / "remediated").glob("*/*.json")):
        for card in read_object(path).get("cards", []):
            card_id = card["id"]
            if card_id in cards:
                raise ValueError(f"duplicate remediated card id: {card_id}")
            cards[card_id] = card

    unit_cards: set[str] = set()
    for path in sorted((P2 / "rule_ir_units").glob("*_unit.json")):
        unit_cards.update(card["id"] for card in read_object(path).get("cards", []))
    return cards, unit_cards


def legacy_option_index() -> dict[str, list[str]]:
    payload = read_object(LEGACY_QUEUE)
    result: dict[str, list[str]] = {}
    for item in payload.get("items", []):
        group = item.get("variant_group")
        options = item.get("options")
        if not group or not isinstance(options, list):
            continue
        card_ids = [option["card_id"] for option in options if option.get("card_id")]
        if group in result and result[group] != card_ids:
            raise ValueError(f"conflicting legacy option lists: {group}")
        result[group] = card_ids
    return result


def parse_decisions(markdown: str) -> list[dict[str, Any]]:
    headings = list(SECTION_RE.finditer(markdown))
    decisions: list[dict[str, Any]] = []
    for index, heading in enumerate(headings):
        end = headings[index + 1].start() if index + 1 < len(headings) else len(markdown)
        body = markdown[heading.end():end]
        options = OPTION_RE.findall(body)
        answer_match = ANSWER_RE.search(body)
        if not answer_match:
            raise ValueError(f"decision {heading['number']}: answer missing")
        raw = answer_match["answer"].strip()

        selected: list[str] = []
        status = "valid"
        resolution = "selected"
        issue = None
        if raw == "모두강등":
            resolution = "all_demoted"
        elif raw == "모두유지":
            resolution = "all_retained"
            selected = list(options)
        else:
            numbers = [int(value) for value in re.findall(r"\((\d+)\)", raw)]
            if not numbers:
                status = "invalid_answer"
                issue = "선택 번호, 모두유지 또는 모두강등으로 해석할 수 없음"
            elif any(number < 1 or number > len(options) for number in numbers):
                status = "option_out_of_range"
                issue = f"응답 {raw}은 {len(options)}개 선택지 범위를 벗어남"
            else:
                selected = [options[number - 1] for number in numbers]

        decisions.append({
            "number": int(heading["number"]),
            "article": heading["article"],
            "module": heading["module"],
            "variant_group": heading["group"],
            "options": options,
            "raw_answer": raw,
            "resolution": resolution,
            "selected_card_ids": selected,
            "status": status,
            "issue": issue,
        })
    return decisions


def build_ledger() -> dict[str, Any]:
    source_bytes = SOURCE.read_bytes()
    decisions = parse_decisions(source_bytes.decode("utf-8"))
    cards, unit_cards = card_indexes()
    legacy_options = legacy_option_index()
    stats: Counter[str] = Counter()

    for decision in decisions:
        if decision["status"] == "option_out_of_range":
            numbers = [int(value) for value in re.findall(r"\((\d+)\)", decision["raw_answer"])]
            original = legacy_options.get(decision["variant_group"], [])
            if numbers and all(0 < number <= len(original) for number in numbers):
                decision["reconciliation"] = {
                    "reason": "후속 Markdown 선택지 축약 시 기존 응답 번호가 재번호화되지 않음",
                    "basis": str(LEGACY_QUEUE.relative_to(ROOT)),
                    "legacy_options": original,
                    "displayed_options": decision["options"],
                }
                decision["selected_card_ids"] = [original[number - 1] for number in numbers]
                decision["status"] = "valid"
                decision["issue"] = None
                stats["reconciled_from_legacy_queue"] += 1

        missing = [card_id for card_id in decision["options"] if card_id not in cards]
        wrong_group = [
            card_id for card_id in decision["options"]
            if card_id in cards and cards[card_id].get("variant_group") != decision["variant_group"]
        ]
        decision["card_catalog_issues"] = list(filter(None, [
                f"remediated card missing: {', '.join(missing)}" if missing else "",
                f"variant_group mismatch: {', '.join(wrong_group)}" if wrong_group else "",
        ]))
        missing_selected = [
            card_id for card_id in decision["selected_card_ids"] if card_id not in cards
        ]
        if missing_selected:
            decision["status"] = "selected_card_missing"
            decision["issue"] = f"selected remediated card missing: {', '.join(missing_selected)}"
            decision["selected_card_ids"] = []

        decision["selected_card_state"] = [
            {
                "card_id": card_id,
                "formalization": cards[card_id].get("formalization"),
                "doctrinal_status": cards[card_id].get("doctrinal_status"),
                "present_in_rule_ir_unit": card_id in unit_cards,
            }
            for card_id in decision["selected_card_ids"]
        ]
        stats[decision["status"]] += 1
        stats["card_catalog_issue_groups"] += bool(decision["card_catalog_issues"])
        stats[decision["resolution"]] += 1
        stats["selected_cards"] += len(decision["selected_card_ids"])
        stats["selected_cards_missing_from_rule_ir_units"] += sum(
            not state["present_in_rule_ir_unit"] for state in decision["selected_card_state"]
        )

    if [item["number"] for item in decisions] != list(range(1, len(decisions) + 1)):
        raise ValueError("decision numbering is not contiguous")
    return {
        "version": "1.0.0",
        "authority": "human_approved_doctrine_choices",
        "source_document": str(SOURCE.relative_to(ROOT)),
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "selection_number_basis": str(LEGACY_QUEUE.relative_to(ROOT)),
        "selection_number_basis_sha256": hashlib.sha256(LEGACY_QUEUE.read_bytes()).hexdigest(),
        "policy": {
            "invalid_choice_handling": "do_not_guess; require correction",
            "promotion": "separate audited step required",
            "runtime_use": "only status=valid decisions may be inherited",
        },
        "stats": dict(sorted(stats.items())),
        "decisions": decisions,
    }


def render_audit(ledger: dict[str, Any]) -> str:
    invalid = [item for item in ledger["decisions"] if item["status"] != "valid"]
    reconciled = [item for item in ledger["decisions"] if item.get("reconciliation")]
    catalog_issues = [item for item in ledger["decisions"] if item["card_catalog_issues"]]
    absent = [
        state
        for item in ledger["decisions"]
        for state in item["selected_card_state"]
        if not state["present_in_rule_ir_unit"]
    ]
    lines = [
        "# P2 학설선택 구조화 감사",
        "",
        f"- authoritative source: `{ledger['source_document']}`",
        f"- source SHA-256: `{ledger['source_sha256']}`",
        f"- decision groups: {len(ledger['decisions'])}",
        f"- valid groups: {ledger['stats'].get('valid', 0)}",
        f"- invalid groups: {len(invalid)}",
        f"- legacy option order reconciliations: {len(reconciled)}",
        f"- card-catalog mismatch groups: {len(catalog_issues)}",
        f"- selected cards absent from current RuleIR units: {len(absent)}",
        "",
        "유효한 기존 선택은 후속 검수 패킷에서 자동 계승한다. 범위를 벗어난 번호는 추정하지 않는다.",
        "선택 카드가 RuleIR unit에 없다는 것은 선택이 폐기됐다는 뜻이 아니라, Markdown 선택과 카드 승격이",
        "아직 연결되지 않았다는 뜻이다.",
        "",
        "## 기존 응답 불일치",
        "",
    ]
    if not invalid:
        lines.append("없음.")
    for item in invalid:
        lines.append(
            f"- #{item['number']} `{item['variant_group']}`: {item['issue']} "
            f"(raw=`{item['raw_answer']}`)"
        )
    lines.extend(["", "## 축약 전 선택지 순서로 복원", ""])
    if not reconciled:
        lines.append("없음.")
    for item in reconciled:
        lines.append(
            f"- #{item['number']} `{item['variant_group']}` raw=`{item['raw_answer']}` → "
            f"`{', '.join(item['selected_card_ids'])}`"
        )
    lines.extend(["", "## 카드 카탈로그 불일치", ""])
    if not catalog_issues:
        lines.append("없음.")
    for item in catalog_issues:
        lines.append(
            f"- #{item['number']} `{item['variant_group']}`: "
            + "; ".join(item["card_catalog_issues"])
            + " (선택 카드가 존재하면 기존 선택 자체는 계승)"
        )
    lines.extend(["", "## RuleIR 미연결 선택 카드", ""])
    if not absent:
        lines.append("없음.")
    else:
        lines.extend(f"- `{state['card_id']}`" for state in absent)
    lines.append("")
    return "\n".join(lines)


def write_outputs() -> tuple[Path, Path, dict[str, Any]]:
    ledger = build_ledger()
    LEDGER.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    AUDIT.parent.mkdir(parents=True, exist_ok=True)
    AUDIT.write_text(render_audit(ledger), encoding="utf-8")
    return LEDGER, AUDIT, ledger


def main() -> None:
    ledger_path, audit_path, ledger = write_outputs()
    print(f"ledger={ledger_path.relative_to(ROOT)}")
    print(f"audit={audit_path.relative_to(ROOT)}")
    print(json.dumps(ledger["stats"], ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
