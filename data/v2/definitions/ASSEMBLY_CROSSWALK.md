# Gate① inventory → production assembly crosswalk

Status: **Phase 5.1 PASS — Phase 6 may begin on instruction** (2026-08-10).

This is the working ledger for the Phase 1 feedback point defined in
[`ASSEMBLY_PLAN.md`](ASSEMBLY_PLAN.md). The canonical sources remain the sealed
Gate① artifacts [`predicate_dictionary_master_v3.md`](../worksheets/predicate_dictionary_master_v3.md)
and, for article 258, [`predicate_dictionary_ext_art258_v0.md`](../worksheets/predicate_dictionary_ext_art258_v0.md).
P1-F01 below is a separately recorded canonical erratum; it does not modify
Master v3 in place. This ledger assigns an owner file and assembly phase; it
does not redefine a canonical predicate ID or meaning.

## Reading rules

- **Source / consumers**: the cited Master § is the authoritative row containing
  the source and reuse/consumer statements. This ledger deliberately does not
  paraphrase or overwrite those canonical meanings.
- **Owner**: `ground_fact → ground_facts.yaml`, `legal_element → legal_elements.yaml`,
  `bundle → element_bundles.yaml`, `primitive → primitives.yaml`,
  `relation → relations.yaml`, `doctrine → doctrines.yaml`, `qualifier →
  qualifiers.yaml`, `offense → offenses.yaml`, and `derived offense →
  derived_offenses.yaml`; completion states belong in the target offense's
  `completion_policies.yaml` entry, not in a StateDef file.
- **Status**: `loaded` means a schema-valid production entry exists; `queued`
  means the canonical item has an owner and later assembly phase; `HOLD` means
  the Master itself requires a later structure/code decision; `normalise` means
  a Master shorthand must be traced to its exact pre-existing canonical spelling
  before it can be written.
- The three Gate①-deleted names — `doctrine.quasi_robbery`,
  `doctrine.complete_suppression_becomes_robbery`, and
  `legal_element.property_of_another` — are exclusions, never production rows.

## Production snapshot

| Owner YAML | Loaded | Canonical scope currently present |
|---|---:|---|
| `ground_facts.yaml` | 29 | Phase 2–3 facts and P3-E01 `injury_conduct` |
| `legal_elements.yaml` | 156 | Phase 2–4 leaves, including B-6, the frozen 301/337/338 intent leaves, and result-attribution |
| `element_bundles.yaml` | 5 | Negligence, omission, the 335 purpose component, and two structural non-intent branch guards |
| `primitives.yaml` | 8 | Phase 4 COMPOSE components, including the Master-canonical result-attribution wrapper |
| `relations.yaml` | 3 | Shared relations plus 347's deception→disposition nexus |
| `offenses.yaml` | 37 | Phase 3 base offenses plus B-6 extortion |
| `qualifiers.yaml` | 7 | 258/258의2 and property/356 qualification patches |
| `exported_components.yaml` | 4 | Existing injury/death result and conduct PROJECT endpoints for result-aggravated COMPOSE |
| `derived_offenses.yaml` | 22 | 258/258의2, B-6 fraud, property variants, intentional branches, and all Master-listed result-aggravated consumers |
| `completion_policies.yaml` | 1 | 319① entry; 319② intentionally omits an attempted state |
| `doctrines.yaml` | 12 | Existing Phase 2 doctrines; B-9 remains HOLD |
| `participation_policies.yaml` | 0 | Phase 5 confirms that no existing policy can lawfully finalise C-33a/C-34; remains unauthored |

The current **284** production objects are unchanged by Phase 5. They have
passed schema loading and all eight type-check axes. Phase 5 adds code-path
evidence only; it does not use a synthetic probe as production assembly.

## Canonical owner ledger

