# Hooks & Automation Reference

## Hook Mapping Examples

### Path Match

```json5
{
  hooks: {
    mappings: [
      { match: { path: "gmail" }, action: "agent", agentId: "main", deliver: true },
      { match: { path: "ci/deploy" }, action: "agent", agentId: "devops" },
      { match: { path: "stripe" }, action: "agent", agentId: "billing" },
    ],
  },
}
```

### Header Match

```json5
{
  hooks: {
    mappings: [
      {
        match: { header: { "X-Event-Type": "push" } },
        action: "agent",
        agentId: "coder",
      },
    ],
  },
}
```

### Body Match

```json5
{
  hooks: {
    mappings: [
      {
        match: { body: { "event": "order.completed" } },
        action: "agent",
        agentId: "sales",
        deliver: true,
      },
    ],
  },
}
```

## Session Key Handling

- **`defaultSessionKey`** — session used for unmatched hooks (default: `"hook:ingress"`)
- **`allowRequestSessionKey`** — if `true`, external callers can specify sessionKey in the request (dangerous)
- **`allowedSessionKeyPrefixes`** — restrict which session key shapes external callers can use

Recommended setup:
```json5
{
  hooks: {
    defaultSessionKey: "hook:ingress",
    allowRequestSessionKey: false,
    allowedSessionKeyPrefixes: ["hook:"],
  },
}
```

## Security Hardening

### Token Auth

Always set a strong, long token:
```json5
{
  hooks: {
    token: "${HOOKS_TOKEN}",  // env var substitution
  },
}
```

Short tokens trigger `hooks.token_too_short` audit warning.

### Tool Policy for Hook Agents

Hook payloads are untrusted — restrict tool access:
```json5
{
  agents: {
    list: [
      {
        id: "hook-agent",
        tools: {
          profile: "messaging",
          deny: ["gateway", "cron", "sessions_spawn", "sessions_send", "group:runtime"],
        },
        sandbox: { mode: "all", scope: "session" },
      },
    ],
  },
}
```

### Model Choice

Use strong, instruction-hardened models for hook-driven agents. Smaller models are more susceptible to prompt injection from hook payloads.

### Unsafe Content Flags

- `hooks.mappings[].allowUnsafeExternalContent` — bypasses safety wrapping (debug only)
- `hooks.gmail.allowUnsafeExternalContent` — bypasses Gmail content safety

Keep both `false` in production.

## Hook + Cron Interaction

Hooks and cron can work together:

1. **Hook triggers cron setup** — a webhook event creates a follow-up cron job
2. **Cron polls for hook results** — scheduled job checks for accumulated hook data
3. **Shared session namespace** — use `hook:` prefixed session keys to separate automation from chat

## Cron Job Schema

When using `openclaw cron add` or the agent `cron` tool:

```json5
{
  id: "daily-briefing",
  schedule: "0 8 * * *",        // crontab syntax
  agentId: "main",
  task: "Generate morning briefing",
  enabled: true,
  // optional:
  sessionKey: "cron:briefing",
  deliver: true,
  timeout: "5m",
}
```

## Cron vs Heartbeat

| Feature | Cron | Heartbeat |
|---------|------|-----------|
| Trigger | Fixed schedule | Idle timer |
| Granularity | Minute-level | Duration string |
| Custom task | Yes (task field) | No (system event) |
| Session | Isolated per run | Existing session |
| Control-plane | Yes (persistent) | No (config only) |

Use cron for tasks that need their own session. Use heartbeat for keep-alive pings to existing conversations.

## Troubleshooting

- **Cron not running**: Check `openclaw cron status` — is scheduler enabled?
- **Hook not triggering**: Verify token, path match, and `hooks.enabled: true`
- **Heartbeat skipping**: Check target session exists and `directPolicy` allows delivery
- See `openclaw-troubleshooting` skill for diagnostics
