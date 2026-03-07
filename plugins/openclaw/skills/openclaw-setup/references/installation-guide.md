# OpenClaw Installation Guide

## Platform-Specific Installation

### macOS

**Via installer:**
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

**What it does:**
1. Detects or installs Node.js 22+
2. Runs `npm install -g openclaw@latest`
3. Launches `openclaw onboard --install-daemon`
4. Installs LaunchAgent for auto-start on login

**macOS App Onboarding (separate flow):**
1. System Permissions - approves macOS warnings + Local Networks
2. Security Notice - explains trust model
3. Gateway Choice: This Mac (Local) / Remote (SSH/Tailnet) / Configure later
4. TCC Permissions - Automation, Notifications, Accessibility, Screen Recording, Microphone, Speech Recognition, Camera, Location
5. CLI Installation - optional global `openclaw` CLI via npm
6. Onboarding Chat - agent introduces itself

### Linux / WSL2

**Via installer:**
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

**Post-install for always-on service:**
```bash
sudo loginctl enable-linger $USER
```

Verify lingering:
```bash
loginctl show-user $USER | grep Linger
```

For always-on/multi-user servers, consider a system-level systemd service.

### Windows

**Strongly recommend WSL2.** Native Windows is not officially supported for the gateway.

**PowerShell (CLI only):**
```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

Skip onboarding:
```powershell
& ([scriptblock]::Create((iwr -useb https://openclaw.ai/install.ps1))) -NoOnboard
```

### Docker / Podman

For containerized/headless deployments. Run `setup-podman.sh` once for Podman, then use the launch script.

### Build from Source

```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm ui:build
pnpm build
pnpm link --global
openclaw onboard --install-daemon
```

Or run without linking: `pnpm openclaw ...` from inside the repo.

## Onboarding Wizard Walkthrough

### QuickStart Mode (Default)

Sensible defaults applied automatically:
- Local gateway on loopback (127.0.0.1:18789)
- Gateway auth via auto-generated token
- Tool policy: `messaging` (restricted)
- DM isolation: `per-channel-peer`
- Tailscale: off
- Telegram + WhatsApp DMs: allowlist mode

### Advanced Mode

Every configuration step exposed. Accessible when wizard detects existing config or via flag.

### Step-by-Step

**1. Model/Auth**
- Choose provider: Anthropic, OpenAI, Perplexity, Brave, Gemini, Grok, Kimi, Custom
- Enter API key (plaintext or env var reference via `ref` mode)
- Custom providers: OpenAI-compatible, Anthropic-compatible, or auto-detect
- For custom endpoint: base URL, API key, model ID, endpoint ID

**2. Workspace**
- Location for agent files (default: `~/.openclaw/workspace`)
- Seeds bootstrap files (SOUL.md, AGENTS.md, etc.)

**3. Gateway**
- Port (default: 18789)
- Bind address (default: loopback)
- Auth mode: Token (auto-generated) or Password
- Tailscale exposure toggle
- Token storage: plaintext or SecretRef (env var / file / exec backed)
- Non-interactive: `--gateway-token-ref-env <ENV_VAR>`

**4. Channels**
- Optional: WhatsApp, Telegram, Discord, Google Chat, Mattermost, Signal, BlueBubbles, iMessage
- Each channel configured with allowlist/blocklist for DMs

**5. Daemon**
- LaunchAgent on macOS / systemd user unit on Linux
- Validates token SecretRef before persisting
- Blocks install if token is unresolved or auth config incomplete

**6. Health Check**
- Starts gateway, verifies it's running

**7. Skills**
- Installs recommended skills and optional dependencies

### Web Search Configuration (Optional)

Provider options: Perplexity, Brave, Gemini, Grok, Kimi. Configure later with:
```bash
openclaw configure --section web
```

## Verification Commands

```bash
openclaw status              # Quick health check
openclaw gateway status      # Service status (running/stopped)
openclaw doctor              # Config validation and diagnostics
openclaw health              # Detailed health check
openclaw dashboard           # Open Control UI in browser (http://127.0.0.1:18789/)
```

Manual gateway start (foreground, for testing):
```bash
openclaw gateway --port 18789
```

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `OPENCLAW_HOME` | Override base directory for all internal paths |
| `OPENCLAW_STATE_DIR` | Override state location (default `~/.openclaw`) |
| `OPENCLAW_CONFIG_PATH` | Override config file location |
| `OPENCLAW_LOG_LEVEL` | Override log level (debug, trace, etc.) |

Precedence: CLI flags > env vars > defaults.

## Troubleshooting Installation

### `openclaw` command not found
```bash
node -v && npm -v && npm prefix -g && echo "$PATH"
export PATH="$(npm prefix -g)/bin:$PATH"
```

### Sharp build errors
```bash
SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm install -g openclaw@latest
```

### pnpm build scripts not approved
```bash
pnpm approve-builds -g
```

### Token/auth not resolved
- Set environment variable before daemon install
- Or use plaintext token (simpler but less secure)
- Or use `--gateway-token-ref-env <ENV_VAR>` for non-interactive mode

### Both token and password configured
Explicitly set `gateway.auth.mode` to either `"token"` or `"password"`.

### systemd stops on logout (Linux)
```bash
sudo loginctl enable-linger $USER
loginctl show-user $USER | grep Linger
```

### Invalid/legacy config keys
```bash
openclaw doctor          # identifies issues
openclaw doctor --fix    # auto-repair
```
