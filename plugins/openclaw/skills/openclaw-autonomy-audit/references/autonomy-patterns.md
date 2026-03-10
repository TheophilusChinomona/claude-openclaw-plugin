# Autonomy Patterns Reference

Concrete templates and configurations for each remediation area. Copy, adapt, and apply.

---

## Pattern A: Autonomous SOUL.md Section

Add this section to any agent's `SOUL.md` to give it explicit idle/proactive behavior rules.

```markdown
## Autonomous Behavior

When I have no pending user messages or active tasks, I follow these rules:

### Proactive checks (every heartbeat cycle)
- Check inbox channels for unread messages
- Review any pending tasks in my task queue
- Check if scheduled reports are due

### Idle behavior (no pending work found)
- Review recent memory entries for follow-up opportunities
- Check if any monitored data sources have updates
- If nothing actionable: log "idle cycle — no action needed" and wait for next trigger

### Frequency
- Heartbeat interval: 30 minutes during active hours (08:00–20:00)
- Reduced interval: 2 hours during off-hours
- Never run more than 20 turns per autonomous cycle

### Boundaries
- NEVER send outbound messages without explicit user pre-approval or a standing rule
- NEVER make purchases, delete data, or modify infrastructure autonomously
- If uncertain whether an action is within mandate: log it and wait for user
```

**Adaptation notes:**
- Replace check items with agent's actual mission tasks
- Adjust frequency to match workload (high-traffic agents: 10–15min, low-traffic: 1–2hr)
- Add domain-specific boundaries

---

## Pattern B: Heartbeat + Cron Combination

Use cron for mechanical tasks and heartbeat for judgment-based tasks.

### Cron jobs (clockwork — no thinking required)

```bash
# Health check every 5 minutes
openclaw cron add --name "health-check" \
  --schedule "*/5 * * * *" \
  --command "openclaw gateway status && openclaw cron list --status"

# Daily summary at 9 AM
openclaw cron add --name "daily-summary" \
  --schedule "0 9 * * *" \
  --prompt "Compile and send daily summary of all activity in the last 24 hours"

# Inbox check every 30 minutes during work hours
openclaw cron add --name "inbox-scan" \
  --schedule "*/30 8-20 * * 1-5" \
  --prompt "Check all channels for unread messages and triage"
```

### Heartbeat config (judgment — needs agent reasoning)

```bash
# Enable heartbeat with 30-minute interval
openclaw config set heartbeat.enabled true
openclaw config set heartbeat.interval 30m
openclaw config set heartbeat.activeHours "08:00-20:00"
```

### HEARTBEAT.md checklist (what the agent evaluates each cycle)

```markdown
# Heartbeat Checklist

On each heartbeat cycle, evaluate and act on:

- [ ] Any unread messages requiring response?
- [ ] Any tasks past their deadline?
- [ ] Any monitored metrics outside normal range?
- [ ] Any follow-ups due from previous interactions?
- [ ] Any scheduled content to prepare or send?

If all items are clear, log idle cycle and wait.
```

---

## Pattern C: Gateway Daemon Configurations

Ensure the OpenClaw gateway stays alive without manual intervention.

### macOS — launchd

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>ai.openclaw.gateway</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/openclaw</string>
        <string>gateway</string>
        <string>start</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/openclaw-gateway.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/openclaw-gateway.err</string>
</dict>
</plist>
```

Save to `~/Library/LaunchAgents/ai.openclaw.gateway.plist`, then:
```bash
launchctl load ~/Library/LaunchAgents/ai.openclaw.gateway.plist
```

### Linux — systemd

```ini
[Unit]
Description=OpenClaw AI Gateway
After=network.target

[Service]
Type=simple
ExecStart=/usr/local/bin/openclaw gateway start
Restart=always
RestartSec=5
User=%i
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
```

Save to `/etc/systemd/system/openclaw-gateway.service`, then:
```bash
sudo systemctl enable openclaw-gateway
sudo systemctl start openclaw-gateway
```

### Cross-platform — pm2

```bash
# Install pm2 globally
npm install -g pm2

# Start gateway with pm2
pm2 start "openclaw gateway start" --name openclaw-gateway

