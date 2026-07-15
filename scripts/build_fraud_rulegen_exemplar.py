from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from idpr.rulegen import compile_rule_ir  # noqa: E402


COMMENTARY = PROJECT_ROOT / "data/commentary/kcl_criminal_v1_commentary_chunks.jsonl"
OUT_DIR = PROJECT_ROOT / "data/rulegen/fraud"
OUT_INDEX = OUT_DIR / "fraud_commentary_index.json"
OUT_REQUESTS = OUT_DIR / "fraud_rulegen_requests.jsonl"
OUT_IR = OUT_DIR / "fraud_rule_ir_exemplar.json"
OUT_SCALLOP = PROJECT_ROOT / "rules/exemplars/fraud_v1_candidate.scl"
MAX_BATCH_CHARS = 12_000


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def source_ref(comment_id: str, section_path: str, quote: str) -> dict[str, str]:
    return {
        "comment_id": comment_id,
        "section_path": section_path,
        "quote": quote,
    }


SUMMARY = source_ref(
    "comm_001692_제347조_Ⅰ_0",
    "Ⅰ",
    "사기죄의 객관적 구성요건은",
)
DECEPTION = source_ref(
    "comm_001692_제347조_Ⅳ.1_11",
    "Ⅳ.1",
    "기망이란 널리 거래관계에서 지켜야 할 신의칙에 반하는 행위",
)
MISTAKE = source_ref(
    "comm_001692_제347조_Ⅳ.2_47",
    "Ⅳ.2",
    "착오란 사실과 일치하지 않는 인식을 의미한다.",
)
DISPOSITION = source_ref(
    "comm_001692_제347조_Ⅳ.3_49",
    "Ⅳ.3",
    "사기죄는 피기망자의 착오에 기한 재산적 처분행위에 의하여",
)
LOSS = source_ref(
    "comm_001692_제347조_Ⅳ.4_62",
    "Ⅳ.4",
    "재산상 손해",
)
ACQUISITION = source_ref(
    "comm_001692_제347조_Ⅳ.5_66",
    "Ⅳ.5",
    "사기죄에서 ‘재물의 교부’란",
)
INTENT = source_ref(
    "comm_001692_제347조_Ⅴ.1_74",
    "Ⅴ.1",
    "범의의 판단 시점은 행위 당시로 보아야 한다.",
)
UNLAWFUL_INTENT = source_ref(
    "comm_001692_제347조_Ⅴ.2_82",
    "Ⅴ.2",
    "불법영득의사가 필요한지에 관하여는",
)


def predicate(
    predicate_id: str,
    arguments: tuple[tuple[str, str], ...],
    *,
    kind: str,
    role: str,
    origin: str,
    definition: str,
    refs: tuple[dict[str, str], ...] = (),
) -> dict[str, Any]:
    return {
        "id": predicate_id,
        "arguments": [{"name": name, "type": type_name} for name, type_name in arguments],
        "kind": kind,
        "role": role,
        "origin": origin,
        "definition": definition,
        "source_refs": list(refs),
    }


def variable(value: str) -> dict[str, str]:
    return {"kind": "variable", "value": value}


def string(value: str) -> dict[str, str]:
    return {"kind": "string", "value": value}


def atom(
    predicate_id: str,
    *arguments: dict[str, Any],
    negated: bool = False,
) -> dict[str, Any]:
    return {
        "predicate": predicate_id,
        "arguments": list(arguments),
        "negated": negated,
    }


def rule(
    rule_id: str,
    head: dict[str, Any],
    body: list[dict[str, Any]],
    refs: tuple[dict[str, str], ...],
    review_notes: str,
) -> dict[str, Any]:
    return {
        "id": rule_id,
        "head": head,
        "body": body,
        "source_refs": list(refs),
        "review_notes": review_notes,
    }


