"""Scenario 3: duplicate_identifier_distinguished_by_mode — tests."""

from swaydm.profile import get_profile_output_mapping


def test_side_display_paired_with_dp4(output_side, output_main, profile_obj):
    result = get_profile_output_mapping(profile_obj, [output_side, output_main])
    by_name = {r.name: r for r in result}
    assert "DP-4" in by_name
    assert by_name["DP-4"].active is True
    assert by_name["DP-4"].mode.width == 1760


def test_main_display_paired_with_dp5(output_side, output_main, profile_obj):
    result = get_profile_output_mapping(profile_obj, [output_side, output_main])
    by_name = {r.name: r for r in result}
    assert "DP-5" in by_name
    assert by_name["DP-5"].active is True
    assert by_name["DP-5"].mode.width == 3360


def test_side_alias_correct(output_side, output_main, profile_obj):
    result = get_profile_output_mapping(profile_obj, [output_side, output_main])
    by_name = {r.name: r for r in result}
    assert by_name["DP-4"].alias == "SIDE"


def test_main_alias_correct(output_side, output_main, profile_obj):
    result = get_profile_output_mapping(profile_obj, [output_side, output_main])
    by_name = {r.name: r for r in result}
    assert by_name["DP-5"].alias == "MAIN"


def test_both_outputs_active(output_side, output_main, profile_obj):
    result = get_profile_output_mapping(profile_obj, [output_side, output_main])
    assert all(r.active for r in result)
