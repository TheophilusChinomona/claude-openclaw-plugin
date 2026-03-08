# OpenClaw Plugin for Claude Code

Set up and manage your OpenClaw self-hosted AI gateway from Claude Code.

## Prerequisites

- **Node.js 22+** (for OpenClaw CLI)
- **OpenClaw CLI** installed (`npm install -g openclaw@latest`)

## What's Included

### Skills (15)
- **openclaw-setup** - Installation, onboarding wizard, service setup
- **openclaw-config** - Configuration reference, CLI commands, environment variables
- **openclaw-channels** - Channel setup (Telegram, WhatsApp, Discord, Slack), DM policies
- **openclaw-troubleshooting** - Diagnostics, common issues, decision trees
- **openclaw-multi-agent** - Multi-agent routing, bindings, per-agent sandboxing
- **openclaw-multi-user-workspaces** - Multi-user access, session isolation, pairing, trust model
- **openclaw-agent-teams** - Agent team design, SOUL.md authoring, hierarchy, memory architecture
- **openclaw-multi-agent-team-setup** - End-to-end multi-agent team orchestration, commander-specialist routing, mention gating, dual-track governance
- **openclaw-workspace-structure** - Workspace directory structure and conventions
- **openclaw-automation** - Cron jobs, webhooks/hooks, heartbeat, event-driven automation
- **openclaw-sessions** - Session management, DM scope, resets, compaction, thread bindings, identity links
- **openclaw-models** - Model selection, provider setup, API keys, failover, auth profiles
- **openclaw-security** - Security audit, hardening, secrets management, incident response
- **openclaw-sandboxing** - Docker sandbox configuration, container isolation, bind mounts, sandbox browser
- **openclaw-nodes** - Device pairing, remote execution, exec routing, node commands

### Slash Commands (14)
- `/oc-status` - Quick gateway health check
- `/oc-doctor` - Run diagnostics and auto-fix
- `/oc-config` - View or edit configuration
- `/oc-setup` - Guided installation and setup
- `/oc-channel` - Channel management
- `/oc-logs` - View gateway logs
- `/oc-team` - Scaffold and manage agent team workspace
- `/oc-workspace` - Multi-user workspace access, pairing, sessions, security audit
- `/oc-structure` - Workspace structure and conventions
- `/oc-cron` - Manage cron jobs (list, add, run, history, remove)
- `/oc-security` - Run security audit with severity grouping and auto-fix
- `/oc-backup` - Backup configuration, credentials, and auth profiles
- `/oc-update` - Update OpenClaw, run diagnostics, restart gateway
- `/oc-improve` - Scan setup and suggest improvements based on available skills and commands

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
