"""Gemini native generateContent client through the lab LiteLLM passthrough."""

from __future__ import annotations

import asyncio
import json
import ssl
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Awaitable, Callable, Mapping, Sequence

from idpr.llm import (
    GatewayConfig,
    GatewayResponseError,
    JSONCompletionJob,
    JSONCompletionResult,
    _canonical_sha256,
    _parse_json_object,
    _read_json,
    _write_json_atomic,
)


NativePostCallable = Callable[..., Awaitable[Mapping[str, Any]]]

THINKING_BUDGETS = {
    "none": 0,
    "minimal": 1_024,
    "low": 1_024,
    "medium": 8_192,
    "high": 24_576,
    "xhigh": 24_576,
}


class GeminiNativeGateway:
    """Call Gemini's native API while retaining the existing cache contract."""

    transport = "gemini_native_generate_content"

    def __init__(
        self,
        config: GatewayConfig,
        *,
        model: str,
        safety_settings: Sequence[Mapping[str, str]],
        response_json_schema: Mapping[str, Any] | None = None,
        post_json: NativePostCallable | None = None,
    ) -> None:
        self.config = config
        self.model = model
        self.native_model = _native_model_name(model)
        self.safety_settings = [dict(setting) for setting in safety_settings]
        self.response_json_schema = (
            json.loads(json.dumps(response_json_schema))
            if response_json_schema is not None
            else None
        )
        self._post_json = post_json or _post_native_json

    async def complete_json(self, job: JSONCompletionJob) -> JSONCompletionResult:
        generation_config: dict[str, Any] = {
            "maxOutputTokens": job.max_tokens,
            "responseMimeType": "application/json",
        }
        if job.temperature is not None:
            generation_config["temperature"] = job.temperature
        if job.reasoning_effort is not None:
            generation_config["thinkingConfig"] = {
                "thinkingBudget": THINKING_BUDGETS[job.reasoning_effort]
            }
        if self.response_json_schema is not None:
            generation_config["responseJsonSchema"] = self.response_json_schema
        body = {
            "systemInstruction": {"parts": [{"text": job.system_prompt}]},
            "contents": [
                {
                    "role": "user",
                    "parts": [
                        {
                            "text": json.dumps(
                                job.payload, ensure_ascii=False, sort_keys=True
                            )
                        }
                    ],
                }
            ],
            "safetySettings": self.safety_settings,
            "generationConfig": generation_config,
        }
        request_envelope = {
            "version": "1.0.0",
            "transport": self.transport,
            "request_id": job.request_id,
            "role": job.role,
            "model": self.model,
            "body": body,
        }
        request_sha256 = _canonical_sha256(request_envelope)
        cache_path = self._cache_path(job.role, request_sha256)
        cached = _read_json(cache_path)
        if cached is not None:
            return JSONCompletionResult(
                request_id=job.request_id,
                role=job.role,
                model=self.model,
                request_sha256=request_sha256,
                output=dict(cached["output"]),
                usage=dict(cached.get("usage", {})),
                cached=True,
                response_id=cached.get("response_id"),
            )

        endpoint = (
            self.config.api_base.rstrip("/")
            + "/gemini/v1beta/models/"
            + urllib.parse.quote(self.native_model, safe="-._~")
            + ":generateContent"
        )
        response: Mapping[str, Any] | None = None
        last_error: Exception | None = None
        for _ in range(self.config.max_retries + 1):
            try:
                response = await self._post_json(
                    endpoint=endpoint,
                    api_key=self.config.api_key,
                    payload=body,
                    timeout_seconds=self.config.timeout_seconds,
                    ssl_verify=self.config.ssl_verify,
                )
                break
            except Exception as error:  # Retried according to the sealed API setting.
                last_error = error
        if response is None:
            assert last_error is not None
            raise last_error

        usage = _native_usage(response)
        response_id = response.get("responseId")
        try:
            content = _native_content(response)
            output = _parse_json_object(content)
        except GatewayResponseError as error:
            self._write_failure(
                job=job,
                request_sha256=request_sha256,
                response=response,
                usage=usage,
                error=str(error),
            )
            raise
        artifact = {
            "version": "1.0.0",
            "transport": self.transport,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "request_id": job.request_id,
            "role": job.role,
            "model": self.model,
            "request_sha256": request_sha256,
            "output": output,
            "usage": usage,
            "response_id": response_id,
        }
        _write_json_atomic(cache_path, artifact)
        return JSONCompletionResult(
            request_id=job.request_id,
            role=job.role,
            model=self.model,
            request_sha256=request_sha256,
            output=output,
            usage=usage,
            cached=False,
            response_id=response_id if isinstance(response_id, str) else None,
        )

    def discard_cache(self, result: JSONCompletionResult) -> None:
        self._cache_path(result.role, result.request_sha256).unlink(missing_ok=True)

    def _cache_path(self, role: str, digest: str) -> Path:
        safe_model = self.model.replace("/", "__")
        return self.config.cache_dir / self.transport / role / safe_model / f"{digest}.json"

    def _write_failure(
        self,
        *,
        job: JSONCompletionJob,
        request_sha256: str,
        response: Mapping[str, Any],
        usage: Mapping[str, int],
        error: str,
    ) -> None:
        candidates = response.get("candidates") or []
        finish_reason = candidates[0].get("finishReason") if candidates else None
        path = (
            self.config.cache_dir
            / "failures"
            / self.transport
            / job.role
            / self.model.replace("/", "__")
            / f"{request_sha256}.json"
        )
        _write_json_atomic(
            path,
            {
                "version": "1.0.0",
                "transport": self.transport,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "request_id": job.request_id,
                "role": job.role,
                "model": self.model,
                "request_sha256": request_sha256,
                "response_id": response.get("responseId"),
                "finish_reason": finish_reason,
                "prompt_feedback": response.get("promptFeedback"),
                "usage": dict(usage),
                "error": error,
            },
        )


