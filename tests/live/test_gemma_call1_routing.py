from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from idpr.neural.vllm_client import VLLMClient
from idpr.prompts import load_prompt
from idpr.v2.registry import load_definitions
from idpr.v2.routing import (
    normalize_router_seeds,
    router_catalog,
    router_request_payload,
    router_schema,
    validate_router_output,
)

ROOT = Path(__file__).resolve().parents[2]


@pytest.mark.parametrize(
    ("case_id", "required"),
    (
        ("kcl_criminal_r10_p1_q1_ga", {"offense.rape"}),
        (
            "kcl_criminal_r10_p1_q3_ga",
            {
                "offense.bribe_delivery_receipt",
                "offense.bribe_giving",
                "offense.bribery_taking",
                "offense.dereliction_of_duty",
                "offense.embezzlement",
                "offense.harboring_or_escape",
            },
        ),
    ),
)
def test_real_gemma_routes_only_the_asked_subquestion_with_closed_ids(
    case_id: str, required: set[str]
) -> None:
    base_url = os.environ.get("IDPR_VLLM_BASE_URL")
    model = os.environ.get("IDPR_VLLM_MODEL")
    if not base_url or not model:
        pytest.skip("live Gemma endpoint not explicitly supplied")
    case = next(
        json.loads(line)
        for line in (ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl")
        .read_text(encoding="utf-8")
        .splitlines()
        if json.loads(line)["sub_question_id"] == case_id
    )
    registry = load_definitions(ROOT / "data/v2/definitions")
    catalog = router_catalog(registry)
    raw, metadata = VLLMClient(base_url, model).complete_json(
        system_prompt=load_prompt("v2_call1_router"),
        user_template=load_prompt("v2_call1_router_user"),
        payload=router_request_payload(
            question_prompt=case["question_prompt"],
            case_text=case["question_text"],
            catalog=catalog,
        ),
        schema_name="v2_call1_routing_gate",
        schema=router_schema(catalog),
        max_tokens=1024,
        temperature=0.0,
        seed=17,
    )
    normalized = normalize_router_seeds(validate_router_output(raw, catalog=catalog))
    assert metadata.get("finish_reason") == "stop"
    assert required <= set(normalized.normalized_seeds), raw
    assert 1 <= len(normalized.normalized_seeds) <= 10
