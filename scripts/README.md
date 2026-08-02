# Script entry points

## Active pipeline

- `run_call1_fact_graphs.py`: grounded fact extraction
- `run_article_select.py`: neural article proposal
- `run_l0_candidates.py`: retrieval/proposal union and issue scope persistence
- `run_issue_assessment.py`: issue assessment plus Scallop composition for one case
- `run_issue_answer.py`: constrained offence-level IRAC generation for one case
- `run_issue_pipeline_batch.py`: resumable dataset sweep
- `refresh_l0_issue_catalog.py`: deterministic refresh after rule-catalog changes

## Diagnostics

Fixed-case checks and historical flat-card comparisons live under `diagnostics/` and
`slurm/diagnostics/`. They may contain explicit fixture IDs by design and must not be used
as production entry points.

## Archived pilot and rule-generation tools

Files whose names begin with `fraud_`, `property_`, or `rulegen_` reproduce earlier
article-specific data-construction experiments. Their runtime code lives under
`src/idpr/legacy/` when it is not part of the general card/issue compiler. They are not
imported by the active pipeline.
