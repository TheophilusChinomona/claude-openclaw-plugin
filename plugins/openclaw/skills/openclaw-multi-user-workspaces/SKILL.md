---
name: openclaw-multi-user-workspaces
description: >
  Use when the user wants to share a gateway with multiple people, set up
  multi-user access, configure session isolation, manage user pairing,
  add a user to the gateway, control workspace access, or understand
  OpenClaw's trust model for shared deployments.
---

# OpenClaw Multi-User Workspaces

Guide the user through setting up a gateway so multiple people can share it safely — with isolated sessions, controlled access, and appropriate security boundaries.

## Trust Model

OpenClaw is a **personal assistant**, not a multi-tenant bus. Understand what's safe before sharing.

| Scenario | Recommendation |
|----------|---------------|
| Family (3-5 people, full trust) | Single gateway, session isolation, one sandboxed agent, pairing policy |
| Small team (5-10, cooperative) | Single gateway, per-user agent routing, sandbox + tool restrictions |
| Company team (same trust boundary) | Single gateway on dedicated machine/user, tiered agents, strict tool policy |
| Adversarial users (competing, untrusted) | **Separate gateways** — ideally separate OS users/hosts per trust boundary |

If users are adversarial to each other, a single gateway is **not** a supported security boundary. See `references/security-guide.md` for the full decision tree.

## Step 1: Session Isolation

Set `session.dmScope` to prevent users from seeing each other's conversations:

| Value | Behavior | When to use |
|-------|----------|-------------|
| `"main"` (default) | All DMs share one session | Single-user only |
| `"per-peer"` | One session per sender (across channels) | Simple multi-user |
| `"per-channel-peer"` | One session per channel + sender pair | **Recommended for multi-user** |
| `"per-account-channel-peer"` | One session per account + channel + sender | Multi-account channels |

```json5
{
  session: {
    dmScope: "per-channel-peer",
  },
}
```

This is a **messaging-context boundary**, not a host-admin boundary. It prevents cross-user context leakage in conversations but does not isolate host-level file access.

If the same person contacts you on multiple channels, use `session.identityLinks` to collapse their DM sessions into one canonical identity.

## Step 2: User Access Control

### DM Policy

Each channel has a `dmPolicy` that gates inbound DMs **before** messages are processed:

| Policy | Behavior |
|--------|----------|
| `"pairing"` (default) | Unknown senders get an 8-character code. Message is not processed until approved. Codes expire after 1 hour. |
| `"allowlist"` | Only senders in `allowFrom` (config + approved store) are accepted. No pairing handshake. |
| `"open"` | Allow anyone to DM. Requires `allowFrom: ["*"]`. Use with extreme caution. |
| `"disabled"` | Ignore all inbound DMs. |

**Recommendation:** Start with `"pairing"` for onboarding, then migrate to `"allowlist"` once your user list is stable. See `references/configuration-examples.md` Examples E and F.

### Approve users via CLI

```bash
# List pending pairing requests
openclaw pairing list <channel>

# Approve a user
openclaw pairing approve <channel> <CODE>
```

Supported channels: `telegram`, `whatsapp`, `signal`, `imessage`, `discord`, `slack`, `feishu`.

### Allowlist configuration

```json5
{
  channels: {
    telegram: {
      dmPolicy: "allowlist",
      allowFrom: ["tg:111111111", "tg:222222222"],
    },
    whatsapp: {
      dmPolicy: "allowlist",
      allowFrom: ["+15551230001", "+15551230002"],
    },
  },
}
```

### Pairing state paths

- Pending requests: `~/.openclaw/credentials/<channel>-pairing.json`
- Approved allowlist (default account): `~/.openclaw/credentials/<channel>-allowFrom.json`
- Approved allowlist (non-default account): `~/.openclaw/credentials/<channel>-<accountId>-allowFrom.json`

Treat these files as sensitive — they gate access to your assistant.

