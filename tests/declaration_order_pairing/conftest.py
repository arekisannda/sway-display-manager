"""Scenario 5: declaration_order_pairing — claimed outputs cannot be reused."""

import pytest
from tests.conftest import FakeOutput, FakeMode, FakeRect
from swaydm.datatypes import Profile, Display, Mode, Position


@pytest.fixture
def output_x():
    mode = FakeMode(width=3840, height=2160, refresh=60000)
    return FakeOutput(
        name="DP-1",
        make="LG",
        model="27UK850",
        serial="LG001",
        modes=[mode],
        current_mode=mode,
        rect=FakeRect(x=0, y=0),
        scale=1.0,
    )


@pytest.fixture
def output_y():
    mode = FakeMode(width=3840, height=2160, refresh=60000)
    return FakeOutput(
        name="DP-2",
        make="BenQ",
        model="EW3270U",
        serial="BQ001",
        modes=[mode],
        current_mode=mode,
        rect=FakeRect(x=3840, y=0),
        scale=1.0,
    )


@pytest.fixture
def profile_obj():
    return Profile(
        name="dual4k",
        auto=True,
        displays=[
            Display(
                name="LG 27UK850 LG001",
                mode=Mode(width=3840, height=2160, refresh=60, scale=1.0),
                position=Position(x=0, y=0),
            ),
            Display(
                name="BenQ EW3270U BQ001",
                mode=Mode(width=3840, height=2160, refresh=60, scale=1.0),
                position=Position(x=3840, y=0),
            ),
        ],
    )


@pytest.fixture
def outputs(output_x, output_y):
    return [output_x, output_y]
