# Step 8 — Call 2 GroundFact grounding contract and prompt review

Status: **Call 2 frozen with a non-destructive factual adapter**
(2026-08-10).  Two 26-case pilots validated the runner/schema, top10 Step 7
replay, artifact, proposition projection, and adapter.  Their semantic
calibration shows that an unbound proposition-level `FALSE` is not reliable
enough to prune a structural path, so Call 2 preserves it as an observation and
maps it to `KEEP`.

This is the next bounded Step 8 task after the frozen Call 1 router at
`deadline_v2_0808` commit `6275987`.  It consumes Call 1's already-recorded
Step 7 result.  It does not reopen the Call 1 router, its ten-seed cap or
normalization, the Step 7 compiler, the 293-object registry, the sealed Gate①
sources, or the coverage boundary.

## Purpose and boundary

Call 2 makes one three-valued factual observation for every distinct GroundFact
*proposition* in the Step 7 `ground_fact_frontier`:

```text
case_text + distinct GroundFact propositions from the occurrence-preserving frontier
  -> TRUE | FALSE | UNKNOWN for each GroundFact proposition
  -> host projects that result to every requesting structural occurrence
```

It is not an offense classifier or a legal evaluator.  In particular, Call 2
does not select or reject an offense, decide an element, relation, doctrine,
completion state, participation mode or actor, assess responsibility, or emit a
legal effect, rationale, confidence, evidence span, event, or verdict.

Step 7 occurrences are structural identities, not case-specific fact instances:
they provide a `ground_fact_ref`, `source_path`, and `occurrence_path`, but do
not bind GroundFact arguments to a particular actor, object, or event in the
case.  An opaque occurrence ID therefore cannot make two occurrences of the
same ref different factual propositions.  Call 2 must not pretend otherwise or
ask the model to make different truth decisions from that ID alone.

The host first performs an explicit, stable first-occurrence projection from
the Step 7 occurrence frontier to unique `ground_fact_ref` propositions.  It
retains both the full occurrence frontier and the proposition-to-occurrences
mapping in the artifact.  After validation, it projects each proposition's
single status back to all structural occurrences that request it.

The host then uses the projected status only at each supplied structural
occurrence:

| Call 2 status | Host action |
|---|---|
| `TRUE` | `OPEN`: retain the occurrence's factual path. |
| `FALSE` | `KEEP`: retain the occurrence's factual path while preserving the model's `FALSE` observation in the artifact. |
| `UNKNOWN` | `KEEP`: retain the path without treating missing support as FALSE. |

`TRUE` is not a legal-element truth and `OPEN` is not an offense activation.
This Call 2 contract does not populate `CaseTruths`, run an expression, prune a
path, or make any later-stage decision; the separately designed downstream
adapter will own those operations.  Case-specific bindings would be a separate
upstream design task; they are deliberately not added to this Call 2 contract.

## Draft wire contract

The host derives an ordered, de-duplicated proposition list by stable first
occurrence of `ground_fact_ref` in the deterministic Step 7 frontier.  The
model sees only that list.  The host retains every original occurrence with its
`source_path` and `occurrence_path`, plus the explicit proposition-to-occurrence
projection, in its artifact.  Neither structural path is model-visible because
it exposes unnecessary upstream legal context and cannot supply a case-specific
binding.

```json
{
  "case_text": "…",
  "ground_facts": [
    {
      "ground_fact_ref": "ground_fact.example",
      "canonical_meaning": "positive factual proposition",
      "arguments": [{"name": "actor", "type": "entity"}]
    }
  ]
}
```

`ground_fact_ref`, `canonical_meaning`, and `arguments` are mechanically read
from the loaded `GroundFactDef`.  They are vocabulary needed to state the fact,
not a case-specific legal mapping.  `ground_facts` has each canonical ref once;
the corresponding occurrence-preserving Step 7 frontier is retained by the
host and is not silently discarded.

The only accepted model response is:

```json
{
  "groundings": [
    {"ground_fact_ref": "ground_fact.example", "truth": "TRUE"}
  ]
}
```

`groundings` must contain exactly one entry for every supplied GroundFact
proposition, in the same order.  No additional property, GroundFact ref, or
truth label is accepted.  The host hard-validates JSON shape; the exact input
cardinality and ordering of `ground_fact_ref`; unique, known refs; and the
closed truth vocabulary `TRUE`, `FALSE`, `UNKNOWN`.  Any malformed response,
empty or wrong-length list, reordered/duplicate/unknown/missing ref, or other
label is a Call 2 contract failure.  The raw model response, the stable
proposition projection, and the host-validated proposition-to-occurrence status
join are all retained; only the structural projection is deduplicated, never
the Step 7 frontier artifact.

