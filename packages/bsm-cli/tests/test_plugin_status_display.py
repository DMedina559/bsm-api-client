from bsm_api_client.models import PluginStatusesResponse
from bsm_cli.plugins import _print_plugin_table


def test_plugin_permissions_and_runtime_survive_typed_response(capsys):
    response = PluginStatusesResponse.model_validate(
        {
            "status": "success",
            "plugins": {
                "broken": {
                    "enabled": True,
                    "status": "ERROR",
                    "permissions": ["path:servers", "custom:future"],
                },
                "idle": {"enabled": False, "status": "DISABLED"},
            },
        }
    )
    assert response.plugins["broken"].permissions == ["path:servers", "custom:future"]
    assert not response.plugins["idle"].permissions
    _print_plugin_table(response.plugins)
    output = capsys.readouterr().out
    broken = next(line for line in output.splitlines() if "broken" in line)
    assert "Enabled" in broken and "ERROR" in broken
    assert "path:servers, custom:future" in broken
    assert "UNKNOWN" not in broken
