from __future__ import annotations

import json
import re
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_PARQUET = Path(
    "/home/jaehoonjeong/data/sp_qwen/warehouse/lbox_kcl/kcl_essay/test.parquet"
)
OUT_JSONL = PROJECT_ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl"
OUT_REVIEW = PROJECT_ROOT / "data/inventory/kcl_criminal_v1_review.md"
OUT_TAG_COUNTS = PROJECT_ROOT / "data/inventory/kcl_criminal_v1_tag_counts.md"


@dataclass(frozen=True, slots=True)
class TagSpec:
    legal_area: str
    issue_tags: tuple[str, ...]
    coverage_candidate: str = "out_of_current_rule_scope"
    notes: str = ""


CURATED_TAGS: dict[str, TagSpec] = {
    "변호사시험 10회 형사법 제1문 1. (가)": TagSpec(
        "substantive",
        (
            "forced_indecent_act_indirect_principal",
            "residential_intrusion_rape_injury",
            "residential_intrusion",
            "voluntary_abandonment",
        ),
    ),
    "변호사시험 10회 형사법 제1문 1. (나)": TagSpec(
        "procedure",
        ("voluntary_submission", "warrantless_seizure", "evidence_admissibility"),
        "procedure_gating_candidate",
    ),
    "변호사시험 10회 형사법 제1문 1. (다)": TagSpec(
        "procedure",
        (
            "emergency_arrest_search_seizure",
            "post_seizure_warrant",
            "seizure_record_photo_admissibility",
        ),
        "procedure_gating_candidate",
    ),
    "변호사시험 10회 형사법 제1문 1. (라)": TagSpec(
        "procedure",
        (
            "secret_recording_by_conversation_party",
            "defendant_statement_hearsay_exception",
            "recording_admissibility",
        ),
        "procedure_gating_candidate",
    ),
    "변호사시험 10회 형사법 제1문 2.": TagSpec(
        "substantive",
        ("independent_concurrent_acts", "injury_resulting_death", "causation_uncertainty"),
    ),
    "변호사시험 10회 형사법 제1문 3. (가)": TagSpec(
        "substantive",
        ("bribery", "bribe_delivery", "official_bribe_receipt", "dereliction_of_duty"),
    ),
    "변호사시험 10회 형사법 제1문 3. (나)": TagSpec(
        "procedure",
        ("hearsay_statement", "co_defendant_statement", "witness_testimony_admissibility"),
        "procedure_gating_candidate",
    ),
    "변호사시험 10회 형사법 제1문 3. (다)": TagSpec(
        "procedure",
        ("appeal_reason_statement_period", "appellate_trial_scope"),
    ),
    "변호사시험 10회 형사법 제2문 1.": TagSpec(
        "substantive",
        (
            "embezzlement",
            "fraud",
            "stolen_property",
            "mistake_of_object",
            "accidental_defense",
        ),
        "property_crime_candidate",
        "Contains fraud and embezzlement, but the row is multi-issue.",
    ),
    "변호사시험 10회 형사법 제2문 2.": TagSpec(
        "substantive",
        (
            "special_robbery_attempt",
            "robbery_preparation",
            "commencement_of_execution",
            "breach_of_trust",
            "harboring_offender",
        ),
        "property_crime_candidate",
    ),
    "변호사시험 10회 형사법 제2문 3.": TagSpec(
        "substantive",
        ("traffic_accident_death", "negligence", "causation", "objective_attribution"),
    ),
    "변호사시험 10회 형사법 제2문 5.": TagSpec(
        "procedure",
        ("appeal_interest", "dismissal_judgment", "formal_judgment"),
    ),
    "변호사시험 10회 형사법 제2문 6.": TagSpec(
        "procedure",
        ("defense_counsel_appointment", "appeal_reason_statement", "procedural_cure"),
    ),
    "변호사시험 11회 형사법 제1문 1.": TagSpec(
        "substantive",
        (
            "special_theft_joint_principal",
            "quasi_robbery_injury",
            "stolen_property",
            "extortion",
            "sexual_image_threat",
        ),
        "property_crime_candidate",
    ),
    "변호사시험 11회 형사법 제1문 2. (나)": TagSpec(
        "mixed",
        ("relative_property_crime_exception", "complaint_withdrawal", "special_theft"),
        "property_crime_candidate",
    ),
    "변호사시험 11회 형사법 제1문 3. (가)": TagSpec(
        "procedure",
        (
            "digital_evidence_admissibility",
            "forensic_participation_right",
            "copy_identity",
        ),
        "procedure_gating_candidate",
    ),
    "변호사시험 11회 형사법 제1문 3. (나)": TagSpec(
        "procedure",
        ("unrelated_electronic_evidence", "separate_warrant", "participation_right"),
        "procedure_gating_candidate",
    ),
    "변호사시험 11회 형사법 제1문 4.": TagSpec(
        "procedure",
        ("retrial", "conflicting_co_offender_judgment", "new_evidence"),
    ),
    "변호사시험 11회 형사법 제2문 1. (가)": TagSpec(
        "substantive",
        ("bribery", "joint_principal", "bribe_giving", "third_party_receipt"),
    ),
    "변호사시험 11회 형사법 제2문 1. (나)": TagSpec(
        "substantive",
        (
            "false_public_document",
            "indirect_principal",
            "obstruction_by_fraud",
            "dereliction_of_duty",
        ),
    ),
    "변호사시험 11회 형사법 제2문 1. (다)": TagSpec(
        "substantive",
        ("quasi_rape_impossible_attempt", "attempt", "mistake_of_circumstance"),
    ),
    "변호사시험 11회 형사법 제2문 2.": TagSpec(
        "procedure",
        ("statute_of_limitations", "co_offender_suspension", "counterpart_offense"),
    ),
    "변호사시험 11회 형사법 제2문 3.": TagSpec(
        "procedure",
        ("prohibition_disadvantageous_change", "appellate_sentencing"),
    ),
    "변호사시험 11회 형사법 제2문 5.": TagSpec(
        "procedure",
        ("evidence_discovery", "prosecutor_appeal", "discovery_noncompliance"),
    ),
    "변호사시험 12회 형사법 제1문 1.": TagSpec(
        "substantive",
        ("cyber_defamation_false_fact", "document_offense", "purpose_to_defame"),
    ),
    "변호사시험 12회 형사법 제1문 2.": TagSpec(
        "substantive",
        ("theft", "victim_consent", "mistake_of_consent", "justification_consent"),
    ),
    "변호사시험 12회 형사법 제1문 3.": TagSpec(
        "substantive",
        ("information_property", "occupational_breach_of_trust", "breach_of_trust_bribe"),
        "property_crime_candidate",
    ),
    "변호사시험 12회 형사법 제1문 4.": TagSpec(
        "substantive",
        (
            "official_secret_disclosure",
            "perjury",
            "obstruction_by_fraud",
            "harboring_offender",
            "status_offense_accomplice",
        ),
    ),
    "변호사시험 12회 형사법 제1문 5. 가.": TagSpec(
        "procedure",
        ("hearsay_vs_original_evidence", "witness_testimony_admissibility"),
        "procedure_gating_candidate",
    ),
    "변호사시험 12회 형사법 제1문 5. 나.": TagSpec(
        "procedure",
        ("multiple_hearsay", "police_statement_record", "hearsay_exception"),
        "procedure_gating_candidate",
    ),
    "변호사시험 12회 형사법 제1문 6.": TagSpec(
        "procedure",
        ("appellate_scope", "imaginative_concurrence", "partial_appeal"),
    ),
    "변호사시험 12회 형사법 제2문 1. 가.": TagSpec(
        "substantive",
        ("murder", "mistake_of_object", "instigator_liability"),
    ),
    "변호사시험 12회 형사법 제2문 1. 나.": TagSpec(
        "substantive",
        ("murder_preparation", "accomplice_of_preparation", "withdrawal_from_preparation"),
    ),
    "변호사시험 12회 형사법 제2문 1. 다.": TagSpec(
        "substantive",
        (
            "theft_from_deceased",
            "private_document_forgery",
            "fraud",
            "improper_use_of_seal",
        ),
        "property_crime_candidate",
    ),
    "변호사시험 12회 형사법 제2문 2.": TagSpec(
        "procedure",
        ("emergency_arrest_search_seizure", "arrest_scene_search", "search_warrant"),
        "procedure_gating_candidate",
    ),
    "변호사시험 12회 형사법 제2문 3.": TagSpec(
        "procedure",
        (
            "inspection_report_photo",
            "reenactment_photo",
            "expert_report_admissibility",
        ),
        "procedure_gating_candidate",
    ),
    "변호사시험 12회 형사법 제2문 4.": TagSpec(
        "procedure",
        (
            "third_party_voluntary_submission",
            "unrelated_electronic_evidence",
            "illegal_evidence",
            "post_warrant_cure",
        ),
        "procedure_gating_candidate",
    ),
    "변호사시험 13회 형사법 제1문 1.": TagSpec(
        "substantive",
        (
            "joint_theft_impossible_attempt",
            "joint_residential_intrusion",
            "quasi_robbery_injury",
            "joint_principal_mistake",
            "relative_property_crime_exception",
        ),
        "property_crime_candidate",
    ),
    "변호사시험 13회 형사법 제1문 2.": TagSpec(
        "procedure",
        ("police_stop_questioning", "use_of_force_stop", "arrest_method"),
    ),
    "변호사시험 13회 형사법 제1문 3.": TagSpec(
        "substantive",
        ("murder_attempt", "voluntary_abandonment", "joint_principal", "secret_recording"),
    ),
    "변호사시험 13회 형사법 제1문 4. 1)": TagSpec(
        "procedure",
        (
            "emergency_arrest_search_seizure",
            "electronic_evidence_admissibility",
            "secret_recording",
            "hearsay_exception",
        ),
        "procedure_gating_candidate",
    ),
    "변호사시험 13회 형사법 제1문 4. 2)": TagSpec(
        "procedure",
        ("investigator_testimony", "police_interrogation_record", "impeachment_evidence"),
        "procedure_gating_candidate",
    ),
    "변호사시험 13회 형사법 제2문 1.": TagSpec(
        "substantive",
        (
            "special_theft",
            "credit_card_crime",
            "theft_vs_fraud",
            "special_injury",
            "obstruction_by_fraud",
            "harboring_offender",
        ),
        "property_crime_candidate",
    ),
    "변호사시험 13회 형사법 제2문 2.": TagSpec(
        "procedure",
        ("unrelated_electronic_evidence", "warrant_relevance", "electronic_evidence"),
        "procedure_gating_candidate",
    ),
    "변호사시험 13회 형사법 제2문 3.": TagSpec(
        "procedure",
        ("partial_appeal", "appellate_disposition", "concurrent_crimes"),
    ),
    "변호사시험 13회 형사법 제2문 4.": TagSpec(
        "procedure",
        ("bail_revocation", "ordinary_appeal", "execution_stay"),
    ),
    "변호사시험 13회 형사법 제2문 5.": TagSpec(
        "mixed",
        ("non_retroactivity", "habitual_offense", "amendment_of_indictment", "identity_of_facts"),
    ),
    "변호사시험 14회 형사법 제1문 1.": TagSpec(
        "substantive",
        ("residential_intrusion", "arson", "attempted_murder", "joint_principal"),
    ),
    "변호사시험 14회 형사법 제1문 2.": TagSpec(
        "substantive",
        ("fraud", "use_deception", "bribe_delivery", "embezzlement", "bribery"),
        "property_crime_candidate",
        "Fraud is present, but the row also includes bribery and embezzlement issues.",
    ),
    "변호사시험 14회 형사법 제1문 3.": TagSpec(
        "substantive",
        ("interference_with_exercise_of_right", "property_possession", "damage"),
        "property_crime_candidate",
    ),
    "변호사시험 14회 형사법 제1문 4. 1)": TagSpec(
        "procedure",
        ("complaint_before_investigation", "offense_subject_to_complaint", "emergency_arrest"),
    ),
    "변호사시험 14회 형사법 제1문 4. 2)": TagSpec(
        "procedure",
        ("complaint_cure_after_indictment", "offense_subject_to_complaint"),
    ),
    "변호사시험 14회 형사법 제1문 5. 1)": TagSpec(
        "procedure",
        ("remand_scope", "partial_appeal", "concurrent_crimes"),
    ),
    "변호사시험 14회 형사법 제1문 5. 2)": TagSpec(
        "procedure",
        ("prohibition_disadvantageous_change", "remand_sentencing"),
    ),
    "변호사시험 14회 형사법 제2문 1.": TagSpec(
        "substantive",
        ("special_theft_joint_principal", "quasi_robbery_injury", "joint_principal"),
        "property_crime_candidate",
    ),
    "변호사시험 14회 형사법 제2문 2.": TagSpec(
        "substantive",
        ("special_robbery", "causation", "objective_attribution", "aggravated_result"),
    ),
    "변호사시험 14회 형사법 제2문 3.": TagSpec(
        "procedure",
        ("hearsay_statement", "co_defendant_statement", "witness_testimony_admissibility"),
        "procedure_gating_candidate",
    ),
    "변호사시험 14회 형사법 제2문 4.": TagSpec(
        "substantive",
        ("obstruction_of_official_duties", "legality_of_official_act", "mistake_of_legality"),
    ),
    "변호사시험 14회 형사법 제2문 5.": TagSpec(
        "procedure",
        (
            "remote_cloud_search_seizure",
            "tablet_imaging",
            "warrant_scope",
            "electronic_evidence",
        ),
        "procedure_gating_candidate",
    ),
    "변호사시험 14회 형사법 제2문 6.": TagSpec(
        "procedure",
        ("video_recording_authenticity", "witness_statement_record", "hearsay_exception"),
        "procedure_gating_candidate",
    ),
    "변호사시험 14회 형사법 제2문 7.": TagSpec(
        "procedure",
        ("appellate_fact_finding", "trial_centered_principle", "direct_examination_principle"),
    ),
}

