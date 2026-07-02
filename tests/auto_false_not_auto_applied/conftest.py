"""Scenario 8: auto_false_not_auto_applied — manual profiles excluded from auto-matching."""

import pytest
from tests.conftest import FakeOutput, FakeMode, FakeRect
from swaydm.datatypes import Profile, Display, Mode, Position, Config


@pytest.fixture
def output():
    mode = FakeMode(width=1920, height=1080, refresh=60000)
    return FakeOutput(
        name="DP-1",
        make="Acer",
        model="XB271HU",
        serial="AC001",
        modes=[mode],
        current_mode=mode,
        rect=FakeRect(x=0, y=0),
        scale=1.0,
    )


@pytest.fixture
def profile_auto():
    return Profile(
        name="gaming_auto",
        auto=True,
        displays=[
            Display(
                name="Acer XB271HU AC001",
                mode=Mode(width=1920, height=1080, refresh=60, scale=1.0),
                position=Position(x=0, y=0),
            )
        ],
    )


@pytest.fixture
def profile_manual():
    return Profile(
        name="gaming_manual",
        auto=False,
        displays=[
            Display(
                name="Acer XB271HU AC001",
                mode=Mode(width=1920, height=1080, refresh=60, scale=1.0),
                position=Position(x=0, y=0),
            )
        ],
    )


@pytest.fixture
def config_obj(profile_auto, profile_manual):
    return Config(profiles=[profile_auto, profile_manual])


@pytest.fixture
def outputs(output):
    return [output]
