from __future__ import annotations

import json
from pathlib import Path

from idpr.eval.input_formatter import scoped_question_text


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INVENTORY = PROJECT_ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl"


def _inventory() -> dict[str, dict]:
    return {
        row["sub_question_id"]: row
        for row in (
            json.loads(line) for line in INVENTORY.read_text(encoding="utf-8").splitlines()
        )
    }


def test_standalone_fact_scope_selects_the_named_narrative_paragraph() -> None:
    row = _inventory()["kcl_criminal_r10_p1_q1_ga"]

    scoped = scoped_question_text(row["question_text"], row["question_prompt"])

    assert "A의 은밀한 신체 부위" in scoped
    assert "3주간의 치료가 필요한 발목" in scoped
    assert "B에게 잡히자" not in scoped
    assert "4,000만 원" not in scoped
    assert row["question_prompt"] in " ".join(scoped.split())


def test_standalone_fact_scope_can_select_a_later_paragraph() -> None:
    row = _inventory()["kcl_criminal_r10_p1_q3_ga"]

    scoped = scoped_question_text(row["question_text"], row["question_prompt"])

    assert "4,000만 원" in scoped
    assert "A의 은밀한 신체 부위" not in scoped
    assert "B에게 잡히자" not in scoped


def test_inline_numbered_facts_support_multiple_requested_blocks() -> None:
    text = """(1) 첫 번째 사실이다.
(2) 두 번째 사실이다.
(3) 세 번째 사실이다.

(1)과 (3)에서 피고인의 죄책을 논하시오."""
    prompt = "(1)과 (3)에서 피고인의 죄책을 논하시오."

    scoped = scoped_question_text(text, prompt)

    assert "첫 번째 사실" in scoped
    assert "두 번째 사실" not in scoped
    assert "세 번째 사실" in scoped
    assert prompt in scoped


def test_unresolvable_scope_keeps_the_original_question() -> None:
    text = "번호가 없는 하나의 사실관계이다."

    assert scoped_question_text(text, "(2)에서 죄책을 논하시오.") == text
