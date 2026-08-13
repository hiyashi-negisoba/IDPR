"""Audit a host-safe card/issue join over the canonical KCL-26 v2 instances."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

from idpr.retrieval import LexicalIndex, corpus_fingerprint
from idpr.rulebase.card_catalog_v2 import compile_card_catalog_v2
from idpr.rulebase.cards import card_corpus
from idpr.rulebase.issue_catalog_v2 import compile_issue_catalog_v2
from idpr.v2.registry import load_definitions
from idpr.v2.runtime.card_issue_bridge import plan_instance_issue_candidates
from idpr.v2.runtime.identity import OffenseInstanceKey


def _jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def _binding_quotes(rows: Iterable[Mapping[str, Any]]) -> dict[tuple[str, str], tuple[str, ...]]:
    output: dict[tuple[str, str], tuple[str, ...]] = {}
    for row in rows:
        case_id = str(row["sub_question_id"])
        for seed in row.get("seed_results", ()):
            for binding in seed.get("bindings", ()):
                quotes = [
                    str(fragment["source_quote"])
                    for key in ("actor_action_fragments", "context_fragments")
                    for fragment in binding.get(key, ())
                    if fragment.get("source_quote")
                ]
                output[(case_id, str(binding["binding_id"]))] = tuple(
                    dict.fromkeys(quotes)
                )
    return output


def _instance(value: Mapping[str, Any]) -> OffenseInstanceKey:
    return OffenseInstanceKey(
        str(value["case_id"]),
        str(value["actor_id"]),
        str(value["offense_ref"]),
        str(value["occurrence_id"]),
    )


def build_audit(
    *,
    definitions: Path,
    plan_path: Path,
    bindings_path: Path,
    call2_path: Path | None,
    top_k_issues: int,
) -> dict[str, Any]:
    registry = load_definitions(definitions)
    corpus = card_corpus()
    issues, _ = compile_issue_catalog_v2(corpus)
    cards = compile_card_catalog_v2(corpus)
    card_fingerprint = corpus_fingerprint(
        tuple(card.proposition for card in corpus.cards)
    )
    dense_cache = Path(
        f"data/eval/cache/cards_embeddinggemma-300m_{card_fingerprint}.json"
    )
    quotes_by_binding = _binding_quotes(_jsonl(bindings_path))
    plan_rows = _jsonl(plan_path)

    selected_function_counts: Counter[str] = Counter()
    selected_runtime_counts: Counter[str] = Counter()
    projection_counts: Counter[str] = Counter()
    unmapped_refs: Counter[str] = Counter()
    article_counts: Counter[str] = Counter()
    issue_candidate_ids: set[str] = set()
    anchor_card_ids: set[str] = set()
    retrieval_card_ids: set[str] = set()
    selected_detail_card_ids: set[str] = set()
    instance_rows: list[dict[str, Any]] = []
    detail_lexical = LexicalIndex.build(tuple(card.proposition for card in corpus.cards))

    derived_sources: dict[tuple[str, str], tuple[str, ...]] = {}
    for row in plan_rows:
        case_id = str(row["sub_question_id"])
        for candidate in row.get("derived_binding_candidates", ()):
            derived_sources[(case_id, str(candidate["binding_id"]))] = tuple(
                str(value) for value in candidate.get("source_binding_ids", ())
            )

    for row in plan_rows:
        for raw_instance in row.get("top_level_instances", ()):
            instance = _instance(raw_instance)
            source_ids = derived_sources.get(
                (instance.case_id, instance.occurrence_id),
                (instance.occurrence_id,),
            )
            quotes = tuple(
                dict.fromkeys(
                    quote
                    for source_id in source_ids
                    for quote in quotes_by_binding.get((instance.case_id, source_id), ())
                )
            )
            issue_plan = plan_instance_issue_candidates(
                registry,
                instance,
                episode_quotes=quotes,
                corpus=corpus,
                issues=issues,
                top_k_issues=top_k_issues,
                detail_lexical=detail_lexical,
            )
            projection_counts[issue_plan.projection.status] += 1
            if not issue_plan.projection.article_keys:
                unmapped_refs[instance.offense_ref] += 1
            article_counts.update(issue_plan.projection.article_keys)
            candidates = []
            for candidate in issue_plan.candidates:
                selected_function_counts[candidate.function] += 1
                selected_runtime_counts[candidate.runtime] += 1
                issue_candidate_ids.add(candidate.issue_id)
                anchor_card_ids.update(candidate.anchor_card_ids)
                retrieval_card_ids.update(candidate.retrieval_card_ids)
                selected_detail_card_ids.update(candidate.selected_detail_card_ids)
                candidates.append(
                    {
                        "issue_id": candidate.issue_id,
                        "article": candidate.article,
                        "function": candidate.function,
                        "runtime": candidate.runtime,
                        "score": candidate.score,
                        "anchor_card_ids": list(candidate.anchor_card_ids),
                        "retrieval_card_ids": list(candidate.retrieval_card_ids),
                        "selected_detail_card_ids": list(
                            candidate.selected_detail_card_ids
                        ),
                    }
                )
            instance_rows.append(
                {
                    "instance_key": {
                        "case_id": instance.case_id,
                        "actor_id": instance.actor_id,
                        "offense_ref": instance.offense_ref,
                        "occurrence_id": instance.occurrence_id,
                    },
                    "projection": {
                        "status": issue_plan.projection.status,
                        "article_keys": list(issue_plan.projection.article_keys),
                        "statutory_refs": list(issue_plan.projection.statutory_refs),
                    },
                    "source_binding_ids": list(source_ids),
                    "episode_quote_count": len(quotes),
                    "issue_candidates": candidates,
                }
            )

    corpus_issue_functions = Counter(issue.function for issue in issues)
    corpus_issue_runtimes = Counter(issue.runtime for issue in issues)
    card_functions = Counter(card.function for card in cards)
    call2_coverage: dict[str, Any] = {}
    if call2_path is not None:
        projection_by_instance = {
            tuple(row["instance_key"][key] for key in ("case_id", "actor_id", "offense_ref", "occurrence_id")):
            row["projection"]["status"]
            for row in instance_rows
        }
        truth_projection_counts: Counter[str] = Counter()
        unknown_refs: Counter[str] = Counter()
        for row in _jsonl(call2_path):
            for assessment in row.get("assessments", ()):
                raw = assessment["instance_key"]
                key = tuple(
                    raw[name]
                    for name in ("case_id", "actor_id", "offense_ref", "occurrence_id")
                )
                projection_status = projection_by_instance.get(key, "NOT_TOP_LEVEL")
                truth = str(assessment["truth"])
                truth_projection_counts[f"{truth}/{projection_status}"] += 1
                if truth == "UNKNOWN" and projection_status == "EXACT_AUTHORED_IDENTITY":
                    unknown_refs[str(assessment["predicate_ref"])] += 1
        call2_coverage = {
            "truth_projection_counts": dict(truth_projection_counts.most_common()),
            "card_joinable_unknown_targets": sum(unknown_refs.values()),
            "card_joinable_unknown_predicate_refs": len(unknown_refs),
            "top_unknown_predicate_refs": dict(unknown_refs.most_common(20)),
        }

    return {
        "scope": {
            "case_count": len(plan_rows),
            "top_level_instance_count": len(instance_rows),
            "top_k_issues_per_instance": top_k_issues,
            "retrieval_mode": "existing issue-first character-bigram BM25; dense/reranker cache compatible",
            "card_corpus_fingerprint": card_fingerprint,
            "embeddinggemma_document_cache": str(dense_cache),
            "embeddinggemma_document_cache_available": dense_cache.is_file(),
        },
        "summary": {
            "projection_status_counts": dict(sorted(projection_counts.items())),
            "mapped_article_counts": dict(sorted(article_counts.items())),
            "unmapped_offense_refs": dict(unmapped_refs.most_common()),
            "physical_issue_candidates": sum(selected_function_counts.values()),
            "unique_issue_candidates": len(issue_candidate_ids),
            "unique_anchor_cards": len(anchor_card_ids),
            "unique_retrieval_cards_in_selected_issues": len(retrieval_card_ids),
            "unique_selected_detail_cards": len(selected_detail_card_ids),
            "selected_issue_functions": dict(selected_function_counts.most_common()),
            "selected_issue_runtimes": dict(selected_runtime_counts.most_common()),
        },
        "corpus_capacity": {
            "cards": len(cards),
            "card_functions": dict(card_functions.most_common()),
            "issues": len(issues),
            "issue_functions": dict(corpus_issue_functions.most_common()),
            "issue_runtimes": dict(corpus_issue_runtimes.most_common()),
        },
        "call2_coverage": call2_coverage,
        "effect_boundaries": {
            "element_issue": "Call 2 predicate interpretation context; never auto-set predicate truth",
            "stage_issue": "completion/stage assessment context; never auto-set completion state",
            "participation_issue": "legal participation probe context; never synthesize a factual interaction",
            "guard_issue": "v2 doctrine/defense candidate context; activation still requires instance-scoped assessment",
            "concurrence_issue": "final-liability relation candidate; never absorb offenses from article match alone",
            "support_issue": "reasoning/IRAC support context; no symbolic effect",
        },
        "instances": instance_rows,
    }


def _markdown(audit: Mapping[str, Any]) -> str:
    scope = audit["scope"]
    summary = audit["summary"]
    capacity = audit["corpus_capacity"]
    call2 = audit["call2_coverage"]
    lines = [
        "# V2 instance-scoped card/issue join audit",
        "",
        "기존 issue-first 검색기를 canonical KCL-26의 top-level `OffenseInstanceKey`에",
        "결박한 offline candidate audit다. 카드 또는 issue hit는 법적 결론이 아니다.",
        "",
        "## 결과",
        "",
        f"- cases / instances: {scope['case_count']} / {scope['top_level_instance_count']}",
        f"- card fingerprint / dense cache: `{scope['card_corpus_fingerprint']}` / {scope['embeddinggemma_document_cache_available']}",
        f"- projection: {summary['projection_status_counts']}",
        f"- physical / unique issue candidates: {summary['physical_issue_candidates']} / {summary['unique_issue_candidates']}",
        f"- selected unique anchor/detail-universe cards: {summary['unique_anchor_cards']} / {summary['unique_retrieval_cards_in_selected_issues']}",
        f"- retrieval-selected unique detail cards: {summary['unique_selected_detail_cards']}",
        f"- current Call 2 UNKNOWN 중 exact card join 가능: {call2.get('card_joinable_unknown_targets', 0)} targets / {call2.get('card_joinable_unknown_predicate_refs', 0)} predicate refs",
        f"- selected issue functions: {summary['selected_issue_functions']}",
        "",
        "현재 자동 조인은 authored statutory identity가 있는 기본 offense에만 허용했다.",
        "DerivedOffenseDef의 base 조문을 따라가는 것은 정확한 죄명 조문 identity가 아니므로",
        "`UNMAPPED_DERIVED_ARTICLE`로 남겼다.",
        "",
        "## 카드 corpus가 보완할 수 있는 위치",
        "",
        f"전체 corpus는 {capacity['cards']} cards / {capacity['issues']} reviewed issues다.",
        "",
        "- `element_issue`: 현재 Call 2가 추상 predicate 정의만 보고 내는 semantic undercall과",
        "  UNKNOWN에 구체 판례·사례 기준을 제공한다. predicate truth는 여전히 neural 판단이다.",
        "- `stage_issue`: 실행착수·기수·중지미수 같은 completion 판단의 규범적 기준을 제공한다.",
        "- `participation_issue`: 교사·방조·공동정범의 법적 평가 기준을 제공하되 Call 1.5-P의",
        "  factual interaction을 대신 만들지는 않는다.",
        "- `guard_issue`: 위법성·책임 조각의 instance-scoped doctrine 후보를 연다.",
        "- `concurrence_issue`: 둘 이상의 established occurrence가 있을 때만 경합·흡수 후보를 연다.",
        "- `support_issue`: Rule/IRAC 설명과 근거 보강용이며 symbolic effect는 없다.",
        "",
        "## 검색기 사용 경계",
        "",
        "1. current closure/binding이 만든 offense instance의 정확한 조문으로 issue family를 제한한다.",
        "2. 해당 occurrence의 exact factual quote로 issue를 검색한다.",
        "3. 활성 issue 아래에서만 detail card를 최대 2장 회수한다.",
        "4. 검색 결과는 assessment context일 뿐 TRUE/FALSE, doctrine activation, absorption을 만들지 않는다.",
        "",
        "현재 audit는 재현 가능한 BM25 경로를 사용했다. 기존 embeddinggemma document cache와",
        "cross-encoder reranker는 같은 contract에 그대로 연결할 수 있다.",
        "",
        "## 선행 authoring gap",
        "",
    ]
    for ref, count in summary["unmapped_offense_refs"].items():
        lines.append(f"- `{ref}`: {count} instances")
    lines.extend(
        [
            "",
            "이 목록에 정확한 statutory identity를 검수·authoring하기 전에는 카드 자동 조인을",
            "열지 않는다. 특히 base article inheritance로 임시 보완하지 않는다.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--definitions", type=Path, default=Path("data/v2/definitions"))
    parser.add_argument(
        "--plan",
        type=Path,
        default=Path(
            "experiments/v2_call15_directscope_26_causal/evaluation_instance_plan.jsonl"
        ),
    )
    parser.add_argument(
        "--bindings",
        type=Path,
        default=Path("experiments/v2_call15_directscope_26_causal/issue_bindings.jsonl"),
    )
    parser.add_argument("--top-k-issues", type=int, default=3)
    parser.add_argument(
        "--call2",
        type=Path,
        default=Path(
            "experiments/v2_call15_directscope_26_causal/call2_full_v2/grounding_output.jsonl"
        ),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("experiments/v2_call15_directscope_26_causal/card_issue_join_v1"),
    )
    args = parser.parse_args()
    audit = build_audit(
        definitions=args.definitions,
        plan_path=args.plan,
        bindings_path=args.bindings,
        call2_path=args.call2,
        top_k_issues=args.top_k_issues,
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "audit.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n"
    )
    (args.output_dir / "audit.md").write_text(_markdown(audit))
    print(json.dumps(audit["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
