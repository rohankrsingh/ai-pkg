#!/usr/bin/env bash
set -euo pipefail

# Uninstall ai-pkg from pipx, yay, paru, or pip

echo "🧹 Uninstalling ai-pkg..."

# Try pipx uninstall
if command -v pipx &>/dev/null && pipx list | grep -q ai-pkg; then
    echo "Removing ai-pkg via pipx..."
    pipx uninstall ai-pkg || true
fi

# Try yay uninstall
if command -v yay &>/dev/null && yay -Q ai-pkg-bin &>/dev/null; then
    echo "Removing ai-pkg-bin via yay..."
    yay -Rns --noconfirm ai-pkg-bin || true
fi

# Try paru uninstall
if command -v paru &>/dev/null && paru -Q ai-pkg-bin &>/dev/null; then
    echo "Removing ai-pkg-bin via paru..."
    paru -Rns --noconfirm ai-pkg-bin || true
fi

# Try pip uninstall (editable/dev mode)
if python3 -m pip show ai-pkg &>/dev/null; then
    echo "Removing ai-pkg via pip..."
    python3 -m pip uninstall -y ai-pkg || true
fi

echo "✅ Uninstall complete. If you set GEMINI_API_KEY in your shell profile, you may want to remove it manually."
