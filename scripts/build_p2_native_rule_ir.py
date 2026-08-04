"""Assemble a P2 unit's RuleIR from its approved decision ledger, in the fraud spec.

The property track derives components from a level map because nobody had ruled on those
480 cards.  Here the reviewer already ruled: role, component, join and track come from the
approved decision ledger, so this assembler reads a decision rather than inferring one.
The emitted shape is the one fraud and the ten property units already use, because that is
the only spec the Scallop runtime and the contract tests have executed.

Nothing about a specific offence lives in this file.  Unit ids, tracks, components, role
tuples and card roles all arrive as data.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from collections import defaultdict
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MAIN_ROOT = Path("/data5/jaehoonjeong/IDPR")
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))


def variable(value: str) -> dict[str, str]:
    return {"kind": "variable", "value": value}


def string(value: str) -> dict[str, str]:
    return {"kind": "string", "value": value}


def atom(predicate_id: str, *arguments: dict[str, str], negated: bool = False) -> dict[str, Any]:
    return {"predicate": predicate_id, "arguments": list(arguments), "negated": negated}


def dedupe_refs(cards: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: dict[tuple[str, str, str], dict[str, Any]] = {}
    for card in cards:
        for ref in card.get("source_refs", []):
            key = (ref.get("comment_id", ""), ref.get("section_path", ""), ref.get("quote", ""))
            seen.setdefault(key, ref)
    return list(seen.values())


P2 = ROOT / "data/rulegen/p2"
LEDGER_DIR = P2 / "native_review"
ROLE_SIGNATURES = P2 / "p2_native_role_signatures.json"
UNIT_MANIFEST = P2 / "p2_native_unit_manifest.json"
SOURCE_DIR = P2 / "rule_ir_units"
REMEDIATED_DIR = P2 / "remediated"
CARD_CORRECTIONS = P2 / "p2_card_metadata_corrections.json"
SOURCE_REF_CORRECTIONS = P2 / "p2_source_ref_corrections.json"
CAMPAIGN = MAIN_ROOT / "data/rulegen/campaign"
OUT_DIR = P2 / "rule_ir"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def slug(value: str) -> str:
    out = []
    for char in value.lower():
        out.append(char if char.isascii() and (char.isalnum()) else "_")
    return "".join(out).strip("_")


def commentary_index(articles: list[str]) -> dict[str, dict[str, Any]]:
    """comment_id -> chunk, merged across the unit's articles."""
    index: dict[str, dict[str, Any]] = {}
    for article in articles:
        path = CAMPAIGN / f"{article}_rulegen_requests.jsonl"
        if not path.is_file():
            raise SystemExit(f"commentary requests missing for {article}: {path}")
        for request in read_jsonl(path):
            for chunk in request.get("commentary_chunks", []):
                index[chunk["comment_id"]] = chunk
    return index


def apply_corrections(cards: dict[str, dict[str, Any]]) -> list[str]:
    """Apply approved metadata corrections, refusing any whose premise no longer holds."""
    if not CARD_CORRECTIONS.is_file():
        return []
    applied = []
    for item in read_json(CARD_CORRECTIONS)["corrections"]:
        card = cards.get(item["card_id"])
        if card is None:
            raise SystemExit(f"correction {item['correction_id']}: unknown card {item['card_id']}")
        current = card.get(item["field"])
        if current != item["from"]:
            raise SystemExit(
                f"correction {item['correction_id']} expected "
                f"{item['field']}={item['from']!r} but the card now has {current!r}")
        cards[item["card_id"]] = {**card, item["field"]: item["to"]}
        applied.append(item["correction_id"])
    return applied


def card_catalog() -> tuple[dict[str, dict[str, Any]], list[str]]:
    """Every card the unit may reference: unit bundles plus the remediated catalog."""
    cards: dict[str, dict[str, Any]] = {}
    for path in sorted(SOURCE_DIR.glob("*_unit.json")):
        for card in read_json(path).get("cards", []):
            cards.setdefault(card["id"], card)
    for path in sorted(REMEDIATED_DIR.glob("*/*.json")):
        for card in read_json(path).get("cards", []):
            cards.setdefault(card["id"], card)
    return cards, apply_corrections(cards)


def whitespace_span(quote: str, text: str) -> str | None:
    """Return the exact source span when only OCR whitespace differs."""
    target = re.sub(r"\s+", "", quote)
    offsets = [index for index, char in enumerate(text) if not char.isspace()]
    dense = "".join(text[index] for index in offsets)
    start = dense.find(target)
    if not target or start < 0:
        return None
    return text[offsets[start]: offsets[start + len(target) - 1] + 1]


