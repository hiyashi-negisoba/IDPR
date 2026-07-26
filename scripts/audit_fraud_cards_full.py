"""사기 core 88장 전수감사 + RuleIR 재빌드 (사용자 지시 2026-07-23).

사기도 재산죄와 같은 방식으로 만들어졌다(에이전트 작업 + 전문가 결정점 검토).
`fraud_core_rule_selection_audit.json`의 `method: manual_full_core_scope_audit_no_api`는
"API 없이 수행"이라는 뜻이지 전수 인간검토가 아니다 — 이 필드를 근거로 두 세트의 검토
수준이 다르다고 본 것은 오독이었다. 정정한다.

재산죄에 적용한 축을 그대로 88장 전수 판독으로 적용했다:
  죄수·다른죄 / 공범·총칙 / 학설서술 / 판단지침형(G) / 증명·소송법(P) / 이득액산정 / 중복

경계획정형(사기 vs 절도·횡령처럼 어느 죄인지 가르는 것)은 재산죄와 동일하게 남긴다.
"종합하여 판단한다"류 판단기준도 남긴다 — 강등 대상 G는 '단정할 수 없다'처럼 사실을
물을 수 없는 것에 한정한다.

RuleIR은 강등 카드를 단독 근거로 하는 규칙·술어를 제거해 재빌드한다. API 0회.
"""

from __future__ import annotations

import glob
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
F = ROOT / "data/rulegen/fraud"

DEMOTE = {
    "deception.fraud.standard.loan-lender-anticipated-risk":
        "판단지침형(G) — '미변제만으로 단정할 수 없다'는 해석 지침이라 모델에게 물을 사실이 없다. "
        "재산죄 G축 7장과 동일 기준.",
    "deception.fraud.standard.intent-to-defraud-loan-inference":
        "증명·소송법(P) — '자백이 없으면 객관적 사정을 종합하여 판단한다'는 사실인정 방법론이지 "
        "실체 요건이 아니다. 재산죄 P축 4장과 동일 기준.",
}

# 이득액 산정 축이지만 유지하기로 한 것 — 기준 예외를 명시해 둔다
KEEP_EXCEPTION = {
    "fraud_damage_acquisition.money_delivery_full_amount":
        "이득액 산정 축이라 선별기준상 강등 후보였으나 **유지**한다(사용자 결정 2026-07-23). "
        "특정경제범죄가중처벌법 연계 시 편취액 산정이 구성요건적 의미를 가지므로 그때 쓴다. "
        "선별기준의 '이득액 계산=context_only'는 이 카드에 한해 예외로 기록한다.",
}

# 메타 래퍼를 벗기면 실질 규칙이 남는 카드
REWRITE = {
    "fraud_intent.precedent_illegal_appropriation_intent":
        "사기죄가 성립하려면 고의 외에 불법영득의사가 있어야 한다.",
    "deception.fraud.standard.precedent-notice-duty-materiality":
        "법률상 고지의무자가 상대방의 착오를 알면서도 고지하지 않은 경우, 일반거래 경험칙상 "
        "상대방이 그 사실을 알았다면 해당 법률행위를 하지 않았을 것이 명백하면 신의칙상 "
        "고지의무가 인정된다.",
}

# 실질 중복 — 남길 카드: 흡수될 카드
MERGE = {
    "fraud_mistake.error_doubt_ignorance": "fraud_mistake.unaware_error",
    "fraud_general_object.causation_required": "fraud_stages_participation.no_causation_attempt",
}


def load_core() -> dict[str, dict]:
    gold = {r["card_id"]: r for r in json.loads(
        (F / "fraud_core_rule_selection_audit.json").read_text(encoding="utf-8"))["rows"]}
    cards: dict[str, dict] = {}
    for p in glob.glob(str(F / "norm_card_sets/*.json")):
        for c in json.loads(Path(p).read_text(encoding="utf-8")).get("cards", []):
            cards[c["id"]] = c
    return {k: cards[k] for k, v in gold.items()
            if v["role"] != "context_only" and k in cards}


