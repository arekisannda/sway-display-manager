"""Scenario 1: basic_single_match — tests."""

from swaydm.profile import get_profile_output_mapping
from swaydm.datatypes import Mode, Position


def test_output_assigned_not_disabled(output, profile_obj):
    result = get_profile_output_mapping(profile_obj, [output])
    assert len(result) == 1
    assert result[0].active is True


def test_apply_output_name_is_connector(output, profile_obj):
    result = get_profile_output_mapping(profile_obj, [output])
    assert result[0].name == "DP-1"


def test_apply_output_mode_correct(output, profile_obj):
    result = get_profile_output_mapping(profile_obj, [output])
    assert result[0].mode == Mode(
        width=2560, height=1440, refresh=60, scale=1.0
    )


def test_apply_output_position_correct(output, profile_obj):
    result = get_profile_output_mapping(profile_obj, [output])
    assert result[0].position == Position(x=0, y=0)


def test_fallback_flag_false(output, profile_obj):
    result = get_profile_output_mapping(profile_obj, [output])
    assert result[0].fallback is False
