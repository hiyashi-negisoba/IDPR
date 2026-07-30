"""LePREC must be a two-stage baseline, not an issue-list emitter.

LePREC's published task is issue classification, so running it end-to-end produces a
JSON issue list rather than an answer to the exam question. Graded as-is it scores near
zero on a rubric that asks for argument, for a reason that has nothing to do with issue
decomposition.

The comparison worth making is "zero-shot, plus an explicit issue decomposition". These
tests pin that stage 2 uses the vanilla prompt verbatim and differs from it only by the
appended issue block.
"""

from __future__ import annotations

import pytest

from idpr.baselines.leprec import LePRECBaseline, format_issue_block
from idpr.baselines.vanilla import (
    VANILLA_SYSTEM_PROMPT,
    VanillaBaseline,
    build_vanilla_user_prompt,
)


class RecordingClient:
    """Captures every prompt so the two stages can be inspected without a model."""

    def __init__(self, responses: list[str]) -> None:
        self._responses = list(responses)
        self.calls: list[dict[str, str]] = []

    def complete_text(self, *, system_prompt: str, user_template: str, **kwargs) -> str:
        self.calls.append(
            {"system_prompt": system_prompt, "user_template": user_template, **kwargs}
        )
        return self._responses.pop(0) if self._responses else ""


CASE = {
    "sub_question_id": "kcl_test_001",
    "question_text": "甲은 A를 협박하여 재물을 교부받았다.\n그 후 甲은 도망하였다.",
    "question_prompt": "甲의 죄책을 논하시오.",
    "fact_sentences": ["甲은 A를 협박하여 재물을 교부받았다.", "그 후 甲은 도망하였다."],
}

ISSUE_JSON = '```json\n["공갈죄의 성부", "준강도죄의 성부"]\n```'


def test_leprec_makes_two_model_calls():
    client = RecordingClient([ISSUE_JSON, "본 사안에서 甲은 공갈죄가 성립한다."])
    result = LePRECBaseline(client=client).run_case(CASE)
    assert len(client.calls) == 2
    assert result["reasoning_trace"]["model_calls"] == 2


def test_stage_two_uses_the_vanilla_prompt_plus_only_the_issue_block():
    client = RecordingClient([ISSUE_JSON, "답안"])
    LePRECBaseline(client=client).run_case(CASE)

    answer_call = client.calls[1]
    vanilla_prompt = build_vanilla_user_prompt(
        CASE["question_text"], CASE["question_prompt"]
    )

    assert answer_call["system_prompt"] == VANILLA_SYSTEM_PROMPT
    assert answer_call["user_template"].startswith(vanilla_prompt)
    # The remainder must be exactly the issue block: nothing else may differ from vanilla.
    remainder = answer_call["user_template"][len(vanilla_prompt) :]
    assert remainder == format_issue_block(["공갈죄의 성부", "준강도죄의 성부"])


def test_stage_two_matches_vanilla_exactly_when_no_issues_were_extracted():
    """A stage-1 failure must degrade to vanilla, not to a broken prompt."""
    client = RecordingClient(["", "답안"])
    LePRECBaseline(client=client).run_case(CASE)
    assert client.calls[1]["user_template"] == build_vanilla_user_prompt(
        CASE["question_text"], CASE["question_prompt"]
    )


def test_graded_response_is_the_answer_not_the_issue_list():
    client = RecordingClient([ISSUE_JSON, "본 사안에서 甲은 공갈죄가 성립한다."])
    result = LePRECBaseline(client=client).run_case(CASE)
    assert result["generated_response"] == "본 사안에서 甲은 공갈죄가 성립한다."
    # The decomposition is retained for analysis, not scored in place of the answer.
    assert result["extracted_issues"] == ["공갈죄의 성부", "준강도죄의 성부"]


def test_vanilla_and_leprec_share_one_prompt_definition():
    """If these drift apart the ablation stops isolating the decomposition."""
    client = RecordingClient(["답안"])
    VanillaBaseline(client=client).run_case(CASE)
    assert client.calls[0]["system_prompt"] == VANILLA_SYSTEM_PROMPT
    assert client.calls[0]["user_template"] == build_vanilla_user_prompt(
        CASE["question_text"], CASE["question_prompt"]
    )


@pytest.mark.parametrize(
    "raw,expected",
    [
        ('["공갈죄의 성부", "준강도죄의 성부"]', ["공갈죄의 성부", "준강도죄의 성부"]),
        ("1. 강제추행 간접정범 성부\n2. 주거침입강간치상 성부", ["강제추행 간접정범 성부", "주거침입강간치상 성부"]),
        # Korean issues are short; a long minimum length would discard real items.
        ("- 중지미수 인정 여부\n- 체포죄 성부", ["중지미수 인정 여부", "체포죄 성부"]),
        ("", []),
        ("ok", []),
    ],
)
def test_issue_parsing_fallbacks(raw, expected):
    assert LePRECBaseline(client=None)._parse_issues(raw) == expected


def test_offline_mode_makes_no_calls_and_returns_no_answer():
    result = LePRECBaseline(client=None).run_case(CASE)
    assert result["reasoning_trace"]["model_calls"] == 0
    assert result["generated_response"] == ""
