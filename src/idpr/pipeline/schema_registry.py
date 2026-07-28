"""
schema_registry.py
Defines the 32 Datalog Input Predicates Schema Registry for P1+P2 criminal law fact extraction.
"""

from __future__ import annotations

from typing import Any, Dict

# 32 Datalog Input Predicate Relations Schema Registry
PREDICATE_SCHEMA_REGISTRY: Dict[str, Dict[str, Any]] = {
    "version": "1.0.0",
    "description": "Schema registry of 32 Datalog input predicates for P1 property and P2 non-property crimes",
    "predicates": {
        "actor": {"datalog": "rel actor(c: case, p: person)", "description": "Accused / Defendant"},
        "victim": {"datalog": "rel victim(c: case, p: person)", "description": "Victim / Counterpart"},
        "deceived_person": {"datalog": "rel deceived_person(c: case, p: person)", "description": "Person in mistake"},
        "disposer": {"datalog": "rel disposer(c: case, p: person)", "description": "Person executing property disposition"},
        "property_owner": {"datalog": "rel property_owner(c: case, p: person, pr: property)", "description": "Owner of property"},
        "beneficiary": {"datalog": "rel beneficiary(c: case, p: person)", "description": "Direct beneficiary of disposition"},
        "possession": {"datalog": "rel possession(c: case, p: person, pr: property)", "description": "Possessor of property"},
        "ownership": {"datalog": "rel ownership(c: case, p: person, pr: property)", "description": "Owner of property"},
        "legal_custody": {"datalog": "rel legal_custody(c: case, p: person, pr: property)", "description": "Custodian of property"},
        "public_office": {"datalog": "rel public_office(c: case, p: person, title: string)", "description": "Public servant status"},
        "action_committed": {"datalog": "rel action_committed(c: case, a: act)", "description": "Execution of action"},
        "unlawful_taking": {"datalog": "rel unlawful_taking(c: case, a: act, pr: property)", "description": "Unlawful taking of property"},
        "deception_committed": {"datalog": "rel deception_committed(c: case, detail: string)", "description": "Deceptive representation"},
        "disposition_committed": {"datalog": "rel disposition_committed(c: case, detail: string)", "description": "Property disposition act"},
        "property_transfer": {"datalog": "rel property_transfer(c: case, pr: property, from_p: person, to_p: person)", "description": "Property transfer"},
        "dwelling_intrusion_committed": {"datalog": "rel dwelling_intrusion_committed(c: case, pl: place)", "description": "Unlawful entry into dwelling"},
        "arson_act": {"datalog": "rel arson_act(c: case, pl: place)", "description": "Setting fire to structure"},
        "force_or_threat": {"datalog": "rel force_or_threat(c: case, degree: string)", "description": "Violence or intimidation"},
        "document_forgery": {"datalog": "rel document_forgery(c: case, doc: document)", "description": "Document forgery"},
        "public_duty_obstruction": {"datalog": "rel public_duty_obstruction(c: case, act: string)", "description": "Obstruction of public duty"},
        "unlawful_intent": {"datalog": "rel unlawful_intent(c: case, kind: string)", "description": "Unlawful intent ('murder', 'theft', 'fraud', 'arson', 'injury')"},
        "true_purpose": {"datalog": "rel true_purpose(c: case, detail: string)", "description": "Inner true purpose"},
        "result_occurred": {"datalog": "rel result_occurred(c: case, res: string)", "description": "Occurred result ('death', 'bodily_injury', 'property_loss')"},
        "independent_combustion": {"datalog": "rel independent_combustion(c: case, pl: place)", "description": "Independent combustion state"},
        "causation_established": {"datalog": "rel causation_established(c: case, cause: act, result: string)", "description": "Causation between act and result"},
        "building_type": {"datalog": "rel building_type(c: case, pl: place, b_type: string)", "description": "Structure type ('dwelling', 'general')"},
        "consent_given": {"datalog": "rel consent_given(c: case, p: person)", "description": "Valid consent from victim"},
        "self_defense_claimed": {"datalog": "rel self_defense_claimed(c: case)", "description": "Self-defense circumstances"},
        "attempt_status": {"datalog": "rel attempt_status(c: case, stage: string)", "description": "Attempt stage"},
        "accomplice_role": {"datalog": "rel accomplice_role(c: case, p: person, role_type: string)", "description": "Accomplice status"},
        "business_nature": {"datalog": "rel business_nature(c: case, b: string)", "description": "Business or occupational nature"},
        "other_fact": {"datalog": "rel other_fact(c: case, detail: string)", "description": "Other relevant fact"}
    }
}

def get_predicate_names() -> list[str]:
    return list(PREDICATE_SCHEMA_REGISTRY["predicates"].keys())