def aligned_span(quote: str, text: str, minimum_coverage: float = 0.75) -> str | None:
    """Restore a bounded exact span when OCR interruptions split a long quote."""
    offsets = [index for index, char in enumerate(text) if not char.isspace()]
    dense = "".join(text[index] for index in offsets)
    target = re.sub(r"\s+", "", quote)
    blocks = [
        block
        for block in SequenceMatcher(None, dense, target, autojunk=False).get_matching_blocks()
        if block.size >= 4
    ]
    if not target or not blocks:
        return None
    if sum(block.size for block in blocks) / len(target) < minimum_coverage:
        return None
    start = offsets[blocks[0].a]
    end = offsets[blocks[-1].a + blocks[-1].size - 1] + 1
    while start > 0 and not text[start - 1].isspace():
        start -= 1
    tail = text.find("다.", end - 1)
    if 0 <= tail <= end + 60:
        end = tail + 2
    else:
        while end < len(text) and not text[end].isspace():
            end += 1
    span = text[start:end].strip()
    return span if len(span) <= 300 else None


def repair_source_refs(
    cards: dict[str, dict[str, Any]],
    card_ids: set[str],
    commentary: dict[str, dict[str, Any]],
) -> list[dict[str, str]]:
    """Restore exact provenance without editing the reviewed propositions."""
    overrides: dict[tuple[str, str, str], dict[str, Any]] = {}
    if SOURCE_REF_CORRECTIONS.is_file():
        for item in read_json(SOURCE_REF_CORRECTIONS).get("corrections", []):
            overrides[(item["card_id"], item["comment_id"], item["from"])] = item

    repairs: list[dict[str, str]] = []
    unrepaired: list[str] = []
    for card_id in sorted(card_ids):
        card = copy.deepcopy(cards[card_id])
        repaired_refs: list[dict[str, Any]] = []
        for ref in card.get("source_refs", []):
            text = commentary.get(ref["comment_id"], {}).get("document_text", "")
            quote = ref["quote"]
            if quote in text:
                repaired_refs.append(ref)
                continue
            override = overrides.get((card_id, ref["comment_id"], quote))
            if override is not None:
                fixed, kind = override["to"], override["correction_id"]
            else:
                fixed, kind = whitespace_span(quote, text), "ocr_whitespace"
                if fixed is None:
                    fixed, kind = aligned_span(quote, text), "aligned_span"
            if fixed is None or fixed not in text:
                unrepaired.append(f"{card_id}:{ref['comment_id']}")
                repaired_refs.append(ref)
                continue
            repaired_refs.append({**ref, "quote": fixed})
            repairs.append({
                "card_id": card_id,
                "comment_id": ref["comment_id"],
                "kind": kind,
                "from": quote,
                "to": fixed,
            })
        card["source_refs"] = repaired_refs
        cards[card_id] = card
    if unrepaired:
        raise SystemExit(f"unrepaired source refs: {sorted(unrepaired)}")
    return repairs


