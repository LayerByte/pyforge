from __future__ import annotations

import json
from typing import Any

from rich.console import Console
from rich.json import JSON
from rich.table import Table


def render_result(console: Console, result: Any) -> None:
    if isinstance(result, (dict, list)):
        console.print(JSON(json.dumps(result, ensure_ascii=False, default=str)))
    else:
        console.print(str(result))


def render_specs(console: Console, specs: list[Any]) -> None:
    table = Table("Name", "Title", "Description", border_style="cyan")
    for spec in specs:
        table.add_row(spec.name, spec.title, spec.description)
    console.print(table)
