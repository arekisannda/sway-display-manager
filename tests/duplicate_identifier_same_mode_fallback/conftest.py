"""Scenario 4: duplicate_identifier_same_mode_fallback — assignment by outputs list order."""

import pytest
from tests.conftest import FakeOutput, FakeMode, FakeRect
from swaydm.datatypes import Profile, Display, Mode, Position


def _make_output(connector: str):
    mode = FakeMode(width=1920, height=1080, refresh=60000)
    return FakeOutput(
        name=connector,
        make="Samsung",
        model="LC49G95T",
        serial="SAME001",
        modes=[mode],
        current_mode=mode,
        rect=FakeRect(x=0, y=0),
        scale=1.0,
    )


@pytest.fixture
def output_a():
    return _make_output("DP-6")


@pytest.fixture
def output_b():
    return _make_output("DP-7")


@pytest.fixture
def profile_obj():
    return Profile(
        name="twin",
        auto=True,
        displays=[
            Display(
                name="Samsung LC49G95T SAME001",
                alias="FIRST",
                mode=Mode(width=1920, height=1080, refresh=60, scale=1.0),
                position=Position(x=0, y=0),
            ),
            Display(
                name="Samsung LC49G95T SAME001",
                alias="SECOND",
                mode=Mode(width=1920, height=1080, refresh=60, scale=1.0),
                position=Position(x=1920, y=0),
            ),
        ],
    )


@pytest.fixture
def outputs(output_a, output_b):
    return [output_a, output_b]
