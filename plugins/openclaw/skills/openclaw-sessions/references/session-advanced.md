# Session Advanced Reference

## Thread Binding Edge Cases

### Forum Threads (Discord)

Forum threads are treated as regular threads for binding purposes. The bot must be mentioned or use `/focus` to bind.

### Auto-Binding

When `threadBindings.enabled: true`, threads created by the bot auto-bind to the session that created them.

### Expiry

- **Idle expiry**: `idleHours` — thread unbinds after no activity
- **Age expiry**: `maxAgeHours` — thread unbinds after max age (0 = no limit)
- Expired bindings are cleaned up lazily on next message

### Per-Channel Override

```json5
{
  channels: {
    discord: {
      threadBindings: {
        enabled: true,
        idleHours: 48,        // override global default
        maxAgeHours: 168,     // 1 week
      },
    },
  },
}
```

## Identity Link Examples

### Multi-Channel Same User

```json5
{
  session: {
    identityLinks: [
      {
        ids: [
          "whatsapp:+15551234567",
          "telegram:987654321",
          "discord:123456789012345678",
        ],
        label: "Alice",
      },
      {
        ids: ["whatsapp:+15559876543", "telegram:111222333"],
        label: "Bob",
      },
    ],
  },
}
```

When Alice messages from WhatsApp or Telegram, she gets the same session context.

### Identity Format

Identity IDs use `channel:platformId` format:
- WhatsApp: `whatsapp:+15551234567`
- Telegram: `telegram:123456789`
- Discord: `discord:123456789012345678`
- Slack: `slack:U0123456789`

## Compaction Internals

### Token Budget

- Budget is computed from model context window minus reserved space
- When messages exceed budget, oldest messages are summarized
- Summary is injected as a system message at the compaction boundary

### What Survives

- System instructions (SOUL.md, personality)
- Compaction summary of older context
- Recent messages (within budget)
- Active session state (model override, pending tasks)

### What Is Removed

- Older tool call details (inputs/outputs)
- Redundant message pairs
- Media attachments (paths preserved, content dropped)

### Manual Compaction

```
/compact
```

Forces immediate compaction regardless of budget state.

## Session Key Format

Session keys are computed deterministically:

| dmScope | Format |
|---------|--------|
| `main` | `agent:<agentId>:main` |
| `per-peer` | `agent:<agentId>:dm:<peerId>` |
| `per-channel-peer` | `agent:<agentId>:<channel>:dm:<peerId>` |
| `per-account-channel-peer` | `agent:<agentId>:<accountId>:<channel>:dm:<peerId>` |

Group/channel sessions: `agent:<agentId>:<channel>:group:<groupId>`

## Spawned Sessions

### Parent-Child Relationship

`sessions_spawn` creates a child session linked to the parent:
- Child inherits the parent's agent context
- `tools.sessions.visibility: "tree"` lets parent see child sessions
- Child runs independently (non-blocking)

### Tool Inheritance

By default, spawned sessions inherit the parent agent's tool policy. Override with:
```json5
{
  // in sessions_spawn params:
  sandbox: { mode: "all", scope: "session" },
}
```

### Timeout

- `runTimeoutSeconds` controls child run timeout
- Default from `agents.defaults.subagents.runTimeoutSeconds` if set, otherwise `0` (no timeout)

## Session Store

Sessions are stored as JSONL files:
- Path: `~/.openclaw/agents/<agentId>/sessions/<sessionKey>.jsonl`
- Each line is a JSON object (message, tool call, system event)
- **Any process with filesystem access can read these** — lock down `~/.openclaw` permissions

## Cron Session Retention

Cron runs create isolated sessions. `cron.sessionRetention` controls cleanup:
```json5
{
  cron: {
    sessionRetention: "24h",  // prune after 24h (false to keep forever)
  },
}
```
