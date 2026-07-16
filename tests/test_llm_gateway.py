from __future__ import annotations

import asyncio
import json
from pathlib import Path

import pytest

from idpr.llm import (
    GatewayConfig,
    GatewayConfigurationError,
    GatewayResponseError,
    JSONCompletionJob,
    LLMGateway,
    write_usage_manifest,
)
from scripts.run_fraud_rulegen_pilot import build_extraction_jobs
from scripts.run_fraud_rulegen_correction import (
    build_final_critic_job,
    build_revision_job,
)


def config(tmp_path: Path) -> GatewayConfig:
    return GatewayConfig(
        api_key="secret-key",
        terra_model="terra-model",
        sol_model="openai/sol-model",
        cache_dir=tmp_path / "cache",
    )


def test_gateway_config_requires_explicit_models_and_hides_key(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("SKIML_API_KEY", "secret-key")
    monkeypatch.delenv("IDPR_TERRA_MODEL", raising=False)
    monkeypatch.delenv("IDPR_SOL_MODEL", raising=False)

    with pytest.raises(GatewayConfigurationError, match="IDPR_TERRA_MODEL"):
        GatewayConfig.from_env()

    value = config(Path(".cache-test"))
    assert "secret-key" not in repr(value)
    assert value.model_for_role("terra") == "openai/terra-model"
    assert value.model_for_role("sol") == "openai/sol-model"


def test_gateway_caches_successful_json_and_records_usage(tmp_path: Path) -> None:
    calls: list[dict] = []

    async def fake_completion(**kwargs: object) -> dict:
        calls.append(dict(kwargs))
        return {
            "id": "response-001",
            "choices": [
                {
                    "message": {
                        "content": '```json\n{"status":"draft","value":1}\n```'
                    }
                }
            ],
            "usage": {
                "prompt_tokens": 100,
                "completion_tokens": 20,
                "total_tokens": 120,
            },
        }

    gateway = LLMGateway(config(tmp_path), completion=fake_completion)
    job = JSONCompletionJob(
        request_id="request-001",
        role="terra",
        system_prompt="Return JSON only.",
        payload={"input": "value"},
    )
    first = asyncio.run(gateway.complete_json(job))
    second = asyncio.run(gateway.complete_json(job))

    assert first.output == {"status": "draft", "value": 1}
    assert first.usage["total_tokens"] == 120
    assert not first.cached
    assert second.cached
    assert len(calls) == 1
    assert calls[0]["model"] == "openai/terra-model"
    assert "api_key" not in calls[0]
    assert "temperature" not in calls[0]
    assert calls[0]["max_completion_tokens"] == 6_000
    assert "max_tokens" not in calls[0]

    manifest = tmp_path / "manifest.jsonl"
    write_usage_manifest(manifest, [first, second])
    records = [json.loads(line) for line in manifest.read_text().splitlines()]
    assert records[0]["request_sha256"] == records[1]["request_sha256"]
    assert records[1]["cached"]
    assert "secret-key" not in manifest.read_text()


def test_gateway_rejects_non_json_without_caching(tmp_path: Path) -> None:
    async def fake_completion(**_: object) -> dict:
        return {"choices": [{"message": {"content": "not json"}}]}

    gateway = LLMGateway(config(tmp_path), completion=fake_completion)
    job = JSONCompletionJob(
        request_id="request-invalid",
        role="sol",
        system_prompt="Return JSON only.",
        payload={"input": "value"},
    )
    with pytest.raises(GatewayResponseError, match="not valid JSON"):
        asyncio.run(gateway.complete_json(job))
    assert not list((tmp_path / "cache" / "sol").rglob("*.json"))
    assert len(list((tmp_path / "cache" / "failures").rglob("*.json"))) == 1


def test_gateway_records_usage_when_reasoning_exhausts_output(
    tmp_path: Path,
) -> None:
    async def fake_completion(**kwargs: object) -> dict:
        assert kwargs["reasoning_effort"] == "low"
        return {
            "id": "response-empty",
            "choices": [
                {
                    "finish_reason": "length",
                    "message": {"content": None, "reasoning_content": "hidden"},
                }
            ],
            "usage": {
                "prompt_tokens": 200,
                "completion_tokens": 3_000,
                "total_tokens": 3_200,
                "completion_tokens_details": {"reasoning_tokens": 3_000},
            },
        }

    gateway = LLMGateway(config(tmp_path), completion=fake_completion)
    job = JSONCompletionJob(
        request_id="request-reasoning-limit",
        role="sol",
        system_prompt="Return JSON only.",
        payload={"input": "value"},
        max_tokens=3_000,
        reasoning_effort="low",
    )
    with pytest.raises(GatewayResponseError, match="finish_reason=length"):
        asyncio.run(gateway.complete_json(job))

    failures = list((tmp_path / "cache" / "failures").rglob("*.json"))
    assert len(failures) == 1
    failure = json.loads(failures[0].read_text())
    assert failure["finish_reason"] == "length"
    assert failure["usage"]["reasoning_tokens"] == 3_000
    assert "hidden" not in failures[0].read_text()


def test_pilot_prompt_includes_exact_output_schema() -> None:
    request = {
        "request_id": "fraud.article347.pass1.001",
        "commentary_chunks": [],
    }
    job = build_extraction_jobs([request], max_tokens=100)[0]

    assert '"$id": "idpr/NormCandidateBatch"' in job.system_prompt
    assert "Exact output JSON Schema" in job.system_prompt


def test_correction_jobs_keep_revision_and_critic_roles_separate() -> None:
    request = {
        "request_id": "fraud.article347.pass1.001",
        "commentary_chunks": [],
    }
    target = {"request_id": request["request_id"], "candidates": []}
    critique = {"report_id": "fraud.review"}

    revision = build_revision_job(
        request, target, [critique], max_tokens=123, revision_label="revision2"
    )
    critic = build_final_critic_job(
        request, target, revision.request_id, max_tokens=456
    )

    assert revision.role == "terra"
    assert revision.request_id.endswith(".revision2")
    assert revision.payload["critique_reports"] == [critique]
    assert '"$id": "idpr/NormCandidateBatch"' in revision.system_prompt
    assert critic.role == "sol"
    assert critic.request_id.endswith(".revision2.critic")
    assert critic.payload["target_id"] == revision.request_id
    assert critic.reasoning_effort == "low"
