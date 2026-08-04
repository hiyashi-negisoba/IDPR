from __future__ import annotations

import pytest

from idpr.neural.vllm_client import VLLMClientError
from scripts.run_rule_ir_core_kcl_e2e import CoreStageCallError, _call


class _FlakyClient:
    def __init__(self, *, always_fail: bool = False) -> None:
        self.calls = 0
        self.always_fail = always_fail

    def complete_json(self, **kwargs):
        self.calls += 1
        if self.always_fail or self.calls == 1:
            raise VLLMClientError("finish_reason=length; incomplete JSON")
        return {"ok": True}, {"finish_reason": "stop"}


def test_stage_call_retries_incomplete_model_json() -> None:
    client = _FlakyClient()
    output, attempts = _call(
        client=client, stage="selection", payload={"case_id": "case-1"},
        schema={"type": "object"}, max_tokens=100,
        validator=lambda value: None,
    )
    assert output == {"ok": True}
    assert client.calls == 2
    assert attempts[0].get("invalid_output") is None
    assert attempts[1]["error"] is None


def test_stage_call_preserves_exhausted_generation_failures() -> None:
    client = _FlakyClient(always_fail=True)
    with pytest.raises(CoreStageCallError) as exc_info:
        _call(
            client=client, stage="selection", payload={"case_id": "case-1"},
            schema={"type": "object"}, max_tokens=100,
            validator=lambda value: None,
        )
    assert exc_info.value.stage == "selection"
    assert len(exc_info.value.attempts) == 3
    assert all(item.get("invalid_output") is None for item in exc_info.value.attempts)
