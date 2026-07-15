from __future__ import annotations

import hashlib
import json
import re
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import pandas as pd
import pdfplumber


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INVENTORY = PROJECT_ROOT / "data/inventory/kcl_criminal_v1_draft.jsonl"
COMMENTARY_PARQUET = Path(
    "/home/jaehoonjeong/data/sp_qwen/data/serve/commentary_chunks/docs.parquet"
)
RAW_COMMENTARY_ROOT = Path(
    "/home/jaehoonjeong/data/sp_qwen/data/raw/commentary_casenote"
)
OUT_DIR = PROJECT_ROOT / "data/commentary"
OUT_MANIFEST = OUT_DIR / "kcl_criminal_v1_tag_commentary_manifest.jsonl"
OUT_CHUNKS = OUT_DIR / "kcl_criminal_v1_commentary_chunks.jsonl"
OUT_REVIEW = OUT_DIR / "kcl_criminal_v1_commentary_review.md"
OUT_POOL = OUT_DIR / "kcl_criminal_v1_commentary_pool.json"
OUT_AUDIT = OUT_DIR / "kcl_criminal_v1_non_mapped_audit.md"


@dataclass(frozen=True, slots=True)
class TargetSpec:
    law_id: str
    law_name: str
    article_no: str
    article_title: str


@dataclass(frozen=True, slots=True)
class AuditSpec:
    outcome: str
    rationale: str
    required_source: str = ""


CRIMINAL = "형법각칙"
PROCEDURE = "형사소송법"


