---
name: openclaw-config
description: >
  Use when the user wants to configure OpenClaw, edit openclaw.json, change OpenClaw settings,
  set up gateway authentication, configure models or providers, manage environment variables,
  use secret references, understand OpenClaw config sections, or use the OpenClaw CLI.
---

# OpenClaw Configuration

Guide the user through configuring their OpenClaw gateway via `~/.openclaw/openclaw.json` (JSON5 format).

## Config File

- **Location**: `~/.openclaw/openclaw.json`
- **Format**: JSON5 (comments, trailing commas, unquoted keys allowed)
- **Validation**: Strict schema — unknown keys or malformed types cause gateway to refuse starting
- **Hot reload**: Gateway watches the file automatically. Most changes apply without restart.

Override location via `OPENCLAW_CONFIG_PATH` env var.

## Key Config Sections

### gateway
Server binding, authentication, and reload behavior.
```json5
{
  gateway: {
    port: 18789,
    bind: "loopback",          // "loopback" | "0.0.0.0" | specific IP
    auth: {
      mode: "token",           // "token" | "password" | "none"
      token: "replace-me",
    },
    reload: { mode: "hybrid" }, // "hybrid" | "hot" | "restart" | "off"
  },
}
```

### agents
Agent defaults and per-agent configuration (model, sandbox, tools, workspace).
```json5
{
  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace",
      model: { primary: "anthropic/claude-sonnet-4-5" },
    },
    list: [
      { id: "main", default: true },
    ],
  },
}
```

### channels
Messaging platform integrations (WhatsApp, Telegram, Discord, Slack, etc.).

### tools
Tool access control: profiles, allow/deny lists, exec security, filesystem restrictions.
```json5
{
  tools: {
    profile: "messaging",       // "messaging" | "full" | "minimal"
    deny: ["group:automation"],
    exec: { security: "deny" },
    fs: { workspaceOnly: true },
  },
}
```

### session
Conversation isolation and reset policies.
```json5
{
  session: {
    dmScope: "per-channel-peer", // "main" | "per-peer" | "per-channel-peer"
  },
}
```

### Other Sections
- **models** - Provider configuration and API keys
- **cron** - Scheduled automation jobs
- **hooks** - HTTP webhook endpoints
- **web** - Browser tool and SSRF policy
- **env** - Environment variable injection
- **bindings** - Multi-agent message routing

## Environment Variable Substitution

Use `${VAR_NAME}` syntax in config values:
```json5
{
  models: {
    providers: {
      anthropic: { apiKey: "${ANTHROPIC_API_KEY}" },
    },
  },
}
```

Escape with `$${VAR}` for literal output. Missing vars throw error at load time.

## Secret References (SecretRef)

For sensitive fields, use SecretRef objects instead of plaintext:
```json5
{
  gateway: {
    auth: {
      token: { source: "env", provider: "default", id: "OPENCLAW_TOKEN" },
    },
  },
}
```

Sources: `"env"` (environment variable), `"file"` (filesystem), `"exec"` (command output).

## File Composition ($include)

Split large configs into multiple files:
```json5
{
  agents: { $include: "./agents.json5" },
  broadcast: { $include: ["./clients/a.json5", "./clients/b.json5"] },
}
```

## CLI Config Commands

```bash
openclaw config get <path>           # Read a config value
openclaw config set <path> <value>   # Set a config value
openclaw config unset <path>         # Delete a config key
openclaw configure                   # Re-run interactive wizard
openclaw doctor                      # Validate config
```

## Hot Reload Behavior

| What Changes | Restart Needed? |
|-------------|-----------------|
| channels, agents, models, tools, hooks, cron, session | No (hot-applied) |
| gateway port/bind/auth/TLS | Yes (auto in hybrid mode) |

## Hardened Baseline Config

```json5
{
  gateway: {
    bind: "loopback",
    auth: { mode: "token", token: "long-random-secret" },
  },
  session: { dmScope: "per-channel-peer" },
  tools: {
    profile: "messaging",
    deny: ["group:automation", "group:runtime", "group:fs"],
    exec: { security: "deny" },
  },
}
```

See `references/config-reference.md` for full section-by-section reference and `references/cli-reference.md` for complete CLI listing.
