from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from idpr.rulegen import (  # noqa: E402
    repair_ocr_interrupted_candidate_quotes,
    validate_norm_candidate_batch,
)


REQUESTS = PROJECT_ROOT / "data/rulegen/fraud/fraud_rulegen_requests.jsonl"
FIRST_BATCH = (
    PROJECT_ROOT
    / "data/rulegen/fraud/fraud_norm_candidate_batch_pass1_001_exemplar.json"
)
RUN_A = PROJECT_ROOT / ".cache/llm/runs/fraud_rulegen/fraud_full_terra_v1a/terra"
RUN_B = PROJECT_ROOT / ".cache/llm/runs/fraud_rulegen/fraud_full_terra_v1b/terra"
PATCHED = (
    PROJECT_ROOT
    / ".cache/llm/runs/fraud_rulegen_patches/fraud_full_patches_v1/candidates"
)
FINAL_PATCHED = (
    PROJECT_ROOT
    / ".cache/llm/runs/fraud_rulegen_patches/fraud_final_risk_patches_v1/candidates"
)
CRITIC_PASS1 = (
    PROJECT_ROOT
    / ".cache/llm/runs/fraud_rulegen_critics/fraud_full_critics_v1/sol"
)
PATCH_PASS1 = (
    PROJECT_ROOT
    / ".cache/llm/runs/fraud_rulegen_patches/fraud_full_patches_v1/patch"
)
CRITIC_PASS2 = (
    PROJECT_ROOT
    / ".cache/llm/runs/fraud_rulegen_critics/fraud_final_risk_critics_v1/sol"
)
PATCH_PASS2 = (
    PROJECT_ROOT
    / ".cache/llm/runs/fraud_rulegen_patches/fraud_final_risk_patches_v1/patch"
)
OUTPUT_ROOT = PROJECT_ROOT / "data/rulegen/fraud/norm_candidate_batches"
REVIEW_ROOT = PROJECT_ROOT / "data/rulegen/fraud/norm_candidate_reviews"
MANIFEST = PROJECT_ROOT / "data/rulegen/fraud/fraud_norm_candidate_manifest.json"


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return value


def load_requests() -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in REQUESTS.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def source_path(batch_number: int, request_id: str) -> Path:
    if batch_number == 1:
        return FIRST_BATCH
    final_patched = FINAL_PATCHED / f"{request_id}.json"
    if final_patched.exists():
        return final_patched
    patched = PATCHED / f"{request_id}.json"
    if patched.exists():
        return patched
    root = RUN_A if batch_number <= 7 else RUN_B
    return root / f"{request_id}.json"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> None:
    requests = load_requests()
    manifest_batches: list[dict[str, Any]] = []
    candidate_locations: dict[str, list[str]] = defaultdict(list)
    totals = Counter()

    for batch_number, request in enumerate(requests, start=1):
        request_id = request["request_id"]
        source = source_path(batch_number, request_id)
        payload = read_json(source)
        commentary = {
            row["comment_id"]: row for row in request["commentary_chunks"]
        }
        repaired, repairs = repair_ocr_interrupted_candidate_quotes(
            payload, commentary
        )
        validate_norm_candidate_batch(repaired, request)

        output_path = OUTPUT_ROOT / f"{request_id}.json"
        write_json(output_path, repaired)
        review_artifacts: dict[str, str] = {}
        if batch_number == 1:
            review_artifacts["final_adjudication"] = (
                "data/rulegen/fraud/"
                "fraud_pass1_001_revision6_final_adjudication.json"
            )
        else:
            for label, review_source in (
                ("critic_pass1", CRITIC_PASS1 / f"{request_id}.critic.json"),
                ("patch_pass1", PATCH_PASS1 / f"{request_id}.json"),
                ("critic_pass2", CRITIC_PASS2 / f"{request_id}.critic.json"),
                ("patch_pass2", PATCH_PASS2 / f"{request_id}.json"),
            ):
                if not review_source.exists():
                    continue
                review_path = REVIEW_ROOT / label / review_source.name
                write_json(review_path, read_json(review_source))
                review_artifacts[label] = str(
                    review_path.relative_to(PROJECT_ROOT)
                )
        encoded = output_path.read_bytes()
        polarity = Counter(
            candidate["polarity"] for candidate in repaired["candidates"]
        )
        for candidate in repaired["candidates"]:
            candidate_locations[candidate["candidate_id"]].append(request_id)
        totals["candidates"] += len(repaired["candidates"])
        totals["unresolved_questions"] += len(repaired["unresolved_questions"])
        totals["provenance_repairs"] += len(repairs)
        manifest_batches.append(
            {
                "batch_number": batch_number,
                "request_id": request_id,
                "generation_source": str(source.relative_to(PROJECT_ROOT)),
                "path": str(output_path.relative_to(PROJECT_ROOT)),
                "review_artifacts": review_artifacts,
                "sha256": hashlib.sha256(encoded).hexdigest(),
                "candidates": len(repaired["candidates"]),
                "unresolved_questions": len(repaired["unresolved_questions"]),
                "polarity": dict(sorted(polarity.items())),
                "provenance_repairs": len(repairs),
            }
        )

    duplicate_ids = {
        candidate_id: locations
        for candidate_id, locations in sorted(candidate_locations.items())
        if len(locations) > 1
    }
    manifest = {
        "version": "1.0.0",
        "issue_tag": "fraud",
        "status": "draft",
        "legal_review": "pending",
        "batches": manifest_batches,
        "totals": dict(totals),
        "unique_candidate_ids": len(candidate_locations),
        "duplicate_candidate_ids": duplicate_ids,
        "notes": [
            "Duplicate candidate IDs are retained as cross-batch merge inputs.",
            "All source quotes passed local exact-substring provenance validation.",
        ],
    }
    write_json(MANIFEST, manifest)
    print(json.dumps(manifest["totals"], ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
