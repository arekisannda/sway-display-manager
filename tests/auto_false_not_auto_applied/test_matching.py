"""Scenario 8: auto_false_not_auto_applied — tests."""

from swaydm.profile import get_profile


def test_auto_profile_selected_automatically(outputs, config_obj, profile_auto):
    result = get_profile(config_obj, outputs)
    assert result.name == profile_auto.name


def test_manual_profile_not_selected_automatically(
    outputs, config_obj, profile_manual
):
    result = get_profile(config_obj, outputs)
    assert result.name != profile_manual.name


def test_explicit_switch_to_manual_works(outputs, config_obj, profile_manual):
    result = get_profile(config_obj, outputs, profile=profile_manual.name)
    assert result.name == profile_manual.name


def test_explicit_switch_to_auto_works(outputs, config_obj, profile_auto):
    result = get_profile(config_obj, outputs, profile=profile_auto.name)
    assert result.name == profile_auto.name


def test_manual_profile_is_active_when_explicitly_requested(
    outputs, config_obj, profile_manual
):
    result = get_profile(config_obj, outputs, profile=profile_manual.name)
    assert all(o.active for o in result.outputs if o.name == "DP-1")
