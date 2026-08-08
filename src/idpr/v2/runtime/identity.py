"""Case-time identity (build-order step 6A).

Step 5 left a boundary in writing, and this module is the other side of it:

    v2.1  RelationInstanceKey = definition-occurrence identity
                               (top-level offense id + the local_key chain traversed)

    v2.2  runtime identity    = case / actor / offense-occurrence namespace
                               WRAPPING that key, never rewriting it

`RelationInstanceKey` already answers "which relation occurrence inside this definition tree?" and
that answer does not change with the case. What changes per case is "for whom, and for which
realization of the offense, are we applying this definition?" -- so runtime keys wrap. Pushing
case/actor fields *into* `RelationInstanceKey` would make the definition layer know about cases and
break the v2.1/v2.2 split exactly there.

Two layers, not one (this was a real design error in the first draft):

    OffenseInstanceKey   facts attach here.        NO form field.
    OffenseFormKey       program selection.        Produced by Completion (step 6B).

Putting `form` in the fact-bearing key creates a circular dependency -- you need truths
(death=FALSE, commencement=TRUE, ...) to decide the form, but the truths' own key would already
contain the form -- and it would store the same facts twice, once per form. `form` is not a
namespace for facts; it selects which program those facts are run against.
"""

from __future__ import annotations

from dataclasses import dataclass

from idpr.v2.relations import RelationInstanceKey


@dataclass(frozen=True)
class OffenseInstanceKey:
    """One offense realization under evaluation, for one actor, in one case.

    Hashable by construction (frozen, str fields only), so it is used directly as a mapping key.
    """

    case_id: str
    actor_id: str
    offense_ref: str
    """Top-level OffenseDef / DerivedOffenseDef id."""

    occurrence_id: str
    """Distinguishes two realizations of the SAME offense by the SAME actor in the same case --
    e.g. 甲 stealing from A and then, separately, from B. Without it those two collapse to one key
    and one set of facts answers for both. This is not 죄수론 (Open Question #6, out of scope):
    concurrence reasoning operates *on* separately identified occurrences, so identifying them is
    strictly upstream of it and belongs here."""


@dataclass(frozen=True)
class OffenseFormKey:
    """Which completion form's program is being run for an instance.

    Wraps `OffenseInstanceKey` rather than extending it, so facts (keyed by the instance) stay
    shared across every form that instance is evaluated under. Step 6B (Completion) produces these;
    step 6A only ever constructs the "completed" one.
    """

    instance: OffenseInstanceKey
    form: str


@dataclass(frozen=True)
class RuntimeRelationKey:
    """A relation obligation at a definite place in a definite case.

    `definition_key` is embedded verbatim -- never re-derived, never flattened into strings. Keyed
    on the base instance, not on a form: whether `causal_nexus` in fact holds is a proposition about
    the case and does not depend on which completion form is being evaluated. Whether a given form
    still *requires* that relation is CompletionPolicy's job (step 6B), not the truth store's.
    """

    instance: OffenseInstanceKey
    definition_key: RelationInstanceKey
