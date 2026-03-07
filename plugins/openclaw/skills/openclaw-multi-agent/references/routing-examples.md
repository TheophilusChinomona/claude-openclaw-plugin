# Multi-Agent Routing Examples

## Example A: Home/Work Split (WhatsApp Multi-Account)

```json5
{
  agents: {
    list: [
      {
        id: "home",
        default: true,
        name: "Home",
        workspace: "~/.openclaw/workspace-home",
        agentDir: "~/.openclaw/agents/home/agent",
      },
      {
        id: "work",
        name: "Work",
        workspace: "~/.openclaw/workspace-work",
        agentDir: "~/.openclaw/agents/work/agent",
      },
    ],
  },

  bindings: [
    { agentId: "home", match: { channel: "whatsapp", accountId: "personal" } },
    { agentId: "work", match: { channel: "whatsapp", accountId: "biz" } },

    // Override: specific group in personal account → work agent
    {
      agentId: "work",
      match: {
        channel: "whatsapp",
        accountId: "personal",
        peer: { kind: "group", id: "1203630...@g.us" },
      },
    },
  ],

  channels: {
    whatsapp: {
      accounts: {
        personal: {},
        biz: {},
      },
    },
  },
}
```

Setup:
```bash
openclaw channels login --channel whatsapp --account personal
openclaw channels login --channel whatsapp --account biz
openclaw gateway restart
```

## Example B: Per-Channel Agent Split

WhatsApp for everyday (fast model), Telegram for deep work (powerful model):

```json5
{
  agents: {
    list: [
      {
        id: "chat",
        name: "Everyday",
        workspace: "~/.openclaw/workspace-chat",
        model: { primary: "anthropic/claude-sonnet-4-5" },
      },
      {
        id: "opus",
        name: "Deep Work",
        workspace: "~/.openclaw/workspace-opus",
        model: { primary: "anthropic/claude-opus-4-6" },
      },
    ],
  },

  bindings: [
    { agentId: "chat", match: { channel: "whatsapp" } },
    { agentId: "opus", match: { channel: "telegram" } },
  ],
}
```

## Example C: Same Channel, One Peer Override

Keep WhatsApp on fast agent, route one DM to Opus:

```json5
{
  agents: {
    list: [
      { id: "chat", model: { primary: "anthropic/claude-sonnet-4-5" } },
      { id: "opus", model: { primary: "anthropic/claude-opus-4-6" } },
    ],
  },

  bindings: [
    // Peer binding (most specific, wins first)
    {
      agentId: "opus",
      match: { channel: "whatsapp", peer: { kind: "direct", id: "+15551234567" } },
    },
    // Channel-wide fallback
    { agentId: "chat", match: { channel: "whatsapp" } },
  ],
}
```

**Peer bindings must come above channel-wide rules** to take precedence.

## Example D: Telegram Bots Per Agent

Two Telegram bots, one per agent:

```json5
{
  agents: {
    list: [
      { id: "main", workspace: "~/.openclaw/workspace-main" },
      { id: "alerts", workspace: "~/.openclaw/workspace-alerts" },
    ],
  },

  bindings: [
    { agentId: "main", match: { channel: "telegram", accountId: "default" } },
    { agentId: "alerts", match: { channel: "telegram", accountId: "alerts" } },
  ],

  channels: {
    telegram: {
      accounts: {
        default: {
          botToken: "123456:ABC...",
          dmPolicy: "pairing",
        },
        alerts: {
          botToken: "987654:XYZ...",
          dmPolicy: "allowlist",
          allowFrom: ["tg:123456789"],
        },
      },
    },
  },
}
```

## Example E: Discord Multi-Bot

Two Discord bots, one per agent:

