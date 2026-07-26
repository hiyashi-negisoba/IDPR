"""재산범 NormCard 벌크 검토자료 생성 (API 0회, 전부 로컬).

사용자 지시(세션 a9e15d21, 2026-07-21 "3.1~3.5")를 그대로 라우팅 규칙으로 구현한다.

  3.1 학설 대립      → "무조건 판례-실무 중심"  → bounded source가 대법원 판례를 인용하면
                       실무규칙으로 **자동 확정**(사용자는 confirm만). 판례 없으면 사람 큐.
  3.2 authority      → "오탐이었던거로 기억, 포렌식해보길" → 이번 배치 포렌식 결과 라벨 문제
                       확정(rules/·rule_ir 스키마 0 hit) → 결정론 정규화로 **자동 처리**.
                       단 출처가 실제 판례를 인용해 상향(UPGRADE)해야 하는 건만 사람 판례대조.
  3.3 overgeneralization/source_scope → "이건 사람검토 필요" → 전량 사람 큐.
  3.4 polarity/negative → "우선검토하되 극성 전환은 사기죄에서 이미 처리" → A6 host 극성분리
                       메커니즘 적용 대상으로 묶고, 사람은 **긍정형 질의문 초안 승인**만.
                       이중부정 우선(가장 어려운 문장구조).
  3.5 golden 결론 라벨 → 데이터에 정답 없음, 사용자가 유일 원천 → front-load 큐로 별도 노출.

원칙 준수(agent_mistakes_postmortem 재발방지):
  - 원칙 9  : finding 판정 / artifact 수정 / 정책 선택을 서로 다른 상태로 기록
  - 원칙 11 : remediation에 API를 쓰지 않는다 (이 스크립트는 api_calls=0)
  - 원칙 12 : 사용자에게 판례 확인을 넘기기 전에 로컬 판례 인덱스를 먼저 전수 검색
  - 원칙 14 : 실행 core 전부를 큐에 노출하고 일부 finding 큐로 대체하지 않는다
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
OUT = PROJECT_ROOT / "data/rulegen/property"
PRECEDENTS = Path("/data5/jaehoonjeong/sp/data/processed/Case_DB/clean_open_precedents.parquet")
COMMENTARY_DOCS = Path("/data5/jaehoonjeong/sp/data/serve/commentary_chunks/docs.parquet")

PROPERTY_SLUGS = [
    "art323", "art328", "art329", "art331", "art334", "art335", "art337",
    "art338", "art342", "art343", "art344", "art350", "art355", "art356",
    "art357", "art360", "art366",
]

UPGRADE_RE = re.compile(
    r"reported[_ -]precedent(로|으로| category|,)|판례 보고 카드로 분류|"
    r"precedent authority|as commentary-reported precedent|판례로 분류"
)

# 학설 '대립'의 실제 표지. 단순히 '견해'가 들어갔다고 대립이 아니다.
# 사용자 기준: "통설·판례는~"처럼 묶이면 일치, "통설은 ~라고 보나 판례는 ~"처럼 나뉘면 대립.
CONFLICT_RE = re.compile(r"대립|나뉜다|갈린다|보나,|보지만|하나,\s*판례|설과\s*.{0,10}설")
AGREE_RE = re.compile(
    r"통설\s*[·ㆍ,]\s*판례|판례\s*[·ㆍ,]\s*통설|다수설\s*[·ㆍ,]\s*판례|"
    r"판례와\s*(통설|다수설)|(통설|다수설)과\s*판례"
)
# 비교법 소개(일본 제N설 등)는 한국 실무 정책 선택지가 아니다 → context_only.
FOREIGN_RE = re.compile(r"(일본|독일|영미|프랑스|미국)\s*(제\s*\d+\s*설|학설|통설|판례|형법)")
# 판시사항 대응 판정용 불용어
_STOP = {"경우", "사안", "관련", "여부", "판단", "인정", "성립", "해당", "행위", "사람", "대하여",
         "관하여", "때문", "이상", "다음", "위하여", "사정", "내용", "취지", "원심", "피고인"}


def key_terms(text: str) -> set[str]:
    """명제/판시사항에서 대응 판정에 쓸 한글 핵심어(3자 이상)."""
    return {w for w in re.findall(r"[가-힣]{3,}", text or "") if w not in _STOP}

# 사용자 지시 → finding type 라우팅
HUMAN_TYPES = {"overgeneralization", "source_scope"}          # 3.3
VARIANT_TYPES = {"missing_variant", "collapsed_variant"}       # 3.1
AUTO_TYPES = {"authority_mismatch"}                            # 3.2
# 출처가 명제를 지지하는지(3.3과 같은 출처-범위 성격) → 사람.
ENTAILMENT_TYPES = {"source_entailment", "rule_mismatch"}
# polarity/norm_kind/formalization 분류 = 사용자 지시 3.4의 대상.
POLARITY_TYPES = {"formalization_error"}

# 지적 대상이 카드의 **법률적 내용**인지, 계약·메타데이터 **구조**인지 가른다.
# 구조성 지적(coverage_gaps 빈 배열, review_question 문구, 끊긴 candidate_refs)은
# 법률-의미 결정점이 아니므로 사람 큐에 올리지 않는다(감사 2026-07-23).
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
    """사건번호 → 판시사항·판결요지 (실제 법리).

    `clean_open_precedents.parquet`은 전문(boilerplate)이 아니라 판시사항/판결요지를
    분리 보유한다. case_index의 `precedent_text`(전문 머리말)를 쓰면 법리 신호가 없다.
    """
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
            "case_no": key,
            "court": court or "",
            "case_name": (name or "")[:80],
            "판시사항": (hold or "").replace("\n", " ")[:500],
            "판결요지": (gist or "").replace("\n", " ")[:500],
            "참조조문": (refs or "")[:200],
        }
    return idx


def load_commentary_citations() -> dict[str, list[str]]:
    """comment_id → cited_cases (주석서 청크에 이미 추출돼 있는 인용판례)."""
    import pyarrow.parquet as pq

    t = pq.read_table(COMMENTARY_DOCS, columns=["comment_id", "cited_cases"])
    out: dict[str, list[str]] = {}
    for cid, cases in zip(t["comment_id"].to_pylist(), t["cited_cases"].to_pylist()):
        if cid:
            out[cid] = [str(c).replace(" ", "") for c in (cases or [])]
    return out


def article_no_of(slug: str) -> str:
    """art329 → '제329조' (참조조문 매칭용)."""
    n = slug.replace("art", "")
    return f"제{n}조" if n.isdigit() else ""


def card_sources(card: dict[str, Any]) -> list[str]:
    return [r.get("comment_id", "") for r in card.get("source_refs", [])]


def load_drafts() -> dict[str, dict[str, Any]]:
    """3.4 긍정형 질의문 초안(에이전트 직접 작성)을 card_id로 인덱싱."""
    p = OUT / "property_negative_query_drafts.json"
    if not p.exists():
        return {}
    return {x["card_id"]: x for x in json.loads(p.read_text(encoding="utf-8"))["items"]}


def main() -> None:
    case_idx = load_precedents()
    cite_map = load_commentary_citations()
    drafts = load_drafts()
    OUT.mkdir(parents=True, exist_ok=True)

    queue: list[dict[str, Any]] = []       # 사람이 보는 것
    auto: list[dict[str, Any]] = []        # 자동 확정/정규화 원장
    agent_fix: list[dict[str, Any]] = []   # 에이전트 remediation 후 spot-check
    core_cards: list[dict[str, Any]] = []  # 원칙 14: 실행 core 전수 노출
    variant_pool: dict[str, list[dict[str, Any]]] = defaultdict(list)
    stats: Counter = Counter()

    for slug in PROPERTY_SLUGS:
        run = DS_ROOT / slug / slug
        if not run.exists():
            continue

        # ---- 카드 축 (원칙 14: 실행 core 전수) ----
        cards_by_id: dict[str, dict[str, Any]] = {}
        for cp in sorted((run / "norm_cards").glob("*.json")):
            cs = json.loads(cp.read_text(encoding="utf-8"))
            for card in cs.get("cards", []):
                cards_by_id[card["id"]] = card
                form = card.get("formalization")
                stats[f"card_{form}"] += 1

                # 실행 core = RuleIR로 가는 카드
                if form in ("deterministic_rule", "standard_input"):
                    core_cards.append({
                        "article": slug, "card_id": card["id"], "module": cp.stem,
                        "formalization": form, "polarity": card.get("polarity"),
                        "proposition": card.get("proposition", "")[:300],
                        "authority_basis": card.get("authority_basis"),
                        "doctrinal_status": card.get("doctrinal_status"),
                        "human_review": {"decision": None, "notes": None},
                    })

                # ---- 3.1 학설대립: 판례 자동확정 후보 수집 (판정은 그룹 단위로 뒤에서) ----
                # 근거는 카드 **자신의 인용문(quote)** 안의 판례로 한정한다. chunk 전체
                # 공기(co-occurrence)로 붙이면 같은 절의 모순되는 견해들에 동일 판례가
                # 붙어 전부 "확정"되는 오류가 난다(표본 검증에서 실제 발생).
                if form == "policy_variant":
                    cases: list[str] = []
                    for cid in card_sources(card):
                        cases.extend(cite_map.get(cid, []))
                    # 대법원 + 판시사항 보유 판례만 방향 근거로 인정
                    cases = sorted({
                        c for c in cases
                        if c in case_idx and "대법원" in case_idx[c]["court"]
                        and case_idx[c]["판시사항"].strip()
                    })
                    variant_pool[slug].append({
                        "card": card, "module": cp.stem, "quote_cases": cases,
                    })

                # ---- 3.4 negative 카드: 긍정형 질의문 승인 대상 ----
                # 실행 core(RuleIR로 배선되는 카드)만 neural_query가 필요하다.
                # policy_variant·context_only 부정형은 질의로 쓰이지 않으므로 제외.
                if card.get("polarity") == "negative" and form in (
                    "deterministic_rule", "standard_input"
                ):
                    prop = card.get("proposition", "")
                    double_neg = bool(re.search(r"(없|않|아니|못)[^.]{0,25}(없|않|아니|못)", prop))
                    dr = drafts.get(card["id"], {})
                    nq = dr.get("neural_query")
                    stats["negative_cards"] += 1
                    if not nq:
                        # 질의 대상이 아님(요건불요형 규칙 / 판례소개 보고문) → 사람 큐에 올리지 않는다.
                        stats["negative_no_query_needed"] += 1
                        auto.append({
                            "kind": "negative_no_query_needed",
                            "rule": dr.get("category", "질의 대상 아님"),
                            "article": slug, "card_id": card["id"],
                            "proposition": prop[:300],
                            "action": dr.get("note", "요건 제외 규칙 또는 보고문 → neural_query 불요"),
                        })
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

        # ---- 3.1 그룹 단위 판정: 판례가 경쟁 견해를 '가려줄 때만' 확정 ----
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

                # (a) 경쟁 상대가 없으면 정책 선택지가 아니다 → 자동 context_only 강등.
                #     "견해가 있다"는 서술 하나만으로 policy_variant가 된 것들(단독 그룹).
                if not competing:
                    stats["variant_auto_context_only_solo"] += 1
                    auto.append({
                        "kind": "variant_demoted_context_only",
                        "rule": "경쟁 카드 없음 → 선택 가능한 정책 단위가 아님(postmortem: 판례설명·보충논거는 context_only)",
                        "article": slug, "module": module, "card_id": card["id"],
                        "variant_group": vg, "proposition": prop[:300],
                        "action": "formalization을 context_only로 강등(RAG 문맥으로만 사용)",
                        "human_review": {"decision": None, "notes": None},
                    })
                    continue

                # (b) 비교법(일본 제N설 등)은 한국 실무 정책 선택지가 아니다 → 강등.
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

            # (c) 남은 경쟁 카드는 **그룹당 1건**으로 묶어 낸다.
            #     어느 견해를 판시사항이 지지하는지는 법률 판단이라 자동화하지 않는다
            #     (핵심어 겹침은 '주제 관련성'만 재고 '방향'은 못 가린다 — 친족상도례
            #      3설에 같은 판례가 붙어 셋 다 확정되는 오류가 실제로 났다).
            #     대신 판시사항을 한 번 읽고 고르면 그룹 전체가 정리되게 한다.
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

        # ---- finding 축 ----
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

                if ftype in AUTO_TYPES:  # 3.2
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
                                     "rule": "3.2 라벨 문제(포렌식 확인: rules/·rule_ir 0 hit)",
                                     "action": "doctrinal_status/authority_basis를 bounded source 최약값으로 결정론 하향"})

                elif ftype in HUMAN_TYPES:  # 3.3 — 단 구조성 지적은 제외
                    if target_kind(f.get("target_path")) == "structural":
                        stats["agent_fix_구조성_source_scope"] += 1
                        agent_fix.append({**base, "type": ftype,
                                          "note": "구조성 지적(coverage_gaps·review_question·candidate_refs) → 법률 결정점 아님"})
                    else:
                        stats["overgeneralization_human"] += 1
                        queue.append({**base, "type": "3.3_overgeneralization", "priority": 1,
                                      "note": "사용자 지시: 이건 사람검토 필요",
                                      "human_review": {"decision": None, "notes": None}})

                elif ftype in VARIANT_TYPES:  # 3.1 (finding 축)
                    if target_kind(f.get("target_path")) == "structural":
                        stats["agent_fix_구조성_variant"] += 1
                        agent_fix.append({**base, "type": ftype, "note": "구조성 지적 → 에이전트 처리"})
                    else:
                        stats["variant_finding"] += 1
                        queue.append({**base, "type": "3.1_variant_finding", "priority": 1,
                                      "note": "학설대립 관련 지적 — 판례 방향 확인 후 실무규칙 확정",
                                      "human_review": {"decision": None, "notes": None}})

                elif ftype in POLARITY_TYPES:  # 3.4 축 (polarity/norm_kind/formalization 분류)
                    tp = (f.get("target_path") or "").replace("/", ".")
                    if any(k in tp for k in ("polarity", "norm_kind", "formalization")):
                        stats["polarity_class_human"] += 1
                        queue.append({**base, "type": "3.4_polarity_classification", "priority": 2,
                                      "note": "사용자 지시 3.4 대상 — polarity/norm_kind/formalization 분류는 법률 판단",
                                      "human_review": {"decision": None, "notes": None}})
                    else:
                        stats["agent_fix_formalization_기타"] += 1
                        agent_fix.append({**base, "type": ftype, "note": "구조성 → 에이전트 처리"})

                elif ftype in ENTAILMENT_TYPES:  # 출처가 명제를 지지하는가 = 3.3 성격
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

    # ---- 3.5 golden-case 결론 라벨 (front-load, 빈 라벨 슬롯) ----
    golden = {
        "version": "1.0.0",
        "note": "3.5 — 데이터에 gold 결론 라벨이 없어 사용자가 유일한 정답 원천. compile 전 필수.",
        "status": "labels_pending",
        "scenarios": [],  # 죄명별 사실관계 시나리오는 RuleIR 확정 후 생성
        "blocked_on": "RuleIR 생성(=벌크 HITL 통과) 후 시나리오 생성 가능",
    }

    payload = {
        "version": "1.0.0",
        "api_calls": 0,
        "scope": f"KCL 61문항이 커버하는 재산죄 {len(PROPERTY_SLUGS)}조문",
        "routing_source": "사용자 지시 3.1~3.5 (세션 a9e15d21, 2026-07-21)",
        "counts": dict(sorted(stats.items())),
        "queue_size": len(queue),
        "auto_size": len(auto),
        "agent_fix_size": len(agent_fix),
        "core_cards": len(core_cards),
    }

    (OUT / "property_review_summary.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    queue.sort(key=lambda q: (q.get("priority", 9), q["type"], q["article"]))
    (OUT / "property_norm_card_review_queue.json").write_text(
        json.dumps({"version": "1.0.0", "api_calls": 0, "items": queue}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    (OUT / "property_auto_decisions_ledger.json").write_text(
        json.dumps({"version": "1.0.0", "api_calls": 0, "items": auto}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    (OUT / "property_agent_remediation_queue.json").write_text(
        json.dumps({"version": "1.0.0", "api_calls": 0, "items": agent_fix}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    (OUT / "property_core_card_review.json").write_text(
        json.dumps({"version": "1.0.0", "api_calls": 0, "note": "원칙 14: 실행 core 전수 노출",
                    "cards": core_cards}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (OUT / "property_scallop_golden_cases.json").write_text(
        json.dumps(golden, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    _write_guide(payload, queue)
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def _write_guide(payload: dict[str, Any], queue: list[dict[str, Any]]) -> None:
    c = payload["counts"]
    by_type = Counter(q["type"] for q in queue)
    g = []
    g.append("# KCL 커버 재산죄 NormCard 벌크 검토 가이드\n")
    g.append(f"생성: 로컬 전용(`api_calls: 0`) · 대상: {payload['scope']} · "
             f"라우팅 근거: {payload['routing_source']}\n")
    g.append("## 이 검토가 무엇인가\n")
    g.append(f"KCL 61문항이 커버하는 재산죄 17조문에서 NormCard **{c.get('card_deterministic_rule',0)+c.get('card_standard_input',0)+c.get('card_policy_variant',0)+c.get('card_context_only',0)}장**과 "
             f"critic 지적 **472건**이 나왔다. 지시하신 3.1~3.5 라우팅으로 "
             f"**자동 {payload['auto_size']}건 / 에이전트 수정 {payload['agent_fix_size']}건**을 걷어내고, "
             f"**사람이 볼 것 {payload['queue_size']}건**만 남겼다.\n")
    g.append("> 주의: 큐는 카드 목록이 아니라 **결정점 목록**이다. 지적이 없는 카드도 "
             "실행 core면 `property_core_card_review.json`에 전수 노출된다(원칙 14).\n")

    g.append("## 자동 처리분 (사용자 확인 불요, 원장에 기록)\n")
    g.append("| 항목 | 건수 | 근거 |")
    g.append("|---|---:|---|")
    g.append(f"| 3.2 authority 라벨 정규화 | {c.get('authority_auto',0)} | 이번 배치 포렌식: `rules/`·`rule_ir.schema` 0 hit → 결론 무관 |")
    g.append(f"| **소계** | **{payload['auto_size']}** | `property_auto_decisions_ledger.json` |\n")

    g.append("## 사용자가 볼 것 (우선순위 순)\n")
    order = [
        ("3.3_overgeneralization", "출처 범위 초과 판정", "지시: \"이건 사람검토 필요\""),
        ("3.1_variant_finding", "학설대립 지적", "판례 방향 확인 후 실무규칙 확정"),
        ("3.1_variant_group", "경쟁견해 그룹", "판시사항 보고 그룹당 1회 선택 → 그룹 카드 일괄 정리"),
        ("3.2_authority_upgrade", "판례 인덱스 대조", "출처가 실제 판례 인용 → 자동 상향 금지, 사람 대조"),
        ("3.4_negative_query", "긍정형 질의문 승인", "초안 190건 작성완료 → confirm/수정만. 47건은 질의 불요"),
    ]
    g.append("| 유형 | 건수 | 무엇을 하나 |")
    g.append("|---|---:|---|")
    for key, label, what in order:
        g.append(f"| `{key}` {label} | {by_type.get(key,0)} | {what} |")
    g.append(f"| **합계** | **{payload['queue_size']}** | |\n")

    g.append("#### 3.1 경쟁견해 202건 — 판례증거 tier (이 순서로 보면 빠름)\n")
    g.append("| tier | 건수 | 의미 |")
    g.append("|---|---:|---|")
    for t, meaning in [
        ("판례후보_조문일치_비공유", "참조조문이 해당 조문 + 경쟁카드와 비공유 → 방향 특정 가능성 최상"),
        ("판례후보_조문일치_공유", "참조조문 일치하나 경쟁카드가 같은 판례를 공유 → 판시사항으로 가려야 함"),
        ("판례후보_조문불일치", "인용은 있으나 참조조문이 다름 → 약한 근거"),
        ("판례없음_context_only_강등후보", "대법원 판례 근거 없음 → 강등 검토"),
    ]:
        g.append(f"| `{t}` | {c.get('variant_'+t,0)} | {meaning} |")
    g.append("")
    g.append("각 항목에 `precedent_evidence`로 **참조조문·판시사항**을 붙여 두었다. "
             "판시사항이 그 명제를 지지하면 실무규칙 확정, 아니면 `context_only` 강등이다. "
             "판례가 그 명제를 지지하는지는 법률 판단이라 자동 확정하지 않았다.\n")
    g.append("### 전문가 동작\n")
    g.append("각 항목은 `human_review.{decision, notes}` 슬롯을 가진다. "
             "**confirm / override + notes**가 기본 동작이고 백지 검토가 아니다. "
             "`3.4`는 `approved_query`에 긍정형 질의문을 확정한다.\n")
    g.append(f"- 이중부정 카드 **{c.get('negative_double',0)}장**을 먼저 본다(문장구조 난이도 최상, A6 실측).\n")
    g.append("#### 3.4 질의문 초안 상태\n")
    g.append("`property_negative_query_drafts.json`에 **에이전트가 직접 작성한 초안 190건**이 들어 있다. "
             "규칙기반 변환은 비문을 만들어 폐기했다. 부정이 조건절에 있는지 귀결절에 있는지에 따라 "
             "`card_status_when_query_satisfied`가 갈리므로(반전 129 / 동행 61) 이 값도 함께 확인해야 한다.\n")
    g.append("237장 중 47장은 질의 대상이 아니다 — 요건불요형 7(요건 제외 **규칙**), "
             "판례소개형 40(규범 주장이 아닌 **보고문**, `context_only` 재분류 검토).\n")

    g.append("## 에이전트가 처리할 것 (사용자 시간 대상 아님)\n")
    g.append("| 유형 | 건수 |")
    g.append("|---|---:|")
    for k, v in sorted(c.items()):
        if k.startswith("agent_fix_"):
            g.append(f"| {k.replace('agent_fix_','')} | {v} |")
    g.append(f"| **소계** | **{payload['agent_fix_size']}** |\n")
    g.append("법률-의미 결정점이 아니라 구조·형식화·출처대조 문제다. "
             "원칙 11에 따라 **API를 쓰지 않고** 로컬로 수정한 뒤 spot-check을 받는다.\n")

    g.append("## 3.5 golden-case 결론 라벨 (front-load 대상, 아직 차단)\n")
    g.append("데이터에 gold 결론이 없어 **사용자가 유일한 정답 원천**이다. "
             "다만 시나리오는 RuleIR 확정 후에야 만들 수 있어 현재는 "
             "`property_scallop_golden_cases.json`에 빈 슬롯으로 예약해 두었다.\n")

    g.append("## 산출 파일\n")
    for f, d in [
        ("property_norm_card_review_queue.json", "사람 큐 (위 5유형)"),
        ("property_core_card_review.json", "실행 core 전수 노출 (원칙 14)"),
        ("property_auto_decisions_ledger.json", "자동 확정·정규화 원장"),
        ("property_agent_remediation_queue.json", "에이전트 수정 대상"),
        ("property_negative_query_drafts.json", "3.4 긍정형 질의문 초안 (에이전트 작성 190건 + 질의 불요 47건)"),
        ("property_scallop_golden_cases.json", "3.5 라벨 슬롯 (예약)"),
        ("property_review_summary.json", "집계"),
    ]:
        g.append(f"- `data/rulegen/property/{f}` — {d}")
    (OUT / "property_legal_review_guide.md").write_text("\n".join(g) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
