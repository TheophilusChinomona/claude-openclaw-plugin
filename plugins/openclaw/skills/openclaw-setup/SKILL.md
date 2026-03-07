---
name: openclaw-setup
description: >
  Use when the user wants to install OpenClaw, set up OpenClaw, onboard OpenClaw,
  get started with OpenClaw, run the OpenClaw installer, configure the OpenClaw daemon,
  or deploy OpenClaw on macOS, Linux, or WSL2.
---

# OpenClaw Installation & Setup

Guide the user through installing and configuring OpenClaw, a self-hosted gateway connecting messaging apps to AI coding agents.

## Prerequisites

- **Node.js 22+** required. Check with `node --version`.
- **OS**: macOS, Linux, or Windows (WSL2 strongly recommended over native Windows).

## Installation Methods

### Installer Script (Recommended)

Detects Node.js, installs if missing, installs the CLI globally via npm, and launches the onboarding wizard.

**macOS / Linux / WSL2:**
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

**Windows (PowerShell):**
```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

Skip onboarding (install CLI only):
```bash
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --no-onboard
```

### npm (Manual)

```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

If sharp build errors occur:
```bash
SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm install -g openclaw@latest
```

### pnpm

```bash
pnpm add -g openclaw@latest
pnpm approve-builds -g
openclaw onboard --install-daemon
```

### Build from Source

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install && pnpm ui:build && pnpm build
pnpm link --global
openclaw onboard --install-daemon
```

## Onboarding Wizard

Run `openclaw onboard --install-daemon` to start the interactive wizard. It configures:

1. **Model/Auth** - Choose provider (Anthropic, OpenAI, etc.), enter API key or use SecretRef for env-backed credentials.
2. **Workspace** - Set workspace directory (default: `~/.openclaw/workspace`).
3. **Gateway** - Configure port (default 18789), bind address, auth mode (token or password).
4. **Channels** - Optionally set up WhatsApp, Telegram, Discord, etc.
5. **Daemon** - Install as LaunchAgent (macOS) or systemd user service (Linux/WSL2).
6. **Health Check** - Starts gateway and verifies it's running.

Use `openclaw configure` to reconfigure later.

## Service Installation

### macOS (LaunchAgent)
Installed automatically by `openclaw onboard --install-daemon`. Auto-starts on login.

### Linux/WSL2 (systemd)
Installed as systemd user service. Enable lingering to survive logout:
```bash
sudo loginctl enable-linger $USER
```

## Verification

After install, verify with:
```bash
openclaw status            # Quick health check
openclaw gateway status    # Service status
openclaw doctor            # Config validation
openclaw dashboard         # Open browser UI
```

## Adding Another Agent

```bash
openclaw agents add <name>
```
Creates a separate agent with its own workspace, sessions, and auth profiles.

## Common Install Issues

- **Command not found**: Add npm global bin to PATH: `export PATH="$(npm prefix -g)/bin:$PATH"`
- **Sharp build errors**: Use `SHARP_IGNORE_GLOBAL_LIBVIPS=1` prefix
- **pnpm build scripts**: Run `pnpm approve-builds -g` after install
- **systemd stops on logout**: Enable lingering with `sudo loginctl enable-linger $USER`
- **Token not resolved**: Set the env var before daemon install, or use plaintext token

## Key Paths

| Path | Purpose |
|------|---------|
| `~/.openclaw/openclaw.json` | Main config file (JSON5) |
| `~/.openclaw/workspace/` | Agent workspace (skills, prompts) |
| `~/.openclaw/credentials/` | Channel auth data |
| `~/.openclaw/agents/` | Per-agent state and sessions |

See `references/installation-guide.md` for detailed per-platform steps.
