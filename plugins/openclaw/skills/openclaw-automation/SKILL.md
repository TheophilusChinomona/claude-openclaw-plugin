---
name: openclaw-automation
description: >
  Use when the user wants to set up cron jobs, configure webhooks, add hooks,
  schedule automated tasks, configure heartbeat, set up periodic messages,
  automate agent actions, manage cron runs, or configure event-driven
  automation in OpenClaw.
---

# OpenClaw Automation

Guide the user through configuring automated actions: cron (scheduled), hooks (event-driven), and heartbeat (keep-alive).

## Three Pillars

| Pillar | Trigger | Use Case |
|--------|---------|----------|
| **Cron** | Schedule (crontab syntax) | Daily briefings, periodic reports, cleanup tasks |
| **Hooks** | HTTP webhook event | Gmail notifications, CI/CD triggers, external service events |
| **Heartbeat** | Idle timer | Keep-alive pings, context refresh, periodic check-ins |

All three hot-apply without gateway restart (in `hybrid` or `hot` reload mode).

## Cron Jobs

### Configuration

```json5
{
  cron: {
    enabled: true,
    maxConcurrentRuns: 2,
    sessionRetention: "24h",   // prune completed run sessions (false to disable)
    runLog: {
      maxBytes: "2mb",
      keepLines: 2000,
    },
  },
}
```

### CLI Commands

```bash
openclaw cron status              # Scheduler status (enabled, running jobs)
openclaw cron list                # All configured jobs as table
openclaw cron add                 # Guided job creation
openclaw cron update <jobId>      # Update existing job
openclaw cron remove <jobId>      # Remove a job
openclaw cron run <jobId>         # Manual trigger (runs immediately)
openclaw cron runs <jobId>        # View run history
openclaw cron wake                # Enqueue system event + optional heartbeat
```

### Cron Tool (Agent)

The agent has a built-in `cron` tool with actions: `status`, `list`, `add`, `update`, `remove`, `run`, `runs`, `wake`.

- `add` expects a full cron job object (same schema as `cron.add` RPC)
- `update` uses `{ jobId, patch }`

### Security

- Cron can create scheduled jobs that persist after the chat ends — this is a **control-plane tool**
- For agents handling untrusted content, deny cron:
  ```json5
  { tools: { deny: ["cron"] } }
  ```
- Use `group:automation` to deny both `cron` and `gateway` tools together
- Cron payloads support `allowUnsafeExternalContent` — keep this `false` in production

## Hooks (Webhooks)

### Configuration

```json5
{
  hooks: {
    enabled: true,
    token: "shared-secret-token",       // auth token for incoming requests
    path: "/hooks",                      // URL path prefix
    defaultSessionKey: "hook:ingress",   // session for unmatched hooks
    allowRequestSessionKey: false,       // external caller can choose sessionKey
    allowedSessionKeyPrefixes: ["hook:"],
    mappings: [
      {
        match: { path: "gmail" },        // match by path, header, or body
        action: "agent",
        agentId: "main",
        deliver: true,                   // deliver to chat after processing
      },
    ],
  },
}
```

### Mapping Syntax

Each mapping has:
- **`match`** — `{ path, header, body }` matchers (string or regex)
- **`action`** — `"agent"` (run agent), `"forward"` (proxy)
- **`agentId`** — target agent for the hook
- **`deliver`** — post result to chat after agent run
- **`allowUnsafeExternalContent`** — bypass safety wrapping (dangerous, debug only)

### Security

- Treat all hook payloads as **untrusted input** (even from trusted systems — content can carry prompt injection)
- Use strong, long tokens for `hooks.token`
- Keep `allowRequestSessionKey: false` unless you need external session routing
- If enabled, bind with `allowedSessionKeyPrefixes` to limit scope
- For hook-driven agents, use strong models + strict tool policy (`tools.profile: "messaging"`)
- Deny control-plane tools for hook agents: `tools: { deny: ["gateway", "cron", "sessions_spawn"] }`

## Heartbeat

### Configuration

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "30m",          // duration string (0m to disable)
        target: "last",        // where to deliver
        directPolicy: "allow", // allow | block (for DM-style targets)
      },
    },
  },
}
```

### Targets

| Target | Behavior |
|--------|----------|
| `last` | Last active chat session |
| `whatsapp` | WhatsApp DM |
| `telegram` | Telegram DM |
| `discord` | Discord channel |
| `none` | No delivery (heartbeat still runs internally) |

### Skip Reasons

Heartbeat may skip if: no active session, target channel disconnected, agent busy, or `directPolicy: "block"` prevents DM delivery.

## Common Patterns

### Webhook-to-Agent Pipeline

Route Gmail notifications to an agent:
```json5
{
  hooks: {
    enabled: true,
    token: "${HOOKS_TOKEN}",
    mappings: [
      {
        match: { path: "gmail" },
        action: "agent",
        agentId: "main",
        deliver: true,
      },
    ],
  },
}
```

### Daily Briefing via Cron

```bash
openclaw cron add   # then configure:
# schedule: "0 8 * * *"  (every day at 8am)
# agentId: "main"
# task: "Give me a morning briefing"
```

### Staggered Cron + Heartbeat

Use cron for scheduled reports and heartbeat for context refresh:
```json5
{
  cron: { enabled: true, maxConcurrentRuns: 1 },
  agents: {
    defaults: {
      heartbeat: { every: "2h", target: "last" },
    },
  },
}
```

See `references/hooks-reference.md` for detailed mapping patterns and security hardening.
