---
name: openclaw-multi-agent
description: >
  Use when the user wants to set up multiple agents, configure agent routing,
  understand OpenClaw bindings, add another agent, create separate workspaces,
  route messages to different agents, or configure per-agent sandboxing and
  tool policies.
---

# OpenClaw Multi-Agent Setup

Guide the user through configuring multiple agents with routing, isolation, and per-agent policies.

## Agent Concept

An agent in OpenClaw is an isolated brain with three components:

- **Workspace** - Contains personality files (`SOUL.md`, `AGENTS.md`, `USER.md`), local notes, and persona rules. Default working directory for tool execution.
- **State directory (`agentDir`)** - Stores auth profiles, model registry, and per-agent config at `~/.openclaw/agents/<agentId>/agent`. Auth profiles are per-agent and never shared automatically.
- **Session store** - Chat history at `~/.openclaw/agents/<agentId>/sessions`.

**Never reuse `agentDir` across agents** - causes auth/session collisions.

## Creating Agents

```bash
openclaw agents add work
```

This creates:
- Workspace at `~/.openclaw/workspace-work`
- State at `~/.openclaw/agents/work/agent`
- Sessions at `~/.openclaw/agents/work/sessions`

Verify: `openclaw agents list --bindings`

## Binding Rules (Message Routing)

Messages route to agents via deterministic, most-specific-wins bindings:

1. **Peer match** (exact DM/group ID) - highest priority
2. **Parent peer match** (thread inheritance)
3. **Guild ID + roles** (Discord)
4. **Guild ID** (Discord)
5. **Team ID** (Slack)
6. **Account ID** match
7. **Channel-level** (`accountId: "*"`)
8. **Default agent** fallback

If multiple bindings match the same tier, first in config order wins. Multiple fields in a binding use AND semantics.

```json5
{
  bindings: [
    // Most specific (peer) - wins over channel-wide
    { agentId: "opus", match: { channel: "whatsapp", peer: { kind: "direct", id: "+15551234567" } } },
    // Channel-wide fallback
    { agentId: "chat", match: { channel: "whatsapp" } },
  ],
}
```

## Per-Agent Configuration

```json5
{
  agents: {
    list: [
      {
        id: "work",
        workspace: "~/.openclaw/workspace-work",
        model: { primary: "anthropic/claude-opus-4-6" },
        identity: { name: "Work Bot" },
        groupChat: { mentionPatterns: ["@work", "@workbot"] },

        sandbox: {
          mode: "all",              // "off" | "non-main" | "all"
          scope: "agent",           // "session" | "agent" | "shared"
          workspaceAccess: "rw",
        },

        tools: {
          allow: ["read", "exec"],
          deny: ["browser", "cron"],
        },
      },
    ],
  },
}
```

## Common Patterns

### Home/Work Split
Route by WhatsApp account:
```json5
{
  bindings: [
    { agentId: "home", match: { channel: "whatsapp", accountId: "personal" } },
    { agentId: "work", match: { channel: "whatsapp", accountId: "biz" } },
  ],
}
```

### Channel Split
Fast model for WhatsApp, powerful for Telegram:
```json5
{
  agents: {
    list: [
      { id: "chat", model: { primary: "anthropic/claude-sonnet-4-5" } },
      { id: "opus", model: { primary: "anthropic/claude-opus-4-6" } },
    ],
  },
  bindings: [
    { agentId: "chat", match: { channel: "whatsapp" } },
    { agentId: "opus", match: { channel: "telegram" } },
  ],
}
```

### Family Agent (Sandboxed, Restricted)
```json5
{
  agents: {
    list: [
      {
        id: "family",
        sandbox: { mode: "all", scope: "agent" },
        tools: {
          allow: ["read", "exec"],
          deny: ["write", "edit", "browser", "cron"],
        },
      },
    ],
  },
  bindings: [
    {
      agentId: "family",
      match: { channel: "whatsapp", peer: { kind: "group", id: "120363...@g.us" } },
    },
  ],
}
```

## Sandbox Settings

| Option | Values | Meaning |
|--------|--------|---------|
| `mode` | `off`, `non-main`, `all` | When to sandbox |
| `scope` | `session`, `agent`, `shared` | Container isolation level |
| `workspaceAccess` | `none`, `ro`, `rw` | Workspace visibility in sandbox |

Per-agent `tools` overrides global `agents.defaults.tools`. Tool denial applies before sandboxing.

See `references/routing-examples.md` for more copy-paste config patterns.
