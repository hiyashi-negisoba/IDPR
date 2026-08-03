from __future__ import annotations

import json
from pathlib import Path

from scripts.report_phase3_candidate_lifecycle import build_report


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def test_lifecycle_report_requires_lossless_candidates_and_mandatory_survival(
    tmp_path: Path,
):
    root = tmp_path / "run"
    root.mkdir()
    (root / "l0_candidates.jsonl").write_text(
        json.dumps(
            {"sub_question_id": "case-1", "articles": ["art136", "art329"]}
        )
        + "\n",
        encoding="utf-8",
    )
    lifecycle = [
        {
            "article": "art136",
            "provenance": {"sources": ["question_selected"]},
            "relevance": "must_discuss",
            "visibility_decision": "compact",
            "visibility_reason": "must_discuss_no_positive_element_support",
            "included_in_call3": True,
        },
        {
            "article": "art329",
            "provenance": {"sources": ["retrieval_selected"]},
            "relevance": "optional",
            "visibility_decision": "hidden",
            "visibility_reason": "no_positive_element_support",
            "included_in_call3": False,
        },
    ]
    answer_path = root / "cases" / "case-1" / "answer.json"
    _write_json(answer_path, {"request": {"candidate_lifecycle": lifecycle}})

    report = build_report(root)
    assert report["status"] == "passed"
    assert report["must_discuss"] == {
        "total": 1,
        "hidden": 0,
        "survival_rate": 1.0,
    }
    assert report["visibility_counts"] == {"compact": 1, "hidden": 1}

    lifecycle[0]["included_in_call3"] = False
    lifecycle[0]["visibility_decision"] = "hidden"
    _write_json(answer_path, {"request": {"candidate_lifecycle": lifecycle}})
    failed = build_report(root)
    assert failed["status"] == "failed"
    assert failed["must_discuss"]["hidden"] == 1
