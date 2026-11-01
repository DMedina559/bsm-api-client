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
        ("auth", "whoami"),
        ("api", "call", "update_account_theme", "--json", '{"theme":"default"}'),
        (
            "api",
            "call",
            "update_account_profile",
            "--json",
            '{"full_name":"CLI Test","email":"cli@example.com"}',
        ),
        ("api", "call", "list_users"),
        ("api", "call", "generate_registration_token", "--json", '{"role":"user"}'),
        ("server", "list"),
        ("player", "scan"),
        ("player", "add", "-p", "CLI Test:987654321"),
        ("overview",),
        ("health",),
        ("monitor", "--once"),
        ("operations", "list"),
        ("audit",),
        ("settings",),
        ("plugin", "settings", "show", "backup_on_start"),
        ("plugin", "list"),
        ("plugin", "reload"),
        (
            "api",
            "call",
            "trigger_plugin_event",
            "--json",
            '{"event_name":"cli_test_event"}',
        ),
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
    config.update(
        base_url=server, username="admin", password="integration secure passphrase"
    )
    result = CliRunner().invoke(cli, ["--json", *args])
    assert result.exit_code == 0, result.output
    assert json.loads(result.stdout) is not None
    assert not result.stderr
    expected_operation = {
        ("auth", "whoami"): "get_account",
        ("server", "list"): "list_servers",
        ("player", "scan"): "scan_players",
        ("player", "add"): "add_players",
        ("plugin", "list"): "list_plugins",
        ("plugin", "reload"): "reload_plugins",
    }.get(args[:2])
    if expected_operation:
        assert expected_operation in generated_operations
        assert "login" in generated_operations
