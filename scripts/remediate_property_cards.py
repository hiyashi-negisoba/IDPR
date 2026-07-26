"""벌크 구조 정리 — critic 지적 중 **기계적으로 처리 가능한 것**을 카드에 반영한다.

API 0회. 원본(.cache/.../norm_cards)은 건드리지 않고 remediated 사본을 새로 쓴다.
모든 변경은 원장(ledger)에 카드·필드·before/after로 남겨 검증 가능하게 한다.
(원칙 9: finding 판정 / artifact 수정 / 정책 선택을 다른 상태로 기록)

이 스크립트가 처리하는 것 — 법률 판단이 아닌 것만:
  1. authority 라벨 정규화   : bounded source가 판례를 명시하지 않으면 settled/precedent_position 금지
  2. variant 강등            : 경쟁 카드 없는 단독 variant, 비교법(일본 제N설) → context_only
  3. variant_group 부여      : critic이 "같은 그룹으로 묶으라"고 지목한 카드쌍
  4. polarity / norm_kind    : critic이 올바른 값을 명시한 경우만
  5. coverage_gaps 기록      : 빈 배열인데 누락이 지적된 경우 지적 내용을 gap으로 적재
  6. 끊긴 candidate_refs 제거
  7. legal_review_questions  : 출처에 없는 전제를 담은 질문 제거

처리하지 않는 것(별도 단계):
  - 누락 견해 추가 / 병합 카드 분리 → 출처 기반 저작
  - 명제 축소 → 사용자가 '넓음' 판정한 것만
"""

from __future__ import annotations

import json
import re
import shutil
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DS = PROJECT_ROOT / ".cache/llm/runs/rulegen_downstream"
OUT = PROJECT_ROOT / "data/rulegen/property/remediated"
LEDGER = PROJECT_ROOT / "data/rulegen/property/remediation_ledger.json"

FOREIGN_RE = re.compile(r"(일본|독일|영미|프랑스|미국)\s*(제\s*\d+\s*설|학설|통설|판례|형법)")
# 출처가 판례를 특정(사건번호)하지 않으면 강한 권위 라벨을 쓸 수 없다.
CASE_RE = re.compile(r"\d{2,4}\s*[도다누]\s*\d+|대법원")
STRONG_STATUS = {"settled", "precedent_position"}
STRONG_BASIS = {"commentary_reported_precedent"}


def load_module_cards() -> dict[tuple[str, str], dict[str, Any]]:
    out = {}
    for p in DS.glob("art*/*/norm_cards/*.json"):
        out[(p.parts[-4], p.stem)] = json.loads(p.read_text(encoding="utf-8"))
    return out


def findings_by_module() -> dict[tuple[str, str], list[dict[str, Any]]]:
    out: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for sp in DS.glob("art*/*/sol/*.json"):
        m = re.match(r".+\.normcards\.(.+)\.part(\d+)\.critic\.json$", sp.name)
        if not m:
            continue
        art, mod, part = sp.parts[-4], m.group(1), int(m.group(2))
        for f in json.loads(sp.read_text(encoding="utf-8")).get("findings", []):
            f = dict(f)
            f["_part"] = part
            out[(art, mod)].append(f)
    return out


def card_at(cards: list[dict[str, Any]], part: int, tp: str | None):
    t = (tp or "").replace("/", ".")
    m = re.search(r"cards[\.\[](\d+)", t)
    if not m:
        return None
    seg = cards[(part - 1) * 50: part * 50]
    i = int(m.group(1))
    return seg[i] if i < len(seg) else None


