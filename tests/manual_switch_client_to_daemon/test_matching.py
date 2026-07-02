"""Scenario 10: manual_switch_client_to_daemon — tests."""

import socket
import time
import swaydm.manager as manager_mod
from swaydm.command import command_handler
from swaydm.code import Code
import swaydm.ipc as ipc_mod


def test_switch_profile_returns_ok(profile_obj):
    response = command_handler(f"switch_profile {profile_obj.name}")
    assert response.startswith(f"{Code.OK}\n")


def test_switch_profile_updates_current_profile(profile_obj):
    command_handler(f"switch_profile {profile_obj.name}")
    assert manager_mod.mgr.current_profile == profile_obj.name


def test_switch_nonexistent_profile_returns_error():
    response = command_handler("switch_profile nonexistent_profile")
    assert response.startswith(f"{Code.ERROR}\n")


def test_switch_nonexistent_profile_does_not_change_current():
    original = manager_mod.mgr.current_profile
    command_handler("switch_profile nonexistent_profile")
    assert manager_mod.mgr.current_profile == original


def test_unknown_command_returns_error():
    response = command_handler("bogus_command")
    assert response.startswith(f"{Code.ERROR}\n")


def test_socket_transport(tmp_path):
    """Start IPC server with a simple echo handler, send a message, check response."""
    sock_path = str(tmp_path / "test.sock")

    # Save and override global socket path
    old_socket = ipc_mod.mgr.socket
    ipc_mod.setup(sock_path)

    try:

        def echo_handler(msg: str) -> str:
            return f"{Code.OK}\necho:{msg}"

        ipc_mod.start_server(echo_handler)

        # Give the daemon thread a moment to start listening
        time.sleep(0.05)

        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(sock_path)
        client.sendall(b"hello")
        client.shutdown(socket.SHUT_WR)
        raw = client.recv(4096).decode()
        client.close()

        resp_code, body = ipc_mod.parse_response(raw)
        assert resp_code is Code.OK
        assert "echo:hello" in body
    finally:
        ipc_mod.setup(old_socket)


def test_socket_transport_error_response(tmp_path):
    """Server returns an ERROR code; parse_response should decode it correctly."""

    sock_path = str(tmp_path / "err.sock")
    old_socket = ipc_mod.mgr.socket
    ipc_mod.setup(sock_path)

    try:

        def error_handler(_msg: str) -> str:
            return f"{Code.ERROR}\nbad input"

        ipc_mod.start_server(error_handler)
        time.sleep(0.05)

        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        client.connect(sock_path)
        client.sendall(b"garbage")
        client.shutdown(socket.SHUT_WR)
        raw = client.recv(4096).decode()
        client.close()

        resp_code, body = ipc_mod.parse_response(raw)
        assert resp_code is Code.ERROR
        assert "bad input" in body
    finally:
        ipc_mod.setup(old_socket)
