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
