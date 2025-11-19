import logging
import typer
import os
import subprocess
from typing import Optional
from . import backends, core
from .banner import show_banner

logging.basicConfig(level=logging.WARNING)

app = typer.Typer(help="AI-powered package recommender for Arch Linux.")

@app.command()
def main(
    goal: str = typer.Argument(..., help="Describe what you want to set up"),
    api_key: Optional[str] = typer.Option(None, help="GEMINI API key (or set GEMINI_API_KEY env var)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Preview without installing"),
    yes: bool = typer.Option(False, "--yes", help="Auto-confirm installation"),
    run_env: bool = typer.Option(False, "--run-env", help="Automatically run environment setup steps without prompting"),
    aur_helper: str = typer.Option(None, "--aur-helper", help="AUR helper to use (yay or paru, default yay; can also set AI_PKG_AUR_HELPER env var)"),
):
    show_banner()

    if not api_key:
        api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        typer.echo("❌ GEMINI_API_KEY required. Set env var or pass --api-key")
        raise typer.Exit(1)

    # Determine AUR helper: CLI > env > default
    aur_helper_final = aur_helper or os.environ.get("AI_PKG_AUR_HELPER", "yay")
    if aur_helper_final not in ("yay", "paru"):
        typer.secho(f"❌ Invalid --aur-helper: {aur_helper_final}. Must be 'yay' or 'paru'", fg=typer.colors.RED)
        raise typer.Exit(1)

    result = backends.suggest_with_gemini(goal, api_key)

    # Backwards-compatible: result can be a simple list of packages, or
    # a dict with keys 'packages' and optional 'env_steps'.
    pkgs = []
    env_steps = []
    if isinstance(result, list):
        pkgs = result
    elif isinstance(result, dict):
        pkgs = result.get("packages", []) or []
        env_steps = result.get("env_steps", []) or []
    else:
        typer.secho("⚠️ Unexpected response shape from AI. Aborting.", fg=typer.colors.RED)
        raise typer.Exit(1)

    typer.secho(f"\n📦 Suggested packages: {', '.join(pkgs)}", fg=typer.colors.CYAN, bold=True)

    if env_steps:
        typer.secho("\n🔧 Recommended environment setup steps:", fg=typer.colors.GREEN, bold=True)
        for i, cmd in enumerate(env_steps, start=1):
            typer.secho(f"  {i}. {cmd}", fg=typer.colors.WHITE)

        if dry_run:
            typer.secho("\n[DRY RUN] Would run env steps above.", fg=typer.colors.MAGENTA)
        else:
            should_run_env = run_env or yes
            if not should_run_env:
                # Ask the user interactively
                should_run_env = typer.confirm("Run the environment setup steps now?")
                if should_run_env:
                    # Run environment setup steps in a single shell session so that
                    # activation (source / .) affects subsequent commands. When we
                    # previously ran each command in its own subprocess, the venv
                    # activation didn't persist and later `pip install` used the
                    # system pip (triggering PEP 668 'externally-managed-environment').
                    # Combining with && preserves state across the sequence.
                    combined = " && ".join(env_steps)
                    typer.secho(f"Running: {combined}", fg=typer.colors.YELLOW)
                    # Use bash so `source` and `.` are available as builtins.
                    result = subprocess.run(combined, shell=True, executable="/bin/bash")
                    if result.returncode != 0:
                        typer.secho("❌ Environment setup steps failed.", fg=typer.colors.RED)
                        raise typer.Exit(result.returncode)

    if dry_run:
        core.install_packages(pkgs, dry_run=True, auto_yes=yes, aur_helper=aur_helper_final)
        return

    if not yes:
        confirm = typer.confirm("Do you want to proceed with installation?")
        if not confirm:
            typer.echo("Aborting installation.")
            raise typer.Exit(0)

    core.install_packages(pkgs, dry_run=False, auto_yes=yes, aur_helper=aur_helper_final)