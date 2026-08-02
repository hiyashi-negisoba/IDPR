"""The fact layer: what call 1 is allowed to say about a case.

Everything the symbolic layer reasons over is either a fact asserted here or a card
status asserted by call 2. This module fixes the first half: a small set of predicates
with *closed, descriptive* label vocabularies.

Descriptive, not normative
--------------------------
This is the constraint the whole design turns on. A fact may say that 甲 applied physical
force; it may not say that 甲 committed 폭행. It may say that A touched A's own body; it
may not say 추행. It may say money changed hands; it may not say 뇌물.

The reason is that 추행·기망·횡령·배임·절취 are conclusions, and conclusions are what the
cards decide. Putting them in the fact vocabulary would let call 1 settle the normative
question in passing, and the card assessment in call 2 would then be scoring a judgment
the extraction step had already made -- with no reviewed proposition behind it and no
audit trail. Every normative verb is therefore excluded from :data:`ACT_LABELS` by
design, and :func:`test_act_labels_are_descriptive_not_normative` pins that.

The same applies to places (아파트 공용 현관 is a physical location; whether it is 주거 is
제319조's question), to results (골절 is a fact; whether it is 상해 is 제257조's question),
and to roles (사법경찰관 is a status; 절도범 is a verdict).

Why closed vocabularies
-----------------------
An open vocabulary makes the fact layer useless for inference. If call 1 may emit
``act(c, a1, "甲", "협박하여 재물을 교부받음")`` then no rule can match it and no card
assessment can cite it, and the Datalog layer degenerates into whatever the model happened
to phrase -- which is how the previous rulebase ended up with 3,487 relations sharing 8
distinct bodies, 1,592 of them reducing to ``actor ∧ action_committed``. Labels come from
the tables below and the host rejects an unlisted label rather than passing it through.

Predicate count
---------------
Fourteen, against the nine originally sketched. Each addition was forced by a case in
the corpus that cannot otherwise be stated:

``relation``   친족상도례(제328·344조) and every 신분범 turn on a relation between two
               people, which no act predicate expresses.
``holds``      절도·횡령·권리행사방해 turn on who owns, possesses or safekeeps a thing.
``purpose``    목적범 is common here, and the purpose is neither the act nor the result.
               Only purposes the fact pattern *states* are asserted.
``causation``  제263조 동시범 turns on the cause being *undetermined*, which is a third
               value, not the absence of a fact. Encoding it as a missing fact would make
               동시범 indistinguishable from a case where nobody was hurt.
``property_transfer``  재산범은 단순한 현재 점유뿐 아니라 점유가 자발적 교부·위탁·
               무승낙 이동·점유이탈 중 어떤 경위로 바뀌었는지에 따라 갈린다.

``act_time`` was folded into :data:`ACT_CIRCUMSTANCES`, which already had to carry
야간/주간 alongside 흉기소지 and 2인이상공동.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence

#: Fact-layer predicate names, used as the SCL relation names.
PERSON = "person"
ROLE = "role"
ACT = "act"
ACT_TARGET = "act_target"
ACT_OBJECT = "act_object"
ACT_PLACE = "act_place"
ACT_CIRCUMSTANCE = "act_circumstance"
PURPOSE = "purpose"
RESULT = "result"
CAUSATION = "causation"
# ``relation`` is a Scallop reserved word, hence the prefix.
RELATION = "party_relation"
HOLDS = "holds"
PRECEDES = "precedes"
PROPERTY_TRANSFER = "property_transfer"


@dataclass(frozen=True)
class Predicate:
    """One fact-layer relation: its argument names and which argument is label-checked."""

    name: str
    args: tuple[str, ...]
    doc: str
    #: ``(argument index, vocabulary name)`` for every argument that must carry a listed
    #: label. Empty when all arguments are opaque identifiers. A predicate may have more
    #: than one: ``holds`` constrains both the object and how it is held.
    label_args: tuple[tuple[int, str], ...] = ()

    @property
    def arity(self) -> int:
        return len(self.args)

    def scl_declaration(self) -> str:
        """``type act(String, String, String, String)`` with argument names in a trailing
        comment, because Scallop types are positional."""
        types = ", ".join("String" for _ in self.args)
        return f"type {self.name}({types})  // {', '.join(self.args)}"


# --------------------------------------------------------------------------- #
# Label vocabularies -- all descriptive
# --------------------------------------------------------------------------- #

#: Conduct types at the level a witness could describe. Deliberately *not* statutory
#: verbs: 폭행·협박·추행·기망·절취·횡령·배임 are card conclusions, never facts.
#:
#: The mapping is many-to-one on purpose. "주먹으로 얼굴을 때렸다", "발로 복부를 걷어찼다"
#: and "때려눕혔다" are all 유형력행사; which offence that supports is decided downstream
#: from the target, the result and the cards.
ACT_LABELS: tuple[str, ...] = (
    # 신체에 대한 작용
    "유형력행사", "신체구속", "신체접촉", "성기삽입", "약물투여", "방치",
    # 말·의사표시
    "해악고지", "요구", "의사표시", "허위진술", "약속", "권유", "유포고지",
    # 물건·금전의 이동
    "물건이동", "물건교부", "물건수령", "물건사용", "물건파손", "물건은닉",
    "물건반환거부", "금전교부", "금전수령", "금전사용",
    # 문서·기록
    "문서작성", "문서변경", "문서제출", "서명압인", "기록변경",
    # 장소·이동
    "출입", "퇴거거부", "은신", "도주", "연행",
    # 그 밖의 태양
    "방화", "촬영", "부작위", "직무불이행", "자발적중단",
)

#: Statuses a person holds as a matter of fact. Verdicts (절도범, 공범, 정범) are excluded:
#: those are what the symbolic layer concludes.
ROLE_LABELS: tuple[str, ...] = (
    "공무원", "사법경찰관", "검사", "판사", "중재인",
    "증인", "감정인", "통역인", "번역인",
    "의사", "변호사", "업무종사자",
    "피해자", "피의자", "피고인", "참고인", "신고자",
    "미성년자", "심신장애자", "장애인", "임신부",
    # 물건보관자, not 재물보관자: whether the thing is 재물 is 제355조's question.
    "사무위임받은자", "물건보관자", "시설관리자", "거주자",
)

#: Things an act was directed at, named physically.
OBJECT_LABELS: tuple[str, ...] = (
    "금전", "동산", "부동산", "자동차", "동물", "사체",
    "사진", "영상", "문서", "전자기록", "인장", "서명", "기호",
    "신체", "정보", "시설물", "식품", "약물",
)

#: Physical locations. Whether a location counts as 주거 · 건조물 · 방실 · 위요지 is
#: 제319조's question and belongs to a card.
PLACE_LABELS: tuple[str, ...] = (
    "주택내부", "공동주택전유부", "공동주택공용부", "계단", "엘리베이터",
    "건물내부", "사무실", "점포", "숙박시설객실", "공중화장실",
    "담장내부", "노상", "야외", "차량내부", "선박내부", "항공기내부",
)

#: Circumstances of the act that aggravated forms depend on.
ACT_CIRCUMSTANCES: tuple[str, ...] = (
    "야간", "주간", "흉기소지", "위험한물건소지", "2인이상공동", "단독",
    "반복", "업무수행중", "직무수행중", "공개장소", "피해자저항", "피해자애원",
    "자발적중단", "외부적장애",
)

#: Purposes, asserted only where the fact pattern states one.
PURPOSE_LABELS: tuple[str, ...] = (
    "성관계목적", "재물취득목적", "이익취득목적", "체포회피목적",
    "증거인멸목적", "도피시킬목적", "문서사용목적", "손해가할목적",
    "재물탈환저지목적", "처분면탈목적",
)

#: Outcomes, named descriptively. 상해 · 재산상 손해 are conclusions; 신체손상 and
#: 금전이전 are what happened.
RESULT_LABELS: tuple[str, ...] = (
    "사망", "신체손상", "의식상실", "정신적증상", "임신중단",
    "물건파손", "물건점유이전", "금전이전", "권리변동",
    "직무불수행", "결과미발생",
)

#: How a result is attributed to an act. ``불명`` is a value, not a gap: 제263조 동시범
#: exists precisely for the case where the cause cannot be determined, and a missing fact
#: would be indistinguishable from no harm at all.
CAUSATION_LABELS: tuple[str, ...] = ("확정", "불명", "경합", "부정")

#: Relations between two people. Kinship is a fact; whether it satisfies 친족상도례 is
#: 제328조's question.
RELATION_LABELS: tuple[str, ...] = (
    "직계혈족", "방계혈족", "배우자", "사실혼동거", "동거친족", "비동거친족",
    "인척", "고용관계", "사무위임관계", "친구관계", "면식", "무관계",
)

#: How a person stands to a thing. ``타인의 재물`` is the victim holding it as 소유.
HOLD_LABELS: tuple[str, ...] = ("소유", "점유", "보관", "관리", "소지", "무권리")

#: Descriptive origin of a change in possession. These labels say how the thing moved;
#: they do not decide 절취, 편취, 횡령 or any other offence.
TRANSFER_MODE_LABELS: tuple[str, ...] = (
    "자발적교부",
    "무승낙이동",
    "보관위탁",
    "점유이탈",
    "반환",
)

TRANSFER_PURPOSE_LABELS: tuple[str, ...] = (
    "보관",
    "전달",
    "사용허락",
    "채무변제",
    "대가교환",
    "무상양도",
    "목적미기재",
)

VOCABULARIES: Mapping[str, tuple[str, ...]] = {
    "ACT_LABELS": ACT_LABELS,
    "ROLE_LABELS": ROLE_LABELS,
    "OBJECT_LABELS": OBJECT_LABELS,
    "PLACE_LABELS": PLACE_LABELS,
    "ACT_CIRCUMSTANCES": ACT_CIRCUMSTANCES,
    "PURPOSE_LABELS": PURPOSE_LABELS,
    "RESULT_LABELS": RESULT_LABELS,
    "CAUSATION_LABELS": CAUSATION_LABELS,
    "RELATION_LABELS": RELATION_LABELS,
    "HOLD_LABELS": HOLD_LABELS,
    "TRANSFER_MODE_LABELS": TRANSFER_MODE_LABELS,
    "TRANSFER_PURPOSE_LABELS": TRANSFER_PURPOSE_LABELS,
}

#: Conclusions that must never appear as a fact label. Enforced by test rather than by
#: code, because the check is on the tables themselves, not on runtime input.
NORMATIVE_TERMS: tuple[str, ...] = (
    "폭행", "협박", "추행", "간음", "강간", "절취", "강취", "갈취", "기망",
    "횡령", "배임", "위조", "변조", "은닉죄", "침입", "상해", "살해", "뇌물",
    "재산상이익", "주거", "건조물", "방실", "위요지", "절도범", "강도범",
    "공범", "정범", "교사자", "방조자", "친족", "재물",
)


# --------------------------------------------------------------------------- #
# Predicates
# --------------------------------------------------------------------------- #

FACT_PREDICATES: tuple[Predicate, ...] = (
    Predicate(
        PERSON,
        ("case", "entity"),
        "A person appearing in the fact pattern. ``entity`` is the surface anchor "
        "(甲, 乙, A, B), resolved deterministically by the host and never invented.",
    ),
    Predicate(
        ROLE,
        ("case", "entity", "roleLabel"),
        "A status the person holds as a matter of fact. Statuses stack: one entity may "
        "be both 사법경찰관 and 피의자.",
        label_args=((2, "ROLE_LABELS"),),
    ),
    Predicate(
        ACT,
        ("case", "actId", "actorEntity", "actLabel"),
        "One conduct event. ``actId`` is opaque and links the satellite predicates "
        "below; ``actLabel`` describes the conduct, it does not classify it.",
        label_args=((3, "ACT_LABELS"),),
    ),
    Predicate(
        ACT_TARGET,
        ("case", "actId", "entity"),
        "The person the act was directed at. Present even when actor and target are the "
        "same entity, which is how a victim used as an instrument is recorded.",
    ),
    Predicate(
        ACT_OBJECT,
        ("case", "actId", "objectLabel"),
        "The thing the act was directed at.",
        label_args=((2, "OBJECT_LABELS"),),
    ),
    Predicate(
        ACT_PLACE,
        ("case", "actId", "placeLabel"),
        "Where the act occurred, physically.",
        label_args=((2, "PLACE_LABELS"),),
    ),
    Predicate(
        ACT_CIRCUMSTANCE,
        ("case", "actId", "circumstanceLabel"),
        "A circumstance of the act that an aggravated form may depend on.",
        label_args=((2, "ACT_CIRCUMSTANCES"),),
    ),
    Predicate(
        PURPOSE,
        ("case", "actId", "purposeLabel"),
        "A purpose the fact pattern states the act was done with. Inferring an unstated "
        "purpose is a card's job.",
        label_args=((2, "PURPOSE_LABELS"),),
    ),
    Predicate(
        RESULT,
        ("case", "resultLabel", "entity"),
        "An outcome and who it befell. ``결과미발생`` is asserted explicitly so that an "
        "attempt is distinguishable from an unrecorded outcome.",
        label_args=((1, "RESULT_LABELS"),),
    ),
    Predicate(
        CAUSATION,
        ("case", "actId", "resultLabel", "attributionLabel"),
        "How the result is attributed to the act, including ``불명``.",
        label_args=((2, "RESULT_LABELS"), (3, "CAUSATION_LABELS")),
    ),
    Predicate(
        RELATION,
        ("case", "entityA", "entityB", "relationLabel"),
        "A relation between two people. Directed: ``직계혈족(A, B)`` reads A is B's "
        "직계혈족.",
        label_args=((3, "RELATION_LABELS"),),
    ),
    Predicate(
        HOLDS,
        ("case", "entity", "objectLabel", "holdLabel"),
        "How a person stands to a thing.",
        label_args=((2, "OBJECT_LABELS"), (3, "HOLD_LABELS")),
    ),
    Predicate(
        PRECEDES,
        ("case", "earlierActId", "laterActId"),
        "Temporal order between two acts. Required by 준강도(절도 후 폭행) and by every "
        "결과적 가중범.",
    ),
    Predicate(
        PROPERTY_TRANSFER,
        (
            "case",
            "transferId",
            "fromEntity",
            "toEntity",
            "objectLabel",
            "transferMode",
            "transferPurpose",
        ),
        "A grounded change in possession and its stated purpose. The labels are "
        "descriptive inputs to property-offence assessment, never offence conclusions.",
        label_args=(
            (4, "OBJECT_LABELS"),
            (5, "TRANSFER_MODE_LABELS"),
            (6, "TRANSFER_PURPOSE_LABELS"),
        ),
    ),
)

FACT_PREDICATES_BY_NAME: Mapping[str, Predicate] = {
    predicate.name: predicate for predicate in FACT_PREDICATES
}


class FactLabelError(ValueError):
    """Raised when a fact is malformed or carries a label outside its vocabulary."""


def validate_fact(name: str, args: Sequence[str]) -> None:
    """Check one fact against its predicate declaration.

    Raises rather than warning: a fact with an unlisted label cannot match any rule and
    cannot be cited by a card assessment, so accepting it would drop the fact from the
    reasoning while appearing to have recorded it. That silent-drop path is what made the
    previous rulebase impossible to falsify.
    """
    predicate = FACT_PREDICATES_BY_NAME.get(name)
    if predicate is None:
        raise FactLabelError(f"unknown fact predicate {name!r}")
    if len(args) != predicate.arity:
        raise FactLabelError(
            f"{name} takes {predicate.arity} arguments, got {len(args)}: {list(args)}"
        )
    for index, vocabulary_name in predicate.label_args:
        label = args[index]
        if label not in VOCABULARIES[vocabulary_name]:
            raise FactLabelError(
                f"{name} argument {index} ({predicate.args[index]}) has label "
                f"{label!r}, which is not in {vocabulary_name}"
            )


def scl_fact_layer() -> str:
    """The fact layer as Scallop type declarations."""
    lines = [
        "// ── 사실층 ─────────────────────────────────────────────────────",
        "// 콜 1이 채운다. 라벨은 idpr.rulebase.facts의 닫힌 서술 어휘만 허용된다.",
        "// 규범적 결론(폭행·추행·기망·주거…)은 사실이 아니라 카드가 판정한다.",
    ]
    for predicate in FACT_PREDICATES:
        lines.append(predicate.scl_declaration())
    return "\n".join(lines)


def vocabulary_size() -> int:
    return sum(len(labels) for labels in VOCABULARIES.values())