The host does not call a model for an empty frontier.  That is a deterministic
no-op with no Call 2 output rather than permission to request an empty response
from the model.

## Truth-label instruction

Each label applies only to the supplied positive `canonical_meaning` as a fact
in `case_text`:

GroundFact arguments are not case-bound in Call 2.  Therefore, when a
GroundFact has arguments, its truth is evaluated existentially over the case:
`TRUE` means that at least one directly stated factual instance satisfies the
canonical proposition.  A contrary statement about some other actor, object,
or event does not make the proposition `FALSE`.  `FALSE` is allowed only when
the case text directly establishes that no instance compatible with the
proposition can exist; otherwise use `UNKNOWN`.

- `TRUE`: case text directly establishes that fact.
- `FALSE`: case text directly establishes that no instance compatible with the
  stated positive fact can exist.
- `UNKNOWN`: neither is directly established, including silence, ambiguity,
  competing accounts, unresolved proof, or a conclusion that would require a
  legal standard or inference beyond the stated fact.

Thus absence of an allegation or evidence is never `FALSE`, and a plausible
theory is never `TRUE`.  A GroundFact's authored wording may be used solely to
identify its factual proposition; it must not be expanded into a legal-element
or offense test.

## First pilot calibration record

The first 26-case pilot artifact is retained as semantic calibration evidence:

```text
/data5/jaehoonjeong/IDPR-step8-v0-host/experiments/
v2_call1_v0_service_221593/runs/20260810T141019Z-call2/
```

Its host/structural layer passed: all 26 rows were contract-valid, the top10
replay and total proposition-to-occurrence projection passed audit.  Its semantic
layer failed: 12 of 19 model-emitted `FALSE` labels treated the absence of a
fact as factual impossibility (including one `killing_conduct` FALSE despite a
directly described fatal collision).  Those labels could destructively prune
paths and therefore prevent a Call 2 freeze.

The full 26-case semantic audit covered all 202 proposition labels: 74 `TRUE`,
19 `FALSE`, and 109 `UNKNOWN`.  Every `TRUE` had a directly stated factual
support on review.  Seven `FALSE` labels had an explicit contrary factual
statement (the three abandoned-before-insertion sexual-conduct rows, the
survival row, and the three uninjured-rescue rows).  The remaining 12 `FALSE`
labels were invalid absence-as-impossibility labels.  Some `UNKNOWN` labels are
conservative undercalls, but they are non-destructive `KEEP` signals; this
calibration gate prioritizes false-label precision rather than FALSE recall.

The two prompt variants are retained as calibration evidence; no third prompt
tuning is permitted.  The repair surface is one non-destructive adapter rule:
`FALSE -> KEEP`.  It does not change the DSL, Step 7 replay, runner/schema,
normalization, proposition projection, model/configuration, or cohort.

The approved proposition-wide contrastive revision was then run once on the
same 26-case cohort at:

```text
/data5/jaehoonjeong/IDPR-step8-v0-host/experiments/
v2_call1_v0_service_221593/runs/20260810T142926Z-call2/
```

Its host/structural audit again passed 26/26 rows.  It reduced `FALSE` labels
from 19 to 6 and moved all 12 prior absence-as-impossibility labels to
`UNKNOWN`.  However, the six remaining `FALSE` labels were still only
instance-local negative facts: two abandoned-before-insertion rows, one named
survivor row, and three named uninjured-rescue rows.  None directly says that
no compatible instance exists anywhere in the case.  Under the approved
case-wide existential semantics, all six should be `UNKNOWN`.  The second
artifact has 64 `TRUE`, 6 `FALSE`, and 132 `UNKNOWN` labels; it introduced no
host/structural failure.  Those retained `FALSE` observations are now
non-destructive `KEEP` signals, so neither calibration artifact can prune a
path under the frozen adapter.

Without a further model request, the frozen adapter was deterministically
replayed over both artifacts' 404 proposition observations.  It produced 138
`OPEN` and 266 `KEEP` actions, with `PRUNE = 0`.  This verifies that the
recorded calibration evidence is safe under the frozen non-destructive adapter.

## Prompt-review checklist

The approved prompts are `prompts/v2_call2_grounding.md` and
`prompts/v2_call2_grounding_user.md`.  Their review confirmed that they:

1. require one and only one closed-vocabulary status for every unique GroundFact
   proposition, while preserving and host-projecting every same-ref structural
   occurrence;
2. distinguish proposition-wide factual impossibility (`FALSE`) from absence
   or uncertainty (`UNKNOWN`);
