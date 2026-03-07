---
name: openclaw-troubleshooting
description: >
  Use when OpenClaw is not working, the gateway is not responding, the user wants to
  run openclaw doctor, debug OpenClaw, view openclaw logs, a channel is not responding,
  messages are not being delivered, the dashboard shows errors, or cron/heartbeat
  jobs are failing.
---

# OpenClaw Troubleshooting

Diagnose and fix common OpenClaw issues using a systematic command ladder.

## Diagnostic Command Ladder

Run these in order for initial triage:

```bash
openclaw status                    # Quick health check
openclaw gateway status            # Gateway runtime state
openclaw logs --follow             # Real-time log stream
openclaw doctor                    # Config/service diagnostics
openclaw channels status --probe   # Channel connectivity
```

**Healthy signals:**
- `openclaw gateway status` shows `Runtime: running` and `RPC probe: ok`
- `openclaw doctor` reports no blocking issues
- `openclaw channels status --probe` shows channels connected

## Decision Tree

### Gateway not responding?
1. `openclaw status` - is it running?
2. `openclaw gateway status` - check runtime state
3. `openclaw logs --follow` - look for errors
4. Common causes: port conflict (`EADDRINUSE`), missing auth on non-loopback bind, `gateway.mode` not set to `"local"`

### No replies from bot?
1. `openclaw channels status --probe` - channels connected?
2. `openclaw pairing list <channel>` - pending pairing requests?
3. Check `dmPolicy` and `allowFrom` in config
4. For groups: check `requireMention` and `groupPolicy`

### Dashboard 1008 / Unauthorized?
1. `openclaw gateway status` - verify gateway is running
2. `openclaw config get gateway.auth.token` - check token
3. Verify URL and auth mode match between client and gateway
4. For device auth errors: update connecting client

### Channel connected but silent?
1. Check `dmPolicy` (pairing/allowlist/open/disabled)
2. Check `groupPolicy` and `requireMention`
3. Check channel-specific permissions (Telegram privacy mode, Discord Message Content Intent)
4. Look for `mention required`, `blocked`, `allowlist` in logs

### Cron/heartbeat not firing?
1. `openclaw cron status` - scheduler enabled?
2. `openclaw cron list` - jobs exist?
3. `openclaw cron runs --id <jobId> --limit 20` - run history
4. Check heartbeat skip reasons: `quiet-hours`, `dm-blocked`, `requests-in-flight`

### Node tool failing?
1. `openclaw nodes status` - node online?
2. `openclaw nodes describe --node <id>` - capabilities
3. `openclaw approvals get --node <id>` - exec approvals
4. Check OS permissions (camera, location, etc.)

### Browser tool failing?
1. `openclaw browser status` - browser running?
2. `openclaw browser profiles` - valid profiles?
3. Check CDP reachability and executable path

## Doctor Command

```bash
openclaw doctor              # Validate config, show errors
openclaw doctor --fix        # Auto-repair fixable issues
openclaw doctor --yes        # Auto-repair without prompting
openclaw doctor --generate-gateway-token  # Generate missing token
```

Doctor checks: config syntax/schema, service metadata, port availability, file permissions, browser paths.

## Log Viewing

```bash
openclaw logs --follow               # Real-time stream
openclaw logs --tail 50              # Last N lines
OPENCLAW_LOG_LEVEL=debug openclaw status  # Debug-level output
```

Log levels: `trace` > `debug` > `info` > `warn` > `error`

## Post-Upgrade Checklist

1. **Check auth**: `openclaw config get gateway.auth.mode` - non-loopback binds now require auth
2. **Check bind**: `openclaw config get gateway.bind` - verify bind/auth alignment
3. **Check devices**: `openclaw devices list` - pending approvals after identity changes
4. **Check pairing**: `openclaw pairing list <channel>` - re-approve if needed
5. **Reinstall service if needed**: `openclaw gateway install --force && openclaw gateway restart`

## Common Error Signatures

| Log Message | Meaning | Fix |
|-------------|---------|-----|
| `Gateway start blocked: set gateway.mode=local` | Local mode not enabled | Set `gateway.mode: "local"` |
| `refusing to bind ... without auth` | Non-loopback without token | Add `gateway.auth.token` |
| `EADDRINUSE` | Port conflict | Change port or stop other process |
| `device identity required` | Device auth not satisfied | Update client, check device pairing |
| `NODE_BACKGROUND_UNAVAILABLE` | Node app not in foreground | Bring app to foreground |
| `SYSTEM_RUN_DENIED` | Exec approval pending | Check `openclaw approvals` |

See `references/common-issues.md` for detailed troubleshooting per issue type.
