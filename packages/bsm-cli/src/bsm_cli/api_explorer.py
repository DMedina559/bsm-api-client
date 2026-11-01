"""Interactive API discovery, schema-driven requests and response inspection."""

import json
import re
from pathlib import Path

import click
import questionary

from bsm_api_client.exceptions import InvalidInputError
from bsm_api_client.openapi import resolve
from bsm_api_client.validation import validate_input
from bsm_cli.api_presentation import (
    fields,
    schema_type,
    show_data,
    show_model,
    show_operation,
)
from bsm_cli.interaction import menu_action
from bsm_cli.output import emit

OMIT = object()
SECRET = re.compile(
    r"password|secret|token|authorization|cookie|api.?key|credential", re.I
)


def redact(value, document, spec=None):
    """Conceal secret and write-only fields in request previews."""
    spec = resolve(document, spec or {})
    if spec.get("writeOnly") or spec.get("format") == "password":
        return "[redacted]"
    if isinstance(value, dict):
        props = fields(document, spec).get("properties", {})
        return {
            key: (
                "[redacted]"
                if SECRET.search(key)
                else redact(item, document, props.get(key, {}))
            )
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [redact(item, document, spec.get("items", {})) for item in value]
    return value


def validate_request(document, operation, locations, body):
    for parameter in operation.parameters:
        location, name = parameter["in"], parameter["name"]
        if name in locations.get(location, {}):
            validate_input(
                document, parameter.get("schema", {}), locations[location][name], name
            )
    if body is not None:
        media = operation.request_body.get("content", {})
        contract = next(
            (
                item.get("schema", {})
                for kind, item in media.items()
                if kind == "application/json" or kind.endswith("+json")
            ),
            None,
        )
        if contract is None:
            raise InvalidInputError(
                "This operation does not advertise a JSON request body."
            )
        validate_input(document, contract, body, "request body")


def preview_request(document, operation, locations, body, form=(), files=()):
    media = operation.request_body.get("content", {})
    contract = next(
        (
            item.get("schema", {})
            for kind, item in media.items()
            if kind == "application/json" or kind.endswith("+json")
        ),
        {},
    )
    safe_locations = redact(locations, document)
    for parameter in operation.parameters:
        location, name = parameter["in"], parameter["name"]
        if (
            name in locations.get(location, {})
            and safe_locations[location][name] != "[redacted]"
        ):
            safe_locations[location][name] = redact(
                locations[location][name], document, parameter.get("schema", {})
            )
    return {
        "operation_id": operation.operation_id,
        "method": operation.method,
        "path": operation.path,
        "parameters": safe_locations,
        "body": redact(body, document, contract),
        "form": redact(dict(item.split("=", 1) for item in form), document),
        "files": [item.partition("=")[0] for item in files],
    }


async def _answer(prompt):
    value = await prompt.ask_async()
    if value is None:
        raise click.Abort()
    return value


def _input_spec(document, raw):
    spec = fields(document, raw)
    variants = spec.get("anyOf", spec.get("oneOf", []))
    non_null = [item for item in variants if item.get("type") != "null"]
    return fields(document, non_null[0]) if len(non_null) == 1 else spec


async def prompt_value(document, raw, name, *, required=True, depth=0):
    spec = _input_spec(document, raw)
    if not required:
        if not await _answer(
            questionary.confirm(f"Set {name}? (optional)", default=False)
        ):
            return OMIT
    if spec.get("description"):
        click.echo(spec["description"])
    if spec.get("properties") and depth < 4:
        return await _prompt_object(document, spec, name, depth)
    while True:
        try:
            value = await _prompt_scalar(document, spec, name)
            validate_input(document, raw, value, name)
            return value
        except (ValueError, InvalidInputError) as error:
            click.secho(str(error), fg="yellow")


async def _prompt_object(document, spec, name, depth):
    result = {}
    for key, child in spec.get("properties", {}).items():
        if resolve(document, child).get("readOnly"):
            continue
        value = await prompt_value(
            document,
            child,
            f"{name}.{key}",
            required=key in spec.get("required", []),
            depth=depth + 1,
        )
        if value is not OMIT:
            result[key] = value
    try:
        validate_input(document, spec, result, name)
    except InvalidInputError:
        click.echo(
            "This model has additional constraints. Enter its complete JSON value."
        )
        return await prompt_value(document, spec, name, depth=4)
    return result


async def _prompt_scalar(document, spec, name):
    choices = spec.get(
        "enum",
        (
            [spec["const"]]
            if "const" in spec
            else [True, False] if spec.get("type") == "boolean" else None
        ),
    )
    if choices is not None:
        index = await _answer(
            questionary.select(
                f"{name} ({schema_type(document, spec)}):",
                choices=[
                    questionary.Choice(json.dumps(value), value=index)
                    for index, value in enumerate(choices)
                ],
            )
        )
        return choices[index]
    secret = (
        spec.get("writeOnly") or spec.get("format") == "password" or SECRET.search(name)
    )
    ask = questionary.password if secret else questionary.text
    default = spec.get("default", "")
    text = await _answer(
        ask(
            f"{name} ({schema_type(document, spec)}):",
            **(
                {}
                if secret
                else {
                    "default": (
                        default if isinstance(default, str) else json.dumps(default)
                    )
                }
            ),
        )
    )
    if spec.get("type") == "string":
        return text
    try:
        return json.loads(text)
    except ValueError:
        if "type" not in spec and not spec.get("anyOf") and not spec.get("oneOf"):
            return text
        raise ValueError("Enter a valid JSON value for this type.") from None


def _is_binary_field(document, raw):
    spec = _input_spec(document, raw)
    return (
        spec.get("format") == "binary"
        or spec.get("contentMediaType") == "application/octet-stream"
    )


def _is_binary_response(document, operation):
    for status, raw in (operation.responses or {}).items():
        if not str(status).startswith("2"):
            continue
        response = resolve(document, raw)
        for media, content in (response.get("content") or {}).items():
            if media == "application/octet-stream" or media.startswith("image/"):
                return True
            if resolve(document, content.get("schema", {})).get("format") == "binary":
                return True
    return False


async def _prompt_file_path(name, *, required=True):
    if not required:
        if not await _answer(
            questionary.confirm(f"Attach file for {name}? (optional)", default=False)
        ):
            return OMIT
    while True:
        path_text = await _answer(questionary.text(f"{name} (local file path):"))
        candidate = Path(path_text).expanduser()
        if candidate.is_file():
            return str(candidate)
        click.secho(f"File not found: {path_text}", fg="yellow")


async def _prompt_form_body(document, operation, form_spec):
    form = []
    files = []
    if not operation.request_body.get("required") and not await _answer(
        questionary.confirm("Provide form/multipart body?", default=True)
    ):
        return (), ()
    model = fields(document, form_spec)
    for key, raw_prop in model.get("properties", {}).items():
        if resolve(document, raw_prop).get("readOnly"):
            continue
        req = key in model.get("required", [])
        if _is_binary_field(document, raw_prop):
            file_path = await _prompt_file_path(key, required=req)
            if file_path is not OMIT:
                files.append(f"{key}={file_path}")
        else:
            val = await prompt_value(document, raw_prop, key, required=req)
            if val is not OMIT:
                form.append(f"{key}={val if isinstance(val, str) else json.dumps(val)}")
    return tuple(form), tuple(files)


async def _prompt_json_body(document, operation, spec):
    mode = await _answer(
        questionary.select(
            "Request body",
            choices=[
                "Guided fields",
                "Raw JSON",
                *([] if operation.request_body.get("required") else ["Omit body"]),
            ],
        )
    )
    if mode == "Guided fields":
        return json.dumps(await prompt_value(document, spec, "body"))
    if mode == "Raw JSON":
        return await _raw_body(document, spec)
    return None


async def build_request_parts(document, operation):
    parameters = []
    for parameter in operation.parameters:
        if parameter["in"] not in {"path", "query", "header"}:
            raise InvalidInputError(
                f"Unsupported parameter location: {parameter['in']}"
            )
        value = await prompt_value(
            document,
            parameter.get("schema", {}),
            f"{parameter['name']} ({parameter['in']})",
            required=parameter.get("required", False),
        )
        if value is not OMIT:
            parameters.append(
                f"{parameter['name']}={value if isinstance(value, str) else json.dumps(value)}"
            )
    content = operation.request_body.get("content", {})
    spec = next(
        (
            item.get("schema", {})
            for kind, item in content.items()
            if kind == "application/json" or kind.endswith("+json")
        ),
        None,
    )
    form_spec = next(
        (
            item.get("schema", {})
            for kind, item in content.items()
            if kind in ("multipart/form-data", "application/x-www-form-urlencoded")
        ),
        None,
    )
    body = None
    form: tuple[str, ...] = ()
    files: tuple[str, ...] = ()
    if spec is not None:
        body = await _prompt_json_body(document, operation, spec)
    elif form_spec is not None:
        form, files = await _prompt_form_body(document, operation, form_spec)
    elif operation.request_body.get("required"):
        raise InvalidInputError(
            "Use api call --form/--file for this request media type."
        )
    return parameters, body, form, files


async def build_request(document, operation):
    parameters, body, _form, _files = await build_request_parts(document, operation)
    return parameters, body


async def _raw_body(document, spec):
    while True:
        text = await _answer(questionary.text("JSON body:", multiline=True))
        try:
            value = json.loads(text)
            validate_input(document, spec, value, "request body")
            return json.dumps(value)
        except (ValueError, InvalidInputError) as error:
            click.secho(str(error), fg="yellow")


def _suggested_filename(headers):
    disposition = ""
    for key, val in (headers or {}).items():
        if key.lower() == "content-disposition":
            disposition = str(val)
            break
    match = re.search(r'filename="?([^";]+)"?', disposition)
    return match.group(1) if match else ""


def _render_response_view(ctx, mode, data, headers, page, query):
    if mode == "Raw JSON":
        emit(ctx, data)
    elif mode == "Headers":
        show_data(headers, page=page, query=query)
    elif isinstance(data, bytes):
        show_data(
            {
                "binary": True,
                "bytes": len(data),
                "content_type": next(
                    (v for k, v in headers.items() if k.lower() == "content-type"),
                    "application/octet-stream",
                ),
                "filename": _suggested_filename(headers) or None,
            },
            page=page,
            query=query,
        )
    else:
        show_data(data, page=page, query=query)


async def response_menu(ctx, result):
    from bsm_cli.api import _write_output_file

    page, query, mode = 1, "", "Body"
    while True:
        click.secho(
            f"HTTP {result.get('status_code', 'complete')} · {result.get('duration_ms', 0)} ms",
            bold=True,
        )
        data = result.get("data")
        headers = result.get("headers", {})
        _render_response_view(ctx, mode, data, headers, page, query)
        choice = await _answer(
            questionary.select(
                "Response view",
                choices=[
                    "Body",
                    "Headers",
                    "Raw JSON",
                    "Save to file",
                    "Filter items",
                    "Next page",
                    "Previous page",
                    "Back",
                ],
            )
        )
        if choice == "Back":
            return
        if choice == "Save to file":
            default_name = _suggested_filename(headers) or "response.bin"
            target_text = await _answer(
                questionary.text("Save response to file:", default=default_name)
            )
            if target_text:
                target = Path(target_text).expanduser()
                written = _write_output_file(target, data)
                click.secho(f"Saved {written} bytes to {target}", fg="green")
        elif choice == "Filter items":
            query = await _answer(
                questionary.text("Filter response items:", default=query)
            )
            page, mode = 1, "Body"
        elif choice == "Next page":
            page, mode = page + 1, "Body"
        elif choice == "Previous page":
            page, mode = max(1, page - 1), "Body"
        else:
            mode = choice


async def browse_models(ctx, document):
    models = document.get("components", {}).get("schemas", {})
    if not models:
        click.echo("This contract has no component models.")
        return
    while True:
        name = await _answer(
            questionary.select(
                "Models (type to search)",
                choices=[*sorted(models), "Back"],
                use_search_filter=True,
                use_jk_keys=False,
            )
        )
        if name == "Back":
            return
        show_model(document, name, models[name])
        mode = await _answer(
            questionary.select("Model view", choices=["Fields", "Raw JSON", "Back"])
        )
        if mode == "Raw JSON":
            emit(ctx, models[name])
        elif mode == "Fields":
            show_model(document, name, models[name])


async def operation_menu(ctx, client, operation):
    from bsm_cli.api import invoke

    while True:
        show_operation(client.schema, operation)
        choice = await _answer(
            questionary.select(
                "Operation view",
                choices=["Build request", "Raw contract", "Models", "Back"],
            )
        )
        if choice == "Back":
            return
        if choice == "Models":
            await browse_models(ctx, client.schema)
        elif choice == "Raw contract":
            emit(ctx, operation.to_dict())
        else:
            parameters, body, form, files = await build_request_parts(
                client.schema, operation
            )
            await invoke(
                ctx,
                operation.operation_id,
                parameters,
                body,
                form,
                file=files,
                dry_run=True,
            )
            can_stream_download = operation.method == "GET" and _is_binary_response(
                client.schema, operation
            )
            preview_choices = [
                "Execute",
                *(["Download to file"] if can_stream_download else []),
                "Edit request",
                "Back",
            ]
            action = await _answer(
                questionary.select("Request preview", choices=preview_choices)
            )
            if action == "Download to file":
                target_text = await _answer(
                    questionary.text(
                        "Save download to file:",
                        default=f"{operation.operation_id}.bin",
                    )
                )
                if target_text:
                    saved = await menu_action(
                        invoke(
                            ctx,
                            operation.operation_id,
                            parameters,
                            body,
                            form,
                            file=files,
                            output=Path(target_text).expanduser(),
                            render=False,
                        )
                    )
                    show_data(saved, title="Download complete")
            elif action == "Execute":
                result = await menu_action(
                    invoke(
                        ctx,
                        operation.operation_id,
                        parameters,
                        body,
                        form,
                        file=files,
                        details=True,
                        render=False,
                    )
                )
                await response_menu(ctx, result)


async def explore(ctx, *, search=""):
    from bsm_cli.api import discover

    client = await discover(ctx)
    while True:
        action = await _answer(
            questionary.select(
                "API Explorer",
                choices=["Operations", "Models", "Refresh contract", "Back"],
            )
        )
        if action == "Back":
            return
        try:
            if action == "Models":
                await browse_models(ctx, client.schema)
            elif action == "Refresh contract":
                client = await discover(ctx, force=True)
            else:
                operations = [
                    op
                    for op in client.operations.values()
                    if search.lower()
                    in f"{op.operation_id} {op.path} {op.method} {op.summary} {' '.join(op.tags)}".lower()
                ]
                choices = [
                    questionary.Choice(
                        f"{op.method:6} {op.operation_id} · {op.namespace} · {op.summary or ''} {op.path}",
                        value=op.operation_id,
                    )
                    for op in sorted(
                        operations, key=lambda op: (op.namespace, op.operation_id)
                    )
                ]
                identifier = await _answer(
                    questionary.select(
                        "Operations (type to search)",
                        choices=[*choices, "Back"],
                        use_search_filter=True,
                        use_jk_keys=False,
                    )
                )
                if identifier != "Back":
                    await operation_menu(ctx, client, client.operations[identifier])
        except click.Abort:
            click.echo("Action cancelled. Returned to the API explorer.")
        except Exception as error:
            click.secho(f"Action failed: {error}", fg="red")
