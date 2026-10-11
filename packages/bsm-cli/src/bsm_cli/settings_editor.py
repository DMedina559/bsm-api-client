"""Shared schema-driven settings editor for interactive terminal workflows."""

from __future__ import annotations

import copy
import json

import click
import questionary

from bsm_api_client.exceptions import InvalidInputError
from bsm_api_client.openapi import resolve
from bsm_api_client.validation import validate_input

CANCEL = object()


def infer_schema(value):
    """Infer editable shapes when a server advertises values without a schema."""
    if isinstance(value, dict):
        return {
            "type": "object",
            "properties": {k: infer_schema(v) for k, v in value.items()},
        }
    if isinstance(value, bool):
        return {"type": "boolean"}
    if isinstance(value, int):
        return {"type": "integer"}
    if isinstance(value, float):
        return {"type": "number"}
    if isinstance(value, str):
        return {"type": "string"}
    return {}


def fields(document, spec, values, path=()):
    spec = resolve(document, spec)
    for key, raw in spec.get("properties", {}).items():
        field = resolve(document, raw)
        if field.get("readOnly") or key == "config_schema_version":
            continue
        value = values.get(key) if isinstance(values, dict) else None
        if field.get("type") == "object" and field.get("properties"):
            yield from fields(document, field, value or {}, (*path, key))
        else:
            yield (*path, key), field, value


def set_value(values, path, value):
    target = values
    for key in path[:-1]:
        target = target.setdefault(key, {})
    target[path[-1]] = value


def is_secret(path, spec):
    return spec.get("format") == "password" or any(
        word in path[-1].lower()
        for word in ("password", "secret", "token", "credential")
    )


def display(value, path, spec):
    return (
        "••••••"
        if is_secret(path, spec) and value
        else json.dumps(value, ensure_ascii=False)
    )


async def prompt_value(document, path, spec, current):  # noqa: C901
    label = spec.get("title") or " / ".join(path)
    if spec.get("description"):
        click.echo(spec["description"])
    if "anyOf" in spec or "oneOf" in spec:
        variants = [
            resolve(document, v) for v in spec.get("anyOf", spec.get("oneOf", []))
        ]
        if any(v.get("type") == "null" for v in variants):
            choice = await questionary.select(
                label, choices=["Edit value", "Set null", "Cancel"]
            ).ask_async()
            if choice in (None, "Cancel"):
                return CANCEL
            if choice == "Set null":
                return None
            non_null = [v for v in variants if v.get("type") != "null"]
            if len(non_null) == 1:
                return await prompt_value(
                    document,
                    path,
                    {**spec, **non_null[0], "anyOf": [], "oneOf": []},
                    current,
                )
    if spec.get("type") == "boolean":
        value = await questionary.confirm(label, default=bool(current)).ask_async()
        return CANCEL if value is None else value
    if spec.get("enum"):
        return await _select_enum(label, spec["enum"], current)
    items = resolve(document, spec.get("items", {}))
    if spec.get("type") == "array" and items.get("enum") is not None:
        selected = current if isinstance(current, list) else []
        choices = [
            questionary.Choice(
                str(v) + ("" if v in items["enum"] else " (unavailable)"),
                value=v,
                checked=v in selected,
            )
            for v in dict.fromkeys([*items["enum"], *selected])
        ]
        if not choices:
            click.echo(
                "No valid servers available."
                if items.get("x-bsm-server-name")
                else "No choices available."
            )
            return []
        value = await questionary.checkbox(
            label + " (Space to toggle, Enter to accept)", choices=choices
        ).ask_async()
        return CANCEL if value is None else value
    secret = is_secret(path, spec)
    text_prompt = questionary.password if secret else questionary.text
    scalar = spec.get("type") in {"string", "integer", "number"}
    default = (
        ""
        if secret
        else (
            str(current)
            if scalar and current is not None
            else json.dumps(current, ensure_ascii=False)
        )
    )
    while True:
        raw = await text_prompt(
            label + (" (blank keeps current value)" if secret else ""), default=default
        ).ask_async()
        if raw is None:
            return CANCEL
        if secret and not raw:
            return current
        try:
            value = raw if spec.get("type") == "string" else json.loads(raw)
            validate_input(document, spec, value, label)
            return value
        except (ValueError, InvalidInputError) as error:
            click.secho(
                (
                    str(error)
                    if isinstance(error, InvalidInputError)
                    else "Enter valid JSON of the expected type."
                ),
                fg="red",
            )


async def _select_enum(label, choices, current):
    value = await questionary.select(
        label,
        choices=[questionary.Choice(str(v), value=(v,)) for v in choices],
        default=(current,) if current in choices else None,
    ).ask_async()
    return CANCEL if value is None else value[0]


async def edit_settings(values, schema=None, *, title="Settings"):  # noqa: C901
    """Return a reviewed draft, or None on cancellation; never write while editing."""
    original = copy.deepcopy(values)
    draft = copy.deepcopy(values)
    document = schema or infer_schema(values)
    while True:
        editable = list(fields(document, document, draft))
        choices = [
            questionary.Choice(
                f"{' / '.join(path)}: {display(value, path, spec)}", value=path
            )
            for path, spec, value in editable
        ]
        if not editable:
            choices.append(questionary.Choice("Edit settings as JSON", value="json"))
        choices.extend(
            [
                questionary.Separator(),
                questionary.Choice("Review and save", value="save"),
                questionary.Choice("Discard and return", value="cancel"),
            ]
        )
        choice = await questionary.select(title, choices=choices).ask_async()
        if choice is None or choice == "cancel":
            if (
                draft != original
                and not await questionary.confirm(
                    "Discard unsaved changes?", default=False
                ).ask_async()
            ):
                continue
            return None
        if choice == "save":
            if draft == original:
                click.echo("No changes to save.")
                return None
            try:
                validate_input(document, document, draft, "settings")
            except InvalidInputError as error:
                click.secho(str(error), fg="red")
                continue
            for path, spec, value in fields(document, document, draft):
                previous = original
                for key in path:
                    previous = previous.get(key) if isinstance(previous, dict) else None
                if previous != value:
                    click.echo(
                        f"{' / '.join(path)}: {display(previous, path, spec)} → {display(value, path, spec)}"
                    )
            if not editable:
                click.echo("Settings JSON changed.")
            if await questionary.confirm(
                "Save these changes?", default=False
            ).ask_async():
                return draft
            continue
        if choice == "json":
            value = await prompt_value(
                document, ("Settings JSON",), {"type": "object"}, draft
            )
            if value is not CANCEL and isinstance(value, dict):
                draft = value
            continue
        path, spec, current = next(item for item in editable if item[0] == choice)
        value = await prompt_value(document, path, spec, current)
        if value is not CANCEL:
            set_value(draft, path, value)
