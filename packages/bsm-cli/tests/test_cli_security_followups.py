"""Challenge-driven terminal authentication and credential-file ownership."""

import stat
from unittest.mock import AsyncMock

import click
import pytest

from bsm_api_client.exceptions import AuthError
from bsm_api_client.models import TokenResponse
from bsm_cli.__main__ import cli
from bsm_cli.auth import _login
from bsm_cli.config import Config, load_config, save_config


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "interactive,json_output,expected_calls",
    [(True, False, 2), (False, False, 1), (True, True, 1)],
)
async def test_login_prompts_only_after_mfa_challenge(
    tmp_path, monkeypatch, interactive, json_output, expected_calls
):
    monkeypatch.setattr("bsm_cli.config.get_config_path", lambda: tmp_path / "cli.json")
    config = Config()
    client = AsyncMock()
    client.__aenter__.return_value = client
    challenge = AuthError(
        "Factor required", status_code=401, response_headers={"X-BSM-MFA": "required"}
    )
    client.authenticate.side_effect = [
        challenge,
        TokenResponse(access_token="new-token"),
    ]
    monkeypatch.setattr("bsm_cli.auth.BedrockServerManagerApi", lambda **kwargs: client)
    monkeypatch.setattr("bsm_cli.auth.sys.stdin.isatty", lambda: interactive)
    prompt = []
    monkeypatch.setattr(
        "bsm_cli.auth.click.prompt",
        lambda *args, **kwargs: prompt.append(kwargs) or "123456",
    )
    ctx = click.Context(
        click.Command("test"), obj={"config": config, "json_output": json_output}
    )
    if expected_calls == 1:
        with pytest.raises(AuthError):
            await _login(ctx, "http://localhost", "user", "password", True, None)
        assert prompt == []
        assert config.jwt_token is None
    else:
        await _login(ctx, "http://localhost", "user", "password", True, None)
        assert prompt == [{"hide_input": True}]
        assert config.jwt_token == "new-token"
    assert client.authenticate.await_count == expected_calls


def test_config_rejects_symlinks_and_keeps_owner_permissions(tmp_path, monkeypatch):
    config_path = tmp_path / "config.json"
    monkeypatch.setattr("bsm_cli.config.get_config_path", lambda: config_path)
    save_config({"jwt_token": "synthetic-secret"})
    import os

    if os.name != "nt":
        assert stat.S_IMODE(config_path.stat().st_mode) == 0o600
    target = tmp_path / "target.json"
    target.write_text("{}")
    config_path.unlink()
    try:
        config_path.symlink_to(target)
    except OSError:
        pytest.skip("Symlinks unavailable on this host")
    with pytest.raises(OSError, match="symbolic link"):
        save_config({"jwt_token": "must-not-write"})
    with pytest.raises(OSError, match="symbolic link"):
        load_config()
    assert target.read_text() == "{}"


def test_normal_help_focuses_on_workflows_and_api_escape_hatch():
    # Formatting help needs no configured backend or network access.
    ctx = click.Context(cli)
    help_text = cli.get_help(ctx)
    for name in ("server", "backup", "scheduler", "api", "auth"):
        assert name in help_text
    assert "access " not in help_text
    assert "passkeys" not in cli.commands["auth"].get_help(
        click.Context(cli.commands["auth"])
    )
    assert "whoami" in cli.commands["auth"].commands
    assert "change-password" in cli.commands["auth"].commands
    # Redundant commands are removed, while the generic API remains available.
    assert "passkeys" not in cli.commands["auth"].commands
    for removed in ("account", "users", "access", "runtime", "events"):
        assert removed not in cli.commands
    assert "call" in cli.commands["api"].commands


def test_windows_credentials_use_protected_dacl(tmp_path, monkeypatch):
    import sys
    from types import SimpleNamespace
    from unittest.mock import Mock

    from bsm_cli import config as module

    token = Mock()
    acl = Mock()
    security = SimpleNamespace(
        OpenProcessToken=Mock(return_value=token),
        GetTokenInformation=Mock(return_value=("owner",)),
        TokenUser=1,
        ACL=Mock(return_value=acl),
        CreateWellKnownSid=Mock(side_effect=["admins", "system"]),
        WinBuiltinAdministratorsSid=2,
        WinLocalSystemSid=3,
        ACL_REVISION=4,
        SE_FILE_OBJECT=5,
        DACL_SECURITY_INFORMATION=8,
        PROTECTED_DACL_SECURITY_INFORMATION=16,
        SetNamedSecurityInfo=Mock(),
    )
    monkeypatch.setattr(module, "os", SimpleNamespace(name="nt"))
    monkeypatch.setitem(sys.modules, "win32security", security)
    monkeypatch.setitem(
        sys.modules, "win32api", SimpleNamespace(GetCurrentProcess=lambda: 1)
    )
    monkeypatch.setitem(sys.modules, "win32con", SimpleNamespace(TOKEN_QUERY=1))
    monkeypatch.setitem(
        sys.modules, "ntsecuritycon", SimpleNamespace(FILE_ALL_ACCESS=99)
    )
    path = tmp_path / "private.json"
    path.write_text("{}")
    module.protect_config(path)
    assert acl.AddAccessAllowedAceEx.call_count == 3
    security.SetNamedSecurityInfo.assert_called_once_with(
        str(path), 5, 24, None, None, acl, None
    )
    token.Close.assert_called_once()
