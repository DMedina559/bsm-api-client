"""Exercise CLI command groups against an isolated real backend."""

import json

import pytest
from click.testing import CliRunner

from bsm_api_client import generated_adapter
from bsm_cli.__main__ import cli
from bsm_cli.config import Config


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
        ("player", "add", "-p", "CLI Test:987654321"),
        ("manager", "overview"),
        ("manager", "health"),
        ("manager", "monitor", "--once"),
        ("manager", "tasks", "list"),
        ("manager", "audit"),
        ("manager", "settings"),
        ("plugin", "settings", "show", "backup_on_start"),
        ("plugin", "list"),
        ("plugin", "reload"),
        ("plugin", "trigger-event", "cli_test_event"),
    ],
)
def test_cli_against_backend(server, tmp_path, monkeypatch, args):
    generated_operations = []
    operation_module = generated_adapter.operation_module

    def resolve_operation(operation_id):
        generated_operations.append(operation_id)
        return operation_module(operation_id)

    monkeypatch.setattr(generated_adapter, "operation_module", resolve_operation)
    monkeypatch.setattr("bsm_cli.config.get_config_path", lambda: tmp_path / "cli.json")
    config = Config()
    config.update(base_url=server, username="admin", password="password")
    result = CliRunner().invoke(cli, ["--json", *args])
    assert result.exit_code == 0, result.output
    assert json.loads(result.stdout) is not None
    assert not result.stderr
    expected_operation = {
        ("account", "details"): "get_account",
        ("account", "update-theme"): "update_account_theme",
        ("account", "update-profile"): "update_account_profile",
        ("users", "list"): "list_users",
        ("users", "invite"): "generate_registration_token",
        ("server", "list"): "list_servers",
        ("player", "scan"): "scan_players",
        ("player", "add"): "add_players",
        ("plugin", "list"): "list_plugins",
        ("plugin", "reload"): "reload_plugins",
        ("plugin", "trigger-event"): "trigger_plugin_event",
    }.get(args[:2])
    if expected_operation:
        assert expected_operation in generated_operations
        assert "login" in generated_operations
