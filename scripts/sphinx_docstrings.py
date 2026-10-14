"""Normalize generated and handwritten docstrings without changing executable code."""

import ast
import inspect
import re
from pathlib import Path


def native_docstring(value: str) -> str:
    """Convert Google field sections to native Sphinx fields."""
    lines = inspect.cleandoc(value).splitlines()
    result: list[str] = []
    section = None
    pending = None
    for line in lines:
        stripped = line.strip()
        if stripped in {
            "Args:",
            "Arguments:",
            "Attributes:",
            "Raises:",
            "Returns:",
            "Yields:",
        }:
            section = stripped[:-1]
            pending = None
            result.append("")
            continue
        if section and stripped and not line.startswith(" "):
            section = None
            pending = None
        if section in {"Args", "Arguments", "Attributes", "Raises"} and stripped:
            match = re.match(r"([\w.*]+)(?:\s*\(.*\))?:\s*(.*)$", stripped)
            if match:
                name, description = match.groups()
                field = (
                    "ivar"
                    if section == "Attributes"
                    else "raises" if section == "Raises" else "param"
                )
                result.append(
                    f":{field} {name}: {description or 'Value supplied to the operation.'}"
                )
                pending = len(result) - 1
            elif pending is not None:
                result[pending] += " " + stripped
            else:
                result.append(stripped)
        elif section in {"Returns", "Yields"} and stripped:
            field = "returns" if section == "Returns" else "yields"
            # Type annotations already describe generated result types.
            description = (
                "The parsed response."
                if re.match(r"^(Response\[|[A-Z]\w*(?:\[|$))", stripped)
                else stripped
            )
            if pending is None:
                result.append(f":{field}: {description}")
                pending = len(result) - 1
            else:
                result[pending] += " " + stripped
        else:
            result.append(line)
    return re.sub(r"\n{3,}", "\n\n", "\n".join(result)).strip()


def normalize_file(path: Path) -> None:
    """Replace docstring literals while preserving code and comments."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    offsets = [0]
    for line in lines:
        offsets.append(offsets[-1] + len(line))
    edits = []
    for node in ast.walk(ast.parse(text)):
        if not isinstance(
            node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)
        ):
            continue
        if not node.body or not isinstance(node.body[0], ast.Expr):
            continue
        literal = node.body[0].value
        if not isinstance(literal, ast.Constant) or not isinstance(literal.value, str):
            continue
        value = native_docstring(literal.value)
        if value == inspect.cleandoc(literal.value):
            continue
        indent = " " * literal.col_offset
        rendered = (
            '"""'
            + value.replace('"""', '\\"\\"\\"').replace("\n", "\n" + indent)
            + '"""'
        )
        start = offsets[literal.lineno - 1] + literal.col_offset
        assert literal.end_lineno is not None and literal.end_col_offset is not None
        end = offsets[literal.end_lineno - 1] + literal.end_col_offset
        edits.append((start, end, rendered))
    for start, end, rendered in sorted(edits, reverse=True):
        text = text[:start] + rendered + text[end:]
    path.write_text(text, encoding="utf-8")


def normalize_package(package: Path) -> None:
    """Normalize every Python docstring in a generated package."""
    for source_file in package.rglob("*.py"):
        normalize_file(source_file)
