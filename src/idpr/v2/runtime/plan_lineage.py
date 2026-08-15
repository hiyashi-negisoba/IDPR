"""plan artifact의 계보 -- 어떤 단계들을 거쳐서 이 plan이 만들어졌는가.

`evaluation_instance_plan.jsonl`은 한 번 만들고 끝나는 파일이 아니다. 기본 planner가 만든
plan 위에 참가 빌더가 target을 얹고, 그 위에 doctrine 빌더가 다시 얹는다. 각 단계는 자기
manifest에 자기 `step` 이름만 적었고, 소비자는 특정 producer의 이름을 하드코딩해서 확인했다.

그래서 실제로는 참가 병합을 **거친** plan인데도, 뒤에 doctrine 단계가 하나 붙었다는 이유만으로
symbolic 단계가 hard-fail했다. 이름을 하나 더 허용하는 것으로 고치면 다음 증강 단계에서 또
끊긴다. 확인해야 하는 것은 마지막 단계의 이름이 아니라 **거쳐 온 단계의 집합**이다.

그래서 여기서 두 가지를 소유한다.

* :func:`lineage_for_manifest` -- 증강 단계가 자기 manifest에 넣을 계보 필드. 입력 plan의
  계보를 이어받고 자기 이름을 끝에 붙인다.
* :func:`plan_lineage` -- 소비자가 읽는 계보. manifest가 없으면 빈 튜플이다.

계보를 이어받지 않는 새 증강 단계는 그 자리에서 가드에 걸린다. 조용히 다른 답을 내지 않는다.
"""

from __future__ import annotations

import json
from pathlib import Path

#: manifest에 계보를 적는 키. `step`은 그 단계 자신의 이름으로 남는다.
LINEAGE_KEY = "plan_lineage"


def _manifest_path(plan_path: Path) -> Path:
    return plan_path.with_suffix(".manifest.json")


def _manifest(plan_path: Path) -> dict | None:
    path = _manifest_path(plan_path)
    if not path.exists():
        return None
    value = json.loads(path.read_text(encoding="utf-8"))
    return value if isinstance(value, dict) else None


def plan_lineage(plan_path: Path) -> tuple[str, ...]:
    """이 plan이 거쳐 온 단계 이름들. 오래된 manifest는 `step` 하나만 있는 것으로 읽는다."""
    manifest = _manifest(plan_path)
    if manifest is None:
        return ()
    recorded = manifest.get(LINEAGE_KEY)
    chain: list[str] = []
    if isinstance(recorded, (list, tuple)):
        chain.extend(str(value) for value in recorded if value)
    step = str(manifest.get("step") or "")
    if step and step not in chain:
        chain.append(step)
    return tuple(chain)


def lineage_for_manifest(input_plan: Path, step: str) -> tuple[str, ...]:
    """증강 단계가 기록할 계보 -- 입력 plan의 계보 + 자기 이름."""
    chain = list(plan_lineage(input_plan))
    if step not in chain:
        chain.append(step)
    return tuple(chain)


def passed_through(plan_path: Path, step: str) -> bool:
    return step in plan_lineage(plan_path)


__all__ = ["LINEAGE_KEY", "lineage_for_manifest", "passed_through", "plan_lineage"]
