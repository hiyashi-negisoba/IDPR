from __future__ import annotations

import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_project_scaffold_matches_initialization_contract() -> None:
    required_paths = [
        "README.md",
        "PROJECT_INIT.md",
        "pyproject.toml",
        ".env.example",
        "configs/pipeline.yaml",
        "data/README.md",
        "docs/contracts/predicate_instance.schema.json",
        "docs/contracts/derivation.schema.json",
        "docs/contracts/inventory_item.schema.json",
        "docs/contracts/verification_report.schema.json",
        "docs/contracts/rulegen_request.schema.json",
        "docs/contracts/norm_candidate_batch.schema.json",
        "docs/contracts/rule_ir.schema.json",
        "rules/schema/predicates.yaml",
        "rules/kr/gates.scl",
        "rules/kr/substantive/fraud.scl",
        "rules/kr/procedural/hearsay.scl",
        "rules/exemplars/fraud_v1_candidate.scl",
        "rules/exemplars/procedural_gate_v1_candidate.scl",
        "src/idpr/extraction/__init__.py",
        "src/idpr/reasoning/__init__.py",
        "src/idpr/generation/__init__.py",
        "src/idpr/verification/__init__.py",
        "src/idpr/refine/__init__.py",
        "src/idpr/rulegen/__init__.py",
        "src/idpr/llm/__init__.py",
        "src/idpr/eval/__init__.py",
    ]

    missing = [path for path in required_paths if not (PROJECT_ROOT / path).exists()]
    assert missing == []


def test_contract_schemas_are_loadable_and_expose_stage_boundaries() -> None:
    contracts = PROJECT_ROOT / "docs" / "contracts"
    expected_required = {
        "predicate_instance.schema.json": {
            "predicate_id",
            "args",
            "confidence",
            "evidence_span",
        },
        "derivation.schema.json": {
            "sub_question_id",
            "verdicts",
            "proof_tree",
            "fired_rules",
            "gated_out",
            "standard_flags",
        },
        "verification_report.schema.json": {
            "sub_question_id",
            "score",
            "violations",
        },
        "inventory_item.schema.json": {
            "sub_question_id",
            "source",
            "question_text",
            "issue_tags",
            "covered",
            "review_status",
            "coverage_review_status",
        },
        "rulegen_request.schema.json": {
            "request_id",
            "task",
            "issue_tag",
            "target",
            "batch",
            "commentary_chunks",
            "constraints",
        },
        "norm_candidate_batch.schema.json": {
            "request_id",
            "status",
            "candidates",
            "unresolved_questions",
        },
        "rule_ir.schema.json": {
            "version",
            "rule_set_id",
            "issue_tag",
            "status",
            "legal_review",
            "source_scope",
            "predicates",
            "rules",
            "legal_review_questions",
            "coverage_gaps",
        },
    }

    for filename, required_fields in expected_required.items():
        schema = json.loads((contracts / filename).read_text(encoding="utf-8"))
        assert schema["type"] == "object"
        assert required_fields.issubset(set(schema["required"]))


def test_fraud_rule_golden_cases_and_evidence_gating() -> None:
    from idpr.legacy.fraud_reasoning import (
        Evidence,
        Fact,
        FraudInputs,
        StandardJudgment,
        derive_fraud,
    )

    admissible_core = Evidence(
        evidence_id="E1",
        supports=[
            Fact("deception", ("D", "V")),
            Fact("mistake_caused", ("V",)),
            Fact("disposition_by_deceived", ("V", "P")),
        ],
    )

    established = derive_fraud(
        FraudInputs(
            sub_question_id="fraud-established",
            defendant="D",
            victim="V",
            property_id="P",
            evidence=[admissible_core],
            standards=[StandardJudgment("intent_to_defraud", ("D",), True, "bootstrap")],
        )
    )
    assert established.conclusion_for("fraud_established") == "established"
    assert established.gated_out == []
    assert "fraud_established" in established.fired_rules

    missing_intent = derive_fraud(
        FraudInputs(
            sub_question_id="fraud-missing-intent",
            defendant="D",
            victim="V",
            property_id="P",
            evidence=[admissible_core],
            standards=[],
        )
    )
    assert missing_intent.conclusion_for("fraud_established") == "not_established"

    inadmissible_deception = Evidence(
        evidence_id="E2",
        hearsay=True,
        hearsay_exception_met=False,
        supports=[Fact("deception", ("D", "V"))],
    )
    gated = derive_fraud(
        FraudInputs(
            sub_question_id="fraud-gated-out",
            defendant="D",
            victim="V",
            property_id="P",
            evidence=[
                inadmissible_deception,
                Evidence(
                    evidence_id="E3",
                    supports=[
                        Fact("mistake_caused", ("V",)),
                        Fact("disposition_by_deceived", ("V", "P")),
                    ],
                ),
            ],
            standards=[StandardJudgment("intent_to_defraud", ("D",), True, "bootstrap")],
        )
    )
    assert gated.conclusion_for("fraud_established") == "not_established"
    assert gated.gated_out == [
        {
            "evidence_id": "E2",
            "fact": {"predicate_id": "deception", "args": ["D", "V"]},
            "reason": "excluded_hearsay",
        }
    ]


def test_verifier_flags_inadmissible_use_against_derivation() -> None:
    from idpr.legacy.fraud_reasoning import (
        Evidence,
        Fact,
        FraudInputs,
        StandardJudgment,
        derive_fraud,
    )
    from idpr.verification import ParagraphClaim, verify_claims

    derivation = derive_fraud(
        FraudInputs(
            sub_question_id="inadmissible-demo",
            defendant="D",
            victim="V",
            property_id="P",
            evidence=[
                Evidence(
                    evidence_id="E-bad",
                    illegally_obtained=True,
                    violation_substantial=True,
                    supports=[Fact("deception", ("D", "V"))],
                )
            ],
            standards=[StandardJudgment("intent_to_defraud", ("D",), True, "bootstrap")],
        )
    )

    report = verify_claims(
        derivation,
        [
            ParagraphClaim(
                paragraph_id="p1",
                predicate=Fact("deception", ("D", "V")),
                evidence_id="E-bad",
            )
        ],
    )

    assert report.score < 1.0
    assert report.violations == [
        {
            "type": "inadmissible_use",
            "paragraph_id": "p1",
            "evidence_id": "E-bad",
            "predicate": {"predicate_id": "deception", "args": ["D", "V"]},
        }
    ]


def test_rulegen_writes_draft_rules_without_claiming_legal_verification(
    tmp_path: Path,
) -> None:
    from idpr.rulegen import RuleDraft, write_rule_draft

    draft = RuleDraft(
        rule_id="fraud.commentary.seed",
        source_ref="commentary://criminal/fraud/seed",
        body="rel candidate_fraud(d, v) = deception(d, v)",
    )

    output = write_rule_draft(draft, tmp_path)

    text = output.read_text(encoding="utf-8")
    assert output.name == "fraud.commentary.seed.scl"
    assert "status: draft" in text
    assert "verified" not in text.lower()
    assert "commentary://criminal/fraud/seed" in text