TARGETS: dict[str, TargetSpec] = {
    "CC_122": TargetSpec("001692", CRIMINAL, "제122조", "직무유기"),
    "CC_127": TargetSpec("001692", CRIMINAL, "제127조", "공무상 비밀의 누설"),
    "CC_129": TargetSpec("001692", CRIMINAL, "제129조", "수뢰, 사전수뢰"),
    "CC_130": TargetSpec("001692", CRIMINAL, "제130조", "제삼자뇌물제공"),
    "CC_133": TargetSpec("001692", CRIMINAL, "제133조", "뇌물공여 등"),
    "CC_136": TargetSpec("001692", CRIMINAL, "제136조", "공무집행방해"),
    "CC_137": TargetSpec("001692", CRIMINAL, "제137조", "위계에 의한 공무집행방해"),
    "CC_151": TargetSpec("001692", CRIMINAL, "제151조", "범인은닉과 친족간의 특례"),
    "CC_152": TargetSpec("001692", CRIMINAL, "제152조", "위증, 모해위증"),
    "CC_164": TargetSpec("001692", CRIMINAL, "제164조", "현주건조물 등 방화"),
    "CC_225": TargetSpec("001692", CRIMINAL, "제225조", "공문서등의 위조변조"),
    "CC_227": TargetSpec("001692", CRIMINAL, "제227조", "허위공문서작성등"),
    "CC_231": TargetSpec("001692", CRIMINAL, "제231조", "사문서등의 위조변조"),
    "CC_234": TargetSpec("001692", CRIMINAL, "제234조", "위조사문서등의 행사"),
    "CC_239": TargetSpec("001692", CRIMINAL, "제239조", "사인등의 위조, 부정사용"),
    "CC_250": TargetSpec("001692", CRIMINAL, "제250조", "살인, 존속살해"),
    "CC_254": TargetSpec("001692", CRIMINAL, "제254조", "미수범"),
    "CC_255": TargetSpec("001692", CRIMINAL, "제255조", "예비, 음모"),
    "CC_257": TargetSpec("001692", CRIMINAL, "제257조", "상해, 존속상해"),
    "CC_258_2": TargetSpec("001692", CRIMINAL, "제258조의2", "특수상해"),
    "CC_259": TargetSpec("001692", CRIMINAL, "제259조", "상해치사"),
    "CC_263": TargetSpec("001692", CRIMINAL, "제263조", "동시범"),
    "CC_267": TargetSpec("001692", CRIMINAL, "제267조", "과실치사"),
    "CC_268": TargetSpec("001692", CRIMINAL, "제268조", "업무상과실·중과실 치사상"),
    "CC_297": TargetSpec("001692", CRIMINAL, "제297조", "강간"),
    "CC_298": TargetSpec("001692", CRIMINAL, "제298조", "강제추행"),
    "CC_299": TargetSpec("001692", CRIMINAL, "제299조", "준강간, 준강제추행"),
    "CC_300": TargetSpec("001692", CRIMINAL, "제300조", "미수범"),
    "CC_301": TargetSpec("001692", CRIMINAL, "제301조", "강간 등 상해·치상"),
    "CC_306": TargetSpec("001692", CRIMINAL, "제306조", "고소"),
    "CC_319": TargetSpec("001692", CRIMINAL, "제319조", "주거침입, 퇴거불응"),
    "CC_323": TargetSpec("001692", CRIMINAL, "제323조", "권리행사방해"),
    "CC_328": TargetSpec("001692", CRIMINAL, "제328조", "친족간의 범행과 고소"),
    "CC_329": TargetSpec("001692", CRIMINAL, "제329조", "절도"),
    "CC_330": TargetSpec("001692", CRIMINAL, "제330조", "야간주거침입절도"),
    "CC_331": TargetSpec("001692", CRIMINAL, "제331조", "특수절도"),
    "CC_333": TargetSpec("001692", CRIMINAL, "제333조", "강도"),
    "CC_334": TargetSpec("001692", CRIMINAL, "제334조", "특수강도"),
    "CC_335": TargetSpec("001692", CRIMINAL, "제335조", "준강도"),
    "CC_337": TargetSpec("001692", CRIMINAL, "제337조", "강도상해, 치상"),
    "CC_338": TargetSpec("001692", CRIMINAL, "제338조", "강도살인·치사"),
    "CC_342": TargetSpec("001692", CRIMINAL, "제342조", "미수범"),
    "CC_343": TargetSpec("001692", CRIMINAL, "제343조", "예비, 음모"),
    "CC_344": TargetSpec("001692", CRIMINAL, "제344조", "친족간의 범행"),
    "CC_347": TargetSpec("001692", CRIMINAL, "제347조", "사기"),
    "CC_350": TargetSpec("001692", CRIMINAL, "제350조", "공갈"),
    "CC_354": TargetSpec("001692", CRIMINAL, "제354조", "친족간의 범행, 동력"),
    "CC_355": TargetSpec("001692", CRIMINAL, "제355조", "횡령, 배임"),
    "CC_356": TargetSpec("001692", CRIMINAL, "제356조", "업무상의 횡령과 배임"),
    "CC_357": TargetSpec("001692", CRIMINAL, "제357조", "배임수증재"),
    "CC_360": TargetSpec("001692", CRIMINAL, "제360조", "점유이탈물횡령"),
    "CC_361": TargetSpec("001692", CRIMINAL, "제361조", "친족간의 범행, 동력"),
    "CC_362": TargetSpec("001692", CRIMINAL, "제362조", "장물의 취득, 알선 등"),
    "CC_365": TargetSpec("001692", CRIMINAL, "제365조", "친족간의 범행"),
    "CC_366": TargetSpec("001692", CRIMINAL, "제366조", "재물손괴등"),
    "CP_32": TargetSpec("001671", PROCEDURE, "제32조", "변호인선임의 효력"),
    "CP_36": TargetSpec("001671", PROCEDURE, "제36조", "변호인의 독립소송행위권"),
    "CP_49": TargetSpec("001671", PROCEDURE, "제49조", "검증 등의 조서"),
    "CP_102": TargetSpec("001671", PROCEDURE, "제102조", "보석조건의 변경과 취소 등"),
    "CP_106": TargetSpec("001671", PROCEDURE, "제106조", "압수"),
    "CP_108": TargetSpec("001671", PROCEDURE, "제108조", "임의 제출물 등의 압수"),
    "CP_113": TargetSpec("001671", PROCEDURE, "제113조", "압수·수색영장"),
    "CP_114": TargetSpec("001671", PROCEDURE, "제114조", "영장의 방식"),
    "CP_115": TargetSpec("001671", PROCEDURE, "제115조", "영장의 집행"),
    "CP_121": TargetSpec("001671", PROCEDURE, "제121조", "영장집행과 당사자의 참여"),
    "CP_122": TargetSpec("001671", PROCEDURE, "제122조", "영장집행과 참여권자에의 통지"),
    "CP_129": TargetSpec("001671", PROCEDURE, "제129조", "압수목록의 교부"),
    "CP_139": TargetSpec("001671", PROCEDURE, "제139조", "검증"),
    "CP_161_2": TargetSpec("001671", PROCEDURE, "제161조의2", "증인신문의 방식"),
    "CP_200_2": TargetSpec("001671", PROCEDURE, "제200조의2", "영장에 의한 체포"),
    "CP_200_3": TargetSpec("001671", PROCEDURE, "제200조의3", "긴급체포"),
    "CP_211": TargetSpec("001671", PROCEDURE, "제211조", "현행범인과 준현행범인"),
    "CP_212": TargetSpec("001671", PROCEDURE, "제212조", "현행범인의 체포"),
    "CP_215": TargetSpec("001671", PROCEDURE, "제215조", "압수, 수색, 검증"),
    "CP_216": TargetSpec("001671", PROCEDURE, "제216조", "영장에 의하지 아니한 강제처분"),
    "CP_217": TargetSpec("001671", PROCEDURE, "제217조", "영장에 의하지 아니하는 강제처분"),
    "CP_218": TargetSpec("001671", PROCEDURE, "제218조", "영장에 의하지 아니한 압수"),
    "CP_221": TargetSpec("001671", PROCEDURE, "제221조", "제3자의 출석요구 등"),
    "CP_223": TargetSpec("001671", PROCEDURE, "제223조", "고소권자"),
    "CP_230": TargetSpec("001671", PROCEDURE, "제230조", "고소기간"),
    "CP_232": TargetSpec("001671", PROCEDURE, "제232조", "고소의 취소"),
    "CP_244": TargetSpec("001671", PROCEDURE, "제244조", "피의자신문조서의 작성"),
    "CP_244_2": TargetSpec("001671", PROCEDURE, "제244조의2", "피의자진술의 영상녹화"),
    "CP_249": TargetSpec("001671", PROCEDURE, "제249조", "공소시효의 기간"),
    "CP_253": TargetSpec("001671", PROCEDURE, "제253조", "시효의 정지와 효력"),
    "CP_254": TargetSpec("001671", PROCEDURE, "제254조", "공소제기의 방식과 공소장"),
    "CP_266_3": TargetSpec("001671", PROCEDURE, "제266조의3", "증거서류 등의 열람·등사"),
    "CP_266_4": TargetSpec("001671", PROCEDURE, "제266조의4", "법원의 열람·등사 결정"),
    "CP_266_5": TargetSpec("001671", PROCEDURE, "제266조의5", "증거개시 관련 조치"),
    "CP_298": TargetSpec("001671", PROCEDURE, "제298조", "공소장의 변경"),
    "CP_307": TargetSpec("001671", PROCEDURE, "제307조", "증거재판주의"),
    "CP_308_2": TargetSpec("001671", PROCEDURE, "제308조의2", "위법수집증거의 배제"),
    "CP_310_2": TargetSpec("001671", PROCEDURE, "제310조의2", "전문증거와 증거능력"),
    "CP_311": TargetSpec("001671", PROCEDURE, "제311조", "법원 또는 법관의 조서"),
    "CP_312": TargetSpec("001671", PROCEDURE, "제312조", "검사 또는 사법경찰관의 조서 등"),
    "CP_313": TargetSpec("001671", PROCEDURE, "제313조", "진술서 등"),
    "CP_314": TargetSpec("001671", PROCEDURE, "제314조", "증거능력에 대한 예외"),
    "CP_315": TargetSpec("001671", PROCEDURE, "제315조", "당연히 증거능력이 있는 서류"),
    "CP_316": TargetSpec("001671", PROCEDURE, "제316조", "전문의 진술"),
    "CP_318": TargetSpec("001671", PROCEDURE, "제318조", "당사자의 동의와 증거능력"),
    "CP_318_2": TargetSpec("001671", PROCEDURE, "제318조의2", "증명력을 다투기 위한 증거"),
    "CP_327": TargetSpec("001671", PROCEDURE, "제327조", "공소기각의 판결"),
    "CP_328": TargetSpec("001671", PROCEDURE, "제328조", "공소기각의 결정"),
    "CP_342": TargetSpec("001671", PROCEDURE, "제342조", "일부상소"),
    "CP_361_3": TargetSpec("001671", PROCEDURE, "제361조의3", "항소이유서와 답변서"),
    "CP_361_4": TargetSpec("001671", PROCEDURE, "제361조의4", "항소기각의 결정"),
    "CP_363": TargetSpec("001671", PROCEDURE, "제363조", "공소기각의 결정"),
    "CP_364": TargetSpec("001671", PROCEDURE, "제364조", "항소법원의 심판"),
    "CP_368": TargetSpec("001671", PROCEDURE, "제368조", "불이익변경의 금지"),
    "CP_397": TargetSpec("001671", PROCEDURE, "제397조", "파기환송"),
    "CP_402": TargetSpec("001671", PROCEDURE, "제402조", "항고"),
    "CP_420": TargetSpec("001671", PROCEDURE, "제420조", "재심이유"),
    "CP_435": TargetSpec("001671", PROCEDURE, "제435조", "재심개시의 결정"),
}


