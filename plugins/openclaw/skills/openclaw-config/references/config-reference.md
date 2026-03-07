# OpenClaw Config Reference

Complete section-by-section reference for `~/.openclaw/openclaw.json`.

## gateway

```json5
{
  gateway: {
    port: 18789,
    bind: "loopback",                    // "loopback" | "0.0.0.0" | IP
    mode: "local",                       // "local" | "remote"

    auth: {
      mode: "token",                     // "token" | "password" | "none" | "device"
      token: "replace-with-secret",
      password: "secret",
    },

    reload: {
      mode: "hybrid",                    // "hybrid" | "hot" | "restart" | "off"
      debounceMs: 300,
    },

    controlUi: {
      allowedOrigins: [],
      allowInsecureAuth: false,
      dangerouslyDisableDeviceAuth: false,
    },

    tailscale: {
      mode: "off",                       // "off" | "serve" | "funnel"
    },

    remote: {
      url: "ws://...",
    },

    nodes: {
      allowCommands: [],
      denyCommands: [],
    },
  },
}
```

**Hot reload**: Changes to `gateway.*` (except `reload` and `remote`) require restart. In hybrid mode, restart is automatic.

## agents

```json5
{
  agents: {
    defaults: {
      workspace: "~/.openclaw/workspace",
      model: {
        primary: "anthropic/claude-sonnet-4-5",
        fallbacks: ["openai/gpt-5.2"],
      },
      imageMaxDimensionPx: 1200,

      sandbox: {
        mode: "non-main",                // "off" | "non-main" | "all"
        scope: "session",                // "session" | "agent" | "shared"
        workspaceAccess: "none",         // "none" | "ro" | "rw"
        docker: {
          image: "openclaw-sandbox:bookworm-slim",
          network: "none",
          binds: ["/source:/source:ro"],
          setupCommand: "apt-get update && apt-get install -y curl",
          env: { VAR: "value" },
        },
        browser: {
          autoStart: true,
          autoStartTimeoutMs: 30000,
          allowHostControl: false,
        },
      },

      heartbeat: {
        every: "30m",
        target: "last",
        directPolicy: "allow",
      },
    },

    list: [
      {
        id: "main",
        default: true,
        workspace: "~/.openclaw/workspace-main",
        model: { primary: "anthropic/claude-opus-4-6" },
        sandbox: { mode: "all" },
        tools: { profile: "messaging" },
        groupChat: {
          mentionPatterns: ["@openclaw"],
        },
      },
    ],
  },
}
```

## channels

```json5
{
  channels: {
    whatsapp: {
      enabled: true,
      accountNumber: "+1234567890",
      dmPolicy: "pairing",              // "pairing" | "allowlist" | "open" | "disabled"
      allowFrom: ["+15555550123"],
      groupPolicy: "disabled",
      groups: {
        "*": { requireMention: true },
      },
    },

    telegram: {
      enabled: true,
      botToken: "123:abc",
      dmPolicy: "pairing",
      allowFrom: ["tg:123"],
      streaming: "partial",             // "off" | "partial" | "block" | "progress"
      groups: {
        "-1001234567890": {
          requireMention: true,
          topics: {
            "1": { agentId: "main" },
          },
        },
      },
    },

    discord: {
      enabled: true,
      botToken: "token",
      dmPolicy: "pairing",
    },

    slack: {
      enabled: true,
      botToken: "xoxb-...",
      appToken: "xapp-...",
    },
  },
}
```

## session

```json5
{
  session: {
    dmScope: "per-channel-peer",         // "main" | "per-peer" | "per-channel-peer"
    mainKey: "main",
    reset: {
      mode: "daily",                     // "daily" | "idle" | "none"
      atHour: 4,
      idleMinutes: 120,
    },
  },
}
```

## tools

```json5
{
  tools: {
    profile: "messaging",               // "messaging" | "full" | "minimal"
    allow: [],
    deny: ["group:automation", "group:runtime", "group:fs"],
    fs: { workspaceOnly: true },
    exec: {
      security: "deny",                 // "allow" | "ask" | "deny"
      host: "sandbox",
    },
    elevated: {
      enabled: false,
      security: "ask",
    },
    browser: {
      ssrfPolicy: "trusted-network",
    },
  },
}
```

## cron

```json5
{
  cron: {
    enabled: true,
    maxConcurrentRuns: 2,
    sessionRetention: "24h",
  },
}
```

## hooks

```json5
{
  hooks: {
    enabled: true,
    token: "shared-secret",
    path: "/hooks",
    defaultSessionKey: "hook:ingress",
    allowRequestSessionKey: false,
    mappings: [
      {
        match: { path: "gmail" },
        action: "agent",
        agentId: "main",
      },
    ],
  },
}
```

## models

```json5
{
  models: {
    providers: {
      anthropic: { apiKey: "${ANTHROPIC_API_KEY}" },
      openai: { apiKey: { source: "env", provider: "default", id: "OPENAI_API_KEY" } },
      custom: {
        baseUrl: "https://api.example.com/v1",
        apiKey: "${CUSTOM_API_KEY}",
      },
    },
  },
}
```

## env

```json5
{
  env: {
    OPENROUTER_API_KEY: "sk-or-...",
    vars: { GROQ_API_KEY: "gsk-..." },
    shellEnv: {
      enabled: true,
      timeoutMs: 15000,
    },
  },
}
```

## bindings

```json5
{
  bindings: [
    { agentId: "home", match: { channel: "whatsapp", accountId: "personal" } },
    { agentId: "work", match: { channel: "whatsapp", accountId: "biz" } },
  ],
}
```

## logging

```json5
{
  logging: {
    level: "info",                       // "debug" | "info" | "warn" | "error"
    consoleLevel: "info",
    redactSensitive: true,
  },
}
```

## Environment Variable Substitution

- Syntax: `${VAR_NAME}` (uppercase only: `[A-Z_][A-Z0-9_]*`)
- Missing/empty vars throw error at load time
- Escape: `$${VAR}` outputs literal `${VAR}`
- Works inside `$include` files

**Precedence (highest to lowest):**
1. Process environment (parent shell/daemon)
2. `.env` in current working directory
3. `~/.openclaw/.env`
4. Config `env` block
5. Login-shell import (if `env.shellEnv.enabled`)

## File Composition ($include)

```json5
// Single file (replaces object)
{ agents: { $include: "./agents.json5" } }

// Array of files (deep merge, later wins)
{ broadcast: { $include: ["./a.json5", "./b.json5"] } }
```

- Relative paths resolved from including file
- Nesting up to 10 levels deep
- Circular includes detected
