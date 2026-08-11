# Step 8 — sub-question factual-scope / evaluation-universe source audit

Status: **completed audit; current source is insufficient for a route-scoped
26-case plan** (2026-08-11).

## Question

This audit asks only whether the benchmark supplies a deterministic mapping:

```text
sub_question_id -> exact factual text surface
```

It does not select an offense candidate, determine that a fact is legally
important, resolve an actor/event, or change frozen Call 1/Step 7 output.

## Existing structural evidence

The inventory has two relevant fields:

- `question_prompt`, which sometimes expressly refers to factual part `(n)`;
- `question_text`, which contains the whole question body plus the displayed
  prompt, and in most rows has top-level literal `(n)` headings.

For a numbered row, the mechanically available source rule would be limited to
removing the terminal displayed prompt by normalized-whitespace equality, then
taking the complete top-level `(n)` section(s) explicitly named by
`question_prompt`.  A prompt naming `(4)` and `(5)` would take those two
complete sections in source order.  This is benchmark structure recovery, not
semantic candidate filtering.

## 26-case source coverage

| Source status | Rows | Audit result |
| --- | --- | --- |
| Explicit numbered prompt + matching literal top-level headings | 21 | A deterministic factual-surface source is structurally feasible, subject to a separate contract fixing normalized terminal-prompt removal and heading boundaries. |
| Prompt names `(1)`, `(2)`, or `(3)`, but `question_text` has no corresponding factual headings | `kcl_criminal_r10_p1_q1_ga`, `kcl_criminal_r10_p1_q2`, `kcl_criminal_r10_p1_q3_ga` | **UNRESOLVED.** The present inventory gives no structural source for mapping the named factual part to a substring.  Inferring it from its legal topic, actors, or narrative meaning is prohibited. |
| Prompt does not name a factual part while the body contains several top-level factual sections | `kcl_criminal_r13_p1_q1`, `kcl_criminal_r13_p1_q3` | **UNRESOLVED.** Selecting a section because its actors appear in the prompt would be a new actor/event association rule, not explicit benchmark structure. |

`kcl_criminal_r11_p1_q1` is the only unnumbered whole-question prompt whose
prompt itself asks the listed actors' liabilities without selecting a numbered
part; retaining its whole factual body is structurally available.  It is
included in the 21 feasible rows.

## Evaluation-universe consequence

For the 21 structurally feasible rows, factual scope may remove material that
belongs solely to a different explicit numbered part.  It may **not** then
remove a Step 7 candidate because the candidate looks legally irrelevant.  The
only permitted universe rule is:

```text
scoped factual surface
  + frozen Call 1 top10 / Step 7 candidate universe for that sub_question
  -> evaluate every retained candidate under the same non-applicability rule
```

Whether Call 1 itself must be regenerated against the scoped source is not
decided here.  Reusing a frozen whole-question Call 1 artifact while changing
only Call 2 text could retain candidates discovered from excluded parts;
regenerating Call 1 would reopen a frozen artifact.  That choice therefore
requires its own source-lineage contract, not host legal filtering.

## Result and gate

```text
existing exact 26-case factual-scope source: NOT ESTABLISHED
structurally feasible rows: 21
unresolved source rows: 5
route-scoped 26-case planner regeneration: BLOCKED
```

The proposed manual benchmark structural-scope source is superseded.  Its five
unresolved rows show why a generic upstream occurrence-grounding surface is
needed: a reviewed neural occurrence stage may mark complete factual episodes
as query-relevant without deriving a substring from numbered headings.  This
audit remains evidence that no fallback manual scope map or legal-candidate
filter is allowed.