TAG_TARGETS: dict[str, tuple[str, ...]] = {}
TAG_LIMITATIONS: dict[str, str] = {}
UNAVAILABLE_REASONS: dict[str, str] = {}


def add(tags: tuple[str, ...], targets: tuple[str, ...], limitation: str = "") -> None:
    for tag in tags:
        TAG_TARGETS[tag] = targets
        if limitation:
            TAG_LIMITATIONS[tag] = limitation


def unavailable(tags: tuple[str, ...], reason: str) -> None:
    for tag in tags:
        UNAVAILABLE_REASONS[tag] = reason


add(("forced_indecent_act_indirect_principal",), ("CC_298",), "간접정범은 형법총칙 영역입니다.")
add(("residential_intrusion_rape_injury",), ("CC_297", "CC_301", "CC_319"))
add(("residential_intrusion", "joint_residential_intrusion"), ("CC_319",))
add(("injury_resulting_death",), ("CC_259",))
add(("independent_concurrent_acts", "causation_uncertainty"), ("CC_263",))
add(("bribery", "official_bribe_receipt"), ("CC_129",))
add(("bribe_delivery", "bribe_giving"), ("CC_133",))
add(("third_party_receipt",), ("CC_130",))
add(("dereliction_of_duty",), ("CC_122",))
add(("embezzlement",), ("CC_355", "CC_356"))
add(("fraud", "use_deception"), ("CC_347",))
add(("stolen_property",), ("CC_362",))
add(("special_robbery_attempt",), ("CC_334", "CC_342"))
add(("robbery_preparation",), ("CC_343",))
add(("commencement_of_execution",), ("CC_334", "CC_342"), "실행의 착수 일반론은 형법총칙 영역입니다.")
add(("breach_of_trust",), ("CC_355", "CC_356"))
add(("traffic_accident_death", "negligence"), ("CC_267", "CC_268"))
add(("causation",), ("CC_268", "CC_337", "CC_338"), "인과관계 일반론은 형법총칙 영역입니다.")
add(("special_theft_joint_principal",), ("CC_331",), "공동정범 일반론은 형법총칙 영역입니다.")
add(("quasi_robbery_injury",), ("CC_335", "CC_337"))
add(("extortion",), ("CC_350",))
add(("relative_property_crime_exception",), ("CC_328", "CC_344"))
add(("special_theft",), ("CC_331",))
add(("false_public_document",), ("CC_225", "CC_227"))
add(("obstruction_by_fraud",), ("CC_137",))
add(("quasi_rape_impossible_attempt",), ("CC_299", "CC_300"), "불능미수 일반론은 형법총칙 영역입니다.")
add(("document_offense",), ("CC_231", "CC_234"))
add(("theft", "victim_consent"), ("CC_329",))
add(("information_property",), ("CC_329", "CC_355", "CC_356"))
add(("occupational_breach_of_trust",), ("CC_356",))
add(("breach_of_trust_bribe",), ("CC_357",))
add(("official_secret_disclosure",), ("CC_127",))
add(("perjury",), ("CC_152",))
add(("harboring_offender",), ("CC_151",))
add(("murder",), ("CC_250",))
add(("murder_preparation", "accomplice_of_preparation", "withdrawal_from_preparation"), ("CC_255",))
add(("theft_from_deceased",), ("CC_329", "CC_360"))
add(("private_document_forgery",), ("CC_231",))
add(("improper_use_of_seal",), ("CC_239",))
add(("joint_theft_impossible_attempt",), ("CC_331", "CC_342"), "불능미수와 공동정범은 형법총칙 영역입니다.")
add(("murder_attempt", "attempted_murder"), ("CC_250", "CC_254"))
add(("arson",), ("CC_164",))
add(("interference_with_exercise_of_right", "property_possession"), ("CC_323",))
add(("damage",), ("CC_366",))
add(("special_injury",), ("CC_258_2",))
add(("special_robbery",), ("CC_334",))
add(("aggravated_result",), ("CC_337", "CC_338"))
add(("obstruction_of_official_duties", "legality_of_official_act"), ("CC_136",))
add(("credit_card_crime", "theft_vs_fraud"), ("CC_329", "CC_347"))

