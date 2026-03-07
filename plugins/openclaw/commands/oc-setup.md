---
description: Guided OpenClaw installation and initial setup
argument-hint:
allowed-tools: Bash, Read, Write
---

# /oc-setup Command

Guide the user through installing and setting up OpenClaw.

## Execution

### Step 1: Check if OpenClaw is installed

```bash
which openclaw && openclaw --version
```

### Step 2: If not installed, guide installation

Detect the platform:
```bash
uname -s
```

Then recommend the appropriate installer:

**macOS / Linux / WSL2:**
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

**Windows (PowerShell):**
```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

**npm (manual):**
```bash
npm install -g openclaw@latest
```

### Step 3: If installed, check status

```bash
openclaw status
openclaw gateway status
```

### Step 4: Run onboarding if needed

If OpenClaw is installed but not configured:
```bash
openclaw onboard --install-daemon
```

### Step 5: Optionally set up a channel

Ask the user which channel they want to connect first (Telegram is fastest).
Guide them through the channel-specific setup using the openclaw-channels skill knowledge.

### Step 6: Verify

```bash
openclaw doctor
openclaw channels status --probe
```

## Notes

- Always check Node.js version: `node --version` (22+ required)
- For sharp build errors: `SHARP_IGNORE_GLOBAL_LIBVIPS=1 npm install -g openclaw@latest`
- For Linux: remind about `sudo loginctl enable-linger $USER` for persistent service
