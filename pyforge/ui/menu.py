from __future__ import annotations

import json
from typing import Any

from rich.console import Console
from rich.prompt import IntPrompt, Prompt

from pyforge.registry import TOOL_SPECS, load_callable
from pyforge.ui.banner import banner
from pyforge.ui.components import render_result

CATEGORIES = ["files", "text", "encoding", "hashing", "json_tools", "network", "system", "developer", "git", "security"]


def interactive_menu(console: Console) -> None:
    while True:
        console.print(banner())
        for index, category in enumerate(CATEGORIES, 1):
            console.print(f"[{index}] {category.replace('_', ' ').title()} Tools")
        console.print("[11] History\n[12] Settings\n[0] Exit")
        choice = IntPrompt.ask("Choose", default=0)
        if choice == 0:
            return
        if choice not in range(1, 11):
            console.print("Use the dedicated history or settings commands for that section.", style="yellow")
            continue
        category = CATEGORIES[choice - 1]
        specs = [spec for spec in TOOL_SPECS if spec.category == category]
        for index, spec in enumerate(specs, 1):
            console.print(f"[{index}] {spec.title} - {spec.description}")
        selected = IntPrompt.ask("Tool", default=1)
        if selected not in range(1, len(specs) + 1):
            console.print("Invalid tool selection", style="red")
            continue
        raw = Prompt.ask("Arguments as JSON object", default="{}", password=specs[selected - 1].sensitive_input)
        try:
            arguments: dict[str, Any] = json.loads(raw)
            render_result(console, load_callable(specs[selected - 1])(**arguments))
        except Exception as exc:
            console.print(f"Error: {exc}", style="bold red")
