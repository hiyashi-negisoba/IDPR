from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from scripts.run_fraud_rulegen_critics import read_json  # noqa: E402
from scripts.run_fraud_rulegen_pilot import write_json  # noqa: E402


CARD_MANIFEST = PROJECT_ROOT / "data/rulegen/fraud/fraud_norm_card_manifest.json"
CRITIC_ROOT = (
    PROJECT_ROOT
    / "data/rulegen/fraud/norm_card_reviews/fraud_norm_cards_critic_v4_final"
)
CRITIC_MANIFEST = CRITIC_ROOT / "manifest.json"
QUEUE = PROJECT_ROOT / "data/rulegen/fraud/fraud_norm_card_review_queue.json"
DECISIONS = PROJECT_ROOT / "data/rulegen/fraud/fraud_human_review_decisions.jsonl"
READINESS = PROJECT_ROOT / "data/rulegen/fraud/fraud_rule_ir_readiness.json"
GUIDE = PROJECT_ROOT / "data/rulegen/fraud/fraud_legal_review_guide.md"


PRIORITY = {
    "source_scope": 1,
    "source_entailment": 1,
    "overgeneralization": 1,
    "missing_norm": 1,
    "authority_mismatch": 2,
    "formalization_error": 3,
    "missing_variant": 4,
    "collapsed_variant": 4,
    "other": 5,
}


def load_cards() -> tuple[
    dict[str, dict[str, Any]], dict[str, list[dict[str, Any]]]
]:
    manifest = read_json(CARD_MANIFEST)
    cards_by_id: dict[str, dict[str, Any]] = {}
    cards_by_module: dict[str, list[dict[str, Any]]] = {}
    for module in manifest["modules"]:
        card_set = read_json(PROJECT_ROOT / module["path"])
        cards_by_module[module["module"]] = card_set["cards"]
        cards_by_id.update({card["id"]: card for card in card_set["cards"]})
    return cards_by_id, cards_by_module


def impacted_card_ids(target_path: str, part_card_ids: list[str]) -> list[str]:
    direct = [card_id for card_id in part_card_ids if card_id in target_path]
    if direct:
        return direct

    indexes: set[int] = set()
    for match in re.finditer(r"cards(?:\[|/)(\d+)(?:\]|/|$)", target_path):
        indexes.add(int(match.group(1)))
    for match in re.finditer(r"cards\[(\d+):(\d+)\]", target_path):
        indexes.update(range(int(match.group(1)), int(match.group(2))))
    for match in re.finditer(r"cards\[(\d+)-(\d+)\]", target_path):
        indexes.update(range(int(match.group(1)), int(match.group(2)) + 1))
    if indexes:
        return [part_card_ids[index] for index in sorted(indexes) if index < len(part_card_ids)]
    if "cards" in target_path:
        return part_card_ids
    return []


def build_queue(
    cards_by_id: dict[str, dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, set[str]]]:
    manifest = read_json(CRITIC_MANIFEST)
    queue: list[dict[str, Any]] = []
    impacted_by_module: dict[str, set[str]] = defaultdict(set)
    for report_meta in manifest["reports"]:
        report = read_json(PROJECT_ROOT / report_meta["path"])
        for finding in report["findings"]:
            impacted = impacted_card_ids(
                finding["target_path"], report_meta["card_ids"]
            )
            impacted_by_module[report_meta["module"]].update(impacted)
            review_id = f"{report_meta['request_id']}.{finding['finding_id']}"
            queue.append(
                {
                    "review_id": review_id,
                    "priority": PRIORITY.get(finding["type"], 5),
                    "module": report_meta["module"],
                    "part": report_meta["part"],
                    "severity": finding["severity"],
                    "type": finding["type"],
                    "target_path": finding["target_path"],
                    "message": finding["message"],
                    "recommended_action": finding["recommended_action"],
                    "source_refs": finding["source_refs"],
                    "impacted_card_ids": impacted,
                    "impacted_cards": [
                        {
                            "id": card_id,
                            "proposition": cards_by_id[card_id]["proposition"],
                            "formalization": cards_by_id[card_id]["formalization"],
                            "authority_basis": cards_by_id[card_id]["authority_basis"],
                            "source_refs": cards_by_id[card_id]["source_refs"],
                        }
                        for card_id in impacted
                    ],
                }
            )
    queue.sort(key=lambda row: (row["priority"], row["module"], row["review_id"]))
    return queue, impacted_by_module


def build_readiness(
    cards_by_module: dict[str, list[dict[str, Any]]],
    impacted_by_module: dict[str, set[str]],
) -> dict[str, Any]:
    modules: list[dict[str, Any]] = []
    totals: Counter[str] = Counter()
    for module, cards in cards_by_module.items():
        buckets: dict[str, list[str]] = defaultdict(list)
        impacted = impacted_by_module[module]
        for card in cards:
            if card["id"] in impacted:
                bucket = "critic_pending"
            elif card["formalization"] == "context_only":
                bucket = "context_only_excluded"
            elif card["formalization"] == "policy_variant":
                bucket = "policy_choice_pending"
            elif card["review_required"]:
                bucket = "human_review_pending"
            else:
                bucket = "provisional_rule_ir_ready"
            buckets[bucket].append(card["id"])
            totals[bucket] += 1
        modules.append(
            {
                "module": module,
                "cards": len(cards),
                "buckets": dict(sorted(buckets.items())),
                "counts": {
                    key: len(value) for key, value in sorted(buckets.items())
                },
            }
        )
    return {
        "version": "1.0.0",
        "issue_tag": "fraud",
        "status": "draft",
        "legal_review": "pending",
        "full_rule_ir_generation_blocked": True,
        "blocking_reason": (
            "The practical precedent choices, source-entailment findings, and policy "
            "variant groups require human legal review before full RuleIR generation."
        ),
        "modules": modules,
        "totals": dict(sorted(totals.items())),
        "existing_executable_exemplar": (
            "data/rulegen/fraud/fraud_rule_ir_exemplar.json"
        ),
    }


