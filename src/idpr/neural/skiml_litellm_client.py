"""Synchronous client for the lab SKI-ML LiteLLM gateway, used against non-vLLM models.

``VLLMClient`` only ever talks to a job-local vLLM server and relies on its
guidance-backend grammar constraints for structured output.  This client instead
goes through the shared SKI-ML gateway (see ``idpr.llm.GatewayConfig``), which fronts
whatever model string litellm is given — including, per this project's confirmed
convention, ``anthropic/claude-sonnet-4-6``.  There is no guided-decoding grammar on
that path, so the JSON Schema is rendered into the prompt as an instruction rather
than enforced at generation time; a model that violates it still fails the same
downstream ``NativeHostError``/per-issue-degradation contract every other assessor
output goes through, so nothing about the pipeline's error handling changes.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any, Mapping


class SkimlClientError(RuntimeError):
    """Raised when the gateway returns a response this client cannot use."""


@dataclass(frozen=True, slots=True)
class SkimlLiteLLMClient:
    model: str
    api_key: str = field(repr=False, default="")
    api_base: str = ""
    ssl_verify: bool = False
    timeout_seconds: float = 300.0
    max_retries: int = 0

    @classmethod
    def from_env(cls, *, model: str) -> "SkimlLiteLLMClient":
        api_key = os.environ.get("SKIML_API_KEY", "").strip()
        api_base = os.environ.get("SKIML_API_BASE", "").strip()
        if not api_key or not api_base:
            raise SkimlClientError(
                "SKIML_API_KEY and SKIML_API_BASE are required for the SKI-ML gateway"
            )
        return cls(
            model=model,
            api_key=api_key,
            api_base=api_base,
            ssl_verify=_env_bool("SKIML_SSL_VERIFY", default=False),
            timeout_seconds=float(os.environ.get("IDPR_LLM_TIMEOUT_SECONDS", "300")),
            max_retries=int(os.environ.get("IDPR_LLM_MAX_RETRIES", "0")),
        )

    def _completion(self):
        import litellm

        os.environ.setdefault("LITELLM_LOG", "ERROR")
        litellm.api_key = self.api_key
        litellm.api_base = self.api_base
        litellm.ssl_verify = self.ssl_verify
        return litellm.completion

    def complete_json(
        self,
        *,
        system_prompt: str,
        payload: Mapping[str, Any],
        schema_name: str,
        schema: Mapping[str, Any],
        max_tokens: int,
        temperature: float = 0.0,
        user_template: str | None = None,
        **_ignored: Any,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        user_content = _render_user_content(payload, user_template)
        user_content += (
            "\n\n다음 JSON Schema를 만족하는 JSON 객체 하나만 출력하라. 코드 펜스나 "
            f"설명 문구 없이 객체만 출력한다.\n\n<JSON_SCHEMA name=\"{schema_name}\">\n"
            f"{json.dumps(schema, ensure_ascii=False, indent=2)}\n</JSON_SCHEMA>"
        )
        response = self._completion()(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
            timeout=self.timeout_seconds,
            num_retries=self.max_retries,
            # The gateway is addressed as an OpenAI-compatible endpoint
            # (Bearer auth against /v1/chat/completions) regardless of which
            # backend model the model string selects — letting litellm infer
            # the provider from the "anthropic/" prefix instead sends
            # Anthropic-native auth straight to the gateway host and 401s.
            # Matches idpr.llm.LLMGateway's existing terra/sol call shape.
            custom_llm_provider="openai",
        )
        content = _response_text(response)
        try:
            output = _parse_json_object(content)
        except SkimlClientError as exc:
            raise SkimlClientError(f"{exc} (schema={schema_name})") from exc
        metadata = {
            "id": getattr(response, "id", None),
            "model": getattr(response, "model", self.model),
            "usage": _response_usage(response),
            "finish_reason": response.choices[0].finish_reason
            if getattr(response, "choices", None)
            else None,
        }
        return output, metadata

    def complete_text(
        self,
        *,
        system_prompt: str,
        user_template: str,
        payload: Mapping[str, Any] | None = None,
        max_tokens: int = 8000,
        temperature: float = 0.0,
        **_ignored: Any,
    ) -> str:
        user_content = _render_user_content(payload or {}, user_template)
        response = self._completion()(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
            timeout=self.timeout_seconds,
            num_retries=self.max_retries,
            # The gateway is addressed as an OpenAI-compatible endpoint
            # (Bearer auth against /v1/chat/completions) regardless of which
            # backend model the model string selects — letting litellm infer
            # the provider from the "anthropic/" prefix instead sends
            # Anthropic-native auth straight to the gateway host and 401s.
            # Matches idpr.llm.LLMGateway's existing terra/sol call shape.
            custom_llm_provider="openai",
        )
        return _response_text(response)


def _render_user_content(payload: Mapping[str, Any], user_template: str | None) -> str:
    if user_template is None:
        return json.dumps(payload, ensure_ascii=False, sort_keys=True)
    if "{{INPUT_JSON}}" in user_template:
        return user_template.replace(
            "{{INPUT_JSON}}", json.dumps(payload, ensure_ascii=False, sort_keys=True)
        )
    return user_template


def _response_text(response: Any) -> str:
    try:
        content = response.choices[0].message.content
    except (AttributeError, IndexError) as exc:
        raise SkimlClientError(f"gateway response has no text content: {exc}") from exc
    if not isinstance(content, str) or not content.strip():
        finish_reason = getattr(response.choices[0], "finish_reason", None) if getattr(
            response, "choices", None
        ) else None
        raise SkimlClientError(f"gateway response is empty (finish_reason={finish_reason})")
    return content


def _parse_json_object(content: str) -> dict[str, Any]:
    stripped = content.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if len(lines) >= 3 and lines[-1].strip().startswith("```"):
            stripped = "\n".join(lines[1:-1])
    try:
        value = json.loads(stripped)
    except json.JSONDecodeError as exc:
        raise SkimlClientError(
            f"gateway content is not valid JSON: {exc} (suffix={stripped[-300:]!r})"
        ) from exc
    if not isinstance(value, dict):
        raise SkimlClientError("gateway JSON response must be an object")
    return value


def _response_usage(response: Any) -> dict[str, int]:
    usage = getattr(response, "usage", None)
    result: dict[str, int] = {}
    for key in ("prompt_tokens", "completion_tokens", "total_tokens"):
        value = getattr(usage, key, None)
        if isinstance(value, int):
            result[key] = value
    return result


def _env_bool(name: str, *, default: bool) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise SkimlClientError(f"{name} must be a boolean")