| Master § | Canonical inventory group (verbatim IDs or Master label) | Owner YAML | Status / phase | Source and consumers |
|---|---|---|---|---|
| 2.1 | `legal_element.intent`, `legal_element.commencement_of_execution`, `legal_element.preparatory_conduct`, `legal_element.conspiracy_agreement`, `legal_element.purpose_to_commit_target_offense`, `legal_element.natural_person_victim_status` | `legal_elements.yaml` | **loaded / 2** | Master §2.1 rows |
| 2.1 | `bundle.negligence_bundle`, `bundle.omission_bundle` | `element_bundles.yaml` | **loaded / 2** | Master §2.1 rows |
| 2.1 | `bundle.mistake_bundle` | `element_bundles.yaml` | HOLD P2-F01 / Phase 3 consumer proof | Master §2.1 and batch02 v2 |
| 2.1 | `relation.causal_nexus`, `relation.occasion_identity` | `relations.yaml` | **loaded / 2**; consumed in 4 | Master §2.1 rows |
| 2.1 | `primitive.aggravated_result_attribution` | `primitives.yaml` | **loaded / 4**; P4-F02 provenance trace resolved | Master §2.1 row; fixture origin was intentionally canonicalized by the batch and Master lineage |
| 2.2 | `ground_fact.actor_age_under_14_at_act_time`, `doctrine.juvenile_defeat`; `legal_element.deaf_mute_status`, `doctrine.deaf_mute_mandatory_reduction`; `ground_fact.coerced_act_performed`, `legal_element.irresistible_coercion`, `legal_element.self_induced_coercion`, `doctrine.coerced_act_defeat`; `legal_element.awareness_of_illegality_lacking`, `legal_element.justifiable_ground_for_mistake`, `doctrine.mistake_of_law_defeat` | facts/elements/doctrines | **loaded / 0** | Master §2.2 rows; source refs use the corresponding general-part commentary chunks |
| P1 erratum | `ground_fact.mental_disorder_at_act_time` | `ground_facts.yaml` | **loaded / 2**; existing Article 10 1-pass ID | P1-F01 decision; Master v3 remains unchanged |
| 2.2 | `legal_element.discrimination_capacity`, `legal_element.control_capacity`, `legal_element.self_induced_disorder`, `doctrine.insanity_defeat` | elements/doctrines | **loaded / 2**; ALIC uses `NOT(self_induced_disorder)` | Master §2.2 and batch01 v1 final rewrite |
| 2.2 | `doctrine.diminished_capacity_modify` | `doctrines.yaml` | HOLD / 2; batch01 v1 leaves the capacity-diminution condition unnamed | Master §2.2 and batch01 v1 |
| 2.3 | `legal_element.duty_of_care`, `legal_element.foreseeability`, `legal_element.avoidability`, `legal_element.breach_of_duty`, `legal_element.mistake_within_same_construct`, `legal_element.foreseeability_of_aggravated_result`, `legal_element.duty_to_act`, `legal_element.equivalence_to_commission`, `legal_element.concurrent_independent_acts`, `legal_element.same_object_of_result`, `legal_element.causal_origin_unascertained` | `legal_elements.yaml` | **loaded / 2** | Master §2.3 rows |
| 2.3 | `ground_fact.perceived_fact`, `ground_fact.actual_fact`, `ground_fact.means_or_object_defect`, `ground_fact.possibility_to_act`, `ground_fact.failure_to_act` | `ground_facts.yaml` | **loaded / 2** | Master §2.3 rows |
| 2.4 | All §2.4 `legal_element.*` entries (`act_pursuant_to_law` through `consent_based_act_not_against_social_norms`) | `legal_elements.yaml` | **loaded / 2** | Master §2.4 rows |
| 2.4 | `doctrine.justifiable_act_defeat`, `doctrine.self_defense`, `doctrine.necessity_defeat`, `doctrine.conflict_of_duties_defeat`, `doctrine.self_help_defeat`, `doctrine.victim_consent_defeat`, `doctrine.presumed_consent_defeat` | `doctrines.yaml` | **loaded / 2** | Master §2.4 rows |
| 2.4 | `doctrine.excessive_defense`, `doctrine.excessive_necessity`, `doctrine.excessive_self_help` | `doctrines.yaml` | HOLD P2-F03 / B-9 | Master §2.4 and batch03 v2 |
| 2.5 | `legal_element.voluntary_cessation_or_prevention`, `legal_element.dangerousness`, `legal_element.voluntary_surrender_before_execution` | `legal_elements.yaml` | **loaded / 2** | Master §2.5 rows |
| 2.5 | `PREPARATION_OR_CONSPIRACY` state label | `completion_policies.yaml` | queued / 4; not a standalone Definition Layer ID | Master §2.5 row; P1-F02 |
| 2.6 | `legal_element.joint_execution_intent`, `legal_element.joint_execution_conduct`, `legal_element.instigator_intent`, `legal_element.aiding_intent`, `legal_element.supervisory_relationship` | `legal_elements.yaml` | **loaded / 2**; no participation policy is authored | Master §2.6 rows; Phase 5 keeps C-33a/C-34 HOLDs after code-path verification |
| 2.7 | `ground_fact.prior_sentence_of_imprisonment_or_greater`, `ground_fact.prior_sentence_execution_completed_or_exempted`, `legal_element.prior_sentence_still_effective`, `legal_element.subsequent_offense_within_recidivism_period` | facts/elements | **loaded / 2** | Master §2.7 rows |
| 2.7 | `doctrine.recidivism_modify` | `doctrines.yaml` | HOLD P2-F04 / modifier classification | Master §2.7 and batch06 v1 |
| 2.8 | Loaded property facts/elements for 329/333/355(1)/356/360/366 and the shared `injury_result`; `object_ownership_other` is the sole art360 ownership reference | facts/elements | **loaded / 3**; A-3/A-4 reuse preserved | Master §2.8 rows; `injury_result` has one owner despite its §2.11 reuse row |
| 2.8 | `legal_element.disposition_authority` and the 355(2) breach-of-trust conduct/result dependency | `legal_elements.yaml` / offenses/derived offenses | **loaded / 3–4**; P3-E02 and B-6 resolved without a substitute predicate | Master §2.8 and §4 B-6 |
| 2.9 | All listed public-official and judicial facts/elements other than C-151; compact groups resolve as `ground_fact.third_party_benefit_causation`, `ground_fact.third_party_benefit_demand`, `ground_fact.third_party_benefit_promise`; `ground_fact.bribe_offer_expression_made`, `ground_fact.bribe_offer_expression_arrived`; and `ground_fact.examination_ended`, `ground_fact.post_oath_completed` | facts/elements | **loaded / 3**; exact-spelling normalisation complete | Master §2.9 rows and batch07 v2/v3 |
| 2.9 | `legal_element.offender_status_of_object` | `legal_elements.yaml` | HOLD C-151 / 5; no cross-instance symbolic dependency exists | Master §2.9 and §4 C-151 |
| 2.10 | All listed arson/document `legal_element.*` entries | `legal_elements.yaml` | **loaded / 3** | Master §2.10 rows |
| 2.11 | `ground_fact.killing_conduct`, `ground_fact.death_of_victim` | `ground_facts.yaml` | **loaded / 3** | Master §2.11 rows |
| P3-E01 | `ground_fact.injury_conduct` | `ground_facts.yaml` | **loaded / 3**; replaces unfit `violence_used` only through the recorded erratum | P3-E01; Master v3 remains sealed |
| 2.11 | All listed life/body `legal_element.*` entries, including `legal_element.serious_injury_result` | `legal_elements.yaml` | **loaded / 3** | Master §2.11 and art258 extension |
| 2.11 | `offense.aggravated_injury[258(1)-(2)]`, `offense.aggravated_ancestral_injury[258(3)]`, and 258의2 four base branches | `qualifiers.yaml` / `derived_offenses.yaml` | **loaded / 4**; P4-F04 records the direct-OffenseDef QUALIFY adaptation | Master §2.11 and art258 extension |
| 2.12 | All listed sexual-freedom facts/elements | facts/elements | **loaded / 3** | Master §2.12 rows |
| 2.13 | All listed dwelling/right-exercise `legal_element.*` entries | `legal_elements.yaml` / `completion_policies.yaml` | 319① **loaded / 4**; B-3 closed and 319② omits an attempted state (B-4 closed) | Master §2.13 rows |
| 2.14 | No new predicate; `offense.robbery[333/334/335]`, `offense.rape[297]`, and `relation.occasion_identity` are references | offenses/relations/completion | queued / 3–5; C-339 HOLD | Master §2.14 and §4 C-339 |

