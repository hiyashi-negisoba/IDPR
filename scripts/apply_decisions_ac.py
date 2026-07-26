"""결정 A/A2(출처범위) · C/C2(학설선택) 반영 — 사용자 답변은 이미 전부 수령됨.

  A  59건 중 기입 4 / 공란 55 = 괜찮음
  A2 10건 전수 기입
  C/C2 67그룹 → `학설선택_확정원장.json`에 확정 (사용자 47 / 자동 16 / 보류 2 / 병합 1 / 결손 1)

C의 반영 규칙: 그룹에서 고른 견해 카드만 실무규칙으로 남기고 나머지는 context_only로 내린다.
'보류'는 uncovered로 정직 보고하고 그룹 전체를 context_only로 둔다.

A/A2 대부분은 오늘 카드 감사에서 이미 강등돼 자동 해소됐다. 남은 것만 처리한다.

API 0회.
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROP = ROOT / "data/rulegen/property"

# --- A/A2 중 아직 core에 살아 있는 것 ---
A_ACTIONS = {
    "art328_sec6_3.disabled_victim_abuse_crimes_no_application": {
        "action": "source_regen_required",
        "user": "출처가 끊김. 이렇게 엉망이었어? / 동일한게 지금 두번 들어가있음 (결정A 4·5번)",
        "note": "명제는 유지한다. 출처 인용이 잘려 있고 같은 카드가 검토서에 두 번 실렸다. "
                "출처 재추출 대상으로 표시하고 preflight 전에 해소한다.",
    },
    "art355_sec3_3.legal_disposition": {
        "action": "keep",
        "user": "성립여부에 대한 카드가 따로있는거아닌가? 기수시기에 대해? 이건 괜찮음 (결정A2 3번)",
        "note": "유지. critic 지적 기각.",
    },
}


def load_all_cards() -> dict:
    import glob
    out = {}
    for p in glob.glob(str(PROP / "remediated/*/*.json")):
        a, m = Path(p).parts[-2], Path(p).stem
        for c in json.loads(Path(p).read_text(encoding="utf-8")).get("cards", []):
            out[c["id"]] = (a, m, c)
    return out


def main() -> None:
    global ALL
    ALL = load_all_cards()
    core_p = PROP / "property_core_set_final_v3.json"
    core = json.loads(core_p.read_text(encoding="utf-8"))
    rows = {r["card_id"]: r for r in core["rows"]}
    ledger_c = json.loads((PROP / "학설선택_확정원장.json").read_text(encoding="utf-8"))
    queue = json.loads((PROP / "property_norm_card_review_queue.json").read_text(encoding="utf-8"))
    groups = {i["variant_group"]: i for i in queue["items"]
              if i.get("type") == "3.1_variant_group"}

    entries, stats = [], Counter()
    for item in ledger_c["items"]:
        gid = item["variant_group"]
        g = groups.get(gid)
        if not g:
            stats["group_missing"] += 1
            continue
        opts = [o["card_id"] for o in g.get("options", [])]
        res = item["resolution"]
        picked_idx = item.get("picked") or []
        chosen = [opts[int(i) - 1] for i in picked_idx
                  if str(i).isdigit() and 0 < int(i) <= len(opts)]

        if res in ("user_hold", "gap_missing_option"):
            # 판단 보류 / 선지에 없음 → 그룹 전체 uncovered
            for cid in opts:
                if cid in rows and rows[cid]["final_role"] not in ("context_only", "deferred_track"):
                    rows[cid].update(final_role="context_only", demoted_at="decision_c",
                                     reason=f"학설선택 {res} — uncovered로 정직 보고 ({gid})")
            stats[f"group_{res}"] += 1
            entries.append({"group": gid, "resolution": res, "chosen": [],
                            "demoted": opts, "note": item.get("note")})
            continue

        losers = [c for c in opts if c not in chosen]
        for cid in losers:
            if cid in rows and rows[cid]["final_role"] not in ("context_only", "deferred_track"):
                rows[cid].update(final_role="context_only", demoted_at="decision_c",
                                 reason=f"학설선택 — 채택되지 않은 경쟁 견해 ({gid})")
                stats["demoted_loser"] += 1
        for cid in chosen:
            if cid in rows:
                rows[cid]["doctrine_selected"] = {"group": gid, "resolution": res,
                                                  "user_comment": item.get("user_comment")}
                stats["kept_chosen"] += 1
            elif cid in ALL:
                # 경쟁견해 카드는 policy_variant라 core에 없다. 채택된 것만 실무규칙으로 승격한다.
                a, m, c = ALL[cid]
                rows[cid] = {"article": a, "module": m, "card_id": cid,
                             "polarity": c.get("polarity"), "proposition": c.get("proposition", ""),
                             "merge_role": "policy_variant", "final_role": "standard_input",
                             "demoted_at": None, "reason": None,
                             "promoted_from_variant": True,
                             "doctrine_selected": {"group": gid, "resolution": res,
                                                   "user_comment": item.get("user_comment")}}
                stats["promoted_chosen"] += 1
            else:
                stats["chosen_card_missing"] += 1
        stats[f"group_{res}"] += 1
        entries.append({"group": gid, "resolution": res, "chosen": chosen, "demoted": losers})

    for cid, a in A_ACTIONS.items():
        if cid in rows:
            rows[cid]["decision_a"] = a
            stats[f"A_{a['action']}"] += 1

    core["rows"] = list(rows.values())
    kept = [r for r in core["rows"] if r["final_role"] not in ("context_only", "deferred_track")]
    core["version"] = "4.0.0"
    core["counts"]["demoted_decision_c"] = stats["demoted_loser"]
    core["counts"]["core_final"] = len(kept)
    (PROP / "property_core_set_final_v4.json").write_text(
        json.dumps(core, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    (PROP / "결정AC_반영원장.json").write_text(json.dumps({
        "version": "1.0.0", "api_calls": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source": "결정A/A2 사용자응답 + 학설선택_확정원장(67그룹)",
        "stats": dict(stats), "a_actions": A_ACTIONS, "c_entries": entries,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("학설선택 67그룹 반영")
    for k, v in sorted(stats.items()):
        print(f"  {k}: {v}")
    print(f"\n재산죄 core {len(kept)}장 (이전 386)")
    print(f"출처 재생성 대상 1장: art328_sec6_3.disabled_victim_abuse_crimes_no_application")


if __name__ == "__main__":
    main()
