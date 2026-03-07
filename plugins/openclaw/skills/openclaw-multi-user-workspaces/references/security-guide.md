# Multi-User Security Guide

## Trust Model Deep Dive

OpenClaw follows a **personal assistant security model** — one trusted operator boundary per gateway. It is **not** a hostile multi-tenant security boundary for multiple adversarial users sharing one agent/gateway.

Key implications:
- If several people can message one tool-enabled agent, each of them can steer that same permission set.
- Per-user session/memory isolation helps privacy, but does not convert a shared agent into per-user host authorization.
- `sessionKey` is a routing selector, not an authorization token.
- Operators with control-plane access can inspect session metadata/history by design.
- Filesystem access equals trust boundary — any process that can read `~/.openclaw` can read session transcripts.

**Shared tool authority**: when multiple users share an agent, each authorized sender can induce tool calls within that agent's policy. If one shared agent has sensitive credentials or files, any allowed sender can potentially drive exfiltration via tool usage.

## Threat Matrix

| Threat | Impact | Mitigation |
|--------|--------|------------|
| Unauthorized sender | Stranger triggers the bot, runs tools | `dmPolicy: "pairing"` or `"allowlist"`, group allowlists + mention gating |
| Destructive tool use | Authorized user runs destructive commands via shared agent | Per-agent `tools.deny`, sandbox `mode: "all"`, `workspaceAccess: "ro"` or `"none"` |
| Session snooping | User A reads User B's conversation | `session.dmScope: "per-channel-peer"`, separate agents per user via bindings |
| File access | User reads files outside their intended scope | Sandbox `scope: "agent"`, `tools.fs.workspaceOnly: true`, separate `agentDir` per agent |
| Compromised channel token | Attacker impersonates the bot | Store tokens via SecretRef (env/file/exec), rotate immediately on exposure, file perms `600` |
| Shared credentials | Agent A accidentally uses Agent B's API keys | Never share `agentDir` across agents, per-agent `auth-profiles.json` |
| Prompt injection via untrusted content | Model tricked into running unintended commands | Strong model tiers, `tools.deny` for `gateway`/`cron`/`sessions_spawn`, sandbox |
| Control-plane escalation | User triggers `config.apply` or `cron` via agent | `tools.deny: ["gateway", "cron", "sessions_spawn", "sessions_send"]` for shared agents |

## Isolation Levels

Escalating from weakest to strongest:

| Level | What it provides | When to use |
|-------|-----------------|-------------|
| Session isolation only | Separate conversation contexts via `dmScope` | Family/friends you fully trust, just want privacy |
| Session + per-user agent routing | Separate workspace, sessions, and personality per user | Small team, cooperative trust, different tool needs |
| Session + agent + sandbox | Containerized execution per agent | Mixed-trust team, untrusted content handling |
| Session + agent + sandbox + tool deny | Containerized + restricted tool set | Users who should only read, not write/exec |
| Separate gateways (separate OS user/host) | Full host-level isolation | Adversarial users, separate trust boundaries |

## Hardened Multi-User Baseline

Copy-paste starting point for any multi-user gateway. Selectively re-enable tools per trusted agent:

```json5
{
  gateway: {
    mode: "local",
    bind: "loopback",
    auth: { mode: "token", token: "${OPENCLAW_GATEWAY_TOKEN}" },
  },

  session: {
    dmScope: "per-channel-peer",  // isolate DMs per sender
  },

  agents: {
    defaults: {
      sandbox: {
        mode: "all",
        scope: "agent",
        workspaceAccess: "ro",
      },
      tools: {
        deny: ["gateway", "cron", "sessions_spawn", "sessions_send", "browser"],
      },
    },
  },

  tools: {
    fs: { workspaceOnly: true },
    exec: { security: "deny", ask: "always" },
    elevated: { enabled: false },
  },

  channels: {
    whatsapp: {
      dmPolicy: "pairing",
      groups: { "*": { requireMention: true } },
    },
  },
}
```

Then override per agent in `agents.list[]`:
- Owner agent: `sandbox.mode: "off"`, broader tool access
- Team member: `sandbox.mode: "all"`, `tools.allow: ["read", "exec"]`
- Guest/viewer: `sandbox.mode: "all"`, `tools.allow: ["read"]`, `tools.deny: ["exec", "write", "edit"]`

## OS-Level Hardening

For multi-user gateways handling sensitive data:

1. **Dedicated machine/VM/container** — one gateway per trust boundary
2. **Dedicated OS user** — run the gateway under its own user account
3. **File permissions** — `~/.openclaw`: `700`, `openclaw.json`: `600`
4. **Dedicated browser profiles** — never sign into personal accounts on the gateway runtime
5. **No personal identity mixing** — do not mix personal Apple/Google accounts with company/team identities on the same runtime

Verify with:
```bash
openclaw security audit --deep
```

## Credential Isolation

- **Never share `agentDir`** across agents — causes auth/session collisions
- Auth profiles are per-agent at `~/.openclaw/agents/<agentId>/agent/auth-profiles.json`
- Use **SecretRef** for channel tokens instead of inline values:
  ```json5
  { source: "env", provider: "default", id: "TELEGRAM_BOT_TOKEN" }
  ```
- Pairing allowlists are stored per-channel and per-account:
  - Default account: `~/.openclaw/credentials/<channel>-allowFrom.json`
  - Non-default: `~/.openclaw/credentials/<channel>-<accountId>-allowFrom.json`
- Treat everything under `~/.openclaw/` as sensitive

## When to Use Separate Gateways

Decision tree:

1. **Are users adversarial to each other?** (e.g., competing departments, external clients)
   - Yes → **Separate gateways**, ideally separate OS users/hosts
2. **Do users need different host-level file access?**
   - Yes → **Separate gateways** (sandbox is cwd isolation, not hard boundary)
3. **Are users in the same trust boundary?** (e.g., one company team, one family)
   - Yes → Single gateway with per-user agents, session isolation, and sandboxing
4. **Is the agent tool-enabled with broad access?**
   - Yes + shared users → Tighten with `tools.deny`, sandbox, `workspaceOnly: true`
   - Yes + only you → Standard single-user setup is fine
5. **Is this a company shared agent?**
   - Yes → Acceptable if: dedicated machine/VM, dedicated OS user, dedicated browser profiles, strictly business-scoped, all users in same trust boundary
