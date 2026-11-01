"""Authentication changes are persisted only after a successful login."""

import json
from unittest.mock import AsyncMock

import pytest
from click.testing import CliRunner

from bsm_api_client import AuthError
from bsm_api_client.models import TokenResponse
from bsm_cli.__main__ import cli
from bsm_cli.config import Config


@pytest.fixture
def auth_config(tmp_path, monkeypatch):
    path = tmp_path / "config.json"
    monkeypatch.setattr("bsm_cli.config.get_config_path", lambda: path)
    config = Config()
    config.update(
        base_url="http://old-server",
        jwt_token="old-token",
        username="old-user",
        password="old-password",
    )
    return config, path


@pytest.mark.parametrize("remember_me", [False, True])
@pytest.mark.parametrize("success", [True, False])
def test_login_commits_destination_and_token_together(
    auth_config, monkeypatch, success, remember_me
):
    config, path = auth_config
    monkeypatch.setattr("bsm_cli.__main__.Config", lambda: config)
    client = AsyncMock()
    client.__aenter__.return_value = client
    client.authenticate.return_value = TokenResponse(
        access_token="new-token", token_type="bearer"
    )
    if not success:
        client.authenticate.side_effect = AuthError("Bad credentials")
    supplied = {}

    def create(**kwargs):
        supplied.update(kwargs)
        return client

    monkeypatch.setattr("bsm_cli.auth.BedrockServerManagerApi", create)
    result = CliRunner().invoke(
        cli,
        [
            "--json",
            "auth",
            "login",
            "--base-url",
            "new-server",
            "--no-verify-ssl",
            "--username",
            "new-user",
            "--password",
            "new-password",
        ]
        + (["--remember-me"] if remember_me else []),
    )
    saved = json.loads(path.read_text())
    assert supplied["remember_me"] is remember_me
    assert result.exit_code == (0 if success else 3), result.output
    assert saved["base_url"] == (
        "http://new-server" if success else "http://old-server"
    )
    assert saved["jwt_token"] == ("new-token" if success else "old-token")
    assert saved["password"] == (None if success else "old-password")
    client.__aexit__.assert_awaited_once()


def test_logout_clears_credentials_that_would_automatically_login_again(
    auth_config, monkeypatch
):
    config, path = auth_config
    monkeypatch.setattr("bsm_cli.__main__.Config", lambda: config)
    client = AsyncMock()
    client.__aenter__.return_value = client
    monkeypatch.setattr("bsm_cli.auth.BedrockServerManagerApi", lambda **kw: client)
    monkeypatch.setattr("bsm_cli.__main__.BedrockServerManagerApi", lambda **kw: client)
    result = CliRunner().invoke(cli, ["--json", "auth", "logout"])
    client.async_logout.assert_awaited_once()
    assert result.exit_code == 0, result.output
    saved = json.loads(path.read_text())
    assert all(saved[key] is None for key in ("jwt_token", "username", "password"))


def test_config_file_is_owner_only_and_replaced_atomically(auth_config):
    import os
    import stat

    config, path = auth_config
    config.update(jwt_token="new-token")
    assert json.loads(path.read_text())["jwt_token"] == "new-token"
    if os.name == "posix":
        assert stat.S_IMODE(path.stat().st_mode) == 0o600
    assert list(path.parent.glob(f".{path.name}.*")) == []


@pytest.mark.asyncio
@pytest.mark.parametrize("remember_me", [False, True])
async def test_interactive_login_offers_remember_me(
    auth_config, monkeypatch, remember_me
):
    import click

    from bsm_cli.auth import auth, interactive_login

    config, _ = auth_config
    login = AsyncMock()
    monkeypatch.setattr("bsm_cli.auth._login", login)
    prompts = []

    def confirm(message, default):
        prompts.append(default)
        return remember_me

    monkeypatch.setattr("bsm_cli.auth.click.confirm", confirm)
    context = click.Context(auth, obj={"config": config})
    await interactive_login(context)
    assert prompts == [False]
    login.assert_awaited_once_with(
        context, config.base_url, None, None, config.verify_ssl, None, remember_me
    )


