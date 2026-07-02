"""Scenario 2: connector_name_changed — profile matches by vendor id regardless of connector."""

import pytest
from tests.conftest import FakeOutput, FakeMode, FakeRect
from swaydm.datatypes import Profile, Display, Mode, Position


def _make_dell_output(connector_name: str):
    primary = FakeMode(width=1920, height=1080, refresh=60000)
    return FakeOutput(
        name=connector_name,
        make="Dell",
        model="U2720Q",
        serial="XYZ999",
        modes=[primary],
        current_mode=primary,
        rect=FakeRect(x=0, y=0),
        scale=1.0,
    )


@pytest.fixture
def output_old_name():
    return _make_dell_output("DP-1")


@pytest.fixture
def output_new_name():
    return _make_dell_output("DP-3")


@pytest.fixture
def profile_obj():
    return Profile(
        name="work",
        auto=True,
        displays=[
            Display(
                name="Dell U2720Q XYZ999",
                mode=Mode(width=1920, height=1080, refresh=60, scale=1.0),
                position=Position(x=0, y=0),
            )
        ],
    )