def _native_model_name(model: str) -> str:
    normalized = model.removeprefix("openai/")
    if not normalized.startswith("gemini/"):
        raise ValueError(f"Gemini native transport requires a gemini/ model: {model}")
    return normalized.removeprefix("gemini/")


def _native_content(response: Mapping[str, Any]) -> str:
    candidates = response.get("candidates") or []
    if not candidates:
        block_reason = (response.get("promptFeedback") or {}).get("blockReason")
        raise GatewayResponseError(
            f"Gemini response has no candidates (block_reason={block_reason})"
        )
    candidate = candidates[0]
    parts = (candidate.get("content") or {}).get("parts") or []
    content = "".join(part.get("text", "") for part in parts if isinstance(part, Mapping))
    if not content.strip():
        raise GatewayResponseError(
            "Gemini response has no text content "
            f"(finish_reason={candidate.get('finishReason')})"
        )
    return content


def _native_usage(response: Mapping[str, Any]) -> dict[str, int]:
    metadata = response.get("usageMetadata") or {}
    mapping = {
        "prompt_tokens": "promptTokenCount",
        "completion_tokens": "candidatesTokenCount",
        "reasoning_tokens": "thoughtsTokenCount",
        "total_tokens": "totalTokenCount",
    }
    return {
        target: value
        for target, source in mapping.items()
        if isinstance((value := metadata.get(source)), int)
    }


async def _post_native_json(
    *,
    endpoint: str,
    api_key: str,
    payload: Mapping[str, Any],
    timeout_seconds: float,
    ssl_verify: bool,
) -> Mapping[str, Any]:
    def send() -> Mapping[str, Any]:
        url = endpoint + "?" + urllib.parse.urlencode({"key": api_key})
        request = urllib.request.Request(
            url,
            data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        context = None if ssl_verify else ssl._create_unverified_context()
        try:
            with urllib.request.urlopen(
                request, timeout=timeout_seconds, context=context
            ) as response:
                value = json.load(response)
        except urllib.error.HTTPError as error:
            try:
                detail = json.loads(error.read().decode("utf-8"))
                message = str((detail.get("error") or {}).get("message", ""))
            except (UnicodeDecodeError, json.JSONDecodeError, AttributeError):
                message = ""
            suffix = f": {message}" if message else ""
            raise GatewayResponseError(
                f"Gemini native HTTP {error.code}{suffix}"
            ) from error
        if not isinstance(value, Mapping):
            raise GatewayResponseError("Gemini native response is not an object")
        return value

    return await asyncio.to_thread(send)
