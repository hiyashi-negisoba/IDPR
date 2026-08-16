# KCL-26 LLM-Judge Metrics and Results

Judge model: `anthropic/claude-sonnet-4-6` (SKI-ML LiteLLM gateway), temperature 0.0,
`reasoning_effort=low`. Protocol: `data/eval/phase3_judge_protocol.json` v1.0.0. Prompt:
`prompts/phase3_kcl_pointwise_judge.md`. Case set: 26 KCL substantive-law questions
(`data/eval/kcl_substantive_case_ids.txt`, a fixed subset of the 61-question inventory).
Rubric: sealed per-question rubric items from the KCL bar-exam-style inventory
(`data/inventory/kcl_criminal_v1_draft.jsonl`), median ~28 items/question.

Our system's final measured condition this round: `v2_idpr_p_v2_aligned_26` (P, "Ours
full") and `v2_idpr_n_v2_aligned_26` (N, card-retrieval-channel ablation). Generation
backbone: `idpr-gemma-4-26b-a4b` (local vLLM), evaluation commit
`agent/v2-semantic-integrity-fix@13232a5`. This is the version after two rounds of fixes
this session: (1) a Scallop-compiler wiring fix for `defeated_by_state` completion-state
yielding, (2) a Call 3 prompt change making retrieved precedent/doctrine citations
mandatory rather than optional, and (3) a post-hoc conclusion-alignment pass. Raw
judgments: `experiments/results/phase3_judge_sonnet_pn_v2_aligned/judgments.jsonl`.
Pooled per-method summary: `experiments/results/phase3_judge_sonnet_pn_v2_aligned/kcl26_pooled_metrics.json`.
Full narrative: `docs/analysis/v2_qualitative_cot_vs_idpr_ko.md` §11 (Korean).

## 1. Metrics

The judge produces four independent scores per (method, question) pair from a single
structured completion. All four are computed by `src/idpr/eval/phase3_judge.py:reduce_judge_output`
from the judge's raw output plus an evidence safeguard (every quoted claim must appear
verbatim, at minimum length, in the actual answer text -- unquotable claims are dropped
before scoring, so a model cannot get credit, or take a penalty, for something the judge
merely characterized rather than found in the text).

### 1.1 Coverage — `met rubric items / all rubric items`

