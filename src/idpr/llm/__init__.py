"""SKI-ML Gateway client with deterministic request caching."""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Awaitable, Callable, Literal, Mapping, Sequence


ModelRole = Literal["terra", "sol"]
ReasoningEffort = Literal["none", "minimal", "low", "medium", "high", "xhigh"]
CompletionCallable = Callable[..., Awaitable[Any]]
DEFAULT_API_BASE = "https://147.47.200.198:7861"


class GatewayConfigurationError(ValueError):
    """Raised before a request when required Gateway settings are missing."""


class GatewayResponseError(ValueError):
    """Raised when a Gateway response cannot satisfy the JSON contract."""


@dataclass(frozen=True, slots=True)
class GatewayConfig:
    api_key: str = field(repr=False)
    terra_model: str
    sol_model: str
    api_base: str = DEFAULT_API_BASE
    cache_dir: Path = Path(".cache/llm")
    ssl_verify: bool = False
    max_concurrency: int = 1
    timeout_seconds: float = 180.0
    max_retries: int = 0
    use_json_response_format: bool = False

    @classmethod
    def from_env(
        cls,
        *,
        require_api_key: bool = True,
        require_models: bool = True,
    ) -> GatewayConfig:
        api_key = os.environ.get("SKIML_API_KEY", "").strip()
        terra_model = os.environ.get("IDPR_TERRA_MODEL", "").strip()
        sol_model = os.environ.get("IDPR_SOL_MODEL", "").strip()
        if require_api_key and not api_key:
            raise GatewayConfigurationError("SKIML_API_KEY is required for execution")
        if require_models and not terra_model:
            raise GatewayConfigurationError("IDPR_TERRA_MODEL is required for execution")
        if require_models and not sol_model:
            raise GatewayConfigurationError("IDPR_SOL_MODEL is required for execution")

        max_concurrency = int(os.environ.get("IDPR_LLM_MAX_CONCURRENCY", "1"))
        if max_concurrency < 1:
            raise GatewayConfigurationError("IDPR_LLM_MAX_CONCURRENCY must be positive")
        return cls(
            api_key=api_key,
            terra_model=terra_model,
            sol_model=sol_model,
            api_base=os.environ.get("SKIML_API_BASE", DEFAULT_API_BASE).strip(),
            cache_dir=Path(os.environ.get("IDPR_LLM_CACHE_DIR", ".cache/llm")),
            ssl_verify=_env_bool("SKIML_SSL_VERIFY", default=False),
            max_concurrency=max_concurrency,
            timeout_seconds=float(os.environ.get("IDPR_LLM_TIMEOUT_SECONDS", "180")),
            max_retries=int(os.environ.get("IDPR_LLM_MAX_RETRIES", "0")),
            use_json_response_format=_env_bool(
                "IDPR_LLM_JSON_RESPONSE_FORMAT", default=False
            ),
        )

    def model_for_role(self, role: ModelRole) -> str:
        model = self.terra_model if role == "terra" else self.sol_model
        if not model:
            raise GatewayConfigurationError(f"No model configured for role {role}")
        return model if model.startswith("openai/") else f"openai/{model}"


@dataclass(frozen=True, slots=True)
class JSONCompletionJob:
    request_id: str
    role: ModelRole
    system_prompt: str
    payload: Mapping[str, Any]
    max_tokens: int = 6_000
    temperature: float | None = None
    reasoning_effort: ReasoningEffort | None = None


@dataclass(frozen=True, slots=True)
class JSONCompletionResult:
    request_id: str
    role: ModelRole
    model: str
    request_sha256: str
    output: dict[str, Any]
    usage: dict[str, int]
    cached: bool
    response_id: str | None

    def manifest_record(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "role": self.role,
            "model": self.model,
            "request_sha256": self.request_sha256,
            "usage": self.usage,
            "cached": self.cached,
            "response_id": self.response_id,
        }