add(("voluntary_submission", "warrantless_seizure"), ("CP_108", "CP_218"))
add(("evidence_admissibility",), ("CP_307", "CP_308_2"))
add(("emergency_arrest_search_seizure",), ("CP_200_3", "CP_216", "CP_217"))
add(("post_seizure_warrant",), ("CP_217",))
add(("seizure_record_photo_admissibility",), ("CP_49", "CP_307", "CP_308_2"))
add(
    ("secret_recording_by_conversation_party", "recording_admissibility"),
    ("CP_310_2", "CP_313"),
)
add(("secret_recording",), ("CP_310_2", "CP_313"), "통신비밀보호법 쟁점은 현재 corpus 밖입니다.")
add(("defendant_statement_hearsay_exception",), ("CP_310_2", "CP_313", "CP_316"))
add(("hearsay_statement", "co_defendant_statement"), ("CP_310_2", "CP_316"))
add(("witness_testimony_admissibility",), ("CP_310_2", "CP_316", "CP_161_2"))
add(
    ("appeal_reason_statement_period", "appellate_trial_scope"),
    ("CP_361_3", "CP_361_4", "CP_364"),
)
add(
    ("appeal_interest", "dismissal_judgment", "formal_judgment"),
    ("CP_327", "CP_328", "CP_363"),
)
add(
    ("defense_counsel_appointment", "appeal_reason_statement", "procedural_cure"),
    ("CP_32", "CP_36", "CP_361_3"),
)
add(
    ("digital_evidence_admissibility", "forensic_participation_right", "copy_identity"),
    ("CP_106", "CP_121", "CP_122", "CP_129", "CP_308_2"),
)
add(
    ("unrelated_electronic_evidence", "separate_warrant", "participation_right"),
    ("CP_106", "CP_113", "CP_121", "CP_122", "CP_215", "CP_308_2"),
)
add(("retrial", "conflicting_co_offender_judgment", "new_evidence"), ("CP_420", "CP_435"))
add(
    ("statute_of_limitations", "co_offender_suspension", "counterpart_offense"),
    ("CP_249", "CP_253"),
)
add(("prohibition_disadvantageous_change", "appellate_sentencing"), ("CP_368",))
add(
    ("evidence_discovery", "prosecutor_appeal", "discovery_noncompliance"),
    ("CP_266_3", "CP_266_4", "CP_266_5"),
)
add(("hearsay_vs_original_evidence",), ("CP_310_2", "CP_316"))
add(("hearsay_exception",), ("CP_310_2", "CP_312", "CP_313", "CP_314", "CP_316"))
add(("multiple_hearsay", "police_statement_record"), ("CP_310_2", "CP_312", "CP_314"))
add(("appellate_scope", "imaginative_concurrence", "partial_appeal"), ("CP_342", "CP_364"))
add(("concurrent_crimes", "appellate_disposition"), ("CP_342", "CP_364"))
add(("arrest_scene_search", "search_warrant"), ("CP_113", "CP_215", "CP_216", "CP_217"))
add(("inspection_report_photo", "reenactment_photo"), ("CP_49", "CP_139", "CP_312"))
add(("expert_report_admissibility",), ("CP_313", "CP_314", "CP_315"))
add(("electronic_evidence_admissibility",), ("CP_106", "CP_215", "CP_308_2"))
add(("investigator_testimony", "police_interrogation_record"), ("CP_312", "CP_316"))
add(("impeachment_evidence",), ("CP_318_2",))
add(("arrest_method",), ("CP_200_2", "CP_200_3", "CP_211", "CP_212"))
add(("bail_revocation", "ordinary_appeal", "execution_stay"), ("CP_102", "CP_402"))
add(("complaint_before_investigation",), ("CP_223", "CP_230", "CP_200_3"))
add(("complaint_cure_after_indictment",), ("CP_223", "CP_230", "CP_254", "CP_327"))
add(("complaint_withdrawal",), ("CP_232",))
add(
    ("offense_subject_to_complaint",),
    ("CC_323", "CC_328", "CP_223", "CP_230", "CP_232", "CP_327"),
)
add(("emergency_arrest",), ("CP_200_3",))
add(
    ("electronic_evidence", "warrant_relevance", "warrant_scope"),
    ("CP_106", "CP_113", "CP_215", "CP_308_2"),
)
add(("tablet_imaging",), ("CP_106", "CP_121", "CP_122", "CP_215"))
add(("remote_cloud_search_seizure",), ("CP_106", "CP_113", "CP_215"))
add(("third_party_voluntary_submission",), ("CP_108", "CP_218"))
add(("illegal_evidence", "post_warrant_cure"), ("CP_308_2", "CP_215", "CP_217"))
add(("video_recording_authenticity",), ("CP_221", "CP_244_2", "CP_312"))
add(("witness_statement_record",), ("CP_312", "CP_314"))
add(
    ("appellate_fact_finding", "trial_centered_principle", "direct_examination_principle"),
    ("CP_307", "CP_364"),
)
add(("remand_scope",), ("CP_342", "CP_397"))
add(("remand_sentencing",), ("CP_368", "CP_397"))
add(("amendment_of_indictment", "identity_of_facts"), ("CP_298",))

GENERAL_GAP = "핵심 일반론은 형법총칙 영역이며 현재 corpus에 형법총칙 주석서가 없습니다."

add(("accidental_defense",), ("CC_257",), GENERAL_GAP)
add(("attempt",), ("CC_299", "CC_300"), GENERAL_GAP)
add(("indirect_principal",), ("CC_227",), GENERAL_GAP)
add(("instigator_liability",), ("CC_250",), GENERAL_GAP)
add(
    ("joint_principal",),
    ("CC_129", "CC_164", "CC_250", "CC_254", "CC_331", "CC_335", "CC_337"),
    GENERAL_GAP,
)
add(("joint_principal_mistake",), ("CC_331", "CC_342"), GENERAL_GAP)
add(("justification_consent", "mistake_of_consent"), ("CC_329",), GENERAL_GAP)
add(("mistake_of_circumstance",), ("CC_299", "CC_300"), GENERAL_GAP)
add(("mistake_of_legality",), ("CC_136",), GENERAL_GAP)
add(("mistake_of_object",), ("CC_250", "CC_257"), GENERAL_GAP)
add(("objective_attribution",), ("CC_268", "CC_337", "CC_338"), GENERAL_GAP)
add(("status_offense_accomplice",), ("CC_127",), GENERAL_GAP)
add(
    ("voluntary_abandonment",),
    ("CC_250", "CC_254", "CC_297", "CC_300"),
    GENERAL_GAP,
)

unavailable(("non_retroactivity",), GENERAL_GAP)
unavailable(
    (
        "cyber_defamation_false_fact",
        "purpose_to_defame",
        "sexual_image_threat",
        "habitual_offense",
    ),
    "특별법 주석서가 현재 commentary corpus에 없습니다.",
)
unavailable(
    ("police_stop_questioning", "use_of_force_stop"),
    "경찰관직무집행법 주석서가 현재 commentary corpus에 없습니다.",
)


