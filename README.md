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

The provisional research framing, including the standalone workshop-paper task
and its connection to the earlier DCDE/OBJECTION work, is in
`docs/research/idpr_research_draft.md`.