3. prohibit all offense, legal-element, doctrine, completion, participation,
   responsibility, and legal-effect conclusions;
4. treat case-text contents as data, not instructions; and
5. contain no output field for spans, confidence, actors, events, rationale, or
   verdicts.

The approved scope permits host-side `run_v2_call2_*` runner/schema,
artifact/evaluator, projection, pruning, and focused-test implementation.  It
does not yet approve a model run; the exact execution command/spec is reviewed
after implementation and before the 26-case pilot.

## Approved execution plan

This plan authorizes its host-side implementation, but not a model run.  Call 2
consumes **only the frontier
corresponding to the frozen first ten normalized Call 1 seeds**.  It never calls
Call 1, uses a full-15 frontier as Call 2 input, or changes Call 1/Step 7
production semantics.  A narrow deterministic Step 7 frontier replay is
permitted only where the final artifact has not retained that prefix frontier,
as specified in 2.1.

| Order | Proposed work | Review-completion condition |
|---|---|---|
| 2.1 | Call 2 runner and structured-output schema backend | A runner has one explicit Call 1 artifact input, derives only the approved proposition request/response schemas, and host validation remains authoritative if structured output is imperfect. |
| 2.2 | Model, sampling, and vLLM configuration | The exact model snapshot/revision, decoding parameters, vLLM service settings, and prompt hashes are reviewed and pinned before the first request. |
| 2.3 | Artifact format | Every request, raw response, validation result, provenance hash, proposition result, and occurrence projection is reconstructible without model replay. |
| 2.4 | Proposition-to-occurrence projection | Stable first-occurrence projection and its inverse audit mapping preserve every Step 7 frontier occurrence. |
| 2.5 | Non-destructive factual adapter | The adapter emits only `OPEN`/`KEEP`; it preserves `FALSE` and `UNKNOWN` observations without pruning, activation, or a CaseTruths decision. |
| 2.6 | 26-case pilot execution plan | Inputs, service boundary, stop conditions, and pre-registered audit criteria are fixed before a first model request. |
| 2.7 | Result audit and Call 2 freeze decision | A successful artifact is audited against those criteria; only then may the frozen Call 2 surface be recorded. |
| 2.8 | Call 2 selected-predicate assessment | A separate substage review may extend the frozen factual artifact with Step 7-selected LegalElement/predicate assessment; it is not a new Call 3. |

### 2.1 Runner and schema backend

The proposed runner accepts an explicit final Call 1 JSONL artifact and its
manifest, not `case_text` and router seeds as an opportunity to rerun upstream
work.  For every row, its Call 2 seed lineage is exactly:

```text
frozen_top10_seeds = normalized_seeds[:10]
```

The current final artifact records one `closure` per row and does **not** retain
a complete prefix10 occurrence frontier, so it follows path B: before Call 2
request construction, the host replays `compile_closure()` only for
`frozen_top10_seeds`.  This is a deterministic frontier reconstruction, not a
Call 1 rerun or a new Step 7 semantic decision.  It must use the frozen Step 7
compiler revision at `6275987` and record that replay source hash; verify the
loaded registry and case-list hashes against the Call 1 lineage; and record the
exact ten-or-fewer seed list in the new manifest and row.
The original artifact's full15-derived `closure` is calibration evidence only
and is never a Call 2 input or fallback.

`case_text` is read by `sub_question_id` from the explicit inventory JSONL used
by Call 1, not inferred from any artifact field.  The runner verifies that
inventory's SHA-256 against the Call 1 manifest before use, records it in the
Call 2 manifest, and records the exact request payload (including `case_text`)
per row.  It accepts exactly the 26 IDs in `data/eval/kcl_substantive_case_ids.txt`,
preserves that file's order, and emits one completed artifact row per ID,
including deterministic no-op or failure rows.

For a nonempty proposition list, the request schema is the approved
`case_text` plus ordered `ground_facts` wire contract above.  The response JSON
schema should be dynamically generated for that request and express:

```text
object only: { groundings }
groundings length: exactly proposition_count
entry[i].ground_fact_ref: the request's i-th canonical ref
entry[i].truth: TRUE | FALSE | UNKNOWN
no extra properties or entries
```

This backend schema is a generation constraint, not correctness evidence.  The
host independently hard-validates parsed JSON, the exact ordered ref sequence,
cardinality, closed truth vocabulary, and no-extra-fields contract before a
result can reach projection or pruning.  An empty Step 7 frontier is recorded
as a deterministic no-op; it creates neither a schema request nor a model
connection.

### 2.2 Approved configuration