## Phase 1 feedback record

| Ref | Recorded issue | Evidence | Assembly rule until feedback | Feedback needed at Phase 1 |
|---|---|---|---|---|
| **P1-F01** | Article 10 canonical erratum | User decision: `ground_fact.mental_disorder_at_act_time` is an existing Article 10 1-pass ID, not a new predicate. Master v3 is the sealed Gate① approval and remains unchanged. | Record the erratum in this crosswalk and load the existing ID in `ground_facts.yaml`; Article 10 ALIC follows batch01 v1's `NOT(self_induced_disorder)` gating, without restoring an exception doctrine. | **Resolved by user decision.** |
| **P1-F02** | `PREPARATION_OR_CONSPIRACY` is a completion-state label, not a Definition Layer object kind | Master §2.5 explicitly labels it `CompletionPolicy state`; the schema has no StateDef. | Write it only inside each affected offense's `completion_policy.states`; never create a YAML registry object for it. | **Resolved by schema contract; no feedback decision needed.** |
| **P1-F03** | Master uses compact suffix notation in §2.9 | Batch07 v1/v2/v3 resolves the full frozen names as `ground_fact.third_party_benefit_causation`, `ground_fact.third_party_benefit_demand`, `ground_fact.third_party_benefit_promise`; `ground_fact.bribe_offer_expression_made`, `ground_fact.bribe_offer_expression_arrived`; and `ground_fact.examination_ended`, `ground_fact.post_oath_completed`. | Use exactly these existing spellings; do not derive a different suffix expansion. | **Resolved by source trace; no feedback decision needed.** |
| **P1-F04** | Article 258 uses explanatory bracket labels rather than schema-valid authored IDs | `offense.aggravated_injury[258(1)-(2)]` and `offense.aggravated_ancestral_injury[258(3)]` describe two future derived offenses, while Definition Layer IDs must match the schema identifier pattern. | Preserve the two frozen legal meanings and QUALIFY paths; choose only a schema-valid *definition identifier* during Phase 4, without creating a new predicate. | **Recorded for Phase 4; no Phase 1 decision needed.** |
| **P1-F05** | Gate① deletion guard | Master §6 removes quasi-robbery, complete-suppression, and `property_of_another`; A-3 fixes the 360 reuse target as `object_ownership_other`. | Add none of the deleted names. Route art360 only through `legal_element.object_ownership_other`. | **Resolved by Gate① canonical record; no feedback decision needed.** |

## Phase 1 completion audit

