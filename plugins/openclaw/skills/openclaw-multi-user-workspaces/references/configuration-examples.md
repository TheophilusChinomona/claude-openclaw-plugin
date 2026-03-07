# Multi-User Configuration Examples

## Example A: Family WhatsApp Bot

3 family members share one WhatsApp number. Pairing policy, single sandboxed agent, session isolation.

```json5
{
  session: {
    dmScope: "per-channel-peer",  // each family member gets isolated DM context
  },

  agents: {
    list: [
      {
        id: "family",
        name: "Family Bot",
        workspace: "~/.openclaw/workspace-family",
        identity: { name: "Family Bot" },
        groupChat: {
          mentionPatterns: ["@family", "@familybot"],
        },
        sandbox: {
          mode: "all",
          scope: "agent",
          workspaceAccess: "ro",
        },
        tools: {
          allow: ["read", "exec", "sessions_list", "sessions_history"],
          deny: ["write", "edit", "apply_patch", "browser", "canvas", "cron", "gateway"],
        },
      },
    ],
  },

  channels: {
    whatsapp: {
      dmPolicy: "pairing",
      groups: { "*": { requireMention: true } },
    },
  },
}
```

**Setup steps:**
```bash
openclaw agents add family
# Family members DM the bot → get pairing code
openclaw pairing list whatsapp
openclaw pairing approve whatsapp <CODE>  # approve each member
openclaw agents list --bindings
```

## Example B: Small Team (Telegram)

5 team members on Telegram. Allowlist policy, admin gets full agent, team members get restricted agent.

```json5
{
  session: {
    dmScope: "per-channel-peer",
  },

  agents: {
    list: [
      {
        id: "admin",
        name: "Admin",
        workspace: "~/.openclaw/workspace-admin",
        sandbox: { mode: "off" },
        // Full tool access for admin
      },
      {
        id: "team",
        name: "Team",
        workspace: "~/.openclaw/workspace-team",
        sandbox: {
          mode: "all",
          scope: "agent",
          workspaceAccess: "ro",
        },
        tools: {
          allow: ["read", "exec"],
          deny: ["write", "edit", "apply_patch", "browser", "cron", "gateway"],
        },
      },
    ],
  },

  // Route admin to admin agent, everyone else to team agent
  bindings: [
    {
      agentId: "admin",
      match: { channel: "telegram", peer: { kind: "direct", id: "tg:111111111" } },
    },
    { agentId: "team", match: { channel: "telegram" } },
  ],

  channels: {
    telegram: {
      dmPolicy: "allowlist",
      allowFrom: [
        "tg:111111111",  // admin
        "tg:222222222",  // team member 1
        "tg:333333333",  // team member 2
        "tg:444444444",  // team member 3
        "tg:555555555",  // team member 4
      ],
    },
  },
}
```

## Example C: Multi-Channel Team (WhatsApp + Slack)

WhatsApp for mobile team chat (restricted), Slack for office (more capable). Different agents per channel.

```json5
{
  session: {
    dmScope: "per-account-channel-peer",  // multi-channel needs account-level scoping
  },

  agents: {
    list: [
      {
        id: "mobile",
        name: "Mobile",
        workspace: "~/.openclaw/workspace-mobile",
        sandbox: { mode: "all", scope: "agent", workspaceAccess: "ro" },
        tools: {
          allow: ["read", "exec"],
          deny: ["write", "edit", "browser", "cron", "gateway"],
        },
      },
      {
        id: "office",
        name: "Office",
        workspace: "~/.openclaw/workspace-office",
        sandbox: { mode: "non-main", scope: "agent" },
        // Broader tool access in office context
      },
    ],
  },

  bindings: [
    { agentId: "mobile", match: { channel: "whatsapp" } },
    { agentId: "office", match: { channel: "slack" } },
  ],

  channels: {
    whatsapp: {
      dmPolicy: "pairing",
      groups: { "*": { requireMention: true } },
    },
    slack: {
      dmPolicy: "allowlist",
      allowFrom: ["U01ADMIN", "U02DEV1", "U03DEV2"],
    },
  },
}
```

## Example D: Company Tiered Access (Slack)

Slack workspace with admin/developer/viewer tiers. Three agents with different permission levels.

