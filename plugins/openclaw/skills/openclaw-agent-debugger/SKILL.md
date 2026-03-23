---
name: openclaw-agent-debugger
description: Diagnose and fix OpenClaw agent and gateway problems — heartbeats not firing, cron jobs failing, agents not responding, wrong routing, model errors, workspace issues, channel connection failures, and openclaw.json config errors. Use this skill when the user reports: agent not responding, heartbeat stopped, cron job not running, wrong agent getting messages, model errors, gateway won't start, channel disconnected, agent sending to wrong place, memory not writing, session errors, openclaw doctor errors, or any "something isn't working" situation with OpenClaw. This skill reads the openclaw.json config, interprets error patterns, walks through diagnostic steps, identifies the root cause, and produces the exact commands or file changes needed to fix it.
---

# OpenClaw Agent Debugger

Diagnose OpenClaw problems systematically — from symptom to root cause to exact fix.

## Diagnostic Philosophy

Every OpenClaw problem has a finite set of root causes. This skill works through them systematically rather than guessing. It always starts with the most likely cause for the reported symptom and works outward.

---

## Stage 1: Symptom Triage

Classify the reported problem into one of these categories:

| Symptom | Most Likely Root Cause | First Check |
|---|---|---|
| Agent not responding at all | Gateway down / channel disconnected | `openclaw gateway status` |
| Wrong agent responding | Binding order wrong / default agent incorrect | Check bindings in openclaw.json |
| Heartbeat stopped firing | `every: "0m"` / activeHours window / no `heartbeat` block on any agent | Check heartbeat config |
| Heartbeat fires but no message sent | `target: "none"` or `target` resolves to nothing | Check `target` + `to` fields |
| Cron job not running | `cron.enabled: false` / wrong timezone / job disabled | `openclaw cron list` |
| Cron job runs but no delivery | `delivery.mode: "none"` / wrong channel target | Check job delivery config |
| Gateway won't start | Config validation error / port conflict / auth missing | `openclaw doctor` |
| Model errors | Wrong model string format / missing API key / rate limit | Check `model.primary` format |
| Memory not persisting | Workspace path wrong / file permissions / session type | Check workspace config |
| Channel offline | Auth expired / bot token invalid / account not linked | `openclaw channels status --probe` |
| "Unauthorized" on connect | Auth token mismatch | Check `OPENCLAW_GATEWAY_TOKEN` |
| Multiple agents, routing broken | Binding specificity order wrong | Check binding priority order |

---

## Stage 2: Gather Diagnostics

Request or run these commands in order. Each is a gate — stop if you find the problem.

### Gate 1: Gateway health
```bash
openclaw gateway status           # Is Gateway running?
openclaw gateway status --deep    # Detailed health
openclaw status                   # Quick overview
```

**If Gateway is down** → skip to Gateway Recovery section

### Gate 2: Config validation
```bash
openclaw doctor                   # Config errors, drift, known issues
openclaw doctor --fix             # Auto-repair where possible
```

**If doctor reports errors** → fix config errors first, then retest

### Gate 3: Channel health
```bash
openclaw channels status --probe  # Are channels connected?
openclaw logs --follow            # Live log stream (watch for errors)
```

### Gate 4: Agent and binding state
```bash
openclaw agents list --bindings   # Which agent handles which channel/peer?
openclaw agents list              # All agents and their workspaces
```

### Gate 5: Cron state (if cron issues)
```bash
openclaw cron list                # All jobs, enabled/disabled status
openclaw cron runs --id <jobId>   # Run history for specific job
```

### Gate 6: Session state
```bash
openclaw sessions                 # Active sessions
```

---

## Stage 3: Diagnosis by Symptom

### HEARTBEAT NOT FIRING

**Check 1: Is heartbeat configured?**
```json5
// In openclaw.json — does agents.defaults.heartbeat exist?
// OR does any agents.list[] entry have a heartbeat block?
// CRITICAL: If ANY agents.list[] entry has a heartbeat block,
// ONLY those agents run heartbeats — not agents without the block.
```
Fix: Add `heartbeat` block to the correct agent in `agents.list`.

