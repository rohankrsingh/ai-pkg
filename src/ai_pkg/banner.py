from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.align import Align

from . import __version__

console = Console()

def show_banner():
    """Compact, small banner that clearly shows 'ai-pkg' and usage hints."""
    title = f"ai-pkg v{__version__}"

    art = Text()
    art.append("ai-pkg\n", style="bold magenta")
    art.append("AI package recommender for Arch Linux\n", style="cyan")
    art.append("\n")
    art.append("Usage: ", style="bold yellow")
    art.append('ai-pkg "setup django dev"', style="yellow")
    art.append("\n")
    art.append("Options: --dry-run (preview)  •  --yes (auto-confirm)\n", style="dim")

    panel = Panel(
        Align.center(art),
        title=f"[bold green]{title}[/bold green]",
        border_style="bright_blue",
        expand=False,
    )

    console.print(panel)
