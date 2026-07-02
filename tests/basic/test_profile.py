"""Tests for swaydm.profile functions."""

import pytest
from swaydm.profile import (
    output_identifier,
    matches_display_name,
    matches_display_mode,
    get_profile_output_mapping,
    get_valid_profiles,
    get_profile,
)
from swaydm.datatypes import (
    Config,
    Profile,
    Display,
    Mode,
    Position,
    FALLBACK,
)
from tests.conftest import FakeOutput, FakeMode


# ---------------------------------------------------------------------------
# output_identifier
# ---------------------------------------------------------------------------


class TestOutputIdentifier:
    def test_returns_make_model_serial_when_all_present(self, make_output):
        output = make_output(manufacturer="Dell", model="U2720Q", serial="XYZ1")
        assert output_identifier(output) == "Dell U2720Q XYZ1"

    def test_falls_back_to_name_when_make_empty(self, make_output):
        output = make_output(
            name="HDMI-1", manufacturer="", model="U2720Q", serial="XYZ1"
        )
        assert output_identifier(output) == "HDMI-1"

    def test_falls_back_to_name_when_model_empty(self, make_output):
        output = make_output(
            name="HDMI-1", manufacturer="Dell", model="", serial="XYZ1"
        )
        assert output_identifier(output) == "HDMI-1"

    def test_falls_back_to_name_when_serial_empty(self, make_output):
        output = make_output(
            name="HDMI-1", manufacturer="Dell", model="U2720Q", serial=""
        )
        assert output_identifier(output) == "HDMI-1"

    def test_falls_back_to_name_when_make_whitespace_only(self):
        output = FakeOutput(
            name="eDP-1",
            make="   ",
            model="InternalDisplay",
            serial="SN999",
            modes=[FakeMode(1920, 1080, 60000)],
        )
        assert output_identifier(output) == "eDP-1"

    def test_falls_back_to_name_when_all_blank(self):
        output = FakeOutput(
            name="VGA-1",
            make="",
            model="",
            serial="",
            modes=[FakeMode(1280, 1024, 75000)],
        )
        assert output_identifier(output) == "VGA-1"

    def test_strips_whitespace_from_fields(self):
        output = FakeOutput(
            name="DP-2",
            make="  Acme  ",
            model="  Widget  ",
            serial="  S100  ",
            modes=[FakeMode(1920, 1080, 60000)],
        )
        assert output_identifier(output) == "Acme Widget S100"


# ---------------------------------------------------------------------------
# matches_display_name
# ---------------------------------------------------------------------------


class TestMatchesDisplayName:
    def test_matches_by_connector_name(self, make_output):
        output = make_output(
            name="DP-1", manufacturer="Acme", model="M1", serial="S1"
        )
        assert matches_display_name(output, "DP-1") is True

    def test_matches_by_vendor_identifier(self, make_output):
        output = make_output(
            name="DP-1", manufacturer="Acme", model="M1", serial="S1"
        )
        assert matches_display_name(output, "Acme M1 S1") is True

    def test_no_match_wrong_name(self, make_output):
        output = make_output(
            name="DP-1", manufacturer="Acme", model="M1", serial="S1"
        )
        assert matches_display_name(output, "DP-2") is False

    def test_no_match_wrong_identifier(self, make_output):
        output = make_output(
            name="DP-1", manufacturer="Acme", model="M1", serial="S1"
        )
        assert matches_display_name(output, "Acme M1 S2") is False

    def test_case_sensitive_match(self, make_output):
        output = make_output(
            name="DP-1", manufacturer="Dell", model="U2720Q", serial="ABC"
        )
        # lowercase should NOT match
        assert matches_display_name(output, "dell u2720q abc") is False

    def test_connector_match_takes_priority(self, make_output):
        # connector name == identifier string (unlikely but valid)
        output = make_output(
            name="Dell U2720Q ABC",
            manufacturer="Dell",
            model="U2720Q",
            serial="ABC",
        )
        assert matches_display_name(output, "Dell U2720Q ABC") is True


# ---------------------------------------------------------------------------
# matches_display_mode
# ---------------------------------------------------------------------------


