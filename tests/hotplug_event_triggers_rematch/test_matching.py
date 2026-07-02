"""Scenario 9: hotplug_event_triggers_rematch — tests."""

import swaydm.manager as manager_mod
from swaydm.manager import on_output_event


def test_on_output_event_updates_current_profile(fake_ipc, profile_obj):
    on_output_event(fake_ipc, None)
    assert manager_mod.mgr.current_profile == profile_obj.name


def test_on_output_event_issues_commands(fake_ipc):
    on_output_event(fake_ipc, None)
    assert len(fake_ipc.commands) > 0


def test_on_output_event_no_effect_when_auto_disabled(fake_ipc):
    manager_mod.mgr._auto = False
    original_profile = manager_mod.mgr.current_profile
    on_output_event(fake_ipc, None)
    assert manager_mod.mgr.current_profile == original_profile


def test_on_output_event_commands_not_called_when_auto_disabled(fake_ipc):
    manager_mod.mgr._auto = False
    on_output_event(fake_ipc, None)
    assert len(fake_ipc.commands) == 0


def test_output_set_updated_after_event(fake_ipc):
    on_output_event(fake_ipc, None)
    # After processing, manager should track DP-2 (the new connector)
    assert "DP-2" in manager_mod.mgr._output_set