Each of the ~28 sealed rubric items is scored `met` (full credit), `partially_met` (half
credit -- e.g. the correct legal standard is stated but not applied to the facts, or the
conclusion is right but under-argued), or `not_met` (0 credit -- absent, reversed, or a
required element missing). `coverage_macro` is the case-level mean of `(met + 0.5 ×
partially_met) / total_items`, averaged again across the 26 questions. A rubric item
resolved as UNRESOLVED (the system's genuine legal posture, not a missing answer) is not
automatically `not_met` if the reasoning substance backing that posture is present --
this exception was added to the judge prompt this round specifically to prevent
penalizing a well-argued abstention the same as an omission.

### 1.2 Precision — `numerator-class claims / all deduplicated substantive claims`

The judge decomposes the answer into atomic, non-redundant legal claims and classifies
each: `gold_aligned_correct`, `necessary_bridge_correct` (both count toward the
numerator), `relevant_correct_extra`, `irrelevant`, `incorrect`, or `unverifiable`.
`precision_macro` is the case-level ratio, averaged. This is the metric closest to "of
everything asserted, how much was right and on-target" -- distinct from coverage
("of everything the rubric wants, how much is there").

### 1.3 Hallucination — severity-weighted incident count, two presentations

The judge records every substantive legal or factual error as a discrete incident with a
`kind` (`nonexistent_offense`, `fabricated_case`, `doctrinal_error`, `statutory_error`,
`factual_invention`, `other`) and a `severity`:

| severity | weight | meaning |
|---|---:|---|
| `minor` | 1 | peripheral inaccuracy, doesn't change the central conclusion |
| `major` | 2 | wrong on an element, illegality, culpability, concurrence, or evidentiary point |
| `critical` | 3 | invented offense/attempt category, fabricated case citation, or a fabricated doctrine that reverses the core liability conclusion |

**Raw score** (`hallucination_score_macro`): the negative case-level sum of severity
weights, averaged across cases. Zero is best; there is no lower bound, since a
sufficiently bad answer can accumulate arbitrarily many incidents. This is the metric to
report for statistical comparison (paired bootstrap), since it is the one the judge
actually emits without any post-hoc rescaling.

**Normalized score** (`hallucination_norm`, added this round for readability, *not* part
of the judge protocol itself): a `[0, 1]` rescaling anchored at the two ends that are
independently meaningful --

```
hallucination_norm = clip( (score - worst_in_pool) / (0 - worst_in_pool), 0, 1 )
```

`0` (no incidents) maps to `1.00` unconditionally -- this anchor is principled, not
relative. The *other* anchor, `0.00`, is **empirical**: it is fixed to whichever method
currently has the worst `hallucination_score_macro` in the comparison pool (currently
`fol_autoformalizer_solver` at −4.200). **This means the normalized score is relative to
the current comparison pool, not an absolute scale** -- adding a new, worse baseline to
the pool later will compress every other method's normalized score upward, and this
column should be recomputed (not reused) whenever the pool changes. Use the raw score for
any claim that needs to survive the pool changing; use the normalized score only for
presentation.

### 1.4 Consistency — `score / 4`, logical coherence independent of legal correctness

A single 0-4 ordinal judgment of whether the answer's own argument holds together --
explicitly scored independent of whether the conclusion is legally correct (an answer
that is wrong throughout but internally coherent scores 4; an answer that reaches the
right conclusion by way of a self-contradiction scores lower).

| score | meaning |
|---:|---|
| 4 | no internal contradiction or conclusion drift |
| 3 | minor phrasing wobble only; argument and conclusion stay coherent |
| 2 | a major local inconsistency -- one section's conclusion conflicts with another section or with the final summary |
| 1 | position changes across multiple sections, or the conclusion barely follows from the argument |
| 0 | the whole answer is mutually contradictory and cannot be read as one argument |

Two clarifications were added to the judge prompt this round, both aimed at a specific
failure mode this project's own hedged/UNRESOLVED reasoning style is prone to: (a)
conditional prose ("X is unresolved; if X holds, Y follows, otherwise Z") stated on an
explicitly-flagged unresolved predicate is not itself a contradiction -- only asserting
the condition in one place and quietly overriding it in another counts; (b) code or
formal-logic traces embedded in the answer (Scallop/Z3/Prolog, etc.) are checked for
circularity -- restating the conclusion as a premise and then reporting it as
"derived"/"satisfiable" does not count as an independent derivation and is scored as a
major local inconsistency regardless of how many times the same conclusion is echoed
across formats.

**Consistency currently has no severity/impact weighting** -- a violation that flips the
final liability outcome and a violation that only unsettles a supporting sub-point both
land in the same 0-4 bucket. A severity-weighted redesign analogous to hallucination's
`minor`/`major`/`critical` scheme (tagging each violation with whether it is
outcome-changing) is sketched but not implemented; see §3.

## 2. Results — 26-case KCL substantive-law subset

Pooled from four separately-run, protocol-identical judge jobs (same prompt/protocol/schema
SHA-256 across all four, verified before pooling), then re-aggregated over the fixed
26-case list so every method is compared on the same questions regardless of which job
originally scored it.

**Ours** -- final measured version only (`agent/v2-semantic-integrity-fix@13232a5`,
citation-mandate + conclusion-alignment applied). Superseded intermediate runs from
earlier this round (pre-citation-mandate P/N, and the unrelated older v1 pipeline results
`idpr_nsn_lean_61` / `idpr_nsn_lean_61_routing_fix`) are intentionally excluded from this
table to avoid conflating versions; see `docs/analysis/v2_qualitative_cot_vs_idpr_ko.md`
§11 for that history if needed.

| method | n | consistency | coverage | precision | hallucination (raw) | hallucination (norm, this pool) |
|---|---:|---:|---:|---:|---:|---:|
| **Ours, P ("full")** | 26 | **0.936** | 0.191 | **0.584** | **−2.692** | **0.359** |
| **Ours, N (card channel off, ablation)** | 26 | **0.933** | 0.168 | 0.514 | −3.269 | 0.222 |

**External baselines** (all run once, single-sample, same judge protocol):

| method | n | consistency | coverage | precision | hallucination (raw) | hallucination (norm, this pool) |
|---|---:|---:|---:|---:|---:|---:|
| chain_of_thought | 26 | 0.827 | **0.211** | 0.522 | −3.654 | 0.130 |
| acal | 26 | 0.856 | 0.168 | 0.456 | −3.231 | 0.231 |
| legal_chain_reasoner | 26 | 0.933 | 0.166 | 0.476 | −3.538 | 0.158 |
| vanilla_zero_shot | 24 | 0.854 | 0.151 | 0.478 | −3.708 | 0.117 |
| standard_rag | 26 | 0.885 | 0.149 | 0.503 | −3.308 | 0.212 |
| leprec | 26 | 0.837 | 0.140 | 0.435 | −3.231 | 0.231 |
| fol_autoformalizer_solver | 25 | 0.750 | 0.101 | 0.394 | −4.200 | 0.000 |

Bold marks the best value in each column (across both tables). Ours (P) leads
hallucination and precision, and is statistically tied with the coverage leader (CoT) --
see below. Ours trails on consistency; §3 traces why.

### 2.1 Paired bootstrap (target = ours, P), vs. select baselines

10,000-sample case-paired bootstrap, seed 20260803, metric-specific paths matching the
protocol (`consistency.normalized_score`, `coverage.rubric_score`, `precision.score`,
`hallucination.score`). Delta is (P − baseline); a 95% CI excluding zero is significant.

| vs. | metric | delta | 95% CI | significant? |
|---|---|---:|---|:---:|
| chain_of_thought | coverage | −0.019 | [−0.077, +0.033] | no (statistical tie) |
| N (card-channel ablation) | precision | +0.070 | [+0.002, +0.142] | **yes** |
| N (card-channel ablation) | coverage | +0.023 | [−0.0002, +0.046] | borderline |
| N (card-channel ablation) | consistency | −0.058 | [−0.154, +0.029] | no |
| N (card-channel ablation) | hallucination | +0.577 | [−0.192, +1.308] | no |

The P−N precision result is the cleanest single-variable finding of this round: with the
symbolic anchor held byte-identical between P and N (verified via `required_final_conclusions`
equality across all 26 cases) and only the retrieved-card channel toggled, precision
moves significantly. Coverage moves the same direction but the CI just crosses zero.

## 3. Known gap and the corresponding future-work item: consistency

Ours trails on consistency (0.750, tied lowest in this pool) despite leading on
hallucination and precision -- the same asymmetry documented qualitatively for the
chain-of-thought baseline throughout this analysis: a confidently-wrong single-narrative
answer reads as more internally coherent to the judge than a correctly-hedged one that
drops a step midway through a long generation. Two independent case reads (not merely
trusting the judge's own rationale) confirmed the judge's specific violation calls were
correct, not an artifact of misreading legitimate hedging as contradiction.

All 21 valid consistency violations in the P condition (26 cases) were traced against
their `analysis` payload (the structured input actually sent to the answer-writing step)
to separate what the generation pipeline can fix from what requires rule-base authoring:

| cause | count | fixable by |
|---|---:|---|
| authored card/dispute content itself conflates two doctrines | 2 | rule-base authoring correction |
| a required doctrinal move (e.g. scope-of-instigation limitation) was never triggered into the payload at all | 2 | rule-base authoring (new predicate/trigger) |
| body-vs-final-conclusion drift the alignment pass (added this round) should have caught but didn't | 4 | widening the alignment pass beyond the final section |
| contradiction between two body sections, outside any pass's current scope | 6 | widening the alignment pass to the whole answer |
| judge-flagged but self-downgraded as non-major | 4 | same, lower priority |

**17 of 21 (81%) are attributable to the generation/alignment pipeline, not to rule-base
content.** A per-case ceiling estimate -- assuming every case whose violations are
entirely pipeline-attributable reaches the maximum score, and cases with any
rule-base-attributable violation stay at their current score -- puts consistency at
**≈0.93-0.94** if the pipeline-side 17 were fully resolved, against a current pool
maximum of 0.933 (`legal_chain_reasoner`). This is a case-level estimate, not a
re-measured result; it is presented as a target for a follow-up round, not a finding.

The same exercise on the **N** condition (17 valid violations, 2 dev cases read in full,
the remaining 15 classified from violation text against the same rule-base-content vs.
pipeline split, at lower verification depth than the P pass above) gives a comparable
ratio: 13/17 (76%) pipeline-attributable, 4/17 rule-base-attributable (1 authored-content
conflation, 3 missing-doctrine-trigger). Ceiling estimate: **≈0.93**, against a current
measured N consistency of 0.808. The two conditions' ceilings landing at roughly the same
value, near the current pool maximum, is consistent with the underlying cause being a
property of the shared answer-generation/alignment pipeline rather than of the P-specific
card-retrieval channel.

Remaining, not yet started as of this document: widening the conclusion-alignment pass's
scope from the final section to the whole answer body (targets the 6+4 rows above); a
severity/impact-weighted redesign of the consistency score itself, analogous to
hallucination's severity weights, so a violation that changes the final liability outcome
is scored differently from one that only unsettles a supporting point (design sketched,
not implemented, requires a judge protocol/schema change); and the router/rule-base
recall gap that remains the largest single lever on coverage independent of consistency
(unchanged from earlier rounds, still not started).