The proposed Call 2 pilot configuration is the final successful Call 1 service
envelope, with a pinned greedy-decoding request configuration.  It remains inside the
designated experiment sandbox; no production host or queue is implied.

| Surface | Fixed pilot value | Basis |
|---|---|---|
| Served model name | `idpr-gemma-4-26b-a4b` | The model name recorded by the final successful Call 1 manifest. |
| Model snapshot | `/data5/jaehoonjeong/.cache/huggingface/hub/models--google--gemma-4-26B-A4B-it/snapshots/01e5b3ee840d3a9e0b0b493c593e85398a30ef75` | The final Call 1 snapshot path. |
| Model revision | `01e5b3ee840d3a9e0b0b493c593e85398a30ef75` | Snapshot directory revision, recorded independently in the Call 1 manifest. |
| System prompt SHA-256 | `54c24d891b32277e6198fc76aa98c3382012172982a1204fd338363195b80528` | Approved proposition-wide semantic-calibration revision of `v2_call2_grounding.md`. |
| User prompt SHA-256 | `4967422f623bac761295eecc6f8dc7a90aa87ab3c23a014afa13c37a022970ce` | Approved `v2_call2_grounding_user.md`. |
| Temperature | `0.0` | Matches the successful Call 1 pilot as part of the pinned greedy-decoding configuration. |
| `top_p` | `1.0` | Explicit no-nucleus restriction. |
| `top_k` | `-1` | Explicit vLLM no-top-k restriction. |
| Request seed | `0` | Explicit OpenAI-compatible vLLM request seed; the runner must send and record it. |
| Maximum completion tokens | `1024` | Matches Call 1; the top10 preflight's largest compact 13-proposition JSON response is 277 snapshot-token tokens, leaving more than 3× headroom. |
| vLLM version | `0.22.0` | Version installed in the same `inv_ass_env` vLLM environment used by the Call 1 launch script. |
| Tensor parallel size | `1` | Final Call 1 service envelope. |
| Maximum model length | `32768` | Final Call 1 service envelope.  The largest top10 request is 2,542 snapshot-token tokens before chat-template overhead; request plus 1,024-token completion remains well below this bound. |
| Maximum concurrent sequences | `1` | Final Call 1 service envelope; server-side concurrency is one.  The host runner, not this setting, preserves case-list artifact order. |
| GPU memory utilization | `0.90` | Final Call 1 service envelope. |
| Reasoning parser | `gemma4` | Final Call 1 service envelope. |
| Structured-output backend | `{"backend":"guidance","disable_any_whitespace":true}` | Final Call 1 service envelope; the dynamically generated strict JSON schema remains a generation constraint only. |

The Call 2 runner must send exactly these sampling values, including `top_p`,
`top_k`, and `seed`; it must not silently inherit server defaults.  It records
the full request-level sampling object, returned model ID, vLLM version, and
all values above in the manifest.  Any unavailable snapshot, revision/hash
mismatch, model-name mismatch, or configuration drift is a pre-request failure,
not a reason to substitute a model or retry with different settings.

The top10 preflight used the frozen 26 Call 1 rows and deterministic replay:
there are 202 proposition requests over 363 preserved occurrences; no case has
an empty frontier; the largest case has 13 unique propositions (and the largest
occurrence frontier has 32).  These are capacity checks only, not Call 2 model
results and not a license to change the frozen Call 1 cap.

### 2.3 Artifact and lineage

The proposed per-case JSONL row has these distinct, non-substitutable layers:

```text
case identity, source-inventory case_text, and Call 1/Step 7 lineage
raw occurrence_frontier (classification, definition_ref, source_path,
                         occurrence_path, ground_fact_ref)
proposition_request (stable-first unique GroundFact definitions sent to model)
raw model response and transport/usage metadata
validated proposition_groundings or a contract/transport failure
proposition_to_occurrences mapping
projected occurrence_groundings (truth + OPEN | KEEP)
```

The manifest pins the runner/schema/prompt source hashes, the frozen Call 1
artifact and manifest hashes, inventory/registry/case-list hashes, the frozen
Step 7 replay source hash, and all reviewed configuration.  It also records
both `normalized_seeds[:10]` as the Call 2 frontier seed rule and the explicit
proposition-projection rule:
`stable_unique(ground_fact_ref, first Step 7 frontier occurrence)`.  A failure
row retains its raw response/error and has no projected grounding or pruning
output.  The artifact is written under ignored `experiments/`; it never alters
the Call 1 artifact.

### 2.4 Projection invariants

Flattening order is exactly the classification order of the deterministically
replayed **top10-only** Step 7 closure
(`mandatory_core`, `offense_probe`, `doctrine_probe`, `completion_probe`,
`participation_probe`), then recorded item order, then recorded frontier order.
The host assigns every flattened frontier record a deterministic structural
occurrence key and retains it even when another record shares its
`ground_fact_ref`.

