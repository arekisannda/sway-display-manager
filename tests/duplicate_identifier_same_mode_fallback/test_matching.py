"""Scenario 4: duplicate_identifier_same_mode_fallback — tests."""

from swaydm.profile import get_profile_output_mapping


def test_first_display_paired_with_output_a(outputs, profile_obj):
    result = get_profile_output_mapping(profile_obj, outputs)
    by_name = {r.name: r for r in result}
    # output_a (DP-6) should be assigned to display[0] (alias FIRST)
    assert by_name["DP-6"].alias == "FIRST"


def test_second_display_paired_with_output_b(outputs, profile_obj):
    result = get_profile_output_mapping(profile_obj, outputs)
    by_name = {r.name: r for r in result}
    # output_b (DP-7) should be assigned to display[1] (alias SECOND)
    assert by_name["DP-7"].alias == "SECOND"


def test_deterministic_repeated_calls(outputs, profile_obj):
    result1 = get_profile_output_mapping(profile_obj, outputs)
    result2 = get_profile_output_mapping(profile_obj, outputs)
    by_name1 = {r.name: r for r in result1}
    by_name2 = {r.name: r for r in result2}
    assert by_name1["DP-6"].alias == by_name2["DP-6"].alias
    assert by_name1["DP-7"].alias == by_name2["DP-7"].alias


def test_reversed_outputs_reverses_assignment(output_a, output_b, profile_obj):
    reversed_outputs = [output_b, output_a]
    result = get_profile_output_mapping(profile_obj, reversed_outputs)
    by_name = {r.name: r for r in result}
    # Now DP-7 comes first in the list → assigned to display[0] (FIRST)
    assert by_name["DP-7"].alias == "FIRST"
    assert by_name["DP-6"].alias == "SECOND"


def test_both_outputs_active(outputs, profile_obj):
    result = get_profile_output_mapping(profile_obj, outputs)
    assert all(r.active for r in result)
