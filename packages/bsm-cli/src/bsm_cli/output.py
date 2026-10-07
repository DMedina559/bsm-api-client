"""Shared CLI output, client access, and deterministic error codes."""

import dataclasses
import functools
import json
from typing import Any

import click

from bsm_api_client.exceptions import (
    AuthError,
    CannotConnectError,
    InvalidInputError,
    NotFoundError,
    OperationFailedError,
)


class CliError(click.ClickException):
    """CLI failure with a conventional nonzero exit status."""


class CliInputError(CliError):
    exit_code = 2


class CliAuthError(CliError):
    exit_code = 3


class CliConnectionError(CliError):
    exit_code = 4


class CliNotFoundError(CliError):
    exit_code = 5


def normalize_error(error: Exception) -> click.ClickException:
    if isinstance(error, click.ClickException):
        return error
    error_class = (
        CliAuthError
        if isinstance(error, AuthError)
        else (
            CliConnectionError
            if isinstance(error, CannotConnectError)
            else (
                CliNotFoundError
                if isinstance(error, NotFoundError)
                else (
                    CliInputError
                    if isinstance(error, (InvalidInputError, ValueError))
                    else CliError
                )
            )
        )
    )
    return error_class(str(error))


def fail(error: Exception) -> None:
    if isinstance(error, click.Abort):
        raise error
    raise normalize_error(error)


def get_client(ctx: click.Context) -> Any:
    client = ctx.obj.get("client")
    if client is None:
        raise CliAuthError("You are not logged in. Run `bsm-cli auth login`.")
    return client


def serializable(value: Any) -> Any:
    if hasattr(value, "model_dump"):
        return value.model_dump(mode="json")
    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        return dataclasses.asdict(value)
    if hasattr(value, "to_dict"):
        return value.to_dict()
    if isinstance(value, bytes):
        import base64

        return {"encoding": "base64", "data": base64.b64encode(value).decode()}
    raise TypeError(f"Cannot serialize {type(value).__name__}")


def echo_json(value: Any, *, err: bool = False) -> None:
    click.echo(
        json.dumps(value, default=serializable, sort_keys=True, ensure_ascii=False),
        err=err,
    )


def emit(ctx: click.Context, value: Any, *, columns: tuple[str, ...] = ()) -> Any:
    if ctx.obj.get("json_output"):
        return value
    if columns and isinstance(value, list):
        rows = [[str(row.get(key, "")) for key in columns] for row in value]
        widths = [
            max([len(key.upper()), *(len(row[i]) for row in rows)])
            for i, key in enumerate(columns)
        ]
        click.echo(
            "  ".join(key.upper().ljust(width) for key, width in zip(columns, widths))
        )
        for row in rows:
            click.echo("  ".join(cell.ljust(width) for cell, width in zip(row, widths)))
    else:
        click.echo(
            json.dumps(
                value,
                default=serializable,
                sort_keys=True,
                indent=2,
                ensure_ascii=False,
            )
        )
    return value


class RecordingClient:
    """Capture structured facade responses while curated commands render text."""

    def __init__(self, client: Any, record: bool = True):
        self.client = client
        self.record = record
        self.results: list[Any] = []

    def __getattr__(self, name: str) -> Any:
        target = getattr(self.client, name)
        if not name.startswith("async_") or not callable(target):
            return target

        @functools.wraps(target)
        async def record(*args, **kwargs):
            result = await target(*args, **kwargs)
            status = (
                result.get("status")
                if isinstance(result, dict)
                else getattr(result, "status", None)
            )
            error = result.get("error") if isinstance(result, dict) else None
            if status in {"error", "failed", "cancelled"} or isinstance(error, dict):
                raise OperationFailedError(
                    (
                        (error or result).get("message", "Operation failed")
                        if isinstance(result, dict)
                        else getattr(result, "message", None) or "Operation failed"
                    ),
                    response_data=(
                        result
                        if isinstance(result, dict)
                        else (
                            result.model_dump(mode="json")
                            if hasattr(result, "model_dump")
                            else {
                                "status": status,
                                "message": getattr(result, "message", None),
                            }
                        )
                    ),
                )
            if self.record:
                self.results.append(result)
            return result

        return record
