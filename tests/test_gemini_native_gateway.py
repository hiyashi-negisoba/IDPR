from __future__ import annotations

import asyncio
from pathlib import Path

import pytest

from idpr.llm import GatewayConfig, JSONCompletionJob
from idpr.llm.gemini_native import GeminiNativeGateway


def config(tmp_path: Path) -> GatewayConfig:
    return GatewayConfig(
        api_key="secret-key",
        terra_model="unused",
        sol_model="unused",
        api_base="https://gateway.example",
        cache_dir=tmp_path / "cache",
        max_retries=0,
    )


def test_native_gateway_sends_full_payload_safety_settings_and_caches(
    tmp_path: Path,
) -> None:
    calls: list[dict] = []

    async def fake_post(**kwargs: object) -> dict:
        calls.append(dict(kwargs))
        return {
            "responseId": "native-1",
            "candidates": [
                {
                    "finishReason": "STOP",
                    "content": {"parts": [{"text": '{"ok":true}'}]},
                }
            ],
            "usageMetadata": {
                "promptTokenCount": 10,
                "candidatesTokenCount": 2,
                "thoughtsTokenCount": 3,
                "totalTokenCount": 15,
            },
        }

    settings = [
        {
            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
            "threshold": "BLOCK_NONE",
        }
    ]
    gateway = GeminiNativeGateway(
        config(tmp_path),
        model="gemini/gemini-2.5-flash",
        safety_settings=settings,
        post_json=fake_post,
    )
    job = JSONCompletionJob(
        request_id="native-test",
        role="terra",
        system_prompt="Academic legal evaluation only.",
        payload={"question": "원문", "answer": "답안"},
        max_tokens=512,
        temperature=0.0,
        reasoning_effort="low",
    )

    first = asyncio.run(gateway.complete_json(job))
    second = asyncio.run(gateway.complete_json(job))

    assert first.output == {"ok": True}
    assert first.model == "gemini/gemini-2.5-flash"
    assert first.usage["reasoning_tokens"] == 3
    assert not first.cached
    assert second.cached
    assert len(calls) == 1
    assert calls[0]["endpoint"].endswith(
        "/gemini/v1beta/models/gemini-2.5-flash:generateContent"
    )
    assert calls[0]["api_key"] == "secret-key"
    payload = calls[0]["payload"]
    assert payload["safetySettings"] == settings
    assert payload["generationConfig"]["thinkingConfig"] == {
        "thinkingBudget": 1024
    }
    assert "원문" in payload["contents"][0]["parts"][0]["text"]


def test_native_gateway_rejects_non_gemini_alias(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="requires a gemini/ model"):
        GeminiNativeGateway(
            config(tmp_path),
            model="openai/gpt-5.6-terra",
            safety_settings=[],
        )