def build_fraud_ir(comment_ids: list[str]) -> dict[str, Any]:
    fact = (("fact_id", "String"),)
    person_pair = (("defendant", "String"), ("victim", "String"))
    fraud_args = (
        ("defendant", "String"),
        ("deceived", "String"),
        ("owner", "String"),
        ("asset", "String"),
        ("beneficiary", "String"),
    )
    predicates = [
        predicate(
            "provable",
            fact,
            kind="rule",
            role="input",
            origin="system",
            definition="Evidence gate output: this fact may be consumed by substantive rules.",
        ),
        predicate(
            "active_policy",
            (("policy_id", "String"),),
            kind="rule",
            role="policy",
            origin="system",
            definition="Exactly one human-approved legal variant is active for an evaluation run.",
        ),
        predicate(
            "deception_fact",
            (("fact_id", "String"), *person_pair),
            kind="standard",
            role="input",
            origin="commentary",
            definition="Defendant conduct qualifies as deception against the deceived person.",
            refs=(DECEPTION,),
        ),
        predicate(
            "mistake_fact",
            (("fact_id", "String"), ("deceived", "String")),
            kind="standard",
            role="input",
            origin="commentary",
            definition="The deceived person held a perception inconsistent with fact.",
            refs=(MISTAKE,),
        ),
        predicate(
            "deception_mistake_causal_fact",
            (("fact_id", "String"), *person_pair),
            kind="standard",
            role="input",
            origin="commentary",
            definition="The deception caused or materially induced the mistake.",
            refs=(SUMMARY, MISTAKE),
        ),
        predicate(
            "disposition_fact",
            (
                ("fact_id", "String"),
                ("deceived", "String"),
                ("owner", "String"),
                ("asset", "String"),
            ),
            kind="standard",
            role="input",
            origin="commentary",
            definition="The deceived person's act or omission qualifies as a property disposition.",
            refs=(DISPOSITION,),
        ),
        predicate(
            "mistake_disposition_causal_fact",
            (
                ("fact_id", "String"),
                ("deceived", "String"),
                ("asset", "String"),
            ),
            kind="standard",
            role="input",
            origin="commentary",
            definition="The mistake caused or materially induced the disposition.",
            refs=(SUMMARY, DISPOSITION),
        ),
        predicate(
            "property_loss_fact",
            (
                ("fact_id", "String"),
                ("owner", "String"),
                ("asset", "String"),
            ),
            kind="standard",
            role="input",
            origin="commentary",
            definition=(
                "The legally selected damage theory treats the disposition as property loss."
            ),
            refs=(LOSS,),
        ),
        predicate(
            "disposition_acquisition_causal_fact",
            (
                ("fact_id", "String"),
                ("deceived", "String"),
                ("beneficiary", "String"),
                ("asset", "String"),
            ),
            kind="standard",
            role="input",
            origin="commentary",
            definition="The disposition caused the beneficiary's acquisition of the asset.",
            refs=(SUMMARY, ACQUISITION),
        ),
        predicate(
            "acquisition_fact",
            (
                ("fact_id", "String"),
                ("defendant", "String"),
                ("beneficiary", "String"),
                ("asset", "String"),
            ),
            kind="rule",
            role="input",
            origin="commentary",
            definition="Defendant or intended third party acquired property or a property benefit.",
            refs=(ACQUISITION,),
        ),
        predicate(
            "intent_to_defraud_fact",
            (("fact_id", "String"), ("defendant", "String")),
            kind="standard",
            role="input",
            origin="commentary",
            definition="Fraud intent is established at the time of the conduct.",
            refs=(INTENT,),
        ),
        predicate(
            "unlawful_gain_intent_fact",
            (("fact_id", "String"), ("defendant", "String")),
            kind="standard",
            role="input",
            origin="commentary",
            definition=(
                "Unlawful acquisition or gain intent is established under the selected theory."
            ),
            refs=(UNLAWFUL_INTENT,),
        ),
    ]
    bridge_specs = [
        ("proven_deception", person_pair, "deception_fact", ("f", "d", "v"), (DECEPTION,)),
        (
            "proven_mistake",
            (("deceived", "String"),),
            "mistake_fact",
            ("f", "v"),
            (MISTAKE,),
        ),
        (
            "proven_deception_mistake_causal",
            person_pair,
            "deception_mistake_causal_fact",
            ("f", "d", "v"),
            (SUMMARY, MISTAKE),
        ),
        (
            "proven_disposition",
            (("deceived", "String"), ("owner", "String"), ("asset", "String")),
            "disposition_fact",
            ("f", "v", "o", "a"),
            (DISPOSITION,),
        ),
        (
            "proven_mistake_disposition_causal",
            (("deceived", "String"), ("asset", "String")),
            "mistake_disposition_causal_fact",
            ("f", "v", "a"),
            (SUMMARY, DISPOSITION),
        ),
        (
            "proven_property_loss",
            (("owner", "String"), ("asset", "String")),
            "property_loss_fact",
            ("f", "o", "a"),
            (LOSS,),
        ),
        (
            "proven_disposition_acquisition_causal",
            (
                ("deceived", "String"),
                ("beneficiary", "String"),
                ("asset", "String"),
            ),
            "disposition_acquisition_causal_fact",
            ("f", "v", "b", "a"),
            (SUMMARY, ACQUISITION),
        ),
        (
            "proven_acquisition",
            (
                ("defendant", "String"),
                ("beneficiary", "String"),
                ("asset", "String"),
            ),
            "acquisition_fact",
            ("f", "d", "b", "a"),
            (ACQUISITION,),
        ),
        (
            "proven_intent_to_defraud",
            (("defendant", "String"),),
            "intent_to_defraud_fact",
            ("f", "d"),
            (INTENT,),
        ),
        (
            "proven_unlawful_gain_intent",
            (("defendant", "String"),),
            "unlawful_gain_intent_fact",
            ("f", "d"),
            (UNLAWFUL_INTENT,),
        ),
    ]
    for predicate_id, arguments, _, _, refs in bridge_specs:
        predicates.append(
            predicate(
                predicate_id,
                arguments,
                kind="rule",
                role="derived",
                origin="commentary",
                definition=f"Evidence-gated form of {predicate_id.removeprefix('proven_')}.",
                refs=refs,
            )
        )
    predicates.extend(
        [
            predicate(
                "fraud_core",
                fraud_args,
                kind="rule",
                role="derived",
                origin="commentary",
                definition=(
                    "Common fraud elements before disputed damage and unlawful-intent variants."
                ),
                refs=(SUMMARY,),
            ),
            predicate(
                "fraud_strict_variant",
                fraud_args,
                kind="rule",
                role="derived",
                origin="commentary",
                definition="Candidate variant requiring separate loss and unlawful-gain intent.",
                refs=(SUMMARY, LOSS, UNLAWFUL_INTENT),
            ),
            predicate(
                "fraud_established",
                fraud_args,
                kind="rule",
                role="derived",
                origin="commentary",
                definition=(
                    "Fraud conclusion under the explicitly activated reviewed policy variant."
                ),
                refs=(SUMMARY, LOSS, UNLAWFUL_INTENT),
            ),
        ]
    )

    rules: list[dict[str, Any]] = []
    for predicate_id, _, fact_predicate, variables, refs in bridge_specs:
        fact_variables = [variable(value) for value in variables]
        rules.append(
            rule(
                f"fraud.bridge.{predicate_id}",
                atom(predicate_id, *fact_variables[1:]),
                [
                    atom(fact_predicate, *fact_variables),
                    atom("provable", fact_variables[0]),
                ],
                refs,
                "Mechanical evidence gate bridge; legal classification remains in the input fact.",
            )
        )

    d, v, o, a, b = map(variable, ("d", "v", "o", "a", "b"))
    rules.append(
        rule(
            "fraud.core",
            atom("fraud_core", d, v, o, a, b),
            [
                atom("proven_deception", d, v),
                atom("proven_mistake", v),
                atom("proven_deception_mistake_causal", d, v),
                atom("proven_disposition", v, o, a),
                atom("proven_mistake_disposition_causal", v, a),
                atom("proven_disposition_acquisition_causal", v, b, a),
                atom("proven_acquisition", d, b, a),
                atom("proven_intent_to_defraud", d),
            ],
            (SUMMARY, DECEPTION, MISTAKE, DISPOSITION, ACQUISITION, INTENT),
            "Human review must confirm the identity constraints for triangular fraud cases.",
        )
    )
    rules.append(
        rule(
            "fraud.variant.strict",
            atom("fraud_strict_variant", d, v, o, a, b),
            [
                atom("fraud_core", d, v, o, a, b),
                atom("proven_property_loss", o, a),
                atom("proven_unlawful_gain_intent", d),
            ],
            (SUMMARY, LOSS, UNLAWFUL_INTENT),
            "Draft strict variant; the two disputed requirements require legal selection.",
        )
    )
    rules.append(
        rule(
            "fraud.activate.strict",
            atom("fraud_established", d, v, o, a, b),
            [
                atom("active_policy", string("kr_fraud_damage_and_unlawful_intent")),
                atom("fraud_strict_variant", d, v, o, a, b),
            ],
            (SUMMARY, LOSS, UNLAWFUL_INTENT),
            "Only activate after human review of the named policy variant.",
        )
    )

    return {
        "version": "1.0.0",
        "rule_set_id": "kr.fraud.article347.v1_candidate",
        "issue_tag": "fraud",
        "status": "draft",
        "legal_review": "pending",
        "source_scope": {
            "target_paths": ["commentary://001692/제347조"],
            "comment_ids": sorted(comment_ids),
        },
        "predicates": predicates,
        "rules": rules,
        "legal_review_questions": [
            "재산상 손해를 독립한 필수요건으로 둘지, 재물 교부·이익 취득에 내재한 침해로 처리할지 선택해야 합니다.",
            "불법영득의사 또는 불법이득의사를 모든 사기 유형의 별도 필수요건으로 둘지 선택해야 합니다.",
            "피기망자, 재산상 피해자, 처분자, 수익자가 다른 삼각사기에서 필요한 권한·근접성 predicate를 확정해야 합니다.",
            "기망·처분행위·손해·고의 중 어느 판단을 standard sub-call로 위임할지 확정해야 합니다.",
        ],
        "coverage_gaps": [
            "제347조 기수 기본형만 대상으로 하며 미수·공범 일반론은 형법총칙 corpus가 필요합니다.",
            "증거능력은 별도 procedural rules와 provable gate에서 처리합니다.",
        ],
    }


