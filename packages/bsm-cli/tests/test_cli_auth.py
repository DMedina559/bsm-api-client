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
