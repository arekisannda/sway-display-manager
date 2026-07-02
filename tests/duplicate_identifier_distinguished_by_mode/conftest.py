"""Scenario 3: duplicate_identifier_distinguished_by_mode — PBP ultrawide split."""

import pytest
from tests.conftest import FakeOutput, FakeMode, FakeRect
from swaydm.datatypes import Profile, Display, Mode, Position


@pytest.fixture
def output_side():
    mode = FakeMode(width=1760, height=1440, refresh=60000)
    return FakeOutput(
        name="DP-4",
        make="Samsung",
        model="LC49G95T",
        serial="H4ZR001",
        modes=[mode],
        current_mode=mode,
        rect=FakeRect(x=0, y=0),
        scale=1.0,
    )


@pytest.fixture
def output_main():
    mode = FakeMode(width=3360, height=1440, refresh=60000)
    return FakeOutput(
        name="DP-5",
        make="Samsung",
        model="LC49G95T",
        serial="H4ZR001",
        modes=[mode],
        current_mode=mode,
        rect=FakeRect(x=1760, y=0),
        scale=1.0,
    )


@pytest.fixture
def profile_obj():
    return Profile(
        name="ultrawide",
        auto=True,
        displays=[
            Display(
                name="Samsung LC49G95T H4ZR001",
                alias="SIDE",
                mode=Mode(width=1760, height=1440, refresh=60, scale=1.0),
                position=Position(x=0, y=0),
            ),
            Display(
                name="Samsung LC49G95T H4ZR001",
                alias="MAIN",
                mode=Mode(width=3360, height=1440, refresh=60, scale=1.0),
                position=Position(x=1760, y=0),
            ),
        ],
    )