```json5
{
  session: {
    dmScope: "per-channel-peer",
  },

  agents: {
    defaults: {
      sandbox: {
        mode: "all",
        scope: "agent",
        workspaceAccess: "none",
      },
      tools: {
        deny: ["gateway", "cron", "sessions_spawn", "sessions_send"],
      },
    },

    list: [
      {
        id: "admin",
        name: "Admin Agent",
        workspace: "~/.openclaw/workspace-admin",
        sandbox: { mode: "off" },  // Override: no sandbox for admin
        tools: {
          allow: ["read", "write", "edit", "exec", "browser"],
          deny: [],  // Override: full access
        },
      },
      {
        id: "developer",
        name: "Dev Agent",
        workspace: "~/.openclaw/workspace-dev",
        sandbox: { mode: "all", scope: "agent", workspaceAccess: "rw" },
        tools: {
          allow: ["read", "write", "edit", "exec"],
          deny: ["browser", "cron", "gateway"],
        },
      },
      {
        id: "viewer",
        name: "Viewer Agent",
        workspace: "~/.openclaw/workspace-viewer",
        sandbox: { mode: "all", scope: "agent", workspaceAccess: "ro" },
        tools: {
          allow: ["read"],
          deny: ["exec", "write", "edit", "apply_patch", "browser", "cron", "gateway"],
        },
      },
    ],
  },

  // Route by Slack user ID → peer binding (most specific, wins first)
  bindings: [
    { agentId: "admin", match: { channel: "slack", peer: { kind: "direct", id: "U01ADMIN" } } },
    { agentId: "developer", match: { channel: "slack", peer: { kind: "direct", id: "U02DEV1" } } },
    { agentId: "developer", match: { channel: "slack", peer: { kind: "direct", id: "U03DEV2" } } },
    { agentId: "viewer", match: { channel: "slack" } },  // Everyone else → viewer
  ],

  channels: {
    slack: {
      dmPolicy: "allowlist",
      allowFrom: ["U01ADMIN", "U02DEV1", "U03DEV2", "U04VIEWER1", "U05VIEWER2"],
    },
  },
}
```

## Example E: Onboarding via Pairing (Step-by-Step)

Step-by-step workflow for onboarding users with the pairing flow.

**1. Configure pairing policy:**
```json5
{
  session: { dmScope: "per-channel-peer" },
  channels: {
    whatsapp: { dmPolicy: "pairing" },
    telegram: { dmPolicy: "pairing" },
  },
}
```

**2. User sends first message:**
The bot replies with a pairing code (8 characters, expires after 1 hour). The message is **not processed** until approved.

**3. List pending requests:**
```bash
openclaw pairing list whatsapp
# Output:
#   Code      Sender           Requested
#   ABCD1234  +15551230001     2 minutes ago
#   EFGH5678  +15551230002     5 minutes ago
```

**4. Approve each user:**
```bash
openclaw pairing approve whatsapp ABCD1234
openclaw pairing approve whatsapp EFGH5678
```

**5. Verify approved users:**
```bash
# Check allowlist files
cat ~/.openclaw/credentials/whatsapp-allowFrom.json
```

**6. (Optional) Route approved users to specific agents:**
Add bindings after approval:
```json5
{
  bindings: [
    {
      agentId: "team-lead",
      match: { channel: "whatsapp", peer: { kind: "direct", id: "+15551230001" } },
    },
    { agentId: "team", match: { channel: "whatsapp" } },  // Everyone else
  ],
}
```

**State files:**
- Pending requests: `~/.openclaw/credentials/<channel>-pairing.json`
- Approved users (default account): `~/.openclaw/credentials/<channel>-allowFrom.json`
- Approved users (non-default account): `~/.openclaw/credentials/<channel>-<accountId>-allowFrom.json`

## Example F: Migrating from Pairing to Allowlist

After onboarding is complete, switch from pairing to a static allowlist for tighter control.

**1. Read current approved users:**
```bash
cat ~/.openclaw/credentials/whatsapp-allowFrom.json
# Copy the approved sender IDs
```

**2. Update config — switch from pairing to allowlist:**
```json5
{
  channels: {
    whatsapp: {
      dmPolicy: "allowlist",  // was "pairing"
      allowFrom: [
        "+15551230001",  // team lead
        "+15551230002",  // member 1
        "+15551230003",  // member 2
      ],
    },
  },
}
```

Or via CLI:
```bash
openclaw config set channels.whatsapp.dmPolicy '"allowlist"'
openclaw config set channels.whatsapp.allowFrom '["+15551230001", "+15551230002", "+15551230003"]'
```

**3. Verify:**
```bash
openclaw doctor
openclaw security audit
```

**Why migrate?** Allowlist is more predictable for stable teams — no pairing codes, no pending request management. New users require explicit config changes, which serves as an audit trail.
