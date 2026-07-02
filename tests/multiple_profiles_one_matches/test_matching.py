"""Scenario 7: multiple_profiles_one_matches — tests."""

from swaydm.profile import get_valid_profiles, get_profile


def test_valid_profiles_excludes_office(
    outputs, profile_home, profile_office, profile_laptop
):
    result = get_valid_profiles(
        [profile_home, profile_office, profile_laptop], outputs
    )
    names = [p.name for p in result]
    assert "office" not in names


def test_valid_profiles_includes_home(
    outputs, profile_home, profile_office, profile_laptop
):
    result = get_valid_profiles(
        [profile_home, profile_office, profile_laptop], outputs
    )
    names = [p.name for p in result]
    assert "home" in names


def test_valid_profiles_includes_laptop(
    outputs, profile_home, profile_office, profile_laptop
):
    result = get_valid_profiles(
        [profile_home, profile_office, profile_laptop], outputs
    )
    names = [p.name for p in result]
    assert "laptop" in names


def test_get_profile_returns_home_as_first_auto(outputs, config_obj):
    result = get_profile(config_obj, outputs)
    assert result.name == "home"


def test_get_profile_office_not_returned(outputs, config_obj):
    result = get_profile(config_obj, outputs)
    assert result.name != "office"
