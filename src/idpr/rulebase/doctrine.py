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


#: The asymmetry that drives most of the recommendations below: absorption is the only rule
#: that *removes* an offence from the final list, and the rubric scores recall with no
#: precision penalty. A wrong absorption costs rubric items; a missing one costs an extra
#: offence name in the answer, which costs nothing.
_RECALL_ASYMMETRY = (
    "흡수는 죄명을 **지우는** 유일한 규칙입니다. rubric은 순수 리콜 채점(정밀도 페널티 "
    "없음)이라, 흡수가 틀리면 채점 항목을 잃고, 흡수가 빠지면 답안에 죄명이 하나 더 "
    "언급될 뿐 감점이 없습니다. 확신이 없으면 빼는 쪽이 안전합니다."
)

OPEN_DECISIONS: tuple[Decision, ...] = (
    Decision(
        key="D1",
        question=(
            "조건부이거나 방향이 이례적인 흡수 규칙 3건을 표에 남길까요, 뺄까요?"
        ),
        why_it_cannot_be_derived=(
            "근거 카드가 조건을 달고 있는데(\"위법사실을 적극 은폐할 목적으로 …한 경우\") "
            "표는 조문 쌍만 담아서 조건을 실을 수 없습니다. 조건 없이 넣으면 조건이 없는 "
            "사안에서도 죄명이 지워집니다."
        ),
        choices=(
            Choice(
                "1. 3건 모두 뺀다",
                "조건이 맞는 사안에서 흡수되어야 할 죄명이 최종 목록에 남습니다. "
                "답안에 죄명이 하나 더 언급됩니다.",
            ),
            Choice(
                "2. 3건 모두 남긴다",
                "조건이 아닌 사안에서도 죄명이 최종 목록에서 빠집니다. "
                "그 죄명에 걸린 rubric 항목을 잃습니다.",
            ),
            Choice(
                "3. 항목별로 지정한다",
                "예: \"제122조는 빼고 제347조는 남긴다\"처럼 적어 주시면 그대로 반영합니다.",
            ),
        ),
        recommended="1",
        recommendation_reason=_RECALL_ASYMMETRY,
        default_if_unanswered="현재대로 3건 모두 남습니다(선택지 2).",
        affected_entries=(
            "제122조 직무유기 → 제227조 허위공문서작성  "
            "(근거 카드가 \"위법사실을 적극 은폐할 목적으로\"를 조건으로 답니다. "
            "같은 조문에 \"은폐 목적이 아니면 실체적 경합\"이라는 반대 카드가 있습니다)",
            "제347조 사기 → 제355조 횡령·배임  "
            "(흡수 방향이 통상과 반대로 읽힙니다)",
            "제255조 살인예비·음모 → 제254조 살인의 미수범  "
            "(제254조는 미수범 처벌 조문이지 독립 죄명이 아니라서, 죄명으로 성립할 일이 "
            "없어 이 규칙은 발화하지 못할 가능성이 큽니다)",
        ),
    ),
    Decision(
        key="D2",
        question=(
            "제255조 살인예비·음모와 제250조 살인의 관계를 흡수로 볼까요, "
            "상상적 경합으로 볼까요?"
        ),
        why_it_cannot_be_derived=(
            "제가 두 관계를 동시에 넣었습니다. 근거 카드가 서로 다른 상황을 말하는데 "
            "(실행의 착수가 있었는가) 조문 쌍만으로는 그 구분을 담을 수 없습니다.\n"
            "  · 흡수 근거: \"살인예비·음모가 살인미수 또는 살인기수 단계에 이르면 "
            "예비·음모죄는 미수 또는 기수죄에 흡수된다\"\n"
            "  · 상상적 경합 근거: \"살인을 교사하였으나 피교사자가 상해행위만 한 경우 … "
            "상상적 경합으로 더 무거운 살인예비·음모죄로 처벌한다\""
        ),
        choices=(
            Choice(
                "1. 흡수만 남긴다",
                "살인이 성립하면 예비·음모가 최종 죄명에서 빠집니다. "
                "상상적 경합 항목을 지웁니다.",
            ),
            Choice(
                "2. 상상적 경합만 남긴다",
                "두 죄가 다 최종 죄명이 되고 관계만 보고됩니다. 흡수 항목을 지웁니다.",
            ),
            Choice(
                "3. 둘 다 남긴다 (현재 상태)",
                "예비·음모가 최종 죄명에서 빠지면서 동시에 상상적 경합으로도 보고됩니다. "
                "출력이 서로 모순되어 보입니다.",
            ),
        ),
        recommended="1",
        recommendation_reason=(
            "상상적 경합 근거 카드의 사안은 **피교사자가 실행에 착수하지 않은** 경우라 "
            "살인죄(art250) 자체가 성립하지 않습니다. 두 죄가 동시에 성립할 때만 "
            "상상적 경합 규칙이 발화하므로, 그 항목은 실제로는 발화할 일이 없습니다."
        ),
        default_if_unanswered="현재대로 둘 다 남아 모순된 출력이 납니다(선택지 3).",
    ),
    Decision(
        key="D3",
        question=(
            "제164조 현주건조물방화와 제250조 살인을 상상적 경합으로 남길까요?"
        ),
        why_it_cannot_be_derived=(
            "같은 조문(art250)에 정반대 카드가 있고, 사망 결과가 발생했는지로 갈립니다.\n"
            "  · 남기는 근거: \"방화하였으나 사망하지 않은 경우 현주건조물방화죄와 "
            "살인미수죄의 상상적 경합범이 된다\"\n"
            "  · 빼는 근거: \"살해할 목적으로 방화하여 사망하게 한 경우 "
            "현주건조물방화치사죄로 의율하며 살인죄와 상상적 경합으로 의율하지 않는다\""
        ),
        choices=(
            Choice(
                "1. 남긴다",
                "사망하지 않은 사안에서 관계가 정확히 보고됩니다. 사망한 사안에서는 "
                "불필요한 관계 표기가 하나 붙습니다.",
            ),
            Choice(
                "2. 뺀다",
                "사망한 사안에서 깔끔합니다. 사망하지 않은 사안에서 상상적 경합 관계가 "
                "보고되지 않습니다.",
            ),
        ),
        recommended="1",
        recommendation_reason=(
            "상상적 경합은 흡수와 달리 죄명을 지우지 않고 관계만 덧붙입니다. 틀렸을 때의 "
            "손해가 표기 하나이고, 빠졌을 때는 rubric의 죄수 항목을 잃습니다."
        ),
        default_if_unanswered="현재대로 남습니다(선택지 1 = 추천).",
    ),
    Decision(
        key="D4",
        question="미수범 처벌 규정 표(17개 조문)에 틀린 것이나 빠진 것이 있습니까?",
        why_it_cannot_be_derived=(
            "제342조가 \"제329조 내지 제341조의 미수범을 처벌한다\"고만 말하므로, 그 열거를 "
            "조문별로 펼친 것은 제 작업입니다. 카드가 조문별로 말해 주지 않습니다. "
            "또 제301조(강간등 상해·치상)의 미수 처벌 여부를 명시한 카드가 없어 "
            "표에 넣지 않았습니다."
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
            "제342조·제300조·제254조의 열거를 조문 텍스트대로 펼친 것이므로 큰 오류는 없을 "
            "것으로 봅니다. 다만 제332조(상습절도)·제334조(특수강도)처럼 제가 펼쳐 넣은 "
            "항목은 한 번 훑어봐 주시면 좋겠습니다."
        ),
        default_if_unanswered="표를 그대로 씁니다.",
    ),
    Decision(
        key="D5",
        question="예비·음모 처벌 규정 표(제250·299·333조)가 맞습니까?",
        why_it_cannot_be_derived=(
            "예비·음모 처벌 규정은 조문에 흩어져 있고(제255조가 살인, 제343조가 강도), "
            "카드가 전수를 진술하지 않습니다. 빠진 조문이 있을 수 있습니다."
        ),
        choices=(
            Choice("1. 맞다", "표를 그대로 씁니다."),
            Choice("2. 빠진 조문이 있다", "적어 주시면 넣습니다."),
        ),
        recommended="1",
        recommendation_reason=(
            "실체법 28문항에서 예비·음모가 쟁점이 되는 것은 강도예비(스모크 케이스 아님)와 "
            "살인예비 정도로 보이므로, 이 3개로 시작해도 무리가 없다고 봅니다."
        ),
        default_if_unanswered="표를 그대로 씁니다.",
    ),
)