## Step 3: Per-User Agent Routing

Route different users to different agents using bindings. Each agent has its own workspace, sessions, and tool policy — so you can give the admin full access while restricting guests.

```json5
{
  agents: {
    list: [
      { id: "admin", workspace: "~/.openclaw/workspace-admin" },
      { id: "team", workspace: "~/.openclaw/workspace-team" },
    ],
  },

  bindings: [
    // Peer binding (most specific, wins first)
    {
      agentId: "admin",
      match: { channel: "whatsapp", peer: { kind: "direct", id: "+15551230001" } },
    },
    // Channel-wide fallback
    { agentId: "team", match: { channel: "whatsapp" } },
  ],
}
```

**Key rules:**
- Peer bindings must come above channel-wide rules to take precedence
- Multiple fields in one binding = AND semantics (all must match)
- Same-tier ties = first in config order wins

For the full 8-tier priority table and advanced routing patterns, see the `openclaw-multi-agent` skill.

## Step 4: Per-User Sandboxing

Control what each user can do by configuring sandbox and tool policy per agent:

### Tiered example

```json5
{
  agents: {
    list: [
      // Owner: full access, no sandbox
      {
        id: "owner",
        workspace: "~/.openclaw/workspace-owner",
        sandbox: { mode: "off" },
      },
      // Family member: sandboxed, read + exec only
      {
        id: "family",
        workspace: "~/.openclaw/workspace-family",
        sandbox: { mode: "all", scope: "agent", workspaceAccess: "ro" },
        tools: {
          allow: ["read", "exec"],
          deny: ["write", "edit", "apply_patch", "browser", "cron", "gateway"],
        },
      },
      // Guest: sandboxed, read-only
      {
        id: "guest",
        workspace: "~/.openclaw/workspace-guest",
        sandbox: { mode: "all", scope: "agent", workspaceAccess: "none" },
        tools: {
          allow: ["read"],
          deny: ["exec", "write", "edit", "apply_patch", "browser", "cron", "gateway"],
        },
      },
    ],
  },
}
```

### Sandbox settings reference

| Option | Values | Meaning |
|--------|--------|---------|
| `mode` | `"off"`, `"non-main"`, `"all"` | When to sandbox |
| `scope` | `"session"`, `"agent"`, `"shared"` | Container isolation level |
| `workspaceAccess` | `"none"`, `"ro"`, `"rw"` | Workspace visibility in sandbox |

Per-agent `tools` overrides `agents.defaults.tools`. Tool denial applies before sandboxing. For shared agents handling untrusted content, always deny control-plane tools:

```json5
{
  tools: {
    deny: ["gateway", "cron", "sessions_spawn", "sessions_send"],
  },
}
```

## Step 5: Device Pairing

Node devices (iOS/Android/macOS/headless) connect to the gateway and require approval:

### Pair via Telegram (recommended for iOS)

1. User messages the bot: `/pair`
2. Bot replies with a setup code (base64-encoded JSON with `url` + `token`)
3. On phone: OpenClaw app → Settings → Gateway → paste setup code
4. Back in Telegram: `/pair approve`

### Pair via CLI

```bash
# List pending device requests
openclaw devices list

# Approve a device
openclaw devices approve <requestId>

# Reject a device
openclaw devices reject <requestId>
```

### Device pairing state

- Pending: `~/.openclaw/devices/pending.json`
- Paired: `~/.openclaw/devices/paired.json`

Treat node pairing like admin access — a paired node can execute commands on the gateway.

## Common Patterns

### Family Gateway

3-4 family members on WhatsApp, single sandboxed agent:

