from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INVENTORY = PROJECT_ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl"
MANIFEST = PROJECT_ROOT / "data/commentary/kcl_criminal_v1_tag_commentary_manifest.jsonl"
CHUNKS = PROJECT_ROOT / "data/commentary/kcl_criminal_v1_commentary_chunks.jsonl"
REVIEW = PROJECT_ROOT / "data/commentary/kcl_criminal_v1_commentary_review.md"
POOL = PROJECT_ROOT / "data/commentary/kcl_criminal_v1_commentary_pool.json"
AUDIT = PROJECT_ROOT / "data/commentary/kcl_criminal_v1_non_mapped_audit.md"


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def test_commentary_bundle_artifacts_exist() -> None:
    assert MANIFEST.exists()
    assert CHUNKS.exists()
    assert REVIEW.exists()
    assert POOL.exists()
    assert AUDIT.exists()


def test_commentary_manifest_covers_every_issue_tag() -> None:
    inventory_tags = {
        tag
        for row in load_jsonl(INVENTORY)
        for tag in row["issue_tags"]
    }
    manifest_rows = load_jsonl(MANIFEST)
    manifest_tags = {row["tag"] for row in manifest_rows}

    assert len(manifest_rows) == 165
    assert manifest_tags == inventory_tags


def test_commentary_manifest_uses_metadata_targets_not_search_scores() -> None:
    rows = {row["tag"]: row for row in load_jsonl(MANIFEST)}

    fraud_targets = rows["fraud"]["targets"]
    assert rows["fraud"]["status"] == "mapped"
    assert any(
        target["law_id"] == "001692" and target["article_no"] == "제347조"
        for target in fraud_targets
    )

    partial_appeal_targets = rows["partial_appeal"]["targets"]
    assert rows["partial_appeal"]["status"] == "mapped"
    assert any(
        target["law_id"] == "001671" and target["article_no"] == "제342조"
        for target in partial_appeal_targets
    )

    assert rows["joint_principal"]["status"] == "mapped_with_corpus_gap"
    assert rows["joint_principal"]["targets"]


def test_commentary_manifest_records_manual_audit_corrections() -> None:
    rows = {row["tag"]: row for row in load_jsonl(MANIFEST)}
    counts = Counter(row["status"] for row in rows.values())

    assert counts == {
        "mapped": 137,
        "mapped_with_corpus_gap": 21,
        "unavailable_in_current_commentary": 7,
    }
    assert rows["attempted_murder"]["status"] == "mapped"
    assert rows["special_robbery_attempt"]["status"] == "mapped"
    assert {
        target["article_no"]
        for target in rows["relative_property_crime_exception"]["targets"]
    } == {"제328조", "제344조"}
    complaint_targets = {
        (target["law_id"], target["article_no"])
        for target in rows["offense_subject_to_complaint"]["targets"]
    }
    assert ("001692", "제306조") not in complaint_targets
    assert {("001692", "제323조"), ("001692", "제328조")} <= complaint_targets


def test_all_33_previously_non_mapped_tags_have_a_manual_audit() -> None:
    text = AUDIT.read_text(encoding="utf-8")

    assert "- 검토: 33/33" in text
    assert text.count("| `") == 33
    assert "KCL `rubric_summary`와 의미검색 점수는 mapping 근거로 사용하지 않았습니다." in text


def test_commentary_chunks_are_unique_and_traceable_to_tags() -> None:
    chunks = load_jsonl(CHUNKS)
    comment_ids = [row["comment_id"] for row in chunks]

    assert chunks
    assert len(comment_ids) == len(set(comment_ids))
    assert all(row["used_by_tags"] for row in chunks)
    assert all(row["law_id"] and row["article_no"] and row["section_path"] for row in chunks)
    assert all(row["document_text"] for row in chunks)
    assert all(row["source_kind"] and row["source_path"] for row in chunks)

    tags_with_chunks = {tag for row in chunks for tag in row["used_by_tags"]}
    mapped_tags = {
        row["tag"]
        for row in load_jsonl(MANIFEST)
        if row["status"] in {"mapped", "mapped_with_corpus_gap"}
    }
    assert mapped_tags <= tags_with_chunks


def test_commentary_pool_is_exact_and_has_raw_pdf_fallbacks() -> None:
    pool = json.loads(POOL.read_text(encoding="utf-8"))
    chunks = load_jsonl(CHUNKS)

    assert pool["selection_policy"]["semantic_search"] is False
    assert pool["selection_policy"]["embedding_or_reranker"] is False
    assert pool["primary_source"]["parsed_rows"] == 9384
    assert pool["selected"] == {
        "excluded_source_rows": 6281,
        "metadata_targets": 102,
        "parsed_parquet_chunks": 3103,
        "raw_pdf_fallback_chunks": 5,
        "unique_chunks": 3108,
    }
    assert {row["article_no"] for row in pool["raw_pdf_fallbacks"]} == {
        "제254조",
        "제300조",
        "제342조",
        "제344조",
    }
    fallback_chunks = [row for row in chunks if row["source_kind"] == "raw_pdf_fallback"]
    assert len(fallback_chunks) == 5
    assert all("raw_pdf.page_" in row["section_path"] for row in fallback_chunks)
