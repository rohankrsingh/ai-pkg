import subprocess
import logging
import typer
import shutil

logger = logging.getLogger(__name__)

def install_packages(pkgs, dry_run=False, auto_yes=False, aur_helper="yay"):
    if not pkgs:
        typer.secho("⚠️ No packages suggested", fg=typer.colors.YELLOW)
        return

    # Split official pacman packages and AUR packages prefixed with 'aur:'
    pacman_pkgs = [p for p in pkgs if not str(p).startswith("aur:")]
    aur_pkgs = [str(p)[4:] for p in pkgs if str(p).startswith("aur:")]

    # Install official packages with pacman --needed
    if pacman_pkgs:
        pacman_cmd = ["sudo", "pacman", "-S", "--needed"]
        if auto_yes:
            pacman_cmd.append("--noconfirm")
        pacman_cmd.extend(pacman_pkgs)

        if dry_run:
            typer.secho(f"[DRY RUN] Would run: {' '.join(pacman_cmd)}", fg=typer.colors.MAGENTA)
        else:
            try:
                subprocess.run(pacman_cmd, check=True)
            except subprocess.CalledProcessError as e:
                typer.secho(f"❌ pacman failed (exit {e.returncode}). See output above.", fg=typer.colors.RED)
                logger.exception('pacman command failed')
                return

    # Install AUR packages using yay or paru
    if aur_pkgs:
        if aur_helper not in ("yay", "paru"):
            typer.secho(f"❌ Invalid aur_helper: {aur_helper}. Must be 'yay' or 'paru'", fg=typer.colors.RED)
            return
        helper_path = shutil.which(aur_helper)
        if not helper_path:
            typer.secho(f"⚠️ '{aur_helper}' not found in PATH. Skipping AUR packages: " + ", ".join(aur_pkgs), fg=typer.colors.YELLOW)
        else:
            aur_cmd = [aur_helper, "-S", "--needed"]
            if auto_yes:
                aur_cmd.append("--noconfirm")
            aur_cmd.extend(aur_pkgs)

            if dry_run:
                typer.secho(f"[DRY RUN] Would run: {' '.join(aur_cmd)}", fg=typer.colors.MAGENTA)
            else:
                try:
                    subprocess.run(aur_cmd, check=True)
                except subprocess.CalledProcessError as e:
                    typer.secho(f"❌ {aur_helper} failed (exit {e.returncode}). See output above.", fg=typer.colors.RED)
                    logger.exception(f'{aur_helper} command failed')
                    return