```json5
{
  agents: {
    list: [
      { id: "main", workspace: "~/.openclaw/workspace-main" },
      { id: "coding", workspace: "~/.openclaw/workspace-coding" },
    ],
  },

  bindings: [
    { agentId: "main", match: { channel: "discord", accountId: "default" } },
    { agentId: "coding", match: { channel: "discord", accountId: "coding" } },
  ],

  channels: {
    discord: {
      accounts: {
        default: {
          token: "DISCORD_BOT_TOKEN_MAIN",
          guilds: {
            "123456789012345678": {
              channels: {
                "222222222222222222": { allow: true, requireMention: false },
              },
            },
          },
        },
        coding: {
          token: "DISCORD_BOT_TOKEN_CODING",
          guilds: {
            "123456789012345678": {
              channels: {
                "333333333333333333": { allow: true, requireMention: false },
              },
            },
          },
        },
      },
    },
  },
}
```

## Example F: Family Agent (Sandboxed, Tool-Restricted)

```json5
{
  agents: {
    list: [
      {
        id: "family",
        name: "Family",
        workspace: "~/.openclaw/workspace-family",
        identity: { name: "Family Bot" },

        groupChat: {
          mentionPatterns: ["@family", "@familybot"],
        },

        sandbox: {
          mode: "all",
          scope: "agent",
        },

        tools: {
          allow: ["exec", "read", "sessions_list", "sessions_history", "sessions_send"],
          deny: ["write", "edit", "apply_patch", "browser", "canvas", "nodes", "cron"],
        },
      },
    ],
  },

  bindings: [
    {
      agentId: "family",
      match: {
        channel: "whatsapp",
        peer: { kind: "group", id: "120363999999999999@g.us" },
      },
    },
  ],
}
```

## Example G: Tiered Sandbox Configuration

```json5
{
  agents: {
    defaults: {
      sandbox: {
        mode: "non-main",
        scope: "session",
        workspaceAccess: "none",
        docker: {
          image: "openclaw-sandbox:bookworm-slim",
          network: "none",
        },
      },
    },

    list: [
      {
        id: "dev",
        workspace: "~/.openclaw/workspace-dev",
        sandbox: { mode: "off" },           // No sandbox (trusted)
      },
      {
        id: "builder",
        workspace: "~/.openclaw/workspace-builder",
        sandbox: {
          mode: "all",
          scope: "agent",
          workspaceAccess: "rw",
          docker: {
            network: "host",
            setupCommand: "apt-get update && apt-get install -y nodejs npm",
          },
        },
        tools: {
          allow: ["exec", "read", "write"],
          deny: ["browser", "cron"],
        },
      },
      {
        id: "reporter",
        workspace: "~/.openclaw/workspace-reporter",
        sandbox: {
          mode: "all",
          scope: "shared",
          workspaceAccess: "ro",
        },
        tools: {
          allow: ["read"],
          deny: ["exec", "write", "edit"],
        },
      },
    ],
  },
}
```

## Example H: Telegram Forum Topics Per Agent

Route different forum topics to different agents:

```json5
{
  agents: {
    list: [
      { id: "main", workspace: "~/.openclaw/workspace-main" },
      { id: "coder", workspace: "~/.openclaw/workspace-coder" },
    ],
  },

  channels: {
    telegram: {
      groups: {
        "-1001234567890": {
          topics: {
            "1": { agentId: "main" },     // General → main
            "3": { agentId: "coder" },    // Dev → coder
          },
        },
      },
    },
  },
}
```

## Binding Priority Reference

Most specific wins (top to bottom):

| Priority | Match Type | Example |
|----------|-----------|---------|
| 1 | Peer (exact DM/group ID) | `peer: { kind: "direct", id: "+1555..." }` |
| 2 | Parent peer (thread) | Thread inherits parent binding |
| 3 | Guild ID + roles | Discord role-based routing |
| 4 | Guild ID | Discord server-level |
| 5 | Team ID | Slack workspace |
| 6 | Account ID | `accountId: "work"` |
| 7 | Channel-level | `channel: "whatsapp"` |
| 8 | Default agent | `default: true` in agents.list |

Multiple fields in one binding = AND semantics (all must match).
Same-tier ties = first in config order wins.
