# IDPR

Logic-verified long-form legal document generation.

Quickstart for local development:

```bash
uv sync
cp .env.example .env
uv run pytest
```

The stage contracts in `docs/contracts/` are the API boundary. The initial
bootstrap implementation is deliberately deterministic so rule golden tests can
run without an LLM or GPU.

KCL commentary and fraud RuleIR artifacts can be regenerated without semantic
search or a GPU:

```bash
python scripts/build_kcl_criminal_inventory.py
python scripts/build_kcl_criminal_commentary_bundle.py
python scripts/build_fraud_rulegen_exemplar.py
```

The commentary-to-Scallop design is documented in
`docs/rulegen/scallop_rulegen_strategy.md`. API models emit source-grounded norm
candidates, NormCards, and RuleIR only; `idpr.rulegen` validates provenance and
compiles RuleIR locally.

The SKI-ML pilot reads credentials and model names from `.env`. Dry-run does not
call the Gateway:

```bash
python scripts/run_fraud_rulegen_pilot.py \
  --with-critic --limit 1 --run-id fraud-pilot-dry
```

Add `--execute` only after checking the dry-run. Valid responses and usage
manifests are cached under `.cache/llm/`; secrets and model reasoning are never
written to run manifests. The audited first fraud batch is tracked as
`data/rulegen/fraud/fraud_norm_candidate_batch_pass1_001_exemplar.json`. It
contains 62 exact-source candidates and 8 unresolved questions, and remains
`status=draft`.

Terra extraction includes the compact
`data/rulegen/fraud/fraud_norm_candidate_fewshot_gold.json` by default. It teaches
doctrine/precedent separation without attaching the full 62-candidate artifact to
every request. Use `--no-fewshot` for the paper's ablation condition.

The API compatibility and cost audit is in
`docs/rulegen/skiml_api_integration.md`. Critic findings are advisory: accepted
findings become bounded correction inputs, while final changes are applied as a
validated `NormCandidatePatch` instead of repeatedly regenerating the full
batch.

The provisional research framing, including the standalone workshop-paper task
and its connection to the earlier DCDE/OBJECTION work, is in
`docs/research/idpr_research_draft.md`.

The full Article 347 fraud preparation run is source-complete but still legally
pending. It contains 662 validated candidates and 636 candidate-linked NormCards.
Rebuild the deterministic final artifacts and review queue with:

```bash
python scripts/finalize_fraud_norm_candidate_batches.py
python scripts/finalize_fraud_norm_cards.py
python scripts/finalize_fraud_norm_card_critics.py
python scripts/build_fraud_legal_review.py
```

Start human review at
`data/rulegen/fraud/fraud_legal_review_guide.md`. Full RuleIR generation is
blocked until the source, authority, and policy-variant decisions in
`fraud_human_review_decisions.jsonl` are resolved. The existing eight-card fraud
RuleIR and Scallop files are structural exemplars, not approval of all 636 cards.