**Check 2: Is every set to 0?**
```bash
openclaw config get agents.defaults.heartbeat.every
# If "0m" → heartbeat disabled globally
```
Fix: `openclaw config set agents.defaults.heartbeat.every "30m"`

**Check 3: activeHours window**
```json5
// Is current time outside activeHours.start → activeHours.end?
// Check timezone — is it correct IANA timezone?
// "Africa/Johannesburg" not "SAST" not "UTC+2"
```
Fix: Correct timezone or adjust hours.

**Check 4: Target is none**
```json5
// heartbeat.target: "none" → runs but never delivers
```
Fix: Set `target: "whatsapp"` + `to: "+27XXXXXXXXX"` on the agent.

**Check 5: Heartbeat runs but HEARTBEAT_OK is stripped**
```
// If HEARTBEAT.md is empty (only headers/blank lines),
// OpenClaw skips the heartbeat turn to save API calls.
```
Fix: Add actual checklist items to HEARTBEAT.md.

---

### CRON JOB NOT RUNNING

**Check 1: Cron enabled?**
```bash
openclaw config get cron.enabled
# Must be true
```

**Check 2: Job state**
```bash
openclaw cron list
# Check: enabled=true, schedule correct, agentId correct
```

**Check 3: Timezone**
```bash
# Is the job scheduled in the right timezone?
# "0 7 * * *" with --tz "UTC" fires at 07:00 UTC = 09:00 SAST
# Common mistake: forgetting Africa/Johannesburg is UTC+2
```

**Check 4: Run history**
```bash
openclaw cron runs --id <jobId>
# Look for error entries — auth failures, model errors, delivery failures
```

**Check 5: Agent binding**
```bash
# If --agent flag was used, does that agentId exist?
openclaw agents list | grep <agentId>
```

**Fix for stuck job with backoff:**
```bash
openclaw cron run <jobId>   # Force immediate run
```

---

### WRONG AGENT RESPONDING

**Root cause**: Binding order. More-specific bindings must come BEFORE less-specific ones.

**Priority order** (highest to lowest):
```
1. peer (exact DM/group ID)
2. parentPeer (thread)
3. guildId + roles (Discord)
4. guildId (Discord)
5. teamId (Slack)
6. accountId
7. channel (no accountId)
8. fallback (default agent)
```

**Diagnosis:**
```bash
openclaw agents list --bindings
# Review binding order — is the more-specific rule ABOVE the less-specific?
```

**Common mistake:**
```json5
// WRONG — channel-wide rule catches everything before peer rule
bindings: [
  { agentId: "apex", match: { channel: "whatsapp" } },           // catches all WhatsApp
  { agentId: "sentinel", match: { channel: "whatsapp",
    peer: { kind: "direct", id: "+27XXXXXXXXX" } } },             // never reached
]

// CORRECT — peer rule first
bindings: [
  { agentId: "sentinel", match: { channel: "whatsapp",
    peer: { kind: "direct", id: "+27XXXXXXXXX" } } },             // specific → first
  { agentId: "apex", match: { channel: "whatsapp" } },            // catch-all → last
]
```

---

### GATEWAY WON'T START

**Step 1:**
```bash
openclaw doctor
# Read every error — schema violations stop the Gateway cold
```

**Common config errors:**

| Error | Fix |
|---|---|
| Unknown key in config | Remove the unrecognised field — strict schema validation |
| `refusing to bind gateway ... without auth` | Non-loopback bind needs `gateway.auth.token` |
| `EADDRINUSE` / port conflict | Another Gateway running: `openclaw gateway stop` then restart |
| `Gateway start blocked: set gateway.mode=local` | Config set to remote mode when running locally |
| Model string format wrong | Use `provider/model` format: `anthropic/claude-sonnet-4-6` |
| `agentDir` collision | Two agents sharing same `agentDir` — give each a unique path |

**Step 2:** After fixing, validate:
```bash
openclaw doctor --fix     # auto-repair where possible
openclaw gateway status   # confirm running
```