def make_batches(chunks: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    batches: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    current_chars = 0
    for chunk in sorted(chunks, key=lambda row: (row["section_path"], row["comment_id"])):
        n_chars = len(chunk["document_text"])
        if current and current_chars + n_chars > MAX_BATCH_CHARS:
            batches.append(current)
            current = []
            current_chars = 0
        current.append(chunk)
        current_chars += n_chars
    if current:
        batches.append(current)
    return batches


def build_request(batch: list[dict[str, Any]], index: int, count: int) -> dict[str, Any]:
    commentary_chunks = [
        {
            "comment_id": row["comment_id"],
            "section_path": row["section_path"],
            "section_title": row["section_title"],
            "document_text": row["document_text"],
        }
        for row in batch
    ]
    return {
        "request_id": f"fraud.article347.pass1.{index:03d}",
        "task": "extract_norm_candidates",
        "issue_tag": "fraud",
        "target": {
            "law_id": "001692",
            "article_no": "제347조",
            "article_title": "사기",
        },
        "batch": {
            "index": index,
            "count": count,
            "section_paths": sorted({row["section_path"] for row in batch}),
            "n_chars": sum(len(row["document_text"]) for row in batch),
        },
        "commentary_chunks": commentary_chunks,
        "constraints": {
            "source_refs_must_be_exact": True,
            "preserve_disagreements": True,
            "legal_status": "draft",
            "output_schema": "idpr/NormCandidateBatch",
        },
    }


def main() -> None:
    all_chunks = load_jsonl(COMMENTARY)
    fraud_chunks = [
        row
        for row in all_chunks
        if row["law_id"] == "001692" and row["article_no"] == "제347조"
    ]
    if len(fraud_chunks) != 127:
        raise ValueError(f"Expected 127 fraud chunks, found {len(fraud_chunks)}")
    commentary_by_id = {row["comment_id"]: row for row in fraud_chunks}

    section_counts: dict[tuple[str, str], dict[str, int]] = defaultdict(
        lambda: {"chunks": 0, "n_chars": 0}
    )
    for row in fraud_chunks:
        stats = section_counts[(row["section_path"], row["section_title"])]
        stats["chunks"] += 1
        stats["n_chars"] += len(row["document_text"])

    batches = make_batches(fraud_chunks)
    requests = [
        build_request(batch, index, len(batches))
        for index, batch in enumerate(batches, start=1)
    ]
    rule_ir = build_fraud_ir(list(commentary_by_id))
    scallop = compile_rule_ir(rule_ir, commentary_by_id)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_SCALLOP.parent.mkdir(parents=True, exist_ok=True)
    index_payload = {
        "target_path": "commentary://001692/제347조",
        "chunks": len(fraud_chunks),
        "n_chars": sum(len(row["document_text"]) for row in fraud_chunks),
        "batch_max_chars": MAX_BATCH_CHARS,
        "batches": len(batches),
        "sections": [
            {
                "section_path": key[0],
                "section_title": key[1],
                **value,
            }
            for key, value in sorted(section_counts.items())
        ],
    }
    OUT_INDEX.write_text(
        json.dumps(index_payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    OUT_REQUESTS.write_text(
        "".join(
            json.dumps(request, ensure_ascii=False, sort_keys=True) + "\n"
            for request in requests
        ),
        encoding="utf-8",
    )
    OUT_IR.write_text(
        json.dumps(rule_ir, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    OUT_SCALLOP.write_text(scallop, encoding="utf-8")
    print(
        json.dumps(
            {
                "chunks": len(fraud_chunks),
                "batches": len(batches),
                "rule_ir": str(OUT_IR),
                "scallop": str(OUT_SCALLOP),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