STANDARD_HINTS = {
    "objective_attribution",
    "causation",
    "negligence",
    "purpose_to_defame",
    "voluntary_abandonment",
    "mistake_of_consent",
    "legality_of_official_act",
    "evidence_admissibility",
    "digital_evidence_admissibility",
    "electronic_evidence_admissibility",
    "witness_testimony_admissibility",
}


def main() -> None:
    df = pd.read_parquet(SOURCE_PARQUET)
    criminal = df[df["meta"].str.contains("형사법", na=False)].copy()
    criminal = criminal.reset_index(names="source_row_index")

    items = [build_item(row) for _, row in criminal.iterrows()]
    missing_specs = [
        item["source"]["original_meta"]
        for item in items
        if "unknown_issue" in item["issue_tags"]
    ]
    if missing_specs:
        raise RuntimeError(f"Missing curated tags: {missing_specs}")

    OUT_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with OUT_JSONL.open("w", encoding="utf-8") as out:
        for item in items:
            out.write(json.dumps(item, ensure_ascii=False, sort_keys=True) + "\n")

    OUT_REVIEW.write_text(render_review(items), encoding="utf-8")
    OUT_TAG_COUNTS.write_text(render_tag_counts(items), encoding="utf-8")
    print(
        {
            "items": len(items),
            "jsonl": str(OUT_JSONL),
            "review": str(OUT_REVIEW),
            "tag_counts": str(OUT_TAG_COUNTS),
        }
    )