| Audit item | Result |
|---|---|
| Canonical inventory coverage | Master §§2.1–2.14 are all assigned to an owner YAML, a later assembly phase, or a documented HOLD/exclusion in the canonical owner ledger above. |
| Source and consumer preservation | Every ledger group points to the Master § row that carries its source and reuse/consumer statement; the ledger never rephrases canonical meaning or invents a second provenance source. |
| Current production reconciliation | At Phase 1 close, all 16 production entries appeared in the §2.2 loaded rows or the P1-F01 erratum row. No entry was outside Gate① scope plus that recorded erratum. |
| A-group reuse | Closed results are preserved: 331/258의2 remain distinct, 335 uses `occasion_identity`, 360 uses `object_ownership_other`, and 355/356/360 share `embezzlement_manifestation`. |
| B/C routing | B-5, B-6, B-8, B-9 and the remaining B items retain their affected-statute phase; C-33/C-34 participation remains HOLD until Phase 5, C-151/C-263 remain Phase 5, and C-339 remains art339-only. |
| Exclusion guard | The three Gate①-deleted names are prohibited from production YAML. Articles 36, 328, and 344 remain outside evaluation population; Article 258 remains a supporting dependency, so coverage remains 80. |
| Feedback residue | **None for Phase 1.** P1-F01 is resolved by user decision; P1-F02, P1-F03, and P1-F05 are resolved; P1-F04 remains a Phase 4 naming record. |

## Phase 2 Article 10 expression boundary

`doctrine.insanity_defeat` is assembled exactly with batch01 v1's three
conjuncts: `NOT(discrimination_capacity)`, `NOT(control_capacity)`, and
`NOT(self_induced_disorder)`. `doctrine.diminished_capacity_modify` is not yet
written: batch01 v1 requires a condition expressing diminished capacity but
does not freeze an ID or expression for that condition. `mental_disorder_at_act_time`
is evidence of mental disorder, not a substitute inferred as diminished capacity.

## Phase 2 completion audit

| Audit item | Result |
|---|---|
| Production delta | 16 → **82** schema-valid objects: 10 ground facts, 56 legal elements, 2 element bundles, 2 relations, and 12 doctrines. No `primitive`, participation policy, offense, derived offense, qualifier, export, or completion policy was prematurely authored. |
| Confirmed General Part assembly | §§13–15, 18–28, 30–32, 34, and the predicate portion of §35 are loaded wherever their Gate① item has a complete existing expression. `negligence_bundle` and `omission_bundle` have their four frozen conjuncts exactly. |
| Doctrine expressions | The completed doctrines use only frozen leaf IDs and schema-supported `ALL`/`ANY`/`NOT`; all 12 pass the stage/effect axis. Article 10 `insanity_defeat` retains the batch01 v1 ALIC gate. |
| Participation boundary | The five participation leaf elements are loaded, but `participation_policies.yaml` remains empty. No mode, constraint, attribution, or indirect-perpetration outcome has been decided before C-33/C-34 code verification. |
| Gate and coverage guard | Master v3 remains unchanged; P1-F01 remains a crosswalk-only erratum. The three Gate① exclusions are absent. Evaluation coverage remains **80** and article 258 remains only a supporting dependency. |
| Verification | `load_definitions(data/v2/definitions)` succeeds; all eight type-check axes report **0 findings**; `tests/test_v2_*.py` reports **228 passed**; `git diff --check` passes. |

## Phase 2 feedback record

| Ref | Boundary / evidence | Current assembly treatment | Feedback requested |
|---|---|---|---|
| **P2-F01** | `bundle.mistake_bundle` requires comparing perceived and actual facts to affect `intent`; batch02 v2 expressly requires a real `OffenseDef.element_modules` + `placement → mental` consumer proof, not a bare schema-shaped bundle. | Not authored. Its three frozen leaf IDs are loaded; test moves with the first affected base offense in Phase 3. | Confirm this is the correct deferred proof boundary; no new kind or predicate is proposed. |
| **P2-F02** | Master §2.1 identifies this primitive's source as the external fixture. That fixture already defines `primitive.aggravated_result_attribution → legal_element.aggravated_result_attribution`, and the type-check design exercises that sole primitive-derived leaf. Production absence is not evidence that the existing fixture ID is unavailable. | No production entry is authored yet. Before Phase 4, trace the fixture leaf's canonical meaning and source. If it is reusable as the same existing canonical supporting dependency, load that leaf and the unchanged `PrimitiveDef` wrapper; create no predicate or schema. Only if the fixture ID proves illustrative-only and non-reusable does the first affected derived-offense assembly become a compatibility HOLD. | **Approved source-trace order; no schema-gap escalation at this point.** |
| **P2-F03** | B-9: batch03 v2 requires all three excessive doctrines to follow one concrete Article 21 downstream structure, but no single `DoctrineDef.stage`/effect shape is frozen. | `excessive_defense`, `excessive_necessity`, and `excessive_self_help` remain absent. The seven ordinary unlawfulness DEFEAT doctrines are loaded. | Keep the three-way decision for the affected-statute/B-group point; no provisional culpability or punishability stage was chosen. |
| **P2-F04** | batch06 v1 reserves `recidivism_modify.effect.modifier_ref` for the actual modifier classification and warns against treating a placeholder symbolic id as frozen. | Its four frozen antecedents are loaded; the doctrine remains absent. | Confirm it remains a narrow authoring HOLD until the modifier classification is fixed, rather than inventing a modifier reference. |
| **P2-F05** | batch01 v1 has no frozen condition for "capacity diminished". Mental disorder, capacity present/absent, and capacity diminished are distinct propositions. | `diminished_capacity_modify` remains absent; no inference from `mental_disorder_at_act_time` is used. | Retain the approved narrow Article 10 HOLD pending a source/history finding of an existing frozen predicate or a later concrete new-atomic-predicate decision. |
| **P2-F06** | C-33/C-34 require Phase 5 code-path verification. | `participation_policies.yaml: []`; only its independently reusable leaf elements are loaded. | Confirm the HOLD remains intact; final participation authoring stays prohibited before Phase 5. |