def rebuild_rule_ir(dropped: set[str]) -> dict:
    p = F / "fraud_full_rule_ir_candidate_unreviewed.json"
    ir = json.loads(p.read_text(encoding="utf-8"))

    def sole(o) -> bool:
        ids = o.get("norm_card_ids", [])
        return bool(ids) and set(ids) <= dropped

    drop_rules = [i for i, r in enumerate(ir["rules"]) if sole(r)]
    drop_preds = [i for i, x in enumerate(ir["predicates"]) if sole(x)]
    dropped_pred_names = {ir["predicates"][i].get("name") for i in drop_preds}
    dropped_pred_names.discard(None)

    ir["rules"] = [r for i, r in enumerate(ir["rules"]) if i not in set(drop_rules)]
    ir["predicates"] = [x for i, x in enumerate(ir["predicates"]) if i not in set(drop_preds)]
    for coll in ("rules", "predicates"):
        for o in ir[coll]:
            if "norm_card_ids" in o:
                o["norm_card_ids"] = [c for c in o["norm_card_ids"] if c not in dropped]
    ir["norm_card_scope"]["card_ids"] = [c for c in ir["norm_card_scope"]["card_ids"]
                                         if c not in dropped]
    # 남은 규칙이 삭제된 술어를 참조하면 정합성이 깨진다 — 검출
    orphan = []
    for i, r in enumerate(ir["rules"]):
        names = {b.get("predicate") for b in r.get("body", [])} | {r.get("head", {}).get("predicate")}
        bad = names & dropped_pred_names
        if bad:
            orphan.append({"rule_index": i, "rule_id": r.get("id"), "missing": sorted(bad)})
    ir["version"] = "1.1.0"
    ir["rebuild"] = {"at": datetime.now(timezone.utc).isoformat(),
                     "reason": "core 카드 전수감사 강등 반영 (사용자 지시)",
                     "dropped_cards": sorted(dropped),
                     "removed_rules": len(drop_rules), "removed_predicates": len(drop_preds),
                     "orphan_references": orphan}
    out = F / "fraud_full_rule_ir_rebuilt.json"
    out.write_text(json.dumps(ir, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"removed_rules": len(drop_rules), "removed_predicates": len(drop_preds),
            "orphans": orphan, "rules_left": len(ir["rules"]),
            "predicates_left": len(ir["predicates"]), "path": str(out.relative_to(ROOT))}


def main() -> None:
    core = load_core()
    dropped = set(DEMOTE) | set(MERGE.values())
    kept = [k for k in core if k not in dropped]
    print(f"사기 core {len(core)}장 전수 판독")
    print(f"  강등 {len(DEMOTE)} + 중복흡수 {len(MERGE)} = {len(dropped)}장")
    print(f"  명제 재작성 {len(REWRITE)}장")
    print(f"  → 최종 core {len(kept)}장")
    for k, v in DEMOTE.items():
        print(f"\n  [강등] {k}\n     {v}")
    for keep, absorbed in MERGE.items():
        print(f"\n  [중복] {absorbed}\n     → {keep} 로 병합")

    ir = rebuild_rule_ir(dropped)
    print(f"\nRuleIR 재빌드: 규칙 -{ir['removed_rules']} (잔여 {ir['rules_left']}), "
          f"술어 -{ir['removed_predicates']} (잔여 {ir['predicates_left']})")
    print(f"  고아 참조: {len(ir['orphans'])}건")
    for o in ir["orphans"][:10]:
        print(f"    rules[{o['rule_index']}] {o['rule_id']} → {o['missing']}")

    (F / "fraud_core_card_full_audit.json").write_text(json.dumps({
        "version": "1.0.0", "api_calls": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "method": "에이전트 88장 전수 판독 — 재산죄와 동일 축",
        "metadata_correction": {
            "field": "fraud_core_rule_selection_audit.json:method",
            "was_read_as": "사람이 646장 전수 검토",
            "actual": "에이전트가 API 없이 수행. 전문가 검토는 결정점 단위 — 재산죄와 동일 방식",
        },
        "counts": {"core_before": len(core), "demoted": len(DEMOTE),
                   "merged": len(MERGE), "rewritten": len(REWRITE), "core_after": len(kept)},
        "demotions": DEMOTE, "rewrites": REWRITE, "merges": MERGE,
        "criteria_exceptions": KEEP_EXCEPTION,
        "rule_ir_rebuild": ir,
        "kept": sorted(kept),
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\n→ data/rulegen/fraud/fraud_core_card_full_audit.json\n→ {ir['path']}")


if __name__ == "__main__":
    main()
