"""라우팅될 수 있는 죄는 cue를 갖거나, 없다고 명시되어 있어야 한다.

2026-08-15 재생성에서 Call 1.5가 `derived_offense.special_robbery`의 cue가 없다는 이유로
사건 7번째에서 죽었다. 그 죄는 그 전 사이클에서 라우팅된 적이 없었을 뿐 결함은 계속 있었다.
정적으로 확인 가능한 것을 런타임이 발견하게 두면, 발견 시점이 항상 실행 도중이 된다.
"""

from __future__ import annotations

from pathlib import Path

from idpr.v2.issue_binding import load_binding_seed_cue_catalog, load_unauthored_cue_refs
from idpr.v2.registry import load_definitions
from idpr.v2.routing import router_catalog

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data/v2/binding_seed_cues.yaml"


def test_every_routable_offense_has_a_cue_or_is_declared_unauthored() -> None:
    registry = load_definitions(ROOT / "data/v2/definitions")
    cues = set(load_binding_seed_cue_catalog(CATALOG))
    unauthored = set(load_unauthored_cue_refs(CATALOG))
    routable = {entry.definition_id for entry in router_catalog(registry)}

    missing = sorted(routable - cues - unauthored)
    assert missing == [], (
        f"라우팅 가능한데 cue도 없고 미저작 선언도 없다: {missing}. "
        "Call 1이 이 죄를 고르는 순간 Call 1.5가 그 사건에서 죽는다."
    )


def test_the_unauthored_list_does_not_hide_an_already_authored_cue() -> None:
    """저작해 놓고 목록에 남겨 두면 다음 사람이 없는 구멍을 메우려 한다."""
    cues = set(load_binding_seed_cue_catalog(CATALOG))
    stale = sorted(cues & set(load_unauthored_cue_refs(CATALOG)))

    assert stale == [], f"cue가 이미 있는데 미저작으로 선언되어 있다: {stale}"


def test_the_unauthored_list_names_only_real_offenses() -> None:
    registry = load_definitions(ROOT / "data/v2/definitions")
    unknown = sorted(
        ref
        for ref in load_unauthored_cue_refs(CATALOG)
        if registry.kind_of(ref) not in {"offense", "derived_offense"}
    )

    assert unknown == [], f"registry에 없는 ref가 미저작 목록에 있다: {unknown}"
