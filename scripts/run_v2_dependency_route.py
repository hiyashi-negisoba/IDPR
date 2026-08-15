"""Dependency ROUTE invocation: offense candidates for a bound linked participant.

This is not a new pipeline stage and not an Article 151 special case.  It is the same ROUTE
operation Call 1 performs, invoked a second time once Call 1.5 has bound the participant whose
own legal outcome an authored rule requires.  The only differences are who is routed and which
text bounds the scope.

Reading the plan rather than the case text is deliberate: the participant, the offense that needs
the dependency, and the factual scope were all decided upstream and are carried in
`linked_offender_dependencies`.  Re-deriving any of them here would put a second, quieter copy of
those decisions in the one place nobody audits.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.eval.input_formatter import assert_no_leaked_fields  # noqa: E402
from idpr.neural.vllm_client import VLLMClient  # noqa: E402
from idpr.prompts import load_prompt, prompt_path  # noqa: E402
from idpr.v2.registry import load_definitions  # noqa: E402
from idpr.v2.routing import (  # noqa: E402
    LINKED_OFFENDER_ROUTING,
    RouteRequest,
    RouterContractError,
    normalize_router_seeds,
    route_request_payload,
    router_catalog,
    router_schema,
    validate_router_output,
)
from idpr.v2.runtime.identity import FactualParticipantKey, OffenseInstanceKey  # noqa: E402
from idpr.v2.runtime.linked_offender import (  # noqa: E402
    LinkedOffenderDependency,
    gate_predecessor_candidates,
    linked_offender_predicate_targets,
)

# 이 스크립트는 후보를 여는 데까지만 간다. 신분 계산은 Call 2가 그 predicate를 답한 뒤
# `article151_predecessor_status()`가 하고, 그 결과는 `article151_status_truths()`가
# dependent instance의 predicate truth로 공급한다 -- 별도 Scallop parity path는 없다.

PROMPTS = ("v2_call1_router", "v2_call1_router_dependency_user")


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _dependency(value: dict[str, Any]) -> LinkedOffenderDependency:
    instance = value["dependent_instance_key"]
    participant = value["participant"]
    return LinkedOffenderDependency(
        OffenseInstanceKey(
            str(instance["case_id"]),
            str(instance["actor_id"]),
            str(instance["offense_ref"]),
            str(instance["occurrence_id"]),
        ),
        FactualParticipantKey(str(participant["case_id"]), str(participant["participant_id"])),
        str(value["role"]),
        str(value["resolved_element"]),
        str(value["factual_scope_text"]),
        str(value.get("provenance_text", "")),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--api-key", default="local-idpr")
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--inventory", type=Path, required=True)
    parser.add_argument("--definitions", type=Path, default=ROOT / "data/v2/definitions")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-tokens", type=int, default=512)
    args = parser.parse_args()

    registry = load_definitions(args.definitions)
    catalog = router_catalog(registry)
    schema = router_schema(catalog)
    case_text_by_id = {
        str(row["sub_question_id"]): str(row["question_text"]) for row in _jsonl(args.inventory)
    }
    system_prompt, user_prompt = (load_prompt(name) for name in PROMPTS)
    client = VLLMClient(base_url=args.base_url, model=args.model, api_key=args.api_key)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.with_suffix(".manifest.json").write_text(
        json.dumps(
            {
                "step": "v2_dependency_route",
                "routing_basis": LINKED_OFFENDER_ROUTING,
                "plan": str(args.plan),
                "plan_sha256": _sha256(args.plan),
                "definitions_dir": str(args.definitions),
                "prompts": {name: _sha256(prompt_path(name)) for name in PROMPTS},
                "model": args.model,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    rows: list[dict[str, Any]] = []
    for plan_row in _jsonl(args.plan):
        case_id = str(plan_row["sub_question_id"])
        for value in plan_row.get("linked_offender_dependencies", []):
            dependency = _dependency(value)
            payload = route_request_payload(
                dependency.route_request(),
                case_text=case_text_by_id[case_id],
                catalog=catalog,
            )
            # 이 호출에는 질문이 실리지 않는다. 실리면 범위가 질문받은 행위자로 끌려간다.
            assert "question_prompt" not in payload
            assert_no_leaked_fields(payload)
            row: dict[str, Any] = {
                "sub_question_id": case_id,
                **dependency.as_dict(),
            }
            try:
                output, metadata = client.complete_json(
                    system_prompt=system_prompt,
                    user_template=user_prompt,
                    payload=payload,
                    schema_name="v2_dependency_route",
                    schema=schema,
                    max_tokens=args.max_tokens,
                    temperature=0.0,
                    seed=1,
                )
                seeds = validate_router_output(output, catalog=catalog)
                normalization = normalize_router_seeds(seeds)
                gate = gate_predecessor_candidates(
                    registry, dependency, normalization.normalized_seeds
                )
                row.update(
                    {
                        "status": "SUCCEEDED",
                        "raw_seeds": list(seeds),
                        **{
                            key: value
                            for key, value in gate.as_dict().items()
                            if key.endswith("offense_refs")
                        },
                        "predicate_targets": [
                            target.as_dict()
                            for target in linked_offender_predicate_targets(registry, gate)
                        ],
                        "usage": metadata.get("usage", {}),
                    }
                )
            except (RouterContractError, ValueError) as error:
                # 실패를 후보 없음으로 접지 않는다. 후보 없음은 결정론적 부정으로 읽히지만
                # 계약 실패는 미확정이고, 둘을 합치면 제151조가 조용히 불성립으로 간다.
                row.update({"status": "CONTRACT_FAILED", "error": str(error)})
            rows.append(row)

    args.out.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows), encoding="utf-8"
    )
    print(f"dependency route rows: {len(rows)} -> {args.out}")


if __name__ == "__main__":
    main()
