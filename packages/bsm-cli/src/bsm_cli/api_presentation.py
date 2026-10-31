"""Readable OpenAPI contracts and bounded terminal response views."""

import json
from collections.abc import Mapping

import click

from bsm_api_client.openapi import resolve
from bsm_cli.output import serializable
from bsm_cli.presentation import table


def schema_type(document, spec):
    if "$ref" in spec:
        return spec["$ref"].rsplit("/", 1)[-1].replace("~1", "/").replace("~0", "~")
    variants = spec.get("anyOf", spec.get("oneOf", []))
    if variants:
        return " | ".join(schema_type(document, item) for item in variants)
    if spec.get("type") == "array":
        return schema_type(document, spec.get("items", {})) + "[]"
    kind = spec.get("type", "object" if "properties" in spec else "JSON")
    return " | ".join(kind) if isinstance(kind, list) else kind


def fields(document, spec, seen=frozenset()):
    ref = spec.get("$ref")
    if ref and ref in seen:
        return {}
    spec = resolve(document, spec)
    merged = {
        **spec,
        "properties": dict(spec.get("properties", {})),
        "required": list(spec.get("required", [])),
    }
    for part in spec.get("allOf", []):
        item = fields(document, part, seen | ({ref} if ref else set()))
        merged["properties"].update(item.get("properties", {}))
        merged["required"].extend(item.get("required", []))
    return merged


def show_model(document, name, spec):
    model = fields(document, spec)
    click.secho(name, bold=True)
    if model.get("description"):
        click.echo(model["description"])
    rows = []
    for key, raw in model.get("properties", {}).items():
        field = resolve(document, raw)
        description = field.get("description", "")
        if "enum" in field:
            description += " Choices: " + ", ".join(map(str, field["enum"]))
        if "default" in field:
            description += " Default: " + json.dumps(field["default"])
        rows.append(
            (
                key,
                schema_type(document, raw),
                "required" if key in model.get("required", []) else "optional",
                description,
            )
        )
    if rows:
        table("Fields", ("Property", "Type", "Presence", "Description"), rows)
    else:
        click.echo("Type: " + schema_type(document, spec))
        if model.get("enum"):
            click.echo("Choices: " + ", ".join(map(str, model["enum"])))
    refs = sorted({part.rsplit("/", 1)[-1] for part in _references(spec)})
    if refs:
        click.echo("Referenced models: " + ", ".join(refs))


def _references(value):
    if isinstance(value, dict):
        if "$ref" in value:
            yield value["$ref"]
        for item in value.values():
            yield from _references(item)
    elif isinstance(value, list):
        for item in value:
            yield from _references(item)


def show_operation(document, operation):
    click.secho(f"{operation.method} {operation.path}", bold=True, fg="cyan")
    click.echo(f"{operation.operation_id} · {operation.summary or operation.namespace}")
    if operation.description:
        click.echo(operation.description)
    if operation.parameters:
        table(
            "Parameters",
            ("Name", "Location", "Type", "Presence"),
            [
                (
                    p["name"],
                    p["in"],
                    schema_type(document, p.get("schema", {})),
                    "required" if p.get("required") else "optional",
                )
                for p in operation.parameters
            ],
        )
    for media, body in operation.request_body.get("content", {}).items():
        show_model(document, f"Request body ({media})", body.get("schema", {}))
    for status, raw in operation.responses.items():
        response = resolve(document, raw)
        click.echo(f"Response {status}: {response.get('description', '')}")
        for media, content in response.get("content", {}).items():
            show_model(document, media, content.get("schema", {}))


def compact(value):
    if isinstance(value, (dict, list)):
        return f"{len(value)} {'properties' if isinstance(value, dict) else 'items'}"
    text = (
        "null"
        if value is None
        else (
            json.dumps(value, ensure_ascii=False)
            if not isinstance(value, str)
            else value
        )
    )
    return text if len(text) < 180 else text[:177] + "…"


def _show_array(value, title, page, page_size, query):
    filtered = (
        [
            item
            for item in value
            if query.lower()
            in json.dumps(item, default=serializable, ensure_ascii=False).lower()
        ]
        if query
        else value
    )
    pages = max(1, (len(filtered) + page_size - 1) // page_size)
    current = min(page, pages)
    start, stop = (current - 1) * page_size, current * page_size
    rows = filtered[start:stop]
    click.echo(f"{title}: {len(filtered)} items · page {current}/{pages}")
    if rows and all(isinstance(row, Mapping) for row in rows):
        columns = list(dict.fromkeys(key for row in rows for key in row))[:8]
        table(
            title,
            tuple(map(str, columns)),
            [[compact(row.get(key)) for key in columns] for row in rows],
        )
    else:
        table(
            title,
            ("#", "Value"),
            [
                ((current - 1) * page_size + index + 1, compact(item))
                for index, item in enumerate(rows)
            ],
        )
    if len(filtered) > page_size:
        click.echo(
            "Use the explorer's response pages or --json/--raw for the complete output."
        )


def show_data(value, *, title="Response", page=1, page_size=25, query="", depth=0):
    if not isinstance(value, (dict, list, str, int, float, bool, type(None))):
        value = serializable(value)
    if isinstance(value, list):
        _show_array(value, title, page, page_size, query)
    elif isinstance(value, dict):
        scalar = [
            (key, compact(item))
            for key, item in list(value.items())[:100]
            if not isinstance(item, (dict, list))
        ]
        if scalar:
            table(title, ("Property", "Value"), scalar[:100])
        for key, item in list(value.items())[:100]:
            if isinstance(item, (dict, list)):
                if depth < 3:
                    show_data(
                        item,
                        title=str(key),
                        page=page,
                        page_size=page_size,
                        query=query,
                        depth=depth + 1,
                    )
                else:
                    click.echo(f"{key}: {compact(item)}")
        if len(value) > 100:
            click.echo(
                "First 100 properties shown; use --json/--raw for complete output."
            )
    else:
        click.echo(f"{title}: {compact(value)}")
