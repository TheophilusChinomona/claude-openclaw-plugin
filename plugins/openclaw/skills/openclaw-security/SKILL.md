---
name: openclaw-security
description: >
  Use when the user wants to run a security audit, harden OpenClaw, manage
  secrets, rotate credentials, handle a security incident, configure gateway
  authentication, set up Tailscale, configure reverse proxy, review file
  permissions, or understand OpenClaw's security model.
---

# OpenClaw Security

Guide the user through security auditing, hardening, secrets management, and incident response.

**Trust model**: OpenClaw is a **personal assistant** — one trusted operator boundary per gateway. It is not a hostile multi-tenant security boundary. For mixed-trust users, split trust boundaries (separate gateways, ideally separate OS users/hosts).

## Security Audit

```bash
openclaw security audit              # Standard audit
openclaw security audit --deep       # Deep audit with live Gateway probe
openclaw security audit --fix        # Auto-fix supported findings
openclaw security audit --json       # Machine-readable output
```

### What It Checks

- **Inbound access** — DM policies, group policies, allowlists
- **Tool blast radius** — elevated tools + open rooms
- **Network exposure** — Gateway bind/auth, Tailscale, weak tokens
- **Browser control** — remote nodes, relay ports, CDP endpoints
- **Disk hygiene** — permissions, symlinks, config includes
- **Plugins** — extensions without explicit allowlist
- **Policy drift** — sandbox config but mode off, runtime expectation drift
- **Model hygiene** — legacy/small models with tool access

### Severity Levels

| Severity | Action |
|----------|--------|
| **CRITICAL** | Fix immediately — active exposure |
| **WARNING** | Fix soon — potential risk |
| **INFO** | Informational — best practice suggestion |

## File Permissions

Keep config and state private:

```bash
chmod 700 ~/.openclaw               # user only
chmod 600 ~/.openclaw/openclaw.json  # user read/write only
```

`openclaw doctor` warns and can fix permissions automatically.

## Network Security

### Gateway Bind Modes

| Mode | Listens On | Use Case |
|------|-----------|----------|
| `loopback` (default) | `127.0.0.1` | Local-only, most secure |
| `lan` | All interfaces | LAN access (needs auth) |
| `tailscale` | Tailscale interface | VPN-secured remote access |

### Gateway Authentication

```json5
{
  gateway: {
    auth: {
      mode: "token",                    // "token" | "password" | "none"
      token: "${OPENCLAW_GATEWAY_TOKEN}",
    },
  },
}
```

**Never use `mode: "none"` with non-loopback bind.**

### Tailscale Integration

```json5
{
  gateway: {
    tailscale: {
      mode: "serve",     // "serve" (private) | "funnel" (public — CRITICAL risk)
    },
  },
}
```

- `serve` — accessible only within your Tailscale network
- `funnel` — **public internet exposure** (triggers critical audit finding)

### Reverse Proxy

```json5
{
  gateway: {
    trustedProxies: ["127.0.0.1"],
    allowRealIpFallback: false,        // keep false unless proxy can't provide X-Forwarded-For
    auth: {
      mode: "password",
      password: "${OPENCLAW_GATEWAY_PASSWORD}",
    },
  },
}
```

Good proxy config: overwrite incoming headers (`proxy_set_header X-Forwarded-For $remote_addr`).

## Secrets Management

### SecretRef (Recommended)

Three source types for secrets:

| Source | Example | Use Case |
|--------|---------|----------|
| `env` | Environment variable | Simple deployments |
| `file` | `~/.openclaw/secrets.json` | File-backed secrets |
| `exec` | External command (e.g., vault) | Enterprise secrets managers |

```json5
{
  models: {
    providers: {
      openai: {
        apiKey: { source: "env", provider: "default", id: "OPENAI_API_KEY" },
      },
    },
  },
}
```

### ${VAR} Substitution

Reference env vars in any config string:
```json5
{
  gateway: { auth: { token: "${OPENCLAW_GATEWAY_TOKEN}" } },
}
```

Rules: uppercase names only (`[A-Z_][A-Z0-9_]*`), missing vars throw error, escape with `$${VAR}`.

### Credential Storage Map

| Credential | Path |
|-----------|------|
| WhatsApp auth | `~/.openclaw/credentials/whatsapp/<accountId>/creds.json` |
| Telegram bot token | config/env or `channels.telegram.tokenFile` |
| Discord bot token | config/env or SecretRef |
| Slack tokens | config/env (`channels.slack.*`) |
| Pairing allowlists | `~/.openclaw/credentials/<channel>-allowFrom.json` |
| Auth profiles | `~/.openclaw/agents/<agentId>/agent/auth-profiles.json` |
| File secrets | `~/.openclaw/secrets.json` |

## Insecure Flags

All `dangerous*`/`dangerously*` config keys disable safety checks. The audit flags them:

- `gateway.controlUi.dangerouslyDisableDeviceAuth` — disables device identity checks
- `gateway.controlUi.dangerouslyAllowHostHeaderOriginFallback` — DNS rebinding risk
- `browser.ssrfPolicy.dangerouslyAllowPrivateNetwork` — SSRF risk
- `agents.*.sandbox.docker.dangerouslyAllowContainerNamespaceJoin` — container escape risk
- `hooks.*.allowUnsafeExternalContent` — bypasses content safety

## Incident Response

### 1. Contain

```bash
openclaw gateway stop                    # Stop the gateway
# Or: kill the process, disable the service
```

### 2. Rotate (assume compromise if secrets leaked)

```bash
# Regenerate gateway token
openclaw config set gateway.auth.token "$(openssl rand -hex 32)"

# Rotate channel tokens (Telegram, Discord, etc.)
# Rotate API keys (Anthropic, OpenAI, etc.)
# Revoke pairing for unknown devices
openclaw devices list
openclaw devices reject <requestId>
```

### 3. Audit

```bash
openclaw security audit --deep --json > audit-report.json
openclaw logs --tail 200 > incident-logs.txt
```

### 4. Collect for Report

```bash
openclaw --version > incident-info.txt
openclaw status >> incident-info.txt
ls -la ~/.openclaw/ >> incident-info.txt
```

## Hardened Baseline

Copy-paste secure starting config:

```json5
{
  gateway: {
    mode: "local",
    bind: "loopback",
    auth: { mode: "token", token: "replace-with-long-random-token" },
  },
  session: { dmScope: "per-channel-peer" },
  tools: {
    profile: "messaging",
    deny: ["group:automation", "group:runtime", "group:fs", "sessions_spawn", "sessions_send"],
    fs: { workspaceOnly: true },
    exec: { security: "deny", ask: "always" },
    elevated: { enabled: false },
  },
  channels: {
    whatsapp: { dmPolicy: "pairing", groups: { "*": { requireMention: true } } },
  },
}
```

## Cross-References

- **Multi-user trust model**: See `openclaw-multi-user-workspaces` for multi-user security
- **Sandbox security**: See `openclaw-sandboxing` for Docker isolation details

See `references/audit-checklist.md` for the complete audit checkId table.
