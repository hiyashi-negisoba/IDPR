"""Minimal OpenAI-compatible client used only against a job-local vLLM server."""

from __future__ import annotations

import copy
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
        temperature: float = 0.0,
        top_p: float | None = None,
        top_k: int | None = None,
        seed: int | None = None,
        chat_template_kwargs: dict[str, Any] | None = None,
        user_template: str | None = None,
    ) -> tuple[dict[str, Any], dict[str, Any]]:
        request_payload = build_chat_request(
            model=self.model,
            system_prompt=system_prompt,
            payload=payload,
            schema_name=schema_name,
            schema=schema,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            seed=seed,
            chat_template_kwargs=chat_template_kwargs,
            user_template=user_template,
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
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise VLLMClientError(
                f"vLLM request failed with HTTP {exc.code}: {body}"
            ) from exc
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise VLLMClientError(f"vLLM request failed: {exc}") from exc

        try:
            choice = response_payload["choices"][0]
            content = choice["message"]["content"]
            output = json.loads(content)
        except json.JSONDecodeError as exc:
            finish_reason = response_payload.get("choices", [{}])[0].get(
                "finish_reason"
            )
            content_text = content if isinstance(content, str) else repr(content)
            raise VLLMClientError(
                "vLLM response contains incomplete JSON: "
                f"finish_reason={finish_reason}, characters={len(content_text)}, "
                f"suffix={content_text[-500:]!r}"
            ) from exc
        except (KeyError, IndexError, TypeError) as exc:
            message: Any = {}
            try:
                message = response_payload["choices"][0]["message"]
            except (KeyError, IndexError, TypeError):
                pass
            if not isinstance(message, Mapping):
                message = {}
            reasoning = message.get("reasoning") or message.get("reasoning_content")
            raise VLLMClientError(
                "vLLM response does not contain one JSON object: "
                f"message_keys={sorted(message)}, "
                f"content_type={type(message.get('content')).__name__}, "
                f"reasoning_chars={len(reasoning) if isinstance(reasoning, str) else 0}, "
                f"finish_reason={response_payload.get('choices', [{}])[0].get('finish_reason')}"
            ) from exc
        if not isinstance(output, dict):
            raise VLLMClientError("vLLM structured output must be a JSON object")
        if not isinstance(output, dict):
            raise VLLMClientError("vLLM structured output must be a JSON object")
        # Diagnostic-only: the gemma4 reasoning parser emits an open-ended
        # thinking phase before the schema-constrained JSON. Whether a
        # per-issue decision (e.g. unit_id="unsupported") was already fixed
        # before that thinking phase, or fixed within it, is only answerable
        # by reading this text — capturing it costs nothing and was
        # previously discarded on the success path (only surfaced in the
        # malformed-JSON error branch above).
        # Confirmed empty for the issue-selection call with no
        # chat_template_kwargs thinking flag set (docs/handoff/CURRENT.md
        # routing-override investigation, job 220284): the gemma4 reasoning
        # parser has a "reasoning" key to fill, but nothing was generated
        # into it — there is no hidden thinking phase preceding the
        # schema-constrained JSON for this call. Kept for future calls that
        # might set the thinking flag; costs nothing when the model leaves it
        # empty.
        reasoning_content = choice.get("message", {}).get(
            "reasoning_content"
        ) or choice.get("message", {}).get("reasoning")
        metadata = {
            "id": response_payload.get("id"),
            "model": response_payload.get("model"),
            "usage": response_payload.get("usage", {}),
            "finish_reason": choice.get("finish_reason"),
            "reasoning_content": reasoning_content,
        }
        return output, metadata

    def complete_text(
        self,
        *,
        system_prompt: str,
        user_template: str,
        payload: Mapping[str, Any] | None = None,
        max_tokens: int = 15000,
        temperature: float = 1.0,
        top_p: float | None = None,
        top_k: int | None = None,
        chat_template_kwargs: dict[str, Any] | None = None,
    ) -> str:
        """Generates plain text or markdown completions using vLLM chat completions API."""
        if payload is not None and "{{INPUT_JSON}}" in user_template:
            serialized_payload = json.dumps(payload, ensure_ascii=False, sort_keys=True)
            user_content = user_template.replace("{{INPUT_JSON}}", serialized_payload)
        else:
            user_content = user_template

        req: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
            "temperature": temperature,
            "max_tokens": max_tokens,
        }
        if top_p is not None:
            req["top_p"] = top_p
        if top_k is not None:
            req["top_k"] = top_k
        if chat_template_kwargs is not None:
            req["chat_template_kwargs"] = chat_template_kwargs

        request = urllib.request.Request(
            f"{self.base_url.rstrip('/')}/v1/chat/completions",
            data=json.dumps(req, ensure_ascii=False).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                response_payload = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise VLLMClientError(
                f"vLLM text request failed with HTTP {exc.code}: {body}"
            ) from exc
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            raise VLLMClientError(f"vLLM text request failed: {exc}") from exc

        try:
            choice = response_payload["choices"][0]
            content = choice["message"]["content"]
            return str(content)
        except (KeyError, IndexError, TypeError) as exc:
            raise VLLMClientError(f"vLLM text response invalid: {exc}") from exc


def build_chat_request(
    *,
    model: str,
    system_prompt: str,
    payload: Mapping[str, Any],
    schema_name: str,
    schema: Mapping[str, Any] | None,
    max_tokens: int,
    temperature: float = 0.0,
    top_p: float | None = None,
    top_k: int | None = None,
    seed: int | None = None,
    chat_template_kwargs: dict[str, Any] | None = None,
    user_template: str | None = None,
) -> dict[str, Any]:
    serialized_payload = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    if user_template is None:
        user_content = serialized_payload
    else:
        if "{{INPUT_JSON}}" in user_template:
            user_content = user_template.replace("{{INPUT_JSON}}", serialized_payload)
        else:
            user_content = user_template
    req: dict[str, Any] = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    if schema is not None:
        req["response_format"] = {
            "type": "json_schema",
            "json_schema": {
                "name": schema_name,
                "strict": True,
                "schema": vllm_compatible_schema(schema),
            },
        }
    if top_p is not None:
        req["top_p"] = top_p
    if top_k is not None:
        req["top_k"] = top_k
    if seed is not None:
        req["seed"] = seed
    if chat_template_kwargs is not None:
        req["chat_template_kwargs"] = chat_template_kwargs
    return req


def vllm_compatible_schema(schema: Mapping[str, Any] | None) -> dict[str, Any]:
    """Remove grammar-unsupported hints; authoritative host validation stays strict."""
    if schema is None:
        return {}

    result = copy.deepcopy(dict(schema))

    def visit(value: Any) -> None:
        if isinstance(value, dict):
            value.pop("uniqueItems", None)
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(result)
    return result
