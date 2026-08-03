# RuleIR registry audit

- Status: `pass`
- Scope: Registered RuleIR assets only. Every unregistered unit resolves to predicate_ir_missing.

| Unit | Articles | Commentary inputs | System inputs | Queries | Result |
|---|---|---:|---:|---|---|
| fraud | art347 | 88 | 4 | fraud_elements_satisfied, fraud_established, fraud_not_established, fraud_undetermined, fraud_conflict | pass |
| theft | art329, art330, art331, art332, art342 | 66 | 4 | theft_elements_satisfied, theft_established, theft_not_established, theft_undetermined, theft_conflict | pass |
| robbery | art333, art334, art335, art337, art338, art343 | 98 | 4 | robbery_elements_satisfied, robbery_established, robbery_not_established, robbery_undetermined, robbery_conflict | pass |
| extortion | art350 | 41 | 4 | extortion_elements_satisfied, extortion_established, extortion_not_established, extortion_undetermined, extortion_conflict | pass |
| embezzlement | art355, art356 | 64 | 4 | embezzlement_elements_satisfied, embezzlement_established, embezzlement_not_established, embezzlement_undetermined, embezzlement_conflict | pass |
| breach_of_trust | art355, art356 | 36 | 4 | breach_of_trust_elements_satisfied, breach_of_trust_established, breach_of_trust_not_established, breach_of_trust_undetermined, breach_of_trust_conflict | pass |
| breach_of_trust_bribe | art357 | 41 | 4 | breach_of_trust_bribe_elements_satisfied, breach_of_trust_bribe_established, breach_of_trust_bribe_not_established, breach_of_trust_bribe_undetermined, breach_of_trust_bribe_conflict | pass |
| lost_property_embezzlement | art360 | 14 | 4 | lost_property_embezzlement_elements_satisfied, lost_property_embezzlement_established, lost_property_embezzlement_not_established, lost_property_embezzlement_undetermined, lost_property_embezzlement_conflict | pass |
| property_damage | art366 | 53 | 4 | property_damage_elements_satisfied, property_damage_established, property_damage_not_established, property_damage_undetermined, property_damage_conflict | pass |
| interference_with_exercise_of_right | art323 | 32 | 4 | interference_with_exercise_of_right_elements_satisfied, interference_with_exercise_of_right_established, interference_with_exercise_of_right_not_established, interference_with_exercise_of_right_undetermined, interference_with_exercise_of_right_conflict | pass |
| occupational_status | art356 | 10 | 4 | occupational_status_elements_satisfied, occupational_status_established, occupational_status_not_established, occupational_status_undetermined, occupational_status_conflict | pass |
