"""죄명-불문 rulegen requests 빌더 (API 아님, 결정론).

주석서 chunk를 section_path 보존 배치로 묶어 `extract_norm_candidates` 요청
JSONL을 만든다. 사기 exemplar 빌더(`build_fraud_rulegen_exemplar.py`)의 배칭 로직
(`make_batches`/`build_request`)을 죄명-파라미터화한 것으로, 손으로 짠 NormCard/
RuleIR 부분(사기 전용 few-shot gold)은 포함하지 않는다 — 그 산출은 terra가 생성한다.

사용 예:
  python scripts/build_rulegen_requests.py \
    --issue-tag stolen_property --law-id 001692 --article-no 제362조 \
    --article-title '장물의 취득, 알선 등' \
    --request-id-prefix stolen_property.article362.pass1 \
    --out data/rulegen/stolen_property/stolen_property_rulegen_requests.jsonl
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
COMMENTARY = PROJECT_ROOT / "data/commentary/kcl_criminal_v1_commentary_chunks.jsonl"
MAX_BATCH_CHARS = 12_000


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def make_batches(chunks: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    batches: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    current_chars = 0
    for chunk in sorted(chunks, key=lambda row: (row["section_path"], row["comment_id"])):
        n_chars = len(chunk["document_text"])
        if current and current_chars + n_chars > MAX_BATCH_CHARS:
            batches.append(current)
            current = []
            current_chars = 0
        current.append(chunk)
        current_chars += n_chars
    if current:
        batches.append(current)
    return batches


def build_request(
    batch: list[dict[str, Any]],
    index: int,
    count: int,
    *,
    issue_tag: str,
    law_id: str,
    article_no: str,
    article_title: str,
    request_id_prefix: str,
) -> dict[str, Any]:
    commentary_chunks = [
        {
            "comment_id": row["comment_id"],
            "section_path": row["section_path"],
            "section_title": row["section_title"],
            "document_text": row["document_text"],
        }
        for row in batch
    ]
    return {
        "request_id": f"{request_id_prefix}.{index:03d}",
        "task": "extract_norm_candidates",
        "issue_tag": issue_tag,
        "target": {
            "law_id": law_id,
            "article_no": article_no,
            "article_title": article_title,
        },
        "batch": {
            "index": index,
            "count": count,
            "section_paths": sorted({row["section_path"] for row in batch}),
            "n_chars": sum(len(row["document_text"]) for row in batch),
        },
        "commentary_chunks": commentary_chunks,
        "constraints": {
            "source_refs_must_be_exact": True,
            "preserve_disagreements": True,
            "legal_status": "draft",
            "output_schema": "idpr/NormCandidateBatch",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--issue-tag", required=True)
    parser.add_argument("--law-id", required=True)
    parser.add_argument("--article-no", required=True)
    parser.add_argument("--article-title", required=True)
    parser.add_argument("--request-id-prefix", required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--commentary", type=Path, default=COMMENTARY)
    args = parser.parse_args()

    all_chunks = load_jsonl(args.commentary)
    chunks = [
        row
        for row in all_chunks
        if row["law_id"] == args.law_id and row["article_no"] == args.article_no
    ]
    if not chunks:
        parser.error(f"no chunks for law_id={args.law_id} article_no={args.article_no}")

    section_counts: dict[tuple[str, str], dict[str, int]] = defaultdict(
        lambda: {"chunks": 0, "n_chars": 0}
    )
    for row in chunks:
        stats = section_counts[(row["section_path"], row["section_title"])]
        stats["chunks"] += 1
        stats["n_chars"] += len(row["document_text"])

    batches = make_batches(chunks)
    requests = [
        build_request(
            batch,
            index,
            len(batches),
            issue_tag=args.issue_tag,
            law_id=args.law_id,
            article_no=args.article_no,
            article_title=args.article_title,
            request_id_prefix=args.request_id_prefix,
        )
        for index, batch in enumerate(batches, start=1)
    ]

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(
            json.dumps(request, ensure_ascii=False, sort_keys=True) + "\n"
            for request in requests
        ),
        encoding="utf-8",
    )
    index_path = args.out.with_name(args.out.stem + "_index.json")
    index_path.write_text(
        json.dumps(
            {
                "target_path": f"commentary://{args.law_id}/{args.article_no}",
                "issue_tag": args.issue_tag,
                "chunks": len(chunks),
                "n_chars": sum(len(row["document_text"]) for row in chunks),
                "batch_max_chars": MAX_BATCH_CHARS,
                "batches": len(batches),
                "sections": [
                    {"section_path": key[0], "section_title": key[1], **value}
                    for key, value in sorted(section_counts.items())
                ],
            },
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "issue_tag": args.issue_tag,
                "chunks": len(chunks),
                "batches": len(batches),
                "requests": str(args.out),
                "index": str(index_path),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
