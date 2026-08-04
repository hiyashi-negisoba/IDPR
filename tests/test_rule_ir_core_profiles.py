from __future__ import annotations

from idpr.rulegen.core_profile import build_core_profiles, load_core_profiles


def test_every_registered_unit_has_a_hash_pinned_core_projection() -> None:
    generated = build_core_profiles()
    committed = load_core_profiles()
    assert committed == generated
    assert len(committed["units"]) == 36


def test_norm_card_inputs_are_not_exposed_as_model_predicates() -> None:
    profiles = load_core_profiles()["units"]
    detailed = sum(
        profile["detailed_card_predicates"]["count"]
        for profile in profiles.values()
    )
    core = sum(len(profile["model_input_predicates"]) for profile in profiles.values())
    assert detailed > 1600
    assert core < detailed // 4
    assert profiles["fraud"]["detailed_card_predicates"]["count"] == 88
    assert len(profiles["fraud"]["model_input_predicates"]) == 10
    assert profiles["theft"]["detailed_card_predicates"]["count"] == 66
    assert len(profiles["theft"]["model_input_predicates"]) == 6


def test_profiles_preserve_tracks_and_component_authority() -> None:
    homicide = load_core_profiles()["units"]["homicide"]
    assert {item["track_id"] for item in homicide["tracks"]} >= {
        "base", "attempt", "parricide"
    }
    assert all(
        item["authority_card_ids"] and item["source_refs"]
        for item in homicide["model_input_predicates"]
    )


def test_every_role_argument_has_a_legal_meaning_contract() -> None:
    profiles = load_core_profiles()["units"]
    for profile in profiles.values():
        expected = {
            item["name"] for item in profile["role_contract"]["arguments"]
            if item["name"] != "case_id"
        }
        assert set(profile["role_contract"]["role_definitions"]) == expected
    owner = profiles["embezzlement"]["role_contract"]["role_definitions"]["owner_id"]
    assert "최초 출연자" in owner
    assert "동일하다고 추정하지 않는다" in owner
    rules = profiles["embezzlement"]["role_contract"]["assignment_rules"]
    assert any("직접 위탁" in rule for rule in rules)
    assert any("소비대차" in rule for rule in rules)
