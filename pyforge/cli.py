from __future__ import annotations

import typer
from rich.console import Console
from pydantic import ValidationError as PydanticValidationError
from typing import Any

from pyforge import __version__

app = typer.Typer(
    help="PyForge developer and system utility toolkit.",
    no_args_is_help=True,
    invoke_without_command=True,
)
console = Console()


def _parse_arguments(raw: str) -> dict[str, Any]:
    import json

    try:
        values = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise typer.BadParameter(f"arguments must be valid JSON: line {exc.lineno}, column {exc.colno}") from exc
    if not isinstance(values, dict):
        raise typer.BadParameter("arguments must be a JSON object")
    return values


@app.callback()
def main(version: bool = typer.Option(False, "--version", is_eager=True, help="Show the version and exit.")) -> None:
    """PyForge developer and system utility toolkit."""
    if version:
        console.print(f"PyForge {__version__}")
        raise typer.Exit()


@app.command()
def version() -> None:
    """Print the installed PyForge version."""
    console.print(f"PyForge {__version__}")


@app.command("categories")
def categories_command() -> None:
    """List available tool categories."""
    from pyforge.registry import TOOL_SPECS

    categories = sorted({spec.category for spec in TOOL_SPECS})
    for category in categories:
        console.print(category)


@app.command("tools")
def tools_command(category: str | None = typer.Argument(None)) -> None:
    """List registered tools, optionally filtered by category."""
    from pyforge.registry import TOOL_SPECS
    from pyforge.ui.components import render_specs

    specs = [spec for spec in TOOL_SPECS if category is None or spec.category == category]
    if not specs:
        console.print(f"No tools found for category: {category}", style="yellow")
        raise typer.Exit(code=1)
    render_specs(console, specs)


@app.command("describe")
def describe_command(name: str) -> None:
    """Show metadata for one registered tool."""
    from pyforge.registry import get_tool
    from pyforge.ui.components import render_result

    try:
        spec = get_tool(name)
    except KeyError as exc:
        console.print(f"Unknown tool: {name}", style="bold red")
        raise typer.Exit(code=1) from exc
    render_result(console, spec.model_dump(mode="json"))


@app.command("search")
def search_command(query: str, category: str | None = None) -> None:
    """Search tool names, titles, and descriptions."""
    from pyforge.registry import TOOL_SPECS
    from pyforge.ui.components import render_specs

    needle = query.casefold()
    specs = [
        spec
        for spec in TOOL_SPECS
        if (category is None or spec.category == category)
        and needle in " ".join((spec.name, spec.title, spec.description)).casefold()
    ]
    if not specs:
        console.print("No matching tools found.", style="yellow")
        raise typer.Exit(code=1)
    render_specs(console, specs)


@app.command("run")
def run_command(name: str, arguments: str = "{}") -> None:
    """Run a registered tool with JSON keyword arguments."""
    from pyforge.registry import get_tool, load_callable
    from pyforge.ui.components import render_result

    try:
        values = _parse_arguments(arguments)
        import time
        from pyforge.config import load_settings
        from pyforge.storage.history import HistoryService

        started = time.perf_counter()
        success = False
        try:
            result = load_callable(get_tool(name))(**values)
            success = True
            render_result(console, result)
        finally:
            settings = load_settings()
            if settings.history_enabled:
                HistoryService().try_record(name, success, (time.perf_counter() - started) * 1000)
    except Exception as exc:
        console.print(f"Error: {exc}", style="bold red")
        raise typer.Exit(code=1) from exc


@app.command("interactive")
def interactive_command() -> None:
    """Open the Rich interactive menu."""
    from pyforge.ui.menu import interactive_menu

    interactive_menu(console)


@app.command("history")
def history_command(limit: int = 50) -> None:
    """Display recent local tool execution metadata."""
    from pyforge.storage.history import HistoryService
    from pyforge.ui.components import render_result

    render_result(console, HistoryService().list(limit))


@app.command("clear-history")
def clear_history_command(confirm: bool = typer.Option(False, "--yes")) -> None:
    """Clear local execution history after explicit confirmation."""
    from pyforge.storage.history import HistoryService

    if not confirm:
        console.print("Pass --yes to confirm history deletion.", style="yellow")
        raise typer.Exit(code=2)
    console.print(f"Cleared {HistoryService().clear()} history row(s).")


@app.command("settings")
def settings_command() -> None:
    """Display validated application settings."""
    from pyforge.config import load_settings
    from pyforge.ui.components import render_result

    render_result(console, load_settings().model_dump(mode="json"))


@app.command("set-setting")
def set_setting_command(key: str, value: str) -> None:
    """Update one validated application setting."""
    import json
    from pyforge.config import load_settings, save_settings
    from pyforge.models import Settings

    settings = load_settings().model_dump(mode="json")
    if key not in settings:
        console.print(f"Unknown setting: {key}", style="red")
        raise typer.Exit(code=2)
    try:
        settings[key] = json.loads(value)
    except json.JSONDecodeError:
        settings[key] = value
    try:
        validated = Settings.model_validate(settings)
    except PydanticValidationError as exc:
        console.print(f"Invalid value for {key}: {exc.errors()[0]['msg']}", style="red")
        raise typer.Exit(code=2) from exc
    save_settings(validated)
    console.print(f"Updated {key}.")


@app.command("export")
def export_command(name: str, arguments: str = "{}", format: str = "json", output: str | None = None) -> None:
    """Run a tool and export its result as txt, JSON, or CSV."""
    from pathlib import Path
    from pyforge.registry import get_tool, load_callable
    from pyforge.services.exporter import export_csv, export_json, export_txt

    try:
        values = _parse_arguments(arguments)
        exporters = {"txt": export_txt, "json": export_json, "csv": export_csv}
        if format not in exporters:
            console.print("Format must be txt, json, or csv.", style="red")
            raise typer.Exit(code=2)
        result = load_callable(get_tool(name))(**values)
        target = Path(output or f"exports/{name.replace('.', '-')}.{format}")
        console.print(f"Exported to {exporters[format](result, target)}")
    except typer.Exit:
        raise
    except Exception as exc:
        console.print(f"Error: {exc}", style="bold red")
        raise typer.Exit(code=1) from exc
