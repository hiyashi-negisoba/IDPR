# Script entry points

## Active pipeline

- `run_call1_fact_graphs.py`: grounded fact extraction
- `run_l0_candidates.py --routing-policy retrieval_only`: ranked retrieval-lane artifact
- `run_article_select.py`: question-domain routing plus mandatory review of every retrieved
  article; the model may supplement missing articles from the closed catalog
- `run_l0_candidates.py --routing-policy reviewed_selection`: activate only reviewed
  articles, preserve retrieval provenance, and persist the normalized issue scope
- `run_issue_assessment.py`: issue assessment plus Scallop composition for one case
- `run_issue_answer.py`: constrained offence-level IRAC generation for one case
- `run_issue_pipeline_batch.py`: resumable dataset sweep
- `refresh_l0_issue_catalog.py`: deterministic refresh after rule-catalog changes

The stage order is retrieval → review → scope assembly. Retrieval is a discovery lane,
not an authorization to open every matched article in Call 2. `legacy_union` remains an
explicit `run_l0_candidates.py` policy only to reproduce Phase-2 measurements.

## Diagnostics

Fixed-case checks and historical flat-card comparisons live under `diagnostics/` and
`slurm/diagnostics/`. They may contain explicit fixture IDs by design and must not be used
as production entry points.

## Archived pilot and rule-generation tools

Files whose names begin with `fraud_`, `property_`, or `rulegen_` reproduce earlier
article-specific data-construction experiments. Their runtime code lives under
`src/idpr/legacy/` when it is not part of the general card/issue compiler. They are not
imported by the active pipeline.
