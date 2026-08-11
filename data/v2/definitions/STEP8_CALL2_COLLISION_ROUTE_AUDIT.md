# Step 8 — collision-route audit

Status: **PASS / FROZEN; no generic occurrence producer or planner extension is
approved** (2026-08-11).

## Question before occurrence identity

The first `"o1"` plan and the preserved multi-occurrence inventory show that
some generated keys can combine distinct factual events.  This audit does not
respond by extracting events from raw case text.  It first asks, for each
collision family:

1. which sub-question issue requires the actor/offense key;
2. whether it is a direct liability target, Article 263 dedicated-route input,
   participation dependency, or closure-expanded candidate;
3. whether more than one `OffenseInstanceKey` is actually required by that
   legal evaluation route.

The audit must use frozen Call 1 top10 lineage, Step 7 closure, the selected
sub-question, and the existing dedicated Article 263 route.  It may not create
an occurrence ID, choose a factual event, or broaden a generic multi-occurrence
subsystem.

## Required output per collision family

```text
collision family
  -> emitted root and structurally related candidate refs
  -> sub-question issue / report target
  -> legal evaluation route classification
  -> whether multiple runtime instances are necessary
  -> permitted next action, or rejection
```

## Gate

No new occurrence-discrimination contract is permitted until this audit shows
that a collision is required by a direct, non-special-route, same-actor
liability evaluation.  Article 263 inputs remain owned by their dedicated
statutory-deeming route.  Closure-expanded irrelevant candidates must be
addressed at the evaluation-universe policy layer, not through occurrence
extraction.

## Frozen evidence

The audit used the frozen Call 1 top10 artifact, the rejected first planner
artifact, each `question_prompt`, and the Article 263 backend-completion
contract.  The material boundary is important: the inventory and planner read
the whole inventory `question_text`, while several frozen prompts expressly
ask only about numbered factual parts such as `(1)` or `(2)`.

## Collision-route classification

| Family / rows | Why the root entered the first universe | Route classification | Are multiple generic `OffenseInstanceKey` values established as necessary? | Required action |
| --- | --- | --- | --- | --- |
| r10 injury: q1/q2/q3 | `offense.injury` is a frozen Call 1 seed in all three rows.  The A injury is in the sexual-assault sequence; the B injury is the separate concurrent-acts / unascertained-causation sequence involving 甲 and 乙. | For the B sequence, **Article 263 dedicated-route input**, not a generic participation or generic occurrence route.  q3's prompt is for 甲/丙/丁 and its bribe-delivery issue; its injury candidate is closure-expanded relative to that stated issue. | **No.** The dedicated Article 263 caller plan must own whether and how the B concurrent-acts configuration reaches its existing underlying `offense.injury` route.  This audit does not authorize `injury:A` / `injury:B` runtime identities. | Re-audit the Article 263 caller-plan/source boundary separately.  Remove or reject q3's irrelevant injury universe at the evaluation-universe layer. |
| r12 homicide: q1-ga/q1-na | Both rows read one whole four-part narrative and seed `offense.homicide`.  q1-ga expressly asks only `(1)` about 甲/乙: B's death is in (1), while A's ventilator death is in (2).  q1-na expressly asks `(2)` only about 乙; its collision is on support actor 甲 and imports B from (1). | **Sub-question factual-scope leakage plus full actor × candidate expansion.**  The apparent B/A pair is not established as two direct homicide targets required by either supplied sub-question. | **No.** Each stated sub-question needs, at most, its own factual part's ordinary route.  The frozen whole-question source prevents the current planner from proving that boundary. | A deterministic sub-question factual-scope source must be reviewed before any occurrence identity work.  No homicide occurrence split is authorized. |
| r14 forcible indecency: q1/q2/q4 | The rows read a two-part narrative and seed `offense.forcible_indecency`.  The X/Y/Z recorded-act material is in (2), while q1 and q2 expressly ask only `(1)` about 甲/乙; q4 asks `(1)` about 丙's public-duty issue. | **Closure-expanded irrelevant candidate caused by whole-question factual-scope leakage.**  丙 is a report target in q4, but the stated issue is public-duty obstruction, not the (2) sexual-offense material. | **No.** No supplied sub-question has established the X/Y/Z acts as simultaneous direct liability targets for this Call 2 route. | Exclude/reject the leaked candidate through a reviewed factual-scope/evaluation-universe policy; do not generate `forcible_indecency:X/Y/Z` instances. |

## Result

```text
Article 263 configuration collision: 1 family
  -> dedicated statutory route / caller-plan source review

whole-question factual-scope leakage + closure expansion: 2 families
  -> evaluation-universe source review

direct non-special-route same-actor multi-occurrence requirement established: 0
generic multi-occurrence runtime subsystem authorized: 0
```

The collision inventory remains valid as evidence that the first cartesian
universe is unsound.  It does not establish that all listed root collisions
need runtime occurrence IDs.  In particular, the rejected regex/pattern-table
approach is not revived by this audit.

## Next gate

The next work is deliberately split:

1. the **sub-question factual-scope / evaluation-universe source audit** is
   complete and found that five rows lack an explicit structural source; and
2. the **Article 263 caller-plan source audit** is complete and found no source
   for the existing underlying injury target.

The two source audits showed that manual factual-scope recovery and an Article
263 target map would only recreate the same missing-event problem at a lower
layer.  They are preserved as negative evidence.  The next review unit is
therefore `STEP8_GENERAL_OCCURRENCE_GROUNDING_CONTRACT.md`: one general neural
factual-occurrence universe, with host span IDs, before any offense instance is
planned.  It supersedes the proposed two source contracts, not the frozen
Article 263 runtime.
