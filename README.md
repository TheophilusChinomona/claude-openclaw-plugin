# OpenClaw Plugin for Claude Code

Set up and manage your [OpenClaw](https://openclaw.ai) self-hosted AI gateway from Claude Code.

OpenClaw connects messaging apps (WhatsApp, Telegram, Discord, Slack) to AI coding agents. This plugin gives Claude Code full knowledge of OpenClaw's setup, configuration, troubleshooting, multi-agent teams, security, and automation.

## Install

Run these commands **in Claude Code** (type them in the chat):

```
/plugin marketplace add TheophilusChinomona/claude-openclaw-plugin
/plugin install openclaw@claude-openclaw-plugin
```

**Important:** Add the marketplace using the GitHub repo above (not a raw URL to `marketplace.json`). That way the plugin installs and updates correctly.

## Updating

To get the latest version of the plugin:

1. In Claude Code, run: `/plugin marketplace update`
2. Reinstall the plugin: `/plugin install openclaw@claude-openclaw-plugin` (or uninstall it, then install again)
3. Restart Claude Code if the new version doesn’t load

If you still don’t see updates, try closing and reopening Claude Code, or remove the cached plugin (e.g. the folder for this plugin under `~/.claude/plugins/cache/`) and install again.

## Post-Install: Set Up Permissions

Run this once after installing to avoid repeated permission prompts:

```bash
node plugins/openclaw/scripts/setup-permissions.js
```

This adds recommended tool permissions (Read, Write, Bash patterns) to your Claude Code allowlist.

## Prerequisites

- **Node.js 22+** (for OpenClaw CLI)
- **OpenClaw CLI** installed (`npm install -g openclaw@latest`)

## What's Included

### Agents (4)

- **openclaw-ops** — Auto-triggers on OpenClaw management questions (model: sonnet)
- **openclaw-docs-sync** — Fetches and syncs documentation from upstream sources (model: sonnet)
- **openclaw-agent-architect** — Build or optimize agent workspace files (SOUL, IDENTITY, AGENTS, MEMORY, GOALS) via interview or scan (model: sonnet)
- **openclaw-agent-planner** — Brainstorm, design, and document agent teams; produce Agent Team Documentation (model: sonnet)

### Slash Commands (22)

| Command | Description |
|---------|-------------|
| `/oc-status` | Quick gateway health check |
| `/oc-doctor` | Run diagnostics and auto-fix |
| `/oc-config` | View or edit configuration |
| `/oc-setup` | Guided installation and setup |
| `/oc-channel` | Channel management |
| `/oc-logs` | View gateway logs |
| `/oc-team` | Scaffold and manage agent team workspace |
| `/oc-workspace` | Multi-user workspace access, pairing, sessions |
| `/oc-structure` | Workspace structure and conventions |
| `/oc-cron` | Manage cron jobs (list, add, run, history, remove) |
| `/oc-security` | Run security audit with severity grouping and auto-fix |
| `/oc-backup` | Backup configuration, credentials, and auth profiles |
| `/oc-update` | Update OpenClaw, run diagnostics, restart gateway |
| `/oc-improve` | Scan setup and suggest improvements |
| `/oc-outreach` | Scaffold and manage outreach agent |
| `/oc-autonomy` | Audit agent autonomy readiness with scored assessment |
| `/oc-docs` | Fetch, search, and manage OpenClaw documentation |
| `/oc-memory` | Initialize, audit, flush, and search agent memory |
| `/oc-architect` | Build or optimize agent workspace files (SOUL, IDENTITY, AGENTS, MEMORY, GOALS) |
| `/oc-planner` | Brainstorm, design, and document agent teams; produce Agent Team Documentation |
| `/oc-wizard` | Full guided journey to create a complete agent workspace (discovery → design → scaffold → audit) |
| `/oc-workspace-audit` | Comprehensive scored audit of workspace quality (SOUL, IDENTITY, AGENTS, memory, config) |

### Skills (24)

| Skill | Domain |
|-------|--------|
| openclaw-setup | Installation, onboarding wizard, service setup |
| openclaw-config | Configuration reference, CLI commands, environment variables |
| openclaw-channels | Channel setup (Telegram, WhatsApp, Discord, Slack), DM policies |
| openclaw-troubleshooting | Diagnostics, common issues, decision trees |
| openclaw-multi-agent | Multi-agent routing, bindings, per-agent sandboxing |
| openclaw-multi-user-workspaces | Multi-user access, session isolation, pairing, trust model |
| openclaw-agent-teams | Agent team design, SOUL.md authoring, hierarchy, memory |
| openclaw-multi-agent-team-setup | End-to-end team orchestration, commander-specialist routing |
| openclaw-workspace-structure | Workspace directory structure and conventions |
| openclaw-automation | Cron jobs, webhooks/hooks, heartbeat, event-driven automation |
| openclaw-sessions | Session management, DM scope, resets, compaction, thread bindings |
| openclaw-models | Model selection, provider setup, API keys, failover, auth profiles |
| openclaw-security | Security audit, hardening, secrets management, incident response |
| openclaw-sandboxing | Docker sandbox, container isolation, bind mounts, sandbox browser |
| openclaw-nodes | Device pairing, remote execution, exec routing, node commands |
| openclaw-outreach-setup | Outreach agent scaffolding, cold email pipeline |
| openclaw-agent-builder | Design and deploy agents end-to-end: interview, workspace files, guardrails |
| openclaw-agent-architect | Build and optimize SOUL/IDENTITY/AGENTS/MEMORY/GOALS via interview and scan |
| openclaw-agent-planner | Brainstorm, design, document agent teams; permissions and roadmap |
| openclaw-autonomy-audit | Audit and score agent autonomy readiness |
| openclaw-docs | Documentation sources, crawled doc access, sync system |
| openclaw-memory | Memory setup, four-layer model, shared memory, SCRIBE compression |
| openclaw-workspace-audit | Comprehensive scored workspace quality audit (200-point rubric) |
| openclaw-workspace-wizard | Full guided workspace creation journey (6 phases with checkpoints) |

## Quick Start

```bash
# After installation:
/oc-setup          # Install and configure OpenClaw
/oc-status         # Check gateway health
/oc-channel telegram setup  # Set up Telegram
/oc-team create my-team     # Scaffold an agent team
```

## Development

For local development, add the marketplace from the cloned repo directory (the folder that contains `.claude-plugin/marketplace.json`). Run in Claude Code:

```
/plugin marketplace add /path/to/openclaw-plugin
/plugin install openclaw@claude-openclaw-plugin
```

Validate plugin structure (from the repo root in a terminal):

```bash
claude plugin validate .
```

## License

MIT
