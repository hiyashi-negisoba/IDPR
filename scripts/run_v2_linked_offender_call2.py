"""Participant-level Call 2 for a linked offender, folded into the Article 151 status.

The dependency ROUTE step chose which predecessor offenses to look at and the authored threshold
already dropped the ones that cannot qualify.  This asks the remaining predicates about the linked
person and folds the answers into one status per candidate.

It enriches the Call 2 artifact rather than writing a parallel one.  The symbolic runner reads
`article151_status_truths` off the row it already iterates, so a separate file would need a merge
step whose only job is to put the value back where it was going anyway.

What this deliberately does not do: create an `OffenseInstanceKey` for the linked person, or write
anything resembling a liability conclusion about them.  The question asks about the harbourer.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from idpr.eval.input_formatter import assert_no_leaked_fields  # noqa: E402
from idpr.neural.vllm_client import VLLMClient  # noqa: E402
from idpr.prompts import load_prompt  # noqa: E402
from idpr.v2.registry import load_definitions  # noqa: E402
from idpr.v2.runtime.identity import FactualParticipantKey, OffenseInstanceKey  # noqa: E402
from idpr.v2.runtime.linked_offender import (  # noqa: E402
    LinkedOffenderDependency,
    LinkedOffenderPredicateTarget,
    article151_predecessor_status,
    article151_status_truths,
    linked_offender_request_payload,
)
from idpr.v2.runtime.utilized_participant_outcome import (  # noqa: E402
    utilized_participant_schema,
    validate_utilized_participant_output,
)

# 이미 승인된 participant assessor를 그대로 쓴다. 묻는 일이 같기 때문이다 -- 한 사람과 하나의
# exact offense에 대해 predicate 각각의 truth. 새 프롬프트를 만들면 같은 질문에 두 문안이
# 생기고, 둘이 갈라지는 날 어느 쪽이 맞는지 아무도 모른다.
PROMPTS = ("v2_call2_utilized_participant_outcome", "v2_call2_utilized_participant_outcome_user")


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


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
    parser.add_argument("--dependency-route", type=Path, required=True)
    parser.add_argument("--call2", type=Path, required=True)
    parser.add_argument("--definitions", type=Path, default=ROOT / "data/v2/definitions")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--max-tokens", type=int, default=1024)
    args = parser.parse_args()

    registry = load_definitions(args.definitions)
    system_prompt, user_prompt = (load_prompt(name) for name in PROMPTS)
    client = VLLMClient(base_url=args.base_url, model=args.model, api_key=args.api_key)

    truths_by_case: dict[str, list[dict[str, Any]]] = {}
    records: list[dict[str, Any]] = []
    for row in _jsonl(args.dependency_route):
        case_id = str(row["sub_question_id"])
        if row.get("status") != "SUCCEEDED":
            # 계약 실패도, 귀속되는 사실이 없는 것도 "자격 있는 선행범죄가 없다"가 아니다.
            # 둘 다 미확정으로 두되 상태는 구분해 기록한다 -- 하나는 고칠 결함이고 다른
            # 하나는 사건이 그렇게 생긴 것이다.
            records.append({"sub_question_id": case_id, "status": row.get("status")})
            continue
        dependency = _dependency(row)
        targets_by_offense: dict[str, list[LinkedOffenderPredicateTarget]] = {}
        for value in row.get("predicate_targets", []):
            participant = value["participant"]
            target = LinkedOffenderPredicateTarget(
                FactualParticipantKey(
                    str(participant["case_id"]), str(participant["participant_id"])
                ),
                str(value["offense_ref"]),
                str(value["predicate_ref"]),
            )
            targets_by_offense.setdefault(target.offense_ref, []).append(target)

        statuses = []
        for offense_ref, targets in sorted(targets_by_offense.items()):
            payload = linked_offender_request_payload(
                registry,
                participant_evidence={
                    "participant_label": dependency.participant.participant_id,
                    # 이 사람에게 귀속되는 사실만. dependency를 연 은닉·도피 증거는
                    # provenance이지 이 판단의 재료가 아니다.
                    "source_text": dependency.factual_scope_text,
                },
                offense_ref=offense_ref,
                predicate_targets=targets,
            )
            assert_no_leaked_fields(payload)
            raw, _metadata = client.complete_json(
                system_prompt=system_prompt,
                user_template=user_prompt,
                payload=payload,
                schema_name="v2_linked_offender_predicate_call2",
                schema=utilized_participant_schema(targets),
                max_tokens=args.max_tokens,
                temperature=0.0,
                seed=1,
            )
            assessed = validate_utilized_participant_output(raw, predicate_targets=targets)
            status = article151_predecessor_status(
                registry,
                participant=dependency.participant,
                offense_ref=offense_ref,
                predicate_truths={
                    value.target.predicate_ref: value.truth for value in assessed
                },
            )
            statuses.append(status)
            records.append(
                {
                    "sub_question_id": case_id,
                    "participant_id": dependency.participant.participant_id,
                    "offense_ref": offense_ref,
                    "assessments": [
                        {"predicate_ref": value.target.predicate_ref, "truth": value.truth}
                        for value in assessed
                    ],
                    "status": status.status,
                }
            )

        for (instance, ref), truth in article151_status_truths(
            registry, ((dependency, status) for status in statuses)
        ).items():
            truths_by_case.setdefault(case_id, []).append(
                {
                    "dependent_instance_key": {
                        "case_id": instance.case_id,
                        "actor_id": instance.actor_id,
                        "offense_ref": instance.offense_ref,
                        "occurrence_id": instance.occurrence_id,
                    },
                    "resolved_element": ref,
                    "truth": truth,
                }
            )

    enriched = []
    for row in _jsonl(args.call2):
        case_id = str(row["sub_question_id"])
        if case_id in truths_by_case:
            row = {**row, "article151_status_truths": truths_by_case[case_id]}
        enriched.append(row)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in enriched), encoding="utf-8"
    )
    args.out.with_suffix(".assessments.jsonl").write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in records), encoding="utf-8"
    )
    print(
        f"linked offender status rows: {len(records)} · enriched cases: {len(truths_by_case)}"
        f" -> {args.out}"
    )


if __name__ == "__main__":
    main()
