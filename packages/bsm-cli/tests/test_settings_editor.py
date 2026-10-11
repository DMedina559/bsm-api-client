"""Settings editing preserves cancellation, secrets, and server choices."""

from unittest.mock import AsyncMock

import pytest

from bsm_cli.settings_editor import display, edit_settings, prompt_value


class Answer:
    def __init__(self, value):
        self.value = value

    async def ask_async(self):
        return self.value


@pytest.mark.asyncio
async def test_editor_reviews_changes_before_saving(monkeypatch, capsys):
    selections = iter([("enabled",), "save"])
    confirmations = iter([True, True])
    monkeypatch.setattr("questionary.select", lambda *a, **k: Answer(next(selections)))
    monkeypatch.setattr(
        "questionary.confirm", lambda *a, **k: Answer(next(confirmations))
    )
    original = {"enabled": False}
    draft = await edit_settings(original)
    assert original == {"enabled": False}
    assert draft == {"enabled": True}
    assert "false → true" in capsys.readouterr().out


@pytest.mark.asyncio
async def test_editor_cancel_never_mutates_input(monkeypatch):
    monkeypatch.setattr("questionary.select", lambda *a, **k: Answer(None))
    original = {"servers": ["alpha"]}
    assert await edit_settings(original) is None
    assert original == {"servers": ["alpha"]}


@pytest.mark.asyncio
async def test_servers_use_a_checklist_with_saved_selection(monkeypatch):
    observed = []

    def checkbox(*a, **kwargs):
        observed.extend(kwargs["choices"])
        return Answer(["beta"])

    monkeypatch.setattr("questionary.checkbox", checkbox)
    schema = {
        "type": "array",
        "items": {
            "type": "string",
            "enum": ["alpha", "beta"],
            "x-bsm-server-name": True,
        },
    }
    assert await prompt_value(schema, ("servers",), schema, ["alpha"]) == ["beta"]
    assert [choice.checked for choice in observed] == [True, False]


@pytest.mark.asyncio
async def test_password_blank_keeps_current_value_without_printing(monkeypatch, capsys):
    def password(*a, **kwargs):
        assert kwargs["default"] == ""
        return Answer("")

    monkeypatch.setattr("questionary.password", password)
    spec = {"type": "string", "format": "password"}
    assert (
        await prompt_value(spec, ("password",), spec, "hidden-value") == "hidden-value"
    )
    assert "hidden-value" not in display("hidden-value", ("password",), spec)
    assert "hidden-value" not in capsys.readouterr().out


@pytest.mark.asyncio
async def test_invalid_numeric_input_is_retried(monkeypatch):
    answers = iter(["-1", "3"])
    monkeypatch.setattr("questionary.text", lambda *a, **k: Answer(next(answers)))
    spec = {"type": "number", "minimum": 0}
    assert await prompt_value(spec, ("interval",), spec, 1) == 3


@pytest.mark.asyncio
async def test_plugin_editor_refuses_overwriting_other_sessions(monkeypatch):
    import click

    from bsm_api_client.models import GetPluginSettingsResponse
    from bsm_cli.plugins import edit_plugin_settings

    client = AsyncMock()
    client.plugins.async_get_plugin_settings.side_effect = [
        GetPluginSettingsResponse(settings={"enabled": True}),
        GetPluginSettingsResponse(settings={"enabled": False}),
    ]
    monkeypatch.setattr(
        "bsm_cli.plugins.edit_settings",
        AsyncMock(return_value={"enabled": True, "delay": 3}),
    )
    with pytest.raises(click.ClickException, match="another session"):
        await edit_plugin_settings(client, "demo")
    client.plugins.async_update_plugin_settings.assert_not_called()
