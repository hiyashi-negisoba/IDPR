"""KCL 실체법 커버 rulegen 캠페인 준비 (API 아님, 결정론).

`docs/research/rulegen_sweep_cost_estimate.md`의 실체 P1(재산범)+P2(OOS 비재산) 대상
형법각칙(law_id 001692) 조문 전부에 대해 rulegen requests JSONL을 배치 생성하고,
캠페인 매니페스트(대상·chunk·배치·파일럿 보정 비용)를 쓴다. terra/sol는 호출하지 않는다.

issue_tag는 조문번호 slug(art347 등)로 통일한다 — 실제 죄명은 `target.article_title`과
commentary로 terra에 전달되므로 slug는 라벨/추적용이다. 배칭 로직은
`build_rulegen_requests`를 재사용한다(중복 금지).

사기(CC_347)와 장물(CC_362, 파일럿 완료)은 기본 제외한다(--include-done로 포함).
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "scripts"))

from build_rulegen_requests import build_request, load_jsonl, make_batches  # noqa: E402

POOL = PROJECT_ROOT / "data/commentary/kcl_criminal_v1_commentary_pool.json"
INVENTORY = PROJECT_ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl"
COMMENTARY = PROJECT_ROOT / "data/commentary/kcl_criminal_v1_commentary_chunks.jsonl"
OUT_DIR = PROJECT_ROOT / "data/rulegen/campaign"
SUBSTANTIVE_LAW = "001692"  # 형법각칙
DONE_TARGETS = {"CC_347", "CC_362"}  # fraud(exemplar) + 장물(pilot)

# 파일럿(장물) 실측 보정: 추출+후보비평 스테이지 비용.
TERRA_COST_PER_BATCH = 0.094  # $ (gpt-5.6-terra, reasoning_effort=low)
SOL_CRITIC_COST_PER_BATCH = 0.125  # $ (gpt-5.6-sol, low)


def article_slug(article_no: str) -> str:
    digits = re.sub(r"[^0-9]", "", article_no)
    suffix = "_2" if "의2" in article_no else ""
    return f"art{digits}{suffix}"


def select_targets() -> list[dict[str, Any]]:
    pool = json.loads(POOL.read_text(encoding="utf-8"))
    targets = {t["target_id"]: t for t in pool["targets"]}
    tag2t: dict[str, set[str]] = collections.defaultdict(set)
    for t in pool["targets"]:
        for tag in t.get("used_by_tags", []):
            tag2t[tag].add(t["target_id"])
    inv = load_jsonl(INVENTORY)

    selected: dict[str, dict[str, Any]] = {}
    for q in inv:
        cov = q.get("coverage_candidate")
        area = q.get("legal_area")
        if cov == "property_crime_candidate" or (
            cov == "out_of_current_rule_scope" and area == "substantive"
        ):
            for tag in q.get("issue_tags", []):
                for tid in tag2t.get(tag, ()):
                    spec = targets[tid]
                    if spec["law_id"] == SUBSTANTIVE_LAW:
                        selected[tid] = spec
    return [selected[tid] for tid in sorted(selected)]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--include-done", action="store_true",
                        help="사기·장물도 포함(기본 제외).")
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR)
    args = parser.parse_args()

    all_chunks = load_jsonl(COMMENTARY)
    by_article: dict[tuple[str, str], list[dict[str, Any]]] = collections.defaultdict(list)
    for row in all_chunks:
        by_article[(row["law_id"], row["article_no"])].append(row)

    targets = select_targets()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    manifest_targets = []
    total_batches = total_chunks = 0
    for spec in targets:
        tid = spec["target_id"]
        if tid in DONE_TARGETS and not args.include_done:
            continue
        chunks = by_article.get((spec["law_id"], spec["article_no"]), [])
        if not chunks:
            continue
        slug = article_slug(spec["article_no"])
        batches = make_batches(chunks)
        requests = [
            build_request(
                batch, i, len(batches),
                issue_tag=slug,
                law_id=spec["law_id"],
                article_no=spec["article_no"],
                article_title=spec.get("article_title") or "",
                request_id_prefix=f"{slug}.pass1",
            )
            for i, batch in enumerate(batches, start=1)
        ]
        out_path = args.out_dir / f"{slug}_rulegen_requests.jsonl"
        out_path.write_text(
            "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in requests),
            encoding="utf-8",
        )
        total_batches += len(batches)
        total_chunks += len(chunks)
        manifest_targets.append({
            "target_id": tid,
            "issue_tag": slug,
            "article_no": spec["article_no"],
            "article_title": spec.get("article_title"),
            "chunks": len(chunks),
            "batches": len(batches),
            "used_by_tags": spec.get("used_by_tags", []),
            "requests_path": str(out_path.relative_to(PROJECT_ROOT)),
            "est_extraction_critic_usd": round(
                len(batches) * (TERRA_COST_PER_BATCH + SOL_CRITIC_COST_PER_BATCH), 2
            ),
        })

    manifest = {
        "version": "1.0.0",
        "scope": "KCL substantive rulegen (P1 property + P2 OOS substantive, 형법각칙)",
        "excludes": sorted(DONE_TARGETS) if not args.include_done else [],
        "pilot_calibration": {
            "source": "장물(제362조) pilot 2-batch (job 211619/211635)",
            "terra_cost_per_batch_usd": TERRA_COST_PER_BATCH,
            "sol_critic_cost_per_batch_usd": SOL_CRITIC_COST_PER_BATCH,
            "density_vs_fraud": "~0.5x (장물 25 cand/batch vs fraud ~51)",
            "note": "이 비용은 추출+후보비평 스테이지만. merge/normcard-critic/RuleIR/RuleIR-critic "
                    "다운스트림은 별도(fraud×density로 추정, 문서 참조).",
        },
        "totals": {
            "targets": len(manifest_targets),
            "chunks": total_chunks,
            "batches": total_batches,
            "est_extraction_critic_usd": round(
                total_batches * (TERRA_COST_PER_BATCH + SOL_CRITIC_COST_PER_BATCH), 2
            ),
        },
        "targets": manifest_targets,
    }
    manifest_path = args.out_dir / "kcl_substantive_campaign_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "targets": len(manifest_targets),
        "chunks": total_chunks,
        "batches": total_batches,
        "est_extraction_critic_usd": manifest["totals"]["est_extraction_critic_usd"],
        "manifest": str(manifest_path.relative_to(PROJECT_ROOT)),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
