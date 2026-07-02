"""Tests for swaydm.config functions."""

import textwrap

import pytest

from swaydm.config import (
    parse_display,
    parse_profile,
    find_config_file,
    load_config,
)
from swaydm.datatypes import FALLBACK, Config, Mode, Position


# ---------------------------------------------------------------------------
# parse_display
# ---------------------------------------------------------------------------


class TestParseDisplay:
    def test_name_only(self):
        d = parse_display({"name": "DP-1"})
        assert d.name == "DP-1"
        assert d.alias is None
        assert d.mode is None
        assert d.position is None

    def test_with_alias(self):
        d = parse_display({"name": "DP-1", "alias": "PRIMARY"})
        assert d.alias == "PRIMARY"

    def test_with_mode(self):
        d = parse_display(
            {
                "name": "DP-1",
                "mode": {
                    "width": 1920,
                    "height": 1080,
                    "refresh": 60,
                    "scale": 1.5,
                },
            }
        )
        assert d.mode == Mode(width=1920, height=1080, refresh=60, scale=1.5)

    def test_with_position(self):
        d = parse_display(
            {
                "name": "DP-1",
                "position": {"x": 1920, "y": 0},
            }
        )
        assert d.position == Position(x=1920, y=0)

    def test_full_display(self):
        d = parse_display(
            {
                "name": "Dell U2720Q XYZ",
                "alias": "LEFT",
                "mode": {
                    "width": 2560,
                    "height": 1440,
                    "refresh": 60,
                    "scale": 1.0,
                },
                "position": {"x": 0, "y": 0},
            }
        )
        assert d.name == "Dell U2720Q XYZ"
        assert d.alias == "LEFT"
        assert d.mode.width == 2560
        assert d.position.x == 0

    def test_scale_preserved(self):
        d = parse_display(
            {
                "name": "eDP-1",
                "mode": {
                    "width": 2560,
                    "height": 1600,
                    "refresh": 60,
                    "scale": 2.0,
                },
            }
        )
        assert d.mode.scale == 2.0


# ---------------------------------------------------------------------------
# parse_profile
# ---------------------------------------------------------------------------


class TestParseProfile:
    def test_basic_profile(self):
        p = parse_profile({"name": "home", "displays": []})
        assert p.name == "home"
        assert p.auto is True
        assert p.displays == []
        assert p.commands == []

    def test_auto_false(self):
        p = parse_profile({"name": "desk", "auto": False})
        assert p.auto is False

    def test_with_displays(self):
        p = parse_profile(
            {
                "name": "dual",
                "displays": [
                    {
                        "name": "DP-1",
                        "mode": {
                            "width": 1920,
                            "height": 1080,
                            "refresh": 60,
                            "scale": 1.0,
                        },
                        "position": {"x": 0, "y": 0},
                    },
                ],
            }
        )
        assert len(p.displays) == 1
        assert p.displays[0].name == "DP-1"

    def test_with_commands(self):
        p = parse_profile(
            {
                "name": "gaming",
                "commands": ["output DP-1 adaptive_sync on"],
            }
        )
        assert p.commands == ["output DP-1 adaptive_sync on"]

    def test_raises_for_reserved_name(self):
        with pytest.raises(ValueError, match="reserved"):
            parse_profile({"name": FALLBACK})

    def test_auto_defaults_to_true_when_absent(self):
        p = parse_profile({"name": "myprofile"})
        assert p.auto is True

    def test_displays_default_to_empty_when_absent(self):
        p = parse_profile({"name": "myprofile"})
        assert p.displays == []

    def test_commands_default_to_empty_when_absent(self):
        p = parse_profile({"name": "myprofile"})
        assert p.commands == []


# ---------------------------------------------------------------------------
# find_config_file
# ---------------------------------------------------------------------------


