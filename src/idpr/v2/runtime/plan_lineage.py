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

import hashlib
import json
import subprocess
from collections.abc import Mapping
from pathlib import Path

#: manifest에 계보를 적는 키. `step`은 그 단계 자신의 이름으로 남는다.
LINEAGE_KEY = "plan_lineage"

#: 이 단계가 읽은 입력 artifact와 그때의 내용 해시. `{경로: sha256}`.
INPUTS_KEY = "plan_inputs"

#: 이 단계가 읽은 규칙베이스의 해시와 코드 커밋.
DEFINITIONS_KEY = "definitions_sha256"
PRODUCER_KEY = "producer_commit"


class PlanLineageError(ValueError):
    """계보가 끊겼거나, 이 plan이 만들어질 때의 입력과 지금 파일이 다르다."""


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


def artifact_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def definitions_digest(definitions_dir: Path) -> str:
    """규칙베이스 전체의 내용 해시. 파일 이름과 내용만 본다."""
    digest = hashlib.sha256()
    for path in sorted(definitions_dir.glob("*.yaml")):
        digest.update(path.name.encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def _git_commit() -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):  # pragma: no cover - git 없는 환경
        return ""


def provenance(
    inputs: Mapping[str, Path], *, definitions_dir: Path | None = None
) -> dict:
    """이 단계가 무엇을 읽고 만들어졌는지. manifest에 그대로 펼쳐 넣는다.

    입력 경로만 적어 두면 나중에 그 파일이 다시 생성되었을 때 알 방법이 없다. 축별 수정과
    부분 재실행을 섞어 돌리는 동안 정확히 그 조합 -- 옛 상류 artifact + 새 하류 가정 -- 이
    만들어졌고, 아무도 오류를 보지 못했다. 내용 해시가 있으면 그 조합은 다음 소비 지점에서
    바로 걸린다.
    """
    value: dict = {
        INPUTS_KEY: {
            str(path): artifact_digest(path) for _name, path in sorted(inputs.items())
        },
        PRODUCER_KEY: _git_commit(),
    }
    if definitions_dir is not None:
        value[DEFINITIONS_KEY] = definitions_digest(definitions_dir)
    return value


def stale_inputs(plan_path: Path) -> tuple[str, ...]:
    """이 plan의 조상 중 지금 파일이 만들어질 때와 달라진 것들.

    manifest에 입력 해시가 없으면 **확인할 수 없는 것**이지 stale이 아니다. 옛 artifact를
    소급해서 거부하지 않는다 -- 새로 만들어지는 것부터 계보가 검증된다.
    """
    problems: list[str] = []
    seen: set[Path] = set()
    frontier = [plan_path]
    while frontier:
        current = frontier.pop()
        if current in seen:
            continue
        seen.add(current)
        manifest = _manifest(current)
        if manifest is None:
            continue
        recorded = manifest.get(INPUTS_KEY)
        if not isinstance(recorded, Mapping):
            continue
        for raw_path, digest in sorted(recorded.items()):
            path = Path(str(raw_path))
            if not path.exists():
                problems.append(f"{current.name}: input artifact is gone: {path}")
                continue
            if artifact_digest(path) != str(digest):
                problems.append(
                    f"{current.name}: {path} changed after this artifact was built"
                )
                continue
            frontier.append(path)
    return tuple(problems)


def require_fresh_inputs(plan_path: Path) -> None:
    problems = stale_inputs(plan_path)
    if problems:
        raise PlanLineageError("; ".join(problems))


def definitions_drift(plan_path: Path, definitions_dir: Path) -> tuple[str, ...]:
    """이 plan이 만들어질 때의 규칙베이스와 지금 규칙베이스가 다른가.

    입력 artifact 불일치와 달리 이것은 hard-fail로 두지 않는다. Call 2 산출물은 비싸고,
    저작 한 줄을 고쳤다고 그 산출물을 버리게 하면 계약이 아니라 장애가 된다. 대신 실행
    기록에 남겨 판단이 그 사실을 모른 채 내려지지 않게 한다.
    """
    current = definitions_digest(definitions_dir)
    problems: list[str] = []
    seen: set[Path] = set()
    frontier = [plan_path]
    while frontier:
        node = frontier.pop()
        if node in seen:
            continue
        seen.add(node)
        manifest = _manifest(node)
        if manifest is None:
            continue
        recorded = manifest.get(DEFINITIONS_KEY)
        if isinstance(recorded, str) and recorded and recorded != current:
            problems.append(f"{node.name}: built against a different definition registry")
        inputs = manifest.get(INPUTS_KEY)
        if isinstance(inputs, Mapping):
            frontier.extend(Path(str(value)) for value in inputs)
    return tuple(problems)


__all__ = [
    "DEFINITIONS_KEY",
    "INPUTS_KEY",
    "LINEAGE_KEY",
    "PRODUCER_KEY",
    "PlanLineageError",
    "artifact_digest",
    "definitions_digest",
    "definitions_drift",
    "lineage_for_manifest",
    "passed_through",
    "plan_lineage",
    "provenance",
    "require_fresh_inputs",
    "stale_inputs",
]
