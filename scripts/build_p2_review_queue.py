"""P2(비재산 형법각칙) NormCard 벌크 검토자료 생성 (API 0회, 전부 로컬).

`build_property_review_queue.py`(P1 재산죄)를 그대로 이식한다 — 새 정책을 만들지 않는다.
사용자 지시(세션 a9e15d21, 2026-07-21 "3.1~3.5") 라우팅 규칙은 죄종-불문이므로 재사용:

  3.1 학설 대립      → 판례가 방향을 가리면 자동 확정, 없으면 사람 큐.
  3.2 authority      → 라벨 문제는 결정론 정규화, 판례 인용 상향만 사람.
  3.3 overgeneralization/source_scope → 전량 사람 큐.
  3.4 polarity/negative → 사람은 긍정형 질의문 초안 **승인**만(초안 자체는 별도 작성 필요).
  3.5 golden 결론 라벨 → front-load, 데이터에 정답 없음.

P1과 다른 점은 SLUGS 목록과 출력 경로뿐이다(law_id는 전부 형법 001692로 동일).
`article_no_of`만 "제258조의2"류(가지번호) 슬러그를 처리하도록 확장했다.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DS_ROOT = PROJECT_ROOT / ".cache/llm/runs/rulegen_downstream"
CAMPAIGN = PROJECT_ROOT / "data/rulegen/campaign"
OUT = PROJECT_ROOT / "data/rulegen/p2"
PRECEDENTS = Path("/data5/jaehoonjeong/sp/data/processed/Case_DB/clean_open_precedents.parquet")
COMMENTARY_DOCS = Path("/data5/jaehoonjeong/sp/data/serve/commentary_chunks/docs.parquet")
MANIFEST = CAMPAIGN / "kcl_substantive_campaign_manifest.json"


def load_p2_slugs() -> list[str]:
    m = json.loads(MANIFEST.read_text(encoding="utf-8"))
    return [t["issue_tag"] for t in m["targets"]]


P2_SLUGS = load_p2_slugs()

UPGRADE_RE = re.compile(
    r"reported[_ -]precedent(로|으로| category|,)|판례 보고 카드로 분류|"
    r"precedent authority|as commentary-reported precedent|판례로 분류"
)

CONFLICT_RE = re.compile(r"대립|나뉜다|갈린다|보나,|보지만|하나,\s*판례|설과\s*.{0,10}설")
AGREE_RE = re.compile(
    r"통설\s*[·ㆍ,]\s*판례|판례\s*[·ㆍ,]\s*통설|다수설\s*[·ㆍ,]\s*판례|"
    r"판례와\s*(통설|다수설)|(통설|다수설)과\s*판례"
)
FOREIGN_RE = re.compile(r"(일본|독일|영미|프랑스|미국)\s*(제\s*\d+\s*설|학설|통설|판례|형법)")
_STOP = {"경우", "사안", "관련", "여부", "판단", "인정", "성립", "해당", "행위", "사람", "대하여",
         "관하여", "때문", "이상", "다음", "위하여", "사정", "내용", "취지", "원심", "피고인"}


def key_terms(text: str) -> set[str]:
    return {w for w in re.findall(r"[가-힣]{3,}", text or "") if w not in _STOP}


HUMAN_TYPES = {"overgeneralization", "source_scope"}
VARIANT_TYPES = {"missing_variant", "collapsed_variant"}
AUTO_TYPES = {"authority_mismatch"}
ENTAILMENT_TYPES = {"source_entailment", "rule_mismatch"}
POLARITY_TYPES = {"formalization_error"}

STRUCTURAL_TARGETS = ("coverage_gaps", "legal_review_questions", "candidate_refs",
                      "review_required", "source_scope")
LEGAL_TARGETS = ("proposition", "polarity", "norm_kind", "formalization",
                 "variant_group", "review_notes")


def target_kind(target_path: str | None) -> str:
    tp = (target_path or "").replace("/", ".")
    for k in STRUCTURAL_TARGETS:
        if k in tp:
            return "structural"
    for k in LEGAL_TARGETS:
        if k in tp:
            return "legal"
    return "legal" if "cards" in tp else "structural"


def load_precedents() -> dict[str, dict[str, str]]:
    import pyarrow.parquet as pq

    t = pq.read_table(
        PRECEDENTS,
        columns=["사건번호", "법원명", "사건명", "판시사항", "판결요지", "참조조문"],
    )
    idx: dict[str, dict[str, str]] = {}
    for no, court, name, hold, gist, refs in zip(
        t["사건번호"].to_pylist(), t["법원명"].to_pylist(), t["사건명"].to_pylist(),
        t["판시사항"].to_pylist(), t["판결요지"].to_pylist(), t["참조조문"].to_pylist(),
    ):
        if not no:
            continue
        key = str(no).replace(" ", "")
        if key in idx:
            continue
        idx[key] = {
            "case_no": key, "court": court or "", "case_name": (name or "")[:80],
            "판시사항": (hold or "").replace("\n", " ")[:500],
            "판결요지": (gist or "").replace("\n", " ")[:500],
            "참조조문": (refs or "")[:200],
        }
    return idx


def load_commentary_citations() -> dict[str, list[str]]:
    import pyarrow.parquet as pq

    t = pq.read_table(COMMENTARY_DOCS, columns=["comment_id", "cited_cases"])
    out: dict[str, list[str]] = {}
    for cid, cases in zip(t["comment_id"].to_pylist(), t["cited_cases"].to_pylist()):
        if cid:
            out[cid] = [str(c).replace(" ", "") for c in (cases or [])]
    return out


def article_no_of(slug: str) -> str:
    """art250 -> '제250조', art2582_2 -> '제258조의2' (가지번호 슬러그 처리)."""
    body = slug.replace("art", "")
    m = re.match(r"^(\d+)(?:_(\d+))?$", body)
    if not m:
        return ""
    main, sub = m.groups()
    return f"제{main}조의{sub}" if sub else f"제{main}조"


def card_sources(card: dict[str, Any]) -> list[str]:
    return [r.get("comment_id", "") for r in card.get("source_refs", [])]


def load_drafts() -> dict[str, dict[str, Any]]:
    """3.4 긍정형 질의문 초안 — P2용은 아직 작성 전이면 빈 딕셔너리(전량 사람 큐 대상 표시)."""
    p = OUT / "p2_negative_query_drafts.json"
    if not p.exists():
        return {}
    return {x["card_id"]: x for x in json.loads(p.read_text(encoding="utf-8"))["items"]}


def main() -> None:
    case_idx = load_precedents()
    cite_map = load_commentary_citations()
    drafts = load_drafts()
    OUT.mkdir(parents=True, exist_ok=True)

    queue: list[dict[str, Any]] = []
    auto: list[dict[str, Any]] = []
    agent_fix: list[dict[str, Any]] = []
    core_cards: list[dict[str, Any]] = []
    variant_pool: dict[str, list[dict[str, Any]]] = defaultdict(list)
    stats: Counter = Counter()
    missing_runs: list[str] = []

    for slug in P2_SLUGS:
        run = DS_ROOT / slug / slug
        if not run.exists():
            missing_runs.append(slug)
            continue

        cards_by_id: dict[str, dict[str, Any]] = {}
        for cp in sorted((run / "norm_cards").glob("*.json")):
            cs = json.loads(cp.read_text(encoding="utf-8"))
            for card in cs.get("cards", []):
                cards_by_id[card["id"]] = card
                form = card.get("formalization")
                stats[f"card_{form}"] += 1

                if form in ("deterministic_rule", "standard_input"):
                    core_cards.append({
                        "article": slug, "card_id": card["id"], "module": cp.stem,
                        "formalization": form, "polarity": card.get("polarity"),
                        "proposition": card.get("proposition", "")[:300],
                        "authority_basis": card.get("authority_basis"),
                        "doctrinal_status": card.get("doctrinal_status"),
                        "human_review": {"decision": None, "notes": None},
                    })

                if form == "policy_variant":
                    cases: list[str] = []
                    for cid in card_sources(card):
                        cases.extend(cite_map.get(cid, []))
                    cases = sorted({
                        c for c in cases
                        if c in case_idx and "대법원" in case_idx[c]["court"]
                        and case_idx[c]["판시사항"].strip()
                    })
                    variant_pool[slug].append({
                        "card": card, "module": cp.stem, "quote_cases": cases,
                    })

                if card.get("polarity") == "negative" and form in (
                    "deterministic_rule", "standard_input"
                ):
                    prop = card.get("proposition", "")
                    double_neg = bool(re.search(r"(없|않|아니|못)[^.]{0,25}(없|않|아니|못)", prop))
                    dr = drafts.get(card["id"], {})
                    nq = dr.get("neural_query")
                    stats["negative_cards"] += 1
                    if not nq:
                        stats["negative_query_pending_draft"] += 1
                        continue
                    if double_neg:
                        stats["negative_double"] += 1
                    queue.append({
                        "type": "3.4_negative_query",
                        "priority": 2 if double_neg else 3,
                        "article": slug, "card_id": card["id"],
                        "double_negative": double_neg,
                        "message": "부정형 카드 — A6 host 극성분리. 아래 긍정형 질의문 초안을 confirm 또는 수정.",
                        "proposition": prop[:400],
                        "draft_neural_query": nq,
                        "recommended_action": ("초안 문장과 card_status_when_query_satisfied(반전/동행)를 함께 확인. "
                                               "수정 시 approved_query에 최종 문장을 적는다."),
                        "human_review": {"decision": None, "notes": None,
                                         "approved_query": None,
                                         "approved_status_when_satisfied": None},
                    })

        groups: dict[Any, list[dict[str, Any]]] = defaultdict(list)
        for e in variant_pool[slug]:
            groups[(e["module"], e["card"].get("variant_group"))].append(e)
        art_no = article_no_of(slug)
        for (module, vg), members in groups.items():
            competing = vg is not None and len(members) > 1
            blob = " ".join(
                (o["card"].get("proposition", "") or "")
                + " " + " ".join(r.get("quote", "") for r in o["card"].get("source_refs", []))
                for o in members
            )
            group_conflict = bool(CONFLICT_RE.search(blob)) and not AGREE_RE.search(blob)

            live: list[dict[str, Any]] = []
            for e in members:
                card, cases = e["card"], e["quote_cases"]
                prop = card.get("proposition", "") or ""

                if not competing:
                    stats["variant_auto_context_only_solo"] += 1
                    auto.append({
                        "kind": "variant_demoted_context_only",
                        "rule": "경쟁 카드 없음 → 선택 가능한 정책 단위가 아님",
                        "article": slug, "module": module, "card_id": card["id"],
                        "variant_group": vg, "proposition": prop[:300],
                        "action": "formalization을 context_only로 강등(RAG 문맥으로만 사용)",
                        "human_review": {"decision": None, "notes": None},
                    })
                    continue

                if FOREIGN_RE.search(prop):
                    stats["variant_auto_context_only_foreign"] += 1
                    auto.append({
                        "kind": "variant_demoted_context_only",
                        "rule": "비교법 학설 소개(외국) → 한국 판례·실무 선택지가 아님",
                        "article": slug, "module": module, "card_id": card["id"],
                        "variant_group": vg, "proposition": prop[:300],
                        "action": "formalization을 context_only로 강등",
                        "human_review": {"decision": None, "notes": None},
                    })
                    continue

                live.append(e)

            if not live:
                continue
            ev: list[str] = []
            for o in live:
                for c in o["quote_cases"]:
                    if art_no and art_no in case_idx[c]["참조조문"] and c not in ev:
                        ev.append(c)
            tier = ("명시적대립" if group_conflict else "경쟁견해")
            tier += "_판례있음" if ev else "_판례없음"
            stats[f"variant_group_{tier}"] += 1
            stats["variant_cards_in_groups"] += len(live)
            queue.append({
                "type": "3.1_variant_group", "tier": tier, "priority": 1,
                "article": slug, "module": module, "variant_group": vg,
                "cards_resolved_by_one_decision": len(live),
                "explicit_conflict_marker": group_conflict,
                "message": ("경쟁 견해 그룹. 아래 판시사항을 보고 **어느 견해가 판례·실무 입장인지 한 번만** "
                            "고르면 이 그룹 카드가 전부 정리된다."),
                "options": [
                    {"card_id": o["card"]["id"],
                     "proposition": (o["card"].get("proposition", "") or "")[:300]}
                    for o in live
                ],
                "precedent_evidence": [
                    {k: case_idx[c][k] for k in
                     ("case_no", "court", "case_name", "판시사항", "참조조문")}
                    for c in ev[:2]
                ],
                "recommended_action": ("판례·실무 입장인 card_id를 선택(나머지는 context_only 강등). "
                                       "판시사항이 해소하지 못하면 실무 관행으로 지정."),
                "human_review": {"decision": None, "chosen_card_id": None, "notes": None},
            })

        for sp in sorted((run / "sol").glob("*.json")):
            rep = json.loads(sp.read_text(encoding="utf-8"))
            for f in rep.get("findings", []):
                ftype = f.get("type", "other")
                base = {
                    "article": slug, "finding_id": f.get("finding_id"),
                    "severity": f.get("severity"), "target_path": f.get("target_path"),
                    "message": f.get("message", "")[:500],
                    "recommended_action": f.get("recommended_action", "")[:400],
                }

                if ftype in AUTO_TYPES:
                    blob = (f.get("recommended_action", "") or "") + " " + (f.get("message", "") or "")
                    is_upgrade = bool(UPGRADE_RE.search(blob))
                    tp = f.get("target_path", "") or ""
                    if is_upgrade and "legal_review_questions" not in tp:
                        stats["authority_human_upgrade"] += 1
                        queue.append({**base, "type": "3.2_authority_upgrade", "priority": 2,
                                      "note": "출처가 실제 판례를 인용 → 판례 인덱스 대조 필요(정규화로 자동 상향 금지)",
                                      "human_review": {"decision": None, "notes": None}})
                    else:
                        stats["authority_auto"] += 1
                        auto.append({**base, "kind": "authority_normalized",
                                     "rule": "3.2 라벨 문제(P1 포렌식 근거 재사용: rules/·rule_ir 0 hit)",
                                     "action": "doctrinal_status/authority_basis를 bounded source 최약값으로 결정론 하향"})

                elif ftype in HUMAN_TYPES:
                    if target_kind(f.get("target_path")) == "structural":
                        stats["agent_fix_구조성_source_scope"] += 1
                        agent_fix.append({**base, "type": ftype,
                                          "note": "구조성 지적(coverage_gaps·review_question·candidate_refs) → 법률 결정점 아님"})
                    else:
                        stats["overgeneralization_human"] += 1
                        queue.append({**base, "type": "3.3_overgeneralization", "priority": 1,
                                      "note": "사용자 지시: 이건 사람검토 필요",
                                      "human_review": {"decision": None, "notes": None}})

                elif ftype in VARIANT_TYPES:
                    if target_kind(f.get("target_path")) == "structural":
                        stats["agent_fix_구조성_variant"] += 1
                        agent_fix.append({**base, "type": ftype, "note": "구조성 지적 → 에이전트 처리"})
                    else:
                        stats["variant_finding"] += 1
                        queue.append({**base, "type": "3.1_variant_finding", "priority": 1,
                                      "note": "학설대립 관련 지적 — 판례 방향 확인 후 실무규칙 확정",
                                      "human_review": {"decision": None, "notes": None}})

                elif ftype in POLARITY_TYPES:
                    tp = (f.get("target_path") or "").replace("/", ".")
                    if any(k in tp for k in ("polarity", "norm_kind", "formalization")):
                        stats["polarity_class_human"] += 1
                        queue.append({**base, "type": "3.4_polarity_classification", "priority": 2,
                                      "note": "사용자 지시 3.4 대상 — polarity/norm_kind/formalization 분류는 법률 판단",
                                      "human_review": {"decision": None, "notes": None}})
                    else:
                        stats["agent_fix_formalization_기타"] += 1
                        agent_fix.append({**base, "type": ftype, "note": "구조성 → 에이전트 처리"})

                elif ftype in ENTAILMENT_TYPES:
                    if target_kind(f.get("target_path")) == "legal":
                        stats["entailment_human"] += 1
                        queue.append({**base, "type": "3.3_source_entailment", "priority": 1,
                                      "note": "출처가 명제를 지지하는지 = 출처-범위 판단(3.3 성격)",
                                      "human_review": {"decision": None, "notes": None}})
                    else:
                        stats["agent_fix_entailment_구조성"] += 1
                        agent_fix.append({**base, "type": ftype, "note": "구조성 → 에이전트 처리"})

                else:
                    stats[f"agent_fix_{ftype}"] += 1
                    agent_fix.append({**base, "type": ftype,
                                      "note": "법률-의미 결정점 아님 → 에이전트 remediation 후 spot-check"})

    golden = {
        "version": "1.0.0",
        "note": "3.5 — 데이터에 gold 결론 라벨이 없어 사용자가 유일한 정답 원천. compile 전 필수.",
        "status": "labels_pending",
        "scenarios": [],
        "blocked_on": "RuleIR 생성(=벌크 HITL 통과) 후 시나리오 생성 가능",
    }

    payload = {
        "version": "1.0.0",
        "api_calls": 0,
        "scope": f"P2(비재산) 형법각칙 {len(P2_SLUGS)}조문",
        "routing_source": "사용자 지시 3.1~3.5 (세션 a9e15d21, 2026-07-21) — P1과 동일 정책 재사용",
        "missing_runs": missing_runs,
        "counts": dict(sorted(stats.items())),
        "queue_size": len(queue),
        "auto_size": len(auto),
        "agent_fix_size": len(agent_fix),
        "core_cards": len(core_cards),
    }

    (OUT / "p2_review_summary.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    queue.sort(key=lambda q: (q.get("priority", 9), q["type"], q["article"]))
    (OUT / "p2_norm_card_review_queue.json").write_text(
        json.dumps({"version": "1.0.0", "api_calls": 0, "items": queue}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    (OUT / "p2_auto_decisions_ledger.json").write_text(
        json.dumps({"version": "1.0.0", "api_calls": 0, "items": auto}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    (OUT / "p2_agent_remediation_queue.json").write_text(
        json.dumps({"version": "1.0.0", "api_calls": 0, "items": agent_fix}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    (OUT / "p2_core_card_review.json").write_text(
        json.dumps({"version": "1.0.0", "api_calls": 0, "note": "원칙 14: 실행 core 전수 노출",
                    "cards": core_cards}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "p2_scallop_golden_cases.json").write_text(
        json.dumps(golden, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
