from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from idpr.rulegen import validate_norm_card_set  # noqa: E402

from scripts.run_fraud_norm_card_merge import (  # noqa: E402
    MODULE_PREFIXES,
    RUN_ROOT,
    allowed_candidates,
    build_module_payloads,
    load_merge_context,
)
from scripts.run_fraud_rulegen_critics import read_json  # noqa: E402
from scripts.run_fraud_rulegen_pilot import write_json  # noqa: E402


SOURCE_RUN_ID = "fraud_norm_cards_v2"
SOURCE_ROOT = RUN_ROOT / SOURCE_RUN_ID / "norm_cards"
OUTPUT_ROOT = PROJECT_ROOT / "data/rulegen/fraud/norm_card_sets"
MANIFEST = PROJECT_ROOT / "data/rulegen/fraud/fraud_norm_card_manifest.json"
FALLBACK_MODULES = {"deception", "special_forms"}


def candidate_source_refs(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    return [dict(ref) for ref in candidate["source_refs"]]


def is_reported_precedent(candidate: dict[str, Any]) -> bool:
    marker = " ".join(
        [
            candidate["candidate_id"],
            candidate["proposition"],
            *(ref["quote"] for ref in candidate["source_refs"]),
        ]
    )
    return any(
        token in marker
        for token in (
            "holding",
            "precedent",
            "판례",
            "판시",
            "판결",
            "대법원",
            "전원합의체",
            "원심",
            "본 사안",
            "성립한다고 본",
            "성립하지 않는다고 본",
            "보기 어렵다고 보아",
            "인정한 사례",
            "부정한 사례",
        )
    )


def candidate_authority_class(candidate: dict[str, Any]) -> str:
    if candidate["norm_kind"] == "variant":
        return "doctrine"
    if is_reported_precedent(candidate):
        return "precedent"
    return "synthesis"


def lifted_card(
    module: str,
    request_id: str,
    candidate: dict[str, Any],
) -> dict[str, Any]:
    authority_class = candidate_authority_class(candidate)
    if authority_class == "doctrine":
        formalization = "policy_variant"
        authority_basis = "commentary_reported_doctrine"
        doctrinal_status = "disputed"
        variant_group = f"pending.{candidate['candidate_id']}"
    elif authority_class == "precedent":
        formalization = "context_only"
        authority_basis = "commentary_reported_precedent"
        doctrinal_status = "precedent_position"
        variant_group = None
    elif candidate["norm_kind"] == "standard" or candidate["review_required"]:
        formalization = "standard_input"
        authority_basis = "commentary_synthesis"
        doctrinal_status = "descriptive"
        variant_group = None
    else:
        formalization = "deterministic_rule"
        authority_basis = "commentary_synthesis"
        doctrinal_status = "settled"
        variant_group = None
    return {
        "id": f"{module}.{candidate['candidate_id']}",
        "candidate_refs": [
            {"request_id": request_id, "candidate_id": candidate["candidate_id"]}
        ],
        "norm_kind": candidate["norm_kind"],
        "proposition": candidate["proposition"],
        "formalization": formalization,
        "authority_basis": authority_basis,
        "doctrinal_status": doctrinal_status,
        "polarity": candidate["polarity"],
        "source_refs": candidate_source_refs(candidate),
        "request_ids": [request_id],
        "variant_group": variant_group,
        "review_required": (
            candidate["review_required"] or authority_class == "precedent"
        ),
        "review_notes": (
            "Deterministic one-candidate lift. Authority and variant grouping "
            "remain pending human review."
        ),
    }


def exact_linked_sources(
    card: dict[str, Any],
    candidates: dict[tuple[str, str], dict[str, Any]],
) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    seen: set[tuple[str, str, str]] = set()
    for candidate_ref in card["candidate_refs"]:
        key = (candidate_ref["request_id"], candidate_ref["candidate_id"])
        for ref in candidates[key]["source_refs"]:
            source_key = (ref["comment_id"], ref["section_path"], ref["quote"])
            if source_key in seen:
                continue
            seen.add(source_key)
            refs.append(dict(ref))
    return refs


def conservative_card_normalization(
    card: dict[str, Any],
    candidates: dict[tuple[str, str], dict[str, Any]],
) -> dict[str, Any]:
    result = dict(card)
    result["source_refs"] = exact_linked_sources(result, candidates)
    linked = [
        candidates[(ref["request_id"], ref["candidate_id"])]
        for ref in result["candidate_refs"]
    ]
    norm_kinds = {candidate["norm_kind"] for candidate in linked}
    polarities = {candidate["polarity"] for candidate in linked}
    if len(norm_kinds) != 1 or len(polarities) != 1:
        raise ValueError(
            f"Mixed candidate metadata requires splitting card {result['id']}"
        )
    result["norm_kind"] = norm_kinds.pop()
    result["polarity"] = polarities.pop()
    result["review_required"] = result["review_required"] or any(
        candidate["review_required"] for candidate in linked
    )
    authority_class = candidate_authority_class(linked[0])
    if authority_class == "doctrine":
        result["formalization"] = "policy_variant"
        result["authority_basis"] = "commentary_reported_doctrine"
        result["doctrinal_status"] = "disputed"
        result["review_required"] = True
        if not result["variant_group"]:
            result["variant_group"] = f"pending.{linked[0]['candidate_id']}"
    elif authority_class == "precedent":
        result["formalization"] = "context_only"
        result["authority_basis"] = "commentary_reported_precedent"
        result["doctrinal_status"] = "precedent_position"
        result["variant_group"] = None
        result["review_required"] = True
    elif result["norm_kind"] == "standard" or result["review_required"]:
        result["formalization"] = "standard_input"
        result["authority_basis"] = "commentary_synthesis"
        result["doctrinal_status"] = "descriptive"
        result["variant_group"] = None
    else:
        result["formalization"] = "deterministic_rule"
        result["authority_basis"] = "commentary_synthesis"
        result["doctrinal_status"] = "descriptive"
        result["variant_group"] = None
    result["review_notes"] += " Conservatively normalized from linked candidates."
    return result


def build_final_card_set(
    module: str, payload: dict[str, Any]
) -> dict[str, Any]:
    candidates = allowed_candidates(payload)
    if module in FALLBACK_MODULES:
        cards = [
            lifted_card(module, request_id, candidate)
            for (request_id, _), candidate in candidates.items()
        ]
        construction = "deterministic_candidate_lift"
        coverage_gaps = [
            "API merge was rejected for silent omission or over-merge; cards are "
            "one-to-one candidate lifts pending human consolidation."
        ]
    else:
        api_output = read_json(SOURCE_ROOT / f"{module}.json")
        cards = []
        split_cards = 0
        for card in api_output["cards"]:
            linked = [
                candidates[(ref["request_id"], ref["candidate_id"])]
                for ref in card["candidate_refs"]
            ]
            if (
                len({candidate["norm_kind"] for candidate in linked}) > 1
                or len({candidate["polarity"] for candidate in linked}) > 1
                or len(
                    {candidate_authority_class(candidate) for candidate in linked}
                )
                > 1
            ):
                split_cards += 1
                cards.extend(
                    lifted_card(module, ref["request_id"], candidate)
                    for ref, candidate in zip(
                        card["candidate_refs"], linked, strict=True
                    )
                )
                continue
            cards.append(conservative_card_normalization(card, candidates))
        covered = {
            (ref["request_id"], ref["candidate_id"])
            for card in cards
            for ref in card["candidate_refs"]
        }
        cards.extend(
            lifted_card(module, request_id, candidate)
            for (request_id, candidate_id), candidate in candidates.items()
            if (request_id, candidate_id) not in covered
        )
        construction = "api_merged"
        coverage_gaps = list(api_output["coverage_gaps"])
        if len(covered) < len(candidates):
            coverage_gaps.append(
                "Candidates omitted by the API merge were restored as one-to-one cards."
            )
        if split_cards:
            coverage_gaps.append(
                f"Split {split_cards} API cards that merged different norm kinds, "
                "polarities, or authority classes into one-to-one candidate cards."
            )

    return {
        "version": "1.1.0",
        "card_set_id": payload["card_set_id"],
        "issue_tag": payload["issue_tag"],
        "status": "draft",
        "legal_review": "pending",
        "construction": construction,
        "source_scope": {
            "target_paths": payload["target_paths"],
            "comment_ids": payload["allowed_comment_ids"],
        },
        "cards": cards,
        "legal_review_questions": payload["unresolved_questions"],
        "coverage_gaps": coverage_gaps,
    }


def main() -> None:
    payloads = build_module_payloads()
    requests, _, _ = load_merge_context()
    commentary_by_id = {
        row["comment_id"]: row
        for request in requests
        for row in request["commentary_chunks"]
    }
    request_comment_ids = {
        request["request_id"]: {
            row["comment_id"] for row in request["commentary_chunks"]
        }
        for request in requests
    }
    modules: list[dict[str, Any]] = []
    totals = Counter()
    for module in MODULE_PREFIXES:
        payload = payloads[module]
        card_set = build_final_card_set(module, payload)
        candidates = allowed_candidates(payload)
        validate_norm_card_set(
            card_set,
            commentary_by_id,
            request_comment_ids,
            allowed_candidates=candidates,
        )
        output_path = OUTPUT_ROOT / f"{module}.json"
        write_json(output_path, card_set)
        formalizations = Counter(
            card["formalization"] for card in card_set["cards"]
        )
        modules.append(
            {
                "module": module,
                "path": str(output_path.relative_to(PROJECT_ROOT)),
                "construction": card_set["construction"],
                "candidates": len(candidates),
                "cards": len(card_set["cards"]),
                "formalizations": dict(sorted(formalizations.items())),
            }
        )
        totals["candidates"] += len(candidates)
        totals["cards"] += len(card_set["cards"])
    manifest = {
        "version": "1.0.0",
        "issue_tag": "fraud",
        "status": "draft",
        "legal_review": "pending",
        "source_run_id": SOURCE_RUN_ID,
        "fallback_modules": sorted(FALLBACK_MODULES),
        "modules": modules,
        "totals": dict(totals),
    }
    write_json(MANIFEST, manifest)
    print(json.dumps(manifest["totals"], ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