AUDITED_NON_MAPPED: dict[str, AuditSpec] = {
    "accidental_defense": AuditSpec(
        "partial_context_only",
        "상해죄 제257조 주석은 확보할 수 있으나 우연방위 일반론은 총칙 자료가 필요합니다.",
        "형법총칙 위법성론 주석",
    ),
    "attempt": AuditSpec(
        "partial_context_only",
        "준강간 제299조와 미수범 제300조는 확보되지만 불능미수 일반론은 총칙 쟁점입니다.",
        "형법총칙 미수론 주석",
    ),
    "attempted_murder": AuditSpec(
        "fully_available_after_raw_fallback",
        "살인 제250조와 미수범 제254조 원천 PDF를 모두 확보했습니다.",
    ),
    "causation": AuditSpec(
        "partial_context_only",
        "과실치사상·강도치사상 조문 주석은 있으나 인과관계 일반론은 총칙 자료가 필요합니다.",
        "형법총칙 인과관계 주석",
    ),
    "commencement_of_execution": AuditSpec(
        "partial_context_only",
        "특수강도 및 절도·강도 미수범 주석은 있으나 실행의 착수 일반론은 총칙 쟁점입니다.",
        "형법총칙 미수론 주석",
    ),
    "cyber_defamation_false_fact": AuditSpec(
        "unavailable",
        "정보통신망을 통한 허위사실 명예훼손의 근거 특별법이 현재 corpus 밖입니다.",
        "정보통신망법 또는 관련 특별법 주석",
    ),
    "forced_indecent_act_indirect_principal": AuditSpec(
        "partial_context_only",
        "강제추행 제298조 주석은 있으나 간접정범 일반론은 총칙 자료가 필요합니다.",
        "형법총칙 정범·공범론 주석",
    ),
    "habitual_offense": AuditSpec(
        "unavailable",
        "문항의 상습성은 아동·청소년성보호법상 쟁점으로 해당 특별법이 corpus 밖입니다.",
        "아동·청소년성보호법 주석",
    ),
    "indirect_principal": AuditSpec(
        "partial_context_only",
        "허위공문서작성 제227조 주석은 있으나 간접정범 일반론은 총칙 자료가 필요합니다.",
        "형법총칙 정범·공범론 주석",
    ),
    "instigator_liability": AuditSpec(
        "partial_context_only",
        "살인 제250조 주석은 있으나 객체의 착오가 교사범에 미치는 효과는 총칙 쟁점입니다.",
        "형법총칙 공범론·착오론 주석",
    ),
    "joint_principal": AuditSpec(
        "partial_context_only",
        "각 문항의 뇌물·방화·살인·절도·준강도 조문은 확보되나 공동정범 일반론이 없습니다.",
        "형법총칙 공동정범 주석",
    ),
    "joint_principal_mistake": AuditSpec(
        "partial_context_only",
        "특수절도와 미수범 조문은 확보되나 공동정범의 착오 일반론이 없습니다.",
        "형법총칙 공동정범·착오론 주석",
    ),
    "joint_theft_impossible_attempt": AuditSpec(
        "partial_context_only",
        "특수절도와 미수범 조문은 확보되나 불능미수·공동정범 일반론이 없습니다.",
        "형법총칙 미수론·공동정범 주석",
    ),
    "justification_consent": AuditSpec(
        "partial_context_only",
        "절도 제329조 주석은 있으나 피해자 승낙의 위법성조각 구조는 총칙 쟁점입니다.",
        "형법총칙 피해자 승낙 주석",
    ),
    "mistake_of_circumstance": AuditSpec(
        "partial_context_only",
        "준강간 및 미수범 조문은 확보되나 반전된 구성요건적 착오 일반론은 총칙 쟁점입니다.",
        "형법총칙 착오론 주석",
    ),
    "mistake_of_consent": AuditSpec(
        "partial_context_only",
        "절도 제329조 주석은 있으나 양해·승낙의 착오 효과는 총칙 자료가 필요합니다.",
        "형법총칙 착오론·피해자 승낙 주석",
    ),
    "mistake_of_legality": AuditSpec(
        "partial_context_only",
        "공무집행방해 제136조 주석은 있으나 적법성의 체계적 지위에 따른 착오는 총칙 쟁점입니다.",
        "형법총칙 고의·위법성의 착오 주석",
    ),
    "mistake_of_object": AuditSpec(
        "partial_context_only",
        "살인·상해 조문 주석은 확보되나 객체의 착오 일반론은 총칙 자료가 필요합니다.",
        "형법총칙 구성요건적 착오 주석",
    ),
    "murder_attempt": AuditSpec(
        "fully_available_after_raw_fallback",
        "살인 제250조와 미수범 제254조 원천 PDF를 모두 확보했습니다.",
    ),
    "non_retroactivity": AuditSpec(
        "unavailable",
        "행위시법·신법 적용 쟁점은 형법총칙이고 대상 특별법 주석도 현재 corpus 밖입니다.",
        "형법총칙 죄형법정주의 및 아동·청소년성보호법 주석",
    ),
    "objective_attribution": AuditSpec(
        "partial_context_only",
        "과실치사상·강도치사상 조문은 확보되나 객관적 귀속 일반론은 총칙 자료가 필요합니다.",
        "형법총칙 객관적 귀속 주석",
    ),
    "offense_subject_to_complaint": AuditSpec(
        "fully_available_after_mapping_correction",
        "권리행사방해·친족상도례와 고소·공소기각 절차 조문으로 정정했습니다.",
    ),
    "police_stop_questioning": AuditSpec(
        "unavailable",
        "불심검문 근거인 경찰관직무집행법 주석이 현재 corpus 밖입니다.",
        "경찰관직무집행법 주석",
    ),
    "purpose_to_defame": AuditSpec(
        "unavailable",
        "비방 목적은 정보통신망 명예훼손 특별구성요건으로 해당 특별법이 corpus 밖입니다.",
        "정보통신망법 또는 관련 특별법 주석",
    ),
    "quasi_rape_impossible_attempt": AuditSpec(
        "partial_context_only",
        "준강간 제299조와 미수범 제300조는 확보되나 불능미수 일반론은 총칙 쟁점입니다.",
        "형법총칙 불능미수 주석",
    ),
    "relative_property_crime_exception": AuditSpec(
        "fully_available_after_mapping_correction",
        "절도 사안에 맞춰 제328조와 제344조로 축소했고 제344조는 원천 PDF로 보완했습니다.",
    ),
    "secret_recording": AuditSpec(
        "partial_context_only",
        "전문증거 관련 형사소송법 주석은 있으나 녹음 적법성의 특별법 근거가 없습니다.",
        "통신비밀보호법 주석",
    ),
    "sexual_image_threat": AuditSpec(
        "unavailable",
        "촬영물 이용 협박의 근거 특별법이 현재 corpus 밖입니다.",
        "성폭력처벌법 주석",
    ),
    "special_robbery_attempt": AuditSpec(
        "fully_available_after_raw_fallback",
        "특수강도 제334조와 미수범 제342조 원천 PDF를 모두 확보했습니다.",
    ),
    "special_theft_joint_principal": AuditSpec(
        "partial_context_only",
        "특수절도 제331조 주석은 있으나 공동정범 일반론은 총칙 자료가 필요합니다.",
        "형법총칙 공동정범 주석",
    ),
    "status_offense_accomplice": AuditSpec(
        "partial_context_only",
        "공무상비밀누설 제127조 주석은 있으나 신분범 공범 일반론은 총칙 자료가 필요합니다.",
        "형법총칙 신분범·공범 주석",
    ),
    "use_of_force_stop": AuditSpec(
        "unavailable",
        "정지·유형력 행사의 근거인 경찰관직무집행법 주석이 현재 corpus 밖입니다.",
        "경찰관직무집행법 주석",
    ),
    "voluntary_abandonment": AuditSpec(
        "partial_context_only",
        "살인·강간 및 해당 미수 처벌 조문은 확보되나 중지미수 일반론은 총칙 쟁점입니다.",
        "형법총칙 중지미수 주석",
    ),
}

