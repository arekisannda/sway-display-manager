"""Scenario 5: declaration_order_pairing — tests."""

from swaydm.profile import get_profile_output_mapping


def test_display0_paired_with_output_x(outputs, profile_obj):
    result = get_profile_output_mapping(profile_obj, outputs)
    by_name = {r.name: r for r in result}
    assert "DP-1" in by_name
    assert by_name["DP-1"].active is True
    assert by_name["DP-1"].position.x == 0


def test_display1_paired_with_output_y(outputs, profile_obj):
    result = get_profile_output_mapping(profile_obj, outputs)
    by_name = {r.name: r for r in result}
    assert "DP-2" in by_name
    assert by_name["DP-2"].active is True
    assert by_name["DP-2"].position.x == 3840


def test_output_x_not_assigned_to_display1(outputs, profile_obj):
    result = get_profile_output_mapping(profile_obj, outputs)
    by_name = {r.name: r for r in result}
    # DP-1 must not have BenQ's position
    assert by_name["DP-1"].position.x != 3840


def test_both_outputs_active(outputs, profile_obj):
    result = get_profile_output_mapping(profile_obj, outputs)
    assert all(r.active for r in result)


def test_result_has_two_entries(outputs, profile_obj):
    result = get_profile_output_mapping(profile_obj, outputs)
    assert len(result) == 2
