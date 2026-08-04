# IDPR documentation map

Start with [`handoff/CURRENT.md`](handoff/CURRENT.md). It is the only document that
describes the current implementation status, known defects, and next work in one place.

## Authoritative documents

- [`../README.md`](../README.md): active entry point and short run instructions
- [`handoff/CURRENT.md`](handoff/CURRENT.md): current state and next work
- [`handoff/DESIGN.md`](handoff/DESIGN.md): RuleIR-native design and invariants
- [`handoff/RECOVERY.md`](handoff/RECOVERY.md): where the pipeline broke and how it was recovered
- [`../project_init.md`](../project_init.md): original end-state architecture and contracts
- [`contracts/`](contracts/): machine-readable API contracts

## Supporting evidence and reference

- [`audits/`](audits/): reproducible registry and prompt audit outputs
- [`review/`](review/): legal review packets, decisions, and gates
- [`rulegen/`](rulegen/): RuleIR generation reference
- [`research/`](research/): research notes; not an active implementation contract
- [`gemma_profiles/`](gemma_profiles/): model-serving reference

## Archive

[`archive/`](archive/) contains superseded handoffs, pipeline designs, incident reports,
conversation dumps, and cumulative work logs. Archive documents are historical evidence,
not instructions for the active pipeline. Do not implement from them without checking
`handoff/CURRENT.md` and the current code.
