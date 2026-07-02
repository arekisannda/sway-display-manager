"""Scenario 1: basic_single_match — single output matched by vendor identifier."""

import pytest
from tests.conftest import FakeOutput, FakeMode, FakeRect
from swaydm.datatypes import Profile, Display, Mode, Position


@pytest.fixture
def output():
    primary = FakeMode(width=2560, height=1440, refresh=60000)
    return FakeOutput(
        name="DP-1",
        make="Acme",
        model="XZ27",
        serial="ABC123",
        modes=[primary],
        current_mode=primary,
        rect=FakeRect(x=0, y=0),
        scale=1.0,
    )


@pytest.fixture
def profile_obj():
    return Profile(
        name="home",
        auto=True,
        displays=[
            Display(
                name="Acme XZ27 ABC123",
                mode=Mode(width=2560, height=1440, refresh=60, scale=1.0),
                position=Position(x=0, y=0),
            )
        ],
    )
