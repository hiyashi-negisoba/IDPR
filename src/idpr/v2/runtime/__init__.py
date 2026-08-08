"""Case-time runtime (v2.2.0, build-order step 6).

The Definition Layer (v2.1.0, `idpr.v2.*`) answers "what does the law require?" and knows nothing
about any particular case. This package answers "what follows for THIS actor in THIS case?" and is
the only place case identity exists.

The layering rule that keeps that separation real: **`idpr.v2.runtime` imports from `idpr.v2`,
never the reverse.** Definition-layer modules stay case-blind, and the runtime adapts at the
boundary (see `truths.CaseTruths`, which hands v2.1 functions exactly the mapping types they
already take). `tests/test_v2_runtime_identity.py` asserts this import direction mechanically.
"""