PRIOR_PARTIAL_TAGS = {
    "attempted_murder",
    "causation",
    "commencement_of_execution",
    "forced_indecent_act_indirect_principal",
    "joint_theft_impossible_attempt",
    "murder_attempt",
    "offense_subject_to_complaint",
    "quasi_rape_impossible_attempt",
    "relative_property_crime_exception",
    "secret_recording",
    "special_robbery_attempt",
    "special_theft_joint_principal",
}


def load_inventory() -> list[dict[str, Any]]:
    return [json.loads(line) for line in INVENTORY.read_text(encoding="utf-8").splitlines()]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def raw_article_pdf(spec: TargetSpec) -> Path | None:
    match = re.fullmatch(r"제(\d+)조(?:의(\d+))?", spec.article_no)
    if match is None:
        raise ValueError(f"Unsupported article number: {spec.article_no}")
    base = f"제{int(match.group(1)):04d}조"
    if match.group(2):
        base += f"의{int(match.group(2))}"
    candidates = sorted(
        (RAW_COMMENTARY_ROOT / spec.law_name / "articles").glob(f"{base}_*.pdf")
    )
    if not candidates:
        return None
    if len(candidates) > 1:
        raise ValueError(f"Multiple raw PDFs for {spec.law_name} {spec.article_no}")
    return candidates[0]


def raw_fallback_rows(spec: TargetSpec, pdf_path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages, start=1):
            text = (page.extract_text(layout=True) or "").strip()
            if not text:
                continue
            comment_id = f"raw_{spec.law_id}_{spec.article_no}_p{page_number:03d}"
            rows.append(
                {
                    "comment_id": comment_id,
                    "document_text": text,
                    "document_text_trim": text,
                    "law_id": spec.law_id,
                    "article_no": spec.article_no,
                    "section_path": f"raw_pdf.page_{page_number}",
                    "section_title": f"{spec.article_no} {spec.article_title}",
                    "cited_cases": [],
                    "n_chars": len(text),
                    "source_kind": "raw_pdf_fallback",
                    "source_path": str(pdf_path),
                }
            )
    return rows


def load_commentary_docs() -> tuple[pd.DataFrame, list[dict[str, Any]]]:
    docs = pd.read_parquet(COMMENTARY_PARQUET).copy()
    docs["law_id"] = docs["law_id"].astype(str)
    docs["article_no"] = docs["article_no"].astype(str)
    docs["comment_id"] = docs["comment_id"].astype(str)
    docs["source_kind"] = "parsed_parquet"
    docs["source_path"] = str(COMMENTARY_PARQUET)

    available = set(zip(docs["law_id"], docs["article_no"], strict=True))
    used_target_ids = {
        target_id for target_ids in TAG_TARGETS.values() for target_id in target_ids
    }
    unique_specs = {
        (TARGETS[target_id].law_id, TARGETS[target_id].article_no): TARGETS[target_id]
        for target_id in used_target_ids
    }
    fallback_rows: list[dict[str, Any]] = []
    fallback_files: list[dict[str, Any]] = []
    for key, spec in sorted(unique_specs.items()):
        if key in available:
            continue
        pdf_path = raw_article_pdf(spec)
        if pdf_path is None:
            continue
        rows = raw_fallback_rows(spec, pdf_path)
        if not rows:
            continue
        fallback_rows.extend(rows)
        fallback_files.append(
            {
                "law_id": spec.law_id,
                "law_name": spec.law_name,
                "article_no": spec.article_no,
                "article_title": spec.article_title,
                "path": str(pdf_path),
                "sha256": sha256_file(pdf_path),
                "page_chunks": len(rows),
            }
        )
    if fallback_rows:
        docs = pd.concat([docs, pd.DataFrame(fallback_rows)], ignore_index=True)
    return docs, fallback_files


def as_jsonable(value: Any) -> Any:
    if hasattr(value, "tolist"):
        return value.tolist()
    if pd.isna(value) if not isinstance(value, (list, tuple, dict)) else False:
        return None
    return value


def target_label(target_id: str) -> str:
    spec = TARGETS[target_id]
    return f"{spec.law_name} {spec.article_no} [{spec.article_title}]"


