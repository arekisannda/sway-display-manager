"""Scenario 6: no_matching_output_for_display — missing monitor causes fallback."""

import pytest
from tests.conftest import FakeOutput, FakeMode, FakeRect
from swaydm.datatypes import Profile, Display, Mode, Position, Config


@pytest.fixture
def connected_output():
    mode = FakeMode(width=1920, height=1080, refresh=60000)
    return FakeOutput(
        name="DP-1",
        make="HP",
        model="Z27k",
        serial="HP001",
        modes=[mode],
        current_mode=mode,
        rect=FakeRect(x=0, y=0),
        scale=1.0,
    )


@pytest.fixture
def profile_obj():
    return Profile(
        name="dual",
        auto=True,
        displays=[
            Display(
                name="HP Z27k HP001",
                mode=Mode(width=1920, height=1080, refresh=60, scale=1.0),
                position=Position(x=0, y=0),
            ),
            Display(
                name="HP Z27k HP999",  # different serial — not connected
                mode=Mode(width=1920, height=1080, refresh=60, scale=1.0),
                position=Position(x=1920, y=0),
            ),
        ],
    )


@pytest.fixture
def config_obj(profile_obj):
    return Config(profiles=[profile_obj])