class TestMatchesDisplayMode:
    def test_exact_match(self, make_output):
        output = make_output(width=1920, height=1080, refresh=60)
        want = Mode(width=1920, height=1080, refresh=60, scale=1.0)
        assert matches_display_mode(output, want) is True

    def test_within_1hz_tolerance(self):
        # output reports 59000 milliHz (rounds to 59), want is 60
        output = FakeOutput(
            name="DP-1",
            make="A",
            model="B",
            serial="C",
            modes=[FakeMode(1920, 1080, 59000)],
        )
        want = Mode(width=1920, height=1080, refresh=60, scale=1.0)
        assert matches_display_mode(output, want) is True

    def test_outside_tolerance_fails(self):
        # output reports 57000 milliHz (rounds to 57), want is 60
        output = FakeOutput(
            name="DP-1",
            make="A",
            model="B",
            serial="C",
            modes=[FakeMode(1920, 1080, 57000)],
        )
        want = Mode(width=1920, height=1080, refresh=60, scale=1.0)
        assert matches_display_mode(output, want) is False

    def test_wrong_resolution_fails(self, make_output):
        output = make_output(width=2560, height=1440, refresh=60)
        want = Mode(width=1920, height=1080, refresh=60, scale=1.0)
        assert matches_display_mode(output, want) is False

    def test_multiple_modes_one_matches(self):
        output = FakeOutput(
            name="DP-1",
            make="A",
            model="B",
            serial="C",
            modes=[
                FakeMode(1280, 720, 60000),
                FakeMode(1920, 1080, 60000),
                FakeMode(1920, 1080, 144000),
            ],
        )
        want = Mode(width=1920, height=1080, refresh=144, scale=1.0)
        assert matches_display_mode(output, want) is True

    def test_no_modes_returns_false(self):
        output = FakeOutput(
            name="DP-1",
            make="A",
            model="B",
            serial="C",
            modes=[],
        )
        want = Mode(width=1920, height=1080, refresh=60, scale=1.0)
        assert matches_display_mode(output, want) is False

    def test_wrong_height_fails(self, make_output):
        output = make_output(width=1920, height=1200, refresh=60)
        want = Mode(width=1920, height=1080, refresh=60, scale=1.0)
        assert matches_display_mode(output, want) is False


# ---------------------------------------------------------------------------
# get_profile_output_mapping
# ---------------------------------------------------------------------------


class TestGetProfileOutputMapping:
    def test_single_display_matched(self, make_output):
        output = make_output(
            name="DP-1", manufacturer="Acme", model="XZ27", serial="ABC"
        )
        profile = Profile(
            name="test",
            displays=[
                Display(
                    name="Acme XZ27 ABC",
                    mode=Mode(1920, 1080, 60, 1.0),
                    position=Position(0, 0),
                )
            ],
        )
        result = get_profile_output_mapping(profile, [output])
        assert len(result) == 1
        assert result[0].name == "DP-1"
        assert result[0].active is True
        assert result[0].mode == Mode(1920, 1080, 60, 1.0)
        assert result[0].position == Position(0, 0)

    def test_unmatched_output_disabled(self, make_output):
        output_main = make_output(
            name="DP-1", manufacturer="Acme", model="XZ27", serial="ABC"
        )
        output_extra = make_output(
            name="DP-2", manufacturer="Other", model="Y1", serial="XX1"
        )
        profile = Profile(
            name="test",
            displays=[
                Display(
                    name="Acme XZ27 ABC",
                    mode=Mode(1920, 1080, 60, 1.0),
                    position=Position(0, 0),
                )
            ],
        )
        result = get_profile_output_mapping(
            profile, [output_main, output_extra]
        )
        by_name = {r.name: r for r in result}
        assert by_name["DP-1"].active is True
        assert by_name["DP-2"].active is False

    def test_raises_when_no_matching_output(self, make_output):
        output = make_output(
            name="DP-1", manufacturer="Acme", model="XZ27", serial="ABC"
        )
        profile = Profile(
            name="test",
            displays=[
                Display(
                    name="Nonexistent Monitor",
                    mode=Mode(1920, 1080, 60, 1.0),
                    position=Position(0, 0),
                )
            ],
        )
        with pytest.raises(ValueError, match="No sway output matches"):
            get_profile_output_mapping(profile, [output])

    def test_display_without_mode_is_skipped(self, make_output):
        output = make_output(name="DP-1")
        profile = Profile(
            name="test",
            displays=[Display(name="DP-1", mode=None)],
        )
        # No mode means the display entry is skipped; DP-1 gets disabled
        result = get_profile_output_mapping(profile, [output])
        assert len(result) == 1
        assert result[0].active is False

    def test_output_order_preserved(self, make_output):
        out_a = make_output(
            name="DP-1", manufacturer="A", model="M", serial="1"
        )
        out_b = make_output(
            name="DP-2", manufacturer="B", model="N", serial="2"
        )
        profile = Profile(
            name="test",
            displays=[
                Display(
                    name="A M 1",
                    mode=Mode(1920, 1080, 60, 1.0),
                    position=Position(0, 0),
                ),
                Display(
                    name="B N 2",
                    mode=Mode(1920, 1080, 60, 1.0),
                    position=Position(1920, 0),
                ),
            ],
        )
        result = get_profile_output_mapping(profile, [out_a, out_b])
        assert result[0].name == "DP-1"
        assert result[1].name == "DP-2"

    def test_alias_propagated(self, make_output):
        output = make_output(
            name="DP-1", manufacturer="Acme", model="XZ27", serial="ABC"
        )
        profile = Profile(
            name="test",
            displays=[
                Display(
                    name="Acme XZ27 ABC",
                    alias="PRIMARY",
                    mode=Mode(1920, 1080, 60, 1.0),
                    position=Position(0, 0),
                )
            ],
        )
        result = get_profile_output_mapping(profile, [output])
        assert result[0].alias == "PRIMARY"


