"""Legacy deterministic fraud bootstrap retained for golden-test reproduction.

The implementation is intentionally small and pure Python. It mirrors the
project contract for evidence gating and fraud golden cases while leaving the
historical contract that preceded the general Scallop runtime.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

Conclusion = Literal["established", "not_established", "admissible", "inadmissible"]


@dataclass(frozen=True, slots=True)
class Fact:
    predicate_id: str
    args: tuple[str, ...]

    def __init__(self, predicate_id: str, args: tuple[str, ...] | list[str]) -> None:
        object.__setattr__(self, "predicate_id", predicate_id)
        object.__setattr__(self, "args", tuple(args))

    def to_dict(self) -> dict[str, Any]:
        return {"predicate_id": self.predicate_id, "args": list(self.args)}


@dataclass(frozen=True, slots=True)
class Evidence:
    evidence_id: str
    supports: list[Fact] = field(default_factory=list)
    hearsay: bool = False
    hearsay_exception_met: bool = False
    illegally_obtained: bool = False
    violation_substantial: bool = False


@dataclass(frozen=True, slots=True)
class StandardJudgment:
    predicate_id: str
    args: tuple[str, ...]
    value: bool
    rationale: str

    def __init__(
        self,
        predicate_id: str,
        args: tuple[str, ...] | list[str],
        value: bool,
        rationale: str,
    ) -> None:
        object.__setattr__(self, "predicate_id", predicate_id)
        object.__setattr__(self, "args", tuple(args))
        object.__setattr__(self, "value", value)
        object.__setattr__(self, "rationale", rationale)

    def to_flag(self) -> dict[str, Any]:
        return {
            "predicate_id": self.predicate_id,
            "args": list(self.args),
            "llm_judgment": self.value,
            "rationale": self.rationale,
        }


@dataclass(frozen=True, slots=True)
class FraudInputs:
    sub_question_id: str
    defendant: str
    victim: str
    property_id: str
    evidence: list[Evidence] = field(default_factory=list)
    standards: list[StandardJudgment] = field(default_factory=list)


@dataclass(frozen=True, slots=True)
class Derivation:
    sub_question_id: str
    verdicts: list[dict[str, str]]
    proof_tree: dict[str, Any]
    fired_rules: list[str]
    gated_out: list[dict[str, Any]]
    standard_flags: list[dict[str, Any]]
    provable_facts: tuple[Fact, ...] = ()

    def conclusion_for(self, issue: str) -> str | None:
        for verdict in self.verdicts:
            if verdict["issue"] == issue:
                return verdict["conclusion"]
        return None

    def to_dict(self) -> dict[str, Any]:
        return {
            "sub_question_id": self.sub_question_id,
            "verdicts": self.verdicts,
            "proof_tree": self.proof_tree,
            "fired_rules": self.fired_rules,
            "gated_out": self.gated_out,
            "standard_flags": self.standard_flags,
        }


def derive_fraud(inputs: FraudInputs) -> Derivation:
    provable_facts: set[Fact] = set()
    gated_out: list[dict[str, Any]] = []

    for evidence in inputs.evidence:
        exclusion_reason = _exclusion_reason(evidence)
        if exclusion_reason is None:
            provable_facts.update(evidence.supports)
            continue

        for fact in evidence.supports:
            gated_out.append(
                {
                    "evidence_id": evidence.evidence_id,
                    "fact": fact.to_dict(),
                    "reason": exclusion_reason,
                }
            )

    required = {
        "deception": Fact("deception", (inputs.defendant, inputs.victim)),
        "mistake_caused": Fact("mistake_caused", (inputs.victim,)),
        "disposition_by_deceived": Fact(
            "disposition_by_deceived",
            (inputs.victim, inputs.property_id),
        ),
    }
    intent = _standard_true(
        inputs.standards,
        "intent_to_defraud",
        (inputs.defendant,),
    )
    established = all(fact in provable_facts for fact in required.values()) and intent

    proof_tree = {
        "fraud_established": {
            "required": {name: fact.to_dict() for name, fact in required.items()},
            "intent_to_defraud": intent,
            "gated_out_count": len(gated_out),
        }
    }
    fired_rules = ["admissible", "provable"]
    fired_rules.append("fraud_established" if established else "fraud_not_established")

    return Derivation(
        sub_question_id=inputs.sub_question_id,
        verdicts=[
            {
                "issue": "fraud_established",
                "conclusion": "established" if established else "not_established",
            }
        ],
        proof_tree=proof_tree,
        fired_rules=fired_rules,
        gated_out=gated_out,
        standard_flags=[judgment.to_flag() for judgment in inputs.standards],
        provable_facts=tuple(
            sorted(provable_facts, key=lambda fact: fact.to_dict()["predicate_id"])
        ),
    )


def _standard_true(
    judgments: list[StandardJudgment],
    predicate_id: str,
    args: tuple[str, ...],
) -> bool:
    return any(
        judgment.predicate_id == predicate_id and judgment.args == args and judgment.value
        for judgment in judgments
    )


def _exclusion_reason(evidence: Evidence) -> str | None:
    if evidence.illegally_obtained and evidence.violation_substantial:
        return "excluded_illegal"
    if evidence.hearsay and not evidence.hearsay_exception_met:
        return "excluded_hearsay"
    return None
