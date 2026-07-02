"""Scenario 2: connector_name_changed — tests."""

from swaydm.profile import get_profile_output_mapping


def test_matches_original_connector(output_old_name, profile_obj):
    result = get_profile_output_mapping(profile_obj, [output_old_name])
    assert len(result) == 1
    assert result[0].active is True
    assert result[0].name == "DP-1"


def test_matches_new_connector_after_redock(output_new_name, profile_obj):
    result = get_profile_output_mapping(profile_obj, [output_new_name])
    assert len(result) == 1
    assert result[0].active is True
    assert result[0].name == "DP-3"


def test_connector_name_reflects_actual_output_old(
    output_old_name, profile_obj
):
    result = get_profile_output_mapping(profile_obj, [output_old_name])
    assert result[0].name == "DP-1"


def test_connector_name_reflects_actual_output_new(
    output_new_name, profile_obj
):
    result = get_profile_output_mapping(profile_obj, [output_new_name])
    assert result[0].name == "DP-3"


def test_mode_unchanged_regardless_of_connector(
    output_old_name, output_new_name, profile_obj
):
    old_result = get_profile_output_mapping(profile_obj, [output_old_name])
    new_result = get_profile_output_mapping(profile_obj, [output_new_name])
    assert old_result[0].mode == new_result[0].mode
