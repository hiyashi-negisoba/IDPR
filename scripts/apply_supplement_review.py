"""보강 3조문 검토 반영 — 학설선택 10그룹 + 확인 5건 → core 확정 (v8 → v9).

사용자 검토(2026-07-25) 결과. 1부 10그룹 중 8건은 제안대로, **2건은 제 제안이 틀렸다는 지적**이다.

  8. 선행행위로 조성된 상태의 이용 — "판례는 `unconsciousness_prior_force_no_causation`"
     제안은 반대 견해(자기 선행행위로 조성한 상태 이용 = 강취)였다. 판례는 탈취 목적 없는
     선행행위와 탈취 사이의 인과관계를 부정하고, 살인 후 사자 소지품 취득은 살인죄와 절도죄의
     경합으로 본다. 강간 사안(그룹 7에서 판례로 확정)과 갈리는 지점은 피해자의 의식 유무다 —
     공포 상태에 있는 피해자로부터의 강취는 강도지만, 심신상실 상태에서는 억압할 반항 자체가
     없어 절도다. 두 결정이 이 경계에서 정합한다.
  10. 권리행사와 강도 — "대법원은 소극설 - `right_exercise_robbery_negative`"
     제안은 적극설(권리남용이면 강도 성립)이었다. 소극설이 오히려 공갈죄 쪽 core 카드
     (`art350_sec4_2.right_exercise_exception`, 권리행사면 위법성 조각)와 층이 맞는다.
     내가 근거로 들었던 정합성이 실은 반대 결론을 가리켰다.

2부 확인 5건은 **무응답**이라 감사 판정(죄수·구체사안 축 강등)을 그대로 적용한다. 다만
`art332_sec5_1.residential_intrusion_absorption`은 재산죄 검토에서 살린 `art329_sec8_3`(주간
주거침입과 상습절도)과 짝이므로, 살리기로 하면 이 파일의 USER_CHECK_DECISION만 바꾸면 된다.

API 0회.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

PROP = ROOT / "data/rulegen/property"
AUDIT = PROP / "supplement_core_audit.json"
CORE_V8 = PROP / "property_core_set_final_v8.json"
CORE_V9 = PROP / "property_core_set_final_v9.json"
LEDGER = PROP / "보강3조문_반영원장.json"

# 그룹 → (선택된 카드, 사용자 응답, 판단 근거)
DOCTRINE_DECISIONS: dict[str, tuple[tuple[str, ...], str, str]] = {
    "art330.night_timing": (
        ("art330_sec1.variant.timing_entry_standard",), "동의",
        "다수설·판례인 침입기준설을 실무규칙으로 세운다."),
    "art330.night_meaning": (
        ("art330_sec2.nighttime.objective",), "동의",
        "통설·판례인 객관적 정의(일몰~일출)를 세운다."),
    "art330.commencement": (
        ("art330_sec4.entry_before_theft_commencement",), "동의",
        "판례인 주거침입시 착수설을 세운다."),
    "art333.resistance_standard": (
        (), "동의",
        "주관설을 내린다. 객관설은 이미 core에 있다."),
    "art333.real_estate": (
        ("art333_sec3_1.real_estate_as_robbery_property_negative",
         "art333_sec3_1.real_estate_rights_as_property_benefit"), "동의",
        "대립이 아니라 보완이므로 둘 다 세운다 — 재물성은 부정하고 권리는 재산상 이익으로 포섭한다."),
    "art333.voluntary_delivery": (
        ("art333_sec3_2.voluntary_delivery_attempt",), "동의",
        "반항억압 없는 교부는 강취가 아니므로 미수로 본다. 공갈죄 경계 카드와 정합한다."),
    "art333.rape_force_taking": (
        ("art333_sec3_3.rape_force_subsequent_taking_precedent",), "동의",
        "판례를 따른다. 다수 학설은 학설 소개로 내린다."),
    "art333.prior_state_use": (
        ("art333_sec3_3.unconsciousness_prior_force_no_causation",),
        "판례는 unconsciousness_prior_force_no_causation",
        "사용자 정정. 탈취 목적 없는 선행행위와 탈취 사이에는 인과관계가 없어 강도가 아니다. "
        "그룹 7(강간 폭행 후 탈취 = 강도)과의 경계는 피해자의 의식 유무다 — 공포 상태의 피해자로부터의 "
        "강취는 강도이고, 심신상실 상태에서는 억압할 반항이 없어 절도다."),
    "art333.debt_evasion_disposition": (
        ("art333_sec4_2.debt_evasion_disposition_not_required",), "동의",
        "통설인 소극설을 세운다. 채권자 살해형 사안을 포섭하려면 처분행위를 요구할 수 없다."),
    "art333.right_exercise": (
        ("art333_sec8.right_exercise_robbery_negative",),
        "대법원은 소극설 - right_exercise_robbery_negative",
        "사용자 정정. 취득할 권리가 있는 이익은 불법이익이 아니다. 이 결론이 공갈죄 쪽 core 카드"
        "(art350_sec4_2.right_exercise_exception)와 층이 맞는다 — 제안 때 든 정합성 근거가 실은 "
        "반대 결론을 가리켰다."),
}

# 승격 카드의 학설 어법 제거 — 선택된 견해를 실무규칙 문장으로
REWRITE: dict[str, str] = {
    "art330_sec1.variant.timing_entry_standard":
        "야간주거침입절도죄는 야간에 주거 등에 침입하였는지를 기준으로 하므로, 야간에 침입한 뒤 "
        "절취가 주간에 이루어진 경우에도 성립한다.",
    "art330_sec2.nighttime.objective":
        "야간은 일몰 후부터 일출 전까지를 의미한다.",
    "art330_sec4.entry_before_theft_commencement":
        "야간주거침입절도죄에서는 주거침입행위가 절취행위에 선행하므로, 주거에 침입할 때에 실행에 "
        "착수한 것으로 본다.",
    "art333_sec3_1.real_estate_as_robbery_property_negative":
        "부동산은 절도죄·강도죄와 같은 도취죄의 객체인 재물에 해당하지 않는다.",
    "art333_sec3_1.real_estate_rights_as_property_benefit":
        "폭행·협박으로 부동산에 관한 권리를 취득한 경우에는 재산상 이익의 강취에 해당한다.",
    "art333_sec3_3.rape_force_subsequent_taking_precedent":
        "강간할 목적으로 폭행·협박하여 피해자의 반항을 제압한 후 비로소 소지품 탈취의 범의가 생겨 "
        "이를 탈취한 경우에도 강도죄가 성립한다.",
    "art333_sec3_3.unconsciousness_prior_force_no_causation":
        "재물탈취의 목적 없이 폭행·협박 또는 약물 사용으로 피해자를 심신상실 상태에 빠지게 한 후 "
        "우발적으로 재물탈취의 범의가 생긴 경우에는 선행행위와 재물탈취 사이에 인과관계가 없어 "
        "강도죄가 성립하지 않으며, 살해 후 사자의 소지품을 취득한 경우에도 살인죄와 절도죄의 "
        "경합범이 성립한다.",
    "art333_sec4_2.debt_evasion_disposition_not_required":
        "채무면탈형 강제이득에서는 피해자의 의사표시나 처분행위가 요건이 아니므로, 채권자에게 "
        "이행청구가 불가능할 정도의 폭행·협박을 가하여 이행을 면한 경우에도 강제이득죄가 성립한다.",
    "art333_sec8.right_exercise_robbery_negative":
        "범인에게 취득할 권리가 있는 재산상 이익은 불법한 이익이 아니므로, 이를 폭행·협박으로 "
        "취득하여도 강도죄가 아니라 폭행죄 또는 협박죄가 성립한다.",
}

# 2부 확인 5건 — 무응답이므로 감사 판정 유지
USER_CHECK_DECISION = "context_only"
USER_CHECK_NOTE = ("2부 무응답 → 감사 판정(축 강등) 유지. art332_sec5_1.residential_intrusion_absorption은 "
                   "재산죄에서 살린 art329_sec8_3과 짝이므로 살리기로 하면 이 항목만 바꾸면 된다.")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> None:
    audit = read_json(AUDIT)
    groups = audit["doctrine_groups"]
    selected = {cid for cids, _, _ in DOCTRINE_DECISIONS.values() for cid in cids}
    all_options = {cid for gid in groups for cid in groups[gid]["options"]}

    if unknown := selected - all_options:
        raise SystemExit(f"선택 카드가 그룹에 없다: {sorted(unknown)}")
    if missing := set(groups) - set(DOCTRINE_DECISIONS):
        raise SystemExit(f"결정이 없는 그룹: {sorted(missing)}")
    if extra := set(REWRITE) - selected:
        raise SystemExit(f"선택되지 않은 카드에 재작성이 있다: {sorted(extra)}")

    ledger: list[dict[str, Any]] = []
    stats: Counter = Counter()
    rows: list[dict[str, Any]] = []

    for row in audit["rows"]:
        cid, role = row["card_id"], row["audit_role"]
        entry = {"card_id": cid, "article": row["article"], "module": row["module"],
                 "polarity": row["polarity"], "proposition": row["proposition"],
                 "merge_role": row["merge_role"], "final_role": role,
                 "demoted_at": None, "reason": row["reason"] or None}

        if role == "doctrine_choice":
            gid = next(g for g in groups if cid in groups[g]["options"])
            picked, answer, why = DOCTRINE_DECISIONS[gid]
            if cid in picked:
                entry.update(final_role="standard_input", promoted_from_variant=True,
                             doctrine_selected={"group": gid, "resolution": "user",
                                                "user_comment": answer, "rationale": why},
                             reason=None)
                if new := REWRITE.get(cid):
                    entry["prev_proposition"] = entry["proposition"]
                    entry["proposition"] = new
                    entry["rewrite_reason"] = "학설 어법 제거 — 선택된 견해를 실무규칙으로 진술"
                    stats["rewritten"] += 1
                stats["promoted"] += 1
                ledger.append({"card_id": cid, "kind": "promote", "group": gid,
                               "user_answer": answer, "reason": why})
            else:
                entry.update(final_role="context_only", demoted_at="doctrine_choice",
                             reason=f"학설 그룹 {gid}에서 선택되지 않았다 — 학설 소개로 남긴다.")
                stats["doctrine_demoted"] += 1
        elif role == "user_check":
            entry.update(final_role=USER_CHECK_DECISION, demoted_at="user_check_no_answer",
                         reason=f"{row['reason']} {USER_CHECK_NOTE}")
            stats["user_check_demoted"] += 1
            ledger.append({"card_id": cid, "kind": "user_check_default",
                           "reason": USER_CHECK_NOTE})
        elif role == "context_only":
            entry.update(demoted_at="supplement_audit")
            stats["audit_demoted"] += 1
        else:
            stats["core_kept"] += 1

        # 감사 단계에서 확정된 재작성·중복병합 반영
        if new := audit["rewrites"].get(cid, {}).get("new"):
            entry["prev_proposition"] = entry["proposition"]
            entry["proposition"] = new
            entry["rewrite_reason"] = audit["rewrites"][cid]["reason"]
            stats["rewritten"] += 1
        if cid in audit["duplicate_merges"]:
            entry["merged_into"] = audit["duplicate_merges"][cid]["kept"]

        rows.append(entry)

    core = read_json(CORE_V8)
    known = {row["card_id"] for row in core["rows"]}
    if overlap := known & {row["card_id"] for row in rows}:
        raise SystemExit(f"v8과 카드가 겹친다: {sorted(overlap)[:3]}")
    core["rows"].extend(rows)
    kept = [row for row in core["rows"]
            if row["final_role"] not in ("context_only", "deferred_track")]
    core["version"] = "9.0.0"
    core["supersedes"] = CORE_V8.name
    core["counts"]["core_final"] = len(kept)
    core["counts"]["supplement_articles"] = audit["articles"]
    core["counts"]["supplement_core"] = sum(
        1 for row in rows if row["final_role"] not in ("context_only", "deferred_track"))
    core["per_article_core"] = dict(sorted(Counter(row["article"] for row in kept).items()))
    CORE_V9.write_text(json.dumps(core, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    LEDGER.write_text(json.dumps({
        "version": "1.0.0", "api_calls": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source": "보강3조문_검토요청.md (1부 학설선택 10그룹 · 2부 확인 5건 무응답)",
        "corrections_by_user": {
            "art333.prior_state_use": DOCTRINE_DECISIONS["art333.prior_state_use"][2],
            "art333.right_exercise": DOCTRINE_DECISIONS["art333.right_exercise"][2],
        },
        "user_check_default": USER_CHECK_NOTE,
        "stats": dict(stats), "entries": ledger,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    supplement_core = [row for row in rows
                       if row["final_role"] not in ("context_only", "deferred_track")]
    print(f"승격 {stats['promoted']} / 학설강등 {stats['doctrine_demoted']} / "
          f"확인강등 {stats['user_check_demoted']} / 재작성 {stats['rewritten']}")
    print(f"보강분 core {len(supplement_core)}장 "
          f"{dict(sorted(Counter(r['article'] for r in supplement_core).items()))}")
    print(f"  극성 {dict(Counter(r['polarity'] for r in supplement_core))}")
    print(f"재산죄 전체 core {len(kept)}장 (v8 422 + 보강 {len(supplement_core)})")


if __name__ == "__main__":
    main()