def build_manifest_rows(
    inventory_rows: list[dict[str, Any]], docs: pd.DataFrame
) -> tuple[list[dict[str, Any]], dict[str, set[str]], list[str]]:
    docs_by_target = {
        (str(law_id), str(article_no)): group
        for (law_id, article_no), group in docs.groupby(["law_id", "article_no"])
    }
    tag_items: dict[str, list[str]] = defaultdict(list)
    tag_areas: dict[str, set[str]] = defaultdict(set)
    for row in inventory_rows:
        for tag in row["issue_tags"]:
            tag_items[tag].append(row["sub_question_id"])
            tag_areas[tag].add(row["legal_area"])

    known_tags = set(TAG_TARGETS) | set(UNAVAILABLE_REASONS)
    unmapped_tags = sorted(set(tag_items) - known_tags)
    if unmapped_tags:
        raise ValueError(f"Tags without mapping policy: {', '.join(unmapped_tags)}")

    tag_chunks: dict[str, set[str]] = defaultdict(set)
    manifest_rows: list[dict[str, Any]] = []
    for tag in sorted(tag_items):
        target_ids = TAG_TARGETS.get(tag, ())
        missing_targets: list[str] = []
        target_rows: list[dict[str, Any]] = []
        for target_id in target_ids:
            spec = TARGETS[target_id]
            key = (spec.law_id, spec.article_no)
            target_docs = docs_by_target.get(key)
            chunk_count = 0 if target_docs is None else int(len(target_docs))
            if chunk_count == 0:
                missing_targets.append(target_id)
            else:
                tag_chunks[tag].update(str(value) for value in target_docs["comment_id"].tolist())
            target_rows.append(
                {
                    "target_id": target_id,
                    **asdict(spec),
                    "target_path": f"commentary://{spec.law_id}/{spec.article_no}",
                    "chunk_count": chunk_count,
                }
            )

        limitations = [TAG_LIMITATIONS[tag]] if TAG_LIMITATIONS.get(tag) else []
        if missing_targets:
            limitations.append(
                "No chunks in docs.parquet for: "
                + ", ".join(target_label(target_id) for target_id in missing_targets)
            )

        if target_ids and missing_targets and tag_chunks[tag]:
            status = "mapped_with_corpus_gap"
        elif target_ids and missing_targets:
            status = "target_missing_in_docs"
        elif target_ids and limitations:
            status = "mapped_with_corpus_gap"
        elif target_ids:
            status = "mapped"
        else:
            status = "unavailable_in_current_commentary"

        manifest_rows.append(
            {
                "tag": tag,
                "status": status,
                "legal_areas": sorted(tag_areas[tag]),
                "sub_question_ids": sorted(tag_items[tag]),
                "targets": target_rows,
                "unique_chunk_count": len(tag_chunks[tag]),
                "limitation": " ".join(limitations),
                "unavailable_reason": UNAVAILABLE_REASONS.get(tag, ""),
            }
        )
    return manifest_rows, tag_chunks, unmapped_tags


def build_chunk_rows(docs: pd.DataFrame, tag_chunks: dict[str, set[str]]) -> list[dict[str, Any]]:
    comment_to_tags: dict[str, set[str]] = defaultdict(set)
    for tag, comment_ids in tag_chunks.items():
        for comment_id in comment_ids:
            comment_to_tags[comment_id].add(tag)

    selected = docs[docs["comment_id"].astype(str).isin(comment_to_tags)]
    rows: list[dict[str, Any]] = []
    sorted_selected = selected.sort_values(
        ["law_id", "article_no", "section_path", "comment_id"]
    )
    for record in sorted_selected.to_dict(orient="records"):
        comment_id = str(record["comment_id"])
        rows.append(
            {
                "comment_id": comment_id,
                "used_by_tags": sorted(comment_to_tags[comment_id]),
                "law_id": str(record["law_id"]),
                "article_no": str(record["article_no"]),
                "section_path": str(record["section_path"]),
                "section_title": str(record["section_title"]),
                "n_chars": int(record["n_chars"]),
                "cited_cases": as_jsonable(record.get("cited_cases", [])),
                "source_kind": str(record["source_kind"]),
                "source_path": str(record["source_path"]),
                "document_text": str(record["document_text"]),
            }
        )
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows),
        encoding="utf-8",
    )