# ---------------------------------------------------------------------------
# get_valid_profiles
# ---------------------------------------------------------------------------


class TestGetValidProfiles:
    def test_returns_profiles_that_can_be_mapped(self, make_output):
        output = make_output(
            name="DP-1", manufacturer="Acme", model="M1", serial="S1"
        )
        good = Profile(
            name="good",
            displays=[
                Display(
                    name="Acme M1 S1",
                    mode=Mode(1920, 1080, 60, 1.0),
                    position=Position(0, 0),
                )
            ],
        )
        bad = Profile(
            name="bad",
            displays=[
                Display(
                    name="Missing Monitor",
                    mode=Mode(1920, 1080, 60, 1.0),
                    position=Position(0, 0),
                )
            ],
        )
        result = get_valid_profiles([good, bad], [output])
        names = [p.name for p in result]
        assert "good" in names
        assert "bad" not in names

    def test_empty_list_when_none_match(self, make_output):
        output = make_output(name="DP-1")
        profile = Profile(
            name="p",
            displays=[
                Display(
                    name="Absent",
                    mode=Mode(1920, 1080, 60, 1.0),
                    position=Position(0, 0),
                )
            ],
        )
        assert get_valid_profiles([profile], [output]) == []

    def test_empty_input_returns_empty(self, make_output):
        output = make_output()
        assert get_valid_profiles([], [output]) == []

    def test_all_valid_profiles_returned(self, make_output):
        out1 = make_output(name="DP-1", manufacturer="A", model="M", serial="1")
        out2 = make_output(name="DP-2", manufacturer="B", model="N", serial="2")
        p1 = Profile(
            name="p1",
            displays=[
                Display(
                    name="A M 1",
                    mode=Mode(1920, 1080, 60, 1.0),
                    position=Position(0, 0),
                )
            ],
        )
        p2 = Profile(
            name="p2",
            displays=[
                Display(
                    name="B N 2",
                    mode=Mode(1920, 1080, 60, 1.0),
                    position=Position(0, 0),
                )
            ],
        )
        result = get_valid_profiles([p1, p2], [out1, out2])
        assert len(result) == 2


# ---------------------------------------------------------------------------
# get_profile
# ---------------------------------------------------------------------------


