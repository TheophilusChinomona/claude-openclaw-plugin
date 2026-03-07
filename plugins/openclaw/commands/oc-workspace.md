---
description: Manage multi-user workspace access, pairing, sessions, and security audit
argument-hint: <users|pair|sessions|audit> [channel]
allowed-tools: Bash, Read
---

# /oc-workspace Command

Manage multi-user workspace access — list approved users, handle pairing, check session isolation, and audit security.

## Arguments

The user provides: `$ARGUMENTS`

Parse:
- **subcommand** (required): `users`, `pair`, `sessions`, or `audit`
- **channel** (optional, for `pair`): channel name like `whatsapp`, `telegram`, `slack`

## Subcommands

### `users`

List all approved users across channels with their agent routing.

1. Read allowlist files:
```bash
# Find all allowlist files
ls ~/.openclaw/credentials/*-allowFrom.json 2>/dev/null
```

2. For each file, read and display approved senders:
```bash
cat ~/.openclaw/credentials/whatsapp-allowFrom.json 2>/dev/null
cat ~/.openclaw/credentials/telegram-allowFrom.json 2>/dev/null
```

3. Get current bindings:
```bash
openclaw agents list --bindings
```

4. Get DM policies:
```bash
openclaw config get channels
```

5. Present a consolidated table:
```
Channel     | DM Policy  | Approved Users | Routed To
------------|------------|----------------|----------
whatsapp    | pairing    | +1555123...    | family
telegram    | allowlist  | tg:111111111   | admin
            |            | tg:222222222   | team
```

### `pair [channel]`

List and manage pending pairing requests.

1. If a channel is specified:
```bash
openclaw pairing list <channel>
```

2. If no channel specified, check all common channels:
```bash
openclaw pairing list whatsapp 2>/dev/null
openclaw pairing list telegram 2>/dev/null
openclaw pairing list discord 2>/dev/null
openclaw pairing list slack 2>/dev/null
openclaw pairing list signal 2>/dev/null
```

3. Also check device pairing:
```bash
openclaw devices list 2>/dev/null
```

4. Present pending requests with instructions:
```
Pending DM Pairing:
  whatsapp: ABCD1234 from +15551230001 (3 min ago)
  telegram: EFGH5678 from tg:999999999 (12 min ago)

Pending Device Pairing:
  (none)

To approve: openclaw pairing approve <channel> <CODE>
To approve device: openclaw devices approve <requestId>
```

### `sessions`

Show session isolation configuration and warn about unsafe settings.

1. Get dmScope setting:
```bash
openclaw config get session.dmScope
```

2. Get active session info:
```bash
openclaw status
```

3. Analyze and report:
   - If `dmScope` is `"main"` or unset: **warn** that all DMs share one session (unsafe for multi-user)
   - If `dmScope` is `"per-channel-peer"` or `"per-account-channel-peer"`: report as properly isolated
   - Show current active sessions count if available

4. Example output:
```
Session Isolation: per-channel-peer (recommended)

Each channel + sender pair gets an isolated DM context.
Cross-user context leakage is prevented.

Note: This is a messaging-context boundary, not host-level isolation.
For adversarial users, use separate gateways.
```

Or if unsafe:
```
WARNING: Session Isolation: main (UNSAFE for multi-user)

All DMs currently share one session. Users can see each other's
conversation context.

Fix: openclaw config set session.dmScope '"per-channel-peer"'
```

### `audit`

Run a security check for multi-user configuration.

1. Check session scope:
```bash
openclaw config get session.dmScope
```

2. Check DM policies:
```bash
openclaw config get channels
```

3. Check sandbox modes:
```bash
openclaw config get agents
```

4. Run the built-in security audit:
```bash
openclaw security audit
```

5. Present a focused multi-user security report:
```
Multi-User Security Audit
=========================

Session Isolation:
  [PASS] dmScope: per-channel-peer

DM Access Control:
  [PASS] whatsapp: pairing
  [WARN] telegram: open (anyone can DM — consider pairing or allowlist)

Agent Sandboxing:
  [PASS] family: sandbox mode=all, scope=agent
  [WARN] admin: sandbox mode=off (acceptable for owner only)

Tool Restrictions:
  [PASS] family: gateway, cron denied
  [WARN] admin: no tool restrictions (acceptable for owner only)

Recommendations:
  1. Set telegram dmPolicy to "pairing" or "allowlist"
```

### No subcommand or unrecognized

Show usage help:
```
Usage: /oc-workspace <subcommand> [args]

  users              List approved users across channels + agent routing
  pair [channel]     List/approve pending pairing and device requests
  sessions           Show session isolation config, warn if unsafe
  audit              Multi-user security audit (dmScope, policies, sandbox, tools)
```

## After Running

- For `users`: if no users found, suggest setting up pairing with `/oc-channel`
- For `pair`: if approvals were made, suggest adding bindings with `openclaw config set`
- For `sessions`: if dmScope is `"main"`, strongly recommend changing it
- For `audit`: if warnings found, provide specific fix commands