**Stop point:** Phase 2 is complete. Do not start Phase 3 base-offense YAML until
the Phase 2 feedback record is reviewed. The record deliberately keeps the
Article 10 diminished-capacity boundary and C-33/C-34 boundary intact.

## Phase 3 completion record

Phase 2 feedback is accepted: P2-F01 and P2-F03–P2-F06 retain their recorded
HOLDs, and P2-F02 is a fixture supporting-dependency source trace before Phase
4 rather than a schema-gap escalation.

| Production delta from Phase 2 | Result |
|---|---|
| `ground_facts.yaml` | 29 loaded: Phase 2 facts plus property, bribery, judicial, homicide, rape, and P3-E01 injury-conduct facts. |
| `legal_elements.yaml` | 152 loaded: Phase 2 elements plus the available §2.8–§2.13 frozen leaves and P3-E02's two breach-of-trust erratum leaves. B-6 and C-151 remain absent exactly as recorded below. |
| `offenses.yaml` | 36 loaded base offenses across property, public-official/judicial, arson/document, life/body, sexual-freedom, dwelling, and right-exercise families. |
| `qualifiers.yaml` / `derived_offenses.yaml` | The narrow 258 supporting chain is exceptionally loaded now: one serious-injury qualifier and its two 258 branches. No other Phase 4 object is pulled forward. |
| All other kinds | Export, completion, and participation policies remain unauthored. |
| Type verification | **236** objects total; eight-axis type check **0 findings**; `tests/test_v2_*.py` **228 passed**; `git diff --check` passes. |

### Phase 3 loaded base-offense families

| Family | Loaded `OffenseDef` ids |
|---|---|
| Property | `theft`, `robbery`, `embezzlement`, `breach_of_trust`, `property_damage`, `lost_property_embezzlement` |
| Public official / judicial | `dereliction_of_duty`, `official_secret_disclosure`, `bribery_taking`, `prospective_bribery_taking`, `third_party_bribery`, `bribe_giving`, `bribe_delivery_receipt`, `obstruction_of_official_duty`, `coercion_of_official_duty_or_resignation`, `deceptive_obstruction_of_official_duty`, `perjury` |
| Arson / document | `arson_of_occupied_structure`, `public_document_forgery`, `false_public_document_creation`, `private_document_forgery`, `use_of_forged_private_document`, `seal_forgery_or_misuse` |
| Life / body | `homicide`, `ancestral_homicide`, `injury`, `ancestral_injury`, `negligent_homicide`, `occupational_or_gross_negligence_injury_or_homicide` |

### Phase 3 canonical errata

Master v3 remains sealed. The following are Phase 3 source-traced corrections
to its inventory; they do not amend Master v3 in place.

| Ref | Source trace and decision | Production consequence |
|---|---|---|
| **P3-E01 (B-8)** | The original art257 record states that injury can be caused by violence **or another method**; `violence_used` is therefore not an adequate canonical name. The concrete Phase 3 decision is `ground_fact.injury_conduct`, meaning “상해의 수단이 되는 유형력 또는 그 밖의 방법을 사용.” | `offense.injury` and `offense.ancestral_injury` are loaded. `derived_offense.aggravated_injury = QUALIFY(offense.injury, qualifier.serious_injury_result)` and `derived_offense.aggravated_ancestral_injury = QUALIFY(offense.ancestral_injury, qualifier.serious_injury_result)`, completing the 258 supporting chain for 258-2. |
| **P3-E02 (355②)** | No existing frozen breach-of-trust conduct/result leaf was found. The source states the two missing minimum propositions: an act of breach yielding self/third-party property benefit, and loss or a concrete, real risk of loss to the principal. | `legal_element.breach_of_trust_conduct` and `legal_element.property_loss_or_concrete_risk` are recorded as the minimal erratum additions; `offense.breach_of_trust` is loaded. `embezzlement_manifestation` is not reused. |
| Sexual freedom | `rape`, `forcible_indecency`, `quasi_rape`, `quasi_forcible_indecency` |
| Dwelling / right exercise | `dwelling_intrusion`, `refusal_to_leave`, `obstruction_of_right_exercise` |

### Phase 3 feedback record

