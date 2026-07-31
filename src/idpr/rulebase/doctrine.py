"""Load the hand-authored doctrine tables: 죄수 and 미수·예비 처벌 규정.

These two tables are the part of the rulebase that cannot be derived. A card says
"주거침입죄는 결합범에 흡수되어 별도로 성립하지 않는다"; turning that into a pair of
article keys is a legal judgment, so it is written down, reviewed, and loaded -- not parsed
out of Korean prose by a heuristic.

Every entry is validated against the corpus on load. An entry naming an article the corpus
does not cover can never fire, and a rule that can never fire is indistinguishable from a
rule that is wrong, so it is an error rather than a warning.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import yaml

PROJECT_ROOT = Path(__file__).resolve().parents[3]
CONCURRENCE_PATH = PROJECT_ROOT / "data/rulebase/concurrence.yaml"
STAGE_PATH = PROJECT_ROOT / "data/rulebase/stage.yaml"

ATTEMPT = "attempt"
PREPARATION = "preparation"

#: Offence names for every article the corpus covers. Display only -- nothing in the
#: reasoning reads these. They exist because a review document showing ``art356`` asks the
#: reviewer to decode article keys, and decoding is where a legal review goes wrong. A test
#: pins that the table stays complete as articles are added.
OFFENSE_NAMES: Mapping[str, str] = {
    "art122": "직무유기",
    "art127": "공무상비밀누설",
    "art129": "수뢰·사전수뢰",
    "art130": "제3자뇌물제공",
    "art133": "뇌물공여·증뢰물전달",
    "art136": "공무집행방해",
    "art137": "위계에 의한 공무집행방해",
    "art151": "범인은닉·도피",
    "art152": "위증·모해위증",
    "art164": "현주건조물방화",
    "art225": "공문서위조·변조",
    "art227": "허위공문서작성",
    "art231": "사문서위조·변조",
    "art234": "위조사문서행사",
    "art239": "사인등의 위조·부정사용",
    "art250": "살인·존속살해",
    "art254": "살인의 미수범",
    "art255": "살인의 예비·음모",
    "art257": "상해·존속상해",
    "art2582_2": "특수상해",
    "art259": "상해치사",
    "art263": "동시범",
    "art267": "과실치사",
    "art268": "업무상과실·중과실 치사상",
    "art297": "강간",
    "art298": "강제추행",
    "art299": "준강간·준강제추행",
    "art300": "강간등의 미수범",
    "art301": "강간등 상해·치상",
    "art319": "주거침입·퇴거불응",
    "art323": "권리행사방해",
    "art328": "친족간의 범행",
    "art329": "절도",
    "art330": "야간주거침입절도",
    "art331": "특수절도",
    "art332": "상습절도",
    "art333": "강도",
    "art334": "특수강도",
    "art335": "준강도",
    "art337": "강도상해·치상",
    "art338": "강도살인·치사",
    "art342": "절도·강도의 미수범",
    "art343": "강도의 예비·음모",
    "art344": "친족간의 범행 준용",
    "art347": "사기",
    "art350": "공갈",
    "art355": "횡령·배임",
    "art356": "업무상횡령·업무상배임",
    "art357": "배임수재·배임증재",
    "art360": "점유이탈물횡령",
    "art366": "재물손괴",
}


def offense_name(article: str) -> str:
    """``art356`` -> ``업무상횡령·업무상배임``, falling back to the key itself."""
    return OFFENSE_NAMES.get(article, article)


# --------------------------------------------------------------------------- #
# The open questions the reviewer has to settle
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Choice:
    """One answerable option, with what it does to the pipeline."""

    label: str
    effect: str


@dataclass(frozen=True)
class Decision:
    """One question for the reviewer.

    A decision is only useful if it can be answered without reading the code, so each one
    carries the options spelled out, what each does, a recommendation with its reason, and
    what happens if it is skipped. Stating the problem without the options is what made the
    first draft of this document unusable.
    """

    key: str
    question: str
    why_it_cannot_be_derived: str
    choices: tuple[Choice, ...]
    recommended: str
    recommendation_reason: str
    default_if_unanswered: str
    affected_entries: tuple[str, ...] = ()


#: What is left to ask once the relations became conditional. The earlier draft asked
#: whether to keep or drop conditional absorptions, which was the wrong question: the
#: condition belongs in the card, not in a keep/drop decision. What remains is whether the
#: offence pairs and the statutory attempt provisions were read correctly.
OPEN_DECISIONS: tuple[Decision, ...] = (
    Decision(
        key="D1",
        question="죄수 카드 12장의 조문 쌍 배정이 맞습니까?",
        why_it_cannot_be_derived=(
            "카드는 죄명을 한국어 산문으로 부릅니다(\"인장위조죄는 사문서위조죄에 "
            "흡수되어\"). 그것을 조문 키 쌍으로 옮기는 것은 법적 판단이라 제가 읽고 "
            "배정했습니다. **조건은 카드에 그대로 남아 있으므로** 조건을 잘못 굳힐 위험은 "
            "없고, 남은 위험은 조문 쌍을 잘못 짚는 것뿐입니다.\n"
            "  아래 '참고 자료'의 표에 카드 명제와 배정된 조문 쌍이 나란히 있습니다."
        ),
        choices=(
            Choice("1. 맞다", "표를 그대로 씁니다."),
            Choice(
                "2. 고칠 것이 있다",
                "틀린 항목의 조문 쌍만 적어 주시면 반영합니다. "
                "예: \"사기→횡령은 반대다\"",
            ),
        ),
        recommended="1",
        recommendation_reason=(
            "조건이 카드에 남으면서 앞서 문제였던 두 충돌이 사라졌습니다. 방화↔살인은 "
            "\"사망하지 않은 경우\" 카드가 조건이라 사망 사안에서는 발화하지 않고, "
            "예비·음모↔살인은 흡수와 상상적 경합이 서로 다른 카드를 조건으로 갖게 되어 "
            "동시에 발화하지 않습니다."
        ),
        default_if_unanswered="표를 그대로 씁니다.",
        affected_entries=(
            "제255조 살인예비·음모 → 제254조 흡수 항목은 제가 **뺐습니다**. 제254조는 "
            "미수범 처벌 조문이지 독립 죄명이 아니라 `offense_established`가 발화할 일이 "
            "없어 죽은 규칙입니다. 되살릴 필요가 있으면 알려 주세요.",
        ),
    ),
    Decision(
        key="D2",
        question="미수범 처벌 규정 표(17개 조문)에 틀린 것이나 빠진 것이 있습니까?",
        why_it_cannot_be_derived=(
            "제342조가 \"제329조 내지 제341조의 미수범을 처벌한다\"고만 말하므로 그 열거를 "
            "조문별로 펼친 것은 제 작업입니다. 카드가 조문별로 말해 주지 않습니다. "
            "또 제301조(강간등 상해·치상)의 미수 처벌 여부를 명시한 카드가 없어 표에 넣지 "
            "않았습니다."
        ),
        choices=(
            Choice("1. 맞다", "표를 그대로 씁니다."),
            Choice(
                "2. 고칠 것이 있다",
                "빼야 할 조문과 넣어야 할 조문을 적어 주시면 반영합니다.",
            ),
        ),
        recommended="1",
        recommendation_reason=(
            "제342조·제300조·제254조의 열거를 조문 텍스트대로 펼친 것이라 큰 오류는 없을 "
            "것으로 봅니다. 다만 제332조(상습절도)·제334조(특수강도)처럼 제가 펼쳐 넣은 "
            "항목은 한 번 훑어봐 주시면 좋겠습니다."
        ),
        default_if_unanswered="표를 그대로 씁니다.",
    ),
    Decision(
        key="D3",
        question="예비·음모 처벌 규정 표(제250·299·333조)가 맞습니까?",
        why_it_cannot_be_derived=(
            "예비·음모 처벌 규정은 조문에 흩어져 있고(제255조가 살인, 제343조가 강도) "
            "카드가 전수를 진술하지 않습니다. 빠진 조문이 있을 수 있습니다."
        ),
        choices=(
            Choice("1. 맞다", "표를 그대로 씁니다."),
            Choice("2. 빠진 조문이 있다", "적어 주시면 넣습니다."),
        ),
        recommended="1",
        recommendation_reason=(
            "실체법 28문항에서 예비·음모가 쟁점이 되는 것은 강도예비와 살인예비 정도로 "
            "보이므로 이 3개로 시작해도 무리가 없다고 봅니다."
        ),
        default_if_unanswered="표를 그대로 씁니다.",
    ),
)


#: Condition value meaning "this relation always holds". Used only where the source card
#: states the relation without a conditional clause.
UNCONDITIONAL = "unconditional"


class DoctrineError(ValueError):
    """Raised when a doctrine table is malformed or names an offence the corpus lacks."""

    def __init__(self, errors: Sequence[str]) -> None:
        self.errors = list(errors)
        super().__init__("; ".join(self.errors))


@dataclass(frozen=True)
class DoctrineTables:
    """The loaded tables, ready to be compiled into data tuples.

    The concurrence relations carry a third element: the id of the card whose proposition
    is the condition. 죄수 관계는 거의 언제나 조건부이고 -- "은폐할 목적으로 …한 경우에는"
    -- an offence pair on its own has nowhere to put that clause, so a two-column table
    silently promotes a conditional rule into an unconditional one. Keeping the card as the
    condition means the reviewed proposition stays the thing that decides.
    """

    absorbed_by: tuple[tuple[str, str, str], ...]
    imaginative_concurrence: tuple[tuple[str, str, str], ...]
    attempt_punishable: tuple[str, ...]
    preparation_punishable: tuple[str, ...]
    #: ``(offense, stage)`` pairs a card positively states are *not* punishable. Recorded
    #: so "absent from the table" and "no such provision" stay distinguishable.
    not_punishable: tuple[tuple[str, str], ...]
    awaiting_review: bool

    @property
    def review_flagged(self) -> bool:
        return self.awaiting_review


DOCTRINE_REVIEW_PATH = PROJECT_ROOT / "data/rulebase/doctrine_review.md"

_DECISION_HEADER_RE = re.compile(r"^##\s+(D\d+)\.")
_ANSWER_RE = re.compile(r"^>\s*answer:\s*(.*)$")


def parse_decision_answers(path: Path | None = None) -> Mapping[str, str]:
    """Read the reviewer's ``> answer:`` lines out of the review document.

    Same contract as :mod:`idpr.rulebase.review`: the markdown the reviewer edits is the
    source of truth, and blank answers are omitted rather than recorded as empty, so an
    unanswered decision is visibly unanswered.
    """
    text = (path or DOCTRINE_REVIEW_PATH).read_text(encoding="utf-8")
    answers: dict[str, str] = {}
    current = ""
    for line in text.splitlines():
        header = _DECISION_HEADER_RE.match(line)
        if header:
            current = header.group(1)
            continue
        answer = _ANSWER_RE.match(line)
        if answer and current:
            body = answer.group(1).strip()
            if body:
                answers[current] = body
    return answers


def unanswered_decisions(answers: Mapping[str, str]) -> tuple[str, ...]:
    return tuple(d.key for d in OPEN_DECISIONS if d.key not in answers)


def _load_yaml(path: Path) -> Mapping[str, Any]:
    if not path.is_file():
        raise DoctrineError([f"missing doctrine table {path}"])
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise DoctrineError([f"{path.name}: top level must be a mapping"])
    return loaded


def _entries(payload: Mapping[str, Any], key: str) -> list[Mapping[str, Any]]:
    value = payload.get(key) or []
    if not isinstance(value, list):
        raise DoctrineError([f"{key} must be a list, got {type(value).__name__}"])
    return [entry for entry in value if isinstance(entry, dict)]


def load_doctrine(
    known_articles: Iterable[str],
    concurrence_path: Path | None = None,
    stage_path: Path | None = None,
    assessable_cards: Iterable[str] | None = None,
) -> DoctrineTables:
    """Read both tables and check every key against the corpus.

    ``assessable_cards`` is the set of card ids call 2 is asked to judge. A condition
    naming a card outside it can never become ``satisfied``, so the relation would never
    fire -- the same silent-death failure as an offence key outside the corpus.
    """
    known = set(known_articles)
    assessable = set(assessable_cards) if assessable_cards is not None else None
    errors: list[str] = []

    concurrence = _load_yaml(concurrence_path or CONCURRENCE_PATH)
    stage = _load_yaml(stage_path or STAGE_PATH)

    def check(article: Any, where: str) -> bool:
        if not isinstance(article, str) or not article:
            errors.append(f"{where}: offence key must be a non-empty string")
            return False
        if article not in known:
            errors.append(f"{where}: {article} is not an article in the corpus")
            return False
        return True

    def condition(entry: Mapping[str, Any], where: str) -> str | None:
        value = entry.get("condition")
        if not isinstance(value, str) or not value:
            errors.append(
                f"{where}: condition must be a card id or {UNCONDITIONAL!r}. "
                f"죄수 관계는 조건부가 기본이므로 생략을 무조건으로 읽지 않는다."
            )
            return None
        if value == UNCONDITIONAL:
            return value
        if assessable is not None and value not in assessable:
            errors.append(
                f"{where}: condition card {value} is not assessed by call 2, so its "
                f"status can never be satisfied and this relation would never fire"
            )
            return None
        return value

    absorbed: list[tuple[str, str, str]] = []
    for index, entry in enumerate(_entries(concurrence, "absorbed_by")):
        where = f"concurrence.absorbed_by[{index}]"
        child, parent = entry.get("child"), entry.get("parent")
        # Every check runs before the conjunction: short-circuiting would report one bad
        # key per run, defeating the point of collecting every error.
        child_ok = check(child, f"{where}.child")
        parent_ok = check(parent, f"{where}.parent")
        cond = condition(entry, where)
        if child_ok and parent_ok and cond is not None:
            if child == parent:
                errors.append(f"{where}: an offence cannot absorb itself")
            else:
                absorbed.append((child, parent, cond))

    imaginative: list[tuple[str, str, str]] = []
    for index, entry in enumerate(
        _entries(concurrence, "imaginative_concurrence")
    ):
        where = f"concurrence.imaginative_concurrence[{index}]"
        offences = entry.get("offenses")
        cond = condition(entry, where)
        if not isinstance(offences, list) or len(offences) != 2:
            errors.append(f"{where}: offenses must be a pair")
            continue
        first, second = offences
        first_ok = check(first, f"{where}[0]")
        second_ok = check(second, f"{where}[1]")
        if first_ok and second_ok and cond is not None:
            if first == second:
                errors.append(f"{where}: an offence cannot concur with itself")
            else:
                # Symmetric relation, stored once in sorted order so the compiled tuples
                # are stable and the rule need not be written both ways.
                low, high = sorted((first, second))
                imaginative.append((low, high, cond))

    attempt: list[str] = []
    for index, entry in enumerate(_entries(stage, "attempt_punishable")):
        where = f"stage.attempt_punishable[{index}]"
        if check(entry.get("offense"), where):
            attempt.append(entry["offense"])

    preparation: list[str] = []
    for index, entry in enumerate(_entries(stage, "preparation_punishable")):
        where = f"stage.preparation_punishable[{index}]"
        if check(entry.get("offense"), where):
            preparation.append(entry["offense"])

    not_punishable: list[tuple[str, str]] = []
    for index, entry in enumerate(_entries(stage, "not_punishable")):
        where = f"stage.not_punishable[{index}]"
        stage_name = entry.get("stage")
        if stage_name not in {ATTEMPT, PREPARATION}:
            errors.append(f"{where}: stage must be {ATTEMPT!r} or {PREPARATION!r}")
            continue
        if check(entry.get("offense"), where):
            not_punishable.append((entry["offense"], stage_name))

    for offence, stage_name in not_punishable:
        table = attempt if stage_name == ATTEMPT else preparation
        if offence in table:
            errors.append(
                f"stage: {offence} is listed both as {stage_name}-punishable and not"
            )

    duplicates = sorted({a for a in attempt if attempt.count(a) > 1})
    if duplicates:
        errors.append(f"stage.attempt_punishable has duplicates: {duplicates}")

    if errors:
        raise DoctrineError(errors)

    awaiting = "awaiting" in str(concurrence.get("status", "")) or "awaiting" in str(
        stage.get("status", "")
    )
    return DoctrineTables(
        absorbed_by=tuple(sorted(set(absorbed))),
        imaginative_concurrence=tuple(sorted(set(imaginative))),
        attempt_punishable=tuple(sorted(set(attempt))),
        preparation_punishable=tuple(sorted(set(preparation))),
        not_punishable=tuple(sorted(set(not_punishable))),
        awaiting_review=awaiting,
    )