class DoctrineError(ValueError):
    """Raised when a doctrine table is malformed or names an offence the corpus lacks."""

    def __init__(self, errors: Sequence[str]) -> None:
        self.errors = list(errors)
        super().__init__("; ".join(self.errors))


@dataclass(frozen=True)
class DoctrineTables:
    """The loaded tables, ready to be compiled into data tuples."""

    absorbed_by: tuple[tuple[str, str], ...]
    imaginative_concurrence: tuple[tuple[str, str], ...]
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
) -> DoctrineTables:
    """Read both tables and check every offence key against the corpus."""
    known = set(known_articles)
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

    absorbed: list[tuple[str, str]] = []
    for index, entry in enumerate(_entries(concurrence, "absorbed_by")):
        where = f"concurrence.absorbed_by[{index}]"
        child, parent = entry.get("child"), entry.get("parent")
        # Both are checked before the conjunction: short-circuiting would report one bad
        # key per run, defeating the point of collecting every error.
        child_ok = check(child, f"{where}.child")
        parent_ok = check(parent, f"{where}.parent")
        if child_ok and parent_ok:
            if child == parent:
                errors.append(f"{where}: an offence cannot absorb itself")
            else:
                absorbed.append((child, parent))

    imaginative: list[tuple[str, str]] = []
    for index, entry in enumerate(
        _entries(concurrence, "imaginative_concurrence")
    ):
        where = f"concurrence.imaginative_concurrence[{index}]"
        offences = entry.get("offenses")
        if not isinstance(offences, list) or len(offences) != 2:
            errors.append(f"{where}: offenses must be a pair")
            continue
        first, second = offences
        first_ok = check(first, f"{where}[0]")
        second_ok = check(second, f"{where}[1]")
        if first_ok and second_ok:
            if first == second:
                errors.append(f"{where}: an offence cannot concur with itself")
            else:
                # Symmetric relation, stored once in sorted order so the compiled tuples
                # are stable and the rule need not be written both ways.
                imaginative.append(tuple(sorted((first, second))))  # type: ignore[arg-type]

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
