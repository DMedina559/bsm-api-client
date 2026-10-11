"""Consistent terminal tables for dashboard data."""

import sys
from rich.console import Console
from rich.table import Table


def table(title, columns, rows):
    view = Table(
        title=title, title_justify="left", header_style="bold cyan", expand=False
    )
    for column in columns:
        view.add_column(column)
    for row in rows:
        view.add_row(
            *(str(value) if value is not None else "Unavailable" for value in row)
        )
    Console(file=sys.stdout, highlight=False).print(view)
