<p align="center">
  <img src="https://raw.githubusercontent.com/rohankrsingh/ai-pkg/main/.github/assets/banner.png" alt="AI-PKG Banner" width="600"/>
</p>

<h1 align="center">🌟 ai-pkg</h1>

<p align="center">
  <strong>Your AI-Powered Development Environment Wizard for Arch Linux</strong>
</p>

<p align="center">
  <em>Transform plain English into perfectly crafted development environments ✨</em>
</p>

<p align="center">
  <code>Just tell it what you want to build, and let the AI magic happen! 🪄</code>
</p>

<p align="center">
  <a href="https://aur.archlinux.org/packages/ai-pkg-bin"><img src="https://img.shields.io/aur/version/ai-pkg-bin?style=flat-square&logo=arch-linux&label=AUR" alt="AUR version"/></a>
  <a href="https://github.com/rohankrsingh/ai-pkg/blob/main/LICENSE"><img src="https://img.shields.io/github/license/rohankrsingh/ai-pkg?style=flat-square" alt="License"/></a>
  <img src="https://img.shields.io/badge/Arch-Linux-1793D1?style=flat-square&logo=arch-linux" alt="Arch Linux"/>
  <img src="https://img.shields.io/badge/AI-Powered-00A67E?style=flat-square&logo=openai" alt="AI Powered"/>
</p>

<p align="center">
  <a href="#installation">Installation</a> •
  <a href="#setup">Setup</a> •
  <a href="#usage">Usage</a> •
  <a href="#options">Options</a> •
  <a href="#features">Features</a> •
  <a href="#updating">Updating</a>
</p>

## ✨ Why AIPkg?

- 🧠 **AI-Powered Intelligence**: Understands context and recommends the perfect package combinations
- 🎯 **Smart Package Selection**: No more manual package hunting - AI picks the right tools for your needs
- 🛠️ **Instant Environment Setup**: Turn ideas into ready-to-code environments in seconds
- � **Project Bootstrapping**: Creates and configures new projects with industry best practices
- ⚡ **AUR Superpowers**: Seamless integration with both official repos and AUR
- 🤝 **Flexible Installation**: Works with both `yay` and `paru` - your choice!
- 🧪 **Safe Preview Mode**: See exactly what will happen before making any changes
- 🎨 **Framework Agnostic**: Works with any tech stack - React, Vue, Django, Express, you name it!

## 📦 Installation

### Via AUR (Recommended)

Install directly from the AUR using your preferred helper:

```bash
# Using yay
yay -S ai-pkg-bin

# Using paru
paru -S ai-pkg-bin
```

### Via GitHub

Clone and install from source:

```bash
# Clone the repository
git clone https://github.com/rohankrsingh/ai-pkg.git
cd ai-pkg

# Run the installation script
./install.sh
```

To uninstall:
```bash
./uninstall.sh
```

## 🔧 Setup

Set up your Gemini API key (required):

```bash
export GEMINI_API_KEY=your_api_key_here
```

For permanent setup, add the above line to your `~/.bashrc` or `~/.zshrc`.

## 🚀 Usage

Experience the future of development setup - where your words become working environments instantly! 🚀

```bash
# Create a new React project with modern stack
ai-pkg "set up a react js app as test-app with tailwind, zod, react hook form"

# Set up a data science environment
ai-pkg "create a python data science environment with jupyter, pandas, and scikit-learn"

# Set up a development environment for backend
ai-pkg "set up nodejs backend environment with express, typescript and mongodb"

# Preview mode (shows what would be installed)
ai-pkg "set up a vue.js development environment" --dry-run
```

The AI will:
1. 📋 Analyze your requirements
2. 🎯 Select the appropriate packages
3. ⚙️ Configure the environment
4. 🚀 Set up the project structure (if requested)
5. 📝 Provide any necessary post-installation instructions

## ⚙️ Options

| Option | Description |
|--------|-------------|
| `--dry-run` | Preview commands without executing them |
| `--yes` | Auto-confirm all prompts |
| `--run-env` | Run environment setup steps automatically |
| `--aur-helper` | Choose AUR helper (`yay` or `paru`) |

Environment variables:
- `AI_PKG_AUR_HELPER`: Set default AUR helper (yay/paru)
- `GEMINI_API_KEY`: Your Gemini API key

## 🔄 Updating

Keep ai-pkg up to date using your AUR helper:

```bash
# Using yay
yay -Syu ai-pkg-bin

# Using paru
paru -Syu ai-pkg-bin
```

## 📝 License

MIT License • [View License](LICENSE)