def write_decision_template(queue: list[dict[str, Any]]) -> None:
    if DECISIONS.exists():
        return
    DECISIONS.write_text(
        "".join(
            json.dumps(
                {
                    "review_id": row["review_id"],
                    "status": "pending",
                    "decision": None,
                    "notes": "",
                    "verified_authority_refs": [],
                },
                ensure_ascii=False,
                sort_keys=True,
            )
            + "\n"
            for row in queue
        ),
        encoding="utf-8",
    )


def build_guide(
    queue: list[dict[str, Any]],
    readiness: dict[str, Any],
    cards_by_module: dict[str, list[dict[str, Any]]],
) -> str:
    by_type = Counter(row["type"] for row in queue)
    by_module = Counter(row["module"] for row in queue)
    lines = [
        "# 사기죄 NormCard 법률 검수 가이드",
        "",
        "## 현재 상태",
        "",
        "- 범위: 형법 제347조 사기죄 주석서 13개 배치만 포함한다.",
        "- 검증 후보 662개가 NormCard 636개에 중복 없이 연결되어 있다.",
        "- Sol 최종 비평은 17개 묶음 전부 계약 검증을 통과했다.",
        f"- 검토 지적은 {len(queue)}개이며, 모든 산출물은 draft/legal_review=pending이다.",
        "- 주석서가 보고한 판례로 추정되는 카드는 원판례 확인 전 context_only로 격리했다.",
        "",
        "## 검수 순서",
        "",
        "1. 출처 의미: source_entailment, overgeneralization, missing_norm, source_scope를 먼저 본다.",
        "2. 권위: commentary_reported_precedent 여부와 원판례의 실제 법리를 판례 인덱스로 확인한다.",
        "3. 형식화: deterministic_rule, standard_input, context_only 구분을 확인한다.",
        "4. 학설 대립: 같은 쟁점의 variant_group을 묶고 실무상 판례 입장을 선택한다.",
        "5. 승인된 카드만 RuleIR로 내린다. 미확인 사실이나 반대사실은 unknown으로 유지한다.",
        "",
        "## 결정값",
        "",
        "`fraud_human_review_decisions.jsonl`에서 각 review_id의 status를 completed로 "
        "바꾸고 decision을 기록한다.",
        "허용 결정 예시는 approve_as_is, narrow_proposition, reclassify_authority, set_context_only, "
        "group_variant, select_precedent_variant, reject_card, needs_more_source이다.",
        "원판례를 확인한 경우 verified_authority_refs에 사용자의 판례 인덱스 식별자를 넣는다.",
        "",
        "## 지적 분포",
        "",
        "| 유형 | 건수 |",
        "|---|---:|",
    ]
    lines.extend(f"| {key} | {value} |" for key, value in sorted(by_type.items()))
    lines.extend(
        [
            "",
            "## 모듈별 우선순위",
            "",
            "| 모듈 | 카드 | 지적 | context_only | policy_variant |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    for module, cards in cards_by_module.items():
        lines.append(
            f"| {module} | {len(cards)} | {by_module[module]} | "
            f"{sum(card['formalization'] == 'context_only' for card in cards)} | "
            f"{sum(card['formalization'] == 'policy_variant' for card in cards)} |"
        )
    lines.extend(
        [
            "",
            "## RuleIR 게이트",
            "",
            f"- critic_pending: {readiness['totals'].get('critic_pending', 0)}",
            f"- context_only_excluded: {readiness['totals'].get('context_only_excluded', 0)}",
            f"- policy_choice_pending: {readiness['totals'].get('policy_choice_pending', 0)}",
            f"- human_review_pending: {readiness['totals'].get('human_review_pending', 0)}",
            "- provisional_rule_ir_ready: "
            f"{readiness['totals'].get('provisional_rule_ir_ready', 0)}",
            "",
            "현재 전체 RuleIR 생성은 차단되어 있다. 기존 8장짜리 사기죄 모범 NormCard/RuleIR/Scallop은 구조 예시로만 유지하며, "
            "636장 전체에 대한 법적 승인으로 간주하지 않는다.",
            "",
            "## 파일",
            "",
            "- 상세 검수 큐: `data/rulegen/fraud/fraud_norm_card_review_queue.json`",
            "- 결정 입력: `data/rulegen/fraud/fraud_human_review_decisions.jsonl`",
            "- RuleIR readiness: `data/rulegen/fraud/fraud_rule_ir_readiness.json`",
            "- Sol 원보고서: `data/rulegen/fraud/norm_card_reviews/fraud_norm_cards_critic_v4_final/`",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    cards_by_id, cards_by_module = load_cards()
    queue, impacted_by_module = build_queue(cards_by_id)
    readiness = build_readiness(cards_by_module, impacted_by_module)
    write_json(
        QUEUE,
        {
            "version": "1.0.0",
            "issue_tag": "fraud",
            "status": "draft",
            "legal_review": "pending",
            "items": queue,
        },
    )
    write_json(READINESS, readiness)
    write_decision_template(queue)
    GUIDE.write_text(
        build_guide(queue, readiness, cards_by_module), encoding="utf-8"
    )
    print(
        json.dumps(
            {"review_items": len(queue), **readiness["totals"]},
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
