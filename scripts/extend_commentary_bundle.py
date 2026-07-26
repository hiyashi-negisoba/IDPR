"""누락 조문 주석서를 원천 파싱본에서 보강한다 — 강도 기본조문 등 (API 0회).

`robbery` 단위에 강도 기본 구성요건이 없다는 것을 RuleIR 단위 설계에서 확인했고, 원인을
"주석서 코퍼스 부재"로 적었는데 **틀렸다**. 원천 파싱본
(`sp_qwen/data/serve/commentary_chunks/docs.parquet`, 형법 4,011 chunks / 251 조문)에는 제333조
[강도] 51 chunks가 절 구조까지 온전히 들어 있다. 원본 PDF도 있다
(`sp/commentary_criminal.zip → casenote_pdfs/044_제333조 [강도].pdf`).

IDPR 번들(`kcl_criminal_v1_commentary_chunks.jsonl`, 3,108 chunks / 96 조문)은 KCL 61문항이 지목한
조문만 골라 담은 부분집합이고, 강도 기본조문은 그 태그 매핑에서 빠져 있었다. 즉 자산이 없던 게
아니라 **선별에서 누락**된 것이다.

보강 대상은 기존 카드가 이미 참조하는 조문으로 한정한다.
  · 제333조 [강도] 51 — robbery 단위의 기본 구성요건(Ⅱ.3 피해자의 반항억압 6 chunks가 핵심)
  · 제332조 [상습범] 15 — `art329_sec8_3` 상습절도 카드가 전제한다
  · 제330조 [야간주거침입절도] 5 — `art328_sec4_1` 야간주거침입절도 카드가 전제한다

친족 준용 조문(제344·354·361·365조)은 넣지 않는다. 친족상도례는 성립이 아니라 처벌·소추 층이고
사용자 결정(2026-07-25)에 따라 절차 레이어(A4)에서 그 층으로 다룬다.

산출은 별도 보강 번들이다. 정본 번들을 덮어쓰지 않으므로 기존 캠페인 산출물의 재현성이 유지된다.
요청 JSONL까지 만들어 두고 **실제 추출·다운스트림은 sbatch + 예산 승인 후** 실행한다.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.build_rulegen_requests import (  # noqa: E402
    build_request,
    make_batches,
)

SOURCE_PARQUET = Path(
    "/home/jaehoonjeong/data/sp_qwen/data/serve/commentary_chunks/docs.parquet")
SOURCE_PDF_ROOT = Path(
    "/home/jaehoonjeong/data/sp_qwen/data/raw/commentary_casenote/형법각칙/articles")
BUNDLE = ROOT / "data/commentary/kcl_criminal_v1_commentary_chunks.jsonl"
SUPPLEMENT = ROOT / "data/commentary/kcl_criminal_v1_commentary_supplement.jsonl"
CAMPAIGN = ROOT / "data/rulegen/campaign"
MANIFEST = CAMPAIGN / "kcl_supplement_manifest.json"

LAW_ID = "001692"  # 형법 (001671은 형사소송법)
# article_no → (조문명, issue_tag, 보강 근거)
TARGETS: dict[str, tuple[str, str, str]] = {
    "제333조": ("강도", "art333",
              "robbery 단위의 기본 구성요건. 지금은 특수강도·준강도·강도상해만 있어 "
              "'폭행·협박으로 반항을 억압하고 재물을 강취한다'가 규칙으로 존재하지 않는다."),
    "제332조": ("상습범", "art332",
              "art329_sec8_3 상습절도-주거침입 경합 카드가 상습절도 구성을 전제한다."),
    "제330조": ("야간주거침입절도", "art330",
              "art328_sec4_1 친족상도례 카드와 art329_sec8_3이 야간주거침입절도를 전제한다."),
}

# 실측 단가 (재산죄 17조문 벌크, `rulegen_sweep_cost_estimate.md` §9)
USD_EXTRACT_PER_CHUNK = 0.0142
USD_DOWNSTREAM_PER_CHUNK = 0.0367


def existing_comment_ids() -> set[str]:
    return {json.loads(line)["comment_id"]
            for line in BUNDLE.read_text(encoding="utf-8").splitlines() if line.strip()}


def main() -> None:
    frame = pd.read_parquet(SOURCE_PARQUET)
    frame = frame[frame.law_id == LAW_ID]
    known = existing_comment_ids()

    rows: list[dict[str, Any]] = []
    summary: list[dict[str, Any]] = []
    for article_no, (title, issue_tag, rationale) in TARGETS.items():
        subset = frame[frame.article_no == article_no].sort_values("comment_id")
        if subset.empty:
            raise SystemExit(f"{article_no} 파싱본이 원천에 없다 — 원본 PDF 파싱이 선행돼야 한다")
        collisions = sorted(set(subset.comment_id) & known)
        if collisions:
            raise SystemExit(f"{article_no} comment_id가 정본 번들과 충돌한다: {collisions[:3]}")

        pdf = next(SOURCE_PDF_ROOT.glob(f"제0{article_no[1:-1]}조_*.pdf"), None)
        chunks = [{
            "article_no": article_no,
            "cited_cases": list(row.cited_cases) if row.cited_cases is not None else [],
            "comment_id": row.comment_id,
            "document_text": row.document_text,
            "law_id": LAW_ID,
            "n_chars": int(row.n_chars),
            "section_path": row.section_path,
            "section_title": row.section_title,
            "source_kind": "parsed_parquet",
            "source_path": str(SOURCE_PARQUET.parent),
            "used_by_tags": [],
        } for row in subset.itertuples()]
        rows.extend(chunks)

        batches = make_batches(chunks)
        requests = [build_request(
            batch, index, len(batches),
            issue_tag=issue_tag, law_id=LAW_ID, article_no=article_no,
            article_title=title,
            request_id_prefix=f"{issue_tag}.pass1",
        ) for index, batch in enumerate(batches, start=1)]
        out = CAMPAIGN / f"{issue_tag}_rulegen_requests.jsonl"
        out.write_text("".join(json.dumps(request, ensure_ascii=False) + "\n"
                               for request in requests), encoding="utf-8")

        chars = sum(chunk["n_chars"] for chunk in chunks)
        cost = len(chunks) * (USD_EXTRACT_PER_CHUNK + USD_DOWNSTREAM_PER_CHUNK)
        summary.append({
            "article_no": article_no, "article_title": title, "issue_tag": issue_tag,
            "chunks": len(chunks), "batches": len(batches), "n_chars": chars,
            # 오케스트레이터(run_property_campaign.py)가 읽는 키와 같은 이름을 쓴다
            "est_extraction_critic_usd": round(len(chunks) * USD_EXTRACT_PER_CHUNK, 2),
            "est_usd": round(cost, 2), "rationale": rationale,
            "requests_path": str(out.relative_to(ROOT)),
            "source_pdf": pdf.name if pdf else None,
        })
        print(f"  {article_no} {title:14s} {len(chunks):3d} chunks / {len(batches)} 배치 "
              f"/ {chars:6,}자 / ${cost:.2f}")

    SUPPLEMENT.write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
                          encoding="utf-8")
    total_chunks = sum(item["chunks"] for item in summary)
    total_usd = sum(item["est_usd"] for item in summary)
    MANIFEST.write_text(json.dumps({
        "version": "1.0.0", "api_calls": 0,
        "scope": "RuleIR 단위 설계에서 드러난 누락 조문 보강 (강도 기본조문 등)",
        "correction": ("'주석서 코퍼스 부재'라고 적었던 것은 오독이다. 원천 파싱본에 절 구조까지 "
                       "있고 원본 PDF도 있다. IDPR 번들이 KCL 태그 매핑에서 빠뜨린 것이다."),
        "source": {"parquet": str(SOURCE_PARQUET), "pdf_root": str(SOURCE_PDF_ROOT),
                   "archive": "/data5/jaehoonjeong/sp/commentary_criminal.zip"},
        "supplement_bundle": str(SUPPLEMENT.relative_to(ROOT)),
        "excluded": {"제344조·제354조·제361조·제365조":
                     "친족 준용 조문. 친족상도례는 처벌·소추 층이므로 절차 레이어(A4)에서 다룬다.",
                     "제336조·제339조·제340조": "KCL 61문항이 묻지 않는다."},
        "unit_rates_usd_per_chunk": {"extraction": USD_EXTRACT_PER_CHUNK,
                                     "downstream": USD_DOWNSTREAM_PER_CHUNK},
        "totals": {"articles": len(summary), "chunks": total_chunks,
                   "est_usd": round(total_usd, 2)},
        "targets": summary,
        "status": "requests_ready_pending_budget_approval",
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"\n보강 {len(summary)}조문 / {total_chunks} chunks / 추정 **${total_usd:.2f}**")
    print(f"  → {SUPPLEMENT.relative_to(ROOT)}")
    print(f"  → {MANIFEST.relative_to(ROOT)}")
    print("  실행은 sbatch + 예산 승인 후 (`run_property_campaign.py` 경로 재사용)")


if __name__ == "__main__":
    main()
