#!/usr/bin/env bash
set -euo pipefail

echo "🌟 Installing ai-pkg - Your AI-Powered Development Environment Wizard"
echo "✨ Transform plain English into perfectly crafted development environments!"

if ! command -v pacman &>/dev/null; then
    echo "❌ This installer is intended for Arch Linux or derivatives."
    exit 1
fi

echo "Choose installation method:"
echo "1) yay (AUR binary)"
echo "2) Local virtualenv (installs a venv under ~/.local/ai-pkg and a shim in ~/.local/bin)"
read -rp "Enter 1 or 2: " choice

if [[ "$choice" == "1" ]]; then
    # AUR install via yay
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
elif [[ "$choice" == "2" ]]; then
    # Local venv install
    echo "⚙️  Installing into a local virtualenv..."

    repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    venv_dir="$HOME/.local/ai-pkg/.venv"
    bin_shim="$HOME/.local/bin/ai-pkg"

    mkdir -p "$(dirname "$bin_shim")"
    mkdir -p "$(dirname "$venv_dir")"

    echo "Creating virtualenv at $venv_dir"
    python -m venv "$venv_dir"

    echo "Installing package in editable mode into the venv"
    # Use the venv's pip to install the package from the repository root
    "$venv_dir/bin/python" -m pip install --upgrade pip
    "$venv_dir/bin/python" -m pip install -e "$repo_root" || {
        echo "❌ Failed to install package into venv"
        exit 1
    }

    # Create a small shim so `ai-pkg` is available on PATH via ~/.local/bin
    cat > "$bin_shim" <<EOF
#!/usr/bin/env bash
exec "$venv_dir/bin/ai-pkg" "\$@"
EOF
    chmod +x "$bin_shim"

    echo "✅ Installed ai-pkg into local venv: $venv_dir"
    echo "Shim created at: $bin_shim"
    if ! command -v ai-pkg &>/dev/null; then
        echo "Note: ensure ~/.local/bin is in your PATH to run 'ai-pkg' directly."
    fi
else
    echo "❌ Invalid choice. Exiting."
    exit 1
fi

echo ""
echo "🎉 Installation complete!"
echo "Try it now:  ai-pkg \"set up a django dev env\" --dry-run"