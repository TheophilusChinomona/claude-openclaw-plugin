# OpenClaw Plugin for Claude Code

Set up and manage your OpenClaw self-hosted AI gateway from Claude Code.

## Prerequisites

- **Node.js 22+** (for OpenClaw CLI)
- **OpenClaw CLI** installed (`npm install -g openclaw@latest`)

## What's Included

### Skills (5)
- **openclaw-setup** - Installation, onboarding wizard, service setup
- **openclaw-config** - Configuration reference, CLI commands, environment variables
- **openclaw-channels** - Channel setup (Telegram, WhatsApp, Discord, Slack), DM policies
- **openclaw-troubleshooting** - Diagnostics, common issues, decision trees
- **openclaw-multi-agent** - Multi-agent routing, bindings, per-agent sandboxing

### Slash Commands (6)
- `/oc-status` - Quick gateway health check
- `/oc-doctor` - Run diagnostics and auto-fix
- `/oc-config` - View or edit configuration
- `/oc-setup` - Guided installation and setup
- `/oc-channel` - Channel management
- `/oc-logs` - View gateway logs

### Agent (1)
- **openclaw-ops** - Auto-triggers on OpenClaw management questions (red, sonnet)

## Quick Start

```bash
# Install the plugin
claude marketplace add --source directory --path ~/.claude/plugins/openclaw-plugin --name openclaw-local
claude plugin install openclaw@openclaw-local

# Then in Claude Code:
/oc-setup          # Install and configure OpenClaw
/oc-status         # Check gateway health
/oc-channel telegram setup  # Set up Telegram
```
