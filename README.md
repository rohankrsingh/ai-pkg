# ai-pkg

AI-powered package recommender and installer for Arch Linux

## Usage

```bash
# Preview what would be installed
ai-pkg "set up a django dev env" --dry-run

# Install with yay (default)


# Install with paru (if you prefer paru)
## Installation

# Or set the helper globally
export AI_PKG_AUR_HELPER=paru
ai-pkg "install something from aur"
```

## Options
- `--dry-run`   : Preview commands without running them
- `--yes`       : Auto-confirm all prompts
- `--run-env`   : Run environment setup steps automatically
- `--aur-helper`: Choose AUR helper (`yay` or `paru`, default: yay; can also set `AI_PKG_AUR_HELPER` env var)

## Installation
- See `install.sh` for Arch Linux or use pipx:
```bash
pipx install --editable .
```
- See `install.sh` for Arch Linux or use pipx:
```bash
pipx install --editable .
```

## Development
- Run tests: `pytest`
- Lint: `flake8 src` and `black --check src`

## Updating

**If installed with pipx (PyPI):**
```bash
pipx upgrade ai-pkg
```

**If installed from the AUR:**
```bash
yay -Syu ai-pkg-bin
# or
paru -Syu ai-pkg-bin
```

**If installed from source (editable):**
```bash
cd ai-pkg
git pull
pipx install --editable .
```

**If using install.sh:**
```bash
./install.sh
```

## License
MIT (add LICENSE file)
