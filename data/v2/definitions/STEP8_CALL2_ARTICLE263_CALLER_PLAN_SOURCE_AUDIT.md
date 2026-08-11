# Step 8 — Article 263 caller-plan source audit

Status: **completed audit; required caller-plan source does not yet exist**
(2026-08-11).

## Existing dedicated route

The frozen Article 263 backend contract is correct about its runtime boundary:

```text
surviving Step 7 statutory-deeming probe
  -> caller supplies existing underlying offense.injury instance
  -> Article 263 statutory truth + ordinary injury Elements/stage chain
```

The runtime does not select that instance.  Its entry point
`resolve_article_263_from_participation_probe(...)` receives an already built
`OffenseInstanceKey`, checks that `offense.injury` is active, and returns
`None` unless the three statutory leaves are TRUE.  This remains a dedicated
route, never a generic participation path and never `offense_ref=263`.

## Source finding

No frozen Call 1 artifact, Step 7 closure item, evaluation-instance plan, or
existing `data/eval/` artifact supplies the caller-owned mapping:

```text
(sub_question_id, surviving Article 263 probe)
  -> existing underlying offense.injury target
```

The rejected first planner's cartesian `(actor, offense.injury, o1)` keys are
not that source: for r10 they can mix the A sexual-assault injury sequence and
the B concurrent-independent-acts sequence.  Choosing `甲`, `乙`, A, or B from
those keys would be exactly the unapproved event/occurrence selection this
audit must not perform.

## Result and gate

```text
Article 263 dedicated runtime: FROZEN / retained
Article 263 caller-plan source: MISSING
r10 Article 263 route-scoped target: NOT AUTHORIZED
generic occurrence extraction as workaround: FORBIDDEN
```

The proposed manual Article 263 caller-plan source is superseded.  A general
validated occurrence universe must first create the existing injury occurrence
key; the frozen dedicated route can then run deterministically when its three
existing statutory leaves are TRUE.  This audit remains evidence that no
manual target map, generic occurrence regex, new offense identity, or
participation attribution may be used as a workaround.