def build_item(row: Any) -> dict[str, Any]:
    meta = normalize_spaces(str(row["meta"]))
    spec = CURATED_TAGS.get(meta)
    if spec is None:
        spec = TagSpec("mixed", ("unknown_issue",), notes="Needs manual tag assignment.")

    exam_round, paper, question_number, subpart = parse_meta(meta)
    item_id = make_item_id(exam_round, paper, question_number, subpart)
    tags = list(spec.issue_tags)
    norm_types = infer_norm_types(tags)
    covered = False
    coverage_notes = spec.notes or "Not fully covered by the current draft rule DB."
    if spec.coverage_candidate == "procedure_gating_candidate":
        coverage_notes = (
            "Procedure/evidence issue candidate for later gates; not fully encoded yet."
        )
    elif spec.coverage_candidate == "property_crime_candidate" and not spec.notes:
        coverage_notes = "Property-crime scope candidate; requires rule implementation and review."

    return {
        "sub_question_id": item_id,
        "source": {
            "dataset": "lbox_kcl_essay",
            "item_id": meta,
            "original_meta": meta,
            "source_row_index": int(row["source_row_index"]),
            "parquet_path": str(SOURCE_PARQUET),
        },
        "subject": "형사법",
        "exam_round": exam_round,
        "paper": paper,
        "question_number": question_number,
        "subpart": subpart,
        "question_text": str(row["question"]).strip(),
        "question_prompt": extract_prompt(str(row["question"])),
        "legal_area": spec.legal_area,
        "issue_tags": tags,
        "norm_types": norm_types,
        "covered": covered,
        "coverage_candidate": spec.coverage_candidate,
        "coverage_notes": coverage_notes,
        "review_status": "reviewed",
        "coverage_review_status": "needs_review",
        "review_notes": (
            "Question split, issue tags, and legal area approved by the user on "
            "2026-07-15; coverage remains pending review."
        ),
        "rubric_count": len(row["rubrics"]),
        "rubric_summary": [str(text) for text in row["rubrics"][:5]],
        "notes": "KCL row treated as one sub-question; content review approved.",
    }