def test_remembered_device_is_account_destination_and_expiry_scoped(auth_config):
    import time

    config, _ = auth_config
    config.update(
        trusted_device_owner="owner",
        trusted_device_backend="https://one.example",
        trusted_device_token="bsm_td_proof",
        trusted_device_expires_at=int(time.time()) + 1000,
        active_username="owner",
    )
    assert config.trusted_device("owner", "https://one.example/") == "bsm_td_proof"
    assert config.trusted_device("other", "https://one.example") is None
    assert config.trusted_device("owner", "https://two.example") is None
    config.update(trusted_device_expires_at=1)
    assert config.trusted_device("owner", "https://one.example") is None


def test_login_remember_device_saves_grant_without_printing_it(
    auth_config, monkeypatch
):
    config, path = auth_config
    monkeypatch.setattr("bsm_cli.__main__.Config", lambda: config)
    client = AsyncMock()
    client.__aenter__.return_value = client
    client.authenticate.return_value = TokenResponse(
        access_token="session",
        token_type="bearer",
        trusted_device_token="bsm_td_private-device-proof",
        trusted_device_expires_at=2000000000,
    )
    supplied = {}

    def create(**kwargs):
        supplied.update(kwargs)
        return client

    monkeypatch.setattr("bsm_cli.auth.BedrockServerManagerApi", create)
    result = CliRunner().invoke(
        cli,
        [
            "--json",
            "auth",
            "login",
            "--base-url",
            "https://manager.example",
            "--no-verify-ssl",
            "--username",
            "owner",
            "--password",
            "password",
            "--otp",
            "recovery-code",
            "--remember-device",
        ],
    )
    assert result.exit_code == 0, result.output
    assert supplied["remember_device"] is True
    saved = json.loads(path.read_text())
    assert saved["trusted_device_token"] == "bsm_td_private-device-proof"
    assert saved["trusted_device_owner"] == "owner"
    assert saved["active_username"] == "owner"
    assert saved["password"] is None
    assert "bsm_td_private-device-proof" not in result.output
    assert "recovery-code" not in path.read_text()


def test_remembering_reauthentication_uses_authenticated_account_not_stale_label(
    auth_config, monkeypatch
):
    config, path = auth_config
    config.update(active_username="previous-owner")
    monkeypatch.setattr("bsm_cli.__main__.Config", lambda: config)
    client = AsyncMock()
    proof = "bsm_td_" + "a" * 32 + "." + "s" * 43

    async def operation(name, **kwargs):
        if name == "get_account":
            return {"username": "current-owner"}
        assert name == "verify_account_security"
        return {
            "verified_until": 2000000000,
            "trusted_device_token": proof,
            "trusted_device_expires_at": 2000000000,
        }

    client.async_call_operation.side_effect = operation
    monkeypatch.setattr(
        "bsm_cli.__main__.BedrockServerManagerApi", lambda **kwargs: client
    )
    result = CliRunner().invoke(
        cli,
        [
            "--json",
            "auth",
            "verify",
            "--password",
            "password",
            "--otp",
            "one-use-code",
            "--remember-device",
        ],
    )
    assert result.exit_code == 0, result.output
    saved = json.loads(path.read_text())
    assert saved["trusted_device_owner"] == saved["active_username"] == "current-owner"
    assert proof not in result.output and "one-use-code" not in path.read_text()
    assert client.async_call_operation.await_args_list[0].args == ("get_account",)


def test_setup_replaces_active_username_when_switching_installations(
    auth_config, monkeypatch
):
    config, path = auth_config
    config.update(active_username="previous-owner")
    monkeypatch.setattr("bsm_cli.__main__.Config", lambda: config)
    client = AsyncMock()
    client.__aenter__.return_value = client
    client.application.async_get_setup_status.return_value.needs_setup = True
    client.application.async_create_first_user.return_value = TokenResponse(
        access_token="new-session", token_type="bearer"
    )
    monkeypatch.setattr(
        "bsm_cli.auth.BedrockServerManagerApi", lambda *args, **kwargs: client
    )
    result = CliRunner().invoke(
        cli,
        [
            "--json",
            "auth",
            "setup",
            "--base-url",
            "https://new.example",
            "--username",
            "new-owner",
            "--password",
            "Otter42!",
        ],
    )
    assert result.exit_code == 0, result.output
    saved = json.loads(path.read_text())
    assert (
        saved["active_username"] == "new-owner"
        and saved["base_url"] == "https://new.example"
    )
    assert "Otter42!" not in path.read_text()