class TestGetProfile:
    def test_auto_profile_selected_when_no_name_given(self, make_output):
        output = make_output(
            name="DP-1", manufacturer="A", model="M", serial="S"
        )
        p_auto = Profile(
            name="auto_prof",
            auto=True,
            displays=[
                Display(
                    name="A M S",
                    mode=Mode(1920, 1080, 60, 1.0),
                    position=Position(0, 0),
                )
            ],
        )
        config = Config(profiles=[p_auto])
        result = get_profile(config, [output])
        assert result.name == "auto_prof"

    def test_non_auto_profile_ignored_in_auto_mode(self, make_output):
        output = make_output(
            name="DP-1", manufacturer="A", model="M", serial="S"
        )
        p_manual = Profile(
            name="manual_prof",
            auto=False,
            displays=[
                Display(
                    name="A M S",
                    mode=Mode(1920, 1080, 60, 1.0),
                    position=Position(0, 0),
                )
            ],
        )
        config = Config(profiles=[p_manual])
        # No auto profiles available in the list → raises ValueError (profile=None, no auto entries)
        with pytest.raises(ValueError):
            get_profile(config, [output])

    def test_fallback_returned_when_no_auto_profiles_match(self, make_output):
        # Auto profile exists but no output matches it → fallback returned
        output = make_output(name="DP-1", width=1920, height=1080, refresh=60)
        p = Profile(
            name="office",
            auto=True,
            displays=[
                Display(
                    name="Absent Monitor",
                    mode=Mode(2560, 1440, 60, 1.0),
                    position=Position(0, 0),
                )
            ],
        )
        config = Config(profiles=[p])
        result = get_profile(config, [output])
        assert result.name == FALLBACK

    def test_fallback_profile_uses_first_mode(self, make_output):
        # Auto profile exists but doesn't match → fallback with modes[0] values
        output = make_output(name="DP-1", width=1920, height=1080, refresh=60)
        p = Profile(
            name="nomatch",
            auto=True,
            displays=[
                Display(
                    name="Missing Monitor",
                    mode=Mode(9999, 9999, 60, 1.0),
                    position=Position(0, 0),
                )
            ],
        )
        config = Config(profiles=[p])
        result = get_profile(config, [output])
        assert result.name == FALLBACK
        assert len(result.outputs) == 1
        assert result.outputs[0].active is True
        assert result.outputs[0].mode.width == 1920
        assert result.outputs[0].mode.height == 1080
        assert result.outputs[0].mode.refresh == 60

    def test_explicit_profile_name_matched(self, make_output):
        output = make_output(
            name="DP-1", manufacturer="A", model="M", serial="S"
        )
        p = Profile(
            name="explicit",
            auto=False,
            displays=[
                Display(
                    name="A M S",
                    mode=Mode(1920, 1080, 60, 1.0),
                    position=Position(0, 0),
                )
            ],
        )
        config = Config(profiles=[p])
        result = get_profile(config, [output], profile="explicit")
        assert result.name == "explicit"

    def test_raises_for_unknown_explicit_profile(self, make_output):
        output = make_output()
        config = Config(profiles=[])
        with pytest.raises(ValueError, match="is not a profile"):
            get_profile(config, [output], profile="nonexistent")

    def test_fallback_name_does_not_raise(self, make_output):
        output = make_output(name="DP-1", width=1920, height=1080, refresh=60)
        config = Config(profiles=[])
        # FALLBACK constant as explicit name should not raise, just return fallback
        result = get_profile(config, [output], profile=FALLBACK)
        assert result.name == FALLBACK

    def test_fallback_positions_outputs_side_by_side(self):
        out1 = FakeOutput(
            name="DP-1",
            make="A",
            model="M",
            serial="1",
            modes=[FakeMode(1920, 1080, 60000)],
        )
        out2 = FakeOutput(
            name="DP-2",
            make="B",
            model="N",
            serial="2",
            modes=[FakeMode(2560, 1440, 60000)],
        )
        # Use an auto profile that won't match so fallback kicks in
        no_match = Profile(
            name="nomatch",
            auto=True,
            displays=[
                Display(
                    name="Ghost Monitor",
                    mode=Mode(9999, 9999, 60, 1.0),
                    position=Position(0, 0),
                )
            ],
        )
        config = Config(profiles=[no_match])
        result = get_profile(config, [out1, out2])
        assert result.name == FALLBACK
        assert result.outputs[0].position.x == 0
        assert result.outputs[1].position.x == 1920
