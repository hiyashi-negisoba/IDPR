"""residual UNKNOWN을 failure mode로 분해한다 — 사례 본문을 열지 않는다.

`audit_v2_call2_distribution.py`는 "어느 predicate가 몇 번 UNKNOWN인가"까지 답한다.
그 목록만 보고 저작을 고치면 문안을 근거 없이 고치게 된다. 같은 predicate라도 어느 요건
자리에서, 어느 죄가 소유한 instance에서, 어떤 저작 표면(legal_standard·semantic_exclusions·
evidence_scope·temporal_anchor·arity)을 달고 물었는지에 따라 실패 양상이 다르기 때문이다.

sealed-59 정책상 사례 본문은 열 수 없다. 그래서 여기서 쓰는 재료는 전부 target metadata와
같은 instance 안의 다른 predicate 상태(동시 응답)뿐이다. Call 2 산출물에는 rationale이나
사건 텍스트가 없고 instance_key·predicate_ref·truth만 있으므로, 이 집계는 구조적으로
사례를 열지 않는다. 사례 식별이 필요한 줄에서는 승인된 dev 2건만 이름을 노출한다.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml

DEV_CASES = frozenset({"kcl_criminal_r10_p1_q1_ga", "kcl_criminal_r14_p1_q2"})
TRUTHS = ("TRUE", "FALSE", "UNKNOWN")


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _walk_refs(node: Any, out: set[str]) -> None:
    if isinstance(node, dict):
        if isinstance(node.get("ref"), str):
            out.add(node["ref"])
        for value in node.values():
            _walk_refs(value, out)
    elif isinstance(node, list):
        for value in node:
            _walk_refs(value, out)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run", type=Path, required=True, help="실행 artifact 루트")
    parser.add_argument("--definitions", type=Path, default=Path("data/v2/definitions"))
    args = parser.parse_args()

    defs = args.definitions
    load = lambda name: yaml.safe_load((defs / f"{name}.yaml").read_text(encoding="utf-8"))
    pred = {e["id"]: e for e in load("legal_elements") + load("ground_facts")}
    offenses = {e["id"]: e for e in load("offenses")}
    derived = {e["id"]: e for e in load("derived_offenses")}

    # 요건 자리(slot) 역인덱스와, 중한 결과 귀속을 쓰는 죄(결과적 가중범) 집합
    slot_of: dict[str, dict[str, set[str]]] = defaultdict(lambda: defaultdict(set))
    aggravated: set[str] = set()
    for oid, payload in {**offenses, **derived}.items():
        elements = payload.get("elements") or payload.get("flattened_elements") or {}
        for slot, expr in elements.items():
            refs: set[str] = set()
            _walk_refs(expr, refs)
            for ref in refs:
                slot_of[oid][ref].add(slot)
        whole: set[str] = set()
        _walk_refs(payload.get("derivation") or {}, whole)
        _walk_refs(elements, whole)
        if any("aggravated_result_attribution" in ref for ref in whole):
            aggravated.add(oid)

    plan = _jsonl(args.run / "plan_doctrine/evaluation_instance_plan.jsonl")
    call2 = _jsonl(args.run / "call2/grounding_output.jsonl")

    def key(value: dict[str, Any]) -> tuple[str, ...]:
        i = value["instance_key"]
        return (i["case_id"], i["actor_id"], i["offense_ref"], i["occurrence_id"], value["predicate_ref"])

    planned = {key(v) for row in plan for v in row.get("assessment_targets", [])}
    asked = {key(v): str(v["truth"]) for row in call2 for v in row.get("case_truths", [])}

    instance_truth: dict[tuple[str, ...], dict[str, str]] = defaultdict(dict)
    for k, truth in asked.items():
        instance_truth[k[:4]][k[4]] = truth

    provenance: dict[tuple[str, ...], dict[str, Any]] = {}
    for row in plan:
        for item in row.get("instance_provenance", []):
            i = item["instance_key"]
            provenance[(i["case_id"], i["actor_id"], i["offense_ref"], i["occurrence_id"])] = item

    def dist(keys) -> tuple[int, Counter]:
        counts = Counter(asked[k] for k in keys if k in asked)
        return sum(counts.values()), counts

    def line(label: str, keys, width: int = 52) -> str:
        n, c = dist(keys)
        if not n:
            return f"  {label:<{width}} asked 0"
        u = c.get("UNKNOWN", 0)
        return (f"  {label:<{width}} asked {n:4}  T {c.get('TRUE', 0):4}  "
                f"F {c.get('FALSE', 0):3}  U {u:4}  ({u / n:5.1%})")

    def header(title: str) -> None:
        print("\n" + "=" * 96 + f"\n{title}\n" + "=" * 96)

    header("0. baseline 재현 — 아래 숫자가 frozen baseline과 다르면 그 뒤는 읽지 말 것")
    n, c = dist(asked)
    print(f"  planned {len(planned)}  asked {len(asked)}  pruned {len(planned - set(asked))}")
    print(f"  TRUE {c['TRUE']}  FALSE {c['FALSE']}  UNKNOWN {c['UNKNOWN']}  ({c['UNKNOWN'] / n:.1%})")
    print(f"  instance {len(instance_truth)}  case {len({k[0] for k in asked})}")

    header("1. 저작 표면별 UNKNOWN — Call 2가 predicate마다 다르게 보는 것은 이 필드들뿐이다")
    groups: dict[tuple[str, Any], set] = defaultdict(set)
    for k in asked:
        e = pred.get(k[4])
        if e is None:
            groups[("<정의 없음>", "-")].add(k)
            continue
        groups[("kind", k[4].split(".")[0])].add(k)
        groups[("legal_standard", bool(e.get("legal_standard")))].add(k)
        groups[("semantic_exclusions>0", bool(e.get("semantic_exclusions")))].add(k)
        groups[("evidence_scope", e.get("evidence_scope", "offense_realization"))].add(k)
        groups[("temporal_anchor", bool(e.get("temporal_anchor")))].add(k)
        groups[("arity", len(e.get("arguments") or ()))].add(k)
    for axis in ("kind", "legal_standard", "semantic_exclusions>0", "evidence_scope",
                 "temporal_anchor", "arity", "<정의 없음>"):
        rows = sorted((k for k in groups if k[0] == axis), key=lambda r: str(r[1]))
        if rows:
            print(f"\n[{axis}]")
            for row in rows:
                print(line(str(row[1]), groups[row]))

    print("\n[semantic_exclusions 보유 predicate 개별 성적]")
    total_by = Counter(k[4] for k in asked)
    for ref in sorted((p for p in total_by if pred.get(p, {}).get("semantic_exclusions")),
                      key=lambda p: -total_by[p]):
        n_excl = len(pred[ref]["semantic_exclusions"])
        print(line(f"excl={n_excl}  {ref}", {k for k in asked if k[4] == ref}))

    print("\n[temporal_anchor 보유 target 개별]")
    anchored = Counter(
        (k[2], k[4], pred[k[4]]["temporal_anchor"], asked[k])
        for k in asked if pred.get(k[4], {}).get("temporal_anchor")
    )
    for (offense, ref, anchor, truth), count in anchored.most_common():
        print(f"  {truth:8} x{count}  {offense}  {ref}  anchor={anchor}")

    header("2. 요건 자리(slot)별 UNKNOWN — 같은 predicate라도 어느 자리에서 물었는가")
    by_slot: dict[str, set] = defaultdict(set)
    for k in asked:
        for slot in (slot_of.get(k[2], {}).get(k[4]) or {"<비요건: 정책·법리·참가>"}):
            by_slot[slot].add(k)
    print()
    for slot in sorted(by_slot, key=lambda s: -len(by_slot[s])):
        print(line(slot, by_slot[slot]))

    header("3. instance 성격별 UNKNOWN")
    print()
    focal = {k for k in asked if (provenance.get(k[:4]) or {}).get("actor_in_focal_action")}
    print(line("focal actor instance", focal))
    print(line("non-focal actor instance", set(asked) - focal))
    derived_keys = {k for k in asked if k[2].startswith("derived_offense.")}
    print(line("derived offense instance", derived_keys))
    print(line("base offense instance", set(asked) - derived_keys))

    header("4. legal_element.intent — 결과적 가중범 사용처 vs 일반 사용처")
    intent = {k for k in asked if k[4] == "legal_element.intent"}
    agg = {k for k in intent if k[2] in aggravated}
    print()
    print(line("전체", intent))
    print(line("결과적 가중범 소유", agg))
    print(line("일반 고의 사용처", intent - agg))
    print("\n  [소유 죄명별]")
    by_offense: dict[str, set] = defaultdict(set)
    for k in intent:
        by_offense[k[2]].add(k)
    for offense in sorted(by_offense, key=lambda o: -len(by_offense[o])):
        print(line(offense + (" ←결과적가중범" if offense in aggravated else ""), by_offense[offense]))

    print("\n  [intent 상태 × 같은 instance의 conduct-slot predicate 상태]")
    cross = Counter()
    for k in intent:
        conduct = [p for p, slots in slot_of.get(k[2], {}).items() if "conduct" in slots]
        values = {instance_truth[k[:4]].get(p, "<미질문>") for p in conduct}
        tag = "conduct TRUE" if "TRUE" in values else (
            "conduct UNKNOWN" if "UNKNOWN" in values else "conduct 없음")
        cross[(asked[k], tag)] += 1
    for (a, b), count in sorted(cross.items()):
        print(f"    intent {a:8} × {b:16}  {count}")

    print("\n  [결과적 가중범 instance: intent 상태 × aggravated_result_attribution 상태]")
    cross = Counter()
    for k in agg:
        other = instance_truth[k[:4]].get("legal_element.aggravated_result_attribution", "<미질문>")
        cross[(asked[k], other)] += 1
    for (a, b), count in sorted(cross.items()):
        print(f"    intent {a:8} × attribution {b:10}  {count}")

    header("5. means_or_object_defect → dangerousness lineage")
    defect = {k for k in asked if k[4] == "ground_fact.means_or_object_defect"}
    danger = {k for k in asked if k[4] == "legal_element.dangerousness"}
    print()
    print(line("ground_fact.means_or_object_defect (upstream)", defect))
    print(line("legal_element.dangerousness (downstream)", danger))

    print("\n  [upstream: defect 상태 × 같은 instance의 commencement_of_execution 상태]")
    cross = Counter()
    for k in defect:
        cross[(asked[k], instance_truth[k[:4]].get("legal_element.commencement_of_execution", "<미질문>"))] += 1
    for (a, b), count in sorted(cross.items()):
        print(f"    defect {a:8} × commencement {b:10}  {count}")

    print("\n  [downstream: dangerousness가 열린 instance에서 upstream defect는 무엇이었나]")
    cross = Counter()
    for k in danger:
        cross[(asked[k], instance_truth[k[:4]].get("ground_fact.means_or_object_defect", "<미질문>"))] += 1
    for (a, b), count in sorted(cross.items()):
        print(f"    dangerousness {a:8} × defect {b:10}  {count}")

    print("\n  [defect 소유 죄명별]")
    by_offense = defaultdict(set)
    for k in defect:
        by_offense[k[2]].add(k)
    for offense in sorted(by_offense, key=lambda o: -len(by_offense[o])):
        print(line(offense, by_offense[offense]))

    print("\n  [defect instance의 기수 대리지표 — 같은 instance의 result-slot predicate 상태]")
    cross = Counter()
    for k in defect:
        results = [p for p, slots in slot_of.get(k[2], {}).items() if "result" in slots]
        values = {instance_truth[k[:4]].get(p, "<미질문>") for p in results}
        tag = "TRUE 있음" if "TRUE" in values else ("result slot 없음" if not values else "미확정")
        cross[(asked[k], tag)] += 1
    for (a, b), count in sorted(cross.items()):
        print(f"    defect {a:8} × {b:16}  {count}")

    header("6. FALSE가 나온 자리 — 비율이 아니라 '어디서 반증이 성립하는가'를 본다")
    false_by = Counter(k[4] for k, t in asked.items() if t == "FALSE")
    unknown_by = Counter(k[4] for k, t in asked.items() if t == "UNKNOWN")
    print("\n  [FALSE가 실제로 나온 predicate]")
    for ref, count in false_by.most_common():
        print(f"    F {count:3}/{total_by[ref]:3}  U {unknown_by[ref]:3}  {ref}")
    print("\n  [asked>=6 인데 FALSE 0 — UNKNOWN 많은 순]")
    for ref in sorted((p for p in total_by if total_by[p] >= 6 and not false_by[p]),
                      key=lambda p: -unknown_by[p]):
        e = pred.get(ref, {})
        print(f"    U {unknown_by[ref]:3}/{total_by[ref]:3}  excl={len(e.get('semantic_exclusions') or ())} "
              f"std={int(bool(e.get('legal_standard')))} "
              f"scope={e.get('evidence_scope', 'offense_realization'):22} {ref}")

    header("7. case별 UNKNOWN — 승인된 dev 2건만 식별한다")
    by_case: dict[str, set] = defaultdict(set)
    for k in asked:
        by_case[k[0]].add(k)
    rows = []
    for case_id, keys in by_case.items():
        n_case, c_case = dist(keys)
        rows.append((c_case.get("UNKNOWN", 0) / n_case, n_case, c_case.get("UNKNOWN", 0), case_id))
    print()
    for ratio, n_case, u_case, case_id in sorted(rows, reverse=True):
        print(f"  {u_case:3}/{n_case:3}  {ratio:5.1%}  {case_id if case_id in DEV_CASES else '(sealed)'}")


if __name__ == "__main__":
    main()