| Ref | Assembly result and evidence | Current treatment | Feedback requested |
|---|---|---|---|
| **P3-F01** | **B-6, arts. 347/350:** `disposition_authority` is frozen as a `legal_element`, but the required disposer/property authority relationship cannot be represented by `OffenseDef.elements`; a `RelationDef` cannot be placed in a base-offense slot. | `fraud` and `extortion` remain unauthored. The result is only a base-OffenseDef failure, not a B-6 final failure. | **Approved:** retry with existing Phase 4 composition patterns; promote to C only after that concrete failure. |
| **P3-F02** | **B-8, art. 257:** resolved as P3-E01. | `injury_conduct` replaces the inadequate `violence_used` name only through this erratum; 257 and the 258 supporting chain are assembled. | **Resolved by user decision.** |
| **P3-F03** | 355(2) existing frozen ID search failed; source trace established the two missing minimal objective propositions. | Resolved as P3-E02; `breach_of_trust` is assembled without reusing `embezzlement_manifestation`. | **Resolved by user decision.** |
| **P3-F04** | **C-151, art. 151:** `offender_status_of_object` remains a cross-actor dependency. | No harboring/escape `OffenseDef` is authored; its ordinary leaf predicates are loaded. | **Approved:** keep the C-151 HOLD until Phase 5 code-path verification. |
| **P3-F05** | Art. 319 entry/refusal are distinct base offenses; refusal has no `omission_bundle`, as it is a true omission offense. Their attempt/completion consequences belong to art. 322 Phase 4. | Both bases are loaded, without premature completion policies. | **Approved:** defer art. 322 completion assembly to Phase 4. |
| **P3-F06** | P2-F01 `mistake_bundle` still lacks the required real `element_modules` consumer proof: none of the completed bases has a frozen consumer placement that lawfully turns perceived/actual facts into intent. | Remains absent; no bundle or new top-level kind is created. | **Approved:** keep B-5 pending its first concrete consumer; promote only on an actual failed attachment. |

**Stop point:** Phase 3 feedback is accepted and its required corrections are
complete. Phase 4 may begin only on instruction; its first B-6 action is the
existing-COMPOSE retry for arts. 347/350.

## Phase 4 assembly-pass record

The pass authors only a relation, primitive, bundle, qualifier, derived-offense,
or completion-policy structure that the frozen inventory and current contract
can support. A schema-valid definition identifier names the authoring structure;
it is not a new canonical predicate. Master v3 and the art258 extension remain
sealed sources.

| Production delta from Phase 3 | Result |
|---|---|
| B-6, arts. 347/350 | `disposition_authority` is loaded as its frozen `legal_element`. `derived_offense.fraud` COMPOSEs `deception`, `property_disposition`, `disposition_authority`, and the existing appropriation intent, with `relation.deception_error_disposition_causal_nexus`; `offense.extortion` uses the same authority element directly because no separate extortion relation was frozen. |
| 258의2 | Seven qualifiers/derived offenses now preserve all four direct base branches. The two serious branches use a combined Qualifier patch because `QUALIFY` accepts an `OffenseDef`, not a `DerivedOffenseDef`, as its base. |
| Result-aggravated supporting dependency | The Master-canonical `legal_element.aggravated_result_attribution` and its unchanged PrimitiveDef wrapper are loaded. `PROJECT` exports only pre-existing result/conduct leaves; no result predicate is created. The 164(치사/치상), 259, 301 치상, 337 치상, and 338 치사 COMPOSE branches compile with the required causal relation; 301/337/338 also retain their distinct occasion relation. |
| 301/337/338 intentional variants | The frozen `injury_intent` and `homicide_intent` are loaded. Three separate intentional `DerivedOffenseDef` COMPOSE paths compile with distinct `causal_nexus` and `occasion_identity` obligations. |
| Property variants | 330, 331, 334, 335, and the two 356 variants are assembled with frozen leaves; 335's existing `occasion_identity` binding and its three-way purpose bundle compile. |
| Completion | Article 319① has a completed/attempted policy with the conduct slot suspended only in its attempted state. Article 319② deliberately omits an attempted state: it does not derive an attempt state merely to mark it unpunishable. |
| Verification | **284** objects total; eight-axis type check **0 findings**; all **59** authored offense/derived-offense entries compile; `tests/test_v2_*.py` **228 passed**; `git diff --check` passes; Master v3 has no diff. |

### Phase 4 feedback record

