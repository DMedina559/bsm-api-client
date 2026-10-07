"""Exercise CLI command groups against an isolated real backend."""

import json

import pytest
from bsm_cli.__main__ import cli
from bsm_cli.config import Config
from click.testing import CliRunner


@pytest.mark.parametrize(
    "args",
    [
        ("api", "info"),
        ("api", "operations"),
        ("api", "schema"),
        ("api", "diff"),
        ("api", "refresh"),
        ("account", "details"),
        ("account", "update-theme", "--theme", "default"),
        (
            "account",
            "update-profile",
            "--full-name",
            "CLI Test",
            "--email",
            "cli@example.com",
        ),
        ("users", "list"),
        ("users", "invite", "user"),
        ("server", "list"),
        ("player", "scan"),
        ("player", "add", "-p", "CLI Test:123456789"),
        ("plugin", "list"),
        ("plugin", "reload"),
        ("plugin", "trigger-event", "cli_test_event"),
    ],
)
def test_cli_against_backend(server, tmp_path, monkeypatch, args):
    monkeypatch.setattr("bsm_cli.config.get_config_path", lambda: tmp_path / "cli.json")
    config = Config()
    config.update(base_url=server, username="admin", password="password")
    result = CliRunner().invoke(cli, ["--json", *args])
    assert result.exit_code == 0, result.output
    assert json.loads(result.stdout) is not None
    assert not result.stderr
