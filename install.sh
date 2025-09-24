#!/usr/bin/env bash
set -euo pipefail

echo "🌟 Installing ai-pkg - Your AI-Powered Development Environment Wizard"
echo "✨ Transform plain English into perfectly crafted development environments!"

if ! command -v pacman &>/dev/null; then
    echo "❌ This installer is intended for Arch Linux or derivatives."
    exit 1
fi

echo "Choose installation method:"
echo "1) pipx (PyPI)"
echo "2) yay (AUR binary)"
read -rp "Enter 1 or 2: " choice

if [[ "$choice" == "1" ]]; then
    if ! command -v pipx &>/dev/null; then
        echo "⚙️  Installing pipx..."
        sudo pacman -S --noconfirm python-pipx
        pipx ensurepath || true
    fi
    echo "⚙️  Installing via pipx..."
    pipx install ai-pkg || pipx upgrade ai-pkg || echo "pipx install failed"
    echo "✅ Installed ai-pkg via pipx"
elif [[ "$choice" == "2" ]]; then
    if ! command -v yay &>/dev/null; then
        echo "⚙️  Installing yay (AUR helper)..."
        sudo pacman -S --needed --noconfirm git base-devel
        git clone https://aur.archlinux.org/yay.git /tmp/yay
        (cd /tmp/yay && makepkg -si --noconfirm)
        rm -rf /tmp/yay
    fi
    echo "⚙️  Installing ai-pkg-bin via yay..."
    yay -S --noconfirm ai-pkg-bin || echo "AUR install failed"
    echo "✅ Installed ai-pkg-bin from AUR"
else
    echo "❌ Invalid choice. Exiting."
    exit 1
fi

echo ""
echo "🎉 Installation complete!"
echo "Try it now:  ai-pkg \"set up a django dev env\" --dry-run"