def test_environment_credential_override_does_not_send_saved_owner_proof(
    auth_config, monkeypatch
):
    config, _ = auth_config
    config.update(
        active_username="owner",
        trusted_device_owner="owner",
        trusted_device_backend=config.base_url,
        trusted_device_token="bsm_td_proof",
        trusted_device_expires_at=2000000000,
    )
    assert config.trusted_device() == "bsm_td_proof"
    monkeypatch.setenv("BSM_JWT_TOKEN", "another-account-session")
    assert config.trusted_device() is None
    assert config.trusted_device("owner", config.base_url) == "bsm_td_proof"


def test_token_history_flags_are_sent_to_backend(auth_config, monkeypatch):
    config, _ = auth_config
    monkeypatch.setattr("bsm_cli.__main__.Config", lambda: config)
    client = AsyncMock()
    client.async_call_operation.return_value = []
    monkeypatch.setattr(
        "bsm_cli.__main__.BedrockServerManagerApi", lambda **kwargs: client
    )
    result = CliRunner().invoke(
        cli,
        [
            "--json",
            "auth",
            "tokens",
            "list",
            "--limit",
            "50",
            "--offset",
            "100",
            "--status",
            "inactive",
        ],
    )
    assert result.exit_code == 0, result.output
    client.async_call_operation.assert_awaited_once_with(
        "list_integration_tokens",
        query={"limit": 50, "offset": 100, "status": "inactive"},
    )


def test_device_forget_modes_are_explicit(auth_config, monkeypatch):
    config, _ = auth_config
    monkeypatch.setattr("bsm_cli.__main__.Config", lambda: config)
    client = AsyncMock()
    client.async_call_operation.return_value = {"status": "success"}
    monkeypatch.setattr(
        "bsm_cli.__main__.BedrockServerManagerApi", lambda **kwargs: client
    )
    result = CliRunner().invoke(
        cli, ["--json", "auth", "devices", "forget", "--all", "--others"]
    )
    assert result.exit_code == 2
    client.async_call_operation.assert_not_awaited()
    result = CliRunner().invoke(
        cli, ["--json", "auth", "devices", "forget", "--others"]
    )
    assert result.exit_code == 0, result.output
    client.async_call_operation.assert_awaited_once_with(
        "revoke_trusted_devices", json_data={"mode": "others"}
    )


def test_passkey_and_admin_mfa_commands_call_expected_operations(
    auth_config, monkeypatch
):
    config, _ = auth_config
    monkeypatch.setattr("bsm_cli.__main__.Config", lambda: config)
    client = AsyncMock()
    client.async_call_operation.return_value = []
    monkeypatch.setattr(
        "bsm_cli.__main__.BedrockServerManagerApi", lambda **kwargs: client
    )
    result = CliRunner().invoke(cli, ["--json", "auth", "passkeys", "list"])
    assert result.exit_code == 0, result.output
    client.async_call_operation.assert_awaited_once_with("list_passkeys")

    client.async_call_operation.reset_mock()
    client.async_call_operation.return_value = {"status": "success"}
    result = CliRunner().invoke(
        cli, ["--json", "auth", "passkeys", "rename", "pk-1", "YubiKey"]
    )
    assert result.exit_code == 0, result.output
    client.async_call_operation.assert_awaited_once_with(
        "rename_passkey",
        path_params={"passkey_id": "pk-1"},
        json_data={"name": "YubiKey"},
    )

    client.async_call_operation.reset_mock()
    result = CliRunner().invoke(cli, ["--json", "auth", "passkeys", "revoke", "pk-1"])
    assert result.exit_code == 0, result.output
    client.async_call_operation.assert_awaited_once_with(
        "revoke_passkey", path_params={"passkey_id": "pk-1"}
    )

    client.async_call_operation.reset_mock()
    client.async_call_operation.return_value = []
    result = CliRunner().invoke(cli, ["--json", "access", "passkeys", "2"])
    assert result.exit_code == 0, result.output
    client.async_call_operation.assert_awaited_once_with(
        "list_account_passkeys", path_params={"user_id": 2}
    )

    client.async_call_operation.reset_mock()
    client.async_call_operation.return_value = {"status": "success"}
    result = CliRunner().invoke(cli, ["--json", "access", "reset-mfa", "2", "--yes"])
    assert result.exit_code == 0, result.output
    client.async_call_operation.assert_awaited_once_with(
        "reset_account_mfa", path_params={"user_id": 2}
    )
