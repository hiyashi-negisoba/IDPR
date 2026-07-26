"""재산죄 검토완료 core를 스키마 유효한 NormCardSet으로 조립한다 (RuleIR 입력 형식).

확정 core 원장(`property_core_set_final_v10.json`)은 감사 원장이라 카드 원본 필드(source_refs·candidate_refs·
authority_basis 등)가 없다. RuleIR 생성기는 `idpr/NormCardSet` 계약을 요구하므로, 그 판정을
캠페인 merge 산출 카드(`.cache/llm/runs/rulegen_downstream/<art>/<art>/norm_cards/*.json`)에
되돌려 적용해 조문별 검토완료 카드셋을 만든다.

확정 판정 → 카드 필드 반영 규칙:
  · final_role                → formalization (학설선택 승격분이 standard_input으로)
  · proposition               → 확정 문장(학설 어법 제거·재작성 반영)
  · review_required: true→false — merge 단계의 "사람이 봐야 한다" 플래그다. 결정 A/A2/B/C/C2로
    그 검토가 실제로 끝났으므로 내린다. 검증기는 legal_review=complete인 카드셋에
    review_required=true를 허용하지 않는다.
  · doctrinal_status: disputed → 확정. 견해 대립이 남아 있다는 표시인데 사용자가 결정C에서
    한쪽을 실무규칙으로 선택했으므로 더는 disputed가 아니다. authority_basis가 판례인 카드는
    precedent_position, 그 외는 settled로 확정하고 카드별로 원장에 남긴다.

모듈 카드셋의 `legal_review_questions`는 비운다(계약상 complete는 빈 목록을 요구). 그 질문들이
결정 문서의 출발점이었고, 답이 카드 판정에 이미 반영됐다. 추적을 위해 원장에 모듈별로 보존한다.

인용 문언은 조립 과정에서 축자성을 복원한다(`repair_quotes` — OCR 공백 복원 + 압축 인용을
연결 후보의 축자 인용으로 교체). 산출물은 조문별로 RuleIR 생성기가 거는 계약 검증을 통과해야
하고, 별도로 merge 단계 계약(후보 대조)까지 건 엄격검증 지적을 원장에 남긴다. API 0회.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.rulegen import (  # noqa: E402
    NormCardValidationError,
    validate_norm_card_set,
)

PROP = ROOT / "data/rulegen/property"
CAMPAIGN = ROOT / "data/rulegen/campaign"
MERGE_ROOT = ROOT / ".cache/llm/runs/rulegen_downstream"
EXTRACT_ROOT = ROOT / ".cache/llm/runs/campaign_prop"
# 최신 확정본을 가리킨다 (v7 → 결정B2 v8 → 보강 3조문 v9 → 결정B3 v10).
CORE_SET = PROP / "property_core_set_final_v10.json"
OUT_DIR = PROP / "core_norm_card_sets"
LEDGER = PROP / "core_norm_card_set_ledger.json"

CORE_ROLES = ("standard_input", "deterministic_rule")
REPAIR_REASON = {
    "ocr_whitespace": "OCR 낱말분리 공백 복원 — 문언 동일",
    "aligned_span": "압축 인용을 정렬 구간의 원문 문언으로 복원",
    "candidate_verbatim": "압축 인용을 연결 후보의 축자 인용으로 교체",
    "aligned_span_loose": "압축 인용을 정렬 구간의 원문 문언으로 복원(느슨한 임계)",
}
HITL_NOTE = (
    "재산죄 벌크 HITL 완료(2026-07-23~25): core scope 감사 2패스 + 카드결함 감사 + "
    "결정 A/A2(출처범위)·B(부정형 질의문)·C/C2(학설선택) 반영. 근거는 "
    "data/rulegen/property/ 결정 원장."
)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def merged_modules(article: str) -> dict[str, dict[str, Any]]:
    """모듈 슬러그 → merge 산출 카드셋."""

    module_dir = MERGE_ROOT / article / article / "norm_cards"
    return {path.stem: read_json(path) for path in sorted(module_dir.glob("*.json"))}


def extraction_candidates(article: str) -> dict[tuple[str, str], dict[str, Any]]:
    """(request_id, candidate_id) → 검증된 후보."""

    out: dict[tuple[str, str], dict[str, Any]] = {}
    for path in sorted((EXTRACT_ROOT / article / "terra").glob("*.json")):
        batch = read_json(path)
        for candidate in batch.get("candidates", []):
            out[(batch["request_id"], candidate["candidate_id"])] = candidate
    return out


def commentary_index(article: str) -> tuple[dict[str, Any], dict[str, set[str]]]:
    requests = load_jsonl(CAMPAIGN / f"{article}_rulegen_requests.jsonl")
    commentary_by_id = {
        chunk["comment_id"]: chunk
        for request in requests
        for chunk in request.get("commentary_chunks", [])
    }
    request_comment_ids = {
        request["request_id"]: {
            chunk["comment_id"] for chunk in request.get("commentary_chunks", [])
        }
        for request in requests
    }
    return commentary_by_id, request_comment_ids


def repair_quotes(card: dict[str, Any], commentary_by_id: dict[str, Any],
                  candidates: dict[tuple[str, str], dict[str, Any]],
                  ledger: list[dict[str, Any]], stats: Counter) -> dict[str, Any]:
    """비축자 인용을 원문 문언으로 되돌린다 (계약: quote는 commentary의 정확한 부분문자열).

    merge 단계에서 두 가지가 생겼다. ① 주석서 OCR이 낱말 중간에 넣은 공백을 모델이 정리한 것
    (`결 정되어야` → `결정되어야`), ② 긴 문장을 압축한 것. ①은 원문에서 공백무시 매칭으로 그
    구간을 찾아 되돌린다. ②는 그 카드가 연결한 **후보의 인용**(추출 단계에서 축자성 검증을
    통과한 문언) 중 같은 comment_id에서 가장 가까운 것으로 바꾼다.
    """

    refs, changed = [], False
    for ref in card["source_refs"]:
        text = commentary_by_id.get(ref["comment_id"], {}).get("document_text", "")
        if ref["quote"] in text:
            refs.append(ref)
            continue

        fixed, kind = whitespace_span(ref["quote"], text), "ocr_whitespace"
        if fixed is None:
            fixed, kind = aligned_span(ref["quote"], text, 0.75), "aligned_span"
        if fixed is None:
            fixed = nearest_candidate_quote(card, ref, candidates, commentary_by_id)
            kind = "candidate_verbatim"
        if fixed is None:
            fixed, kind = aligned_span(ref["quote"], text, 0.5), "aligned_span_loose"
        if fixed is None:
            refs.append(ref)
            stats["quote_unrepaired"] += 1
            continue

        ledger.append({"card_id": card["id"], "change": f"quote_{kind}",
                       "comment_id": ref["comment_id"],
                       "from": ref["quote"], "to": fixed,
                       "reason": REPAIR_REASON[kind]})
        refs.append({**ref, "quote": fixed})
        stats[f"quote_repaired_{kind}"] += 1
        changed = True

    if changed:
        seen, unique = set(), []
        for ref in refs:
            key = (ref["comment_id"], ref["section_path"], ref["quote"])
            if key not in seen:
                seen.add(key)
                unique.append(ref)
        refs = unique
    card["source_refs"] = refs
    return card


def aligned_span(quote: str, text: str, min_coverage: float,
                 min_block: int = 4) -> str | None:
    """인용과 정렬되는 원문 구간을 축자로 잘라낸다.

    모델이 문장 중간을 덜어낸 압축 인용은 공백 복원으로 안 잡힌다. 공백을 제거한 좌표에서
    일치 블록을 구해 첫 블록부터 마지막 블록까지를 원문에서 그대로 떠 온다. 덜어낸 부분이
    되살아나므로 인용은 길어지지만 축자성이 회복된다. `min_coverage`(인용 대비 일치 문자
    비율) 미달이면 포기한다 — 다른 대목을 잘못 집는 것보다 낫다.
    """

    offsets = [index for index, char in enumerate(text) if not char.isspace()]
    dense = "".join(text[index] for index in offsets)
    target = re.sub(r"\s+", "", quote)
    if not target or not dense:
        return None
    blocks = [block for block
              in SequenceMatcher(None, dense, target, autojunk=False).get_matching_blocks()
              if block.size >= min_block]
    if not blocks or sum(block.size for block in blocks) / len(target) < min_coverage:
        return None
    start = offsets[blocks[0].a]
    end = offsets[blocks[-1].a + blocks[-1].size - 1] + 1
    # 낱말 중간에서 끊기지 않게 앞은 어절 경계로, 뒤는 문장 끝으로 맞춘다.
    while start > 0 and not text[start - 1].isspace():
        start -= 1
    tail = text.find("다.", end - 1)
    if 0 <= tail <= end + 60:
        end = tail + 2
    else:
        while end < len(text) and not text[end].isspace():
            end += 1
    span = text[start:end].strip()
    return span if len(span) <= 300 else None


def whitespace_span(quote: str, text: str) -> str | None:
    """공백을 무시하면 일치하는 원문 구간을 그대로 돌려준다."""

    stripped = re.sub(r"\s+", "", quote)
    if not stripped:
        return None
    offsets = [i for i, ch in enumerate(text) if not ch.isspace()]
    dense = "".join(text[i] for i in offsets)
    start = dense.find(stripped)
    if start < 0:
        return None
    return text[offsets[start]: offsets[start + len(stripped) - 1] + 1]


def nearest_candidate_quote(card: dict[str, Any], ref: dict[str, Any],
                            candidates: dict[tuple[str, str], dict[str, Any]],
                            commentary_by_id: dict[str, Any]) -> str | None:
    """같은 commentary chunk를 인용한 연결 후보의 축자 인용 중 가장 가까운 것."""

    text = commentary_by_id.get(ref["comment_id"], {}).get("document_text", "")
    pool = []
    for candidate_ref in card["candidate_refs"]:
        candidate = candidates.get(
            (candidate_ref["request_id"], candidate_ref["candidate_id"]))
        if candidate is None:
            continue
        for source in candidate["source_refs"]:
            if source["comment_id"] != ref["comment_id"] or source["quote"] not in text:
                continue
            score = SequenceMatcher(
                None, re.sub(r"\s+", "", ref["quote"]), re.sub(r"\s+", "", source["quote"])
            ).ratio()
            pool.append((score, source["quote"]))
    if not pool:
        return None
    return max(pool)[1]


def resolve_doctrinal_status(card: dict[str, Any]) -> str:
    """disputed를 확정 상태로 — 판례 근거면 판례입장, 그 외는 확립."""

    if card["authority_basis"] == "commentary_reported_precedent":
        return "precedent_position"
    return "settled"


def build_card(row: dict[str, Any], card: dict[str, Any],
               ledger: list[dict[str, Any]], stats: Counter,
               merged: dict[str, dict[str, Any]] | None = None) -> dict[str, Any]:
    out = dict(card)
    merged = merged or {}
    notes = [out["review_notes"].rstrip()]

    if out["proposition"] != row["proposition"]:
        ledger.append({"card_id": row["card_id"], "change": "proposition",
                       "from": out["proposition"], "to": row["proposition"],
                       "reason": row.get("rewrite_reason", "결정 반영")})
        out["proposition"] = row["proposition"]
        stats["proposition_rewritten"] += 1

    if out["formalization"] != row["final_role"]:
        ledger.append({"card_id": row["card_id"], "change": "formalization",
                       "from": out["formalization"], "to": row["final_role"],
                       "reason": (f"결정C 학설선택 승격 — {row.get('doctrine_selected')}"
                                  if row.get("promoted_from_variant") else "core 판정")})
        out["formalization"] = row["final_role"]
        stats["formalization_changed"] += 1

    if out["doctrinal_status"] == "disputed":
        resolved = resolve_doctrinal_status(out)
        ledger.append({"card_id": row["card_id"], "change": "doctrinal_status",
                       "from": "disputed", "to": resolved,
                       "reason": ("사용자가 이 견해를 실무규칙으로 선택했으므로 견해 대립 상태가 "
                                  "아니다" if row.get("promoted_from_variant") else
                                  "경쟁 변이 카드가 core에 없어 대립이 남지 않는다")})
        out["doctrinal_status"] = resolved
        stats[f"doctrinal_status_to_{resolved}"] += 1
        notes.append(f"결정C 반영으로 doctrinal_status를 {resolved}로 확정했다.")

    if out["review_required"]:
        out["review_required"] = False
        stats["review_required_cleared"] += 1

    for absorbed_id in row.get("absorb_source_refs_from", []):
        absorbed = merged.get(absorbed_id)
        if absorbed is None:
            raise SystemExit(f"{row['card_id']}가 흡수할 카드 {absorbed_id}를 찾지 못했다")
        seen = {(ref["comment_id"], ref["section_path"], ref["quote"])
                for ref in out["source_refs"]}
        out["source_refs"] = out["source_refs"] + [
            ref for ref in absorbed["source_refs"]
            if (ref["comment_id"], ref["section_path"], ref["quote"]) not in seen]
        keys = {(ref["request_id"], ref["candidate_id"]) for ref in out["candidate_refs"]}
        out["candidate_refs"] = out["candidate_refs"] + [
            ref for ref in absorbed["candidate_refs"]
            if (ref["request_id"], ref["candidate_id"]) not in keys]
        out["request_ids"] = sorted(set(out["request_ids"]) | set(absorbed["request_ids"]))
        notes.append(f"근사중복 병합으로 {absorbed_id}의 인용을 함께 근거로 삼는다.")
        stats["absorbed_source_refs"] += 1

    if row.get("promoted_from_variant"):
        comment = (row.get("doctrine_selected") or {}).get("user_comment")
        notes.append("결정C에서 사용자가 선택한 견해다."
                     + (f" 사용자 코멘트: {comment}" if comment else ""))

    notes.append(HITL_NOTE)
    out["review_notes"] = " ".join(notes)
    return out


def main() -> None:
    v7 = read_json(CORE_SET)
    rows_by_article: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in v7["rows"]:
        if row["final_role"] in CORE_ROLES:
            rows_by_article[row["article"]].append(row)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ledger: list[dict[str, Any]] = []
    stats: Counter = Counter()
    carried_questions: dict[str, dict[str, list[str]]] = {}
    strict_findings: dict[str, list[str]] = {}
    index: list[dict[str, Any]] = []
    failures: list[str] = []

    for article in sorted(rows_by_article):
        rows = rows_by_article[article]
        modules = merged_modules(article)
        by_id = {card["id"]: (slug, card)
                 for slug, payload in modules.items() for card in payload["cards"]}

        commentary_by_id, request_comment_ids = commentary_index(article)
        candidates = extraction_candidates(article)

        cards, gaps, questions, used_modules = [], [], {}, set()
        for row in sorted(rows, key=lambda r: r["card_id"]):
            slug, card = by_id[row["card_id"]]
            used_modules.add(slug)
            built = build_card(row, card, ledger, stats,
                               {cid: payload for cid, (_, payload) in by_id.items()})
            cards.append(repair_quotes(built, commentary_by_id, candidates, ledger, stats))
        for slug in sorted(used_modules):
            payload = modules[slug]
            gaps.extend(payload.get("coverage_gaps", []))
            if payload.get("legal_review_questions"):
                questions[slug] = payload["legal_review_questions"]
        carried_questions[article] = questions

        comment_ids = sorted({ref["comment_id"] for card in cards
                              for ref in card["source_refs"]})
        card_set = {
            "version": "1.1.0",
            "card_set_id": f"kr.property.{article}.core.norms.v1",
            "issue_tag": article,
            "status": "draft",
            "legal_review": "complete",
            "construction": "reviewed_aggregate",
            "source_scope": {
                "target_paths": sorted({f"commentary://001692/{article}#{slug}"
                                        for slug in used_modules}),
                "comment_ids": comment_ids,
            },
            "cards": cards,
            "legal_review_questions": [],
            "coverage_gaps": sorted(dict.fromkeys(gaps)),
        }

        # 계약 검증 — RuleIR 생성기가 실제로 거는 게이트와 동일하게 commentary만 대조한다
        # (`validate_full_rule_ir_generation`이 core set을 이 형태로 검증한다).
        try:
            validate_norm_card_set(card_set, commentary_by_id)
            verdict = "valid"
        except NormCardValidationError as exc:
            verdict = "invalid"
            failures.append(f"{article}: {exc}")

        # 엄격 검증 — merge 단계 계약(후보 전수 커버·후보 대조)까지 걸어 품질 결함을 뽑는다.
        # core는 정의상 후보 일부만 승격하므로 "omits N validated candidates"는 결함이 아니다.
        try:
            validate_norm_card_set(
                card_set,
                commentary_by_id,
                request_comment_ids=request_comment_ids,
                allowed_candidates=candidates,
            )
            strict = []
        except NormCardValidationError as exc:
            strict = [line for line in str(exc).splitlines()
                      if line.startswith("- ") and "validated candidates" not in line]
        strict_findings[article] = strict

        (OUT_DIR / f"{article}.json").write_text(
            json.dumps(card_set, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        index.append({"article": article, "cards": len(cards),
                      "modules": len(used_modules), "coverage_gaps": len(gaps),
                      "validation": verdict, "strict_findings": len(strict)})
        print(f"  {article:8s} {len(cards):4d}장 / 모듈 {len(used_modules):2d} / "
              f"{verdict} / 엄격검증 지적 {len(strict)}")

    LEDGER.write_text(json.dumps({
        "version": "1.0.0", "api_calls": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source": {"core_set": CORE_SET.name, "merge_runs": str(MERGE_ROOT.relative_to(ROOT))},
        "method": "v7 판정을 merge 카드에 반영 → 조문별 reviewed_aggregate 카드셋",
        "stats": dict(stats),
        "index": index,
        "carried_legal_review_questions": carried_questions,
        "strict_findings": {k: v for k, v in strict_findings.items() if v},
        "entries": ledger,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    total = sum(item["cards"] for item in index)
    print(f"\n조문 {len(index)}개 / core {total}장 → {OUT_DIR.relative_to(ROOT)}")
    for key, value in sorted(stats.items()):
        print(f"  {key}: {value}")
    if failures:
        print("\n검증 실패:")
        for line in failures:
            print(f"  {line}")
        raise SystemExit(1)
    print("  전 조문 NormCardSet 계약 통과")


if __name__ == "__main__":
    main()