class TestFindConfigFile:
    def test_explicit_existing_path_returned(self, tmp_path, monkeypatch):
        config_file = tmp_path / "my_config.yaml"
        config_file.write_text("profiles: []")
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "xdg"))
        result = find_config_file(str(config_file))
        assert result == config_file

    def test_explicit_nonexistent_falls_through_to_default(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
        default_dir = tmp_path / "swaydm"
        default_dir.mkdir()
        default_file = default_dir / "config.yaml"
        default_file.write_text("profiles: []")
        result = find_config_file(str(tmp_path / "nonexistent.yaml"))
        assert result == default_file

    def test_first_default_wins(self, tmp_path, monkeypatch):
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
        # Create both default locations
        default_dir = tmp_path / "swaydm"
        default_dir.mkdir()
        first_default = default_dir / "config.yaml"
        first_default.write_text("profiles: []")
        second_default = tmp_path / "swaydm.yaml"
        second_default.write_text("profiles: []")
        result = find_config_file("")
        assert result == first_default

    def test_second_default_used_when_first_absent(self, tmp_path, monkeypatch):
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
        # Only second default exists
        second_default = tmp_path / "swaydm.yaml"
        second_default.write_text("profiles: []")
        result = find_config_file("")
        assert result == second_default

    def test_returns_none_when_nothing_exists(self, tmp_path, monkeypatch):
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "empty"))
        result = find_config_file("")
        assert result is None

    def test_none_target_falls_through_to_defaults(self, tmp_path, monkeypatch):
        monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
        result = find_config_file(None)
        assert result is None  # no defaults exist in tmp_path

    def test_xdg_config_home_first_default(self, tmp_path, monkeypatch):
        xdg = tmp_path / "xdgconfig"
        xdg.mkdir()
        monkeypatch.setenv("XDG_CONFIG_HOME", str(xdg))
        (xdg / "swaydm").mkdir()
        config_file = xdg / "swaydm" / "config.yaml"
        config_file.write_text("profiles: []")
        result = find_config_file("")
        assert result == config_file


# ---------------------------------------------------------------------------
# load_config
# ---------------------------------------------------------------------------


class TestLoadConfig:
    def test_none_path_returns_empty_config(self):
        result = load_config(None)
        assert isinstance(result, Config)
        assert result.profiles == []

    def test_missing_file_returns_empty_config(self, tmp_path):
        result = load_config(tmp_path / "does_not_exist.yaml")
        assert isinstance(result, Config)
        assert result.profiles == []

    def test_empty_yaml_returns_empty_config(self, tmp_path):
        f = tmp_path / "empty.yaml"
        f.write_text("")
        result = load_config(f)
        assert result.profiles == []

    def test_valid_yaml_returns_populated_config(self, tmp_path):
        yaml_content = textwrap.dedent("""\
            profiles:
              - name: home
                auto: true
                displays:
                  - name: "DP-1"
                    mode:
                      width: 1920
                      height: 1080
                      refresh: 60
                      scale: 1.0
                    position:
                      x: 0
                      y: 0
                commands: []
        """)
        f = tmp_path / "config.yaml"
        f.write_text(yaml_content)
        result = load_config(f)
        assert len(result.profiles) == 1
        assert result.profiles[0].name == "home"
        assert result.profiles[0].auto is True
        assert len(result.profiles[0].displays) == 1
        assert result.profiles[0].displays[0].name == "DP-1"
        assert result.profiles[0].displays[0].mode.width == 1920

    def test_multiple_profiles_loaded(self, tmp_path):
        yaml_content = textwrap.dedent("""\
            profiles:
              - name: home
                displays: []
              - name: office
                auto: false
                displays: []
        """)
        f = tmp_path / "config.yaml"
        f.write_text(yaml_content)
        result = load_config(f)
        assert len(result.profiles) == 2
        names = [p.name for p in result.profiles]
        assert "home" in names
        assert "office" in names

    def test_reserved_profile_name_raises(self, tmp_path):
        yaml_content = textwrap.dedent(f"""\
            profiles:
              - name: {FALLBACK}
        """)
        f = tmp_path / "config.yaml"
        f.write_text(yaml_content)
        with pytest.raises(ValueError, match="reserved"):
            load_config(f)

    def test_yaml_with_no_profiles_key_returns_empty(self, tmp_path):
        f = tmp_path / "config.yaml"
        f.write_text("some_other_key: value\n")
        result = load_config(f)
        assert result.profiles == []

    def test_profile_with_commands(self, tmp_path):
        yaml_content = textwrap.dedent("""\
            profiles:
              - name: gaming
                commands:
                  - "output DP-1 adaptive_sync on"
        """)
        f = tmp_path / "config.yaml"
        f.write_text(yaml_content)
        result = load_config(f)
        assert result.profiles[0].commands == ["output DP-1 adaptive_sync on"]
