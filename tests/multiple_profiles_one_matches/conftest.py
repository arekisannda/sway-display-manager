"""Scenario 7: multiple_profiles_one_matches — only home profile is valid."""

import pytest
from tests.conftest import FakeOutput, FakeMode, FakeRect
from swaydm.datatypes import Profile, Display, Mode, Position, Config


def _make_dell_output(connector: str, serial: str):
    mode = FakeMode(width=2560, height=1440, refresh=60000)
    return FakeOutput(
        name=connector,
        make="Dell",
        model="U2720Q",
        serial=serial,
        modes=[mode],
        current_mode=mode,
        rect=FakeRect(x=0, y=0),
        scale=1.0,
    )


@pytest.fixture
def output_home_a():
    return _make_dell_output("DP-1", "DELL01")


@pytest.fixture
def output_home_b():
    return _make_dell_output("DP-2", "DELL02")


@pytest.fixture
def profile_home(output_home_a, output_home_b):
    return Profile(
        name="home",
        auto=True,
        displays=[
            Display(
                name="Dell U2720Q DELL01",
                mode=Mode(width=2560, height=1440, refresh=60, scale=1.0),
                position=Position(x=0, y=0),
            ),
            Display(
                name="Dell U2720Q DELL02",
                mode=Mode(width=2560, height=1440, refresh=60, scale=1.0),
                position=Position(x=2560, y=0),
            ),
        ],
    )


@pytest.fixture
def profile_office():
    return Profile(
        name="office",
        auto=True,
        displays=[
            Display(
                name="HP Z24q HP001",  # not connected
                mode=Mode(width=2560, height=1440, refresh=60, scale=1.0),
                position=Position(x=0, y=0),
            ),
        ],
    )


@pytest.fixture
def profile_laptop():
    return Profile(
        name="laptop",
        auto=True,
        displays=[
            Display(
                name="DP-1",  # match by connector name
                mode=Mode(width=2560, height=1440, refresh=60, scale=1.0),
                position=Position(x=0, y=0),
            ),
        ],
    )


@pytest.fixture
def config_obj(profile_home, profile_office, profile_laptop):
    return Config(profiles=[profile_home, profile_office, profile_laptop])


@pytest.fixture
def outputs(output_home_a, output_home_b):
    return [output_home_a, output_home_b]