| Ref | Assembly result and evidence | Current treatment | Feedback requested |
|---|---|---|---|
| **P4-F01 (B-6)** | Existing COMPOSE is feasible. The 347 relation binds the event-sorted `deception` and `property_disposition` primitive occurrences; `disposition_authority` remains the frozen evaluative legal element. The previously considered relation candidate was `disposer_identity_match`, not either property disposition or authority. 350 has no separately frozen relation. | **Accepted and resolved**: `derived_offense.fraud` and `offense.extortion` compile without an invented extortion relation or C escalation. | **Closed.** |
| **P4-F02 (P2-F02 provenance trace)** | This is a **Master v3 ↔ fixture provenance source-consistency check**, not an architecture HOLD. The fixture supplies the original leaf/wrapper shape, but batch08/09/10/12 repeatedly consume it and both Master v2 and sealed Master v3 explicitly freeze `primitive.aggravated_result_attribution` with consumers 164, 259, 301, 337, and 338. That is intentional canonicalization of the supporting dependency. | The production leaf retains the frozen combined meaning and the unchanged `PrimitiveDef` wrapper. The fixture's example-only citation and its injury-only `grounded_by` are not copied. `foreseeability_of_aggravated_result` is not substituted because it covers only the foreseeability conjunct, not the primitive's combined attribution meaning. | **Resolved by source trace; no erratum.** |
| **P4-F03 (B-1)** | Current COMPOSE supports separate intentional and result-aggravated forms. The intentional 301/337/338 definitions remain separate. Once P4-F02 resolved, the result forms were assembled with the same canonical primitive; `PROJECT` separates the pre-existing conduct and result exports where `occasion_identity` needs a conduct endpoint. | The result branch carries `NOT(injury_intent)` or `NOT(homicide_intent)` through a structural bundle, preserving the documented exact-one boundary without a new predicate. | **Accepted and resolved.** |
| **P4-F04 (258의2)** | Schema restricts `QUALIFY.base` to an `OffenseDef`; the two 258 supporting bases are `DerivedOffenseDef`s. A nested QUALIFY would fail the reference contract. | Four branches remain direct qualification of the two 257 bases; serious branches apply the combined serious-result + special-method qualifier. Thus each `DerivedOffenseDef` uses `QUALIFY(base OffenseDef, QualifierDef)`, rather than treating a qualifier as an offense-producing object. | **Accepted and resolved.** |
| **P4-F05 (B-3/B-4, art319)** | The frozen `dwelling_or_managed_premises_object` remains the sole 319 object predicate; no seasonal-unused-house subtype is inferred. 319① attempt compiles. Under the completion contract, `punishable: false` would mean an attempted state exists, whereas the B-4 conclusion is that 319② has no derivable attempted state. | 319② attempted state is **omitted**. No `punishable: false` entry is authored. | **B-3 and B-4 closed.** |
| **P4-F06 (B-5)** | No completed offense has supplied the required lawful perceived/actual-fact → intent `element_modules` attachment. | `bundle.mistake_bundle` remains absent; no C escalation occurs without a concrete consumer failure. | **Accepted HOLD.** |
| **P4-F07 (B-9 and prior narrow HOLDs)** | The excessive doctrines still lack the frozen stage/effect shape; `diminished_capacity_modify` and `recidivism_modify` retain their earlier expression/modifier holds. | No provisional doctrine, modifier, or capacity predicate is authored. | **Accepted HOLD.** |

**Phase 4 stop point (cleared by the subsequent Phase 5 instruction):** Phase 4
feedback was accepted with all approved corrections complete. Its C-33/C-34
participation prohibition remains in force until the Phase 5 results below are
reviewed.

## Phase 5 completion record — C-group code-path verification

Phase 5 deliberately performs no production YAML assembly. Its synthetic
registries and case instances are probe inputs only: they establish what the
current contract/runtime can and cannot represent without turning a probe
predicate, policy, or mode into production data. `participation_policies.yaml`
therefore remains empty.

| Probe | Executed evidence | Result |
|---|---|---|
| C-33a, art323 / constitutive-status co-principal | With `subject` made attributable for `offense.bribery_taking`, the target non-official's `official_or_arbitrator_status=FALSE` was merged with the co-actor official's `TRUE` to **TRUE**. | `apply_attribution()` is a leaf-wise `fold_any`; using it for status is the confirmed semantic-contamination failure, not an Article 33 solution. |
| C-33b, art250 proviso | A realized `offense.homicide` principal and a distinct `offense.ancestral_homicide` instigator target were passed to `resolve_derivative_liability()`. The target `offense_ref` was preserved and derivative liability was reached. | The 6C core permits a cross-offense derivative target. Repository search found no production caller/orchestrator that constructs this route, so this is a validated core capability but not an end-to-end Article 33 closure. |
| C-34, indirect perpetration | A synthetic `indirect_principal` participation mode is schema-rejected. The existing derivative path is positively gated by `principal_realization_truth`; it cannot read the required actor-specific non-punishment/other-offense outcomes. | No existing mode or expression can represent the required stage-sensitive cross-actor dependency. `supervisory_relationship` remains an unused frozen leaf. |
| C-151, art151 offender status | `CaseTruths.predicate_view()` exposes only one complete `OffenseInstanceKey` (`case, actor, offense, occurrence`), and Definition Layer expressions carry only predicate refs, not another actor's `LiabilityEvaluation` or `OffenseRealization`. | `offender_status_of_object` cannot be written as a truthful production leaf that derives from the other actor's offense result. |
| C-263, art263 deemed co-principal | The policy schema offers only `direct`, `attribution`, and positive `derivative` bases. `apply_attribution()` requires participant sources and merges actual attributable leaves, whereas Article 263 requires no mutual intent and a statutory deemed effect. | No existing participation path represents the statutory deeming without falsely asserting actual co-principal attribution. |
| C-339 D-1/D-2 | Completion `when` expressions have no component-local-key selector (D-1). The existing `robbery_rape` probe with two conduct contributors and an attempted conduct suspension produces `completion_unsupported_slot_suspension` (D-2). | Both active holds are confirmed. Do not author art339 or its CompletionPolicy before a 339-specific design decision. |

