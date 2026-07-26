"""절 계층(ancestry) 기반 재감사 — 잎 절 제목만 보던 것을 조상 절까지 타고 올라간다.

기존 S1/S2 축은 카드가 붙은 **잎 절의 제목**만 봤다. 그래서 이런 것들이 새어 나갔다.

  art350 Ⅹ.5 "5. 체포·감금죄"        ← 잎 제목엔 죄수 표지가 없다
         Ⅹ   "Ⅹ. 죄수"                 ← 부모가 죄수다
  art329 "3. 주거침입죄(형법 제319조 내지 제321조)와의 관계"
                                       ← 괄호가 끼어 `[가-힣]죄와의 관계` 패턴을 빗나갔다

또 학설선택 승격이 이중매매 트랙을 우회했다. 승격은 v3 rows에 없는 카드를 새로 만들기
때문에 트랙 이관 여부를 볼 수 없었다. 모듈 단위로 다시 막는다.

정리하면 감사 신호는 셋을 함께 봐야 한다.
  ① 절 계층 (자기 절 + 모든 조상 절)
  ② 모듈이 별도 트랙인지
  ③ 명제 문언 (마지막 안전망)

API 0회.
"""

from __future__ import annotations

import glob
import json
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROP = ROOT / "data/rulegen/property"

CONC = re.compile(r"죄수|다른 죄와의 관계|타죄와의 관계|기타의? 죄와의 관계"
                  r"|죄.{0,30}와의 관계|법위반죄와의 관계|본죄와 다른 죄")
COMP = re.compile(r"공범관계|공범")
# 명제 문언 안전망 — 절 정보가 없거나 어긋날 때
PROP_CONC = re.compile(r"경합범|상상적 경합|실체적 경합|포괄일죄|법조경합|불가벌적 사후행위"
                       r"|흡수관계|흡수된다|별죄를 구성|별도로? .{0,10}죄가 성립|일죄만 성립")
DEFERRED_MODULES = {("art355", "sec5_3")}  # 부동산 이중매매 트랙


def build_maps():
    path_title: dict[tuple[str, str], str] = {}   # (article, section_path) -> title
    cid_info: dict[str, tuple[str, str]] = {}     # comment_id -> (article, section_path)
    for p in glob.glob(str(ROOT / "data/rulegen/campaign/*_rulegen_requests.jsonl")):
        art = Path(p).name.split("_")[0]
        with open(p, encoding="utf-8") as f:
            for line in f:
                for ch in json.loads(line).get("commentary_chunks", []):
                    sp, st = ch.get("section_path"), ch.get("section_title")
                    if sp and st:
                        path_title[(art, sp)] = st
                        cid_info[ch["comment_id"]] = (art, sp)
    return path_title, cid_info


def ancestry_titles(art: str, sp: str, path_title: dict) -> list[str]:
    """자기 절 + 모든 조상 절 제목. 'Ⅹ.5' → ['5. 체포·감금죄', 'Ⅹ. 죄수']"""
    out, parts = [], sp.split(".")
    for i in range(len(parts), 0, -1):
        t = path_title.get((art, ".".join(parts[:i])))
        if t:
            out.append(t)
    return out


def main() -> None:
    path_title, cid_info = build_maps()
    card_titles: dict[str, list[str]] = {}
    for p in glob.glob(str(PROP / "remediated/*/*.json")):
        for c in json.loads(Path(p).read_text(encoding="utf-8")).get("cards", []):
            ts: list[str] = []
            for r in c.get("source_refs", []):
                info = cid_info.get(r.get("comment_id", ""))
                if info:
                    ts += ancestry_titles(info[0], info[1], path_title)
            card_titles[c["id"]] = sorted(set(ts))

    core = json.loads((PROP / "property_core_set_final_v5.json").read_text(encoding="utf-8"))
    rows = {r["card_id"]: r for r in core["rows"]}
    stats, hits = Counter(), []

    for r in rows.values():
        if r["final_role"] in ("context_only", "deferred_track"):
            continue
        cid = r["card_id"]
        ts = card_titles.get(cid, [])
        if (r["article"], r["module"]) in DEFERRED_MODULES:
            r.update(final_role="deferred_track", deferred_to="부동산 이중매매",
                     reason="이중매매 모듈 — 별도 트랙(승격 우회분 회수)")
            stats["deferred_recovered"] += 1
            hits.append({"card_id": cid, "axis": "deferred_module", "titles": ts})
            continue
        why = None
        if any(CONC.search(t) for t in ts):
            why = "죄수·다른죄 관계 절(계층) — 다른 죄명의 성부는 이 조문의 요건이 아님"
            stats["concurrence_ancestry"] += 1
        elif any(COMP.search(t) for t in ts):
            why = "공범관계 절(계층) — 형법총칙 영역"
            stats["complicity_ancestry"] += 1
        elif PROP_CONC.search(r["proposition"]):
            why = "죄수·경합 문언 — 절 정보로 잡히지 않은 안전망 적발"
            stats["concurrence_proposition"] += 1
        if why:
            r.update(final_role="context_only", demoted_at="section_ancestry_audit", reason=why)
            hits.append({"card_id": cid, "axis": why[:20], "titles": ts,
                         "proposition": r["proposition"][:160],
                         "was_promoted": bool(r.get("promoted_from_variant"))})

    kept = [r for r in rows.values() if r["final_role"] not in ("context_only", "deferred_track")]
    core["rows"] = list(rows.values())
    core["version"] = "6.0.0"
    core["counts"]["demoted_section_ancestry"] = sum(stats.values())
    core["counts"]["core_final"] = len(kept)
    (PROP / "property_core_set_final_v6.json").write_text(
        json.dumps(core, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (PROP / "section_ancestry_audit.json").write_text(json.dumps({
        "version": "1.0.0", "api_calls": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "method": "절 계층(자기+조상) + 별도트랙 모듈 + 명제 문언 안전망",
        "stats": dict(stats), "hits": hits,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print("절 계층 재감사")
    for k, v in sorted(stats.items()):
        print(f"  {k}: {v}")
    print(f"  그중 학설승격분: {sum(1 for h in hits if h.get('was_promoted'))}")
    print(f"\n재산죄 core {len(kept)}장 (이전 437)")


if __name__ == "__main__":
    main()
