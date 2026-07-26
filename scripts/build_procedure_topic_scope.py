"""수직 확장 범위 집계 — KCL 커버 재산죄와 사실관계를 공유하는 절차법 쟁점.

1. 커버된 재산죄가 걸린 (회차, 문) 사실관계를 찾는다.
2. 그 사실관계의 절차/mixed 문항이 다루는 **절차법 토픽(issue_tag)** 을 전부 집계·중복제거한다.
3. 토픽 → 형소법 조문 → **per-issue 스코핑된 절(section)** 로 좁혀 chunk를 센다.
   (조문 전량을 세면 5~6배 과대계상된다. 예: 제106조 압수 150ch 중 전자정보·참여권은 43ch.)
4. 실측 단가로 카드 생성~최종(RuleIR)까지 비용을 계상한다.

스코핑은 절 제목 키워드 매칭이라 **법률 검토가 필요한 휴리스틱**이다. 매칭 실패 토픽은
needs_manual_scoping으로 분리해 따로 보고한다(빠뜨리면 규칙이 비고, 넘치면 비용이 는다).

단가(실측): 형소법 $0.0533/chunk (추출+merge+critic, 파일럿 cp342·cp308_2)
            RuleIR ~$0.0048/chunk (사기 단일런 스케일)
API 호출 없음 — 집계 전용.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
INVENTORY = PROJECT_ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl"
TAG_MANIFEST = PROJECT_ROOT / "data/commentary/kcl_criminal_v1_tag_commentary_manifest.jsonl"
CHUNKS = PROJECT_ROOT / "data/commentary/kcl_criminal_v1_commentary_chunks.jsonl"
CAMPAIGN = PROJECT_ROOT / "data/rulegen/campaign/kcl_substantive_campaign_manifest.json"
OUT = PROJECT_ROOT / "data/rulegen/procedure"

RATE_CP = 0.0533      # 형소법 추출+merge+critic (실측)
RATE_RULEIR = 0.0048  # RuleIR gen+critic

PROPERTY = {323, 328, 329, 331, 334, 335, 337, 338, 342, 343, 344,
            350, 355, 356, 357, 360, 366}

# 토픽 → 절 제목 매칭 키워드 (한국어 주석서 절 제목 기준).
# 절 선택은 법률 판단이 섞이므로 사용자 검토 대상이다.
TOPIC_KEYWORDS: dict[str, list[str]] = {
    "digital_evidence_admissibility": ["전자", "디지털", "정보저장", "동일성", "무결성", "증거능력"],
    "forensic_participation_right": ["참여", "전자", "정보저장", "별건"],
    "copy_identity": ["동일성", "무결성", "복제", "이미징", "전자"],
    "unrelated_electronic_evidence": ["무관정보", "관련성", "별건", "전자", "정보저장"],
    "separate_warrant": ["별건", "영장", "관련성", "무관정보"],
    "participation_right": ["참여", "별건", "전자"],
    "electronic_evidence": ["전자", "정보저장", "디지털"],
    "electronic_evidence_admissibility": ["전자", "증거능력", "동일성"],
    "remote_cloud_search_seizure": ["원격", "제3자 보관", "클라우드", "전자"],
    "tablet_imaging": ["이미징", "복제", "전자", "동일성"],
    "warrant_scope": ["영장", "범위", "관련성"],
    "warrant_relevance": ["관련성", "영장"],
    "third_party_voluntary_submission": ["임의제출", "참여", "전자"],
    "illegal_evidence": ["위법수집", "배제", "증거능력"],
    "post_warrant_cure": ["사후", "영장", "하자", "치유"],
    "hearsay_exception": ["전문", "예외", "증거능력"],
    "hearsay_statement": ["전문", "진술"],
    "multiple_hearsay": ["재전문", "전문"],
    "hearsay_vs_original_evidence": ["전문", "원본", "본래증거"],
    "police_statement_record": ["조서", "진술조서", "사법경찰"],
    "police_interrogation_record": ["피의자신문조서", "조서", "내용부인"],
    "investigator_testimony": ["조사자", "증언", "전문"],
    "impeachment_evidence": ["탄핵", "증명력"],
    "witness_testimony_admissibility": ["증인", "증언", "신문"],
    "co_defendant_statement": ["공범", "공동피고인", "진술"],
    "video_recording_authenticity": ["영상녹화", "성립의 진정", "진정"],
    "witness_statement_record": ["진술조서", "조서", "진정"],
    "secret_recording": ["녹음", "통신비밀", "대화"],
    "inspection_report_photo": ["검증조서", "사진", "검증"],
    "reenactment_photo": ["재연", "사진", "검증"],
    "expert_report_admissibility": ["감정", "감정서", "증거능력"],
    "emergency_arrest": ["긴급체포", "체포"],
    "emergency_arrest_search_seizure": ["긴급체포", "체포", "압수"],
    "arrest_scene_search": ["체포현장", "압수", "영장주의 예외"],
    "arrest_method": ["체포", "방법", "고지"],
    "search_warrant": ["영장", "압수", "수색"],
    "statute_of_limitations": ["공소시효", "시효", "기간"],
    "co_offender_suspension": ["공범", "정지", "시효"],
    "counterpart_offense": ["대향범", "공범"],
    "prohibition_disadvantageous_change": ["불이익변경", "형의 경중"],
    "appellate_sentencing": ["양형", "항소심", "선고"],
    "partial_appeal": ["일부상소", "상소", "범위"],
    "appellate_scope": ["심판 범위", "항소", "범위"],
    "remand_scope": ["환송", "심판", "범위"],
    "remand_sentencing": ["환송", "양형", "불이익변경"],
    "appellate_disposition": ["항소", "파기", "자판"],
    "appellate_fact_finding": ["사실오인", "항소심", "심리"],
    "trial_centered_principle": ["공판중심", "직접심리"],
    "direct_examination_principle": ["직접심리", "공판중심"],
    "appeal_interest": ["상소이익", "상소"],
    "ordinary_appeal": ["항고", "보통항고"],
    "execution_stay": ["집행정지", "집행"],
    "bail_revocation": ["보석", "취소"],
    "retrial": ["재심", "재심이유"],
    "conflicting_co_offender_judgment": ["재심", "공범", "모순"],
    "new_evidence": ["증거", "명백", "재심"],
    "dismissal_judgment": ["공소기각", "판결"],
    "formal_judgment": ["형식재판", "공소기각", "면소"],
    "offense_subject_to_complaint": ["친고죄", "고소"],
    "complaint_withdrawal": ["고소취소", "취소"],
    "complaint_before_investigation": ["고소", "고소권자", "수사"],
    "complaint_cure_after_indictment": ["고소", "추완", "공소제기"],
    "amendment_of_indictment": ["공소장변경", "변경"],
    "identity_of_facts": ["공소사실 동일성", "동일성"],
    "evidence_discovery": ["증거개시", "열람", "등사"],
    "discovery_noncompliance": ["증거개시", "불이행"],
    "prosecutor_appeal": ["검사", "상소"],
    "defense_counsel_appointment": ["변호인", "선임"],
    "appeal_reason_statement": ["항소이유서", "기간"],
    "procedural_cure": ["추완", "하자", "치유"],
    "concurrent_crimes": ["경합범", "죄수"],
    "imaginative_concurrence": ["상상적 경합", "경합"],
}


def load_jsonl(p: Path) -> list[dict[str, Any]]:
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def main() -> None:
    rows = load_jsonl(INVENTORY)
    tagman = {r["tag"]: r for r in load_jsonl(TAG_MANIFEST)}
    campaign = json.loads(CAMPAIGN.read_text(encoding="utf-8"))

    # 형소법 절 인덱스: article_no -> [(section_path, title, n)]
    sections: dict[str, list[tuple[str, str]]] = defaultdict(list)
    for r in load_jsonl(CHUNKS):
        if r["law_id"] == "001671":
            sections[r["article_no"]].append((r["section_path"], r.get("section_title", "") or ""))

    # 1) 커버 재산죄가 걸린 사실관계
    covered_tags: set[str] = set()
    for t in campaign["targets"]:
        n = int(re.sub(r"[^0-9]", "", t["article_no"]) or 0)
        if n in PROPERTY:
            covered_tags.update(t["used_by_tags"])
    key = lambda r: (r["exam_round"], r["paper"])  # noqa: E731
    sub = [r for r in rows if r["legal_area"] == "substantive" and covered_tags & set(r["issue_tags"] or [])]
    groups = sorted({key(r) for r in sub})
    proc_q = [r for r in rows if r["legal_area"] != "substantive" and key(r) in groups]

    # 2) 절차 토픽 집계 (중복제거)
    topic_qs: dict[str, list[str]] = defaultdict(list)
    for r in proc_q:
        for t in r["issue_tags"] or []:
            topic_qs[t].append(r["sub_question_id"])
    topics = sorted(topic_qs)

    # 3) 토픽 → 조문 → per-issue 스코핑 절
    scoped_sections: dict[str, set[str]] = defaultdict(set)  # article -> section_paths
    topic_rows: list[dict[str, Any]] = []
    unavailable, needs_manual = [], []
    for t in topics:
        e = tagman.get(t)
        if not e:
            needs_manual.append({"topic": t, "reason": "tag manifest에 없음"})
            continue
        if not e.get("targets"):
            unavailable.append({"topic": t, "reason": e.get("unavailable_reason", "")[:80]})
            continue
        kws = TOPIC_KEYWORDS.get(t)
        arts, ch_full, ch_scoped, matched_any = [], 0, 0, False
        for tg in e["targets"]:
            if tg["law_id"] != "001671":
                continue
            art = tg["article_no"]
            ss = sections.get(art, [])
            ch_full += len(ss)
            if len(ss) <= 10:            # 소형 조문은 전량(스코핑 무의미)
                pick = {s[0] for s in ss}
            elif kws:
                pick = {s[0] for s in ss if any(k in s[1] for k in kws)}
                if pick:
                    matched_any = True
            else:
                pick = set()
            arts.append({"article_no": art, "full": len(ss), "scoped": len(pick)})
            scoped_sections[art] |= pick
            ch_scoped += len(pick)
        if kws is None:
            needs_manual.append({"topic": t, "reason": "키워드 사전 미정의"})
        elif ch_full > 0 and ch_scoped == 0:
            needs_manual.append({"topic": t, "reason": "키워드가 어떤 절도 매칭 못함"})
        topic_rows.append({
            "topic": t, "questions": sorted(set(topic_qs[t])),
            "articles": arts, "chunks_full": ch_full, "chunks_scoped": ch_scoped,
            "keyword_matched": matched_any,
        })

    # 4) 중복제거된 절 기준 총량·비용
    uniq_ch = sum(len(v) for v in scoped_sections.values())
    full_ch = sum(len(sections[a]) for a in scoped_sections)
    cards = uniq_ch * RATE_CP
    ruleir = uniq_ch * RATE_RULEIR
    report = {
        "version": "1.0.0", "api_calls": 0,
        "fact_patterns": [f"r{g[0]}{g[1]}" for g in groups],
        "procedural_questions": len(proc_q),
        "unique_topics": len(topics),
        "topics_costed": len(topic_rows),
        "articles_touched": len(scoped_sections),
        "chunks_whole_article": full_ch,
        "chunks_per_issue_scoped": uniq_ch,
        "scoping_ratio": round(uniq_ch / full_ch, 3) if full_ch else None,
        "cost_cards_usd": round(cards, 1),
        "cost_ruleir_usd": round(ruleir, 1),
        "cost_total_usd": round(cards + ruleir, 1),
        "rates": {"cards_per_chunk": RATE_CP, "ruleir_per_chunk": RATE_RULEIR,
                  "source": "형소법 파일럿 cp342·cp308_2 실측"},
        "needs_manual_scoping": needs_manual,
        "unavailable": unavailable,
        "topics": sorted(topic_rows, key=lambda r: -r["chunks_scoped"]),
        "per_article_scoped": {a: sorted(v) for a, v in sorted(scoped_sections.items())},
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "procedure_topic_scope.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"사실관계 {len(groups)}개 / 절차·mixed 문항 {len(proc_q)}개")
    print(f"유니크 절차 토픽 {len(topics)}개 (비용계상 {len(topic_rows)})")
    print(f"조문 {len(scoped_sections)}개: 전량 {full_ch}ch → per-issue {uniq_ch}ch ({uniq_ch/full_ch*100:.0f}%)")
    print(f"비용: 카드생성 ${cards:.1f} + RuleIR ${ruleir:.1f} = ${cards+ruleir:.1f}")
    print(f"스코핑 수동확인 필요 {len(needs_manual)} / unavailable {len(unavailable)}")
    print(f"→ {(OUT/'procedure_topic_scope.json').relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()
