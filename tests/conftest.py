import sys
from dataclasses import dataclass, field
from typing import List, Optional
from unittest.mock import MagicMock

import pytest

from swaydm import utils

_i3ipc_mock = MagicMock()
sys.modules.setdefault('i3ipc', _i3ipc_mock)
sys.modules.setdefault('i3ipc.events', MagicMock())


@pytest.fixture(autouse=True, scope="session")
def init_logger():
    utils.setup("ERROR")


@dataclass
class FakeMode:
    width: int
    height: int
    refresh: int  # milliHz (i3ipc uses milliHz, e.g. 60000 for 60 Hz)


@dataclass
class FakeRect:
    x: int = 0
    y: int = 0


@dataclass
class FakeOutput:
    name: str
    make: str
    model: str
    serial: str
    modes: List[FakeMode]
    active: bool = True
    current_mode: Optional[FakeMode] = None
    rect: FakeRect = field(default_factory=FakeRect)
    scale: float = 1.0


@pytest.fixture
def make_output():
    def _factory(
        name="DP-1",
        manufacturer="ACME",
        model="Monitor1",
        serial="SN001",
        width=1920,
        height=1080,
        refresh=60,
        scale=1.0,
        extra_modes=None,
    ):
        primary = FakeMode(width=width, height=height, refresh=refresh * 1000)
        return FakeOutput(
            name=name,
            make=manufacturer,
            model=model,
            serial=serial,
            modes=[primary] + (extra_modes or []),
            current_mode=primary,
            rect=FakeRect(x=0, y=0),
            scale=scale,
        )

    return _factory


@pytest.fixture
def make_profile_display():
    def _factory(
        name,
        alias=None,
        width=1920,
        height=1080,
        refresh=60,
        scale=1.0,
        x=0,
        y=0,
    ):
        d = {"name": name}
        if alias is not None:
            d["alias"] = alias
        d["mode"] = {
            "width": width,
            "height": height,
            "refresh": refresh,
            "scale": scale,
        }
        d["position"] = {"x": x, "y": y}
        return d

    return _factory
