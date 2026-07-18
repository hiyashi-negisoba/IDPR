"""Minimal OpenAI-compatible client used only against a job-local vLLM server."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Mapping


class VLLMClientError(RuntimeError):
    """Raised when the local vLLM endpoint returns an unusable response."""


@dataclass(frozen=True, slots=True)
class VLLMClient:
    base_url: str
    model: str
    api_key: str = "local-idpr"
    timeout_seconds: float = 1200.0

    def complete_json(
        self,
        *,
        system_prompt: str,
        payload: Mapping[str, Any],
        schema_name: str,
        schema: Mapping[str, Any],
        max_tokens: int,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        request_payload = build_chat_request(
            model=self.model,
            system_prompt=system_prompt,
            payload=payload,
            schema_name=schema_name,
            schema=schema,
            max_tokens=max_tokens,
        )
        request = urllib.request.Request(
            f"{self.base_url.rstrip('/')}/v1/chat/completions",
            data=json.dumps(request_payload, ensure_ascii=False).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                response_payload = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise VLLMClientError(f"vLLM request failed: {exc}") from exc

        try:
            content = response_payload["choices"][0]["message"]["content"]
            output = json.loads(content)
        except (KeyError, IndexError, TypeError, json.JSONDecodeError) as exc:
            raise VLLMClientError("vLLM response does not contain one JSON object") from exc
        if not isinstance(output, dict):
            raise VLLMClientError("vLLM structured output must be a JSON object")
        metadata = {
            "id": response_payload.get("id"),
            "model": response_payload.get("model"),
            "usage": response_payload.get("usage", {}),
            "finish_reason": response_payload["choices"][0].get("finish_reason"),
        }
        return output, metadata


def build_chat_request(
    *,
    model: str,
    system_prompt: str,
    payload: Mapping[str, Any],
    schema_name: str,
    schema: Mapping[str, Any],
    max_tokens: int,
) -> dict[str, Any]:
    return {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": json.dumps(payload, ensure_ascii=False, sort_keys=True),
            },
        ],
        "temperature": 0,
        "max_tokens": max_tokens,
        "response_format": {
            "type": "json_schema",
            "json_schema": {
                "name": schema_name,
                "strict": True,
                "schema": dict(schema),
            },
        },
    }
