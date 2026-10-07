"""Exercise the reported interactive login against the actual backend."""

import json

from bsm_cli.__main__ import cli
from click.testing import CliRunner


def test_interactive_cli_login(server, tmp_path, monkeypatch):
    config_path = tmp_path / "cli.json"
    monkeypatch.setattr("bsm_cli.config.get_config_path", lambda: config_path)
    result = CliRunner().invoke(
        cli, ["auth", "login"], input=f"{server}\nn\nadmin\npassword\n"
    )
    assert result.exit_code == 0, result.output
    assert "Login successful" in result.output
    saved = json.loads(config_path.read_text())
    assert saved["base_url"] == server
    assert saved["verify_ssl"] is False
    assert saved["jwt_token"]
    assert saved["password"] is None
