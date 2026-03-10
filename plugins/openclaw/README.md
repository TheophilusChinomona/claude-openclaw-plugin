# OpenClaw Plugin for Claude Code

Set up and manage your OpenClaw self-hosted AI gateway from Claude Code.

## Prerequisites

- **Node.js 22+** (for OpenClaw CLI)
- **OpenClaw CLI** installed (`npm install -g openclaw@latest`)

## What's Included

### Skills (19)
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
- **openclaw-outreach-setup** - Outreach agent scaffolding, cold email pipeline, human voice standard, prompt injection protection
- **openclaw-agent-builder** - Design and deploy OpenClaw agents end-to-end: interview, workspace file generation, guardrails, acceptance tests
- **openclaw-autonomy-audit** - Audit and score agent autonomy readiness, identify gaps preventing independent operation
- **openclaw-docs** - Documentation sources, crawled doc access, sync system knowledge

### Slash Commands (17)
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
- `/oc-outreach` - Scaffold and manage outreach agent — setup, show, validate
- `/oc-autonomy` - Audit agent autonomy readiness with scored assessment and interactive fix mode
- `/oc-docs` - Fetch, search, and manage OpenClaw documentation from upstream sources

### Agents (2)
- **openclaw-ops** - Auto-triggers on OpenClaw management questions (red, sonnet)
- **openclaw-docs-sync** - Fetches and syncs OpenClaw documentation from upstream (blue, sonnet)

## Install

```bash
# From GitHub (recommended)
claude marketplace add --source github --repo TheophilusChinomona/claude-openclaw-plugin
claude plugin install openclaw@claude-openclaw-plugin
```

## Quick Start

```bash
# Then in Claude Code:
/oc-setup          # Install and configure OpenClaw
/oc-status         # Check gateway health
/oc-channel telegram setup  # Set up Telegram
```