def write_review(manifest_rows: list[dict[str, Any]], chunk_rows: list[dict[str, Any]]) -> None:
    status_counts: dict[str, int] = defaultdict(int)
    for row in manifest_rows:
        status_counts[row["status"]] += 1

    lines = [
        "# KCL 형사법 issue tag commentary bundle",
        "",
        "이 파일은 의미검색이나 reranker 점수를 쓰지 않고, `issue_tags`를 조문 metadata에",
        "직접 매핑한 뒤 해당 `(law_id, article_no)` chunk를 전량 수집한 검수본입니다.",
        "",
        "## Summary",
        "",
        f"- Tags: {len(manifest_rows)}",
        f"- Unique commentary chunks: {len(chunk_rows)}",
        f"- Mapped: {status_counts['mapped']}",
        f"- Mapped with corpus gap: {status_counts['mapped_with_corpus_gap']}",
        "- Unavailable in current commentary: "
        f"{status_counts['unavailable_in_current_commentary']}",
        f"- Target missing in docs: {status_counts['target_missing_in_docs']}",
        "- Raw PDF fallback chunks: "
        f"{sum(r['source_kind'] == 'raw_pdf_fallback' for r in chunk_rows)}",
        "- Previously non-mapped tags manually audited: 33/33",
        "- Pool specification: `kcl_criminal_v1_commentary_pool.json`",
        "- Exception audit: `kcl_criminal_v1_non_mapped_audit.md`",
        "",
        "## Tag targets",
        "",
        "| tag | status | chunks | targets / reason | sub_questions |",
        "|---|---|---:|---|---|",
    ]
    for row in manifest_rows:
        if row["targets"]:
            target_text = "<br>".join(
                f"{target['law_name']} {target['article_no']} {target['article_title']}"
                f" ({target['chunk_count']})"
                for target in row["targets"]
            )
            if row["limitation"]:
                target_text += f"<br>gap: {row['limitation']}"
        else:
            target_text = row["unavailable_reason"]
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['tag']}`",
                    row["status"],
                    str(row["unique_chunk_count"]),
                    target_text,
                    ", ".join(f"`{item}`" for item in row["sub_question_ids"]),
                ]
            )
            + " |"
        )

    OUT_REVIEW.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_pool(
    docs: pd.DataFrame,
    manifest_rows: list[dict[str, Any]],
    chunk_rows: list[dict[str, Any]],
    fallback_files: list[dict[str, Any]],
) -> None:
    target_tags: dict[str, set[str]] = defaultdict(set)
    targets: dict[str, dict[str, Any]] = {}
    for row in manifest_rows:
        for target in row["targets"]:
            target_id = target["target_id"]
            target_tags[target_id].add(row["tag"])
            targets[target_id] = target

    selected_targets = []
    for target_id in sorted(targets):
        selected_targets.append(
            {
                **targets[target_id],
                "used_by_tags": sorted(target_tags[target_id]),
            }
        )

    law_names = {"001692": CRIMINAL, "001671": PROCEDURE}
    source_laws = []
    parsed_docs = docs[docs["source_kind"] == "parsed_parquet"]
    for law_id, group in parsed_docs.groupby("law_id"):
        source_laws.append(
            {
                "law_id": str(law_id),
                "law_name": law_names[str(law_id)],
                "rows": int(len(group)),
                "articles": int(group["article_no"].nunique()),
            }
        )

    pool = {
        "version": "1.0.0",
        "selection_basis": "inventory.issue_tags -> explicit (law_id, article_no) metadata targets",
        "selection_policy": {
            "semantic_search": False,
            "embedding_or_reranker": False,
            "unit": ["law_id", "article_no"],
            "include": "all chunks under every selected metadata target",
            "fallback": (
                "when a selected target has a raw article PDF but zero parsed parquet chunks, "
                "include one deterministic text chunk per PDF page"
            ),
            "deduplicate": "comment_id; merge used_by_tags across targets",
            "exclude": (
                "unselected articles, embeddings.npy, search scores, KCL rubric_summary, "
                "and laws absent from the source corpus"
            ),
        },
        "primary_source": {
            "path": str(COMMENTARY_PARQUET),
            "sha256": sha256_file(COMMENTARY_PARQUET),
            "parsed_rows": int(sum(docs["source_kind"] == "parsed_parquet")),
            "laws": sorted(source_laws, key=lambda row: row["law_id"]),
        },
        "raw_pdf_fallbacks": fallback_files,
        "inventory": {
            "path": str(INVENTORY),
            "sha256": sha256_file(INVENTORY),
            "issue_tags": len(manifest_rows),
        },
        "selected": {
            "metadata_targets": len(selected_targets),
            "unique_chunks": len(chunk_rows),
            "parsed_parquet_chunks": sum(
                row["source_kind"] == "parsed_parquet" for row in chunk_rows
            ),
            "raw_pdf_fallback_chunks": sum(
                row["source_kind"] == "raw_pdf_fallback" for row in chunk_rows
            ),
            "excluded_source_rows": len(docs) - len(chunk_rows),
        },
        "targets": selected_targets,
    }
    OUT_POOL.write_text(
        json.dumps(pool, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_non_mapped_audit(manifest_rows: list[dict[str, Any]]) -> None:
    manifest = {row["tag"]: row for row in manifest_rows}
    if set(AUDITED_NON_MAPPED) - set(manifest):
        missing = sorted(set(AUDITED_NON_MAPPED) - set(manifest))
        raise ValueError(f"Audited tags absent from manifest: {missing}")

    outcome_counts = Counter(spec.outcome for spec in AUDITED_NON_MAPPED.values())
    fully_available_count = sum(
        count
        for key, count in outcome_counts.items()
        if key.startswith("fully_available")
    )
    lines = [
        "# KCL commentary 비-mapped 33개 육안 검토",
        "",
        "2026-07-15 기준 기존 `mapped`가 아니었던 33개 issue tag를 원천 PDF,",
        "`docs.parquet`의 `(law_id, article_no)` metadata, 문항의 issue tag 조합으로 전수 검토했습니다.",
        "KCL `rubric_summary`와 의미검색 점수는 mapping 근거로 사용하지 않았습니다.",
        "",
        "## 결과",
        "",
        f"- 검토: {len(AUDITED_NON_MAPPED)}/33",
        "- 원천 PDF fallback 또는 오매핑 정정으로 완전 확보: "
        f"{fully_available_count}",
        f"- 개별 범죄 조문만 확보, 총칙/특별법 gap 유지: {outcome_counts['partial_context_only']}",
        f"- 현재 corpus에서 확보 불가: {outcome_counts['unavailable']}",
        "",
        "| tag | 이전 상태 | 검토 결론 | 현재 상태 | metadata targets | 판단 및 남은 자료 |",
        "|---|---|---|---|---|---|",
    ]
    for tag, audit in sorted(AUDITED_NON_MAPPED.items()):
        row = manifest[tag]
        prior_status = (
            "mapped_with_corpus_gap"
            if tag in PRIOR_PARTIAL_TAGS
            else "unavailable_in_current_commentary"
        )
        targets = "<br>".join(
            f"{target['law_name']} {target['article_no']} ({target['chunk_count']})"
            for target in row["targets"]
        ) or "없음"
        explanation = audit.rationale
        if audit.required_source:
            explanation += f"<br>필요: {audit.required_source}"
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{tag}`",
                    prior_status,
                    audit.outcome,
                    row["status"],
                    targets,
                    explanation,
                ]
            )
            + " |"
        )
    OUT_AUDIT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    inventory_rows = load_inventory()
    docs, fallback_files = load_commentary_docs()
    manifest_rows, tag_chunks, _ = build_manifest_rows(inventory_rows, docs)
    chunk_rows = build_chunk_rows(docs, tag_chunks)
    write_jsonl(OUT_MANIFEST, manifest_rows)
    write_jsonl(OUT_CHUNKS, chunk_rows)
    write_pool(docs, manifest_rows, chunk_rows, fallback_files)
    write_non_mapped_audit(manifest_rows)
    write_review(manifest_rows, chunk_rows)
    print(
        json.dumps(
            {
                "tags": len(manifest_rows),
                "unique_commentary_chunks": len(chunk_rows),
                "manifest": str(OUT_MANIFEST),
                "chunks": str(OUT_CHUNKS),
                "pool": str(OUT_POOL),
                "audit": str(OUT_AUDIT),
                "review": str(OUT_REVIEW),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
