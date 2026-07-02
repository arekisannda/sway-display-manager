"""Scenario 6: no_matching_output_for_display — tests."""

import pytest
from swaydm.profile import (
    get_profile_output_mapping,
    get_valid_profiles,
    get_profile,
)
from swaydm.datatypes import FALLBACK


def test_mapping_raises_value_error(connected_output, profile_obj):
    with pytest.raises(ValueError, match="No sway output matches"):
        get_profile_output_mapping(profile_obj, [connected_output])


def test_valid_profiles_returns_empty(connected_output, profile_obj):
    result = get_valid_profiles([profile_obj], [connected_output])
    assert result == []


def test_get_profile_returns_fallback(connected_output, config_obj):
    result = get_profile(config_obj, [connected_output])
    assert result.name == FALLBACK


def test_fallback_output_is_active(connected_output, config_obj):
    result = get_profile(config_obj, [connected_output])
    assert len(result.outputs) == 1
    assert result.outputs[0].active is True


def test_fallback_output_uses_modes0(connected_output, config_obj):
    result = get_profile(config_obj, [connected_output])
    ap = result.outputs[0]
    assert ap.mode.width == 1920
    assert ap.mode.height == 1080
    assert ap.mode.refresh == 60


def test_fallback_output_is_marked_fallback(connected_output, config_obj):
    result = get_profile(config_obj, [connected_output])
    assert result.outputs[0].fallback is True


def test_fallback_output_position_is_origin(connected_output, config_obj):
    result = get_profile(config_obj, [connected_output])
    assert result.outputs[0].position.x == 0
    assert result.outputs[0].position.y == 0
