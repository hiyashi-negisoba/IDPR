"""재산죄 RuleIR 결정론적 조립 — 사기(제347조)와 **동일 규격** (API 0회).

사기 RuleIR은 terra 1콜 산출이 아니다. terra는 규칙 4개짜리 부분 초안만 냈고, 최종 349 규칙은
`build_fraud_full_rule_ir_candidate.py`가 카드 구동으로 조립했다. 이 스크립트는 그 조립 규격을
죄명-파라미터화해 재산죄 10단위에 적용한다. 규격을 새로 만들지 않는다 — 사기 것이 계약·Scallop
런타임 테스트를 통과한 유일한 규격이다.

사기와 같은 것(규격):
  · 카드마다 `assess_<slug>` 입력 술어 + `satisfied_<slug>` 파생 술어 + satisfied 규칙
    (평가가 satisfied이고 provable일 때만 조건으로 승격)
  · 카드마다 undetermined 규칙(unknown 평가 보존)과 conflict 규칙(satisfied·not_satisfied 동시 증명)
  · component 술어(구성요건 단계) ← 카드 조건의 인정 경로
  · BAR 카드 → `<unit>_not_established`, 필수 positive 카드의 not_satisfied → 불성립
  · `<unit>_has_negative` / `<unit>_has_conflict` 2항 요약
  · `<unit>.core.outcome.established` 단 하나의 규칙에서만 부정 사용(완결 게이트 뒤)
  · 시스템 입력 4개: provable · case_assessment_complete · distinct_entity · `<unit>_case_roles`

죄명마다 달라지는 것(설정):
  · 행위자 역할 슬롯 — preflight `ACTOR_ROLES`
  · component 구성 — 레벨 맵(L0~L4, +L0o/L0p/L3a)에서 유도한다. 사기는 `COMPONENT_SOURCES`를
    손으로 썼는데, 재산죄는 480장이라 레벨 맵이 그 역할을 한다(L0 적격·객체 → object,
    L1 → conduct, L2 → causation, L3 → intent, L4 → completion). L0o/L0p/L3a는 절도·배임처럼
    한 레벨에 결합적(AND) 요건 둘이 섞여 있던 자리만 명시 카드 표로 쪼갠 것이다
    (`CARD_LEVEL_OVERRIDE`, `scripts/build_rule_ir_phase_map.py`) — 나머지 레벨은 그대로 OR다.
  · BAR 카드 — polarity가 negative/exception인 카드 + L6(위법성·책임) 카드
  · 필수 positive 카드 — L0~L4의 positive 카드(그 요건이 명시적으로 not_satisfied면 불성립)
  · 가중 플래그 — L5 카드를 조문별 kind에 묶는다(제330조→nighttime_residential 등)
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from idpr.rulegen import (  # noqa: E402
    RuleIRGenerationContractError,
    RuleIRGenerationProfile,
    RuleIRValidationError,
    render_rule_ir_natural_language_scaffold,
    validate_full_rule_ir_generation,
)

from scripts.build_property_core_norm_card_sets import commentary_index  # noqa: E402
from scripts.build_property_rule_ir_preflight import ACTOR_ROLES  # noqa: E402
from scripts.prepare_fraud_full_rule_ir_generation import (  # noqa: E402
    atom,
    predicate,
    rule,
    source_union,
    string,
    variable,
)

PROP = ROOT / "data/rulegen/property"
UNITS = PROP / "rule_ir_units"
UNIT_MANIFEST = PROP / "rule_ir_unit_manifest.json"
PHASE_MAP = PROP / "rule_ir_phase_map.json"
OUT_DIR = PROP / "rule_ir"
DEFERRED_UNITS = ("relative_property_crime_exception",)
# 공유 수정요소 — 자기 객체·행위가 없고 기본범 결론에 얹힌다
SHARED_UNITS = ("occupational_status", "relative_property_crime_exception")

# 레벨 → component 이름과 정의 (사기 COMPONENT_SOURCES의 역할)
# L0o·L0p·L3a는 component 재분해로 추가됐다 — 절도(소유 AND 점유)·배임(고의 AND 불법이득의사)
# 처럼 한 레벨에 결합적(AND) 요건 둘이 섞여 있던 자리만 쪼갰다. 나머지 단위는 그대로 L0/L3 하나다.
LEVEL_COMPONENTS: dict[str, tuple[str, str]] = {
    "L0": ("object", "객체·적격 요건이 충족됨 — 재물성·타인성·점유·주체 신분"),
    "L0o": ("object_ownership", "객체 요건 중 타인 소유가 인정됨"),
    "L0p": ("object_possession", "객체 요건 중 타인 점유가 인정됨"),
    "L0c": ("custody", "객체 요건 중 행위자의 보관자 지위(위탁관계)가 인정됨"),
    "L0r": ("object_property", "객체 요건 중 재물(강취 대상)이 인정됨 — 재물강취 트랙 전용"),
    "L0b": ("object_benefit", "객체 요건 중 재산상 이익(강취 대상)이 인정됨 — 이득강취 트랙 전용"),
    "L1": ("conduct", "실행행위 요건이 충족됨"),
    "L2": ("causation", "행위와 결과의 연결(인과·귀속)이 인정됨"),
    "L3": ("intent", "주관적 요건이 충족됨 — 고의"),
    "L3a": ("appropriation_intent", "주관적 요건 중 불법영득·이득의사가 인정됨"),
    "L4": ("completion", "단계 요건이 충족됨 — 실행의 착수 이후 기수에 이름"),
    "L4r": ("completion_property", "기수 요건 중 재물강취 기수(배타적 지배 취득)가 인정됨"),
    "L4b": ("completion_benefit", "기수 요건 중 이득강취 기수(이익 이전)가 인정됨"),
}
BAR_LEVEL = "L6"
AGGRAVATION_LEVEL = "L5"

# 한 단위 안에 서로 배타적인 대안적 실행형태가 있으면 등록한다(예: 강도의 재물강취 제1항/
# 이득강취 제2항 — 둘 다 요구되는 AND가 아니라 어느 한쪽으로 성립하는 대안이다). 공유
# component는 그대로 AND, 트랙 전용 component는 그 트랙 안에서만 AND, 트랙끼리는 OR로 성립을
# 낸다. 두 트랙이 동시에 완전히 충족되면 어느 죄명인지 모호해지므로 conflict로 잡아 성립을
# 보류한다 — 사건이 둘 다 만족할 리 없다는 가정으로 임의로 하나를 고르지 않는다.
UNIT_TRACKS: dict[str, dict[str, tuple[str, ...]]] = {
    "robbery": {"property": ("L0r", "L4r"), "benefit": ("L0b", "L4b")},
}

# 부정·예외 카드의 규칙 내 역할은 **카드별 명시 표**에서 읽는다
# (`data/rulegen/property/rule_ir_card_roles.json`, `scripts/build_rule_ir_card_roles.py`).
# 사기 조립기의 `BAR_CARD_IDS`가 손으로 열거된 목록이었던 것과 같은 자리다. 이 자리를 명제 문언
# 정규식으로 채우면 법리 판정이 문자열 매칭으로 결정되고 그것이 그대로 규칙 구조에 박힌다.
CARD_ROLES = ROOT / "data/rulegen/property/rule_ir_card_roles.json"
EXCEPTION_GATE = ROOT / "data/rulegen/exception_polarity_gate.json"


def quarantined_cards(unit: str) -> set[str]:
    """저지 효과를 결론에서 떼어 둘 카드 — `polarity=exception` 미검수분.

    `exception`은 명제가 어느 방향인지 말해 주지 않는데 88장이 성립을 막는 자리에 있다.
    유닛을 잠그면 36개 중 25개가 멈추므로, 카드는 그대로 평가·기록하고 결론에 닿는
    선만 끊는다(검수 003 I).
    """

    if not EXCEPTION_GATE.is_file():
        return set()
    payload = read_json(EXCEPTION_GATE)
    approved = set(payload.get("approved", []))
    return {
        str(row["card_id"])
        for row in payload.get("cards", [])
        if row.get("blocking")
        and row.get("unit_id") == unit
        and row["card_id"] not in approved
    }

# 가중 조문 → 플래그 kind (preflight AGGRAVATION과 같은 열거)
ARTICLE_AGGRAVATION: dict[str, str] = {
    "art330": "nighttime_residential",
    "art331": "special",
    "art332": "habitual",
    "art334": "special",
    "art335": "quasi",
    "art337": "injury",
    "art338": "death",
    "art343": "preparation",
    "art342": "attempt",
    "art356": "occupational",
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                    encoding="utf-8")


def card_slug(card_id: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", card_id.lower()).strip("_")


def input_id(card_id: str) -> str:
    return f"assess_{card_slug(card_id)}"


def condition_id(card_id: str) -> str:
    return f"satisfied_{card_slug(card_id)}"


def module_slug(card_id: str) -> str:
    """카드가 속한 주석서 모듈 — 규칙 id 이름공간(사기의 module_slug와 같은 역할)."""

    head = card_id.split(".")[0]
    return re.sub(r"[^a-z0-9]+", "_", head.lower()).strip("_") or "misc"


class UnitBuilder:
    """단위 하나의 RuleIR을 사기 규격으로 조립한다."""

    def __init__(self, unit: str, card_set: dict[str, Any],
                 phase_rows: list[dict[str, Any]],
                 card_roles: dict[str, dict[str, Any]] | None = None) -> None:
        self.unit = unit
        self.shared = unit in SHARED_UNITS
        self.card_roles = card_roles if card_roles is not None \
            else read_json(CARD_ROLES)["cards"]
        self.card_set = card_set
        self.cards = card_set["cards"]
        self.cards_by_id = {card["id"]: card for card in self.cards}
        self.roles = ACTOR_ROLES[unit]
        self.actor_arguments = [(name, "String") for name in ("case_id", *self.roles)]
        self.assessment_arguments = [
            ("case_id", "String"), ("assessment_id", "String"),
            *[(name, "String") for name in self.roles], ("status", "String"),
        ]
        self.actors = [variable(name) for name in ("case_id", *self.roles)]
        raw_levels = {row["card_id"]: row["level"] for row in phase_rows
                      if row["unit"] == unit}
        # 공유 수정요소(업무자 신분)는 그 자체가 요건이므로 L5를 객체·적격 요건으로 읽는다.
        # 죄명 단위에서는 L5가 기본범 위에 얹히는 가중 플래그다.
        self.levels = {card_id: ("L0" if self.shared and level == AGGRAVATION_LEVEL
                                 else level)
                       for card_id, level in raw_levels.items()}
        self.tracks = UNIT_TRACKS.get(unit, {})
        self.track_levels = {level for levels in self.tracks.values() for level in levels}
        self.predicates: list[dict[str, Any]] = []
        self.rules: list[dict[str, Any]] = []
        self.quarantined = quarantined_cards(unit)

    # ── 분류 ───────────────────────────────────────────────────────────
    def cards_at(self, level: str) -> list[dict[str, Any]]:
        return [card for card in self.cards if self.levels.get(card["id"]) == level]

    def negative_kind(self, card: dict[str, Any]) -> str:
        """카드의 규칙 내 역할 — 명시 표에서 읽는다. 표에 없으면 조립을 중단한다.

        `component`는 요건 인정 경로이므로 positive 카드와 같이 취급한다(빈 문자열).
        """

        needs_role = (card["polarity"] in ("negative", "exception")
                      or self.levels.get(card["id"]) == BAR_LEVEL)
        if not needs_role:
            return ""
        entry = self.card_roles.get(card["id"])
        if entry is None:
            raise SystemExit(
                f"{card['id']}의 역할이 지정되지 않았다 — "
                "scripts/build_rule_ir_card_roles.py에 추가해야 한다")
        role = entry["role"]
        return "" if role == "component" else role

    def bar_cards(self) -> list[dict[str, Any]]:
        """성립을 막는 카드 — 순수 저지형과 경계획정형만. 요건불요·검토필요는 뺀다."""

        return [card for card in self.cards
                if self.negative_kind(card) in ("bar", "boundary")]

    def cards_of_kind(self, kind: str) -> list[dict[str, Any]]:
        return [card for card in self.cards if self.negative_kind(card) == kind]

    def mandatory_cards(self) -> list[dict[str, Any]]:
        """필수 positive 요건 — 명시적 not_satisfied면 불성립을 도출한다.

        트랙 전용 레벨(예: 강도의 재물강취/이득강취)은 뺀다 — 그 요건은 해당 트랙에서만
        필수이지 단위 전체의 필수가 아니라서, 다른 트랙으로 성립하는 사건에서 반대쪽 트랙
        카드가 명시적으로 not_satisfied라고 해서 전체를 저지하면 안 된다.
        """

        return [card for card in self.cards
                if not self.negative_kind(card)
                and self.levels.get(card["id"]) in LEVEL_COMPONENTS
                and self.levels.get(card["id"]) not in self.track_levels]

    def component_id(self, level: str) -> str:
        return f"{self.unit}_{LEVEL_COMPONENTS[level][0]}_satisfied"

    def active_components(self) -> list[str]:
        return [level for level in LEVEL_COMPONENTS
                if any(not self.negative_kind(card) for card in self.cards_at(level))]

    def aggravation_kinds(self) -> dict[str, list[dict[str, Any]]]:
        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for card in self.cards_at(AGGRAVATION_LEVEL):
            article = card["id"].split("_")[0].split(".")[0]
            kind = ARTICLE_AGGRAVATION.get(article)
            if kind:
                grouped[kind].append(card)
        return dict(sorted(grouped.items()))

    # ── 조립 ───────────────────────────────────────────────────────────
    def system_inputs(self) -> None:
        self.predicates.extend([
            predicate("provable", [("case_id", "String"), ("assessment_id", "String")],
                      kind="rule", role="input", origin="system",
                      definition="해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 "
                                 "사용될 수 있음"),
            predicate("case_assessment_complete",
                      [("case_id", "String"), ("defendant_id", "String")],
                      kind="rule", role="input", origin="system",
                      definition="라우터가 선택한 사건 평가 묶음이 유한하고 완결됨 — 이 게이트 뒤 "
                                 "최종 결론 층에서만 부정을 쓴다"),
            predicate("distinct_entity",
                      [("case_id", "String"), ("left_entity_id", "String"),
                       ("right_entity_id", "String")],
                      kind="rule", role="input", origin="system",
                      definition="두 역할에 배정된 entity가 서로 다른 사람임"),
            predicate(f"{self.unit}_case_roles", self.actor_arguments,
                      kind="rule", role="input", origin="system",
                      definition="사건의 행위자 역할 배정 — 슬롯이 달라도 같은 사람일 수 있다"),
        ])

    def card_layer(self) -> None:
        for index, card in enumerate(self.cards, 1):
            card_id = card["id"]
            owner = module_slug(card_id)
            # 계약: standard_input 카드의 입력 술어는 kind="standard"여야 한다.
            # deterministic_rule 카드도 사실 트리거가 필요하므로 입력을 두되 kind="rule"로 둔다
            # (질의문 배선은 standard_input에만 붙는다 — preflight neural_state 항목).
            self.predicates.append(predicate(
                input_id(card_id), self.assessment_arguments,
                kind=("standard" if card["formalization"] == "standard_input" else "rule"),
                role="input", origin="commentary",
                definition=f"이 카드의 사건별 적용 평가: {card['proposition']}",
                cards=[card]))
            self.predicates.append(predicate(
                condition_id(card_id), self.actor_arguments,
                kind="rule", role="derived", origin="commentary",
                definition=f"증명 가능한 평가에서 다음 조건이 충족됨: {card['proposition']}",
                cards=[card]))

            assessment = f"assessment_{index:03d}"
            self.rules.append(rule(
                f"{self.unit}.{owner}.card.{index:03d}.satisfied",
                atom(condition_id(card_id), *self.actors),
                [self.assessment_atom(card_id, "satisfied", assessment),
                 atom("provable", self.actors[0], variable(assessment))],
                [card],
                "이 카드의 사건별 평가가 satisfied이고 provable일 때만 충족 조건으로 승격한다."))

            unknown = f"unknown_assessment_{index:03d}"
            self.rules.append(rule(
                f"{self.unit}.{owner}.card.{index:03d}.undetermined",
                atom(f"{self.unit}_undetermined", self.actors[0], self.actors[1],
                     string(card_id)),
                [self.assessment_atom(card_id, "unknown", unknown),
                 atom("provable", self.actors[0], variable(unknown))],
                [card],
                "관련성이 확인된 평가가 unknown이면 부정으로 접지 않고 미확인 쟁점으로 보존한다."))

            positive, negative = f"positive_{index:03d}", f"negative_{index:03d}"
            self.rules.append(rule(
                f"{self.unit}.{owner}.card.{index:03d}.conflict",
                atom(f"{self.unit}_conflict", self.actors[0], self.actors[1],
                     string(card_id)),
                [self.assessment_atom(card_id, "satisfied", positive),
                 atom("provable", self.actors[0], variable(positive)),
                 self.assessment_atom(card_id, "not_satisfied", negative),
                 atom("provable", self.actors[0], variable(negative))],
                [card],
                "상반된 두 평가가 모두 provable이면 conflict를 드러내고 임의로 하나를 고르지 않는다."))

            not_sat = f"not_satisfied_{index:03d}"
            self.predicates.append(predicate(
                f"not_satisfied_{condition_id(card_id)}", self.actor_arguments,
                kind="rule", role="derived", origin="commentary",
                definition=f"증명 가능한 평가에서 다음 조건이 부인됨: {card['proposition']}",
                cards=[card]))
            self.rules.append(rule(
                f"{self.unit}.{owner}.card.{index:03d}.not_satisfied",
                atom(f"not_satisfied_{condition_id(card_id)}", *self.actors),
                [self.assessment_atom(card_id, "not_satisfied", not_sat),
                 atom("provable", self.actors[0], variable(not_sat))],
                [card],
                "이 카드의 사건별 평가가 not_satisfied이고 provable일 때 부정 조건으로 승격한다."))

    def assessment_atom(self, card_id: str, status: str, assessment: str) -> dict[str, Any]:
        return atom(input_id(card_id), self.actors[0], variable(assessment),
                    *self.actors[1:], string(status))

    def component_layer(self) -> None:
        for level in self.active_components():
            component = self.component_id(level)
            members = [card for card in self.cards_at(level)
                       if not self.negative_kind(card)]
            self.predicates.append(predicate(
                component, self.actor_arguments,
                kind="rule", role="derived", origin="commentary",
                definition=LEVEL_COMPONENTS[level][1], cards=members))
            for branch, card in enumerate(members, 1):
                self.rules.append(rule(
                    f"{self.unit}.{module_slug(card['id'])}.component."
                    f"{component}.{branch:02d}",
                    atom(component, *self.actors),
                    [atom(condition_id(card["id"]), *self.actors)],
                    [card],
                    "해당 승인 카드의 조건을 구성요건 component의 한 인정 경로로 연결한다."))

    def outcome_layer(self) -> None:
        components = [self.component_id(level) for level in self.active_components()]
        bars = self.bar_cards()
        mandatory = self.mandatory_cards()
        elements = f"{self.unit}_elements_satisfied"

        self.predicates.extend([
            predicate(elements, self.actor_arguments,
                      kind="rule", role="derived", origin="commentary",
                      definition="구성요건 component가 모두 충족됨(부정을 쓰지 않는 층)",
                      cards=mandatory),
            predicate(f"{self.unit}_not_established",
                      [("case_id", "String"), ("defendant_id", "String"),
                       ("issue_id", "String")],
                      kind="rule", role="derived", origin="commentary",
                      definition="명시적으로 증명된 불성립 사유 또는 필수요건 부정이 존재함",
                      cards=bars or mandatory),
            predicate(f"{self.unit}_undetermined",
                      [("case_id", "String"), ("defendant_id", "String"),
                       ("issue_id", "String")],
                      kind="rule", role="derived", origin="commentary",
                      definition="관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음",
                      cards=self.cards),
            predicate(f"{self.unit}_conflict",
                      [("case_id", "String"), ("defendant_id", "String"),
                       ("issue_id", "String")],
                      kind="rule", role="derived", origin="commentary",
                      definition="같은 쟁점에 satisfied와 not_satisfied 평가가 모두 증명됨",
                      cards=self.cards),
            predicate(f"{self.unit}_has_negative",
                      [("case_id", "String"), ("defendant_id", "String")],
                      kind="rule", role="derived", origin="commentary",
                      definition="해당 피고인에 관해 하나 이상의 명시적 불성립 사유가 존재함",
                      cards=bars or mandatory),
            predicate(f"{self.unit}_has_conflict",
                      [("case_id", "String"), ("defendant_id", "String")],
                      kind="rule", role="derived", origin="commentary",
                      definition="해당 피고인에 관해 하나 이상의 상충 평가가 존재함",
                      cards=self.cards),
            predicate(f"{self.unit}_established", self.actor_arguments,
                      kind="rule", role="derived", origin="commentary",
                      definition="완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 확정 성립",
                      cards=mandatory),
        ])

        quarantined = [card for card in bars if card["id"] in self.quarantined]
        if quarantined:
            # 평가와 기록은 그대로 두고 결론 연결만 끊는다 — 유닛을 멈추지 않으면서
            # 극성 미검수 카드가 유·무죄를 뒤집는 것만 막는다(검수 003 I).
            self.predicates.append(predicate(
                f"{self.unit}_quarantined_effect",
                [("case_id", "String"), ("defendant_id", "String"),
                 ("issue_id", "String")],
                kind="rule", role="derived", origin="commentary",
                definition="극성이 검수되지 않아 저지 효과를 결론에서 격리한 카드 — "
                           "평가는 되었으나 성립·불성립을 만들지 않는다",
                cards=quarantined))
        for index, card in enumerate(bars, 1):
            head = (f"{self.unit}_quarantined_effect" if card["id"] in self.quarantined
                    else f"{self.unit}_not_established")
            note = ("극성이 검수되지 않은 카드라 저지 효과를 결론에 연결하지 않고 격리해 "
                    "기록만 한다."
                    if card["id"] in self.quarantined else
                    "이 카드의 부정·배제 조건이 충족되면 해당 쟁점에서 성립을 부정한다.")
            self.rules.append(rule(
                f"{self.unit}.{module_slug(card['id'])}.bar.{index:03d}",
                atom(head, self.actors[0], self.actors[1], string(card["id"])),
                [atom(condition_id(card["id"]), *self.actors)],
                [card], note))


        for index, level in enumerate(self.active_components(), 1):
            component_cards = [card for card in self.cards_at(level) if not self.negative_kind(card)]
            if not component_cards:
                continue
            if level in self.track_levels:
                continue

            comp_id = self.component_id(level)
            body_atoms = []
            cards_in_rule = []
            for card in component_cards:
                body_atoms.append(atom(f"not_satisfied_{condition_id(card['id'])}", *self.actors))
                cards_in_rule.append(card)

            self.rules.append(rule(
                f"{self.unit}.component.{level.lower()}.mandatory_negative.{index:02d}",
                atom(f"{self.unit}_not_established", self.actors[0], self.actors[1],
                     string(comp_id)),
                body_atoms,
                cards_in_rule,
                f"구성요건 {level}에 속한 모든 대안 카드가 명시적으로 not_satisfied일 때만 해당 component 불성립을 도출한다."))

        if self.tracks:
            track_component_ids = {self.component_id(level)
                                   for levels in self.tracks.values() for level in levels}
            shared = [component for component in components
                     if component not in track_component_ids]
            track_predicates: dict[str, str] = {}
            for track_name, levels in self.tracks.items():
                track_components = [self.component_id(level) for level in levels
                                    if level in self.active_components()]
                track_cards = [card for card in self.cards
                               if not self.negative_kind(card)
                               and self.levels.get(card["id"]) in levels]
                track_pred = f"{self.unit}_track_{track_name}_satisfied"
                track_predicates[track_name] = track_pred
                self.predicates.append(predicate(
                    track_pred, self.actor_arguments,
                    kind="rule", role="derived", origin="commentary",
                    definition=f"대안적 실행형태 '{track_name}' 트랙의 component가 공유 "
                              "component와 함께 모두 충족됨", cards=track_cards))
                self.rules.append(rule(
                    f"{self.unit}.core.outcome.track.{track_name}",
                    atom(track_pred, *self.actors),
                    [atom(component, *self.actors) for component in shared + track_components],
                    track_cards,
                    f"공유 component와 '{track_name}' 트랙 전용 component를 AND 결합한다."))
                self.rules.append(rule(
                    f"{self.unit}.core.outcome.elements_satisfied.{track_name}",
                    atom(elements, *self.actors),
                    [atom(track_pred, *self.actors)],
                    track_cards,
                    f"'{track_name}' 트랙이 충족되면 구성요건 전체가 충족된 것으로 본다"
                    "(대안적 실행형태이므로 트랙끼리는 OR)."))
            names = list(track_predicates)
            for i in range(len(names)):
                for j in range(i + 1, len(names)):
                    left, right = track_predicates[names[i]], track_predicates[names[j]]
                    self.rules.append(rule(
                        f"{self.unit}.core.outcome.track_conflict."
                        f"{names[i]}_{names[j]}",
                        atom(f"{self.unit}_conflict", self.actors[0], self.actors[1],
                             string(f"dual_track:{names[i]}_{names[j]}")),
                        [atom(left, *self.actors), atom(right, *self.actors)],
                        mandatory,
                        "서로 배타적이어야 할 두 트랙이 동시에 완전히 충족되면 어느 실행형태인지 "
                        "모호해지므로 임의로 하나를 고르지 않고 충돌로 보류한다."))
        else:
            self.rules.append(rule(
                f"{self.unit}.core.outcome.elements_satisfied",
                atom(elements, *self.actors),
                [atom(component, *self.actors) for component in components],
                mandatory,
                "구성요건 component를 AND 결합한다. 가중유형은 여기 섞지 않는다."))

        self.rules.append(rule(
            f"{self.unit}.core.outcome.has_negative",
            atom(f"{self.unit}_has_negative", self.actors[0], self.actors[1]),
            [atom(f"{self.unit}_not_established", self.actors[0], self.actors[1],
                  variable("negative_issue_id"))],
            bars or mandatory,
            "명시적 불성립 사유를 최종 결론 계층에서 검사할 2항 relation으로 모은다."))

        self.rules.append(rule(
            f"{self.unit}.core.outcome.has_conflict",
            atom(f"{self.unit}_has_conflict", self.actors[0], self.actors[1]),
            [atom(f"{self.unit}_conflict", self.actors[0], self.actors[1],
                  variable("conflict_issue_id"))],
            self.cards,
            "카드·결론 충돌을 최종 결론 계층에서 검사할 2항 relation으로 모은다."))

        self.rules.append(rule(
            f"{self.unit}.core.outcome.established",
            atom(f"{self.unit}_established", *self.actors),
            [atom(elements, *self.actors),
             atom("case_assessment_complete", self.actors[0], self.actors[1]),
             atom(f"{self.unit}_has_negative", self.actors[0], self.actors[1],
                  negated=True),
             atom(f"{self.unit}_has_conflict", self.actors[0], self.actors[1],
                  negated=True)],
            mandatory,
            "라우터가 선택한 사건 평가 묶음이 완결된 뒤, 성립 후보에 명시적 불성립 사유와 충돌이 "
            "모두 없을 때만 확정 성립을 출력한다. 이 두 부정은 완결 게이트 뒤 최종 층에서만 쓴다."))

    def annotation_layer(self) -> None:
        """요건불요·경계획정 카드를 결론 밖 신호로 배출한다.

        요건불요는 성립을 막지 않으므로 BAR에 넣을 수 없지만, 그 카드가 무엇을 면제하는지는
        결론 설명에 필요하다. 경계획정은 이 죄의 불성립이면서 **다른 죄로 넘어간다**는 정보라
        불성립과 따로 드러나야 한다(사기 RuleIR이 미해결로 남긴 항목).
        """

        for kind, suffix, definition, note in (
            ("waiver", "requirement_waived",
             "이 죄의 성립에 요구되지 않는 요건이 확인됨 — 성립을 막지 않는다",
             "요건 불요 규칙이므로 불성립 사유로 쓰지 않고 면제 사실만 기록한다."),
            ("boundary", "boundary_shift",
             "이 죄가 아니라 다른 죄로 평가되는 경계 사유가 확인됨",
             "이 죄의 불성립과 함께 다른 죄로 넘어간다는 신호를 남긴다."),
            ("assessment_standard", "assessment_standard",
             "이 요건을 어떤 기준으로 판단하는지 — 기준일 뿐 충족 여부의 결론이 아니다",
             "판단기준은 결론 계층에 연결하지 않는다. 기준으로 성립을 만들거나 막으면 "
             "정의만으로 유·무죄가 갈린다."),
            ("proof_standard", "proof_standard",
             "유죄 인정을 위한 증명·특정 요건 — 구성요건 자체가 아니다",
             "증명요건을 구성요건에 넣으면 '증명이 필요하다는 법리가 참'이라는 이유로 "
             "요건이 인정되는 역전이 생긴다."),
            ("subtype_outcome", "subtype_outcome",
             "같은 죄 안에서 어느 적용유형으로 의율되는지 — 죄 전체의 성립은 유지된다",
             "내부 의율유형이므로 죄의 성부를 바꾸지 않는다."),
            ("post_outcome", "post_outcome",
             "구성요건 판단 뒤에 오는 죄수·처벌 효과",
             "불가벌적 사후행위 등은 구성요건 불성립과 구별해 별도로 기록한다."),
        ):
            members = self.cards_of_kind(kind)
            if not members:
                continue
            relation = f"{self.unit}_{suffix}"
            self.predicates.append(predicate(
                relation, [("case_id", "String"), ("defendant_id", "String"),
                           ("issue_id", "String"), ("value", "String")],
                kind="rule", role="derived", origin="commentary",
                definition=definition, cards=members))
            for index, card in enumerate(members, 1):
                # 답안에 나가는 것은 마지막 인수다. 카드 ID를 그 자리에 두면 내부
                # 식별자가 그대로 노출되므로 검수자가 적은 우리말 값을 쓴다.
                value = self.card_roles[card["id"]]["value"]
                self.rules.append(rule(
                    f"{self.unit}.{module_slug(card['id'])}.{suffix}.{index:03d}",
                    atom(relation, self.actors[0], self.actors[1],
                         string(card["id"]), string(str(value))),
                    [atom(condition_id(card["id"]), *self.actors)],
                    [card], note))

        # 경계획정 카드가 가리키는 후속 죄명을 인수로 배출한다 — 사기가 미해결로 남긴 항목이다.
        referred = [(card, self.card_roles[card["id"]]["refers_to"])
                    for card in self.cards_of_kind("boundary")]
        referred = [(card, crime) for card, crime in referred if crime]
        if referred:
            relation = f"{self.unit}_refers_to_crime"
            self.predicates.append(predicate(
                relation, [("case_id", "String"), ("defendant_id", "String"),
                           ("crime_name", "String")],
                kind="rule", role="derived", origin="commentary",
                definition="이 죄가 아니라 어느 죄로 평가되는지 — 경계획정 카드가 가리키는 죄명",
                cards=[card for card, _ in referred]))
            for index, (card, crime) in enumerate(referred, 1):
                self.rules.append(rule(
                    f"{self.unit}.{module_slug(card['id'])}.refers_to_crime.{index:03d}",
                    atom(relation, self.actors[0], self.actors[1], string(crime)),
                    [atom(condition_id(card["id"]), *self.actors)],
                    [card],
                    "이 죄의 불성립에 그치지 않고 후속 죄명을 명시해 라우터가 다시 묻지 않게 한다."))

    def aggravation_layer(self) -> None:
        kinds = self.aggravation_kinds()
        if not kinds:
            return
        flag = f"{self.unit}_aggravation"
        members = [card for cards in kinds.values() for card in cards]
        self.predicates.append(predicate(
            flag, [("case_id", "String"), ("defendant_id", "String"),
                   ("kind", "String")],
            kind="rule", role="derived", origin="commentary",
            definition="가중유형 플래그 — 기본범 성립 위에 얹히고, 꺼지면 기본범으로 남는다",
            cards=members))
        for kind, cards in kinds.items():
            for index, card in enumerate(cards, 1):
                self.rules.append(rule(
                    f"{self.unit}.aggravation.{kind}.{index:03d}",
                    atom(flag, self.actors[0], self.actors[1], string(kind)),
                    [atom(f"{self.unit}_established", *self.actors),
                     atom(condition_id(card["id"]), *self.actors)],
                    [card],
                    f"기본범이 성립한 위에 {kind} 가중요건이 충족되면 플래그를 켠다."))

    def bridge_layer(self) -> None:
        """공유 수정요소(친족상도례·업무자 신분)가 받는 이음새."""

        if self.shared:
            return
        defendant = "defendant_id" if "defendant_id" in self.roles else self.roles[0]
        owner = "owner_id" if "owner_id" in self.roles else defendant
        possessor = "possessor_id" if "possessor_id" in self.roles else owner
        arguments = [("case_id", "String"), ("crime_id", "String"),
                     ("defendant_id", "String"), ("owner_id", "String"),
                     ("possessor_id", "String")]
        self.predicates.append(predicate(
            "property_crime_established", arguments,
            kind="rule", role="derived", origin="commentary",
            definition="재산죄 성립을 공유 수정요소(친족상도례·업무자 신분)에 넘기는 브리지",
            cards=self.mandatory_cards()))
        self.rules.append(rule(
            f"{self.unit}.core.outcome.bridge",
            atom("property_crime_established", self.actors[0], string(self.unit),
                 variable(defendant), variable(owner), variable(possessor)),
            [atom(f"{self.unit}_established", *self.actors)],
            self.mandatory_cards(),
            "성립 결론을 죄명-불문 브리지 술어로 배출한다. 받는 쪽 규칙은 절차 레이어에서 쓴다."))

    def build(self) -> dict[str, Any]:
        self.system_inputs()
        self.card_layer()
        self.component_layer()
        self.outcome_layer()
        self.annotation_layer()
        self.aggravation_layer()
        self.bridge_layer()
        return {
            "version": "1.1.0",
            "rule_set_id": f"kr.property.{self.unit}.full.v1_candidate",
            "issue_tag": self.unit,
            "status": "draft",
            "legal_review": "pending",
            "source_scope": self.card_set["source_scope"],
            "norm_card_scope": {"card_set_id": self.card_set["card_set_id"],
                                "card_ids": sorted(self.cards_by_id)},
            "predicates": self.predicates,
            "rules": self.rules,
            "legal_review_questions": [
                "component 배정(레벨 맵 유도)이 이 죄명의 구성요건 단계와 맞는지 검토해야 한다.",
                "부정·예외 카드 4분류(저지·요건불요·경계획정·검토필요)가 맞는지 검토해야 한다.",
                (f"자동 분류가 판정하지 못한 카드 {len(self.cards_of_kind('review'))}장은 "
                 "성립 저지인지 인정 경로인지 확정해야 한다."),
                "경계획정 카드가 가리키는 후속 죄명을 술어 인수로 옮길지 검토해야 한다.",
                "가중 플래그의 전제조건을 조문별로 더 좁힐지 검토해야 한다.",
            ],
            "coverage_gaps": self.card_set["coverage_gaps"],
        }


def main() -> None:
    manifest = read_json(UNIT_MANIFEST)
    phase_rows = read_json(PHASE_MAP)["rows"]
    results, failures = [], []

    for entry in manifest["units"]:
        unit = entry["issue_tag"]
        if unit in DEFERRED_UNITS:
            print(f"  {unit:36s} 이월(절차 레이어) — 생성 안 함")
            continue
        card_set = read_json(UNITS / f"{unit}.json")
        commentary: dict[str, Any] = {}
        for article in entry["articles"]:
            chunks, _ = commentary_index(article)
            commentary.update(chunks)

        rule_ir = UnitBuilder(unit, card_set, phase_rows).build()
        profile = RuleIRGenerationProfile.for_crime(unit, ACTOR_ROLES[unit])
        errors: list[str] = []
        try:
            validate_full_rule_ir_generation(rule_ir, commentary, card_set, profile)
        except (RuleIRValidationError, RuleIRGenerationContractError) as exc:
            errors = list(exc.errors)

        write_json(OUT_DIR / f"{unit}_rule_ir_candidate.json", rule_ir)
        if not errors:
            (OUT_DIR / f"{unit}_scaffold.md").write_text(
                render_rule_ir_natural_language_scaffold(rule_ir), encoding="utf-8")
        results.append({"unit": unit, "cards": len(card_set["cards"]),
                        "predicates": len(rule_ir["predicates"]),
                        "rules": len(rule_ir["rules"]),
                        "valid": not errors, "errors": errors})
        state = "valid" if not errors else f"invalid({len(errors)})"
        print(f"  {unit:36s} 카드 {len(card_set['cards']):3d} / 술어 "
              f"{len(rule_ir['predicates']):3d} / 규칙 {len(rule_ir['rules']):4d} / {state}")
        for line in errors[:6]:
            print(f"       - {line}")
        if errors:
            failures.append(unit)

    write_json(OUT_DIR / "build_summary.json", {
        "version": "1.0.0", "api_calls": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "method": "사기(제347조) 조립 규격을 죄명-파라미터화 — LLM 생성 아님",
        "spec_source": "scripts/build_fraud_full_rule_ir_candidate.py",
        "deferred_units": list(DEFERRED_UNITS),
        "units": results,
    })
    total_rules = sum(item["rules"] for item in results)
    print(f"\n단위 {len(results)} / 규칙 {total_rules} / 계약통과 "
          f"{sum(1 for item in results if item['valid'])}")
    if failures:
        raise SystemExit(f"계약 실패 단위: {failures}")


if __name__ == "__main__":
    main()
