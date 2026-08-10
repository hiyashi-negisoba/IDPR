# v2 Definition Layer assembly

This directory is the production Definition Layer.  It is intentionally separate
from `docs/contracts/v2/examples/`, whose fixtures remain frozen.

The approved execution phases and HOLD boundaries are in
[`ASSEMBLY_PLAN.md`](ASSEMBLY_PLAN.md).

## Authoring unit and build order

The registry's authoring unit is one YAML list per Definition Layer kind, not one
file per statute.  Every file named in `src/idpr/v2/registry.py::KIND_TO_EXAMPLE_FILE`
must exist, including empty lists for kinds not reached by the current slice.

Author in dependency order (the registry's fixed file-iteration order is not a
build order; it first creates a flat index and then type-checks the whole graph):

1. `ground_facts.yaml` and `legal_elements.yaml`
2. `element_bundles.yaml`, `primitives.yaml`, `relations.yaml`, and `qualifiers.yaml`
3. Independent General Part objects: `doctrines.yaml` and
   `participation_policies.yaml`; base offenses in `offenses.yaml`
4. `exported_components.yaml` (after its source base offense)
5. `derived_offenses.yaml` (after every referenced offense/component/relation)
6. `completion_policies.yaml` (after its offense or derived offense, and any
   relation it disposes)

`DerivedOffenseDef.flattened_elements` is compiler-replayed cache data: author its
`derivation` first and verify the cache through the type checker; never treat the
cache as an independent source of truth.  A doctrine is independent from an
offense assembly, so this first slice can safely finish its doctrine objects after
their leaf predicates are loaded.

## Gate① boundary

This slice transcribes only Gate①-frozen predicates from
`predicate_dictionary_master_v3.md`, plus any canonical erratum explicitly
recorded in `ASSEMBLY_CROSSWALK.md`. It does not change the 80-article evaluation
population. The empty files are deliberate assembly placeholders, not a claim
that the corresponding definition kinds are complete.