---

### CHANNEL DISCONNECTED

**WhatsApp:**
```bash
openclaw channels status --probe
# If offline: re-link the account
openclaw channels login --channel whatsapp --account personal
```

**Telegram:**
```bash
# If offline: verify bot token is still valid
# Check: channels.telegram.accounts.default.botToken
# Env var: TELEGRAM_BOT_TOKEN
openclaw logs --follow  # Watch for "bot token invalid" errors
```

**Discord:**
```bash
# Check bot token, guild invite, Message Content Intent enabled
openclaw logs --follow  # Watch for Discord-specific errors
```

---

### MODEL ERRORS

**Check 1: Model string format**
```json5
// Must be: "provider/model"
// Common mistakes:
"claude-opus-4-6"                      // WRONG — missing provider prefix
"claude-opus-4-20250514"               // WRONG — old model string format
"anthropic/claude-opus-4-6"            // CORRECT
"anthropic/claude-sonnet-4-6"          // CORRECT
"anthropic/claude-haiku-4-5-20251001"  // CORRECT
```

**Check 2: API key present**
```bash
# Anthropic key should be in environment or ~/.openclaw/.env
echo $ANTHROPIC_API_KEY  # should not be empty
cat ~/.openclaw/.env     # check if key is there
```

**Check 3: Rate limits**
```bash
openclaw logs --follow  # Look for "429" or "overloaded" errors
# Cron jobs have exponential backoff for rate limits — wait and retry
```

---

### MEMORY NOT WRITING

**Check 1: Workspace is writable**
```bash
ls -la ~/.openclaw/workspace-[agentid]/
# Check permissions — should not be 444 on .md files other than SOUL/IDENTITY
```

**Check 2: Correct workspace path**
```bash
openclaw config get agents.list  # check workspace path for the agent
ls ~/.openclaw/workspace-[agentid]/  # does this directory exist?
```

**Check 3: Session type**
```
// MEMORY.md only loads in main/private sessions, NOT group contexts
// If agent is running in a group chat, MEMORY.md is intentionally excluded
```

**Check 4: Compaction memory flush disabled**
```json5
// Is memoryFlush.enabled: true?
agents.defaults.compaction.memoryFlush.enabled = true
```

---

## Stage 4: Fix Output Format

After diagnosis, produce the fix in this format:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DIAGNOSIS: [Agent/Feature] — [Root Cause]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ROOT CAUSE:
[Clear explanation of what's wrong and why]

FIX:
[Exact commands or file changes — copy-paste ready]

VERIFY:
[Command to confirm the fix worked]

PREVENT:
[One sentence on how to avoid this happening again]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Gateway Recovery (Emergency)

If Gateway is completely unresponsive:

```bash
# 1. Check if it's running
openclaw gateway status

# 2. Force stop and restart
openclaw gateway stop
openclaw gateway restart

# 3. If that fails, kill the process directly
pkill -f openclaw
openclaw gateway --port 18789

# 4. Check logs for why it crashed
openclaw logs --follow

# 5. If config is corrupted, validate
openclaw doctor

# 6. Nuclear option — reset to minimal config
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak
# Restore a git-backed version:
cd ~/.openclaw && git log --oneline  # find last good commit
git checkout <commit-hash> -- openclaw.json
openclaw gateway restart
```

---

## Quick Reference: All Diagnostic Commands

```bash
openclaw gateway status           # Gateway health
openclaw gateway status --deep    # Detailed health
openclaw doctor                   # Config validation + known issues
openclaw doctor --fix             # Auto-repair
openclaw channels status --probe  # Channel connectivity
openclaw agents list --bindings   # Agent routing state
openclaw cron list                # All cron jobs
openclaw cron runs --id <id>      # Cron run history
openclaw logs --follow            # Live log stream
openclaw sessions                 # Active sessions
openclaw config get <key>         # Read specific config value
openclaw config set <key> <val>   # Set specific config value
openclaw system event --text "x"  # Manual heartbeat trigger
openclaw cron run <id>            # Force cron job run
```
