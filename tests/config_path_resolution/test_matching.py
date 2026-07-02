"""Scenario 11: config_path_resolution — find_config_file path resolution tests."""

from swaydm.config import find_config_file


def test_explicit_existing_path_returned_directly(tmp_path, monkeypatch):
    """An explicit path that exists is returned without checking defaults."""
    config_file = tmp_path / "custom.yaml"
    config_file.write_text("profiles: []")
    # Point XDG to a location with no defaults
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "xdg_empty"))
    result = find_config_file(str(config_file))
    assert result == config_file


def test_explicit_nonexistent_falls_through_to_first_default(
    tmp_path, monkeypatch
):
    """When explicit path doesn't exist, first XDG default is tried."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    swaydm_dir = tmp_path / "swaydm"
    swaydm_dir.mkdir()
    first_default = swaydm_dir / "config.yaml"
    first_default.write_text("profiles: []")

    result = find_config_file(str(tmp_path / "does_not_exist.yaml"))
    assert result == first_default


def test_explicit_nonexistent_no_defaults_returns_none(tmp_path, monkeypatch):
    """When explicit path doesn't exist and no defaults exist, returns None."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "nonexistent_xdg"))
    result = find_config_file(str(tmp_path / "nonexistent.yaml"))
    assert result is None


def test_first_xdg_default_wins_when_both_exist(tmp_path, monkeypatch):
    """$XDG_CONFIG_HOME/swaydm/config.yaml takes priority over swaydm.yaml."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    swaydm_dir = tmp_path / "swaydm"
    swaydm_dir.mkdir()
    first_default = swaydm_dir / "config.yaml"
    first_default.write_text("profiles: []")
    second_default = tmp_path / "swaydm.yaml"
    second_default.write_text("profiles: []")

    result = find_config_file("")
    assert result == first_default


def test_second_xdg_default_used_when_first_absent(tmp_path, monkeypatch):
    """$XDG_CONFIG_HOME/swaydm.yaml is used when swaydm/config.yaml is absent."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    second_default = tmp_path / "swaydm.yaml"
    second_default.write_text("profiles: []")

    result = find_config_file("")
    assert result == second_default


def test_no_config_anywhere_returns_none(tmp_path, monkeypatch):
    """When no files exist, returns None."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "empty"))
    result = find_config_file("")
    assert result is None


def test_none_target_uses_defaults(tmp_path, monkeypatch):
    """None target skips explicit check and goes straight to defaults."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path))
    swaydm_dir = tmp_path / "swaydm"
    swaydm_dir.mkdir()
    default_file = swaydm_dir / "config.yaml"
    default_file.write_text("profiles: []")

    result = find_config_file(None)
    assert result == default_file


def test_none_target_returns_none_when_no_defaults(tmp_path, monkeypatch):
    """None target with no defaults returns None."""
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "empty"))
    result = find_config_file(None)
    assert result is None


def test_first_default_swaydm_config_yaml(tmp_path, monkeypatch):
    """Verify the exact path $XDG_CONFIG_HOME/swaydm/config.yaml is the first default."""
    xdg = tmp_path / "myconfig"
    xdg.mkdir()
    monkeypatch.setenv("XDG_CONFIG_HOME", str(xdg))
    swaydm_dir = xdg / "swaydm"
    swaydm_dir.mkdir()
    config_file = swaydm_dir / "config.yaml"
    config_file.write_text("profiles: []")

    result = find_config_file("")
    assert result == config_file


def test_second_default_swaydm_yaml(tmp_path, monkeypatch):
    """Verify the exact path $XDG_CONFIG_HOME/swaydm.yaml is the second default."""
    xdg = tmp_path / "myconfig"
    xdg.mkdir()
    monkeypatch.setenv("XDG_CONFIG_HOME", str(xdg))
    # Only second default exists
    config_file = xdg / "swaydm.yaml"
    config_file.write_text("profiles: []")

    result = find_config_file("")
    assert result == config_file