class UnitAssembler:
    """One unit's RuleIR, driven entirely by its approved decisions."""

    def __init__(self, unit_id: str, tracks: tuple[str, ...] | None) -> None:
        self.unit_id = unit_id
        self.ledger = read_json(LEDGER_DIR / f"{unit_id}_decision_ledger.json")
        if self.ledger["status"] != "ready_for_rule_ir":
            raise SystemExit(f"{unit_id}: decision ledger is {self.ledger['status']}")
        signatures = read_json(ROLE_SIGNATURES)["units"]
        if unit_id not in signatures:
            raise SystemExit(f"{unit_id}: no role signature declared")
        self.signature = signatures[unit_id]["default"]
        self.roles = list(self.signature["arguments"])
        if self.roles[0] != "case_id":
            raise SystemExit(f"{unit_id}: role signature must start with case_id")
        # A gaining track may build on a base track instead of restating its elements:
        # 존속상해·특수상해·상해치사는 기본 구성요건을 그대로 요구하고 자기 요건만 더한다.
        self.track_parent = {
            item["track_id"]: item.get("inherits_from")
            for item in self.ledger.get("tracks", [])
        }
        self.track_placement_inheritance = {
            item["track_id"]: tuple(item.get("inherits_placements", ()))
            for item in self.ledger.get("tracks", [])
        }
        compiled = tuple(self.signature.get("applies_to_tracks", ()))
        self.tracks = tuple(tracks) if tracks else compiled
        unknown = sorted(set(self.tracks) - set(compiled))
        if unknown:
            raise SystemExit(f"{unit_id}: tracks outside the declared signature: {unknown}")
        self.placement_tracks = set(self.tracks)
        pending = list(self.tracks)
        while pending:
            target = pending.pop()
            for inherited in self.track_placement_inheritance.get(target, ()):
                source = inherited["track_id"]
                if source not in self.track_parent:
                    raise SystemExit(
                        f"{unit_id}: {target} imports placements from undeclared {source}"
                    )
                if source not in self.placement_tracks:
                    self.placement_tracks.add(source)
                    pending.append(source)

        manifest = read_json(UNIT_MANIFEST)
        unit = next(item for item in manifest["units"] if item["unit_id"] == unit_id)
        self.articles = list(unit["articles"])
        self.label = unit["label"]
        self.law_snapshot = self.ledger["law_snapshot"]
        self.catalog, self.corrections = card_catalog()
        self.materialize_approved_propositions()
        unit_card_ids = {
            row["card_id"]
            for row in self.ledger["placements"]
            if row["track_id"] in self.placement_tracks
        }
        self.source_repairs = repair_source_refs(
            self.catalog, unit_card_ids, commentary_index(self.articles)
        )

        self.actor_arguments = [(name, "String") for name in self.roles]
        self.assessment_arguments = [
            ("case_id", "String"),
            ("assessment_id", "String"),
            *[(name, "String") for name in self.roles[1:]],
            ("status", "String"),
        ]
        self.actors = [variable(name) for name in self.roles]
        self.predicates: list[dict[str, Any]] = []
        self.rules: list[dict[str, Any]] = []
        self.seen_predicates: set[str] = set()
        self.used_cards: set[str] = set()
        self.deferred: list[dict[str, Any]] = []
        self.track_cards: dict[str, list[dict[str, Any]]] = {}

    def materialize_approved_propositions(self) -> None:
        """Make approved rewrites—and each approved split part—executable cards."""
        rewritten: dict[str, str] = {}
        for row in self.ledger["placements"]:
            original_id = row["card_id"]
            rewrite = row.get("proposition_rewrite")
            part_id = row.get("part_id")
            if part_id:
                if not rewrite:
                    raise SystemExit(
                        f"{self.unit_id}: split {original_id}#{part_id} has no proposition rewrite"
                    )
                synthetic_id = f"{original_id}.part.{slug(part_id)}"
                if synthetic_id in self.catalog:
                    if self.catalog[synthetic_id]["proposition"] != rewrite:
                        raise SystemExit(
                            f"{self.unit_id}: conflicting split rewrites for {synthetic_id}"
                        )
                else:
                    source = copy.deepcopy(self.catalog[original_id])
                    source["id"] = synthetic_id
                    source["proposition"] = rewrite
                    self.catalog[synthetic_id] = source
                row["source_card_id"] = original_id
                row["card_id"] = synthetic_id
                continue
            if not rewrite:
                continue
            previous = rewritten.setdefault(original_id, rewrite)
            if previous != rewrite:
                raise SystemExit(
                    f"{self.unit_id}: conflicting proposition rewrites for {original_id}"
                )
            card = copy.deepcopy(self.catalog[original_id])
            card["proposition"] = rewrite
            self.catalog[original_id] = card

    # ── placements ────────────────────────────────────────────────────
    def placements(self) -> list[dict[str, Any]]:
        """Per-card placements restricted to the tracks being compiled."""
        for component in self.ledger["components"]:
            if component["track_id"] not in self.placement_tracks:
                self.deferred.append(component)
        return [row for row in self.ledger["placements"]
                if row["track_id"] in self.placement_tracks]

    def card(self, card_id: str) -> dict[str, Any]:
        if card_id not in self.catalog:
            raise SystemExit(f"{self.unit_id}: card absent from the catalog: {card_id}")
        return self.catalog[card_id]

    # ── predicate and rule emission ───────────────────────────────────
    def add_predicate(
        self,
        predicate_id: str,
        arguments: list[tuple[str, str]],
        *,
        definition: str,
        origin: str,
        role: str,
        cards: list[dict[str, Any]] | None = None,
    ) -> str:
        if predicate_id in self.seen_predicates:
            return predicate_id
        self.seen_predicates.add(predicate_id)
        cards = cards or []
        refs = dedupe_refs(cards)
        self.predicates.append({
            "id": predicate_id,
            "kind": "rule",
            "origin": origin,
            "role": role,
            "definition": definition,
            "arguments": [{"name": name, "type": kind} for name, kind in arguments],
            "norm_card_ids": sorted({card["id"] for card in cards}),
            "source_refs": refs,
        })
        return predicate_id

    def add_rule(
        self,
        rule_id: str,
        head: dict[str, Any],
        body: list[dict[str, Any]],
        *,
        rationale: str,
        cards: list[dict[str, Any]],
    ) -> None:
        # The contract requires every rule to name the cards it came from, including the
        # aggregate ones: a conclusion with no provenance is exactly what this track exists
        # to prevent.
        if not cards:
            raise SystemExit(f"{rule_id}: a rule must carry at least one norm card")
        self.rules.append({
            "id": rule_id,
            "head": head,
            "body": body,
            "review_notes": rationale,
            "norm_card_ids": sorted({card["id"] for card in cards}),
            "source_refs": dedupe_refs(cards),
        })

    def system_predicates(self) -> None:
        self.add_predicate(
            "provable", [("case_id", "String"), ("assessment_id", "String")],
            definition="해당 사건의 평가가 절차·증명 게이트를 통과하여 실체법 규칙에 사용될 수 있음",
            origin="system", role="input")
        self.add_predicate(
            "case_assessment_complete",
            [("case_id", "String"), ("defendant_id", "String")],
            definition="사건 라우터가 선택한 평가 묶음이 완결되어 결론 계층의 폐쇄세계 검사를 허용함",
            origin="system", role="input")
        self.add_predicate(
            "distinct_entity",
            [("case_id", "String"), ("left_entity_id", "String"), ("right_entity_id", "String")],
            definition="사건의 entity resolution에서 두 역할이 서로 다른 실체임이 확인됨",
            origin="system", role="input")
        self.add_predicate(
            self.signature["predicate"], self.actor_arguments,
            definition=self.signature["definition"],
            origin="system", role="input")

    def card_predicates(self, card: dict[str, Any]) -> tuple[str, str]:
        name = slug(card["id"])
        assess = self.add_predicate(
            f"assess_{name}", self.assessment_arguments,
            definition=f"이 카드의 사건별 적용 평가: {card['proposition']}",
            origin="commentary", role="input", cards=[card])
        satisfied = self.add_predicate(
            f"satisfied_{name}", self.actor_arguments,
            definition=f"증명 가능한 평가에서 다음 조건이 충족됨: {card['proposition']}",
            origin="commentary", role="derived", cards=[card])
        return assess, satisfied

    def assessment_atom(self, assess: str, assessment_variable: str, status: str) -> dict[str, Any]:
        arguments = [
            variable("case_id"),
            variable(assessment_variable),
            *[variable(name) for name in self.roles[1:]],
            string(status),
        ]
        return atom(assess, *arguments)

    def emit_cards(self, placements: list[dict[str, Any]]) -> dict[str, str]:
        """Per-card input, condition, undetermined and conflict rules."""
        satisfied_by_card: dict[str, str] = {}
        card_ids = sorted({row["card_id"] for row in placements})
        for index, card_id in enumerate(card_ids, start=1):
            card = self.card(card_id)
            self.used_cards.add(card_id)
            assess, satisfied = self.card_predicates(card)
            tag = f"{index:03d}"
            self.add_rule(
                f"{self.unit_id}.card.{slug(card_id)}.satisfied",
                atom(satisfied, *self.actors),
                [
                    self.assessment_atom(assess, f"assessment_{tag}", "satisfied"),
                    atom("provable", variable("case_id"), variable(f"assessment_{tag}")),
                ],
                rationale="증명 가능한 평가가 satisfied일 때만 조건으로 승격한다.",
                cards=[card])
            self.add_rule(
                f"{self.unit_id}.card.{slug(card_id)}.undetermined",
                atom(self.undetermined, variable("case_id"), variable("defendant_id"),
                     string(card_id)),
                [
                    self.assessment_atom(assess, f"unknown_{tag}", "unknown"),
                    atom("provable", variable("case_id"), variable(f"unknown_{tag}")),
                ],
                rationale="unknown 평가를 결론 계층에 보존한다.",
                cards=[card])
            self.add_rule(
                f"{self.unit_id}.card.{slug(card_id)}.conflict",
                atom(self.conflict, variable("case_id"), variable("defendant_id"),
                     string(card_id)),
                [
                    self.assessment_atom(assess, f"positive_{tag}", "satisfied"),
                    self.assessment_atom(assess, f"negative_{tag}", "not_satisfied"),
                    atom("provable", variable("case_id"), variable(f"positive_{tag}")),
                    atom("provable", variable("case_id"), variable(f"negative_{tag}")),
                ],
                rationale="같은 카드에 satisfied와 not_satisfied가 모두 증명되면 충돌이다.",
                cards=[card])
            satisfied_by_card[card_id] = satisfied
        return satisfied_by_card

    def emit_components(
        self, placements: list[dict[str, Any]], satisfied_by_card: dict[str, str]
    ) -> dict[str, list[str]]:
        """Element predicates, joined the way the reviewer approved."""
        by_track: dict[str, list[str]] = defaultdict(list)
        track_card_ids: dict[str, set[str]] = defaultdict(set)
        grouped: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
        for row in placements:
            track_card_ids[row["track_id"]].add(row["card_id"])
            if row["role"] == "component":
                grouped[(row["track_id"], row["component_id"])].append(row)
        for (track, component), rows in sorted(grouped.items()):
            joins = sorted({row["component_join"] for row in rows})
            if len(joins) != 1:
                raise SystemExit(
                    f"{self.unit_id}: {track}::{component} has conflicting joins {joins}")
            join = joins[0]
            cards = [self.card(row["card_id"]) for row in rows]
            name = f"{self.unit_id}_{track}_{component}_satisfied"
            self.add_predicate(
                name, self.actor_arguments,
                definition=f"'{component}' 요건이 충족됨 ({track} track, {join})",
                origin="commentary", role="derived", cards=cards)
            by_track[track].append(name)
            if join == "alternative_any":
                for card in cards:
                    self.add_rule(
                        f"{self.unit_id}.component.{track}.{component}.{slug(card['id'])}",
                        atom(name, *self.actors),
                        [atom(satisfied_by_card[card["id"]], *self.actors)],
                        rationale="어느 한 인정 경로가 충족되면 요건이 충족된다.",
                        cards=[card])
            else:
                self.add_rule(
                    f"{self.unit_id}.component.{track}.{component}.all",
                    atom(name, *self.actors),
                    [atom(satisfied_by_card[card["id"]], *self.actors) for card in cards],
                    rationale="결합적 요건이므로 모든 카드가 충족되어야 한다.",
                    cards=cards)
        self.track_cards = {
            track: [self.card(cid) for cid in sorted(ids)]
            for track, ids in track_card_ids.items()
        }
        return by_track

    def lineage(self, track: str) -> list[str]:
        chain: list[str] = []
        cursor: str | None = track
        while cursor and cursor not in chain:
            chain.append(cursor)
            cursor = self.track_parent.get(cursor)
        return chain

    def placement_applies_to_track(self, row: dict[str, Any], target: str) -> bool:
        """Whether a placement constrains target, directly or through declared inheritance."""
        lineage = self.lineage(target)
        if row["track_id"] in lineage:
            return True
        # Selective placement inheritance is itself inherited by a child track.  For
        # example, voluntary_desistance inherits attempt, while attempt selectively
        # imports the base intent/object components.  The grandchild therefore needs
        # those same facts and their conflict/blocker reports even though it does not
        # repeat attempt's imports in the approval ledger.
        for ancestor in lineage:
            for inherited in self.track_placement_inheritance.get(ancestor, ()):
                if (row["track_id"] == inherited["track_id"]
                        and row["component_id"] in inherited["component_ids"]):
                    return True
        return False

    def emit_track_reports(
        self, placements: list[dict[str, Any]], satisfied_by_card: dict[str, str]
    ) -> None:
        """Scope blockers and conflicts to their track, propagating only by inheritance."""
        emitted: set[tuple[str, str, str]] = set()
        for row in placements:
            if row["role"] not in ("component", "bar", "boundary"):
                continue
            card_id = row["card_id"]
            card = self.card(card_id)
            for target in self.tracks:
                if not self.placement_applies_to_track(row, target):
                    continue
                conflict_key = ("conflict", target, card_id)
                if conflict_key not in emitted:
                    emitted.add(conflict_key)
                    self.add_rule(
                        f"{self.unit_id}.track_conflict.{target}.{slug(card_id)}",
                        atom(self.track_conflict, variable("case_id"),
                             variable("defendant_id"), string(target), string(card_id)),
                        [atom(self.conflict, variable("case_id"), variable("defendant_id"),
                              string(card_id))],
                        rationale="카드 평가 충돌은 해당 track과 그 상속 track에만 전파한다.",
                        cards=[card])
                if row["role"] not in ("bar", "boundary"):
                    continue
                blocked_key = ("blocked", target, card_id)
                if blocked_key in emitted:
                    continue
                emitted.add(blocked_key)
                self.add_rule(
                    f"{self.unit_id}.track_blocked.{target}.{slug(card_id)}",
                    atom(self.track_not_established, variable("case_id"),
                         variable("defendant_id"), string(target), string(card_id)),
                    [atom(satisfied_by_card[card_id], *self.actors)],
                    rationale="저지·경계 카드는 해당 track과 그 상속 track만 막는다.",
                    cards=[card])

    def inherited_elements(self, track: str) -> list[str]:
        """The elements predicate this track inherits, if the reviewer declared one."""
        parent = self.track_parent.get(track)
        inherited: list[str] = []
        if parent:
            if parent not in self.tracks:
                raise SystemExit(
                    f"{self.unit_id}: {track} inherits from {parent}, which is not being compiled")
            inherited.append(f"{self.unit_id}_{parent}_elements_satisfied")
        for item in self.track_placement_inheritance.get(track, ()):
            source = item["track_id"]
            if source not in self.placement_tracks:
                raise SystemExit(
                    f"{self.unit_id}: {track} inherits unavailable placements from {source}")
            inherited.extend(
                f"{self.unit_id}_{source}_{component}_satisfied"
                for component in item["component_ids"]
                if any(row["track_id"] == source
                       and row["component_id"] == component
                       and row["role"] == "component"
                       for row in self.ledger["placements"])
            )
        return list(dict.fromkeys(inherited))

    def track_conclusion_cards(self, track: str) -> list[dict[str, Any]]:
        """Provenance for a track conclusion: its own cards plus every inherited one."""
        cards: dict[str, dict[str, Any]] = {}
        cursor: str | None = track
        seen: set[str] = set()
        while cursor and cursor not in seen:
            seen.add(cursor)
            for card in self.track_cards.get(cursor, []):
                cards.setdefault(card["id"], card)
            cursor = self.track_parent.get(cursor)
        for item in self.track_placement_inheritance.get(track, ()):
            for row in self.ledger["placements"]:
                if (row["track_id"] == item["track_id"]
                        and row["component_id"] in item["component_ids"]):
                    cards.setdefault(row["card_id"], self.card(row["card_id"]))
        return [cards[card_id] for card_id in sorted(cards)]

    def emit_conclusions(self, by_track: dict[str, list[str]]) -> None:
        all_cards = [self.card(cid) for cid in sorted(self.used_cards)]
        self.add_predicate(
            self.has_negative, [("case_id", "String"), ("defendant_id", "String")],
            definition="이 unit에 증명된 불성립 사유가 존재함",
            origin="system", role="derived")
        self.add_predicate(
            self.has_conflict, [("case_id", "String"), ("defendant_id", "String")],
            definition="이 unit에 증명된 평가 충돌이 존재함",
            origin="system", role="derived")
        self.add_rule(
            f"{self.unit_id}.summary.has_negative",
            atom(self.has_negative, variable("case_id"), variable("defendant_id")),
            [atom(self.not_established, variable("case_id"), variable("defendant_id"),
                  variable("norm_card_id"))],
            rationale="불성립 사유의 존재를 2항으로 요약한다.",
            cards=all_cards)
        self.add_rule(
            f"{self.unit_id}.summary.has_conflict",
            atom(self.has_conflict, variable("case_id"), variable("defendant_id")),
            [atom(self.conflict, variable("case_id"), variable("defendant_id"),
                  variable("norm_card_id"))],
            rationale="충돌의 존재를 2항으로 요약한다.",
            cards=all_cards)
        self.add_rule(
            f"{self.unit_id}.summary.canonical_not_established",
            atom(self.not_established, variable("case_id"), variable("defendant_id"),
                 variable("norm_card_id")),
            [atom(self.track_not_established, variable("case_id"),
                  variable("defendant_id"), variable("track_id"),
                  variable("norm_card_id"))],
            rationale="track별 불성립 사유를 canonical unit 보고 관계로 투영한다.",
            cards=all_cards)
        self.add_rule(
            f"{self.unit_id}.summary.track_has_negative",
            atom(self.track_has_negative, variable("case_id"), variable("defendant_id"),
                 variable("track_id")),
            [atom(self.track_not_established, variable("case_id"),
                  variable("defendant_id"), variable("track_id"),
                  variable("norm_card_id"))],
            rationale="track별 불성립 사유의 존재를 요약한다.",
            cards=all_cards)
        self.add_rule(
            f"{self.unit_id}.summary.track_has_conflict",
            atom(self.track_has_conflict, variable("case_id"), variable("defendant_id"),
                 variable("track_id")),
            [atom(self.track_conflict, variable("case_id"), variable("defendant_id"),
                  variable("track_id"), variable("norm_card_id"))],
            rationale="track별 충돌의 존재를 요약한다.",
            cards=all_cards)

        for track in self.tracks:
            components = sorted(by_track.get(track, []))
            inherited = self.inherited_elements(track)
            if not components and not inherited:
                continue
            elements = f"{self.unit_id}_{track}_elements_satisfied"
            established = f"{self.unit_id}_{track}_established"
            parent = self.track_parent.get(track)
            definition = f"'{track}' track의 구성요건 component가 모두 충족된 잠정 성립 후보"
            if parent:
                definition = (
                    f"'{parent}' track의 구성요건을 그대로 충족하고 "
                    f"'{track}' track의 가중 요건이 더해진 잠정 성립 후보"
                )
            self.add_predicate(
                elements, self.actor_arguments,
                definition=definition,
                origin="system", role="derived")
            self.add_predicate(
                established, self.actor_arguments,
                definition=f"완결 게이트 뒤에 불성립 사유와 충돌이 모두 없는 '{track}' track 확정 성립",
                origin="system", role="derived")
            rationale = f"'{track}' track의 모든 component를 AND 결합한다."
            if parent:
                rationale = (
                    f"'{track}'는 '{parent}' track의 구성요건 위에 얹히는 가중 track이므로 "
                    f"'{parent}'의 elements를 그대로 요구하고 자기 component를 더한다."
                )
            self.add_rule(
                f"{self.unit_id}.outcome.{track}.elements_satisfied",
                atom(elements, *self.actors),
                [atom(name, *self.actors) for name in [*inherited, *components]],
                rationale=rationale,
                cards=self.track_conclusion_cards(track))
            self.add_rule(
                f"{self.unit_id}.outcome.{track}.established",
                atom(established, *self.actors),
                [
                    atom(elements, *self.actors),
                    atom("case_assessment_complete", variable("case_id"),
                         variable("defendant_id")),
                    atom(self.track_has_negative, variable("case_id"), variable("defendant_id"),
                         string(track),
                         negated=True),
                    atom(self.track_has_conflict, variable("case_id"), variable("defendant_id"),
                         string(track),
                         negated=True),
                ],
                rationale="완결 게이트 뒤에서만 부정을 사용해 확정 성립을 낸다.",
                cards=self.track_conclusion_cards(track))

    # ── conclusion relation names ─────────────────────────────────────
    @property
    def not_established(self) -> str:
        return f"{self.unit_id}_not_established"

    @property
    def undetermined(self) -> str:
        return f"{self.unit_id}_undetermined"

    @property
    def conflict(self) -> str:
        return f"{self.unit_id}_conflict"

    @property
    def has_negative(self) -> str:
        return f"{self.unit_id}_has_negative"

    @property
    def has_conflict(self) -> str:
        return f"{self.unit_id}_has_conflict"

    @property
    def track_not_established(self) -> str:
        return f"{self.unit_id}_track_not_established"

    @property
    def track_conflict(self) -> str:
        return f"{self.unit_id}_track_conflict"

    @property
    def track_has_negative(self) -> str:
        return f"{self.unit_id}_track_has_negative"

    @property
    def track_has_conflict(self) -> str:
        return f"{self.unit_id}_track_has_conflict"

    def outcome_predicates(self) -> None:
        report_arguments = [
            ("case_id", "String"), ("defendant_id", "String"), ("norm_card_id", "String"),
        ]
        self.add_predicate(
            self.not_established, report_arguments,
            definition="증명된 불성립 사유 또는 경계 이동이 존재함",
            origin="system", role="derived")
        self.add_predicate(
            self.undetermined, report_arguments,
            definition="관련 카드의 평가가 unknown이어서 결론을 확정할 수 없음",
            origin="system", role="derived")
        self.add_predicate(
            self.conflict, report_arguments,
            definition="같은 카드에 satisfied와 not_satisfied 평가가 모두 증명됨",
            origin="system", role="derived")
        track_report_arguments = [
            ("case_id", "String"), ("defendant_id", "String"),
            ("track_id", "String"), ("norm_card_id", "String"),
        ]
        self.add_predicate(
            self.track_not_established, track_report_arguments,
            definition="해당 track에만 적용되는 증명된 불성립 사유 또는 경계 이동",
            origin="system", role="derived")
        self.add_predicate(
            self.track_conflict, track_report_arguments,
            definition="해당 track에 적용되는 카드 평가 충돌",
            origin="system", role="derived")
        self.add_predicate(
            self.track_has_negative,
            [("case_id", "String"), ("defendant_id", "String"), ("track_id", "String")],
            definition="해당 track에 증명된 불성립 사유가 존재함",
            origin="system", role="derived")
        self.add_predicate(
            self.track_has_conflict,
            [("case_id", "String"), ("defendant_id", "String"), ("track_id", "String")],
            definition="해당 track에 증명된 평가 충돌이 존재함",
            origin="system", role="derived")

    def build(self) -> tuple[dict[str, Any], dict[str, Any]]:
        placements = self.placements()
        self.system_predicates()
        self.outcome_predicates()
        satisfied_by_card = self.emit_cards(placements)
        by_track = self.emit_components(placements, satisfied_by_card)
        self.emit_track_reports(placements, satisfied_by_card)
        self.emit_conclusions(by_track)

        cards = [self.card(card_id) for card_id in sorted(self.used_cards)]
        comment_ids = sorted({
            ref["comment_id"] for card in cards for ref in card.get("source_refs", [])
        })
        index = commentary_index(self.articles)
        missing = [cid for cid in comment_ids if cid not in index]
        if missing:
            raise SystemExit(f"{self.unit_id}: comment_ids absent from commentary: {missing}")

        card_set = {
            "version": "1.1.0",
            "card_set_id": f"kr.p2.{self.unit_id}.native.norms.v1",
            "issue_tag": self.unit_id,
            "status": "draft",
            "legal_review": "pending",
            "construction": "deterministic_candidate_lift",
            "source_scope": {
                "comment_ids": comment_ids,
                "target_paths": sorted({
                    f"commentary://001692/{article}" for article in self.articles
                }),
            },
            "cards": cards,
            "legal_review_questions": [],
            "coverage_gaps": self.coverage_gaps(),
        }
        rule_ir = {
            "version": "1.1.0",
            "rule_set_id": f"kr.p2.{self.unit_id}.native.v1_candidate",
            "issue_tag": self.unit_id,
            "status": "draft",
            "legal_review": "pending",
            "legal_review_questions": [],
            "source_scope": {
                "comment_ids": comment_ids,
                "target_paths": card_set["source_scope"]["target_paths"],
            },
            "norm_card_scope": {
                "card_set_id": card_set["card_set_id"],
                "card_ids": sorted(self.used_cards),
            },
            "predicates": self.predicates,
            "rules": self.rules,
            "coverage_gaps": self.coverage_gaps(),
        }
        return rule_ir, card_set

    def coverage_gaps(self) -> list[str]:
        gaps: list[str] = [
            f"predicate_ir_missing: {item['card_id']} → {item['refers_to_unit']}"
            for item in self.ledger["unresolved_unit_references"]
        ]
        gaps.extend(
            f"track_deferred: {item['track_id']}::{item['component_id']} "
            f"({len(item['norm_card_ids'])} cards)"
            for item in self.deferred
        )
        gaps.extend(
            f"context_only: {item['card_id']}"
            for item in self.ledger["excluded_cards"]
        )
        gaps.extend(
            f"card_metadata_correction: {correction_id}"
            for correction_id in self.corrections
        )
        gaps.extend(
            f"source_quote_repair: {item['card_id']}::{item['comment_id']} ({item['kind']})"
            for item in self.source_repairs
        )
        return gaps


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--unit", required=True)
    parser.add_argument("--track", action="append", default=[])
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR)
    args = parser.parse_args()

    assembler = UnitAssembler(args.unit, tuple(args.track) or None)
    rule_ir, card_set = assembler.build()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    rule_ir_path = args.out_dir / f"{args.unit}_rule_ir_candidate.json"
    card_set_path = args.out_dir / f"{args.unit}_norm_card_set.json"
    rule_ir_path.write_text(
        json.dumps(rule_ir, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    card_set_path.write_text(
        json.dumps(card_set, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    repair_path = args.out_dir / f"{args.unit}_source_quote_repairs.json"
    repair_path.write_text(json.dumps({
        "version": "1.0.0",
        "unit_id": args.unit,
        "policy": "원문 exact substring을 복원하는 provenance-only 교정; proposition은 변경하지 않는다",
        "repairs": assembler.source_repairs,
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "unit": args.unit,
        "tracks": list(assembler.tracks),
        "cards": len(rule_ir["norm_card_scope"]["card_ids"]),
        "predicates": len(rule_ir["predicates"]),
        "rules": len(rule_ir["rules"]),
        "coverage_gaps": len(rule_ir["coverage_gaps"]),
        "source_quote_repairs": len(assembler.source_repairs),
        "rule_ir": str(rule_ir_path),
        "norm_card_set": str(card_set_path),
        "source_quote_repair_ledger": str(repair_path),
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