### Phase 5 feedback record

| Ref | Current treatment | Feedback requested |
|---|---|---|
| **P5-F01 (C-33a)** | Confirmed unsupported by ATTRIBUTE: actor-specific status must not be propagated. No participation policy or offense constraint is authored. | **Accepted:** Phase 5.1 minimum, non-status-propagating Article 33 mechanism required. |
| **P5-F02 (C-33b)** | Core cross-offense derivative evaluation is proven, but no orchestrator invokes it. | **Accepted:** move to the Step 7 caller-orchestration requirement; no architecture HOLD remains. |
| **P5-F03 (C-34)** | Existing policy/runtime cannot express indirect perpetration's stage-sensitive cross-actor condition. No new mode or predicate is invented. | **Accepted:** Phase 5.1 indirect-principal-specific architecture change required. |
| **P5-F04 (C-151/C-263)** | Neither cross-actor offender status nor statutory deemed co-principal effect has a current symbolic path. Arts. 151 and 263 remain unauthored. | **Accepted:** Phase 5.1 cross-instance dependency and statutory-deeming changes required. |
| **P5-F05 (C-339)** | D-1/D-2 are confirmed only for art339; no art339 YAML was written. | **Accepted:** Phase 5.1 art339-specific completion change required. |

| Verification | Result |
|---|---|
| Targeted probes | C-33a output `TRUE` after status merge; C-33b preserves `offense.ancestral_homicide` and reaches liability; C-34 synthetic mode has one schema error; 339 D-2 is rejected by the existing completion checker. |
| Targeted regression | `test_suspending_a_slot_several_components_contribute_to_is_refused` plus runtime-participation tests: **21 passed**. |
| Production delta | **None** — still 284 objects, with C-33/C-34 participation and every C-affected offense deliberately unauthored. |

### Phase 5 disposition

| Ref | Accepted disposition |
|---|---|
| P5-F01 / C-33a | **Architecture change required.** |
| P5-F02 / C-33b | **6C core sufficient.** Move to a Step 7 caller-orchestration requirement; no architecture HOLD remains. |
| P5-F03 / C-34 | **Architecture change required.** |
| P5-F04 / C-151 | **Architecture change required.** |
| P5-F04 / C-263 | **Architecture change required.** |
| P5-F05 / C-339 | **339-specific completion change required.** |

## Phase 5.1 completion record — proven minimum changes

| Item | Implementation and production result | Focused regression |
|---|---|---|
| C-33a | Added offence-local `constitutive_status_refs`; art323 uses `own_property_object`. The new co-principal path substitutes only that Elements leaf through `CoPrincipalConstitutiveStatusObligation`, without status propagation in `CaseTruths`. | The target non-owner remains `FALSE`; the co-principal status makes the Elements stage pass. |
| C-151 | Added the frozen `offender_status_of_object` and `offense.harboring_or_escape`. The Article 151 path supplies the leaf solely from caller-selected linked qualifying liability, preserving link/provenance and leaving missing input unresolved. | Linked qualifying result reaches liability; no link leaves Elements unresolved. |
| C-263 | Added the Article 263-specific statutory-deeming runtime path over the existing Article 19 leaves and injury result. | The result has `offense.injury`, a `StatutoryDeemingObligation`, and no attribution merge. |
| C-34 | Added and tested a separate indirect-principal path only. | Distinguishes Elements, Unlawfulness, Culpability, and caller-selected different-negligence outcomes. **No production policy was authored.** |
| C-339 | Added checked component-local `when` and component contribution suspension, both using existing `OffenseInstanceKey` identities. The three sealed robbery-side candidates are assembled separately: `robbery_rape = COMPOSE(robbery[333], rape)`, `special_robbery_rape = COMPOSE(special_robbery[334], rape)`, and `quasi_robbery_rape = COMPOSE(quasi_robbery[335], rape)`, each with its own CompletionPolicy. 336 remains a coverage reference only. | A rape-component `when` selects the state from the rape instance; each variant suspends only its named robbery-side contribution. 335 also explicitly disposes its nested quasi-robbery occasion relation. |

| Whole Phase 5.1 verification | Result |
|---|---|
| Production registry | **293** objects; eight-axis type check **0 findings**; **63/63** base/derived offenses compile. |
| Runtime regression | Focused Phase 5.1 paths pass, including all 333/334/335 Art.339 variants; `tests/test_v2_*.py` **236 passed**. |
| Guardrails | Master v3 remains sealed; C-33b is untouched and remains a Step 7 caller-orchestration item; C-34 production policy remains HOLD; coverage remains **80**. |

**Stop point:** **Phase 5.1 PASS.** The affected production assembly now covers
the sealed Art.339 333/334/335 candidate set without an offense-ref union or a
new abstraction. Phase 6 whole-registry audit may begin on instruction.