def parse_meta(meta: str) -> tuple[int, str, str, str]:
    match = re.match(r"변호사시험\s+(\d+)회\s+형사법\s+제(\d+)문\s+(.+)", meta)
    if not match:
        raise ValueError(f"Unexpected meta format: {meta}")
    exam_round = int(match.group(1))
    paper = f"제{match.group(2)}문"
    tail = match.group(3).strip()
    number_match = re.match(r"([^.\s]+\.?)\s*(.*)", tail)
    if not number_match:
        return exam_round, paper, tail, ""
    question_number = number_match.group(1).rstrip(".")
    subpart = number_match.group(2).strip()
    return exam_round, paper, question_number, subpart


def make_item_id(exam_round: int, paper: str, question_number: str, subpart: str) -> str:
    paper_id = re.sub(r"\D", "", paper)
    subpart_id = normalize_subpart(subpart)
    parts = [f"kcl_criminal_r{exam_round:02d}", f"p{paper_id}", f"q{question_number}"]
    if subpart_id:
        parts.append(subpart_id)
    return "_".join(parts)


def normalize_subpart(subpart: str) -> str:
    value = subpart.strip().strip(".")
    value = value.replace("(", "").replace(")", "")
    value = value.replace(" ", "_")
    korean = {"가": "ga", "나": "na", "다": "da", "라": "ra"}
    return korean.get(value, re.sub(r"[^0-9A-Za-z가-힣_]+", "", value))