```json5
{
  session: { dmScope: "per-channel-peer" },
  agents: {
    list: [{
      id: "family",
      workspace: "~/.openclaw/workspace-family",
      identity: { name: "Family Bot" },
      groupChat: { mentionPatterns: ["@family", "@familybot"] },
      sandbox: { mode: "all", scope: "agent", workspaceAccess: "ro" },
      tools: {
        allow: ["read", "exec", "sessions_list", "sessions_history"],
        deny: ["write", "edit", "apply_patch", "browser", "canvas", "cron", "gateway"],
      },
    }],
  },
  channels: {
    whatsapp: {
      dmPolicy: "pairing",
      groups: { "*": { requireMention: true } },
    },
  },
}
```

### Small Team

Admin + 4 team members on Telegram, tiered access:

```json5
{
  session: { dmScope: "per-channel-peer" },
  agents: {
    list: [
      { id: "admin", workspace: "~/.openclaw/workspace-admin", sandbox: { mode: "off" } },
      {
        id: "team",
        workspace: "~/.openclaw/workspace-team",
        sandbox: { mode: "all", scope: "agent", workspaceAccess: "ro" },
        tools: { allow: ["read", "exec"], deny: ["write", "edit", "browser", "cron", "gateway"] },
      },
    ],
  },
  bindings: [
    { agentId: "admin", match: { channel: "telegram", peer: { kind: "direct", id: "tg:111111111" } } },
    { agentId: "team", match: { channel: "telegram" } },
  ],
  channels: {
    telegram: {
      dmPolicy: "allowlist",
      allowFrom: ["tg:111111111", "tg:222222222", "tg:333333333", "tg:444444444", "tg:555555555"],
    },
  },
}
```

### Company Shared Agent

Larger team on Slack, dedicated machine, strict business scope:

```json5
{
  session: { dmScope: "per-channel-peer" },
  agents: {
    defaults: {
      sandbox: { mode: "all", scope: "agent", workspaceAccess: "none" },
      tools: { deny: ["gateway", "cron", "sessions_spawn", "sessions_send"] },
    },
    list: [
      { id: "admin", workspace: "~/.openclaw/workspace-admin", sandbox: { mode: "off" }, tools: { deny: [] } },
      {
        id: "dev",
        workspace: "~/.openclaw/workspace-dev",
        sandbox: { workspaceAccess: "rw" },
        tools: { allow: ["read", "write", "edit", "exec"], deny: ["browser", "cron", "gateway"] },
      },
      {
        id: "viewer",
        workspace: "~/.openclaw/workspace-viewer",
        sandbox: { workspaceAccess: "ro" },
        tools: { allow: ["read"], deny: ["exec", "write", "edit", "apply_patch", "browser"] },
      },
    ],
  },
  bindings: [
    { agentId: "admin", match: { channel: "slack", peer: { kind: "direct", id: "U01ADMIN" } } },
    { agentId: "dev", match: { channel: "slack", peer: { kind: "direct", id: "U02DEV1" } } },
    { agentId: "dev", match: { channel: "slack", peer: { kind: "direct", id: "U03DEV2" } } },
    { agentId: "viewer", match: { channel: "slack" } },
  ],
  channels: {
    slack: {
      dmPolicy: "allowlist",
      allowFrom: ["U01ADMIN", "U02DEV1", "U03DEV2", "U04VIEW1", "U05VIEW2"],
    },
  },
}
```

**Requirements for company shared agent:** dedicated machine/VM, dedicated OS user, dedicated browser profiles, strictly business-scoped, no personal identity mixing.

## Verification

After setting up multi-user access, verify:

```bash
# Check session isolation
openclaw config get session.dmScope
# Should return "per-channel-peer" or "per-account-channel-peer"

# Check DM policies per channel
openclaw config get channels.whatsapp.dmPolicy
openclaw config get channels.telegram.dmPolicy

# List agents and their bindings
openclaw agents list --bindings

# List approved users
openclaw pairing list <channel>

# Run security audit
openclaw security audit

# Full diagnostic
openclaw doctor
```

See `references/configuration-examples.md` for six complete copy-paste configurations and `references/security-guide.md` for the full threat matrix and hardening guide.