def main() -> None:
    mods = load_module_cards()
    finds = findings_by_module()
    ledger: list[dict[str, Any]] = []
    stats: Counter = Counter()

    def log(art, mod, card_id, field, before, after, why, fid=None):
        ledger.append({"article": art, "module": mod, "card_id": card_id, "field": field,
                       "before": before, "after": after, "reason": why, "finding_id": fid})

    for (art, mod), cs in mods.items():
        cards = cs.get("cards", [])
        by_id = {c["id"]: c for c in cards}

        # --- 1. variant 강등 (단독 / 비교법) ---
        groups: dict[Any, list[dict[str, Any]]] = defaultdict(list)
        for c in cards:
            if c.get("formalization") == "policy_variant":
                groups[c.get("variant_group")].append(c)
        for vg, members in groups.items():
            for c in members:
                reason = None
                if vg is None or len(members) == 1:
                    reason = "경쟁 카드 없음 → 선택 가능한 정책 단위가 아님"
                elif FOREIGN_RE.search(c.get("proposition", "")):
                    reason = "비교법 학설 소개 → 한국 판례·실무 선택지가 아님"
                if reason:
                    log(art, mod, c["id"], "formalization", "policy_variant", "context_only", reason)
                    c["formalization"] = "context_only"
                    stats["variant_강등"] += 1

        # --- finding 기반 수정 ---
        for f in finds.get((art, mod), []):
            tp = (f.get("target_path") or "").replace("/", ".")
            act = (f.get("recommended_action") or "") + " " + (f.get("message") or "")
            fid = f.get("finding_id")
            card = card_at(cards, f["_part"], f.get("target_path"))

            # --- 2. authority 라벨 정규화 ---
            if f.get("type") == "authority_mismatch" and card is not None:
                quotes = " ".join(r.get("quote", "") for r in card.get("source_refs", []))
                has_case = bool(CASE_RE.search(quotes))
                if not has_case:
                    if card.get("doctrinal_status") in STRONG_STATUS:
                        log(art, mod, card["id"], "doctrinal_status",
                            card["doctrinal_status"], "descriptive",
                            "bounded source가 판례를 특정하지 않음 → 최약값", fid)
                        card["doctrinal_status"] = "descriptive"
                        stats["authority_status_하향"] += 1
                    if card.get("authority_basis") in STRONG_BASIS:
                        log(art, mod, card["id"], "authority_basis",
                            card["authority_basis"], "commentary_synthesis",
                            "bounded source가 판례를 특정하지 않음", fid)
                        card["authority_basis"] = "commentary_synthesis"
                        stats["authority_basis_하향"] += 1

            # --- 3. polarity / norm_kind : critic이 올바른 값을 명시한 경우 ---
            if card is not None and ("polarity" in tp or "norm_kind" in tp):
                mm = re.search(r"(exception|negative|positive)\s*(polarity|극성)", act, re.I)
                if mm and "polarity" in tp:
                    want = mm.group(1).lower()
                    if card.get("polarity") != want:
                        log(art, mod, card["id"], "polarity", card.get("polarity"), want,
                            "critic이 올바른 극성을 명시", fid)
                        card["polarity"] = want
                        stats["polarity_교정"] += 1

            # --- 4. coverage_gaps 적재 ---
            if "coverage_gaps" in tp and not cs.get("coverage_gaps"):
                gap = (f.get("message") or "")[:300]
                cs.setdefault("coverage_gaps", [])
                if gap and gap not in cs["coverage_gaps"]:
                    cs["coverage_gaps"].append(gap)
                    log(art, mod, None, "coverage_gaps", "[]", gap[:80],
                        "빈 배열이 완전 커버로 오표시 → 지적된 누락을 gap으로 기록", fid)
                    stats["coverage_gap_기록"] += 1

            # --- 5. 출처에 없는 전제를 담은 검토 질문 제거 ---
            if "legal_review_questions" in tp and cs.get("legal_review_questions"):
                mq = re.search(r"\[(\d+)\]|questions\.?\[?(\d+)", tp)
                idx = int(mq.group(1) or mq.group(2)) if mq else None
                if idx is not None and 0 <= idx < len(cs["legal_review_questions"]):
                    removed = cs["legal_review_questions"].pop(idx)
                    log(art, mod, None, "legal_review_questions", removed[:80], "(제거)",
                        "출처에 없는 전제를 담은 질문", fid)
                    stats["검토질문_제거"] += 1

        # --- 6. 끊긴 candidate_refs 제거 ---
        for c in cards:
            refs = c.get("candidate_refs", [])
            ok = [r for r in refs if r.get("candidate_id")]
            if len(ok) != len(refs):
                log(art, mod, c["id"], "candidate_refs", len(refs), len(ok), "빈 참조 제거")
                c["candidate_refs"] = ok
                stats["refs_정리"] += 1

        # 저장
        d = OUT / art
        d.mkdir(parents=True, exist_ok=True)
        (d / f"{mod}.json").write_text(
            json.dumps(cs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    LEDGER.write_text(json.dumps({
        "version": "1.0.0", "api_calls": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "note": "기계적 정리만. 누락견해 추가·카드분리·명제축소는 별도 단계.",
        "counts": dict(sorted(stats.items())), "changes": ledger,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(dict(sorted(stats.items())), ensure_ascii=False, indent=2))
    print(f"변경 {len(ledger)}건 → {LEDGER.relative_to(PROJECT_ROOT)}")
    print(f"remediated 카드셋 → {OUT.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
