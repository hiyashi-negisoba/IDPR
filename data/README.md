# Data assets

Raw benchmark, precedent, and commentary texts are not committed. This directory holds
reviewed or deterministically generated stage-boundary assets.

## Main assets

- `inventory/kcl_criminal_v1_draft.jsonl`: 61 KCL criminal-law sub-questions
- `commentary/kcl_criminal_v1_commentary_chunks.jsonl`: selected commentary chunks
- `rulebase/card_catalog_v2.json`: normalized card roles and loading policies
- `rulebase/issue_catalog_v2.json`: article → issue → anchor/detail hierarchy
- `rulebase/kcl_rulebase.scl`: compiled Scallop program
- `eval/fact_graphs.jsonl`: admitted fact graphs
- `eval/article_selection.jsonl`: neural article proposals
- `eval/l0_candidates.jsonl`: persisted article and issue scope
- `eval/rubric_crime_article_map.json`: legally reviewed rubric-to-article map

The `rulegen/fraud/` and `e2e/fraud/` trees are archived pilot artifacts. They remain for
reproduction and provenance, but the current pipeline does not load them as runtime
contracts.

## External source configuration

Set source locations through environment variables or explicit CLI arguments. Do not
commit workstation paths.

- `IDPR_KCL_PARQUET`: source KCL parquet used for rubric evaluation
- commentary source paths: pass to the relevant offline builder CLI

Local model outputs belong under `experiments/results/`; diagnostic outputs and caches
are ignored by Git.
