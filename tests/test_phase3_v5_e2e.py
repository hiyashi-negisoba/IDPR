from __future__ import annotations

import json
from pathlib import Path

from scripts.verify_phase3_v5_e2e import KCL, USER, verify_v5


def _write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")


def test_v5_gate_prioritizes_core_coverage_and_logical_consistency(tmp_path: Path):
    root = tmp_path / "v5"
    root.mkdir()
    rows = [
        {"sub_question_id": KCL, "articles": ["art298", "art297", "art301"]},
        {"sub_question_id": USER, "articles": ["art347"]},
    ]
    (root / "l0_candidates.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )
    for case_id, articles in ((KCL, rows[0]["articles"]), (USER, rows[1]["articles"])):
        lifecycle = [
            {
                "article": article,
                "provenance": {"sources": ["model_selected"]},
                "relevance": "must_discuss",
                "visibility_decision": "compact",
                "visibility_reason": "must_discuss_no_positive_element_support",
                "included_in_call3": True,
            }
            for article in articles
        ]
        required = [
            {
                "article": article,
                "verdict": "unknown",
                "stated_conclusion": "undetermined",
                "symbolic_directive": "undetermined",
            }
            for article in articles
        ]
        _write_json(
            root / "cases" / case_id / "answer.json",
            {"request": {"candidate_lifecycle": lifecycle, "required_sections": required}},
        )

    report = verify_v5(root)
    assert report["status"] == "passed"
    assert report["checks"]["kcl_core_issue_families_reach_call3"] is True

    answer_path = root / "cases" / KCL / "answer.json"
    answer = json.loads(answer_path.read_text(encoding="utf-8"))
    answer["request"]["required_sections"][0].update(
        {"verdict": "not_established", "stated_conclusion": "established"}
    )
    _write_json(answer_path, answer)
    failed = verify_v5(root)
    assert failed["status"] == "failed"
    assert failed["checks"]["relevance_verdict_conclusion_consistent"] is False


def test_v5_slurm_wraps_full_smoke_and_lifecycle_gates():
    root = Path(__file__).resolve().parents[1]
    script = (root / "scripts/slurm/run_phase3_v5_e2e.sh").read_text(
        encoding="utf-8"
    )
    assert "run_phase3_e2e_smoke.sh" in script
    assert "report_phase3_candidate_lifecycle.py" in script
    assert "verify_phase3_v5_e2e.py" in script
    assert "IDPR_TESTED_CODE_COMMIT" in script
