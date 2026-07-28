"""
schema_registry.py
Defines the 32 Datalog Input Predicates Schema Registry for P1+P2 criminal law fact extraction.
Provides valid OpenAI/vLLM JSON Schema (Draft 7) for structured neural output.
"""

from __future__ import annotations

from typing import Any, Dict

PREDICATE_SCHEMA_REGISTRY: Dict[str, Any] = {
    "version": "1.0.0",
    "description": "Schema registry of 32 Datalog input predicates for P1 property and P2 non-property crimes",
    "predicates": {
        # 1. 당사자 및 신분 (6)
        "actor": {"datalog": "rel actor(c: string, p: string)", "description": "Accused / Defendant"},
        "victim": {"datalog": "rel victim(c: string, p: string)", "description": "Victim / Counterpart"},
        "deceived_person": {"datalog": "rel deceived_person(c: string, p: string)", "description": "Person in mistake"},
        "disposer": {"datalog": "rel disposer(c: string, p: string)", "description": "Person executing property disposition"},
        "property_owner": {"datalog": "rel property_owner(c: string, p: string, pr: string)", "description": "Owner of property"},
        "public_office": {"datalog": "rel public_office(c: string, p: string, title: string)", "description": "Public servant status"},

        # 2. 점유 및 권리 (4)
        "possession": {"datalog": "rel possession(c: string, p: string, pr: string)", "description": "Possessor of property"},
        "ownership": {"datalog": "rel ownership(c: string, p: string, pr: string)", "description": "Owner of property"},
        "legal_custody": {"datalog": "rel legal_custody(c: string, p: string, pr: string)", "description": "Custodian of property"},
        "business_nature": {"datalog": "rel business_nature(c: string, b: string)", "description": "Occupational or business nature"},

        # 3. 실행 행위 (10)
        "action_committed": {"datalog": "rel action_committed(c: string, a: string)", "description": "Execution of action"},
        "unlawful_taking": {"datalog": "rel unlawful_taking(c: string, a: string, pr: string)", "description": "Unlawful taking of property"},
        "deception_committed": {"datalog": "rel deception_committed(c: string, d: string)", "description": "Deceptive representation"},
        "disposition_committed": {"datalog": "rel disposition_committed(c: string, d: string)", "description": "Property disposition act"},
        "dwelling_intrusion_committed": {"datalog": "rel dwelling_intrusion_committed(c: string, pl: string)", "description": "Unlawful entry into dwelling"},
        "arson_act": {"datalog": "rel arson_act(c: string, pl: string)", "description": "Setting fire to structure"},
        "force_or_threat": {"datalog": "rel force_or_threat(c: string, degree: string)", "description": "Violence or intimidation"},
        "document_forgery": {"datalog": "rel document_forgery(c: string, doc: string)", "description": "Document forgery"},
        "public_duty_obstruction": {"datalog": "rel public_duty_obstruction(c: string, act: string)", "description": "Obstruction of public duty"},
        "bribery_delivery_committed": {"datalog": "rel bribery_delivery_committed(c: string, giver: string, recipient: string)", "description": "Accepting money with knowledge of bribery delivery purpose"},

        # 4. 고의 및 내심 (3)
        "unlawful_intent": {"datalog": "rel unlawful_intent(c: string, kind: string)", "description": "Unlawful intent ('murder', 'theft', 'fraud', 'arson', 'injury', 'embezzlement', 'breach')"},
        "true_purpose": {"datalog": "rel true_purpose(c: string, detail: string)", "description": "Inner true purpose"},
        "knowledge_of_fact": {"datalog": "rel knowledge_of_fact(c: string, detail: string)", "description": "Knowledge of criminal fact"},

        # 5. 결과 및 상태 (5)
        "result_occurred": {"datalog": "rel result_occurred(c: string, res: string)", "description": "Occurred result ('death', 'bodily_injury', 'property_loss')"},
        "independent_combustion": {"datalog": "rel independent_combustion(c: string, pl: string)", "description": "Independent combustion state"},
        "causation_established": {"datalog": "rel causation_established(c: string, cause: string, result: string)", "description": "Causation between act and result"},
        "building_type": {"datalog": "rel building_type(c: string, pl: string, b_type: string)", "description": "Structure type ('dwelling', 'general')"},
        "public_danger_occurred": {"datalog": "rel public_danger_occurred(c: string, detail: string)", "description": "Concrete public danger"},

        # 6. 위법성 및 책임 조각 사유 (4)
        "consent_given": {"datalog": "rel consent_given(c: string, p: string)", "description": "Valid consent from victim"},
        "self_defense_claimed": {"datalog": "rel self_defense_claimed(c: string)", "description": "Self-defense circumstances"},
        "necessity_claimed": {"datalog": "rel necessity_claimed(c: string)", "description": "State of emergency / necessity"},
        "insanity_claimed": {"datalog": "rel insanity_claimed(c: string)", "description": "Mental insanity / diminished capacity"}
    }
}

def get_fact_graph_json_schema() -> Dict[str, Any]:
    """Generates valid OpenAI / vLLM JSON Schema Draft 7 for Stage 1 Neural Fact Graph."""
    predicate_list = list(PREDICATE_SCHEMA_REGISTRY["predicates"].keys())
    return {
        "type": "object",
        "properties": {
            "case_id": {"type": "string"},
            "actors": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "entity_id": {"type": "string"},
                        "roles": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["entity_id", "roles"],
                    "additionalProperties": False
                }
            },
            "facts": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "fact_id": {"type": "string"},
                        "predicate": {
                            "type": "string",
                            "enum": predicate_list
                        },
                        "statement": {"type": "string"},
                        "arguments": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["fact_id", "predicate", "statement", "arguments"],
                    "additionalProperties": False
                }
            }
        },
        "required": ["case_id", "actors", "facts"],
        "additionalProperties": False
    }
