---
name: openclaw-sessions
description: >
  Use when the user wants to manage sessions, configure session resets, set up
  compaction, link identities across channels, configure thread bindings,
  understand DM scope, view session history, spawn sub-sessions, or
  configure session isolation in OpenClaw.
---

# OpenClaw Sessions

Guide the user through session management: scoping, resets, compaction, thread bindings, identity links, and session tools.

## Session Concept

A **session** is a conversation context identified by a `sessionKey`. Sessions store:
- Chat history (transcript) at `~/.openclaw/agents/<agentId>/sessions/*.jsonl`
- Context state (model, tools, compaction state)

The `sessionKey` is computed from `dmScope` + channel + peer + account. It is a routing key, **not an authorization token**.

## DM Scope

`session.dmScope` controls how DM sessions are isolated:

| Value | Behavior | Use Case |
|-------|----------|----------|
| `main` | All DMs share one session | Single-user continuity (default) |
| `per-peer` | One session per sender | Multi-user, channel-agnostic |
| `per-channel-peer` | One session per channel+sender | Multi-user, channel-isolated |
| `per-account-channel-peer` | One per account+channel+sender | Multi-account channels |

```json5
{
  session: {
    dmScope: "per-channel-peer",  // recommended for multi-user
  },
}
```

**`main` is the canonical direct-chat key.** Group/channel sessions use their own keys (they always count as non-main).

## Session Reset

Control when session history is cleared:

```json5
{
  session: {
    reset: {
      mode: "daily",        // "daily" | "idle"
      atHour: 4,            // hour (0-23) for daily reset
      idleMinutes: 120,     // minutes of inactivity for idle reset
    },
  },
}
```

- **`daily`** — resets at `atHour` every day
- **`idle`** — resets after `idleMinutes` of no activity

## Thread Bindings (Discord)

Thread bindings route messages in Discord threads to specific sessions:

```json5
{
  session: {
    threadBindings: {
      enabled: true,
      idleHours: 24,       // auto-unbind after idle
      maxAgeHours: 0,      // max thread age (0 = no limit)
    },
  },
}
```

### Discord Commands

- `/focus` — bind current thread to a session
- `/unfocus` — unbind thread
- `/agents` — list available agents for thread binding
- `/session idle <hours>` — set idle timeout for current thread
- `/session max-age <hours>` — set max age for current thread

Thread bindings are also configurable per-channel: `channels.discord.threadBindings.*`.

## Identity Links

Map the same user across channels to share session context:

```json5
{
  session: {
    identityLinks: [
      {
        ids: ["whatsapp:+15551234567", "telegram:123456789"],
        label: "Alice",
      },
    ],
  },
}
```

When identity links are configured, sessions are shared across channels for the same user (with `per-peer` or `per-channel-peer` scope).

## Compaction

When conversation context grows large, compaction summarizes older messages:

- **`/compact`** — manually trigger compaction
- **Auto-compaction** — triggered when token budget is exceeded
- **Adaptive token budgeting** — adjusts based on model context window

What survives compaction: system instructions, recent messages, compaction summary.
What is removed: older tool call details, redundant message pairs.

## Session Tools

The agent has built-in session tools:

| Tool | Purpose |
|------|---------|
| `sessions_list` | List sessions (filter by kind, limit, activity) |
| `sessions_history` | Read transcript of a session |
| `sessions_send` | Send message to another session (ping-pong) |
| `sessions_spawn` | Start a sub-agent run |
| `session_status` | Current session status, model override |

### Visibility

`tools.sessions.visibility` controls what sessions an agent can see:
- `"tree"` (default) — current session + spawned sub-sessions
- `"self"` — current session only (recommended for shared/multi-user agents)

```json5
{
  tools: {
    sessions: { visibility: "self" },
  },
}
```

### sessions_send

Runs a reply-back ping-pong between sessions:
- Target replies with `REPLY_SKIP` to stop
- Max turns via `session.agentToAgent.maxPingPongTurns` (0–5)
- After ping-pong, target runs an announce step (reply `ANNOUNCE_SKIP` to suppress)

### sessions_spawn

Starts a sub-agent run:
- `mode: "run"` — one-shot
- `mode: "session"` with `thread: true` — persistent thread-bound mode
- Non-blocking: returns `status: "accepted"` immediately
- Supports inline file attachments (`attachments` array)

## Cross-References

- **Multi-user isolation**: See `openclaw-multi-user-workspaces` for trust model and pairing
- **Sandbox session visibility**: When sandboxed, `sessionToolsVisibility: "spawned"` clamps visibility to `tree`

See `references/session-advanced.md` for edge cases and internal details.
