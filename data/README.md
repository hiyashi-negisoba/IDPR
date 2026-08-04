# Data assets

Raw benchmark, precedent, and commentary texts are not committed. This directory holds
reviewed or deterministically generated assets. The active runtime loads RuleIR assets
directly; older FactGraph/article-selection assets remain for historical experiments.

## Main assets

- `inventory/kcl_criminal_v1_draft.jsonl`: 61 KCL criminal-law sub-questions
- `commentary/kcl_criminal_v1_commentary_chunks.jsonl`: selected commentary chunks
- `rulegen/rule_ir_registry_manifest.json`: active closed runtime registry
- `rulegen/property/rule_ir/`: property RuleIR candidates
- `rulegen/p2/rule_ir/`: non-property RuleIR candidates
- `rulegen/p2/native_review/`: approval ledgers and legal-review provenance
- `../rules/generated/`: committed Scallop programs executed by the active host
- `eval/rubric_crime_article_map.json`: legally reviewed rubric-to-article map

`rulebase/`, `eval/fact_graphs.jsonl`, `eval/article_selection.jsonl`,
`eval/l0_candidates.jsonl`, `rulegen/fraud/`, and `e2e/fraud/` belong to older pipelines
or pilot reproduction unless the active registry explicitly points to an asset inside
them.

## External source configuration

Set source locations through environment variables or explicit CLI arguments. Do not
commit workstation paths.

- `IDPR_KCL_PARQUET`: source KCL parquet used for rubric evaluation
- commentary source paths: pass to the relevant offline builder CLI

Local model outputs belong under `experiments/results/`; diagnostic outputs and caches
are ignored by Git.
