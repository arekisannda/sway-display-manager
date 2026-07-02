"""Scenario 10: manual_switch_client_to_daemon — command_handler and IPC transport."""

import pytest
from tests.conftest import FakeOutput, FakeMode, FakeRect
from swaydm.datatypes import Profile, Display, Mode, Position, Config


class FakeIPC:
    def __init__(self, outputs):
        self._outputs = outputs
        self.commands = []

    def get_outputs(self):
        return self._outputs

    def command(self, cmd: str):
        self.commands.append(cmd)

    def on(self, event, handler):
        pass


@pytest.fixture
def output():
    mode = FakeMode(width=1920, height=1080, refresh=60000)
    return FakeOutput(
        name="DP-1",
        make="Philips",
        model="276E8V",
        serial="PH001",
        modes=[mode],
        current_mode=mode,
        rect=FakeRect(x=0, y=0),
        scale=1.0,
    )


@pytest.fixture
def profile_obj():
    return Profile(
        name="desk",
        auto=False,
        displays=[
            Display(
                name="Philips 276E8V PH001",
                mode=Mode(width=1920, height=1080, refresh=60, scale=1.0),
                position=Position(x=0, y=0),
            )
        ],
    )


@pytest.fixture
def config_obj(profile_obj):
    return Config(profiles=[profile_obj])


@pytest.fixture
def fake_ipc(output):
    return FakeIPC(outputs=[output])


@pytest.fixture(autouse=True)
def reset_manager(fake_ipc, config_obj):
    import swaydm.manager as manager_mod

    old_ipc = manager_mod.mgr.ipc
    old_config = manager_mod.mgr.config
    old_current_profile = manager_mod.mgr.current_profile
    old_auto = manager_mod.mgr._auto
    old_output_set = manager_mod.mgr._output_set.copy()
    old_profile_set = manager_mod.mgr._profile_set.copy()

    manager_mod.mgr.ipc = fake_ipc
    manager_mod.mgr.config = config_obj
    manager_mod.mgr._auto = True
    manager_mod.mgr._output_set = set()
    manager_mod.mgr.update_profile_map()

    yield

    manager_mod.mgr.ipc = old_ipc
    manager_mod.mgr.config = old_config
    manager_mod.mgr.current_profile = old_current_profile
    manager_mod.mgr._auto = old_auto
    manager_mod.mgr._output_set = old_output_set
    manager_mod.mgr._profile_set = old_profile_set