class LLMGateway:
    """Call LiteLLM asynchronously while caching parsed JSON responses."""

    def __init__(
        self,
        config: GatewayConfig,
        *,
        completion: CompletionCallable | None = None,
    ) -> None:
        self.config = config
        self._completion = completion

    async def complete_json(self, job: JSONCompletionJob) -> JSONCompletionResult:
        model = self.config.model_for_role(job.role)
        request_payload = {
            "version": "1.0.0",
            "request_id": job.request_id,
            "role": job.role,
            "model": model,
            "messages": [
                {"role": "system", "content": job.system_prompt},
                {
                    "role": "user",
                    "content": json.dumps(
                        job.payload, ensure_ascii=False, sort_keys=True
                    ),
                },
            ],
            "max_tokens": job.max_tokens,
        }
        if job.temperature is not None:
            request_payload["temperature"] = job.temperature
        if job.reasoning_effort is not None:
            request_payload["reasoning_effort"] = job.reasoning_effort
        request_sha256 = _canonical_sha256(request_payload)
        cache_path = self._cache_path(job.role, model, request_sha256)
        cached = _read_json(cache_path)
        if cached is not None:
            return JSONCompletionResult(
                request_id=job.request_id,
                role=job.role,
                model=model,
                request_sha256=request_sha256,
                output=dict(cached["output"]),
                usage=dict(cached.get("usage", {})),
                cached=True,
                response_id=cached.get("response_id"),
            )

        completion = self._completion or self._load_litellm_completion()
        call_args: dict[str, Any] = {
            "model": model,
            "messages": request_payload["messages"],
            "max_completion_tokens": job.max_tokens,
            "custom_llm_provider": "openai",
            "timeout": self.config.timeout_seconds,
            "num_retries": self.config.max_retries,
        }
        if job.temperature is not None:
            call_args["temperature"] = job.temperature
        if job.reasoning_effort is not None:
            call_args["reasoning_effort"] = job.reasoning_effort
        if self.config.use_json_response_format:
            call_args["response_format"] = {"type": "json_object"}
        response = await completion(**call_args)
        usage = _response_usage(response)
        response_id = _read_value(response, "id")
        try:
            content = _response_content(response)
            output = _parse_json_object(content)
        except GatewayResponseError as exc:
            self._write_failure(
                job=job,
                model=model,
                request_sha256=request_sha256,
                response=response,
                response_id=response_id,
                usage=usage,
                error=str(exc),
            )
            raise
        artifact = {
            "version": "1.0.0",
            "created_at": datetime.now(timezone.utc).isoformat(),
            "request_id": job.request_id,
            "role": job.role,
            "model": model,
            "request_sha256": request_sha256,
            "output": output,
            "usage": usage,
            "response_id": response_id,
        }
        _write_json_atomic(cache_path, artifact)
        return JSONCompletionResult(
            request_id=job.request_id,
            role=job.role,
            model=model,
            request_sha256=request_sha256,
            output=output,
            usage=usage,
            cached=False,
            response_id=response_id,
        )

    async def complete_many(
        self, jobs: Sequence[JSONCompletionJob]
    ) -> list[JSONCompletionResult]:
        semaphore = asyncio.Semaphore(self.config.max_concurrency)

        async def run(job: JSONCompletionJob) -> JSONCompletionResult:
            async with semaphore:
                return await self.complete_json(job)

        return list(await asyncio.gather(*(run(job) for job in jobs)))

    def discard_cache(self, result: JSONCompletionResult) -> None:
        """Remove a parsed response that failed its stage-specific contract."""

        self._cache_path(
            result.role, result.model, result.request_sha256
        ).unlink(missing_ok=True)

    def _cache_path(self, role: ModelRole, model: str, digest: str) -> Path:
        safe_model = model.replace("/", "__")
        return self.config.cache_dir / role / safe_model / f"{digest}.json"

    def _write_failure(
        self,
        *,
        job: JSONCompletionJob,
        model: str,
        request_sha256: str,
        response: Any,
        response_id: str | None,
        usage: Mapping[str, int],
        error: str,
    ) -> None:
        safe_model = model.replace("/", "__")
        path = (
            self.config.cache_dir
            / "failures"
            / job.role
            / safe_model
            / f"{request_sha256}.json"
        )
        choices = _read_value(response, "choices") or []
        finish_reason = _read_value(choices[0], "finish_reason") if choices else None
        _write_json_atomic(
            path,
            {
                "version": "1.0.0",
                "created_at": datetime.now(timezone.utc).isoformat(),
                "request_id": job.request_id,
                "role": job.role,
                "model": model,
                "request_sha256": request_sha256,
                "response_id": response_id,
                "finish_reason": finish_reason,
                "usage": dict(usage),
                "error": error,
            },
        )

    def _load_litellm_completion(self) -> CompletionCallable:
        try:
            import litellm
        except ImportError as exc:
            raise GatewayConfigurationError(
                "litellm is required for execution; install the project dependencies"
            ) from exc

        os.environ.setdefault("LITELLM_LOG", "ERROR")
        litellm.api_key = self.config.api_key
        litellm.api_base = self.config.api_base
        litellm.ssl_verify = self.config.ssl_verify
        return litellm.acompletion


def write_usage_manifest(
    path: Path, results: Sequence[JSONCompletionResult]
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(
            json.dumps(result.manifest_record(), ensure_ascii=False, sort_keys=True)
            + "\n"
            for result in results
        ),
        encoding="utf-8",
    )


def _env_bool(name: str, *, default: bool) -> bool:
    value = os.environ.get(name)
    if value is None:
        return default
    normalized = value.strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    raise GatewayConfigurationError(f"{name} must be a boolean")


def _canonical_sha256(payload: Mapping[str, Any]) -> str:
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise GatewayResponseError(f"Cache artifact is not an object: {path}")
    return value


def _write_json_atomic(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def _read_value(value: Any, key: str) -> Any:
    if isinstance(value, Mapping):
        return value.get(key)
    return getattr(value, key, None)


def _response_content(response: Any) -> str:
    choices = _read_value(response, "choices") or []
    if not choices:
        raise GatewayResponseError("Gateway response has no choices")
    message = _read_value(choices[0], "message")
    content = _read_value(message, "content")
    if not isinstance(content, str) or not content.strip():
        finish_reason = _read_value(choices[0], "finish_reason")
        raise GatewayResponseError(
            f"Gateway response has no text content (finish_reason={finish_reason})"
        )
    return content


def _response_usage(response: Any) -> dict[str, int]:
    usage = _read_value(response, "usage")
    result: dict[str, int] = {}
    for key in ("prompt_tokens", "completion_tokens", "total_tokens"):
        value = _read_value(usage, key)
        if isinstance(value, int):
            result[key] = value
    completion_details = _read_value(usage, "completion_tokens_details")
    reasoning_tokens = _read_value(completion_details, "reasoning_tokens")
    if isinstance(reasoning_tokens, int):
        result["reasoning_tokens"] = reasoning_tokens
    return result


def _parse_json_object(content: str) -> dict[str, Any]:
    stripped = content.strip()
    if stripped.startswith("```"):
        lines = stripped.splitlines()
        if len(lines) >= 3 and lines[-1].strip() == "```":
            stripped = "\n".join(lines[1:-1])
    try:
        value = json.loads(stripped)
    except json.JSONDecodeError as exc:
        raise GatewayResponseError("Gateway content is not valid JSON") from exc
    if not isinstance(value, dict):
        raise GatewayResponseError("Gateway JSON response must be an object")
    return value
