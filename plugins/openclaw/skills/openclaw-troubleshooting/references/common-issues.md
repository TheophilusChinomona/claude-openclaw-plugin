# Common OpenClaw Issues

## Gateway Not Starting

### Port Conflict (EADDRINUSE)
```bash
openclaw gateway status
# Check what's using the port:
lsof -i :18789   # macOS/Linux
```
Fix: Change port in config or stop the conflicting process.

### Missing Auth on Non-Loopback Bind
Log: `refusing to bind gateway ... without auth`

Fix:
```json5
{
  gateway: {
    auth: { mode: "token", token: "long-random-secret" },
  },
}
```

### Gateway Mode Not Set
Log: `Gateway start blocked: set gateway.mode=local`

Fix: Set `gateway.mode: "local"` in config, or run `openclaw configure`.

For Podman deployments with dedicated `openclaw` user, config is at `~openclaw/.openclaw/openclaw.json`.

### Config Validation Failure
Gateway refuses to start with invalid config. Only diagnostic commands work (`doctor`, `logs`, `health`, `status`).

Fix:
```bash
openclaw doctor --fix
```

---

## No Replies

### Pending Pairing
```bash
openclaw pairing list <channel>
openclaw pairing approve <channel> <CODE>
```

### Group Mention Required
Log: `drop guild message (mention required`

Fix: Either mention the bot, or set `requireMention: false` for the group.

### DM Policy Blocking
Check config: `openclaw config get channels.<channel>.dmPolicy`

If `allowlist`, verify sender ID is in `allowFrom`. If `disabled`, change to `pairing` or `open`.

### Telegram Privacy Mode
Bot can't see group messages unless:
- Privacy mode disabled via `/setprivacy` in BotFather, OR
- Bot is a group admin

After changing, remove and re-add bot to each group.

---

## Dashboard 1008 / Unauthorized

### Wrong URL
```bash
openclaw gateway status    # Check actual URL
openclaw status            # Verify reachability
```

For remote access via SSH tunnel:
```bash
ssh -N -L 18789:127.0.0.1:18789 user@host
```

### Token Mismatch
```bash
openclaw config get gateway.auth.token
```
Ensure the dashboard uses the same token.

### No Token Configured
```bash
openclaw doctor --generate-gateway-token
```

### Device Auth Issues
Log: `device identity required`, `device nonce required`, `device signature invalid`

Update connecting client to latest version. Verify device auth v2 handshake:
1. Client waits for `connect.challenge`
2. Signs challenge-bound payload
3. Sends `connect.params.device.nonce` with same challenge nonce

---

## Channel Connected But Silent

### Check Access Policies
```bash
openclaw config get channels.<channel>.dmPolicy
openclaw config get channels.<channel>.groupPolicy
openclaw config get channels.<channel>.groups
```

### Missing Channel Permissions
- **Discord**: Enable Message Content Intent in Developer Portal
- **Telegram**: Disable privacy mode or make bot admin
- **Slack**: Add required Bot Token Scopes

### Log Analysis
```bash
openclaw logs --follow
```

Look for:
- `mention required` - group mention policy
- `pairing` - sender needs approval
- `blocked` / `allowlist` - sender filtered
- `missing_scope` / `Forbidden` / `401/403` - channel auth issue

---

## Cron/Heartbeat Issues

### Scheduler Disabled
```bash
openclaw cron status
```
Log: `cron: scheduler disabled; jobs will not run automatically`

Fix: Set `cron.enabled: true` in config.

### Scheduler Tick Failed
Log: `cron: timer tick failed`

Check file/log/runtime errors in `openclaw logs --follow`.

### Heartbeat Skipped
```bash
openclaw system heartbeat last
```

Skip reasons:
- `quiet-hours` - outside active window
- `dm-blocked` - `heartbeat.directPolicy` set to `block`
- `requests-in-flight` - already processing
- `alerts-disabled` - notifications disabled
- `unknown accountId` - invalid account for delivery target

### Job Run History
```bash
openclaw cron runs --id <jobId> --limit 20
openclaw cron logs <jobId>
```

---

## Node Tool Failures

### Node Not Online
```bash
openclaw nodes status
openclaw nodes describe --node <id>
```

### App Not in Foreground
Log: `NODE_BACKGROUND_UNAVAILABLE`

Fix: Bring the node app to foreground on the device.

### Missing OS Permissions
Log: `*_PERMISSION_REQUIRED`, `LOCATION_PERMISSION_REQUIRED`

Fix: Grant the required permission in device settings (camera, microphone, location, etc.).

### Exec Approval Required
Log: `SYSTEM_RUN_DENIED: approval required` or `SYSTEM_RUN_DENIED: allowlist miss`

Fix:
```bash
openclaw approvals get --node <id>
# Approve the pending command or add to allowlist
```

---

## Browser Tool Failures

### Browser Not Starting
Log: `Failed to start Chrome CDP on port`

Fix: Check `web.browser.cdpPort` config and browser executable path.

### Invalid Executable Path
Log: `browser.executablePath not found`

Fix: Set correct path in config:
```json5
{
  web: {
    browser: {
      executablePath: "/usr/bin/chromium-browser",
    },
  },
}
```

### Extension Relay Not Attached
Log: `Chrome extension relay is running, but no tab is connected`

Fix: Open Chrome with the OpenClaw extension and ensure a tab is connected.

### Attach-Only Profile Unreachable
Log: `Browser attachOnly is enabled ... not reachable`

Fix: Ensure the target browser is running and CDP is accessible.

---

## Anthropic 429: Long Context Required

### Cause
Long-context requests fail due to API usage limits when model has `params.context1m: true`.

### Fix Options
1. Disable `context1m` for the model (fall back to normal context)
2. Use an Anthropic API key with billing/Extra Usage enabled
3. Configure fallback models for graceful degradation

---

## Post-Upgrade Breakage

Most post-upgrade issues are config drift or stricter defaults.

### Step 1: Auth & URL
```bash
openclaw gateway status
openclaw config get gateway.mode
openclaw config get gateway.auth.mode
```

### Step 2: Bind Guardrails
Non-loopback binds now require auth configured.
```bash
openclaw config get gateway.bind
openclaw config get gateway.auth.token
```

### Step 3: Pairing & Device State
```bash
openclaw devices list
openclaw pairing list --channel <channel>
```

### If All Else Fails
```bash
openclaw gateway install --force
openclaw gateway restart
```

---

## Environment Diagnostics

### Key Environment Variables
| Variable | Purpose |
|----------|---------|
| `OPENCLAW_HOME` | Override home directory for all paths |
| `OPENCLAW_STATE_DIR` | Override state directory |
| `OPENCLAW_CONFIG_PATH` | Override config file path |
| `OPENCLAW_LOG_LEVEL` | Override log level (takes precedence over config) |

### Debug Mode
```bash
OPENCLAW_LOG_LEVEL=debug openclaw status
OPENCLAW_LOG_LEVEL=trace openclaw gateway   # Most verbose
```

### Env Var Precedence
1. Process environment (parent shell/daemon)
2. `.env` in current working directory
3. `~/.openclaw/.env`
4. Config `env` block
5. Login-shell import (if enabled)
