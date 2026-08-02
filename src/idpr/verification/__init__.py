"""Verification helpers for derivation-conditioned outputs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from idpr.legacy.fraud_reasoning import Derivation, Fact


@dataclass(frozen=True, slots=True)
class ParagraphClaim:
    paragraph_id: str
    predicate: Fact
    evidence_id: str | None = None


@dataclass(frozen=True, slots=True)
class VerificationReport:
    sub_question_id: str
    score: float
    violations: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "sub_question_id": self.sub_question_id,
            "score": self.score,
            "violations": self.violations,
        }


def verify_claims(
    derivation: Derivation,
    claims: list[ParagraphClaim],
) -> VerificationReport:
    gated_pairs = {
        (item["evidence_id"], item["fact"]["predicate_id"], tuple(item["fact"]["args"]))
        for item in derivation.gated_out
    }
    violations: list[dict[str, Any]] = []

    for claim in claims:
        if claim.evidence_id is None:
            continue
        key = (claim.evidence_id, claim.predicate.predicate_id, claim.predicate.args)
        if key in gated_pairs:
            violations.append(
                {
                    "type": "inadmissible_use",
                    "paragraph_id": claim.paragraph_id,
                    "evidence_id": claim.evidence_id,
                    "predicate": claim.predicate.to_dict(),
                }
            )

    score = max(0.0, 1.0 - len(violations) * 0.25)
    return VerificationReport(
        sub_question_id=derivation.sub_question_id,
        score=score,
        violations=violations,
    )
