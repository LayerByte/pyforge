from rich.align import Align
from rich.panel import Panel
from rich.text import Text


def banner() -> Panel:
    title = Text("PYFORGE", style="bold cyan")
    subtitle = Text("Developer & System Utility Toolkit", style="white")
    return Panel(Align.center(Text.assemble(title, "\n", subtitle)), border_style="cyan")