# Save process list and configure startup
pm2 save
pm2 startup
```

### macOS — caffeinate (quick fix, not recommended for production)

```bash
# Prevent sleep while gateway runs
caffeinate -s openclaw gateway start
```

---

## Pattern D: Session Hygiene

Prevent context overflow in long-running autonomous sessions.

### Configuration

```bash
# Reset session after each autonomous cycle
openclaw config set session.reset true

# Keep last 3 sessions for context continuity
openclaw config set cron.sessionRetention 3

# Enable compaction for long sessions
openclaw config set session.compaction true
openclaw config set session.compactionThreshold 50000
```

### SOUL.md session rules

```markdown
## Session Management

- At the start of each autonomous cycle, check context size
- If context exceeds 50k tokens, trigger compaction before proceeding
- After completing an autonomous task cycle, write a brief summary to memory/ before session reset
- Never carry stale context across cycles — prefer fresh starts with memory lookup
```

---

## Pattern E: Cost Controls in AGENTS.md

Add this section to `AGENTS.md` to prevent runaway autonomous operation.

```markdown
## Cost Controls

### Per-cycle limits
- **Max turns per autonomous cycle:** 20
- **Max retries on failure:** 3
- **Max consecutive idle cycles before sleep:** 5

### Stop conditions
Stop the current cycle immediately if:
- Turn count exceeds max turns
- Same error occurs 3 times in a row
- Cost estimate for next action exceeds $0.50
- Agent detects it is in a loop (same action attempted twice with same result)

### Circuit breaker
If 3 consecutive cycles fail:
1. Log the failure pattern to memory/
2. Send alert to owner via primary channel
3. Enter sleep mode (disable heartbeat, keep health-check cron only)
4. Wait for manual intervention

### Daily budget
- Maximum daily API spend: $10.00 (adjust per agent)
- At 80% of budget: reduce heartbeat frequency to 2x current interval
- At 100% of budget: enter sleep mode until next day
```

---

## Pattern F: Health Monitoring Cron Job

5-minute interval health check that validates all critical systems.

```bash
openclaw cron add --name "health-monitor" \
  --schedule "*/5 * * * *" \
  --command "openclaw gateway status && openclaw cron list --status && openclaw channel list --status"
```

### Advanced health check prompt (for cron jobs that use agent reasoning)

```bash
openclaw cron add --name "health-audit" \
  --schedule "0 */2 * * *" \
  --prompt "Run a health check:
1. Verify gateway is responding (openclaw gateway status)
2. Check all channels are connected (openclaw channel list)
3. Review cron job history for failures in last 2 hours
4. Check memory/ for error patterns
5. If any issues found: log to memory/ and alert owner
6. If all clear: log 'health-check passed' to memory/"
```

---

## Pattern G: Structured Logging Configuration

Enable audit trails and debugging for autonomous operation.

### Cron run logging

```bash
# Enable run logging for all cron jobs
openclaw config set cron.runLog true
openclaw config set cron.runLogPath "./logs/cron/"
openclaw config set cron.runLogRetention 30d
```

### Agent daily log workflow

Add to `SOUL.md`:

```markdown
## Activity Logging

At the end of each autonomous cycle, append to `memory/YYYY-MM-DD.md`:

### Log entry format
```
## HH:MM — [cycle-type]

**Actions taken:** (bulleted list)
**Decisions made:** (with reasoning)
**Issues encountered:** (if any)
**Next cycle plan:** (what to check next)
```

### Log hygiene
- One file per day, append-only during the day
- At end of day (last cycle after 20:00): write a day summary at the top
- Archive logs older than 30 days to memory/archive/
```

---

## Quick Reference: Remediation Commands

| Gap | Fix Command |
|-----|------------|
| No cron jobs | `openclaw cron add --name "..." --schedule "..." --prompt "..."` |
| No heartbeat | `openclaw config set heartbeat.enabled true` |
| No daemon | `pm2 start "openclaw gateway start" --name openclaw-gateway` |
| No session reset | `openclaw config set session.reset true` |
| No run logging | `openclaw config set cron.runLog true` |
| No health check | `openclaw cron add --name "health-monitor" --schedule "*/5 * * * *" --command "openclaw gateway status"` |
