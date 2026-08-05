"""`polarity=exception` 카드가 어느 역할로 컴파일되는지 전수 노출한다 (API 0회).

배치 001에서 극성 기반으로 역할 오배치를 훑었을 때 이 카드들이 **전부 통과했다**.
`positive`도 `negative`도 아닌 값이라 "부정 카드인가"라는 물음에 걸리지 않았기 때문이다.
극성이 셋으로 갈리면서 `norm_kind`의 예외 여부와 명제의 방향이 한 필드에 뭉개졌고,
그 결과 "요건이 필요 없다"는 확인 법리가 `bar`로 앉아 죄를 불성립시키는 사고
(상해죄·방화죄)를 걸러내지 못했다.

이 감사는 두 가지를 한다.

1. 141장이 각각 어느 유닛에서 어느 역할로 컴파일되는지 표로 뽑는다.
2. 그 중 성립을 막는 역할(bar/boundary/waiver)에 앉은 것을 게이트 대상으로 표시한다.

게이트를 실제로 잠그면(`enforce: true`) 36개 유닛 중 26개가 실행되지 않는다. 그래서
기본값은 잠그지 않고 노출만 하며, 별도 검수 배치에서 극성을 positive/negative로 복구한
카드를 `approved`에 적어 하나씩 풀어 간다. `norm_kind=exception`은 규범의 성질이므로
건드리지 않는다 — 고치는 것은 `polarity`뿐이다.
"""

from __future__ import annotations

import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

P2_LEDGERS = ROOT / "data/rulegen/p2/native_review"
P2_CARD_SETS = ROOT / "data/rulegen/p2/rule_ir"
PROP_UNITS = ROOT / "data/rulegen/property/rule_ir_units"
PROP_ROLES = ROOT / "data/rulegen/property/rule_ir_card_roles.json"
OUT = ROOT / "data/rulegen/exception_polarity_gate.json"

BLOCKING_ROLES = ("bar", "boundary", "waiver")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def collect() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    polarity: dict[str, str] = {}
    proposition: dict[str, str] = {}
    for path in sorted(P2_CARD_SETS.glob("*_norm_card_set.json")):
        for card in read_json(path).get("cards", []):
            polarity[card["id"]] = card.get("polarity", "")
            proposition[card["id"]] = card.get("proposition", "")
    for path in sorted(P2_LEDGERS.glob("*_decision_ledger.json")):
        ledger = read_json(path)
        for placement in ledger["placements"]:
            card_id = placement["card_id"]
            if polarity.get(card_id) != "exception":
                continue
            rows.append({
                "system": "p2",
                "unit_id": ledger["unit_id"],
                "card_id": card_id,
                "role": placement["role"],
                "blocking": placement["role"] in BLOCKING_ROLES,
                "proposition": proposition.get(card_id, ""),
            })

    roles = read_json(PROP_ROLES)["cards"]
    for path in sorted(PROP_UNITS.glob("*.json")):
        unit = read_json(path)
        for card in unit.get("cards", []):
            if card.get("polarity") != "exception":
                continue
            # 역할표에 없는 카드는 재산죄 조립기가 긍정 경로로 취급한다.
            role = (roles.get(card["id"]) or {}).get("role", "component")
            rows.append({
                "system": "property",
                "unit_id": unit["issue_tag"],
                "card_id": card["id"],
                "role": role,
                "blocking": role in BLOCKING_ROLES,
                "proposition": card.get("proposition", ""),
            })
    return sorted(rows, key=lambda row: (row["system"], row["unit_id"], row["card_id"]))


def main() -> None:
    rows = collect()
    previous = read_json(OUT) if OUT.is_file() else {}
    approved = sorted(previous.get("approved", []))
    blocked = [row for row in rows if row["blocking"] and row["card_id"] not in approved]
    by_role = Counter(row["role"] for row in rows)
    OUT.write_text(json.dumps({
        "version": "1.0.0",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "purpose": "polarity=exception 카드의 역할 배치를 노출하고, 성립을 막는 자리에 "
                   "앉은 것을 검수 전까지 표시해 둔다",
        # 잠그면 26개 유닛이 멈춘다. 극성 복구 배치가 끝난 뒤에 켠다.
        "enforce": previous.get("enforce", False),
        "approved": approved,
        "counts": {
            "cards": len(rows),
            "blocking": sum(1 for row in rows if row["blocking"]),
            "pending_review": len(blocked),
            "affected_units": len({row["unit_id"] for row in blocked}),
            **dict(sorted(by_role.items())),
        },
        "cards": rows,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"polarity=exception {len(rows)}장 — 차단 역할 "
          f"{sum(1 for row in rows if row['blocking'])}장 / 승인 {len(approved)}장")
    print(f"  검수 대기 {len(blocked)}장, 유닛 {len({row['unit_id'] for row in blocked})}개")
    print(f"  → {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