The proposition list is `stable_unique` over that flattened ref sequence.  Its
mapping is a one-to-many total map from every proposition request ref to all
and only the original occurrences with that ref.  Projection is a total join:
every validated proposition truth appears once at every mapped occurrence, and
no occurrence is added, dropped, re-ordered, or assigned a truth from another
ref.  These invariants are unit-tested without a model.

### 2.5 Non-destructive factual adapter boundary

The adapter consumes only a validated projected occurrence truth and returns:

```text
TRUE    -> OPEN
FALSE   -> KEEP
UNKNOWN -> KEEP
```

`FALSE` remains a retained model observation, but it produces the same `KEEP`
action as `UNKNOWN`.  A shared proposition result is projected to every mapped
occurrence without adding, dropping, reordering, or pruning a path.  The
adapter does not deduplicate paths, remove an offense, activate a candidate,
write `CaseTruths`, evaluate a legal element, or resolve doctrine, completion,
participation, responsibility, or legal effect.  A contract/transport failure
produces no adapter signal.

### 2.6 26-case pilot plan

The first pilot uses exactly the frozen 26-case list and an explicit final Call
1 artifact path.  Its only Call 2 frontier source is the verified deterministic
replay for `normalized_seeds[:10]`; it does not repeat Call 1, consume a
full15 frontier, or repeat any cap calibration.  No model request begins until
2.1–2.5 and the reviewed configuration of 2.2 are merged, their focused tests
pass, and the execution command contains explicit `--prompt-approved` and
`--execution-approved` acknowledgements.  The latter is granted only in the
final command/spec review immediately before the pilot.

The pre-run manifest and the runner must make it possible to audit: all 26
input IDs and their order; the empty-frontier no-op count; model-request count;
row-level contract/transport failures; every unique proposition request; every
original occurrence; and each projected adapter action.  No Call 2
recall/accuracy claim is made without a separately reviewed Call 2 factual gold
annotation.

### Service reuse and cross-session handoff

Call 2 must reuse the already-running experimental Step 8 v0 vLLM service,
Slurm job `221593` on `n05`; it must never submit or start a second vLLM/GPU
service.  At this review point the service state is `READY` and its state file
is:

```text
/data5/jaehoonjeong/IDPR-step8-v0-host/experiments/
v2_call1_v0_service_221593/state.json
```

That service is intentionally bound to `127.0.0.1` on `n05`, inside the
`experiment/step8_v0-*` sandbox.  A login-node client cannot call it directly:
the final approved Call 2 command must be dispatched through that same service
host/queue boundary.  Artifact order remains the responsibility of the Call 2
host runner, not the vLLM server's `max-num-seqs=1` setting.

The currently running v0 queue/host loop dispatches Call 1 only.  Call 2
therefore uses a one-CPU Slurm job step inside the existing allocation, rather
than changing that running loop or submitting another allocation.  The reviewed
submission command is:

```bash
srun --jobid=221593 --ntasks=1 --cpus-per-task=1 /bin/bash \
  /home/jaehoonjeong/data/IDPR/scripts/slurm/run_v2_call2_pilot.sh \
  --execution-approved
```

`run_v2_call2_pilot.sh` verifies the READY state, job ID, host, model, and
loopback port before calling the frozen runner and audit.  It does not start a
model server, rerun Call 1, consume a full15 frontier, or alter Call 1/Step 7
production semantics.  The `srun` job step was preflight-verified to execute
on `n05`; no Call 2 model request was made during that check.

### 2.7 Audit and freeze gate

The audit first checks deterministic invariants across all 26 rows: exact case
coverage, lineage hashes, exact `normalized_seeds[:10]` replay, no full15
frontier input, request/response contract validity for every model-called row,
total proposition-to-occurrence projection, and no adapter signal following a
failed row.  It retains `FALSE` rows as semantic calibration evidence, but all
`FALSE` and `UNKNOWN` rows must project to `KEEP`; only directly supported
`TRUE` may project to `OPEN`.  No Call 2 label is a legal conclusion.

This gate is satisfied by the two recorded structural PASS artifacts, the
reviewed adapter change, focused tests, and deterministic non-destructive
reprojection.  The factual-grounding surface of Call 2 is frozen.  A later
Call 2 selected-predicate-assessment substage may consume that frozen artifact
under its own contract review; it does not change this factual schema or create
a new numbered neural call.  Call 3 is the later final IRAC writer after
symbolic execution, not a LegalElement assessor.