def infer_norm_types(tags: list[str]) -> list[str]:
    norms = {"rule"}
    if any(tag in STANDARD_HINTS for tag in tags):
        norms.add("standard")
    return sorted(norms)


def extract_prompt(question: str) -> str:
    parts = [normalize_spaces(part) for part in re.split(r"\n\s*\n", question) if part.strip()]
    if not parts:
        return normalize_spaces(question)
    return parts[-1]


def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def render_review(items: list[dict[str, Any]]) -> str:
    lines = [
        "# KCL 형사법 설문 분해 및 태깅 검수본",
        "",
        "- Source: `sp_qwen/warehouse/lbox_kcl/kcl_essay/test.parquet`",
        f"- Items: {len(items)}",
        "- Content review: all 61 rows are `reviewed` for split, tags, and legal area.",
        "- Coverage review: all 61 rows remain `needs_review`.",
        "- Split rule: one KCL essay row is treated as one sub-question.",
        "- `covered=false` means not fully executable by the current draft rule DB.",
        "",
        (
            "| # | sub_question_id | content review | coverage review | covered | meta | "
            "area | tags | prompt | rubric cues |"
        ),
        "|---:|---|---|---|---|---|---|---|---|---|",
    ]
    for idx, item in enumerate(items, start=1):
        tags = ", ".join(item["issue_tags"])
        rubric = " / ".join(item["rubric_summary"][:2])
        lines.append(
            "| "
            + " | ".join(
                [
                    str(idx),
                    f"`{item['sub_question_id']}`",
                    item["review_status"],
                    item["coverage_review_status"],
                    str(item["covered"]).lower(),
                    escape_md(item["source"]["original_meta"]),
                    item["legal_area"],
                    f"`{escape_md(tags)}`",
                    escape_md(shorten(item["question_prompt"], 180)),
                    escape_md(shorten(rubric, 220)),
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## 검수 요청",
            "",
            "설문 분해, `issue_tags`, `legal_area`는 승인 반영되었습니다.",
            "사용자 검수가 남은 항목은 coverage 결정뿐입니다.",
            "",
            "1. 1차 구현 scope로 `covered`를 올릴 항목이 있는지",
            "2. 승인한 항목은 `coverage_review_status=reviewed`로 바꿀지",
        ]
    )
    return "\n".join(lines) + "\n"


def render_tag_counts(items: list[dict[str, Any]]) -> str:
    counts = Counter(tag for item in items for tag in item["issue_tags"])
    repeated = sum(count > 1 for count in counts.values())
    singletons = sum(count == 1 for count in counts.values())
    lines = [
        "# KCL 형사법 태그 빈도",
        "",
        f"- Items: {len(items)}",
        f"- Unique tags: {len(counts)}",
        f"- Total tag assignments: {sum(counts.values())}",
        f"- Repeated tags: {repeated}",
        f"- Singleton tags: {singletons}",
        "",
        "| tag | count | repeated |",
        "|---|---:|---|",
    ]
    for tag, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{tag}` | {count} | {'yes' if count > 1 else 'no'} |")
    return "\n".join(lines) + "\n"


def escape_md(text: str) -> str:
    return normalize_spaces(text).replace("|", "\\|")


def shorten(text: str, limit: int) -> str:
    text = normalize_spaces(text)
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


if __name__ == "__main__":
    main()
